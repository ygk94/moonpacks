// Prépare les fichiers publics du front, sans rien versionner :
// - public/catalog.json : fiche publique de chaque carte (ticker, nom, chaîne, état), mythiques exclues ;
// - public/cards/*.svg : visuels générés par art/ (version anglaise), dos « ? » des mythiques compris.
// Relancé à chaque `npm run dev` / `build`, mais ne régénère que si le catalogue ou art/ a changé.

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ici = dirname(fileURLToPath(import.meta.url));
const front = resolve(ici, "..");
const depot = resolve(front, "..");
const catalogue = join(depot, "docs", "data", "catalogue-v2.json");
const art = join(depot, "art");
const sortieCartes = join(front, "public", "cards");
const sortieCatalogue = join(front, "public", "catalog.json");

// --- catalogue public -------------------------------------------------------------------------

function chaine(c) {
  const v = (c.chaine_normalisee || c.chaine || "").trim();
  if (!v || v === "?" || v.startsWith("à vérifier")) return null;
  if (v === "blockchain propre") return "Own chain";
  return v;
}

function etat(c) {
  const v = (c.etat || "").trim();
  if (v.startsWith("mort")) return "dead";
  if (v.startsWith("en déclin")) return "declining";
  if (v.startsWith("actif")) return "active";
  return "unknown";
}

function propre(v) {
  return v && v !== "?" && v !== "à vérifier" ? v : null;
}

const brut = JSON.parse(readFileSync(catalogue, "utf8"));
const fiches = {};
for (const c of brut) {
  // Mythiques : jamais publiées, même anonymes (le front les affiche toutes en « ? »).
  if (c.rarete === "mythique" || String(c.id).startsWith("mythique")) continue;
  // Les 101 jetons « À décider » (politiques, obscènes, personnes réelles, arnaques, cas douteux) restent hors du
  // site tant qu'ils ne sont pas tranchés (décision du 13/11). Les séries de app3 ne les contiennent pas.
  if (c.section !== "catalogue") continue;
  fiches[c.id] = {
    no: c.numero,
    ticker: propre(c.ticker) ?? "TBD",
    // Précision française entre parenthèses retirée du nom (« 財務自由 (Liberté financière) »).
    name: String(c.nom).replace(/ \((?=[^)]*(?:[éèàêç]|\bne\b|\bde\b|\bla\b|\ble\b))[^)]*\)?$/, ""),
    chain: chaine(c),
    state: etat(c),
    address: propre(c.adresse),
    coingecko: propre(c.coingecko_id),
  };
}
mkdirSync(dirname(sortieCatalogue), { recursive: true });
writeFileSync(sortieCatalogue, JSON.stringify(fiches));
console.log(`[assets] catalog.json : ${Object.keys(fiches).length} cards (mythics excluded)`);

// --- visuels ----------------------------------------------------------------------------------

function empreinte() {
  const h = createHash("sha256");
  h.update(readFileSync(catalogue));
  const paquet = join(art, "memaster_art");
  for (const f of readdirSync(paquet).filter((f) => f.endsWith(".py")).sort()) {
    h.update(f);
    h.update(readFileSync(join(paquet, f)));
  }
  return h.digest("hex");
}

const tampon = join(sortieCartes, ".stamp");
const attendu = empreinte();
if (existsSync(tampon) && readFileSync(tampon, "utf8") === attendu) {
  console.log("[assets] card visuals up to date");
} else {
  rmSync(sortieCartes, { recursive: true, force: true });
  mkdirSync(sortieCartes, { recursive: true });
  const r = spawnSync(
    "python3",
    ["-m", "memaster_art", "--catalogue", catalogue, "--langue", "en", "--out", sortieCartes],
    { cwd: art, stdio: ["ignore", "pipe", "inherit"], encoding: "utf8" },
  );
  if (r.status !== 0) {
    console.warn("[assets] python3 / art generator unavailable: cards will show without visuals");
  } else {
    // Seuls les SVG servent au front ; les JSON NEP-177 restent l'affaire du contrat.
    for (const f of readdirSync(sortieCartes)) if (f.endsWith(".json")) rmSync(join(sortieCartes, f));
    writeFileSync(tampon, attendu);
    const n = readdirSync(sortieCartes).filter((f) => f.endsWith(".svg")).length;
    console.log(`[assets] ${n} card visuals generated (${r.stdout.trim()})`);
  }
}

// Garde-fou : aucun fichier public ne doit porter le contenu d'une mythique.
for (const f of readdirSync(sortieCartes)) {
  if (f.startsWith("mythique-")) throw new Error(`mythic file must not be public: ${f}`);
}
