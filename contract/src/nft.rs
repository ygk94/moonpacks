//! NEP-171 (cœur), 177 (métadonnées), 178 (approbations), 181 (énumération), 199 (payouts).
//! Toute sortie d'une carte passe par `before_transfer` : refus en `Redeeming`, retrait de l'annonce.

use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::approval::NonFungibleTokenApproval;
use near_contract_standards::non_fungible_token::core::{
    NonFungibleTokenCore, NonFungibleTokenResolver,
};
use near_contract_standards::non_fungible_token::enumeration::NonFungibleTokenEnumeration;
use near_contract_standards::non_fungible_token::metadata::NonFungibleTokenMetadataProvider;
use near_contract_standards::non_fungible_token::core::{ext_nft_receiver, ext_nft_resolver};
use near_contract_standards::non_fungible_token::events::NftTransfer;
use near_contract_standards::non_fungible_token::{refund_approved_account_ids, Token};
use near_sdk::{Promise, PromiseOrValue};
use std::collections::HashMap;

/// Gaz fixe de `nft_resolve_transfer` (le standard n'en donne que 5 Tgas ; mesuré : voir README).
pub const GAS_FOR_RESOLVE_TRANSFER: Gas = Gas::from_tgas(15);
/// Gaz minimal pour `nft_transfer_call` : propre exécution + receveur + résolution.
pub const MIN_GAS_FOR_NFT_TRANSFER_CALL: Gas = Gas::from_tgas(45);

/// Rend au propriétaire le stockage de ses approbations effacées, comme le standard.
pub(crate) fn refund_approvals(owner: &AccountId, approvals: Option<&HashMap<AccountId, u64>>) {
    if let Some(a) = approvals {
        if !a.is_empty() {
            refund_approved_account_ids(owner.clone(), a).detach();
        }
    }
}

impl Contract {
    pub(crate) fn before_transfer(&mut self, token_id: &TokenId) {
        if let Some(info) = self.cards.get(token_id) {
            require!(info.state == CardState::Normal, "Carte en cours de burn : transfert refusé");
        }
        self.remove_listing(token_id, "transferred");
    }

    /// Payout NEP-199 : redevances de la série, le reste au propriétaire.
    pub(crate) fn compute_payout(
        &self,
        token_id: &TokenId,
        owner: &AccountId,
        balance: u128,
        max_len_payout: Option<u32>,
    ) -> Payout {
        let royalties = self
            .cards
            .get(token_id)
            .map(|c| self.series_ref(c.series_id).table.royalties.clone())
            .unwrap_or_default();
        let mut payout: HashMap<AccountId, U128> = HashMap::new();
        let mut paid: u128 = 0;
        for r in royalties.iter() {
            let amount = balance * r.bps as u128 / 10_000;
            paid += amount;
            let e = payout.entry(r.account_id.clone()).or_insert(U128(0));
            e.0 += amount;
        }
        let e = payout.entry(owner.clone()).or_insert(U128(0));
        e.0 += balance - paid;
        if let Some(max) = max_len_payout {
            require!(payout.len() as u32 <= max, "Payout trop long pour max_len_payout");
        }
        Payout { payout }
    }
}

#[near]
impl NonFungibleTokenCore for Contract {
    #[payable]
    fn nft_transfer(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
    ) {
        near_sdk::assert_one_yocto();
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, approvals) =
            self.tokens.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        refund_approvals(&old_owner, approvals.as_ref());
    }

    #[payable]
    fn nft_transfer_call(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
        msg: String,
    ) -> PromiseOrValue<bool> {
        near_sdk::assert_one_yocto();
        require!(env::prepaid_gas() >= MIN_GAS_FOR_NFT_TRANSFER_CALL, "Gaz insuffisant pour nft_transfer_call");
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, old_approvals) =
            self.tokens.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        // Comme le standard, mais avec une résolution à 15 Tgas fixes au lieu de 5.
        ext_nft_receiver::ext(receiver_id.clone())
            .with_unused_gas_weight(1)
            .nft_on_transfer(sender, old_owner.clone(), token_id.clone(), msg)
            .then(
                ext_nft_resolver::ext(env::current_account_id())
                    .with_static_gas(GAS_FOR_RESOLVE_TRANSFER)
                    .with_unused_gas_weight(0)
                    .nft_resolve_transfer(old_owner, receiver_id, token_id, old_approvals),
            )
            .into()
    }

    fn nft_token(&self, token_id: TokenId) -> Option<Token> {
        self.tokens.nft_token(token_id)
    }
}

#[near]
impl NonFungibleTokenResolver for Contract {
    #[private]
    fn nft_resolve_transfer(
        &mut self,
        previous_owner_id: AccountId,
        receiver_id: AccountId,
        token_id: TokenId,
        approved_account_ids: Option<HashMap<AccountId, u64>>,
    ) -> bool {
        // Réécrit (au lieu de déléguer au standard) pour rester léger et gérer
        // le burn, l'annonce et le remboursement des approbations.
        let must_revert = env::promise_result_checked(0, "false".len())
            .ok()
            .and_then(|v| near_sdk::serde_json::from_slice::<bool>(&v).ok())
            .unwrap_or(true);
        let current = self.tokens.owner_by_id.get(&token_id);
        let keep = !must_revert
            || current.as_ref() != Some(&receiver_id)
            || self.cards.get(&token_id).is_some_and(|c| c.state == CardState::Redeeming);
        if keep {
            // Le destinataire garde la carte (ou elle a déjà bougé, ou elle est brûlée / en burn) :
            // l'annonce éventuelle n'est pas touchée ; les approbations du précédent propriétaire
            // sont effacées, leur stockage lui est rendu.
            refund_approvals(&previous_owner_id, approved_account_ids.as_ref());
            return true;
        }
        // Retour réel au précédent propriétaire : seule une annonce posée entre-temps par le
        // destinataire est retirée.
        if self.listings.get(&token_id).is_some() {
            self.remove_listing(&token_id, "transfer_reverted");
        }
        self.tokens.internal_transfer_unguarded(&token_id, &receiver_id, &previous_owner_id);
        if let Some(by_id) = self.tokens.approvals_by_id.as_mut() {
            if let Some(receiver_approvals) = by_id.remove(&token_id) {
                refund_approvals(&receiver_id, Some(&receiver_approvals));
            }
            if let Some(prev) = approved_account_ids {
                by_id.insert(&token_id, &prev);
            }
        }
        NftTransfer {
            old_owner_id: &receiver_id,
            new_owner_id: &previous_owner_id,
            token_ids: &[&token_id],
            authorized_id: None,
            memo: None,
        }
        .emit();
        false
    }
}

#[near]
impl NonFungibleTokenApproval for Contract {
    #[payable]
    fn nft_approve(&mut self, token_id: TokenId, account_id: AccountId, msg: Option<String>) -> Option<Promise> {
        self.tokens.nft_approve(token_id, account_id, msg)
    }

    #[payable]
    fn nft_revoke(&mut self, token_id: TokenId, account_id: AccountId) {
        self.tokens.nft_revoke(token_id, account_id)
    }

    #[payable]
    fn nft_revoke_all(&mut self, token_id: TokenId) {
        self.tokens.nft_revoke_all(token_id)
    }

    fn nft_is_approved(&self, token_id: TokenId, approved_account_id: AccountId, approval_id: Option<u64>) -> bool {
        self.tokens.nft_is_approved(token_id, approved_account_id, approval_id)
    }
}

#[near]
impl NonFungibleTokenEnumeration for Contract {
    fn nft_total_supply(&self) -> U128 {
        self.tokens.nft_total_supply()
    }

    fn nft_tokens(&self, from_index: Option<U128>, limit: Option<u64>) -> Vec<Token> {
        self.tokens.nft_tokens(from_index, limit)
    }

    fn nft_supply_for_owner(&self, account_id: AccountId) -> U128 {
        self.tokens.nft_supply_for_owner(account_id)
    }

    fn nft_tokens_for_owner(&self, account_id: AccountId, from_index: Option<U128>, limit: Option<u64>) -> Vec<Token> {
        self.tokens.nft_tokens_for_owner(account_id, from_index, limit)
    }
}

#[near]
impl NonFungibleTokenMetadataProvider for Contract {
    fn nft_metadata(&self) -> NFTContractMetadata {
        self.metadata.clone()
    }
}

#[near]
impl Contract {
    /// NEP-199 : répartition d'un montant `balance` pour cette carte.
    pub fn nft_payout(&self, token_id: TokenId, balance: U128, max_len_payout: Option<u32>) -> Payout {
        let owner = self.tokens.owner_by_id.get(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        self.compute_payout(&token_id, &owner, balance.0, max_len_payout)
    }

    /// NEP-199 : transfert + répartition (pour marchés externes approuvés).
    #[payable]
    pub fn nft_transfer_payout(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
        balance: U128,
        max_len_payout: Option<u32>,
    ) -> Payout {
        near_sdk::assert_one_yocto();
        let owner = self.tokens.owner_by_id.get(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        let payout = self.compute_payout(&token_id, &owner, balance.0, max_len_payout);
        self.before_transfer(&token_id);
        let sender = env::predecessor_account_id();
        let (old_owner, approvals) =
            self.tokens.internal_transfer(&sender, &receiver_id, &token_id, approval_id, memo);
        refund_approvals(&old_owner, approvals.as_ref());
        payout
    }
}
