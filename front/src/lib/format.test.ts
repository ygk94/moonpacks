import { describe, expect, it } from "vitest";
import { formatDuration, formatNear, formatNearExact, formatQty, formatUsd, parseNear, shortAccount, yoctoToNumber } from "./format";
import { burnableLast } from "./reveal";

describe("NEAR amounts", () => {
  it("formats yoctoNEAR", () => {
    expect(formatNear("100000000000000000000000")).toBe("0.1");
    expect(formatNear("116050000000000000000000")).toBe("0.116");
    expect(formatNear("116050000000000000000000", 6)).toBe("0.11605");
    expect(formatNear("3000000000000000000000000")).toBe("3");
    expect(formatNear("1")).toBe("0");
  });
  it("parses user input to yoctoNEAR", () => {
    expect(parseNear("0.5")).toBe("500000000000000000000000");
    expect(parseNear("1,25")).toBe("1250000000000000000000000");
    expect(parseNear("2")).toBe("2000000000000000000000000");
    expect(parseNear(".01")).toBe("10000000000000000000000");
    expect(() => parseNear("abc")).toThrow();
    expect(() => parseNear("")).toThrow();
    expect(() => parseNear("-1")).toThrow();
  });
  it("rejects ambiguous input instead of reading part of it", () => {
    expect(() => parseNear("1.2.3")).toThrow();
    expect(() => parseNear("1,000.5")).toThrow();
    expect(() => parseNear("0." + "1".repeat(25))).toThrow();
    expect(parseNear("0." + "0".repeat(23) + "1")).toBe("1");
    expect(parseNear(" 3 ")).toBe("3000000000000000000000000");
  });
  it("shows a price to pay exactly, never rounded down to 0", () => {
    expect(formatNear("50000000000000000000")).toBe("0");
    expect(formatNearExact("50000000000000000000")).toBe("0.00005");
    expect(formatNearExact("1234567890000000000000001")).toBe("1.234567890000000000000001");
    expect(formatNearExact(16n * 10n ** 21n)).toBe("0.016");
    expect(formatNearExact("0")).toBe("0");
  });
  it("keeps yoctoNEAR in BigInt: no float drift on large amounts", () => {
    const big = "123456789012345678901234567890";
    expect(parseNear(formatNearExact(big))).toBe(big);
    expect(formatNearExact(BigInt(parseNear("0.1")) + BigInt(parseNear("0.016")))).toBe("0.116");
  });
  it("round-trips", () => {
    expect(formatNear(parseNear("0.0123"))).toBe("0.0123");
    expect(yoctoToNumber(parseNear("0.04"))).toBeCloseTo(0.04);
  });
});

describe("display formats", () => {
  it("compacts token quantities without scientific notation", () => {
    expect(formatQty(1_234_567)).toBe("1.23M");
    expect(formatQty(1.47e16)).not.toMatch(/e/);
    expect(formatQty(42)).toBe("42");
    expect(formatQty(0.000123)).toBe("0.000123");
    expect(formatQty(Number.NaN)).toBe("—");
    expect(formatQty(0)).toBe("0");
    expect(formatQty(Infinity)).toBe("—");
  });
  it("formats dollars for memecoin prices", () => {
    expect(formatUsd(3.68)).toBe("$3.68");
    expect(formatUsd(0.368)).toBe("$0.368");
    expect(formatUsd(0.00001234)).toBe("$0.0000123");
    expect(formatUsd(1234)).toBe("$1234");
    expect(formatUsd(0)).toBe("$0");
    expect(formatUsd(Number.NaN)).toBe("—");
  });
  it("formats durations", () => {
    expect(formatDuration(1800)).toBe("30m 00s");
    expect(formatDuration(3600)).toBe("1h 00m");
    expect(formatDuration(-5)).toBe("0s");
  });
  it("shortens accounts", () => {
    expect(shortAccount("0x1234567890abcdef1234567890abcdef12345678")).toBe("0x1234…5678");
    expect(shortAccount("alice.testnet")).toBe("alice.testnet");
  });
});

describe("reveal order", () => {
  it("keeps slot order and moves burnable cards last", () => {
    const cards = [
      { slot: 0, burnable: false },
      { slot: 1, burnable: true },
      { slot: 2, burnable: false },
      { slot: 3, burnable: false },
      { slot: 4, burnable: true },
    ];
    expect(burnableLast(cards).map((c) => c.slot)).toEqual([0, 2, 3, 1, 4]);
  });
});
