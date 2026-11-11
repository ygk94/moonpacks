//! Memaster : boosters de cartes NFT (NEP-171/177/178/181/199) représentant des memecoins.
//!
//! - séries à table figée et hachée à l'ouverture (`series.rs`) ;
//! - achat en une signature puis tirage sur k reçus privés chaînés (`pack.rs`, `draw.rs`) ;
//! - mythiques secrètes sous engagement, révélées à leur première sortie (`mythic.rs`) ;
//! - marché intégré (`market.rs`) ;
//! - burn en deux temps via un `redeemer` abstrait (`redeem.rs`) ;
//! - interfaces NFT standard (`nft.rs`).

use near_contract_standards::non_fungible_token::metadata::{
    NFTContractMetadata, TokenMetadata, NFT_METADATA_SPEC,
};
use near_contract_standards::non_fungible_token::{NonFungibleToken, TokenId};
use near_sdk::json_types::U128;
use near_sdk::store::{IterableMap, LookupMap, Vector};
use near_sdk::{env, near, require, AccountId, BorshStorageKey, Gas, NearToken, PanicOnDefault};

pub mod draw;
pub mod events;
mod hash_stream;
mod market;
mod mythic;
mod nft;
mod pack;
mod redeem;
mod series;
pub mod types;
mod views;

#[cfg(test)]
mod tests;
#[cfg(test)]
mod tests_batch;

use types::*;

// ---------------------------------------------------------------- gaz
/// Gaz de chaque reçu intermédiaire du tirage (sa propre exécution + création du suivant).
pub const INTERMEDIATE_STEP_GAS: Gas = Gas::from_tgas(10);
/// Gaz du dernier reçu (tirage + création de jusqu'à 10 cartes + journal).
pub const FINAL_STEP_GAS: Gas = Gas::from_tgas(120);
/// Gaz propre de `buy_pack` / `retry_reveal`, hors chaîne de tirage.
pub const ENTRY_OWN_GAS: Gas = Gas::from_tgas(20);
/// Gaz donné au `redeemer`.
pub const REDEEMER_GAS: Gas = Gas::from_tgas(30);
/// Gaz du callback du burn.
pub const REDEEM_CALLBACK_GAS: Gas = Gas::from_tgas(20);
/// Gaz minimal exigé pour `redeem`.
pub const MIN_REDEEM_GAS: Gas = Gas::from_tgas(70);

// ---------------------------------------------------------------- limites
/// Cartes visibles d'une série, tous lots confondus.
pub const MAX_CARDS_PER_SERIES: usize = 2_000;
/// Cartes visibles par appel (`create_series`, `replace_series_table`, `append_series_cards`).
pub const MAX_CARDS_PER_CALL: usize = 200;
/// Cartes par bloc de stockage (`series_cards`). Le tirage lit au plus un bloc par emplacement.
pub const CARDS_PER_CHUNK: u32 = 50;
pub const MAX_MYTHICS_PER_SERIES: usize = 20;
pub const MAX_MYTHIC_CAP: u32 = 100;
pub const MAX_CARDS_PER_PACK: u8 = 10;
pub const MAX_ROYALTIES: usize = 10;
pub const MAX_ROYALTY_BPS: u32 = 5_000;
pub const MAX_ID_LEN: usize = 64;
pub const MAX_TITLE_LEN: usize = 64;
pub const MAX_URL_LEN: usize = 256;
pub const MAX_ASSET_ID_LEN: usize = 128;
pub const MAX_ATTEMPTS: u32 = 10;
pub const MIN_REVEAL_STEPS: u8 = 2;
pub const MAX_REVEAL_STEPS: u8 = 6;

// ---------------------------------------------------------------- stockage (octets)
/// Partie fixe d'un enregistrement de pack (hors graines, tirages, jetons).
pub const PACK_BASE_BYTES: u64 = 400;
/// Une graine journalisée (attempt, step, hauteur, graine, acc).
pub const SEED_RECORD_BYTES: u64 = 100;
/// Entrée de la liste paginée des packs par propriétaire, compteur compris.
pub const OWNER_PACK_LIST_BYTES: u64 = 250;
/// Par carte, en plus des métadonnées et de l'estimation du standard :
/// CardInfo, DrawRecord dans le pack, identifiant dans le pack.
pub const PER_CARD_EXTRA_BYTES: u64 = 300;
/// Entrée du registre d'adossement, hors longueur de `asset_id`.
pub const BACKING_BASE_BYTES: u64 = 120;
/// Dépôt d'une annonce de marché.
pub const LISTING_DEPOSIT: NearToken = NearToken::from_millinear(5);

#[derive(BorshStorageKey)]
#[near]
enum StorageKey {
    NftOwners,
    NftMetadata,
    NftEnumeration,
    NftApprovals,
    Series,
    Packs,
    PacksByOwner,
    PackCountByOwner,
    Cards,
    Backing,
    Listings,
    SeriesCards,
}

#[near(contract_state)]
#[derive(PanicOnDefault)]
pub struct Contract {
    owner_id: AccountId,
    redeemer_id: Option<AccountId>,
    config: Config,
    metadata: NFTContractMetadata,
    tokens: NonFungibleToken,
    series: Vector<Series>,
    /// Cartes visibles des séries, par blocs de `CARDS_PER_CHUNK` : `(series_id, bloc) → cartes`.
    series_cards: LookupMap<(u32, u32), Vec<CardDef>>,
    packs: LookupMap<u64, Pack>,
    packs_by_owner: LookupMap<(AccountId, u32), u64>,
    pack_count_by_owner: LookupMap<AccountId, u32>,
    cards: LookupMap<TokenId, CardInfo>,
    backing: LookupMap<TokenId, Backing>,
    listings: IterableMap<TokenId, Listing>,
    next_pack_id: u64,
    next_token_id: u64,
    /// Total encaissé en prix de boosters (yoctoNEAR). Aucun retrait pour l'instant.
    revenue: u128,
}

#[near]
impl Contract {
    #[init]
    #[private]
    pub fn new(
        owner_id: AccountId,
        redeemer_id: Option<AccountId>,
        metadata: Option<NFTContractMetadata>,
        reveal_steps: Option<u8>,
        retry_delay_blocks: Option<u64>,
    ) -> Self {
        let metadata = metadata.unwrap_or(NFTContractMetadata {
            spec: NFT_METADATA_SPEC.to_string(),
            name: "Memaster".to_string(),
            symbol: "MEME".to_string(),
            icon: None,
            base_uri: None,
            reference: None,
            reference_hash: None,
        });
        metadata.assert_valid();
        let reveal_steps = reveal_steps.unwrap_or(3);
        require!(
            (MIN_REVEAL_STEPS..=MAX_REVEAL_STEPS).contains(&reveal_steps),
            "reveal_steps hors bornes"
        );
        Self {
            owner_id: owner_id.clone(),
            redeemer_id,
            config: Config {
                reveal_steps,
                retry_delay_blocks: retry_delay_blocks.unwrap_or(100),
            },
            metadata,
            tokens: NonFungibleToken::new(
                StorageKey::NftOwners,
                owner_id,
                Some(StorageKey::NftMetadata),
                Some(StorageKey::NftEnumeration),
                Some(StorageKey::NftApprovals),
            ),
            series: Vector::new(StorageKey::Series),
            series_cards: LookupMap::new(StorageKey::SeriesCards),
            packs: LookupMap::new(StorageKey::Packs),
            packs_by_owner: LookupMap::new(StorageKey::PacksByOwner),
            pack_count_by_owner: LookupMap::new(StorageKey::PackCountByOwner),
            cards: LookupMap::new(StorageKey::Cards),
            backing: LookupMap::new(StorageKey::Backing),
            listings: IterableMap::new(StorageKey::Listings),
            next_pack_id: 0,
            next_token_id: 0,
            revenue: 0,
        }
    }

    // ------------------------------------------------------------ administration

    /// Change le compte qui reçoit `redeem(owner, asset_id, amount)`.
    pub fn set_redeemer(&mut self, redeemer_id: Option<AccountId>) {
        self.assert_owner();
        self.redeemer_id = redeemer_id.clone();
        events::emit("redeemer_set", near_sdk::serde_json::json!({ "redeemer_id": redeemer_id }));
    }

    /// Fait échouer le dernier reçu du tirage (build `test-hooks` seulement).
    #[cfg(feature = "test-hooks")]
    pub fn test_set_reveal_failure(&mut self, fail: bool) {
        self.assert_owner();
        if fail {
            env::storage_write(b"__fail_reveal", &[1]);
        } else {
            env::storage_remove(b"__fail_reveal");
        }
    }
}

impl Contract {
    pub(crate) fn assert_owner(&self) {
        require!(env::predecessor_account_id() == self.owner_id, "Réservé à l'owner");
    }

    pub(crate) fn gas_for_step(&self, step: u8) -> Gas {
        let remaining = (self.config.reveal_steps - step) as u64;
        Gas::from_gas(FINAL_STEP_GAS.as_gas() + remaining * INTERMEDIATE_STEP_GAS.as_gas())
    }

    /// Gaz minimal exigé pour `buy_pack` et `retry_reveal`.
    pub(crate) fn min_entry_gas(&self) -> Gas {
        Gas::from_gas(ENTRY_OWN_GAS.as_gas() + self.gas_for_step(1).as_gas())
    }

    pub(crate) fn series_ref(&self, series_id: u32) -> &Series {
        self.series.get(series_id).unwrap_or_else(|| env::panic_str("Série inconnue"))
    }

    pub(crate) fn card_info(&self, token_id: &TokenId) -> &CardInfo {
        self.cards.get(token_id).unwrap_or_else(|| env::panic_str("Carte inconnue"))
    }

    /// Carte visible d'index `index` (lit un seul bloc).
    pub(crate) fn card_def(&self, series_id: u32, index: u32) -> CardDef {
        self.series_cards
            .get(&(series_id, index / CARDS_PER_CHUNK))
            .and_then(|chunk| chunk.get((index % CARDS_PER_CHUNK) as usize))
            .cloned()
            .unwrap_or_else(|| env::panic_str("Carte de table inconnue"))
    }

    /// Toutes les cartes visibles d'une série, dans l'ordre de la table.
    pub(crate) fn all_cards(&self, series_id: u32, s: &Series) -> Vec<CardDef> {
        let n = s.draw_cards.len() as u32;
        let mut out = Vec::with_capacity(n as usize);
        for k in 0..n.div_ceil(CARDS_PER_CHUNK) {
            if let Some(chunk) = self.series_cards.get(&(series_id, k)) {
                out.extend(chunk.iter().cloned());
            }
        }
        require!(out.len() == n as usize, "Blocs de cartes incohérents");
        out
    }

    /// Table complète (en-tête + cartes) : ce que renvoie `get_series_table` et ce qui est haché.
    pub(crate) fn full_table(&self, series_id: u32) -> SeriesTable {
        let s = self.series_ref(series_id);
        let mut t = s.table.clone();
        t.cards = self.all_cards(series_id, s);
        t
    }

    /// Métadonnées NEP-177 d'une carte visible. Sert au mint et à l'estimation du stockage.
    pub(crate) fn card_metadata(series_id: u32, c: &CardDef, pack_id: u64) -> TokenMetadata {
        let extra = near_sdk::serde_json::json!({
            "series_id": series_id,
            "card_id": c.card_id,
            "rarity": c.rarity.as_str(),
            "burnable": c.backing.is_some(),
            "pack_id": pack_id,
        });
        TokenMetadata {
            title: Some(c.title.clone()),
            media: c.media.clone(),
            reference: c.reference.clone(),
            copies: c.cap.map(|x| x as u64),
            issued_at: Some((env::block_timestamp_ms()).to_string()),
            extra: Some(extra.to_string()),
            ..Default::default()
        }
    }

    /// Métadonnées NEP-177 d'une mythique (scellée ou révélée). Les cartes visibles passent par
    /// `card_metadata`, car leurs définitions ne sont pas dans `Series`.
    pub(crate) fn build_metadata(
        series_id: u32,
        series: &Series,
        kind: CardKind,
        index: u32,
        pack_id: u64,
    ) -> TokenMetadata {
        require!(kind == CardKind::Mythic, "build_metadata : mythiques seulement");
        let issued_at = Some((env::block_timestamp_ms()).to_string());
        let m = &series.table.mythics[index as usize];
        match &series.revealed_mythics[index as usize] {
            Some(r) => Self::revealed_mythic_metadata(series_id, m, r, pack_id, issued_at),
            None => {
                let extra = near_sdk::serde_json::json!({
                    "series_id": series_id,
                    "rarity": "mythic",
                    "sealed": true,
                    "mythic_index": index,
                    "commitment": m.commitment,
                    "pack_id": pack_id,
                });
                TokenMetadata {
                    title: Some("Mythique scellée".to_string()),
                    copies: Some(m.cap as u64),
                    issued_at,
                    extra: Some(extra.to_string()),
                    ..Default::default()
                }
            }
        }
    }

    pub(crate) fn revealed_mythic_metadata(
        series_id: u32,
        m: &MythicCommitment,
        r: &RevealedMythic,
        pack_id: u64,
        issued_at: Option<String>,
    ) -> TokenMetadata {
        let extra = near_sdk::serde_json::json!({
            "series_id": series_id,
            "card_id": r.card_id,
            "rarity": "mythic",
            "burnable": r.content.backing.is_some(),
            "commitment": m.commitment,
            "pack_id": pack_id,
        });
        TokenMetadata {
            title: Some(r.content.title.clone()),
            media: r.content.media.clone(),
            reference: r.content.reference.clone(),
            copies: Some(m.cap as u64),
            issued_at,
            extra: Some(extra.to_string()),
            ..Default::default()
        }
    }

    pub(crate) fn refund(to: &AccountId, amount: u128) {
        if amount > 0 {
            near_sdk::Promise::new(to.clone()).transfer(NearToken::from_yoctonear(amount)).detach();
        }
    }
}

pub(crate) fn hex32(b: &[u8; 32]) -> String {
    hex_encode(b)
}

pub(crate) fn hex_encode(b: &[u8]) -> String {
    const H: &[u8; 16] = b"0123456789abcdef";
    let mut s = String::with_capacity(b.len() * 2);
    for x in b {
        s.push(H[(x >> 4) as usize] as char);
        s.push(H[(x & 15) as usize] as char);
    }
    s
}

pub(crate) fn hex_decode(s: &str) -> Option<Vec<u8>> {
    if s.len() % 2 != 0 {
        return None;
    }
    let v = |c: u8| -> Option<u8> {
        match c {
            b'0'..=b'9' => Some(c - b'0'),
            b'a'..=b'f' => Some(c - b'a' + 10),
            _ => None,
        }
    };
    s.as_bytes().chunks(2).map(|p| Some(v(p[0])? << 4 | v(p[1])?)).collect()
}
