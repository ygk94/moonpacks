// Accueil et boutique : un titre court, les packs en vente, « Open pack » ouvre directement (le wallet affiche le
// montant à signer). La consigne est tenue : prix en NEAR et en dollars, dépôt de stockage indiqué, lien vers les
// taux sur chaque pack, gold rush réel, aucun minuteur inventé ni compteur de pitié.

import { useEffect, useState } from "react";
import { ConnectButton } from "../components/Header";
import { PackArt } from "../components/PackArt";
import { BLOCK_TIME_S } from "../config";
import { seriesName } from "../lib/brand";
import { formatDuration, formatNearExact, formatUsd, yoctoToNumber } from "../lib/format";
import { nearUsd } from "../lib/prices";
import { rushTarget } from "../lib/series";
import { useAsync } from "../lib/useAsync";
import { getRushState, getSeries, getSeriesCount, isV3Contract } from "../near/contract";
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
  const v3 = useAsync(() => isV3Contract(), []);

  return (
    <div className="page home">
      <section className="home__hero">
        <h1>
          Rip a pack.
          <br />
          <span className="home__accent">Catch the moon.</span>
        </h1>
        <p className="home__lead">
          Booster packs of memecoin cards from every chain. Pull a burnable card and burn it for the coin's tokens.
        </p>
      </section>

      {series.loading && !series.data && <div className="home__packs home__packs--loading" aria-busy />}
      {series.error != null && <p className="error">Could not load the packs. Please refresh.</p>}
      <div className="home__packs">
        {series.data?.map((s, i) => (
          <PackOffer
            key={s.series_id}
            series={s}
            featured={i === series.data!.length - 1}
            usd={usd.data ?? null}
            connected={!!accountId}
            accountId={accountId}
            storageReturned={v3.data === true}
            onBuy={() => onBuy(s)}
          />
        ))}
        {series.data && !series.data.length && <p className="muted">No pack is on sale right now.</p>}
      </div>

      <section className="steps-row" aria-label="How it works">
        <Step n={1} title="Open" text="5 cards drawn on-chain, revealed one by one." />
        <Step n={2} title="Collect" text="Keep them, trade them on the market." />
        <Step n={3} title="Burn" text="Burnable cards hold tokens of their memecoin." />
      </section>
    </div>
  );
}

function Step({ n, title, text }: { n: number; title: string; text: string }) {
  return (
    <div className="step">
      <span className="step__n">{n}</span>
      <div>
        <strong>{title}</strong>
        <p>{text}</p>
      </div>
    </div>
  );
}

function PackOffer({
  series,
  featured,
  usd,
  connected,
  accountId,
  storageReturned,
  onBuy,
}: {
  series: SeriesView;
  featured: boolean;
  usd: number | null;
  connected: boolean;
  accountId: string | null;
  storageReturned: boolean;
  onBuy: () => void;
}) {
  const storage = BigInt(series.required_deposit) - BigInt(series.price);
  const price = yoctoToNumber(series.price);
  // « Memaster Entry » → « Entry » : la marque est déjà dans l'en-tête.
  const short = seriesName(series.name).replace(/^Moonpacks\s+/i, "") || seriesName(series.name);
  return (
    <article className={`pack-offer${featured ? " pack-offer--featured" : ""}`}>
      <div className="pack-offer__art">
        <PackArt seed={series.series_id * 31 + 11} label={`${short.toUpperCase()} · 5 CARDS`} />
      </div>
      <div className="pack-offer__info">
        <div className="pack-offer__head">
          <h2>{short} pack</h2>
          <a className="pack-offer__odds" href={`#/rates?series=${series.series_id}`}>
            Odds
          </a>
        </div>
        <div className="pack-offer__price">
          <strong>{formatNearExact(series.price)} NEAR</strong>
          {usd != null && <span>≈ {formatUsd(price * usd)}</span>}
        </div>
        {connected ? (
          <button className="btn btn--primary btn--big" onClick={onBuy}>
            Open pack
          </button>
        ) : (
          <ConnectButton big label="Connect to open" />
        )}
        <p className="pack-offer__fine">
          + {formatNearExact(storage)} NEAR storage deposit{storageReturned ? ", unused part refunded" : ""}
        </p>
        <RushPanel accountId={accountId} series={series} multi={false} />
      </div>
    </article>
  );
}

/** Gold rush d'une série : avancement collectif réel ; pendant un rush, sa fin et les packs rush restants du compte. */
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

/** Rendu compact d'un état de rush (séparé pour les tests). */
export function RushView({ rush, name, now, fetchedAt }: { rush: RushState | null; name: string | null; now: number; fetchedAt: number }) {
  const suffix = name ? ` · ${name}` : "";
  if (!rush?.enabled || !rush.params || rush.height == null) return null;
  const p = rush.params;
  const height = rush.height + (now - fetchedAt) / 1000 / BLOCK_TIME_S;

  if (rush.active && rush.rush_until != null) {
    const left = (rush.rush_until - height) * BLOCK_TIME_S;
    return (
      <div className="rush-mini rush-mini--active">
        <div className="rush-mini__top">
          <span>⚡ Gold rush in progress{suffix}</span>
          <strong>{formatDuration(left)}</strong>
        </div>
        <small>
          Better odds for everyone until it ends
          {rush.account ? ` · ${rush.account.remaining} rush packs left for you (max ${p.max_per_account})` : ""}.
        </small>
      </div>
    );
  }

  const window = rush.window_count ?? 0;
  const target = rushTarget(rush);
  const pct = Math.min(100, (window / target) * 100);
  const paused = rush.pause_until != null && height <= rush.pause_until;
  return (
    <div className="rush-mini" title={`When the community opens ${target} packs within ${formatDuration(p.window_blocks * BLOCK_TIME_S)}, odds improve for everyone for about ${formatDuration(p.duration_blocks * BLOCK_TIME_S)}.`}>
      <div className="rush-mini__top">
        <span>Gold rush{suffix}</span>
        <small>
          {window} / {target} packs opened in the last {formatDuration(p.window_blocks * BLOCK_TIME_S)}
        </small>
      </div>
      <div className="progress" aria-label={`${window} of ${target} packs`}>
        <div className="progress__bar" style={{ width: `${pct}%` }} />
      </div>
      {paused && rush.pause_until != null && (
        <small>Next rush possible in {formatDuration((rush.pause_until - height) * BLOCK_TIME_S)}</small>
      )}
    </div>
  );
}
