// Accueil et boutique : deux lignes de packs, « Classic » et « Full Moon », chacune en 5, 10 et 20 cartes.
//
// Sur le contrat, un pack fait toujours 5 cartes : 10 et 20 cartes sont 2 et 4 packs achetés d'un coup (une seule
// validation si le wallet sait signer un lot) et ouverts ensemble. « Full Moon » est la série au prix le plus haut :
// mêmes cartes et mêmes cotes, la carte brûlable y bloque plus de jetons (valeur proportionnelle au prix).
// Consigne tenue : prix en NEAR et en dollars, dépôt de stockage indiqué, lien vers les cotes sur chaque ligne,
// gold rush réel, aucun minuteur inventé ni compteur de pitié. « Open » ouvre directement : le wallet affiche le
// montant à signer.

import { useEffect, useMemo, useState } from "react";
import { ConnectButton } from "../components/Header";
import { PackArt } from "../components/PackArt";
import { BLOCK_TIME_S } from "../config";
import { loadCatalog } from "../lib/catalog";
import { formatDuration, formatNearExact, formatUsd, yoctoToNumber } from "../lib/format";
import { cardsOf, offerFor, PACK_ROWS, PACK_TYPES, regularSeries, type PackRowId, type PackType } from "../lib/packTypes";
import { seriesShareOdds } from "../lib/odds";
import { nearUsd } from "../lib/prices";
import { rushTarget } from "../lib/series";
import { useAsync } from "../lib/useAsync";
import { getRushState, getSeries, getSeriesCount, isV3Contract } from "../near/contract";
import type { RushState, SeriesView } from "../near/types";
import { useWallet } from "../near/wallet";

/** Tailles proposées, en nombre de packs de 5 cartes. */
export const BUNDLES = [1, 2, 4];

/** Les lignes de la boutique : séries triées par prix, la moins chère « Classic », les suivantes « Full Moon ». */
export function shopRows(list: SeriesView[]): { series: SeriesView; title: string; variant: "standard" | "moon"; ratio: number }[] {
  const sorted = [...list].sort((a, b) => (BigInt(a.price) < BigInt(b.price) ? -1 : 1));
  const base = sorted.length ? BigInt(sorted[0].price) : 1n;
  return sorted.map((s, i) => ({
    series: s,
    title: i === 0 ? "Classic" : sorted.length > 2 ? `Full Moon ${i}` : "Full Moon",
    variant: i === 0 ? "standard" : "moon",
    ratio: Number((BigInt(s.price) * 100n) / base) / 100,
  }));
}

const fmtRatio = (r: number) => (Number.isInteger(r) ? String(r) : r.toFixed(1).replace(/\.0$/, ""));

export function Shop({ onBuy }: { onBuy: (s: SeriesView, count: number, packKind?: number) => void }) {
  const { accountId } = useWallet();
  const series = useAsync(async () => {
    const n = await getSeriesCount();
    const all = await Promise.all(Array.from({ length: n }, (_, i) => getSeries(i)));
    return all.filter((s) => s.status === "open");
  }, []);
  const usd = useAsync(() => nearUsd(), []);
  const v3 = useAsync(() => isV3Contract(), []);
  const shared = useAsync(() => (series.data ? seriesShareOdds(series.data) : Promise.resolve(false)), [series.data]);
  const rows = series.data ? shopRows(regularSeries(series.data)) : [];
  const catalog = useAsync(() => loadCatalog(), []);

  return (
    <div className="page shop">
      <header className="page-intro shop__intro">
        <h1>Shop</h1>
        <p>Every pack, from the classic booster to themed packs. Odds are one click away on each row.</p>
      </header>

      {series.loading && !series.data && <div className="shop-row shop-row--loading" aria-busy />}
      {series.error != null && <p className="error">Could not load the packs. Please refresh.</p>}
      {series.data && !series.data.length && <p className="muted">No pack is on sale right now.</p>}

      {rows.map((row) => (
        <section key={row.series.series_id} className={`shop-row shop-row--${row.variant}`}>
          <header className="shop-row__head">
            <div>
              <h2>
                {row.title} <span>packs</span>
              </h2>
              <p>
                {row.variant === "standard"
                  ? `${row.series.cards_per_pack} memecoin cards per pack, at least one burnable.`
                  : shared.data
                    ? `Exactly the same cards and odds as Classic. Burnable cards hold ${fmtRatio(row.ratio)}× the tokens.`
                    : `Burnable cards hold more tokens.`}
              </p>
            </div>
            <a className="shop-row__odds" href={`#/rates?series=${row.series.series_id}`}>
              Odds
            </a>
          </header>

          <div className="shop-row__offers">
            {BUNDLES.map((n) => (
              <Offer
                key={n}
                series={row.series}
                count={n}
                variant={row.variant}
                badge={row.variant === "moon" && shared.data ? `${fmtRatio(row.ratio)}× tokens` : null}
                usd={usd.data ?? null}
                connected={!!accountId}
                onBuy={() => onBuy(row.series, n)}
              />
            ))}
          </div>

          <footer className="shop-row__foot">
            <span>
              + {formatNearExact(BigInt(row.series.required_deposit) - BigInt(row.series.price))} NEAR storage deposit per
              pack{v3.data ? ", unused part refunded" : ""}
            </span>
            <RushPanel accountId={accountId} series={row.series} multi={false} />
          </footer>
        </section>
      ))}

      {series.data &&
        PACK_ROWS.map((row) => (
          <ThemedRow
            key={row.id}
            row={row}
            open={series.data!}
            catalog={catalog.data ?? null}
            usd={usd.data ?? null}
            connected={!!accountId}
            onBuy={onBuy}
          />
        ))}
    </div>
  );
}

export function Step({ n, title, text }: { n: number; title: string; text: string }) {
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

/**
 * Ligne de packs thématiques. Un pack dont la série n'existe pas encore sur le contrat est montré « Coming soon »,
 * sans prix ni bouton d'achat ; il devient achetable dès que sa série est ouverte (`seriesFor`).
 */
function ThemedRow({
  row,
  open,
  catalog,
  usd,
  connected,
  onBuy,
}: {
  row: { id: PackRowId; title: string; lead: string };
  open: SeriesView[];
  catalog: Record<string, import("../lib/catalog").CatalogEntry> | null;
  usd: number | null;
  connected: boolean;
  onBuy: (s: SeriesView, count: number, packKind?: number) => void;
}) {
  const types = useMemo(() => PACK_TYPES.filter((t) => t.row === row.id), [row.id]);
  const live = types.map((t) => offerFor(t, open));
  // Calculé une fois par catalogue : la mosaïque du pack ne doit pas se redessiner à chaque rendu.
  const pools = useMemo(() => (catalog ? types.map((t) => cardsOf(t, catalog)) : null), [catalog, types]);
  return (
    <section className={`shop-row shop-row--themed shop-row--${row.id}`}>
      <header className="shop-row__head">
        <div>
          <h2>{row.title}</h2>
          <p>{row.lead}</p>
        </div>
        {live.every((s) => !s) && <span className="soon-pill">Coming soon</span>}
      </header>
      <div className="shop-row__offers">
        {types.map((t, i) => (
          <ThemedOffer
            key={t.id}
            type={t}
            offer={live[i]}
            pool={pools ? pools[i] : null}
            usd={usd}
            connected={connected}
            onBuy={(o) => onBuy(o.series, 1, o.kind?.kind)}
          />
        ))}
      </div>
    </section>
  );
}

function ThemedOffer({
  type,
  offer,
  pool,
  usd,
  connected,
  onBuy,
}: {
  type: PackType;
  offer: ReturnType<typeof offerFor>;
  pool: string[] | null;
  usd: number | null;
  connected: boolean;
  onBuy: (o: NonNullable<ReturnType<typeof offerFor>>) => void;
}) {
  const unit = type.row === "families" ? `${type.title.split(" ")[0].toLowerCase()} cards` : "cards";
  // Contrat à types de packs : nombre exact de cartes du type, lu sur la chaîne ; sinon, le filtre du catalogue.
  const count = offer?.kind?.card_count ?? pool?.length ?? null;
  return (
    <article className={`offer-card offer-card--themed${offer ? "" : " offer-card--soon"}`}>
      <div className="pack-stack pack-stack--1">
        <PackArt
          seed={type.id.length * 97 + type.cards * 13}
          pool={pool ?? undefined}
          label={`${type.cards} CARD${type.cards > 1 ? "S" : ""}`}
        />
        <span className="offer-card__emoji" aria-hidden>
          {type.emoji}
        </span>
      </div>
      <div className="offer-card__body">
        <strong className="offer-card__cards">{type.title}</strong>
        <small className="offer-card__note">
          {type.cards} card{type.cards > 1 ? "s" : ""} per pack{count != null ? ` · from ${count} ${unit}` : ""}
        </small>
        {type.note && <small className="offer-card__perk">{type.note}</small>}
        {offer && (
          <span className="offer-card__price">
            {formatNearExact(offer.price)} NEAR
            {usd != null && <small> ≈ {formatUsd(yoctoToNumber(offer.price) * usd)}</small>}
          </span>
        )}
      </div>
      {!offer ? (
        <button className="btn" disabled>
          Coming soon
        </button>
      ) : connected ? (
        <button className="btn btn--primary" onClick={() => onBuy(offer)}>
          Open
        </button>
      ) : (
        <ConnectButton label="Connect to open" />
      )}
    </article>
  );
}

export function Offer({
  series,
  count,
  variant,
  badge,
  usd,
  connected,
  onBuy,
}: {
  series: SeriesView;
  count: number;
  variant: "standard" | "moon";
  badge: string | null;
  usd: number | null;
  connected: boolean;
  onBuy: () => void;
}) {
  const cards = count * series.cards_per_pack;
  const price = BigInt(series.price) * BigInt(count);
  return (
    <article className={`offer-card offer-card--${count}`}>
      {badge && <span className="offer-card__badge">{badge}</span>}
      <div className={`pack-stack pack-stack--${Math.min(count, 4)}`}>
        <PackArt seed={series.series_id * 31 + count * 7 + 11} variant={variant} label={`${cards} CARDS`} />
      </div>
      <div className="offer-card__body">
        <strong className="offer-card__cards">{cards} cards</strong>
        <span className="offer-card__price">
          {formatNearExact(price)} NEAR
          {usd != null && <small> ≈ {formatUsd(yoctoToNumber(price) * usd)}</small>}
        </span>
        {count > 1 && <small className="offer-card__note">{count} packs, opened together</small>}
      </div>
      {connected ? (
        <button className="btn btn--primary" onClick={onBuy}>
          Open
        </button>
      ) : (
        <ConnectButton label="Connect to open" />
      )}
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

  return <RushView rush={rush} name={multi ? series.name : null} now={now} fetchedAt={fetchedAt} />;
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
    <div
      className="rush-mini"
      title={`When the community opens ${target} packs within ${formatDuration(p.window_blocks * BLOCK_TIME_S)}, odds improve for everyone for about ${formatDuration(p.duration_blocks * BLOCK_TIME_S)}.`}
    >
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
