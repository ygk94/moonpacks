// Vérification d'un tirage dans le navigateur, à partir de données publiques seulement.
//
// Reprend verifier/memaster_verifier/core.py (lui-même calqué sur contract/src/draw.rs), niveau « sans état »
// (`--no-state`) :
//   1. table : sha256(serde_json(table)) = hash enregistré (la sérialisation JSON du navigateur est celle de
//      serde_json pour ces types : mêmes champs dans le même ordre, mêmes échappements) ;
//   2. graines : initial_acc = sha256("memaster:pack" ‖ pack_id_le ‖ owner ‖ table_hash), puis
//      acc = sha256(acc ‖ seed ‖ pack_id_le ‖ owner) pour chaque graine, jusqu'à l'acc final ;
//   3. chaque emplacement : rarity_roll = roll(acc, slot, 0) mod Σpoids, rareté visée, retombée cohérente,
//      rareté de la carte tirée = rareté finale ;
//   4. valeur du pack : value_roll = roll(acc, 0, 3) mod Σpoids des paliers, palier et points de base.
// Le choix exact de la carte (card_roll) dépend des compteurs de la série au moment du tirage, et le passage en
// gold pack d'un historique par compte : ils demandent tout l'historique, donc le vérificateur en ligne de commande.

export const RARITIES = ["mythic", "legendary", "epic", "rare", "common"] as const;
export type R = (typeof RARITIES)[number];
type Weights = Record<R, number>;

export interface TableCard {
  card_id: string;
  rarity: R;
}

export interface Table {
  price: string;
  cards_per_pack: number;
  rarity_weights: Weights;
  cards: TableCard[];
  mechanics?: {
    gold?: { slots: { floor: R; weights: Weights | null; burnable: boolean }[] } | null;
    rush?: { weights: Weights } | null;
    value?: { normal: [number, number][]; gold: [number, number][]; rush: [number, number][] } | null;
  } | null;
}

export interface PackInput {
  pack_id: number;
  owner_id: string;
  acc: string;
  mode?: "base" | "gold" | "rush";
  seeds: { seed: string }[];
  draws: { slot: number; rarity_roll: string; rolled_rarity: R; final_rarity: R; kind: "visible" | "mythic"; index: number }[];
  value?: { bps: number } | null;
}

export interface Check {
  label: string;
  ok: boolean;
  detail?: string;
}

const enc = new TextEncoder();

export function hex(b: Uint8Array): string {
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

export function unhex(s: string): Uint8Array {
  if (!/^[0-9a-f]*$/i.test(s) || s.length % 2) throw new Error(`invalid hex: ${s}`);
  const out = new Uint8Array(s.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(s.slice(2 * i, 2 * i + 2), 16);
  return out;
}

function concat(...parts: Uint8Array[]): Uint8Array<ArrayBuffer> {
  const out = new Uint8Array(parts.reduce((n, p) => n + p.length, 0));
  let o = 0;
  for (const p of parts) {
    out.set(p, o);
    o += p.length;
  }
  return out;
}

export async function sha256(...parts: Uint8Array[]): Promise<Uint8Array> {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", concat(...parts)));
}

function u64le(n: number): Uint8Array {
  const b = new Uint8Array(8);
  let v = BigInt(n);
  for (let i = 0; i < 8; i++) {
    b[i] = Number(v & 0xffn);
    v >>= 8n;
  }
  return b;
}

export async function tableHash(table: unknown): Promise<string> {
  return hex(await sha256(enc.encode(JSON.stringify(table))));
}

export async function initialAcc(packId: number, owner: string, tableHashHex: string): Promise<Uint8Array> {
  return sha256(enc.encode("memaster:pack"), u64le(packId), enc.encode(owner), unhex(tableHashHex));
}

export async function mix(acc: Uint8Array, seed: Uint8Array, packId: number, owner: string): Promise<Uint8Array> {
  return sha256(acc, seed, u64le(packId), enc.encode(owner));
}

/** `roll(acc, slot, tag)` : 16 premiers octets de sha256(acc ‖ slot ‖ tag), en grand-boutiste. */
export async function roll(acc: Uint8Array, slot: number, tag: number): Promise<bigint> {
  const h = await sha256(acc, new Uint8Array([slot & 0xff, tag & 0xff]));
  return BigInt("0x" + hex(h.slice(0, 16)));
}

const total = (w: Weights) => RARITIES.reduce((s, r) => s + BigInt(w[r]), 0n);

export function rarityFromRoll(w: Weights, r: bigint): R {
  let cum = 0n;
  for (const k of RARITIES) {
    cum += BigInt(w[k]);
    if (r < cum) return k;
  }
  return "common";
}

function goldSlotWeights(base: Weights, s: { floor: R; weights: Weights | null }): Weights {
  if (s.weights) return s.weights;
  const f = RARITIES.indexOf(s.floor);
  return Object.fromEntries(RARITIES.map((r, i) => [r, i <= f ? base[r] : 0])) as Weights;
}

/** Ordre de retombée : visée, vers le bas jusqu'au plancher, vers le haut, puis sous le plancher. */
export function fallbackOrder(rolled: R, floor: R): R[] {
  const f = RARITIES.indexOf(floor);
  const r = Math.min(RARITIES.indexOf(rolled), f);
  const out: R[] = [];
  for (let i = r; i <= f; i++) out.push(RARITIES[i]);
  for (let i = r - 1; i >= 0; i--) out.push(RARITIES[i]);
  for (let i = f + 1; i < 5; i++) out.push(RARITIES[i]);
  return out;
}

/** Règle (poids, plancher) de chaque emplacement pour le mode du pack. */
function slotRules(t: Table, mode: string): { weights: Weights; floor: R; rule: boolean }[] {
  const m = t.mechanics ?? {};
  if (mode === "gold" && m.gold) {
    return m.gold.slots.map((s) => ({ weights: goldSlotWeights(t.rarity_weights, s), floor: s.floor, rule: true }));
  }
  const w = mode === "rush" && m.rush ? m.rush.weights : t.rarity_weights;
  const last = !!m.value;
  return Array.from({ length: t.cards_per_pack }, (_, i) => ({ weights: w, floor: "common" as R, rule: last && i === t.cards_per_pack - 1 }));
}

export async function verifyPack(table: Table, storedTableHash: string, pack: PackInput): Promise<Check[]> {
  const checks: Check[] = [];
  const computed = await tableHash(table);
  checks.push({
    label: "Rate table matches the hash frozen on-chain",
    ok: computed === storedTableHash,
    detail: computed,
  });

  let acc = await initialAcc(pack.pack_id, pack.owner_id, storedTableHash);
  for (const s of pack.seeds) acc = await mix(acc, unhex(s.seed), pack.pack_id, pack.owner_id);
  checks.push({
    label: `Random seeds (${pack.seeds.length}) chain to the final draw state`,
    ok: hex(acc) === pack.acc,
    detail: hex(acc),
  });

  const mode = pack.mode ?? "base";
  const rules = slotRules(table, mode);
  const rulesOk = rules.length === pack.draws.length;
  checks.push({ label: `Pack type “${mode}” has ${rules.length} slots`, ok: rulesOk });

  for (const d of pack.draws) {
    const rule = rules[d.slot];
    if (!rule) continue;
    const rr = (await roll(acc, d.slot, 0)) % (total(rule.weights) || 1n);
    const rolled = rarityFromRoll(rule.weights, rr);
    const order = rule.rule ? fallbackOrder(rolled, rule.floor) : RARITIES.slice(RARITIES.indexOf(rolled));
    const card = d.kind === "visible" ? table.cards[d.index] : null;
    const ok =
      rr.toString() === d.rarity_roll &&
      rolled === d.rolled_rarity &&
      order.includes(d.final_rarity) &&
      (d.kind === "mythic" ? d.final_rarity === "mythic" : card?.rarity === d.final_rarity);
    checks.push({
      label: `Slot ${d.slot + 1}: rarity roll gives ${rolled}${d.final_rarity !== rolled ? `, falls back to ${d.final_rarity}` : ""}`,
      ok,
    });
  }

  const v = table.mechanics?.value;
  if (v && pack.value) {
    const tiers = mode === "base" ? v.normal : v[mode];
    const sum = tiers.reduce((s, [, w]) => s + BigInt(w), 0n) || 1n;
    const r = (await roll(acc, 0, 3)) % sum;
    let cum = 0n;
    let bps = tiers[0]?.[0] ?? 0;
    for (const [b, w] of tiers) {
      cum += BigInt(w);
      if (r < cum) {
        bps = b;
        break;
      }
    }
    checks.push({ label: "Tokens locked in the pack follow the published value table", ok: bps === pack.value.bps });
  }
  return checks;
}
