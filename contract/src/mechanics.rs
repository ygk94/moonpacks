//! Mécaniques de série (spécification complète : `docs/mechanics.md`).
//!
//! - **Pitié** : compteur on-chain `(compte, série) → n`, lu et mis à jour par le dernier reçu du
//!   tirage ; gold pack si `gold_roll < min(p_max, p0 + k × n)` en ppb (`draw::pity_is_gold`), sans
//!   garantie (sauf `n_max` optionnel) ; le compteur ne repart à 0 qu'après un gold pack.
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
//! - **Gold pack** : plancher de rareté par emplacement (`GoldParams`), compteur de pitié inchangé.
//! - **Valeur** : `V` tiré dans la table du pack, réparti entre les brûlables (`ValueParams`) ; le
//!   dernier emplacement d'un pack normal est tiré parmi les brûlables.
//!
//! Tout ce qui influence un tirage est figé et journalisé : `pack_bought.rush`,
//! `pack_revealed.mechanics` (`mode`, `rush`, `pity`, `burn_seq`, `resurrect_seq`, `value`) et
//! `card_redeemed.burn_seq`.

use crate::series::check_backing;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{json, Value};

/// Tables de poids de rareté d'une série : base, rush, et poids propres des emplacements du gold
/// pack (un emplacement sans poids propres prend la base tronquée, déjà couverte par la base).
pub(crate) fn weight_tables(t: &SeriesTable) -> Vec<&RarityWeights> {
    let mut v = vec![&t.rarity_weights];
    if let Some(m) = &t.mechanics {
        if let Some(g) = &m.gold {
            v.extend(g.slots.iter().filter_map(|s| s.weights.as_ref()));
        }
        if let Some(r) = &m.rush {
            v.push(&r.weights);
        }
    }
    v
}

/// Table de valeur (`None` sans la mécanique).
pub(crate) fn value_params(t: &SeriesTable) -> Option<&ValueParams> {
    t.mechanics.as_ref().and_then(|m| m.value.as_ref())
}

/// Une règle « tiré parmi les brûlables » peut s'appliquer : table de valeur (dernier emplacement
/// d'un pack normal) ou emplacement `burnable` du gold pack.
pub(crate) fn needs_burnable(t: &SeriesTable) -> bool {
    t.mechanics.as_ref().is_some_and(|m| {
        m.value.is_some() || m.gold.as_ref().is_some_and(|g| g.slots.iter().any(|s| s.burnable))
    })
}

fn check_tiers(tiers: &[ValueTier], what: &str, min_bps: u32, max_bps: u32) {
    require!(
        !tiers.is_empty() && tiers.len() <= MAX_VALUE_TIERS,
        format!("E_MECH_VALUE: value.{what} : 1 à {MAX_VALUE_TIERS} paliers")
    );
    for (bps, w) in tiers {
        require!(*w > 0, format!("E_MECH_VALUE: value.{what} : poids nuls interdits"));
        require!(
            *bps >= min_bps && *bps <= max_bps,
            format!("E_MECH_VALUE: value.{what} : valeur hors de [{min_bps}, {max_bps}] points de base")
        );
    }
}

fn validate_value(t: &SeriesTable, v: &ValueParams) {
    check_tiers(&v.normal, "normal", MIN_NORMAL_VALUE_BPS, MAX_NORMAL_VALUE_BPS);
    check_tiers(&v.gold, "gold", 1, MAX_VALUE_BPS);
    check_tiers(&v.rush, "rush", 1, MAX_VALUE_BPS);
    let m = &v.multipliers;
    require!(m.mythic == 0, "E_MECH_VALUE: value.multipliers.mythic = 0 (une mythique garde l'adossement de son contenu)");
    for r in [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common] {
        let x = m.get(r);
        require!(x >= 1 && x <= MAX_VALUE_MULT, format!("E_MECH_VALUE: value.multipliers.{} : 1 à {MAX_VALUE_MULT}", r.as_str()));
    }
    // Aucun dépassement au tirage : ⌊prix × V / 10⁴⌋ × multiplicateur tient sur u128.
    let max_bps = v.normal.iter().chain(&v.gold).chain(&v.rush).map(|x| x.0).max().unwrap_or(0) as u128;
    let max_mult = [m.legendary, m.epic, m.rare, m.common].into_iter().max().unwrap_or(0) as u128;
    require!(
        t.price.0.checked_mul(max_bps).and_then(|x| (x / 10_000).checked_mul(max_mult)).is_some(),
        "E_MECH_VALUE: value : prix trop élevé pour ces valeurs et multiplicateurs (dépassement de u128)"
    );
}

fn validate_gold(t: &SeriesTable, g: &GoldParams) {
    require!(
        !g.slots.is_empty() && g.slots.len() <= MAX_CARDS_PER_PACK as usize,
        "E_MECH_GOLD: gold.slots : 1 à 10 emplacements"
    );
    for (i, s) in g.slots.iter().enumerate() {
        let w = crate::draw::gold_slot_weights(&t.rarity_weights, s);
        check_weights(t, &w, &format!("gold.slots[{i}]"));
        for r in Rarity::ALL {
            if r.index() > s.floor.index() {
                require!(w.get(r) == 0, format!("E_MECH_GOLD: gold.slots[{i}] : poids sous le plancher {}", s.floor.as_str()));
            }
        }
    }
}

/// Types de packs : contrôles de l'en-tête (avant le chargement des cartes).
pub(crate) fn validate_kinds_header(t: &SeriesTable) {
    let Some(kinds) = &t.kinds else { return };
    require!(!kinds.is_empty() && kinds.len() <= MAX_PACK_KINDS, "E_KINDS: kinds : 1 à 16 types de packs");
    let mut names = std::collections::BTreeSet::new();
    for (i, k) in kinds.iter().enumerate() {
        let what = format!("kinds[{i}]");
        require!(
            !k.name.is_empty() && k.name.len() <= MAX_KIND_NAME_LEN,
            format!("E_KINDS: {what}.name : 1 à {MAX_KIND_NAME_LEN} octets")
        );
        require!(names.insert(k.name.as_str()), format!("E_KINDS: {what}.name en double"));
        require!(k.price.0 > 0, format!("E_KINDS: {what}.price doit être > 0"));
        require!(
            k.cards_per_pack >= 1 && k.cards_per_pack <= MAX_CARDS_PER_PACK,
            format!("E_KINDS: {what}.cards_per_pack hors bornes")
        );
        require!(k.pool.windows(2).all(|w| w[0] < w[1]), format!("E_KINDS: {what}.pool : index strictement croissants"));
        require!(k.pool.len() <= MAX_CARDS_PER_SERIES, format!("E_KINDS: {what}.pool : trop d'index"));
        if k.value {
            let v = t.mechanics.as_ref().and_then(|m| m.value.as_ref());
            let v = v.unwrap_or_else(|| env::panic_str(&format!("E_KINDS: {what}.value sans table de valeur dans la série")));
            // Aucun dépassement au tirage, comme pour le prix de la série.
            let max_bps = v.normal.iter().chain(&v.rush).map(|x| x.0).max().unwrap_or(0) as u128;
            let m = &v.multipliers;
            let max_mult = [m.legendary, m.epic, m.rare, m.common].into_iter().max().unwrap_or(0) as u128;
            require!(
                k.price.0.checked_mul(max_bps).and_then(|x| (x / 10_000).checked_mul(max_mult)).is_some(),
                format!("E_KINDS: {what}.price trop élevé pour la table de valeur (dépassement de u128)")
            );
        }
        let base = crate::draw::kind_weights(&t.rarity_weights, Some(k));
        check_weights(t, &base, &what);
        if let Some(slots) = &k.slots {
            require!(
                slots.len() == k.cards_per_pack as usize,
                format!("E_KINDS: {what}.slots : une règle par carte du pack ({} attendues)", k.cards_per_pack)
            );
            for (j, s) in slots.iter().enumerate() {
                let w = crate::draw::kind_weights(&crate::draw::gold_slot_weights(&base, s), Some(k));
                check_weights(t, &w, &format!("{what}.slots[{j}]"));
                for r in Rarity::ALL {
                    if r.index() > s.floor.index() {
                        require!(w.get(r) == 0, format!("E_KINDS: {what}.slots[{j}] : poids sous le plancher {}", s.floor.as_str()));
                    }
                }
            }
        }
    }
}

/// Types de packs : contrôles sur les cartes (à l'ouverture). Chaque type tire toujours une carte :
/// une commune illimitée parmi ses cartes, et une brûlable illimitée s'il en garantit une.
pub(crate) fn validate_kinds_cards(t: &SeriesTable, cards: &[DrawCard]) {
    let Some(kinds) = &t.kinds else { return };
    for (i, k) in kinds.iter().enumerate() {
        let what = format!("kinds[{i}]");
        require!(
            k.pool.last().is_none_or(|&last| (last as usize) < cards.len()),
            format!("E_KINDS: {what}.pool : index de carte inconnu")
        );
        let dc = crate::draw::kind_cards(cards, Some(k));
        require!(
            dc.iter().any(|c| c.rarity == Rarity::Common && c.cap.is_none() && c.weight > 0),
            format!("E_KINDS: {what} : il faut une commune sans plafond et de poids non nul parmi ses cartes")
        );
        let burnable_slot = k.slots.as_ref().is_some_and(|s| s.iter().any(|r| r.burnable)) || (k.value && k.slots.is_none());
        if burnable_slot {
            require!(
                dc.iter().any(|c| c.backed && c.cap.is_none() && c.weight > 0),
                format!("E_KINDS: {what} : brûlable garantie sans carte adossée, sans plafond et de poids non nul parmi ses cartes")
            );
        }
        if k.value {
            require!(burnable_slot, format!("E_KINDS: {what}.value : il faut un emplacement parmi les brûlables"));
        }
    }
}

/// Une rareté est tirable si l'une des tables lui donne un poids.
pub(crate) fn rarity_used(t: &SeriesTable, r: Rarity) -> bool {
    weight_tables(t).iter().any(|w| w.get(r) > 0)
}

fn check_weights(t: &SeriesTable, w: &RarityWeights, what: &str) {
    require!(w.total() > 0, format!("E_WEIGHTS_ZERO: {what} : poids nuls"));
    if w.mythic > 0 {
        require!(
            t.mythics.iter().any(|m| m.weight > 0),
            format!("E_MYTHIC_WEIGHT: {what} : poids mythique sans engagement de poids non nul")
        );
    }
}

/// Contrôles des paramètres (dans l'en-tête, donc avant tout chargement de cartes).
pub(crate) fn validate_mechanics(t: &SeriesTable) {
    let Some(m) = &t.mechanics else { return };
    if let Some(g) = &m.gold {
        validate_gold(t, g);
    }
    if let Some(v) = &m.value {
        validate_value(t, v);
    }
    if let Some(p) = &m.pity {
        require!(m.gold.is_some(), "E_MECH_PITY: pity exige gold");
        require!(
            p.n_max.is_none_or(|n| (1..=MAX_PITY_N).contains(&n)),
            "E_MECH_PITY: pity.n_max hors bornes (absent, ou 1 à 10 000)"
        );
        require!(
            p.p0_ppb as u64 <= PPB && p.k_ppb as u64 <= PPB && p.p_max_ppb as u64 <= PPB,
            "E_MECH_PITY: pity : probabilités en ppb (≤ 10⁹)"
        );
        require!(p.p0_ppb <= p.p_max_ppb, "E_MECH_PITY: pity : p0_ppb ≤ p_max_ppb");
        require!(p.p_max_ppb > 0 || p.n_max.is_some(), "E_MECH_PITY: pity : gold pack inatteignable (p_max_ppb = 0 sans n_max)");
    }
    if let Some(r) = &m.resurrection {
        require!(r.eligible.len() <= MAX_RESURRECTABLE, "E_MECH_RESURRECTION: resurrection.eligible : 200 cartes au plus");
        require!(
            r.eligible.windows(2).all(|p| p[0] < p[1]),
            "E_MECH_RESURRECTION: resurrection.eligible : index strictement croissants"
        );
    }
    if let Some(b) = &m.burn {
        require!(b.floor_bps <= 10_000, "E_MECH_BURN: burn.floor_bps ≤ 10 000");
        require!(b.prior_k <= MAX_BURN_PRIOR_K, "E_MECH_BURN: burn.prior_k ≤ 1 000 000");
    }
    if let Some(r) = &m.rush {
        check_weights(t, &r.weights, "rush.weights");
        require!(r.ratio_bps >= 10_000, "E_MECH_RUSH: rush.ratio_bps ≥ 10 000 (×1)");
        require!(r.min_packs >= 1, "E_MECH_RUSH: rush.min_packs ≥ 1");
        require!(r.max_per_account >= 1, "E_MECH_RUSH: rush.max_per_account ≥ 1");
        require!(r.bucket_blocks >= 1 && r.duration_blocks >= 1, "E_MECH_RUSH: rush : seaux et durée ≥ 1 bloc");
        require!(
            r.window_blocks % r.bucket_blocks == 0 && r.baseline_blocks % r.bucket_blocks == 0,
            "E_MECH_RUSH: rush : window_blocks et baseline_blocks multiples de bucket_blocks"
        );
        let (mw, ml) = (r.window_blocks / r.bucket_blocks, r.baseline_blocks / r.bucket_blocks);
        require!(mw >= 1 && ml <= MAX_RUSH_BUCKETS, "E_MECH_RUSH: rush : 1 à 96 seaux");
        require!(mw < ml, "E_MECH_RUSH: rush : fenêtre courte plus courte que la fenêtre longue");
        // Le rythme court ne peut pas dépasser m_l / m_w fois le rythme long (il y est inclus).
        require!(
            (r.ratio_bps as u128) * (mw as u128) < 10_000u128 * ml as u128,
            "E_MECH_RUSH: rush.ratio_bps inatteignable pour ces fenêtres"
        );
    }
}

/// Cartes ressuscitables de la table (liste vide sans `mechanics.resurrection`).
pub(crate) fn resurrectable(t: &SeriesTable) -> &[u32] {
    t.mechanics.as_ref().and_then(|m| m.resurrection.as_ref()).map(|r| r.eligible.as_slice()).unwrap_or(&[])
}

/// Contrôles de la liste ressuscitable qui portent sur les cartes (à l'ouverture, et à la création
/// d'une table complète) : chaque index désigne une épique ou une légendaire non adossée.
pub(crate) fn validate_resurrectable(t: &SeriesTable, cards: &[DrawCard]) {
    // Brûlable garantie : une carte adossée par la table, illimitée et de poids non nul, existe
    // toujours ; la retombée parcourt toutes les raretés visibles, elle la trouve donc toujours.
    if needs_burnable(t) {
        require!(
            cards.iter().any(|c| c.backed && c.cap.is_none() && c.weight > 0),
            "E_MECH_BURNABLE: Brûlable garantie : il faut une carte adossée par la table, sans plafond et de poids non nul"
        );
    }
    for &i in resurrectable(t) {
        let c = cards.get(i as usize).unwrap_or_else(|| env::panic_str("E_MECH_RESURRECTION: resurrection.eligible : index de carte inconnu"));
        require!(
            matches!(c.rarity, Rarity::Epic | Rarity::Legendary),
            "E_MECH_RESURRECTION: resurrection.eligible : cartes épiques et légendaires seulement"
        );
        require!(!c.backed, "E_MECH_RESURRECTION: resurrection.eligible : carte déjà adossée par la table");
    }
}

pub(crate) fn burn_params(t: &SeriesTable) -> Option<&BurnParams> {
    t.mechanics.as_ref().and_then(|m| m.burn.as_ref())
}

#[near]
impl Contract {
    /// Résurrection d'un coin mort, réservée à l'oracle de prix : la carte visible `card_index`,
    /// **engagée dans la table hachée** (`mechanics.resurrection.eligible` : épiques et légendaires
    /// non adossées seulement), devient brûlable contre `backing`,
    /// pour les cartes à venir **et** pour les exemplaires existants (l'adossement est lu à la
    /// demande). Un nouvel appel remplace l'adossement. Refusé pour une carte déjà adossée par la
    /// table. Le stockage ajouté est payé par l'appelant (excédent rendu). Événement
    /// `card_resurrected` avec `resurrect_seq` (la carte rejoint les brûlables de sa rareté, ce
    /// qui compte pour la rareté pilotée par les burns).
    #[payable]
    pub fn set_resurrected(&mut self, series_id: u32, card_index: u32, backing: Backing) {
        let start = env::storage_usage();
        let oracle = self.price_oracle_id.clone().unwrap_or_else(|| env::panic_str("E_NO_ORACLE: Aucun oracle de prix configuré"));
        require!(env::predecessor_account_id() == oracle, "E_NOT_ORACLE: Réservé à l'oracle de prix");
        check_backing(&Some(backing.clone()));
        let s = self.series_ref(series_id);
        require!(
            matches!(s.status, SeriesStatus::Open | SeriesStatus::Paused | SeriesStatus::Closed),
            "E_SERIES_NOT_OPEN: Série non ouverte"
        );
        require!((card_index as usize) < s.draw_cards.len(), "E_UNKNOWN_CARD_INDEX: Index de carte inconnu");
        require!(
            resurrectable(&s.table).binary_search(&card_index).is_ok(),
            "E_NOT_RESURRECTABLE: Carte non ressuscitable : absente de mechanics.resurrection.eligible (table hachée)"
        );
        let card = self.card_def(series_id, card_index);
        require!(
            matches!(card.rarity, Rarity::Epic | Rarity::Legendary),
            "E_RESURRECT_RARITY: Résurrection réservée aux cartes épiques et légendaires"
        );
        require!(card.backing.is_none(), "E_ALREADY_BACKED: Carte déjà adossée par la table");
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
        require!(deposit >= cost, format!("E_STORAGE_DEPOSIT: Dépôt insuffisant pour le stockage : {} yoctoNEAR", cost));
        Self::refund(&env::predecessor_account_id(), deposit - cost);
    }

    /// Adossement donné par l'oracle à une carte (`None` si aucun).
    pub fn get_resurrected(&self, series_id: u32, card_index: u32) -> Option<Backing> {
        self.resurrected.get(&(series_id, card_index)).cloned()
    }

    /// Compteur de pitié d'un compte pour une série : `n` packs consécutifs sans gold pack,
    /// probabilité du prochain (`p_ppb`, parties par milliard), packs restants avant le plafond
    /// (`packs_to_max`, 0 s'il est atteint) et avant la garantie (`guaranteed_in`, `null` sans `n_max`).
    pub fn get_pity(&self, account_id: AccountId, series_id: u32) -> Value {
        let s = self.series_ref(series_id);
        let Some(p) = s.table.mechanics.as_ref().and_then(|m| m.pity.as_ref()) else {
            return json!({ "enabled": false });
        };
        let n = self.pity.get(&(account_id, series_id)).copied().unwrap_or(0);
        let packs_to_max = if p.k_ppb == 0 {
            0
        } else {
            let gap = (p.p_max_ppb as u64).saturating_sub(draw::pity_p_ppb(p, n));
            gap.div_ceil(p.k_ppb as u64)
        };
        json!({
            "enabled": true, "n": n, "p_ppb": draw::pity_p_ppb(p, n),
            "packs_to_max": packs_to_max,
            "guaranteed_in": p.n_max.map(|m| m.saturating_sub(n).max(1)),
            "params": p,
        })
    }

    /// État du gold rush : dernier déclenchement, fin du rush, nombre de rushes, packs dans la
    /// fenêtre à la hauteur `at_height` (bloc courant par défaut), et si un achat à cette hauteur
    /// serait un pack rush. Avec `account_id` : packs rush de ce compte pendant le rush en cours et
    /// packs rush qui lui restent (`max_per_account`).
    pub fn get_rush_state(&self, series_id: u32, at_height: Option<u64>, account_id: Option<AccountId>) -> Value {
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
            "account": account_id.map(|a| {
                let n = self.rush_accounts.get(&(a.clone(), series_id)).filter(|(t, _)| Some(*t) == st.last_trigger).map(|(_, n)| *n).unwrap_or(0);
                json!({ "account_id": a, "rush_packs": n, "remaining": if active { p.max_per_account.saturating_sub(n) } else { 0 } })
            }),
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
