import { describe, expect, it } from "vitest";
import type { MemasterEvent, PackView } from "../near/types";
import {
  burnStorageRefund,
  canRefund,
  canRetryReveal,
  isV3Pack,
  refundAmount,
  refundedTotal,
  revealStorageRefund,
  storageDepositNote,
  unusedStorage,
} from "./pack";

const NEAR = 10n ** 24n;
const pack = (over: Partial<PackView> = {}): PackView => ({
  pack_id: 7,
  series_id: 0,
  owner_id: "buyer.testnet",
  price_paid: (NEAR / 10n).toString(), // 0.1 NEAR
  storage_prepaid: (1605n * 10n ** 19n).toString(), // 1 605 o
  storage_used: 975,
  bought_at_height: 100,
  status: "pending",
  attempt: 0,
  step: 1,
  last_progress_height: 100,
  token_ids: [],
  draws: [],
  rush: false,
  mode: "base",
  value: null,
  ...over,
});
const ev = (event: string, data: Record<string, unknown>): MemasterEvent => ({ standard: "memaster", version: "1.0.0", event, data: [data] });

describe("retry_reveal: only the buyer", () => {
  it("is offered to the buyer once the delay has passed", () => {
    expect(canRetryReveal(pack(), "buyer.testnet", 120, 20)).toBe(true);
    expect(canRetryReveal(pack(), "buyer.testnet", 119, 20)).toBe(false);
  });
  it("is never offered to another account, nor without a wallet", () => {
    expect(canRetryReveal(pack(), "someone.testnet", 500, 20)).toBe(false);
    expect(canRetryReveal(pack(), null, 500, 20)).toBe(false);
  });
  it("is not offered on a pack that is revealed, stuck or refunded", () => {
    for (const status of ["revealed", "stuck", "refunded"] as const)
      expect(canRetryReveal(pack({ status }), "buyer.testnet", 500, 20), status).toBe(false);
    expect(canRetryReveal(pack({ token_ids: ["70"] }), "buyer.testnet", 500, 20)).toBe(false);
  });
});

describe("refund of a stuck pack", () => {
  it("is offered on a stuck v3 pack without cards", () => {
    expect(canRefund(pack({ status: "stuck" }))).toBe(true);
    expect(canRefund(pack({ status: "pending" }))).toBe(false);
    expect(canRefund(pack({ status: "refunded" }))).toBe(false);
    expect(canRefund(pack({ status: "stuck", token_ids: ["70"] }))).toBe(false);
  });
  it("is not offered on app2 (no storage_used, no refund_stuck_pack)", () => {
    const old = pack({ status: "stuck", storage_used: undefined });
    expect(isV3Pack(old)).toBe(false);
    expect(canRefund(old)).toBe(false);
    expect(refundAmount(old)).toBeNull();
  });
  it("returns the price and the unused storage, as the contract does", () => {
    // 0.1 NEAR + (1 605 − 975) o × 10¹⁹ = 0.1063 NEAR
    expect(refundAmount(pack({ status: "stuck" }))).toBe(NEAR / 10n + 630n * 10n ** 19n);
    // Stockage utilisé au-delà du prépayé : rien de plus que le prix.
    expect(refundAmount(pack({ status: "stuck", storage_used: 2000 }))).toBe(NEAR / 10n);
  });
  it("reads the refunded total in pack_refunded", () => {
    const events = [ev("pack_refunded", { pack_id: 7, price: "1", storage_refund: "2", total: "3" })];
    expect(refundedTotal(events, 7)).toBe(3n);
    expect(refundedTotal(events, 8)).toBeNull();
    expect(refundedTotal([], 7)).toBeNull();
  });
});

describe("storage returned", () => {
  it("reads the refund in the storage block of pack_revealed", () => {
    expect(revealStorageRefund({ storage: { prepaid_bytes: 1605, used_bytes: 1034, refund: "5710000000000000000000" } })).toBe(
      5710000000000000000000n,
    );
    expect(revealStorageRefund({ pack_id: 3 })).toBeNull(); // app2 : pas de bloc storage
    expect(revealStorageRefund(undefined)).toBeNull();
  });
  it("gives the same amount from get_pack once revealed", () => {
    expect(unusedStorage(pack({ status: "revealed", storage_used: 1034 }))).toBe(571n * 10n ** 19n);
    expect(unusedStorage(pack({ storage_used: 1700 }))).toBe(0n);
    expect(unusedStorage(pack({ storage_used: undefined }))).toBeNull();
  });
  it("reads storage_refund in card_redeemed", () => {
    expect(burnStorageRefund([ev("card_redeemed", { token_id: "70", storage_refund: "160000000000000000000" })])).toBe(
      160000000000000000000n,
    );
    expect(burnStorageRefund([ev("card_redeemed", { token_id: "70" })])).toBeNull();
    expect(burnStorageRefund([])).toBeNull();
  });
});

describe("storage deposit before buying", () => {
  const attached = 1605n * 10n ** 19n;
  it("keeps the worst case and says the unused part is returned at opening (v3)", () => {
    const t = storageDepositNote(attached, true, true);
    expect(t).toMatch(/^\+ storage deposit: 0\.01605 NEAR is attached/);
    expect(t).toMatch(/worst case/);
    expect(t).toMatch(/unused part is returned to you when the pack is opened/);
    expect(t).toMatch(/0\.01 NEAR is actually used for the first pack/);
    expect(t).not.toMatch(/not returned/i);
  });
  it("promises nothing on app2", () => {
    const t = storageDepositNote(attached, false, false);
    expect(t).not.toMatch(/returned/);
    expect(t).toMatch(/about 0\.006 NEAR is actually used\)/);
    expect(storageDepositNote(attached, null, false)).toMatch(/0\.006 NEAR is actually used, 0\.01 NEAR for the first pack/);
  });
});
