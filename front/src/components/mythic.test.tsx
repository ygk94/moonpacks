// Mythiques invisibles (consigne, règle 2) : quelle que soit l'identité transmise, une mythique s'affiche
// comme la carte « ? » commune, sans nom, sans ticker et sans visuel propre.

import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { cardFromToken, cardImage, MYTHIC_IMAGE, type CatalogEntry } from "../lib/catalog";
import { Card } from "./Card";

// Identité factice : si elle apparaît dans le rendu, la mythique fuit.
const SECRET_ID = "zorblax-coin-zrbx";

describe("mythic cards render as “?”", () => {
  it("uses the shared “?” visual and label, whatever the card id or title", () => {
    const html = renderToStaticMarkup(<Card cardId={SECRET_ID} rarity="mythic" title="ZRBX" burnable />);
    expect(html).toContain(`src="${MYTHIC_IMAGE}"`);
    expect(html).toContain('aria-label="?, mythic, burnable"');
    expect(html).not.toMatch(/zorblax|zrbx/i);
  });

  it("renders the three mythics identically", () => {
    const a = renderToStaticMarkup(<Card cardId="m-a" rarity="mythic" title="A" />);
    const b = renderToStaticMarkup(<Card cardId="m-b" rarity="mythic" title="B" />);
    const c = renderToStaticMarkup(<Card cardId={null} rarity="mythic" />);
    expect(a).toBe(c);
    expect(b).toBe(c);
  });

  it("shows a visible card with its own visual", () => {
    const html = renderToStaticMarkup(<Card cardId="bonk-bonk" rarity="common" title="BONK" />);
    expect(html).toContain('src="/cards/bonk-bonk.svg"');
    expect(cardImage(null)).toBe(MYTHIC_IMAGE);
  });

  it("drops the identity of a mythic NFT in the collection", () => {
    const catalog: Record<string, CatalogEntry> = {
      "bonk-bonk": { no: "1", ticker: "BONK", name: "Bonk", chain: "Solana", state: "active", address: null, coingecko: null },
    };
    const mythic = cardFromToken(
      { token_id: "123", metadata: { extra: JSON.stringify({ card_id: SECRET_ID, rarity: "mythic", burnable: true, pack_id: 12 }) } },
      catalog,
    );
    expect(mythic).toEqual({ tokenId: "123", cardId: null, rarity: "mythic", burnable: true, packId: 12, ticker: "?" });
    const visible = cardFromToken({ token_id: "45", metadata: { extra: JSON.stringify({ card_id: "bonk-bonk", rarity: "rare" }) } }, catalog);
    expect(visible).toMatchObject({ cardId: "bonk-bonk", rarity: "rare", ticker: "BONK", packId: 4, burnable: false });
    expect(cardFromToken({ token_id: "7", metadata: { extra: "{oops" } }, catalog)).toMatchObject({ rarity: "common", ticker: "?" });
  });
});
