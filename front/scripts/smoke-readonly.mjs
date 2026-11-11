// Parcours en lecture seule du front dans un navigateur sans tête (Playwright), contre le contrat configuré.
// Aucune transaction : aucun wallet n'est connecté, `call` refuse toute signature, et toute requête
// broadcast_tx / send_tx est signalée comme erreur.
//
// Prérequis : `npm run dev` (et `npm run indexer` pour la vérification complète), puis
//   npx playwright install chromium-headless-shell   (une fois)
//   npm run smoke [-- --out DOSSIER] [--base http://127.0.0.1:5173/] [--account compte.testnet]
// Captures dans smoke-captures/ (ignoré par git). Code de sortie 1 si une page a une erreur, hors cours
// publics (CoinGecko limite le débit sans clé, ce qui n'est pas une erreur du front).

import { mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { chromium } from "playwright";

const args = process.argv.slice(2);
const opt = (name, def) => (args.includes(name) ? args[args.indexOf(name) + 1] : def);
const BASE = opt("--base", "http://127.0.0.1:5173/");
const OUT = resolve(opt("--out", "smoke-captures")) + "/";
const ACCOUNT = opt("--account", "buyer1.memaster-demo-j7xg7z.testnet");
mkdirSync(OUT, { recursive: true });
let failed = 0;
const log = (...a) => console.log(...a);

const browser = await chromium.launch();

async function newPage({ account = false, mobile = false } = {}) {
  const ctx = await browser.newContext(
    mobile ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { viewport: { width: 1360, height: 900 } },
  );
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => m.type() === "error" && errors.push(`console: ${m.text()}`));
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("requestfailed", (r) => errors.push(`requestfailed: ${r.url()} ${r.failure()?.errorText}`));
  page.on("response", (r) => r.status() >= 400 && errors.push(`http ${r.status()}: ${r.url()}`));
  // Garde-fou : aucune requête de signature ou d'envoi de transaction ne doit partir.
  page.on("request", (r) => {
    const body = r.postData() ?? "";
    if (/broadcast_tx|send_tx/.test(body)) errors.push(`TRANSACTION ATTEMPT: ${r.url()}`);
  });
  if (account) {
    // Compte affiché sans wallet : on remplace seulement l'état initial `accountId` du module servi par Vite.
    // `call` exige toujours un wallet, donc aucune signature n'est possible.
    await page.route("**/src/near/wallet.tsx*", async (route) => {
      const res = await route.fetch();
      let body = await res.text();
      const before = body;
      body = body.replace("const [accountId, setAccountId] = useState(null);", `const [accountId, setAccountId] = useState(${JSON.stringify(ACCOUNT)});`);
      if (body === before) throw new Error("wallet stub failed");
      await route.fulfill({ response: res, body });
    });
  }
  return { ctx, page, errors };
}

// Cours publics : CoinGecko renvoie 429 sans en-tête CORS quand on dépasse son débit gratuit.
const EXTERNAL = /favicon|api\.coingecko\.com|api\.dexscreener\.com|Failed to load resource: net::ERR_FAILED/;

function flush(name, errors) {
  const useful = errors.filter((e) => !EXTERNAL.test(e));
  const external = errors.length - useful.length;
  if (useful.length) failed++;
  log(`[${name}] ${useful.length ? "ERRORS:\n  " + useful.join("\n  ") : "no error"}${external ? ` (${external} public price API message(s) ignored)` : ""}`);
}

async function bodyText(page) {
  return page.evaluate(() => document.body.innerText);
}

function rules(name, text) {
  // Règles de la consigne : pas de rendement, pas de « garanti » affirmatif, bandeau présent.
  if (!/Demo · NEAR testnet/.test(text)) (failed++, log(`[${name}] MISSING testnet banner`));
  const bad = text.match(/\b\d+(\.\d+)?\s?%[^\n]*(profit|return|value|roi)|profitable|guaranteed value(?! )/gi);
  if (bad) (failed++, log(`[${name}] suspicious wording: ${bad.join(" | ")}`));
  if (/pity/i.test(text)) (failed++, log(`[${name}] mentions pity`));
}

// 1. Boutique
{
  const { ctx, page, errors } = await newPage();
  await page.goto(BASE + "#/shop");
  await page.getByText(/NEAR$/).first().waitFor({ timeout: 20000 });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: OUT + "01-shop.png", fullPage: true });
  const t = await bodyText(page);
  rules("shop", t);
  log("[shop] price:", (t.match(/[\d.]+ NEAR\n/) ?? ["?"])[0].trim(), "| usd:", (t.match(/≈ \$[\d.]+/) ?? ["none"])[0], "| rush:", /Gold rush/.test(t));
  log("[shop] storage line:", (t.match(/\+ storage deposit[^\n]*/) ?? ["?"])[0]);
  flush("shop", errors);
  await ctx.close();
}

// 2. Transparence
{
  const { ctx, page, errors } = await newPage();
  await page.goto(BASE + "#/rates");
  await page.locator("table.table tbody tr").first().waitFor({ timeout: 30000 });
  await page.waitForFunction(() => !document.body.innerText.includes("Contract code hash\n…"), null, { timeout: 20000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: OUT + "02-rates.png", fullPage: true });
  const t = await bodyText(page);
  rules("rates", t);
  const rows = await page.locator("table.table tbody tr").allInnerTexts();
  log("[rates] rarities:\n  " + rows.join("\n  "));
  log("[rates] code hash:", (t.match(/Contract code hash\n(\S+)/) ?? [, "?"])[1], "| table hash:", (t.match(/table hash\n(\S+)/) ?? [, "?"])[1]);
  // Mythiques : filtre « Mythic », toutes en « ? ».
  await page.getByRole("button", { name: "Mythic" }).last().click();
  await page.waitForTimeout(800);
  const mythRows = await page.locator(".rates-list__row").allInnerTexts();
  log(`[rates] mythic rows: ${mythRows.length}, all "?": ${mythRows.every((r) => r.startsWith("?"))}`);
  const imgs = await page.locator(".rates-list__row img").evaluateAll((els) => els.map((e) => e.getAttribute("src")));
  log(`[rates] mythic images: ${[...new Set(imgs)].join(", ")}`);
  await page.screenshot({ path: OUT + "03-rates-mythic.png", fullPage: false });
  flush("rates", errors);
  await ctx.close();
}

// 3. Rejeu et vérification d'un pack existant
for (const packId of [0, 12, 30]) {
  const { ctx, page, errors } = await newPage();
  await page.goto(BASE + `#/open?pack=${packId}`);
  const deadline = Date.now() + 60000;
  while (Date.now() < deadline) {
    if (await page.getByText("Your pack", { exact: true }).count()) break;
    if (await page.locator(".reveal").count()) await page.locator(".reveal").click({ force: true }).catch(() => {});
    await page.waitForTimeout(250);
  }
  await page.getByText("Your pack", { exact: true }).waitFor({ timeout: 5000 });
  await page.waitForTimeout(1200);
  const summary = await page.locator(".summary__item").allInnerTexts();
  log(`[open ${packId}] cards: ${summary.map((s) => s.replace(/\n/g, " ")).join(" | ")}`);
  await page.getByRole("button", { name: "Verify this pack" }).click();
  await page.locator(".verify__result").waitFor({ timeout: 60000 });
  const v = await page.locator(".verify__result").innerText();
  log(`[open ${packId}] verify: ${v.split("\n")[0]} | ${(v.match(/✗[^\n]*/g) ?? []).join(" ; ") || "no failed check"}`);
  if (/✗/.test(v)) failed++;
  if (packId === 12) {
    await page.locator(".verify__result").scrollIntoViewIfNeeded();
    await page.screenshot({ path: OUT + "04-open-verify-pack12.png", fullPage: false });
  }
  rules(`open ${packId}`, await bodyText(page));
  flush(`open ${packId}`, errors);
  await ctx.close();
}

// 4. Collection d'un compte (lecture seule)
{
  const { ctx, page, errors } = await newPage({ account: true });
  await page.goto(BASE + "#/collection");
  await page.locator(".grid__item").first().waitFor({ timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: OUT + "05-collection.png", fullPage: true });
  const t = await bodyText(page);
  rules("collection", t);
  log("[collection] tabs:", (t.match(/Cards \(\d+\)/) ?? ["?"])[0], (t.match(/Packs \(\d+\)/) ?? ["?"])[0]);
  const chips = await page.locator(".filters .chip").allInnerTexts();
  log("[collection] filters:", chips.join(" / "));
  // Filtre brûlable
  await page.getByLabel("Burnable only").check();
  await page.waitForTimeout(500);
  log("[collection] burnable cards:", await page.locator(".grid__item").count());
  // Détail d'une carte brûlable
  await page.locator(".grid__item .card").first().click();
  await page.locator(".detail").waitFor({ timeout: 10000 });
  await page.waitForTimeout(3000);
  const d = await page.locator(".detail").innerText();
  log("[collection] detail:", d.replace(/\n/g, " | ").slice(0, 400));
  await page.screenshot({ path: OUT + "06-card-detail.png", fullPage: false });
  // Le bouton Burn demande une confirmation, qu'on annule (aucune transaction).
  const burn = page.getByRole("button", { name: /Burn/ });
  if (await burn.count()) {
    await burn.first().click();
    const confirm = await page.locator(".burnbox--confirm").innerText().catch(() => "");
    log("[collection] burn confirm shown:", !!confirm, "|", confirm.replace(/\n/g, " ").slice(0, 160));
    await page.screenshot({ path: OUT + "07-burn-confirm.png", fullPage: false });
    await page.getByRole("button", { name: "Keep it" }).click();
  }
  await page.keyboard.press("Escape");
  await page.getByLabel("Burnable only").uncheck();
  await page.getByRole("button", { name: /^Packs/ }).click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: OUT + "08-collection-packs.png", fullPage: false });
  flush("collection", errors);
  await ctx.close();
}

// 5. Marché et mentions légales
for (const [name, hash, file] of [["market", "#/market", "09-market.png"], ["legal", "#/legal", "10-legal.png"]]) {
  const { ctx, page, errors } = await newPage();
  await page.goto(BASE + hash);
  await page.waitForTimeout(4000);
  await page.screenshot({ path: OUT + file, fullPage: true });
  const t = await bodyText(page);
  rules(name, t);
  log(`[${name}]`, t.replace(/\n+/g, " | ").slice(0, 300));
  flush(name, errors);
  await ctx.close();
}

// 6. Téléphone : boutique et connexion (liste des wallets, sans se connecter)
{
  const { ctx, page, errors } = await newPage({ mobile: true });
  await page.goto(BASE + "#/shop");
  await page.waitForTimeout(4000);
  await page.screenshot({ path: OUT + "11-shop-mobile.png", fullPage: true });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  log("[mobile] horizontal overflow px:", overflow);
  const btn = page.getByRole("button", { name: /Connect/ }).first();
  await btn.click();
  await page.waitForTimeout(2500);
  await page.screenshot({ path: OUT + "12-connect-mobile.png", fullPage: false });
  log("[mobile] connect dialog:", (await bodyText(page)).replace(/\n+/g, " | ").slice(0, 400));
  flush("mobile", errors);
  await ctx.close();
}

await browser.close();
log(failed ? `\n${failed} problem(s), captures in ${OUT}` : `\nall pages ok, captures in ${OUT}`);
process.exit(failed ? 1 : 0);
