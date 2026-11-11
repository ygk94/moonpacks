// Consigne : pas d'achat en un clic. Le bouton d'une annonce ouvre la confirmation, il ne signe pas.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("market buy button", () => {
  it("opens the confirmation instead of signing", () => {
    const src = readFileSync(resolve(__dirname, "Market.tsx"), "utf8");
    expect(src).not.toMatch(/onClick=\{\(\) => buy\(r\)\}/);
    expect(src).toMatch(/onClick=\{\(\) => setConfirming\(r\)\}/);
    expect(src).toMatch(/onConfirm=\{\(\) => buy\(confirming\)\}/);
  });
});
