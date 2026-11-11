//! Burn en deux temps via un `redeemer` abstrait.
//!
//! 1. `redeem(token_id)` : la carte passe en `Redeeming` (transfert, vente et nouveau burn refusés),
//!    puis appel `redeemer.redeem(owner, asset_id, amount)` à gaz fixe ;
//! 2. `on_redeem_complete` : succès du reçu → `nft_burn`, suppression de l'adossement et
//!    remboursement au propriétaire du stockage libéré (mesuré) ; échec → retour à `Normal`. L'adossement envoyé au redeemer est passé en argument au callback
//!    et c'est lui que `card_redeemed` journalise : un remplacement par l'oracle pendant le burn
//!    (carte ressuscitée) ne change pas ce qui a été livré.
//!
//! Série à table de valeur : `amount` est la part de la valeur tirée pour le pack (yoctoNEAR de
//! valeur, `draw::split_value`), pas le montant de la table ; le redeemer, abstrait, la convertit.
//!
//! Contrat d'interface : le redeemer **panique** s'il ne livre pas ; tout retour sans panique vaut succès.

use crate::types::*;
use crate::*;
use near_sdk::serde_json::json;
use near_sdk::{ext_contract, Promise, PromiseError};

#[allow(dead_code)]
#[ext_contract(ext_redeemer)]
pub trait Redeemer {
    fn redeem(&mut self, owner: AccountId, asset_id: String, amount: U128);
}

#[allow(dead_code)]
#[ext_contract(ext_self)]
pub trait SelfCallbacks {
    fn on_redeem_complete(&mut self, token_id: TokenId, owner: AccountId, backing: Backing);
}

#[near]
impl Contract {
    /// Brûle une carte adossée contre ses jetons. 1 yoctoNEAR exactement ; gaz ≥ 70 Tgas.
    #[payable]
    pub fn redeem(&mut self, token_id: TokenId) -> Promise {
        near_sdk::assert_one_yocto();
        require!(env::prepaid_gas() >= MIN_REDEEM_GAS, "Gaz insuffisant pour le burn");
        let owner = env::predecessor_account_id();
        let token_owner = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        require!(token_owner == owner, "Seul le propriétaire peut brûler");
        require!(self.listings.get(&token_id).is_none(), "Carte en vente : retirez l'annonce d'abord");
        let redeemer = self.redeemer_id.clone().unwrap_or_else(|| env::panic_str("Aucun redeemer configuré"));
        let backing = self.token_backing(&token_id).unwrap_or_else(|| env::panic_str("Carte non brûlable"));
        let slot = self.slot_mut_by_id(&token_id);
        require!(slot.state == CardState::Normal, "Burn déjà en cours");
        slot.state = CardState::Redeeming;

        events::emit(
            "redeem_started",
            json!({
                "token_id": token_id, "owner_id": owner, "redeemer_id": redeemer,
                "asset_id": backing.asset_id, "amount": backing.amount,
            }),
        );
        ext_redeemer::ext(redeemer)
            .with_static_gas(REDEEMER_GAS)
            .with_unused_gas_weight(0)
            .redeem(owner.clone(), backing.asset_id.clone(), backing.amount)
            .then(
                ext_self::ext(env::current_account_id())
                    .with_static_gas(REDEEM_CALLBACK_GAS)
                    .with_unused_gas_weight(0)
                    .on_redeem_complete(token_id, owner, backing),
            )
    }

    /// Callback du burn. Ne panique pas : finalise ou restaure. `backing` = adossement envoyé au
    /// redeemer par `redeem` (journalisé tel quel, même si l'oracle l'a remplacé entre-temps).
    #[private]
    pub fn on_redeem_complete(
        &mut self,
        token_id: TokenId,
        owner: AccountId,
        backing: Backing,
    ) -> bool {
        // Tout reçu réussi vaut succès, quelle que soit la valeur renvoyée.
        let ok = env::promise_results_count() == 1
            && matches!(env::promise_result_checked(0, 1024), Ok(_) | Err(PromiseError::TooLong(_)));
        let Some((_, slot, pack)) = self.live(&token_id) else {
            env::log_str("on_redeem_complete: carte inconnue");
            return false;
        };
        if pack.cards[slot].state != CardState::Redeeming {
            env::log_str("on_redeem_complete: carte pas en burn");
            return false;
        }
        let (series_id, d) = (pack.series_id, pack.draws[slot]);
        if !ok {
            self.slot_mut_by_id(&token_id).state = CardState::Normal;
            events::emit("redeem_failed", json!({ "token_id": token_id, "owner_id": owner }));
            return false;
        }
        // Adossement courant de l'exemplaire (part de la valeur du pack comprise).
        let current = self.token_backing(&token_id);
        let value_share = self.slot_value(pack, slot).unwrap_or(0);
        let start = env::storage_usage();
        let approvals_refund = self.internal_burn(&token_id, &owner);
        // Rareté pilotée par les burns : compteur de la carte et numéro d'ordre du burn.
        let burn_seq = self.record_burn(series_id, d.kind, d.index);
        self.value_reserved = self.value_reserved.saturating_sub(value_share);
        // Stockage libéré par le burn (entrées des listes NEP-181, blocs et compteurs vidés,
        // approbations, propriétaire de l'emplacement), mesuré : rendu au propriétaire, moins ce qui
        // l'a déjà été pour les approbations. Jamais plus que les octets libérés. L'emplacement du
        // pack (`CardSlot`, `PackDraw`) reste : `token_id` = pack × 10 + emplacement, et la part de
        // valeur des autres cartes du pack se recalcule depuis tous les tirages du pack.
        let freed = self.storage_freed_since(start);
        let storage_refund =
            (env::storage_byte_cost().as_yoctonear() * freed as u128).saturating_sub(approvals_refund);
        Self::refund(&owner, storage_refund);
        events::emit(
            "card_redeemed",
            json!({
                "token_id": token_id, "owner_id": owner,
                // Adossement livré par le redeemer (celui du lancement du burn).
                "asset_id": backing.asset_id, "amount": backing.amount,
                // Adossement courant s'il a changé pendant le burn (remplacement par l'oracle).
                "replaced_by": current.filter(|c| *c != backing),
                "series_id": series_id, "kind": d.kind, "index": d.index,
                "burn_seq": burn_seq,
                // Stockage rendu au propriétaire (octets libérés mesurés, approbations comprises).
                "freed_bytes": freed, "storage_refund": U128(storage_refund + approvals_refund),
            }),
        );
        true
    }
}
