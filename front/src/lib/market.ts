// Achat sur le marché : répartition du prix (NEP-199, `nft_payout`) affichée avant de confirmer.
// L'acheteur paie exactement le prix de l'annonce ; les redevances de la série sont prises sur ce prix.

export interface PayoutBreakdown {
  price: bigint;
  royalties: { account: string; amount: bigint }[];
  royaltyTotal: bigint;
  seller: bigint;
}

/** `payout` : réponse de `nft_payout(token_id, balance = prix)`, `{ payout: { compte: yocto } }`. */
export function payoutBreakdown(payout: { payout: Record<string, string> }, sellerId: string, price: string): PayoutBreakdown {
  const p = BigInt(price);
  const royalties = Object.entries(payout.payout)
    .filter(([account]) => account !== sellerId)
    .map(([account, amount]) => ({ account, amount: BigInt(amount) }))
    .filter((r) => r.amount > 0n)
    .sort((a, b) => (b.amount > a.amount ? 1 : b.amount < a.amount ? -1 : a.account.localeCompare(b.account)));
  const royaltyTotal = royalties.reduce((s, r) => s + r.amount, 0n);
  const seller = BigInt(payout.payout[sellerId] ?? "0");
  return { price: p, royalties, royaltyTotal, seller };
}
