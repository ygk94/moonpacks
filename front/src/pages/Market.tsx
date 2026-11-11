// Marché intégré au contrat : `get_listings`, `buy(token_id, expected_price)`, `delist`.
// « Trending » : en attendant l'indexeur des événements (`card_listed`, `card_sold`), on classe les coins les plus
// listés en ce moment, à partir des annonces elles-mêmes.

import { useMemo, useState } from "react";
import { Card } from "../components/Card";
import { CardDetail } from "../components/CardDetail";
import { Modal } from "../components/Modal";
import { loadCatalog } from "../lib/catalog";
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

  const trending = useMemo(() => {
    const by = new Map<string, { key: string; ticker: string; count: number; floor: bigint; row: Row }>();
    for (const r of rows.data ?? []) {
      if (!r.card) continue;
      const key = r.card.kind === "mythic" ? "mythic" : (r.card.card_id ?? r.tokenId);
      const cur = by.get(key);
      const price = BigInt(r.listing.price);
      if (!cur) by.set(key, { key, ticker: r.ticker, count: 1, floor: price, row: r });
      else {
        cur.count++;
        if (price < cur.floor) cur.floor = price;
      }
    }
    return [...by.values()].sort((a, b) => b.count - a.count).slice(0, 6);
  }, [rows.data]);

  const buy = async (r: Row) => {
    setBusy(r.tokenId);
    setMessage(null);
    try {
      await call("buy", { token_id: r.tokenId, expected_price: r.listing.price }, { deposit: r.listing.price, gas: "100000000000000" });
      setMessage({ ok: true, text: `You bought ${r.ticker} #${r.tokenId}. It is now in your collection.` });
      rows.reload();
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
        <button className="btn btn--ghost" onClick={rows.reload}>
          Refresh
        </button>
      </div>
      {message && <p className={message.ok ? "success" : "error"}>{message.text}</p>}

      {trending.length > 0 && (
        <section className="trending">
          <h2>Trending</h2>
          <p className="small muted">Most listed coins right now.</p>
          <div className="trending__row">
            {trending.map((t) => (
              <button key={t.key} className="trending__item" onClick={() => setOpen(t.row.tokenId)}>
                <Card cardId={t.row.card?.card_id ?? null} rarity={t.row.card!.rarity} size="sm" tilt={false} />
                <span className="trending__ticker">{t.ticker}</span>
                <small>
                  {t.count} listed · from {formatNear(t.floor)} NEAR
                </small>
              </button>
            ))}
          </div>
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
