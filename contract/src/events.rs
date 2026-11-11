//! Événements NEP-297. Les événements NEP-171 (`nft_mint`, `nft_transfer`, `nft_burn`)
//! sont émis par `nft.rs`. Plus de `nft_metadata_update` : les métadonnées d'une mythique restent
//! anonymes après sa révélation, aucune ne change.

use near_sdk::env;
use near_sdk::serde_json::{json, Value};

pub const STANDARD: &str = "memaster";
pub const VERSION: &str = "1.0.0";

pub fn emit(event: &str, data: Value) {
    let log = json!({
        "standard": STANDARD,
        "version": VERSION,
        "event": event,
        "data": [data],
    });
    env::log_str(&format!("EVENT_JSON:{}", log));
}
