// Petit indexeur des événements Memaster, pour « Trending », les ventes récentes et les résurrections.
//
// Source : API de transactions de fastnear. `/v0/account` liste les transactions qui touchent le contrat ;
// `/v0/transactions` renvoie chacune avec tous ses reçus et leurs journaux (tirage en 3 blocs compris).
// On ne lit donc que les transactions utiles, sans parcourir les blocs (neardata limite fortement le débit).
// Stockage : SQLite intégré à Node (node:sqlite). API HTTP en lecture seule, CORS ouvert :
//   GET /status                       transactions indexées
//   GET /trending?hours=24&limit=8    cartes les plus vendues ou listées sur la fenêtre
//   GET /sales?limit=20               dernières ventes
//   GET /resurrected                  cartes devenues brûlables (card_resurrected)
//   GET /events?event=…&limit=50      événements bruts
// Lancement : npm run indexer (depuis front/). Variables : voir .env.example (INDEXER_*).

import { mkdirSync } from "node:fs";
import { createServer } from "node:http";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import { eventsFromTx, rankTrending, tokensFromReveal } from "./lib.mjs";

const env = process.env;
const CONTRACT = env.INDEXER_CONTRACT_ID ?? env.VITE_CONTRACT_ID ?? "app2.memaster-demo-j7xg7z.testnet";
const TX_API = env.INDEXER_TX_API ?? "https://tx.test.fastnear.com";
const RPC = env.INDEXER_RPC_URL ?? env.VITE_RPC_URL ?? "https://rpc.testnet.fastnear.com";
const PORT = Number(env.INDEXER_PORT ?? 8787);
const POLL_MS = Number(env.INDEXER_POLL_MS ?? 3000);
// Une transaction n'est lue qu'une fois ce nombre de blocs passé : le tirage (3 blocs) et ses reçus sont finis.
const SETTLE_BLOCKS = 20;
const ici = dirname(fileURLToPath(import.meta.url));
const DB_PATH = env.INDEXER_DB ?? resolve(ici, "data", `${CONTRACT}.sqlite`);

mkdirSync(dirname(DB_PATH), { recursive: true });
const db = new DatabaseSync(DB_PATH);
db.exec(`
  PRAGMA journal_mode = WAL;
  CREATE TABLE IF NOT EXISTS txs (hash TEXT PRIMARY KEY, height INTEGER NOT NULL);
  CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    height INTEGER NOT NULL, ts INTEGER NOT NULL, receipt_id TEXT NOT NULL, log_index INTEGER NOT NULL,
    event TEXT NOT NULL, token_id TEXT, data TEXT NOT NULL
  );
  CREATE UNIQUE INDEX IF NOT EXISTS events_unique ON events (receipt_id, log_index, ifnull(token_id, ''));
  CREATE INDEX IF NOT EXISTS events_event_ts ON events (event, ts);
  CREATE TABLE IF NOT EXISTS tokens (
    token_id TEXT PRIMARY KEY, series_id INTEGER, kind TEXT, card_index INTEGER, card_id TEXT, rarity TEXT
  );
`);

const hasTx = db.prepare("SELECT 1 FROM txs WHERE hash = ?");
const insTx = db.prepare("INSERT OR IGNORE INTO txs (hash, height) VALUES (?, ?)");
const insEvent = db.prepare(
  "INSERT OR IGNORE INTO events (height, ts, receipt_id, log_index, event, token_id, data) VALUES (?, ?, ?, ?, ?, ?, ?)",
);
const insToken = db.prepare(
  "INSERT OR REPLACE INTO tokens (token_id, series_id, kind, card_index, card_id, rarity) VALUES (?, ?, ?, ?, ?, ?)",
);
const countTx = db.prepare("SELECT count(*) AS n, max(height) AS h FROM txs");

// --- Lecture de la chaîne ---------------------------------------------------------------------

async function post(url, body) {
  for (let i = 0; ; i++) {
    try {
      const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
      if (r.status === 429 || r.status >= 500) throw new Error(`${url} ${r.status}`);
      const j = await r.json();
      if (j.error) throw new Error(JSON.stringify(j.error));
      return j;
    } catch (e) {
      if (i >= 5) throw e;
      await sleep(500 * 2 ** i);
    }
  }
}

const rpc = async (method, params) => (await post(RPC, { jsonrpc: "2.0", id: 1, method, params })).result;

async function view(method, args) {
  const r = await rpc("query", {
    request_type: "call_function",
    finality: "final",
    account_id: CONTRACT,
    method_name: method,
    args_base64: Buffer.from(JSON.stringify(args)).toString("base64"),
  });
  return JSON.parse(Buffer.from(r.result).toString());
}

// card_id par (série, index), chargé une fois par série (les tables ouvertes sont immuables).
const series = new Map();
async function loadSeries(id) {
  if (series.has(id)) return;
  const { card_count } = await view("get_series_header", { series_id: id });
  const ids = [];
  for (let from = 0; from < card_count; from += 200) {
    const page = await view("get_series_cards", { series_id: id, from_index: from, limit: 200 });
    ids.push(...page.map((c) => c.card_id));
  }
  series.set(id, ids);
}
const cardIdOf = (s, i) => series.get(s)?.[i];

// --- Boucle d'indexation ----------------------------------------------------------------------

let head = 0;
let total = 0;

async function tick() {
  head = (await rpc("block", { finality: "final" })).header.height;
  const list = await post(`${TX_API}/v0/account`, { account_id: CONTRACT });
  total = list.txs_count ?? 0;
  if ((list.account_txs?.length ?? 0) < total) {
    console.warn(`[indexer] the API returned ${list.account_txs.length} of ${total} transactions (pagination not handled)`);
  }
  const todo = (list.account_txs ?? []).filter(
    (t) => t.tx_block_height + SETTLE_BLOCKS <= head && !hasTx.get(t.transaction_hash),
  );
  for (let i = 0; i < todo.length; i += 20) {
    const part = todo.slice(i, i + 20);
    const { transactions } = await post(`${TX_API}/v0/transactions`, { tx_hashes: part.map((t) => t.transaction_hash) });
    const events = transactions.flatMap((tx) => eventsFromTx(tx, CONTRACT));
    // Ordre global : hauteur, puis pack_id pour départager un même bloc (consigne, § 6).
    events.sort((a, b) => a.height - b.height || (a.data.pack_id ?? 0) - (b.data.pack_id ?? 0));
    for (const e of events) if (e.event === "pack_revealed") await loadSeries(e.data.series_id);
    db.exec("BEGIN");
    try {
      for (const e of events) {
        insEvent.run(e.height, e.ts, e.receipt_id, e.log_index, e.event, e.token_id, JSON.stringify(e.data));
        if (e.event === "pack_revealed") {
          for (const t of tokensFromReveal(e.data, cardIdOf)) {
            insToken.run(t.token_id, t.series_id, t.kind, t.card_index, t.card_id, t.rarity);
          }
        }
      }
      // Une transaction absente de la réponse sera redemandée au tour suivant.
      const got = new Set(transactions.map((tx) => tx.transaction?.hash));
      for (const t of part) if (got.has(t.transaction_hash)) insTx.run(t.transaction_hash, t.tx_block_height);
      db.exec("COMMIT");
    } catch (err) {
      db.exec("ROLLBACK");
      throw err;
    }
    console.log(`[indexer] ${Math.min(i + 20, todo.length)} / ${todo.length} new transactions, ${events.length} events`);
  }
}

async function loop() {
  for (;;) {
    try {
      await tick();
    } catch (e) {
      console.warn("[indexer]", e.message);
    }
    await sleep(POLL_MS);
  }
}

// --- API --------------------------------------------------------------------------------------

const qTrending = db.prepare(`
  SELECT e.event, e.ts, json_extract(e.data, '$.price') AS price, t.card_id, t.kind, t.rarity
  FROM events e JOIN tokens t ON t.token_id = e.token_id
  WHERE e.event IN ('card_sold', 'card_listed') AND e.ts >= ?
`);
const qSales = db.prepare(`
  SELECT e.height, e.ts, e.token_id, json_extract(e.data, '$.price') AS price,
         json_extract(e.data, '$.seller_id') AS seller_id, json_extract(e.data, '$.buyer_id') AS buyer_id,
         t.card_id, t.kind, t.rarity
  FROM events e LEFT JOIN tokens t ON t.token_id = e.token_id
  WHERE e.event = 'card_sold' ORDER BY e.height DESC, e.id DESC LIMIT ?
`);
const qResurrected = db.prepare(`
  SELECT e.height, e.ts, json_extract(e.data, '$.series_id') AS series_id,
         json_extract(e.data, '$.card_index') AS card_index, json_extract(e.data, '$.card_id') AS card_id
  FROM events e WHERE e.event = 'card_resurrected' ORDER BY e.height
`);
const qEvents = db.prepare("SELECT height, ts, event, data FROM events WHERE event = ? ORDER BY height DESC, id DESC LIMIT ?");

function send(res, code, body) {
  res.writeHead(code, {
    "content-type": "application/json",
    "access-control-allow-origin": "*",
    "cache-control": "no-store",
  });
  res.end(JSON.stringify(body));
}

const num = (v, lo, hi, d) => {
  const n = Number(v);
  return v == null || !Number.isFinite(n) ? d : Math.min(hi, Math.max(lo, n));
};

createServer((req, res) => {
  const url = new URL(req.url ?? "/", "http://localhost");
  const p = url.searchParams;
  try {
    switch (url.pathname) {
      case "/status": {
        const c = countTx.get();
        return send(res, 200, { contract: CONTRACT, indexed_txs: c.n, last_tx_height: c.h, contract_txs: total, head });
      }
      case "/trending": {
        const hours = num(p.get("hours"), 1, 24 * 30, 24);
        const rows = qTrending.all(Date.now() - hours * 3600_000);
        return send(res, 200, { hours, items: rankTrending(rows, num(p.get("limit"), 1, 50, 8)) });
      }
      case "/sales":
        return send(res, 200, { items: qSales.all(num(p.get("limit"), 1, 100, 20)).map(hideMythic) });
      case "/resurrected":
        return send(res, 200, { items: qResurrected.all() });
      case "/events": {
        const ev = p.get("event") ?? "";
        if (!/^[a-z_]+$/.test(ev)) return send(res, 400, { error: "event required" });
        const items = qEvents.all(ev, num(p.get("limit"), 1, 500, 50)).map((r) => ({ ...r, data: JSON.parse(r.data) }));
        return send(res, 200, { items });
      }
      default:
        return send(res, 404, { error: "not found" });
    }
  } catch (e) {
    return send(res, 500, { error: String(e.message ?? e) });
  }
}).listen(PORT, () => console.log(`[indexer] ${CONTRACT}, API on http://localhost:${PORT}`));

function hideMythic(r) {
  return r.kind === "mythic" ? { ...r, card_id: null } : r;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

loop();
