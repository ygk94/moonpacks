// Fiches publiques des cartes (public/catalog.json, généré depuis docs/data/catalogue-v2.json).
// Les mythiques n'y figurent pas : le front les montre toutes en « ? ».

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
