// Types de packs (packs thématiques) : le vérificateur TypeScript retrouve exactement le tirage du contrat
// (verifier/tests/vectors/kind_vectors.json, généré par verifier/vectorgen depuis contract/src/draw.rs).

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { drawPackMech, kindTable, type Burn, type FullTable } from "./replay";
import { tableHash, unhex } from "./verify";

/* eslint-disable @typescript-eslint/no-explicit-any */
const KINDS = JSON.parse(readFileSync(resolve(__dirname, "../../../verifier/tests/vectors/kind_vectors.json"), "utf8"));

describe("pack kinds (themed packs)", () => {
  it("serializes and hashes a table with kinds like serde_json", async () => {
    for (const c of KINDS.cases) {
      expect(JSON.stringify(c.table)).toBe(c.table_json);
      expect(await tableHash(c.table)).toBe(c.table_hash);
    }
  });

  it("recomputes every card of a themed pack exactly", async () => {
    let rules = 0;
    for (const c of KINDS.cases) {
      const t = c.table as FullTable;
      const m = (c.table as any).mechanics;
      const burn: Burn | null = m.burn
        ? { burned: c.burned, backed: c.backed, floorBps: m.burn.floor_bps, priorK: m.burn.prior_k, resurrectable: new Set() }
        : null;
      const minted = [...c.minted];
      const mm = [...c.mythic_minted];
      const got = await drawPackMech(kindTable(t, c.kind), minted, mm, unhex(c.acc), c.mode, burn, c.backed);
      expect(got, `case ${c.case}`).toEqual(c.draws);
      expect(minted, `case ${c.case}`).toEqual(c.minted_after);
      expect(mm, `case ${c.case}`).toEqual(c.mythic_minted_after);
      rules += t.kinds![c.kind].slots ? 1 : 0;
    }
    expect(rules).toBeGreaterThan(20);
  }, 60_000);

  it("leaves the base pack untouched", () => {
    const t = KINDS.cases[0].table as FullTable;
    expect(kindTable(t, null)).toBe(t);
    expect(() => kindTable(t, 99)).toThrow();
  });
});
