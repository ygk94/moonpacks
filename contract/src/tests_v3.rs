//! Tests unitaires de la version 3 : stockage prépayé rendu au tirage, stockage rendu au burn,
//! remboursement d'un pack `Stuck`, retrait des recettes avec garde-fous.

use crate::types::*;
use crate::*;
use near_sdk::mock::MockAction;
use near_sdk::serde_json::Value;
use near_sdk::test_utils::{accounts, get_created_receipts, get_logs, VMContextBuilder};
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
fn contract_id() -> AccountId {
    "memaster.test".parse().unwrap()
}

fn ctx(pred: AccountId, deposit: u128, height: u64, balance: u128) -> VMContextBuilder {
    let mut b = VMContextBuilder::new();
    b.current_account_id(contract_id())
        .predecessor_account_id(pred.clone())
        .signer_account_id(pred)
        .attached_deposit(NearToken::from_yoctonear(deposit))
        .prepaid_gas(Gas::from_tgas(300))
        .block_height(height)
        .account_balance(NearToken::from_yoctonear(balance));
    b
}

fn set(pred: AccountId, deposit: u128, height: u64) {
    testing_env!(ctx(pred, deposit, height, 1_000 * NEAR).build());
}

fn set_balance(pred: AccountId, deposit: u128, height: u64, balance: u128) {
    testing_env!(ctx(pred, deposit, height, balance).build());
}

fn set_seed(height: u64, seed: [u8; 32]) {
    let mut c = ctx(contract_id(), 0, height, 1_000 * NEAR);
    c.random_seed(seed);
    testing_env!(c.build());
}

fn set_result(result: PromiseResult) {
    testing_env!(
        ctx(contract_id(), 0, 50, 1_000 * NEAR).build(),
        near_sdk::test_vm_config(),
        RuntimeFeesConfig::test(),
        Default::default(),
        vec![result],
    );
}

fn card(id: &str, rarity: Rarity, weight: u32, backing: bool) -> CardDef {
    CardDef {
        card_id: id.to_string(),
        title: id.to_uppercase(),
        rarity,
        weight,
        cap: None,
        media: None,
        reference: None,
        backing: backing.then(|| Backing { asset_id: format!("nep141:{id}.near"), amount: U128(1_000) }),
    }
}

/// Table de 4 cartes, toutes brûlables sauf la rare ; `value` : table de valeur (75 % du prix).
fn table(value: bool) -> SeriesTable {
    let mult = RarityWeights { mythic: 0, legendary: 20, epic: 5, rare: 2, common: 1 };
    SeriesTable {
        name: "V3".into(),
        price: U128(NEAR / 10),
        cards_per_pack: 5,
        rarity_weights: RarityWeights { mythic: 0, legendary: 1, epic: 9, rare: 30, common: 960 },
        cards: vec![
            card("leg", Rarity::Legendary, 1, true),
            card("epic", Rarity::Epic, 1, true),
            card("rare", Rarity::Rare, 1, false),
            card("com", Rarity::Common, 1, true),
        ],
        mythics: vec![],
        royalties: vec![],
        mechanics: value.then(|| Mechanics {
            gold: None,
            pity: None,
            burn: None,
            rush: None,
            resurrection: None,
            value: Some(ValueParams {
                normal: vec![(7_500, 1)],
                gold: vec![(30_000, 1)],
                rush: vec![(9_000, 1)],
                multipliers: mult,
            }),
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

// En test unitaire, le contrat n'est jamais « déposé » entre deux appels : ses écritures restent en
// cache. `flush_all` avant chaque appel mesuré met le stockage simulé à jour, comme sur la chaîne.

fn buy(c: &mut Contract, who: AccountId, height: u64) -> u64 {
    c.flush_all();
    let dep = c.get_series(0).required_deposit.0;
    set(who, dep, height);
    c.buy_pack(0).0 as u64
}

fn reveal(c: &mut Contract, pack_id: u64, seed: u8, height: u64) {
    for step in 1..=3u8 {
        c.flush_all();
        set_seed(height + step as u64, [seed.wrapping_add(step); 32]);
        c.reveal_step(pack_id, 0, step);
    }
}

fn event(name: &str) -> Value {
    let line = get_logs()
        .into_iter()
        .filter_map(|l| l.strip_prefix("EVENT_JSON:").map(str::to_string))
        .find(|l| l.contains(&format!("\"event\":\"{name}\"")))
        .unwrap_or_else(|| panic!("événement {name} absent : {:?}", get_logs()));
    near_sdk::serde_json::from_str::<Value>(&line).unwrap()["data"][0].clone()
}

fn transfers_to(who: &AccountId) -> Vec<u128> {
    get_created_receipts()
        .iter()
        .filter(|r| &r.receiver_id == who)
        .flat_map(|r| r.actions.iter())
        .filter_map(|a| match a {
            MockAction::Transfer { deposit, .. } => Some(deposit.as_yoctonear()),
            _ => None,
        })
        .collect()
}

fn u128_of(v: &Value) -> u128 {
    v.as_str().unwrap().parse().unwrap()
}

fn byte() -> u128 {
    env::storage_byte_cost().as_yoctonear()
}

// ----------------------------------------------------------------- 1. stockage rendu au tirage

#[test]
fn unused_storage_is_refunded_at_final_step() {
    let mut c = contract_with(table(false));
    let prepaid = c.get_series(0).storage_per_pack;
    let price = c.get_series(0).price.0;
    let p = buy(&mut c, alice(), 20);
    let after_buy = c.packs.get(&p).unwrap().storage_used as u64;
    assert!(after_buy > 0, "le stockage de buy_pack est mesuré");
    // Pendant le tirage, l'engagement = prix + prépayé non utilisé.
    assert_eq!(c.pack_escrow, price + byte() * (prepaid - after_buy) as u128);
    c.flush_all();
    set_seed(21, [1; 32]);
    c.reveal_step(p, 0, 1);
    let after_step = c.packs.get(&p).unwrap().storage_used as u64;
    assert!(after_step > after_buy, "la graine d'une étape intermédiaire est comptée");
    c.flush_all();
    set_seed(22, [2; 32]);
    c.reveal_step(p, 0, 2);
    c.flush_all();
    set_seed(23, [3; 32]);
    c.reveal_step(p, 0, 3);
    let ev = event("pack_revealed");
    let used = ev["storage"]["used_bytes"].as_u64().unwrap();
    let refund = u128_of(&ev["storage"]["refund"]);
    assert_eq!(ev["storage"]["prepaid_bytes"].as_u64().unwrap(), prepaid);
    assert_eq!(used, c.packs.get(&p).unwrap().storage_used as u64);
    assert!(used > after_step && used <= prepaid, "utilisé {used} / prépayé {prepaid}");
    assert_eq!(refund, byte() * (prepaid - used) as u128, "rendu = prépayé − utilisé, jamais plus");
    assert!(refund > 0);
    assert_eq!(transfers_to(&alice()), vec![refund], "un seul virement, à l'acheteur");
    assert_eq!(c.pack_escrow, 0, "plus aucun engagement une fois tiré");
    assert_eq!(c.get_pack(p).unwrap()["storage_used"], used);
}

#[test]
fn second_pack_of_same_account_uses_less_storage() {
    let mut c = contract_with(table(false));
    let p0 = buy(&mut c, alice(), 20);
    reveal(&mut c, p0, 1, 20);
    let first = c.packs.get(&p0).unwrap().storage_used as u64;
    let p1 = buy(&mut c, alice(), 40);
    reveal(&mut c, p1, 9, 40);
    let second = c.packs.get(&p1).unwrap().storage_used as u64;
    assert!(second < first, "premier achat {first} o, suivant {second} o (compteurs et blocs déjà créés)");
}

// ----------------------------------------------------------------- 2. stockage rendu au burn

fn first_backed(c: &Contract, who: &AccountId) -> String {
    use near_contract_standards::non_fungible_token::enumeration::NonFungibleTokenEnumeration;
    c.nft_tokens_for_owner(who.clone(), None, None)
        .into_iter()
        .map(|t| t.token_id)
        .find(|t| c.get_backing(t.clone()).is_some())
        .expect("une carte brûlable")
}

fn burn(c: &mut Contract, who: AccountId, tid: &str) -> bool {
    c.flush_all();
    set(who.clone(), 1, 60);
    let b = c.get_backing(tid.to_string()).unwrap();
    let _ = c.redeem(tid.to_string());
    c.flush_all();
    set_result(PromiseResult::Successful(vec![]));
    c.on_redeem_complete(tid.to_string(), who, b)
}

#[test]
fn burn_refunds_freed_storage_to_owner() {
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 4, 20);
    let tid = first_backed(&c, &alice());
    assert!(burn(&mut c, alice(), &tid));
    let ev = event("card_redeemed");
    let freed = ev["freed_bytes"].as_u64().unwrap();
    let refund = u128_of(&ev["storage_refund"]);
    // Deux entrées de 8 o (liste du propriétaire, liste globale) au moins.
    assert!(freed >= 16, "octets libérés : {freed}");
    assert_eq!(refund, byte() * freed as u128);
    assert_eq!(transfers_to(&alice()), vec![refund]);
    // L'emplacement du pack reste : get_pack garde le tirage de la carte brûlée.
    let pack = c.get_pack(p).unwrap();
    assert_eq!(pack["draws"].as_array().unwrap().len(), 5);
}

#[test]
fn burning_last_card_of_account_frees_counters() {
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 4, 20);
    // Alice donne une carte brûlable à Bob, qui n'a rien d'autre : son burn vide sa liste et son compteur.
    use near_contract_standards::non_fungible_token::core::NonFungibleTokenCore;
    let tid = first_backed(&c, &alice());
    c.flush_all();
    set(alice(), 1, 50);
    c.nft_transfer(bob(), tid.clone(), None, None);
    assert!(burn(&mut c, bob(), &tid));
    let freed = event("card_redeemed")["freed_bytes"].as_u64().unwrap();
    // Bloc de liste, compteur de cartes et propriétaire de l'emplacement (le nom de Bob).
    assert!(freed > 100, "octets libérés : {freed}");
}

#[test]
fn burn_with_approvals_never_refunds_more_than_freed() {
    use near_contract_standards::non_fungible_token::approval::NonFungibleTokenApproval;
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 4, 20);
    let tid = first_backed(&c, &alice());
    c.flush_all();
    set(alice(), NEAR / 100, 40);
    let _ = c.nft_approve(tid.clone(), "market.test".parse().unwrap(), None);
    assert!(burn(&mut c, alice(), &tid));
    let ev = event("card_redeemed");
    let freed = ev["freed_bytes"].as_u64().unwrap();
    let total: u128 = transfers_to(&alice()).iter().sum();
    assert_eq!(total, u128_of(&ev["storage_refund"]));
    assert_eq!(total, byte() * freed as u128, "approbations comprises, exactement les octets libérés");
}

// ----------------------------------------------------------------- 3. pack stuck remboursé

fn stuck_pack(c: &mut Contract) -> u64 {
    let p = buy(c, alice(), 20);
    let mut h = 20;
    for _ in 0..MAX_ATTEMPTS {
        h += 200;
        set(bob(), 0, h);
        c.retry_reveal(p);
    }
    assert_eq!(c.get_pack(p).unwrap()["status"], "stuck");
    p
}

#[test]
fn stuck_pack_is_refunded_once_and_never_drawn() {
    let mut c = contract_with(table(false));
    let price = c.get_series(0).price.0;
    let prepaid = c.get_series(0).storage_per_pack;
    let p = stuck_pack(&mut c);
    let used = c.packs.get(&p).unwrap().storage_used as u64;
    let revenue = c.revenue;
    assert_eq!(c.pack_escrow, price + byte() * (prepaid - used) as u128);
    // Par un tiers : l'argent va à l'acheteur.
    set(bob(), 0, 5_000);
    let total = c.refund_stuck_pack(p).0;
    assert_eq!(total, price + byte() * (prepaid - used) as u128);
    assert_eq!(transfers_to(&alice()), vec![total]);
    assert!(transfers_to(&bob()).is_empty());
    let ev = event("pack_refunded");
    assert_eq!(u128_of(&ev["total"]), total);
    assert_eq!(u128_of(&ev["price"]), price);
    assert_eq!(c.get_pack(p).unwrap()["status"], "refunded");
    assert_eq!(c.revenue, revenue - price, "le prix remboursé sort des recettes");
    assert_eq!(c.pack_escrow, 0);
    // Aucun tirage possible ensuite : étape ignorée, relance refusée.
    set_seed(5_001, [7; 32]);
    c.reveal_step(p, MAX_ATTEMPTS - 1, 1);
    c.reveal_step(p, MAX_ATTEMPTS - 1, 3);
    let pack = c.get_pack(p).unwrap();
    assert_eq!(pack["status"], "refunded");
    assert!(pack["token_ids"].as_array().unwrap().is_empty());
    set(bob(), 0, 6_000);
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.retry_reveal(p)));
    assert!(r.is_err(), "relance refusée après remboursement");
}

#[test]
#[should_panic(expected = "Pack déjà remboursé")]
fn stuck_pack_cannot_be_refunded_twice() {
    let mut c = contract_with(table(false));
    let p = stuck_pack(&mut c);
    set(alice(), 0, 5_000);
    c.refund_stuck_pack(p);
    set(alice(), 0, 5_001);
    c.refund_stuck_pack(p);
}

#[test]
#[should_panic(expected = "Seul un pack bloqué")]
fn pending_pack_cannot_be_refunded() {
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    set(alice(), 0, 5_000);
    c.refund_stuck_pack(p);
}

#[test]
#[should_panic(expected = "Seul un pack bloqué")]
fn revealed_pack_cannot_be_refunded() {
    // Pas de tirage gratuit : un pack tiré, bon ou mauvais, n'est jamais remboursable.
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 3, 20);
    set(alice(), 0, 5_000);
    c.refund_stuck_pack(p);
}

#[test]
fn revealed_pack_can_never_become_stuck() {
    // Par construction : `retry_reveal` exige un pack `Pending` sans carte ; un pack tiré reste tiré.
    let mut c = contract_with(table(false));
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 3, 20);
    for k in 0..MAX_ATTEMPTS + 1 {
        set(bob(), 0, 1_000 + 200 * k as u64);
        let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.retry_reveal(p)));
        assert!(r.is_err());
    }
    assert_eq!(c.get_pack(p).unwrap()["status"], "revealed");
}

// ----------------------------------------------------------------- 4. retrait des recettes

fn treasury(c: &Contract) -> Value {
    c.get_treasury()
}

#[test]
fn withdraw_never_goes_below_commitments() {
    let mut c = contract_with(table(true));
    // Un pack tiré (valeur réservée), un pack en attente (engagement), une annonce (dépôt).
    let p0 = buy(&mut c, alice(), 20);
    reveal(&mut c, p0, 5, 20);
    assert!(c.value_reserved > 0, "valeur des brûlables réservée");
    let _p1 = buy(&mut c, bob(), 40);
    assert!(c.pack_escrow > 0);
    let tid = first_backed(&c, &alice());
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 50);
    c.list(tid, U128(NEAR));
    assert_eq!(c.listing_deposits, LISTING_DEPOSIT.as_yoctonear());

    // Solde fixé à engagements + 3 yocto : 3 yocto retirables, pas un de plus.
    set(owner(), 1, 60);
    let t = treasury(&c);
    let committed = u128_of(&t["committed"]);
    let expected = u128_of(&t["storage_locked"])
        + c.listing_deposits
        + c.pack_escrow
        + c.value_reserved
        + TREASURY_MIN_RESERVE.as_yoctonear();
    assert_eq!(committed, expected);
    // (Le solde vu par le contrat comprend le yocto joint.)
    set_balance(owner(), 1, 60, committed + 2);
    let balance = env::account_balance().as_yoctonear();
    let w = u128_of(&treasury(&c)["withdrawable"]);
    assert_eq!(w, balance - committed);
    assert!(w > 0 && w <= 3);
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.withdraw_revenue(Some(U128(w + 1)))));
    assert!(r.is_err(), "un yocto de plus : sous les engagements");
    set_balance(owner(), 1, 60, committed + 2);
    assert_eq!(c.withdraw_revenue(None).0, w);
    assert_eq!(transfers_to(&owner()), vec![w]);
    assert_eq!(u128_of(&event("revenue_withdrawn")["amount"]), w);
    assert_eq!(c.withdrawn, w);
    // Le virement est déjà déduit du solde vu par le contrat.
    assert_eq!(env::account_balance().as_yoctonear(), balance - w);
    assert!(env::account_balance().as_yoctonear() >= committed, "solde après retrait ≥ engagements");
    // Solde sous les engagements : rien.
    set_balance(owner(), 1, 61, committed - 1);
    assert_eq!(u128_of(&treasury(&c)["withdrawable"]), 0);
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| c.withdraw_revenue(None)));
    assert!(r.is_err());
}

#[test]
fn commitments_follow_reveal_burn_and_delist() {
    let mut c = contract_with(table(true));
    let price = c.get_series(0).price.0;
    let p = buy(&mut c, alice(), 20);
    reveal(&mut c, p, 5, 20);
    assert_eq!(c.pack_escrow, 0);
    let total_value = u128_of(&c.get_pack(p).unwrap()["value"]["total"]);
    assert_eq!(c.value_reserved, total_value, "toute la valeur va aux brûlables (75 % du prix)");
    assert_eq!(total_value, price * 3 / 4);
    let tid = first_backed(&c, &alice());
    let share = c.get_backing(tid.clone()).unwrap().amount.0;
    set(alice(), LISTING_DEPOSIT.as_yoctonear(), 30);
    c.list(tid.clone(), U128(NEAR));
    set(alice(), 0, 31);
    c.delist(tid.clone());
    assert_eq!(c.listing_deposits, 0);
    assert!(burn(&mut c, alice(), &tid));
    assert_eq!(c.value_reserved, total_value - share, "la part brûlée n'est plus réservée");
}

#[test]
#[should_panic(expected = "Réservé à l'owner")]
fn only_owner_withdraws() {
    let mut c = contract_with(table(false));
    set(alice(), 1, 20);
    c.withdraw_revenue(Some(U128(1)));
}

#[test]
#[should_panic(expected = "exactly 1 yoctoNEAR")]
fn withdraw_requires_one_yocto() {
    let mut c = contract_with(table(false));
    set(owner(), 0, 20);
    c.withdraw_revenue(Some(U128(1)));
}
