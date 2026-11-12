import { describe, expect, it } from "vitest";
import { createLimiter } from "./rpc";

describe("RPC limiter", () => {
  it("runs at most n requests at once, in order", async () => {
    const limit = createLimiter(2);
    let active = 0;
    let peak = 0;
    const done: number[] = [];
    const task = (i: number) =>
      limit(async () => {
        active++;
        peak = Math.max(peak, active);
        await new Promise((r) => setTimeout(r, 5));
        active--;
        done.push(i);
        return i;
      });
    expect(await Promise.all([0, 1, 2, 3, 4].map(task))).toEqual([0, 1, 2, 3, 4]);
    expect(peak).toBe(2);
    expect(done).toHaveLength(5);
  });

  it("frees its slot when a request fails", async () => {
    const limit = createLimiter(1);
    await expect(limit(() => Promise.reject(new Error("429")))).rejects.toThrow("429");
    expect(await limit(async () => "next")).toBe("next");
  });
});
