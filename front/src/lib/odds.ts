// Les packs en vente ont-ils les mêmes cotes ? Sur app3, « Entry » et « Standard » ont la même table de tirage :
// seuls le prix et la valeur bloquée dans la carte brûlable changent (proportionnelle au prix). On l'affiche ainsi,
// et la page « Odds » ne montre qu'une table. Si un jour les tables diffèrent, le sélecteur de série revient.

import { getRatesFirstPage } from "../near/contract";
import type { RatesPage, SeriesView } from "../near/types";

/** Empreinte des cotes d'une série : probabilités par rareté (normales, rush, gold) et des premières cartes. */
export function oddsSignature(page: RatesPage): string {
  return JSON.stringify(
    page.rarities.map((r) => [
      r.rarity,
      r.rarity_ppb,
      r.rush_rarity_ppb,
      r.gold_slot_ppb,
      r.cards.map((c) => [c.card_id ?? c.commitment ?? c.mythic_index, c.ppb, !!c.burnable]),
    ]),
  );
}

export function sameOdds(pages: RatesPage[]): boolean {
  return pages.every((p) => oddsSignature(p) === oddsSignature(pages[0]));
}

export async function seriesShareOdds(list: SeriesView[]): Promise<boolean> {
  if (list.length < 2) return true;
  return sameOdds(await Promise.all(list.map((s) => getRatesFirstPage(s.series_id))));
}

/** Ligne qui distingue un pack des autres quand les cotes sont les mêmes : la quantité de jetons, jamais un rendement. */
export function packBlurb(series: SeriesView, list: SeriesView[], shared: boolean): string {
  if (list.length < 2 || !shared) return `${series.cards_per_pack} cards · at least one burnable`;
  const min = list.reduce((m, s) => (BigInt(s.price) < m ? BigInt(s.price) : m), BigInt(list[0].price));
  const ratio = Number((BigInt(series.price) * 100n) / min) / 100;
  if (ratio <= 1) return "Same cards and odds as every pack · smallest token stash";
  const r = Number.isInteger(ratio) ? String(ratio) : ratio.toFixed(1).replace(/\.0$/, "");
  return `Same cards and odds · ${r}× the tokens in the burnable card`;
}
