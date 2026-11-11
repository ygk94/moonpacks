import { describe, expect, it } from "vitest";
import { eventsFromTx, listenHost, rankTrending, tokensFromReveal } from "./lib.mjs";

const C = "app2.memaster-demo-j7xg7z.testnet";
const log = (event, data) => `EVENT_JSON:${JSON.stringify({ standard: "memaster", version: "1.0.0", event, data: [data] })}`;
const receipt = (height, index, executor, logs, status = { SuccessValue: "" }) => ({
  receipt: {},
  execution_outcome: {
    id: `r${height}-${index}`,
    block_height: height,
    block_timestamp: String(1_794_432_583_147_355_725 + height),
    index,
    outcome: { executor_id: executor, logs, status },
  },
});

describe("eventsFromTx", () => {
  it("keeps the contract's memaster events in execution order", () => {
    const tx = {
      receipts: [
        receipt(12, 0, C, [log("pack_revealed", { pack_id: 1, draws: [] })]),
        receipt(10, 0, C, [log("pack_bought", { pack_id: 1 }), "not an event"]),
        receipt(10, 1, "other.testnet", [log("pack_bought", { pack_id: 9 })]),
        receipt(11, 0, C, [`EVENT_JSON:${JSON.stringify({ standard: "nep171", version: "1", event: "nft_mint", data: [{}] })}`]),
      ],
    };
    const out = eventsFromTx(tx, C);
    expect(out.map((e) => [e.height, e.event])).toEqual([
      [10, "pack_bought"],
      [12, "pack_revealed"],
    ]);
    expect(out[0].ts).toBeGreaterThan(1.7e12);
  });

  it("ignores failed receipts (their state is reverted)", () => {
    const tx = { receipts: [receipt(10, 0, C, [log("card_sold", { token_id: "5" })], { Failure: {} })] };
    expect(eventsFromTx(tx, C)).toEqual([]);
  });

  it("keeps the token id as a string", () => {
    const tx = { receipts: [receipt(10, 0, C, [log("card_listed", { token_id: 42, price: "1" })])] };
    expect(eventsFromTx(tx, C)[0].token_id).toBe("42");
  });
});

describe("tokensFromReveal", () => {
  it("never stores a card id for a mythic", () => {
    const tokens = tokensFromReveal(
      {
        series_id: 0,
        draws: [
          { token_id: "10", kind: "visible", index: 3, final_rarity: "rare" },
          { token_id: "11", kind: "mythic", index: 0, final_rarity: "mythic" },
        ],
      },
      (_s, i) => `card-${i}`,
    );
    expect(tokens).toEqual([
      { token_id: "10", series_id: 0, kind: "visible", card_index: 3, card_id: "card-3", rarity: "rare" },
      { token_id: "11", series_id: 0, kind: "mythic", card_index: null, card_id: null, rarity: "mythic" },
    ]);
  });
});

describe("rankTrending", () => {
  it("ranks by sales then listings and groups mythics together", () => {
    const rows = [
      { event: "card_listed", card_id: "bonk", kind: "visible", rarity: "legendary", price: "5", ts: 1 },
      { event: "card_listed", card_id: "bonk", kind: "visible", rarity: "legendary", price: "6", ts: 2 },
      { event: "card_sold", card_id: "popcat", kind: "visible", rarity: "common", price: "3", ts: 3 },
      { event: "card_sold", card_id: "popcat", kind: "visible", rarity: "common", price: "4", ts: 5 },
      { event: "card_listed", card_id: null, kind: "mythic", rarity: "mythic", price: "9", ts: 4 },
      { event: "card_listed", card_id: null, kind: "mythic", rarity: "mythic", price: "9", ts: 4 },
    ];
    const out = rankTrending(rows);
    expect(out.map((g) => g.card_id)).toEqual(["popcat", "bonk", null]);
    expect(out[0]).toMatchObject({ sales: 2, listings: 0, volume: "7", last_price: "4", score: 4 });
    expect(out[2]).toMatchObject({ kind: "mythic", listings: 2 });
    expect(rankTrending(rows, 1)).toHaveLength(1);
  });
});

describe("contract v3 events", () => {
  it("keeps pack_refunded, revenue_withdrawn and the v3 fields without failing", () => {
    const tx = {
      receipts: [
        receipt(20, 0, C, [
          log("pack_refunded", { pack_id: 4, owner_id: "b.testnet", price: "1", storage_refund: "2", total: "3", storage_used: 90, by: "x.testnet" }),
        ]),
        receipt(21, 0, C, [log("revenue_withdrawn", { amount: "5", to: "owner.testnet", balance_before: "9", committed: "1" })]),
        receipt(22, 0, C, [log("card_redeemed", { token_id: 41, owner_id: "b.testnet", freed_bytes: 16, storage_refund: "160000000000000000000" })]),
        receipt(23, 0, C, [
          log("pack_revealed", {
            pack_id: 5,
            series_id: 1,
            draws: [{ token_id: 50, kind: "visible", index: 0, final_rarity: "common" }],
            storage: { prepaid_bytes: 1605, used_bytes: 1034, refund: "5710000000000000000000" },
          }),
        ]),
      ],
    };
    const out = eventsFromTx(tx, C);
    expect(out.map((e) => [e.event, e.token_id])).toEqual([
      ["pack_refunded", null],
      ["revenue_withdrawn", null],
      ["card_redeemed", "41"],
      ["pack_revealed", null],
    ]);
    expect(out[0].data.total).toBe("3");
    expect(tokensFromReveal(out[3].data, () => "abc")).toEqual([
      { token_id: "50", series_id: 1, kind: "visible", card_index: 0, card_id: "abc", rarity: "common" },
    ]);
  });
});

describe("listen address", () => {
  it("listens on the local machine only by default", () => {
    expect(listenHost({})).toBe("127.0.0.1");
    expect(listenHost({ INDEXER_HOST: "" })).toBe("127.0.0.1");
    expect(listenHost({ INDEXER_HOST: "0.0.0.0" })).toBe("0.0.0.0");
  });
});
