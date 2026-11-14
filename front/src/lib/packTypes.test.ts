import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import type { SeriesView } from "../near/types";
import type { CatalogEntry } from "./catalog";
import { cardsOf, offerFor, PACK_TYPES, regularSeries, seriesFor } from "./packTypes";

const e = (name: string, ticker: string, extra: Partial<CatalogEntry> = {}): CatalogEntry => ({
  no: "1", name, ticker, chain: null, state: "dead", address: null, coingecko: null, era: null, ...extra,
});
const catalog: Record<string, CatalogEntry> = {
  woof: e("Woofcoin", "WOOF DOG", { era: "2013-2018" }),
  bonk: e("Bonk", "BONK", { chain: "Solana" }),
  mew: e("cat in a dogs world", "MEW", { chain: "Solana" }),
  popcat: e("Popcat", "POPCAT"),
  pepe: e("Pepe", "PEPE", { chain: "Ethereum" }),
  bnb: e("Some Coin", "SOME", { chain: "BNB Chain" }),
};
const type = (id: string) => PACK_TYPES.find((t) => t.id === id)!;
const series = (name: string, cards = 5) => ({ series_id: 9, name, cards_per_pack: cards, price: "1" }) as SeriesView;

describe("themed packs", () => {
  it("sorts the catalogue into families, a cat never in the dog pack", () => {
    expect(cardsOf(type("dog"), catalog).sort()).toEqual(["bonk", "woof"]);
    expect(cardsOf(type("cat"), catalog).sort()).toEqual(["mew", "popcat"]);
    expect(cardsOf(type("frog"), catalog)).toEqual(["pepe"]);
  });

  it("chain and OG packs", () => {
    expect(cardsOf(type("solana"), catalog).sort()).toEqual(["bonk", "mew"]);
    expect(cardsOf(type("bnb"), catalog)).toEqual(["bnb"]);
    expect(cardsOf(type("og-5"), catalog)).toEqual(["woof"]);
    expect(PACK_TYPES.filter((t) => t.row === "og").map((t) => t.cards)).toEqual([1, 2, 5]);
  });

  it("a pack becomes buyable once a series with its name and size is open", () => {
    expect(seriesFor(type("dog"), [series("Memaster Entry")])).toBeUndefined();
    expect(seriesFor(type("dog"), [series("Moonpacks Dog", 8)])?.name).toBe("Moonpacks Dog");
    expect(seriesFor(type("dog"), [series("Moonpacks Dog", 5)])).toBeUndefined();
    expect(type("dog").cards).toBe(8);
    expect(seriesFor(type("og-2"), [series("Memaster OG 2", 2)])).toBeDefined();
    expect(seriesFor(type("og-2"), [series("Memaster OG 2", 5)])).toBeUndefined();
    expect(regularSeries([series("Memaster Entry"), series("Moonpacks Dog")]).map((s) => s.name)).toEqual(["Memaster Entry"]);
  });

  it("a themed pack can also be a pack type of an open series (shared counters)", () => {
    const base = {
      ...series("Memaster Entry"),
      kinds: [{ kind: 0, name: "Dog", price: "7", required_deposit: "9", cards_per_pack: 8, card_count: 291, mythics: false, value: false, slots: null }],
    } as SeriesView;
    const o = offerFor(type("dog"), [base]);
    expect(o?.series.name).toBe("Memaster Entry");
    expect(o?.kind?.kind).toBe(0);
    expect(o?.price).toBe("7");
    expect(offerFor(type("cat"), [base])).toBeUndefined();
    // Une série dédiée garde la priorité.
    expect(offerFor(type("dog"), [base, series("Moonpacks Dog", 8)])?.kind).toBeNull();
  });

  it("matches the pack types of the v4 Classic series, name and size (contract/series-v4)", () => {
    const m = JSON.parse(readFileSync(resolve(__dirname, "../../../contract/series-v4/classic/manifest.json"), "utf8"));
    const kinds = m.kinds.map((k: { name: string; cards_per_pack: number }) => `${k.name}/${k.cards_per_pack}`);
    expect(kinds).toEqual(PACK_TYPES.map((t) => `${t.seriesName}/${t.cards}`));
  });
});
