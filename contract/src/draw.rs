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
//! Mécaniques (`docs/mecaniques-spec.md`), toutes désactivées pour une table sans `mechanics` :
//! - la table de poids de rareté du pack (base, or, rush) est choisie avant les emplacements ;
//!   pitié : `gold_roll = u128_be(sha256(acc || 0x00 || 0x02)[0..16]) mod 10⁶` ;
//! - rareté pilotée par les burns : le tirage de rareté ne change pas ; dans la rareté, les
//!   brûlables prennent un poids brut `max(⌊w × circ / émises⌋, ⌊w × plancher⌋, 1)` renormalisé pour
//!   que leur part totale reste celle de leurs poids de base (`in_rarity_weight`) ;
//! - gold rush : palier relatif sur fenêtre glissante par seaux (`rush_on_buy`), figé à l'achat.

use crate::types::{
    CardKind, DrawCard, MythicCommitment, PackMode, PityParams, Rarity, RarityWeights, RushParams, RushState,
    SeriesTable,
};
use near_sdk::env;

/// Tags de `roll` : rareté et carte (par emplacement), gold pack (emplacement 0).
pub const TAG_RARITY: u8 = 0;
pub const TAG_CARD: u8 = 1;
pub const TAG_GOLD: u8 = 2;
pub const PPM: u64 = 1_000_000;

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

/// Compteurs de burn d'une série et plancher (rareté pilotée par les burns).
#[derive(Clone, Copy, Debug)]
pub struct BurnView<'a> {
    pub burned: &'a [u32],
    pub floor_bps: u32,
}

/// Poids brut d'une brûlable : 0 si épuisée (plafond) ou de poids nul ; `w` si aucune émise ;
/// sinon `max(⌊w × (émises − brûlées) / émises⌋, ⌊w × floor_bps / 10⁴⌋, 1)` (calcul en u128).
pub fn raw_burn_weight(weight: u32, minted: u32, burned: u32, cap: Option<u32>, floor_bps: u32) -> u64 {
    if weight == 0 || cap.is_some_and(|c| minted >= c) {
        return 0;
    }
    if minted == 0 {
        return weight as u64;
    }
    let circ = minted.saturating_sub(burned) as u128;
    let ratio = (weight as u128 * circ / minted as u128) as u64;
    let floor = ((weight as u128 * floor_bps as u128 / 10_000) as u64).max(1);
    ratio.max(floor)
}

/// Facteurs d'une rareté : `E` = Σ poids bruts des brûlables, `B` = Σ poids disponibles (de base)
/// des brûlables. Poids dans la rareté : non brûlable `a × E` (`a` si `E = 0`), brûlable `brut × B`.
/// La part des brûlables vaut donc exactement `B / (B + Σ a des non brûlables)`, comme sans burn :
/// le poids perdu par une brûlable très brûlée revient aux autres brûlables de la rareté.
pub fn burn_factors(cards: &[DrawCard], minted: &[u32], bv: &BurnView, rarity: Rarity) -> (u128, u128) {
    let (mut e, mut b) = (0u128, 0u128);
    for (i, (c, n)) in cards.iter().zip(minted).enumerate() {
        if c.rarity != rarity || !c.backed {
            continue;
        }
        e += raw_burn_weight(c.weight, *n, bv.burned.get(i).copied().unwrap_or(0), c.cap, bv.floor_bps) as u128;
        b += available(c.weight, *n, c.cap) as u128;
    }
    (e, b)
}

/// Poids d'une carte visible dans sa rareté (rareté pilotée par les burns), avec les facteurs
/// `(E, B)` de `burn_factors`.
pub fn in_rarity_weight(c: &DrawCard, minted: u32, burned: u32, floor_bps: u32, f: (u128, u128)) -> u128 {
    let (e, b) = f;
    if c.backed {
        if e == 0 {
            0
        } else {
            raw_burn_weight(c.weight, minted, burned, c.cap, floor_bps) as u128 * b
        }
    } else {
        let a = available(c.weight, minted, c.cap) as u128;
        if e == 0 {
            a
        } else {
            a * e
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
                .map(|(i, (c, n))| in_rarity_weight(c, *n, bv.burned.get(i).copied().unwrap_or(0), bv.floor_bps, f))
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
                (Some(bv), Some(f)) => in_rarity_weight(card, *n, bv.burned.get(i).copied().unwrap_or(0), bv.floor_bps, f),
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

/// Probabilité (ppm) d'un gold pack après `n` packs consécutifs sans gold pack.
pub fn pity_p_ppm(p: &PityParams, n: u32) -> u64 {
    (p.p0_ppm as u64 + p.k_ppm as u64 * n as u64).min(PPM)
}

/// `gold_roll = u128_be(sha256(acc || 0x00 || 0x02)[0..16]) mod 10⁶`.
pub fn gold_roll(acc: &[u8; 32]) -> u64 {
    (roll(acc, 0, TAG_GOLD) % PPM as u128) as u64
}

/// Pitié : (gold pack ?, gold_roll, probabilité en ppm). Garanti quand `n + 1 ≥ n_max`.
pub fn pity_is_gold(p: &PityParams, n: u32, acc: &[u8; 32]) -> (bool, u64, u64) {
    let r = gold_roll(acc);
    let pp = pity_p_ppm(p, n);
    (n.saturating_add(1) >= p.n_max || r < pp, r, pp)
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

/// Poids de rareté d'un pack selon sa table (retombe sur la base si la table manque).
pub fn mode_weights(t: &SeriesTable, mode: PackMode) -> &RarityWeights {
    let m = t.mechanics.as_ref();
    match mode {
        PackMode::Base => &t.rarity_weights,
        PackMode::Gold => m.and_then(|m| m.gold_weights.as_ref()).unwrap_or(&t.rarity_weights),
        PackMode::Rush => m.and_then(|m| m.rush.as_ref()).map(|r| &r.weights).unwrap_or(&t.rarity_weights),
    }
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
