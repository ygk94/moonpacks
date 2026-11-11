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
}

impl From<&CardDef> for DrawCard {
    fn from(c: &CardDef) -> Self {
        DrawCard { rarity: c.rarity, weight: c.weight, cap: c.cap }
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
    /// En-tête de la table (nom, prix, poids, mythiques, redevances). `table.cards` est toujours
    /// vide ici : les cartes visibles sont rangées par blocs dans `Contract::series_cards`, et la
    /// table complète est reconstituée pour les vues, la validation et le hash.
    pub table: SeriesTable,
    /// `draw_cards[i]` pour la carte d'index `i` (même ordre que la table).
    pub draw_cards: Vec<DrawCard>,
    /// Plus grandes métadonnées (borsh) et plus grande entrée d'adossement parmi les cartes
    /// visibles, tenues à jour au chargement (stockage du pire cas sans relire les cartes).
    pub max_card_meta_bytes: u64,
    pub max_card_backing_bytes: u64,
    pub table_hash: Option<[u8; 32]>,
    /// `minted[i]` pour la carte visible d'index `i`.
    pub minted: Vec<u32>,
    /// `mythic_minted[j]` pour `table.mythics[j]`.
    pub mythic_minted: Vec<u32>,
    pub revealed_mythics: Vec<Option<RevealedMythic>>,
    /// Cartes mythiques créées avant la révélation (bornées par le plafond).
    pub sealed_tokens: Vec<Vec<TokenId>>,
    /// Stockage du pire cas d'un booster, en octets, calculé à l'ouverture.
    pub storage_per_pack: u64,
    pub packs_sold: u64,
    /// Stockage payé par l'owner (yoctoNEAR) pendant le chargement par lots, net des
    /// remboursements. `delete_draft` ne rend jamais plus que ce montant.
    pub storage_deposit: u128,
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

#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct SeedRecord {
    pub attempt: u32,
    pub step: u8,
    pub block_height: u64,
    pub seed: [u8; 32],
    pub acc_after: [u8; 32],
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CardKind {
    Visible,
    Mythic,
}

/// Une ligne de tirage, journalisée et stockée pour la vérification publique.
#[near(serializers = [borsh, json])]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DrawRecord {
    pub slot: u8,
    /// `u128(sha256(acc || slot || 0)[0..16]) mod total_rarity_weight`.
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

#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct Pack {
    pub pack_id: u64,
    pub series_id: u32,
    pub owner_id: AccountId,
    pub price_paid: u128,
    pub storage_prepaid: u128,
    pub bought_at_height: u64,
    pub status: PackStatus,
    pub attempt: u32,
    /// Étapes terminées dans la tentative en cours.
    pub step: u8,
    pub acc: [u8; 32],
    pub seeds: Vec<SeedRecord>,
    pub last_progress_height: u64,
    pub token_ids: Vec<TokenId>,
    pub draws: Vec<DrawRecord>,
}

#[near(serializers = [borsh, json])]
#[serde(rename_all = "snake_case")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CardState {
    Normal,
    Redeeming,
}

#[near(serializers = [borsh])]
#[derive(Clone, Debug)]
pub struct CardInfo {
    pub series_id: u32,
    pub kind: CardKind,
    pub index: u32,
    pub rarity: Rarity,
    pub state: CardState,
    /// Mythique tirée avant sa révélation.
    pub sealed: bool,
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
