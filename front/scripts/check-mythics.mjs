// Garde-fou « mythiques invisibles » (consigne, règle 2) : aucun nom de mythique dans le code, les fichiers
// publics ou le build du front.
//
// 1. Toujours : pas de fiche mythique dans public/catalog.json, pas de fichier `mythique-*` dans public/cards/.
// 2. Si le fichier secret existe (docs/data/secrets/mythiques.json, hors git, écrit par consolider.py) : aucun
//    vrai nom, ticker, id CoinGecko ou adresse de mythique dans src/, public/, dist/, indexer/ et index.html.
//    Les noms et tickers sont cherchés en mot entier ; un homonyme d'une carte publique (même ticker qu'une
//    carte du catalogue, par exemple) est signalé mais ne fait pas échouer.
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
  const publicWords = new Set(
    Object.values(catalog).flatMap((e) => [e.ticker, e.name].filter(Boolean).map((v) => String(v).toLowerCase())),
  );
  const terms = [];
  for (const m of mythics) {
    for (const k of ["nom", "ticker", "coingecko_id", "adresse"]) {
      const v = String(m[k] ?? "").replace(/`/g, "").trim();
      if (v.length < 3 || v === "?") continue;
      const esc = v.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      // Mot entier pour un nom ou un ticker ; sous-chaîne pour un id ou une adresse.
      const re = k === "nom" || k === "ticker" ? new RegExp(`(?<![\\p{L}\\p{N}])${esc}(?![\\p{L}\\p{N}])`, "iu") : new RegExp(esc, "i");
      terms.push({ kind: k, value: v, re, homonym: publicWords.has(v.toLowerCase()) });
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
      if (t.homonym) warnings.push(`${where} (also a public card's name or ticker: homonym, not counted)`);
      else errors.push(where);
    }
  }
} else {
  warnings.push(`secret file not found (${relative(process.cwd(), secrets)}): only structural checks were run`);
}

for (const w of warnings) console.warn(`[check-mythics] warning: ${w}`);
if (errors.length) {
  for (const e of errors) console.error(`[check-mythics] LEAK: ${e}`);
  process.exit(1);
}
// Le terme trouvé n'est jamais affiché : le journal ne doit pas fuiter non plus.
console.log(`[check-mythics] ok (${scanned} files scanned for mythic names)`);
