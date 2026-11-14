//! Tests des types de packs (`SeriesTable::kinds`) : packs thématiques tirés dans la même table que le
//! pack de base, avec les mêmes compteurs et plafonds, leur prix, leurs cartes et leurs règles par
//! emplacement.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::Value;
use near_sdk::test_utils::{accounts, get_logs, VMContextBuilder};
use near_sdk::testing_env;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;

fn owner() -> AccountId {
    accounts(0)
}
fn alice() -> AccountId {
    accounts(1)
}
fn contract_id() -> AccountId {
    "memaster.test".parse().unwrap()
}

fn set(pred: AccountId, deposit: u128, height: u64) {
    let mut b = VMContextBuilder::new();
    b.current_account_id(contract_id())
        .predecessor_account_id(pred.clone())
        .signer_account_id(pred)
        .attached_deposit(NearToken::from_yoctonear(deposit))
        .prepaid_gas(Gas::from_tgas(300))
        .block_height(height)
        .account_balance(NearToken::from_yoctonear(1_000 * NEAR));
    testing_env!(b.build());
}

fn set_seed(height: u64, seed: [u8; 32]) {
    let mut b = VMContextBuilder::new();
    b.current_account_id(contract_id())
        .predecessor_account_id(contract_id())
        .signer_account_id(contract_id())
        .prepaid_gas(Gas::from_tgas(300))
        .block_height(height)
        .account_balance(NearToken::from_yoctonear(1_000 * NEAR))
        .random_seed(seed);
    testing_env!(b.build());
}

fn card(id: &str, rarity: Rarity, cap: Option<u32>, backing: bool) -> CardDef {
    CardDef {
        card_id: id.to_string(),
        title: id.to_uppercase(),
        rarity,
        weight: 1,
        cap,
        media: None,
        reference: None,
        backing: backing.then(|| Backing { asset_id: format!("nep141:{id}.near"), amount: U128(1_000) }),
    }
}

/// 0 dog-com (illimitée), 1 dog-com-2, 2 dog-rare, 3 dog-epic (plafond 2), 4 dog-burn (commune adossée),
/// 5 cat-com, 6 cat-rare, 7 com (illimitée, adossée), 8 rare, 9 epic, 10 leg.
fn cards() -> Vec<CardDef> {
    vec![
        card("dog-com", Rarity::Common, None, false),
        card("dog-com-2", Rarity::Common, None, false),
        card("dog-rare", Rarity::Rare, None, false),
        card("dog-epic", Rarity::Epic, Some(2), false),
        card("dog-burn", Rarity::Common, None, true),
        card("cat-com", Rarity::Common, None, false),
        card("cat-rare", Rarity::Rare, None, false),
        card("com", Rarity::Common, None, true),
        card("rare", Rarity::Rare, None, false),
        card("epic", Rarity::Epic, None, false),
        card("leg", Rarity::Legendary, None, false),
    ]
}

const DOGS: [u32; 5] = [0, 1, 2, 3, 4];

fn kind(name: &str, price: u128, n: u8, cards: Vec<u32>) -> PackKind {
    PackKind { name: name.into(), price: U128(price), cards_per_pack: n, pool: cards, mythics: false, slots: None, value: false }
}

fn table(kinds: Option<Vec<PackKind>>, mechanics: Option<Mechanics>) -> SeriesTable {
    SeriesTable {
        name: "Kinds".into(),
        price: U128(NEAR / 10),
        cards_per_pack: 5,
        rarity_weights: RarityWeights { mythic: 0, legendary: 10, epic: 90, rare: 300, common: 600 },
        cards: cards(),
        mythics: vec![],
        royalties: vec![],
        mechanics,
        kinds,
    }
}

fn value_mech() -> Mechanics {
    Mechanics {
        gold: None,
        pity: None,
        burn: None,
        rush: None,
        resurrection: None,
        value: Some(ValueParams {
            normal: vec![(7_500, 1)],
            gold: vec![(30_000, 1)],
            rush: vec![(9_000, 1)],
            multipliers: RarityWeights { mythic: 0, legendary: 20, epic: 5, rare: 2, common: 1 },
        }),
    }
}

fn contract_with(t: SeriesTable) -> Contract {
    set(owner(), 0, 10);
    let mut c = Contract::new(owner(), Some("redeemer.test".parse().unwrap()), None, None, Some(100), None);
    let id = c.create_series(t);
    c.open_series(id);
    c
}

fn deposit(c: &Contract, kind: Option<u32>) -> u128 {
    let s = c.get_series(0);
    match kind {
        None => s.required_deposit.0,
        Some(k) => s.kinds[k as usize]["required_deposit"].as_str().unwrap().parse().unwrap(),
    }
}

fn buy(c: &mut Contract, kind: Option<u32>, height: u64) -> u64 {
    c.flush_all();
    let dep = deposit(c, kind);
    set(alice(), dep, height);
    c.buy_pack(0, kind).0 as u64
}

fn reveal(c: &mut Contract, pack_id: u64, seed: u8, height: u64) {
    for step in 1..=3u8 {
        c.flush_all();
        set_seed(height + step as u64, [seed.wrapping_add(step); 32]);
        c.reveal_step(pack_id, 0, step);
    }
}

fn open(c: &mut Contract, kind: Option<u32>, seed: u8, height: u64) -> (u64, Value) {
    let pid = buy(c, kind, height);
    reveal(c, pid, seed, height);
    (pid, c.get_pack(pid).unwrap())
}

fn event(name: &str) -> Value {
    let line = get_logs()
        .into_iter()
        .filter_map(|l| l.strip_prefix("EVENT_JSON:").map(str::to_string))
        .find(|l| l.contains(&format!("\"event\":\"{name}\"")))
        .unwrap_or_else(|| panic!("événement {name} absent : {:?}", get_logs()));
    near_sdk::serde_json::from_str::<Value>(&line).unwrap()["data"][0].clone()
}

fn indexes(p: &Value) -> Vec<u32> {
    p["draws"].as_array().unwrap().iter().map(|d| d["index"].as_u64().unwrap() as u32).collect()
}

// ----------------------------------------------------------------- tirage dans les cartes du type

#[test]
fn kind_pack_draws_only_its_cards_with_its_size() {
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    for i in 0..20u8 {
        let (_, p) = open(&mut c, Some(0), i, 100 + i as u64 * 10);
        assert_eq!(p["draws"].as_array().unwrap().len(), 8, "8 cartes par pack Dog");
        assert_eq!(p["kind"], 0);
        for ix in indexes(&p) {
            assert!(DOGS.contains(&ix), "carte {ix} hors du pack Dog");
        }
    }
}

#[test]
fn kind_shares_caps_and_counters_with_the_base_pack() {
    // dog-epic a un plafond de 2 pour toute la série : packs Dog et packs de base confondus.
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    for i in 0..30u8 {
        let k = if i % 2 == 0 { Some(0) } else { None };
        open(&mut c, k, i, 100 + i as u64 * 10);
    }
    let s = c.get_series(0);
    assert!(s.minted[3] <= 2, "plafond partagé dépassé : {}", s.minted[3]);
    let total: u32 = s.minted.iter().sum();
    assert_eq!(total, 15 * 8 + 15 * 5, "un seul jeu de compteurs pour toute la série");
}

#[test]
fn kind_price_and_deposit_are_its_own() {
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    let s = c.get_series(0);
    let storage = s.required_deposit.0 - s.price.0;
    assert_eq!(deposit(&c, Some(0)), NEAR / 5 + storage);
    let pid = buy(&mut c, Some(0), 100);
    let ev = event("pack_bought");
    assert_eq!(ev["kind"], 0);
    assert_eq!(ev["price"].as_str().unwrap(), (NEAR / 5).to_string());
    reveal(&mut c, pid, 1, 100);
    assert_eq!(c.get_pack(pid).unwrap()["price_paid"].as_str().unwrap(), (NEAR / 5).to_string());
    // Le pack de base garde son prix, et son événement ne porte pas de champ `kind`.
    buy(&mut c, None, 200);
    assert!(event("pack_bought").get("kind").is_none());
}

#[test]
#[should_panic(expected = "E_DEPOSIT")]
fn kind_pack_needs_its_own_deposit() {
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    c.flush_all();
    let base = deposit(&c, None);
    set(alice(), base, 100);
    c.buy_pack(0, Some(0));
}

#[test]
#[should_panic(expected = "E_UNKNOWN_KIND")]
fn unknown_kind_is_rejected() {
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    set(alice(), 10 * NEAR, 100);
    c.buy_pack(0, Some(3));
}

// ----------------------------------------------------------------- règles par emplacement

#[test]
fn slot_floor_holds_on_every_pack() {
    let mut k = kind("Cat", NEAR / 10, 3, vec![5, 6, 7, 8, 9]);
    let floor = GoldSlot { floor: Rarity::Rare, weights: None, burnable: false };
    let any = GoldSlot { floor: Rarity::Common, weights: None, burnable: false };
    k.slots = Some(vec![any.clone(), any, floor]);
    let mut c = contract_with(table(Some(vec![k]), None));
    for i in 0..40u8 {
        let (_, p) = open(&mut c, Some(0), i, 100 + i as u64 * 10);
        let last = &p["draws"][2]["final_rarity"];
        assert!(last == "rare" || last == "epic" || last == "legendary", "carte 3 sous le plancher : {last}");
    }
}

#[test]
fn burnable_slot_rule_draws_a_burnable() {
    let mut k = kind("Dog", NEAR / 5, 4, DOGS.to_vec());
    let any = GoldSlot { floor: Rarity::Common, weights: None, burnable: false };
    k.slots = Some(vec![any.clone(), any.clone(), any, GoldSlot { floor: Rarity::Common, weights: None, burnable: true }]);
    let mut c = contract_with(table(Some(vec![k]), None));
    for i in 0..10u8 {
        let (_, p) = open(&mut c, Some(0), i, 100 + i as u64 * 10);
        assert_eq!(p["draws"][3]["index"], 4, "dernière carte : la seule brûlable du pack Dog");
    }
}

// ----------------------------------------------------------------- pitié, valeur, mythiques

#[test]
fn kind_packs_never_turn_gold_nor_move_pity() {
    let mut m = value_mech();
    m.value = None;
    m.pity = Some(PityParams { p0_ppb: 1_000_000_000, k_ppb: 0, p_max_ppb: 1_000_000_000, n_max: None });
    m.gold = Some(GoldParams { slots: vec![GoldSlot { floor: Rarity::Rare, weights: None, burnable: false }; 5] });
    let mut c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), Some(m)));
    let (_, p) = open(&mut c, Some(0), 1, 100);
    assert_eq!(p["mode"], "base");
    let ev = event("pack_revealed");
    assert!(ev["mechanics"]["pity"].is_null(), "pas de pitié pour un type de pack");
    assert_eq!(c.get_pity(alice(), 0)["n"], 0, "compteur de pitié inchangé");
    // Le pack de base, lui, devient gold (p0 = 100 %).
    let (_, p) = open(&mut c, None, 2, 200);
    assert_eq!(p["mode"], "gold");
}

#[test]
fn value_follows_the_kind_price_or_is_absent() {
    let with_value = PackKind { value: true, ..kind("Big", NEAR / 5, 5, vec![]) };
    let no_value = kind("Plain", NEAR / 5, 5, vec![]);
    let mut c = contract_with(table(Some(vec![with_value, no_value]), Some(value_mech())));
    let (_, base) = open(&mut c, None, 1, 100);
    let (_, big) = open(&mut c, Some(0), 2, 200);
    let (_, plain) = open(&mut c, Some(1), 3, 300);
    let total = |p: &Value| p["value"]["total"].as_str().unwrap().parse::<u128>().unwrap();
    assert_eq!(total(&base), NEAR / 10 * 7_500 / 10_000);
    assert_eq!(total(&big), 2 * total(&base), "valeur ∝ prix du type");
    assert!(plain["value"].is_null(), "pas de valeur pour un type sans table de valeur");
}

#[test]
fn kind_without_mythics_never_draws_one() {
    let mut t = table(None, None);
    t.rarity_weights = RarityWeights { mythic: 1_000, legendary: 0, epic: 0, rare: 0, common: 1 };
    t.mythics = vec![MythicCommitment { commitment: "aa".repeat(32), content_hash: "bb".repeat(32), weight: 1, cap: 100 }];
    let k = kind("NoMyth", 1, 5, vec![]);
    let cards: Vec<DrawCard> = t.cards.iter().map(DrawCard::from).collect();
    for seed in 0..20u8 {
        let mut minted = vec![0; cards.len()];
        let mut mm = vec![0; 1];
        let kc = draw::kind_cards(&cards, Some(&k));
        let (base, _) = draw::draw_pack_mech(&t, PackMode::Base, None, &cards, &mut minted.clone(), &mut mm.clone(), None, &[seed; 32]);
        assert!(base.iter().any(|d| d.kind == CardKind::Mythic), "le pack de base tire des mythiques");
        let (d, _) = draw::draw_pack_mech(&t, PackMode::Base, Some(&k), &kc, &mut minted, &mut mm, None, &[seed; 32]);
        assert!(d.iter().all(|d| d.kind == CardKind::Visible));
    }
}

// ----------------------------------------------------------------- hash et vues

#[test]
fn table_without_kinds_keeps_its_bytes() {
    let json = near_sdk::serde_json::to_string(&table(None, None)).unwrap();
    assert!(!json.contains("kinds"), "aucun champ kinds sans types de packs : hash d'avant inchangé");
    let json = near_sdk::serde_json::to_string(&table(Some(vec![kind("Dog", 1, 8, vec![0])]), None)).unwrap();
    assert!(json.ends_with(r#""kinds":[{"name":"Dog","price":"1","cards_per_pack":8,"pool":[0],"mythics":false,"slots":null,"value":false}]}"#));
}

#[test]
fn kind_rates_list_only_its_cards() {
    let c = contract_with(table(Some(vec![kind("Dog", NEAR / 5, 8, DOGS.to_vec())]), None));
    let r = c.get_kind_rates(0, 0, None, None);
    let listed: Vec<u64> = r["rarities"]
        .as_array()
        .unwrap()
        .iter()
        .flat_map(|x| x["cards"].as_array().unwrap().iter().map(|c| c["index"].as_u64().unwrap()))
        .collect();
    let mut listed = listed;
    listed.sort();
    assert_eq!(listed, vec![0, 1, 2, 3, 4]);
    assert_eq!(r["kind"]["name"], "Dog");
    // Pas de légendaire chez les chiens : la rareté garde son poids, sans carte (le tirage retombe).
    let leg = r["rarities"].as_array().unwrap().iter().find(|x| x["rarity"] == "legendary").unwrap();
    assert_eq!(leg["rarity_card_weight"], 0);
}

#[test]
fn storage_covers_the_biggest_kind() {
    let small = contract_with(table(None, None)).get_series(0).storage_per_pack;
    let big = contract_with(table(Some(vec![kind("Ten", NEAR, 10, vec![])]), None)).get_series(0).storage_per_pack;
    assert!(big > small, "10 cartes par pack : plus de stockage prépayé ({big} > {small})");
}

// ----------------------------------------------------------------- validation

#[test]
#[should_panic(expected = "E_KINDS")]
fn slots_must_match_pack_size() {
    let mut k = kind("Bad", 1, 3, vec![]);
    k.slots = Some(vec![GoldSlot { floor: Rarity::Common, weights: None, burnable: false }]);
    contract_with(table(Some(vec![k]), None));
}

#[test]
#[should_panic(expected = "E_KINDS")]
fn kind_cards_must_exist() {
    contract_with(table(Some(vec![kind("Bad", 1, 3, vec![0, 99])]), None));
}

#[test]
#[should_panic(expected = "E_KINDS")]
fn kind_needs_an_unlimited_common() {
    // cat-rare et rare seulement : aucune commune, le tirage pourrait ne rien trouver.
    contract_with(table(Some(vec![kind("Bad", 1, 3, vec![6, 8])]), None));
}

#[test]
#[should_panic(expected = "E_KINDS")]
fn value_kind_needs_a_burnable() {
    let k = PackKind { value: true, ..kind("Bad", 1, 3, vec![0, 1, 2]) };
    contract_with(table(Some(vec![k]), Some(value_mech())));
}

#[test]
#[should_panic(expected = "E_KINDS")]
fn kind_names_are_unique() {
    contract_with(table(Some(vec![kind("Dog", 1, 3, vec![]), kind("Dog", 2, 3, vec![])]), None));
}
