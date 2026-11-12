// Contrôle après build : le wallet de test des parcours e2e (src/near/testKeyWallet.ts, clé locale) ne doit
// jamais être dans un build de production. Lancé par `npm run build` ; code de sortie 1 s'il y est.
//   node scripts/check-no-e2e-wallet.mjs [dossier du build, dist/ par défaut]

import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

export const E2E_MARKERS = ["e2e-key-wallet", "__MEMASTER_E2E_KEY__", "Test key (e2e)", "PKCS8_ED25519", "testKeyWallet"];

function* files(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* files(p);
    else if (/\.(js|mjs|html|map|css|json)$/.test(name)) yield p;
  }
}

/** Fichiers du build qui contiennent un marqueur du wallet de test. */
export function findE2eWallet(dir) {
  const hits = [];
  for (const f of files(dir)) {
    const text = readFileSync(f, "utf8");
    const m = E2E_MARKERS.find((k) => text.includes(k));
    if (m) hits.push({ file: f, marker: m });
  }
  return hits;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const dir = resolve(process.argv[2] ?? "dist");
  const hits = findE2eWallet(dir);
  if (hits.length) {
    for (const h of hits) console.error(`[check-no-e2e-wallet] ${h.file}: ${h.marker}`);
    process.exit(1);
  }
  console.log(`[check-no-e2e-wallet] ok (no test wallet in ${dir})`);
}
