// Boutique : packs en vente (prix en NEAR et en dollars), dépôt de stockage, lien vers les taux, gold rush.
// Rien d'autre ne pousse à l'achat : pas de minuteur inventé, pas de compteur de pitié, pas d'achat en un clic.

import { useEffect, useState } from "react";
import { ConnectButton } from "../components/Header";
import { PackArt } from "../components/PackArt";
import { BLOCK_TIME_S } from "../config";
import { formatDuration, formatNear, formatUsd, yoctoToNumber } from "../lib/format";
import { nearUsd } from "../lib/prices";
import { useAsync } from "../lib/useAsync";
import { getPackCount, getRushState, getSeries, getSeriesCount } from "../near/contract";
import type { RushState, SeriesView } from "../near/types";
import { useWallet } from "../near/wallet";

// Stockage effectivement consommé (mesuré sur testnet) : environ 1 034 o au premier pack d'un compte, 602 o
// ensuite (docs/testnet.md). Le contrat demande le pire cas et ne garde que ce qui sert.
const STORAGE_FIRST_PACK = 1034n;
const STORAGE_NEXT_PACK = 602n;
const BYTE_COST = 10n ** 19n; // 1 octet = 10¹⁹ yoctoNEAR

export function Shop({ onBuy }: { onBuy: (s: SeriesView) => void }) {
  const { accountId } = useWallet();
  const series = useAsync(async () => {
    const n = await getSeriesCount();
    const all = await Promise.all(Array.from({ length: n }, (_, i) => getSeries(i)));
    return all.filter((s) => s.status === "open");
  }, []);
  const usd = useAsync(() => nearUsd(), []);
  const packs = useAsync(() => (accountId ? getPackCount(accountId) : Promise.resolve(null)), [accountId]);

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

      <RushPanel accountId={accountId} />

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
  onBuy,
}: {
  series: SeriesView;
  usd: number | null;
  firstPack: boolean | null;
  connected: boolean;
  onBuy: () => void;
}) {
  const [confirm, setConfirm] = useState(false);
  const storageMax = BigInt(series.required_deposit) - BigInt(series.price);
  const used = (bytes: bigint) => formatNear(bytes * BYTE_COST, 3);
  const usedText =
    firstPack == null
      ? `about ${used(STORAGE_NEXT_PACK)} NEAR is actually used, ${used(STORAGE_FIRST_PACK)} NEAR for the first pack of an account`
      : `about ${used(firstPack ? STORAGE_FIRST_PACK : STORAGE_NEXT_PACK)} NEAR is actually used${firstPack ? " for the first pack of an account" : ""}`;
  const price = yoctoToNumber(series.price);
  return (
    <article className="offer">
      <PackArt seed={series.series_id * 31 + 11} />
      <div className="offer__body">
        <h2>{series.name}</h2>
        <p className="muted">{series.cards_per_pack} cards · at least one burnable</p>
        <div className="offer__price">
          <span className="offer__near">{formatNear(series.price)} NEAR</span>
          {usd != null && <span className="offer__usd">≈ {formatUsd(price * usd)}</span>}
        </div>
        <p className="small muted">
          + storage deposit: {formatNear(storageMax, 3)} NEAR is attached to pay for the cards' on-chain storage (
          {usedText}). It is returned when the card is burned.
        </p>
        {!connected ? (
          <ConnectButton />
        ) : confirm ? (
          <div className="confirm">
            <p>
              You will pay <strong>{formatNear(series.price)} NEAR</strong> plus the storage deposit. The cards are drawn
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

/** Gold rush : avancement collectif réel, et pendant un rush, sa fin et les packs rush restants du compte. */
function RushPanel({ accountId }: { accountId: string | null }) {
  const [rush, setRush] = useState<RushState | null>(null);
  const [now, setNow] = useState(Date.now());
  const [fetchedAt, setFetchedAt] = useState(Date.now());
  useEffect(() => {
    let stop = false;
    const load = () =>
      getRushState(accountId)
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
  }, [accountId]);

  if (!rush?.enabled || !rush.params || rush.height == null) return null;
  const p = rush.params;
  const elapsedBlocks = (now - fetchedAt) / 1000 / BLOCK_TIME_S;
  const height = rush.height + elapsedBlocks;

  if (rush.active && rush.rush_until != null) {
    const left = (rush.rush_until - height) * BLOCK_TIME_S;
    return (
      <section className="rush rush--active">
        <div className="rush__title">⚡ Gold rush in progress</div>
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

  // Seuil : au moins `min_packs` packs dans la fenêtre, et un rythme `ratio` fois supérieur à la moyenne.
  const bsz = Math.max(1, p.bucket_blocks);
  const ml = Math.max(1, Math.floor(p.baseline_blocks / bsz));
  const mw = Math.min(Math.max(1, Math.floor(p.window_blocks / bsz)), ml);
  const window = rush.window_count ?? 0;
  const baseline = rush.baseline_count ?? 0;
  const byRatio = Math.ceil((p.ratio_bps * baseline * mw) / (ml * 10_000));
  const target = Math.max(p.min_packs, byRatio, 1);
  const pct = Math.min(100, (window / target) * 100);
  const paused = rush.pause_until != null && height <= rush.pause_until;
  const windowLabel = formatDuration(p.window_blocks * BLOCK_TIME_S);

  return (
    <section className="rush">
      <div className="rush__title">Gold rush</div>
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
