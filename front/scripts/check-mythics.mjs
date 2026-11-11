// Garde-fou « mythiques invisibles » (consigne, règle 2) : aucun nom de mythique dans le code, les fichiers
// publics ou le build du front.
//
// 1. Toujours : pas de fiche mythique dans public/catalog.json, pas de fichier `mythique-*` dans public/cards/.
// 2. Si le fichier secret existe (docs/data/secrets/mythiques.json, hors git, écrit par consolider.py) : aucun
//    vrai nom, ticker, id CoinGecko ou adresse de mythique dans src/, public/, dist/, indexer/ et index.html.
//    Les noms et tickers sont cherchés en mot entier. Une occurrence qui n'est qu'à l'intérieur du nom, du
//    ticker, de l'id ou de l'adresse d'une carte publique (homonyme, dérivé) est signalée mais ne fait pas échouer.
//
// Usage : node scripts/check-mythics.mjs [--secrets FICHIER] [--root DOSSIER]   (code de sortie 1 si fuite)

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ici = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const root = resolve(opt("--root", resolve(ici, "..")));
const secrets = resolve(opt("--secrets", resolve(ici, "..", "..", "docs", "data", "secrets", "mythiques.json")));

const errors = [];
const warnings = [];
const homonyms = new Set();

// --- 1. Contrôles de structure ----------------------------------------------------------------

const catalogPath = join(root, "public", "catalog.json");
let catalog = {};
if (existsSync(catalogPath)) {
  catalog = JSON.parse(readFileSync(catalogPath, "utf8"));
  for (const id of Object.keys(catalog)) if (id.startsWith("mythique")) errors.push(`public/catalog.json: mythic entry ${id}`);
}
const cardsDir = join(root, "public", "cards");
if (existsSync(cardsDir)) {
  for (const f of readdirSync(cardsDir)) if (f.startsWith("mythique")) errors.push(`public/cards/${f}: mythic file must not be public`);
}

// --- 2. Vrais noms, si le fichier secret est là ------------------------------------------------

function files(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const f of readdirSync(dir)) {
    if (f === "node_modules" || f === "data" || f.startsWith(".")) continue;
    const p = join(dir, f);
    if (statSync(p).isDirectory()) files(p, out);
    else if (/\.(ts|tsx|js|mjs|json|svg|html|css|md)$/.test(f)) out.push(p);
  }
  return out;
}

let scanned = 0;
if (existsSync(secrets)) {
  const raw = JSON.parse(readFileSync(secrets, "utf8"));
  const mythics = raw.mythiques ?? raw;
  // Textes publics : id, ticker, nom, adresse et id CoinGecko de chaque carte du catalogue. Le catalogue contient
  // des cartes dont le nom ou l'id contient celui d'une mythique (copies, dérivés) : ces occurrences-là sont
  // retirées du texte avant la recherche, et seulement signalées.
  // Les visuels de art/ abrègent l'id (`abreger_id` : 10 premiers caractères, « … », 8 derniers) et le nom
  // perd ses marques finales (« † ») : ces formes-là comptent aussi comme publiques.
  const variants = (v) => {
    const s = String(v);
    const out = [s, s.replace(/[^\p{L}\p{N}]+$/u, "")];
    if (s.length > 22) out.push(`${s.slice(0, 10)}…${s.slice(-8)}`);
    return out.filter(Boolean);
  };
  const publicTexts = [
    ...new Set(
      Object.entries(catalog).flatMap(([id, e]) => [id, e.ticker, e.name, e.address, e.coingecko].filter(Boolean).flatMap(variants)),
    ),
  ];
  const escRe = (v) => v.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const terms = [];
  for (const m of mythics) {
    for (const k of ["nom", "ticker", "coingecko_id", "adresse"]) {
      const v = String(m[k] ?? "").replace(/`/g, "").trim();
      if (v.length < 3 || v === "?") continue;
      const esc = v.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      // Mot entier pour un nom ou un ticker ; sous-chaîne pour un id ou une adresse.
      const re = k === "nom" || k === "ticker" ? new RegExp(`(?<![\\p{L}\\p{N}])${esc}(?![\\p{L}\\p{N}])`, "iu") : new RegExp(esc, "i");
      // Textes publics qui contiennent le terme, du plus long au plus court, en une seule expression.
      const hosts = publicTexts.filter((p) => re.test(p)).sort((a, b) => b.length - a.length);
      const strip = hosts.length ? new RegExp(hosts.map(escRe).join("|"), "giu") : null;
      terms.push({ kind: k, re, strip });
    }
  }
  const targets = [
    ...files(join(root, "src")),
    ...files(join(root, "public")),
    ...files(join(root, "dist")),
    ...files(join(root, "indexer")),
    ...files(join(root, "scripts")).filter((p) => !p.endsWith("check-mythics.mjs")),
    join(root, "index.html"),
  ].filter(existsSync);
  for (const p of targets) {
    const text = readFileSync(p, "utf8");
    scanned++;
    for (const t of terms) {
      if (!t.re.test(text)) continue;
      const where = `${relative(root, p)}: mythic ${t.kind} found`;
      if (t.strip && !t.re.test(text.replace(t.strip, " "))) homonyms.add(relative(root, p));
      else errors.push(where);
    }
  }
} else {
  warnings.push(`secret file not found (${relative(process.cwd(), secrets)}): only structural checks were run`);
}

if (homonyms.size) {
  // Un fichier par ligne serait trop long (des centaines de visuels), et les noms de fichiers trahiraient le
  // terme : on compte seulement.
  const list = [...homonyms];
  warnings.push(
    `${list.length} file(s) contain a mythic term only inside a public card's name, ticker or id (homonym, not counted)`,
  );
}
for (const w of warnings) console.warn(`[check-mythics] warning: ${w}`);
if (errors.length) {
  for (const e of errors) console.error(`[check-mythics] LEAK: ${e}`);
  process.exit(1);
}
// Le terme trouvé n'est jamais affiché : le journal ne doit pas fuiter non plus.
console.log(`[check-mythics] ok (${scanned} files scanned for mythic names)`);
