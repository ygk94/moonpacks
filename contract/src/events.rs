//! Événements NEP-297. Les événements NEP-171 (`nft_mint`, `nft_transfer`, `nft_burn`)
//! viennent de near-contract-standards ; `nft_metadata_update` (NEP-171 1.2.0) est émis ici.

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

/// NEP-171 v1.2.0 : `nft_metadata_update`.
pub fn emit_nft_metadata_update(token_ids: &[String]) {
    let log = json!({
        "standard": "nep171",
        "version": "1.2.0",
        "event": "nft_metadata_update",
        "data": [{ "token_ids": token_ids }],
    });
    env::log_str(&format!("EVENT_JSON:{}", log));
}
