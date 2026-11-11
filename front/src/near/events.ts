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
  return events.find((e) => e.event === name)?.data[0];
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
