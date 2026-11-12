// Le wallet de test (clé locale, `npm run e2e`) ne doit jamais entrer dans un build de production, même si
// VITE_E2E_KEY_WALLET=1 traîne dans l'environnement. On construit le front dans un dossier temporaire et on cherche
// ses marqueurs ; le même build en mode dev, lui, doit les contenir (le contrôle sait donc les trouver).

import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { build } from "vite";
import { afterAll, describe, expect, it } from "vitest";
// @ts-expect-error module .mjs sans types
import { findE2eWallet } from "./check-no-e2e-wallet.mjs";

const root = resolve(__dirname, "..");
const dirs: string[] = [];
const out = () => {
  const d = mkdtempSync(join(tmpdir(), "memaster-build-"));
  dirs.push(d);
  return d;
};
afterAll(() => dirs.forEach((d) => rmSync(d, { recursive: true, force: true })));

// NODE_ENV décide de `import.meta.env.DEV` dans un build : `npm run build` le met à `production`, vitest à `test`.
async function buildTo(dir: string, nodeEnv: "production" | "development", flag: string | undefined) {
  const before = { flag: process.env.VITE_E2E_KEY_WALLET, nodeEnv: process.env.NODE_ENV };
  if (flag == null) delete process.env.VITE_E2E_KEY_WALLET;
  else process.env.VITE_E2E_KEY_WALLET = flag;
  process.env.NODE_ENV = nodeEnv;
  try {
    await build({ root, logLevel: "silent", build: { outDir: dir, emptyOutDir: true, copyPublicDir: false } });
  } finally {
    if (before.flag == null) delete process.env.VITE_E2E_KEY_WALLET;
    else process.env.VITE_E2E_KEY_WALLET = before.flag;
    process.env.NODE_ENV = before.nodeEnv;
  }
}

describe("test key wallet stays out of production builds", () => {
  it("is absent from the default production build", async () => {
    const dir = out();
    await buildTo(dir, "production", undefined);
    expect(findE2eWallet(dir)).toEqual([]);
  }, 60_000);

  it("is absent from a production build even with VITE_E2E_KEY_WALLET=1", async () => {
    const dir = out();
    await buildTo(dir, "production", "1");
    expect(findE2eWallet(dir)).toEqual([]);
  }, 60_000);

  it("is found by the check in a development build with VITE_E2E_KEY_WALLET=1", async () => {
    const dir = out();
    await buildTo(dir, "development", "1");
    expect(findE2eWallet(dir).length).toBeGreaterThan(0);
  }, 60_000);
});
