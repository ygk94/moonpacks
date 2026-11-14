import { describe, expect, it } from "vitest";
import type { SeriesView } from "../near/types";
import { BUNDLES, shopRows } from "./Shop";

const s = (id: number, price: string) => ({ series_id: id, price, cards_per_pack: 5 }) as SeriesView;

describe("shop rows", () => {
  it("puts the cheapest series first as Classic, the other as Full Moon with its token multiple", () => {
    const rows = shopRows([s(1, "138100000000000000000000"), s(0, "55200000000000000000000")]);
    expect(rows.map((r) => [r.series.series_id, r.title, r.variant])).toEqual([
      [0, "Classic", "standard"],
      [1, "Full Moon", "moon"],
    ]);
    expect(rows[1].ratio).toBe(2.5);
  });

  it("offers 5, 10 and 20 cards: 1, 2 and 4 packs of 5", () => {
    expect(BUNDLES.map((n) => n * 5)).toEqual([5, 10, 20]);
  });
});
