// Mise en ligne sur Vercel du build statique (`dist/`), après `npm run build`.
//
// Le build est recopié dans `.deploy/moonpacks/` (ignoré par git) : Vercel nomme le projet d'après le dossier
// publié, et le lien vers le projet (`.vercel/`) y reste d'un déploiement à l'autre (Vite vide `dist/` à chaque
// build). Le site est déjà construit : Vercel ne fait que le servir (aucune commande de build côté Vercel).
// Usage : npm run deploy (production) ; node scripts/deploy.mjs --preview (adresse de prévisualisation).
// En CI (.github/workflows/ci.yml) : mêmes commandes, avec les secrets VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID.

import { spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const front = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(front, "dist");
const target = join(front, ".deploy", "moonpacks");

if (!existsSync(join(dist, "index.html"))) {
  console.error("[deploy] dist/ is missing: run npm run build first");
  process.exit(1);
}
mkdirSync(target, { recursive: true });
for (const f of readdirSync(target)) if (f !== ".vercel") rmSync(join(target, f), { recursive: true, force: true });
cpSync(dist, target, { recursive: true });

const prod = !process.argv.includes("--preview");
// En CI : jeton dans VERCEL_TOKEN, projet désigné par VERCEL_ORG_ID et VERCEL_PROJECT_ID (pas de dossier .vercel).
const token = process.env.VERCEL_TOKEN ? ["--token", process.env.VERCEL_TOKEN] : [];
const r = spawnSync("npx", ["--yes", "vercel@65.15.0", "deploy", target, "--yes", ...(prod ? ["--prod"] : []), ...token], {
  stdio: "inherit",
  cwd: front,
});
process.exit(r.status ?? 1);
