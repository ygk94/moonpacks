//! Trésorerie : retrait des recettes par l'owner, avec garde-fous.
//!
//! Seul ce qui dépasse les engagements est retirable :
//!
//! ```text
//! retirable = solde − (stockage occupé + dépôts d'annonces + packs non tirés
//!                      + valeur des brûlables vivantes + réserve minimale)
//! ```
//!
//! - **stockage occupé** : `env::storage_usage()` × 10¹⁹ (tout l'état, stockage payé par les
//!   acheteurs, l'owner ou le contrat ; le protocole l'exige de toute façon) ;
//! - **dépôts d'annonces** : `listing_deposits`, rendus aux vendeurs ;
//! - **packs non tirés** : `pack_escrow`, prix et stockage prépayé non encore utilisé des packs
//!   `Pending` et `Stuck` (rendus au tirage ou par `refund_stuck_pack`) ;
//! - **valeur des brûlables vivantes** : `value_reserved`, la part de valeur tirée (yoctoNEAR) des
//!   cartes non brûlées d'une série à table de valeur ;
//! - **réserve minimale** : `TREASURY_MIN_RESERVE` (1 NEAR).
//!
//! Le reste est fait des recettes (`revenue`) et des excédents (récompenses de gaz du contrat,
//! virements reçus, remboursements revenus d'un compte supprimé).

use crate::*;
use near_sdk::serde_json::{json, Value};

/// Décomposition des engagements (yoctoNEAR).
pub(crate) struct Treasury {
    pub balance: u128,
    pub storage_bytes: u64,
    pub storage_locked: u128,
    pub committed: u128,
    pub withdrawable: u128,
}

#[near]
impl Contract {
    /// Solde, engagements et montant retirable (yoctoNEAR, en chaînes).
    pub fn get_treasury(&self) -> Value {
        let t = self.treasury();
        json!({
            "balance": U128(t.balance),
            "storage_bytes": t.storage_bytes,
            "storage_locked": U128(t.storage_locked),
            "listing_deposits": U128(self.listing_deposits),
            "pack_escrow": U128(self.pack_escrow),
            "value_reserved": U128(self.value_reserved),
            "min_reserve": U128(TREASURY_MIN_RESERVE.as_yoctonear()),
            "committed": U128(t.committed),
            "withdrawable": U128(t.withdrawable),
            "revenue": U128(self.revenue),
            "withdrawn": U128(self.withdrawn),
        })
    }

    /// Retire `amount` yoctoNEAR (tout le retirable si absent) vers l'owner. Owner seulement,
    /// 1 yoctoNEAR exactement. Refusé au-delà du retirable (`get_treasury().withdrawable`) :
    /// le solde ne descend jamais sous les engagements plus la réserve. Événement
    /// `revenue_withdrawn`. Renvoie le montant retiré.
    #[payable]
    pub fn withdraw_revenue(&mut self, amount: Option<U128>) -> U128 {
        crate::assert_one_yocto();
        self.assert_owner();
        let t = self.treasury();
        let amount = amount.map(|a| a.0).unwrap_or(t.withdrawable);
        require!(amount > 0, "E_NOTHING_TO_WITHDRAW: Rien à retirer");
        require!(
            amount <= t.withdrawable,
            format!("E_WITHDRAW_LIMIT: Retrait refusé : {} yoctoNEAR demandés, {} retirables (engagements {})", amount, t.withdrawable, t.committed)
        );
        self.withdrawn += amount;
        events::emit(
            "revenue_withdrawn",
            json!({
                "amount": U128(amount), "to": self.owner_id,
                "balance_before": U128(t.balance), "committed": U128(t.committed),
                "withdrawable_before": U128(t.withdrawable), "withdrawn_total": U128(self.withdrawn),
                "revenue": U128(self.revenue), "block_height": env::block_height(),
            }),
        );
        Self::refund(&self.owner_id, amount);
        U128(amount)
    }
}

impl Contract {
    pub(crate) fn treasury(&self) -> Treasury {
        let balance = env::account_balance().as_yoctonear();
        let storage_bytes = env::storage_usage();
        let storage_locked = env::storage_byte_cost().as_yoctonear() * storage_bytes as u128;
        let committed = storage_locked
            .saturating_add(self.listing_deposits)
            .saturating_add(self.pack_escrow)
            .saturating_add(self.value_reserved)
            .saturating_add(TREASURY_MIN_RESERVE.as_yoctonear());
        Treasury { balance, storage_bytes, storage_locked, committed, withdrawable: balance.saturating_sub(committed) }
    }
}
