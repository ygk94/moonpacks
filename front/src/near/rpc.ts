// Client JSON-RPC minimal (fastnear). Les vues sont gratuites. fastnear limite le débit (429, souvent sans en-tête
// CORS : le navigateur n'y voit qu'un échec réseau) : au plus MAX_INFLIGHT requêtes à la fois, et reprise avec un
// recul exponentiel (0,4 s, 0,8 s, 1,6 s, 3,2 s) sur 429, 5xx et échec réseau. Une erreur du contrat ne se reprend pas.

import { CONTRACT_ID, RPC_URL } from "../config";

let nextId = 1;
const MAX_INFLIGHT = 6;
const TRIES = 5;

/** File d'attente : au plus `n` tâches en cours. */
export function createLimiter(n: number) {
  let active = 0;
  const waiting: (() => void)[] = [];
  return async function limit<T>(task: () => Promise<T>): Promise<T> {
    if (active >= n) await new Promise<void>((r) => waiting.push(r));
    active++;
    try {
      return await task();
    } finally {
      active--;
      waiting.shift()?.();
    }
  };
}
const limit = createLimiter(MAX_INFLIGHT);

async function rpc<T>(method: string, params: unknown, tries = TRIES): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await limit(async () => {
        const res = await fetch(RPC_URL, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ jsonrpc: "2.0", id: nextId++, method, params }),
        });
        if (res.status === 429 || res.status >= 500) throw new Error(`RPC ${res.status}`);
        const body = await res.json();
        if (body.error) {
          const msg = body.error?.data ?? body.error?.cause?.name ?? body.error?.message ?? "RPC error";
          throw new RpcError(typeof msg === "string" ? msg : JSON.stringify(msg));
        }
        return body.result as T;
      });
    } catch (e) {
      if (e instanceof RpcError || attempt + 1 >= tries) throw e;
      // Hors de la file pendant l'attente : les autres requêtes avancent.
      await new Promise((r) => setTimeout(r, 400 * 2 ** attempt * (0.75 + Math.random() / 2)));
    }
  }
}

export class RpcError extends Error {}

function b64(s: string): string {
  return btoa(String.fromCharCode(...new TextEncoder().encode(s)));
}

/** Appel `view` du contrat (gratuit). */
export async function view<T>(method: string, args: Record<string, unknown> = {}, contractId = CONTRACT_ID): Promise<T> {
  const r = await rpc<{ result?: number[]; error?: string }>("query", {
    request_type: "call_function",
    finality: "optimistic",
    account_id: contractId,
    method_name: method,
    args_base64: b64(JSON.stringify(args)),
  });
  if (r.error) throw new RpcError(r.error);
  const text = new TextDecoder().decode(new Uint8Array(r.result ?? []));
  return (text ? JSON.parse(text) : null) as T;
}

export async function blockHeight(): Promise<number> {
  const b = await rpc<{ header: { height: number } }>("block", { finality: "optimistic" });
  return b.header.height;
}

export async function viewAccount(accountId: string): Promise<{ amount: string; code_hash: string; storage_usage: number }> {
  return rpc("query", { request_type: "view_account", finality: "final", account_id: accountId });
}

/** Statut d'une transaction et de tous ses reçus (pour relire les événements). */
export async function txStatus(hash: string, signerId: string): Promise<TxOutcome> {
  return rpc("EXPERIMENTAL_tx_status", { tx_hash: hash, sender_account_id: signerId, wait_until: "EXECUTED" });
}

export interface TxOutcome {
  status: { SuccessValue?: string; Failure?: unknown } | string;
  transaction: { hash: string; signer_id: string };
  transaction_outcome: { outcome: { logs: string[] } };
  receipts_outcome: { outcome: { logs: string[]; status: unknown; executor_id: string } }[];
}
