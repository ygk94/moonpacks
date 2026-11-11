// Fiches publiques des cartes (public/catalog.json, généré depuis docs/data/catalogue-v2.json).
// Les mythiques n'y figurent pas : le front les montre toutes en « ? ».

import type { Rarity } from "../near/types";

export interface CatalogEntry {
  no: string;
  ticker: string;
  name: string;
  chain: string | null;
  state: "active" | "declining" | "dead" | "unknown";
  address: string | null;
  coingecko: string | null;
}

let catalog: Promise<Record<string, CatalogEntry>> | null = null;

export function loadCatalog(): Promise<Record<string, CatalogEntry>> {
  if (!catalog) {
    catalog = fetch("/catalog.json").then((r) => (r.ok ? r.json() : {}));
    catalog.catch(() => (catalog = null));
  }
  return catalog;
}

/** Carte d'un NFT de la collection, d'après `metadata.extra`. Une mythique n'a ni identité ni ticker : « ? ». */
export function cardFromToken(
  token: { token_id: string; metadata: { extra: string | null } | null },
  catalog: Record<string, CatalogEntry>,
): { tokenId: string; cardId: string | null; rarity: Rarity; burnable: boolean; packId: number; ticker: string } {
  let extra: { card_id?: string; rarity?: Rarity; burnable?: boolean; pack_id?: number } = {};
  try {
    extra = JSON.parse(token.metadata?.extra ?? "{}") ?? {};
  } catch {
    // métadonnées sans extra lisible
  }
  const rarity = extra.rarity ?? "common";
  const cardId = rarity === "mythic" ? null : (extra.card_id ?? null);
  const e = cardId ? catalog[cardId] : undefined;
  return {
    tokenId: token.token_id,
    cardId,
    rarity,
    burnable: !!extra.burnable,
    packId: extra.pack_id ?? Math.floor(Number(token.token_id) / 10),
    ticker: rarity === "mythic" ? "?" : (e?.ticker ?? cardId ?? "?"),
  };
}

export const MYTHIC_IMAGE = "/cards/dos-mythique.svg";

export function cardImage(cardId: string | null | undefined): string {
  return cardId ? `/cards/${cardId}.svg` : MYTHIC_IMAGE;
}

export const STATE_LABEL: Record<CatalogEntry["state"], string> = {
  active: "Active",
  declining: "Declining",
  dead: "Dead",
  unknown: "Status unknown",
};
