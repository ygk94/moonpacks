// Ouverture d'un booster : le moment fort du produit.
//
// Déroulé : signature (le pack flotte, « confirm in your wallet ») → pack scellé on-chain (`pack_bought`) →
// tirage en 3 blocs (le pack vibre, étape n/3) → le pack se déchire → 5 cartes révélées une par une, la
// brûlable en dernier → récapitulatif avec la quantité de jetons de la brûlable.
// L'animation ne s'arrête jamais sans rien montrer, et révèle dès que `get_pack` renvoie le tirage.
// Gold pack : mise en scène à part (fond or, suspense sur la dernière carte), annoncé seulement à la déchirure.

import { AnimatePresence, motion } from "framer-motion";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Card, CardBack } from "../components/Card";
import { PackArt } from "../components/PackArt";
import { estimateTokens, type TokenEstimate } from "../lib/backing";
import { loadCatalog, type CatalogEntry } from "../lib/catalog";
import { formatQty, RARITY_LABEL } from "../lib/format";
import { burnableLast } from "../lib/reveal";
import { navigate } from "../lib/router";
import { getCardDefs, getConfig, getPack } from "../near/contract";
import { humanError } from "../near/errors";
import { eventsOf, findEvent, returnValue } from "../near/events";
import { blockHeight } from "../near/rpc";
import type { PackMode, PackView, Rarity, SeriesView } from "../near/types";
import { useWallet } from "../near/wallet";
import { VerifyPanel } from "../verify/VerifyPanel";

export type OpeningRequest = { kind: "buy"; series: SeriesView } | { kind: "replay"; packId: number };

type Phase = "signing" | "sealing" | "drawing" | "tearing" | "revealing" | "done" | "error" | "stuck";

interface RevealCard {
  slot: number;
  tokenId: string;
  cardId: string | null;
  rarity: Rarity;
  burnable: boolean;
  amount: string | null;
  entry?: CatalogEntry;
}

// Temps de pose d'une carte révélée, de plus en plus long avec la rareté.
const HOLD_MS: Record<Rarity, number> = { common: 650, rare: 1000, epic: 1350, legendary: 2000, mythic: 2800 };
// Anticipation avant le retournement (lueur du dos) : aucune pour une commune.
const ANTICIPATION_MS: Record<Rarity, number> = { common: 0, rare: 260, epic: 420, legendary: 650, mythic: 900 };
const GOLD_SUSPENSE_MS = 2600;
const POLL_MS = 500;
const MAX_GAS = "300000000000000";

export function Opening({ request, onClose }: { request: OpeningRequest; onClose: () => void }) {
  const { call, accountId } = useWallet();
  const [phase, setPhase] = useState<Phase>(request.kind === "buy" ? "signing" : "sealing");
  const [packId, setPackId] = useState<number | null>(request.kind === "replay" ? request.packId : null);
  const [pack, setPack] = useState<PackView | null>(null);
  const [cards, setCards] = useState<RevealCard[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [step, setStep] = useState(0);
  const [steps, setSteps] = useState(3);
  const [canRetry, setCanRetry] = useState(false);
  const [retrying, setRetrying] = useState(false);
  const started = useRef(false);

  // Données préchargées pendant la signature : définitions des cartes et fiches publiques.
  useEffect(() => {
    getCardDefs().catch(() => undefined);
    loadCatalog().catch(() => undefined);
    getConfig()
      .then((c) => setSteps(c.reveal_steps))
      .catch(() => undefined);
  }, []);

  // 1. Achat (signature) : l'animation tourne déjà.
  useEffect(() => {
    if (request.kind !== "buy" || started.current) return;
    started.current = true;
    const s = request.series;
    const gas = BigInt(s.min_gas) > BigInt(MAX_GAS) ? s.min_gas : MAX_GAS;
    call("buy_pack", { series_id: s.series_id }, { deposit: s.required_deposit, gas })
      .then((out) => {
        const ev = findEvent(eventsOf(out), "pack_bought");
        const id = Number(ev?.pack_id ?? returnValue<string>(out));
        if (!Number.isFinite(id)) throw new Error("Pack id not found in the transaction.");
        setPackId(id);
        setPhase("sealing");
      })
      .catch((e) => {
        setError(humanError(e));
        setPhase("error");
      });
  }, [request, call]);

  // 2. Attente du tirage : get_pack toutes les 500 ms ; relance proposée si le pack ne progresse plus.
  useEffect(() => {
    if (packId == null || !["sealing", "drawing"].includes(phase)) return;
    let stop = false;
    const tick = async () => {
      try {
        const p = await getPack(packId);
        if (stop) return;
        if (!p) throw new Error("Pack not found.");
        setPack(p);
        setStep(p.step);
        if (p.status === "revealed") {
          setCards(await resolveCards(p));
          if (!stop) setPhase("tearing");
          return;
        }
        if (p.status === "stuck") {
          setPhase("stuck");
          return;
        }
        setPhase("drawing");
        const [h, cfg] = await Promise.all([blockHeight(), getConfig()]);
        setCanRetry(h >= p.last_progress_height + cfg.retry_delay_blocks);
      } catch {
        // erreur réseau passagère : on réessaie au prochain tour
      }
      if (!stop) setTimeout(tick, POLL_MS);
    };
    tick();
    return () => {
      stop = true;
    };
  }, [packId, phase]);

  const retry = async () => {
    if (packId == null) return;
    setRetrying(true);
    try {
      const cfg = await getConfig();
      await call("retry_reveal", { pack_id: packId }, { gas: maxGas(cfg.gas.min_entry) });
      setCanRetry(false);
      setPhase("drawing");
    } catch (e) {
      setError(humanError(e));
    } finally {
      setRetrying(false);
    }
  };

  const mode: PackMode = pack?.mode ?? "base";
  const gold = mode === "gold" && ["tearing", "revealing", "done"].includes(phase);

  return (
    <div className={`opening${gold ? " opening--gold" : ""}`}>
      <div className="opening__bg" aria-hidden />
      <header className="opening__top">
        <span className="opening__title">
          {packId != null ? `Pack #${packId}` : "New pack"}
          {pack?.rush && <span className="pill pill--rush">Rush pack</span>}
          {gold && <span className="pill pill--gold">Gold pack</span>}
        </span>
        {["done", "error", "stuck"].includes(phase) || request.kind === "replay" ? (
          <button className="btn btn--ghost" onClick={onClose}>
            Close
          </button>
        ) : null}
      </header>

      <div className="opening__stage">
        <AnimatePresence mode="wait">
          {(phase === "signing" || phase === "sealing" || phase === "drawing") && (
            <PackStage key="pack" phase={phase} step={step} steps={steps} />
          )}
          {phase === "tearing" && <TearStage key="tear" gold={mode === "gold"} onDone={() => setPhase("revealing")} />}
          {phase === "revealing" && (
            <RevealStage key="reveal" cards={cards} gold={mode === "gold"} onDone={() => setPhase("done")} />
          )}
          {phase === "done" && <Summary key="done" cards={cards} packId={packId} />}
          {phase === "error" && (
            <motion.div key="err" className="opening__message" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <h2>The pack was not bought</h2>
              <p>{error}</p>
              <p className="muted">Nothing was charged if the transaction did not go through.</p>
            </motion.div>
          )}
          {phase === "stuck" && (
            <motion.div key="stuck" className="opening__message" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <h2>This pack could not be revealed</h2>
              <p>
                The draw failed several times and the pack is marked as stuck on-chain. Please contact the team with your
                pack number: <strong>#{packId}</strong>.
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <footer className="opening__bottom">
        {phase === "drawing" && canRetry && (
          <div className="opening__retry">
            <p>The draw is taking longer than expected. You can restart it; this does not change your odds.</p>
            <button className="btn btn--primary" onClick={retry} disabled={retrying || !accountId}>
              {retrying ? "Restarting…" : "Retry reveal"}
            </button>
            {error && <p className="error">{error}</p>}
          </div>
        )}
        {phase === "done" && (
          <div className="opening__actions">
            <button
              className="btn btn--primary"
              onClick={() => {
                onClose();
                navigate("/shop");
              }}
            >
              Back to shop
            </button>
            <button
              className="btn"
              onClick={() => {
                onClose();
                navigate("/collection");
              }}
            >
              View my collection
            </button>
          </div>
        )}
        {phase === "error" && (
          <button className="btn btn--primary" onClick={onClose}>
            Back to shop
          </button>
        )}
      </footer>
    </div>
  );
}

function maxGas(min: string): string {
  return BigInt(min) > BigInt(MAX_GAS) ? min : MAX_GAS;
}

/** Cartes du tirage, brûlable(s) en dernier ; identité lue dans la table (marche même après un burn). */
async function resolveCards(p: PackView): Promise<RevealCard[]> {
  const [defs, catalog] = await Promise.all([getCardDefs(p.series_id), loadCatalog()]);
  const cards = p.draws.map((d) => {
    const def = d.kind === "visible" ? defs[d.index] : undefined;
    const amount = p.value?.amounts[d.slot] ?? null;
    const cardId = def?.card_id ?? null;
    return {
      slot: d.slot,
      tokenId: d.token_id,
      cardId,
      rarity: d.final_rarity,
      burnable: amount != null || !!def?.backing,
      amount: amount ?? def?.backing?.amount ?? null,
      entry: cardId ? catalog[cardId] : undefined,
    };
  });
  return burnableLast(cards);
}

// --- Étapes de la scène ------------------------------------------------------------------------

function PackStage({ phase, step, steps }: { phase: Phase; step: number; steps: number }) {
  const text =
    phase === "signing"
      ? "Confirm the purchase in your wallet"
      : phase === "sealing"
        ? "Sealing your pack on-chain…"
        : `Drawing your cards… block ${Math.min(step + 1, steps)} of ${steps}`;
  return (
    <motion.div
      className="pack-stage"
      initial={{ opacity: 0, y: 40, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 1.08, filter: "brightness(2)" }}
      transition={{ duration: 0.45 }}
    >
      <motion.div
        className={`pack-stage__pack pack-stage__pack--${phase}`}
        animate={
          phase === "drawing"
            ? { rotate: [0, -2.5, 2.5, -1.5, 1.5, 0], y: [0, -4, 0] }
            : { y: [0, -14, 0], rotate: [0, 1.2, 0] }
        }
        transition={
          phase === "drawing"
            ? { duration: 0.55, repeat: Infinity, ease: "easeInOut" }
            : { duration: 3.2, repeat: Infinity, ease: "easeInOut" }
        }
      >
        <PackArt seed={11} />
        <div className="pack-stage__charge" style={{ opacity: phase === "drawing" ? 0.35 + (0.6 * step) / steps : 0 }} />
      </motion.div>
      <div className="pack-stage__status">
        <span className="spinner" aria-hidden />
        <span>{text}</span>
      </div>
      {phase === "drawing" && (
        <div className="steps" aria-label={`Step ${step} of ${steps}`}>
          {Array.from({ length: steps }, (_, i) => (
            <span key={i} className={`steps__dot${i < step ? " steps__dot--done" : i === step ? " steps__dot--live" : ""}`} />
          ))}
        </div>
      )}
    </motion.div>
  );
}

function TearStage({ gold, onDone }: { gold: boolean; onDone: () => void }) {
  useEffect(() => {
    const t = setTimeout(onDone, gold ? 1900 : 1100);
    return () => clearTimeout(t);
  }, [gold, onDone]);
  return (
    <motion.div className="tear" initial={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
      <motion.div
        className="tear__burst"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: [0, 1.4, 2.6], opacity: [0, 1, 0] }}
        transition={{ duration: gold ? 1.6 : 1, delay: 0.25, ease: "easeOut" }}
      />
      <motion.div
        className="tear__top"
        initial={{ y: 0, rotate: 0 }}
        animate={{ y: -260, rotate: -18, opacity: 0 }}
        transition={{ duration: 0.7, delay: 0.15, ease: [0.3, 0.7, 0.4, 1] }}
      >
        <PackArt seed={11} variant={gold ? "gold" : "standard"} className="pack--clip-top" />
      </motion.div>
      <motion.div
        className="tear__bottom"
        initial={{ y: 0 }}
        animate={{ y: 340, opacity: 0 }}
        transition={{ duration: 0.8, delay: 0.3, ease: [0.5, 0, 0.75, 0] }}
      >
        <PackArt seed={11} variant={gold ? "gold" : "standard"} className="pack--clip-bottom" />
      </motion.div>
      {gold && (
        <motion.div
          className="tear__gold"
          initial={{ opacity: 0, scale: 0.8, letterSpacing: "0.1em" }}
          animate={{ opacity: [0, 1, 1], scale: 1, letterSpacing: "0.4em" }}
          transition={{ duration: 1.4, delay: 0.4 }}
        >
          GOLD PACK
        </motion.div>
      )}
    </motion.div>
  );
}

function RevealStage({ cards, gold, onDone }: { cards: RevealCard[]; gold: boolean; onDone: () => void }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [anticipating, setAnticipating] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const card = cards[index];
  const last = index === cards.length - 1;
  const suspense = gold && last;

  const clear = () => {
    if (timer.current) clearTimeout(timer.current);
  };

  const next = useCallback(() => {
    clear();
    setFlipped(false);
    setAnticipating(false);
    if (index + 1 >= cards.length) onDone();
    else setIndex(index + 1);
  }, [index, cards.length, onDone]);

  // Pour chaque carte : anticipation (lueur), retournement, pose, puis carte suivante.
  useEffect(() => {
    if (!card) return;
    clear();
    const pre = suspense ? GOLD_SUSPENSE_MS : ANTICIPATION_MS[card.rarity] + 350;
    setAnticipating(ANTICIPATION_MS[card.rarity] > 0 || suspense);
    timer.current = setTimeout(() => {
      setAnticipating(false);
      setFlipped(true);
      timer.current = setTimeout(next, HOLD_MS[card.rarity] + (last ? 900 : 0));
    }, pre);
    return clear;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [index]);

  // Toucher la scène : retourne tout de suite, ou passe à la suivante si la carte est déjà retournée.
  const tap = () => {
    if (!flipped) {
      clear();
      setAnticipating(false);
      setFlipped(true);
      timer.current = setTimeout(next, HOLD_MS[card.rarity]);
    } else next();
  };

  if (!card) return null;
  return (
    <motion.div className="reveal" onClick={tap} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <div className="reveal__spot">
        <AnimatePresence mode="popLayout">
          <motion.div
            key={index}
            className={`reveal__card${suspense && anticipating ? " reveal__card--suspense" : ""}`}
            initial={{ y: 120, opacity: 0, scale: 0.85 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: 220, x: (index - 2) * 40, opacity: 0, scale: 0.4 }}
            transition={{ type: "spring", stiffness: 260, damping: 26 }}
          >
            {flipped && <Burst rarity={card.rarity} />}
            <motion.div
              className="flip"
              animate={{ rotateY: flipped ? 0 : 180 }}
              initial={{ rotateY: 180 }}
              transition={{ duration: 0.55, ease: [0.3, 0.8, 0.3, 1] }}
            >
              <div className="flip__face flip__face--front">
                <Card cardId={card.cardId} rarity={card.rarity} title={card.entry?.ticker} burnable={card.burnable} size="lg" />
              </div>
              <div className="flip__face flip__face--back">
                <CardBack size="lg" glow={anticipating ? (suspense ? "legendary" : card.rarity) : null} />
              </div>
            </motion.div>
          </motion.div>
        </AnimatePresence>
        <AnimatePresence>
          {flipped && (
            <motion.div
              key={`label-${index}`}
              className={`reveal__label rarity-text-${card.rarity}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <strong>{RARITY_LABEL[card.rarity]}</strong>
              <span>{card.rarity === "mythic" ? "?" : (card.entry?.name ?? card.cardId)}</span>
              {card.burnable && <BurnableLine card={card} />}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      <div className="reveal__tray">
        {cards.map((c, i) => (
          <div key={c.tokenId} className={`reveal__slot${i === index ? " reveal__slot--live" : ""}`}>
            {i < index || (i === index && flipped) ? (
              <Card cardId={c.cardId} rarity={c.rarity} size="sm" tilt={false} burnable={false} />
            ) : (
              <CardBack size="sm" />
            )}
          </div>
        ))}
      </div>
      <p className="reveal__hint muted">{suspense && !flipped ? "…" : "Tap to continue"}</p>
    </motion.div>
  );
}

/** Éclat coloré au retournement, plus riche avec la rareté (particules dès légendaire). */
function Burst({ rarity }: { rarity: Rarity }) {
  const particles = rarity === "mythic" ? 36 : rarity === "legendary" ? 24 : rarity === "epic" ? 10 : 0;
  const dots = useMemo(
    () =>
      Array.from({ length: particles }, (_, i) => {
        const a = (i / particles) * Math.PI * 2 + Math.random() * 0.4;
        const d = 160 + Math.random() * 160;
        return { x: Math.cos(a) * d, y: Math.sin(a) * d, s: 3 + Math.random() * 5, delay: Math.random() * 0.15 };
      }),
    [particles],
  );
  if (rarity === "common") return null;
  return (
    <div className={`burst rarity-${rarity}`} aria-hidden>
      <motion.div
        className="burst__ring"
        initial={{ scale: 0.3, opacity: 0.9 }}
        animate={{ scale: 2.4, opacity: 0 }}
        transition={{ duration: rarity === "rare" ? 0.7 : 1.1, ease: "easeOut" }}
      />
      {dots.map((p, i) => (
        <motion.span
          key={i}
          className="burst__dot"
          style={{ width: p.s, height: p.s }}
          initial={{ x: 0, y: 0, opacity: 1 }}
          animate={{ x: p.x, y: p.y, opacity: 0 }}
          transition={{ duration: 1.2, delay: p.delay, ease: "easeOut" }}
        />
      ))}
    </div>
  );
}

function useTokenEstimate(card: RevealCard): TokenEstimate | null {
  const [est, setEst] = useState<TokenEstimate | null>(null);
  useEffect(() => {
    if (!card.amount) return;
    estimateTokens(card.amount, card.entry).then(setEst);
  }, [card.amount, card.entry]);
  return est;
}

function BurnableLine({ card }: { card: RevealCard }) {
  const est = useTokenEstimate(card);
  return (
    <span className="burnable-line">
      🔥 Burnable · {est?.qty != null ? `≈ ${formatQty(est.qty)} ${est.ticker}` : `${card.entry?.ticker ?? "tokens"} locked`}
    </span>
  );
}

function Summary({ cards, packId }: { cards: RevealCard[]; packId: number | null }) {
  return (
    <motion.div className="summary" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
      <h2>Your pack</h2>
      <div className="summary__grid">
        {cards.map((c, i) => (
          <motion.div
            key={c.tokenId}
            className="summary__item"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            <Card cardId={c.cardId} rarity={c.rarity} burnable={c.burnable} size="md" />
            <div className="summary__caption">
              <span className={`rarity-text-${c.rarity}`}>{RARITY_LABEL[c.rarity]}</span>
              <span>{c.rarity === "mythic" ? "?" : (c.entry?.ticker ?? c.cardId)}</span>
              {c.burnable && <BurnableLine card={c} />}
            </div>
          </motion.div>
        ))}
      </div>
      {cards.some((c) => c.burnable) && (
        <p className="muted small">
          Burn a burnable card from your collection to receive its tokens. The token amount shown is estimated from
          public market prices.
        </p>
      )}
      {packId != null && <VerifyPanel packId={packId} />}
    </motion.div>
  );
}
