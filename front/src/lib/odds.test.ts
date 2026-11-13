import { describe, expect, it } from "vitest";
import type { RatesPage, SeriesView } from "../near/types";
import { packBlurb, sameOdds } from "./odds";

const page = (ppb: number): RatesPage =>
  ({
    series_id: 0,
    table_hash: "h",
    card_count: 1,
    from_index: 0,
    next_index: null,
    rarities: [{ rarity: "common", rarity_ppb: ppb, rush_rarity_ppb: null, gold_slot_ppb: null, cards: [{ card_id: "a", weight: 1, cap: null, minted: 0, ppm: 1, ppb, burnable: true }] }],
  }) as RatesPage;
const series = (id: number, price: string) => ({ series_id: id, price, cards_per_pack: 5 }) as SeriesView;

describe("odds shared between packs", () => {
  it("compares the odds, not the price or the minted counts", () => {
    const a = page(900);
    const b = { ...page(900), series_id: 1, table_hash: "other" };
    b.rarities[0].cards[0].minted = 7;
    expect(sameOdds([a, b])).toBe(true);
    expect(sameOdds([a, page(800)])).toBe(false);
  });

  it("tells the packs apart by the tokens of the burnable card, never by a return", () => {
    const list = [series(0, "55200000000000000000000"), series(1, "138100000000000000000000")];
    expect(packBlurb(list[0], list, true)).toBe("Same cards and odds as every pack · smallest token stash");
    expect(packBlurb(list[1], list, true)).toBe("Same cards and odds · 2.5× the tokens in the burnable card");
    expect(packBlurb(list[1], list, false)).toBe("5 cards · at least one burnable");
    expect(packBlurb(list[0], [list[0]], true)).toBe("5 cards · at least one burnable");
    for (const s of list) expect(packBlurb(s, list, true)).not.toMatch(/%|profit|value|return/i);
  });
});
