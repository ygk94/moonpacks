// Marché intégré au contrat : `get_listings`, `buy(token_id, expected_price)`, `delist`.
// « Trending » : avec l'indexeur (front/indexer/), cartes les plus vendues ou listées sur 24 h, et dernières
// ventes ; sans lui, coins les plus listés en ce moment, à partir des annonces elles-mêmes.

import { useMemo, useState } from "react";
import { Card } from "../components/Card";
import { CardDetail } from "../components/CardDetail";
import { Modal } from "../components/Modal";
import { loadCatalog } from "../lib/catalog";
import { fetchSales, fetchTrending } from "../lib/indexer";
import { formatNear, formatUsd, RARITY_LABEL, shortAccount, yoctoToNumber } from "../lib/format";
import { nearUsd } from "../lib/prices";
import { useAsync } from "../lib/useAsync";
import { getCard, getListings } from "../near/contract";
import { humanError } from "../near/errors";
import type { CardView, Listing } from "../near/types";
import { useWallet } from "../near/wallet";

interface Row {
  tokenId: string;
  listing: Listing;
  card: CardView | null;
  ticker: string;
  name: string;
}

export function Market() {
  const { accountId, call } = useWallet();
  const [open, setOpen] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);
  const usd = useAsync(() => nearUsd(), []);

  const rows = useAsync(async (): Promise<Row[]> => {
    const [listings, catalog] = await Promise.all([getListings(), loadCatalog()]);
    const cards = await Promise.all(listings.map(([id]) => getCard(id).catch(() => null)));
    return listings.map(([tokenId, listing], i) => {
      const card = cards[i];
      const e = card?.card_id ? catalog[card.card_id] : undefined;
      const mythic = card?.kind === "mythic";
      return {
        tokenId,
        listing,
        card,
        ticker: mythic ? "?" : (e?.ticker ?? card?.card_id ?? "?"),
        name: mythic ? "?" : (e?.name ?? ""),
      };
    });
  }, []);

  const indexed = useAsync(async () => {
    const [t, s] = await Promise.all([fetchTrending(24), fetchSales()]);
    return t && s ? { trending: t.items, sales: s.items } : null;
  }, []);
  const catalog = useAsync(() => loadCatalog(), []);
  const tickerOf = (cardId: string | null, kind?: string | null) =>
    kind === "mythic" || !cardId ? "?" : (catalog.data?.[cardId]?.ticker ?? cardId);

  interface TrendView {
    key: string;
    cardId: string | null;
    rarity: CardView["rarity"];
    ticker: string;
    line: string;
    tokenId?: string;
  }

  const trending = useMemo((): { items: TrendView[]; caption: string } => {
    // Annonce ouverte la moins chère pour chaque carte (pour ouvrir le détail depuis Trending).
    const cheapest = new Map<string, Row>();
    for (const r of rows.data ?? []) {
      if (!r.card) continue;
      const key = r.card.kind === "mythic" ? "mythic" : (r.card.card_id ?? r.tokenId);
      const cur = cheapest.get(key);
      if (!cur || BigInt(r.listing.price) < BigInt(cur.listing.price)) cheapest.set(key, r);
    }
    if (indexed.data?.trending.length) {
      return {
        caption: "Most sold and listed cards over the last 24 hours.",
        items: indexed.data.trending.map((t) => {
          const key = t.kind === "mythic" ? "mythic" : (t.card_id ?? "");
          return {
            key,
            cardId: t.card_id,
            rarity: t.rarity,
            ticker: tickerOf(t.card_id, t.kind),
            line: `${t.sales} sold · ${t.listings} listed`,
            tokenId: cheapest.get(key)?.tokenId,
          };
        }),
      };
    }
    const counts = new Map<string, number>();
    for (const r of rows.data ?? []) {
      if (!r.card) continue;
      const key = r.card.kind === "mythic" ? "mythic" : (r.card.card_id ?? r.tokenId);
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    return {
      caption: "Most listed coins right now.",
      items: [...counts.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([key, n]) => {
          const r = cheapest.get(key)!;
          return {
            key,
            cardId: r.card?.card_id ?? null,
            rarity: r.card!.rarity,
            ticker: r.ticker,
            line: `${n} listed · from ${formatNear(r.listing.price)} NEAR`,
            tokenId: r.tokenId,
          };
        }),
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rows.data, indexed.data, catalog.data]);

  const buy = async (r: Row) => {
    setBusy(r.tokenId);
    setMessage(null);
    try {
      await call("buy", { token_id: r.tokenId, expected_price: r.listing.price }, { deposit: r.listing.price, gas: "100000000000000" });
      setMessage({ ok: true, text: `You bought ${r.ticker} #${r.tokenId}. It is now in your collection.` });
      rows.reload();
      indexed.reload();
    } catch (e) {
      setMessage({ ok: false, text: humanError(e) });
    } finally {
      setBusy(null);
    }
  };

  const nearPrice = usd.data ?? null;

  return (
    <div className="page market">
      <div className="page__head">
        <h1>Market</h1>
        <button
          className="btn btn--ghost"
          onClick={() => {
            rows.reload();
            indexed.reload();
          }}
        >
          Refresh
        </button>
      </div>
      {message && <p className={message.ok ? "success" : "error"}>{message.text}</p>}

      {trending.items.length > 0 && (
        <section className="trending">
          <h2>Trending</h2>
          <p className="small muted">{trending.caption}</p>
          <div className="trending__row">
            {trending.items.map((t) => (
              <button
                key={t.key}
                className="trending__item"
                onClick={() => t.tokenId && setOpen(t.tokenId)}
                disabled={!t.tokenId}
                title={t.tokenId ? "See the cheapest listing" : "Not listed right now"}
              >
                <Card cardId={t.cardId} rarity={t.rarity} size="sm" tilt={false} />
                <span className="trending__ticker">{t.ticker}</span>
                <small>{t.line}</small>
              </button>
            ))}
          </div>
        </section>
      )}

      {indexed.data && indexed.data.sales.length > 0 && (
        <section className="sales">
          <h2>Recent sales</h2>
          <ul className="sales__list">
            {indexed.data.sales.map((s) => (
              <li key={`${s.token_id}-${s.height}`}>
                <Card cardId={s.kind === "mythic" ? null : s.card_id} rarity={s.rarity ?? "common"} size="sm" tilt={false} />
                <span className="sales__ticker">{tickerOf(s.card_id, s.kind)}</span>
                <span className="sales__price">{formatNear(s.price)} NEAR</span>
                <small className="muted">{new Date(s.ts).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" })}</small>
              </li>
            ))}
          </ul>
        </section>
      )}

      <h2>All listings</h2>
      {rows.loading && !rows.data && <p className="muted">Loading listings…</p>}
      {rows.error != null && <p className="error">Could not load the market.</p>}
      {rows.data && !rows.data.length && <p className="muted">No card is listed for now. List one from your collection.</p>}
      <div className="grid">
        {rows.data?.map((r) => {
          const mine = r.listing.seller_id === accountId;
          return (
            <div key={r.tokenId} className="grid__item listing">
              <Card
                cardId={r.card?.card_id ?? null}
                rarity={r.card?.rarity ?? "common"}
                burnable={!!r.card?.backing}
                onClick={() => setOpen(r.tokenId)}
              />
              <div className="listing__info">
                <span className={`rarity-text-${r.card?.rarity ?? "common"}`}>{RARITY_LABEL[r.card?.rarity ?? "common"]}</span>
                <strong>{r.ticker}</strong>
                <span className="listing__price">
                  {formatNear(r.listing.price)} NEAR
                  {nearPrice != null && <small> ≈ {formatUsd(yoctoToNumber(r.listing.price) * nearPrice)}</small>}
                </span>
                <small className="muted">by {shortAccount(r.listing.seller_id)}</small>
                {mine ? (
                  <button className="btn btn--ghost" onClick={() => setOpen(r.tokenId)}>
                    Manage
                  </button>
                ) : (
                  <button className="btn btn--primary" disabled={!accountId || busy === r.tokenId} onClick={() => buy(r)}>
                    {busy === r.tokenId ? "Buying…" : accountId ? "Buy" : "Connect to buy"}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <Modal open={open != null} onClose={() => setOpen(null)} wide>
        {open && <CardDetail tokenId={open} onChanged={rows.reload} />}
      </Modal>
    </div>
  );
}
