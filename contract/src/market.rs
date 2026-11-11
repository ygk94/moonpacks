//! Marché intégré : `list`, `delist`, `buy` dans le même contrat et le même reçu.
//! Interdit sur une carte en `Redeeming`. Un transfert ou un burn retire l'annonce.

use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::events::NftTransfer;
use near_sdk::serde_json::json;

#[near]
impl Contract {
    /// Met une carte en vente. Dépôt ≥ `LISTING_DEPOSIT` (rendu au retrait ou à la vente).
    #[payable]
    pub fn list(&mut self, token_id: TokenId, price: U128) {
        let seller = env::predecessor_account_id();
        let owner = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        require!(owner == seller, "Seul le propriétaire peut vendre");
        require!(self.card_state(&token_id) == CardState::Normal, "Carte en cours de burn");
        require!(price.0 > 0, "Prix nul");
        require!(self.listings.get(&token_id).is_none(), "Déjà en vente");
        let deposit = env::attached_deposit().as_yoctonear();
        let need = LISTING_DEPOSIT.as_yoctonear();
        require!(deposit >= need, format!("Dépôt d'annonce : {} yoctoNEAR requis", need));
        self.listings.insert(token_id.clone(), Listing { seller_id: seller.clone(), price, deposit: U128(need) });
        events::emit("card_listed", json!({ "token_id": token_id, "seller_id": seller, "price": price }));
        Self::refund(&seller, deposit - need);
    }

    /// Retire une annonce (propriétaire seulement).
    pub fn delist(&mut self, token_id: TokenId) {
        let l = self.listings.get(&token_id).cloned().unwrap_or_else(|| env::panic_str("Pas en vente"));
        require!(env::predecessor_account_id() == l.seller_id, "Seul le vendeur peut retirer l'annonce");
        require!(self.card_state(&token_id) == CardState::Normal, "Carte en cours de burn");
        self.remove_listing(&token_id, "delisted");
    }

    /// Achète une carte en vente au prix `expected_price` (protège contre une remise en vente
    /// plus chère juste avant l'achat). Dépôt ≥ prix ; l'excédent est rendu.
    /// Le vendeur reçoit le prix moins les redevances de la série (NEP-199), plus son dépôt d'annonce.
    #[payable]
    pub fn buy(&mut self, token_id: TokenId, expected_price: U128) {
        let buyer = env::predecessor_account_id();
        let l = self.listings.get(&token_id).cloned().unwrap_or_else(|| env::panic_str("Pas en vente"));
        require!(l.price == expected_price, "Le prix de l'annonce a changé");
        require!(self.card_state(&token_id) == CardState::Normal, "Carte en cours de burn");
        require!(buyer != l.seller_id, "Le vendeur ne peut pas acheter sa carte");
        let owner = self.owner_of(&token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"));
        require!(owner == l.seller_id, "Annonce périmée");
        let deposit = env::attached_deposit().as_yoctonear();
        require!(deposit >= l.price.0, "Dépôt inférieur au prix");

        self.listings.remove(&token_id);
        let removed = self.take_approvals(&token_id);
        crate::nft::refund_approvals(&owner, Some(&removed));
        self.internal_transfer_unguarded(&token_id, &owner, &buyer);
        NftTransfer {
            old_owner_id: &owner,
            new_owner_id: &buyer,
            token_ids: &[&token_id],
            authorized_id: None,
            memo: Some("market"),
        }
        .emit();

        let payout = self.compute_payout(&token_id, &owner, l.price.0, None);
        for (acc, amount) in payout.payout.iter() {
            let extra = if *acc == owner { l.deposit.0 } else { 0 };
            Self::refund(acc, amount.0 + extra);
        }
        if !payout.payout.contains_key(&owner) {
            Self::refund(&owner, l.deposit.0);
        }
        Self::refund(&buyer, deposit - l.price.0);
        events::emit(
            "card_sold",
            json!({ "token_id": token_id, "seller_id": owner, "buyer_id": buyer, "price": l.price }),
        );
    }
}

impl Contract {
    /// Retire l'annonce et rend le dépôt au vendeur.
    pub(crate) fn remove_listing(&mut self, token_id: &TokenId, reason: &str) {
        if let Some(l) = self.listings.remove(token_id) {
            Self::refund(&l.seller_id, l.deposit.0);
            events::emit(
                "card_delisted",
                json!({ "token_id": token_id, "seller_id": l.seller_id, "reason": reason }),
            );
        }
    }
}
