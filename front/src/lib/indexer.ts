// Client de l'indexeur (front/indexer/). Facultatif : sans VITE_INDEXER_URL ou s'il ne répond pas,
// les fonctions renvoient `null` et le front se rabat sur ce que le contrat donne directement.

import { INDEXER_URL } from "../config";
import type { Rarity } from "../near/types";

export interface TrendingItem {
  card_id: string | null;
  kind: "visible" | "mythic";
  rarity: Rarity;
  sales: number;
  listings: number;
  volume: string;
  last_price: string | null;
  score: number;
}

export interface SaleItem {
  height: number;
  ts: number;
  token_id: string;
  price: string;
  seller_id: string;
  buyer_id: string;
  card_id: string | null;
  kind: "visible" | "mythic" | null;
  rarity: Rarity | null;
}

async function get<T>(path: string): Promise<T | null> {
  if (!INDEXER_URL) return null;
  try {
    const r = await fetch(`${INDEXER_URL}${path}`, { signal: AbortSignal.timeout(4000) });
    return r.ok ? ((await r.json()) as T) : null;
  } catch {
    return null;
  }
}

export const fetchTrending = (hours = 24) =>
  get<{ hours: number; items: TrendingItem[] }>(`/trending?hours=${hours}&limit=8`);

export const fetchSales = () => get<{ items: SaleItem[] }>("/sales?limit=12");

/** Historique d'une série (achats, tirages, burns, résurrections) dans l'ordre d'exécution, pour le rejeu. */
export const fetchHistory = (seriesId: number) =>
  get<{ complete: boolean; items: { event: string; data: Record<string, unknown> }[] }>(`/history?series_id=${seriesId}`);
