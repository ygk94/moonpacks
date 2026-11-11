//! Tests d'intégration en sandbox (near-workspaces 0.24 + near-sandbox).
//! Les wasm sont compilés par cargo-near-build au premier test (variante `test-hooks` à part).
//!
//! Lancer : `cargo test --test sandbox -- --nocapture` (les mesures sont imprimées).

use anyhow::Result;
use memaster::types::*;
use near_sdk::json_types::U128;
use near_workspaces::network::Sandbox;
use near_workspaces::result::ExecutionFinalResult;
use near_workspaces::types::{Gas, NearToken};
use near_workspaces::{Account, Contract, Worker};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::sync::Mutex;
use tokio::sync::OnceCell;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;

// ------------------------------------------------------------------ build

static BUILD_LOCK: Mutex<()> = Mutex::new(());
static WASM_PROD: OnceCell<Vec<u8>> = OnceCell::const_new();
static WASM_HOOKS: OnceCell<Vec<u8>> = OnceCell::const_new();
static WASM_MOCK: OnceCell<Vec<u8>> = OnceCell::const_new();
static WASM_ORACLE: OnceCell<Vec<u8>> = OnceCell::const_new();

fn build(manifest: &str, features: Option<&str>, target: &str) -> Vec<u8> {
    let _g = BUILD_LOCK.lock().unwrap_or_else(|e| e.into_inner());
    let root = env!("CARGO_MANIFEST_DIR");
    let opts = cargo_near_build::BuildOpts {
        no_locked: true,
        manifest_path: Some(cargo_near_build::camino::Utf8PathBuf::from(format!("{root}/{manifest}"))),
        features: features.map(String::from),
        override_cargo_target_dir: Some(format!("{root}/target/near-test/{target}")),
        skip_rust_version_check: true,
        ..Default::default()
    };
    let path = cargo_near_build::build_with_cli(opts).expect("build wasm");
    std::fs::read(path).expect("lecture wasm")
}

async fn wasm_prod() -> &'static [u8] {
    WASM_PROD
        .get_or_init(|| async { tokio::task::spawn_blocking(|| build("Cargo.toml", None, "prod")).await.unwrap() })
        .await
}
async fn wasm_hooks() -> &'static [u8] {
    WASM_HOOKS
        .get_or_init(|| async {
            tokio::task::spawn_blocking(|| build("Cargo.toml", Some("test-hooks"), "hooks")).await.unwrap()
        })
        .await
}
async fn wasm_mock() -> &'static [u8] {
    WASM_MOCK
        .get_or_init(|| async {
            tokio::task::spawn_blocking(|| build("mock-redeemer/Cargo.toml", None, "mock")).await.unwrap()
        })
        .await
}

async fn wasm_oracle() -> &'static [u8] {
    WASM_ORACLE
        .get_or_init(|| async {
            tokio::task::spawn_blocking(|| build("mock-oracle/Cargo.toml", None, "oracle")).await.unwrap()
        })
        .await
}

// ------------------------------------------------------------------ environnement

struct Env {
    worker: Worker<Sandbox>,
    contract: Contract,
    redeemer: Contract,
    owner: Account,
    alice: Account,
    bob: Account,
    carol: Account,
}

async fn setup_with(hooks: bool, retry_delay: u64) -> Result<Env> {
    let worker = near_workspaces::sandbox().await?;
    let wasm = if hooks { wasm_hooks().await } else { wasm_prod().await };
    let root = worker.root_account()?;
    let mk = |name: &'static str, near: u128| {
        let root = root.clone();
        async move {
            root.create_subaccount(name)
                .initial_balance(NearToken::from_near(near))
                .transact()
                .await?
                .into_result()
                .map_err(anyhow::Error::from)
        }
    };
    let owner = mk("owner", 100).await?;
    let alice = mk("alice", 2_000).await?;
    let bob = mk("bob", 500).await?;
    let carol = mk("carol", 100).await?;
    let mc = mk("memaster", 200).await?;
    let contract = mc.deploy(wasm).await?.into_result()?;
    let rc = mk("redeemer", 50).await?;
    let redeemer = rc.deploy(wasm_mock().await).await?.into_result()?;
    redeemer.call("new").args_json(json!({ "memaster": contract.id() })).transact().await?.into_result()?;
    contract
        .call("new")
        .args_json(json!({
            "owner_id": owner.id(), "redeemer_id": redeemer.id(), "retry_delay_blocks": retry_delay,
            "oracle_delay_blocks": ORACLE_DELAY,
        }))
        .transact()
        .await?
        .into_result()?;
    Ok(Env { worker, contract, redeemer, owner, alice, bob, carol })
}

/// Délai du changement d'oracle dans le sandbox (24 h en production).
const ORACLE_DELAY: u64 = 10;

async fn setup() -> Result<Env> {
    setup_with(false, 30).await
}

fn card(id: &str, rarity: Rarity, weight: u32, cap: Option<u32>, backed: bool) -> CardDef {
    CardDef {
        card_id: id.into(),
        title: id.to_uppercase(),
        rarity,
        weight,
        cap,
        media: Some(format!("ipfs://bafy/{id}.png")),
        reference: None,
        backing: backed.then(|| Backing { asset_id: format!("nep141:{id}.tkn.near"), amount: U128(1_000_000) }),
    }
}

fn weights(m: u32, l: u32, e: u32, r: u32, c: u32) -> RarityWeights {
    RarityWeights { mythic: m, legendary: l, epic: e, rare: r, common: c }
}

fn sha(parts: &[&[u8]]) -> [u8; 32] {
    let mut h = Sha256::new();
    for p in parts {
        h.update(p);
    }
    h.finalize().into()
}

fn mythic_secret(card_id: &str, sel: &[u8; 32], content: &MythicContent) -> MythicCommitment {
    let c = sha(&[card_id.as_bytes(), sel]);
    let h = sha(&[&serde_json::to_vec(content).unwrap(), sel]);
    MythicCommitment { commitment: hex::encode(c), content_hash: hex::encode(h), weight: 1, cap: 2 }
}

fn table(name: &str, price: u128, w: RarityWeights, cards: Vec<CardDef>, mythics: Vec<MythicCommitment>, royalty_to: &Account) -> SeriesTable {
    SeriesTable {
        name: name.into(),
        price: U128(price),
        cards_per_pack: 5,
        rarity_weights: w,
        cards,
        mythics,
        royalties: vec![Royalty { account_id: royalty_to.id().as_str().parse().unwrap(), bps: 500 }],
        mechanics: None,
    }
}

async fn open_series(env: &Env, t: &SeriesTable) -> Result<u32> {
    let r = env.owner.call(env.contract.id(), "create_series").args_json(json!({ "table": t })).max_gas().transact().await?;
    let id: u32 = r.into_result()?.json()?;
    env.owner.call(env.contract.id(), "open_series").args_json(json!({ "series_id": id })).max_gas().transact().await?.into_result()?;
    Ok(id)
}

async fn series_view(env: &Env, id: u32) -> Result<Value> {
    Ok(env.contract.view("get_series").args_json(json!({ "series_id": id })).await?.json()?)
}

async fn buy(env: &Env, who: &Account, series_id: u32) -> Result<ExecutionFinalResult> {
    let s = series_view(env, series_id).await?;
    let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
    let gas: u64 = s["min_gas"].as_str().unwrap().parse()?;
    Ok(who
        .call(env.contract.id(), "buy_pack")
        .args_json(json!({ "series_id": series_id }))
        .deposit(NearToken::from_yoctonear(dep))
        .gas(Gas::from_gas(gas))
        .transact()
        .await?)
}

fn events(logs: &[&str], name: &str) -> Vec<Value> {
    logs.iter()
        .filter_map(|l| l.strip_prefix("EVENT_JSON:"))
        .filter_map(|l| serde_json::from_str::<Value>(l).ok())
        .filter(|v| v["standard"] == "memaster" && v["event"] == name)
        .map(|v| v["data"][0].clone())
        .collect()
}

fn revealed(r: &ExecutionFinalResult) -> Value {
    let logs = r.logs();
    let ev = events(&logs, "pack_revealed");
    assert_eq!(ev.len(), 1, "pack_revealed attendu, logs: {:?}", logs);
    ev[0].clone()
}

/// Lignes `EVENT_JSON:` des événements utiles au rejeu d'une série, dans l'ordre des reçus.
fn series_event_lines(r: &ExecutionFinalResult) -> Vec<String> {
    const NAMES: [&str; 4] = ["pack_bought", "pack_revealed", "card_redeemed", "card_resurrected"];
    r.receipt_outcomes()
        .iter()
        .flat_map(|o| o.logs.iter())
        .filter(|l| {
            l.strip_prefix("EVENT_JSON:")
                .and_then(|j| serde_json::from_str::<Value>(j).ok())
                .is_some_and(|v| v["standard"] == "memaster" && NAMES.contains(&v["event"].as_str().unwrap_or("")))
        })
        .cloned()
        .collect()
}

fn token_ids(ev: &Value) -> Vec<String> {
    ev["draws"].as_array().unwrap().iter().map(|d| d["token_id"].as_str().unwrap().to_string()).collect()
}

/// Vérificateur public : recalcule acc et les tirages d'un événement `pack_revealed`.
fn verify_pack_event(ev: &Value, owner: &str, table: &SeriesTable) {
    let pack_id = ev["pack_id"].as_u64().unwrap();
    let table_hash = hex::decode(ev["table_hash"].as_str().unwrap()).unwrap();
    let expected_hash = sha(&[&serde_json::to_vec(table).unwrap()]);
    assert_eq!(table_hash, expected_hash, "hash de table");
    let mut acc = sha(&[b"memaster:pack", &pack_id.to_le_bytes(), owner.as_bytes(), &table_hash]);
    assert_eq!(hex::encode(acc), ev["initial_acc"].as_str().unwrap());
    for s in ev["seeds"].as_array().unwrap() {
        let seed = hex::decode(s["seed"].as_str().unwrap()).unwrap();
        acc = sha(&[&acc, &seed, &pack_id.to_le_bytes(), owner.as_bytes()]);
        assert_eq!(hex::encode(acc), s["acc"].as_str().unwrap());
    }
    assert_eq!(hex::encode(acc), ev["acc"].as_str().unwrap());
    // Table de taux du pack (série à mécaniques : base, or ou rush, journalisée).
    let w = match ev["mechanics"]["mode"].as_str() {
        Some("gold") => table.mechanics.as_ref().and_then(|m| m.gold_weights.clone()).unwrap(),
        Some("rush") => table.mechanics.as_ref().and_then(|m| m.rush.as_ref()).map(|r| r.weights.clone()).unwrap(),
        _ => table.rarity_weights.clone(),
    };
    let total: u128 = [w.mythic, w.legendary, w.epic, w.rare, w.common].iter().map(|x| *x as u128).sum();
    for d in ev["draws"].as_array().unwrap() {
        let slot = d["slot"].as_u64().unwrap() as u8;
        let h = sha(&[&acc, &[slot, 0]]);
        let roll = u128::from_be_bytes(h[..16].try_into().unwrap()) % total;
        assert_eq!(roll.to_string(), d["rarity_roll"].as_str().unwrap(), "rarity_roll recalculé");
    }
}

// ------------------------------------------------------------------ tests

/// Achat simple + mesures : hauteur de bloc de chaque reçu, gaz, stockage du pire cas.
#[tokio::test]
async fn buy_pack_and_measurements() -> Result<()> {
    let env = setup().await?;
    let t = table(
        "Mesure",
        NEAR / 10,
        weights(0, 50, 150, 300, 500),
        vec![
            card("leg", Rarity::Legendary, 1, Some(100), true),
            card("epic", Rarity::Epic, 1, None, true),
            card("rare", Rarity::Rare, 1, None, false),
            card("com", Rarity::Common, 1, None, true),
        ],
        vec![],
        &env.owner,
    );
    let sid = open_series(&env, &t).await?;
    let before = env.worker.view_account(env.contract.id()).await?;
    let r = buy(&env, &env.alice, sid).await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let after = env.worker.view_account(env.contract.id()).await?;
    let ev = revealed(&r);
    verify_pack_event(&ev, env.alice.id().as_str(), &t);
    assert_eq!(token_ids(&ev).len(), 5);

    println!("\n=== MESURE : reçus d'un buy_pack (k = 3) ===");
    let mut seed_heights = vec![];
    for o in r.receipt_outcomes() {
        let block = env.worker.view_block().block_hash(o.block_hash).await?;
        let steps = events(&o.logs.iter().map(|s| s.as_str()).collect::<Vec<_>>(), "reveal_step");
        let label = if !steps.is_empty() {
            format!("reveal_step {}", steps[0]["step"])
        } else if o.logs.iter().any(|l| l.contains("pack_revealed")) {
            "reveal_step 3 (tirage)".to_string()
        } else if o.logs.iter().any(|l| l.contains("pack_bought")) {
            "buy_pack".to_string()
        } else {
            format!("remboursement gaz ({})", o.executor_id)
        };
        println!("  {:<26} bloc {:>5}  gaz brûlé {:>7.2} Tgas", label, block.height(), o.gas_burnt.as_gas() as f64 / 1e12);
    }
    for s in ev["seeds"].as_array().unwrap() {
        seed_heights.push((s["block_height"].as_u64().unwrap(), s["seed"].as_str().unwrap().to_string()));
        println!("  graine étape {} : bloc {} seed {}", s["step"], s["block_height"], &s["seed"].as_str().unwrap()[..16]);
    }
    let distinct_heights: std::collections::BTreeSet<_> = seed_heights.iter().map(|x| x.0).collect();
    let distinct_seeds: std::collections::BTreeSet<_> = seed_heights.iter().map(|x| x.1.clone()).collect();
    println!("  hauteurs distinctes : {} / 3, graines distinctes : {} / 3", distinct_heights.len(), distinct_seeds.len());
    assert_eq!(distinct_seeds.len(), 3, "les graines doivent changer d'un reçu à l'autre");

    let sv = series_view(&env, sid).await?;
    let prepaid = sv["storage_per_pack"].as_u64().unwrap();
    let used = after.storage_usage - before.storage_usage;
    println!("  gaz total brûlé : {:.2} Tgas (gaz attaché : {} Tgas)", r.total_gas_burnt.as_gas() as f64 / 1e12, sv["min_gas"].as_str().unwrap().parse::<u64>()? / 1_000_000_000_000);
    println!("  stockage : utilisé {} o, prépayé {} o", used, prepaid);
    assert!(used <= prepaid);

    // Pire cas : 200 cartes aux chaînes de longueur maximale, toutes adossées, 5 puis 10 cartes par booster.
    for per_pack in [5u8, 10u8] {
        let long = |n: usize, c: char| std::iter::repeat_n(c, n).collect::<String>();
        let mut cards = vec![];
        for i in 0..200 {
            let rarity = [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common][i % 4];
            cards.push(CardDef {
                card_id: format!("{:0>64}", i),
                title: long(64, 'T'),
                rarity,
                weight: 1,
                cap: if rarity == Rarity::Common { None } else { Some(1_000_000) },
                media: Some(long(256, 'm')),
                reference: Some(long(256, 'r')),
                backing: Some(Backing { asset_id: format!("{:a>128}", i), amount: U128(u128::MAX) }),
            });
        }
        let mut wt = table("Pire cas", NEAR / 10, weights(0, 1, 1, 1, 1), cards, vec![], &env.owner);
        wt.cards_per_pack = per_pack;
        let wid = open_series(&env, &wt).await?;
        let before = env.worker.view_account(env.contract.id()).await?;
        let r = buy(&env, &env.bob, wid).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let after = env.worker.view_account(env.contract.id()).await?;
        let sv = series_view(&env, wid).await?;
        let prepaid = sv["storage_per_pack"].as_u64().unwrap();
        let used = after.storage_usage - before.storage_usage;
        let max_receipt = r.receipt_outcomes().iter().map(|o| o.gas_burnt.as_gas()).max().unwrap();
        println!(
            "=== PIRE CAS ({} cartes/booster, table de 200 cartes) : gaz total {:.2} Tgas, plus gros reçu {:.2} Tgas, stockage utilisé {} o / prépayé {} o, dépôt requis {} NEAR",
            per_pack,
            r.total_gas_burnt.as_gas() as f64 / 1e12,
            max_receipt as f64 / 1e12,
            used,
            prepaid,
            sv["required_deposit"].as_str().unwrap().parse::<f64>()? / 1e24
        );
        assert!(used <= prepaid, "stockage prépayé insuffisant");
    }
    Ok(())
}

/// ~300 boosters : test statistique grossier des raretés tirées, plafonds, vérification publique.
#[tokio::test]
async fn distribution_over_300_packs() -> Result<()> {
    let env = setup().await?;
    let sel = [7u8; 32];
    let content = MythicContent { title: "Hidden".into(), media: None, reference: None, backing: None };
    let t = table(
        "Distribution",
        NEAR / 20,
        weights(10, 40, 150, 300, 500),
        vec![
            card("leg_a", Rarity::Legendary, 1, Some(5), true),
            card("leg_b", Rarity::Legendary, 1, Some(5), false),
            card("epic", Rarity::Epic, 1, None, true),
            card("rare", Rarity::Rare, 1, None, false),
            card("com_a", Rarity::Common, 3, None, true),
            card("com_b", Rarity::Common, 1, None, false),
        ],
        vec![mythic_secret("hidden", &sel, &content)],
        &env.owner,
    );
    let sid = open_series(&env, &t).await?;
    let buyers: Vec<Account> = {
        let mut v = vec![];
        for i in 0..10 {
            v.push(
                env.alice
                    .create_subaccount(&format!("b{i}"))
                    .initial_balance(NearToken::from_near(60))
                    .transact()
                    .await?
                    .into_result()?,
            );
        }
        v
    };
    let started = std::time::Instant::now();
    let mut handles = vec![];
    for b in buyers {
        let cid = env.contract.id().clone();
        let s = series_view(&env, sid).await?;
        let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
        let gas: u64 = s["min_gas"].as_str().unwrap().parse()?;
        handles.push(tokio::spawn(async move {
            let mut evs = vec![];
            for _ in 0..30 {
                let r = b
                    .call(&cid, "buy_pack")
                    .args_json(json!({ "series_id": sid }))
                    .deposit(NearToken::from_yoctonear(dep))
                    .gas(Gas::from_gas(gas))
                    .transact()
                    .await
                    .unwrap();
                assert!(r.is_success());
                evs.push((b.id().to_string(), revealed(&r)));
            }
            evs
        }));
    }
    let mut all = vec![];
    for h in handles {
        all.extend(h.await?);
    }
    println!("\n=== 300 boosters achetés en {:.0} s ===", started.elapsed().as_secs_f64());
    assert_eq!(all.len(), 300);

    let mut rolled = [0u32; 5];
    let mut final_ = [0u32; 5];
    let mut fallbacks = 0;
    for (owner, ev) in &all {
        verify_pack_event(ev, owner, &t);
        for d in ev["draws"].as_array().unwrap() {
            let r: Rarity = serde_json::from_value(d["rolled_rarity"].clone())?;
            let f: Rarity = serde_json::from_value(d["final_rarity"].clone())?;
            rolled[r.index()] += 1;
            final_[f.index()] += 1;
            assert!(f >= r, "la retombée ne peut que descendre");
            if f != r {
                fallbacks += 1;
                assert!(matches!(r, Rarity::Mythic | Rarity::Legendary), "seules mythique et légendaire sont plafonnées");
            }
        }
    }
    let n: f64 = 1500.0;
    let p: [f64; 5] = [0.01, 0.04, 0.15, 0.30, 0.50];
    println!("  rareté   tirée  attendu  finale");
    for i in 0..5 {
        let e = p[i] * n;
        let sd = (n * p[i] * (1.0 - p[i])).sqrt();
        println!("  {:<9} {:>5}  {:>7.0}  {:>6}", Rarity::ALL[i].as_str(), rolled[i], e, final_[i]);
        assert!((rolled[i] as f64 - e).abs() <= 5.0 * sd + 2.0, "rareté {} hors tolérance", Rarity::ALL[i].as_str());
    }
    println!("  retombées dues aux plafonds : {fallbacks}");

    let sv = series_view(&env, sid).await?;
    let minted: Vec<u32> = serde_json::from_value(sv["minted"].clone())?;
    let mythic_minted: Vec<u32> = serde_json::from_value(sv["mythic_minted"].clone())?;
    println!("  minted par carte : {:?}, mythiques : {:?}", minted, mythic_minted);
    assert!(minted[0] <= 5 && minted[1] <= 5 && mythic_minted[0] <= 2);
    assert_eq!(minted[0] + minted[1], 10, "les légendaires doivent atteindre leur plafond");
    assert_eq!(mythic_minted[0], 2, "la mythique doit atteindre son plafond");
    // communes : poids 3 contre 1
    let ratio = minted[4] as f64 / minted[5].max(1) as f64;
    println!("  ratio com_a / com_b = {:.2} (attendu 3)", ratio);
    assert!(ratio > 2.2 && ratio < 4.0);
    let supply: String = env.contract.view("nft_total_supply").await?.json()?;
    assert_eq!(supply, "1500");
    Ok(())
}

/// Plafond atteint : le tirage retombe sur la rareté inférieure disponible.
#[tokio::test]
async fn caps_fall_back_to_lower_rarity() -> Result<()> {
    let env = setup().await?;
    let t = table(
        "Plafonds",
        NEAR / 10,
        weights(0, 900, 0, 0, 100),
        vec![card("leg", Rarity::Legendary, 1, Some(3), true), card("com", Rarity::Common, 1, None, false)],
        vec![],
        &env.owner,
    );
    let sid = open_series(&env, &t).await?;
    let mut legendary = 0;
    let mut fell = 0;
    for _ in 0..4 {
        let ev = revealed(&buy(&env, &env.alice, sid).await?);
        for d in ev["draws"].as_array().unwrap() {
            if d["final_rarity"] == "legendary" {
                legendary += 1;
            }
            if d["rolled_rarity"] == "legendary" && d["final_rarity"] == "common" {
                fell += 1;
            }
        }
    }
    let sv = series_view(&env, sid).await?;
    assert_eq!(sv["minted"][0], 3);
    assert_eq!(legendary, 3);
    assert!(fell > 0, "des légendaires tirées doivent retomber en commune");
    println!("caps: 3 légendaires créées, {fell} tirages légendaires retombés en commune");
    Ok(())
}

/// Mythique secrète : sortie scellée, engagement vérifié, révélation, puis sortie directe.
#[tokio::test]
async fn mythic_reveal_and_commitment_check() -> Result<()> {
    let env = setup().await?;
    let sel: [u8; 32] = sha(&[b"sel secret de test"]);
    let content = MythicContent {
        title: "PEPE MYTHIQUE".into(),
        media: Some("ipfs://bafy/pepe-mythic.png".into()),
        reference: None,
        backing: Some(Backing { asset_id: "nep141:pepe.tkn.near".into(), amount: U128(777) }),
    };
    let mut m = mythic_secret("pepe-mythic", &sel, &content);
    m.cap = 6;
    let t = table(
        "Mythiques",
        NEAR / 10,
        weights(900, 0, 0, 0, 100),
        vec![card("com", Rarity::Common, 1, None, false)],
        vec![m.clone()],
        &env.owner,
    );
    let sid = open_series(&env, &t).await?;

    // La table publique ne montre que l'engagement.
    let raw = env.contract.view("get_series_table").args_json(json!({ "series_id": sid })).await?.result;
    assert!(!String::from_utf8_lossy(&raw).contains("pepe"), "le mème mythique ne doit pas apparaître");
    let hash = sha(&[&raw]);
    assert_eq!(hex::encode(hash), series_view(&env, sid).await?["table_hash"].as_str().unwrap(), "hash = sha256(octets de la vue)");

    let r = buy(&env, &env.alice, sid).await?;
    let logs = r.logs();
    let drawn = events(&logs, "mythic_drawn");
    assert!(!drawn.is_empty(), "au moins une mythique attendue (p = 0,99999)");
    let sealed_id = drawn[0]["token_id"].as_str().unwrap().to_string();
    assert_eq!(drawn[0]["commitment"], m.commitment);
    let tok: Value = env.contract.view("nft_token").args_json(json!({ "token_id": sealed_id })).await?.json()?;
    assert_eq!(tok["metadata"]["title"], "Mythique scellée");
    let card: Value = env.contract.view("get_card").args_json(json!({ "token_id": sealed_id })).await?.json()?;
    assert_eq!(card["sealed"], true);
    assert!(card["backing"].is_null());

    // Mauvais sel : refusé.
    let bad = env
        .owner
        .call(env.contract.id(), "reveal_mythic")
        .args_json(json!({ "series_id": sid, "mythic_index": 0, "card_id": "pepe-mythic", "sel": hex::encode([0u8; 32]), "content": content }))
        .deposit(NearToken::from_near(1))
        .max_gas()
        .transact()
        .await?;
    assert!(bad.is_failure());

    // Bonne préimage : acceptée.
    let ok = env
        .owner
        .call(env.contract.id(), "reveal_mythic")
        .args_json(json!({ "series_id": sid, "mythic_index": 0, "card_id": "pepe-mythic", "sel": hex::encode(sel), "content": content }))
        .deposit(NearToken::from_near(1))
        .max_gas()
        .transact()
        .await?;
    assert!(ok.is_success(), "{:?}", ok.failures());
    let ev = &events(&ok.logs(), "mythic_revealed")[0];

    // Vérification publique de l'engagement à partir de l'événement.
    let card_id = ev["card_id"].as_str().unwrap();
    let sel_pub = hex::decode(ev["sel"].as_str().unwrap())?;
    assert_eq!(hex::encode(sha(&[card_id.as_bytes(), &sel_pub])), m.commitment);
    let content_pub: MythicContent = serde_json::from_value(ev["content"].clone())?;
    assert_eq!(hex::encode(sha(&[&serde_json::to_vec(&content_pub)?, &sel_pub])), m.content_hash);

    let tok: Value = env.contract.view("nft_token").args_json(json!({ "token_id": sealed_id })).await?.json()?;
    assert_eq!(tok["metadata"]["title"], "PEPE MYTHIQUE");
    let backing: Value = env.contract.view("get_backing").args_json(json!({ "token_id": sealed_id })).await?.json()?;
    assert_eq!(backing["amount"], "777");
    let views: Value = env.contract.view("get_mythic_commitments").args_json(json!({ "series_id": sid })).await?.json()?;
    assert_eq!(views[0]["revealed"]["card_id"], "pepe-mythic");

    // Après la révélation, la mythique sort directement avec contenu et adossement.
    let r2 = buy(&env, &env.bob, sid).await?;
    let ev2 = revealed(&r2);
    assert!(events(&r2.logs(), "mythic_drawn").is_empty());
    let direct = ev2["draws"].as_array().unwrap().iter().find(|d| d["kind"] == "mythic").expect("mythique attendue");
    let card: Value = env.contract.view("get_card").args_json(json!({ "token_id": direct["token_id"] })).await?.json()?;
    assert_eq!(card["sealed"], false);
    assert_eq!(card["card_id"], "pepe-mythic");
    assert_eq!(card["backing"]["amount"], "777");
    Ok(())
}

async fn simple_backed_series(env: &Env) -> Result<u32> {
    let t = table(
        "Brûlables",
        NEAR / 10,
        weights(0, 0, 0, 0, 1),
        vec![card("doge", Rarity::Common, 1, None, true)],
        vec![],
        &env.owner,
    );
    open_series(env, &t).await
}

/// Marché intégré : mise en vente, achat avec redevances, retrait, transfert qui retire l'annonce.
#[tokio::test]
async fn integrated_market() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let ids = token_ids(&revealed(&buy(&env, &env.alice, sid).await?));
    let cid = env.contract.id();

    let r = env.alice.call(cid, "list").args_json(json!({ "token_id": ids[0], "price": (10 * NEAR).to_string() }))
        .deposit(NearToken::from_millinear(5)).transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let listings: Value = env.contract.view("get_listings").args_json(json!({})).await?.json()?;
    assert_eq!(listings.as_array().unwrap().len(), 1);

    // Seul le propriétaire vend.
    assert!(env.bob.call(cid, "list").args_json(json!({ "token_id": ids[1], "price": "1" }))
        .deposit(NearToken::from_millinear(5)).transact().await?.is_failure());
    // Prix non couvert.
    assert!(env.bob.call(cid, "buy").args_json(json!({ "token_id": ids[0], "expected_price": (10 * NEAR).to_string() }))
        .deposit(NearToken::from_near(9)).max_gas().transact().await?.is_failure());

    let a0 = env.alice.view_account().await?.balance.as_yoctonear();
    let o0 = env.owner.view_account().await?.balance.as_yoctonear();
    let r = env.bob.call(cid, "buy").args_json(json!({ "token_id": ids[0], "expected_price": (10 * NEAR).to_string() }))
        .deposit(NearToken::from_near(11)).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let a1 = env.alice.view_account().await?.balance.as_yoctonear();
    let o1 = env.owner.view_account().await?.balance.as_yoctonear();
    assert_eq!(a1 - a0, 9_500_000_000_000_000_000_000_000 + 5_000_000_000_000_000_000_000, "vendeur : 95 % + dépôt");
    assert_eq!(o1 - o0, NEAR / 2, "redevance 5 %");
    let tok: Value = env.contract.view("nft_token").args_json(json!({ "token_id": ids[0] })).await?.json()?;
    assert_eq!(tok["owner_id"], env.bob.id().as_str());
    assert!(env.contract.view("get_listing").args_json(json!({ "token_id": ids[0] })).await?.json::<Value>()?.is_null());

    // Retrait d'annonce, puis achat impossible.
    env.alice.call(cid, "list").args_json(json!({ "token_id": ids[1], "price": NEAR.to_string() }))
        .deposit(NearToken::from_millinear(5)).transact().await?.into_result()?;
    env.alice.call(cid, "delist").args_json(json!({ "token_id": ids[1] })).transact().await?.into_result()?;
    assert!(env.bob.call(cid, "buy").args_json(json!({ "token_id": ids[1], "expected_price": NEAR.to_string() }))
        .deposit(NearToken::from_near(1)).max_gas().transact().await?.is_failure());

    // Remise en vente plus chère juste avant l'achat : l'achat au prix attendu échoue.
    env.alice.call(cid, "list").args_json(json!({ "token_id": ids[3], "price": NEAR.to_string() }))
        .deposit(NearToken::from_millinear(5)).transact().await?.into_result()?;
    env.alice.call(cid, "delist").args_json(json!({ "token_id": ids[3] })).transact().await?.into_result()?;
    env.alice.call(cid, "list").args_json(json!({ "token_id": ids[3], "price": (3 * NEAR).to_string() }))
        .deposit(NearToken::from_millinear(5)).transact().await?.into_result()?;
    let x = env.bob.call(cid, "buy").args_json(json!({ "token_id": ids[3], "expected_price": NEAR.to_string() }))
        .deposit(NearToken::from_near(3)).max_gas().transact().await?;
    assert!(format!("{:?}", x.failures()).contains("prix de l'annonce a changé"));

    // Un transfert NEP-171 retire l'annonce.
    env.alice.call(cid, "list").args_json(json!({ "token_id": ids[2], "price": NEAR.to_string() }))
        .deposit(NearToken::from_millinear(5)).transact().await?.into_result()?;
    env.alice.call(cid, "nft_transfer").args_json(json!({ "receiver_id": env.carol.id(), "token_id": ids[2] }))
        .deposit(NearToken::from_yoctonear(1)).transact().await?.into_result()?;
    assert!(env.contract.view("get_listing").args_json(json!({ "token_id": ids[2] })).await?.json::<Value>()?.is_null());

    // NEP-199
    let p: Value = env.contract.view("nft_payout").args_json(json!({ "token_id": ids[2], "balance": "10000", "max_len_payout": 10 })).await?.json()?;
    assert_eq!(p["payout"][env.owner.id().as_str()], "500");
    assert_eq!(p["payout"][env.carol.id().as_str()], "9500");
    Ok(())
}

/// Burn en deux temps : succès (carte brûlée, redeemer appelé) et échec (carte restaurée).
#[tokio::test]
async fn burn_success_and_failure() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let ids = token_ids(&revealed(&buy(&env, &env.alice, sid).await?));
    let cid = env.contract.id();

    // Succès.
    let r = env.alice.call(cid, "redeem").args_json(json!({ "token_id": ids[0] }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    println!("=== MESURE : redeem réussi, gaz total {:.2} Tgas ===", r.total_gas_burnt.as_gas() as f64 / 1e12);
    assert_eq!(events(&r.logs(), "card_redeemed").len(), 1);
    assert!(r.logs().iter().any(|l| l.contains("\"nft_burn\"")));
    assert_eq!(r.json::<bool>()?, true);
    let tok: Value = env.contract.view("nft_token").args_json(json!({ "token_id": ids[0] })).await?.json()?;
    assert!(tok.is_null());
    let red: Value = env.redeemer.view("get_redemptions").await?.json()?;
    assert_eq!(red[0]["owner"], env.alice.id().as_str());
    assert_eq!(red[0]["asset_id"], "nep141:doge.tkn.near");
    assert_eq!(red[0]["amount"], "1000000");

    // Échec côté redeemer : la carte est restaurée.
    env.redeemer.call("set_fail").args_json(json!({ "fail": true })).transact().await?.into_result()?;
    let r = env.alice.call(cid, "redeem").args_json(json!({ "token_id": ids[1] }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
    assert_eq!(events(&r.logs(), "redeem_failed").len(), 1);
    assert_eq!(r.json::<bool>()?, false);
    let card: Value = env.contract.view("get_card").args_json(json!({ "token_id": ids[1] })).await?.json()?;
    assert_eq!(card["state"], "normal");
    assert_eq!(card["backing"]["amount"], "1000000");
    // Après restauration : la carte se vend et se brûle normalement.
    env.redeemer.call("set_fail").args_json(json!({ "fail": false })).transact().await?.into_result()?;
    let r = env.alice.call(cid, "redeem").args_json(json!({ "token_id": ids[1] }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
    assert_eq!(r.json::<bool>()?, true);

    // Garde-fous : pas de 1 yocto, pas propriétaire, carte en vente.
    assert!(env.alice.call(cid, "redeem").args_json(json!({ "token_id": ids[2] })).gas(Gas::from_tgas(100)).transact().await?.is_failure());
    assert!(env.bob.call(cid, "redeem").args_json(json!({ "token_id": ids[2] }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?.is_failure());
    env.alice.call(cid, "list").args_json(json!({ "token_id": ids[2], "price": "1" }))
        .deposit(NearToken::from_millinear(5)).transact().await?.into_result()?;
    assert!(env.alice.call(cid, "redeem").args_json(json!({ "token_id": ids[2] }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?.is_failure());
    // Le callback est privé.
    assert!(env.alice.call(cid, "on_redeem_complete").args_json(json!({ "token_id": ids[3], "owner": env.alice.id(), "backing": { "asset_id": "x", "amount": "1" } }))
        .transact().await?.is_failure());
    Ok(())
}

/// Aucune annulation : pas de méthode, tirage privé, paiement acquis, livraison par mint direct.
#[tokio::test]
async fn no_cancellation_possible() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let b0 = env.alice.view_account().await?.balance.as_yoctonear();
    let r = buy(&env, &env.alice, sid).await?;
    let ev = revealed(&r);
    let b1 = env.alice.view_account().await?.balance.as_yoctonear();
    assert!(b0 - b1 >= NEAR / 10, "le prix est acquis");
    let pack_id = ev["pack_id"].as_u64().unwrap();

    // Livraison : uniquement des mints, aucun nft_transfer, aucun appel vers un autre contrat.
    assert!(!r.logs().iter().any(|l| l.contains("\"nft_transfer\"")));
    for o in r.receipt_outcomes() {
        assert!(o.executor_id == *env.contract.id() || o.executor_id == *env.alice.id(), "reçu inattendu vers {}", o.executor_id);
    }

    for m in ["cancel_pack", "cancel", "refund_pack", "refund"] {
        let x = env.alice.call(env.contract.id(), m).args_json(json!({ "pack_id": pack_id })).transact().await?;
        assert!(x.is_failure(), "{m} ne doit pas exister");
    }
    // reveal_step est privé : l'acheteur ne peut pas rejouer le tirage.
    let x = env.alice.call(env.contract.id(), "reveal_step").args_json(json!({ "pack_id": pack_id, "attempt": 0, "step": 3 }))
        .max_gas().transact().await?;
    assert!(x.is_failure());
    // Relance interdite une fois écrit, même après le délai.
    env.worker.fast_forward(40).await?;
    let x = env.bob.call(env.contract.id(), "retry_reveal").args_json(json!({ "pack_id": pack_id })).max_gas().transact().await?;
    assert!(x.is_failure());
    // ABI : aucune méthode d'annulation ou de remboursement.
    let abi = std::fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/target/near-test/prod/near/memaster_abi.json"))
        .or_else(|_| std::fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/target/near/memaster_abi.json")))
        .unwrap_or_default();
    if !abi.is_empty() {
        let v: Value = serde_json::from_str(&abi)?;
        for f in v["body"]["functions"].as_array().unwrap() {
            let name = f["name"].as_str().unwrap();
            assert!(!name.contains("cancel") && !name.contains("refund"), "méthode suspecte : {name}");
        }
    }
    Ok(())
}

/// Dépôt ou gaz insuffisant : refus, rien n'est enregistré.
#[tokio::test]
async fn insufficient_deposit_or_gas() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let s = series_view(&env, sid).await?;
    let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
    let gas: u64 = s["min_gas"].as_str().unwrap().parse()?;

    let r = env.alice.call(env.contract.id(), "buy_pack").args_json(json!({ "series_id": sid }))
        .deposit(NearToken::from_yoctonear(dep - 1)).gas(Gas::from_gas(gas)).transact().await?;
    assert!(r.is_failure());
    assert!(format!("{:?}", r.failures()).contains("Dépôt insuffisant"));

    let r = env.alice.call(env.contract.id(), "buy_pack").args_json(json!({ "series_id": sid }))
        .deposit(NearToken::from_near(1)).gas(Gas::from_tgas(100)).transact().await?;
    assert!(r.is_failure());
    assert!(format!("{:?}", r.failures()).contains("Gaz insuffisant"));

    let cfg: Value = env.contract.view("get_config").await?.json()?;
    assert_eq!(cfg["next_pack_id"], 0);
    assert_eq!(cfg["revenue"], "0");

    // Excédent de dépôt rendu (on laisse d'abord arriver les remboursements des échecs ci-dessus).
    env.worker.fast_forward(5).await?;
    let b0 = env.alice.view_account().await?.balance.as_yoctonear();
    let r = env.alice.call(env.contract.id(), "buy_pack").args_json(json!({ "series_id": sid }))
        .deposit(NearToken::from_yoctonear(dep + 5 * NEAR)).gas(Gas::from_gas(gas)).transact().await?;
    assert!(r.is_success());
    env.worker.fast_forward(5).await?;
    let b1 = env.alice.view_account().await?.balance.as_yoctonear();
    let burnt: u128 = r.outcomes().iter().map(|o| o.tokens_burnt.as_yoctonear()).sum();
    println!("excédent : payé {} yocto, requis {} yocto, jetons brûlés (gaz) {} yocto", b0 - b1, dep, burnt);
    assert!(b0 - b1 <= dep + burnt + NEAR / 1000, "l'excédent doit être rendu");
    Ok(())
}

/// `retry_reveal` : le dernier reçu échoue (build test-hooks), relance après délai par un tiers.
#[tokio::test]
async fn retry_reveal_after_failed_draw() -> Result<()> {
    let env = setup_with(true, 20).await?;
    let sid = simple_backed_series(&env).await?;
    let cid = env.contract.id();
    env.owner.call(cid, "test_set_reveal_failure").args_json(json!({ "fail": true })).transact().await?.into_result()?;

    let b0 = env.alice.view_account().await?.balance.as_yoctonear();
    let r = buy(&env, &env.alice, sid).await?;
    assert!(!r.receipt_failures().is_empty(), "le dernier reçu doit échouer");
    let b1 = env.alice.view_account().await?.balance.as_yoctonear();
    assert!(b0 - b1 >= NEAR / 10, "aucun remboursement");
    let pack: Value = env.contract.view("get_pack").args_json(json!({ "pack_id": 0 })).await?.json()?;
    assert_eq!(pack["status"], "pending");
    assert_eq!(pack["step"], 2);
    assert!(pack["token_ids"].as_array().unwrap().is_empty());

    // Trop tôt.
    let x = env.carol.call(cid, "retry_reveal").args_json(json!({ "pack_id": 0 })).max_gas().transact().await?;
    assert!(x.is_failure());
    assert!(format!("{:?}", x.failures()).contains("Délai"));

    env.owner.call(cid, "test_set_reveal_failure").args_json(json!({ "fail": false })).transact().await?.into_result()?;
    env.worker.fast_forward(25).await?;
    // Gaz insuffisant pour la chaîne : refusé.
    assert!(env.carol.call(cid, "retry_reveal").args_json(json!({ "pack_id": 0 })).gas(Gas::from_tgas(50)).transact().await?.is_failure());
    let x = env.carol.call(cid, "retry_reveal").args_json(json!({ "pack_id": 0 })).max_gas().transact().await?;
    assert!(x.is_success(), "{:?}", x.failures());
    let ev = revealed(&x);
    assert_eq!(ev["attempt"], 1);
    assert_eq!(ev["owner_id"], env.alice.id().as_str());
    assert_eq!(ev["seeds"].as_array().unwrap().len(), 2 + 3, "graines de la tentative 0 (2) puis 1 (3)");
    let pack: Value = env.contract.view("get_pack").args_json(json!({ "pack_id": 0 })).await?.json()?;
    assert_eq!(pack["status"], "revealed");
    let n: String = env.contract.view("nft_supply_for_owner").args_json(json!({ "account_id": env.alice.id() })).await?.json()?;
    assert_eq!(n, "5");
    // Une seconde relance est refusée.
    env.worker.fast_forward(25).await?;
    assert!(env.carol.call(cid, "retry_reveal").args_json(json!({ "pack_id": 0 })).max_gas().transact().await?.is_failure());
    Ok(())
}

/// Coût réel pour l'acheteur selon le gaz attaché (mesure, voir README).
#[tokio::test]
async fn buyer_cost_vs_attached_gas() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let s = series_view(&env, sid).await?;
    let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
    let min_gas: u64 = s["min_gas"].as_str().unwrap().parse()?;
    for gas in [min_gas, 200_000_000_000_000, 300_000_000_000_000] {
        let b0 = env.alice.view_account().await?.balance.as_yoctonear();
        let r = env.alice.call(env.contract.id(), "buy_pack").args_json(json!({ "series_id": sid }))
            .deposit(NearToken::from_yoctonear(dep)).gas(Gas::from_gas(gas)).transact().await?;
        assert!(r.is_success());
        // Laisse arriver d'éventuels remboursements tardifs.
        env.worker.fast_forward(5).await?;
        let b1 = env.alice.view_account().await?.balance.as_yoctonear();
        let burnt: u128 = r.outcomes().iter().map(|o| o.tokens_burnt.as_yoctonear()).sum();
        println!(
            "=== MESURE : gaz attaché {} Tgas → coût acheteur {:.5} NEAR (dépôt {:.5}, gaz brûlé {:.5}, non rendu {:.5}) ===",
            gas / 1_000_000_000_000,
            (b0 - b1) as f64 / 1e24,
            dep as f64 / 1e24,
            burnt as f64 / 1e24,
            (b0 - b1 - dep - burnt) as f64 / 1e24
        );
    }
    Ok(())
}

/// Plafond MetaMask : 270 Tgas pour toute la transaction, dans le pire cas
/// (table de 200 cartes aux chaînes maximales, 5 cartes, plafonds légendaires atteints, mythique révélée
/// au contenu maximal qui ressort).
#[tokio::test]
async fn worst_case_fits_in_270_tgas() -> Result<()> {
    let env = setup().await?;
    let long = |n: usize, c: char| std::iter::repeat_n(c, n).collect::<String>();
    let sel: [u8; 32] = sha(&[b"pire cas"]);
    let content = MythicContent {
        title: long(64, 'M'),
        media: Some(long(256, 'm')),
        reference: Some(long(256, 'r')),
        backing: Some(Backing { asset_id: long(128, 'a'), amount: U128(u128::MAX) }),
    };
    let card_id = long(64, 'x');
    let mut mythic = mythic_secret(&card_id, &sel, &content);
    mythic.cap = 100;
    mythic.weight = 1;
    let mut mythics = vec![mythic.clone()];
    // 19 autres engagements (maximum 20), jamais tirés (poids nul).
    for i in 0..19u8 {
        let mut m = mythic_secret(&format!("autre{i}"), &[i; 32], &content);
        m.weight = 0;
        mythics.push(m);
    }
    let mut cards = vec![];
    for i in 0..198 {
        let rarity = [Rarity::Epic, Rarity::Rare, Rarity::Common][i % 3];
        cards.push(CardDef {
            card_id: format!("{:0>64}", i),
            title: long(64, 'T'),
            rarity,
            weight: 1,
            cap: if rarity == Rarity::Common { None } else { Some(1_000_000) },
            media: Some(long(256, 'm')),
            reference: Some(long(256, 'r')),
            backing: Some(Backing { asset_id: format!("{:a>128}", i), amount: U128(u128::MAX) }),
        });
    }
    cards.push(card("leg1", Rarity::Legendary, 1, Some(1), true));
    cards.push(card("leg2", Rarity::Legendary, 1, Some(1), true));
    let mut t = table("270 Tgas", NEAR / 10, weights(400, 300, 100, 100, 100), cards, mythics, &env.owner);
    t.royalties = (0..10).map(|i| Royalty { account_id: format!("r{i}.test.near").parse().unwrap(), bps: 100 }).collect();
    let sid = open_series(&env, &t).await?;

    let s = series_view(&env, sid).await?;
    let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
    let buy270 = |who: Account| {
        let cid = env.contract.id().clone();
        async move {
            who.call(&cid, "buy_pack")
                .args_json(json!({ "series_id": sid }))
                .deposit(NearToken::from_yoctonear(dep))
                .gas(Gas::from_tgas(270))
                .transact()
                .await
        }
    };

    // Préparation : faire sortir la mythique, la révéler, épuiser les légendaires.
    let mut revealed_done = false;
    for _ in 0..20 {
        let r = buy270(env.alice.clone()).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        revealed(&r);
        if !revealed_done && !events(&r.logs(), "mythic_drawn").is_empty() {
            env.owner.call(env.contract.id(), "reveal_mythic")
                .args_json(json!({ "series_id": sid, "mythic_index": 0, "card_id": card_id, "sel": hex::encode(sel), "content": content }))
                .deposit(NearToken::from_near(1)).max_gas().transact().await?.into_result()?;
            revealed_done = true;
        }
        let sv = series_view(&env, sid).await?;
        if revealed_done && sv["minted"][198] == 1 && sv["minted"][199] == 1 {
            break;
        }
    }
    let sv = series_view(&env, sid).await?;
    assert!(revealed_done, "mythique non sortie pendant la préparation");
    assert_eq!((sv["minted"][198].as_u64(), sv["minted"][199].as_u64()), (Some(1), Some(1)), "légendaires non épuisées");

    // Mesure : boosters à 270 Tgas, jusqu'à en avoir un qui contient une mythique révélée et une retombée.
    let mut worst_seen = false;
    for _ in 0..20 {
        let r = buy270(env.bob.clone()).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let ev = revealed(&r);
        let draws = ev["draws"].as_array().unwrap();
        let has_mythic = draws.iter().any(|d| d["kind"] == "mythic");
        let has_fallback = draws.iter().any(|d| d["rolled_rarity"] == "legendary" && d["final_rarity"] != "legendary");
        let max_receipt = r.receipt_outcomes().iter().map(|o| o.gas_burnt.as_gas()).max().unwrap();
        println!(
            "=== MESURE 270 Tgas : pack_revealed OK, mythiques révélées {} , retombée légendaire {} , gaz total {:.2} Tgas, plus gros reçu {:.2} Tgas ===",
            draws.iter().filter(|d| d["kind"] == "mythic").count(),
            has_fallback,
            r.total_gas_burnt.as_gas() as f64 / 1e12,
            max_receipt as f64 / 1e12
        );
        if has_mythic && has_fallback {
            worst_seen = true;
            break;
        }
    }
    assert!(worst_seen, "pas de booster avec mythique révélée et retombée");
    Ok(())
}


/// `new` est privé : un tiers ne peut pas initialiser le contrat avant l'owner.
#[tokio::test]
async fn init_is_private() -> Result<()> {
    let worker = near_workspaces::sandbox().await?;
    let contract = worker.dev_deploy(wasm_prod().await).await?;
    let mallory = worker.dev_create_account().await?;
    let x = mallory.call(contract.id(), "new").args_json(json!({ "owner_id": mallory.id() })).transact().await?;
    assert!(x.is_failure());
    assert!(format!("{:?}", x.failures()).contains("private"));
    contract.call("new").args_json(json!({ "owner_id": mallory.id() })).transact().await?.into_result()?;
    Ok(())
}

/// `nft_transfer_call` : receveur qui garde, qui rend (true), qui panique. Gaz de la résolution.
#[tokio::test]
async fn nft_transfer_call_receivers() -> Result<()> {
    let env = setup().await?;
    let sid = simple_backed_series(&env).await?;
    let ids = token_ids(&revealed(&buy(&env, &env.alice, sid).await?));
    let cid = env.contract.id();
    let recv = env.redeemer.id(); // le mock implémente aussi nft_on_transfer
    for (i, (msg, back)) in [("keep", false), ("return", true), ("panic", true)].iter().enumerate() {
        // une approbation pour vérifier sa restauration ou son effacement
        env.alice.call(cid, "nft_approve").args_json(json!({ "token_id": ids[i], "account_id": env.carol.id() }))
            .deposit(NearToken::from_millinear(10)).max_gas().transact().await?.into_result()?;
        let r = env.alice.call(cid, "nft_transfer_call")
            .args_json(json!({ "receiver_id": recv, "token_id": ids[i], "msg": msg }))
            .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
        assert!(r.is_success(), "{msg}: {:?}", r.failures());
        let total = r.total_gas_burnt;
        let resolve_gas = r.receipt_outcomes().iter()
            .filter(|o| o.executor_id == *cid)
            .last()
            .unwrap()
            .gas_burnt;
        let kept: bool = r.json()?;
        assert_eq!(kept, !back, "{msg}: valeur NEP-171 de nft_resolve_transfer");
        let tok: Value = env.contract.view("nft_token").args_json(json!({ "token_id": ids[i] })).await?.json()?;
        let expected_owner = if *back { env.alice.id().as_str() } else { recv.as_str() };
        assert_eq!(tok["owner_id"], expected_owner, "{msg}");
        let approved = !tok["approved_account_ids"].as_object().unwrap().is_empty();
        assert_eq!(approved, *back, "{msg}: approbations restaurées seulement en cas de retour");
        println!("=== MESURE nft_transfer_call ({msg}) : résolution {:.2} Tgas (fixe 15), total {:.2} Tgas ===",
            resolve_gas.as_gas() as f64 / 1e12, total.as_gas() as f64 / 1e12);
        assert!(resolve_gas.as_gas() < 15_000_000_000_000);
    }
    // Gaz insuffisant refusé d'emblée.
    let x = env.alice.call(cid, "nft_transfer_call")
        .args_json(json!({ "receiver_id": recv, "token_id": ids[3], "msg": "keep" }))
        .deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(30)).transact().await?;
    assert!(x.is_failure());
    Ok(())
}

/// Révélation d'une mythique avec 100 cartes scellées et un contenu maximal : mesure du gaz.
#[tokio::test]
async fn reveal_with_100_sealed_cards() -> Result<()> {
    let env = setup().await?;
    let long = |n: usize, c: char| std::iter::repeat_n(c, n).collect::<String>();
    let sel: [u8; 32] = sha(&[b"cent scellees"]);
    let content = MythicContent {
        title: long(64, 'M'),
        media: Some(long(256, 'm')),
        reference: Some(long(256, 'r')),
        backing: Some(Backing { asset_id: long(128, 'a'), amount: U128(u128::MAX) }),
    };
    let card_id = long(64, 'x');
    let mut m = mythic_secret(&card_id, &sel, &content);
    m.cap = 100;
    let mut t = table("Cent", NEAR / 100, weights(990, 0, 0, 0, 10), vec![card("com", Rarity::Common, 1, None, false)], vec![m], &env.owner);
    t.cards_per_pack = 10;
    let sid = open_series(&env, &t).await?;
    let mut n = 0;
    while n < 100 {
        let r = buy(&env, &env.alice, sid).await?;
        assert!(r.is_success());
        n = series_view(&env, sid).await?["mythic_minted"][0].as_u64().unwrap();
    }
    let r = env.owner.call(env.contract.id(), "reveal_mythic")
        .args_json(json!({ "series_id": sid, "mythic_index": 0, "card_id": card_id, "sel": hex::encode(sel), "content": content }))
        .deposit(NearToken::from_near(5)).gas(Gas::from_tgas(300)).transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let ev = &events(&r.logs(), "mythic_revealed")[0];
    assert_eq!(ev["token_ids"].as_array().unwrap().len(), 100);
    let receipt = r.receipt_outcomes().iter().map(|o| o.gas_burnt.as_gas()).max().unwrap();
    println!("=== MESURE reveal_mythic (100 scellées, contenu maximal) : reçu {:.2} Tgas, total {:.2} Tgas ===",
        receipt as f64 / 1e12, r.total_gas_burnt.as_gas() as f64 / 1e12);
    assert!(receipt < 150_000_000_000_000, "au-delà de 150 Tgas : paginer la révélation");
    Ok(())
}

// ------------------------------------------------------------------ grosses séries, chargement par lots

fn tgas(g: u64) -> f64 {
    g as f64 / 1e12
}

/// Exécute `scripts/build_series.py` (catalogue v2 complet) dans un dossier temporaire.
fn build_v2_args(tag: &str) -> std::path::PathBuf {
    let root = env!("CARGO_MANIFEST_DIR");
    let dir = std::path::PathBuf::from(format!("{root}/target/near-test/build-series-{tag}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&dir);
    let out = std::process::Command::new("python3")
        .arg("-I")
        .arg(format!("{root}/scripts/build_series.py"))
        .arg(format!("{root}/scripts/serie-exemple.json"))
        .arg("--out")
        .arg(dir.join("out"))
        .arg("--secrets")
        .arg(dir.join("secrets").join("s.json"))
        .output()
        .expect("python3 requis");
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
    dir
}

/// Lance le vérificateur Python (`verifier/`) ; renvoie (succès, sortie).
fn run_verifier(args: &[&str]) -> (bool, String) {
    let root = env!("CARGO_MANIFEST_DIR");
    let out = std::process::Command::new("python3")
        .current_dir(format!("{root}/../verifier"))
        .arg("-m")
        .arg("memaster_verifier")
        .args(args)
        .output()
        .expect("python3 requis");
    (out.status.success(), format!("{}{}", String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr)))
}

/// Attend que l'ouverture de la série soit finale (le vérificateur lit en `finality = final`) :
/// sous charge, quelques blocs ne suffisent pas toujours.
async fn wait_final_open(env: &Env, sid: u32) -> Result<()> {
    for _ in 0..30 {
        env.worker.fast_forward(5).await?;
        let raw = env
            .worker
            .view(env.contract.id(), "get_series_table_hash")
            .args_json(json!({ "series_id": sid }))
            .finality(near_workspaces::types::Finality::Final)
            .await?;
        if !raw.json::<Value>()?["stored"].is_null() {
            return Ok(());
        }
    }
    anyhow::bail!("ouverture de la série {sid} jamais finale")
}

/// Série v2 complète (1 646 cartes visibles + 3 mythiques) : refus en une transaction, chargement
/// en 9 lots, ouverture, hash = vérificateur Python, achats au gaz minimal, tirages revérifiés
/// par le vérificateur Python (rejeu des plafonds depuis l'ouverture). Mesures imprimées.
#[tokio::test]
async fn catalogue_v2_batched_load_and_packs() -> Result<()> {
    let env = setup().await?;
    let dir = build_v2_args("e2e");
    let out = dir.join("out");
    let read = |name: &str| -> Value { serde_json::from_slice(&std::fs::read(out.join(name)).unwrap()).unwrap() };
    let manifest = read("manifest.json");
    let expected_hash = std::fs::read_to_string(out.join("table_hash.txt"))?.trim().to_string();
    let table_bytes = std::fs::read(out.join("table.json"))?;
    let full: SeriesTable = serde_json::from_slice(&table_bytes)?;
    println!("\n=== SÉRIE V2 : {} cartes visibles, {} mythiques, table {} o ===", full.cards.len(), full.mythics.len(), table_bytes.len());

    // 1. En une seule transaction : refusé (au plus 200 cartes par appel).
    let single = serde_json::to_vec(&json!({ "table": full }))?;
    let r = env.owner.call(env.contract.id(), "create_series").args(single.clone()).max_gas().transact().await?;
    assert!(r.is_failure());
    assert!(format!("{:?}", r.failures()).contains("Trop de cartes pour un appel"));
    println!("  create_series en 1 tx ({} o d'arguments) : refusé, {:.2} Tgas", single.len(), tgas(r.total_gas_burnt.as_gas()));

    // 2. Par lots.
    let before = env.worker.view_account(env.contract.id()).await?;
    let mut sid = None;
    let (mut load_gas, mut max_call) = (0u64, 0u64);
    for name in manifest["calls"].as_array().unwrap().iter().map(|v| v.as_str().unwrap()) {
        let method = name.split('.').next().unwrap();
        let args = std::fs::read(out.join(name))?;
        // Dépôt calculé par le script (borne haute du stockage ajouté ; l'excédent est rendu).
        let deposit: u128 = manifest["deposits"][name].as_str().unwrap().parse()?;
        let r = env
            .owner
            .call(env.contract.id(), method)
            .args(args.clone())
            .deposit(NearToken::from_yoctonear(deposit))
            .max_gas()
            .transact()
            .await?;
        assert!(r.is_success(), "{name}: {:?}", r.failures());
        let g = r.total_gas_burnt.as_gas();
        println!("  {:<30} {:>7} o d'arguments  {:>7.2} Tgas", name, args.len(), tgas(g));
        max_call = max_call.max(g);
        load_gas += g;
        match method {
            "create_series_batched" => sid = Some(r.json::<u32>()?),
            "open_series" => assert_eq!(r.json::<String>()?, expected_hash, "hash du contrat = vérificateur Python"),
            _ => {}
        }
    }
    let sid = sid.unwrap();
    let after = env.worker.view_account(env.contract.id()).await?;
    let series_storage = after.storage_usage - before.storage_usage;
    println!(
        "  chargement complet : {:.2} Tgas en {} transactions (plus grosse {:.2} Tgas), stockage {} o ({:.2} NEAR)",
        tgas(load_gas),
        manifest["calls"].as_array().unwrap().len(),
        tgas(max_call),
        series_storage,
        series_storage as f64 / 1e5
    );
    assert!(max_call < 300_000_000_000_000);
    // Stockage payé par l'owner : exactement l'augmentation mesurée.
    let hd: Value = env.contract.view("get_series_header").args_json(json!({ "series_id": sid })).await?.json()?;
    let paid: u128 = hd["storage_deposit"].as_str().unwrap().parse()?;
    let attached: u128 = manifest["deposits"].as_object().unwrap().values().map(|v| v.as_str().unwrap().parse::<u128>().unwrap()).sum();
    println!(
        "  stockage payé par l'owner : {:.4} NEAR (dépôts joints {:.3} NEAR, excédent rendu) ; le contrat n'avance rien",
        paid as f64 / 1e24,
        attached as f64 / 1e24
    );
    // L'ouverture (non payable) change le stockage de quelques dizaines d'octets (flux de hachage effacé, hash écrit).
    assert!(paid.abs_diff(series_storage as u128 * 10u128.pow(19)) <= 200 * 10u128.pow(19), "stockage payé ≈ stockage mesuré");

    // Octets bruts de la vue complète (petite série : encore utilisable) = table.json.
    let raw = env.contract.view("get_series_table").args_json(json!({ "series_id": sid })).await?.result;
    assert_eq!(raw, table_bytes, "get_series_table = table.json du script");
    assert_eq!(hex::encode(sha(&[&raw])), expected_hash);
    let hv: Value = env.contract.view("get_series_table_hash").args_json(json!({ "series_id": sid })).await?.json()?;
    assert_eq!(hv["stored"].as_str(), Some(expected_hash.as_str()), "hash enregistré");
    // Vérificateur en mode pagination (en-tête + pages) : même hash qu'avant (table complète).
    wait_final_open(&env, sid).await?; // le vérificateur lit l'état final (finality = final)
    for page in ["200", "77"] {
        let (ok, txt) = run_verifier(&[
            "table", "--rpc", &env.worker.rpc_addr(), "--contract", env.contract.id().as_str(), "--series", &sid.to_string(),
            "--page-size", page,
        ]);
        assert!(ok, "vérificateur table : {txt}");
        assert!(txt.contains("lue par pages") && txt.contains(&format!("sha256 calculé : {expected_hash}")), "{txt}");
    }
    println!("  vérificateur Python, table lue par pages (200 et 77) : hash = {expected_hash}, VÉRIFIÉ");

    // 3. Achats au gaz minimal (160 Tgas), tirages revérifiés.
    let sv = series_view(&env, sid).await?;
    let prepaid = sv["storage_per_pack"].as_u64().unwrap();
    let mut jsonl = String::new();
    let (mut worst_total, mut worst_buy, mut worst_final, mut worst_used) = (0u64, 0u64, 0u64, 0u64);
    for i in 0..12 {
        let who = if i % 2 == 0 { &env.alice } else { &env.bob };
        let b = env.worker.view_account(env.contract.id()).await?;
        let r = buy(&env, who, sid).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let a = env.worker.view_account(env.contract.id()).await?;
        let ev = revealed(&r);
        verify_pack_event(&ev, who.id().as_str(), &full);
        let outs = r.receipt_outcomes();
        worst_buy = worst_buy.max(outs[0].gas_burnt.as_gas());
        worst_final = worst_final.max(
            outs.iter().filter(|o| o.logs.iter().any(|l| l.contains("pack_revealed"))).map(|o| o.gas_burnt.as_gas()).max().unwrap(),
        );
        worst_total = worst_total.max(r.total_gas_burnt.as_gas());
        worst_used = worst_used.max(a.storage_usage - b.storage_usage);
        for l in series_event_lines(&r) {
            jsonl.push_str(&l);
            jsonl.push('\n');
        }
    }
    println!(
        "  12 boosters à {} Tgas : gaz total max {:.2} Tgas, buy_pack max {:.2} Tgas (budget 20), dernier reçu max {:.2} Tgas (budget 120), stockage max {} o / prépayé {} o",
        sv["min_gas"].as_str().unwrap().parse::<u64>()? / 1_000_000_000_000,
        tgas(worst_total),
        tgas(worst_buy),
        tgas(worst_final),
        worst_used,
        prepaid
    );
    assert!(worst_used <= prepaid);
    assert!(worst_buy < 20_000_000_000_000, "buy_pack dans son budget propre");
    let events_path = dir.join("events.jsonl");
    std::fs::write(&events_path, jsonl)?;
    let (ok, txt) = run_verifier(&["pack", "--event", events_path.to_str().unwrap(), "--table", out.join("table.json").to_str().unwrap()]);
    assert!(ok, "vérificateur pack : {txt}");
    assert!(!txt.contains("NON CONFORME"), "{txt}");
    println!("  vérificateur Python : 12 boosters rejoués depuis l'ouverture (mécaniques de serie-exemple.json), VÉRIFIÉ");
    std::fs::remove_dir_all(&dir).ok();
    Ok(())
}

/// Taille maximale : 2 000 cartes aux chaînes maximales (10 lots), 20 engagements, 10 cartes par
/// booster. L'ouverture (validation, JSON, hash) doit tenir en une transaction et l'achat au gaz minimal.
#[tokio::test]
async fn max_size_series_fits() -> Result<()> {
    let env = setup().await?;
    let long = |n: usize, c: char| std::iter::repeat_n(c, n).collect::<String>();
    let content = MythicContent { title: long(64, 'M'), media: Some(long(256, 'm')), reference: Some(long(256, 'r')), backing: None };
    let mythics: Vec<MythicCommitment> = (0..20u8).map(|i| mythic_secret(&format!("m{i}"), &[i; 32], &content)).collect();
    let cards: Vec<CardDef> = (0..memaster::MAX_CARDS_PER_SERIES)
        .map(|i| {
            let rarity = [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common][i % 4];
            CardDef {
                card_id: format!("{:0>64}", i),
                title: long(64, 'T'),
                rarity,
                weight: 1,
                cap: if rarity == Rarity::Common { None } else { Some(1_000_000) },
                media: Some(long(256, 'm')),
                reference: Some(long(256, 'r')),
                backing: Some(Backing { asset_id: format!("{:a>128}", i), amount: U128(u128::MAX) }),
            }
        })
        .collect();
    let mut t = table("Taille max", NEAR / 10, weights(1, 1, 1, 1, 1), cards, mythics, &env.owner);
    t.cards_per_pack = 10;
    // Pire cas des mécaniques : toutes actives (pitié garantie un pack sur deux, burns, rush).
    t.mechanics = Some(Mechanics {
        gold_weights: Some(weights(4, 4, 3, 2, 1)),
        pity: Some(PityParams { p0_ppm: 20_000, k_ppm: 2_000, n_max: 2 }),
        burn: Some(BurnParams { floor_bps: 2_500, prior_k: 20 }),
        rush: Some(RushParams {
            ratio_bps: 25_000,
            min_packs: 50,
            window_blocks: 6_000,
            baseline_blocks: 144_000,
            bucket_blocks: 1_500,
            duration_blocks: 3_000,
            cooldown_blocks: 36_000,
            max_per_account: 3,
            weights: weights(2, 2, 2, 2, 1),
        }),
        // Toutes les cartes sont adossées par la table : aucune n'est ressuscitable.
        resurrection: None,
    });
    t.royalties = (0..10).map(|i| Royalty { account_id: format!("r{i}.test.near").parse().unwrap(), bps: 100 }).collect();
    let mut first = t.clone();
    first.cards.truncate(memaster::MAX_CARDS_PER_CALL);
    let before = env.worker.view_account(env.contract.id()).await?;
    let lot_deposit = NearToken::from_millinear(2_500); // > 188 Ko de stockage par lot ; excédent rendu
    let r = env.owner.call(env.contract.id(), "create_series_batched").args_json(json!({ "table": first })).deposit(lot_deposit).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let sid: u32 = r.json()?;
    let mut max_append = 0u64;
    for lot in t.cards[memaster::MAX_CARDS_PER_CALL..].chunks(memaster::MAX_CARDS_PER_CALL) {
        let r = env.owner.call(env.contract.id(), "append_series_cards").args_json(json!({ "series_id": sid, "cards": lot })).deposit(lot_deposit).max_gas().transact().await?;
        assert!(r.is_success(), "{:?}", r.failures());
        max_append = max_append.max(r.total_gas_burnt.as_gas());
    }
    // Une carte de plus : refusée.
    let mut extra = t.cards[0].clone();
    extra.card_id = "en-trop".into();
    let r = env.owner.call(env.contract.id(), "append_series_cards").args_json(json!({ "series_id": sid, "cards": [extra] })).deposit(lot_deposit).max_gas().transact().await?;
    assert!(format!("{:?}", r.failures()).contains("Trop de cartes"));
    let r = env.owner.call(env.contract.id(), "open_series").args_json(json!({ "series_id": sid })).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let open_gas = r.total_gas_burnt.as_gas();
    let h: String = r.json()?;
    assert_eq!(h, hex::encode(sha(&[&serde_json::to_vec(&t)?])));
    let after = env.worker.view_account(env.contract.id()).await?;
    let args_lot = serde_json::to_vec(&json!({ "series_id": sid, "cards": &t.cards[..memaster::MAX_CARDS_PER_CALL] }))?.len();
    println!(
        "\n=== TAILLE MAX (2 000 cartes, chaînes max) : lot de 200 = {} o d'arguments, append max {:.2} Tgas, open_series {:.2} Tgas, stockage {} o ===",
        args_lot,
        tgas(max_append),
        tgas(open_gas),
        after.storage_usage - before.storage_usage
    );
    let raw = env.contract.view("get_series_table").args_json(json!({ "series_id": sid })).await?.result;
    assert_eq!(hex::encode(sha(&[&raw])), h, "vue complète lisible et hachable");
    let paid: u128 = {
        let hd: Value = env.contract.view("get_series_header").args_json(json!({ "series_id": sid })).await?.json()?;
        hd["storage_deposit"].as_str().unwrap().parse()?
    };
    println!("  stockage payé par l'owner : {:.3} NEAR", paid as f64 / 1e24);

    // Gaz des vues légères, appelées en transaction pour lire le gaz brûlé du reçu.
    let view_gas = |name: &'static str, args: Value| {
        let env = &env;
        async move {
            let r = env.owner.call(env.contract.id(), name).args_json(args).max_gas().transact().await?;
            anyhow::ensure!(r.is_success(), "{name}: {:?}", r.failures());
            let g = r.receipt_outcomes()[0].gas_burnt.as_gas();
            Ok::<(u64, Vec<u8>), anyhow::Error>((g, r.raw_bytes()?))
        }
    };
    let (g_header, hb) = view_gas("get_series_header", json!({ "series_id": sid })).await?;
    let (g_hash, _) = view_gas("get_series_table_hash", json!({ "series_id": sid })).await?;
    let (mut g_cards, mut g_rates) = (0u64, 0u64);
    let mut rebuilt: Value = serde_json::from_slice::<Value>(&hb)?["header"].clone();
    let mut cards = Vec::new();
    for from in (0..memaster::MAX_CARDS_PER_SERIES as u32).step_by(200) {
        let (g, page) = view_gas("get_series_cards", json!({ "series_id": sid, "from_index": from, "limit": 200 })).await?;
        g_cards = g_cards.max(g);
        cards.extend(serde_json::from_slice::<Vec<Value>>(&page)?);
        let (g, _) = view_gas("get_rates", json!({ "series_id": sid, "from_index": from, "limit": 200 })).await?;
        g_rates = g_rates.max(g);
    }
    rebuilt["cards"] = Value::Array(cards);
    let rebuilt: SeriesTable = serde_json::from_value(rebuilt)?;
    assert_eq!(hex::encode(sha(&[&serde_json::to_vec(&rebuilt)?])), h, "en-tête + 10 pages = table hachée");
    println!(
        "  vues légères (2 000 cartes, chaînes max) : get_series_header {:.2} Tgas, get_series_table_hash {:.2} Tgas, get_series_cards (200) {:.2} Tgas au plus, get_rates (200) {:.2} Tgas au plus",
        tgas(g_header),
        tgas(g_hash),
        tgas(g_cards),
        tgas(g_rates)
    );
    for g in [g_header, g_hash, g_cards, g_rates] {
        assert!(g < 100_000_000_000_000, "vue légère sous 100 Tgas (limite 300)");
    }
    // Le vérificateur Python lit cette table par pages (aucune vue lourde) et retrouve le hash.
    wait_final_open(&env, sid).await?;
    let (ok, txt) = run_verifier(&[
        "table", "--rpc", &env.worker.rpc_addr(), "--contract", env.contract.id().as_str(), "--series", &sid.to_string(),
    ]);
    assert!(ok && txt.contains(&format!("sha256 calculé : {h}")), "vérificateur table : {txt}");

    let prepaid = series_view(&env, sid).await?["storage_per_pack"].as_u64().unwrap();
    for _ in 0..4 {
        let b = env.worker.view_account(env.contract.id()).await?;
        let r = buy(&env, &env.alice, sid).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let a = env.worker.view_account(env.contract.id()).await?;
        let ev = revealed(&r);
        verify_pack_event(&ev, env.alice.id().as_str(), &t);
        let outs = r.receipt_outcomes();
        let last = outs.iter().map(|o| o.gas_burnt.as_gas()).max().unwrap();
        println!(
            "  booster de 10 cartes à 160 Tgas (mécaniques, table {}) : total {:.2} Tgas, buy_pack {:.2} Tgas, dernier reçu {:.2} Tgas, stockage {} o / prépayé {} o",
            ev["mechanics"]["mode"],
            tgas(r.total_gas_burnt.as_gas()),
            tgas(outs[0].gas_burnt.as_gas()),
            tgas(last),
            a.storage_usage - b.storage_usage,
            prepaid
        );
        assert!(outs[0].gas_burnt.as_gas() < 20_000_000_000_000);
        assert!(last < memaster::FINAL_STEP_GAS.as_gas(), "dernier reçu dans son gaz fixe");
        assert!(a.storage_usage - b.storage_usage <= prepaid);
    }
    Ok(())
}

/// Brouillon par lots : stockage payé par l'owner (refus sans dépôt, excédent rendu), puis
/// `delete_draft` qui libère le stockage et le rend à l'owner. Le contrat n'y perd rien.
#[tokio::test]
async fn draft_storage_is_paid_by_owner_and_refunded_on_delete() -> Result<()> {
    let env = setup().await?;
    let cards: Vec<CardDef> = (0..300).map(|i| card(&format!("c{i:04}"), Rarity::Common, 1, None, i % 7 == 0)).collect();
    let t = table("Brouillon", NEAR / 10, weights(0, 0, 0, 0, 1), cards, vec![], &env.owner);
    let mut first = t.clone();
    first.cards.truncate(200);
    let c0 = env.worker.view_account(env.contract.id()).await?;

    // Sans dépôt : refusé, rien n'est écrit.
    let r = env.owner.call(env.contract.id(), "create_series_batched").args_json(json!({ "table": first })).max_gas().transact().await?;
    assert!(format!("{:?}", r.failures()).contains("Dépôt insuffisant pour le stockage"), "{:?}", r.failures());
    assert_eq!(env.worker.view_account(env.contract.id()).await?.storage_usage, c0.storage_usage);

    // Avec dépôt : l'owner paie exactement le stockage, l'excédent revient. Les soldes sont lus
    // après quelques blocs, une fois les remboursements de gaz arrivés.
    env.worker.fast_forward(3).await?;
    let o0 = env.owner.view_account().await?.balance.as_yoctonear();
    let r = env.owner.call(env.contract.id(), "create_series_batched").args_json(json!({ "table": first })).deposit(NearToken::from_near(5)).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let sid: u32 = r.json()?;
    let r = env
        .owner
        .call(env.contract.id(), "append_series_cards")
        .args_json(json!({ "series_id": sid, "cards": &t.cards[200..] }))
        .deposit(NearToken::from_near(5))
        .max_gas()
        .transact()
        .await?;
    assert!(r.is_success(), "{:?}", r.failures());
    env.worker.fast_forward(3).await?;
    let c1 = env.worker.view_account(env.contract.id()).await?;
    let o1 = env.owner.view_account().await?.balance.as_yoctonear();
    let added = c1.storage_usage - c0.storage_usage;
    let hd: Value = env.contract.view("get_series_header").args_json(json!({ "series_id": sid })).await?.json()?;
    let paid: u128 = hd["storage_deposit"].as_str().unwrap().parse()?;
    assert_eq!(paid, added as u128 * 10u128.pow(19), "payé = augmentation mesurée");
    let spent = o0 - o1;
    assert!(spent >= paid && spent < paid + NEAR / 100, "owner : stockage + gaz seulement ({spent} vs {paid})");
    println!("\n=== BROUILLON 300 cartes : {added} o, {:.4} NEAR payés par l'owner (10 NEAR joints, excédent rendu)", paid as f64 / 1e24);

    // Suppression : réservée à l'owner, puis stockage libéré et rendu.
    let r = env.alice.call(env.contract.id(), "delete_draft").args_json(json!({ "series_id": sid })).max_gas().transact().await?;
    assert!(format!("{:?}", r.failures()).contains("Réservé à l'owner"));
    let r = env.owner.call(env.contract.id(), "delete_draft").args_json(json!({ "series_id": sid })).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let delete_gas = r.total_gas_burnt.as_gas();
    let refund: U128 = r.json()?;
    env.worker.fast_forward(3).await?;
    let c2 = env.worker.view_account(env.contract.id()).await?;
    let o2 = env.owner.view_account().await?.balance.as_yoctonear();
    let freed = c1.storage_usage - c2.storage_usage;
    let slot = c2.storage_usage - c0.storage_usage;
    assert_eq!(refund.0, freed as u128 * 10u128.pow(19));
    assert!(o2 + NEAR / 100 > o1 + refund.0 && o2 < o1 + refund.0, "rendu à l'owner, moins le gaz");
    assert!(slot < 300, "emplacement restant {slot} o");
    let hd: Value = env.contract.view("get_series_header").args_json(json!({ "series_id": sid })).await?.json()?;
    assert_eq!(hd["status"], "deleted");
    assert_eq!(hd["card_count"], 0);
    assert_eq!(hd["storage_deposit"].as_str().unwrap().parse::<u128>()?, slot as u128 * 10u128.pow(19), "l'emplacement reste payé par l'owner");
    println!(
        "  delete_draft : {freed} o libérés, {:.4} NEAR rendus, emplacement restant {slot} o, {:.2} Tgas",
        refund.0 as f64 / 1e24,
        tgas(delete_gas)
    );
    // Plus rien n'est possible sur la série supprimée ; une série ouverte ne se supprime pas.
    let r = env.owner.call(env.contract.id(), "open_series").args_json(json!({ "series_id": sid })).max_gas().transact().await?;
    assert!(format!("{:?}", r.failures()).contains("Brouillon supprimé"));
    let open = open_series(&env, &table("Ouverte", NEAR / 10, weights(0, 0, 0, 0, 1), vec![card("x", Rarity::Common, 1, None, false)], vec![], &env.owner)).await?;
    let r = env.owner.call(env.contract.id(), "delete_draft").args_json(json!({ "series_id": open })).max_gas().transact().await?;
    assert!(format!("{:?}", r.failures()).contains("Seul un brouillon"));
    assert_eq!(open, sid + 1, "identifiants jamais réutilisés");
    Ok(())
}

// ------------------------------------------------------------------ mécaniques

/// Série à toutes les mécaniques, de bout en bout : pitié (N = 3), gold rush déclenché par un pic
/// d'achats (palier relatif, pause), burns jusqu'à la dernière carte d'un coin, résurrection d'une
/// épique par l'oracle factice. Tous les événements sont rejoués par le vérificateur Python, sans
/// archive d'état. Mesures de gaz et de stockage imprimées.
#[tokio::test]
async fn mechanics_end_to_end() -> Result<()> {
    let env = setup().await?;
    let oc = env.worker.root_account()?.create_subaccount("oracle").initial_balance(NearToken::from_near(20)).transact().await?.into_result()?;
    let oracle = oc.deploy(wasm_oracle().await).await?.into_result()?;
    oracle.call("new").args_json(json!({ "memaster": env.contract.id(), "operator": env.owner.id() })).transact().await?.into_result()?;
    // Changement d'oracle en deux temps : refusé avant le délai, accepté après.
    env.owner.call(env.contract.id(), "propose_price_oracle").args_json(json!({ "price_oracle_id": oracle.id() })).transact().await?.into_result()?;
    let r = env.owner.call(env.contract.id(), "accept_price_oracle").args_json(json!({})).transact().await?;
    assert!(format!("{:?}", r.failures()).contains("non écoulé"), "{:?}", r.failures());
    env.worker.fast_forward(ORACLE_DELAY).await?;
    env.owner.call(env.contract.id(), "accept_price_oracle").args_json(json!({})).transact().await?.into_result()?;

    let mut t = table(
        "Mécaniques",
        NEAR / 10,
        weights(0, 20, 100, 200, 680),
        vec![
            card("leg_a", Rarity::Legendary, 1, None, true),
            card("leg_b", Rarity::Legendary, 1, None, false),
            card("epic_a", Rarity::Epic, 1, None, true),
            card("epic_b", Rarity::Epic, 1, None, true),
            card("epic_c", Rarity::Epic, 1, None, false),
            card("rare", Rarity::Rare, 1, None, false),
            card("com_a", Rarity::Common, 10, None, true),
            card("com_b", Rarity::Common, 10, None, true),
            card("com_c", Rarity::Common, 10, None, false),
        ],
        vec![],
        &env.owner,
    );
    t.mechanics = Some(Mechanics {
        gold_weights: Some(weights(0, 80, 300, 300, 320)),
        pity: Some(PityParams { p0_ppm: 100_000, k_ppm: 50_000, n_max: 3 }),
        // A priori petit : sur une vingtaine de boosters, les burns doivent se voir dans les tirages.
        burn: Some(BurnParams { floor_bps: 2_500, prior_k: 2 }),
        rush: Some(RushParams {
            ratio_bps: 15_000,
            min_packs: 2,
            window_blocks: 10,
            baseline_blocks: 50,
            bucket_blocks: 5,
            duration_blocks: 20,
            cooldown_blocks: 20,
            // Le pic vient de trois comptes : le plafond par compte ne coupe pas le rush.
            max_per_account: 3,
            weights: weights(0, 30, 150, 250, 570),
        }),
        // leg_b et epic_c, non adossées par la table.
        resurrection: Some(ResurrectionParams { eligible: vec![1, 4] }),
    });
    let sid = open_series(&env, &t).await?;
    let prepaid = series_view(&env, sid).await?["storage_per_pack"].as_u64().unwrap();
    let mut lines: Vec<String> = vec![];
    let mut held: Vec<(String, usize, Account)> = vec![]; // (token_id, index, propriétaire)
    let (mut max_used, mut max_last, mut modes) = (0u64, 0u64, std::collections::BTreeMap::<String, u32>::new());
    let buyers = [env.alice.clone(), env.bob.clone(), env.carol.clone()];
    let mut k = 0usize;
    macro_rules! buy_one {
        () => {{
            let who = &buyers[k % 3];
            k += 1;
            let b = env.worker.view_account(env.contract.id()).await?;
            let r = buy(&env, who, sid).await?;
            assert!(r.is_success(), "{:?}", r.failures());
            let a = env.worker.view_account(env.contract.id()).await?;
            max_used = max_used.max(a.storage_usage - b.storage_usage);
            let last = r.receipt_outcomes().iter().filter(|o| o.logs.iter().any(|l| l.contains("pack_revealed"))).map(|o| o.gas_burnt.as_gas()).max().unwrap();
            max_last = max_last.max(last);
            let ev = revealed(&r);
            verify_pack_event(&ev, who.id().as_str(), &t);
            *modes.entry(ev["mechanics"]["mode"].as_str().unwrap().to_string()).or_default() += 1;
            for d in ev["draws"].as_array().unwrap() {
                held.push((d["token_id"].as_str().unwrap().to_string(), d["index"].as_u64().unwrap() as usize, who.clone()));
            }
            lines.extend(series_event_lines(&r));
            ev
        }};
    }
    // 1. Trafic calme, puis la fenêtre longue (50 blocs) se remplit.
    for _ in 0..3 {
        buy_one!();
    }
    env.worker.fast_forward(60).await?;
    // 2. Pic d'achats consécutifs : le rythme court dépasse 1,5 × la moyenne, le rush se déclenche.
    let mut rush_packs = 0;
    for _ in 0..8 {
        let ev = buy_one!();
        rush_packs += ev["mechanics"]["rush"].as_bool().unwrap() as u32;
    }
    assert!(rush_packs > 0, "aucun pack rush pendant le pic");
    let rs: Value = env.contract.view("get_rush_state").args_json(json!({ "series_id": sid })).await?.json()?;
    println!("\n=== MÉCANIQUES : {rush_packs} packs rush pendant le pic, état du rush {rs}");
    // 3. Burns : toutes les com_a (jusqu'à la dernière), quelques epic_a.
    let mut burn_gas = 0u64;
    let to_burn: Vec<_> = held.iter().filter(|(_, i, _)| *i == 6 || *i == 2).cloned().collect();
    for (tid, _, who) in &to_burn {
        let r = who.call(env.contract.id(), "redeem").args_json(json!({ "token_id": tid })).deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let cb = r.receipt_outcomes().iter().filter(|o| o.logs.iter().any(|l| l.contains("card_redeemed"))).map(|o| o.gas_burnt.as_gas()).max().unwrap();
        burn_gas = burn_gas.max(cb);
        lines.extend(series_event_lines(&r));
    }
    let sv = series_view(&env, sid).await?;
    assert_eq!(sv["burned"][6].as_u64().unwrap() as usize, to_burn.iter().filter(|x| x.1 == 6).count());
    let rates: Value = env.contract.view("get_rates").args_json(json!({ "series_id": sid })).await?.json()?;
    println!("  {} burns (toutes les com_a, jusqu'à la dernière, et les epic_a), on_redeem_complete {:.2} Tgas au plus (20 fixes) ; communes : {}", to_burn.len(), tgas(burn_gas), rates["rarities"][4]["cards"]);
    assert!(burn_gas < 20_000_000_000_000);
    // 4. Résurrection d'une épique morte par l'oracle (rare et commune refusées).
    for (idx, ok) in [(4u32, true), (5, false), (8, false)] {
        let r = env.owner.call(oracle.id(), "push_resurrection")
            .args_json(json!({ "series_id": sid, "card_index": idx, "asset_id": "nep141:revived.near", "amount": "5" }))
            .deposit(NearToken::from_millinear(10)).max_gas().transact().await?;
        let logs = series_event_lines(&r);
        assert_eq!(!logs.is_empty(), ok, "résurrection de {idx} : {:?}", r.failures());
        lines.extend(logs);
    }
    let epic_c = held.iter().find(|x| x.1 == 4);
    if let Some((tid, _, _)) = epic_c {
        let b: Option<Backing> = env.contract.view("get_backing").args_json(json!({ "token_id": tid })).await?.json()?;
        assert_eq!(b.unwrap().amount, U128(5), "exemplaire existant ressuscité");
    }
    // 5. Achats après burns et résurrection (pause du rush comprise).
    env.worker.fast_forward(5).await?;
    for _ in 0..6 {
        buy_one!();
    }
    println!(
        "  {} boosters : tables {:?}, stockage {} o au plus / prépayé {} o, dernier reçu {:.2} Tgas au plus",
        k, modes, max_used, prepaid, tgas(max_last)
    );
    assert!(modes.get("gold").copied().unwrap_or(0) > 0, "pitié : aucun gold pack");
    assert!(max_used <= prepaid);
    // 6. Vérificateur Python : rejeu de tous les événements (achats, tirages, burns, résurrections).
    let dir = std::path::PathBuf::from(format!("{}/target/near-test/mech-{}", env!("CARGO_MANIFEST_DIR"), std::process::id()));
    std::fs::create_dir_all(&dir)?;
    std::fs::write(dir.join("events.jsonl"), lines.join("\n"))?;
    std::fs::write(dir.join("table.json"), serde_json::to_vec(&t)?)?;
    let (ok, txt) = run_verifier(&["pack", "--event", dir.join("events.jsonl").to_str().unwrap(), "--table", dir.join("table.json").to_str().unwrap()]);
    assert!(ok && !txt.contains("NON CONFORME"), "vérificateur : {txt}");
    assert!(txt.contains("burns ") && txt.contains("résurrections 1"), "{txt}");
    println!("  vérificateur Python : {} événements rejoués, VÉRIFIÉ", lines.len());
    // Vecteurs du vérificateur (verifier/tests/vectors/sandbox_mech_vectors.json), sur demande.
    if let Ok(out) = std::env::var("MECH_VECTORS_OUT") {
        let events: Vec<Value> = lines.iter().map(|l| serde_json::from_str(l.strip_prefix("EVENT_JSON:").unwrap()).unwrap()).collect();
        let doc = json!({
            "source": "tests/sandbox.rs mechanics_end_to_end (contrat déployé dans near-sandbox, événements réels)",
            "table_raw": String::from_utf8(serde_json::to_vec(&t)?)?,
            "events": events,
        });
        std::fs::write(out, serde_json::to_string_pretty(&doc)? + "\n")?;
    }
    std::fs::remove_dir_all(&dir).ok();
    Ok(())
}

/// Pire cas du dernier reçu (revue, point 6) : 2 000 cartes, 10 cartes par booster, toutes les
/// mécaniques, et des raretés épuisées en cascade. Légendaires, épiques et rares ont un plafond nul :
/// chaque emplacement vise la légendaire (poids de rareté presque tout là) et retombe trois fois
/// jusqu'à la commune, en recalculant à chaque cran les facteurs des burns sur les 2 000 cartes.
/// Des communes adossées sont brûlées entre les achats, et 200 cartes sont ressuscitables
/// (recherche dans la liste pour chaque brûlable). Le dernier reçu doit rester sous son gaz fixe.
#[tokio::test]
async fn worst_case_cascade_with_burns_fits() -> Result<()> {
    let env = setup().await?;
    let cards: Vec<CardDef> = (0..memaster::MAX_CARDS_PER_SERIES)
        .map(|i| {
            let (rarity, cap, backed) = match i {
                0..=199 => (Rarity::Legendary, Some(0), false),
                200..=399 => (Rarity::Epic, Some(0), true),
                400..=599 => (Rarity::Rare, Some(0), false),
                _ => (Rarity::Common, None, i % 2 == 0),
            };
            card(&format!("c{i:04}"), rarity, 1 + (i % 7) as u32, cap, backed)
        })
        .collect();
    let mut t = table("Cascade", NEAR / 10, weights(0, 9_997, 1, 1, 1), cards, vec![], &env.owner);
    t.cards_per_pack = 10;
    t.mechanics = Some(Mechanics {
        gold_weights: Some(weights(0, 9_996, 2, 1, 1)),
        pity: Some(PityParams { p0_ppm: 20_000, k_ppm: 2_000, n_max: 2 }),
        burn: Some(BurnParams { floor_bps: 2_500, prior_k: 20 }),
        rush: Some(RushParams {
            ratio_bps: 25_000,
            min_packs: 100,
            window_blocks: 6_000,
            baseline_blocks: 144_000,
            bucket_blocks: 1_500,
            duration_blocks: 3_000,
            cooldown_blocks: 36_000,
            max_per_account: 3,
            weights: weights(0, 9_995, 3, 1, 1),
        }),
        resurrection: Some(ResurrectionParams { eligible: (0..200).collect() }),
    });
    let mut first = t.clone();
    first.cards.truncate(memaster::MAX_CARDS_PER_CALL);
    let dep = NearToken::from_near(1);
    let r = env.owner.call(env.contract.id(), "create_series_batched").args_json(json!({ "table": first })).deposit(dep).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let sid: u32 = r.json()?;
    for lot in t.cards[memaster::MAX_CARDS_PER_CALL..].chunks(memaster::MAX_CARDS_PER_CALL) {
        let r = env.owner.call(env.contract.id(), "append_series_cards").args_json(json!({ "series_id": sid, "cards": lot })).deposit(dep).max_gas().transact().await?;
        assert!(r.is_success(), "{:?}", r.failures());
    }
    let r = env.owner.call(env.contract.id(), "open_series").args_json(json!({ "series_id": sid })).max_gas().transact().await?;
    assert!(r.is_success(), "{:?}", r.failures());
    let (mut max_last, mut falls, mut modes) = (0u64, 0usize, std::collections::BTreeSet::new());
    let mut burned = 0;
    for round in 0..8 {
        let r = buy(&env, &env.alice, sid).await?;
        assert!(r.is_success(), "{:?}", r.failures());
        let ev = revealed(&r);
        verify_pack_event(&ev, env.alice.id().as_str(), &t);
        modes.insert(ev["mechanics"]["mode"].as_str().unwrap().to_string());
        let last = r.receipt_outcomes().iter().filter(|o| o.logs.iter().any(|l| l.contains("pack_revealed"))).map(|o| o.gas_burnt.as_gas()).max().unwrap();
        max_last = max_last.max(last);
        for d in ev["draws"].as_array().unwrap() {
            assert_eq!(d["final_rarity"], "common", "cascade jusqu'à la commune");
            falls += (d["rolled_rarity"] == "legendary") as usize;
        }
        // Burns entre deux achats : les communes adossées de ce booster.
        if round < 4 {
            for d in ev["draws"].as_array().unwrap() {
                if d["index"].as_u64().unwrap() % 2 == 0 {
                    let r = env.alice.call(env.contract.id(), "redeem").args_json(json!({ "token_id": d["token_id"] })).deposit(NearToken::from_yoctonear(1)).gas(Gas::from_tgas(100)).transact().await?;
                    assert!(r.is_success(), "{:?}", r.failures());
                    burned += 1;
                }
            }
        }
    }
    let sv = series_view(&env, sid).await?;
    assert_eq!(sv["burn_seq"].as_u64().unwrap() as usize, burned);
    println!(
        "\n=== PIRE CAS EN CASCADE (2 000 cartes, 10 par booster, toutes les mécaniques, {burned} burns, tables {modes:?}) : {falls} emplacements sur 80 tombés de la légendaire à la commune, dernier reçu {:.2} Tgas au plus (gaz fixe {:.0}) ===",
        tgas(max_last),
        tgas(memaster::FINAL_STEP_GAS.as_gas())
    );
    assert!(falls > 70, "la cascade doit être le cas courant : {falls}");
    assert!(burned > 0);
    assert!(max_last < memaster::FINAL_STEP_GAS.as_gas(), "dernier reçu dans son gaz fixe");
    Ok(())
}
