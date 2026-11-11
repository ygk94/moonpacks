// Transparence : taux de drop publiés on-chain (`get_rates`, paginé), hash de la table, hash du code du contrat,
// et comment vérifier soi-même un tirage avec verifier/.

import { useMemo, useState } from "react";
import { Card } from "../components/Card";
import { CONTRACT_ID, EXPLORER, SERIES_ID } from "../config";
import { loadCatalog } from "../lib/catalog";
import { RARITY_LABEL } from "../lib/format";
import { useAsync } from "../lib/useAsync";
import { getAllRates, getTableHash } from "../near/contract";
import { viewAccount } from "../near/rpc";
import { RARITIES, type RatesCard, type Rarity } from "../near/types";

const PAGE = 50;

function pctFromPpb(ppb: number): string {
  const p = ppb / 1e7;
  if (p >= 1) return `${p.toFixed(2)}%`;
  if (p >= 0.01) return `${p.toFixed(3)}%`;
  return `${p.toPrecision(2)}%`;
}

function oneIn(ppb: number): string {
  if (!ppb) return "—";
  const n = 1e9 / ppb;
  return `1 in ${n >= 1000 ? Math.round(n).toLocaleString("en-US") : n.toPrecision(3)}`;
}

export function Transparency() {
  const rates = useAsync(() => getAllRates(), []);
  const hash = useAsync(() => getTableHash(), []);
  const account = useAsync(() => viewAccount(CONTRACT_ID), []);
  const catalog = useAsync(() => loadCatalog(), []);
  const [query, setQuery] = useState("");
  const [rarity, setRarity] = useState<Rarity | "all">("all");
  const [onlyBurnable, setOnlyBurnable] = useState(false);
  const [page, setPage] = useState(0);

  const rows = useMemo(() => {
    if (!rates.data) return [];
    const out: (RatesCard & { rarity: Rarity; ticker: string; name: string })[] = [];
    for (const r of rates.data.rarities) {
      for (const c of r.cards) {
        const e = c.card_id ? catalog.data?.[c.card_id] : undefined;
        out.push({ ...c, rarity: r.rarity, ticker: r.rarity === "mythic" ? "?" : (e?.ticker ?? c.card_id ?? "?"), name: r.rarity === "mythic" ? "?" : (e?.name ?? "") });
      }
    }
    const q = query.trim().toLowerCase();
    return out.filter(
      (c) =>
        (rarity === "all" || c.rarity === rarity) &&
        (!onlyBurnable || c.burnable) &&
        (!q || c.ticker.toLowerCase().includes(q) || c.name.toLowerCase().includes(q)),
    );
  }, [rates.data, catalog.data, query, rarity, onlyBurnable]);

  const pages = Math.max(1, Math.ceil(rows.length / PAGE));
  const shown = rows.slice(page * PAGE, page * PAGE + PAGE);
  const gold = rates.data?.rarities.find((r) => r.gold_slot_ppb)?.gold_slot_ppb?.length ?? 0;

  return (
    <div className="page transparency">
      <h1>Drop rates &amp; transparency</h1>
      <p className="muted">
        Every rate below is read directly from the contract. The cards are drawn on-chain from a table whose hash was
        frozen when the series opened, so anyone can check that the published rates are the ones used.
      </p>

      <section className="panel">
        <h2>Chance per card slot</h2>
        {rates.loading && !rates.data && <p className="muted">Reading the rates from the contract…</p>}
        {rates.error != null && <p className="error">Could not read the rates.</p>}
        {rates.data && (
          <table className="table">
            <thead>
              <tr>
                <th>Rarity</th>
                <th>Chance</th>
                <th>During a gold rush</th>
                <th>Cards</th>
                <th>Burnable</th>
              </tr>
            </thead>
            <tbody>
              {RARITIES.slice()
                .reverse()
                .map((r) => {
                  const x = rates.data!.rarities.find((y) => y.rarity === r)!;
                  return (
                    <tr key={r}>
                      <td className={`rarity-text-${r}`}>{RARITY_LABEL[r]}</td>
                      <td>
                        {pctFromPpb(x.rarity_ppb)} <small className="muted">({oneIn(x.rarity_ppb)})</small>
                      </td>
                      <td>{x.rush_rarity_ppb != null ? pctFromPpb(x.rush_rarity_ppb) : "—"}</td>
                      <td>{x.cards.length}</td>
                      <td>{x.cards.filter((c) => c.burnable).length}</td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        )}
        <p className="small muted">
          A pack has 5 slots. The last slot always holds a burnable card. Mythic cards stay sealed: they all show as “?”.
          {gold > 0 && " Gold packs are very rare special packs with better odds on every slot and no common card."}
        </p>
      </section>

      <section className="panel">
        <h2>Every card</h2>
        <div className="filters">
          <input
            className="search"
            placeholder="Search a coin"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(0);
            }}
          />
          <button className={`chip${rarity === "all" ? " chip--on" : ""}`} onClick={() => (setRarity("all"), setPage(0))}>
            All
          </button>
          {RARITIES.map((r) => (
            <button key={r} className={`chip chip--${r}${rarity === r ? " chip--on" : ""}`} onClick={() => (setRarity(r), setPage(0))}>
              {RARITY_LABEL[r]}
            </button>
          ))}
          <label className="toggle">
            <input type="checkbox" checked={onlyBurnable} onChange={(e) => (setOnlyBurnable(e.target.checked), setPage(0))} />
            Burnable only
          </label>
        </div>
        <div className="rates-list">
          {shown.map((c) => (
            <div key={`${c.rarity}-${c.index ?? c.mythic_index}`} className="rates-list__row">
              <Card cardId={c.rarity === "mythic" ? null : (c.card_id ?? null)} rarity={c.rarity} size="sm" tilt={false} />
              <div className="rates-list__name">
                <strong>{c.ticker}</strong>
                <small className="muted">{c.name}</small>
              </div>
              <span className={`rarity-text-${c.rarity}`}>{RARITY_LABEL[c.rarity]}</span>
              <span title={`${c.ppb} parts per billion per slot`}>{oneIn(c.ppb)}</span>
              <span>{c.burnable ? "🔥 Burnable" : ""}</span>
              <span className="muted small">
                {c.minted} drawn{c.cap != null ? ` / ${c.cap} max` : ""}
              </span>
            </div>
          ))}
        </div>
        {rows.length > PAGE && (
          <div className="pager">
            <button className="btn btn--ghost" disabled={page === 0} onClick={() => setPage(page - 1)}>
              ← Previous
            </button>
            <span className="muted">
              {page + 1} / {pages}
            </span>
            <button className="btn btn--ghost" disabled={page + 1 >= pages} onClick={() => setPage(page + 1)}>
              Next →
            </button>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>Verify it yourself</h2>
        <dl className="facts facts--wide">
          <dt>Contract</dt>
          <dd>
            <a className="link mono" href={`${EXPLORER}/address/${CONTRACT_ID}`} target="_blank" rel="noreferrer">
              {CONTRACT_ID}
            </a>
          </dd>
          <dt>Contract code hash</dt>
          <dd className="mono break">{account.data?.code_hash ?? "…"}</dd>
          <dt>Series {SERIES_ID} table hash</dt>
          <dd className="mono break">{hash.data?.stored ?? "…"}</dd>
          <dt>Cards in the table</dt>
          <dd>{hash.data?.card_count ?? "…"}</dd>
        </dl>
        <p className="small muted">
          The code hash identifies the exact program deployed on NEAR testnet; compare it with the one shown on{" "}
          <a className="link" href={`${EXPLORER}/address/${CONTRACT_ID}`} target="_blank" rel="noreferrer">
            nearblocks
          </a>{" "}
          and with a build of the published source. The public verifier (Python, standard library only) recomputes the
          table hash and replays any pack from public data:
        </p>
        <pre className="code">{`python3 -m memaster_verifier table --rpc testnet --contract ${CONTRACT_ID} --series ${SERIES_ID}
python3 -m memaster_verifier pack --rpc testnet --contract ${CONTRACT_ID} \\
    --tx-hash <your buy_pack transaction> --sender <your account>`}</pre>
      </section>
    </div>
  );
}
