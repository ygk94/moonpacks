// Suivi d'un burn en deux temps (`redeem_started`, puis `card_redeemed` ou `redeem_failed`) quand la réponse du
// wallet ne contient pas l'issue : on relit la carte jusqu'à ce qu'elle quitte l'état `redeeming`.

import type { CardView } from "../near/types";

export type BurnOutcome = "burned" | "restored" | "pending";

export async function waitBurnOutcome(
  read: () => Promise<CardView | null>,
  { intervalMs = 2000, timeoutMs = 60_000, sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms)) } = {},
): Promise<BurnOutcome> {
  const until = Date.now() + timeoutMs;
  for (;;) {
    let card: CardView | null | undefined;
    try {
      card = await read();
    } catch {
      card = undefined; // erreur réseau passagère : on réessaie
    }
    if (card === null) return "burned";
    if (card && card.state !== "redeeming") return card.state === "burned" ? "burned" : "restored";
    if (Date.now() >= until) return "pending";
    await sleep(intervalMs);
  }
}
