// Lecture des événements NEP-297 (`EVENT_JSON:`) dans les journaux d'une transaction.

import type { MemasterEvent } from "./types";
import type { TxOutcome } from "./rpc";

const PREFIX = "EVENT_JSON:";

export function parseLogs(logs: string[]): MemasterEvent[] {
  const out: MemasterEvent[] = [];
  for (const l of logs) {
    if (!l.startsWith(PREFIX)) continue;
    try {
      const e = JSON.parse(l.slice(PREFIX.length)) as MemasterEvent;
      if (e.standard === "memaster") out.push(e);
    } catch {
      // journal mal formé : ignoré
    }
  }
  return out;
}

/** Tous les événements Memaster d'une transaction, reçus compris, dans l'ordre d'exécution. */
export function eventsOf(outcome: Pick<TxOutcome, "transaction_outcome" | "receipts_outcome">): MemasterEvent[] {
  const logs = [
    ...(outcome.transaction_outcome?.outcome.logs ?? []),
    ...(outcome.receipts_outcome ?? []).flatMap((r) => r.outcome.logs),
  ];
  return parseLogs(logs);
}

export function findEvent(events: MemasterEvent[], name: string): Record<string, unknown> | undefined {
  const data = events.find((e) => e.event === name)?.data;
  return Array.isArray(data) ? data[0] : undefined;
}

/** Hash de la transaction renvoyée par un wallet : résultat complet, `transaction_outcome.id`, ou hash seul. */
export function txHashOf(out: unknown): string | undefined {
  if (typeof out === "string") return /^[1-9A-HJ-NP-Za-km-z]{43,44}$/.test(out) ? out : undefined;
  if (!out || typeof out !== "object") return undefined;
  const o = out as { transaction?: { hash?: unknown }; transaction_outcome?: { id?: unknown } };
  const h = o.transaction?.hash ?? o.transaction_outcome?.id;
  return typeof h === "string" && h ? h : undefined;
}

/** Valeur de retour d'une transaction réussie (JSON), ou `undefined`. */
export function returnValue<T>(outcome: { status: TxOutcome["status"] }): T | undefined {
  const s = outcome.status;
  if (typeof s !== "object" || !s || typeof s.SuccessValue !== "string" || !s.SuccessValue) return undefined;
  try {
    return JSON.parse(atob(s.SuccessValue)) as T;
  } catch {
    return undefined;
  }
}

/** Message d'échec lisible d'une transaction (panique du contrat comprise). */
export function failureOf(outcome: Pick<TxOutcome, "status" | "receipts_outcome">): string | undefined {
  const all = [outcome.status, ...(outcome.receipts_outcome ?? []).map((r) => r.outcome.status)];
  for (const s of all) {
    if (s && typeof s === "object" && "Failure" in s && s.Failure) return describeFailure(s.Failure);
  }
  return undefined;
}

function describeFailure(f: unknown): string {
  const text = JSON.stringify(f);
  const m = text.match(/Smart contract panicked: ([^"\\]+)/);
  return m ? m[1] : text.slice(0, 300);
}
