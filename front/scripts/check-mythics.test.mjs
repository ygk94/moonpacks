// Le garde-fou détecte bien une fuite (fichier secret et front factices dans un dossier temporaire).

import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { describe, expect, it } from "vitest";

const script = resolve(__dirname, "check-mythics.mjs");

function fakeFront(files) {
  const root = mkdtempSync(join(tmpdir(), "memaster-check-"));
  for (const [path, content] of Object.entries(files)) {
    mkdirSync(join(root, path, ".."), { recursive: true });
    writeFileSync(join(root, path), content);
  }
  const secrets = join(root, "secrets.json");
  writeFileSync(
    secrets,
    JSON.stringify({ mythiques: [{ nom: "Zorblax Coin", ticker: "ZRBX", coingecko_id: "zorblax-coin", adresse: "0xFEEDFACE1234" }] }),
  );
  return { root, secrets };
}

const run = ({ root, secrets }) =>
  spawnSync(process.execPath, [script, "--root", root, "--secrets", secrets], { encoding: "utf8" });

describe("check-mythics", () => {
  it("passes on a clean front", () => {
    const r = run(fakeFront({ "src/a.ts": "const x = 'BONK';", "public/catalog.json": JSON.stringify({ "bonk-bonk": { ticker: "BONK", name: "Bonk" } }) }));
    expect(r.status).toBe(0);
  });

  it("fails on a mythic ticker in the code, without printing it", () => {
    const r = run(fakeFront({ "src/a.ts": "const secret = 'ZRBX';" }));
    expect(r.status).toBe(1);
    expect(r.stderr).toMatch(/LEAK: src\/a\.ts: mythic ticker found/);
    expect(r.stderr + r.stdout).not.toMatch(/ZRBX|Zorblax/i);
  });

  it("fails on a mythic address in the build and on a public mythic file", () => {
    const r = run(fakeFront({ "dist/assets/x.js": "a='0xfeedface1234'", "public/cards/mythique-m1.svg": "<svg/>" }));
    expect(r.status).toBe(1);
    expect(r.stderr).toMatch(/dist\/assets\/x\.js: mythic adresse found/);
    expect(r.stderr).toMatch(/mythique-m1\.svg/);
  });

  it("does not match inside a longer word, and tolerates a public homonym", () => {
    const r = run(
      fakeFront({
        "src/a.ts": "const y = 'ZRBXL';",
        "src/b.ts": "const z = 'Zorblax Coin';",
        "public/catalog.json": JSON.stringify({ "other-zorblax": { ticker: "ZBX", name: "Zorblax Coin" } }),
      }),
    );
    expect(r.status).toBe(0);
    expect(r.stderr).toMatch(/homonym/);
  });
});
