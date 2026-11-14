// Accueil : à quoi sert le site, en quelques secondes, et deux packs pour commencer. Tout le reste est dans la
// boutique (#/shop). Consigne tenue sur les deux packs montrés : prix en NEAR et en dollars, lien vers les cotes.

import { PackArt } from "../components/PackArt";
import { useAsync } from "../lib/useAsync";
import { loadCatalog } from "../lib/catalog";
import { nearUsd } from "../lib/prices";
import { regularSeries } from "../lib/packTypes";
import { getSeries, getSeriesCount } from "../near/contract";
import type { SeriesView } from "../near/types";
import { useWallet } from "../near/wallet";
import { Offer, shopRows, Step } from "./Shop";

export function Home({ onBuy }: { onBuy: (s: SeriesView, count: number) => void }) {
  const { accountId } = useWallet();
  const series = useAsync(async () => {
    const n = await getSeriesCount();
    const all = await Promise.all(Array.from({ length: n }, (_, i) => getSeries(i)));
    return all.filter((s) => s.status === "open");
  }, []);
  const usd = useAsync(() => nearUsd(), []);
  const catalog = useAsync(() => loadCatalog(), []);
  const rows = series.data ? shopRows(regularSeries(series.data)) : [];
  const cards = catalog.data ? Object.keys(catalog.data).length : null;
  const chains = catalog.data ? new Set(Object.values(catalog.data).map((e) => e.chain).filter(Boolean)).size : null;

  return (
    <div className="page landing">
      <section className="landing__hero">
        <div className="landing__copy">
          <span className="landing__kicker">Memecoin trading cards on NEAR</span>
          <h1>
            Rip a pack.
            <br />
            <span className="home__accent">Catch the moon.</span>
          </h1>
          <p className="landing__lead">
            Every card is a memecoin, from the 2013 classics to this week's pump. Open packs, collect the coins you love,
            and burn the rare <strong>burnable</strong> cards for the coin's tokens.
          </p>
          <div className="landing__cta">
            <a className="btn btn--primary btn--big" href="#/shop">
              Open a pack
            </a>
            <a className="btn btn--ghost btn--big" href="#/rates">
              See the odds
            </a>
          </div>
          {cards != null && (
            <p className="landing__facts">
              <span>
                <strong>{cards.toLocaleString("en-US")}</strong> cards
              </span>
              <span>
                <strong>{chains}</strong> chains
              </span>
              <span>
                <strong>3</strong> sealed mythics
              </span>
            </p>
          )}
        </div>
        <div className="landing__art" aria-hidden>
          <div className="landing__pack landing__pack--back">
            <PackArt seed={23} variant="moon" label="5 CARDS" />
          </div>
          <div className="landing__pack landing__pack--front">
            <PackArt seed={11} label="5 CARDS" />
          </div>
        </div>
      </section>

      <section className="landing__how" aria-label="How it works">
        <h2>How it works</h2>
        <div className="steps-row">
          <Step n={1} title="Open a pack" text="5 memecoin cards, drawn on-chain and revealed one by one." />
          <Step n={2} title="Collect and trade" text="Dead coins, legends and everything between. Sell or buy on the market." />
          <Step n={3} title="Burn for tokens" text="A burnable card holds tokens of its coin. Burn it to receive them." />
        </div>
        <p className="landing__fair">
          Fair by design: the odds are published on-chain and every pack can be verified from public data.
        </p>
      </section>

      {rows.length > 0 && (
        <section className="landing__packs">
          <div className="landing__packs-head">
            <h2>Start here</h2>
            <a className="link" href="#/shop">
              All packs →
            </a>
          </div>
          <div className="landing__offers">
            {rows.slice(0, 2).map((row) => (
              <div key={row.series.series_id} className="landing__offer">
                <span className="landing__offer-name">{row.title}</span>
                <Offer
                  series={row.series}
                  count={1}
                  variant={row.variant}
                  badge={row.variant === "moon" ? `${row.ratio}× tokens` : null}
                  usd={usd.data ?? null}
                  connected={!!accountId}
                  onBuy={() => onBuy(row.series, 1)}
                />
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
