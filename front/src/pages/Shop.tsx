// Boutique : packs en vente (prix en NEAR et en dollars), dépôt de stockage, lien vers les taux, gold rush.
// Rien d'autre ne pousse à l'achat : pas de minuteur inventé, pas de compteur de pitié, pas d'achat en un clic.

import { seriesName } from "../lib/brand";
import { useEffect, useState } from "react";
import { ConnectButton } from "../components/Header";
import { PackArt } from "../components/PackArt";
import { BLOCK_TIME_S } from "../config";
import { formatDuration, formatNearExact, formatUsd, yoctoToNumber } from "../lib/format";
import { nearUsd } from "../lib/prices";
import { useAsync } from "../lib/useAsync";
import { storageDepositNote } from "../lib/pack";
import { rushTarget } from "../lib/series";
import { getPackCount, getRushState, getSeries, getSeriesCount, isV3Contract } from "../near/contract";
import type { RushState, SeriesView } from "../near/types";
import { useWallet } from "../near/wallet";

export function Shop({ onBuy }: { onBuy: (s: SeriesView) => void }) {
  const { accountId } = useWallet();
  const series = useAsync(async () => {
    const n = await getSeriesCount();
    const all = await Promise.all(Array.from({ length: n }, (_, i) => getSeries(i)));
    return all.filter((s) => s.status === "open");
  }, []);
  const usd = useAsync(() => nearUsd(), []);
  const packs = useAsync(() => (accountId ? getPackCount(accountId) : Promise.resolve(null)), [accountId]);
  const v3 = useAsync(() => isV3Contract(), []);

  return (
    <div className="page shop">
      <section className="hero">
        <div className="hero__text">
          <h1>Memecoin booster packs</h1>
          <p>
            Each pack holds 5 NFT cards of memecoins from every chain. Some cards are <strong>burnable</strong>: burn
            one and you receive the memecoin's tokens, locked when the pack was opened.
          </p>
          <a className="link" href="#/rates">
            Drop rates →
          </a>
        </div>
      </section>

      {/* Un gold rush par série (contrat v3 : entrée et standard), chacun avec son propre avancement. */}
      {series.data?.map((s) => (
        <RushPanel key={s.series_id} accountId={accountId} series={s} multi={series.data!.length > 1} />
      ))}

      {series.loading && !series.data && <p className="muted">Loading packs…</p>}
      {series.error != null && <p className="error">Could not load the packs. Please refresh.</p>}
      <div className="shop__grid">
        {series.data?.map((s) => (
          <PackOffer
            key={s.series_id}
            series={s}
            usd={usd.data ?? null}
            firstPack={packs.data == null ? null : packs.data === 0}
            connected={!!accountId}
            storageReturned={v3.data === true}
            onBuy={() => onBuy(s)}
          />
        ))}
        {series.data && !series.data.length && <p className="muted">No pack is on sale right now.</p>}
      </div>
    </div>
  );
}

function PackOffer({
  series,
  usd,
  firstPack,
  connected,
  storageReturned,
  onBuy,
}: {
  series: SeriesView;
  usd: number | null;
  firstPack: boolean | null;
  connected: boolean;
  storageReturned: boolean;
  onBuy: () => void;
}) {
  const [confirm, setConfirm] = useState(false);
  const storageMax = BigInt(series.required_deposit) - BigInt(series.price);
  const price = yoctoToNumber(series.price);
  return (
    <article className="offer">
      <PackArt seed={series.series_id * 31 + 11} />
      <div className="offer__body">
        <h2>{seriesName(series.name)}</h2>
        <p className="muted">{series.cards_per_pack} cards · at least one burnable</p>
        <div className="offer__price">
          <span className="offer__near">{formatNearExact(series.price)} NEAR</span>
          {usd != null && <span className="offer__usd">≈ {formatUsd(price * usd)}</span>}
        </div>
        <p className="small muted">
          {storageDepositNote(storageMax, firstPack, storageReturned)}
        </p>
        {!connected ? (
          <ConnectButton />
        ) : confirm ? (
          <div className="confirm">
            <p>
              You will pay <strong>{formatNearExact(series.price)} NEAR</strong> plus the storage deposit of{" "}
              {formatNearExact(storageMax)} NEAR
              {storageReturned ? " (its unused part comes back when the pack is opened)" : ""}. The cards are drawn
              on-chain; the purchase cannot be cancelled once signed.
            </p>
            <div className="row">
              <button
                className="btn btn--primary"
                onClick={() => {
                  setConfirm(false);
                  onBuy();
                }}
              >
                Buy and open
              </button>
              <button className="btn btn--ghost" onClick={() => setConfirm(false)}>
                Cancel
              </button>
            </div>
            <a className="link small" href="#/rates">
              Check the drop rates first
            </a>
          </div>
        ) : (
          <button className="btn btn--primary btn--big" onClick={() => setConfirm(true)}>
            Buy pack
          </button>
        )}
      </div>
    </article>
  );
}

/**
 * Gold rush d'une série : avancement collectif réel, et pendant un rush, sa fin et les packs rush restants du compte.
 * Avec plusieurs séries, le titre nomme la série (chaque série a son propre rush).
 */
export function RushPanel({ accountId, series, multi }: { accountId: string | null; series: SeriesView; multi: boolean }) {
  const [rush, setRush] = useState<RushState | null>(null);
  const [now, setNow] = useState(Date.now());
  const [fetchedAt, setFetchedAt] = useState(Date.now());
  useEffect(() => {
    let stop = false;
    const load = () =>
      getRushState(accountId, series.series_id)
        .then((r) => {
          if (stop) return;
          setRush(r);
          setFetchedAt(Date.now());
        })
        .catch(() => undefined);
    load();
    const poll = setInterval(load, 15_000);
    const clock = setInterval(() => setNow(Date.now()), 1000);
    return () => {
      stop = true;
      clearInterval(poll);
      clearInterval(clock);
    };
  }, [accountId, series.series_id]);

  return <RushView rush={rush} name={multi ? seriesName(series.name) : null} now={now} fetchedAt={fetchedAt} />;
}

/** Rendu d'un état de rush (séparé pour les tests). */
export function RushView({ rush, name, now, fetchedAt }: { rush: RushState | null; name: string | null; now: number; fetchedAt: number }) {
  const suffix = name ? ` · ${name}` : "";
  if (!rush?.enabled || !rush.params || rush.height == null) return null;
  const p = rush.params;
  const elapsedBlocks = (now - fetchedAt) / 1000 / BLOCK_TIME_S;
  const height = rush.height + elapsedBlocks;

  if (rush.active && rush.rush_until != null) {
    const left = (rush.rush_until - height) * BLOCK_TIME_S;
    return (
      <section className="rush rush--active">
        <div className="rush__title">⚡ Gold rush in progress{suffix}</div>
        <p>Drop rates are improved for everyone until the rush ends.</p>
        <div className="rush__stats">
          <div>
            <span className="rush__big">{formatDuration(left)}</span>
            <small>left (estimated from block time)</small>
          </div>
          {rush.account && (
            <div>
              <span className="rush__big">{rush.account.remaining}</span>
              <small>rush packs left for you (max {p.max_per_account})</small>
            </div>
          )}
        </div>
      </section>
    );
  }

  const window = rush.window_count ?? 0;
  const target = rushTarget(rush);
  const pct = Math.min(100, (window / target) * 100);
  const paused = rush.pause_until != null && height <= rush.pause_until;
  const windowLabel = formatDuration(p.window_blocks * BLOCK_TIME_S);

  return (
    <section className="rush">
      <div className="rush__title">Gold rush{suffix}</div>
      <p>
        When the community opens enough packs in a short time, drop rates improve for everyone for about{" "}
        {formatDuration(p.duration_blocks * BLOCK_TIME_S)}.
      </p>
      <div className="progress" aria-label={`${window} of ${target} packs`}>
        <div className="progress__bar" style={{ width: `${pct}%` }} />
      </div>
      <p className="small muted">
        {window} / {target} packs opened in the last {windowLabel}
        {paused && rush.pause_until != null
          ? ` · next rush possible in ${formatDuration((rush.pause_until - height) * BLOCK_TIME_S)}`
          : ""}
      </p>
    </section>
  );
}
