// Bouton « Verify this pack » : relit la table et le pack sur la chaîne et recalcule le tirage dans le navigateur.

import { useState } from "react";
import { CONTRACT_ID, SERIES_ID } from "../config";
import { getCardDefs, getPack } from "../near/contract";
import { view } from "../near/rpc";
import { verifyPack, type Check, type PackInput, type Table } from "./verify";

async function loadTable(seriesId: number): Promise<{ table: Table; stored: string }> {
  const h = await view<{ table_hash: string | null; header: Table & Record<string, unknown> }>("get_series_header", {
    series_id: seriesId,
  });
  if (!h.table_hash) throw new Error("This series has no frozen table yet.");
  // `header.cards` est vide : on y remet les pages de cartes, à la même place (l'ordre des champs compte).
  const cards = await getCardDefs(seriesId);
  return { table: { ...h.header, cards: cards as unknown as Table["cards"] }, stored: h.table_hash };
}

export function VerifyPanel({ packId }: { packId: number }) {
  const [checks, setChecks] = useState<Check[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setBusy(true);
    setError(null);
    try {
      const pack = await getPack(packId);
      if (!pack || pack.status !== "revealed") throw new Error("This pack is not revealed yet.");
      const { table, stored } = await loadTable(pack.series_id ?? SERIES_ID);
      setChecks(await verifyPack(table, stored, pack as unknown as PackInput));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const allOk = checks?.every((c) => c.ok);
  return (
    <div className="verify">
      {!checks && (
        <button className="btn btn--ghost" onClick={run} disabled={busy}>
          {busy ? "Verifying…" : "Verify this pack"}
        </button>
      )}
      {error && <p className="error">{error}</p>}
      {checks && (
        <div className={`verify__result${allOk ? " verify__result--ok" : " verify__result--ko"}`}>
          <strong>{allOk ? "✓ Draw verified" : "✗ Verification failed"}</strong>
          <ul>
            {checks.map((c, i) => (
              <li key={i} className={c.ok ? "ok" : "ko"}>
                {c.ok ? "✓" : "✗"} {c.label}
              </li>
            ))}
          </ul>
          <p className="small muted">
            Recomputed in your browser from public on-chain data (table, seeds, draws). The exact card within a rarity
            depends on the series history: check it with the command-line verifier,{" "}
            <span className="mono">memaster_verifier pack --contract {CONTRACT_ID} --history …</span>
          </p>
        </div>
      )}
    </div>
  );
}
