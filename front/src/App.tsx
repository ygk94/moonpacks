import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";
import { DemoBanner, Header } from "./components/Header";
import { useRoute } from "./lib/router";
import { Collection } from "./pages/Collection";
import { Legal } from "./pages/Legal";
import { Market } from "./pages/Market";
import { Opening, type OpeningRequest } from "./pages/Opening";
import { Shop } from "./pages/Shop";
import { Transparency } from "./pages/Transparency";

export function App() {
  const { path, params } = useRoute();
  const [opening, setOpening] = useState<OpeningRequest | null>(null);

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
      <main className="main">{page}</main>
      <footer className="footer">
        <span>Memaster · NEAR testnet demo</span>
        <a href="#/rates">Drop rates</a>
        <a href="#/legal">Legal notice</a>
      </footer>
      <AnimatePresence>
        {request && (
          <motion.div className="overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Opening key={request.kind === "replay" ? `r${request.packId}` : "buy"} request={request} onClose={close} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
