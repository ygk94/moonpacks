// Formats d'affichage : NEAR (yocto → décimal), dollars, quantités de jetons, durées.

const YOCTO = 10n ** 24n;

/** yoctoNEAR → NEAR, `digits` décimales au plus, zéros finaux retirés. */
export function formatNear(yocto: string | bigint, digits = 4): string {
  const v = BigInt(yocto);
  const whole = v / YOCTO;
  const frac = (v % YOCTO).toString().padStart(24, "0").slice(0, digits).replace(/0+$/, "");
  return frac ? `${whole}.${frac}` : whole.toString();
}

export function yoctoToNumber(yocto: string | bigint): number {
  return Number(BigInt(yocto) / 10n ** 16n) / 1e8;
}

/** NEAR décimal saisi par l'utilisateur → yoctoNEAR (chaîne). */
export function parseNear(near: string): string {
  const [w, f = ""] = near.trim().replace(",", ".").split(".");
  if (!/^\d*$/.test(w) || !/^\d*$/.test(f) || (!w && !f)) throw new Error("Invalid amount");
  return (BigInt(w || "0") * YOCTO + BigInt((f + "0".repeat(24)).slice(0, 24))).toString();
}

export function formatUsd(v: number): string {
  if (v >= 100) return `$${v.toFixed(0)}`;
  if (v >= 1) return `$${v.toFixed(2)}`;
  if (v >= 0.01) return `$${v.toFixed(3)}`;
  if (v === 0) return "$0";
  // Prix de memecoins : quelques chiffres significatifs.
  return `$${v.toPrecision(3)}`;
}

/** Quantité de jetons, compacte : 1 234 567 → « 1.23M ». */
const COMPACT = new Intl.NumberFormat("en-US", { notation: "compact", maximumSignificantDigits: 3 });
const PLAIN = new Intl.NumberFormat("en-US", { maximumSignificantDigits: 4 });

export function formatQty(v: number): string {
  if (!Number.isFinite(v)) return "—";
  if (v >= 1000) return COMPACT.format(v);
  if (v >= 1) return PLAIN.format(v);
  return v.toPrecision(3);
}

export function formatDuration(seconds: number): string {
  const s = Math.max(0, Math.round(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const r = s % 60;
  if (h) return `${h}h ${String(m).padStart(2, "0")}m`;
  if (m) return `${m}m ${String(r).padStart(2, "0")}s`;
  return `${r}s`;
}

export function shortAccount(id: string): string {
  if (/^0x[0-9a-f]{40}$/i.test(id)) return `${id.slice(0, 6)}…${id.slice(-4)}`;
  return id.length > 28 ? `${id.slice(0, 14)}…${id.slice(-10)}` : id;
}

export const RARITY_LABEL: Record<string, string> = {
  common: "Common",
  rare: "Rare",
  epic: "Epic",
  legendary: "Legendary",
  mythic: "Mythic",
};
