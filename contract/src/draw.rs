//! Tirage pur et déterministe à partir de `acc`. Aucune dépendance à l'état :
//! le même code sert aux tests et au vérificateur public (à réécrire en JS/Python).
//!
//! Pour l'emplacement `slot` d'un booster :
//! 1. `rarity_roll = u128_be(sha256(acc || slot || 0x00)[0..16]) mod total_rarity_weight`
//!    choisit la rareté visée par cumul dans l'ordre mythique → commune ;
//! 2. si aucune carte n'est disponible dans cette rareté (poids nul ou plafond atteint),
//!    on descend à la rareté inférieure, jusqu'à commune (qui a toujours une carte illimitée) ;
//! 3. `card_roll = u128_be(sha256(acc || slot || 0x01)[0..16]) mod somme_des_poids_disponibles`
//!    choisit la carte par cumul, dans l'ordre de la table.
//!
//! Mécaniques (`docs/mechanics.md`), toutes désactivées pour une table sans `mechanics` :
//! - la table de poids de rareté du pack (base, or, rush) est choisie avant les emplacements ;
//!   pitié : `gold_roll = u128_be(sha256(acc || 0x00 || 0x02)[0..16]) mod 10⁹` ;
//! - rareté pilotée par les burns : le tirage de rareté ne change pas ; dans la rareté, les
//!   brûlables prennent un poids brut `max(⌊w × (e − b + K) / (e + K)⌋, ⌊w × plancher⌋, 1)` renormalisé pour
//!   que leur part totale reste celle de leurs poids de base (`in_rarity_weight`) ;
//! - gold rush : palier relatif sur fenêtre glissante par seaux (`rush_on_buy`), figé à l'achat ;
//! - gold pack : plancher de rareté par emplacement (`draw_slot_rule`, `fallback_order`) ;
//! - valeur du pack : `value_roll = roll(acc, 0, 3)` choisit un palier de la table du pack
//!   (`value_tier`), réparti entre les brûlables (`split_value`) ; le dernier emplacement d'un pack
//!   normal est tiré parmi les brûlables (`draw_slot_rule` avec `burnable_only`).

use crate::types::{
    CardKind, DrawCard, GoldSlot, MythicCommitment, PackKind, PackMode, PityParams, Rarity, RarityWeights, RushParams,
    RushState, SeriesTable, ValueParams, ValueTier,
};
use near_sdk::env;
use std::borrow::Cow;

/// Tags de `roll` : rareté et carte (par emplacement), gold pack et valeur (emplacement 0).
pub const TAG_RARITY: u8 = 0;
pub const TAG_CARD: u8 = 1;
pub const TAG_GOLD: u8 = 2;
pub const TAG_VALUE: u8 = 3;
pub const PPM: u64 = 1_000_000;
/// Résolution de la pitié : parties par milliard (1 sur 50 000 = 20 000 ppb).
pub const PPB: u64 = 1_000_000_000;

pub fn roll(acc: &[u8; 32], slot: u8, tag: u8) -> u128 {
    let mut buf = Vec::with_capacity(34);
    buf.extend_from_slice(acc);
    buf.push(slot);
    buf.push(tag);
    let h = env::sha256_array(&buf);
    let mut b = [0u8; 16];
    b.copy_from_slice(&h[..16]);
    u128::from_be_bytes(b)
}

/// Accumulateur : `acc = sha256(acc || seed || pack_id_le || owner)`.
pub fn mix(acc: &[u8; 32], seed: &[u8; 32], pack_id: u64, owner: &str) -> [u8; 32] {
    let mut buf = Vec::with_capacity(72 + owner.len());
    buf.extend_from_slice(acc);
    buf.extend_from_slice(seed);
    buf.extend_from_slice(&pack_id.to_le_bytes());
    buf.extend_from_slice(owner.as_bytes());
    env::sha256_array(&buf)
}

/// Valeur initiale : `acc0 = sha256("memaster:pack" || pack_id_le || owner || table_hash)`.
pub fn initial_acc(pack_id: u64, owner: &str, table_hash: &[u8; 32]) -> [u8; 32] {
    let mut buf = Vec::new();
    buf.extend_from_slice(b"memaster:pack");
    buf.extend_from_slice(&pack_id.to_le_bytes());
    buf.extend_from_slice(owner.as_bytes());
    buf.extend_from_slice(table_hash);
    env::sha256_array(&buf)
}

fn available(weight: u32, minted: u32, cap: Option<u32>) -> u64 {
    if weight == 0 || cap.is_some_and(|c| minted >= c) {
        0
    } else {
        weight as u64
    }
}

/// Somme des poids encore tirables dans une rareté.
pub fn available_weight(
    table: &SeriesTable,
    minted: &[u32],
    mythic_minted: &[u32],
    rarity: Rarity,
) -> u64 {
    let cards: Vec<DrawCard> = table.cards.iter().map(DrawCard::from).collect();
    available_weight_compact(&cards, &table.mythics, minted, mythic_minted, rarity)
}

/// Même calcul que `available_weight`, sur les données de tirage compactes de la série.
pub fn available_weight_compact(
    cards: &[DrawCard],
    mythics: &[MythicCommitment],
    minted: &[u32],
    mythic_minted: &[u32],
    rarity: Rarity,
) -> u64 {
    if rarity == Rarity::Mythic {
        mythics
            .iter()
            .zip(mythic_minted)
            .map(|(m, n)| available(m.weight, *n, Some(m.cap)))
            .sum()
    } else {
        cards
            .iter()
            .zip(minted)
            .filter(|(c, _)| c.rarity == rarity)
            .map(|(c, n)| available(c.weight, *n, c.cap))
            .sum()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SlotDraw {
    pub rarity_roll: u128,
    pub rolled_rarity: Rarity,
    pub final_rarity: Rarity,
    pub card_roll: u128,
    pub kind: CardKind,
    pub index: u32,
}

/// Tire un emplacement. Ne panique jamais si la table a été validée
/// (au moins une commune illimitée de poids non nul).
pub fn draw_slot(
    table: &SeriesTable,
    minted: &[u32],
    mythic_minted: &[u32],
    acc: &[u8; 32],
    slot: u8,
) -> SlotDraw {
    let cards: Vec<DrawCard> = table.cards.iter().map(DrawCard::from).collect();
    draw_slot_compact(&table.rarity_weights, &cards, &table.mythics, minted, mythic_minted, acc, slot)
}

/// `draw_slot` sur les données compactes (`Series::draw_cards`) : résultat identique, sans
/// charger les métadonnées des cartes. C'est la fonction appelée par le contrat.
pub fn draw_slot_compact(
    weights: &RarityWeights,
    cards: &[DrawCard],
    mythics: &[MythicCommitment],
    minted: &[u32],
    mythic_minted: &[u32],
    acc: &[u8; 32],
    slot: u8,
) -> SlotDraw {
    draw_slot_mech(weights, cards, mythics, minted, mythic_minted, None, acc, slot)
}

/// Compteurs de burn d'une série, plancher, a priori et cartes ressuscitables (rareté pilotée par
/// les burns).
#[derive(Clone, Copy, Debug)]
pub struct BurnView<'a> {
    pub burned: &'a [u32],
    pub floor_bps: u32,
    /// A priori `K` : `K` exemplaires fictifs émis et jamais brûlés, ajoutés à chaque carte.
    pub prior_k: u32,
    /// Index des cartes ressuscitables de la table (`mechanics.resurrection.eligible`, croissants).
    /// Une carte brûlable de cette liste a été ressuscitée par l'oracle (elle n'était pas adossée).
    pub resurrectable: &'a [u32],
}

impl BurnView<'_> {
    /// Brûlable par résurrection (et non par la table).
    pub fn resurrected(&self, i: usize, c: &DrawCard) -> bool {
        c.backed && self.resurrectable.binary_search(&(i as u32)).is_ok()
    }
}

/// Poids brut d'une brûlable : 0 si épuisée (plafond) ou de poids nul ; `w` si aucune émise ;
/// sinon `max(⌊w × (e − b + K) / (e + K)⌋, ⌊w × floor_bps / 10⁴⌋, 1)` (calcul en u128), avec
/// `e` émises, `b` brûlées et `K` l'a priori (lissage : quelques burns en début de série ne
/// font presque rien bouger).
pub fn raw_burn_weight(weight: u32, minted: u32, burned: u32, cap: Option<u32>, floor_bps: u32, prior_k: u32) -> u64 {
    if weight == 0 || cap.is_some_and(|c| minted >= c) {
        return 0;
    }
    if minted == 0 {
        return weight as u64;
    }
    let k = prior_k as u128;
    let circ = minted.saturating_sub(burned) as u128 + k;
    let ratio = (weight as u128 * circ / (minted as u128 + k)) as u64;
    ratio.max(floor_weight(weight, floor_bps))
}

fn floor_weight(weight: u32, floor_bps: u32) -> u64 {
    ((weight as u128 * floor_bps as u128 / 10_000) as u64).max(1)
}

/// Facteurs d'une rareté pour les burns.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct BurnFactors {
    /// Σ poids bruts des brûlables (adossées par la table et ressuscitées).
    pub e: u128,
    /// Σ poids disponibles (de base) des brûlables.
    pub b: u128,
    /// Mêmes sommes sur les seules brûlables adossées par la table : leur ratio moyen
    /// `e0 / b0` sert aux cartes ressuscitées.
    pub e0: u128,
    pub b0: u128,
}

/// Poids brut d'une brûlable dans sa rareté. Adossée par la table : `raw_burn_weight`. Ressuscitée :
/// le **ratio moyen** des brûlables de la table dans la rareté, `max(⌊w × e0 / b0⌋, plancher)`,
/// borné par son propre poids brut (ses burns depuis la résurrection la font encore baisser) ;
/// son propre poids brut si la rareté n'a aucune brûlable de table. Une carte ressuscitée après
/// des burns ne prend donc pas plus que sa part de base parmi les brûlables.
pub fn burnable_raw(c: &DrawCard, i: usize, minted: u32, burned: u32, bv: &BurnView, e0: u128, b0: u128) -> u64 {
    let own = raw_burn_weight(c.weight, minted, burned, c.cap, bv.floor_bps, bv.prior_k);
    if own == 0 || b0 == 0 || !bv.resurrected(i, c) {
        return own;
    }
    let mean = ((c.weight as u128 * e0 / b0) as u64).max(floor_weight(c.weight, bv.floor_bps));
    own.min(mean)
}

/// Facteurs d'une rareté. Poids dans la rareté : non brûlable `a × E` (`a` si `E = 0`), brûlable
/// `brut × B`. La part des brûlables vaut donc exactement `B / (B + Σ a des non brûlables)`, comme
/// sans burn : le poids perdu par une brûlable très brûlée revient aux autres brûlables de la rareté.
pub fn burn_factors(cards: &[DrawCard], minted: &[u32], bv: &BurnView, rarity: Rarity) -> BurnFactors {
    let mut f = BurnFactors::default();
    let burned = |i: usize| bv.burned.get(i).copied().unwrap_or(0);
    for (i, (c, n)) in cards.iter().zip(minted).enumerate() {
        if c.rarity != rarity || !c.backed || bv.resurrected(i, c) {
            continue;
        }
        f.e0 += raw_burn_weight(c.weight, *n, burned(i), c.cap, bv.floor_bps, bv.prior_k) as u128;
        f.b0 += available(c.weight, *n, c.cap) as u128;
    }
    f.e = f.e0;
    f.b = f.b0;
    for (i, (c, n)) in cards.iter().zip(minted).enumerate() {
        if c.rarity != rarity || !bv.resurrected(i, c) {
            continue;
        }
        f.e += burnable_raw(c, i, *n, burned(i), bv, f.e0, f.b0) as u128;
        f.b += available(c.weight, *n, c.cap) as u128;
    }
    f
}

/// Poids de la carte visible `i` dans sa rareté (rareté pilotée par les burns), avec les facteurs
/// de `burn_factors`.
pub fn in_rarity_weight(c: &DrawCard, i: usize, minted: u32, bv: &BurnView, f: BurnFactors) -> u128 {
    if c.backed {
        if f.e == 0 {
            0
        } else {
            let burned = bv.burned.get(i).copied().unwrap_or(0);
            burnable_raw(c, i, minted, burned, bv, f.e0, f.b0) as u128 * f.b
        }
    } else {
        let a = available(c.weight, minted, c.cap) as u128;
        if f.e == 0 {
            a
        } else {
            a * f.e
        }
    }
}

/// Somme des poids tirables d'une rareté, avec ou sans burns (`bv = None` : poids de base).
pub fn available_weight_mech(
    cards: &[DrawCard],
    mythics: &[MythicCommitment],
    minted: &[u32],
    mythic_minted: &[u32],
    bv: Option<&BurnView>,
    rarity: Rarity,
) -> u128 {
    match bv {
        Some(bv) if rarity != Rarity::Mythic => {
            let f = burn_factors(cards, minted, bv, rarity);
            cards
                .iter()
                .zip(minted)
                .enumerate()
                .filter(|(_, (c, _))| c.rarity == rarity)
                .map(|(i, (c, n))| in_rarity_weight(c, i, *n, bv, f))
                .sum()
        }
        _ => available_weight_compact(cards, mythics, minted, mythic_minted, rarity) as u128,
    }
}

/// Tirage d'un emplacement avec les mécaniques : `weights` est la table de rareté du pack (base,
/// or ou rush), `bv` les compteurs de burn (rareté pilotée par les burns) ou `None`.
/// Avec `bv = None`, identique à `draw_slot_compact` au bit près. Le tirage de rareté
/// (`rarity_roll`) ne dépend jamais des burns : seuls le choix de la carte et la retombée
/// (rareté épuisée) les voient.
#[allow(clippy::too_many_arguments)]
pub fn draw_slot_mech(
    weights: &RarityWeights,
    cards: &[DrawCard],
    mythics: &[MythicCommitment],
    minted: &[u32],
    mythic_minted: &[u32],
    bv: Option<&BurnView>,
    acc: &[u8; 32],
    slot: u8,
) -> SlotDraw {
    let total = weights.total().max(1) as u128;
    let rarity_roll = roll(acc, slot, TAG_RARITY) % total;
    let mut cum: u128 = 0;
    let mut rolled = Rarity::Common;
    for r in Rarity::ALL {
        cum += weights.get(r) as u128;
        if rarity_roll < cum {
            rolled = r;
            break;
        }
    }

    // Retombée sur la rareté inférieure si épuisée.
    let avail = |r| available_weight_mech(cards, mythics, minted, mythic_minted, bv, r);
    let mut final_rarity = rolled;
    let mut sum = avail(final_rarity);
    while sum == 0 {
        match final_rarity.lower() {
            Some(l) => {
                final_rarity = l;
                sum = avail(final_rarity);
            }
            None => break,
        }
    }

    let raw_card = roll(acc, slot, TAG_CARD);
    let card_roll = if sum == 0 { 0 } else { raw_card % sum };

    let (kind, index) = if final_rarity == Rarity::Mythic {
        let mut c: u128 = 0;
        let mut pick = 0u32;
        for (j, (m, n)) in mythics.iter().zip(mythic_minted).enumerate() {
            c += available(m.weight, *n, Some(m.cap)) as u128;
            if card_roll < c {
                pick = j as u32;
                break;
            }
        }
        (CardKind::Mythic, pick)
    } else {
        let mut c: u128 = 0;
        let mut pick = first_unlimited_common(cards);
        let f = bv.map(|bv| burn_factors(cards, minted, bv, final_rarity));
        for (i, (card, n)) in cards.iter().zip(minted).enumerate() {
            if card.rarity != final_rarity {
                continue;
            }
            c += match (bv, f) {
                (Some(bv), Some(f)) => in_rarity_weight(card, i, *n, bv, f),
                _ => available(card.weight, *n, card.cap) as u128,
            };
            if card_roll < c {
                pick = i as u32;
                break;
            }
        }
        (CardKind::Visible, pick)
    };

    SlotDraw { rarity_roll, rolled_rarity: rolled, final_rarity, card_roll, kind, index }
}

/// Filet de sécurité : la première commune illimitée (garantie par la validation).
fn first_unlimited_common(cards: &[DrawCard]) -> u32 {
    cards
        .iter()
        .position(|c| c.rarity == Rarity::Common && c.cap.is_none() && c.weight > 0)
        .unwrap_or(0) as u32
}

// ------------------------------------------------------------------ mécaniques

/// Probabilité (ppb) d'un gold pack après `n` packs consécutifs sans gold pack :
/// `min(p_max_ppb, p0_ppb + k_ppb × n)` (calcul en u128, sans dépassement ; ≤ 10⁹ par validation).
pub fn pity_p_ppb(p: &PityParams, n: u32) -> u64 {
    let x = p.p0_ppb as u128 + p.k_ppb as u128 * n as u128;
    x.min(p.p_max_ppb as u128).min(PPB as u128) as u64
}

/// `gold_roll = u128_be(sha256(acc || 0x00 || 0x02)[0..16]) mod 10⁹`.
pub fn gold_roll(acc: &[u8; 32]) -> u64 {
    (roll(acc, 0, TAG_GOLD) % PPB as u128) as u64
}

/// Pitié : (gold pack ?, gold_roll, probabilité en ppb). Gold pack si `gold_roll < p(n)`, ou si la
/// garantie optionnelle `n_max` est atteinte (`n + 1 ≥ n_max`).
pub fn pity_is_gold(p: &PityParams, n: u32, acc: &[u8; 32]) -> (bool, u64, u64) {
    let r = gold_roll(acc);
    let pp = pity_p_ppb(p, n);
    let guaranteed = p.n_max.is_some_and(|m| n.saturating_add(1) >= m);
    (guaranteed || r < pp, r, pp)
}

/// Compteur après le tirage : 0 après un gold pack, `n + 1` sinon (pack normal ou rush).
pub fn pity_after(n: u32, gold: bool) -> u32 {
    if gold {
        0
    } else {
        n.saturating_add(1)
    }
}

/// Table de taux du pack : la pitié prime (table or), puis le rush (sa propre table), sinon la base.
pub fn pack_mode(pity_gold: bool, rush: bool) -> PackMode {
    if pity_gold {
        PackMode::Gold
    } else if rush {
        PackMode::Rush
    } else {
        PackMode::Base
    }
}

/// Poids de rareté d'un pack normal selon sa table (base ou rush ; retombe sur la base si la
/// table manque). Un gold pack tire chaque emplacement avec `gold_slot_weights`.
pub fn mode_weights(t: &SeriesTable, mode: PackMode) -> &RarityWeights {
    let m = t.mechanics.as_ref();
    match mode {
        PackMode::Base | PackMode::Gold => &t.rarity_weights,
        PackMode::Rush => m.and_then(|m| m.rush.as_ref()).map(|r| &r.weights).unwrap_or(&t.rarity_weights),
    }
}

// ------------------------------------------------------------------ gold pack et brûlable garantie

/// Poids d'un emplacement de gold pack : les siens, ou les poids de base mis à zéro sous le plancher.
pub fn gold_slot_weights(base: &RarityWeights, s: &GoldSlot) -> RarityWeights {
    if let Some(w) = &s.weights {
        return w.clone();
    }
    let keep = |r: Rarity, x: u32| if r.index() <= s.floor.index() { x } else { 0 };
    RarityWeights {
        mythic: keep(Rarity::Mythic, base.mythic),
        legendary: keep(Rarity::Legendary, base.legendary),
        epic: keep(Rarity::Epic, base.epic),
        rare: keep(Rarity::Rare, base.rare),
        common: keep(Rarity::Common, base.common),
    }
}

/// Ordre de retombée d'un emplacement à plancher : la rareté visée, puis vers le bas jusqu'au
/// plancher, puis vers le haut (au-dessus de la visée, jusqu'à la mythique), puis sous le plancher
/// (jusqu'à la commune) en dernier recours. Avec le plancher commune : vers le bas, puis vers le haut.
pub fn fallback_order(rolled: Rarity, floor: Rarity) -> Vec<Rarity> {
    let f = floor.index();
    let r = rolled.index().min(f);
    let mut v = Vec::with_capacity(5);
    v.extend((r..=f).map(|i| Rarity::ALL[i]));
    v.extend((0..r).rev().map(|i| Rarity::ALL[i]));
    v.extend((f + 1..5).map(|i| Rarity::ALL[i]));
    v
}

/// Poids tirables des seules brûlables (adossées par la table ou ressuscitées) d'une rareté. Une
/// mythique n'est jamais comptée : son adossement est dans son contenu, secret jusqu'à la révélation.
pub fn burnable_weight(cards: &[DrawCard], minted: &[u32], bv: Option<&BurnView>, rarity: Rarity) -> u128 {
    if rarity == Rarity::Mythic {
        return 0;
    }
    let f = bv.map(|bv| burn_factors(cards, minted, bv, rarity));
    cards
        .iter()
        .zip(minted)
        .enumerate()
        .filter(|(_, (c, _))| c.rarity == rarity && c.backed)
        .map(|(i, (c, n))| match (bv, f) {
            (Some(bv), Some(f)) => in_rarity_weight(c, i, *n, bv, f),
            _ => available(c.weight, *n, c.cap) as u128,
        })
        .sum()
}

/// Tirage d'un emplacement à règle : rareté visée avec `weights`, retombée selon
/// `fallback_order(visée, floor)` sur la première rareté qui a une carte tirable (une brûlable si
/// `burnable_only`), puis choix de la carte comme `draw_slot_mech` (mêmes tags, mêmes poids dans la
/// rareté, restreints aux brûlables si `burnable_only`). Ne panique jamais ; si rien n'est tirable
/// (impossible pour une table validée), commune, `card_roll = 0`, première commune illimitée.
#[allow(clippy::too_many_arguments)]
pub fn draw_slot_rule(
    weights: &RarityWeights,
    floor: Rarity,
    burnable_only: bool,
    cards: &[DrawCard],
    mythics: &[MythicCommitment],
    minted: &[u32],
    mythic_minted: &[u32],
    bv: Option<&BurnView>,
    acc: &[u8; 32],
    slot: u8,
) -> SlotDraw {
    let total = weights.total().max(1) as u128;
    let rarity_roll = roll(acc, slot, TAG_RARITY) % total;
    let mut cum: u128 = 0;
    let mut rolled = Rarity::Common;
    for r in Rarity::ALL {
        cum += weights.get(r) as u128;
        if rarity_roll < cum {
            rolled = r;
            break;
        }
    }
    let avail = |r| {
        if burnable_only {
            burnable_weight(cards, minted, bv, r)
        } else {
            available_weight_mech(cards, mythics, minted, mythic_minted, bv, r)
        }
    };
    let mut final_rarity = Rarity::Common;
    let mut sum = 0;
    for r in fallback_order(rolled, floor) {
        let s = avail(r);
        if s > 0 {
            final_rarity = r;
            sum = s;
            break;
        }
    }
    let raw_card = roll(acc, slot, TAG_CARD);
    let card_roll = if sum == 0 { 0 } else { raw_card % sum };
    let (kind, index) = if final_rarity == Rarity::Mythic && sum > 0 {
        let mut c: u128 = 0;
        let mut pick = 0u32;
        for (j, (m, n)) in mythics.iter().zip(mythic_minted).enumerate() {
            c += available(m.weight, *n, Some(m.cap)) as u128;
            if card_roll < c {
                pick = j as u32;
                break;
            }
        }
        (CardKind::Mythic, pick)
    } else {
        let mut c: u128 = 0;
        let mut pick = first_unlimited_common(cards);
        let f = bv.map(|bv| burn_factors(cards, minted, bv, final_rarity));
        for (i, (card, n)) in cards.iter().zip(minted).enumerate() {
            if card.rarity != final_rarity || (burnable_only && !card.backed) {
                continue;
            }
            c += match (bv, f) {
                (Some(bv), Some(f)) => in_rarity_weight(card, i, *n, bv, f),
                _ => available(card.weight, *n, card.cap) as u128,
            };
            if card_roll < c {
                pick = i as u32;
                break;
            }
        }
        (CardKind::Visible, pick)
    };
    SlotDraw { rarity_roll, rolled_rarity: rolled, final_rarity, card_roll, kind, index }
}

// ------------------------------------------------------------------ types de packs

/// Type de pack d'un pack (`None` : pack de base, ou index hors de la table).
pub fn pack_kind(t: &SeriesTable, kind: Option<u32>) -> Option<&PackKind> {
    kind.and_then(|k| t.kinds.as_ref()?.get(k as usize))
}

/// Prix d'un pack : celui de son type, sinon celui de la série.
pub fn kind_price(t: &SeriesTable, kind: Option<&PackKind>) -> u128 {
    kind.map(|k| k.price.0).unwrap_or(t.price.0)
}

/// Cartes tirables d'un pack : poids à 0 hors de `kind.pool`. Les compteurs `minted` restent ceux
/// de la série : un type de pack ne réimprime rien, il puise dans les mêmes plafonds.
pub fn kind_cards<'a>(cards: &'a [DrawCard], kind: Option<&PackKind>) -> Cow<'a, [DrawCard]> {
    match kind {
        Some(k) if !k.pool.is_empty() => {
            let mut v: Vec<DrawCard> = cards.iter().map(|c| DrawCard { weight: 0, ..c.clone() }).collect();
            for &i in &k.pool {
                if let (Some(dst), Some(src)) = (v.get_mut(i as usize), cards.get(i as usize)) {
                    dst.weight = src.weight;
                }
            }
            Cow::Owned(v)
        }
        _ => Cow::Borrowed(cards),
    }
}

/// Poids de rareté d'un pack de ce type : mythique à 0 si le type exclut les mythiques.
pub fn kind_weights(w: &RarityWeights, kind: Option<&PackKind>) -> RarityWeights {
    let mut w = w.clone();
    if kind.is_some_and(|k| !k.mythics) {
        w.mythic = 0;
    }
    w
}

/// Tous les emplacements d'un pack, comme le dernier reçu : gold pack (un emplacement par entrée de
/// `mechanics.gold`, avec son plancher), sinon `cards_per_pack` emplacements avec la table de taux du
/// pack, le dernier tiré parmi les brûlables si la série a une table de valeur. `minted` et
/// `mythic_minted` sont incrémentés entre deux emplacements. Renvoie les tirages et, par emplacement,
/// (rareté finale, brûlable au tirage) pour la répartition de la valeur.
///
/// Pack d'un type (`kind`) : `cards` doit déjà être `kind_cards(…)` ; jamais de gold pack ;
/// `kind.cards_per_pack` emplacements ; mythiques exclues si `!kind.mythics` ; la règle de
/// l'emplacement `i` est `kind.slots[i]` (poids propres, ou poids du pack tronqués sous le plancher),
/// sinon la règle par défaut, dont la brûlable garantie au dernier emplacement si `kind.value`.
#[allow(clippy::too_many_arguments)]
pub fn draw_pack_mech(
    t: &SeriesTable,
    mode: PackMode,
    kind: Option<&PackKind>,
    cards: &[DrawCard],
    minted: &mut [u32],
    mythic_minted: &mut [u32],
    bv: Option<&BurnView>,
    acc: &[u8; 32],
) -> (Vec<SlotDraw>, Vec<(Rarity, bool)>) {
    let m = t.mechanics.as_ref();
    let gold = m.and_then(|m| m.gold.as_ref()).filter(|_| mode == PackMode::Gold && kind.is_none());
    let value = m.is_some_and(|m| m.value.is_some()) && kind.is_none_or(|k| k.value);
    let weights = kind_weights(mode_weights(t, mode), kind);
    let mythics: &[MythicCommitment] = if kind.is_some_and(|k| !k.mythics) { &[] } else { &t.mythics };
    let rules = kind.and_then(|k| k.slots.as_ref());
    let n = gold.map(|g| g.slots.len() as u8).unwrap_or(kind.map_or(t.cards_per_pack, |k| k.cards_per_pack));
    let mut draws = Vec::with_capacity(n as usize);
    let mut slots = Vec::with_capacity(n as usize);
    for slot in 0..n {
        let d = if let Some(g) = gold {
            let gs = &g.slots[slot as usize];
            let w = gold_slot_weights(&t.rarity_weights, gs);
            draw_slot_rule(&w, gs.floor, gs.burnable, cards, &t.mythics, minted, mythic_minted, bv, acc, slot)
        } else if let Some(rule) = rules.and_then(|r| r.get(slot as usize)) {
            let w = kind_weights(&gold_slot_weights(&weights, rule), kind);
            draw_slot_rule(&w, rule.floor, rule.burnable, cards, mythics, minted, mythic_minted, bv, acc, slot)
        } else if value && rules.is_none() && slot + 1 == n {
            draw_slot_rule(&weights, Rarity::Common, true, cards, mythics, minted, mythic_minted, bv, acc, slot)
        } else {
            draw_slot_mech(&weights, cards, mythics, minted, mythic_minted, bv, acc, slot)
        };
        slots.push((d.final_rarity, d.kind == CardKind::Visible && cards[d.index as usize].backed));
        match d.kind {
            CardKind::Visible => minted[d.index as usize] += 1,
            CardKind::Mythic => mythic_minted[d.index as usize] += 1,
        }
        draws.push(d);
    }
    (draws, slots)
}

// ------------------------------------------------------------------ valeur du pack

/// Valeur tirée d'un pack (série à table de valeur).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PackValueDraw {
    pub roll: u64,
    pub tier: u32,
    pub bps: u32,
    pub total: u128,
    pub amounts: Vec<Option<u128>>,
}

/// Palier, total et répartition d'un pack (`None` sans table de valeur).
pub fn pack_value(
    t: &SeriesTable,
    mode: PackMode,
    kind: Option<&PackKind>,
    acc: &[u8; 32],
    slots: &[(Rarity, bool)],
) -> Option<PackValueDraw> {
    let v = t.mechanics.as_ref()?.value.as_ref()?;
    if kind.is_some_and(|k| !k.value) {
        return None;
    }
    let (roll, tier, bps) = value_tier(value_table(v, mode), acc);
    let total = value_total(kind_price(t, kind), bps);
    Some(PackValueDraw { roll, tier, bps, total, amounts: split_value(total, slots, &v.multipliers) })
}

/// Table de valeur d'un pack selon sa table de taux.
pub fn value_table(v: &ValueParams, mode: PackMode) -> &[ValueTier] {
    match mode {
        PackMode::Base => &v.normal,
        PackMode::Gold => &v.gold,
        PackMode::Rush => &v.rush,
    }
}

/// `value_roll = u128_be(sha256(acc || 0x00 || 0x03)[0..16]) mod Σpoids`, palier choisi par cumul
/// dans l'ordre de la table. Renvoie (value_roll, index du palier, valeur en points de base).
pub fn value_tier(tiers: &[ValueTier], acc: &[u8; 32]) -> (u64, u32, u32) {
    let total: u128 = tiers.iter().map(|(_, w)| *w as u128).sum::<u128>().max(1);
    let r = roll(acc, 0, TAG_VALUE) % total;
    let mut cum = 0u128;
    for (i, (bps, w)) in tiers.iter().enumerate() {
        cum += *w as u128;
        if r < cum {
            return (r as u64, i as u32, *bps);
        }
    }
    (r as u64, 0, tiers.first().map(|t| t.0).unwrap_or(0))
}

/// `⌊prix × bps / 10⁴⌋`, calculé sans dépasser u128 (`prix = 10⁴ q + r`).
pub fn value_total(price: u128, bps: u32) -> u128 {
    (price / 10_000) * bps as u128 + (price % 10_000) * bps as u128 / 10_000
}

/// Répartition de `total` (yoctoNEAR) entre les emplacements brûlables (`slots[i] = (rareté, brûlable)`)
/// au prorata du multiplicateur de leur rareté : `⌊total × m_i / Σm⌋`, le reste à l'emplacement au plus
/// fort multiplicateur (le premier en cas d'égalité). `None` pour un emplacement non brûlable.
/// Sans brûlable (ou multiplicateurs nuls), rien n'est réparti.
pub fn split_value(total: u128, slots: &[(Rarity, bool)], mult: &RarityWeights) -> Vec<Option<u128>> {
    let sum: u128 = slots.iter().filter(|(_, b)| *b).map(|(r, _)| mult.get(*r) as u128).sum();
    if sum == 0 {
        return vec![None; slots.len()];
    }
    let mut out: Vec<Option<u128>> =
        slots.iter().map(|(r, b)| b.then(|| total * mult.get(*r) as u128 / sum)).collect();
    let given: u128 = out.iter().flatten().sum();
    let mut best: Option<usize> = None;
    for (i, (r, b)) in slots.iter().enumerate() {
        if *b && best.is_none_or(|j| mult.get(*r) > mult.get(slots[j].0)) {
            best = Some(i);
        }
    }
    if let Some(j) = best {
        out[j] = out[j].map(|x| x + (total - given));
    }
    out
}

/// Résultat de `rush_on_buy` pour un achat.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RushOutcome {
    /// Le pack acheté est un pack rush (figé à l'achat).
    pub active: bool,
    /// Packs achetés dans la fenêtre courte, celui-ci compris.
    pub window_count: u64,
    /// Packs achetés dans la fenêtre longue (24 h), celui-ci compris.
    pub baseline_count: u64,
    /// Cet achat déclenche un rush (actif pour les achats des `duration_blocks` blocs suivants).
    pub triggered: bool,
}

/// Achat à la hauteur `h` : met à jour la fenêtre glissante et dit si le pack est un pack rush.
///
/// - seaux de `B = bucket_blocks` blocs ; `m_w = window_blocks / B`, `m_l = baseline_blocks / B`
///   (≤ 96) ; le seau de `h` est `b = ⌊h / B⌋` ; une fenêtre de `m` seaux compte les achats des
///   seaux `b − m + 1 … b`, celui-ci compris (`C_w`, `C_l`) ;
/// - le pack est rush si un déclenchement a eu lieu à `t` avec `t < h ≤ t + D` ;
/// - l'achat déclenche un rush (`t = h`) si : aucun rush ni pause en cours
///   (`h > t + D + cooldown`, ou aucun déclenchement), `h ≥ premier achat + baseline_blocks`
///   (fenêtre longue remplie), `C_w ≥ min_packs` et `C_w × m_l × 10⁴ ≥ ratio_bps × C_l × m_w`
///   (rythme court ≥ ratio × rythme moyen sur la fenêtre longue).
///
/// Coût borné : `m_l` entrées lues, une écrite.
pub fn rush_on_buy(p: &RushParams, st: &mut RushState, h: u64) -> RushOutcome {
    let bsz = p.bucket_blocks.max(1);
    let ml = (p.baseline_blocks / bsz).max(1);
    let mw = (p.window_blocks / bsz).clamp(1, ml);
    if st.ring.len() as u64 != ml {
        st.ring = vec![(u64::MAX, 0); ml as usize];
    }
    let start = *st.start_height.get_or_insert(h);
    let in_period = st.last_trigger.is_some_and(|t| h <= t.saturating_add(p.duration_blocks));
    let active = in_period && st.last_trigger.is_some_and(|t| h > t);
    let paused = st
        .last_trigger
        .is_some_and(|t| h <= t.saturating_add(p.duration_blocks).saturating_add(p.cooldown_blocks));
    let b = h / bsz;
    let i = (b % ml) as usize;
    if st.ring[i].0 != b {
        st.ring[i] = (b, 0);
    }
    st.ring[i].1 = st.ring[i].1.saturating_add(1);
    let ring = &st.ring;
    let count = |m: u64| -> u64 { ring.iter().filter(|(bb, _)| *bb <= b && b - *bb < m).map(|(_, c)| *c as u64).sum() };
    let (cw, cl) = (count(mw), count(ml));
    let warm = h >= start.saturating_add(p.baseline_blocks);
    let triggered = !paused
        && warm
        && cw >= p.min_packs as u64
        && cw as u128 * ml as u128 * 10_000 >= p.ratio_bps as u128 * cl as u128 * mw as u128;
    if triggered {
        st.last_trigger = Some(h);
        st.rush_count += 1;
    }
    RushOutcome { active, window_count: cw, baseline_count: cl, triggered }
}

/// Plafond de packs rush par compte et par rush. `prev` = (déclenchement, packs rush du compte
/// pendant ce rush) avant l'achat. Renvoie (pack rush ?, plafonné ?, nouvel état du compte).
/// Hors rush, rien ne change. Le compteur repart de zéro à chaque nouveau déclenchement.
pub fn rush_account(p: &RushParams, active: bool, trigger: Option<u64>, prev: Option<(u64, u32)>) -> (bool, bool, Option<(u64, u32)>) {
    let Some(t) = trigger.filter(|_| active) else {
        return (false, false, prev);
    };
    let n = prev.filter(|(pt, _)| *pt == t).map(|(_, n)| n).unwrap_or(0);
    if n >= p.max_per_account {
        (false, true, Some((t, n)))
    } else {
        (true, false, Some((t, n + 1)))
    }
}
