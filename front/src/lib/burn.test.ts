import { describe, expect, it } from "vitest";
import type { CardView } from "../near/types";
import { waitBurnOutcome } from "./burn";

const card = (state: CardView["state"]) => ({ state }) as CardView;
const seq = (...xs: (CardView | null | Error)[]) => {
  let i = 0;
  return async () => {
    const x = xs[Math.min(i++, xs.length - 1)];
    if (x instanceof Error) throw x;
    return x;
  };
};
const fast = { intervalMs: 0, sleep: async () => undefined };

describe("burn outcome", () => {
  it("waits while the card is redeeming, then reports the burn", async () => {
    expect(await waitBurnOutcome(seq(card("redeeming"), card("redeeming"), null), fast)).toBe("burned");
    expect(await waitBurnOutcome(seq(card("redeeming"), card("burned")), fast)).toBe("burned");
  });
  it("reports a restored card after redeem_failed", async () => {
    expect(await waitBurnOutcome(seq(card("redeeming"), card("normal")), fast)).toBe("restored");
  });
  it("survives a network error", async () => {
    expect(await waitBurnOutcome(seq(new Error("RPC 429"), null), fast)).toBe("burned");
  });
  it("gives up after the timeout without claiming an outcome", async () => {
    expect(await waitBurnOutcome(seq(card("redeeming")), { ...fast, timeoutMs: 0 })).toBe("pending");
  });
});
