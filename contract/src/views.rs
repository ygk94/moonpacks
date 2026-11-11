//! Fonctions de lecture : table, taux, engagements, hash, packs, cartes, marché.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{json, Value};

#[near(serializers = [json])]
pub struct SeriesView {
    pub series_id: u32,
    pub status: SeriesStatus,
    pub name: String,
    pub price: U128,
    pub cards_per_pack: u8,
    pub table_hash: Option<String>,
    pub storage_per_pack: u64,
    /// Dépôt exact à joindre à `buy_pack` (prix + stockage du pire cas).
    pub required_deposit: U128,
    pub min_gas: U64,
    pub packs_sold: u64,
    /// Cartes visibles chargées (lots compris).
    pub card_count: u32,
    pub minted: Vec<u32>,
    pub mythic_minted: Vec<u32>,
    /// Paramètres des mécaniques (`None` : série sans mécanique).
    pub mechanics: Option<Mechanics>,
    /// Cartes brûlées par index (rareté pilotée par les burns ; vide sinon) et numéro d'ordre.
    pub burned: Vec<u32>,
    pub burn_seq: u64,
}

use near_sdk::json_types::U64;

/// En-tête léger d'une série : tout sauf les cartes visibles, avec le hash figé et le nombre de
/// cartes. Coût constant quelle que soit la taille de la table (aucun bloc de cartes lu).
///
/// Pour vérifier une table : `header` avec `cards` = concaténation des pages de
/// `get_series_cards(series_id, from_index, 200)` pour `from_index` = 0, 200, … < `card_count`,
/// puis `sha256(serde_json)` de cette table = `table_hash`.
#[near(serializers = [json])]
pub struct SeriesHeaderView {
    pub series_id: u32,
    pub status: SeriesStatus,
    /// Hash enregistré à l'ouverture (`None` pour un brouillon).
    pub table_hash: Option<String>,
    pub card_count: u32,
    /// Taille maximale d'une page de `get_series_cards` et de `get_rates`.
    pub max_page: u32,
    /// Stockage payé par l'owner pour le chargement par lots (yoctoNEAR, net des remboursements).
    pub storage_deposit: U128,
    /// La table sans ses cartes (`cards` toujours vide), champs dans l'ordre du hash.
    pub header: SeriesTable,
}

#[near(serializers = [json])]
pub struct MythicView {
    pub index: u32,
    pub commitment: String,
    pub content_hash: String,
    pub weight: u32,
    pub cap: u32,
    pub minted: u32,
    pub revealed: Option<RevealedMythic>,
}

#[near(serializers = [json])]
pub struct CardView {
    pub token_id: TokenId,
    pub owner_id: AccountId,
    pub series_id: u32,
    pub kind: CardKind,
    pub index: u32,
    pub card_id: Option<String>,
    pub rarity: Rarity,
    pub state: CardState,
    pub sealed: bool,
    pub backing: Option<Backing>,
    pub listing: Option<Listing>,
}

#[near]
impl Contract {
    pub fn get_config(&self) -> Value {
        json!({
            "owner_id": self.owner_id,
            "redeemer_id": self.redeemer_id,
            "price_oracle_id": self.price_oracle_id,
            "price_oracle_pending": self.price_oracle_pending,
            "oracle_delay_blocks": self.config.oracle_delay_blocks,
            "reveal_steps": self.config.reveal_steps,
            "retry_delay_blocks": self.config.retry_delay_blocks,
            "gas": {
                "intermediate_step": U64(INTERMEDIATE_STEP_GAS.as_gas()),
                "final_step": U64(FINAL_STEP_GAS.as_gas()),
                "min_entry": U64(self.min_entry_gas().as_gas()),
                "min_redeem": U64(MIN_REDEEM_GAS.as_gas()),
            },
            "listing_deposit": U128(LISTING_DEPOSIT.as_yoctonear()),
            "revenue": U128(self.revenue),
            "next_pack_id": self.next_pack_id,
            // token_id = pack_id × 10 + emplacement : borne haute des identifiants à venir.
            "next_token_id": self.next_pack_id * 10,
            "total_supply": self.total_supply,
        })
    }

    pub fn get_series_count(&self) -> u32 {
        self.series.len()
    }

    pub fn get_series(&self, series_id: u32) -> SeriesView {
        let s = self.series_ref(series_id);
        let storage = env::storage_byte_cost().as_yoctonear() * s.storage_per_pack as u128;
        SeriesView {
            series_id,
            status: s.status,
            name: s.table.name.clone(),
            price: s.table.price,
            cards_per_pack: s.table.cards_per_pack,
            table_hash: s.table_hash.map(|h| hex32(&h)),
            storage_per_pack: s.storage_per_pack,
            required_deposit: U128(s.table.price.0 + storage),
            min_gas: U64(self.min_entry_gas().as_gas()),
            packs_sold: s.packs_sold,
            card_count: s.draw_cards.len() as u32,
            minted: s.minted.clone(),
            mythic_minted: s.mythic_minted.clone(),
            mechanics: s.table.mechanics.clone(),
            burned: self.series_burns.get(&series_id).map(|b| b.burned.clone()).unwrap_or_default(),
            burn_seq: self.series_burns.get(&series_id).map(|b| b.seq).unwrap_or(0),
        }
    }

    /// La table exacte : `sha256` des octets JSON renvoyés = `table_hash`.
    /// **Petites séries seulement** : elle relit toutes les cartes (183 Tgas mesurés pour 2 000
    /// cartes aux chaînes maximales). Au-delà de quelques centaines de cartes, utiliser
    /// `get_series_header` et `get_series_cards`.
    pub fn get_series_table(&self, series_id: u32) -> SeriesTable {
        self.full_table(series_id)
    }

    /// En-tête sans les cartes, hash figé et nombre de cartes (voir `SeriesHeaderView`).
    pub fn get_series_header(&self, series_id: u32) -> SeriesHeaderView {
        let s = self.series_ref(series_id);
        SeriesHeaderView {
            series_id,
            status: s.status,
            table_hash: s.table_hash.map(|h| hex32(&h)),
            card_count: s.draw_cards.len() as u32,
            max_page: MAX_CARDS_PER_CALL as u32,
            storage_deposit: U128(s.storage_deposit),
            header: s.table.clone(),
        }
    }

    /// Cartes visibles paginées (`limit` ≤ 200, 100 par défaut), dans l'ordre de la table.
    /// Ces pages concaténées dans `get_series_header(..).header.cards` redonnent la table hachée.
    /// Lit au plus 5 blocs de 50 cartes par appel.
    pub fn get_series_cards(&self, series_id: u32, from_index: Option<u32>, limit: Option<u32>) -> Vec<CardDef> {
        let (from, to) = self.page(series_id, from_index, limit.unwrap_or(100));
        self.cards_range(series_id, from, to)
    }

    /// Hash **enregistré à l'ouverture** (`None` pour un brouillon). Coût constant : le contrat
    /// ne recalcule rien. Le vérificateur relit la table page par page et compare son propre
    /// calcul à cette valeur.
    pub fn get_series_table_hash(&self, series_id: u32) -> Value {
        let s = self.series_ref(series_id);
        json!({ "stored": s.table_hash.map(|h| hex32(&h)), "card_count": s.draw_cards.len() })
    }

    pub fn get_mythic_commitments(&self, series_id: u32) -> Vec<MythicView> {
        let s = self.series_ref(series_id);
        s.table
            .mythics
            .iter()
            .enumerate()
            .map(|(j, m)| MythicView {
                index: j as u32,
                commitment: m.commitment.clone(),
                content_hash: m.content_hash.clone(),
                weight: m.weight,
                cap: m.cap,
                minted: s.mythic_minted[j],
                revealed: s.revealed_mythics[j].clone(),
            })
            .collect()
    }

    /// Taux publics. Probabilité d'une carte (hors effet des plafonds) =
    /// `rarity_weight / total_rarity_weight × card_weight / rarity_card_weight`.
    /// `ppm` = la même valeur en parties par million (arrondie). `available_*` tient compte des plafonds.
    ///
    /// **Paginée sur les cartes visibles** (`limit` ≤ 200, 200 par défaut) : les sommes par rareté
    /// portent sur toute la table (données de tirage compactes, aucun bloc relu), mais `cards` ne
    /// liste que les cartes visibles d'index `from_index .. next_index` (les engagements
    /// mythiques, 20 au plus, sont toujours tous listés). Une table de 200 cartes au plus tient
    /// en une page. Page suivante : `from_index = next_index`, tant qu'il n'est pas `null`.
    pub fn get_rates(&self, series_id: u32, from_index: Option<u32>, limit: Option<u32>) -> Value {
        let s = self.series_ref(series_id);
        let (from, to) = self.page(series_id, from_index, limit.unwrap_or(MAX_CARDS_PER_CALL as u32));
        let page = self.cards_range(series_id, from, to);
        let t = &s.table;
        let total = t.rarity_weights.total();
        let burned = self.series_burns.get(&series_id).map(|b| b.burned.clone());
        let bp = crate::mechanics::burn_params(t);
        let (floor, prior_k) = bp.map(|b| (b.floor_bps, b.prior_k)).unwrap_or((0, 0));
        let resurrectable = crate::mechanics::resurrectable(t);
        let bv = burned.as_ref().map(|b| draw::BurnView { burned: b, floor_bps: floor, prior_k, resurrectable });
        let burn_f: Vec<draw::BurnFactors> = Rarity::ALL
            .iter()
            .map(|r| bv.as_ref().map(|bv| draw::burn_factors(&s.draw_cards, &s.minted, bv, *r)).unwrap_or_default())
            .collect();
        let rarities: Vec<Value> = Rarity::ALL
            .iter()
            .map(|r| {
                let rw = t.rarity_weights.get(*r) as u64;
                let (sum, cards): (u64, Vec<Value>) = if *r == Rarity::Mythic {
                    let sum: u64 = t.mythics.iter().map(|m| m.weight as u64).sum();
                    let cards = t
                        .mythics
                        .iter()
                        .enumerate()
                        .map(|(j, m)| {
                            json!({
                                "mythic_index": j, "commitment": m.commitment, "weight": m.weight,
                                "cap": m.cap, "minted": s.mythic_minted[j],
                                "ppm": ppm(rw, total, m.weight as u64, sum),
                                "ppb": scaled(rw, total, m.weight as u64, sum, 1_000_000_000),
                            })
                        })
                        .collect();
                    (sum, cards)
                } else {
                    let sum: u64 =
                        s.draw_cards.iter().filter(|c| c.rarity == *r).map(|c| c.weight as u64).sum();
                    let cards = page
                        .iter()
                        .enumerate()
                        .filter(|(_, c)| c.rarity == *r)
                        .map(|(k, c)| {
                            let i = from as usize + k;
                            json!({
                                "index": i, "card_id": c.card_id, "weight": c.weight, "cap": c.cap,
                                "minted": s.minted[i],
                                "burnable": c.backing.is_some() || self.resurrected.contains_key(&(series_id, i as u32)),
                                "ppm": ppm(rw, total, c.weight as u64, sum),
                                "ppb": scaled(rw, total, c.weight as u64, sum, 1_000_000_000),
                                // Poids dans la rareté (renormalisé entre brûlables) et part en ppm de la rareté.
                                "effective_weight": bv.as_ref().map(|bv| U128(draw::in_rarity_weight(&s.draw_cards[i], i, s.minted[i], bv, burn_f[r.index()]))),
                            })
                        })
                        .collect();
                    (sum, cards)
                };
                json!({
                    "rarity": r.as_str(),
                    "rarity_weight": rw,
                    "total_rarity_weight": total,
                    "rarity_ppm": if total == 0 { 0 } else { rw * 1_000_000 / total },
                    // Parties par milliard : la mythique (5 sur 2·10⁷ par emplacement) vaut 0 ppm arrondi.
                    "rarity_ppb": if total == 0 { 0 } else { (rw as u128 * 1_000_000_000 / total as u128) as u64 },
                    "rarity_card_weight": sum,
                    "available_card_weight": draw::available_weight_compact(&s.draw_cards, &t.mythics, &s.minted, &s.mythic_minted, *r),
                    // Rareté pilotée par les burns : somme des poids renormalisés (modulo de card_roll).
                    "effective_card_weight": bv.as_ref().map(|bv| U128(draw::available_weight_mech(&s.draw_cards, &t.mythics, &s.minted, &s.mythic_minted, Some(bv), *r))),
                    "rush_rarity_ppm": t.mechanics.as_ref().and_then(|m| m.rush.as_ref()).map(|x| rarity_ppm(&x.weights, *r)),
                    "rush_rarity_ppb": t.mechanics.as_ref().and_then(|m| m.rush.as_ref()).map(|x| rarity_scaled(&x.weights, *r, 1_000_000_000)),
                    // Gold pack : probabilité visée de la rareté, emplacement par emplacement (plancher compris).
                    "gold_slot_ppm": t.mechanics.as_ref().and_then(|m| m.gold.as_ref()).map(|g| g.slots.iter().map(|gs| rarity_ppm(&draw::gold_slot_weights(&t.rarity_weights, gs), *r)).collect::<Vec<_>>()),
                    "gold_slot_ppb": t.mechanics.as_ref().and_then(|m| m.gold.as_ref()).map(|g| g.slots.iter().map(|gs| rarity_scaled(&draw::gold_slot_weights(&t.rarity_weights, gs), *r, 1_000_000_000)).collect::<Vec<_>>()),
                    "cards": cards,
                })
            })
            .collect();
        let n = s.draw_cards.len() as u32;
        json!({
            "series_id": series_id,
            "table_hash": s.table_hash.map(|h| hex32(&h)),
            "card_count": n,
            "from_index": from,
            "next_index": if to < n { Some(to) } else { None },
            "rarities": rarities,
        })
    }

    pub fn get_pack(&self, pack_id: u64) -> Option<Value> {
        let p = self.packs.get(&pack_id)?;
        let s = self.series_ref(p.series_id);
        let draws: Vec<DrawRecord> = p
            .draws
            .iter()
            .enumerate()
            .map(|(slot, d)| DrawRecord {
                slot: slot as u8,
                rarity_roll: U128(d.rarity_roll as u128),
                rolled_rarity: d.rolled_rarity,
                final_rarity: d.final_rarity,
                card_roll: U128(d.card_roll),
                kind: d.kind,
                index: d.index,
                token_id: token_id_of(pack_id, slot as u8),
            })
            .collect();
        let token_ids: Vec<TokenId> = (0..p.cards.len()).map(|i| token_id_of(pack_id, i as u8)).collect();
        Some(json!({
            "pack_id": pack_id,
            "series_id": p.series_id,
            "owner_id": p.owner_id,
            // Prix et stockage de la série (figés à l'ouverture) : plus stockés par pack.
            "price_paid": s.table.price,
            "storage_prepaid": U128(env::storage_byte_cost().as_yoctonear() * s.storage_per_pack as u128),
            // Stockage mesuré du pack (octets) ; au tirage, `storage_prepaid` moins ce montant est rendu.
            "storage_used": p.storage_used,
            "bought_at_height": p.bought_at_height,
            "status": p.status,
            "attempt": p.attempt,
            "step": p.step,
            "acc": hex32(&p.acc),
            "last_progress_height": p.last_progress_height,
            "seeds": Self::seeds_json(pack_id, p, &s.table_hash.unwrap_or([0; 32])),
            "token_ids": token_ids,
            "draws": draws,
            "rush": p.flags & FLAG_RUSH != 0,
            "mode": p.mode(),
            // Valeur tirée (série à table de valeur) : points de base du prix et part de chaque emplacement.
            "value": p.value.map(|v| json!({
                "bps": v.bps,
                "total": U128(draw::value_total(s.table.price.0, v.bps)),
                "amounts": (0..p.draws.len()).map(|i| self.slot_value(p, i).map(U128)).collect::<Vec<_>>(),
            })),
        }))
    }

    /// Nombre de boosters achetés par un compte.
    pub fn get_pack_count_for_owner(&self, account_id: AccountId) -> u32 {
        self.pack_count_by_owner.get(&account_id).copied().unwrap_or(0)
    }

    /// Boosters d'un compte, paginés (ordre d'achat ; `limit` ≤ 100, 50 par défaut).
    pub fn get_packs_for_owner(&self, account_id: AccountId, from_index: Option<u32>, limit: Option<u32>) -> Vec<u64> {
        let count = self.pack_count_by_owner.get(&account_id).copied().unwrap_or(0);
        let from = from_index.unwrap_or(0).min(count);
        let to = from.saturating_add(limit.unwrap_or(50).min(100)).min(count);
        let mut out = Vec::new();
        let mut i = from;
        while i < to {
            let Some(chunk) = self.owner_packs.get(&(account_id.clone(), i / OWNER_CHUNK)) else { break };
            let lo = (i % OWNER_CHUNK) as usize;
            let hi = (lo + (to - i) as usize).min(chunk.len());
            if hi <= lo {
                break;
            }
            out.extend_from_slice(&chunk[lo..hi]);
            i += (hi - lo) as u32;
        }
        out
    }

    pub fn get_card(&self, token_id: TokenId) -> Option<CardView> {
        let (_, slot, pack) = self.live(&token_id)?;
        let d = pack.draws[slot];
        let owner_id = pack.cards[slot].owner.clone().unwrap_or_else(|| pack.owner_id.clone());
        let s = self.series_ref(pack.series_id);
        // Mythique : ni `card_id` ni adossement, même après la révélation (rien ne trahit le coin ;
        // `sealed` dit seulement si l'engagement a été ouvert, `get_backing` reste la vue du burn).
        let (card_id, sealed, backing) = match d.kind {
            CardKind::Visible => (Some(self.card_def(pack.series_id, d.index).card_id), false, self.slot_backing(pack, slot)),
            CardKind::Mythic => (None, s.revealed_mythics[d.index as usize].is_none(), None),
        };
        Some(CardView {
            token_id: token_id.clone(),
            owner_id,
            series_id: pack.series_id,
            kind: d.kind,
            index: d.index,
            card_id,
            rarity: d.final_rarity,
            state: pack.cards[slot].state,
            sealed,
            backing,
            listing: self.listings.get(&token_id).cloned(),
        })
    }

    /// Adossement courant d'une carte (table, résurrection, ou mythique révélée).
    pub fn get_backing(&self, token_id: TokenId) -> Option<Backing> {
        self.token_backing(&token_id)
    }

    pub fn get_listing(&self, token_id: TokenId) -> Option<Listing> {
        self.listings.get(&token_id).cloned()
    }

    pub fn get_listings(&self, from_index: Option<u32>, limit: Option<u32>) -> Vec<(TokenId, Listing)> {
        self.listings
            .iter()
            .skip(from_index.unwrap_or(0) as usize)
            .take(limit.unwrap_or(50) as usize)
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect()
    }
}

impl Contract {
    /// Bornes `[from, to)` d'une page de cartes visibles (`limit` plafonné à 200).
    fn page(&self, series_id: u32, from_index: Option<u32>, limit: u32) -> (u32, u32) {
        let n = self.series_ref(series_id).draw_cards.len() as u32;
        let from = from_index.unwrap_or(0).min(n);
        (from, from.saturating_add(limit.min(MAX_CARDS_PER_CALL as u32)).min(n))
    }

    /// Cartes visibles d'index `from .. to`, bloc par bloc (chaque bloc lu une fois).
    fn cards_range(&self, series_id: u32, from: u32, to: u32) -> Vec<CardDef> {
        let mut out = Vec::with_capacity((to - from) as usize);
        let mut i = from;
        while i < to {
            let chunk = self
                .series_cards
                .get(&(series_id, i / CARDS_PER_CHUNK))
                .unwrap_or_else(|| env::panic_str("E_INTERNAL: Bloc de cartes manquant"));
            let lo = (i % CARDS_PER_CHUNK) as usize;
            let hi = (lo + (to - i) as usize).min(chunk.len());
            require!(hi > lo, "E_INTERNAL: Blocs de cartes incohérents");
            out.extend_from_slice(&chunk[lo..hi]);
            i += (hi - lo) as u32;
        }
        out
    }
}

fn ppm(rw: u64, total: u64, w: u64, sum: u64) -> u64 {
    scaled(rw, total, w, sum, 1_000_000)
}

/// `rw / total × w / sum × unit`, arrondi vers le bas, en u128 : `rw, w < 2³²`, `total, sum < 2⁴²`
/// (2 000 cartes de poids u32 au plus), `unit ≤ 10⁹`, donc le produit reste sous 2⁹⁴.
fn scaled(rw: u64, total: u64, w: u64, sum: u64, unit: u128) -> u64 {
    if total == 0 || sum == 0 {
        return 0;
    }
    ((rw as u128 * w as u128 * unit) / (total as u128 * sum as u128)) as u64
}

fn rarity_ppm(w: &RarityWeights, r: Rarity) -> u64 {
    rarity_scaled(w, r, 1_000_000)
}

fn rarity_scaled(w: &RarityWeights, r: Rarity, unit: u128) -> u64 {
    let total = w.total();
    if total == 0 {
        0
    } else {
        (w.get(r) as u128 * unit / total as u128) as u64
    }
}
