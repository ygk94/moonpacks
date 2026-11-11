//! Redeemer factice pour les tests : enregistre les demandes `redeem(owner, asset_id, amount)`.
//! Panique (= échec côté Memaster, la carte est restaurée) si `fail` est actif ou si
//! l'actif figure dans `failing_assets`. N'accepte que le contrat Memaster configuré.
//! Sert aussi de receveur `nft_on_transfer` pour les tests de `nft_transfer_call`.

use near_sdk::json_types::U128;
use near_sdk::{env, near, require, AccountId, PanicOnDefault};

#[near(serializers = [json, borsh])]
#[derive(Clone)]
pub struct Redemption {
    pub owner: AccountId,
    pub asset_id: String,
    pub amount: U128,
    pub block_height: u64,
}

#[near(contract_state)]
#[derive(PanicOnDefault)]
pub struct MockRedeemer {
    memaster: AccountId,
    fail: bool,
    failing_assets: Vec<String>,
    redemptions: Vec<Redemption>,
}

#[near]
impl MockRedeemer {
    #[init]
    pub fn new(memaster: AccountId) -> Self {
        Self { memaster, fail: false, failing_assets: vec![], redemptions: vec![] }
    }

    pub fn set_fail(&mut self, fail: bool) {
        self.fail = fail;
    }

    pub fn set_failing_assets(&mut self, assets: Vec<String>) {
        self.failing_assets = assets;
    }

    pub fn redeem(&mut self, owner: AccountId, asset_id: String, amount: U128) -> bool {
        require!(env::predecessor_account_id() == self.memaster, "appelant non autorisé");
        if self.fail || self.failing_assets.contains(&asset_id) {
            env::panic_str("mock: livraison impossible");
        }
        self.redemptions.push(Redemption { owner, asset_id, amount, block_height: env::block_height() });
        true
    }

    /// Receveur NEP-171 factice : `msg` = "return" rend la carte, "panic" panique, sinon la garde.
    #[allow(unused_variables)]
    pub fn nft_on_transfer(
        &mut self,
        sender_id: AccountId,
        previous_owner_id: AccountId,
        token_id: String,
        msg: String,
    ) -> bool {
        match msg.as_str() {
            "return" => true,
            "panic" => env::panic_str("mock: receveur en échec"),
            _ => false,
        }
    }

    pub fn get_redemptions(&self) -> Vec<Redemption> {
        self.redemptions.clone()
    }
}
