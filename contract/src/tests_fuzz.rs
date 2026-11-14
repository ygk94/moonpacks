//! Fuzz différentiel du tirage : le code du contrat (`draw.rs`) et le vérificateur Python
//! (`verifier/memaster_verifier/core.py`), nourris des mêmes entrées aléatoires, doivent donner le
//! même résultat au bit près.
//!
//! Chaque cas tire une table **valide** (validée par `validate_table`, comme à l'ouverture), avec
//! des mécaniques au hasard (gold pack à planchers, pitié, burns, rush, résurrection, valeur), un
//! état au hasard (plafonds atteints, raretés épuisées, burns jusqu'au plancher, cartes
//! ressuscitées), une table de taux, un `acc`, puis compare : tirages, compteurs après le pack,
//! brûlables par emplacement, valeur et répartition, pitié (décision, compteur après), et des
//! séquences d'achats du gold rush (fenêtres, pause, plafond par compte).
//!
//! Variables : `MEMASTER_FUZZ_SEED` (graine ; par défaut une graine fixe **et** une graine tirée
//! de l'horloge, imprimée), `MEMASTER_FUZZ_CASES` (cas par graine, 300 par défaut),
//! `MEMASTER_FUZZ_OUT` (écrit le corpus de la graine fixe, pour `verifier/tests/vectors/`).

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{self, json, Value};
use near_sdk::test_utils::VMContextBuilder;
use near_sdk::testing_env;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;
const FIXED_SEED: u64 = 0x6d65_6d61_7374_6572; // "memaster"

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn below(&mut self, n: u64) -> u64 {
        if n == 0 {
            0
        } else {
            self.next() % n
        }
    }
    fn range(&mut self, lo: u64, hi: u64) -> u64 {
        lo + self.below(hi - lo + 1)
    }
    fn chance(&mut self, num: u64, den: u64) -> bool {
        self.below(den) < num
    }
    fn bytes32(&mut self) -> [u8; 32] {
        let mut b = [0u8; 32];
        for c in b.chunks_mut(8) {
            c.copy_from_slice(&self.next().to_le_bytes());
        }
        b
    }
    /// Poids : souvent petits, parfois nuls, parfois énormes (jusqu'à u32::MAX).
    fn weight(&mut self) -> u32 {
        match self.below(10) {
            0 => 0,
            1 => u32::MAX - self.below(3) as u32,
            2 => self.range(1_000_000, u32::MAX as u64) as u32,
            3..=5 => self.range(1, 3) as u32,
            _ => self.range(1, 1_000) as u32,
        }
    }
    fn rarity_visible(&mut self) -> Rarity {
        [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common][self.below(4) as usize]
    }
    fn rarity_any(&mut self) -> Rarity {
        Rarity::ALL[self.below(5) as usize]
    }
}

fn hex(b: &[u8]) -> String {
    hex_encode(b)
}

fn card(i: usize, rarity: Rarity, weight: u32, cap: Option<u32>, backed: bool) -> CardDef {
    CardDef {
        card_id: format!("c{i:03}"),
        title: format!("C{i}"),
        rarity,
        weight,
        cap,
        media: None,
        reference: None,
        backing: backed.then(|| Backing { asset_id: format!("nep141:c{i}.near"), amount: U128(1 + i as u128) }),
    }
}

fn rw(r: &mut Rng, mythic_ok: bool) -> RarityWeights {
    loop {
        let w = RarityWeights {
            mythic: if mythic_ok && r.chance(1, 2) { r.weight() } else { 0 },
            legendary: if r.chance(2, 3) { r.weight() } else { 0 },
            epic: if r.chance(2, 3) { r.weight() } else { 0 },
            rare: if r.chance(2, 3) { r.weight() } else { 0 },
            common: r.weight().max(1),
        };
        if w.total() > 0 {
            return w;
        }
    }
}

/// Poids d'un emplacement de gold pack : nuls sous le plancher, au moins un poids non nul.
fn gold_weights(r: &mut Rng, floor: Rarity, mythic_ok: bool) -> RarityWeights {
    let mut w = RarityWeights { mythic: 0, legendary: 0, epic: 0, rare: 0, common: 0 };
    for x in Rarity::ALL {
        if x.index() > floor.index() || (x == Rarity::Mythic && !mythic_ok) {
            continue;
        }
        let v = if r.chance(2, 3) { r.weight() } else { 0 };
        match x {
            Rarity::Mythic => w.mythic = v,
            Rarity::Legendary => w.legendary = v,
            Rarity::Epic => w.epic = v,
            Rarity::Rare => w.rare = v,
            Rarity::Common => w.common = v,
        }
    }
    if w.total() == 0 {
        // Le plancher lui-même (une mythique seulement si elle est pondérée).
        match floor {
            Rarity::Mythic if mythic_ok => w.mythic = 1,
            Rarity::Mythic | Rarity::Legendary => w.legendary = 1,
            Rarity::Epic => w.epic = 1,
            Rarity::Rare => w.rare = 1,
            Rarity::Common => w.common = 1,
        }
    }
    w
}

fn tiers(r: &mut Rng, lo: u32, hi: u32) -> Vec<ValueTier> {
    (0..r.range(1, 6))
        .map(|_| {
            let bps = r.range(lo as u64, hi as u64) as u32;
            let w = if r.chance(1, 10) { u32::MAX } else { r.range(1, 1_000) as u32 };
            (bps, w)
        })
        .collect()
}

/// Table valide au hasard (validée par le contrat).
fn random_table(r: &mut Rng) -> SeriesTable {
    let n_myth = r.below(4) as usize;
    let mythics: Vec<MythicCommitment> = (0..n_myth)
        .map(|j| MythicCommitment {
            commitment: hex(&env::sha256(format!("c{j}").as_bytes())),
            content_hash: hex(&env::sha256(format!("h{j}").as_bytes())),
            weight: if r.chance(3, 4) { r.weight() } else { 0 },
            cap: r.range(1, 3) as u32,
        })
        .collect();
    let mythic_ok = mythics.iter().any(|m| m.weight > 0);
    let base = rw(r, mythic_ok);
    let n = r.range(1, 40) as usize;
    let mut cards: Vec<CardDef> = (0..n)
        .map(|i| {
            let cap = if r.chance(1, 3) { Some(r.range(1, 4) as u32) } else { None };
            card(i, r.rarity_visible(), r.weight(), cap, r.chance(2, 5))
        })
        .collect();
    let mut mech = None;
    if r.chance(3, 4) {
        let mut m = Mechanics { gold: None, pity: None, burn: None, rush: None, resurrection: None, value: None };
        if r.chance(2, 3) {
            let slots = (0..r.range(1, 10))
                .map(|_| {
                    let floor = r.rarity_any();
                    let floor = if floor == Rarity::Mythic && !mythic_ok { Rarity::Legendary } else { floor };
                    let own = r.chance(1, 2) || draw::gold_slot_weights(&base, &GoldSlot { floor, weights: None, burnable: false }).total() == 0;
                    let weights = own.then(|| gold_weights(r, floor, mythic_ok));
                    GoldSlot { floor, weights, burnable: r.chance(1, 4) }
                })
                .collect();
            m.gold = Some(GoldParams { slots });
            if r.chance(3, 4) {
                let p0 = r.below(PPB / 100) as u32;
                let p_max = r.range(p0 as u64, PPB) as u32;
                let k = if r.chance(1, 4) { PPB as u32 } else { r.below(1_000_000) as u32 };
                let n_max = r.chance(1, 3).then(|| r.range(1, MAX_PITY_N as u64) as u32);
                let p_max = if p_max == 0 && n_max.is_none() { 1 } else { p_max };
                m.pity = Some(PityParams { p0_ppb: p0, k_ppb: k, p_max_ppb: p_max, n_max });
            }
        }
        if r.chance(1, 2) {
            let floor_bps = [0, 1, 2_500, 9_999, 10_000][r.below(5) as usize];
            let prior_k = [0, 1, 20, MAX_BURN_PRIOR_K][r.below(4) as usize];
            m.burn = Some(BurnParams { floor_bps, prior_k });
        }
        if r.chance(1, 3) {
            let bucket = r.range(1, 5);
            let mw = r.range(1, 4);
            let ml = r.range(mw + 1, 96);
            let max_ratio = 10_000 * ml / mw - 1;
            m.rush = Some(RushParams {
                ratio_bps: r.range(10_000, max_ratio.min(u32::MAX as u64)) as u32,
                min_packs: r.range(1, 5) as u32,
                window_blocks: mw * bucket,
                baseline_blocks: ml * bucket,
                bucket_blocks: bucket,
                duration_blocks: r.range(1, 30),
                cooldown_blocks: r.below(30),
                max_per_account: r.range(1, 4) as u32,
                weights: rw(r, mythic_ok),
            });
        }
        if r.chance(1, 2) {
            let price = match r.below(5) {
                0 => 1,
                1 => r.range(1, 20_000) as u128,
                2 => NEAR / 10,
                3 => NEAR * r.range(1, 1_000) as u128 + r.below(10_000) as u128,
                _ => u64::MAX as u128 * r.range(1, 1 << 20) as u128,
            };
            let mult = |r: &mut Rng| if r.chance(1, 10) { MAX_VALUE_MULT } else { r.range(1, 1_000) as u32 };
            m.value = Some(ValueParams {
                normal: tiers(r, MIN_NORMAL_VALUE_BPS, MAX_NORMAL_VALUE_BPS),
                gold: tiers(r, 1, MAX_VALUE_BPS),
                rush: tiers(r, 1, MAX_VALUE_BPS),
                multipliers: RarityWeights { mythic: 0, legendary: mult(r), epic: mult(r), rare: mult(r), common: mult(r) },
            });
            // Le prix doit tenir sur u128 avec ces valeurs (sinon le contrat refuse la table).
            let v = m.value.as_ref().unwrap();
            let max_bps = v.normal.iter().chain(&v.gold).chain(&v.rush).map(|x| x.0).max().unwrap() as u128;
            let max_mult = [v.multipliers.legendary, v.multipliers.epic, v.multipliers.rare, v.multipliers.common]
                .into_iter()
                .max()
                .unwrap() as u128;
            let fits = |p: u128| p.checked_mul(max_bps).and_then(|x| (x / 10_000).checked_mul(max_mult)).is_some();
            let price = if fits(price) { price } else { NEAR / 10 };
            mech = Some((m, price));
        } else {
            mech = Some((m, NEAR / 10));
        }
    }
    let (mechanics, price) = match mech {
        Some((m, p)) => (Some(m), p),
        None => (None, NEAR / 10),
    };
    let mut t = SeriesTable {
        kinds: None,
        name: "Fuzz".into(),
        price: U128(price),
        cards_per_pack: r.range(1, MAX_CARDS_PER_PACK as u64) as u8,
        rarity_weights: base,
        cards: vec![],
        mythics,
        royalties: vec![],
        mechanics,
    };
    // Couverture : une carte de poids non nul par rareté pondérée, une commune illimitée, une
    // brûlable garantie si une règle la demande.
    for r_ in [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common] {
        if crate::mechanics::rarity_used(&t, r_) && !cards.iter().any(|c| c.rarity == r_ && c.weight > 0) {
            let i = cards.len();
            cards.push(card(i, r_, r.range(1, 100) as u32, None, false));
        }
    }
    if !cards.iter().any(|c| c.rarity == Rarity::Common && c.cap.is_none() && c.weight > 0) {
        let i = cards.len();
        cards.push(card(i, Rarity::Common, r.range(1, 1_000) as u32, None, r.chance(1, 2)));
    }
    if crate::mechanics::needs_burnable(&t) && !cards.iter().any(|c| c.backing.is_some() && c.cap.is_none() && c.weight > 0) {
        let i = cards.len();
        let rar = if r.chance(1, 2) { Rarity::Common } else { Rarity::Rare };
        let rar = if crate::mechanics::rarity_used(&t, rar) { rar } else { Rarity::Common };
        cards.push(card(i, rar, r.range(1, 100) as u32, None, true));
    }
    // Les cartes d'une rareté jamais tirable sont refusées : elles passent en commune.
    for c in cards.iter_mut() {
        if !crate::mechanics::rarity_used(&t, c.rarity) {
            c.rarity = Rarity::Common;
        }
    }
    // Résurrection : épiques et légendaires non adossées.
    if let Some(m) = t.mechanics.as_mut() {
        if r.chance(1, 2) {
            let eligible: Vec<u32> = cards
                .iter()
                .enumerate()
                .filter(|(_, c)| matches!(c.rarity, Rarity::Epic | Rarity::Legendary) && c.backing.is_none())
                .filter(|_| r.chance(2, 3))
                .map(|(i, _)| i as u32)
                .collect();
            m.resurrection = Some(ResurrectionParams { eligible });
        }
    }
    t.cards = cards;
    crate::series::validate_table(&t);
    t
}

struct Case {
    input: Value,
    expected: Value,
}

fn random_case(r: &mut Rng, id: usize) -> Case {
    let t = random_table(r);
    let mut cards: Vec<DrawCard> = t.cards.iter().map(DrawCard::from).collect();
    // Résurrections déjà faites (une partie de la liste hachée).
    let eligible = crate::mechanics::resurrectable(&t).to_vec();
    for &i in &eligible {
        if r.chance(1, 2) {
            cards[i as usize].backed = true;
        }
    }
    // État : plafonds souvent atteints, burns jusqu'au plancher (tout brûlé) ou au hasard.
    let mut minted: Vec<u32> = t
        .cards
        .iter()
        .map(|c| match c.cap {
            Some(cap) => match r.below(3) {
                0 => cap,
                1 => r.below(cap as u64 + 1) as u32,
                _ => 0,
            },
            None => match r.below(4) {
                0 => 0,
                1 => r.range(1, 5) as u32,
                2 => r.range(1, 10_000) as u32,
                _ => r.range(1, 100) as u32,
            },
        })
        .collect();
    let mut mythic_minted: Vec<u32> =
        t.mythics.iter().map(|m| if r.chance(1, 2) { m.cap } else { r.below(m.cap as u64 + 1) as u32 }).collect();
    let burned: Vec<u32> = minted
        .iter()
        .map(|&n| match r.below(4) {
            0 => n,
            1 => r.below(n as u64 + 1) as u32,
            _ => 0,
        })
        .collect();
    let m = t.mechanics.clone();
    let mut modes = vec![PackMode::Base];
    if m.as_ref().is_some_and(|m| m.gold.is_some()) {
        modes.push(PackMode::Gold);
    }
    if m.as_ref().is_some_and(|m| m.rush.is_some()) {
        modes.push(PackMode::Rush);
    }
    let mode = modes[r.below(modes.len() as u64) as usize];
    let acc = r.bytes32();
    let burn = m.as_ref().and_then(|m| m.burn.clone());
    let bv = burn.as_ref().map(|b| draw::BurnView {
        burned: &burned,
        floor_bps: b.floor_bps,
        prior_k: b.prior_k,
        resurrectable: &eligible,
    });
    let minted_before = minted.clone();
    let mythic_before = mythic_minted.clone();
    let (draws, slots) = draw::draw_pack_mech(&t, mode, None, &cards, &mut minted, &mut mythic_minted, bv.as_ref(), &acc);
    let value = draw::pack_value(&t, mode, None, &acc, &slots);

    // Pitié : compteur au hasard, jusqu'à u32::MAX.
    let pity = m.as_ref().and_then(|m| m.pity.clone()).map(|p| {
        let n = match r.below(4) {
            0 => 0,
            1 => u32::MAX - r.below(2) as u32,
            2 => p.n_max.map(|x| x.saturating_sub(1)).unwrap_or(0),
            _ => r.below(20_000) as u32,
        };
        let (g, roll, pp) = draw::pity_is_gold(&p, n, &acc);
        json!({ "n": n, "gold": g, "gold_roll": roll, "p_ppb": pp, "after": draw::pity_after(n, g) })
    });

    // Gold rush : séquence d'achats (hauteurs croissantes, sauts aux frontières des fenêtres).
    let rush = m.as_ref().and_then(|m| m.rush.clone()).map(|p| {
        let mut st = RushState::default();
        let mut accounts: std::collections::BTreeMap<u8, (u64, u32)> = Default::default();
        let mut h = r.range(0, 1_000);
        let mut buys = Vec::new();
        for _ in 0..r.range(1, 80) {
            h += match r.below(6) {
                0 => 0,
                1 => p.bucket_blocks,
                2 => p.baseline_blocks,
                3 => p.duration_blocks,
                4 => p.duration_blocks + p.cooldown_blocks,
                _ => r.below(3),
            };
            let who = r.below(3) as u8;
            let o = draw::rush_on_buy(&p, &mut st, h);
            let prev = if o.active { accounts.get(&who).copied() } else { None };
            let (rush, capped, entry) = draw::rush_account(&p, o.active, st.last_trigger, prev);
            if rush {
                if let Some(e) = entry {
                    accounts.insert(who, e);
                }
            }
            buys.push(json!({
                "h": h, "who": who, "active": o.active, "window_count": o.window_count,
                "baseline_count": o.baseline_count, "triggered": o.triggered, "rush": rush,
                "capped": capped, "last_trigger": st.last_trigger,
            }));
        }
        json!({ "buys": buys, "rush_count": st.rush_count })
    });

    let draws_json: Vec<Value> = draws
        .iter()
        .enumerate()
        .map(|(slot, d)| {
            json!({
                "slot": slot, "rarity_roll": d.rarity_roll.to_string(), "rolled_rarity": d.rolled_rarity,
                "final_rarity": d.final_rarity, "card_roll": d.card_roll.to_string(), "kind": d.kind,
                "index": d.index,
            })
        })
        .collect();
    let value_json = value.map(|v| {
        json!({
            "roll": v.roll, "tier": v.tier, "bps": v.bps, "total": v.total.to_string(),
            "amounts": v.amounts.iter().map(|a| a.map(|x| x.to_string())).collect::<Vec<_>>(),
        })
    });
    Case {
        input: json!({
            "case": id,
            "table": serde_json::to_value(&t).unwrap(),
            "mode": mode,
            "acc": hex(&acc),
            "minted": minted_before,
            "mythic_minted": mythic_before,
            "burned": burned,
            "backed": cards.iter().map(|c| c.backed).collect::<Vec<_>>(),
            "pity_n": pity.as_ref().map(|p| p["n"].clone()),
            "rush_heights": rush.as_ref().map(|x| x["buys"].as_array().unwrap().iter().map(|b| json!([b["h"], b["who"]])).collect::<Vec<_>>()),
        }),
        expected: json!({
            "draws": draws_json,
            "slots": slots.iter().map(|(r, b)| json!([r, b])).collect::<Vec<_>>(),
            "minted_after": minted,
            "mythic_minted_after": mythic_minted,
            "value": value_json,
            "pity": pity,
            "rush": rush,
        }),
    }
}

fn corpus(seed: u64, n: usize) -> Value {
    let mut r = Rng(seed);
    let cases: Vec<Value> = (0..n)
        .map(|i| {
            // Contexte neuf par cas : le gaz du mock (sha256) s'accumule sinon.
            env_ctx();
            let c = random_case(&mut r, i);
            json!({ "input": c.input, "expected": c.expected })
        })
        .collect();
    json!({
        "source": "contract/src/tests_fuzz.rs (memaster::draw sur des tables valides au hasard)",
        "seed": seed,
        "cases": cases,
    })
}

fn run_python(doc: &Value, seed: u64) {
    let root = env!("CARGO_MANIFEST_DIR");
    let dir = std::env::temp_dir().join(format!("memaster-fuzz-{}-{seed}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("cases.json");
    std::fs::write(&path, serde_json::to_vec(doc).unwrap()).unwrap();
    let out = std::process::Command::new("python3")
        .arg("-I")
        .arg(format!("{root}/../verifier/tests/crosscheck.py"))
        .arg(&path)
        .output()
        .expect("python3 requis pour ce test");
    let _ = std::fs::remove_dir_all(&dir);
    assert!(
        out.status.success(),
        "divergence contrat / vérificateur (MEMASTER_FUZZ_SEED={seed}) :\n{}{}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
    );
    println!("graine {seed} : {}", String::from_utf8_lossy(&out.stdout).trim());
}

fn env_ctx() {
    testing_env!(VMContextBuilder::new().build());
}

#[test]
fn contract_and_python_verifier_agree_on_random_inputs() {
    env_ctx();
    let n: usize = std::env::var("MEMASTER_FUZZ_CASES").ok().and_then(|s| s.parse().ok()).unwrap_or(300);
    let seeds: Vec<u64> = match std::env::var("MEMASTER_FUZZ_SEED").ok().and_then(|s| s.parse().ok()) {
        Some(s) => vec![s],
        None => {
            let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos() as u64;
            vec![FIXED_SEED, t]
        }
    };
    for seed in seeds {
        let doc = corpus(seed, n);
        if seed == FIXED_SEED {
            if let Ok(p) = std::env::var("MEMASTER_FUZZ_OUT") {
                std::fs::write(&p, serde_json::to_string(&doc).unwrap() + "\n").unwrap();
                println!("écrit : {p}");
            }
        }
        run_python(&doc, seed);
    }
}

/// Le générateur couvre bien les cas limites visés (sinon le fuzz ne prouve rien).
#[test]
fn fuzz_generator_reaches_edge_cases() {
    env_ctx();
    let doc = corpus(FIXED_SEED, 300);
    let cases = doc["cases"].as_array().unwrap();
    let mut seen = std::collections::BTreeMap::<&str, usize>::new();
    for c in cases {
        let (i, e) = (&c["input"], &c["expected"]);
        let m = &i["table"]["mechanics"];
        let mut hit = |k: &'static str, b: bool| {
            if b {
                *seen.entry(k).or_default() += 1;
            }
        };
        let draws = e["draws"].as_array().unwrap();
        hit("gold", i["mode"] == "gold");
        hit("rush", i["mode"] == "rush");
        hit("retombee", draws.iter().any(|d| d["rolled_rarity"] != d["final_rarity"]));
        hit("mythique", draws.iter().any(|d| d["kind"] == "mythic"));
        hit("valeur", !e["value"].is_null());
        hit("burns", !m["burn"].is_null());
        hit("ressuscitee", {
            let el: Vec<u64> = m["resurrection"]["eligible"].as_array().map(|a| a.iter().map(|x| x.as_u64().unwrap()).collect()).unwrap_or_default();
            el.iter().any(|&j| i["backed"][j as usize] == true)
        });
        hit("pitie_plafond", e["pity"]["n"].as_u64().is_some_and(|n| n >= u32::MAX as u64 - 1));
        hit("rush_declenche", e["rush"]["rush_count"].as_u64().is_some_and(|n| n > 0));
        hit("rush_plafonne", e["rush"]["buys"].as_array().is_some_and(|b| b.iter().any(|x| x["capped"] == true)));
        hit("tout_brule", {
            let (mn, bn) = (i["minted"].as_array().unwrap(), i["burned"].as_array().unwrap());
            !m["burn"].is_null() && mn.iter().zip(bn).any(|(a, b)| a.as_u64().unwrap() > 0 && a == b)
        });
    }
    for k in [
        "gold", "rush", "retombee", "mythique", "valeur", "burns", "ressuscitee", "pitie_plafond", "rush_declenche",
        "rush_plafonne", "tout_brule",
    ] {
        assert!(seen.get(k).copied().unwrap_or(0) >= 3, "cas limite trop rare : {k} ({seen:?})");
    }
}

// ----------------------------------------------------------------- validateur hors ligne

/// Mutation au hasard d'une table valide : la plupart la rendent invalide, certaines non.
fn mutate(r: &mut Rng, t: &mut SeriesTable) -> &'static str {
    let n = t.cards.len();
    if n == 0 {
        return "aucune carte";
    }
    let pick = |r: &mut Rng| r.below(n as u64) as usize;
    match r.below(40) {
        0 => { t.name = String::new(); "name vide" }
        1 => { t.name = "é".repeat(33); "name de 66 octets" }
        2 => { t.price = U128(0); "prix nul" }
        3 => { t.cards_per_pack = [0, 11, 255][r.below(3) as usize]; "cards_per_pack" }
        4 => { t.rarity_weights = RarityWeights { mythic: 0, legendary: 0, epic: 0, rare: 0, common: 0 }; "poids nuls" }
        5 => { t.rarity_weights.common = 0; "commune à 0" }
        6 => { t.rarity_weights.mythic = r.range(1, 10) as u32; "poids mythique" }
        7 => { if let Some(m) = t.mythics.first_mut() { m.cap = [0, 101][r.below(2) as usize]; } "plafond mythique" }
        8 => { if t.mythics.len() >= 2 { t.mythics[1].commitment = t.mythics[0].commitment.clone(); } "engagement en double" }
        9 => { if let Some(m) = t.mythics.first_mut() { m.content_hash = m.content_hash.to_uppercase(); } "hex majuscule" }
        10 => { t.royalties = vec![Royalty { account_id: "a.near".parse().unwrap(), bps: r.range(4_000, 6_000) as u16 }]; "redevances" }
        11 => { let i = pick(r); t.cards[i].card_id = "x".repeat(r.range(64, 65) as usize); "card_id long" }
        12 => { let i = pick(r); t.cards[i].title = String::new(); "titre vide" }
        13 => { let i = pick(r); t.cards[i].backing = Some(Backing { asset_id: "a".into(), amount: U128(0) }); "montant nul" }
        14 => { let i = pick(r); t.cards[i].rarity = Rarity::Mythic; "carte mythique" }
        15 => { if n >= 2 { let id = t.cards[0].card_id.clone(); t.cards[1].card_id = id; } "card_id en double" }
        16 => { let rr = r.rarity_visible(); for c in t.cards.iter_mut().filter(|c| c.rarity == rr) { c.weight = 0; } "rareté sans poids" }
        17 => { for c in t.cards.iter_mut().filter(|c| c.rarity == Rarity::Common) { c.cap = Some(r.range(1, 3) as u32); } "communes plafonnées" }
        18 => { for c in t.cards.iter_mut() { if r.chance(1, 2) { c.backing = None; } } "adossements retirés" }
        19 => { let i = pick(r); t.cards[i].rarity = r.rarity_visible(); "rareté changée" }
        20 => { let i = pick(r); t.cards[i].media = Some("m".repeat(r.range(255, 257) as usize)); "media long" }
        21 => { t.rarity_weights.legendary = 0; t.rarity_weights.epic = 0; "raretés retirées" }
        _ => {
            let Some(m) = t.mechanics.as_mut() else { t.cards.clear(); return "aucune carte" };
            match r.below(18) {
                0 => { m.gold = None; "gold retiré" }
                1 => { if let Some(b) = m.burn.as_mut() { b.floor_bps = r.range(10_000, 10_001) as u32; } "floor_bps" }
                2 => { if let Some(b) = m.burn.as_mut() { b.prior_k = r.range(1_000_000, 1_000_001) as u32; } "prior_k" }
                3 => { if let Some(p) = m.pity.as_mut() { p.n_max = Some([0, 10_000, 10_001][r.below(3) as usize]); } "n_max" }
                4 => { if let Some(p) = m.pity.as_mut() { p.p0_ppb = p.p_max_ppb.saturating_add(r.below(2) as u32); } "p0 > p_max" }
                5 => { if let Some(p) = m.pity.as_mut() { p.p_max_ppb = 0; p.p0_ppb = 0; p.n_max = None; } "pitié inatteignable" }
                6 => { if let Some(x) = m.rush.as_mut() { x.window_blocks += r.below(2); } "window non multiple" }
                7 => { if let Some(x) = m.rush.as_mut() { x.ratio_bps = (10_000 * (x.baseline_blocks / x.bucket_blocks) / (x.window_blocks / x.bucket_blocks)) as u32 - r.below(2) as u32; } "ratio limite" }
                8 => { if let Some(x) = m.rush.as_mut() { x.min_packs = 0; } "min_packs" }
                9 => { if let Some(x) = m.rush.as_mut() { x.baseline_blocks = x.bucket_blocks * r.range(95, 97); } "96 seaux" }
                10 => { if let Some(v) = m.value.as_mut() { v.normal = vec![(r.range(1_999, 2_000) as u32, 1)]; } "value.normal bas" }
                11 => { if let Some(v) = m.value.as_mut() { v.multipliers.rare = r.below(2) as u32; } "multiplicateur rare" }
                12 => { if let Some(v) = m.value.as_mut() { v.multipliers.mythic = r.below(2) as u32; } "multiplicateur mythique" }
                13 => { t.price = U128(u128::MAX / r.range(1, 1_000_000) as u128); "prix énorme" }
                14 => { m.resurrection = Some(ResurrectionParams { eligible: vec![r.below(n as u64 + 2) as u32] }); "résurrection d'une carte au hasard" }
                15 => { m.resurrection = Some(ResurrectionParams { eligible: vec![1, 0] }); "résurrection non triée" }
                16 => { if let Some(g) = m.gold.as_mut() { g.slots[0].floor = Rarity::Common; g.slots[0].weights = Some(RarityWeights { mythic: 0, legendary: 0, epic: 0, rare: 0, common: 0 }); } "emplacement or nul" }
                _ => { if let Some(g) = m.gold.as_mut() { g.slots[0].floor = Rarity::Legendary; g.slots[0].weights = Some(RarityWeights { mythic: 0, legendary: 1, epic: 1, rare: 0, common: 0 }); } "sous le plancher" }
            }
        }
    }
}

thread_local! {
    static QUIET: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}

#[test]
fn offline_validator_agrees_with_contract_validation() {
    // Les refus du contrat paniquent : leurs messages sont tus pour ce test seulement.
    let prev = std::sync::Arc::new(std::panic::take_hook());
    let p2 = prev.clone();
    std::panic::set_hook(Box::new(move |info| {
        if !QUIET.with(|q| q.get()) {
            p2(info);
        }
    }));
    let seed: u64 = std::env::var("MEMASTER_FUZZ_SEED").ok().and_then(|s| s.parse().ok()).unwrap_or(FIXED_SEED ^ 0x5eed);
    let n: usize = std::env::var("MEMASTER_FUZZ_CASES").ok().and_then(|s| s.parse().ok()).unwrap_or(300);
    let mut r = Rng(seed);
    let mut raws = Vec::new();
    let mut expected = Vec::new();
    let mut labels = Vec::new();
    for _ in 0..n {
        env_ctx();
        let mut t = random_table(&mut r);
        let mut what = vec![];
        for _ in 0..r.range(1, 2) {
            what.push(mutate(&mut r, &mut t));
        }
        let tt = t.clone();
        QUIET.with(|q| q.set(true));
        let ok = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            env_ctx();
            crate::series::validate_table(&tt);
        }))
        .is_ok();
        QUIET.with(|q| q.set(false));
        raws.push(serde_json::to_string(&t).unwrap());
        expected.push(ok);
        labels.push(what.join(" + "));
    }
    let root = env!("CARGO_MANIFEST_DIR");
    let dir = std::env::temp_dir().join(format!("memaster-validate-{}-{seed}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("tables.json");
    std::fs::write(&path, format!("[{}]", raws.join(","))).unwrap();
    let script = "import json,sys; sys.path.insert(0, sys.argv[1]); import validate_series as v; \
        ts = json.load(open(sys.argv[2], encoding='utf-8')); \
        print(json.dumps([[v.validate_table(t).ok, v.validate_table(t).errors[:1]] for t in ts]))";
    let out = std::process::Command::new("python3")
        .arg("-I")
        .arg("-c")
        .arg(script)
        .arg(format!("{root}/scripts"))
        .arg(&path)
        .output()
        .expect("python3 requis pour ce test");
    let _ = std::fs::remove_dir_all(&dir);
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
    let got: Vec<(bool, Vec<String>)> = serde_json::from_slice(&out.stdout).unwrap();
    let mut diffs = vec![];
    for (i, ((g, e), want)) in got.iter().zip(&expected).enumerate() {
        if g != want {
            diffs.push(format!("cas {i} ({}) : contrat {}, validateur {} {:?}", labels[i], if *want { "accepte" } else { "refuse" }, if *g { "accepte" } else { "refuse" }, e));
        }
    }
    let refused = expected.iter().filter(|x| !**x).count();
    assert!(diffs.is_empty(), "graine {seed} :\n{}", diffs.join("\n"));
    assert!(refused > n / 3 && refused < n, "mutations peu variées : {refused} refus sur {n}");
    println!("graine {seed} : {n} tables, {refused} refusées, accord complet");
}
