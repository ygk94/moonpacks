// Lectures typées du contrat Memaster (toutes des `view` gratuites).

import { SERIES_ID } from "../config";
import { RpcError, view } from "./rpc";
import type {
  Backing,
  CardDef,
  CardView,
  ContractConfig,
  Listing,
  NftToken,
  PackView,
  RatesPage,
  RushState,
  SeriesView,
} from "./types";

export const getConfig = () => view<ContractConfig>("get_config");
export const getSeries = (seriesId = SERIES_ID) => view<SeriesView>("get_series", { series_id: seriesId });
export const getSeriesCount = () => view<number>("get_series_count");
export const getPack = (packId: number) => view<PackView | null>("get_pack", { pack_id: packId });
export const getCard = (tokenId: string) => view<CardView | null>("get_card", { token_id: tokenId });
export const getBacking = (tokenId: string) => view<Backing | null>("get_backing", { token_id: tokenId });
export const getListing = (tokenId: string) => view<Listing | null>("get_listing", { token_id: tokenId });
/** Adossement donné par l'oracle à une carte d'un coin mort (`card_resurrected`), ou `null`. */
export const getResurrected = (seriesId: number, cardIndex: number) =>
  view<Backing | null>("get_resurrected", { series_id: seriesId, card_index: cardIndex });
export const getTableHash = (seriesId = SERIES_ID) =>
  view<{ stored: string | null; card_count: number }>("get_series_table_hash", { series_id: seriesId });

export const getRushState = (accountId?: string | null, seriesId = SERIES_ID) =>
  view<RushState>("get_rush_state", { series_id: seriesId, at_height: null, account_id: accountId ?? null });

export const getPackCount = (accountId: string) => view<number>("get_pack_count_for_owner", { account_id: accountId });

export async function getPacksForOwner(accountId: string): Promise<number[]> {
  const n = await getPackCount(accountId);
  const out: number[] = [];
  for (let from = 0; from < n; from += 100) {
    out.push(...(await view<number[]>("get_packs_for_owner", { account_id: accountId, from_index: from, limit: 100 })));
  }
  return out;
}

export async function getTokensForOwner(accountId: string): Promise<NftToken[]> {
  const out: NftToken[] = [];
  for (let from = 0; ; from += 100) {
    const page = await view<NftToken[]>("nft_tokens_for_owner", {
      account_id: accountId,
      from_index: String(from),
      limit: 100,
    });
    out.push(...page);
    if (page.length < 100) return out;
  }
}

export async function getListings(): Promise<[string, Listing][]> {
  const out: [string, Listing][] = [];
  for (let from = 0; ; from += 100) {
    const page = await view<[string, Listing][]>("get_listings", { from_index: from, limit: 100 });
    out.push(...page);
    if (page.length < 100) return out;
  }
}

/** Taux complets : toutes les pages de `get_rates`, cartes fusionnées par rareté. */
export async function getAllRates(seriesId = SERIES_ID): Promise<RatesPage> {
  let page = await view<RatesPage>("get_rates", { series_id: seriesId, from_index: 0, limit: 200 });
  const merged: RatesPage = { ...page, rarities: page.rarities.map((r) => ({ ...r, cards: [...r.cards] })) };
  while (page.next_index != null) {
    page = await view<RatesPage>("get_rates", { series_id: seriesId, from_index: page.next_index, limit: 200 });
    page.rarities.forEach((r, i) => {
      if (r.rarity !== "mythic") merged.rarities[i].cards.push(...r.cards);
    });
  }
  merged.next_index = null;
  return merged;
}

// Définitions de cartes de la série, chargées une fois (1 646 cartes = 9 pages).
let cardDefs: Promise<CardDef[]> | null = null;
export function getCardDefs(seriesId = SERIES_ID): Promise<CardDef[]> {
  if (!cardDefs) {
    cardDefs = (async () => {
      const s = await getSeries(seriesId);
      const pages: Promise<CardDef[]>[] = [];
      for (let from = 0; from < s.card_count; from += 200) {
        pages.push(view<CardDef[]>("get_series_cards", { series_id: seriesId, from_index: from, limit: 200 }));
      }
      return (await Promise.all(pages)).flat();
    })();
    cardDefs.catch(() => (cardDefs = null));
  }
  return cardDefs;
}

/**
 * Contrat v3 (stockage non utilisé rendu à l'ouverture et au burn, `refund_stuck_pack`) : reconnu à sa vue
 * `get_treasury`, absente d'app2. Sans réponse du réseau, on ne promet rien (`false`) et on réessaiera.
 */
let v3: Promise<boolean> | null = null;
export function isV3Contract(): Promise<boolean> {
  if (!v3) {
    v3 = view<unknown>("get_treasury").then(
      () => true,
      (e) => {
        if (!(e instanceof RpcError)) v3 = null;
        return false;
      },
    );
  }
  return v3;
}

/** `token_id = pack_id × 10 + emplacement`. */
export const packOfToken = (tokenId: string) => Math.floor(Number(tokenId) / 10);
