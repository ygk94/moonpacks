//! Achat d'un booster et tirage sur k reçus privés chaînés.
//!
//! `buy_pack` encaisse définitivement (aucune annulation, aucun remboursement hors excédent
//! de dépôt) et programme `reveal_step(pack_id, attempt, 1)`. Chaque étape mélange
//! `env::random_seed()` dans `acc`, puis programme la suivante à gaz fixe. La dernière tire,
//! crée les cartes par mint direct (jamais de `*_transfer_call`) et journalise `pack_revealed`.

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
            self.schedule_step(pack_id, attempt, step + 1);
            return;
        }

        #[cfg(feature = "test-hooks")]
        if env::storage_has_key(b"__fail_reveal") {
            env::panic_str("test-hooks: échec simulé du dernier reçu");
        }

        self.finalize_pack(pack_id, pack);
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
    /// `pack_stuck`). Il n'y a volontairement pas de remboursement : le tirage échoué a pu être connu.
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
}

impl Contract {
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
    /// gaz fixe, stockage prépayé (borne du pire cas), aucun `require` sur les cartes, la table de
    /// taux ou les compteurs (pitié, burns).
    fn finalize_pack(&mut self, pack_id: u64, mut pack: Pack) {
        let series_id = pack.series_id;
        let owner = pack.owner_id.clone();
        let mut series = self.series.get(series_id).cloned().unwrap_or_else(|| env::panic_str("Série inconnue"));
        let n = series.table.cards_per_pack;
        let mech = series.table.mechanics.clone();

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
                let (g, roll, p_ppm) = draw::pity_is_gold(p, nb, &pack.acc);
                pity_gold = g;
                pity_n = Some(nb);
                pity_ev = json!({ "before": nb, "gold_roll": roll, "p_ppm": p_ppm, "gold": g });
            }
            mode = draw::pack_mode(pity_gold, rush);
            if let Some(nb) = pity_n {
                // Gold pack (pitié) ou pack rush : le compteur repart à 0.
                let after = if mode == PackMode::Base { nb.saturating_add(1) } else { 0 };
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
        }
        match mode {
            PackMode::Gold => pack.flags |= FLAG_GOLD,
            PackMode::Rush => pack.flags |= FLAG_MODE_RUSH,
            PackMode::Base => {}
        }
        let weights = draw::mode_weights(&series.table, mode).clone();

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
        let mut draws = Vec::with_capacity(n as usize);
        let mut records = Vec::with_capacity(n as usize);
        let mut minted_tokens = Vec::with_capacity(n as usize);
        for slot in 0..n {
            let d = draw::draw_slot_mech(
                &weights,
                &series.draw_cards,
                &series.table.mythics,
                &series.minted,
                &series.mythic_minted,
                bv.as_ref(),
                &acc,
                slot,
            );
            let token_id = self.internal_mint_slot(pack_id, &owner);
            match d.kind {
                CardKind::Visible => series.minted[d.index as usize] += 1,
                CardKind::Mythic => {
                    let j = d.index as usize;
                    series.mythic_minted[j] += 1;
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
        if let Some(p) = self.packs.get_mut(&pack_id) {
            p.draws = draws;
        }

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
                "resurrect_seq": resurrect_seq,
            });
        }
        events::emit("pack_revealed", ev);
        if let Some(slot) = self.series.get_mut(series_id) {
            *slot = series;
        }
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
