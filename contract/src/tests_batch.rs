//! Tests unitaires du chargement par lots (`create_series_batched`, `append_series_cards`) et
//! du rangement des cartes par blocs. Le hash et le tirage doivent être identiques à ceux d'une
//! table chargée d'un coup.

use crate::draw;
use crate::types::*;
use crate::*;
use near_sdk::serde_json::{self, Value};
use near_sdk::test_utils::{accounts, VMContextBuilder};
use near_sdk::testing_env;
use near_contract_standards::non_fungible_token::core::NonFungibleTokenCore;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;
/// Dépôt joint aux appels de chargement par lots (l'excédent est rendu).
const LOAD_DEPOSIT: u128 = 1_000 * NEAR;

fn owner() -> AccountId {
    accounts(0)
}
fn alice() -> AccountId {
    accounts(1)
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
        .account_balance(NearToken::from_near(10_000));
    b
}

/// Nouveau contexte d'appel. `storage_usage` est reporté d'un appel à l'autre (comme sur la
/// chaîne) : sans cela, le simulateur le remet à sa valeur par défaut à chaque `testing_env!`.
fn set(pred: AccountId, deposit: u128, height: u64) {
    let mut b = ctx(pred, deposit, height);
    b.storage_usage(env::storage_usage());
    testing_env!(b.build());
}

fn set_seed(pred: AccountId, height: u64, seed: [u8; 32]) {
    let mut c = ctx(pred, 0, height);
    c.random_seed(seed);
    testing_env!(c.build());
}

/// Table pseudo-aléatoire de `n` cartes (plafonds, poids nuls, adossements variés).
fn big_table(n: usize) -> SeriesTable {
    let rarities = [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common];
    let cards = (0..n)
        .map(|i| {
            let h = env::sha256_array(&(i as u64).to_le_bytes());
            let rarity = rarities[(h[0] % 4) as usize];
            CardDef {
                card_id: format!("carte-{i:04}"),
                title: format!("Carte « {i} »"),
                rarity,
                weight: 1 + (h[1] % 5) as u32,
                cap: if rarity == Rarity::Common && h[2] % 2 == 0 { None } else { Some(1 + (h[3] % 3) as u32) },
                media: Some(format!("ipfs://TODO/carte-{i:04}.svg")),
                reference: None,
                backing: (h[4] % 3 == 0).then(|| Backing { asset_id: format!("nep141:c{i}.near"), amount: U128(h[5] as u128 + 1) }),
            }
        })
        .collect();
    SeriesTable {
        name: "Grosse série".into(),
        price: U128(NEAR / 10),
        cards_per_pack: 10,
        rarity_weights: RarityWeights { mythic: 0, legendary: 30, epic: 120, rare: 300, common: 550 },
        cards,
        mythics: vec![],
        royalties: vec![],
        mechanics: None,
    }
}

fn new_contract() -> Contract {
    set(owner(), 0, 10);
    Contract::new(owner(), None, None, None, Some(100), None)
}

/// Charge `t` par lots de `lot` cartes ; renvoie l'identifiant de série.
fn load_batched(c: &mut Contract, t: &SeriesTable, lot: usize) -> u32 {
    set(owner(), LOAD_DEPOSIT, 10);
    let mut first = t.clone();
    first.cards = t.cards[..lot.min(t.cards.len())].to_vec();
    let id = c.create_series_batched(first);
    for chunk in t.cards[lot.min(t.cards.len())..].chunks(lot) {
        set(owner(), LOAD_DEPOSIT, 10);
        c.append_series_cards(id, chunk.to_vec());
    }
    id
}

fn buy_and_reveal(c: &mut Contract, series_id: u32, seed_byte: u8, height: u64) -> Vec<DrawRecord> {
    let dep = c.get_series(series_id).required_deposit.0;
    set(alice(), dep, height);
    let pack_id = c.buy_pack(series_id).0 as u64;
    for step in 1..=3u8 {
        set_seed(contract_id(), height + step as u64, [seed_byte.wrapping_add(step); 32]);
        c.reveal_step(pack_id, 0, step);
    }
    serde_json::from_value(c.get_pack(pack_id).unwrap()["draws"].clone()).unwrap()
}

#[test]
fn batched_load_gives_same_table_hash_and_draws() {
    let t = big_table(180);
    // Une seule fois (180 ≤ 200 cartes par appel) ...
    let mut c = new_contract();
    let ia = c.create_series(t.clone());
    let ha = c.open_series(ia);
    // ... et par lots de 37 (les lots ne tombent pas sur les blocs de 50).
    let ib = load_batched(&mut c, &t, 37);
    set(owner(), 0, 10);
    let hb = c.open_series(ib);
    assert_eq!(ha, hb);
    let expected = hex32(&env::sha256_array(&serde_json::to_vec(&t).unwrap()));
    assert_eq!(ha, expected, "hash = sha256 de la table d'origine");
    for id in [ia, ib] {
        assert_eq!(serde_json::to_vec(&c.get_series_table(id)).unwrap(), serde_json::to_vec(&t).unwrap());
    }
    assert_eq!(c.get_series(ib).card_count, 180);
    assert_eq!(c.get_series_table_hash(ib)["stored"], Value::String(expected));
    assert_eq!(c.get_series(ia).storage_per_pack, c.get_series(ib).storage_per_pack);
    // Pages de cartes = cartes de la table.
    let mut pages = vec![];
    let mut from = 0;
    loop {
        let p = c.get_series_cards(ib, Some(from), Some(64));
        if p.is_empty() {
            break;
        }
        from += p.len() as u32;
        pages.extend(p);
    }
    assert_eq!(pages, t.cards);

    // Chaque tirage du contrat = tirage de référence sur la table complète, avec les plafonds.
    for id in [ia, ib] {
        let mut minted = vec![0u32; 180];
        for k in 0..30u8 {
            let draws = buy_and_reveal(&mut c, id, k, 20 + 10 * k as u64);
            let pack_id = c.get_config()["next_pack_id"].as_u64().unwrap() - 1;
            let acc = c.packs.get(&pack_id).unwrap().acc;
            for d in &draws {
                let r = draw::draw_slot(&t, &minted, &[], &acc, d.slot);
                assert_eq!((r.kind, r.index, r.final_rarity, r.card_roll), (d.kind, d.index, d.final_rarity, d.card_roll.0));
                minted[d.index as usize] += 1;
                let card = &t.cards[d.index as usize];
                let tok = c.nft_token(d.token_id.clone()).unwrap().metadata.unwrap();
                assert_eq!(tok.title.as_deref(), Some(card.title.as_str()));
                assert_eq!(c.get_backing(d.token_id.clone()), card.backing);
                assert_eq!(c.get_card(d.token_id.clone()).unwrap().card_id.as_deref(), Some(card.card_id.as_str()));
            }
        }
        assert_eq!(c.get_series(id).minted, minted);
        assert!(minted.iter().zip(&t.cards).all(|(m, c)| c.cap.is_none_or(|cap| *m <= cap)), "plafonds respectés");
    }
}

#[test]
fn compact_draw_matches_reference_draw() {
    let t = big_table(400);
    let cards: Vec<DrawCard> = t.cards.iter().map(DrawCard::from).collect();
    let mut minted = vec![0u32; 400];
    for i in 0..3000u32 {
        set(owner(), 0, 1);
        let acc = env::sha256_array(&i.to_le_bytes());
        let slot = (i % 10) as u8;
        let a = draw::draw_slot(&t, &minted, &[], &acc, slot);
        let b = draw::draw_slot_compact(&t.rarity_weights, &cards, &[], &minted, &[], &acc, slot);
        assert_eq!(a, b);
        minted[a.index as usize] += 1;
    }
}

#[test]
fn replace_batched_clears_previous_cards() {
    let mut c = new_contract();
    let id = load_batched(&mut c, &big_table(160), 60);
    let t2 = big_table(70);
    set(owner(), 0, 10);
    let mut first = t2.clone();
    first.cards.truncate(30);
    c.replace_series_table_batched(id, first);
    set(owner(), LOAD_DEPOSIT, 10);
    assert_eq!(c.append_series_cards(id, t2.cards[30..].to_vec()), 70);
    set(owner(), 0, 10);
    let h = c.open_series(id);
    assert_eq!(h, hex32(&env::sha256_array(&serde_json::to_vec(&t2).unwrap())));
    assert!(c.series_cards.get(&(id, 2)).is_none(), "bloc 2 de l'ancienne table supprimé");
    assert_eq!(c.get_series(id).minted.len(), 70);
}

#[test]
#[should_panic(expected = "Table figée")]
fn append_after_open_is_refused() {
    let mut c = new_contract();
    let t = big_table(20);
    let id = c.create_series(t.clone());
    c.open_series(id);
    set(owner(), 0, 11);
    c.append_series_cards(id, big_table(1).cards.into_iter().map(|mut x| { x.card_id = "nouvelle".into(); x }).collect());
}

#[test]
#[should_panic(expected = "Réservé à l'owner")]
fn append_is_owner_only() {
    let mut c = new_contract();
    let id = load_batched(&mut c, &big_table(20), 10);
    set(alice(), 0, 11);
    c.append_series_cards(id, vec![]);
}

#[test]
#[should_panic(expected = "Trop de cartes pour un appel")]
fn single_call_is_limited_to_200_cards() {
    let mut c = new_contract();
    c.create_series(big_table(MAX_CARDS_PER_CALL + 1));
}

#[test]
#[should_panic(expected = "Lot de 1 à 200 cartes")]
fn append_batch_is_limited_to_200_cards() {
    let mut c = new_contract();
    let t = big_table(MAX_CARDS_PER_CALL + 10);
    let id = load_batched(&mut c, &big_table(10), 10);
    set(owner(), 0, 11);
    c.append_series_cards(id, t.cards[..MAX_CARDS_PER_CALL + 1].to_vec());
}

#[test]
#[should_panic(expected = "card_id en double")]
fn duplicate_id_across_batches_is_refused() {
    let mut c = new_contract();
    let t = big_table(60);
    let id = load_batched(&mut c, &t, 30);
    set(owner(), 0, 11);
    c.append_series_cards(id, vec![t.cards[59].clone()]);
}

#[test]
#[should_panic(expected = "hors ordre")]
fn batched_ids_must_be_increasing() {
    let mut c = new_contract();
    let mut t = big_table(20);
    t.cards.swap(3, 4);
    load_batched(&mut c, &t, 10);
}

#[test]
#[should_panic(expected = "append_series_cards suit create_series_batched")]
fn append_to_complete_series_is_refused() {
    let mut c = new_contract();
    let t = big_table(20);
    let id = c.create_series(t);
    set(owner(), 0, 11);
    let mut x = big_table(1).cards;
    x[0].card_id = "zzz".into();
    c.append_series_cards(id, x);
}

#[test]
#[should_panic(expected = "commune sans plafond")]
fn coverage_is_checked_at_open() {
    let mut c = new_contract();
    let mut t = big_table(60);
    for x in t.cards.iter_mut() {
        x.cap = Some(5);
    }
    let id = load_batched(&mut c, &t, 25);
    set(owner(), 0, 11);
    c.open_series(id);
}

#[test]
#[should_panic(expected = "Trop de cartes")]
fn series_is_limited_to_max_cards() {
    let mut c = new_contract();
    let t = big_table(MAX_CARDS_PER_SERIES + 1);
    load_batched(&mut c, &t, MAX_CARDS_PER_CALL);
}

/// Contrôle croisé du script : `scripts/build_series.py` (catalogue v2 complet, hash calculé par le
/// vérificateur Python) contre le contrat qui charge les mêmes arguments lot par lot.
#[test]
fn build_series_script_matches_contract_table_hash() {
    let root = env!("CARGO_MANIFEST_DIR");
    let dir = std::env::temp_dir().join(format!("memaster-build-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let out = dir.join("out");
    let secrets = dir.join("secrets").join("s.json");
    let res = std::process::Command::new("python3")
        .arg("-I")
        .arg(format!("{root}/scripts/build_series.py"))
        .arg(format!("{root}/scripts/serie-exemple.json"))
        .arg("--out")
        .arg(&out)
        .arg("--secrets")
        .arg(&secrets)
        .output()
        .expect("python3 requis pour ce test");
    assert!(res.status.success(), "{}", String::from_utf8_lossy(&res.stderr));
    let read = |name: &str| -> Value { serde_json::from_slice(&std::fs::read(out.join(name)).unwrap()).unwrap() };
    let manifest = read("manifest.json");
    let expected_hash = std::fs::read_to_string(out.join("table_hash.txt")).unwrap().trim().to_string();

    let mut c = new_contract();
    let mut id = None;
    for name in manifest["calls"].as_array().unwrap().iter().map(|v| v.as_str().unwrap()) {
        // Dépôt calculé par le script : doit couvrir le stockage mesuré par le contrat.
        let deposit: u128 = manifest["deposits"][name].as_str().unwrap().parse().unwrap();
        set(owner(), deposit, 10);
        let args = read(name);
        if name == "create_series_batched.json" {
            id = Some(c.create_series_batched(serde_json::from_value(args["table"].clone()).unwrap()));
        } else if name.starts_with("append_series_cards.") {
            let cards: Vec<CardDef> = serde_json::from_value(args["cards"].clone()).unwrap();
            c.append_series_cards(args["series_id"].as_u64().unwrap() as u32, cards);
        } else if name == "open_series.json" {
            assert_eq!(args["series_id"].as_u64().unwrap() as u32, id.unwrap());
            let h = c.open_series(id.unwrap());
            assert_eq!(h, expected_hash, "table_hash du contrat = vérificateur Python");
        }
    }
    let id = id.unwrap();
    let view = serde_json::to_vec(&c.get_series_table(id)).unwrap();
    assert_eq!(view, std::fs::read(out.join("table.json")).unwrap(), "octets de get_series_table = table.json");
    assert_eq!(c.get_series(id).card_count as u64, manifest["cards"].as_u64().unwrap());
    assert_eq!(c.get_mythic_commitments(id).len(), 3);

    // Les engagements publics correspondent aux préimages secrètes (calculées par le contrat).
    let secs: Vec<Value> = serde_json::from_slice(&std::fs::read(&secrets).unwrap()).unwrap();
    let pubs = c.get_mythic_commitments(id);
    for (p, s) in pubs.iter().zip(&secs) {
        let sel = hex_decode(s["sel"].as_str().unwrap()).unwrap();
        let content: MythicContent = serde_json::from_value(s["content"].clone()).unwrap();
        let (cm, ch) = crate::mythic::compute_commitments(s["card_id"].as_str().unwrap(), &sel, &content);
        assert_eq!((hex32(&cm), hex32(&ch)), (p.commitment.clone(), p.content_hash.clone()));
        // Le vrai nom n'apparaît pas dans la table publique.
        let quoted = serde_json::to_vec(&content.title).unwrap();
        assert!(!view.windows(quoted.len()).any(|w| w == quoted.as_slice()), "nom de mythique dans la table");
    }
    std::fs::remove_dir_all(&dir).ok();
}

// ------------------------------------------------------------------ revue : vues, stockage, brouillons

/// Montants des virements créés par le dernier appel vers `who`.
fn transfers_to(who: &AccountId) -> Vec<u128> {
    near_sdk::test_utils::get_created_receipts()
        .iter()
        .filter(|r| &r.receiver_id == who)
        .flat_map(|r| r.actions.iter())
        .filter_map(|a| match a {
            near_sdk::mock::MockAction::Transfer { deposit, .. } => Some(deposit.as_yoctonear()),
            _ => None,
        })
        .collect()
}

/// Ce que fait le vérificateur : en-tête léger + pages de `get_series_cards`, puis hash local.
/// Doit retomber sur le hash stocké, sans aucune vue qui relise toute la table.
#[test]
fn header_and_pages_rebuild_the_stored_hash() {
    let t = big_table(437);
    let mut c = new_contract();
    let id = load_batched(&mut c, &t, 200);
    set(owner(), 0, 11);
    let h = c.open_series(id);
    for page in [200u32, 64, 50, 1] {
        let hv = c.get_series_header(id);
        assert!(hv.header.cards.is_empty());
        assert_eq!(hv.card_count, 437);
        assert_eq!(hv.max_page, 200);
        let mut table = hv.header;
        let mut from = 0;
        while from < hv.card_count {
            let p = c.get_series_cards(id, Some(from), Some(page));
            assert!(!p.is_empty() && p.len() <= page as usize);
            from += p.len() as u32;
            table.cards.extend(p);
        }
        assert_eq!(hex32(&crate::series::table_hash(&table)), h, "page de {page}");
        assert_eq!(hv.table_hash.as_deref(), Some(h.as_str()));
    }
    // Plafond de page : 200.
    assert_eq!(c.get_series_cards(id, Some(0), Some(10_000)).len(), 200);
    assert_eq!(c.get_series_cards(id, Some(437), Some(10)).len(), 0);
    // Hash stocké, pas recalculé.
    assert_eq!(c.get_series_table_hash(id)["stored"].as_str(), Some(h.as_str()));
    assert_eq!(c.get_series_table_hash(id)["card_count"], 437);
}

/// `get_rates` paginée : les pages couvrent chaque carte une fois, et les sommes par rareté sont
/// celles de la table complète (calcul de référence sur la table entière).
#[test]
fn rates_are_paginated_and_match_full_table() {
    let t = big_table(437);
    let mut c = new_contract();
    let id = load_batched(&mut c, &t, 200);
    set(owner(), 0, 11);
    c.open_series(id);
    for k in 0..5u8 {
        buy_and_reveal(&mut c, id, k, 20 + 10 * k as u64);
    }
    let minted = c.get_series(id).minted;
    let mut seen = vec![0u32; 437];
    let mut from = Some(0u64);
    let mut pages = 0;
    while let Some(f) = from {
        let r = c.get_rates(id, Some(f as u32), Some(150));
        assert_eq!(r["card_count"], 437);
        for rr in r["rarities"].as_array().unwrap() {
            let rarity = Rarity::ALL.iter().find(|x| x.as_str() == rr["rarity"]).copied().unwrap();
            let sum: u64 = if rarity == Rarity::Mythic {
                0
            } else {
                t.cards.iter().filter(|c| c.rarity == rarity).map(|c| c.weight as u64).sum()
            };
            assert_eq!(rr["rarity_card_weight"].as_u64().unwrap(), sum);
            assert_eq!(
                rr["available_card_weight"].as_u64().unwrap(),
                draw::available_weight(&t, &minted, &[], rarity)
            );
            for card in rr["cards"].as_array().unwrap() {
                let i = card["index"].as_u64().unwrap() as usize;
                assert_eq!(card["card_id"], t.cards[i].card_id.as_str());
                assert_eq!(card["minted"].as_u64().unwrap() as u32, minted[i]);
                assert_eq!(t.cards[i].rarity, rarity);
                seen[i] += 1;
            }
        }
        from = r["next_index"].as_u64();
        pages += 1;
    }
    assert_eq!(pages, 3);
    assert!(seen.iter().all(|&n| n == 1), "chaque carte sur une seule page");
    // Une petite table tient en une page par défaut.
    assert!(c.get_rates(id, None, None)["next_index"].as_u64() == Some(200));
}

#[test]
#[should_panic(expected = "Dépôt insuffisant pour le stockage")]
fn batched_create_requires_storage_deposit() {
    let mut c = new_contract();
    let mut t = big_table(20);
    t.cards.truncate(10);
    set(owner(), 0, 10);
    c.create_series_batched(t);
}

/// Dépôt d'un yoctoNEAR de moins que l'augmentation mesurée : refusé. Le coût exact est mesuré
/// sur une première série ; le même ajout sur une deuxième série identique passe avec ce dépôt
/// exact, et sur une troisième échoue à un yoctoNEAR près. (Le stockage simulé est partagé entre
/// contrats d'un même test : on reste sur une seule instance, avec des clés distinctes.)
#[test]
#[should_panic(expected = "Dépôt insuffisant pour le stockage")]
fn append_requires_storage_deposit() {
    let t = big_table(20);
    let mut first = t.clone();
    first.cards.truncate(10);
    let mut c = new_contract();
    let [a, b, d] = [0, 1, 2].map(|_| load_batched(&mut c, &first, 10));
    set(owner(), LOAD_DEPOSIT, 11);
    let before = env::storage_usage();
    c.append_series_cards(a, t.cards[10..].to_vec());
    let cost = env::storage_byte_cost().as_yoctonear() * (env::storage_usage() - before) as u128;
    assert!(cost > 0);
    set(owner(), cost, 12);
    assert_eq!(c.append_series_cards(b, t.cards[10..].to_vec()), 20, "dépôt exact accepté");
    assert!(transfers_to(&owner()).is_empty());
    set(owner(), cost - 1, 13);
    c.append_series_cards(d, t.cards[10..].to_vec());
}

/// Le dépôt retenu = augmentation mesurée × coût d'un octet ; l'excédent est rendu au centime près.
#[test]
fn storage_charge_is_measured_and_excess_refunded() {
    let mut c = new_contract();
    let t = big_table(120);
    let byte = env::storage_byte_cost().as_yoctonear();
    let mut first = t.clone();
    first.cards.truncate(70);
    set(owner(), 3 * NEAR, 10);
    let s0 = env::storage_usage();
    let id = c.create_series_batched(first);
    let added = (env::storage_usage() - s0) as u128;
    assert!(added > 70 * 60, "stockage mesuré : {added} o");
    assert_eq!(transfers_to(&owner()), vec![3 * NEAR - added * byte], "excédent rendu");
    assert_eq!(c.get_series_header(id).storage_deposit.0, added * byte);

    set(owner(), 2 * NEAR, 11);
    let s1 = env::storage_usage();
    c.append_series_cards(id, t.cards[70..].to_vec());
    let added2 = (env::storage_usage() - s1) as u128;
    assert_eq!(transfers_to(&owner()), vec![2 * NEAR - added2 * byte]);
    assert_eq!(c.get_series_header(id).storage_deposit.0, (added + added2) * byte);

    // Dépôt exact (même lot, nouvelle série : mêmes tailles de clés et de valeurs) : rien à rendre.
    // Le stockage simulé est partagé entre contrats d'un même test, d'où la même instance.
    let mut first = t.clone();
    first.cards.truncate(70);
    set(owner(), added * byte, 12);
    let id2 = c.create_series_batched(first);
    assert!(transfers_to(&owner()).is_empty());
    assert_eq!(c.get_series_header(id2).storage_deposit.0, added * byte);
}

/// `delete_draft` : tout est vidé, le stockage libéré revient à l'owner (borné par ce qu'il a
/// payé), il ne reste qu'un emplacement de quelques centaines d'octets, et la série supprimée
/// n'accepte plus rien.
#[test]
fn delete_draft_frees_storage_and_refunds_owner() {
    let mut c = new_contract();
    let t = big_table(437);
    set(owner(), 0, 10);
    let s_start = env::storage_usage();
    let id = load_batched(&mut c, &t, 200);
    let paid = c.get_series_header(id).storage_deposit.0;
    assert!(paid > 0);
    set(owner(), 0, 20);
    let s0 = env::storage_usage();
    let refund = c.delete_draft(id).0;
    let freed = (s0 - env::storage_usage()) as u128;
    let byte = env::storage_byte_cost().as_yoctonear();
    assert_eq!(refund, freed * byte);
    assert_eq!(transfers_to(&owner()), vec![refund]);
    let slot = env::storage_usage() - s_start;
    assert!(slot < 300, "emplacement restant : {slot} o");
    assert_eq!(c.get_series_header(id).storage_deposit.0, paid - refund, "reste = l'emplacement");
    assert_eq!(paid - refund, slot as u128 * byte);
    for k in 0..(437u32).div_ceil(CARDS_PER_CHUNK) {
        assert!(c.series_cards.get(&(id, k)).is_none(), "bloc {k} supprimé");
    }
    let v = c.get_series(id);
    assert_eq!(v.status, SeriesStatus::Deleted);
    assert_eq!(v.card_count, 0);
    assert!(v.minted.is_empty() && v.mythic_minted.is_empty());
    assert!(c.series_ref(id).hash_stream.is_none());
    assert!(c.get_series_cards(id, None, None).is_empty());

    // Brouillon de create_series (stockage payé par le contrat) : rien n'est rendu.
    set(owner(), 0, 21);
    let id2 = c.create_series(big_table(30));
    set(owner(), 0, 22);
    assert_eq!(c.delete_draft(id2).0, 0);
    assert!(transfers_to(&owner()).is_empty());
    // Les identifiants ne sont pas réutilisés.
    set(owner(), LOAD_DEPOSIT, 23);
    let mut small = big_table(30);
    small.cards.truncate(30);
    assert_eq!(c.create_series_batched(small), id2 + 1);
}

#[test]
#[should_panic(expected = "Brouillon supprimé")]
fn deleted_draft_cannot_be_opened() {
    let mut c = new_contract();
    let id = load_batched(&mut c, &big_table(60), 30);
    set(owner(), 0, 20);
    c.delete_draft(id);
    c.open_series(id);
}

#[test]
#[should_panic(expected = "Brouillon supprimé")]
fn deleted_draft_cannot_be_appended() {
    let mut c = new_contract();
    let t = big_table(60);
    let id = load_batched(&mut c, &t, 30);
    set(owner(), 0, 20);
    c.delete_draft(id);
    set(owner(), LOAD_DEPOSIT, 21);
    let mut x = big_table(1).cards;
    x[0].card_id = "zzz".into();
    c.append_series_cards(id, x);
}

#[test]
#[should_panic(expected = "Seul un brouillon peut être supprimé")]
fn open_series_cannot_be_deleted() {
    let mut c = new_contract();
    let id = c.create_series(big_table(30));
    c.open_series(id);
    c.delete_draft(id);
}

#[test]
#[should_panic(expected = "Réservé à l'owner")]
fn delete_draft_is_owner_only() {
    let mut c = new_contract();
    let id = load_batched(&mut c, &big_table(30), 30);
    set(alice(), 0, 20);
    c.delete_draft(id);
}
