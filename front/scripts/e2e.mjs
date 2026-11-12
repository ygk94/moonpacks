// Parcours de bout en bout du front, sur testnet, avec de vraies transactions signées par une clé locale
// (wallet de test, src/near/testKeyWallet.ts). Testnet seulement, comptes buyer seulement, montants minuscules.
//
//   npx playwright install chromium-headless-shell   (une fois)
//   npm run e2e [-- --out DOSSIER] [--only buy,low,burn,market]
//
// Le script lance lui-même Vite (port 5183, VITE_E2E_KEY_WALLET=1) et l'indexeur (port 8797, base à part), puis
// les arrête par PID. Les clés sont lues dans ~/.near-credentials/testnet/buyer{1,2}.<racine>.json et injectées
// dans la page par `page.addInitScript` : jamais dans le dépôt, un log, une variable VITE_* ou une capture.
// Garde-fous : chaque réponse servie par Vite et chaque fichier écrit sont relus, et le script échoue si une clé
// y apparaît.
//
// Parcours :
//   buy     achat d'un pack en série 0 puis en série 1 (dépôt = prix + 0,01605 NEAR), ouverture jusqu'au
//           récapitulatif, stockage rendu, « Verify this pack » jusqu'à la vérification complète
//   low     solde insuffisant : compte implicite neuf crédité de 0,01 NEAR par buyer1, achat refusé avec un message
//           clair, puis compte supprimé (solde rendu à buyer1)
//   burn    burn d'une carte brûlable depuis le détail, jusqu'à `card_redeemed` et le stockage rendu
//   market  mise en vente par buyer1, retrait, nouvelle mise en vente, achat par buyer2 via la confirmation,
//           puis « Trending » et les dernières ventes avec l'indexeur

import { spawn, spawnSync } from "node:child_process";
import { createWriteStream, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { base58Encode, jsonRpc, keyPairFromSecret, signAndSend } from "../src/near/keySigner.ts";

const here = dirname(fileURLToPath(import.meta.url));
const front = resolve(here, "..");
const args = process.argv.slice(2);
const opt = (name, def) => (args.includes(name) ? args[args.indexOf(name) + 1] : def);
const OUT = resolve(opt("--out", join(front, "e2e-captures"))) + "/";
const ONLY = new Set((opt("--only", "buy,low,burn,market") ?? "").split(","));
const ROOT = "memaster-demo-j7xg7z.testnet";
const CONTRACT = process.env.E2E_CONTRACT_ID ?? `app3.${ROOT}`;
const RPC_URL = "https://rpc.testnet.fastnear.com";
const VITE_PORT = Number(opt("--port", 5183));
const INDEXER_PORT = Number(opt("--indexer-port", 8797));
const BASE = `http://127.0.0.1:${VITE_PORT}/`;
const INDEXER = `http://127.0.0.1:${INDEXER_PORT}`;
const LIST_PRICE = "0.00123"; // NEAR
const STORAGE_PREPAID = 10n ** 19n * 1605n; // 1 605 o à 10¹⁹ yocto : 0,01605 NEAR

if (!CONTRACT.endsWith(".testnet")) throw new Error("e2e: testnet only");
mkdirSync(OUT, { recursive: true });

const report = { contract: CONTRACT, started: new Date().toISOString(), flows: {}, txs: [] };
let failed = 0;
const log = (...a) => console.log(...a);
const check = (flow, ok, what) => {
  log(`  ${ok ? "ok  " : "FAIL"} ${what}`);
  (report.flows[flow] ??= { checks: [] }).checks.push({ ok, what });
  if (!ok) failed++;
  return ok;
};

// --- Clés (jamais affichées) -------------------------------------------------------------------------------
const secrets = [];
function loadKey(name) {
  const accountId = `${name}.${ROOT}`;
  const c = JSON.parse(readFileSync(join(homedir(), ".near-credentials", "testnet", `${accountId}.json`), "utf8"));
  secrets.push(c.private_key, c.private_key.replace(/^ed25519:/, ""));
  return { accountId, secretKey: c.private_key };
}
const buyer1 = loadKey("buyer1");
const buyer2 = loadKey("buyer2");
const leaks = (text) => secrets.some((s) => s.length > 20 && text.includes(s));

// --- RPC côté Node (vues, statut des transactions) ---------------------------------------------------------------
const rpc = jsonRpc(RPC_URL);
async function view(method, a = {}) {
  const r = await rpc("query", {
    request_type: "call_function",
    finality: "optimistic",
    account_id: CONTRACT,
    method_name: method,
    args_base64: Buffer.from(JSON.stringify(a)).toString("base64"),
  });
  return JSON.parse(Buffer.from(r.result).toString() || "null");
}
const txStatus = (hash, signer) => rpc("EXPERIMENTAL_tx_status", { tx_hash: hash, sender_account_id: signer, wait_until: "EXECUTED" });
const eventsOfTx = (o) =>
  [...o.transaction_outcome.outcome.logs, ...o.receipts_outcome.flatMap((r) => r.outcome.logs)]
    .filter((l) => l.startsWith("EVENT_JSON:"))
    .map((l) => JSON.parse(l.slice(11)))
    .filter((e) => e.standard === "memaster");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// --- Services lancés pour le test, arrêtés par PID ---------------------------------------------------------------
const children = [];
function start(name, cmd, cmdArgs, env) {
  const out = createWriteStream(join(OUT, `${name}.log`));
  const child = spawn(cmd, cmdArgs, { cwd: front, env: { ...process.env, ...env }, stdio: ["ignore", "pipe", "pipe"] });
  child.stdout.pipe(out);
  child.stderr.pipe(out);
  children.push(child);
  log(`[e2e] ${name} started (pid ${child.pid})`);
  return child;
}
function stopAll() {
  for (const c of children) if (c.exitCode == null) c.kill("SIGTERM");
}
process.on("exit", stopAll);
for (const sig of ["SIGINT", "SIGTERM"]) process.on(sig, () => (stopAll(), process.exit(130)));

async function waitHttp(url, ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    try {
      if ((await fetch(url)).ok) return;
    } catch {
      // pas encore prêt
    }
    await sleep(500);
  }
  throw new Error(`${url} did not answer`);
}

// Fichiers publics (catalogue, visuels) : même préparation que `npm run dev`.
if (spawnSync(process.execPath, ["scripts/prepare-assets.mjs"], { cwd: front, stdio: "inherit" }).status !== 0) throw new Error("prepare-assets failed");
const INDEXER_DB = join(front, "indexer", "data", `e2e-${CONTRACT}.sqlite`);
start("indexer", process.execPath, ["indexer/indexer.mjs"], {
  INDEXER_PORT: String(INDEXER_PORT),
  INDEXER_DB,
  INDEXER_CONTRACT_ID: CONTRACT,
});
start("vite", process.execPath, ["node_modules/vite/bin/vite.js", "--port", String(VITE_PORT), "--strictPort"], {
  VITE_E2E_KEY_WALLET: "1",
  VITE_CONTRACT_ID: CONTRACT,
  VITE_INDEXER_URL: INDEXER,
});
await waitHttp(`${INDEXER}/status`, 30_000);
await waitHttp(BASE, 30_000);

// --- Navigateur ---------------------------------------------------------------------------------------------------
const browser = await chromium.launch();
let step = "setup";
const pageErrors = [];

async function session(key, label) {
  const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 } });
  // La clé n'existe que dans cette page, posée avant le chargement des scripts ; le wallet de test la retire de
  // `window` dès qu'il l'a lue.
  await ctx.addInitScript((k) => {
    window.__MEMASTER_E2E_KEY__ = k;
  }, key);
  const page = await ctx.newPage();
  page.on("pageerror", (e) => pageErrors.push(`${label}: ${e.message}`));
  page.on("response", async (r) => {
    const url = r.url();
    try {
      if (url.startsWith(BASE)) {
        // Garde-fou : la clé ne doit jamais être servie par Vite.
        const ct = r.headers()["content-type"] ?? "";
        if (/javascript|json|html|css|text/.test(ct) && leaks(await r.text())) {
          failed++;
          log(`  FAIL key found in a served file: ${url}`);
        }
        return;
      }
      if (url.startsWith(RPC_URL) && /"send_tx"/.test(r.request().postData() ?? "")) {
        const body = await r.json();
        const res = body.result;
        const hash = res?.transaction?.hash ?? res?.transaction_outcome?.id;
        const entry = {
          step,
          account: label,
          hash: hash ?? null,
          method: res?.transaction?.actions?.[0]?.FunctionCall?.method_name ?? null,
          error: body.error ? JSON.stringify(body.error.data ?? body.error.cause ?? body.error).slice(0, 200) : null,
          events: res ? eventsOfTx(res).map((e) => e.event) : [],
        };
        report.txs.push(entry);
        log(`  tx ${entry.method ?? "?"} ${entry.hash ?? "(rejected)"} ${entry.error ?? entry.events.join(",")}`);
      }
    } catch {
      // réponse illisible (navigation) : ignorée
    }
  });
  return { ctx, page };
}

async function shot(page, name) {
  await page.screenshot({ path: OUT + name, fullPage: false });
}

async function connect(page) {
  await page.goto(BASE + "#/shop");
  await page.locator(".header__wallet").getByRole("button", { name: "Connect wallet" }).click();
  const opt = page.locator(".modal").getByRole("button", { name: /Test key \(e2e\)/ });
  await opt.waitFor({ timeout: 20_000 });
  await sleep(600); // fin de l'animation de la fenêtre
  await shot(page, "00-wallets.png");
  await opt.click({ timeout: 10_000 });
  await page.locator(".btn--account").waitFor({ timeout: 20_000 });
}

async function runToSummary(page, ms = 120_000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (await page.getByText("Your pack", { exact: true }).count()) return true;
    if (await page.getByText("The pack was not bought").count()) return false;
    if (await page.locator(".reveal").count()) await page.locator(".reveal").first().click({ force: true }).catch(() => {});
    await sleep(250);
  }
  return false;
}

/** Attend que l'indexeur (port à part) ait lu le tirage du pack : le rejeu complet en a besoin. */
async function waitIndexed(packId, ms = 240_000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    const r = await fetch(`${INDEXER}/events?event=pack_revealed&limit=500`).then((x) => x.json()).catch(() => ({ items: [] }));
    if (r.items.some((e) => Number(e.data.pack_id) === packId)) return true;
    await sleep(3000);
  }
  return false;
}

/** « Verify this pack » jusqu'à la vérification complète (rejeu de la série avec l'historique de l'indexeur). */
async function verifyFully(page, packId, prefix) {
  const indexed = await waitIndexed(packId);
  for (let attempt = 0; attempt < 4; attempt++) {
    if (attempt > 0) {
      // Nouvelle ouverture du même pack (rejeu), pour un bouton « Verify this pack » neuf.
      await page.locator(".opening__top").getByRole("button", { name: "Close" }).click();
      await sleep(10_000);
      await page.goto(BASE + `#/open?pack=${packId}`);
      if (!(await runToSummary(page, 60_000))) continue;
    }
    await page.getByRole("button", { name: "Verify this pack" }).click();
    await page.locator(".verify__result").waitFor({ timeout: 90_000 });
    const v = await page.locator(".verify__result").innerText();
    if (/✗/.test(v)) return { ok: false, text: v.split("\n")[0] };
    if (/fully verified/.test(v)) {
      await page.locator(".verify__result").scrollIntoViewIfNeeded();
      await shot(page, `${prefix}-verify.png`);
      const checks = (v.match(/✓/g) ?? []).length - 1;
      return { ok: true, text: `${v.split("\n")[0]} (${checks} checks)` };
    }
  }
  return { ok: false, text: indexed ? "not fully verified" : "pack not indexed in time" };
}

async function buyPack(page, seriesName, seriesId, prefix) {
  const flow = "buy";
  step = `buy series ${seriesId}`;
  log(`[buy] series ${seriesId} (${seriesName})`);
  const s = await view("get_series", { series_id: seriesId });
  check(flow, BigInt(s.required_deposit) - BigInt(s.price) === STORAGE_PREPAID, `series ${seriesId}: required deposit = price + 0.01605 NEAR`);
  await page.goto(BASE + "#/shop");
  const offer = page.locator(".offer", { has: page.getByRole("heading", { name: seriesName }) });
  await offer.getByRole("button", { name: "Buy pack" }).click();
  await shot(page, `${prefix}-confirm.png`);
  const confirmText = await offer.locator(".confirm").innerText();
  check(flow, confirmText.includes("0.01605 NEAR"), `series ${seriesId}: confirmation shows the 0.01605 NEAR storage deposit`);
  const txBefore = report.txs.length;
  await offer.getByRole("button", { name: "Buy and open" }).click();
  const done = await runToSummary(page);
  if (!check(flow, done, `series ${seriesId}: opening reaches the summary`)) {
    await shot(page, `${prefix}-error.png`);
    return null;
  }
  await sleep(800);
  await shot(page, `${prefix}-summary.png`);
  const title = await page.locator(".opening__title").innerText();
  const packId = Number(/Pack #(\d+)/.exec(title)?.[1]);
  const tx = report.txs.slice(txBefore).find((t) => t.method === "buy_pack");
  const full = tx?.hash ? await txStatus(tx.hash, buyer1.accountId) : null;
  const action = full?.transaction?.actions?.[0]?.FunctionCall;
  check(flow, action?.deposit === s.required_deposit, `series ${seriesId}: attached deposit ${action?.deposit} = required ${s.required_deposit}`);
  const revealed = full && eventsOfTx(full).find((e) => e.event === "pack_revealed")?.data?.[0];
  const summaryText = await page.locator(".summary").innerText();
  const refundLine = /Unused storage deposit returned[^\n]*/.exec(summaryText)?.[0];
  check(flow, !!refundLine, `series ${seriesId}: summary shows the returned storage (${refundLine ?? "missing"})`);
  const v = await verifyFully(page, packId, prefix);
  check(flow, v.ok, `series ${seriesId}: pack #${packId} ${v.text}`);
  await page.locator(".opening__top").getByRole("button", { name: "Close" }).click().catch(() => {});
  report.flows[flow][`series${seriesId}`] = { packId, tx: tx?.hash, storageRefund: revealed?.storage?.refund ?? null, verify: v.text };
  return packId;
}

// --- Parcours -----------------------------------------------------------------------------------------------------
const b1 = await session(buyer1, "buyer1");
await connect(b1.page);
await shot(b1.page, "00-connected.png");
let pack0 = null;

if (ONLY.has("buy")) {
  pack0 = await buyPack(b1.page, "Memaster Entry", 0, "01-s0");
  await buyPack(b1.page, "Memaster Standard", 1, "02-s1");
}

if (ONLY.has("low")) {
  const flow = "low";
  step = "low balance";
  log("[low] insufficient balance (fresh implicit account with 0.01 NEAR)");
  const kp = await crypto.subtle.generateKey({ name: "Ed25519" }, true, ["sign", "verify"]);
  const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
  const pub = new Uint8Array(await crypto.subtle.exportKey("raw", kp.publicKey));
  const raw = new Uint8Array(64);
  raw.set(pkcs8.slice(16, 48));
  raw.set(pub, 32);
  const tmp = { accountId: Buffer.from(pub).toString("hex"), secretKey: `ed25519:${base58Encode(raw)}` };
  secrets.push(tmp.secretKey, tmp.secretKey.slice(8));
  const k1 = await keyPairFromSecret(buyer1.secretKey);
  const fund = await signAndSend(rpc, k1, buyer1.accountId, tmp.accountId, [{ type: "Transfer", deposit: String(10n ** 22n) }]);
  report.txs.push({ step, account: "buyer1", method: "transfer 0.01 NEAR", hash: fund.transaction.hash, error: null, events: [] });
  log(`  tx transfer ${fund.transaction.hash}`);
  await sleep(2000);
  const low = await session(tmp, "empty");
  try {
    await connect(low.page);
    await low.page.goto(BASE + "#/shop");
    const offer = low.page.locator(".offer", { has: low.page.getByRole("heading", { name: "Memaster Entry" }) });
    await offer.getByRole("button", { name: "Buy pack" }).click();
    await offer.getByRole("button", { name: "Buy and open" }).click();
    await low.page.getByText("The pack was not bought").waitFor({ timeout: 60_000 });
    await sleep(500);
    await shot(low.page, "03-low-balance.png");
    const msg = await low.page.locator(".opening__message p").first().innerText();
    check(flow, /Your wallet balance is too low for this transaction\./.test(msg), `clear message: ${msg}`);
    report.flows[flow].message = msg;
  } finally {
    await low.ctx.close();
    const kt = await keyPairFromSecret(tmp.secretKey);
    const del = await signAndSend(rpc, kt, tmp.accountId, tmp.accountId, [{ type: "DeleteAccount", beneficiaryId: buyer1.accountId }]);
    report.txs.push({ step, account: "empty", method: "delete_account → buyer1", hash: del.transaction.hash, error: null, events: [] });
    log(`  tx delete_account ${del.transaction.hash}`);
  }
}

/** Cartes d'un pack : jeton, brûlable ou non, mythique ou non. */
async function packCards(packId) {
  const p = await view("get_pack", { pack_id: packId });
  const out = [];
  for (const d of p.draws) {
    const token = String(packId * 10 + d.slot);
    const c = await view("get_card", { token_id: token });
    if (c) out.push({ token, burnable: !!c.backing, mythic: c.kind === "mythic", listed: !!c.listing, owner: c.owner_id });
  }
  return out;
}

async function openCard(page, token) {
  await page.goto(BASE + "#/shop");
  await page.goto(BASE + "#/collection");
  const item = page.locator(`.grid__item[data-token="${token}"]`);
  await item.waitFor({ timeout: 30_000 });
  await item.locator(".card").first().click();
  await page.locator(".detail").waitFor({ timeout: 15_000 });
  await sleep(1500);
}

if (ONLY.has("burn")) {
  const flow = "burn";
  step = "burn";
  log("[burn] burnable card from the detail");
  if (pack0 == null) {
    const ids = await view("get_packs_for_owner", { account_id: buyer1.accountId, from_index: 0, limit: 100 });
    pack0 = ids[ids.length - 1];
  }
  const target = (await packCards(pack0)).find((c) => c.burnable && !c.listed && c.owner === buyer1.accountId);
  if (check(flow, !!target, `burnable card in pack #${pack0}: ${target?.token}`)) {
    await openCard(b1.page, target.token);
    await b1.page.getByRole("button", { name: /Burn/ }).first().click();
    await shot(b1.page, "04-burn-confirm.png");
    const txBefore = report.txs.length;
    await b1.page.getByRole("button", { name: "Burn the card" }).click();
    const result = b1.page.locator(".modal .success, .modal .burnbox .error, .modal .detail .error").first();
    await result.waitFor({ timeout: 120_000 });
    await sleep(800);
    await shot(b1.page, "05-burn-done.png");
    const text = await result.innerText();
    const tx = report.txs.slice(txBefore).find((t) => t.method === "redeem");
    check(flow, !!tx?.events.includes("redeem_started") && !!tx?.events.includes("card_redeemed"), `events: ${tx?.events.join(", ")}`);
    check(flow, /Card burned/.test(text) && /freed storage deposit \([\d.]+ NEAR\) was returned/.test(text), `shown: ${text}`);
    const full = tx?.hash ? await txStatus(tx.hash, buyer1.accountId) : null;
    const redeemed = full && eventsOfTx(full).find((e) => e.event === "card_redeemed")?.data?.[0];
    report.flows[flow].result = { token: target.token, tx: tx?.hash, storage_refund: redeemed?.storage_refund ?? null, shown: text };
    await b1.page.keyboard.press("Escape");
  }
}

if (ONLY.has("market")) {
  const flow = "market";
  step = "market";
  log("[market] list, delist, list again (buyer1), buy (buyer2), trending");
  const ids = await view("get_packs_for_owner", { account_id: buyer1.accountId, from_index: 0, limit: 100 });
  let target = null;
  for (const id of [pack0, ...ids.slice().reverse()].filter((x) => x != null)) {
    target = (await packCards(id)).find((c) => !c.burnable && !c.mythic && !c.listed && c.owner === buyer1.accountId);
    if (target) break;
  }
  if (check(flow, !!target, `card to sell: #${target?.token}`)) {
    const T = target.token;
    const p = b1.page;
    await openCard(p, T);
    step = "market list";
    await p.locator("#price").fill(LIST_PRICE);
    await p.getByRole("button", { name: "List", exact: true }).click();
    await p.getByRole("button", { name: "Remove from market" }).waitFor({ timeout: 60_000 });
    await sleep(800);
    await shot(p, "06-listed.png");
    check(flow, /Listed for 0\.00123 NEAR/.test(await p.locator(".detail").innerText()), "listed for 0.00123 NEAR");
    step = "market delist";
    await p.getByRole("button", { name: "Remove from market" }).click();
    await p.getByRole("button", { name: "List", exact: true }).waitFor({ timeout: 60_000 });
    await shot(p, "07-delisted.png");
    check(flow, (await view("get_listing", { token_id: T })) == null, "listing removed on-chain");
    step = "market list again";
    await p.locator("#price").fill(LIST_PRICE);
    await p.getByRole("button", { name: "List", exact: true }).click();
    await p.getByRole("button", { name: "Remove from market" }).waitFor({ timeout: 60_000 });
    check(flow, (await view("get_listing", { token_id: T }))?.price === "1230000000000000000000", "listed again on-chain");
    await p.keyboard.press("Escape");

    step = "market buy";
    const b2 = await session(buyer2, "buyer2");
    await connect(b2.page);
    await b2.page.goto(BASE + "#/market");
    const row = b2.page.locator(`.listing[data-token="${T}"]`);
    await row.waitFor({ timeout: 60_000 });
    await row.getByRole("button", { name: "Buy", exact: true }).click();
    await b2.page.locator(".buy-confirm").waitFor({ timeout: 10_000 });
    await sleep(1500);
    await shot(b2.page, "08-buy-confirm.png");
    const conf = await b2.page.locator(".buy-confirm").innerText();
    check(flow, /You pay exactly 0\.00123 NEAR/.test(conf), "confirmation shows the exact price");
    await b2.page.getByRole("button", { name: /^Confirm and buy/ }).click();
    const msg = b2.page.locator(".market .success, .market .error").first();
    await msg.waitFor({ timeout: 90_000 });
    await shot(b2.page, "09-bought.png");
    const bought = await msg.innerText();
    check(flow, /You bought/.test(bought), `shown: ${bought}`);
    check(flow, (await view("get_card", { token_id: T }))?.owner_id === buyer2.accountId, "buyer2 owns the card on-chain");

    step = "market trending";
    let indexed = false;
    for (let i = 0; i < 60 && !indexed; i++) {
      const s = await fetch(`${INDEXER}/sales?limit=50`).then((r) => r.json()).catch(() => ({ items: [] }));
      indexed = s.items.some((x) => x.token_id === T);
      if (!indexed) await sleep(5000);
    }
    check(flow, indexed, "sale indexed by the indexer (separate port)");
    await b2.page.goto(BASE + "#/shop");
    await b2.page.goto(BASE + "#/market");
    await b2.page.locator(".sales").waitFor({ timeout: 30_000 }).catch(() => {});
    await sleep(2000);
    await b2.page.screenshot({ path: OUT + "10-trending-sales.png", fullPage: true });
    const page = await b2.page.locator(".page.market").innerText();
    check(flow, /Trending/.test(page) && /\d+ sold/.test(page), "Trending shows sales from the indexer");
    check(flow, /Recent sales[\s\S]*0\.00123 NEAR/.test(page), "Recent sales shows the 0.00123 NEAR sale");
    report.flows[flow].token = T;
    await b2.ctx.close();
  }
}

await b1.ctx.close();
await browser.close();

// Garde-fou final : aucune clé dans les fichiers écrits.
report.pageErrors = pageErrors;
report.finished = new Date().toISOString();
writeFileSync(OUT + "report.json", JSON.stringify(report, null, 2));
for (const f of readdirSync(OUT)) {
  const p = join(OUT, f);
  if (statSync(p).isFile() && /\.(json|log|txt)$/.test(f) && leaks(readFileSync(p, "utf8"))) {
    failed++;
    log(`FAIL key found in ${p}`);
  }
}
if (pageErrors.length) log(`page errors:\n  ${pageErrors.join("\n  ")}`);
log(failed ? `\n${failed} problem(s), captures in ${OUT}` : `\nall e2e flows ok, captures in ${OUT}`);
stopAll();
process.exit(failed ? 1 : 0);
