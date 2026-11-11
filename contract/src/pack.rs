//! Achat d'un booster et tirage sur k reçus privés chaînés.
//!
//! `buy_pack` encaisse définitivement (aucune annulation, aucun remboursement hors excédent
//! de dépôt) et programme `reveal_step(pack_id, attempt, 1)`. Chaque étape mélange
//! `env::random_seed()` dans `acc`, puis programme la suivante à gaz fixe. La dernière tire,
//! crée les cartes par mint direct (jamais de `*_transfer_call`) et journalise `pack_revealed`.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::json;
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
        let pack = Pack {
            pack_id,
            series_id,
            owner_id: buyer.clone(),
            price_paid: price,
            storage_prepaid: storage,
            bought_at_height: height,
            status: PackStatus::Pending,
            attempt: 0,
            step: 0,
            acc: draw::initial_acc(pack_id, buyer.as_str(), &table_hash),
            seeds: Vec::new(),
            last_progress_height: height,
            token_ids: Vec::new(),
            draws: Vec::new(),
        };
        self.packs.insert(pack_id, pack);
        // Liste paginée par compte : (compte, rang) → pack_id, et un compteur par compte.
        let rank = self.pack_count_by_owner.get(&buyer).copied().unwrap_or(0);
        self.packs_by_owner.insert((buyer.clone(), rank), pack_id);
        self.pack_count_by_owner.insert(buyer.clone(), rank + 1);
        self.series.get_mut(series_id).unwrap().packs_sold += 1;
        self.revenue += price;

        events::emit(
            "pack_bought",
            json!({
                "pack_id": pack_id, "series_id": series_id, "owner_id": buyer,
                "price": U128(price), "storage_prepaid": U128(storage), "block_height": height,
            }),
        );
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
        pack.seeds.push(SeedRecord { attempt, step, block_height: height, seed, acc_after: pack.acc });

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

        self.finalize_pack(pack);
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
        require!(pack.token_ids.is_empty(), "Tirage déjà écrit : relance interdite");
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

    /// Tirage final + création des cartes + journal. Aucun chemin d'échec.
    fn finalize_pack(&mut self, mut pack: Pack) {
        let pack_id = pack.pack_id;
        let series_id = pack.series_id;
        let mut series = self.series.get(series_id).cloned().unwrap_or_else(|| env::panic_str("Série inconnue"));
        let n = series.table.cards_per_pack;
        let mut draws = Vec::with_capacity(n as usize);
        let mut minted_tokens = Vec::with_capacity(n as usize);

        for slot in 0..n {
            let d = draw::draw_slot_compact(
                &series.table.rarity_weights,
                &series.draw_cards,
                &series.table.mythics,
                &series.minted,
                &series.mythic_minted,
                &pack.acc,
                slot,
            );
            let token_id = self.next_token_id.to_string();
            self.next_token_id += 1;
            let mut sealed = false;
            let mut backing = None;
            let meta;
            match d.kind {
                CardKind::Visible => {
                    let card = self.card_def(series_id, d.index);
                    meta = Self::card_metadata(series_id, &card, pack_id);
                    series.minted[d.index as usize] += 1;
                    backing = card.backing;
                }
                CardKind::Mythic => {
                    meta = Self::build_metadata(series_id, &series, d.kind, d.index, pack_id);
                    let j = d.index as usize;
                    series.mythic_minted[j] += 1;
                    match &series.revealed_mythics[j] {
                        Some(r) => backing = r.content.backing.clone(),
                        None => {
                            sealed = true;
                            series.sealed_tokens[j].push(token_id.clone());
                        }
                    }
                }
            }
            self.tokens.internal_mint_with_refund(token_id.clone(), pack.owner_id.clone(), Some(meta), None);
            self.cards.insert(
                token_id.clone(),
                CardInfo {
                    series_id,
                    kind: d.kind,
                    index: d.index,
                    rarity: d.final_rarity,
                    state: CardState::Normal,
                    sealed,
                },
            );
            if let Some(b) = backing {
                self.backing.insert(token_id.clone(), b);
            }
            if sealed {
                events::emit(
                    "mythic_drawn",
                    json!({
                        "series_id": series_id, "mythic_index": d.index,
                        "commitment": series.table.mythics[d.index as usize].commitment,
                        "token_id": token_id, "pack_id": pack_id,
                    }),
                );
            }
            draws.push(DrawRecord {
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

        near_contract_standards::non_fungible_token::events::NftMint {
            owner_id: &pack.owner_id,
            token_ids: &minted_tokens.iter().map(|s| s.as_str()).collect::<Vec<_>>(),
            memo: Some(&format!("pack {}", pack_id)),
        }
        .emit();

        let seeds: Vec<_> = pack
            .seeds
            .iter()
            .map(|s| {
                json!({
                    "attempt": s.attempt, "step": s.step, "block_height": s.block_height,
                    "seed": hex32(&s.seed), "acc": hex32(&s.acc_after),
                })
            })
            .collect();
        events::emit(
            "pack_revealed",
            json!({
                "pack_id": pack_id,
                "series_id": series_id,
                "owner_id": pack.owner_id,
                "table_hash": series.table_hash.map(|h| hex32(&h)),
                "attempt": pack.attempt,
                "initial_acc": hex32(&draw::initial_acc(pack_id, pack.owner_id.as_str(), &series.table_hash.unwrap_or([0; 32]))),
                "seeds": seeds,
                "acc": hex32(&pack.acc),
                "draws": draws,
            }),
        );

        pack.status = PackStatus::Revealed;
        pack.token_ids = minted_tokens;
        pack.draws = draws;
        self.packs.insert(pack_id, pack);
        if let Some(slot) = self.series.get_mut(series_id) {
            *slot = series;
        }
    }
}
