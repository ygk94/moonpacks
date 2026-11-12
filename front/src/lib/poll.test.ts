import { describe, expect, it } from "vitest";
import { readUntil } from "./poll";

const noSleep = { sleep: async () => {} };

describe("readUntil", () => {
  it("re-reads a stale value until the expected state shows up", async () => {
    const values = [null, null, { listed: true }];
    let n = 0;
    const v = await readUntil(async () => values[n++], (x) => x?.listed === true, noSleep);
    expect(v).toEqual({ listed: true });
    expect(n).toBe(3);
  });

  it("gives up after `tries` and returns the last value, network errors included", async () => {
    let n = 0;
    const v = await readUntil(
      async () => {
        n++;
        if (n === 1) throw new Error("network");
        return "old";
      },
      (x) => x === "new",
      { ...noSleep, tries: 4 },
    );
    expect(v).toBe("old");
    expect(n).toBe(4);
  });
});
