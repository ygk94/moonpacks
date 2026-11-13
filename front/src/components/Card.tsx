// Carte : visuel généré par art/, cadre et effets selon la rareté, inclinaison 3D au survol.
// Mythique : toujours la carte « ? » (même image, même nom, même description pour les 3).

import { useRef, type CSSProperties, type PointerEvent } from "react";
import { cardImage } from "../lib/catalog";
import type { Rarity } from "../near/types";

interface Props {
  cardId: string | null;
  rarity: Rarity;
  title?: string;
  burnable?: boolean;
  size?: "sm" | "md" | "lg";
  tilt?: boolean;
  onClick?: () => void;
  badge?: string;
  dimmed?: boolean;
}

export function Card({ cardId, rarity, title, burnable, size = "md", tilt = true, onClick, badge, dimmed }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const mythic = rarity === "mythic";
  const src = cardImage(mythic ? null : cardId);
  const label = mythic ? "?" : (title ?? cardId ?? "?");

  const move = (e: PointerEvent<HTMLDivElement>) => {
    if (!tilt || !ref.current || e.pointerType === "touch") return;
    const r = ref.current.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    ref.current.style.setProperty("--rx", `${(0.5 - y) * 14}deg`);
    ref.current.style.setProperty("--ry", `${(x - 0.5) * 18}deg`);
    ref.current.style.setProperty("--mx", `${x * 100}%`);
    ref.current.style.setProperty("--my", `${y * 100}%`);
  };
  const leave = () => {
    ref.current?.style.setProperty("--rx", "0deg");
    ref.current?.style.setProperty("--ry", "0deg");
  };

  return (
    <div
      ref={ref}
      className={`card card--${size} rarity-${rarity}${onClick ? " card--clickable" : ""}${dimmed ? " card--dimmed" : ""}`}
      onPointerMove={move}
      onPointerLeave={leave}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={(e) => onClick && (e.key === "Enter" || e.key === " ") && onClick()}
      aria-label={`${label}, ${rarity}${burnable ? ", burnable" : ""}`}
      style={{ "--rx": "0deg", "--ry": "0deg" } as CSSProperties}
    >
      <div className="card__inner">
        <img className="card__img" src={src} alt="" loading="lazy" draggable={false} />
        <div className="card__sheen" aria-hidden />
        {(rarity === "legendary" || rarity === "mythic") && <div className="card__sparkles" aria-hidden />}
        {burnable && <span className="card__chip card__chip--burn">🔥 Burnable</span>}
        {badge && <span className="card__chip card__chip--badge">{badge}</span>}
      </div>
    </div>
  );
}

/** Dos neutre d'une carte avant révélation (sans rien qui trahisse la rareté). */
export function CardBack({ size = "md", glow }: { size?: "sm" | "md" | "lg"; glow?: Rarity | null }) {
  return (
    <div className={`card card--${size} card-back${glow ? ` card-back--glow rarity-${glow}` : ""}`}>
      <div className="card__inner card-back__inner">
        <div className="card-back__pattern" />
        <div className="card-back__logo">
          <span>M</span>
          <small>MOONPACKS</small>
        </div>
      </div>
    </div>
  );
}
