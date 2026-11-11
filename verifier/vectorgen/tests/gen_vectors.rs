//! Génération des vecteurs de test du vérificateur Python, depuis le contrat lui-même.
//!
//! - `draw_vectors` : appelle directement `memaster::draw` (le code compilé dans le contrat) sur des
//!   tables, des compteurs `minted` et des `acc` pseudo-aléatoires, y compris des chaînes Unicode et des
//!   caractères de contrôle pour le hash de table. Rapide, sans réseau.
//! - `sandbox_vectors` : déploie le wasm du contrat dans near-sandbox, ouvre des séries, achète des
//!   boosters, révèle une mythique, et enregistre les événements réels (`pack_revealed`, `mythic_revealed`)
//!   avec l'état `minted` avant chaque achat. Lance ensuite le CLI Python contre le RPC du sandbox.
//!
//! ```bash
//! cd verifier/vectorgen
//! NEAR_SANDBOX_BIN_PATH=/chemin/vers/near-sandbox cargo test -- --nocapture --test-threads 1
//! ```
//! Variables : `MEMASTER_WASM` (défaut `../../contract/target/near/memaster.wasm`),
//! `VECTORS_OUT` (défaut `../tests/vectors`), `SKIP_PY_RPC=1` pour ne pas lancer le CLI Python.

use memaster::draw;
use memaster::types::*;
use near_sdk::json_types::U128;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::path::PathBuf;

const NEAR: u128 = 1_000_000_000_000_000_000_000_000;

fn out_dir() -> PathBuf {
    let p = std::env::var("VECTORS_OUT")
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/vectors"));
    std::fs::create_dir_all(&p).unwrap();
    p
}

fn verifier_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..")
}

fn sha(parts: &[&[u8]]) -> [u8; 32] {
    let mut h = Sha256::new();
    for p in parts {
        h.update(p);
    }
    h.finalize().into()
}

fn write_json(name: &str, v: &Value) {
    let path = out_dir().join(name);
    std::fs::write(&path, serde_json::to_string_pretty(v).unwrap() + "\n").unwrap();
    println!("écrit : {}", path.display());
}

// ------------------------------------------------------------------ PRNG déterministe

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
        self.next() % n
    }
    fn bytes32(&mut self) -> [u8; 32] {
        let mut b = [0u8; 32];
        for c in b.chunks_mut(8) {
            c.copy_from_slice(&self.next().to_le_bytes());
        }
        b
    }
    fn chance(&mut self, num: u64, den: u64) -> bool {
        self.below(den) < num
    }
}

const ALPHABET: &[&str] = &[
    "a", "Z", "0", "-", "_", ".", " ", "/", "<", ">", "&", "'", "\"", "\\", "\n", "\r", "\t", "\u{8}", "\u{c}",
    "\u{0}", "\u{1}", "\u{1f}", "\u{7f}", "é", "ß", "€", "\u{2028}", "\u{2029}", "\u{feff}", "🐸", "日本",
    "\u{10ffff}", "ʼ", "%", "{", "}", "[", "]", ":", ",",
];

fn rand_str(rng: &mut Rng, max: usize) -> String {
    let n = 1 + rng.below(max as u64) as usize;
    (0..n).map(|_| ALPHABET[rng.below(ALPHABET.len() as u64) as usize]).collect()
}

fn rand_opt_str(rng: &mut Rng, max: usize) -> Option<String> {
    rng.chance(1, 2).then(|| rand_str(rng, max))
}

fn rand_backing(rng: &mut Rng) -> Option<Backing> {
    rng.chance(1, 2).then(|| Backing {
        asset_id: rand_str(rng, 12),
        amount: U128(((rng.next() as u128) << 64 | rng.next() as u128).max(1)),
    })
}

fn rand_table(rng: &mut Rng) -> SeriesTable {
    let lower = [Rarity::Legendary, Rarity::Epic, Rarity::Rare, Rarity::Common];
    let n = 1 + rng.below(12) as usize;
    let mut cards = Vec::new();
    for i in 0..n {
        let rarity = lower[rng.below(4) as usize];
        cards.push(CardDef {
            card_id: format!("c{i}-{}", rand_str(rng, 4)),
            title: rand_str(rng, 10),
            rarity,
            weight: rng.below(6) as u32,
            cap: rng.chance(1, 2).then(|| rng.below(4) as u32),
            media: rand_opt_str(rng, 8),
            reference: rand_opt_str(rng, 8),
            backing: rand_backing(rng),
        });
    }
    // Garantie du contrat : au moins une commune illimitée de poids non nul.
    let pos = rng.below(n as u64 + 1) as usize;
    cards.insert(
        pos,
        CardDef {
            card_id: "base-common".into(),
            title: "Base".into(),
            rarity: Rarity::Common,
            weight: 1 + rng.below(5) as u32,
            cap: None,
            media: None,
            reference: None,
            backing: None,
        },
    );
    let m = rng.below(4) as usize;
    let mythics = (0..m)
        .map(|_| MythicCommitment {
            commitment: hex::encode(rng.bytes32()),
            content_hash: hex::encode(rng.bytes32()),
            weight: rng.below(4) as u32,
            cap: 1 + rng.below(3) as u32,
        })
        .collect();
    let rw = |rng: &mut Rng| if rng.chance(1, 4) { 0 } else { 1 + rng.below(1000) as u32 };
    let rarity_weights = RarityWeights {
        mythic: rw(rng),
        legendary: rw(rng),
        epic: rw(rng),
        rare: rw(rng),
        common: 1 + rng.below(1000) as u32,
    };
    let royalties = (0..rng.below(3))
        .map(|i| Royalty { account_id: format!("roy{i}.near").parse().unwrap(), bps: rng.below(2500) as u16 })
        .collect();
    SeriesTable {
        name: rand_str(rng, 16),
        price: U128((rng.next() as u128) << 64 | rng.next() as u128),
        cards_per_pack: 1 + rng.below(10) as u8,
        rarity_weights,
        cards,
        mythics,
        royalties,
    }
}

fn draw_json(d: &draw::SlotDraw, slot: u8) -> Value {
    json!({
        "slot": slot,
        "rarity_roll": d.rarity_roll.to_string(),
        "rolled_rarity": d.rolled_rarity,
        "final_rarity": d.final_rarity,
        "card_roll": d.card_roll.to_string(),
        "kind": d.kind,
        "index": d.index,
    })
}

/// Vecteurs du code pur de `draw.rs` (compilé depuis `contract/src`).
#[test]
fn draw_vectors() {
    let mut rng = Rng(0x6d65_6d61_7374_6572);
    let mut cases = Vec::new();
    for case in 0..200 {
        let table = rand_table(&mut rng);
        let table_json = serde_json::to_string(&table).unwrap();
        let table_hash = sha(&[table_json.as_bytes()]);
        let pack_id = if case % 7 == 0 { u64::MAX - rng.below(5) } else { rng.below(1 << 40) };
        let owner = match case % 4 {
            0 => format!("buyer{case}.testnet"),
            1 => hex::encode(rng.bytes32()),
            2 => format!("0x{}", &hex::encode(rng.bytes32())[..40]),
            _ => format!("b{case}.alice.test.near"),
        };
        let initial = draw::initial_acc(pack_id, &owner, &table_hash);
        let mut acc = initial;
        let mut seeds = Vec::new();
        for step in 1..=(2 + rng.below(5)) {
            let seed = rng.bytes32();
            acc = draw::mix(&acc, &seed, pack_id, &owner);
            seeds.push(json!({ "step": step, "seed": hex::encode(seed), "acc": hex::encode(acc) }));
        }
        // État des plafonds : parfois vierge, parfois proche ou au-delà du plafond.
        let mut minted: Vec<u32> = table
            .cards
            .iter()
            .map(|c| match c.cap {
                Some(cap) if rng.chance(2, 3) => (cap as u64 + rng.below(2)).saturating_sub(rng.below(2)) as u32,
                _ => rng.below(3) as u32,
            })
            .collect();
        let mut mythic_minted: Vec<u32> =
            table.mythics.iter().map(|m| (m.cap as u64).saturating_sub(rng.below(3)) as u32).collect();
        let minted_before = minted.clone();
        let mythic_minted_before = mythic_minted.clone();
        let mut draws = Vec::new();
        for slot in 0..table.cards_per_pack {
            let d = draw::draw_slot(&table, &minted, &mythic_minted, &acc, slot);
            draws.push(draw_json(&d, slot));
            match d.kind {
                CardKind::Visible => minted[d.index as usize] += 1,
                CardKind::Mythic => mythic_minted[d.index as usize] += 1,
            }
        }
        // Quelques `roll` bruts (valeurs u128 avant le modulo).
        let rolls: Vec<Value> = [(0u8, 0u8), (0, 1), (9, 0), (255, 1)]
            .iter()
            .map(|(s, t)| json!({ "slot": s, "tag": t, "value": draw::roll(&acc, *s, *t).to_string() }))
            .collect();
        cases.push(json!({
            "table": table,
            "table_json": table_json,
            "table_hash": hex::encode(table_hash),
            "pack_id": pack_id,
            "owner": owner,
            "initial_acc": hex::encode(initial),
            "seeds": seeds,
            "acc": hex::encode(acc),
            "minted": minted_before,
            "mythic_minted": mythic_minted_before,
            "minted_after": minted,
            "mythic_minted_after": mythic_minted,
            "rolls": rolls,
            "draws": draws,
        }));
    }

    // Engagements mythiques : sha256(card_id || sel) et sha256(json(content) || sel).
    let mut mythics = Vec::new();
    for _ in 0..60 {
        let card_id = rand_str(&mut rng, 20);
        let sel = rng.bytes32();
        let content = MythicContent {
            title: rand_str(&mut rng, 20),
            media: rand_opt_str(&mut rng, 20),
            reference: rand_opt_str(&mut rng, 20),
            backing: rand_backing(&mut rng),
        };
        let content_json = serde_json::to_string(&content).unwrap();
        mythics.push(json!({
            "card_id": card_id,
            "sel": hex::encode(sel),
            "content": content,
            "content_json": content_json,
            "commitment": hex::encode(sha(&[card_id.as_bytes(), &sel])),
            "content_hash": hex::encode(sha(&[content_json.as_bytes(), &sel])),
        }));
    }
    write_json(
        "draw_vectors.json",
        &json!({
            "source": "memaster::draw (contract/src/draw.rs), serde_json::to_vec(SeriesTable), sha256",
            "cases": cases,
            "mythics": mythics,
        }),
    );
}

// ------------------------------------------------------------------ sandbox

mod sandbox {
    use super::*;
    use near_workspaces::result::ExecutionFinalResult;
    use near_workspaces::types::{Gas, NearToken};
    use near_workspaces::{Account, Contract};

    fn events(logs: &[&str], name: &str) -> Vec<Value> {
        logs.iter()
            .filter_map(|l| l.strip_prefix("EVENT_JSON:"))
            .filter_map(|l| serde_json::from_str::<Value>(l).ok())
            .filter(|v| v["standard"] == "memaster" && v["event"] == name)
            .map(|v| v["data"][0].clone())
            .collect()
    }

    pub struct Ctx {
        pub contract: Contract,
        pub owner: Account,
    }

    pub async fn open_series(ctx: &Ctx, t: &SeriesTable) -> anyhow::Result<(u32, Value)> {
        let r = ctx
            .owner
            .call(ctx.contract.id(), "create_series")
            .args_json(json!({ "table": t }))
            .max_gas()
            .transact()
            .await?;
        let id: u32 = r.into_result()?.json()?;
        let r = ctx
            .owner
            .call(ctx.contract.id(), "open_series")
            .args_json(json!({ "series_id": id }))
            .max_gas()
            .transact()
            .await?
            .into_result()?;
        let opened = events(&r.logs(), "series_opened");
        Ok((id, opened[0].clone()))
    }

    pub async fn series_view(ctx: &Ctx, id: u32) -> anyhow::Result<Value> {
        Ok(ctx.contract.view("get_series").args_json(json!({ "series_id": id })).await?.json()?)
    }

    pub async fn buy(ctx: &Ctx, who: &Account, sid: u32) -> anyhow::Result<ExecutionFinalResult> {
        let s = series_view(ctx, sid).await?;
        let dep: u128 = s["required_deposit"].as_str().unwrap().parse()?;
        let gas: u64 = s["min_gas"].as_str().unwrap().parse()?;
        let r = who
            .call(ctx.contract.id(), "buy_pack")
            .args_json(json!({ "series_id": sid }))
            .deposit(NearToken::from_yoctonear(dep))
            .gas(Gas::from_gas(gas))
            .transact()
            .await?;
        anyhow::ensure!(r.is_success(), "buy_pack : {:?}", r.failures());
        Ok(r)
    }

    /// Une série : table brute, hash, puis les boosters achetés dans l'ordre, avec `minted` avant chacun.
    pub async fn run_series(
        ctx: &Ctx,
        label: &str,
        t: &SeriesTable,
        buyers: &[Account],
        packs: usize,
        mut on_pack: impl FnMut(&ExecutionFinalResult) -> Option<(u32, String, MythicContent, [u8; 32])>,
    ) -> anyhow::Result<(Value, Vec<(u32, String, MythicContent, [u8; 32])>)> {
        let (sid, opened) = open_series(ctx, t).await?;
        let raw = ctx.contract.view("get_series_table").args_json(json!({ "series_id": sid })).await?.result;
        let raw_str = String::from_utf8(raw.clone())?;
        let hash_view: Value =
            ctx.contract.view("get_series_table_hash").args_json(json!({ "series_id": sid })).await?.json()?;
        let rates: Value = ctx.contract.view("get_rates").args_json(json!({ "series_id": sid })).await?.json()?;
        let mut pack_records = Vec::new();
        let mut reveals = Vec::new();
        for i in 0..packs {
            let who = &buyers[i % buyers.len()];
            let before = series_view(ctx, sid).await?;
            let r = buy(ctx, who, sid).await?;
            let logs = r.logs();
            let ev = events(&logs, "pack_revealed");
            anyhow::ensure!(ev.len() == 1, "pack_revealed attendu");
            pack_records.push(json!({
                "tx_hash": r.outcome().transaction_hash.to_string(),
                "sender": who.id().to_string(),
                "minted_before": before["minted"],
                "mythic_minted_before": before["mythic_minted"],
                "event": ev[0],
                "mythic_drawn": events(&logs, "mythic_drawn"),
            }));
            if let Some(x) = on_pack(&r) {
                reveals.push(x);
            }
        }
        let after = series_view(ctx, sid).await?;
        println!("série {label} (id {sid}) : {packs} boosters, minted final {:?} / {:?}", after["minted"], after["mythic_minted"]);
        Ok((
            json!({
                "label": label,
                "series_id": sid,
                "table_raw": raw_str,
                "table_hash": opened["table_hash"],
                "get_series_table_hash": hash_view,
                "rates": rates,
                "packs": pack_records,
                "minted_final": after["minted"],
                "mythic_minted_final": after["mythic_minted"],
            }),
            reveals,
        ))
    }

    pub async fn reveal(
        ctx: &Ctx,
        sid: u32,
        index: u32,
        card_id: &str,
        sel: &[u8; 32],
        content: &MythicContent,
    ) -> anyhow::Result<Value> {
        let r = ctx
            .owner
            .call(ctx.contract.id(), "reveal_mythic")
            .args_json(json!({
                "series_id": sid, "mythic_index": index, "card_id": card_id,
                "sel": hex::encode(sel), "content": content,
            }))
            .deposit(NearToken::from_near(1))
            .max_gas()
            .transact()
            .await?;
        anyhow::ensure!(r.is_success(), "reveal_mythic : {:?}", r.failures());
        Ok(events(&r.logs(), "mythic_revealed")[0].clone())
    }
}

fn mythic_commit(card_id: &str, sel: &[u8; 32], content: &MythicContent, weight: u32, cap: u32) -> MythicCommitment {
    MythicCommitment {
        commitment: hex::encode(sha(&[card_id.as_bytes(), sel])),
        content_hash: hex::encode(sha(&[&serde_json::to_vec(content).unwrap(), sel])),
        weight,
        cap,
    }
}

/// Événements réels du contrat déployé dans near-sandbox.
#[tokio::test]
async fn sandbox_vectors() -> anyhow::Result<()> {
    use sandbox::*;
    use near_workspaces::types::NearToken;

    let wasm_path = std::env::var("MEMASTER_WASM").map(PathBuf::from).unwrap_or_else(|_| {
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../contract/target/near/memaster.wasm")
    });
    let wasm = std::fs::read(&wasm_path)
        .map_err(|e| anyhow::anyhow!("wasm introuvable ({}) : {e} ; lancez `cargo near build` dans contract/", wasm_path.display()))?;
    let worker = near_workspaces::sandbox().await?;
    let root = worker.root_account()?;
    let mk = |name: String, near: u128| {
        let root = root.clone();
        async move {
            root.create_subaccount(&name)
                .initial_balance(NearToken::from_near(near))
                .transact()
                .await?
                .into_result()
                .map_err(anyhow::Error::from)
        }
    };
    let owner = mk("owner".into(), 100).await?;
    let mc = mk("memaster".into(), 200).await?;
    let contract = mc.deploy(&wasm).await?.into_result()?;
    contract
        .call("new")
        .args_json(json!({ "owner_id": owner.id(), "retry_delay_blocks": 30 }))
        .transact()
        .await?
        .into_result()?;
    let mut buyers = Vec::new();
    for name in ["alice", "bob", "carol"] {
        buyers.push(mk(name.into(), 80).await?);
    }
    let ctx = Ctx { contract, owner };

    // Série 0 : plafonds sur les légendaires et une mythique (cap 2) au contenu Unicode.
    let sel: [u8; 32] = sha(&[b"memaster verifier vectors"]);
    let content = MythicContent {
        title: "Pépé « mythique » 🐸 \"v1\"".into(),
        media: Some("ipfs://bafy/pepe-mythic.png".into()),
        reference: None,
        backing: Some(Backing { asset_id: "nep141:pepe.tkn.near".into(), amount: U128(777) }),
    };
    let t0 = SeriesTable {
        name: "Distribution".into(),
        price: U128(NEAR / 20),
        cards_per_pack: 5,
        rarity_weights: weights_(10, 40, 150, 300, 500),
        cards: vec![
            card_("leg_a", Rarity::Legendary, 1, Some(5), true),
            card_("leg_b", Rarity::Legendary, 1, Some(5), false),
            card_("epic", Rarity::Epic, 1, None, true),
            card_("rare", Rarity::Rare, 1, None, false),
            card_("com_a", Rarity::Common, 3, None, true),
            card_("com_b", Rarity::Common, 1, None, false),
        ],
        mythics: vec![mythic_commit("pepe-mythic", &sel, &content, 1, 2)],
        royalties: vec![Royalty { account_id: ctx.owner.id().as_str().parse().unwrap(), bps: 500 }],
    };
    let (mut s0, _) = run_series(&ctx, "distribution", &t0, &buyers, 90, |_| None).await?;
    // Révélation après coup (la mythique est sortie au moins une fois).
    let sid0 = s0["series_id"].as_u64().unwrap() as u32;
    let mythic_minted: u64 = s0["mythic_minted_final"][0].as_u64().unwrap();
    anyhow::ensure!(mythic_minted > 0, "aucune mythique sortie en 90 boosters");
    let rev = reveal(&ctx, sid0, 0, "pepe-mythic", &sel, &content).await?;
    let commitments: Value =
        ctx.contract.view("get_mythic_commitments").args_json(json!({ "series_id": sid0 })).await?.json()?;
    s0["mythic_revealed"] = json!([rev]);
    s0["mythic_commitments"] = commitments;

    // Série 1 : retombées en cascade (légendaire, épique, rare plafonnées très bas), 10 cartes par booster.
    let t1 = SeriesTable {
        name: "Cascade".into(),
        price: U128(NEAR / 20),
        cards_per_pack: 10,
        rarity_weights: weights_(0, 1, 1, 1, 1),
        cards: vec![
            card_("leg", Rarity::Legendary, 1, Some(1), true),
            card_("epic_a", Rarity::Epic, 2, Some(1), false),
            card_("epic_b", Rarity::Epic, 1, Some(2), false),
            card_("rare", Rarity::Rare, 1, Some(2), false),
            card_("com_cap", Rarity::Common, 5, Some(3), false),
            card_("com", Rarity::Common, 1, None, false),
        ],
        mythics: vec![],
        royalties: vec![],
    };
    let (s1, _) = run_series(&ctx, "cascade", &t1, &buyers, 4, |_| None).await?;

    // Série 2 : chaînes Unicode, échappements JSON, champs nuls ; deux boosters.
    let t2 = SeriesTable {
        name: "Série \"spéciale\" \\ \n\t\u{1}\u{1f}\u{7f} é 🐸 \u{2028} </script>".into(),
        price: U128(NEAR / 20),
        cards_per_pack: 3,
        rarity_weights: weights_(0, 0, 7, 0, 3),
        cards: vec![
            CardDef {
                card_id: "日本-ü".into(),
                title: "Ünïcødé ‘quote’ \u{feff}".into(),
                rarity: Rarity::Epic,
                weight: 2,
                cap: Some(4),
                media: None,
                reference: Some("https://example.org/a?b=c&d=\"e\"".into()),
                backing: Some(Backing { asset_id: "nep141:ü.near".into(), amount: U128(u128::MAX) }),
            },
            CardDef {
                card_id: "plain".into(),
                title: "Plain/€".into(),
                rarity: Rarity::Common,
                weight: 1,
                cap: None,
                media: None,
                reference: None,
                backing: None,
            },
        ],
        mythics: vec![],
        royalties: vec![],
    };
    let (s2, _) = run_series(&ctx, "unicode", &t2, &buyers, 2, |_| None).await?;

    let doc = json!({
        "source": "contrat memaster déployé dans near-sandbox (événements réels)",
        "wasm": wasm_path.display().to_string(),
        "wasm_sha256": hex::encode(sha(&[&wasm])),
        "contract_id": ctx.contract.id().to_string(),
        "series": [s0, s1, s2],
    });
    write_json("sandbox_vectors.json", &doc);

    // Vérification de bout en bout du CLI Python contre le RPC du sandbox.
    if std::env::var("SKIP_PY_RPC").is_err() {
        let url = worker.rpc_addr();
        let cid = ctx.contract.id().to_string();
        let packs0 = doc["series"][0]["packs"].as_array().unwrap();
        let last = &packs0[packs0.len() - 1];
        let mid = &packs0[packs0.len() - 10];
        let casc = &doc["series"][1]["packs"][3];
        let wasm_s = wasm_path.display().to_string();
        let runs: Vec<Vec<String>> = vec![
            vec!["table".into(), "--series".into(), "0".into()],
            vec!["table".into(), "--series".into(), "2".into()],
            vec!["pack".into(), "--tx-hash".into(), last["tx_hash"].as_str().unwrap().into(), "--sender".into(), last["sender"].as_str().unwrap().into()],
            vec!["pack".into(), "--tx-hash".into(), mid["tx_hash"].as_str().unwrap().into(), "--sender".into(), mid["sender"].as_str().unwrap().into()],
            vec!["pack".into(), "--tx-hash".into(), casc["tx_hash"].as_str().unwrap().into(), "--sender".into(), casc["sender"].as_str().unwrap().into()],
            vec!["mythic".into(), "--series".into(), "0".into(), "--index".into(), "0".into()],
            vec!["code".into(), "--wasm".into(), wasm_s],
        ];
        for args in runs {
            let mut cmd = std::process::Command::new("python3");
            cmd.current_dir(verifier_dir()).args(["-m", "memaster_verifier"]).args(&args[..1]);
            cmd.args(["--rpc", &url, "--contract", &cid]).args(&args[1..]);
            let out = cmd.output()?;
            println!("$ python3 -m memaster_verifier {}\n{}{}", args.join(" "), String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr));
            anyhow::ensure!(out.status.success(), "le vérificateur Python a échoué : {:?}", args);
        }
        // Information seulement : une transaction ancienne peut ne plus être servie par un nœud non archive.
        let first = &packs0[0];
        let out = std::process::Command::new("python3")
            .current_dir(verifier_dir())
            .args(["-m", "memaster_verifier", "pack", "--rpc", &url, "--contract", &cid, "--no-state"])
            .args(["--tx-hash", first["tx_hash"].as_str().unwrap(), "--sender", first["sender"].as_str().unwrap()])
            .output()?;
        println!("(info) premier booster par RPC, code {:?}\n{}{}", out.status.code(), String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr));
    }
    Ok(())
}

fn card_(id: &str, rarity: Rarity, weight: u32, cap: Option<u32>, backed: bool) -> CardDef {
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

fn weights_(m: u32, l: u32, e: u32, r: u32, c: u32) -> RarityWeights {
    RarityWeights { mythic: m, legendary: l, epic: e, rare: r, common: c }
}
