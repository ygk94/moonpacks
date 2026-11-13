// Bouton « Verify this pack » : relit la table et le pack sur la chaîne et recalcule le tirage dans le navigateur.
// Avec l'indexeur, rejoue en plus toute la série jusqu'à ce pack : la carte exacte de chaque emplacement, la
// décision gold pack, le gold rush et la répartition de la valeur sont alors recalculés aussi.

import { useState } from "react";
import { CONTRACT_ID, SERIES_ID } from "../config";
import { fetchHistory } from "../lib/indexer";
import { getCardDefs, getPack } from "../near/contract";
import { view } from "../near/rpc";
import { replaySeries, type ChainEvent, type FullTable } from "./replay";
import { verifyPack, type Check, type PackInput, type Table } from "./verify";

async function loadTable(seriesId: number): Promise<{ table: Table & FullTable; stored: string }> {
  const h = await view<{ table_hash: string | null; header: Table & FullTable & Record<string, unknown> }>(
    "get_series_header",
    { series_id: seriesId },
  );
  if (!h.table_hash) throw new Error("This series has no frozen table yet.");
  // `header.cards` est vide : on y remet les pages de cartes, à la même place (l'ordre des champs compte).
  const cards = await getCardDefs(seriesId);
  return { table: { ...h.header, cards: cards as unknown as FullTable["cards"] }, stored: h.table_hash };
}

interface Result {
  quick: Check[];
  full: Check[] | null;
  note: string | null;
}

export function VerifyPanel({ packId }: { packId: number }) {
  const [result, setResult] = useState<Result | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setBusy(true);
    setError(null);
    try {
      const pack = await getPack(packId);
      if (pack?.status === "refunded" || pack?.status === "stuck")
        throw new Error("This pack has no draw to verify: it could not be revealed.");
      if (!pack || pack.status !== "revealed") throw new Error("This pack is not revealed yet.");
      const seriesId = pack.series_id ?? SERIES_ID;
      const [{ table, stored }, history] = await Promise.all([loadTable(seriesId), fetchHistory(seriesId)]);
      const quick = await verifyPack(table, stored, pack as unknown as PackInput);
      let full: Check[] | null = null;
      let note: string | null = null;
      const known = history?.items.some((e) => e.event === "pack_revealed" && Number(e.data.pack_id) === packId);
      if (history && known) {
        const [report] = await replaySeries(table, stored, history.items as ChainEvent[], packId);
        full = report?.checks ?? null;
        if (!history.complete) note = "The indexer is still catching up: the history may be incomplete.";
      } else {
        note = history
          ? "This pack is not indexed yet. Try again in a minute for the exact-card check."
          : "The exact-card check needs the full series history: use the command-line verifier below.";
      }
      setResult({ quick, full, note });
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const checks = result ? [...result.quick, ...(result.full ?? [])] : [];
  const allOk = checks.length > 0 && checks.every((c) => c.ok);
  return (
    <div className="verify">
      {!result && (
        <button className="btn btn--ghost" onClick={run} disabled={busy}>
          {busy ? "Verifying…" : "Verify this pack"}
        </button>
      )}
      {error && <p className="error">{error}</p>}
      {result && (
        <div className={`verify__result${allOk ? " verify__result--ok" : " verify__result--ko"}`}>
          <strong>
            {allOk ? (result.full ? "✓ Draw fully verified" : "✓ Draw verified") : "✗ Verification failed"}
          </strong>
          <h4>From the pack and the rate table</h4>
          <CheckList checks={result.quick} />
          {result.full && (
            <>
              <h4>Replaying the whole series history</h4>
              <CheckList checks={result.full} />
            </>
          )}
          {result.note && <p className="small muted">{result.note}</p>}
          <p className="small muted">
            Recomputed in your browser from public on-chain data. Command-line verifier:{" "}
            <span className="mono">memaster_verifier pack --contract {CONTRACT_ID} --history …</span>
          </p>
        </div>
      )}
    </div>
  );
}

function CheckList({ checks }: { checks: Check[] }) {
  return (
    <ul>
      {checks.map((c, i) => (
        <li key={i} className={c.ok ? "ok" : "ko"}>
          {c.ok ? "✓" : "✗"} {c.label}
        </li>
      ))}
    </ul>
  );
}
