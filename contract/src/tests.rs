//! Tests unitaires (environnement simulé de near-sdk).

use crate::draw;
use crate::types::*;
use crate::*;
use near_contract_standards::non_fungible_token::core::NonFungibleTokenCore;
use near_contract_standards::non_fungible_token::enumeration::NonFungibleTokenEnumeration;
use near_sdk::test_utils::{accounts, VMContextBuilder};
use near_sdk::{testing_env, PromiseResult, RuntimeFeesConfig};

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
fn redeemer() -> AccountId {
    "redeemer.test".parse().unwrap()
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

fn set_seed(pred: AccountId, height: u64, seed: [u8; 32]) {
    let mut c = ctx(pred, 0, height);
    c.random_seed(seed);
    testing_env!(c.build());
}

fn set_with_result(pred: AccountId, result: PromiseResult) {
    testing_env!(
        ctx(pred, 0, 50).build(),
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

fn mythic_content() -> MythicContent {
    MythicContent {
        title: "SECRET".to_string(),
        media: None,
        reference: None,
        backing: Some(Backing { asset_id: "nep141:secret.near".to_string(), amount: U128(42) }),
    }
}

const SEL: &str = "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff";

fn table() -> SeriesTable {
    let sel = hex_decode(SEL).unwrap();
    let (c, h) = crate::mythic::compute_commitments("secret", &sel, &mythic_content());
    SeriesTable {
        name: "Serie 1".to_string(),
        price: U128(NEAR),
        cards_per_pack: 5,
        rarity_weights: RarityWeights { mythic: 10, legendary: 40, epic: 150, rare: 300, common: 500 },
        cards: vec![
            card("leg", Rarity::Legendary, 1, Some(2), true),
            card("epic", Rarity::Epic, 1, None, true),
            card("rare", Rarity::Rare, 1, None, false),
            card("common_a", Rarity::Common, 3, None, true),
            card("common_b", Rarity::Common, 1, Some(5), false),
        ],
        mythics: vec![MythicCommitment {
            commitment: hex32(&c),
            content_hash: hex32(&h),
            weight: 1,
            cap: 3,
        }],
        royalties: vec![Royalty { account_id: owner(), bps: 500 }],
        mechanics: None,
    }
}

fn setup() -> Contract {
    set(owner(), 0, 10);
    let mut c = Contract::new(owner(), Some(redeemer()), None, None, Some(100));
    let id = c.create_series(table());
    c.open_series(id);
    c
}

fn required(c: &Contract) -> u128 {
    c.get_series(0).required_deposit.0
}

/// Achète et déroule le tirage complet (k = 3) ; renvoie le pack.
fn buy_and_reveal(c: &mut Contract, buyer: AccountId, seed_byte: u8) -> u64 {
    let dep = required(c);
    set(buyer, dep, 20);
    let pack_id = c.buy_pack(0).0 as u64;
    for step in 1..=3u8 {
        set_seed(contract_id(), 20 + step as u64, [seed_byte.wrapping_add(step); 32]);
        let attempt = 0;
        c.reveal_step(pack_id, attempt, step);
    }
    pack_id
}

// ----------------------------------------------------------------- séries

#[test]
#[should_panic(expected = "commune sans plafond")]
fn table_without_unlimited_common_is_rejected() {
    set(owner(), 0, 1);
    let mut c = Contract::new(owner(), None, None, None, None);
    let mut t = table();
    for x in t.cards.iter_mut() {
        if x.rarity == Rarity::Common {
            x.cap = Some(10);
        }
    }
    c.create_series(t);
}

#[test]
#[should_panic(expected = "engagements")]
fn visible_mythic_card_is_rejected() {
    set(owner(), 0, 1);
    let mut c = Contract::new(owner(), None, None, None, None);
    let mut t = table();
    t.cards[0].rarity = Rarity::Mythic;
    c.create_series(t);
}

#[test]
#[should_panic(expected = "Réservé à l'owner")]
fn only_owner_creates_series() {
    set(owner(), 0, 1);
    let mut c = Contract::new(owner(), None, None, None, None);
    set(alice(), 0, 1);
    c.create_series(table());
}

#[test]
fn table_hash_is_sha256_of_view_json() {
    let c = setup();
    let t = c.get_series_table(0);
    let bytes = near_sdk::serde_json::to_vec(&t).unwrap();
    let h = hex32(&env::sha256_array(&bytes));
    assert_eq!(c.get_series(0).table_hash.unwrap(), h);
    let v = c.get_series_table_hash(0);
    assert_eq!(v["stored"].as_str(), Some(h.as_str()), "hash enregistré, pas recalculé");
}

#[test]
#[should_panic(expected = "Table figée")]
fn open_table_cannot_be_replaced() {
    let mut c = setup();
    set(owner(), 0, 11);
    c.replace_series_table(0, table());
}

#[test]
#[should_panic(expected = "Série non ouverte")]
fn paused_series_refuses_sales() {
    let mut c = setup();
    set(owner(), 0, 11);
    c.pause_series(0);
    let dep = required(&c);
    set(alice(), dep, 12);
    c.buy_pack(0);
}

// ----------------------------------------------------------------- achat

#[test]
#[should_panic(expected = "Dépôt insuffisant")]
fn insufficient_deposit_is_rejected() {
    let mut c = setup();
    let dep = required(&c);
    set(alice(), dep - 1, 12);
    c.buy_pack(0);
}

#[test]
#[should_panic(expected = "Gaz insuffisant")]
fn insufficient_gas_is_rejected() {
    let mut c = setup();
    let dep = required(&c);
    let mut b = ctx(alice(), dep, 12);
    b.prepaid_gas(Gas::from_tgas(100));
    testing_env!(b.build());
    c.buy_pack(0);
}

#[test]
fn full_reveal_mints_cards_and_fills_backing_registry() {
    let mut c = setup();
    let pack_id = buy_and_reveal(&mut c, alice(), 7);
    let p = c.get_pack(pack_id).unwrap();
    assert_eq!(p["status"], "revealed");
    let ids: Vec<String> = near_sdk::serde_json::from_value(p["token_ids"].clone()).unwrap();
    assert_eq!(ids.len(), 5);
    assert_eq!(p["seeds"].as_array().unwrap().len(), 3);
    assert_eq!(c.nft_supply_for_owner_internal(&alice()), 5);
    for id in ids {
        let card = c.get_card(id.clone()).unwrap();
        assert_eq!(card.owner_id, alice());
        if card.kind == CardKind::Visible {
            let def = &table().cards[card.index as usize];
            assert_eq!(c.get_backing(id), def.backing);
        }
    }
}

#[test]
fn stale_or_out_of_order_steps_are_ignored() {
    let mut c = setup();
    let dep = required(&c);
    set(alice(), dep, 20);
    let pack_id = c.buy_pack(0).0 as u64;
    set_seed(contract_id(), 21, [1; 32]);
    c.reveal_step(pack_id, 0, 2); // hors ordre
    c.reveal_step(pack_id, 5, 1); // mauvaise tentative
    assert_eq!(c.get_pack(pack_id).unwrap()["step"], 0);
    c.reveal_step(pack_id, 0, 1);
    assert_eq!(c.get_pack(pack_id).unwrap()["step"], 1);
}

#[test]
fn retry_reveal_rules() {
    let mut c = setup();
    let dep = required(&c);
    set(alice(), dep, 20);
    let pack_id = c.buy_pack(0).0 as u64;
    set_seed(contract_id(), 21, [1; 32]);
    c.reveal_step(pack_id, 0, 1);

    // après le délai, par n'importe qui
    set(bob(), 0, 200);
    c.retry_reveal(pack_id);
    let p = c.get_pack(pack_id).unwrap();
    assert_eq!(p["attempt"], 1);
    assert_eq!(p["step"], 0);
    // l'ancienne chaîne est périmée
    set_seed(contract_id(), 201, [2; 32]);
    c.reveal_step(pack_id, 0, 2);
    assert_eq!(c.get_pack(pack_id).unwrap()["step"], 0);
    for s in 1..=3u8 {
        set_seed(contract_id(), 201 + s as u64, [9 + s; 32]);
        c.reveal_step(pack_id, 1, s);
    }
    assert_eq!(c.get_pack(pack_id).unwrap()["status"], "revealed");
}

#[test]
#[should_panic(expected = "Délai de relance non écoulé")]
fn retry_before_delay_is_forbidden() {
    let mut c = setup();
    let dep = required(&c);
    set(alice(), dep, 20);
    let pack_id = c.buy_pack(0).0 as u64;
    set(bob(), 0, 60);
    c.retry_reveal(pack_id);
}

#[test]
#[should_panic(expected = "relance interdite")]
fn retry_after_reveal_is_forbidden() {
    let mut c = setup();
    let pack_id = buy_and_reveal(&mut c, alice(), 3);
    set(bob(), 0, 10_000);
    c.retry_reveal(pack_id);
}

// ----------------------------------------------------------------- tirage

#[test]
fn draw_is_deterministic() {
    let t = table();
    let acc = [5u8; 32];
    let a = draw::draw_slot(&t, &[0; 5], &[0], &acc, 0);
    let b = draw::draw_slot(&t, &[0; 5], &[0], &acc, 0);
    assert_eq!(a, b);
}

#[test]
fn capped_rarity_falls_to_lower() {
    let t = table();
    // légendaire et mythique au plafond
    let minted = [2, 0, 0, 0, 0];
    let mythic = [3];
    for i in 0..2000u32 {
        let acc = env::sha256_array(&i.to_le_bytes());
        let d = draw::draw_slot(&t, &minted, &mythic, &acc, 0);
        assert!(d.final_rarity >= Rarity::Epic, "{:?}", d);
        if d.rolled_rarity == Rarity::Legendary || d.rolled_rarity == Rarity::Mythic {
            assert_eq!(d.final_rarity, Rarity::Epic);
        }
    }
}

#[test]
fn capped_card_is_skipped_within_rarity() {
    let t = table();
    let minted = [0, 0, 0, 0, 5]; // common_b au plafond
    for i in 0..2000u32 {
        let acc = env::sha256_array(&i.to_le_bytes());
        let d = draw::draw_slot(&t, &minted, &[0], &acc, 1);
        assert!(!(d.kind == CardKind::Visible && d.index == 4));
    }
}

#[test]
fn draw_frequencies_match_weights() {
    let t = table();
    let n = 20_000u32;
    let mut counts = [0u32; 5];
    for i in 0..n {
        if i % 1000 == 0 {
            set(owner(), 0, 1); // remet le compteur de gaz simulé à zéro
        }
        let acc = env::sha256_array(&i.to_le_bytes());
        let d = draw::draw_slot(&t, &[0; 5], &[0], &acc, 0);
        counts[d.rolled_rarity.index()] += 1;
    }
    let expected = [10.0, 40.0, 150.0, 300.0, 500.0];
    for r in 0..5 {
        let e = expected[r] / 1000.0 * n as f64;
        let sd = (e * (1.0 - expected[r] / 1000.0)).sqrt();
        assert!((counts[r] as f64 - e).abs() < 5.0 * sd, "rareté {r}: {} vs {e}", counts[r]);
    }
}

// ----------------------------------------------------------------- mythiques

#[test]
fn commitment_helper_matches_table() {
    let c = setup();
    let v = c.compute_mythic_commitment("secret".into(), SEL.into(), mythic_content());
    let m = &c.get_mythic_commitments(0)[0];
    assert_eq!(v.commitment, m.commitment);
    assert_eq!(v.content_hash, m.content_hash);
}

/// Force une mythique scellée par écriture directe (le tirage réel est couvert en sandbox).
fn mint_sealed(c: &mut Contract) -> String {
    let mut s = c.series_ref(0).clone();
    s.mythic_minted[0] += 1;
    let pid = c.next_pack_id;
    c.next_pack_id += 1;
    s.sealed_tokens[0].push(token_id_of(pid, 0));
    *c.series.get_mut(0).unwrap() = s;
    c.packs.insert(
        pid,
        Pack {
            series_id: 0,
            owner_id: alice(),
            bought_at_height: 0,
            status: PackStatus::Revealed,
            attempt: 0,
            step: 3,
            acc: [0; 32],
            seeds: vec![],
            last_progress_height: 0,
            revealed_at_ms: 0,
            flags: 0,
            draws: vec![PackDraw {
                rarity_roll: 0,
                rolled_rarity: Rarity::Mythic,
                final_rarity: Rarity::Mythic,
                card_roll: 0,
                kind: CardKind::Mythic,
                index: 0,
            }],
            cards: vec![],
        },
    );
    c.internal_mint_slot(pid, &alice())
}

#[test]
fn mythic_reveal_verifies_and_updates_sealed_cards() {
    let mut c = setup();
    let tid = mint_sealed(&mut c);
    assert!(c.get_card(tid.clone()).unwrap().sealed);
    assert!(c.get_backing(tid.clone()).is_none());
    set(owner(), NEAR, 30);
    c.reveal_mythic(0, 0, "secret".into(), SEL.into(), mythic_content());
    let card = c.get_card(tid.clone()).unwrap();
    assert!(!card.sealed);
    assert_eq!(card.card_id.as_deref(), Some("secret"));
    assert_eq!(c.get_backing(tid.clone()).unwrap().amount, U128(42));
    let tok = c.nft_token(tid).unwrap();
    assert_eq!(tok.metadata.unwrap().title.as_deref(), Some("SECRET"));
}

#[test]
#[should_panic(expected = "engagement")]
fn mythic_reveal_with_wrong_sel_fails() {
    let mut c = setup();
    mint_sealed(&mut c);
    set(owner(), NEAR, 30);
    c.reveal_mythic(0, 0, "secret".into(), "ff".repeat(32), mythic_content());
}

#[test]
#[should_panic(expected = "content_hash")]
fn mythic_reveal_with_altered_backing_fails() {
    let mut c = setup();
    mint_sealed(&mut c);
    set(owner(), NEAR, 30);
    let mut content = mythic_content();
    content.backing.as_mut().unwrap().amount = U128(4_200_000);
    c.reveal_mythic(0, 0, "secret".into(), SEL.into(), content);
}

#[test]
#[should_panic(expected = "jamais sortie")]
fn undrawn_mythic_cannot_be_revealed() {
    let mut c = setup();
    set(owner(), NEAR, 30);
    c.reveal_mythic(0, 0, "secret".into(), SEL.into(), mythic_content());
}

// ----------------------------------------------------------------- marché et burn

fn first_backed_token(c: &Contract, owner: &AccountId) -> Option<String> {
    c.nft_tokens_for_owner(owner.clone(), None, None)
        .into_iter()
        .map(|t| t.token_id)
        .find(|t| c.get_backing(t.clone()).is_some())
}

fn pack_with_backed_card(c: &mut Contract) -> String {
    for seed in 0..50u8 {
        buy_and_reveal(c, alice(), seed);
        if let Some(t) = first_backed_token(c, &alice()) {
            return t;
        }
    }
    panic!("pas de carte adossée");
}

#[test]
fn market_list_buy_with_royalties() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 40);
    c.list(tid.clone(), U128(10 * NEAR));
    assert!(c.get_listing(tid.clone()).is_some());
    set(bob(), 10 * NEAR, 41);
    c.buy(tid.clone(), U128(10 * NEAR));
    assert_eq!(c.get_card(tid.clone()).unwrap().owner_id, bob());
    assert!(c.get_listing(tid.clone()).is_none());
    let p = c.nft_payout(tid, U128(10_000), None);
    assert_eq!(p.payout.get(&owner()).unwrap().0, 500);
    assert_eq!(p.payout.get(&bob()).unwrap().0, 9_500);
}

#[test]
fn transfer_removes_listing() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 40);
    c.list(tid.clone(), U128(NEAR));
    set(alice(), 1, 41);
    c.nft_transfer(bob(), tid.clone(), None, None);
    assert!(c.get_listing(tid).is_none());
}

#[test]
fn redeem_success_burns_card() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    let supply = c.nft_supply_for_owner_internal(&alice());
    set(alice(), 1, 40);
    let _ = c.redeem(tid.clone());
    assert_eq!(c.get_card(tid.clone()).unwrap().state, CardState::Redeeming);
    set_with_result(contract_id(), PromiseResult::Successful(b"true".to_vec()));
    assert!(c.on_redeem_complete(tid.clone(), alice()));
    assert!(c.get_card(tid.clone()).is_none());
    assert!(c.get_backing(tid.clone()).is_none());
    assert!(c.nft_token(tid).is_none());
    assert_eq!(c.nft_supply_for_owner_internal(&alice()), supply - 1);
}

#[test]
fn redeem_failure_restores_card() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), 1, 40);
    let _ = c.redeem(tid.clone());
    set_with_result(contract_id(), PromiseResult::Failed);
    assert!(!c.on_redeem_complete(tid.clone(), alice()));
    assert_eq!(c.get_card(tid.clone()).unwrap().state, CardState::Normal);
    assert!(c.get_backing(tid).is_some());
}

fn redeeming_card() -> (Contract, String) {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), 1, 40);
    let _ = c.redeem(tid.clone());
    (c, tid)
}

#[test]
#[should_panic(expected = "burn")]
fn redeeming_card_cannot_be_listed() {
    let (mut c, tid) = redeeming_card();
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 41);
    c.list(tid, U128(NEAR));
}

#[test]
#[should_panic(expected = "burn")]
fn redeeming_card_cannot_be_transferred() {
    let (mut c, tid) = redeeming_card();
    set(alice(), 1, 41);
    c.nft_transfer(bob(), tid, None, None);
}

#[test]
#[should_panic(expected = "Burn déjà en cours")]
fn redeeming_card_cannot_be_redeemed_twice() {
    let (mut c, tid) = redeeming_card();
    set(alice(), 1, 41);
    let _ = c.redeem(tid);
}

#[test]
#[should_panic(expected = "en vente")]
fn listed_card_cannot_be_redeemed() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 40);
    c.list(tid.clone(), U128(NEAR));
    set(alice(), 1, 41);
    let _ = c.redeem(tid);
}

#[test]
#[should_panic(expected = "Le prix de l'annonce a changé")]
fn buy_with_stale_price_fails() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 40);
    c.list(tid.clone(), U128(2 * NEAR));
    set(bob(), 2 * NEAR, 41);
    c.buy(tid, U128(NEAR));
}

#[test]
#[should_panic(expected = "Poids mythique sans engagement de poids non nul")]
fn mythic_weight_needs_a_weighted_commitment() {
    set(owner(), 0, 1);
    let mut c = Contract::new(owner(), None, None, None, None);
    let mut t = table();
    t.mythics[0].weight = 0;
    c.create_series(t);
}

#[test]
#[should_panic(expected = "content_hash en double")]
fn duplicate_content_hash_is_rejected() {
    set(owner(), 0, 1);
    let mut c = Contract::new(owner(), None, None, None, None);
    let mut t = table();
    let sel = hex_decode(SEL).unwrap();
    let (c2, _) = crate::mythic::compute_commitments("autre", &sel, &mythic_content());
    let mut m = t.mythics[0].clone();
    m.commitment = hex32(&c2);
    t.mythics.push(m);
    c.create_series(t);
}

#[test]
#[should_panic(expected = "32 octets")]
fn short_sel_is_rejected() {
    let mut c = setup();
    mint_sealed(&mut c);
    set(owner(), NEAR, 30);
    c.reveal_mythic(0, 0, "secret".into(), "0011".into(), mythic_content());
}

#[test]
fn pack_becomes_stuck_after_max_attempts() {
    let mut c = setup();
    let dep = required(&c);
    set(alice(), dep, 20);
    let pack_id = c.buy_pack(0).0 as u64;
    let mut h = 20;
    for _ in 1..MAX_ATTEMPTS {
        h += 200;
        set(bob(), 0, h);
        c.retry_reveal(pack_id); // les chaînes programmées ne s'exécutent pas en test unitaire
    }
    assert_eq!(c.get_pack(pack_id).unwrap()["attempt"], MAX_ATTEMPTS - 1);
    h += 200;
    set(bob(), 0, h);
    c.retry_reveal(pack_id);
    let p = c.get_pack(pack_id).unwrap();
    assert_eq!(p["status"], "stuck");
    assert!(near_sdk::test_utils::get_logs().iter().any(|l| l.contains("pack_stuck")));
    // plus aucune issue : ni relance, ni étape
    set_seed(contract_id(), h + 1, [1; 32]);
    c.reveal_step(pack_id, MAX_ATTEMPTS - 1, 1);
    assert_eq!(c.get_pack(pack_id).unwrap()["status"], "stuck");
}

#[test]
fn packs_by_owner_is_paginated() {
    let mut c = setup();
    for i in 0..7u8 {
        buy_and_reveal(&mut c, alice(), i);
    }
    buy_and_reveal(&mut c, bob(), 99);
    assert_eq!(c.get_pack_count_for_owner(alice()), 7);
    assert_eq!(c.get_packs_for_owner(alice(), None, Some(3)), vec![0, 1, 2]);
    assert_eq!(c.get_packs_for_owner(alice(), Some(5), Some(10)), vec![5, 6]);
    assert_eq!(c.get_packs_for_owner(alice(), Some(9), None), Vec::<u64>::new());
    assert_eq!(c.get_packs_for_owner(bob(), None, None), vec![7]);
}

fn transfer_called_to_bob(c: &mut Contract, tid: &str) {
    set(alice(), 1, 40);
    let _ = c.nft_transfer_call(bob(), tid.to_string(), None, None, "x".into());
    set(bob(), LISTING_DEPOSIT.as_yoctonear(), 41);
    c.list(tid.to_string(), U128(NEAR)); // le destinataire met en vente pendant le transfert
}

#[test]
fn resolve_keeps_listing_when_receiver_keeps_card() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    transfer_called_to_bob(&mut c, &tid);
    set_with_result(contract_id(), PromiseResult::Successful(b"false".to_vec()));
    use near_contract_standards::non_fungible_token::core::NonFungibleTokenResolver;
    assert!(c.nft_resolve_transfer(alice(), bob(), tid.clone(), Some(Default::default())));
    assert_eq!(c.get_card(tid.clone()).unwrap().owner_id, bob());
    assert_eq!(c.get_listing(tid).unwrap().seller_id, bob());
}

#[test]
fn resolve_removes_listing_only_on_real_return() {
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    transfer_called_to_bob(&mut c, &tid);
    set_with_result(contract_id(), PromiseResult::Successful(b"true".to_vec()));
    use near_contract_standards::non_fungible_token::core::NonFungibleTokenResolver;
    assert!(!c.nft_resolve_transfer(alice(), bob(), tid.clone(), Some(Default::default())));
    assert_eq!(c.get_card(tid.clone()).unwrap().owner_id, alice());
    assert!(c.get_listing(tid).is_none());
}

/// Un virement de exactement le stockage d'une approbation de `market.test` (11 + 4 + 8 octets).
fn has_transfer_to(who: &AccountId) -> bool {
    let expected = env::storage_byte_cost().as_yoctonear() * (11 + 4 + 8);
    near_sdk::test_utils::get_created_receipts().iter().any(|r| {
        &r.receiver_id == who
            && r.actions.iter().any(|a| {
                matches!(a, near_sdk::mock::MockAction::Transfer { deposit, .. } if deposit.as_yoctonear() == expected)
            })
    })
}

#[test]
fn approvals_storage_is_refunded_on_transfer_sale_and_burn() {
    use near_contract_standards::non_fungible_token::approval::NonFungibleTokenApproval;
    let mut c = setup();
    let tid = pack_with_backed_card(&mut c);
    let approve = |c: &mut Contract, owner: AccountId, tid: &str| {
        set(owner, NEAR / 100, 40);
        let _ = c.nft_approve(tid.to_string(), "market.test".parse().unwrap(), None);
    };
    // transfert
    approve(&mut c, alice(), &tid);
    set(alice(), 1, 41);
    c.nft_transfer(bob(), tid.clone(), None, None);
    assert!(has_transfer_to(&alice()), "remboursement des approbations au transfert");
    // vente sur le marché intégré
    approve(&mut c, bob(), &tid);
    set(bob(), LISTING_DEPOSIT.as_yoctonear(), 42);
    c.list(tid.clone(), U128(NEAR));
    set(alice(), NEAR, 43);
    c.buy(tid.clone(), U128(NEAR));
    assert!(has_transfer_to(&bob()));
    // burn
    approve(&mut c, alice(), &tid);
    set(alice(), 1, 44);
    let _ = c.redeem(tid.clone());
    set_with_result(contract_id(), PromiseResult::Successful(vec![]));
    assert!(c.on_redeem_complete(tid, alice()));
    assert!(has_transfer_to(&alice()), "remboursement des approbations au burn");
}

#[test]
fn gen_mythics_script_matches_contract_hashes() {
    set(owner(), 0, 1);
    let root = env!("CARGO_MANIFEST_DIR");
    let dir = std::env::temp_dir().join(format!("memaster-gen-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let public = dir.join("public.json");
    let secrets = dir.join("secrets").join("s.json");
    let out = std::process::Command::new("python3")
        .arg("-I")
        .arg(format!("{root}/scripts/gen_mythics.py"))
        .arg(format!("{root}/scripts/example-mythics.json"))
        .arg(&public)
        .arg(&secrets)
        .output()
        .expect("python3 requis pour ce test");
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
    let pubs: Vec<MythicCommitment> = near_sdk::serde_json::from_slice(&std::fs::read(&public).unwrap()).unwrap();
    let secs: Vec<near_sdk::serde_json::Value> = near_sdk::serde_json::from_slice(&std::fs::read(&secrets).unwrap()).unwrap();
    assert_eq!(pubs.len(), 2);
    assert_ne!(secs[0]["sel"], secs[1]["sel"], "un sel par mythique");
    for (p, s) in pubs.iter().zip(&secs) {
        let sel = hex_decode(s["sel"].as_str().unwrap()).unwrap();
        assert_eq!(sel.len(), 32);
        let content: MythicContent = near_sdk::serde_json::from_value(s["content"].clone()).unwrap();
        let (cm, ch) = crate::mythic::compute_commitments(s["card_id"].as_str().unwrap(), &sel, &content);
        assert_eq!(hex32(&cm), p.commitment);
        assert_eq!(hex32(&ch), p.content_hash);
    }
    std::fs::remove_dir_all(&dir).ok();
}

impl Contract {
    fn nft_supply_for_owner_internal(&self, a: &AccountId) -> u64 {
        self.owner_token_count.get(a).copied().unwrap_or(0) as u64
    }
}
