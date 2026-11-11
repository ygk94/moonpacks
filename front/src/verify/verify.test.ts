// Vecteurs réels : table et événements de la série v2 sur testnet (docs/data/testnet-2026-11-11-v2/).

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { fallbackOrder, rarityFromRoll, tableHash, verifyPack, type PackInput, type Table } from "./verify";

const dir = resolve(__dirname, "../../../docs/data/testnet-2026-11-11-v2");
const table = JSON.parse(readFileSync(`${dir}/table.json`, "utf8")) as Table;
const stored = readFileSync(`${dir}/table_hash.txt`, "utf8").trim();
const revealed = readFileSync(`${dir}/events-serie0.jsonl`, "utf8")
  .split("\n")
  .filter(Boolean)
  .map((l) => JSON.parse(l))
  .filter((e) => e.event === "pack_revealed")
  .map((e) => e.data[0]);

function asInput(e: (typeof revealed)[number]): PackInput {
  return {
    pack_id: e.pack_id,
    owner_id: e.owner_id,
    acc: e.acc,
    mode: e.mechanics?.mode,
    seeds: e.seeds,
    draws: e.draws,
    value: e.mechanics?.value ? { bps: e.mechanics.value.bps } : null,
  };
}

describe("table hash", () => {
  it("matches the hash frozen on-chain", async () => {
    expect(await tableHash(table)).toBe(stored);
  });
  it("changes when a weight changes", async () => {
    const t = structuredClone(table);
    t.cards[0] = { ...t.cards[0], card_id: t.cards[0].card_id + "x" };
    expect(await tableHash(t)).not.toBe(stored);
  });
});

describe("verifyPack", () => {
  it("accepts every revealed pack of the series", async () => {
    expect(revealed.length).toBe(31);
    for (const e of revealed) {
      const checks = await verifyPack(table, stored, asInput(e));
      expect(checks.filter((c) => !c.ok), `pack ${e.pack_id}`).toEqual([]);
    }
  });

  it("rejects a tampered seed", async () => {
    const input = asInput(revealed[0]);
    input.seeds = input.seeds.map((s, i) => (i === 0 ? { seed: "00".repeat(32) } : s));
    const checks = await verifyPack(table, stored, input);
    expect(checks.find((c) => c.label.startsWith("Random seeds"))?.ok).toBe(false);
  });

  it("rejects a tampered rarity", async () => {
    const input = asInput(revealed[0]);
    input.draws = input.draws.map((d, i) => (i === 0 ? { ...d, rolled_rarity: "legendary", final_rarity: "legendary" } : d));
    const checks = await verifyPack(table, stored, input);
    expect(checks.some((c) => c.label.startsWith("Slot 1") && !c.ok)).toBe(true);
  });
});

describe("helpers", () => {
  it("picks the rarity from cumulative weights", () => {
    const w = { mythic: 1, legendary: 2, epic: 3, rare: 4, common: 10 };
    expect(rarityFromRoll(w, 0n)).toBe("mythic");
    expect(rarityFromRoll(w, 1n)).toBe("legendary");
    expect(rarityFromRoll(w, 6n)).toBe("rare");
    expect(rarityFromRoll(w, 19n)).toBe("common");
  });
  it("falls back down to the floor, then up", () => {
    expect(fallbackOrder("epic", "common")).toEqual(["epic", "rare", "common", "legendary", "mythic"]);
    expect(fallbackOrder("common", "rare")).toEqual(["rare", "epic", "legendary", "mythic", "common"]);
  });
});
