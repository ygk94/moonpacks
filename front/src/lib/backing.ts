// Quantité de jetons d'une carte brûlable.
//
// Sur testnet, l'adossement (`amount`) est une part de la valeur du pack en yoctoNEAR (docs/mechanics.md,
// « Adossement transmis ») : la conversion en jetons dépend du financement, pas encore décidé. Le front l'estime
// donc avec les cours publics (NEAR/USD et cours du coin). On n'affiche que la quantité de jetons, jamais un
// rendement ni une « valeur garantie ».

import type { CatalogEntry } from "./catalog";
import { yoctoToNumber } from "./format";
import { coinUsd, nearUsd } from "./prices";

export interface TokenEstimate {
  qty: number | null;
  ticker: string;
}

export async function estimateTokens(amountYocto: string, coin: CatalogEntry | undefined): Promise<TokenEstimate> {
  const ticker = coin?.ticker ?? "tokens";
  if (!coin) return { qty: null, ticker };
  const [n, c] = await Promise.all([nearUsd(), coinUsd(coin)]);
  if (!n || !c) return { qty: null, ticker };
  return { qty: (yoctoToNumber(amountYocto) * n) / c, ticker };
}
