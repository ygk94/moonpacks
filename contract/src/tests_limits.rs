//! Revue du 12/11 : cas limites des mécaniques (pitié au plafond du compteur, burns jusqu'au
//! plancher, raretés et mythiques épuisées dans le dernier reçu) et tables refusées à la validation.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::test_utils::{accounts, VMContextBuilder};
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

fn set(pred: AccountId, deposit: u128, height: u64, seed: [u8; 32]) {
    let mut b = VMContextBuilder::new();
    b.current_account_id(contract_id())
        .predecessor_account_id(pred.clone())
        .signer_account_id(pred)
        .attached_deposit(NearToken::from_yoctonear(deposit))
        .prepaid_gas(Gas::from_tgas(300))
        .block_height(height)
        .random_seed(seed)
        .account_balance(NearToken::from_near(1_000));
    testing_env!(b.build());
}

fn card(id: &str, rarity: Rarity, weight: u32, cap: Option<u32>, backed: bool) -> CardDef {
    CardDef {
        card_id: id.to_string(),
        title: id.to_uppercase(),
        rarity,
        weight,
        cap,
        media: None,
        reference: None,
        backing: backed.then(|| Backing { asset_id: format!("nep141:{id}.near"), amount: U128(1_000) }),
    }
}

fn w(m: u32, l: u32, e: u32, r: u32, c: u32) -> RarityWeights {
    RarityWeights { mythic: m, legendary: l, epic: e, rare: r, common: c }
}

fn hex64(tag: &str) -> String {
    hex_encode(&env::sha256(tag.as_bytes()))
}

fn no_mech() -> Mechanics {
    Mechanics { gold: None, pity: None, burn: None, rush: None, resurrection: None, value: None }
}

fn base_table() -> SeriesTable {
    SeriesTable {
        kinds: None,
        name: "Limites".into(),
        price: U128(NEAR / 10),
        cards_per_pack: 5,
        rarity_weights: w(0, 10, 10, 10, 70),
        cards: vec![
            card("leg", Rarity::Legendary, 1, None, true),
            card("epic", Rarity::Epic, 1, None, false),
            card("rare", Rarity::Rare, 1, None, false),
            card("com", Rarity::Common, 1, None, true),
        ],
        mythics: vec![],
        royalties: vec![],
        mechanics: None,
    }
}

fn open(t: SeriesTable) -> Contract {
    set(owner(), 0, 10, [0; 32]);
    let mut c = Contract::new(owner(), Some("redeemer.test".parse().unwrap()), None, None, Some(100), None);
    let id = c.create_series(t);
    c.open_series(id);
    c
}

/// Achat puis les trois reçus du tirage (graines distinctes par pack).
fn buy_reveal(c: &mut Contract, n: u64) -> u64 {
    let dep = c.get_series(0).required_deposit.0;
    let h = 100 + n * 10;
    set(alice(), dep, h, [0; 32]);
    let p = c.buy_pack(0, None).0 as u64;
    for step in 1..=3u8 {
        let mut seed = [0u8; 32];
        seed[..8].copy_from_slice(&n.to_le_bytes());
        seed[8] = step;
        set(contract_id(), 0, h + step as u64, seed);
        c.reveal_step(p, 0, step);
    }
    p
}

fn draws(c: &Contract, p: u64) -> Vec<near_sdk::serde_json::Value> {
    c.get_pack(p).unwrap()["draws"].as_array().unwrap().clone()
}

// ----------------------------------------------------------------- pitié au plafond

fn pity_table(n_max: Option<u32>) -> SeriesTable {
    let mut t = base_table();
    t.mechanics = Some(Mechanics {
        gold: Some(GoldParams { slots: vec![GoldSlot { floor: Rarity::Legendary, weights: Some(w(0, 1, 0, 0, 0)), burnable: false }; 3] }),
        pity: Some(PityParams { p0_ppb: 0, k_ppb: 7, p_max_ppb: 40_000, n_max }),
        ..no_mech()
    });
    t
}

#[test]
fn pity_counter_saturates_at_u32_max_without_panic() {
    let mut c = open(pity_table(None));
    c.pity.insert((alice(), 0), u32::MAX - 1);
    let v = c.get_pity(alice(), 0);
    assert_eq!(v["p_ppb"], 40_000, "p plafonné à p_max");
    assert_eq!(v["packs_to_max"], 0);
    // Deux packs (le gold pack est très improbable : 1 sur 25 000) : le compteur sature à u32::MAX.
    let mut after = vec![];
    for n in 0..2 {
        let p = buy_reveal(&mut c, n);
        let gold = c.get_pack(p).unwrap()["mode"] == "gold";
        after.push((gold, c.get_pity(alice(), 0)["n"].as_u64().unwrap()));
    }
    for (gold, n) in after {
        assert!(gold && n == 0 || !gold && n == u32::MAX as u64, "compteur après : {n} (gold {gold})");
    }
    // Décision au plafond : seuil p_max, jamais au-delà.
    let p = PityParams { p0_ppb: 1, k_ppb: u32::MAX, p_max_ppb: 1_000_000_000, n_max: None };
    assert_eq!(draw::pity_p_ppb(&p, u32::MAX), 1_000_000_000);
    let acc = [7u8; 32];
    assert!(draw::pity_is_gold(&p, u32::MAX, &acc).0, "p = 10⁹ ppb : toujours gold");
    assert_eq!(draw::pity_after(u32::MAX, false), u32::MAX);
}

#[test]
fn pity_guarantee_holds_even_past_n_max() {
    // Un compteur déjà au-delà de la garantie (n_max abaissé n'existe pas, mais l'état est là) :
    // le pack suivant est un gold pack et le compteur repart à 0.
    let mut c = open(pity_table(Some(5)));
    c.pity.insert((alice(), 0), 9);
    assert_eq!(c.get_pity(alice(), 0)["guaranteed_in"], 1);
    let p = buy_reveal(&mut c, 0);
    assert_eq!(c.get_pack(p).unwrap()["mode"], "gold");
    assert_eq!(draws(&c, p).len(), 3, "gold pack de 3 emplacements");
    assert_eq!(c.get_pity(alice(), 0)["n"], 0);
    c.pity.insert((alice(), 0), u32::MAX);
    let p = buy_reveal(&mut c, 1);
    assert_eq!(c.get_pack(p).unwrap()["mode"], "gold", "n = u32::MAX ≥ n_max : garanti");
}

// ----------------------------------------------------------------- burns jusqu'au plancher

#[test]
fn burns_down_to_floor_bounds() {
    // Tout brûlé : plancher, jamais 0 ; plancher 100 % : les burns ne changent rien ; plancher 0 :
    // poids 1 ; burned > minted (impossible, mais sans panique) : comme tout brûlé.
    for (w_, floor, k) in [(100u32, 2_500u32, 0u32), (100, 10_000, 0), (100, 0, 0), (u32::MAX, 2_500, 1_000_000), (1, 0, 0)] {
        let all = draw::raw_burn_weight(w_, 50, 50, None, floor, k);
        let fl = ((w_ as u128 * floor as u128 / 10_000) as u64).max(1);
        let ratio = (w_ as u128 * k as u128 / (50 + k as u128)) as u64;
        assert_eq!(all, fl.max(ratio), "w {w_} plancher {floor} K {k}");
        assert!(all >= 1);
        assert_eq!(draw::raw_burn_weight(w_, 50, 60, None, floor, k), all, "burned > minted : saturé");
        if floor == 10_000 {
            assert_eq!(all, w_ as u64);
        }
    }
    // Épuisée par son plafond : 0, même sans burn.
    assert_eq!(draw::raw_burn_weight(100, 3, 0, Some(3), 2_500, 20), 0);
    // Rareté dont toutes les brûlables sont au plancher : la part des brûlables ne bouge pas.
    let cards = [
        DrawCard { rarity: Rarity::Common, weight: 100, cap: None, backed: true },
        DrawCard { rarity: Rarity::Common, weight: 300, cap: None, backed: true },
        DrawCard { rarity: Rarity::Common, weight: 600, cap: None, backed: false },
    ];
    let minted = [40, 40, 40];
    let burned = [40, 40, 0];
    let bv = draw::BurnView { burned: &burned, floor_bps: 2_500, prior_k: 0, resurrectable: &[] };
    let f = draw::burn_factors(&cards, &minted, &bv, Rarity::Common);
    let ws: Vec<u128> = (0..3).map(|i| draw::in_rarity_weight(&cards[i], i, minted[i], &bv, f)).collect();
    let total: u128 = ws.iter().sum();
    assert_eq!((ws[0] + ws[1]) * 1_000 / total, 400, "brûlables : 40 % comme sans burn");
    assert_eq!(ws[0] * 3, ws[1], "au plancher, proportionnelles à leur poids de base");
}

// ----------------------------------------------------------------- raretés épuisées

#[test]
fn exhausted_rarities_and_mythics_fall_back_in_final_receipt() {
    let mut t = base_table();
    t.rarity_weights = w(30, 30, 20, 10, 10);
    t.cards = vec![
        card("leg", Rarity::Legendary, 1, Some(1), true),
        card("epic", Rarity::Epic, 1, Some(2), false),
        card("rare", Rarity::Rare, 1, Some(1), true),
        card("com_b", Rarity::Common, 5, None, true),
        card("com_c", Rarity::Common, 5, Some(1), false),
    ];
    t.mythics = vec![MythicCommitment { commitment: hex64("m"), content_hash: hex64("h"), weight: 1, cap: 1 }];
    t.mechanics = Some(Mechanics {
        gold: Some(GoldParams {
            slots: vec![
                GoldSlot { floor: Rarity::Legendary, weights: Some(w(1, 1, 0, 0, 0)), burnable: false },
                GoldSlot { floor: Rarity::Rare, weights: None, burnable: true },
            ],
        }),
        pity: Some(PityParams { p0_ppb: 0, k_ppb: 0, p_max_ppb: 0, n_max: Some(2) }),
        burn: Some(BurnParams { floor_bps: 2_500, prior_k: 0 }),
        value: Some(ValueParams {
            normal: vec![(7_500, 1)],
            gold: vec![(30_000, 1)],
            rush: vec![(7_500, 1)],
            multipliers: w(0, 10, 5, 2, 1),
        }),
        ..no_mech()
    });
    let mut c = open(t);
    let mut counts = [0u32; 5];
    let mut myth = 0;
    for n in 0..40 {
        let p = buy_reveal(&mut c, n);
        let v = c.get_pack(p).unwrap();
        let ds = draws(&c, p);
        // Le dernier emplacement d'un pack normal et l'emplacement 1 d'un gold pack sont brûlables.
        let last = if v["mode"] == "gold" { 1 } else { ds.len() - 1 };
        let d = &ds[last];
        assert_eq!(d["kind"], "visible");
        let i = d["index"].as_u64().unwrap() as usize;
        assert!(matches!(i, 0 | 2 | 3), "brûlable garantie : {d}");
        // Valeur répartie : total exact entre les brûlables.
        let total: u128 = v["value"]["total"].as_str().unwrap().parse().unwrap();
        let sum: u128 = v["value"]["amounts"].as_array().unwrap().iter().filter_map(|a| a.as_str()).map(|s| s.parse::<u128>().unwrap()).sum();
        assert_eq!(sum, total);
        for d in &ds {
            if d["kind"] == "mythic" {
                myth += 1;
            } else {
                counts[d["index"].as_u64().unwrap() as usize] += 1;
            }
        }
    }
    assert_eq!(myth, 1, "mythique au plafond 1");
    assert_eq!(counts[0], 1, "légendaire au plafond 1");
    assert_eq!(counts[1], 2, "épique au plafond 2");
    assert_eq!(counts[2], 1, "rare au plafond 1");
    assert_eq!(counts[4], 1, "commune plafonnée à 1");
    // Tout est épuisé sauf la commune illimitée : les derniers packs, gold compris, n'ont qu'elle.
    let p = buy_reveal(&mut c, 99);
    assert!(draws(&c, p).iter().all(|d| d["index"] == 3 && d["kind"] == "visible"));
}

// ----------------------------------------------------------------- tables refusées

fn rejected(t: SeriesTable, msg: &str) {
    let r = std::panic::catch_unwind(move || open(t));
    let e = r.err().unwrap_or_else(|| panic!("table acceptée (attendu : {msg})"));
    let s = e.downcast_ref::<String>().cloned().unwrap_or_default();
    assert!(s.contains(msg), "« {s} » ne contient pas « {msg} »");
}

fn with(f: impl FnOnce(&mut SeriesTable)) -> SeriesTable {
    let mut t = base_table();
    f(&mut t);
    t
}

fn with_mech(f: impl FnOnce(&mut Mechanics, &mut SeriesTable)) -> SeriesTable {
    let mut t = base_table();
    let mut m = no_mech();
    f(&mut m, &mut t);
    t.mechanics = Some(m);
    t
}

fn myth(tag: &str, weight: u32, cap: u32) -> MythicCommitment {
    MythicCommitment { commitment: hex64(tag), content_hash: hex64(&format!("{tag}/h")), weight, cap }
}

fn value() -> ValueParams {
    ValueParams { normal: vec![(7_500, 1)], gold: vec![(30_000, 1)], rush: vec![(7_500, 1)], multipliers: w(0, 10, 5, 2, 1) }
}

#[test]
fn invalid_headers_are_rejected() {
    rejected(with(|t| t.name = String::new()), "name : longueur invalide");
    rejected(with(|t| t.name = "x".repeat(MAX_TITLE_LEN + 1)), "name : longueur invalide");
    rejected(with(|t| t.price = U128(0)), "Le prix doit être > 0");
    rejected(with(|t| t.cards_per_pack = 0), "cards_per_pack hors bornes");
    rejected(with(|t| t.cards_per_pack = MAX_CARDS_PER_PACK + 1), "cards_per_pack hors bornes");
    rejected(with(|t| t.rarity_weights = w(0, 0, 0, 0, 0)), "Poids de rareté nuls");
    rejected(with(|t| t.mythics = (0..=MAX_MYTHICS_PER_SERIES).map(|i| myth(&i.to_string(), 1, 1)).collect()), "Trop de mythiques");
    rejected(with(|t| t.mythics = vec![MythicCommitment { commitment: hex64("a").to_uppercase(), ..myth("a", 1, 1) }]), "commitment : 64 caractères hex");
    rejected(with(|t| t.mythics = vec![MythicCommitment { commitment: hex64("a")[..62].into(), ..myth("a", 1, 1) }]), "commitment : 64 caractères hex");
    rejected(with(|t| t.mythics = vec![MythicCommitment { content_hash: "zz".repeat(32), ..myth("a", 1, 1) }]), "content_hash : 64 caractères hex");
    rejected(with(|t| t.mythics = vec![myth("a", 1, 0)]), "Plafond de mythique hors bornes");
    rejected(with(|t| t.mythics = vec![myth("a", 1, MAX_MYTHIC_CAP + 1)]), "Plafond de mythique hors bornes");
    rejected(
        with(|t| t.mythics = vec![myth("a", 1, 1), MythicCommitment { content_hash: hex64("b/h"), ..myth("a", 1, 1) }]),
        "Engagement en double",
    );
    let r = |bps| Royalty { account_id: accounts(3), bps };
    rejected(with(|t| t.royalties = vec![r(2_500), r(2_501)]), "Redevances > 50 %");
    rejected(with(|t| t.royalties = (0..=MAX_ROYALTIES).map(|_| r(1)).collect()), "Trop de redevances");
}

#[test]
fn invalid_cards_and_coverage_are_rejected() {
    rejected(with(|t| t.cards[0].card_id = String::new()), "card_id : longueur invalide");
    rejected(with(|t| t.cards[0].card_id = "x".repeat(MAX_ID_LEN + 1)), "card_id : longueur invalide");
    rejected(with(|t| t.cards[0].title = String::new()), "title : longueur invalide");
    rejected(with(|t| t.cards[0].media = Some("u".repeat(MAX_URL_LEN + 1))), "media : longueur invalide");
    rejected(with(|t| t.cards[0].reference = Some(String::new())), "reference : longueur invalide");
    rejected(with(|t| t.cards[0].backing = Some(Backing { asset_id: "a".into(), amount: U128(0) })), "amount doit être > 0");
    rejected(with(|t| t.cards[0].backing = Some(Backing { asset_id: "a".repeat(MAX_ASSET_ID_LEN + 1), amount: U128(1) })), "asset_id : longueur invalide");
    rejected(with(|t| t.cards[0].rarity = Rarity::Mythic), "Les mythiques passent par des engagements");
    rejected(with(|t| t.rarity_weights.legendary = 0), "Carte dans une rareté de poids nul");
    rejected(with(|t| t.cards[1].card_id = "leg".into()), "card_id en double");
    // Rareté pondérée dont la seule carte a un poids nul.
    rejected(with(|t| t.cards[1].weight = 0), "Rareté epic sans carte");
    // Seule commune plafonnée, ou de poids nul.
    rejected(with(|t| t.cards[3].cap = Some(10)), "commune sans plafond");
    rejected(with(|t| t.cards[3].weight = 0), "Rareté common sans carte");
    // Table de 201 cartes en un appel.
    rejected(
        with(|t| t.cards.extend((0..MAX_CARDS_PER_CALL).map(|i| card(&format!("c{i:03}"), Rarity::Common, 1, None, false)))),
        "Trop de cartes pour un appel",
    );
}

#[test]
fn invalid_mechanics_params_are_rejected() {
    rejected(with_mech(|m, _| m.burn = Some(BurnParams { floor_bps: 0, prior_k: MAX_BURN_PRIOR_K + 1 })), "burn.prior_k");
    // Poids mythiques d'une table rush ou d'un emplacement or sans engagement pondéré.
    let rp = RushParams {
        ratio_bps: 15_000, min_packs: 1, window_blocks: 10, baseline_blocks: 100, bucket_blocks: 10,
        duration_blocks: 5, cooldown_blocks: 0, max_per_account: 1, weights: w(1, 0, 0, 0, 1),
    };
    rejected(with_mech(|m, _| m.rush = Some(rp.clone())), "rush.weights : poids mythique sans engagement");
    rejected(with_mech(|m, _| m.rush = Some(RushParams { weights: w(0, 0, 0, 0, 0), ..rp.clone() })), "rush.weights : poids nuls");
    rejected(
        with_mech(|m, t| {
            t.mythics = vec![myth("a", 0, 1)];
            m.gold = Some(GoldParams { slots: vec![GoldSlot { floor: Rarity::Mythic, weights: Some(w(1, 0, 0, 0, 0)), burnable: false }] });
        }),
        "gold.slots[0] : poids mythique sans engagement",
    );
    // Résurrection : index inconnu, non croissants, rareté, carte adossée, liste trop longue.
    let res = |v: Vec<u32>| Some(ResurrectionParams { eligible: v });
    rejected(with_mech(|m, _| m.resurrection = res(vec![9])), "resurrection.eligible : index de carte inconnu");
    rejected(with_mech(|m, _| m.resurrection = res(vec![1, 1])), "strictement croissants");
    rejected(with_mech(|m, _| m.resurrection = res(vec![2])), "épiques et légendaires seulement");
    rejected(with_mech(|m, _| m.resurrection = res(vec![0])), "carte déjà adossée par la table");
    rejected(with_mech(|m, _| m.resurrection = res((0..=MAX_RESURRECTABLE as u32).collect())), "200 cartes au plus");
    // Valeur : dépassement de u128, brûlable garantie absente (seule brûlable plafonnée).
    rejected(with_mech(|m, t| {
        t.price = U128(u128::MAX / 2);
        m.value = Some(value());
    }), "dépassement de u128");
    rejected(with_mech(|m, t| {
        t.cards[0].cap = Some(1);
        t.cards[3].backing = None;
        m.value = Some(value());
    }), "Brûlable garantie");
    // Gold pack avec un emplacement parmi les brûlables : même exigence.
    rejected(with_mech(|m, t| {
        t.cards[0].backing = None;
        t.cards[3].backing = None;
        m.gold = Some(GoldParams { slots: vec![GoldSlot { floor: Rarity::Common, weights: None, burnable: true }] });
    }), "Brûlable garantie");
}

#[test]
fn borderline_valid_tables_are_accepted() {
    // Juste aux bornes : 50 % de redevances, 10 redevances, 20 mythiques au plafond 100, 10 cartes
    // par pack, valeur au prix maximal qui tient sur u128, n_max = 10 000, plancher 100 %.
    let r = |bps| Royalty { account_id: accounts(3), bps };
    let mut t = with(|t| {
        t.royalties = (0..MAX_ROYALTIES).map(|_| r(500)).collect();
        t.mythics = (0..MAX_MYTHICS_PER_SERIES).map(|i| myth(&i.to_string(), 1, MAX_MYTHIC_CAP)).collect();
        t.rarity_weights.mythic = 1;
        t.cards_per_pack = MAX_CARDS_PER_PACK;
    });
    let v = value();
    // ⌊prix × 30 000 / 10⁴⌋ × 10 (multiplicateur maximal) doit tenir sur u128.
    let max_price = u128::MAX / 30_000;
    t.price = U128(max_price);
    t.mechanics = Some(Mechanics {
        gold: Some(GoldParams { slots: vec![GoldSlot { floor: Rarity::Mythic, weights: None, burnable: false }; 10] }),
        pity: Some(PityParams { p0_ppb: 1_000_000_000, k_ppb: 1_000_000_000, p_max_ppb: 1_000_000_000, n_max: Some(MAX_PITY_N) }),
        burn: Some(BurnParams { floor_bps: 10_000, prior_k: MAX_BURN_PRIOR_K }),
        value: Some(v),
        ..no_mech()
    });
    let mut c = open(t);
    // Achat et tirage au prix maximal : aucune panique, valeur exacte.
    let p = buy_reveal(&mut c, 0);
    let v = c.get_pack(p).unwrap()["value"].clone();
    let total: u128 = v["total"].as_str().unwrap().parse().unwrap();
    assert_eq!(total, draw::value_total(max_price, 30_000), "p = 10⁹ ppb : gold pack, table gold");
}

// ----------------------------------------------------------------- retry_reveal : délai minimal

#[test]
fn retry_delay_below_minimum_is_rejected() {
    // Avant la revue, `new` acceptait 0 : n'importe qui pouvait alors relancer le tirage d'un pack
    // encore en cours, dès l'achat, et le faire passer en `Stuck` (sans remboursement) en 10 appels.
    for d in [0u64, 1, MIN_RETRY_DELAY_BLOCKS - 1] {
        set(owner(), 0, 10, [0; 32]);
        let r = std::panic::catch_unwind(|| Contract::new(owner(), None, None, None, Some(d), None));
        let e = r.err().unwrap_or_else(|| panic!("retry_delay_blocks = {d} accepté"));
        assert!(e.downcast_ref::<String>().unwrap().contains("retry_delay_blocks"));
    }
    set(owner(), 0, 10, [0; 32]);
    let c = Contract::new(owner(), None, None, None, Some(MIN_RETRY_DELAY_BLOCKS), None);
    assert_eq!(c.config.retry_delay_blocks, MIN_RETRY_DELAY_BLOCKS);
}

#[test]
fn third_party_cannot_stall_a_progressing_pack() {
    // Délai minimal : tant que la chaîne de reçus progresse (un reçu par bloc), une relance par un
    // tiers est refusée ; le pack se révèle normalement.
    set(owner(), 0, 10, [0; 32]);
    let mut c = Contract::new(owner(), None, None, None, Some(MIN_RETRY_DELAY_BLOCKS), None);
    let id = c.create_series(base_table());
    c.open_series(id);
    let dep = c.get_series(0).required_deposit.0;
    set(alice(), dep, 100, [0; 32]);
    let p = c.buy_pack(0, None).0 as u64;
    let carol = accounts(3);
    for step in 1..=3u8 {
        set(carol.clone(), 0, 100 + step as u64, [0; 32]);
        let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.retry_reveal(p)));
        assert!(r.is_err(), "relance acceptée au bloc {}", 100 + step as u64);
        set(contract_id(), 0, 100 + step as u64, [step; 32]);
        c.reveal_step(p, 0, step);
    }
    assert_eq!(c.get_pack(p).unwrap()["status"], "revealed");
    assert_eq!(c.get_pack(p).unwrap()["attempt"], 0);
}
