import { describe, expect, it } from "vitest";
import type { SeriesView } from "../near/types";
import type { CatalogEntry } from "./catalog";
import { cardsOf, PACK_TYPES, regularSeries, seriesFor } from "./packTypes";

const e = (name: string, ticker: string, extra: Partial<CatalogEntry> = {}): CatalogEntry => ({
  no: "1", name, ticker, chain: null, state: "dead", address: null, coingecko: null, era: null, ...extra,
});
const catalog: Record<string, CatalogEntry> = {
  doge: e("Dogecoin", "DOGE", { era: "2013-2018" }),
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
    expect(cardsOf(type("dog"), catalog).sort()).toEqual(["bonk", "doge"]);
    expect(cardsOf(type("cat"), catalog).sort()).toEqual(["mew", "popcat"]);
    expect(cardsOf(type("frog"), catalog)).toEqual(["pepe"]);
  });

  it("chain and OG packs", () => {
    expect(cardsOf(type("solana"), catalog).sort()).toEqual(["bonk", "mew"]);
    expect(cardsOf(type("bnb"), catalog)).toEqual(["bnb"]);
    expect(cardsOf(type("og-5"), catalog)).toEqual(["doge"]);
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
});
