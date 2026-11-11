//! Types publics du contrat : table de série, packs, cartes, marché.

use near_contract_standards::non_fungible_token::TokenId;
use near_sdk::json_types::U128;
use near_sdk::{near, AccountId};

/// Les cinq raretés, de la plus haute à la plus basse.
/// L'ordre compte : quand une rareté est épuisée, le tirage retombe sur la suivante.
#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum Rarity {
    Mythic,
    Legendary,
    Epic,
    Rare,
    Common,
}

impl Rarity {
    pub const ALL: [Rarity; 5] =
        [Rarity::Mythic, Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common];

    pub fn index(self) -> usize {
        self as usize
    }

    pub fn as_str(self) -> &'static str {
        match self {
            Rarity::Mythic => "mythic",
            Rarity::Legendary => "legendary",
            Rarity::Epic => "epic",
            Rarity::Rare => "rare",
            Rarity::Common => "common",
        }
    }

    /// Rareté immédiatement inférieure (None pour commune).
    pub fn lower(self) -> Option<Rarity> {
        match self {
            Rarity::Mythic => Some(Rarity::Legendary),
            Rarity::Legendary => Some(Rarity::Epic),
            Rarity::Epic => Some(Rarity::Rare),
            Rarity::Rare => Some(Rarity::Common),
            Rarity::Common => None,
        }
    }
}

/// Poids de tirage des raretés (pas forcément normalisés).
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RarityWeights {
    pub mythic: u32,
    pub legendary: u32,
    pub epic: u32,
    pub rare: u32,
    pub common: u32,
}

impl RarityWeights {
    pub fn get(&self, r: Rarity) -> u32 {
        match r {
            Rarity::Mythic => self.mythic,
            Rarity::Legendary => self.legendary,
            Rarity::Epic => self.epic,
            Rarity::Rare => self.rare,
            Rarity::Common => self.common,
        }
    }

    pub fn total(&self) -> u64 {
        Rarity::ALL.iter().map(|r| self.get(*r) as u64).sum()
    }
}

/// Adossement d'une carte : identifiant d'actif opaque et quantité (unités de base).
/// La mécanique d'approvisionnement et de retrait sera conçue plus tard ;
/// le contrat ne fait que tenir ce registre et le transmettre au `redeemer`.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Backing {
    pub asset_id: String,
    pub amount: U128,
}

/// Carte visible de la table (toutes les raretés sauf mythique).
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CardDef {
    pub card_id: String,
    pub title: String,
    pub rarity: Rarity,
    pub weight: u32,
    /// Plafond de cartes créées. `None` = illimité.
    pub cap: Option<u32>,
    pub media: Option<String>,
    pub reference: Option<String>,
    /// `Some` = carte brûlable contre cet adossement.
    pub backing: Option<Backing>,
}

/// Carte mythique secrète : seul l'engagement est public.
/// `commitment = sha256(card_id || sel)` ;
/// `content_hash = sha256(json(MythicContent) || sel)` lie le titre, les médias et l'adossement.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MythicCommitment {
    pub commitment: String,
    pub content_hash: String,
    pub weight: u32,
    pub cap: u32,
}

/// Contenu d'une mythique, révélé avec `sel` à sa première sortie.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MythicContent {
    pub title: String,
    pub media: Option<String>,
    pub reference: Option<String>,
    pub backing: Option<Backing>,
}

#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RevealedMythic {
    pub card_id: String,
    pub sel: String,
    pub content: MythicContent,
    pub revealed_at_height: u64,
}

#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Royalty {
    pub account_id: AccountId,
    /// Points de base (100 = 1 %).
    pub bps: u16,
}

/// La table d'une série. Figée à l'ouverture ; son hash est
/// `sha256(serde_json::to_vec(table))`, soit exactement les octets renvoyés par
/// la vue `get_series_table`.
///
/// **L'ordre des champs fait partie du hash** (serde les sérialise dans l'ordre de déclaration) :
/// `hash_stream::header_json_parts` coupe l'en-tête autour de `"cards":[`, et le vérificateur
/// (`verifier/memaster_verifier/canon.py`) reproduit cet ordre. Le test
/// `hash_stream::tests::series_table_field_order_is_locked` casse si un champ est ajouté ou déplacé.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SeriesTable {
    pub name: String,
    /// Prix d'un booster en yoctoNEAR (hors stockage).
    pub price: U128,
    pub cards_per_pack: u8,
    pub rarity_weights: RarityWeights,
    pub cards: Vec<CardDef>,
    pub mythics: Vec<MythicCommitment>,
    pub royalties: Vec<Royalty>,
    /// Mécaniques optionnelles (pitié, rareté pilotée par les burns, gold rush), hachées avec la
    /// table. **Absent du JSON quand `None`** : une table sans mécanique garde exactement les
    /// octets, donc le hash et les tirages, d'avant leur introduction.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mechanics: Option<Mechanics>,
}

/// Paramètres des mécaniques d'une série (voir `docs/mecaniques-spec.md`). Tous les champs sont
/// toujours sérialisés (`null` pour une option absente), dans cet ordre.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Mechanics {
    /// Table de taux « or » : poids de rareté d'un gold pack (pitié).
    pub gold_weights: Option<RarityWeights>,
    /// Compteur de pitié par compte et par série.
    pub pity: Option<PityParams>,
    /// Rareté pilotée par les burns, renormalisée entre brûlables d'une même rareté.
    pub burn: Option<BurnParams>,
    /// Gold rush collectif, avec sa propre table de taux.
    pub rush: Option<RushParams>,
}

/// Pitié : probabilité d'un gold pack `min(10⁶, p0_ppm + k_ppm × n)` ppm, `n` = packs consécutifs
/// sans gold pack ; gold pack garanti quand `n = n_max − 1` ; `n` repart à 0 après un gold pack.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PityParams {
    pub p0_ppm: u32,
    pub k_ppm: u32,
    /// N : le N-ième pack sans gold pack est un gold pack (N = 1 : tous les packs sont or).
    pub n_max: u32,
}

/// Rareté pilotée par les burns : poids brut d'une brûlable
/// `max(⌊poids × (émises − brûlées + K) / (émises + K)⌋, ⌊poids × floor_bps / 10⁴⌋, 1)`, puis
/// renormalisation entre les brûlables de la rareté (leur part totale dans la rareté ne bouge pas).
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BurnParams {
    /// Plancher en points de base du poids de base (2 500 = 25 %).
    pub floor_bps: u32,
    /// A priori `K` (lissage) : tout se passe comme si chaque carte avait `K` exemplaires de plus,
    /// émis et jamais brûlés. De l'ordre des émissions attendues par carte (20 par défaut).
    pub prior_k: u32,
}

/// Gold rush à palier relatif : un achat déclenche un rush si, dans la fenêtre courte
/// (`window_blocks`), au moins `min_packs` packs ont été achetés et le rythme vaut au moins
/// `ratio_bps / 10⁴` fois le rythme moyen de la fenêtre longue (`baseline_blocks`, 24 h), une fois
/// la série active depuis `baseline_blocks` blocs et hors pause (`cooldown_blocks` après la fin du
/// rush précédent). Les packs achetés dans les `duration_blocks` blocs suivants utilisent `weights`.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RushParams {
    pub ratio_bps: u32,
    pub min_packs: u32,
    pub window_blocks: u64,
    pub baseline_blocks: u64,
    pub bucket_blocks: u64,
    pub duration_blocks: u64,
    pub cooldown_blocks: u64,
    /// Table de taux « rush », distincte de la table or (couverture ≤ 80 %, contrôlée hors chaîne
    /// par `scripts/build_series.py`).
    pub weights: RarityWeights,
}

/// État glissant du rush (dans la série) : `ring[b % m] = (seau b, packs achetés dans ce seau)`,
/// `m = baseline_blocks / bucket_blocks`.
#[near(serializers = [borsh])]
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub struct RushState {
    pub ring: Vec<(u64, u32)>,
    /// Hauteur du premier achat (début de la fenêtre longue).
    pub start_height: Option<u64>,
    /// Hauteur du dernier déclenchement.
    pub last_trigger: Option<u64>,
    pub rush_count: u32,
}

/// Compteurs de burn d'une série (rareté pilotée par les burns) : `burned[i]` cartes visibles
/// d'index `i` brûlées, `seq` = Σ burned (numéro d'ordre journalisé dans `card_redeemed`).
#[near(serializers = [borsh])]
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub struct BurnState {
    pub burned: Vec<u32>,
    pub seq: u64,
}

/// Table de taux utilisée pour un pack.
#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PackMode {
    Base,
    Gold,
    Rush,
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SeriesStatus {
    Draft,
    Open,
    Paused,
    Closed,
    /// Brouillon supprimé par `delete_draft` : cartes, données de tirage et flux de hachage vidés.
    /// L'emplacement reste (les identifiants de série sont des index de `Vector`), avec l'en-tête
    /// réduit au nom, au prix et aux poids.
    Deleted,
}

/// Données de tirage d'une carte visible (rareté, poids, plafond), gardées dans la série.
/// Le tirage n'a besoin que de cela : les métadonnées des cartes restent dans `series_cards`.
#[near(serializers = [borsh])]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct DrawCard {
    pub rarity: Rarity,
    pub weight: u32,
    pub cap: Option<u32>,
    /// Brûlable : adossée par la table, ou ressuscitée par l'oracle. Ne sert qu'à la rareté
    /// pilotée par les burns (aucun effet sur un tirage sans cette mécanique).
    pub backed: bool,
}

impl From<&CardDef> for DrawCard {
    fn from(c: &CardDef) -> Self {
        DrawCard { rarity: c.rarity, weight: c.weight, cap: c.cap, backed: c.backing.is_some() }
    }
}

#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct Series {
    pub id: u32,
    pub status: SeriesStatus,
    /// Créée par `create_series_batched` (ou remplacée par `replace_series_table_batched`) :
    /// accepte `append_series_cards`, avec des `card_id` strictement croissants.
    pub batched: bool,
    /// Dernier `card_id` chargé (brouillon par lots).
    pub last_card_id: Option<String>,
    /// SHA-256 du JSON de la table, en cours de calcul pendant le chargement (brouillon).
    pub hash_stream: Option<crate::hash_stream::Sha256Stream>,
    /// En-tête de la table (nom, prix, poids, mythiques, redevances, mécaniques). `table.cards`
    /// est toujours vide ici : les cartes visibles sont rangées par blocs dans
    /// `Contract::series_cards`, et la table complète est reconstituée pour les vues et le hash.
    pub table: SeriesTable,
    /// `draw_cards[i]` pour la carte d'index `i` (même ordre que la table).
    pub draw_cards: Vec<DrawCard>,
    pub table_hash: Option<[u8; 32]>,
    /// `minted[i]` pour la carte visible d'index `i`.
    pub minted: Vec<u32>,
    /// `mythic_minted[j]` pour `table.mythics[j]`.
    pub mythic_minted: Vec<u32>,
    pub revealed_mythics: Vec<Option<RevealedMythic>>,
    /// Horodatage (ms) de la révélation de chaque mythique (0 tant qu'elle est scellée).
    pub mythic_revealed_ms: Vec<u64>,
    /// Cartes mythiques créées scellées (bornées par le plafond). Gardées après la révélation :
    /// leurs métadonnées portent `updated_at`.
    pub sealed_tokens: Vec<Vec<TokenId>>,
    /// Stockage du pire cas d'un booster, en octets, calculé à l'ouverture.
    pub storage_per_pack: u64,
    pub packs_sold: u64,
    /// Stockage payé par l'owner (yoctoNEAR) pendant le chargement par lots, net des
    /// remboursements. `delete_draft` ne rend jamais plus que ce montant.
    pub storage_deposit: u128,
    /// État du gold rush (si `mechanics.rush`).
    pub rush: Option<RushState>,
    /// Résurrections de la série (cartes devenues brûlables), journalisé dans `card_resurrected`
    /// et `pack_revealed.mechanics.resurrect_seq`.
    pub resurrect_seq: u64,
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PackStatus {
    Pending,
    Revealed,
    /// `MAX_ATTEMPTS` tentatives échouées : plus de relance, pas de remboursement.
    Stuck,
}

/// Graine journalisée d'une étape réussie. `acc` après l'étape n'est pas stocké : il se recalcule
/// en enchaînant les graines depuis `initial_acc` (vue `get_pack`).
#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct SeedRecord {
    pub attempt: u32,
    pub step: u8,
    pub block_height: u64,
    pub seed: [u8; 32],
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CardKind {
    Visible,
    Mythic,
}

/// Une ligne de tirage, journalisée dans `pack_revealed` et renvoyée par `get_pack`.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DrawRecord {
    pub slot: u8,
    /// `u128(sha256(acc || slot || 0)[0..16]) mod total_rarity_weight` (poids de la table du pack).
    pub rarity_roll: U128,
    pub rolled_rarity: Rarity,
    pub final_rarity: Rarity,
    /// `u128(sha256(acc || slot || 1)[0..16]) mod somme_des_poids_disponibles`.
    pub card_roll: U128,
    pub kind: CardKind,
    /// Index dans `table.cards` ou `table.mythics`.
    pub index: u32,
    pub token_id: TokenId,
}

/// Tirage stocké dans le pack (31 octets) : `DrawRecord` sans `token_id` (déduit du pack et de
/// l'emplacement). `rarity_roll` < Σ poids de rareté < 2³⁵ tient sur 64 bits ; `card_roll` reste
/// sur 128 bits (poids renormalisés des burns, jusqu'à 2⁸⁶).
#[near(serializers = [borsh])]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PackDraw {
    pub rarity_roll: u64,
    pub rolled_rarity: Rarity,
    pub final_rarity: Rarity,
    pub card_roll: u128,
    pub kind: CardKind,
    pub index: u32,
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CardState {
    Normal,
    Redeeming,
    /// Brûlée : l'emplacement reste dans le pack (les index des autres cartes ne bougent pas).
    Burned,
}

/// Une carte = un emplacement de pack. Sa référence (série, index de carte) est dans le pack et
/// dans son tirage ; ses métadonnées NEP-177 sont reconstruites à la lecture depuis la table.
/// 10 octets tant que l'acheteur du pack la détient.
#[near(serializers = [borsh])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CardSlot {
    /// `None` = l'acheteur du pack.
    pub owner: Option<AccountId>,
    pub state: CardState,
    /// Position dans la liste des cartes du propriétaire (`nft_tokens_for_owner`).
    pub owner_pos: u32,
    /// Position dans la liste globale (`nft_tokens`).
    pub global_pos: u32,
}

/// Bits de `Pack::flags`.
pub const FLAG_RUSH: u8 = 1;
pub const FLAG_GOLD: u8 = 2;
pub const FLAG_MODE_RUSH: u8 = 4;

#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct Pack {
    pub series_id: u32,
    pub owner_id: AccountId,
    pub bought_at_height: u64,
    pub status: PackStatus,
    pub attempt: u32,
    /// Étapes terminées dans la tentative en cours.
    pub step: u8,
    pub acc: [u8; 32],
    pub seeds: Vec<SeedRecord>,
    pub last_progress_height: u64,
    /// Horodatage (ms) du tirage : `issued_at` des cartes.
    pub revealed_at_ms: u64,
    /// `FLAG_RUSH` : rush actif à l'achat (figé par `buy_pack`). `FLAG_GOLD` / `FLAG_MODE_RUSH` :
    /// table utilisée au tirage.
    pub flags: u8,
    pub draws: Vec<PackDraw>,
    /// Cartes du pack, emplacement par emplacement (`token_id = pack_id × 10 + emplacement`).
    pub cards: Vec<CardSlot>,
}

impl Pack {
    pub fn mode(&self) -> PackMode {
        if self.flags & FLAG_GOLD != 0 {
            PackMode::Gold
        } else if self.flags & FLAG_MODE_RUSH != 0 {
            PackMode::Rush
        } else {
            PackMode::Base
        }
    }
}

/// Approbations NEP-178 d'une carte. `next_id` survit aux transferts (identifiants croissants).
#[near(serializers = [borsh])]
#[derive(Clone, Debug, Default)]
pub struct TokenApprovals {
    pub next_id: u64,
    pub accounts: std::collections::BTreeMap<AccountId, u64>,
}

#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Listing {
    pub seller_id: AccountId,
    pub price: U128,
    /// Dépôt de stockage de l'annonce, rendu au vendeur au retrait ou à la vente.
    pub deposit: U128,
}

#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Config {
    /// Nombre de reçus chaînés du tirage (k).
    pub reveal_steps: u8,
    /// Délai, en blocs, avant qu'un `retry_reveal` soit permis.
    pub retry_delay_blocks: u64,
}

/// NEP-199.
#[near(serializers = [json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Payout {
    pub payout: std::collections::HashMap<AccountId, U128>,
}
