//! Tests unitaires des mécaniques (pitié, rareté pilotée par les burns, gold rush, résurrection)
//! et du stockage minimal par carte (listes NEP-181, propriétaire compact).

use crate::draw;
use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::core::NonFungibleTokenCore;
use near_contract_standards::non_fungible_token::enumeration::NonFungibleTokenEnumeration;
use near_sdk::serde_json::{self, Value};
use near_sdk::test_utils::{accounts, VMContextBuilder};
use near_sdk::{testing_env, PromiseResult, RuntimeFeesConfig};
use std::collections::BTreeSet;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;

fn owner() -> AccountId {
    accounts(0)
}
fn alice() -> AccountId {
    accounts(1)
}
fn bob() -> AccountId {
    accounts(2)
}
fn oracle() -> AccountId {
    "oracle.test".parse().unwrap()
}
fn contract_id() -> AccountId {
    "memaster.test".parse().unwrap()
}

fn ctx(pred: AccountId, deposit: u128, height: u64) -> VMContextBuilder {
    let mut b = VMContextBuilder::new();
    b.current_account_id(contract_id())
        .predecessor_account_id(pred.clone())
        .signer_account_id(pred)
        .attached_deposit(NearToken::from_yoctonear(deposit))
        .prepaid_gas(Gas::from_tgas(300))
        .block_height(height)
        .account_balance(NearToken::from_near(1_000));
    b
}

fn set(pred: AccountId, deposit: u128, height: u64) {
    testing_env!(ctx(pred, deposit, height).build());
}

fn set_seed(height: u64, seed: [u8; 32]) {
    let mut c = ctx(contract_id(), 0, height);
    c.random_seed(seed);
    testing_env!(c.build());
}

fn set_result(result: PromiseResult) {
    testing_env!(
        ctx(contract_id(), 0, 50).build(),
        near_sdk::test_vm_config(),
        RuntimeFeesConfig::test(),
        Default::default(),
        vec![result],
    );
}

fn card(id: &str, rarity: Rarity, weight: u32, cap: Option<u32>, backing: bool) -> CardDef {
    CardDef {
        card_id: id.to_string(),
        title: id.to_uppercase(),
        rarity,
        weight,
        cap,
        media: Some(format!("ipfs://{id}")),
        reference: None,
        backing: backing.then(|| Backing { asset_id: format!("nep141:{id}.near"), amount: U128(1_000) }),
    }
}

fn w(m: u32, l: u32, e: u32, r: u32, c: u32) -> RarityWeights {
    RarityWeights { mythic: m, legendary: l, epic: e, rare: r, common: c }
}

fn table(mechanics: Option<Mechanics>) -> SeriesTable {
    SeriesTable {
        kinds: None,
        name: "Mécaniques".into(),
        price: U128(NEAR / 10),
        cards_per_pack: 5,
        rarity_weights: w(0, 1, 9, 30, 960),
        cards: vec![
            card("leg", Rarity::Legendary, 1, None, true),
            card("epic", Rarity::Epic, 1, None, true),
            card("rare", Rarity::Rare, 1, None, false),
            card("com_a", Rarity::Common, 100, None, true),
            card("com_b", Rarity::Common, 100, None, false),
            card("com_c", Rarity::Common, 100, None, true),
            card("epic_b", Rarity::Epic, 1, None, false),
        ],
        mythics: vec![],
        royalties: vec![],
        mechanics,
    }
}

fn gold_w(weights: RarityWeights, floor: Rarity, n: usize) -> GoldParams {
    GoldParams { slots: vec![GoldSlot { floor, weights: Some(weights), burnable: false }; n] }
}

fn gold() -> GoldParams {
    // Gold pack : 5 emplacements légendaires (le test voit tout de suite s'il est utilisé).
    gold_w(w(0, 1, 0, 0, 0), Rarity::Legendary, 5)
}

fn mech(pity: Option<PityParams>, burn: bool, rush: Option<RushParams>) -> Mechanics {
    Mechanics { gold: Some(gold()), pity, burn: burn.then_some(BurnParams { floor_bps: 2_500, prior_k: PRIOR_K }), rush, resurrection: None, value: None }
}

fn contract_with(t: SeriesTable) -> Contract {
    set(owner(), 0, 10);
    let mut c = Contract::new(owner(), Some("redeemer.test".parse().unwrap()), None, None, Some(100), None);
    let id = c.create_series(t);
    c.open_series(id);
    c
}

/// Achat à `height`, sans tirage. Renvoie le pack.
fn buy_at(c: &mut Contract, buyer: AccountId, height: u64) -> u64 {
    let dep = c.get_series(0).required_deposit.0;
    set(buyer, dep, height);
    c.buy_pack(0, None).0 as u64
}

fn reveal(c: &mut Contract, pack_id: u64, seed: u8, height: u64) {
    for step in 1..=3u8 {
        set_seed(height + step as u64, [seed.wrapping_add(step); 32]);
        c.reveal_step(pack_id, 0, step);
    }
}

fn buy_reveal(c: &mut Contract, buyer: AccountId, seed: u8, height: u64) -> u64 {
    let p = buy_at(c, buyer, height);
    reveal(c, p, seed, height);
    p
}

fn pack(c: &Contract, id: u64) -> Value {
    c.get_pack(id).unwrap()
}

fn rarities(c: &Contract, id: u64) -> Vec<String> {
    pack(c, id)["draws"].as_array().unwrap().iter().map(|d| d["final_rarity"].as_str().unwrap().to_string()).collect()
}

// ----------------------------------------------------------------- pitié

#[test]
fn pity_n1_makes_every_pack_gold() {
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(1) }), false, None))));
    for k in 0..4u8 {
        let p = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        assert_eq!(pack(&c, p)["mode"], "gold");
        assert!(rarities(&c, p).iter().all(|r| r == "legendary"));
        assert_eq!(c.get_pity(alice(), 0)["n"], 0);
    }
}

#[test]
fn pity_is_guaranteed_at_n_max_minus_one_then_resets() {
    // p0 = k = 0 : seul la garantie peut donner un gold pack.
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(4) }), false, None))));
    let mut modes = vec![];
    for k in 0..9u8 {
        let p = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        modes.push(pack(&c, p)["mode"].as_str().unwrap().to_string());
    }
    assert_eq!(modes, ["base", "base", "base", "gold", "base", "base", "base", "gold", "base"]);
    assert_eq!(c.get_pity(alice(), 0)["n"], 1);
    assert_eq!(c.get_pity(alice(), 0)["guaranteed_in"], 3);
    // Compteur par compte : bob part de zéro.
    assert_eq!(c.get_pity(bob(), 0)["n"], 0);
}

#[test]
fn pity_roll_uses_acc_with_new_tag() {
    // p0 = 50 % : le choix suit exactement gold_roll(acc) < p (mod 10⁹), avec acc final du tirage.
    let p = PityParams { p0_ppb: 500_000_000, k_ppb: 0, p_max_ppb: 500_000_000, n_max: None };
    let mut c = contract_with(table(Some(mech(Some(p.clone()), false, None))));
    let (mut gold_n, mut n) = (0, 0u32);
    for k in 0..40u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let acc: [u8; 32] = hex_decode(pack(&c, id)["acc"].as_str().unwrap()).unwrap().try_into().unwrap();
        let (g, roll, pp) = draw::pity_is_gold(&p, n, &acc);
        assert_eq!(roll as u128, draw::roll(&acc, 0, draw::TAG_GOLD) % 1_000_000_000);
        assert_eq!(pp, 500_000_000);
        assert_eq!(pack(&c, id)["mode"] == "gold", g);
        n = if g { gold_n += 1; 0 } else { n + 1 };
        assert_eq!(c.get_pity(alice(), 0)["n"], n);
    }
    assert!(gold_n > 5 && gold_n < 35, "{gold_n} gold packs sur 40 à 50 %");
}

#[test]
fn pity_probability_grows_linearly_and_caps() {
    // Paramètres de la série v2 : 1 sur 50 000 au départ, 1 sur 25 000 au plus, plafond en 1 000 packs.
    let p = PityParams { p0_ppb: 20_000, k_ppb: 20, p_max_ppb: 40_000, n_max: None };
    assert_eq!(draw::pity_p_ppb(&p, 0), 20_000);
    assert_eq!(draw::pity_p_ppb(&p, 1), 20_020);
    assert_eq!(draw::pity_p_ppb(&p, 500), 30_000);
    assert_eq!(draw::pity_p_ppb(&p, 999), 39_980);
    assert_eq!(draw::pity_p_ppb(&p, 1_000), 40_000);
    assert_eq!(draw::pity_p_ppb(&p, 5_000), 40_000);
    assert_eq!(draw::pity_p_ppb(&p, u32::MAX), 40_000, "aucun dépassement : u128");
    // Bornes extrêmes : jamais plus de 10⁹.
    let q = PityParams { p0_ppb: 1_000_000_000, k_ppb: 1_000_000_000, p_max_ppb: 1_000_000_000, n_max: None };
    assert_eq!(draw::pity_p_ppb(&q, u32::MAX), 1_000_000_000);
    // Sans garantie, même à n = u32::MAX : décision = gold_roll < p, et le compteur sature.
    let acc = [7u8; 32];
    let (g, r, pp) = draw::pity_is_gold(&p, u32::MAX, &acc);
    assert_eq!((g, pp), (r < 40_000, 40_000));
    assert_eq!(draw::pity_after(u32::MAX, false), u32::MAX);
    assert_eq!(draw::pity_after(12, true), 0);
}

#[test]
fn pity_without_guarantee_keeps_climbing() {
    // p = 0 ppb au départ, + 1 ppb par pack, n_max absent : aucun gold pack en 30 packs, le compteur monte.
    let p = PityParams { p0_ppb: 0, k_ppb: 1, p_max_ppb: 40_000, n_max: None };
    let mut c = contract_with(table(Some(mech(Some(p), false, None))));
    for k in 0..30u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        assert_eq!(pack(&c, id)["mode"], "base");
    }
    let v = c.get_pity(alice(), 0);
    assert_eq!(v["n"], 30);
    assert_eq!(v["p_ppb"], 30);
    assert_eq!(v["packs_to_max"], 40_000 - 30);
    assert!(v["guaranteed_in"].is_null(), "{v}");
}

#[test]
fn series_without_pity_has_no_counter() {
    let mut c = contract_with(table(None));
    buy_reveal(&mut c, alice(), 1, 20);
    assert_eq!(c.get_pity(alice(), 0)["enabled"], false);
    assert_eq!(pack(&c, 0)["mode"], "base");
}

// ----------------------------------------------------------------- burns

const FLOOR: u32 = 2_500;
/// A priori des tests : celui de `serie-exemple.json`.
const PRIOR_K: u32 = 20;

#[test]
fn raw_burn_weight_rounding_and_floor() {
    let f = |w, m, b, cap| draw::raw_burn_weight(w, m, b, cap, FLOOR, 0);
    assert_eq!(f(100, 0, 0, None), 100, "aucune émise : poids de base");
    assert_eq!(f(100, 10, 0, None), 100);
    assert_eq!(f(100, 10, 5, None), 50);
    assert_eq!(f(100, 3, 1, None), 66, "arrondi vers le bas");
    assert_eq!(f(100, 10, 8, None), 25, "plancher à 25 % du poids de base");
    assert_eq!(f(100, 10, 10, None), 25, "dernière carte brûlée : plancher, pas 0");
    assert_eq!(f(3, 10, 10, None), 1, "plancher arrondi, au moins 1");
    assert_eq!(f(100, 5, 0, Some(5)), 0, "épuisée par son plafond : 0");
    assert_eq!(f(100, 5, 5, Some(5)), 0, "épuisée même toutes brûlées");
    assert_eq!(f(0, 5, 0, None), 0);
    assert_eq!(draw::raw_burn_weight(100, 10, 10, None, 0, 0), 1, "plancher nul : 1");
    assert_eq!(f(u32::MAX, u32::MAX, 1, None), u32::MAX as u64 - 1);
    // A priori K : brut = ⌊w × (e − b + K) / (e + K)⌋.
    let k = |m, b| draw::raw_burn_weight(100, m, b, None, FLOOR, PRIOR_K);
    assert_eq!(k(0, 0), 100);
    assert_eq!(k(1, 1), 95, "une carte émise une fois et brûlée : 20/21");
    assert_eq!(k(20, 20), 50);
    assert_eq!(k(60, 60), 25, "plancher atteint à e = b = 3K");
    assert_eq!(k(1_000, 1_000), 25, "plancher gardé");
    assert_eq!(draw::raw_burn_weight(u32::MAX, u32::MAX, u32::MAX, None, 0, MAX_BURN_PRIOR_K), 1_000_000 * (u32::MAX as u64) / (u32::MAX as u64 + 1_000_000), "u128, sans débordement");
}

/// La part des brûlables dans leur rareté ne bouge pas, quels que soient les burns : le poids perdu
/// revient aux autres brûlables (vérifié en entiers, par produits croisés, sur 2 000 cas).
#[test]
fn renormalization_keeps_burnable_share_exact() {
    let mut x: u64 = 7;
    let mut rnd = |m: u64| {
        x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (x >> 33) % m
    };
    for _ in 0..2_000 {
        let n = 1 + rnd(12) as usize;
        let cards: Vec<DrawCard> = (0..n)
            .map(|_| DrawCard {
                rarity: Rarity::Common,
                weight: rnd(1_000) as u32,
                cap: if rnd(4) == 0 { Some(rnd(20) as u32) } else { None },
                backed: rnd(2) == 0,
            })
            .collect();
        let minted: Vec<u32> = (0..n).map(|_| rnd(30) as u32).collect();
        let burned: Vec<u32> = minted.iter().map(|m| if *m == 0 { 0 } else { rnd(*m as u64 + 1) as u32 }).collect();
        // Une partie des brûlables sont des ressuscitées (ratio moyen des autres).
        let resurrectable: Vec<u32> = (0..n as u32).filter(|_| rnd(3) == 0).collect();
        let bv = draw::BurnView { burned: &burned, floor_bps: FLOOR, prior_k: (rnd(3) * 10) as u32, resurrectable: &resurrectable };
        let f = draw::burn_factors(&cards, &minted, &bv, Rarity::Common);
        let ws: Vec<u128> =
            (0..n).map(|i| draw::in_rarity_weight(&cards[i], i, minted[i], &bv, f)).collect();
        let base: Vec<u128> = (0..n)
            .map(|i| draw::available_weight_compact(&cards[i..=i], &[], &minted[i..=i], &[], Rarity::Common) as u128)
            .collect();
        let (wb, wt): (u128, u128) =
            (cards.iter().zip(&ws).filter(|(c, _)| c.backed).map(|(_, w)| *w).sum(), ws.iter().sum());
        let (bb, bt): (u128, u128) =
            (cards.iter().zip(&base).filter(|(c, _)| c.backed).map(|(_, w)| *w).sum(), base.iter().sum());
        assert_eq!(wb * bt, bb * wt, "part des brûlables inchangée");
        // Une carte non épuisée garde un poids non nul ; une carte épuisée a 0.
        for i in 0..n {
            assert_eq!(ws[i] == 0, base[i] == 0);
        }
    }
}

fn backed_tokens(c: &Contract, who: &AccountId, card_id: &str) -> Vec<String> {
    c.nft_tokens_for_owner(who.clone(), None, None)
        .into_iter()
        .filter(|t| c.get_card(t.token_id.clone()).unwrap().card_id.as_deref() == Some(card_id))
        .map(|t| t.token_id)
        .collect()
}

fn burn(c: &mut Contract, who: AccountId, tid: &str) -> bool {
    set(who.clone(), 1, 40);
    let b = c.get_backing(tid.to_string()).unwrap();
    let _ = c.redeem(tid.to_string());
    set_result(PromiseResult::Successful(vec![]));
    c.on_redeem_complete(tid.to_string(), who, b)
}

fn burn_mech() -> Mechanics {
    burn_mech_k(PRIOR_K)
}

fn burn_mech_k(prior_k: u32) -> Mechanics {
    Mechanics { gold: None, pity: None, burn: Some(BurnParams { floor_bps: FLOOR, prior_k }), rush: None, resurrection: None, value: None }
}

#[test]
fn burns_shift_weight_between_burnables_of_the_rarity() {
    // Sans a priori (K = 0) : le plancher est atteint dès que toutes les com_a sont brûlées.
    let mut c = contract_with(table(Some(burn_mech_k(0))));
    for k in 0..12u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    let a = backed_tokens(&c, &alice(), "com_a");
    assert!(a.len() > 3);
    for (i, t) in a.iter().enumerate() {
        assert!(burn(&mut c, alice(), t));
        assert_eq!(c.get_series(0).burned[3], i as u32 + 1);
        assert_eq!(c.get_series(0).burn_seq, i as u64 + 1);
    }
    // com_a toutes brûlées : brut 25 (plancher), com_c 100 ; E = 125, B = 200.
    // Poids dans la rareté : com_a 25 × 200, com_b (non brûlable) 100 × 125, com_c 100 × 200.
    let rates = c.get_rates(0, None, None);
    let commons = rates["rarities"][4]["cards"].as_array().unwrap().clone();
    let ew: Vec<&str> = commons.iter().map(|x| x["effective_weight"].as_str().unwrap()).collect();
    assert_eq!(ew, ["5000", "12500", "20000"]);
    assert_eq!(rates["rarities"][4]["effective_card_weight"], "37500");
    // Part des brûlables : 25 000 / 37 500 = 200 / 300, comme sans burn. Taux de rareté inchangé.
    assert_eq!(rates["rarities"][4]["rarity_ppm"], 960_000);
    // Les tirages suivants = tirage de référence avec les compteurs de burn.
    let s = c.series_ref(0).clone();
    let (mut minted, burned) = (s.minted.clone(), c.get_series(0).burned);
    let bv = draw::BurnView { burned: &burned, floor_bps: FLOOR, prior_k: 0, resurrectable: &[] };
    let id = buy_reveal(&mut c, alice(), 99, 300);
    let p = pack(&c, id);
    let acc: [u8; 32] = hex_decode(p["acc"].as_str().unwrap()).unwrap().try_into().unwrap();
    for d in p["draws"].as_array().unwrap() {
        let slot = d["slot"].as_u64().unwrap() as u8;
        let base = draw::draw_slot_compact(&s.table.rarity_weights, &s.draw_cards, &[], &minted, &[], &acc, slot);
        let r = draw::draw_slot_mech(&s.table.rarity_weights, &s.draw_cards, &[], &minted, &[], Some(&bv), &acc, slot);
        assert_eq!(r.rarity_roll, base.rarity_roll, "le tirage de rareté ignore les burns");
        assert_eq!(r.index as u64, d["index"].as_u64().unwrap());
        assert_eq!(r.card_roll.to_string(), d["card_roll"].as_str().unwrap());
        minted[r.index as usize] += 1;
    }
    assert_eq!(c.get_series(0).minted, minted);
}

#[test]
fn burn_counters_only_with_mechanic() {
    let mut c = contract_with(table(None));
    for k in 0..6u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    let t = backed_tokens(&c, &alice(), "com_a")[0].clone();
    assert!(burn(&mut c, alice(), &t));
    assert!(c.get_series(0).burned.is_empty());
    assert_eq!(c.get_burns(0, None, None)["enabled"], false);
}

#[test]
fn exhausted_card_stays_at_zero_after_burns() {
    // Légendaire plafonnée à 1 : une fois sortie et brûlée, elle reste épuisée (poids 0).
    let mut t = table(Some(Mechanics {
        gold: Some(gold()),
        pity: Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(1) }),
        burn: Some(BurnParams { floor_bps: FLOOR, prior_k: PRIOR_K }),
        rush: None,
        resurrection: None,
        value: None,
    }));
    t.cards[0].cap = Some(1);
    let mut c = contract_with(t);
    buy_reveal(&mut c, alice(), 1, 20);
    let r = rarities(&c, 0);
    assert_eq!(r[0], "legendary");
    // Gold pack légendaire ; légendaire épuisée, aucune mythique au-dessus : sous le plancher (épique).
    assert!(r[1..].iter().all(|x| x == "epic"), "retombée : {r:?}");
    let leg = backed_tokens(&c, &alice(), "leg")[0].clone();
    assert!(burn(&mut c, alice(), &leg));
    let rates = c.get_rates(0, None, None);
    assert_eq!(rates["rarities"][1]["cards"][0]["effective_weight"], "0");
    buy_reveal(&mut c, alice(), 2, 40);
    assert!(rarities(&c, 1).iter().all(|x| x == "epic"));
}

// ----------------------------------------------------------------- gold rush

fn rush_weights() -> RarityWeights {
    w(0, 0, 1, 0, 0) // épique seulement : un pack rush se voit tout de suite
}

#[allow(clippy::too_many_arguments)]
fn rush(ratio_bps: u32, min_packs: u32, window: u64, baseline: u64, bucket: u64, duration: u64, cooldown: u64) -> RushParams {
    RushParams {
        ratio_bps,
        min_packs,
        window_blocks: window,
        baseline_blocks: baseline,
        bucket_blocks: bucket,
        duration_blocks: duration,
        cooldown_blocks: cooldown,
        max_per_account: 1_000,
        weights: rush_weights(),
    }
}

#[test]
fn rush_threshold_is_relative_to_traffic() {
    // Seaux de 10 blocs, fenêtre 20 (2 seaux), 24 h simulées par 100 blocs (10 seaux), ×2.
    let p = rush(20_000, 3, 20, 100, 10, 15, 30);
    for per_bucket in [1u64, 4, 16] {
        // Trafic régulier, à n'importe quel niveau : jamais de rush.
        let mut st = RushState::default();
        for h in 0..1_000u64 {
            for _ in 0..per_bucket {
                if h % 10 == 0 {
                    let o = draw::rush_on_buy(&p, &mut st, h);
                    assert!(!o.triggered, "trafic régulier ×{per_bucket} : rush à {h}");
                }
            }
        }
        assert_eq!(st.ring.len(), 10, "coût borné : m_l seaux");
        // Un pic (rythme ≥ 2 × la moyenne sur la fenêtre longue) déclenche.
        let mut fired = None;
        for k in 0..(10 * per_bucket) {
            let o = draw::rush_on_buy(&p, &mut st, 1_005);
            if o.triggered {
                fired = Some(k);
                break;
            }
        }
        assert!(fired.is_some(), "pic ×{per_bucket} sans rush");
    }
}

#[test]
fn rush_warmup_cooldown_and_window_overlap() {
    let p = rush(20_000, 3, 20, 100, 10, 15, 30);
    let mut st = RushState::default();
    // Pas de rush avant que la fenêtre longue soit remplie (premier achat + 100 blocs).
    for _ in 0..10 {
        assert!(!draw::rush_on_buy(&p, &mut st, 50).triggered);
    }
    for h in (60..200).step_by(10) {
        draw::rush_on_buy(&p, &mut st, h);
    }
    // Pic au dernier bloc d'un seau (209) : le rush déborde sur les seaux suivants.
    let mut t = None;
    for _ in 0..20 {
        if draw::rush_on_buy(&p, &mut st, 209).triggered {
            t = Some(209u64);
            break;
        }
    }
    let t = t.expect("pas de rush");
    assert!(!draw::rush_on_buy(&p, &mut st, t).active, "même bloc que le déclenchement : pas rush");
    for h in t + 1..=t + 15 {
        let o = draw::rush_on_buy(&p, &mut st, h);
        assert!(o.active && !o.triggered, "rush à {h}");
    }
    // Pause de 30 blocs après la fin : même un pic énorme ne redéclenche pas.
    for h in t + 16..=t + 45 {
        for _ in 0..5 {
            let o = draw::rush_on_buy(&p, &mut st, h);
            assert!(!o.active && !o.triggered, "pause à {h}");
        }
    }
    assert_eq!(st.rush_count, 1);
    // Après la pause, un nouveau pic redéclenche (les achats du rush comptent dans la moyenne).
    let mut again = false;
    for _ in 0..200 {
        if draw::rush_on_buy(&p, &mut st, t + 90).triggered {
            again = true;
            break;
        }
    }
    assert!(again);
    assert_eq!(st.rush_count, 2);
}

fn small_rush() -> RushParams {
    // Fenêtre 1 seau, longue 5 seaux, ×1,5, 2 packs au moins, rush de 30 blocs, sans pause.
    rush(15_000, 2, 10, 50, 10, 30, 0)
}

#[test]
fn rush_is_frozen_at_purchase_not_at_reveal() {
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(1_000) }), false, Some(small_rush())))));
    buy_reveal(&mut c, alice(), 1, 0); // début de la fenêtre longue
    assert_eq!(c.get_pity(alice(), 0)["n"], 1);
    buy_reveal(&mut c, bob(), 2, 60);
    let b = buy_reveal(&mut c, bob(), 3, 60); // 2 packs dans la fenêtre courte, ×2 la moyenne : déclenche
    assert_eq!(c.get_rush_state(0, Some(60), None)["last_trigger"], 60);
    assert_eq!(pack(&c, b)["rush"], false);
    // Acheté pendant le rush, révélé bien après sa fin : reste un pack rush (table rush).
    let p = buy_at(&mut c, alice(), 70);
    assert_eq!(c.get_rush_state(0, Some(70), None)["active"], true);
    reveal(&mut c, p, 4, 500);
    assert_eq!(pack(&c, p)["rush"], true);
    assert_eq!(pack(&c, p)["mode"], "rush");
    assert!(rarities(&c, p).iter().all(|r| r == "epic"));
    // Un pack rush ne remet plus le compteur de pitié à zéro : il compte comme un pack sans gold pack.
    assert_eq!(c.get_pity(alice(), 0)["n"], 2);
    // Acheté après la fin : pack normal, même révélé tout de suite.
    let q = buy_reveal(&mut c, bob(), 5, 600);
    assert_eq!(pack(&c, q)["rush"], false);
    assert_eq!(pack(&c, q)["mode"], "base");
}

// ----------------------------------------------------------------- résurrection

fn epic_table(m: Option<Mechanics>) -> SeriesTable {
    let mut t = table(m);
    t.rarity_weights = w(0, 1, 600, 30, 369);
    t
}

#[test]
fn resurrection_makes_existing_and_future_cards_burnable() {
    let mut c = contract_with(epic_table(Some(res_mech(&[6]))));
    for k in 0..6u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    let b = backed_tokens(&c, &alice(), "epic_b");
    assert!(!b.is_empty());
    assert!(c.get_backing(b[0].clone()).is_none());
    install_oracle(&mut c, 100);
    set(oracle(), NEAR, 101);
    let backing = Backing { asset_id: "nep141:revived.near".into(), amount: U128(77) };
    c.set_resurrected(0, 6, backing.clone());
    assert_eq!(c.get_backing(b[0].clone()), Some(backing.clone()), "exemplaire existant");
    let meta: Value = serde_json::from_str(&c.nft_token(b[0].clone()).unwrap().metadata.unwrap().extra.unwrap()).unwrap();
    assert_eq!(meta["burnable"], true);
    // La carte rejoint les brûlables de sa rareté (rareté pilotée par les burns), une seule fois.
    assert!(c.series_ref(0).draw_cards[6].backed);
    assert_eq!(c.series_ref(0).resurrect_seq, 1);
    set(oracle(), NEAR, 102);
    c.set_resurrected(0, 6, Backing { asset_id: "nep141:revived.near".into(), amount: U128(78) });
    assert_eq!(c.series_ref(0).resurrect_seq, 1, "remplacement de l'adossement : même ensemble");
    assert!(burn(&mut c, alice(), &b[0]));
    assert_eq!(c.get_series(0).burned[6], 1);
    // Nouvelles cartes : adossement lu à la demande.
    for k in 10..16u8 {
        buy_reveal(&mut c, bob(), k, 200 + 10 * k as u64);
    }
    let nb = backed_tokens(&c, &bob(), "epic_b");
    assert_eq!(c.get_backing(nb[0].clone()).unwrap().amount, U128(78));
}

/// Une carte hors des épiques et légendaires non adossées ne peut pas figurer dans la liste
/// ressuscitable : la table est refusée.
fn resurrect(index: u32) {
    contract_with(table(Some(res_mech(&[index]))));
}

#[test]
#[should_panic(expected = "Réservé à l'oracle de prix")]
fn resurrection_is_oracle_only() {
    let mut c = contract_with(table(Some(res_mech(&[6]))));
    install_oracle(&mut c, 100);
    set(owner(), NEAR, 101);
    c.set_resurrected(0, 6, Backing { asset_id: "x".into(), amount: U128(1) });
}

#[test]
#[should_panic(expected = "déjà adossée par la table")]
fn resurrection_refuses_table_backed_card() {
    resurrect(1); // épique adossée
}

#[test]
#[should_panic(expected = "épiques et légendaires")]
fn resurrection_refuses_common() {
    resurrect(4);
}

#[test]
#[should_panic(expected = "épiques et légendaires")]
fn resurrection_refuses_rare() {
    resurrect(2);
}

// ----------------------------------------------------------------- validation

fn rejects(m: Mechanics, msg: &str) {
    let r = std::panic::catch_unwind(|| contract_with(table(Some(m))));
    let e = r.err().expect("table acceptée");
    let s = e.downcast_ref::<String>().cloned().unwrap_or_default();
    assert!(s.contains(msg), "{s} ne contient pas {msg}");
}

#[test]
fn invalid_mechanics_are_rejected() {
    let pity = |n| Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(n) });
    let none = Mechanics { gold: None, pity: None, burn: None, rush: None, resurrection: None, value: None };
    rejects(Mechanics { pity: pity(3), ..none.clone() }, "pity exige gold");
    rejects(mech(pity(0), false, None), "n_max");
    rejects(mech(pity(10_001), false, None), "n_max");
    rejects(mech(Some(PityParams { p0_ppb: 2_000_000_000, k_ppb: 0, p_max_ppb: 2_000_000_000, n_max: None }), false, None), "ppb");
    rejects(mech(Some(PityParams { p0_ppb: 0, k_ppb: 2_000_000_000, p_max_ppb: 10, n_max: None }), false, None), "ppb");
    rejects(mech(Some(PityParams { p0_ppb: 50_000, k_ppb: 20, p_max_ppb: 40_000, n_max: None }), false, None), "p0_ppb ≤ p_max_ppb");
    rejects(mech(Some(PityParams { p0_ppb: 0, k_ppb: 20, p_max_ppb: 0, n_max: None }), false, None), "inatteignable");
    rejects(mech(None, false, Some(rush(15_000, 2, 25, 100, 10, 5, 0))), "multiples");
    rejects(mech(None, false, Some(rush(15_000, 2, 10, 1_000, 10, 5, 0))), "96 seaux");
    rejects(mech(None, false, Some(rush(9_999, 2, 10, 100, 10, 5, 0))), "ratio_bps ≥ 10 000");
    rejects(mech(None, false, Some(rush(60_000, 2, 10, 50, 10, 5, 0))), "inatteignable");
    rejects(mech(None, false, Some(rush(15_000, 0, 10, 100, 10, 5, 0))), "min_packs");
    rejects(mech(None, false, Some(RushParams { max_per_account: 0, ..rush(15_000, 2, 10, 100, 10, 5, 0) })), "max_per_account");
    rejects(mech(None, false, Some(rush(15_000, 2, 10, 100, 10, 0, 0))), "durée");
    rejects(mech(None, false, Some(rush(15_000, 2, 100, 100, 10, 5, 0))), "plus courte");
    rejects(Mechanics { gold: Some(gold_w(w(1, 0, 0, 0, 0), Rarity::Mythic, 1)), ..none.clone() }, "engagement");
    rejects(Mechanics { burn: Some(BurnParams { floor_bps: 10_001, prior_k: 0 }), ..none.clone() }, "floor_bps");
    // Table or qui donne du poids à une rareté sans carte : refusée à l'ouverture.
    let mut t = table(Some(Mechanics { gold: Some(gold()), ..none.clone() }));
    t.rarity_weights = w(0, 0, 9, 30, 960);
    t.cards.remove(0);
    let r = std::panic::catch_unwind(|| contract_with(t));
    assert!(r.is_err());
}

#[test]
fn table_without_mechanics_keeps_bytes_and_events() {
    let mut c = contract_with(table(None));
    let json = serde_json::to_string(&c.get_series_table(0)).unwrap();
    assert!(!json.contains("mechanics"));
    buy_reveal(&mut c, alice(), 1, 20);
    assert_eq!(pack(&c, 0)["mode"], "base");
}

// ----------------------------------------------------------------- stockage par carte

#[test]
fn enumeration_stays_consistent_through_transfers_and_burns() {
    let mut c = contract_with(table(None));
    for k in 0..15u8 {
        buy_reveal(&mut c, if k % 3 == 0 { bob() } else { alice() }, k, 20 + 10 * k as u64);
    }
    assert_eq!(c.nft_total_supply().0, 75);
    // Transferts (dans les deux sens) et burns au milieu des listes.
    let alice_tokens: Vec<String> = c.nft_tokens_for_owner(alice(), None, None).into_iter().map(|t| t.token_id).collect();
    for t in alice_tokens.iter().step_by(4) {
        set(alice(), 1, 400);
        c.nft_transfer(bob(), t.clone(), None, None);
    }
    let back = alice_tokens[0].clone();
    set(bob(), 1, 401);
    c.nft_transfer(alice(), back.clone(), None, None);
    let mut burned = 0;
    for t in backed_tokens(&c, &alice(), "com_a").iter().take(5) {
        assert!(burn(&mut c, alice(), t));
        burned += 1;
    }
    let all: Vec<String> = c.nft_tokens(None, None).into_iter().map(|t| t.token_id).collect();
    let set_all: BTreeSet<_> = all.iter().cloned().collect();
    assert_eq!(all.len(), set_all.len(), "aucun doublon");
    assert_eq!(all.len() as u128, c.nft_total_supply().0);
    assert_eq!(all.len(), 75 - burned);
    // Pages (from_index, limit) = liste complète.
    let mut paged = vec![];
    let mut from = 0u128;
    while from < c.nft_total_supply().0 {
        let p = c.nft_tokens(Some(U128(from)), Some(7));
        from += p.len() as u128;
        paged.extend(p.into_iter().map(|t| t.token_id));
    }
    assert_eq!(paged, all);
    // Listes par propriétaire = propriétaires réels.
    let mut n = 0;
    for who in [alice(), bob()] {
        let mine = c.nft_tokens_for_owner(who.clone(), None, None);
        assert_eq!(mine.len() as u128, c.nft_supply_for_owner(who.clone()).0);
        for t in &mine {
            assert_eq!(t.owner_id, who);
            assert_eq!(c.nft_token(t.token_id.clone()).unwrap().owner_id, who);
        }
        n += mine.len();
    }
    assert_eq!(n, all.len());
    // Retour chez l'acheteur du pack : propriétaire compact (None).
    let tid = parse_token_id(&back).unwrap();
    assert_eq!(c.packs.get(&(tid / 10)).unwrap().cards[(tid % 10) as usize].owner, None);
    // Métadonnées reconstruites : identiques à la table.
    let tok = c.nft_token(back.clone()).unwrap();
    let card = c.get_card(back).unwrap();
    let def = &table(None).cards[card.index as usize];
    let meta = tok.metadata.unwrap();
    assert_eq!(meta.title.as_deref(), Some(def.title.as_str()));
    assert_eq!(meta.media, def.media);
    assert!(meta.issued_at.is_some());
}

#[test]
fn token_ids_are_canonical() {
    let mut c = contract_with(table(None));
    buy_reveal(&mut c, alice(), 1, 20);
    buy_reveal(&mut c, alice(), 2, 40);
    assert_eq!(pack(&c, 1)["token_ids"], serde_json::json!(["10", "11", "12", "13", "14"]));
    assert!(c.nft_token("010".into()).is_none(), "forme non canonique refusée");
    assert!(c.nft_token("15".into()).is_none());
    assert!(c.nft_token("10".into()).is_some());
}

// ----------------------------------------------------------------- revue de sécurité

/// Revue, point 1 : burns en début de série. 10 épiques brûlables de même poids ; un joueur brûle
/// les 9 bon marché, chacune émise une fois (e = 1, b = 1). Sans lissage, elles tombaient toutes au
/// plancher et la 10ᵉ passait de 10 % à 30,8 % des épiques brûlables. Avec l'a priori K, une
/// carte émise une fois et brûlée garde presque tout son poids.
#[test]
fn early_burns_are_smoothed_by_prior() {
    let mut t = table(Some(burn_mech()));
    t.rarity_weights = w(0, 0, 100, 0, 900);
    t.cards = (0..10).map(|i| card(&format!("e{i}"), Rarity::Epic, 100, None, true)).collect();
    t.cards.push(card("com", Rarity::Common, 1, None, false));
    let mut c = contract_with(t);
    for i in 0..9 {
        c.series.get_mut(0).unwrap().minted[i] = 1;
        c.series_burns.get_mut(&0).unwrap().burned[i] = 1;
    }
    let rates = c.get_rates(0, None, None);
    let epics = rates["rarities"][2]["cards"].as_array().unwrap();
    let ew: Vec<u128> = epics.iter().map(|x| x["effective_weight"].as_str().unwrap().parse().unwrap()).collect();
    let total: u128 = ew.iter().sum();
    let share_ppm = ew[9] * 1_000_000 / total;
    assert!(share_ppm < 110_000, "part de la 10ᵉ épique : {share_ppm} ppm (10 % sans burn)");
    assert!(share_ppm > 100_000, "elle gagne quand même un peu : {share_ppm} ppm");
}

/// Mécaniques d'une série où les épiques mortes `dead` (index de table) sont ressuscitables.
fn res_mech(dead: &[u32]) -> Mechanics {
    Mechanics { resurrection: Some(ResurrectionParams { eligible: dead.to_vec() }), ..burn_mech() }
}

/// Oracle de prix installé en deux temps : proposition, puis acceptation après le délai.
fn install_oracle(c: &mut Contract, at: u64) {
    set(owner(), 0, at);
    c.propose_price_oracle(Some(oracle()));
    set(owner(), 0, at + DEFAULT_ORACLE_DELAY_BLOCKS);
    c.accept_price_oracle();
}

/// Revue, point 3 : une carte ressuscitée entre dans le calcul des burns avec le ratio moyen des
/// brûlables de sa rareté, pas avec un poids plein. Quatre épiques adossées entièrement brûlées
/// (au plancher), une épique morte émise 100 fois puis ressuscitée : sa part parmi les brûlables
/// doit rester sa part de base (20 %), pas 50 %.
#[test]
fn resurrected_card_enters_with_mean_ratio() {
    let mut t = table(Some(res_mech(&[4])));
    t.rarity_weights = w(0, 0, 100, 0, 900);
    t.cards = (0..4).map(|i| card(&format!("e{i}"), Rarity::Epic, 100, None, true)).collect();
    t.cards.push(card("dead", Rarity::Epic, 100, None, false));
    t.cards.push(card("com", Rarity::Common, 1, None, false));
    let mut c = contract_with(t);
    for i in 0..5 {
        c.series.get_mut(0).unwrap().minted[i] = 100;
        if i < 4 {
            c.series_burns.get_mut(&0).unwrap().burned[i] = 100;
        }
    }
    install_oracle(&mut c, 50);
    set(oracle(), NEAR, 101);
    c.set_resurrected(0, 4, Backing { asset_id: "nep141:dead.near".into(), amount: U128(1) });
    let rates = c.get_rates(0, None, None);
    let ew: Vec<u128> = rates["rarities"][2]["cards"].as_array().unwrap().iter().map(|x| x["effective_weight"].as_str().unwrap().parse().unwrap()).collect();
    let share_ppm = ew[4] * 1_000_000 / ew.iter().sum::<u128>();
    assert!(share_ppm <= 200_000, "part de la ressuscitée parmi les brûlables : {share_ppm} ppm (base 20 %)");
}

/// Revue, point 3 : l'oracle ne ressuscite que les cartes engagées dans la table hachée.
#[test]
#[should_panic(expected = "non ressuscitable")]
fn resurrection_limited_to_hashed_list() {
    let mut c = contract_with(epic_table(Some(res_mech(&[]))));
    install_oracle(&mut c, 50);
    set(oracle(), NEAR, 101);
    c.set_resurrected(0, 6, Backing { asset_id: "x".into(), amount: U128(1) });
}

/// Revue, point 3 : le changement d'oracle se fait en deux temps, avec un délai et un événement
/// à chaque étape ; le retrait est immédiat.
#[test]
fn oracle_change_is_two_step_with_delay() {
    let mut c = contract_with(epic_table(Some(res_mech(&[6]))));
    set(owner(), 0, 100);
    c.propose_price_oracle(Some(oracle()));
    let logs = near_sdk::test_utils::get_logs();
    assert!(logs.iter().any(|l| l.contains("price_oracle_proposed") && l.contains("\"effective_from\":144100")), "{logs:?}");
    assert_eq!(c.get_config()["price_oracle_id"], Value::Null, "pas encore actif");
    // Avant le délai : refus ; l'oracle proposé ne peut rien faire.
    set(owner(), 0, 100 + DEFAULT_ORACLE_DELAY_BLOCKS - 1);
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.accept_price_oracle()));
    assert!(r.is_err());
    set(oracle(), NEAR, 200);
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        c.set_resurrected(0, 6, Backing { asset_id: "x".into(), amount: U128(1) })
    }));
    assert!(r.is_err(), "oracle proposé mais pas accepté");
    // Seul l'owner propose et accepte.
    set(alice(), 0, 300);
    assert!(std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.propose_price_oracle(Some(alice())))).is_err());
    set(owner(), 0, 100 + DEFAULT_ORACLE_DELAY_BLOCKS);
    c.accept_price_oracle();
    assert!(near_sdk::test_utils::get_logs().iter().any(|l| l.contains("price_oracle_accepted")));
    assert_eq!(c.get_config()["price_oracle_id"], oracle().to_string());
    assert_eq!(c.get_config()["price_oracle_pending"], Value::Null);
    // Retrait immédiat.
    set(owner(), 0, 200_000);
    c.revoke_price_oracle();
    assert!(near_sdk::test_utils::get_logs().iter().any(|l| l.contains("price_oracle_revoked")));
    assert_eq!(c.get_config()["price_oracle_id"], Value::Null);
}

/// Paramètres du rush de `small_rush`, avec un plafond de packs rush par compte et par rush.
fn capped_rush(cap: u32) -> RushParams {
    RushParams { max_per_account: cap, ..small_rush() }
}

/// Revue, point 2 : après un creux, un seul acteur déclenche le rush puis achète au taux rush. Au-delà
/// du plafond par compte (3), ses packs sont normaux, figés à l'achat et journalisés.
#[test]
fn rush_packs_are_capped_per_account() {
    let mut c = contract_with(table(Some(mech(None, false, Some(capped_rush(3))))));
    buy_reveal(&mut c, alice(), 1, 0);
    buy_at(&mut c, bob(), 60);
    buy_at(&mut c, bob(), 60); // déclenche
    assert_eq!(c.get_rush_state(0, Some(60), None)["last_trigger"], 60);
    let mut rush = vec![];
    for k in 0..5u64 {
        let p = buy_at(&mut c, bob(), 61 + k);
        let logs = near_sdk::test_utils::get_logs();
        rush.push(pack(&c, p)["rush"].as_bool().unwrap());
        if k == 4 {
            assert!(logs.iter().any(|l| l.contains("\"capped\":true") && l.contains("\"account_rush_packs\":3")), "{logs:?}");
        }
    }
    assert_eq!(rush, [true, true, true, false, false], "3 packs rush par compte et par rush");
    let st = c.get_rush_state(0, Some(66), Some(bob()));
    assert_eq!(st["account"]["rush_packs"], 3);
    assert_eq!(st["account"]["remaining"], 0);
    // Un autre compte a son propre plafond.
    let p = buy_at(&mut c, alice(), 70);
    assert_eq!(pack(&c, p)["rush"], true);
}

/// Fin du burn telle que le contrat la programme (adossement figé au lancement du burn).
fn complete_redeem(c: &mut Contract, tid: &str, who: AccountId, delivered: &Backing) -> bool {
    set_result(PromiseResult::Successful(vec![]));
    c.on_redeem_complete(tid.to_string(), who, delivered.clone())
}

/// Revue, point 4 : l'oracle remplace l'adossement d'une carte ressuscitée pendant un burn. Le
/// redeemer a livré l'adossement lu au lancement : c'est lui que `card_redeemed` journalise.
#[test]
fn redeem_logs_the_backing_actually_delivered() {
    let mut c = contract_with(epic_table(Some(res_mech(&[6]))));
    for k in 0..6u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    install_oracle(&mut c, 100);
    let a = Backing { asset_id: "nep141:a.near".into(), amount: U128(11) };
    set(oracle(), NEAR, 101);
    c.set_resurrected(0, 6, a.clone());
    let tid = backed_tokens(&c, &alice(), "epic_b")[0].clone();
    set(alice(), 1, 102);
    let _ = c.redeem(tid.clone());
    // Pendant le burn, l'oracle change l'adossement.
    set(oracle(), NEAR, 103);
    c.set_resurrected(0, 6, Backing { asset_id: "nep141:b.near".into(), amount: U128(99) });
    assert!(complete_redeem(&mut c, &tid, alice(), &a));
    let logs = near_sdk::test_utils::get_logs();
    let ev = logs.iter().find(|l| l.contains("card_redeemed")).expect("card_redeemed");
    assert!(ev.contains("\"asset_id\":\"nep141:a.near\"") && ev.contains("\"amount\":\"11\""), "{ev}");
    assert!(ev.contains("\"replaced_by\":{\"asset_id\":\"nep141:b.near\""), "remplacement journalisé : {ev}");
}

// ----------------------------------------------------------------- valeur du pack et gold pack

const MULT: RarityWeights = RarityWeights { mythic: 0, legendary: 20, epic: 5, rare: 2, common: 1 };

fn none_mech() -> Mechanics {
    Mechanics { gold: None, pity: None, burn: None, rush: None, resurrection: None, value: None }
}

fn value_p(normal: Vec<ValueTier>) -> ValueParams {
    ValueParams { normal, gold: vec![(30_000, 1)], rush: vec![(9_000, 1)], multipliers: MULT }
}

fn value_mech(normal: Vec<ValueTier>) -> Mechanics {
    Mechanics { value: Some(value_p(normal)), ..none_mech() }
}

/// Gold pack de la décision du 11/11 : 1-2 rare ou mieux (le 2 parmi les brûlables), 3-4 épique ou
/// mieux, 5 légendaire 99 % ou mythique 1 %.
fn gold_v2() -> GoldParams {
    let s = |floor, burnable| GoldSlot { floor, weights: None, burnable };
    GoldParams {
        slots: vec![
            s(Rarity::Rare, false),
            s(Rarity::Rare, true),
            s(Rarity::Epic, false),
            s(Rarity::Epic, false),
            GoldSlot { floor: Rarity::Legendary, weights: Some(w(1, 99, 0, 0, 0)), burnable: false },
        ],
    }
}

fn mythic_commit(i: u8, cap: u32) -> MythicCommitment {
    MythicCommitment { commitment: hex_encode(&[i; 32]), content_hash: hex_encode(&[i + 100; 32]), weight: 1, cap }
}

/// Table de `table()` avec une mythique (plafond `cap`) et le gold pack v2 à chaque pack (N = 1).
fn gold_table(myth_cap: u32, value: bool) -> SeriesTable {
    let mut t = table(Some(Mechanics {
        gold: Some(gold_v2()),
        pity: Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(1) }),
        value: value.then(|| value_p(vec![(7_500, 1)])),
        ..none_mech()
    }));
    t.mythics = vec![mythic_commit(1, myth_cap)];
    t
}

/// `pack_revealed` du dernier tirage (journal du dernier reçu).
fn last_revealed() -> Value {
    let logs = near_sdk::test_utils::get_logs();
    let l = logs.iter().find(|l| l.contains("\"pack_revealed\"")).expect("pack_revealed");
    serde_json::from_str::<Value>(l.strip_prefix("EVENT_JSON:").unwrap()).unwrap()["data"][0].clone()
}

fn draws(c: &Contract, id: u64) -> Vec<Value> {
    pack(c, id)["draws"].as_array().unwrap().clone()
}

fn backed_at(c: &Contract, d: &Value) -> bool {
    d["kind"] == "visible" && c.series_ref(0).draw_cards[d["index"].as_u64().unwrap() as usize].backed
}

/// Un seul palier : V fixe. Prix non multiple de 10⁴ : arrondi des yocto. Le total est réparti
/// exactement entre les brûlables du pack, et le dernier emplacement en est toujours une.
#[test]
fn single_tier_value_is_split_exactly_among_burnables() {
    let mut t = table(Some(value_mech(vec![(7_777, 3)])));
    t.price = U128(NEAR / 10 + 7);
    let mut c = contract_with(t);
    let total = (NEAR / 10 + 7) * 7_777 / 10_000;
    assert_eq!(draw::value_total(NEAR / 10 + 7, 7_777), total);
    let mut several = 0;
    for k in 0..30u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let ev = last_revealed();
        let v = &ev["mechanics"]["value"];
        assert_eq!((v["tier"].as_u64(), v["bps"].as_u64()), (Some(0), Some(7_777)));
        assert_eq!(v["total"], total.to_string());
        let ds = draws(&c, id);
        assert!(backed_at(&c, ds.last().unwrap()), "dernier emplacement brûlable : {ds:?}");
        let amounts: Vec<Option<u128>> =
            v["amounts"].as_array().unwrap().iter().map(|a| a.as_str().map(|s| s.parse().unwrap())).collect();
        for (d, a) in ds.iter().zip(&amounts) {
            assert_eq!(a.is_some(), backed_at(&c, d), "part seulement pour les brûlables");
        }
        assert_eq!(amounts.iter().flatten().sum::<u128>(), total, "aucun yocto perdu");
        several += (amounts.iter().flatten().count() > 1) as u32;
        // La vue redonne les mêmes montants (recalculés depuis bps et le masque).
        assert_eq!(pack(&c, id)["value"]["amounts"], v["amounts"]);
        assert_eq!(c.packs.get(&id).unwrap().value.unwrap().bps, 7_777);
    }
    assert!(several > 0, "jamais plus d'une brûlable dans un pack");
}

#[test]
fn yocto_rounding_gives_remainder_to_highest_multiplier() {
    let slots = [
        (Rarity::Common, true),
        (Rarity::Epic, true),
        (Rarity::Rare, false),
        (Rarity::Epic, true),
        (Rarity::Mythic, false),
        (Rarity::Common, true),
    ];
    let total = 1_000_000_000_000_000_000_000_007u128;
    let a = draw::split_value(total, &slots, &MULT);
    // Σm = 1 + 5 + 5 + 1 = 12.
    let unit = total / 12;
    assert_eq!(a[0], Some(unit));
    assert_eq!(a[2], None);
    assert_eq!(a[4], None);
    assert_eq!(a[3], Some(total * 5 / 12));
    assert_eq!(a[1], Some(total * 5 / 12 + (total - 2 * unit - 2 * (total * 5 / 12))), "reste au premier plus fort multiplicateur");
    assert_eq!(a.iter().flatten().sum::<u128>(), total);
    // 1 yocto à partager entre deux cartes : tout au plus fort multiplicateur.
    assert_eq!(draw::split_value(1, &[(Rarity::Common, true), (Rarity::Legendary, true)], &MULT), vec![Some(0), Some(1)]);
    // Aucune brûlable : rien n'est réparti.
    assert_eq!(draw::split_value(9, &[(Rarity::Common, false)], &MULT), vec![None]);
    // Pas de dépassement sur un prix extrême.
    assert_eq!(draw::value_total(u128::MAX, 10_000), u128::MAX - u128::MAX % 10_000 + (u128::MAX % 10_000));
    assert_eq!(draw::value_total(u128::MAX, 5_000), u128::MAX / 2);
}

/// Pack sans brûlable tirée naturellement : seules des communes de collection sortent ; le dernier
/// emplacement vise une commune, n'en trouve aucune brûlable et remonte à la rare brûlable.
#[test]
fn last_slot_climbs_to_a_burnable_when_none_is_drawn_naturally() {
    let mut t = table(Some(value_mech(vec![(5_000, 1)])));
    t.rarity_weights = w(0, 0, 0, 1, 999_999);
    t.cards = vec![
        card("rare_b", Rarity::Rare, 1, None, true),
        card("com_x", Rarity::Common, 1, None, false),
        card("com_y", Rarity::Common, 1, None, false),
    ];
    let mut c = contract_with(t);
    for k in 0..10u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let ds = draws(&c, id);
        for d in &ds[..4] {
            assert_eq!(d["final_rarity"], "common");
            assert!(!backed_at(&c, d));
        }
        let last = &ds[4];
        assert_eq!((last["rolled_rarity"].as_str(), last["final_rarity"].as_str(), last["index"].as_u64()), (Some("common"), Some("rare"), Some(0)));
        let v = &pack(&c, id)["value"];
        assert_eq!(v["amounts"], serde_json::json!([null, null, null, null, (NEAR / 20).to_string()]));
    }
}

/// Retombée de la brûlable garantie : d'abord vers le bas (épique visée, commune brûlable), jamais
/// vers une légendaire brûlable tant qu'une brûlable existe plus bas.
#[test]
fn burnable_slot_falls_down_before_climbing() {
    let mut t = table(Some(value_mech(vec![(5_000, 1)])));
    t.rarity_weights = w(0, 1, 999_998, 0, 1);
    t.cards = vec![
        card("leg_b", Rarity::Legendary, 1, None, true),
        card("epic_x", Rarity::Epic, 1, None, false),
        card("com_b", Rarity::Common, 1, None, true),
        card("com_x", Rarity::Common, 1, None, false),
    ];
    let mut c = contract_with(t);
    for k in 0..10u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let last = &draws(&c, id)[4];
        assert_eq!(last["rolled_rarity"], "epic");
        assert_eq!((last["final_rarity"].as_str(), last["index"].as_u64()), (Some("common"), Some(2)));
    }
}

#[test]
fn fallback_order_rules() {
    use Rarity::*;
    assert_eq!(draw::fallback_order(Epic, Common), vec![Epic, Rare, Common, Legendary, Mythic]);
    assert_eq!(draw::fallback_order(Legendary, Legendary), vec![Legendary, Mythic, Epic, Rare, Common]);
    assert_eq!(draw::fallback_order(Mythic, Legendary), vec![Mythic, Legendary, Epic, Rare, Common]);
    assert_eq!(draw::fallback_order(Epic, Rare), vec![Epic, Rare, Legendary, Mythic, Common]);
    // Visée sous le plancher (impossible avec des poids validés) : traitée comme le plancher.
    assert_eq!(draw::fallback_order(Common, Epic), vec![Epic, Legendary, Mythic, Rare, Common]);
}

/// Gold pack : 5 cartes, aucune commune, planchers par emplacement, 99 / 1 au dernier, le 2 parmi
/// les brûlables ; table de valeur gold.
#[test]
fn gold_pack_has_slot_floors_and_no_common() {
    let mut t = gold_table(100, true);
    t.mechanics.as_mut().unwrap().value.as_mut().unwrap().gold = vec![(30_000, 1)];
    let mut c = contract_with(t);
    let (mut myth, mut leg) = (0, 0);
    for k in 0..80u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        assert_eq!(pack(&c, id)["mode"], "gold");
        let ds = draws(&c, id);
        assert_eq!(ds.len(), 5);
        let rank = |d: &Value| ["mythic", "legendary", "epic", "rare", "common"].iter().position(|r| d["final_rarity"] == *r).unwrap();
        assert!(ds.iter().all(|d| d["final_rarity"] != "common"), "aucune commune : {ds:?}");
        assert!(rank(&ds[0]) <= 3 && rank(&ds[1]) <= 3);
        assert!(rank(&ds[2]) <= 2 && rank(&ds[3]) <= 2);
        assert!(rank(&ds[4]) <= 1);
        assert!(backed_at(&c, &ds[1]), "emplacement 2 parmi les brûlables");
        match ds[4]["final_rarity"].as_str() {
            Some("mythic") => myth += 1,
            _ => leg += 1,
        }
        assert_eq!(pack(&c, id)["value"]["bps"], 30_000, "table de valeur gold");
    }
    assert!(myth <= 5, "mythique au dernier emplacement : {myth} sur 80 (1 % attendu)");
    assert!(leg > myth);
    // Fréquence du 1 % sur 20 000 tirages du 5e emplacement (même fonction que le dernier reçu).
    let t = gold_table(1_000_000, true);
    let g = t.mechanics.as_ref().unwrap().gold.clone().unwrap();
    let cards: Vec<DrawCard> = t.cards.iter().map(DrawCard::from).collect();
    let minted = vec![0u32; cards.len()];
    let mm = vec![0u32; t.mythics.len()];
    let mut hits = 0;
    for i in 0..20_000u32 {
        if i % 500 == 0 {
            set(owner(), 0, 10); // gaz du contexte simulé renouvelé (les sha256 en consomment)
        }
        let acc = env::sha256_array(&i.to_le_bytes());
        let gs = &g.slots[4];
        let wts = draw::gold_slot_weights(&t.rarity_weights, gs);
        let d = draw::draw_slot_rule(&wts, gs.floor, gs.burnable, &cards, &t.mythics, &minted, &mm, None, &acc, 4);
        hits += (d.final_rarity == Rarity::Mythic) as u32;
    }
    assert!((140..=270).contains(&hits), "{hits} mythiques sur 20 000 (200 attendues)");
}

/// Gold pack, légendaires épuisées : le 5 visé légendaire monte à la mythique ; mythique épuisée à
/// son tour, il descend sous le plancher (épique). Les emplacements rare+ ne montent pas sans raison.
#[test]
fn gold_pack_with_exhausted_legendaries() {
    let mut t = gold_table(1, false);
    t.cards[0].cap = Some(0); // la seule légendaire, épuisée d'emblée
    let mut c = contract_with(t);
    let id = buy_reveal(&mut c, alice(), 1, 20);
    let ds = draws(&c, id);
    assert!(ds.iter().all(|d| d["final_rarity"] != "legendary"));
    assert_eq!(ds[4]["final_rarity"], "mythic", "légendaire épuisée : vers le haut");
    for k in 2..12u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let ds = draws(&c, id);
        assert_eq!(ds[4]["final_rarity"], "epic", "légendaire et mythique épuisées : sous le plancher, {ds:?}");
        assert!(ds[2..4].iter().all(|d| d["final_rarity"] == "epic"));
    }
}

/// Mythique au plafond : l'emplacement qui la vise retombe sur la légendaire (vers le bas d'abord).
#[test]
fn mythic_at_cap_falls_down_to_legendary() {
    let mut t = gold_table(1, false);
    t.mechanics.as_mut().unwrap().gold.as_mut().unwrap().slots[4].weights = Some(w(1, 0, 0, 0, 0));
    let mut c = contract_with(t);
    let id = buy_reveal(&mut c, alice(), 1, 20);
    let first = draws(&c, id);
    assert_eq!(first[4]["final_rarity"], "mythic");
    for k in 2..6u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let ds = draws(&c, id);
        assert_eq!((ds[4]["rolled_rarity"].as_str(), ds[4]["final_rarity"].as_str()), (Some("mythic"), Some("legendary")));
    }
}

/// La table de valeur suit la table de taux du pack : normale, gold (pitié), rush (figé à l'achat).
#[test]
fn value_table_follows_pack_mode() {
    // N = 2 : le deuxième pack d'alice est un gold pack ; carol achète pendant le rush.
    let mut m = mech(Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(2) }), false, Some(small_rush()));
    m.value = Some(ValueParams { normal: vec![(5_000, 1)], gold: vec![(30_000, 1)], rush: vec![(9_000, 1)], multipliers: MULT });
    let mut c = contract_with(table(Some(m)));
    let mut seen = vec![];
    for (k, h) in [(1u8, 0u64), (2, 60), (3, 60), (4, 70)] {
        let who = [alice(), bob(), alice(), accounts(3)][k as usize - 1].clone();
        let id = buy_reveal(&mut c, who, k, h);
        seen.push((pack(&c, id)["mode"].as_str().unwrap().to_string(), pack(&c, id)["value"]["bps"].as_u64().unwrap()));
    }
    let want = |m: &str| match m {
        "base" => 5_000,
        "gold" => 30_000,
        _ => 9_000,
    };
    assert!(seen.iter().all(|(m, b)| *b == want(m)), "{seen:?}");
    assert!(seen.iter().any(|(m, _)| m == "rush"), "{seen:?}");
    assert!(seen.iter().any(|(m, _)| m == "gold"), "{seen:?}");
}

/// `redeem` transmet au redeemer la part de la valeur tirée (pas le montant de la table).
#[test]
fn redeem_sends_the_drawn_value() {
    let mut c = contract_with(table(Some(value_mech(vec![(2_000, 1), (20_000, 1)]))));
    let id = buy_reveal(&mut c, alice(), 3, 20);
    let v = pack(&c, id)["value"].clone();
    let slot = v["amounts"].as_array().unwrap().iter().rposition(|a| !a.is_null()).unwrap();
    let tid = token_id_of(id, slot as u8);
    let amount: u128 = v["amounts"][slot].as_str().unwrap().parse().unwrap();
    let b = c.get_backing(tid.clone()).unwrap();
    assert_eq!(b.amount, U128(amount));
    assert_ne!(b.amount, U128(1_000), "pas le montant de la table");
    assert_eq!(c.get_card(tid.clone()).unwrap().backing, Some(b.clone()));
    set(alice(), 1, 40);
    let _ = c.redeem(tid.clone());
    let logs = near_sdk::test_utils::get_logs();
    assert!(logs.iter().any(|l| l.contains("redeem_started") && l.contains(&format!("\"amount\":\"{amount}\""))), "{logs:?}");
    set_result(PromiseResult::Successful(vec![]));
    assert!(c.on_redeem_complete(tid, alice(), b));
    let logs = near_sdk::test_utils::get_logs();
    let ev = logs.iter().find(|l| l.contains("card_redeemed")).unwrap();
    assert!(ev.contains(&format!("\"amount\":\"{amount}\"")) && ev.contains("\"replaced_by\":null"), "{ev}");
}

/// Cas spécial documenté : un exemplaire devenu brûlable après son tirage (résurrection) n'a pas
/// de part de valeur ; il garde le montant de l'oracle. Les exemplaires tirés ensuite en ont une.
#[test]
fn card_resurrected_after_draw_keeps_oracle_amount() {
    let mut m = res_mech(&[6]);
    m.value = Some(value_p(vec![(10_000, 1)]));
    let mut t = epic_table(Some(m));
    t.mechanics.as_mut().unwrap().burn = None;
    let mut c = contract_with(t);
    for k in 0..6u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    let old = backed_tokens(&c, &alice(), "epic_b")[0].clone();
    install_oracle(&mut c, 100);
    set(oracle(), NEAR, 101);
    c.set_resurrected(0, 6, Backing { asset_id: "nep141:revived.near".into(), amount: U128(77) });
    assert_eq!(c.get_backing(old).unwrap().amount, U128(77));
    let mut seen = false;
    for k in 10..30u8 {
        let id = buy_reveal(&mut c, bob(), k, 200 + 10 * k as u64);
        let ev = last_revealed();
        assert_eq!(ev["mechanics"]["resurrect_seq"], 1, "résurrections journalisées");
        for (slot, d) in draws(&c, id).iter().enumerate() {
            if d["kind"] == "visible" && d["index"] == 6 {
                let b = c.get_backing(token_id_of(id, slot as u8)).unwrap();
                assert_eq!(b.asset_id, "nep141:revived.near");
                assert_eq!(Some(b.amount.0), c.slot_value(c.packs.get(&id).unwrap(), slot), "part de la valeur");
                seen = true;
            }
        }
    }
    assert!(seen, "epic_b jamais retirée après la résurrection");
}

#[test]
fn invalid_value_tables_are_rejected() {
    let v = |f: &dyn Fn(&mut ValueParams)| {
        let mut p = value_p(vec![(7_500, 1)]);
        f(&mut p);
        Mechanics { value: Some(p), ..none_mech() }
    };
    rejects(v(&|p| p.normal = vec![(1_999, 1)]), "value.normal");
    rejects(v(&|p| p.normal = vec![(20_001, 1)]), "value.normal");
    rejects(v(&|p| p.normal = vec![(7_500, 0)]), "poids nuls");
    rejects(v(&|p| p.normal = vec![]), "paliers");
    rejects(v(&|p| p.normal = vec![(7_500, 1); 33]), "paliers");
    rejects(v(&|p| p.gold = vec![(0, 1)]), "value.gold");
    rejects(v(&|p| p.rush = vec![(1_000_001, 1)]), "value.rush");
    rejects(v(&|p| p.multipliers.mythic = 1), "mythic = 0");
    rejects(v(&|p| p.multipliers.rare = 0), "multipliers.rare");
    let mut t = table(Some(value_mech(vec![(7_500, 1)])));
    t.price = U128(u128::MAX / 3);
    let r = std::panic::catch_unwind(|| contract_with(t));
    assert!(r.err().unwrap().downcast_ref::<String>().unwrap().contains("dépassement"));
    // Gold : planchers et nombre d'emplacements.
    let g = |slots: Vec<GoldSlot>| Mechanics { gold: Some(GoldParams { slots }), ..none_mech() };
    rejects(g(vec![]), "1 à 10");
    rejects(g(vec![GoldSlot { floor: Rarity::Rare, weights: None, burnable: false }; 11]), "1 à 10");
    rejects(g(vec![GoldSlot { floor: Rarity::Epic, weights: Some(w(0, 1, 1, 1, 0)), burnable: false }]), "sous le plancher");
    rejects(g(vec![GoldSlot { floor: Rarity::Mythic, weights: None, burnable: false }]), "poids nuls");
}

/// Brûlable garantie : refusée sans carte adossée illimitée (table de valeur, ou emplacement gold
/// `burnable`).
#[test]
fn burnable_guarantee_needs_an_unlimited_backed_card() {
    for m in [value_mech(vec![(7_500, 1)]), Mechanics { gold: Some(gold_v2()), ..none_mech() }] {
        let mut t = table(Some(m));
        t.mythics = vec![mythic_commit(1, 5)];
        for c in t.cards.iter_mut().filter(|c| c.backing.is_some()) {
            c.cap = Some(10);
        }
        let r = std::panic::catch_unwind(|| contract_with(t));
        assert!(r.err().unwrap().downcast_ref::<String>().unwrap().contains("Brûlable garantie"));
    }
}

/// Stockage prépayé : un gold pack plus long que `cards_per_pack` et la valeur sont comptés.
#[test]
fn storage_covers_longer_gold_packs_and_value() {
    let mut t0 = table(Some(none_mech()));
    t0.mythics = vec![mythic_commit(1, 5)];
    let plain = contract_with(t0).get_series(0).storage_per_pack;
    let mut g = gold_v2();
    g.slots.extend(g.slots.clone()[..2].iter().cloned());
    let mut t = table(Some(Mechanics { gold: Some(g), value: Some(value_p(vec![(7_500, 1)])), ..none_mech() }));
    t.mythics = vec![mythic_commit(1, 5)];
    let mut c = contract_with(t);
    let s = c.get_series(0).storage_per_pack;
    assert_eq!(s, plain + 2 * (PER_CARD_BYTES + SEALED_TOKEN_BYTES) + PACK_VALUE_BYTES);
    // Le gold pack a bien 7 cartes (pitié absente : on force le mode or par le tirage pur).
    let cards: Vec<DrawCard> = c.series_ref(0).draw_cards.clone();
    let mut minted = vec![0; cards.len()];
    let (d, slots) = draw::draw_pack_mech(&c.series_ref(0).table, PackMode::Gold, None, &cards, &mut minted, &mut [0], None, &[7; 32]);
    assert_eq!((d.len(), slots.len()), (7, 7));
    assert!(slots[1].1, "emplacement 2 brûlable");
    let _ = &mut c;
}

/// Série à mécaniques sans table de valeur : pas de règle au dernier emplacement, `value` nul.
#[test]
fn series_without_value_has_no_value_and_no_rule() {
    let mut c = contract_with(table(Some(burn_mech())));
    let id = buy_reveal(&mut c, alice(), 1, 20);
    assert!(last_revealed()["mechanics"]["value"].is_null());
    assert!(pack(&c, id)["value"].is_null());
    assert!(c.packs.get(&id).unwrap().value.is_none());
    let tid = backed_tokens(&c, &alice(), "com_a").into_iter().next();
    if let Some(t) = tid {
        assert_eq!(c.get_backing(t).unwrap().amount, U128(1_000), "montant de la table");
    }
}
