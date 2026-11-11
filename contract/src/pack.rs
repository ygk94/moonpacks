//! Achat d'un booster et tirage sur k reçus privés chaînés.
//!
//! `buy_pack` encaisse le prix (aucune annulation ; seul un pack `Stuck` est remboursable, par
//! `refund_stuck_pack`) et programme `reveal_step(pack_id, attempt, 1)`. Chaque étape mélange
//! `env::random_seed()` dans `acc`, puis programme la suivante à gaz fixe. La dernière tire,
//! crée les cartes par mint direct (jamais de `*_transfer_call`), rend le stockage prépayé non
//! utilisé et journalise `pack_revealed`.
//!
//! **Stockage mesuré.** Chaque reçu (`buy_pack`, chaque étape, tirage final) écrit son état
//! (`flush_all`) et mesure `env::storage_usage()` avant et après : le cumul est `Pack::storage_used`.
//! Le dernier reçu rend `storage_per_pack − storage_used` (octets × 10¹⁹ yoctoNEAR) à l'acheteur,
//! jamais plus : le contrat reste couvert pour tout ce que le pack occupe.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{json, Value};
use near_sdk::Promise;

#[near]
impl Contract {
    /// Achète un booster. Dépôt ≥ prix + stockage du pire cas (`get_series(id).required_deposit`) ;
    /// gaz ≥ `get_series(id).min_gas`.
    /// L'excédent de dépôt est rendu ; le reste est acquis, sans annulation possible.
    #[payable]
    pub fn buy_pack(&mut self, series_id: u32) -> U128 {
        let start = env::storage_usage();
        let buyer = env::predecessor_account_id();
        let min_gas = self.min_entry_gas();
        require!(env::prepaid_gas() >= min_gas, format!("Gaz insuffisant : {} requis", min_gas));
        let s = self.series_ref(series_id);
        require!(s.status == SeriesStatus::Open, "Série non ouverte à la vente");
        let price = s.table.price.0;
        let storage = env::storage_byte_cost().as_yoctonear() * s.storage_per_pack as u128;
        let required = price + storage;
        let deposit = env::attached_deposit().as_yoctonear();
        require!(
            deposit >= required,
            format!("Dépôt insuffisant : {} yoctoNEAR requis (prix {} + stockage {})", required, price, storage)
        );
        let table_hash = s.table_hash.unwrap_or_else(|| env::panic_str("Table non hachée"));

        let pack_id = self.next_pack_id;
        self.next_pack_id += 1;
        let height = env::block_height();

        // Gold rush : l'état est figé ici, à l'achat (pas au tirage), pour qu'on ne puisse pas
        // viser le rush en retardant la révélation.
        let mut flags = 0u8;
        let mut rush_ev = None;
        let series = self.series.get_mut(series_id).unwrap();
        series.packs_sold += 1;
        let mut rush_account = None;
        if let Some(rp) = series.table.mechanics.as_ref().and_then(|m| m.rush.clone()) {
            let st = series.rush.get_or_insert_with(RushState::default);
            let o = draw::rush_on_buy(&rp, st, height);
            // Plafond par compte et par rush : au-delà, pack normal (figé ici, journalisé).
            let key = (buyer.clone(), series_id);
            let prev = if o.active { self.rush_accounts.get(&key).copied() } else { None };
            let (rush, capped, entry) = draw::rush_account(&rp, o.active, st.last_trigger, prev);
            if rush {
                flags |= FLAG_RUSH;
            }
            rush_ev = Some(json!({
                "active": o.active, "window_count": o.window_count, "baseline_count": o.baseline_count,
                "triggered": o.triggered, "last_trigger": st.last_trigger,
                "rush_until": st.last_trigger.map(|t| t.saturating_add(rp.duration_blocks)),
                "rush": rush, "capped": capped,
                "account_rush_packs": entry.filter(|_| o.active).map(|(_, n)| n),
            }));
            if rush {
                rush_account = entry.map(|e| (key, e));
            }
        }
        if let Some((key, e)) = rush_account {
            self.rush_accounts.insert(key, e);
        }

        let pack = Pack {
            series_id,
            owner_id: buyer.clone(),
            bought_at_height: height,
            status: PackStatus::Pending,
            attempt: 0,
            step: 0,
            acc: draw::initial_acc(pack_id, buyer.as_str(), &table_hash),
            seeds: Vec::new(),
            last_progress_height: height,
            revealed_at_ms: 0,
            flags,
            draws: Vec::new(),
            cards: Vec::new(),
            value: None,
            storage_used: 0,
        };
        self.packs.insert(pack_id, pack);
        // Liste paginée par compte, par blocs : (compte, bloc) → pack_ids, et un compteur par compte.
        let rank = self.pack_count_by_owner.get(&buyer).copied().unwrap_or(0);
        let key = (buyer.clone(), rank / OWNER_CHUNK);
        if rank % OWNER_CHUNK == 0 {
            self.owner_packs.insert(key, vec![pack_id]);
        } else {
            self.owner_packs.get_mut(&key).unwrap_or_else(|| env::panic_str("Bloc de liste manquant")).push(pack_id);
        }
        self.pack_count_by_owner.insert(buyer.clone(), rank + 1);
        self.revenue += price;
        // Engagement envers l'acheteur jusqu'au tirage : prix (rendu si le pack finit `Stuck`) et
        // stockage prépayé ; le stockage réellement écrit en est déduit reçu par reçu.
        self.pack_escrow += price + storage;
        let added = self.storage_added_since(start);
        self.charge_pack_storage(pack_id, added);

        let mut ev = json!({
            "pack_id": pack_id, "series_id": series_id, "owner_id": buyer,
            "price": U128(price), "storage_prepaid": U128(storage), "block_height": height,
        });
        if let Some(r) = rush_ev {
            ev["rush"] = r;
        }
        events::emit("pack_bought", ev);
        Self::refund(&buyer, deposit - required);
        self.schedule_step(pack_id, 0, 1);
        U128(pack_id as u128)
    }

    /// Étape du tirage. Privée : seul le contrat peut l'appeler.
    /// Ne panique jamais sur un résultat ; une étape périmée est simplement ignorée.
    #[private]
    pub fn reveal_step(&mut self, pack_id: u64, attempt: u32, step: u8) {
        let start = env::storage_usage();
        let Some(mut pack) = self.packs.get(&pack_id).cloned() else {
            env::log_str("reveal_step: pack inconnu");
            return;
        };
        if pack.status != PackStatus::Pending || pack.attempt != attempt || pack.step + 1 != step {
            env::log_str("reveal_step: étape périmée, ignorée");
            return;
        }
        let seed = env::random_seed_array();
        let height = env::block_height();
        pack.acc = draw::mix(&pack.acc, &seed, pack_id, pack.owner_id.as_str());
        pack.step = step;
        pack.last_progress_height = height;
        pack.seeds.push(SeedRecord { attempt, step, block_height: height, seed });

        if step < self.config.reveal_steps {
            events::emit(
                "reveal_step",
                json!({
                    "pack_id": pack_id, "attempt": attempt, "step": step,
                    "block_height": height, "seed": hex32(&seed), "acc": hex32(&pack.acc),
                }),
            );
            self.packs.insert(pack_id, pack);
            let added = self.storage_added_since(start);
            self.charge_pack_storage(pack_id, added);
            self.schedule_step(pack_id, attempt, step + 1);
            return;
        }

        #[cfg(feature = "test-hooks")]
        if env::storage_has_key(b"__fail_reveal") {
            env::panic_str("test-hooks: échec simulé du dernier reçu");
        }

        self.finalize_pack(pack_id, pack, start);
    }

    /// Relance le tirage d'un booster resté `Pending` (aucune carte écrite) après
    /// `retry_delay_blocks` blocs sans progrès. Ouvert à tous ; les graines sont nouvelles
    /// et `acc` continue d'accumuler.
    ///
    /// Le résultat qu'aurait donné un dernier reçu échoué **peut être recalculé** : sa graine vaut
    /// `hash(action_hash || random_value)`, deux valeurs publiques, et `acc` avant ce reçu est
    /// journalisé. Ce n'est pas exploitable, car l'échec ne dépend pas du résultat : le dernier reçu
    /// n'a aucun chemin d'échec conditionné au tirage (gaz fixe, stockage prépayé, pas de `require`
    /// sur les cartes). Personne ne peut donc « faire échouer les mauvais tirages » pour relancer.
    /// Un échec relève du protocole ou d'un bug, et la relance repart de nouvelles graines.
    ///
    /// Après `MAX_ATTEMPTS` tentatives, l'appel fait passer le pack en `Stuck` (événement
    /// `pack_stuck`) : plus aucun tirage possible, le pack devient remboursable (`refund_stuck_pack`).
    pub fn retry_reveal(&mut self, pack_id: u64) {
        let min_gas = self.min_entry_gas();
        require!(env::prepaid_gas() >= min_gas, format!("Gaz insuffisant : {} requis", min_gas));
        let delay = self.config.retry_delay_blocks;
        let pack = self.packs.get_mut(&pack_id).unwrap_or_else(|| env::panic_str("Pack inconnu"));
        require!(pack.status == PackStatus::Pending, "Tirage déjà écrit : relance interdite");
        require!(pack.cards.is_empty(), "Tirage déjà écrit : relance interdite");
        require!(
            env::block_height() >= pack.last_progress_height + delay,
            "Délai de relance non écoulé"
        );
        if pack.attempt + 1 >= MAX_ATTEMPTS {
            pack.status = PackStatus::Stuck;
            events::emit(
                "pack_stuck",
                json!({
                    "pack_id": pack_id, "attempts": pack.attempt + 1,
                    "by": env::predecessor_account_id(), "block_height": env::block_height(),
                }),
            );
            return;
        }
        pack.attempt += 1;
        pack.step = 0;
        pack.last_progress_height = env::block_height();
        let attempt = pack.attempt;
        events::emit(
            "reveal_retried",
            json!({
                "pack_id": pack_id, "attempt": attempt,
                "by": env::predecessor_account_id(), "block_height": env::block_height(),
            }),
        );
        self.schedule_step(pack_id, attempt, 1);
    }

    /// Rembourse un pack `Stuck` à son acheteur : le prix et le stockage prépayé non utilisé
    /// (`storage_per_pack − storage_used`). Ouvert à tous (les fonds vont toujours à l'acheteur).
    /// Le pack passe en `Refunded` : plus aucun tirage, aucune relance, aucun second remboursement.
    ///
    /// **Pas de tirage gratuit, par construction.** Un pack n'est `Stuck` qu'après `MAX_ATTEMPTS`
    /// derniers reçus en échec, et seulement s'il n'a **aucune carte écrite** : un pack tiré
    /// (`Revealed`) ne peut plus changer d'état. Or le dernier reçu n'a aucun chemin d'échec qui
    /// dépende du tirage (gaz fixe, stockage prépayé, aucun `require` sur le résultat, solde gardé
    /// par la réserve de `withdraw_revenue`) : personne ne peut faire échouer les seuls mauvais
    /// tirages. Voir un tirage (réussi), puis demander le remboursement, est donc impossible.
    /// Renvoie le montant rendu (yoctoNEAR).
    pub fn refund_stuck_pack(&mut self, pack_id: u64) -> U128 {
        let cost = env::storage_byte_cost().as_yoctonear();
        let pack = self.packs.get(&pack_id).unwrap_or_else(|| env::panic_str("Pack inconnu"));
        require!(pack.status != PackStatus::Refunded, "Pack déjà remboursé");
        require!(pack.status == PackStatus::Stuck, "Seul un pack bloqué (stuck) est remboursable");
        require!(pack.cards.is_empty(), "Tirage déjà écrit : remboursement interdit");
        let (owner, series_id, storage_used) = (pack.owner_id.clone(), pack.series_id, pack.storage_used);
        let s = self.series_ref(series_id);
        let price = s.table.price.0;
        let storage_refund = cost * s.storage_per_pack.saturating_sub(storage_used as u64) as u128;
        let total = price + storage_refund;
        self.packs.get_mut(&pack_id).unwrap().status = PackStatus::Refunded;
        self.pack_escrow = self.pack_escrow.saturating_sub(total);
        self.revenue = self.revenue.saturating_sub(price);
        events::emit(
            "pack_refunded",
            json!({
                "pack_id": pack_id, "owner_id": owner, "price": U128(price),
                "storage_refund": U128(storage_refund), "total": U128(total),
                "storage_used": storage_used,
                "by": env::predecessor_account_id(), "block_height": env::block_height(),
            }),
        );
        Self::refund(&owner, total);
        U128(total)
    }
}

impl Contract {
    /// Impute `added` octets au pack : `storage_used` augmente et l'engagement `pack_escrow` baisse
    /// d'autant (dans la limite du prépayé restant : au-delà, c'est le contrat qui paie, comme les
    /// graines des relances).
    fn charge_pack_storage(&mut self, pack_id: u64, added: u64) {
        let Some(pack) = self.packs.get(&pack_id) else { return };
        let prepaid = self.series_ref(pack.series_id).storage_per_pack;
        let before = prepaid.saturating_sub(pack.storage_used as u64);
        let used = (pack.storage_used as u64).saturating_add(added).min(u32::MAX as u64) as u32;
        let after = prepaid.saturating_sub(used as u64);
        let cost = env::storage_byte_cost().as_yoctonear();
        self.pack_escrow = self.pack_escrow.saturating_sub(cost * (before - after) as u128);
        // Même taille borsh : la réécriture du pack ne change pas le stockage mesuré.
        self.packs.get_mut(&pack_id).unwrap().storage_used = used;
    }

    fn schedule_step(&self, pack_id: u64, attempt: u32, step: u8) {
        Promise::new(env::current_account_id())
            .function_call(
                "reveal_step".to_string(),
                json!({ "pack_id": pack_id, "attempt": attempt, "step": step })
                    .to_string()
                    .into_bytes(),
                NearToken::from_yoctonear(0),
                self.gas_for_step(step),
            )
            .detach();
    }

    /// Tirage final + création des cartes + journal. Aucun chemin d'échec qui dépende du résultat :
    /// gaz fixe, stockage prépayé (borne du pire cas, gold pack et valeur compris), aucun `require`
    /// sur les cartes, la table de taux, les compteurs (pitié, burns) ou la valeur (dépassements
    /// exclus par la validation de la série).
    fn finalize_pack(&mut self, pack_id: u64, mut pack: Pack, start: u64) {
        let series_id = pack.series_id;
        let owner = pack.owner_id.clone();
        let mut series = self.series.get(series_id).cloned().unwrap_or_else(|| env::panic_str("Série inconnue"));
        let mech = series.table.mechanics.clone();
        let (price, series_storage_per_pack) = (series.table.price.0, series.storage_per_pack);

        // Table de taux du pack : pitié (même aléa `acc`, tag 2), rush figé à l'achat.
        let rush = pack.flags & FLAG_RUSH != 0;
        let mut mode = PackMode::Base;
        let mut pity_ev = Value::Null;
        let mut burned: Option<(Vec<u32>, BurnParams)> = None;
        let mut burn_seq = None;
        let mut resurrect_seq = None;
        if let Some(m) = &mech {
            let mut pity_gold = false;
            let mut pity_n = None;
            if let Some(p) = &m.pity {
                let nb = self.pity.get(&(owner.clone(), series_id)).copied().unwrap_or(0);
                let (g, roll, p_ppb) = draw::pity_is_gold(p, nb, &pack.acc);
                pity_gold = g;
                pity_n = Some(nb);
                pity_ev = json!({ "before": nb, "gold_roll": roll, "p_ppb": p_ppb, "gold": g });
            }
            mode = draw::pack_mode(pity_gold, rush);
            if let Some(nb) = pity_n {
                // Le compteur repart à 0 après un gold pack seulement ; un pack rush le fait monter.
                let after = draw::pity_after(nb, pity_gold);
                self.pity.insert((owner.clone(), series_id), after);
                pity_ev["after"] = json!(after);
            }
            if let Some(bp) = &m.burn {
                if let Some(b) = self.series_burns.get(&series_id) {
                    burned = Some((b.burned.clone(), bp.clone()));
                    burn_seq = Some(b.seq);
                    resurrect_seq = Some(series.resurrect_seq);
                }
            }
            // La brûlable garantie et la répartition de la valeur lisent les brûlables du moment,
            // résurrections comprises : leur numéro est journalisé.
            if m.value.is_some() {
                resurrect_seq = Some(series.resurrect_seq);
            }
        }
        match mode {
            PackMode::Gold => pack.flags |= FLAG_GOLD,
            PackMode::Rush => pack.flags |= FLAG_MODE_RUSH,
            PackMode::Base => {}
        }

        pack.revealed_at_ms = env::block_timestamp_ms();
        pack.status = PackStatus::Revealed;
        let acc = pack.acc;
        let seeds_ev = Self::seeds_json(pack_id, &pack, &series.table_hash.unwrap_or([0; 32]));
        self.packs.insert(pack_id, pack);

        let resurrectable = crate::mechanics::resurrectable(&series.table).to_vec();
        let bv = burned.as_ref().map(|(b, p)| draw::BurnView {
            burned: b,
            floor_bps: p.floor_bps,
            prior_k: p.prior_k,
            resurrectable: &resurrectable,
        });
        // Gold pack : un emplacement par plancher de la table gold. Pack normal : `cards_per_pack`
        // emplacements, le dernier tiré parmi les brûlables si la série a une table de valeur.
        let (slot_draws, burnable_slots) = draw::draw_pack_mech(
            &series.table,
            mode,
            &series.draw_cards,
            &mut series.minted,
            &mut series.mythic_minted,
            bv.as_ref(),
            &acc,
        );
        let n = slot_draws.len();
        let mut draws = Vec::with_capacity(n);
        let mut records = Vec::with_capacity(n);
        let mut minted_tokens = Vec::with_capacity(n);
        for (slot, d) in slot_draws.into_iter().enumerate() {
            let slot = slot as u8;
            let token_id = self.internal_mint_slot(pack_id, &owner);
            if d.kind == CardKind::Mythic {
                let j = d.index as usize;
                if series.revealed_mythics[j].is_none() {
                    series.sealed_tokens[j].push(token_id.clone());
                    events::emit(
                        "mythic_drawn",
                        json!({
                            "series_id": series_id, "mythic_index": d.index,
                            "commitment": series.table.mythics[j].commitment,
                            "token_id": token_id, "pack_id": pack_id,
                        }),
                    );
                }
            }
            draws.push(PackDraw {
                rarity_roll: d.rarity_roll as u64,
                rolled_rarity: d.rolled_rarity,
                final_rarity: d.final_rarity,
                card_roll: d.card_roll,
                kind: d.kind,
                index: d.index,
            });
            records.push(DrawRecord {
                slot,
                rarity_roll: U128(d.rarity_roll),
                rolled_rarity: d.rolled_rarity,
                final_rarity: d.final_rarity,
                card_roll: U128(d.card_roll),
                kind: d.kind,
                index: d.index,
                token_id: token_id.clone(),
            });
            minted_tokens.push(token_id);
        }
        // Valeur du pack : palier tiré dans la table du pack (tag 3), réparti entre les brûlables.
        let mut value_ev = Value::Null;
        let mut value_backing = 0u128;
        let pack_value = draw::pack_value(&series.table, mode, &acc, &burnable_slots).map(|v| {
            value_backing = v.amounts.iter().flatten().sum();
            let mask = burnable_slots.iter().enumerate().fold(0u16, |m, (i, (_, b))| if *b { m | (1u16 << i) } else { m });
            value_ev = json!({
                "roll": v.roll, "tier": v.tier, "bps": v.bps, "total": U128(v.total),
                "amounts": v.amounts.iter().map(|a| a.map(U128)).collect::<Vec<_>>(),
            });
            PackValue { bps: v.bps, mask }
        });
        if let Some(p) = self.packs.get_mut(&pack_id) {
            p.draws = draws;
            p.value = pack_value;
        }
        // Valeur tirée : elle adosse les brûlables du pack tant qu'elles ne sont pas brûlées.
        self.value_reserved += value_backing;

        Self::emit_mint(&owner, &minted_tokens, pack_id);
        let mut ev = json!({
            "pack_id": pack_id,
            "series_id": series_id,
            "owner_id": owner,
            "table_hash": series.table_hash.map(|h| hex32(&h)),
            "attempt": self.packs.get(&pack_id).map(|p| p.attempt).unwrap_or(0),
            "initial_acc": hex32(&draw::initial_acc(pack_id, owner.as_str(), &series.table_hash.unwrap_or([0; 32]))),
            "seeds": seeds_ev,
            "acc": hex32(&acc),
            "draws": records,
        });
        if mech.is_some() {
            // État figé qui a servi au tirage : table de taux, rush (figé à l'achat), pitié, burns.
            ev["mechanics"] = json!({
                "mode": mode, "rush": rush, "pity": pity_ev, "burn_seq": burn_seq,
                "resurrect_seq": resurrect_seq, "value": value_ev,
            });
        }
        if let Some(slot) = self.series.get_mut(series_id) {
            *slot = series;
        }
        // Stockage réellement écrit par ce reçu, puis remboursement du prépayé non utilisé. Le
        // montant dépend du tirage (cartes scellées, gold pack, premier achat), mais ce n'est
        // qu'un virement sortant : il ne peut pas faire échouer ce reçu (le solde est couvert par
        // `pack_escrow`, que `withdraw_revenue` ne touche jamais).
        let added = self.storage_added_since(start);
        self.charge_pack_storage(pack_id, added);
        let prepaid = series_storage_per_pack;
        let used = self.packs.get(&pack_id).map(|p| p.storage_used).unwrap_or(0);
        let refund = env::storage_byte_cost().as_yoctonear() * prepaid.saturating_sub(used as u64) as u128;
        self.pack_escrow = self.pack_escrow.saturating_sub(price + refund);
        ev["storage"] = json!({
            "prepaid_bytes": prepaid, "used_bytes": used, "refund": U128(refund),
        });
        events::emit("pack_revealed", ev);
        Self::refund(&owner, refund);
    }

    /// Graines journalisées, avec `acc` recalculé après chaque étape depuis `initial_acc`.
    pub(crate) fn seeds_json(pack_id: u64, pack: &Pack, table_hash: &[u8; 32]) -> Vec<Value> {
        let mut acc = draw::initial_acc(pack_id, pack.owner_id.as_str(), table_hash);
        pack.seeds
            .iter()
            .map(|s| {
                acc = draw::mix(&acc, &s.seed, pack_id, pack.owner_id.as_str());
                json!({
                    "attempt": s.attempt, "step": s.step, "block_height": s.block_height,
                    "seed": hex32(&s.seed), "acc": hex32(&acc),
                })
            })
            .collect()
    }
}
