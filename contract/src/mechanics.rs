//! Mécaniques de série (spécification complète : `docs/mecaniques-spec.md`).
//!
//! - **Pitié** : compteur on-chain `(compte, série) → n`, lu et mis à jour par le dernier reçu du
//!   tirage ; gold pack si `n + 1 ≥ N` ou `gold_roll < p0 + k × n` (`draw::pity_is_gold`).
//! - **Rareté pilotée par les burns** : `BurnState` par série, mis à jour dans
//!   `on_redeem_complete` ; poids dans la rareté renormalisés entre brûlables (`draw::in_rarity_weight`),
//!   avec un plancher (25 % du poids de base par défaut). Le tirage de rareté ne change pas.
//! - **Gold rush** : palier relatif au trafic des 24 dernières heures, pause entre deux rushs,
//!   table « rush » propre ; fenêtre glissante par seaux dans `Series::rush`, appliquée et figée par
//!   `buy_pack` (`draw::rush_on_buy`).
//! - **Résurrection** : l'oracle de prix (`price_oracle_id`, abstrait comme le redeemer) rend une
//!   carte de collection **épique ou légendaire** brûlable (`set_resurrected`), pour les cartes à
//!   venir et pour les exemplaires existants (l'adossement est lu à la demande, jamais copié dans
//!   les cartes).
//!
//! Tout ce qui influence un tirage est figé et journalisé : `pack_bought.rush`,
//! `pack_revealed.mechanics` (`mode`, `rush`, `pity`, `burn_seq`) et `card_redeemed.burn_seq`.

use crate::series::check_backing;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{json, Value};

/// Tables de poids de rareté d'une série : base, or, rush.
pub(crate) fn weight_tables(t: &SeriesTable) -> Vec<&RarityWeights> {
    let mut v = vec![&t.rarity_weights];
    if let Some(m) = &t.mechanics {
        if let Some(g) = &m.gold_weights {
            v.push(g);
        }
        if let Some(r) = &m.rush {
            v.push(&r.weights);
        }
    }
    v
}

/// Une rareté est tirable si l'une des tables lui donne un poids.
pub(crate) fn rarity_used(t: &SeriesTable, r: Rarity) -> bool {
    weight_tables(t).iter().any(|w| w.get(r) > 0)
}

fn check_weights(t: &SeriesTable, w: &RarityWeights, what: &str) {
    require!(w.total() > 0, format!("{what} : poids nuls"));
    if w.mythic > 0 {
        require!(
            t.mythics.iter().any(|m| m.weight > 0),
            format!("{what} : poids mythique sans engagement de poids non nul")
        );
    }
}

/// Contrôles des paramètres (dans l'en-tête, donc avant tout chargement de cartes).
pub(crate) fn validate_mechanics(t: &SeriesTable) {
    let Some(m) = &t.mechanics else { return };
    if let Some(g) = &m.gold_weights {
        check_weights(t, g, "gold_weights");
    }
    if let Some(p) = &m.pity {
        require!(m.gold_weights.is_some(), "pity exige gold_weights");
        require!(p.n_max >= 1 && p.n_max <= MAX_PITY_N, "pity.n_max hors bornes (1 à 10 000)");
        require!(p.p0_ppm as u64 <= PPM && p.k_ppm as u64 <= PPM, "pity : probabilités en ppm (≤ 10⁶)");
    }
    if let Some(b) = &m.burn {
        require!(b.floor_bps <= 10_000, "burn.floor_bps ≤ 10 000");
    }
    if let Some(r) = &m.rush {
        check_weights(t, &r.weights, "rush.weights");
        if let Some(g) = &m.gold_weights {
            require!(&r.weights != g, "rush.weights : table propre, distincte de la table or");
        }
        require!(r.ratio_bps >= 10_000, "rush.ratio_bps ≥ 10 000 (×1)");
        require!(r.min_packs >= 1, "rush.min_packs ≥ 1");
        require!(r.bucket_blocks >= 1 && r.duration_blocks >= 1, "rush : seaux et durée ≥ 1 bloc");
        require!(
            r.window_blocks % r.bucket_blocks == 0 && r.baseline_blocks % r.bucket_blocks == 0,
            "rush : window_blocks et baseline_blocks multiples de bucket_blocks"
        );
        let (mw, ml) = (r.window_blocks / r.bucket_blocks, r.baseline_blocks / r.bucket_blocks);
        require!(mw >= 1 && ml <= MAX_RUSH_BUCKETS, "rush : 1 à 96 seaux");
        require!(mw < ml, "rush : fenêtre courte plus courte que la fenêtre longue");
        // Le rythme court ne peut pas dépasser m_l / m_w fois le rythme long (il y est inclus).
        require!(
            (r.ratio_bps as u128) * (mw as u128) < 10_000u128 * ml as u128,
            "rush.ratio_bps inatteignable pour ces fenêtres"
        );
    }
}

pub(crate) fn burn_params(t: &SeriesTable) -> Option<&BurnParams> {
    t.mechanics.as_ref().and_then(|m| m.burn.as_ref())
}

#[near]
impl Contract {
    /// Résurrection d'un coin mort, réservée à l'oracle de prix : la carte visible `card_index`,
    /// **épique ou légendaire** (rare et commune refusées), devient brûlable contre `backing`,
    /// pour les cartes à venir **et** pour les exemplaires existants (l'adossement est lu à la
    /// demande). Un nouvel appel remplace l'adossement. Refusé pour une carte déjà adossée par la
    /// table. Le stockage ajouté est payé par l'appelant (excédent rendu). Événement
    /// `card_resurrected` avec `resurrect_seq` (la carte rejoint les brûlables de sa rareté, ce
    /// qui compte pour la rareté pilotée par les burns).
    #[payable]
    pub fn set_resurrected(&mut self, series_id: u32, card_index: u32, backing: Backing) {
        let start = env::storage_usage();
        let oracle = self.price_oracle_id.clone().unwrap_or_else(|| env::panic_str("Aucun oracle de prix configuré"));
        require!(env::predecessor_account_id() == oracle, "Réservé à l'oracle de prix");
        check_backing(&Some(backing.clone()));
        let s = self.series_ref(series_id);
        require!(
            matches!(s.status, SeriesStatus::Open | SeriesStatus::Paused | SeriesStatus::Closed),
            "Série non ouverte"
        );
        require!((card_index as usize) < s.draw_cards.len(), "Index de carte inconnu");
        let card = self.card_def(series_id, card_index);
        require!(
            matches!(card.rarity, Rarity::Epic | Rarity::Legendary),
            "Résurrection réservée aux cartes épiques et légendaires"
        );
        require!(card.backing.is_none(), "Carte déjà adossée par la table");
        let previous = self.resurrected.insert((series_id, card_index), backing.clone());
        let s = self.series.get_mut(series_id).unwrap();
        if previous.is_none() {
            s.draw_cards[card_index as usize].backed = true;
            s.resurrect_seq += 1;
        }
        let resurrect_seq = s.resurrect_seq;
        events::emit(
            "card_resurrected",
            json!({
                "series_id": series_id, "card_index": card_index, "card_id": card.card_id,
                "backing": backing, "previous": previous, "oracle_id": oracle,
                "resurrect_seq": resurrect_seq,
                "block_height": env::block_height(),
            }),
        );
        self.resurrected.flush();
        self.series.flush();
        let cost = env::storage_byte_cost().as_yoctonear() * env::storage_usage().saturating_sub(start) as u128;
        let deposit = env::attached_deposit().as_yoctonear();
        require!(deposit >= cost, format!("Dépôt insuffisant pour le stockage : {} yoctoNEAR", cost));
        Self::refund(&env::predecessor_account_id(), deposit - cost);
    }

    /// Adossement donné par l'oracle à une carte (`None` si aucun).
    pub fn get_resurrected(&self, series_id: u32, card_index: u32) -> Option<Backing> {
        self.resurrected.get(&(series_id, card_index)).cloned()
    }

    /// Compteur de pitié d'un compte pour une série : `n` packs consécutifs sans gold pack,
    /// probabilité du prochain (`p_ppm`) et packs restants avant la garantie.
    pub fn get_pity(&self, account_id: AccountId, series_id: u32) -> Value {
        let s = self.series_ref(series_id);
        let Some(p) = s.table.mechanics.as_ref().and_then(|m| m.pity.as_ref()) else {
            return json!({ "enabled": false });
        };
        let n = self.pity.get(&(account_id, series_id)).copied().unwrap_or(0);
        json!({
            "enabled": true, "n": n, "p_ppm": draw::pity_p_ppm(p, n),
            "guaranteed_in": p.n_max.saturating_sub(n).max(1),
            "params": p,
        })
    }

    /// État du gold rush : dernier déclenchement, fin du rush, nombre de rushes, packs dans la
    /// fenêtre à la hauteur `at_height` (bloc courant par défaut), et si un achat à cette hauteur
    /// serait un pack rush.
    pub fn get_rush_state(&self, series_id: u32, at_height: Option<u64>) -> Value {
        let s = self.series_ref(series_id);
        let Some(p) = s.table.mechanics.as_ref().and_then(|m| m.rush.as_ref()) else {
            return json!({ "enabled": false });
        };
        let h = at_height.unwrap_or_else(env::block_height);
        let st = s.rush.clone().unwrap_or_default();
        let bsz = p.bucket_blocks.max(1);
        let m = (p.baseline_blocks / bsz).max(1);
        let b = h / bsz;
        let mw = (p.window_blocks / bsz).clamp(1, m);
        let count = |k: u64| -> u64 { st.ring.iter().filter(|(bb, _)| *bb <= b && b - *bb < k).map(|(_, c)| *c as u64).sum() };
        let (window, baseline) = (count(mw), count(m));
        let active = st.last_trigger.is_some_and(|t| h > t && h <= t.saturating_add(p.duration_blocks));
        let pause_until = st.last_trigger.map(|t| t.saturating_add(p.duration_blocks).saturating_add(p.cooldown_blocks));
        json!({
            "enabled": true, "params": p, "height": h,
            "last_trigger": st.last_trigger,
            "rush_until": st.last_trigger.map(|t| t.saturating_add(p.duration_blocks)),
            "rush_count": st.rush_count,
            "window_count": window,
            "baseline_count": baseline,
            "start_height": st.start_height,
            "pause_until": pause_until,
            "active": active,
        })
    }

    /// Compteurs de burn d'une série (rareté pilotée par les burns), paginés (200 au plus).
    pub fn get_burns(&self, series_id: u32, from_index: Option<u32>, limit: Option<u32>) -> Value {
        let Some(b) = self.series_burns.get(&series_id) else {
            return json!({ "enabled": false });
        };
        let n = b.burned.len() as u32;
        let from = from_index.unwrap_or(0).min(n);
        let to = from.saturating_add(limit.unwrap_or(200).min(200)).min(n);
        json!({
            "enabled": true, "seq": b.seq, "card_count": n, "from_index": from,
            "burned": &b.burned[from as usize..to as usize],
        })
    }
}

impl Contract {
    /// Burn d'une carte visible d'une série à rareté pilotée par les burns : incrémente son
    /// compteur et le numéro d'ordre des burns de la série. Renvoie ce numéro (journalisé).
    pub(crate) fn record_burn(&mut self, series_id: u32, kind: CardKind, index: u32) -> Option<u64> {
        if kind != CardKind::Visible {
            return None;
        }
        let b = self.series_burns.get_mut(&series_id)?;
        if let Some(x) = b.burned.get_mut(index as usize) {
            *x += 1;
            b.seq += 1;
            return Some(b.seq);
        }
        None
    }
}
