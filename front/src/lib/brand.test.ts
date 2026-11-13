import { describe, expect, it } from "vitest";
import { BRAND, seriesName } from "./brand";

describe("brand", () => {
  it("shows on-chain series names under the site name", () => {
    expect(BRAND).toBe("Moonpacks");
    expect(seriesName("Memaster Entry")).toBe("Moonpacks Entry");
    expect(seriesName("Memaster v2")).toBe("Moonpacks v2");
    expect(seriesName("Gold Edition")).toBe("Gold Edition");
  });
});
