// Détail d'une carte : visuel, rareté, chaîne, cours du coin, jetons bloqués ; burn et mise en vente.
// Jamais de « valeur garantie » : on montre un cours public et une quantité de jetons, le joueur fait ses calculs.

import { useEffect, useState } from "react";
import { estimateTokens, type TokenEstimate } from "../lib/backing";
import { waitBurnOutcome } from "../lib/burn";
import { listingDepositNote } from "../lib/market";
import { burnStorageRefund } from "../lib/pack";
import { readUntil } from "../lib/poll";
import { loadCatalog, STATE_LABEL, type CatalogEntry } from "../lib/catalog";
import { formatNearExact, formatQty, formatUsd, parseNear, RARITY_LABEL, yoctoToNumber } from "../lib/format";
import { coinUsd, nearUsd } from "../lib/prices";
import { getCard, getConfig, getResurrected } from "../near/contract";
import { humanError } from "../near/errors";
import { eventsOf, findEvent } from "../near/events";
import type { CardView } from "../near/types";
import { useWallet } from "../near/wallet";
import { Card } from "./Card";

type BurnState =
  | { kind: "idle" }
  | { kind: "confirm" }
  | { kind: "pending" }
  | { kind: "done"; text: string }
  | { kind: "failed"; text: string };

export function CardDetail({ tokenId, onChanged }: { tokenId: string; onChanged?: () => void }) {
  const { accountId, call } = useWallet();
  const [card, setCard] = useState<CardView | null | undefined>(undefined);
  const [entry, setEntry] = useState<CatalogEntry | undefined>();
  const [price, setPrice] = useState<number | null>(null);
  const [est, setEst] = useState<TokenEstimate | null>(null);
  const [usd, setUsd] = useState<number | null>(null);
  const [burn, setBurn] = useState<BurnState>({ kind: "idle" });
  const [listPrice, setListPrice] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Dépôt d'annonce lu dans `get_config` (pas écrit en dur).
  const [listingDeposit, setListingDeposit] = useState<string | null>(null);
  useEffect(() => {
    getConfig().then(
      (c) => setListingDeposit(c.listing_deposit),
      () => undefined,
    );
  }, []);

  const reload = () => getCard(tokenId).then(setCard, () => setCard(null));
  // Après une mise en vente ou un retrait : relecture jusqu'à voir le nouvel état (nœud RPC en retard).
  const reloadUntil = async (listed: boolean) => {
    const c = await readUntil(() => getCard(tokenId), (x) => !!x?.listing === listed);
    if (c !== undefined) setCard(c);
  };
  useEffect(() => {
    reload();
    nearUsd().then(setUsd);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tokenId]);

  useEffect(() => {
    if (!card?.card_id) return;
    loadCatalog().then((c) => {
      const e = c[card.card_id!];
      setEntry(e);
      if (e) coinUsd(e).then(setPrice);
      if (card.backing) estimateTokens(card.backing.amount, e).then(setEst);
    });
  }, [card?.card_id, card?.backing]);

  const [revived, setRevived] = useState(false);
  useEffect(() => {
    if (!card || card.kind !== "visible" || !card.backing) return setRevived(false);
    getResurrected(card.series_id, card.index).then(
      (b) => setRevived(b != null),
      () => setRevived(false),
    );
  }, [card]);

  if (card === undefined) return <p className="muted">Loading card…</p>;
  if (card === null)
    // Après un burn réussi, la carte n'existe plus : on garde le message du burn plutôt qu'un écran vide.
    return burn.kind === "done" ? <p className="success">{burn.text}</p> : <p className="muted">This card no longer exists (it may have been burned).</p>;

  const mine = card.owner_id === accountId;
  const mythic = card.kind === "mythic";
  const burnable = !!card.backing;
  // Carte d'un coin mort devenue brûlable (`card_resurrected`) : on le signale.
  const resurrected = burnable && revived;

  const doBurn = async () => {
    setBurn({ kind: "pending" });
    try {
      const out = await call("redeem", { token_id: card.token_id }, { deposit: "1", gas: "100000000000000" });
      const events = eventsOf(out);
      if (findEvent(events, "card_redeemed")) {
        // v3 : le stockage libéré par le burn est rendu (`card_redeemed.storage_refund`).
        const storage = burnStorageRefund(events);
        setBurn({
          kind: "done",
          text:
            `Card burned. ${est?.qty != null ? `About ${formatQty(est.qty)} ${est.ticker}` : "The tokens"} were sent to your account.` +
            (storage != null && storage > 0n ? ` The freed storage deposit (${formatNearExact(storage)} NEAR) was returned too.` : ""),
        });
      } else if (findEvent(events, "redeem_failed")) {
        setBurn({ kind: "failed", text: "The token delivery failed, so your card was restored. You can try again later." });
      } else {
        // Événements absents de la réponse du wallet : on relit la carte jusqu'à l'issue du burn
        // (sinon l'écran restait sur « Burn in progress… » sans jamais se mettre à jour).
        const outcome = await waitBurnOutcome(() => getCard(card.token_id));
        if (outcome === "burned") setBurn({ kind: "done", text: "Card burned. The tokens were sent to your account." });
        else if (outcome === "restored")
          setBurn({ kind: "failed", text: "The token delivery failed, so your card was restored. You can try again later." });
        else setBurn({ kind: "failed", text: "The burn is still in progress. Check your collection again in a minute." });
      }
      onChanged?.();
      reload();
    } catch (e) {
      setBurn({ kind: "failed", text: humanError(e) });
    }
  };

  const doList = async () => {
    setError(null);
    setBusy(true);
    try {
      const price = parseNear(listPrice);
      if (BigInt(price) <= 0n) throw new Error("Prix nul");
      const cfg = await getConfig();
      await call("list", { token_id: card.token_id, price }, { deposit: cfg.listing_deposit, gas: "30000000000000" });
      setListPrice("");
      await reloadUntil(true);
      onChanged?.();
    } catch (e) {
      setError(e instanceof Error && e.message === "Invalid amount" ? "Enter a price in NEAR, e.g. 0.5" : humanError(e));
    } finally {
      setBusy(false);
    }
  };

  const doDelist = async () => {
    setError(null);
    setBusy(true);
    try {
      await call("delist", { token_id: card.token_id }, { gas: "30000000000000" });
      await reloadUntil(false);
      onChanged?.();
    } catch (e) {
      setError(humanError(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="detail">
      <div className="detail__visual">
        <Card cardId={card.card_id} rarity={card.rarity} burnable={burnable} size="lg" />
      </div>
      <div className="detail__info">
        <span className={`rarity-text-${card.rarity} detail__rarity`}>{RARITY_LABEL[card.rarity]}</span>
        <h2>{mythic ? "?" : (entry?.name ?? card.card_id)}</h2>
        {!mythic && <p className="muted">{entry?.ticker}</p>}
        {mythic && <p className="muted">?</p>}
        {resurrected && <p className="pill pill--resurrected">Back from the dead · now burnable</p>}

        {!mythic && (
          <dl className="facts">
            <dt>Chain</dt>
            <dd>{entry?.chain ?? "Unknown"}</dd>
            <dt>Status</dt>
            <dd>{entry ? STATE_LABEL[entry.state] : "—"}</dd>
            <dt>Coin price</dt>
            <dd>{price != null ? `${formatUsd(price)} (public market price)` : "Not available"}</dd>
            <dt>Card</dt>
            <dd className="mono">#{card.token_id}</dd>
          </dl>
        )}

        {burnable && (
          <div className="locked">
            <span className="locked__label">Tokens locked in this card</span>
            <span className="locked__qty">
              {est?.qty != null ? `≈ ${formatQty(est.qty)} ${est.ticker}` : `${entry?.ticker ?? "Tokens"} · amount pending price`}
            </span>
            <small className="muted">Estimated from public prices at the time you burn. Not a guaranteed value.</small>
          </div>
        )}

        {card.listing && (
          <p className="listing-note">
            Listed for <strong>{formatNearExact(card.listing.price)} NEAR</strong>
            {usd != null && ` (≈ ${formatUsd(yoctoToNumber(card.listing.price) * usd)})`}
          </p>
        )}

        {mine && card.state === "redeeming" && <p className="pill">Burn in progress…</p>}

        {mine && card.state === "normal" && (
          <div className="detail__actions">
            {burnable && !card.listing && <BurnBox state={burn} setState={setBurn} onBurn={doBurn} ticker={entry?.ticker} />}
            {burn.kind !== "pending" &&
              (card.listing ? (
                <button className="btn" onClick={doDelist} disabled={busy}>
                  Remove from market
                </button>
              ) : (
                <div className="list-form">
                  <label htmlFor="price">Sell on the market</label>
                  <div className="row">
                    <input
                      id="price"
                      inputMode="decimal"
                      placeholder="Price in NEAR"
                      value={listPrice}
                      onChange={(e) => setListPrice(e.target.value)}
                    />
                    <button className="btn" onClick={doList} disabled={busy || !listPrice}>
                      List
                    </button>
                  </div>
                  <small className="muted">{listingDepositNote(listingDeposit)}</small>
                </div>
              ))}
          </div>
        )}
        {burn.kind === "done" && <p className="success">{burn.text}</p>}
        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

function BurnBox({
  state,
  setState,
  onBurn,
  ticker,
}: {
  state: BurnState;
  setState: (s: BurnState) => void;
  onBurn: () => void;
  ticker?: string;
}) {
  if (state.kind === "done") return null;
  if (state.kind === "pending")
    return (
      <div className="burnbox burnbox--pending">
        <span className="spinner" /> Burning… waiting for the token delivery.
      </div>
    );
  if (state.kind === "confirm")
    return (
      <div className="burnbox burnbox--confirm">
        <p>
          <strong>Burning destroys this card.</strong> You receive the {ticker ?? "coin"} tokens locked in it, directly in
          your account. This cannot be undone.
        </p>
        <div className="row">
          <button className="btn btn--danger" onClick={onBurn}>
            Burn the card
          </button>
          <button className="btn btn--ghost" onClick={() => setState({ kind: "idle" })}>
            Keep it
          </button>
        </div>
      </div>
    );
  return (
    <div className="burnbox">
      <button className="btn btn--burn" onClick={() => setState({ kind: "confirm" })}>
        🔥 Burn
      </button>
      {state.kind === "failed" && <p className="error">{state.text}</p>}
    </div>
  );
}
