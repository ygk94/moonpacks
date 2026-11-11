// Visuel de booster : une mosaïque de mèmes du catalogue sous un emballage métallisé.
// Les cartes montrées sont tirées des fiches publiques (mythiques exclues par construction).

import { useEffect, useState } from "react";
import { cardImage, loadCatalog } from "../lib/catalog";

interface Props {
  variant?: "standard" | "gold";
  seed?: number;
  label?: string;
  className?: string;
}

function pick(ids: string[], n: number, seed: number): string[] {
  // Tirage pseudo-aléatoire stable (mulberry32), pour que le visuel ne change pas à chaque rendu.
  let a = seed >>> 0;
  const rnd = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const out = new Set<string>();
  while (out.size < Math.min(n, ids.length)) out.add(ids[Math.floor(rnd() * ids.length)]);
  return [...out];
}

export function PackArt({ variant = "standard", seed = 7, label = "5 CARDS", className = "" }: Props) {
  const [ids, setIds] = useState<string[]>([]);
  useEffect(() => {
    loadCatalog().then((c) => {
      // Des coins connus de toutes les chaînes : ceux qui ont une chaîne identifiée.
      const known = Object.entries(c)
        .filter(([, e]) => e.chain)
        .map(([id]) => id);
      setIds(pick(known, 12, seed));
    });
  }, [seed]);

  return (
    <div className={`pack pack--${variant} ${className}`}>
      <div className="pack__crimp pack__crimp--top" />
      <div className="pack__body">
        <div className="pack__mosaic">
          {ids.map((id, i) => (
            <img key={id} src={cardImage(id)} alt="" style={{ animationDelay: `${i * -1.3}s` }} draggable={false} />
          ))}
        </div>
        <div className="pack__foil" />
        <div className="pack__brand">
          <span className="pack__logo">MEMASTER</span>
          <span className="pack__sub">{variant === "gold" ? "GOLD" : "MEMECOIN BOOSTER"}</span>
        </div>
        <div className="pack__count">{label}</div>
      </div>
      <div className="pack__crimp pack__crimp--bottom" />
    </div>
  );
}
