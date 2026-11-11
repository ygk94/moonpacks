// Rejeu complet de la série v2 du testnet (vecteurs réels : docs/data/testnet-2026-11-11-v2/).

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { replaySeries, type ChainEvent, type FullTable } from "./replay";

const dir = resolve(__dirname, "../../../docs/data/testnet-2026-11-11-v2");
const table = JSON.parse(readFileSync(`${dir}/table.json`, "utf8")) as FullTable;
const stored = readFileSync(`${dir}/table_hash.txt`, "utf8").trim();
const events: ChainEvent[] = readFileSync(`${dir}/events-serie0.jsonl`, "utf8")
  .split("\n")
  .filter(Boolean)
  .map((l) => JSON.parse(l))
  .flatMap((e) => e.data.map((data: object) => ({ event: e.event, data })));

describe("replaySeries", () => {
  it("recomputes every card of the 31 testnet packs exactly", async () => {
    const reports = await replaySeries(table, stored, events);
    expect(reports).toHaveLength(31);
    for (const r of reports) {
      expect(r.checks.filter((c) => !c.ok), `pack ${r.packId}`).toEqual([]);
      expect(r.checks.filter((c) => c.label.includes("exact card"))).toHaveLength(5);
    }
  }, 60_000);

  it("stops at the requested pack", async () => {
    const reports = await replaySeries(table, stored, events, 5);
    expect(reports.map((r) => r.packId)).toEqual([5]);
    expect(reports[0].checks.every((c) => c.ok)).toBe(true);
  }, 60_000);

  it("detects a swapped card", async () => {
    const forged = structuredClone(events);
    const ev = forged.find((e) => e.event === "pack_revealed" && e.data.pack_id === 3)!;
    ev.data.draws[1].index = (ev.data.draws[1].index + 1) % table.cards.length;
    const [r] = await replaySeries(table, stored, forged, 3);
    expect(r.checks.find((c) => c.label.startsWith("Slot 2"))?.ok).toBe(false);
  }, 60_000);

  it("detects a missing purchase in the history (rush flag unverifiable)", async () => {
    const partial = events.filter((e) => !(e.event === "pack_bought" && e.data.pack_id === 4));
    const [r] = await replaySeries(table, stored, partial, 4);
    expect(r.checks.some((c) => !c.ok)).toBe(true);
  }, 60_000);

  it("never mentions the pity counter value in its labels", async () => {
    const reports = await replaySeries(table, stored, events);
    for (const r of reports) for (const c of r.checks) expect(c.label).not.toMatch(/pity|counter|\d+ packs? (left|until)/i);
  }, 60_000);
});
