// Client JSON-RPC minimal (fastnear). Les vues sont gratuites ; reprise courte sur 429 et erreurs réseau.

import { CONTRACT_ID, RPC_URL } from "../config";

let nextId = 1;

async function rpc<T>(method: string, params: unknown, tries = 3): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
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
    } catch (e) {
      if (e instanceof RpcError || attempt + 1 >= tries) throw e;
      await new Promise((r) => setTimeout(r, 300 * 2 ** attempt));
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
