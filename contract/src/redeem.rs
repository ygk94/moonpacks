//! Burn en deux temps via un `redeemer` abstrait.
//!
//! 1. `redeem(token_id)` : la carte passe en `Redeeming` (transfert, vente et nouveau burn refusés),
//!    puis appel `redeemer.redeem(owner, asset_id, amount)` à gaz fixe ;
//! 2. `on_redeem_complete` : succès du reçu → `nft_burn` et suppression de l'adossement ;
//!    échec → retour à `Normal`.
//!
//! Contrat d'interface : le redeemer **panique** s'il ne livre pas ; tout retour sans panique vaut succès.

use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::events::NftBurn;
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
    fn on_redeem_complete(&mut self, token_id: TokenId, owner: AccountId);
}

#[near]
impl Contract {
    /// Brûle une carte adossée contre ses jetons. 1 yoctoNEAR exactement ; gaz ≥ 70 Tgas.
    #[payable]
    pub fn redeem(&mut self, token_id: TokenId) -> Promise {
        near_sdk::assert_one_yocto();
        require!(env::prepaid_gas() >= MIN_REDEEM_GAS, "Gaz insuffisant pour le burn");
        let owner = env::predecessor_account_id();
        let token_owner =
            self.tokens.owner_by_id.get(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        require!(token_owner == owner, "Seul le propriétaire peut brûler");
        require!(self.listings.get(&token_id).is_none(), "Carte en vente : retirez l'annonce d'abord");
        let redeemer = self.redeemer_id.clone().unwrap_or_else(|| env::panic_str("Aucun redeemer configuré"));
        let backing =
            self.backing.get(&token_id).cloned().unwrap_or_else(|| env::panic_str("Carte non brûlable"));
        let info = self.cards.get_mut(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        require!(info.state == CardState::Normal, "Burn déjà en cours");
        info.state = CardState::Redeeming;

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
            .redeem(owner.clone(), backing.asset_id, backing.amount)
            .then(
                ext_self::ext(env::current_account_id())
                    .with_static_gas(REDEEM_CALLBACK_GAS)
                    .with_unused_gas_weight(0)
                    .on_redeem_complete(token_id, owner),
            )
    }

    /// Callback du burn. Ne panique pas : finalise ou restaure.
    #[private]
    pub fn on_redeem_complete(
        &mut self,
        token_id: TokenId,
        owner: AccountId,
    ) -> bool {
        // Tout reçu réussi vaut succès, quelle que soit la valeur renvoyée.
        let ok = env::promise_results_count() == 1
            && matches!(env::promise_result_checked(0, 1024), Ok(_) | Err(PromiseError::TooLong(_)));
        let Some(info) = self.cards.get_mut(&token_id) else {
            env::log_str("on_redeem_complete: carte inconnue");
            return false;
        };
        if info.state != CardState::Redeeming {
            env::log_str("on_redeem_complete: carte pas en burn");
            return false;
        }
        if !ok {
            info.state = CardState::Normal;
            events::emit("redeem_failed", json!({ "token_id": token_id, "owner_id": owner }));
            return false;
        }
        let backing = self.backing.remove(&token_id);
        self.cards.remove(&token_id);
        self.internal_burn(&token_id, &owner);
        events::emit(
            "card_redeemed",
            json!({
                "token_id": token_id, "owner_id": owner,
                "asset_id": backing.as_ref().map(|b| b.asset_id.clone()),
                "amount": backing.map(|b| b.amount),
            }),
        );
        true
    }
}

impl Contract {
    /// Supprime la carte des structures NEP-171/177/178/181 et émet `nft_burn`.
    pub(crate) fn internal_burn(&mut self, token_id: &TokenId, owner: &AccountId) {
        self.tokens.owner_by_id.remove(token_id);
        if let Some(m) = self.tokens.token_metadata_by_id.as_mut() {
            m.remove(token_id);
        }
        if let Some(per_owner) = self.tokens.tokens_per_owner.as_mut() {
            if let Some(mut set) = per_owner.get(owner) {
                set.remove(token_id);
                if set.is_empty() {
                    per_owner.remove(owner);
                } else {
                    per_owner.insert(owner, &set);
                }
            }
        }
        if let Some(a) = self.tokens.approvals_by_id.as_mut() {
            let removed = a.remove(token_id);
            crate::nft::refund_approvals(owner, removed.as_ref());
        }
        if let Some(n) = self.tokens.next_approval_id_by_id.as_mut() {
            n.remove(token_id);
        }
        NftBurn { owner_id: owner, token_ids: &[token_id], authorized_id: None, memo: Some("redeem") }.emit();
    }
}
