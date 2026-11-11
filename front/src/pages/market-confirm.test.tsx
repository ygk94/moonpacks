// Consigne : pas d'achat en un clic. « Buy » ouvre un récapitulatif (prix exact, redevances) avant la signature.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { BuyConfirm } from "./Market";

const row = {
  tokenId: "123",
  listing: { seller_id: "seller.testnet", price: "123456789000000000000000", deposit: "0" },
  card: null,
  ticker: "ZZTEST",
  name: "Test coin",
};

describe("market purchase confirmation", () => {
  it("shows the exact price in NEAR before signing", () => {
    const html = renderToStaticMarkup(<BuyConfirm row={row} nearPrice={null} onConfirm={() => {}} onCancel={() => {}} />);
    expect(html).toContain("You pay exactly <strong>0.123456789 NEAR</strong>");
    expect(html).toContain("Confirm and buy for 0.123456789 NEAR");
    expect(html).toMatch(/Royalties are taken from the price/);
    expect(html).toContain("Cancel");
  });

  it("does not sign from the listing button", () => {
    const src = readFileSync(resolve(__dirname, "Market.tsx"), "utf8");
    expect(src).not.toMatch(/onClick=\{\(\) => buy\(r\)\}/);
    expect(src).toMatch(/onClick=\{\(\) => setConfirming\(r\)\}/);
  });
});
