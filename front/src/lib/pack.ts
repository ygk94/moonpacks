// Logique d'un pack côté front (contrat v3) : relance réservée à l'acheteur, remboursement d'un pack `stuck`,
// stockage rendu à l'ouverture et au burn. Fonctions pures, testées dans pack.test.ts.

import { findEvent } from "../near/events";
import { formatNear, formatNearExact } from "./format";
import type { MemasterEvent, PackView } from "../near/types";

/** 1 octet de stockage = 10¹⁹ yoctoNEAR. */
export const BYTE_COST = 10n ** 19n;

/** Contrat v3 : `get_pack` renvoie `storage_used`, et `refund_stuck_pack` existe. */
export const isV3Pack = (p: Pick<PackView, "storage_used">) => typeof p.storage_used === "number";

/**
 * `retry_reveal` (v3) : réservé à l'acheteur, sur un pack `pending` sans carte, après `retry_delay_blocks` blocs sans
 * progrès. Sur app2, n'importe qui pouvait relancer ; on ne le propose de toute façon qu'à l'acheteur.
 */
export function canRetryReveal(
  p: Pick<PackView, "status" | "owner_id" | "token_ids" | "last_progress_height">,
  accountId: string | null,
  height: number,
  retryDelayBlocks: number,
): boolean {
  return (
    !!accountId &&
    accountId === p.owner_id &&
    p.status === "pending" &&
    p.token_ids.length === 0 &&
    height >= p.last_progress_height + retryDelayBlocks
  );
}

/** `refund_stuck_pack` : pack `stuck` sans carte, contrat v3. Ouvert à tous : l'argent va toujours à l'acheteur. */
export function canRefund(p: Pick<PackView, "status" | "token_ids" | "storage_used">): boolean {
  return p.status === "stuck" && p.token_ids.length === 0 && isV3Pack(p);
}

/**
 * Montant rendu par `refund_stuck_pack` (yoctoNEAR) : prix + stockage prépayé non utilisé, comme le contrat
 * (`storage_per_pack − storage_used`, jamais négatif). `null` sans `storage_used` (app2).
 */
export function refundAmount(p: Pick<PackView, "price_paid" | "storage_prepaid" | "storage_used">): bigint | null {
  const unused = unusedStorage(p);
  return unused == null ? null : BigInt(p.price_paid) + unused;
}

/**
 * Stockage prépayé non utilisé (yoctoNEAR) : `storage_prepaid − storage_used × 10¹⁹`, jamais négatif. Pour un pack
 * tiré, c'est exactement ce que le dernier reçu a rendu (`pack_revealed.storage.refund`) : `storage_used` ne change
 * plus après le tirage. `null` sur app2.
 */
export function unusedStorage(p: Pick<PackView, "storage_prepaid" | "storage_used">): bigint | null {
  if (!isV3Pack(p)) return null;
  const unused = BigInt(p.storage_prepaid) - BigInt(p.storage_used!) * BYTE_COST;
  return unused > 0n ? unused : 0n;
}

const asYocto = (v: unknown): bigint | null => (typeof v === "string" && /^\d+$/.test(v) ? BigInt(v) : null);

/** Total rendu d'après l'événement `pack_refunded` d'une transaction, ou `null`. */
export function refundedTotal(events: MemasterEvent[], packId: number): bigint | null {
  const e = events.find((x) => x.event === "pack_refunded" && Number(x.data?.[0]?.pack_id) === packId)?.data?.[0];
  return e ? asYocto(e.total) : null;
}

/** Stockage rendu à l'ouverture : `pack_revealed.storage.refund` (yoctoNEAR), ou `null` (app2, ou absent). */
export function revealStorageRefund(data: Record<string, unknown> | undefined): bigint | null {
  const s = data?.storage as { refund?: unknown } | undefined;
  return s ? asYocto(s.refund) : null;
}

/** Stockage rendu au burn : `card_redeemed.storage_refund` (yoctoNEAR), ou `null`. */
export function burnStorageRefund(events: MemasterEvent[]): bigint | null {
  return asYocto(findEvent(events, "card_redeemed")?.storage_refund);
}

// Stockage effectivement consommé (mesuré sur testnet) : environ 1 034 o au premier pack d'un compte, 602 o
// ensuite (docs/testnet.md ; +4 o en v3). Le contrat demande le pire cas.
export const STORAGE_FIRST_PACK = 1034n;
export const STORAGE_NEXT_PACK = 602n;

/**
 * Texte du dépôt de stockage avant l'achat. Le dépôt joint reste le pire cas (`required_deposit − price`) ; en v3,
 * l'excédent est rendu à l'ouverture, en app2 il reste au contrat.
 */
export function storageDepositNote(attached: bigint, firstPack: boolean | null, v3: boolean): string {
  const used = (bytes: bigint) => formatNear(bytes * BYTE_COST, 3);
  const estimate =
    firstPack == null
      ? `about ${used(STORAGE_NEXT_PACK)} NEAR is actually used, ${used(STORAGE_FIRST_PACK)} NEAR for the first pack of an account`
      : `about ${used(firstPack ? STORAGE_FIRST_PACK : STORAGE_NEXT_PACK)} NEAR is actually used${firstPack ? " for the first pack of an account" : ""}`;
  const head = `+ storage deposit: ${formatNearExact(attached)} NEAR is attached to pay for the cards' on-chain storage in the worst case`;
  return v3
    ? `${head}. The unused part is returned to you when the pack is opened (${estimate}).`
    : `${head} (${estimate}).`;
}
