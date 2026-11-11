import { describe, expect, it } from "vitest";
import { listingDepositNote, payoutBreakdown } from "./market";

describe("market payout before buying", () => {
  it("splits the price into royalties and what the seller receives", () => {
    const b = payoutBreakdown(
      { payout: { "seller.testnet": "950000000000000000000000", "creator.testnet": "40000000000000000000000", "dao.testnet": "10000000000000000000000" } },
      "seller.testnet",
      "1000000000000000000000000",
    );
    expect(b.price).toBe(10n ** 24n);
    expect(b.royalties).toEqual([
      { account: "creator.testnet", amount: 4n * 10n ** 22n },
      { account: "dao.testnet", amount: 10n ** 22n },
    ]);
    expect(b.royaltyTotal).toBe(5n * 10n ** 22n);
    expect(b.seller).toBe(95n * 10n ** 22n);
    expect(b.royaltyTotal + b.seller).toBe(b.price);
  });
  it("has no royalty line when the series has none", () => {
    const b = payoutBreakdown({ payout: { "seller.testnet": "5" } }, "seller.testnet", "5");
    expect(b.royalties).toEqual([]);
    expect(b.royaltyTotal).toBe(0n);
  });
});

describe("listing deposit text", () => {
  it("reads the amount from get_config", () => {
    expect(listingDepositNote("5000000000000000000000")).toBe("A 0.005 NEAR listing deposit is returned when the listing ends.");
    expect(listingDepositNote("10000000000000000000000")).toMatch(/^A 0\.01 NEAR/);
  });
  it("gives no amount before the config is read", () => {
    expect(listingDepositNote(undefined)).toBe("A small listing deposit is returned when the listing ends.");
    expect(listingDepositNote(null)).not.toMatch(/\d/);
  });
});
