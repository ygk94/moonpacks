// Mes cartes (`nft_tokens_for_owner`), filtrables par rareté et par « burnable », et mes packs (rejouables).
// Pas de cimetière séparé : les coins morts sont des cartes comme les autres.

import { useMemo, useState } from "react";
import { Card } from "../components/Card";
import { CardDetail } from "../components/CardDetail";
import { ConnectButton } from "../components/Header";
import { Modal } from "../components/Modal";
import { loadCatalog } from "../lib/catalog";
import { RARITY_LABEL } from "../lib/format";
import { useAsync } from "../lib/useAsync";
import { getCard, getPacksForOwner, getResurrected, getTokensForOwner } from "../near/contract";
import { RARITIES, RARITY_RANK, type Rarity } from "../near/types";
import { useWallet } from "../near/wallet";
import { VerifyPanel } from "../verify/VerifyPanel";

interface OwnedCard {
  tokenId: string;
  cardId: string | null;
  rarity: Rarity;
  burnable: boolean;
  packId: number;
  ticker: string;
  revived: boolean;
}

export function Collection({ onReplay }: { onReplay: (packId: number) => void }) {
  const { accountId } = useWallet();
  const [rarity, setRarity] = useState<Rarity | "all">("all");
  const [onlyBurnable, setOnlyBurnable] = useState(false);
  const [open, setOpen] = useState<string | null>(null);
  const [tab, setTab] = useState<"cards" | "packs">("cards");

  const cards = useAsync(async (): Promise<OwnedCard[]> => {
    if (!accountId) return [];
    const [tokens, catalog] = await Promise.all([getTokensForOwner(accountId), loadCatalog()]);
    const list = tokens.map((t) => {
      let extra: { card_id?: string; rarity?: Rarity; burnable?: boolean; pack_id?: number } = {};
      try {
        extra = JSON.parse(t.metadata?.extra ?? "{}");
      } catch {
        // métadonnées sans extra lisible
      }
      const rarity = extra.rarity ?? "common";
      const cardId = rarity === "mythic" ? null : (extra.card_id ?? null);
      const e = cardId ? catalog[cardId] : undefined;
      return {
        tokenId: t.token_id,
        cardId,
        rarity,
        burnable: !!extra.burnable,
        packId: extra.pack_id ?? Math.floor(Number(t.token_id) / 10),
        ticker: rarity === "mythic" ? "?" : (e?.ticker ?? cardId ?? "?"),
        revived: false,
      };
    });
    // Cartes ressuscitées (`card_resurrected`) : seules les épiques et légendaires peuvent l'être.
    await Promise.all(
      list
        .filter((c) => c.burnable && (c.rarity === "epic" || c.rarity === "legendary"))
        .map(async (c) => {
          const v = await getCard(c.tokenId).catch(() => null);
          if (v?.kind === "visible") c.revived = (await getResurrected(v.series_id, v.index).catch(() => null)) != null;
        }),
    );
    return list;
  }, [accountId]);

  const packs = useAsync(() => (accountId ? getPacksForOwner(accountId) : Promise.resolve([])), [accountId]);

  const shown = useMemo(() => {
    const list = (cards.data ?? []).filter(
      (c) => (rarity === "all" || c.rarity === rarity) && (!onlyBurnable || c.burnable),
    );
    return list.sort((a, b) => RARITY_RANK[b.rarity] - RARITY_RANK[a.rarity] || Number(b.tokenId) - Number(a.tokenId));
  }, [cards.data, rarity, onlyBurnable]);

  if (!accountId)
    return (
      <div className="page empty">
        <h1>My collection</h1>
        <p className="muted">Connect a wallet to see your cards.</p>
        <ConnectButton big />
      </div>
    );

  const counts = (cards.data ?? []).reduce<Record<string, number>>((m, c) => ((m[c.rarity] = (m[c.rarity] ?? 0) + 1), m), {});

  return (
    <div className="page collection">
      <div className="page__head">
        <h1>My collection</h1>
        <div className="tabs">
          <button className={tab === "cards" ? "active" : ""} onClick={() => setTab("cards")}>
            Cards {cards.data ? `(${cards.data.length})` : ""}
          </button>
          <button className={tab === "packs" ? "active" : ""} onClick={() => setTab("packs")}>
            Packs {packs.data ? `(${packs.data.length})` : ""}
          </button>
        </div>
      </div>

      {tab === "cards" && (
        <>
          <div className="filters">
            <button className={`chip${rarity === "all" ? " chip--on" : ""}`} onClick={() => setRarity("all")}>
              All
            </button>
            {RARITIES.map((r) => (
              <button
                key={r}
                className={`chip chip--${r}${rarity === r ? " chip--on" : ""}`}
                onClick={() => setRarity(r)}
              >
                {RARITY_LABEL[r]} {counts[r] ? `· ${counts[r]}` : ""}
              </button>
            ))}
            <label className="toggle">
              <input type="checkbox" checked={onlyBurnable} onChange={(e) => setOnlyBurnable(e.target.checked)} />
              Burnable only
            </label>
          </div>
          {cards.loading && !cards.data && <p className="muted">Loading your cards…</p>}
          {cards.error != null && <p className="error">Could not load your cards.</p>}
          {cards.data && !shown.length && (
            <p className="muted">{cards.data.length ? "No card matches these filters." : "No card yet. Open a pack in the shop!"}</p>
          )}
          <div className="grid">
            {shown.map((c) => (
              <div key={c.tokenId} className="grid__item">
                <Card
                  cardId={c.cardId}
                  rarity={c.rarity}
                  burnable={c.burnable}
                  badge={c.revived ? "Back from the dead" : undefined}
                  onClick={() => setOpen(c.tokenId)}
                  size="md"
                />
                <span className="grid__caption">{c.ticker}</span>
              </div>
            ))}
          </div>
        </>
      )}

      {tab === "packs" && (
        <div className="packs-list">
          {packs.data && !packs.data.length && <p className="muted">No pack yet.</p>}
          {[...(packs.data ?? [])].reverse().map((id) => (
            <div key={id} className="packs-list__row">
              <div className="packs-list__head">
                <span>Pack #{id}</span>
                <button className="btn btn--ghost" onClick={() => onReplay(id)}>
                  Replay opening
                </button>
              </div>
              <VerifyPanel packId={id} />
            </div>
          ))}
        </div>
      )}

      <Modal open={open != null} onClose={() => setOpen(null)} wide>
        {open && <CardDetail tokenId={open} onChanged={cards.reload} />}
      </Modal>
    </div>
  );
}
