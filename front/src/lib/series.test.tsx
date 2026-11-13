// Page des taux et gold rush sur plusieurs séries (contrat v3 : 0 « entrée », 1 « standard »).

import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { RushState, SeriesView } from "../near/types";
import { RushView } from "../pages/Shop";
import { SeriesPicker } from "../pages/Transparency";
import { pickSeries, publicSeries, rushTarget } from "./series";

const series = (id: number, over: Partial<SeriesView> = {}): SeriesView => ({
  series_id: id,
  status: "open",
  name: id === 0 ? "Memaster Entry" : "Memaster Standard",
  price: id === 0 ? "55200000000000000000000" : "138100000000000000000000",
  cards_per_pack: 5,
  table_hash: "abc",
  storage_per_pack: 1605,
  required_deposit: "0",
  min_gas: "0",
  packs_sold: 0,
  card_count: 1527,
  ...over,
});

const params = {
  ratio_bps: 30_000,
  min_packs: 10,
  window_blocks: 6000,
  baseline_blocks: 144_000,
  bucket_blocks: 600,
  duration_blocks: 3000,
  cooldown_blocks: 6000,
  max_per_account: 3,
};

describe("series shown on the rates page", () => {
  it("keeps series with a frozen table, drafts and deleted ones excluded", () => {
    const all = [series(0), series(1), series(2, { status: "draft", table_hash: null }), series(3, { status: "deleted" }), series(4, { status: "closed" })];
    expect(publicSeries(all).map((s) => s.series_id)).toEqual([0, 1, 4]);
  });

  it("picks ?series=N when it exists, else VITE_SERIES_ID, else the first one", () => {
    const list = [series(0), series(1)];
    expect(pickSeries("1", list, 0)).toBe(1);
    expect(pickSeries("7", list, 0)).toBe(0);
    expect(pickSeries("abc", list, 1)).toBe(1);
    expect(pickSeries(null, list, 5)).toBe(0);
    expect(pickSeries(null, [], 0)).toBeNull();
  });

  it("renders one tab per series with its price, the current one selected", () => {
    const html = renderToStaticMarkup(<SeriesPicker list={[series(0), series(1)]} current={1} onPick={() => {}} />);
    // Nom on-chain « Memaster … » affiché sous la marque du site.
    expect(html).toContain("Moonpacks Entry");
    expect(html).toContain("Moonpacks Standard");
    expect(html).not.toContain("Memaster");
    expect(html).toContain("0.0552 NEAR");
    expect(html).toContain("0.1381 NEAR");
    expect(html).toMatch(/aria-selected="true" class="active">Moonpacks Standard/);
    // Une seule série : pas de sélecteur.
    expect(renderToStaticMarkup(<SeriesPicker list={[series(0)]} current={0} onPick={() => {}} />)).toBe("");
  });
});

describe("gold rush per series", () => {
  const rush: RushState = { enabled: true, params, height: 1000, window_count: 4, baseline_count: 0, active: false };

  it("computes the threshold from min_packs and the baseline rate", () => {
    expect(rushTarget({ params, baseline_count: 0 })).toBe(10);
    // 240 packs sur la base de 24 h, fenêtre = 1/24 de la base, ratio ×3 : ceil(3 × 240 / 24) = 30.
    expect(rushTarget({ params, baseline_count: 240 })).toBe(30);
  });

  it("names the series in the panel when several are open", () => {
    const html = renderToStaticMarkup(<RushView rush={rush} name="Memaster Standard" now={0} fetchedAt={0} />);
    expect(html).toContain("Gold rush · Memaster Standard");
    expect(html).toContain("4 / 10 packs opened");
    const single = renderToStaticMarkup(<RushView rush={rush} name={null} now={0} fetchedAt={0} />);
    expect(single).toContain(">Gold rush<");
  });

  it("shows the end of an active rush for that series", () => {
    const html = renderToStaticMarkup(
      <RushView rush={{ ...rush, active: true, rush_until: 2000, account: { account_id: "a", rush_packs: 1, remaining: 2 } }} name="Memaster Entry" now={0} fetchedAt={0} />,
    );
    expect(html).toContain("Gold rush in progress · Memaster Entry");
    expect(html).toContain("rush packs left for you");
  });

  it("renders nothing for a series without gold rush", () => {
    expect(renderToStaticMarkup(<RushView rush={{ enabled: false }} name="X" now={0} fetchedAt={0} />)).toBe("");
  });
});
