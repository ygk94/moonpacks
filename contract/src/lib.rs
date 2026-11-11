//! Memaster : boosters de cartes NFT (NEP-171/177/178/181/199) représentant des memecoins.
//!
//! - séries à table figée et hachée à l'ouverture (`series.rs`) ;
//! - achat en une signature puis tirage sur k reçus privés chaînés (`pack.rs`, `draw.rs`) ;
//! - mythiques secrètes sous engagement, révélées à leur première sortie (`mythic.rs`) ;
//! - marché intégré (`market.rs`) ;
//! - burn en deux temps via un `redeemer` abstrait (`redeem.rs`) ;
//! - mécaniques : pitié, rareté pilotée par les burns, gold rush, résurrection (`mechanics.rs`) ;
//! - interfaces NFT standard, stockage minimal par carte (`nft.rs`).

use near_contract_standards::non_fungible_token::metadata::{
    NFTContractMetadata, TokenMetadata, NFT_METADATA_SPEC,
};
use near_contract_standards::non_fungible_token::TokenId;
use near_sdk::json_types::U128;
use near_sdk::store::{IterableMap, LookupMap, Vector};
use near_sdk::{env, near, require, AccountId, BorshStorageKey, Gas, NearToken, PanicOnDefault};

pub mod draw;
pub mod events;
mod hash_stream;
mod mechanics;
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
#[cfg(test)]
mod tests_mech;

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
//
// Une carte ne stocke que sa référence : un emplacement de pack (`CardSlot`, 10 o) et son tirage
// (`PackDraw`, 23 o), plus une entrée de 8 o dans la liste de son propriétaire et une dans la liste
// globale (listes par blocs). Les métadonnées NEP-177 et l'adossement sont reconstruits à la lecture
// depuis la table de série. Les constantes ci-dessous bornent le pire cas (comptes de 64 octets,
// premier achat du compte, nouveaux blocs de liste) ; la mesure est dans le README.

/// Enregistrement de pack hors graines et cartes : clé, surcoût de 40 o par entrée, champs fixes,
/// propriétaire de 64 octets au plus.
pub const PACK_RECORD_BYTES: u64 = 200;
/// Une graine journalisée (tentative, étape, hauteur, graine).
pub const SEED_RECORD_BYTES: u64 = 45;
/// Par carte : `PackDraw` (31) + `CardSlot` (10) + liste du propriétaire (8) + liste globale (8).
pub const PER_CARD_BYTES: u64 = 60;
/// Par mythique scellée : identifiant ajouté à `Series::sealed_tokens`.
pub const SEALED_TOKEN_BYTES: u64 = 24;
/// Entrée de la liste des packs du compte.
pub const OWNER_PACK_LIST_BYTES: u64 = 8;
/// Nouveaux blocs de liste au pire (cartes du compte, liste globale, packs du compte).
pub const NEW_CHUNKS_BYTES: u64 = 120 + 50 + 120;
/// Premier achat d'un compte : compteurs de packs et de cartes du compte.
pub const NEW_ACCOUNT_BYTES: u64 = 230;
/// Entrée du compteur de pitié (compte, série), à son premier tirage.
pub const PITY_ENTRY_BYTES: u64 = 120;
/// Entrée du plafond de packs rush (compte, série), au premier pack rush du compte.
pub const RUSH_ENTRY_BYTES: u64 = 130;
/// Marge.
pub const PACK_MARGIN_BYTES: u64 = 64;
/// Dépôt d'une annonce de marché.
pub const LISTING_DEPOSIT: NearToken = NearToken::from_millinear(5);

/// Cartes par bloc de la liste d'un propriétaire.
pub const OWNER_CHUNK: u32 = 32;
/// Cartes par bloc de la liste globale.
pub const GLOBAL_CHUNK: u32 = 64;
/// Seaux au plus dans la fenêtre du gold rush.
pub const MAX_RUSH_BUCKETS: u64 = 96;
/// Bornes du compteur de pitié.
pub const MAX_PITY_N: u32 = 10_000;
/// Cartes ressuscitables au plus par série (`ResurrectionParams::eligible`).
pub const MAX_RESURRECTABLE: usize = 200;
/// Délai par défaut du changement d'oracle : 24 h à 0,6 s par bloc.
pub const DEFAULT_ORACLE_DELAY_BLOCKS: u64 = 144_000;
/// Borne de l'a priori des burns (`BurnParams::prior_k`).
pub const MAX_BURN_PRIOR_K: u32 = 1_000_000;
pub const PPM: u64 = 1_000_000;

#[derive(BorshStorageKey)]
#[near]
enum StorageKey {
    Series,
    SeriesCards,
    SeriesBurns,
    Resurrected,
    Packs,
    OwnerPacks,
    PackCountByOwner,
    OwnerTokens,
    OwnerTokenCount,
    AllTokens,
    Approvals,
    Pity,
    Listings,
    RushAccounts,
}

#[near(contract_state)]
#[derive(PanicOnDefault)]
pub struct Contract {
    owner_id: AccountId,
    redeemer_id: Option<AccountId>,
    /// Oracle de prix abstrait (résurrection des coins morts), comme le redeemer.
    price_oracle_id: Option<AccountId>,
    /// Changement d'oracle en attente (`propose_price_oracle`, puis `accept_price_oracle`).
    price_oracle_pending: Option<OracleProposal>,
    config: Config,
    metadata: NFTContractMetadata,
    series: Vector<Series>,
    /// Cartes visibles des séries, par blocs de `CARDS_PER_CHUNK` : `(series_id, bloc) → cartes`.
    series_cards: LookupMap<(u32, u32), Vec<CardDef>>,
    /// Compteurs de burn (séries à rareté pilotée par les burns).
    series_burns: LookupMap<u32, BurnState>,
    /// Adossement donné par l'oracle à une carte de collection : `(series_id, index) → adossement`.
    resurrected: LookupMap<(u32, u32), Backing>,
    packs: LookupMap<u64, Pack>,
    /// Packs d'un compte, par blocs de `OWNER_CHUNK` : `(compte, bloc) → pack_id`.
    owner_packs: LookupMap<(AccountId, u32), Vec<u64>>,
    pack_count_by_owner: LookupMap<AccountId, u32>,
    /// Cartes d'un compte (NEP-181), par blocs de `OWNER_CHUNK`, retrait par échange avec la dernière.
    owner_tokens: LookupMap<(AccountId, u32), Vec<u64>>,
    owner_token_count: LookupMap<AccountId, u32>,
    /// Toutes les cartes vivantes (NEP-181), par blocs de `GLOBAL_CHUNK`.
    all_tokens: LookupMap<u32, Vec<u64>>,
    total_supply: u32,
    approvals: LookupMap<u64, TokenApprovals>,
    /// Compteur de pitié : `(compte, série) → packs consécutifs sans gold pack`.
    pity: LookupMap<(AccountId, u32), u32>,
    /// Packs rush d'un compte pendant le dernier rush où il en a acheté :
    /// `(compte, série) → (hauteur du déclenchement, packs rush)`.
    rush_accounts: LookupMap<(AccountId, u32), (u64, u32)>,
    listings: IterableMap<TokenId, Listing>,
    next_pack_id: u64,
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
        oracle_delay_blocks: Option<u64>,
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
            owner_id,
            redeemer_id,
            price_oracle_id: None,
            price_oracle_pending: None,
            config: Config {
                reveal_steps,
                retry_delay_blocks: retry_delay_blocks.unwrap_or(100),
                oracle_delay_blocks: oracle_delay_blocks.unwrap_or(DEFAULT_ORACLE_DELAY_BLOCKS),
            },
            metadata,
            series: Vector::new(StorageKey::Series),
            series_cards: LookupMap::new(StorageKey::SeriesCards),
            series_burns: LookupMap::new(StorageKey::SeriesBurns),
            resurrected: LookupMap::new(StorageKey::Resurrected),
            packs: LookupMap::new(StorageKey::Packs),
            owner_packs: LookupMap::new(StorageKey::OwnerPacks),
            pack_count_by_owner: LookupMap::new(StorageKey::PackCountByOwner),
            owner_tokens: LookupMap::new(StorageKey::OwnerTokens),
            owner_token_count: LookupMap::new(StorageKey::OwnerTokenCount),
            all_tokens: LookupMap::new(StorageKey::AllTokens),
            total_supply: 0,
            approvals: LookupMap::new(StorageKey::Approvals),
            pity: LookupMap::new(StorageKey::Pity),
            rush_accounts: LookupMap::new(StorageKey::RushAccounts),
            listings: IterableMap::new(StorageKey::Listings),
            next_pack_id: 0,
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

    /// Propose un nouvel oracle de prix (résurrection des coins morts), `None` pour n'en plus avoir.
    /// Le changement n'a lieu qu'à `accept_price_oracle`, au plus tôt `oracle_delay_blocks` blocs
    /// plus tard (24 h par défaut) : les joueurs voient venir tout changement de ceux qui peuvent
    /// rendre une carte brûlable. Une nouvelle proposition remplace la précédente et relance le délai.
    pub fn propose_price_oracle(&mut self, price_oracle_id: Option<AccountId>) {
        self.assert_owner();
        let h = env::block_height();
        let p = OracleProposal {
            price_oracle_id,
            proposed_at: h,
            effective_from: h.saturating_add(self.config.oracle_delay_blocks),
        };
        events::emit(
            "price_oracle_proposed",
            near_sdk::serde_json::json!({
                "price_oracle_id": p.price_oracle_id, "current": self.price_oracle_id,
                "proposed_at": p.proposed_at, "effective_from": p.effective_from,
            }),
        );
        self.price_oracle_pending = Some(p);
    }

    /// Applique le changement d'oracle proposé, une fois le délai écoulé (owner).
    pub fn accept_price_oracle(&mut self) {
        self.assert_owner();
        let p = self.price_oracle_pending.clone().unwrap_or_else(|| env::panic_str("Aucun changement d'oracle proposé"));
        require!(
            env::block_height() >= p.effective_from,
            format!("Délai du changement d'oracle non écoulé : bloc {} au plus tôt", p.effective_from)
        );
        let previous = std::mem::replace(&mut self.price_oracle_id, p.price_oracle_id.clone());
        self.price_oracle_pending = None;
        events::emit(
            "price_oracle_accepted",
            near_sdk::serde_json::json!({
                "price_oracle_id": p.price_oracle_id, "previous": previous,
                "proposed_at": p.proposed_at, "block_height": env::block_height(),
            }),
        );
    }

    /// Retire l'oracle de prix tout de suite (owner), par exemple si sa clé est compromise. Retirer
    /// l'oracle ne fait que supprimer des résurrections futures : pas de délai. Une proposition en
    /// attente reste en attente.
    pub fn revoke_price_oracle(&mut self) {
        self.assert_owner();
        let previous = self.price_oracle_id.take();
        events::emit(
            "price_oracle_revoked",
            near_sdk::serde_json::json!({ "previous": previous, "block_height": env::block_height() }),
        );
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

    /// Métadonnées NEP-177 d'une carte visible, reconstruites depuis la table (rien n'est stocké
    /// par carte). `burnable` suit l'adossement courant (table, ou résurrection par l'oracle).
    pub(crate) fn card_metadata(
        series_id: u32,
        c: &CardDef,
        pack_id: u64,
        burnable: bool,
        issued_at_ms: u64,
    ) -> TokenMetadata {
        let extra = near_sdk::serde_json::json!({
            "series_id": series_id,
            "card_id": c.card_id,
            "rarity": c.rarity.as_str(),
            "burnable": burnable,
            "pack_id": pack_id,
        });
        TokenMetadata {
            title: Some(c.title.clone()),
            media: c.media.clone(),
            reference: c.reference.clone(),
            copies: c.cap.map(|x| x as u64),
            issued_at: Some(issued_at_ms.to_string()),
            extra: Some(extra.to_string()),
            ..Default::default()
        }
    }

    /// Métadonnées NEP-177 d'une mythique : scellée tant que l'engagement n'est pas révélé, puis
    /// révélée (avec `updated_at` = date de révélation pour une carte créée scellée).
    pub(crate) fn mythic_metadata(
        series_id: u32,
        series: &Series,
        index: u32,
        pack_id: u64,
        issued_at_ms: u64,
        token_id: &str,
    ) -> TokenMetadata {
        let issued_at = Some(issued_at_ms.to_string());
        let j = index as usize;
        let m = &series.table.mythics[j];
        match &series.revealed_mythics[j] {
            Some(r) => {
                let mut meta = Self::revealed_mythic_metadata(series_id, m, r, pack_id, issued_at);
                if series.sealed_tokens[j].iter().any(|t| t == token_id) {
                    meta.updated_at = Some(series.mythic_revealed_ms[j].to_string());
                }
                meta
            }
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

/// `token_id = pack_id × 10 + emplacement` (10 cartes par booster au plus).
pub fn token_id_of(pack_id: u64, slot: u8) -> TokenId {
    (pack_id * 10 + slot as u64).to_string()
}

/// Inverse de `token_id_of` ; refuse les formes non canoniques (zéros de tête, signe…).
pub fn parse_token_id(token_id: &str) -> Option<u64> {
    let n: u64 = token_id.parse().ok()?;
    (n.to_string() == token_id).then_some(n)
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
