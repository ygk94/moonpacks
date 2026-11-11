// Concordance du vérificateur TypeScript avec le Rust : on rejoue les vecteurs de verifier/tests/vectors/
// (générés par verifier/vectorgen depuis contract/src/draw.rs et le contrat en sandbox), comme le fait
// verifier/tests/test_vectors.py, test_mechanics.py et test_value.py côté Python.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import {
  drawPackMech,
  replaySeries,
  rushAccount,
  rushOnBuy,
  splitValue,
  type Burn,
  type ChainEvent,
  type FullTable,
  type RushParams,
  type RushState,
} from "./replay";
import { hex, initialAcc, mix, roll, tableHash, unhex, verifyPack, type PackInput, type R, type Table } from "./verify";

/* eslint-disable @typescript-eslint/no-explicit-any */
const dir = resolve(__dirname, "../../../verifier/tests/vectors");
// Les pack_id des vecteurs vont jusqu'à 2⁶⁴ − 1 : au-delà de 2⁵³, on les lit en BigInt depuis le texte source.
const load = (name: string) =>
  JSON.parse(readFileSync(`${dir}/${name}`, "utf8"), (key, value, ctx?: { source?: string }) =>
    key === "pack_id" && typeof value === "number" && !Number.isSafeInteger(value) && ctx?.source ? BigInt(ctx.source) : value,
  );
const DRAW = load("draw_vectors.json");
const MECH = load("mech_vectors.json");
const SANDBOX = load("sandbox_vectors.json");
const SBX_MECH = load("sandbox_mech_vectors.json");

const backedOf = (t: FullTable) => t.cards.map((c) => c.backing != null);

describe("draw vectors (pure draw.rs code, 200 tables)", () => {
  it("serializes and hashes each table like serde_json", async () => {
    for (const c of DRAW.cases) {
      expect(JSON.stringify(c.table)).toBe(c.table_json);
      expect(await tableHash(c.table)).toBe(c.table_hash);
    }
  });

  it("chains the seeds and computes the rolls, up to pack_id = 2⁶⁴ − 1", async () => {
    expect(DRAW.cases.some((c: any) => typeof c.pack_id === "bigint")).toBe(true);
    for (const c of DRAW.cases) {
      let acc = await initialAcc(c.pack_id, c.owner, c.table_hash);
      expect(hex(acc)).toBe(c.initial_acc);
      for (const s of c.seeds) {
        acc = await mix(acc, unhex(s.seed), c.pack_id, c.owner);
        expect(hex(acc)).toBe(s.acc);
      }
      expect(hex(acc)).toBe(c.acc);
      for (const r of c.rolls) expect((await roll(acc, r.slot, r.tag)).toString()).toBe(r.value);
    }
  });

  it("draws the same cards, caps and fallbacks included", async () => {
    let falls = 0;
    let mythics = 0;
    for (const c of DRAW.cases) {
      const t = c.table as FullTable;
      const minted = [...c.minted];
      const mm = [...c.mythic_minted];
      const got = await drawPackMech(t, minted, mm, unhex(c.acc), "base", null, backedOf(t));
      expect(got).toEqual(c.draws);
      expect(minted).toEqual(c.minted_after);
      expect(mm).toEqual(c.mythic_minted_after);
      falls += got.filter((d) => d.rolled_rarity !== d.final_rarity).length;
      mythics += got.filter((d) => d.kind === "mythic").length;
    }
    expect(falls).toBeGreaterThan(100);
    expect(mythics).toBeGreaterThan(20);
  }, 60_000);
});

describe("mechanics vectors (gold slots, guaranteed burnable, burns, resurrections, rush)", () => {
  it("hashes tables with mechanics", async () => {
    for (const c of MECH.cases) {
      expect(JSON.stringify(c.table)).toBe(c.table_json);
      expect(await tableHash(c.table)).toBe(c.table_hash);
    }
  });

  it("computes the gold roll", async () => {
    for (const c of MECH.cases) expect(Number((await roll(unhex(c.acc), 0, 2)) % 1_000_000_000n)).toBe(c.gold_roll);
  });

  it("draws every slot like draw::draw_pack_mech", async () => {
    let golds = 0;
    for (const c of MECH.cases) {
      const t = c.table as FullTable;
      const m = t.mechanics!;
      const burn: Burn | null = m.burn
        ? {
            burned: c.burned,
            backed: c.backed,
            floorBps: m.burn.floor_bps,
            priorK: m.burn.prior_k,
            resurrectable: new Set(m.resurrection?.eligible ?? []),
          }
        : null;
      const minted = [...c.minted];
      const mm = [...c.mythic_minted];
      const got = await drawPackMech(t, minted, mm, unhex(c.acc), c.mode, burn, c.backed);
      expect(got, `case ${c.case}`).toEqual(c.draws);
      expect(minted, `case ${c.case}`).toEqual(c.minted_after);
      expect(mm, `case ${c.case}`).toEqual(c.mythic_minted_after);
      golds += c.mode === "gold" ? 1 : 0;
    }
    expect(golds).toBeGreaterThan(20);
  }, 60_000);

  it("splits the value like draw::split_value", () => {
    for (const c of MECH.splits) {
      const total = (BigInt(c.price) * BigInt(c.bps)) / 10_000n;
      expect(total.toString()).toBe(c.total);
      expect(splitValue(total, c.slots as [R, boolean][], c.multipliers)).toEqual(c.amounts);
    }
  });

  it("replays the gold rush sequences", () => {
    let triggered = 0;
    let capped = 0;
    for (const r of MECH.rushes) {
      const st: RushState = { ring: [], start: null, lastTrigger: null };
      const accounts = new Map<number, [number, number]>();
      let count = 0;
      for (const b of r.buys) {
        const o = rushOnBuy(r.params as RushParams, st, b.height);
        expect(o).toEqual({
          active: b.active,
          window_count: b.window_count,
          baseline_count: b.baseline_count,
          triggered: b.triggered,
        });
        const prev = o.active ? accounts.get(b.account) : undefined;
        const a = rushAccount(r.params, o.active, st.lastTrigger, prev);
        if (a.rush && a.entry) accounts.set(b.account, a.entry);
        expect([a.rush, a.capped]).toEqual([b.rush, b.capped]);
        count += o.triggered ? 1 : 0;
        capped += a.capped ? 1 : 0;
      }
      expect(count).toBe(r.rush_count);
      triggered += count;
    }
    expect(triggered).toBeGreaterThan(50);
    expect(capped).toBeGreaterThan(20);
  });
});

describe("sandbox vectors (events of the contract deployed in near-sandbox)", () => {
  it("hashes the bytes of the table view", async () => {
    for (const s of SANDBOX.series) {
      const t = JSON.parse(s.table_raw);
      expect(JSON.stringify(t)).toBe(s.table_raw);
      expect(await tableHash(t)).toBe(s.table_hash);
    }
  });

  it("accepts every pack, stateless and with a full replay", async () => {
    let n = 0;
    for (const s of SANDBOX.series) {
      const t = JSON.parse(s.table_raw) as FullTable & Table;
      for (const p of s.packs) {
        const checks = await verifyPack(t, s.table_hash, p.event as PackInput);
        expect(checks.filter((c) => !c.ok), `${s.label} pack ${p.event.pack_id}`).toEqual([]);
        n++;
      }
      const events: ChainEvent[] = s.packs.map((p: any) => ({ event: "pack_revealed", data: p.event }));
      const reports = await replaySeries(t, s.table_hash, events);
      expect(reports).toHaveLength(s.packs.length);
      for (const r of reports) expect(r.checks.filter((c) => !c.ok), `${s.label} pack ${r.packId}`).toEqual([]);
    }
    expect(n).toBe(96);
  }, 60_000);

  it("rejects a swapped card in a capped series", async () => {
    const s = SANDBOX.series.find((x: any) => x.label === "cascade");
    const t = JSON.parse(s.table_raw) as FullTable;
    const events: ChainEvent[] = structuredClone(s.packs.map((p: any) => ({ event: "pack_revealed", data: p.event })));
    const last = events[events.length - 1];
    last.data.draws[0].index = (last.data.draws[0].index + 1) % t.cards.length;
    const reports = await replaySeries(t, s.table_hash, events, Number(last.data.pack_id));
    expect(reports[0].checks.some((c) => !c.ok)).toBe(true);
  }, 60_000);
});

describe("sandbox mechanics vectors (pity, gold packs, rush, burns, resurrection, value)", () => {
  const table = JSON.parse(SBX_MECH.table_raw) as FullTable;
  const events = (): ChainEvent[] =>
    structuredClone(SBX_MECH.events.flatMap((e: any) => e.data.map((data: object) => ({ event: e.event, data }))));
  const revealed = events().filter((e) => e.event === "pack_revealed");
  const stored = revealed[0].data.table_hash as string;

  it("hashes the table bytes", async () => {
    expect(JSON.stringify(table)).toBe(SBX_MECH.table_raw);
    expect(await tableHash(table)).toBe(stored);
  });

  it("replays the whole series exactly", async () => {
    const reports = await replaySeries(table, stored, events());
    expect(reports).toHaveLength(revealed.length);
    for (const r of reports) expect(r.checks.filter((c) => !c.ok), `pack ${r.packId}`).toEqual([]);
    const modes = revealed.map((e) => e.data.mechanics.mode);
    expect(modes).toContain("gold");
    expect(modes).toContain("rush");
  }, 60_000);

  it("detects a tampered value, pity counter or missing burn", async () => {
    const tamper = async (pred: (e: ChainEvent) => boolean, change: (e: ChainEvent) => void, drop = false) => {
      let list = events();
      const target = list.find(pred)!;
      expect(target).toBeDefined();
      if (drop) list = list.filter((e) => e !== target);
      else change(target);
      const reports = await replaySeries(table, stored, list);
      return reports.filter((r) => r.checks.some((c) => !c.ok)).length;
    };
    expect(
      await tamper(
        (e) => e.event === "pack_revealed" && e.data.mechanics.value != null,
        (e) => (e.data.mechanics.value.bps += 1),
      ),
    ).toBeGreaterThan(0);
    expect(
      await tamper(
        (e) => e.event === "pack_revealed" && e.data.mechanics.pity != null,
        (e) => (e.data.mechanics.pity.before += 1),
      ),
    ).toBeGreaterThan(0);
    expect(await tamper((e) => e.event === "card_redeemed", () => undefined, true)).toBeGreaterThan(0);
  }, 60_000);
});
