//! Oracle de prix factice pour les tests (résurrection des coins morts).
//!
//! Un vrai oracle (voir `docs/mechanics.md`, « Résurrection ») lirait un cours fiable,
//! constaterait qu'un coin « mort » repasse au-dessus de son seuil, s'assurerait que le stock de
//! jetons est acheté, puis appellerait `set_resurrected`. Ici, l'opérateur du mock pousse
//! directement la décision : aucun prix n'est lu.

use near_sdk::json_types::U128;
use near_sdk::serde_json::json;
use near_sdk::{env, near, require, AccountId, Gas, NearToken, PanicOnDefault, Promise};

#[near(contract_state)]
#[derive(PanicOnDefault)]
pub struct MockOracle {
    memaster: AccountId,
    operator: AccountId,
}

#[near]
impl MockOracle {
    #[init]
    pub fn new(memaster: AccountId, operator: AccountId) -> Self {
        Self { memaster, operator }
    }

    /// Déclare la résurrection d'une carte : appelle `memaster.set_resurrected` avec le dépôt joint
    /// (stockage, excédent rendu à l'oracle).
    #[payable]
    pub fn push_resurrection(&mut self, series_id: u32, card_index: u32, asset_id: String, amount: U128) -> Promise {
        require!(env::predecessor_account_id() == self.operator, "opérateur seulement");
        Promise::new(self.memaster.clone()).function_call(
            "set_resurrected".to_string(),
            json!({
                "series_id": series_id, "card_index": card_index,
                "backing": { "asset_id": asset_id, "amount": amount },
            })
            .to_string()
            .into_bytes(),
            env::attached_deposit().max(NearToken::from_millinear(10)),
            Gas::from_tgas(20),
        )
    }
}
