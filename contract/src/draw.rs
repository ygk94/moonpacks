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

use crate::types::{CardKind, DrawCard, MythicCommitment, Rarity, RarityWeights, SeriesTable};
use near_sdk::env;

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
    let total = weights.total().max(1) as u128;
    let rarity_roll = roll(acc, slot, 0) % total;
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
    let avail = |r| available_weight_compact(cards, mythics, minted, mythic_minted, r);
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

    let raw_card = roll(acc, slot, 1);
    let card_roll = if sum == 0 { 0 } else { raw_card % sum as u128 };

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
        for (i, (card, n)) in cards.iter().zip(minted).enumerate() {
            if card.rarity != final_rarity {
                continue;
            }
            c += available(card.weight, *n, card.cap) as u128;
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
