// Transparence : taux de drop publiés on-chain (`get_rates`, paginé), hash de la table, hash du code du contrat,
// et comment vérifier soi-même un tirage avec verifier/.

import { seriesName } from "../lib/brand";
import { useMemo, useState } from "react";
import { Card } from "../components/Card";
import { CONTRACT_ID, EXPLORER, SERIES_ID } from "../config";
import { loadCatalog } from "../lib/catalog";
import { formatNearExact, RARITY_LABEL } from "../lib/format";
import { navigate, useRoute } from "../lib/router";
import { seriesShareOdds } from "../lib/odds";
import { pickSeries, publicSeries } from "../lib/series";
import { useAsync } from "../lib/useAsync";
import { getAllRates, getSeries, getSeriesCount, getTableHash } from "../near/contract";
import { viewAccount } from "../near/rpc";
import { RARITIES, type RatesCard, type Rarity, type SeriesView } from "../near/types";

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

/** Choix de la série (contrat v3 : « entrée » et « standard ») ; l'URL garde le choix : #/rates?series=1. */
export function SeriesPicker({ list, current, onPick }: { list: SeriesView[]; current: number; onPick: (id: number) => void }) {
  if (list.length < 2) return null;
  return (
    <div className="tabs series-picker" role="tablist" aria-label="Series">
      {list.map((s) => (
        <button
          key={s.series_id}
          role="tab"
          aria-selected={s.series_id === current}
          className={s.series_id === current ? "active" : ""}
          onClick={() => onPick(s.series_id)}
        >
          {seriesName(s.name)} <small className="muted">· {formatNearExact(s.price)} NEAR</small>
        </button>
      ))}
    </div>
  );
}

export function Transparency() {
  const { params } = useRoute();
  const list = useAsync(async () => {
    const n = await getSeriesCount();
    return publicSeries(await Promise.all(Array.from({ length: n }, (_, i) => getSeries(i))));
  }, []);
  // Tant que la liste n'est pas lue, on part de la série demandée (ou VITE_SERIES_ID) pour ne pas attendre.
  const param = params.get("series");
  const seriesId = list.data
    ? (pickSeries(param, list.data, SERIES_ID) ?? SERIES_ID)
    : param != null && /^\d+$/.test(param)
      ? Number(param)
      : SERIES_ID;
  const current = list.data?.find((s) => s.series_id === seriesId);
  // Packs aux mêmes cotes (app3 : Entry et Standard) : une seule table, sans sélecteur.
  const shared = useAsync(() => (list.data ? seriesShareOdds(list.data) : Promise.resolve(true)), [list.data]);
  const single = shared.data !== false;
  const rates = useAsync(() => getAllRates(seriesId), [seriesId]);
  const hash = useAsync(() => getTableHash(seriesId), [seriesId]);
  const account = useAsync(() => viewAccount(CONTRACT_ID), []);
  const catalog = useAsync(() => loadCatalog(), []);
  const [query, setQuery] = useState("");
  const [rarity, setRarity] = useState<Rarity | "all">("all");
  const [onlyBurnable, setOnlyBurnable] = useState(false);
  const [page, setPage] = useState(0);
  const pick = (id: number) => {
    setPage(0);
    navigate(`/rates?series=${id}`);
  };

  const rows = useMemo(() => {
    if (!rates.data || rates.loading) return [];
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
  }, [rates.data, rates.loading, catalog.data, query, rarity, onlyBurnable]);

  const pages = Math.max(1, Math.ceil(rows.length / PAGE));
  const shown = rows.slice(page * PAGE, page * PAGE + PAGE);
  const gold = rates.data?.rarities.find((r) => r.gold_slot_ppb)?.gold_slot_ppb?.length ?? 0;

  const totalCards = rates.data ? rates.data.rarities.reduce((n, r) => n + r.cards.length, 0) : null;

  return (
    <div className="page transparency">
      <header className="page-intro">
        <h1>Odds</h1>
        <p>
          Read live from the contract, the same table that draws your cards.
          {single && (list.data?.length ?? 0) > 1 ? " Every pack has the same odds." : ""}
        </p>
      </header>
      {list.data && !single && <SeriesPicker list={list.data} current={seriesId} onPick={pick} />}

      <section className="odds">
        {rates.loading && <p className="muted">Reading the odds from the contract…</p>}
        {rates.error != null && <p className="error">Could not read the odds.</p>}
        {rates.data &&
          !rates.loading &&
          RARITIES.map((r) => {
              const x = rates.data!.rarities.find((y) => y.rarity === r)!;
              const burnable = x.cards.filter((c) => c.burnable).length;
              // Barre en échelle logarithmique : de 1 sur 10⁸ (vide) à 1 sur 1 (pleine).
              const width = x.rarity_ppb ? Math.max(4, Math.min(100, ((Math.log10(x.rarity_ppb) + 1) / 10) * 100)) : 0;
              return (
                <div key={r} className={`odds__row rarity-${r}`}>
                  <span className={`odds__name rarity-text-${r}`}>{RARITY_LABEL[r]}</span>
                  <div className="odds__bar">
                    <div style={{ width: `${width}%` }} />
                  </div>
                  <span className="odds__value">
                    <strong>{oneIn(x.rarity_ppb)}</strong>
                    <small>{pctFromPpb(x.rarity_ppb)}</small>
                  </span>
                  <span className="odds__meta">
                    {r === "mythic" ? "sealed “?”" : `${x.cards.length} cards${burnable ? ` · ${burnable} burnable` : ""}`}
                    {x.rush_rarity_ppb != null && x.rush_rarity_ppb !== x.rarity_ppb ? ` · rush ${oneIn(x.rush_rarity_ppb)}` : ""}
                  </span>
                </div>
              );
            })}
        <p className="odds__note">
          Odds per card. A pack has 5 cards and the last one is always burnable.
          {gold > 0 && " Gold packs are rare special packs with no common card."}
        </p>
      </section>

      <details className="fold">
        <summary>Browse every card{totalCards != null ? ` (${totalCards})` : ""}</summary>
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
              <span title={`${c.ppb} parts per billion per card`}>{oneIn(c.ppb)}</span>
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
      </details>

      <details className="fold">
        <summary>Verify it yourself</summary>
        <dl className="facts facts--wide">
          <dt>Contract</dt>
          <dd>
            <a className="link mono" href={`${EXPLORER}/address/${CONTRACT_ID}`} target="_blank" rel="noreferrer">
              {CONTRACT_ID}
            </a>
          </dd>
          <dt>Contract code hash</dt>
          <dd className="mono break">{account.data?.code_hash ?? "…"}</dd>
          <dt>
            Series {seriesId}
            {current ? ` (${seriesName(current.name)})` : ""} table hash
          </dt>
          <dd className="mono break">{hash.loading ? "…" : (hash.data?.stored ?? "…")}</dd>
          <dt>Cards in the table</dt>
          <dd>{hash.loading ? "…" : (hash.data?.card_count ?? "…")}</dd>
        </dl>
        <p className="small muted">
          The table hash was frozen when the series opened. The public verifier (Python, standard library only)
          recomputes it and replays any pack from public data. Each pack can also be checked in your browser with
          “Verify this pack”.
        </p>
        <pre className="code">{`python3 -m memaster_verifier table --rpc testnet --contract ${CONTRACT_ID} --series ${seriesId}
python3 -m memaster_verifier pack --rpc testnet --contract ${CONTRACT_ID} \\
    --tx-hash <your buy_pack transaction> --sender <your account>`}</pre>
      </details>
    </div>
  );
}
