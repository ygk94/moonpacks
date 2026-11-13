import { AnimatePresence, motion } from "framer-motion";
import { lazy, Suspense, useEffect, useState } from "react";
import { DemoBanner, Header } from "./components/Header";
import { BRAND } from "./lib/brand";
import { useRoute } from "./lib/router";
import type { OpeningRequest } from "./pages/Opening";
import { Shop } from "./pages/Shop";

// Pages secondaires chargées à la demande : la boutique s'affiche plus vite.
const loadOpening = () => import("./pages/Opening");
const Opening = lazy(() => loadOpening().then((m) => ({ default: m.Opening })));
const Collection = lazy(() => import("./pages/Collection").then((m) => ({ default: m.Collection })));
const Market = lazy(() => import("./pages/Market").then((m) => ({ default: m.Market })));
const Transparency = lazy(() => import("./pages/Transparency").then((m) => ({ default: m.Transparency })));
const Legal = lazy(() => import("./pages/Legal").then((m) => ({ default: m.Legal })));

export function App() {
  const { path, params } = useRoute();
  const [opening, setOpening] = useState<OpeningRequest | null>(null);

  // L'écran d'ouverture est préchargé dès l'arrivée : il doit démarrer à la signature, sans attente.
  useEffect(() => {
    const t = setTimeout(() => void loadOpening(), 800);
    return () => clearTimeout(t);
  }, []);

  // Lien direct vers le rejeu d'une ouverture : #/open?pack=12
  const replay = path === "/open" && params.get("pack") != null ? Number(params.get("pack")) : null;
  const request = opening ?? (replay != null && Number.isFinite(replay) ? { kind: "replay" as const, packId: replay } : null);

  const close = () => {
    setOpening(null);
    if (replay != null) window.location.hash = "/collection";
  };

  let page;
  if (path.startsWith("/collection")) page = <Collection onReplay={(id) => setOpening({ kind: "replay", packId: id })} />;
  else if (path.startsWith("/market")) page = <Market />;
  else if (path.startsWith("/rates")) page = <Transparency />;
  else if (path.startsWith("/legal")) page = <Legal />;
  else page = <Shop onBuy={(series) => setOpening({ kind: "buy", series })} />;

  return (
    <div className="app">
      <DemoBanner />
      <Header />
      <main className="main">
        <Suspense fallback={<p className="muted">Loading…</p>}>{page}</Suspense>
      </main>
      <footer className="footer">
        <span>{BRAND} · NEAR testnet demo</span>
        <a href="#/rates">Odds</a>
        <a href="#/legal">Legal notice</a>
      </footer>
      <AnimatePresence>
        {request && (
          <motion.div className="overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Suspense fallback={<div className="opening opening--loading"><div className="opening__bg" /></div>}>
              <Opening key={request.kind === "replay" ? `r${request.packId}` : "buy"} request={request} onClose={close} />
            </Suspense>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
