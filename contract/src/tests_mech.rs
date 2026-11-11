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

fn gold() -> RarityWeights {
    // Table or : légendaire seulement (le test voit tout de suite si elle est utilisée).
    w(0, 1, 0, 0, 0)
}

fn mech(pity: Option<PityParams>, burn: bool, rush: Option<RushParams>) -> Mechanics {
    Mechanics { gold_weights: Some(gold()), pity, burn: burn.then_some(BurnParams { floor_bps: 2_500, prior_k: PRIOR_K }), rush }
}

fn contract_with(t: SeriesTable) -> Contract {
    set(owner(), 0, 10);
    let mut c = Contract::new(owner(), Some("redeemer.test".parse().unwrap()), None, None, Some(100));
    let id = c.create_series(t);
    c.open_series(id);
    c
}

/// Achat à `height`, sans tirage. Renvoie le pack.
fn buy_at(c: &mut Contract, buyer: AccountId, height: u64) -> u64 {
    let dep = c.get_series(0).required_deposit.0;
    set(buyer, dep, height);
    c.buy_pack(0).0 as u64
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
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppm: 0, k_ppm: 0, n_max: 1 }), false, None))));
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
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppm: 0, k_ppm: 0, n_max: 4 }), false, None))));
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
    // p0 = 50 % : le choix suit exactement gold_roll(acc) < p, avec acc final du tirage.
    let p = PityParams { p0_ppm: 500_000, k_ppm: 0, n_max: 1_000 };
    let mut c = contract_with(table(Some(mech(Some(p.clone()), false, None))));
    let (mut gold_n, mut n) = (0, 0u32);
    for k in 0..40u8 {
        let id = buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
        let acc: [u8; 32] = hex_decode(pack(&c, id)["acc"].as_str().unwrap()).unwrap().try_into().unwrap();
        let (g, roll, pp) = draw::pity_is_gold(&p, n, &acc);
        assert_eq!(roll as u128, draw::roll(&acc, 0, draw::TAG_GOLD) % 1_000_000);
        assert_eq!(pp, 500_000);
        assert_eq!(pack(&c, id)["mode"] == "gold", g);
        n = if g { gold_n += 1; 0 } else { n + 1 };
    }
    assert!(gold_n > 5 && gold_n < 35, "{gold_n} gold packs sur 40 à 50 %");
}

#[test]
fn pity_probability_grows_linearly_and_caps() {
    let p = PityParams { p0_ppm: 20_000, k_ppm: 10_000, n_max: 500 };
    assert_eq!(draw::pity_p_ppm(&p, 0), 20_000);
    assert_eq!(draw::pity_p_ppm(&p, 10), 120_000);
    assert_eq!(draw::pity_p_ppm(&p, 200), 1_000_000);
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
        let bv = draw::BurnView { burned: &burned, floor_bps: FLOOR, prior_k: (rnd(3) * 10) as u32 };
        let f = draw::burn_factors(&cards, &minted, &bv, Rarity::Common);
        let ws: Vec<u128> =
            (0..n).map(|i| draw::in_rarity_weight(&cards[i], minted[i], burned[i], &bv, f)).collect();
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
    let _ = c.redeem(tid.to_string());
    set_result(PromiseResult::Successful(vec![]));
    c.on_redeem_complete(tid.to_string(), who)
}

fn burn_mech() -> Mechanics {
    burn_mech_k(PRIOR_K)
}

fn burn_mech_k(prior_k: u32) -> Mechanics {
    Mechanics { gold_weights: None, pity: None, burn: Some(BurnParams { floor_bps: FLOOR, prior_k }), rush: None }
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
    let bv = draw::BurnView { burned: &burned, floor_bps: FLOOR, prior_k: 0 };
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
        gold_weights: Some(gold()),
        pity: Some(PityParams { p0_ppm: 0, k_ppm: 0, n_max: 1 }),
        burn: Some(BurnParams { floor_bps: FLOOR, prior_k: PRIOR_K }),
        rush: None,
    }));
    t.cards[0].cap = Some(1);
    let mut c = contract_with(t);
    buy_reveal(&mut c, alice(), 1, 20);
    let r = rarities(&c, 0);
    assert_eq!(r[0], "legendary");
    // Table or = légendaire seulement ; légendaire épuisée : retombée d'un cran (épique).
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
    let mut c = contract_with(table(Some(mech(Some(PityParams { p0_ppm: 0, k_ppm: 0, n_max: 1_000 }), false, Some(small_rush())))));
    buy_reveal(&mut c, alice(), 1, 0); // début de la fenêtre longue
    assert_eq!(c.get_pity(alice(), 0)["n"], 1);
    buy_reveal(&mut c, bob(), 2, 60);
    let b = buy_reveal(&mut c, bob(), 3, 60); // 2 packs dans la fenêtre courte, ×2 la moyenne : déclenche
    assert_eq!(c.get_rush_state(0, Some(60))["last_trigger"], 60);
    assert_eq!(pack(&c, b)["rush"], false);
    // Acheté pendant le rush, révélé bien après sa fin : reste un pack rush (table rush).
    let p = buy_at(&mut c, alice(), 70);
    assert_eq!(c.get_rush_state(0, Some(70))["active"], true);
    reveal(&mut c, p, 4, 500);
    assert_eq!(pack(&c, p)["rush"], true);
    assert_eq!(pack(&c, p)["mode"], "rush");
    assert!(rarities(&c, p).iter().all(|r| r == "epic"));
    // Un pack rush remet le compteur de pitié à zéro.
    assert_eq!(c.get_pity(alice(), 0)["n"], 0);
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
    let mut c = contract_with(epic_table(Some(burn_mech())));
    for k in 0..6u8 {
        buy_reveal(&mut c, alice(), k, 20 + 10 * k as u64);
    }
    let b = backed_tokens(&c, &alice(), "epic_b");
    assert!(!b.is_empty());
    assert!(c.get_backing(b[0].clone()).is_none());
    set(owner(), 0, 100);
    c.set_price_oracle(Some(oracle()));
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

fn resurrect(index: u32) {
    let mut c = contract_with(table(None));
    set(owner(), 0, 100);
    c.set_price_oracle(Some(oracle()));
    set(oracle(), NEAR, 101);
    c.set_resurrected(0, index, Backing { asset_id: "x".into(), amount: U128(1) });
}

#[test]
#[should_panic(expected = "Réservé à l'oracle de prix")]
fn resurrection_is_oracle_only() {
    let mut c = contract_with(table(None));
    set(owner(), 0, 100);
    c.set_price_oracle(Some(oracle()));
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
    let pity = |n| Some(PityParams { p0_ppm: 0, k_ppm: 0, n_max: n });
    rejects(Mechanics { gold_weights: None, pity: pity(3), burn: None, rush: None }, "pity exige gold_weights");
    rejects(mech(pity(0), false, None), "n_max");
    rejects(mech(Some(PityParams { p0_ppm: 2_000_000, k_ppm: 0, n_max: 3 }), false, None), "ppm");
    rejects(mech(None, false, Some(rush(15_000, 2, 25, 100, 10, 5, 0))), "multiples");
    rejects(mech(None, false, Some(rush(15_000, 2, 10, 1_000, 10, 5, 0))), "96 seaux");
    rejects(mech(None, false, Some(rush(9_999, 2, 10, 100, 10, 5, 0))), "ratio_bps ≥ 10 000");
    rejects(mech(None, false, Some(rush(60_000, 2, 10, 50, 10, 5, 0))), "inatteignable");
    rejects(mech(None, false, Some(rush(15_000, 0, 10, 100, 10, 5, 0))), "min_packs");
    rejects(mech(None, false, Some(rush(15_000, 2, 10, 100, 10, 0, 0))), "durée");
    rejects(mech(None, false, Some(rush(15_000, 2, 100, 100, 10, 5, 0))), "plus courte");
    let mut same = rush(15_000, 2, 10, 100, 10, 5, 0);
    same.weights = gold();
    rejects(mech(None, false, Some(same)), "distincte de la table or");
    rejects(Mechanics { gold_weights: Some(w(1, 0, 0, 0, 0)), pity: None, burn: None, rush: None }, "engagement");
    rejects(Mechanics { gold_weights: None, pity: None, burn: Some(BurnParams { floor_bps: 10_001, prior_k: 0 }), rush: None }, "floor_bps");
    // Table or qui donne du poids à une rareté sans carte : refusée à l'ouverture.
    let mut t = table(Some(Mechanics { gold_weights: Some(w(0, 1, 0, 0, 0)), pity: None, burn: None, rush: None }));
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
