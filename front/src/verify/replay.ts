// Vérification complète d'un tirage : rejeu de toute la série depuis son ouverture, à partir des événements seuls.
//
// Portage de verifier/memaster_verifier (core.py : draw_pack_mech, burn_factors, rush_on_buy, pity_is_gold,
// split_value ; verify.py : SeriesReplay, verify_pack, verify_mechanics, verify_value), lui-même calqué sur
// contract/src/draw.rs. Les événements viennent de l'indexeur, dans l'ordre d'exécution.
// Les poids sont en BigInt : un poids renormalisé (poids brut × somme des poids) dépasse 2⁵³.
//
// Rien de ce module n'est affiché tel quel au joueur hormis les libellés des contrôles, qui ne donnent jamais
// la valeur du compteur de pitié (consigne : pas de compteur de pitié visible).

import { hex, initialAcc, mix, RARITIES, roll, unhex, type Check, type R } from "./verify";

type Weights = Record<R, number>;

export interface FullCard {
  card_id: string;
  rarity: R;
  weight: number;
  cap: number | null;
  backing: unknown | null;
}

export interface FullTable {
  price: string;
  cards_per_pack: number;
  rarity_weights: Weights;
  cards: FullCard[];
  mythics: { weight: number; cap: number | null }[];
  mechanics?: {
    gold?: { slots: { floor: R; weights: Weights | null; burnable: boolean }[] } | null;
    pity?: { p0_ppb: number; k_ppb: number; p_max_ppb: number; n_max: number | null } | null;
    burn?: { floor_bps: number; prior_k: number } | null;
    rush?: RushParams | null;
    resurrection?: { eligible: number[] } | null;
    value?: { normal: [number, number][]; gold: [number, number][]; rush: [number, number][]; multipliers: Weights } | null;
  } | null;
  /** Types de packs (packs thématiques) de la série, tirés dans la même table (contract/src/types.rs, PackKind). */
  kinds?: PackKindDef[] | null;
  /** Vue d'un type de pack (`kindTable`) : règles par emplacement et mythiques autorisées. */
  _kindSlots?: { floor: R; weights: Weights | null; burnable: boolean }[] | null;
  _kindMythics?: boolean;
}

export interface PackKindDef {
  name: string;
  price: string;
  cards_per_pack: number;
  pool: number[];
  mythics: boolean;
  slots: { floor: R; weights: Weights | null; burnable: boolean }[] | null;
  value: boolean;
}

/**
 * Table vue par un pack d'un type, comme `draw::draw_pack_mech` avec `kind` (et `core.kind_table` du
 * vérificateur Python) : poids à 0 hors du `pool`, mythiques de poids 0 si le type les exclut, taille et
 * prix du type, ni gold pack ni pitié, valeur seulement si `value`. `kind` nul : la table telle quelle.
 */
export function kindTable(t: FullTable, kind: number | null | undefined): FullTable {
  if (kind == null) return t;
  const k = t.kinds?.[kind];
  if (!k) throw new Error(`unknown pack type ${kind}`);
  const pool = new Set(k.pool);
  const noMyth = (w: Weights): Weights => (k.mythics ? w : { ...w, mythic: 0 });
  const m = t.mechanics ? { ...t.mechanics } : null;
  if (m) {
    m.gold = null;
    m.pity = null;
    if (!k.value) m.value = null;
    if (m.rush) m.rush = { ...m.rush, weights: noMyth(m.rush.weights) };
  }
  return {
    ...t,
    price: k.price,
    cards_per_pack: k.cards_per_pack,
    rarity_weights: noMyth(t.rarity_weights),
    cards: t.cards.map((c, i) => (pool.size === 0 || pool.has(i) ? c : { ...c, weight: 0 })),
    mythics: k.mythics ? t.mythics : t.mythics.map((mc) => ({ ...mc, weight: 0 })),
    mechanics: m,
    _kindSlots: k.slots,
    _kindMythics: k.mythics,
  };
}

export interface RushParams {
  ratio_bps: number;
  min_packs: number;
  window_blocks: number;
  baseline_blocks: number;
  bucket_blocks: number;
  duration_blocks: number;
  cooldown_blocks: number;
  max_per_account: number;
  weights: Weights;
}

export interface ChainEvent {
  event: string;
  data: Record<string, any>; // eslint-disable-line @typescript-eslint/no-explicit-any
}

interface Draw {
  slot: number;
  rarity_roll: string;
  rolled_rarity: R;
  final_rarity: R;
  card_roll: string;
  kind: "visible" | "mythic";
  index: number;
}

const PPB = 1_000_000_000n;
const U32_MAX = 4294967295;
const big = (n: number | bigint) => BigInt(n);
const rIndex = (r: R) => RARITIES.indexOf(r);

// --- Poids et burns (core.py) --------------------------------------------------------------------

function available(w: number, minted: number, cap: number | null): bigint {
  return w === 0 || (cap != null && minted >= cap) ? 0n : big(w);
}

export interface Burn {
  burned: number[];
  backed: boolean[];
  floorBps: number;
  priorK: number;
  resurrectable: Set<number>;
}

const isResurrected = (b: Burn, i: number) => b.backed[i] && b.resurrectable.has(i);
const floorWeight = (w: number, floorBps: number) => {
  const f = (big(w) * big(floorBps)) / 10_000n;
  return f > 1n ? f : 1n;
};

function rawBurnWeight(w: number, minted: number, burned: number, cap: number | null, floorBps: number, priorK: number): bigint {
  if (w === 0 || (cap != null && minted >= cap)) return 0n;
  if (minted === 0) return big(w);
  const circ = big(Math.max(minted - burned, 0) + priorK);
  const v = (big(w) * circ) / big(minted + priorK);
  const f = floorWeight(w, floorBps);
  return v > f ? v : f;
}

function burnableRaw(t: FullTable, i: number, minted: number, b: Burn, e0: bigint, b0: bigint): bigint {
  const c = t.cards[i];
  const own = rawBurnWeight(c.weight, minted, b.burned[i], c.cap, b.floorBps, b.priorK);
  if (own === 0n || b0 === 0n || !isResurrected(b, i)) return own;
  let avg = (big(c.weight) * e0) / b0;
  const f = floorWeight(c.weight, b.floorBps);
  if (avg < f) avg = f;
  return own < avg ? own : avg;
}

interface Factors {
  e: bigint;
  b: bigint;
  e0: bigint;
  b0: bigint;
}

function burnFactors(t: FullTable, minted: number[], b: Burn, rarity: R): Factors {
  let e0 = 0n;
  let b0 = 0n;
  t.cards.forEach((c, i) => {
    if (c.rarity !== rarity || !b.backed[i] || isResurrected(b, i)) return;
    e0 += rawBurnWeight(c.weight, minted[i], b.burned[i], c.cap, b.floorBps, b.priorK);
    b0 += available(c.weight, minted[i], c.cap);
  });
  let e = e0;
  let bb = b0;
  t.cards.forEach((c, i) => {
    if (c.rarity !== rarity || !isResurrected(b, i)) return;
    e += burnableRaw(t, i, minted[i], b, e0, b0);
    bb += available(c.weight, minted[i], c.cap);
  });
  return { e, b: bb, e0, b0 };
}

function inRarityWeight(t: FullTable, i: number, minted: number, b: Burn, f: Factors): bigint {
  const c = t.cards[i];
  if (b.backed[i]) return f.e === 0n ? 0n : burnableRaw(t, i, minted, b, f.e0, f.b0) * f.b;
  const a = available(c.weight, minted, c.cap);
  return f.e === 0n ? a : a * f.e;
}

function availableWeight(t: FullTable, minted: number[], mm: number[], burn: Burn | null, rarity: R): bigint {
  if (rarity === "mythic") {
    let s = 0n;
    for (let j = 0; j < Math.min(t.mythics.length, mm.length); j++) s += available(t.mythics[j].weight, mm[j], t.mythics[j].cap);
    return s;
  }
  if (!burn) {
    let s = 0n;
    t.cards.forEach((c, i) => {
      if (c.rarity === rarity) s += available(c.weight, minted[i], c.cap);
    });
    return s;
  }
  const f = burnFactors(t, minted, burn, rarity);
  let s = 0n;
  t.cards.forEach((c, i) => {
    if (c.rarity === rarity) s += inRarityWeight(t, i, minted[i], burn, f);
  });
  return s;
}

function burnableWeight(t: FullTable, minted: number[], backed: boolean[], burn: Burn | null, rarity: R): bigint {
  if (rarity === "mythic") return 0n;
  const f = burn ? burnFactors(t, minted, burn, rarity) : null;
  let s = 0n;
  t.cards.forEach((c, i) => {
    if (c.rarity !== rarity || !backed[i]) return;
    s += burn && f ? inRarityWeight(t, i, minted[i], burn, f) : available(c.weight, minted[i], c.cap);
  });
  return s;
}

// --- Tirage d'un emplacement ---------------------------------------------------------------------

function rarityFromRoll(w: Weights, r: bigint): R {
  let cum = 0n;
  for (const k of RARITIES) {
    cum += big(w[k]);
    if (r < cum) return k;
  }
  return "common";
}

function fallbackOrder(rolled: R, floor: R): R[] {
  const f = rIndex(floor);
  const r = Math.min(rIndex(rolled), f);
  const out: R[] = [];
  for (let i = r; i <= f; i++) out.push(RARITIES[i]);
  for (let i = r - 1; i >= 0; i--) out.push(RARITIES[i]);
  for (let i = f + 1; i < 5; i++) out.push(RARITIES[i]);
  return out;
}

function firstUnlimitedCommon(t: FullTable): number {
  const i = t.cards.findIndex((c) => c.rarity === "common" && c.cap == null && c.weight > 0);
  return i < 0 ? 0 : i;
}

const total = (w: Weights) => RARITIES.reduce((s, r) => s + big(w[r]), 0n);

async function drawSlot(
  t: FullTable,
  minted: number[],
  mm: number[],
  acc: Uint8Array,
  slot: number,
  weights: Weights,
  rule: { floor: R; burnableOnly: boolean; ruled: boolean },
  backed: boolean[],
  burn: Burn | null,
): Promise<Draw> {
  const tot = total(weights) || 1n;
  const rarityRoll = (await roll(acc, slot, 0)) % tot;
  const rolled = rarityFromRoll(weights, rarityRoll);
  const avail = (r: R) => (rule.burnableOnly ? burnableWeight(t, minted, backed, burn, r) : availableWeight(t, minted, mm, burn, r));

  let final: R = rolled;
  let s = 0n;
  if (rule.ruled) {
    final = "common";
    for (const r of fallbackOrder(rolled, rule.floor)) {
      const a = avail(r);
      if (a > 0n) {
        final = r;
        s = a;
        break;
      }
    }
  } else {
    // Retombée sur la rareté inférieure tant que la rareté est épuisée.
    s = avail(final);
    while (s === 0n) {
      const i = rIndex(final);
      if (i + 1 >= RARITIES.length) break;
      final = RARITIES[i + 1];
      s = avail(final);
    }
  }
  const raw = await roll(acc, slot, 1);
  const cardRoll = s === 0n ? 0n : raw % s;

  if (final === "mythic" && s > 0n) {
    let c = 0n;
    let pick = 0;
    for (let j = 0; j < Math.min(t.mythics.length, mm.length); j++) {
      c += available(t.mythics[j].weight, mm[j], t.mythics[j].cap);
      if (cardRoll < c) {
        pick = j;
        break;
      }
    }
    return { slot, rarity_roll: rarityRoll.toString(), rolled_rarity: rolled, final_rarity: final, card_roll: cardRoll.toString(), kind: "mythic", index: pick };
  }
  let c = 0n;
  let pick = firstUnlimitedCommon(t);
  const f = burn ? burnFactors(t, minted, burn, final) : null;
  for (let i = 0; i < t.cards.length; i++) {
    const card = t.cards[i];
    if (card.rarity !== final || (rule.burnableOnly && !backed[i])) continue;
    c += burn && f ? inRarityWeight(t, i, minted[i], burn, f) : available(card.weight, minted[i], card.cap);
    if (cardRoll < c) {
      pick = i;
      break;
    }
  }
  return { slot, rarity_roll: rarityRoll.toString(), rolled_rarity: rolled, final_rarity: final, card_roll: cardRoll.toString(), kind: "visible", index: pick };
}

function goldSlotWeights(base: Weights, s: { floor: R; weights: Weights | null }): Weights {
  if (s.weights) return s.weights;
  const f = rIndex(s.floor);
  return Object.fromEntries(RARITIES.map((r, i) => [r, i <= f ? base[r] : 0])) as Weights;
}

export async function drawPackMech(t: FullTable, minted: number[], mm: number[], acc: Uint8Array, mode: string, burn: Burn | null, backed: boolean[]) {
  const m = t.mechanics ?? {};
  const gold = mode === "gold" ? m.gold : null;
  const weights = mode === "rush" && m.rush ? m.rush.weights : t.rarity_weights;
  const rules = t._kindSlots ?? null;
  const n = gold ? gold.slots.length : t.cards_per_pack;
  const out: Draw[] = [];
  for (let slot = 0; slot < n; slot++) {
    let d: Draw;
    if (gold) {
      const gs = gold.slots[slot];
      d = await drawSlot(t, minted, mm, acc, slot, goldSlotWeights(t.rarity_weights, gs), { floor: gs.floor, burnableOnly: gs.burnable, ruled: true }, backed, burn);
    } else if (rules) {
      const rule = rules[slot];
      let w = goldSlotWeights(weights, rule);
      if (t._kindMythics === false) w = { ...w, mythic: 0 };
      d = await drawSlot(t, minted, mm, acc, slot, w, { floor: rule.floor, burnableOnly: rule.burnable, ruled: true }, backed, burn);
    } else if (m.value && slot === n - 1) {
      d = await drawSlot(t, minted, mm, acc, slot, weights, { floor: "common", burnableOnly: true, ruled: true }, backed, burn);
    } else {
      d = await drawSlot(t, minted, mm, acc, slot, weights, { floor: "common", burnableOnly: false, ruled: false }, backed, burn);
    }
    if (d.kind === "visible") minted[d.index] += 1;
    else mm[d.index] += 1;
    out.push(d);
  }
  return out;
}

// --- Gold rush, pitié, valeur ------------------------------------------------------------------

export interface RushState {
  ring: [number | null, number][];
  start: number | null;
  lastTrigger: number | null;
}

export function rushOnBuy(p: RushParams, st: RushState, h: number) {
  const bsz = Math.max(p.bucket_blocks, 1);
  const ml = Math.max(Math.floor(p.baseline_blocks / bsz), 1);
  const mw = Math.min(Math.max(Math.floor(p.window_blocks / bsz), 1), ml);
  if (st.ring.length !== ml) st.ring = Array.from({ length: ml }, () => [null, 0] as [number | null, number]);
  if (st.start == null) st.start = h;
  const t = st.lastTrigger;
  const active = t != null && h <= t + p.duration_blocks && h > t;
  const paused = t != null && h <= t + p.duration_blocks + p.cooldown_blocks;
  const b = Math.floor(h / bsz);
  const e = st.ring[b % ml];
  if (e[0] !== b) {
    e[0] = b;
    e[1] = 0;
  }
  e[1] += 1;
  const count = (m: number) => st.ring.reduce((s, [bb, c]) => (bb != null && bb <= b && b - bb < m ? s + c : s), 0);
  const cw = count(mw);
  const cl = count(ml);
  const triggered =
    !paused && h >= st.start + p.baseline_blocks && cw >= p.min_packs && big(cw) * big(ml) * 10_000n >= big(p.ratio_bps) * big(cl) * big(mw);
  if (triggered) st.lastTrigger = h;
  return { active, window_count: cw, baseline_count: cl, triggered };
}

export function rushAccount(p: RushParams, active: boolean, trigger: number | null, prev: [number, number] | undefined) {
  if (!active || trigger == null) return { rush: false, capped: false, entry: prev };
  const n = prev && prev[0] === trigger ? prev[1] : 0;
  if (n >= p.max_per_account) return { rush: false, capped: true, entry: [trigger, n] as [number, number] };
  return { rush: true, capped: false, entry: [trigger, n + 1] as [number, number] };
}

export function splitValue(totalV: bigint, slots: [R, boolean][], mult: Weights): (string | null)[] {
  const s = slots.reduce((a, [r, b]) => (b ? a + big(mult[r]) : a), 0n);
  if (s === 0n) return slots.map(() => null);
  const out = slots.map(([r, b]) => (b ? (totalV * big(mult[r])) / s : null));
  let best = -1;
  slots.forEach(([r, b], i) => {
    if (b && (best < 0 || mult[r] > mult[slots[best][0]])) best = i;
  });
  const used = out.reduce<bigint>((a, x) => (x == null ? a : a + x), 0n);
  out[best] = (out[best] as bigint) + (totalV - used);
  return out.map((x) => (x == null ? null : x.toString()));
}

// --- Rejeu de la série -------------------------------------------------------------------------

export interface PackReport {
  packId: number;
  checks: Check[];
}

/**
 * Rejoue `events` (pack_bought, pack_revealed, card_redeemed, card_resurrected) dans l'ordre d'exécution et
 * renvoie le rapport de chaque booster. `tableHashHex` : hash enregistré on-chain (déjà vérifié à part).
 */
export async function replaySeries(t: FullTable, tableHashHex: string, events: ChainEvent[], onlyPack?: number): Promise<PackReport[]> {
  const mech = t.mechanics ?? null;
  const minted = t.cards.map(() => 0);
  const mm = t.mythics.map(() => 0);
  const pity = new Map<string, number>();
  const burned = t.cards.map(() => 0);
  let burnSeq = 0;
  const backed = t.cards.map((c) => c.backing != null);
  let resurrectSeq = 0;
  const pendingBurns = new Map<number, number>();
  const pendingRes = new Map<number, number>();
  const rushState: RushState = { ring: [], start: null, lastTrigger: null };
  const rushOf = new Map<number, boolean>();
  const rushAccounts = new Map<string, [number, number]>();
  const resurrectable = new Set(mech?.resurrection?.eligible ?? []);
  const reports: PackReport[] = [];

  for (const { event, data } of events) {
    if (event === "pack_bought" && mech?.rush) {
      const o = rushOnBuy(mech.rush, rushState, Number(data.block_height));
      const owner = String(data.owner_id);
      const prev = o.active ? rushAccounts.get(owner) : undefined;
      const a = rushAccount(mech.rush, o.active, rushState.lastTrigger, prev);
      if (a.rush && a.entry) rushAccounts.set(owner, a.entry);
      rushOf.set(Number(data.pack_id), a.rush);
    } else if (event === "card_redeemed") {
      if (data.burn_seq != null && data.kind === "visible") pendingBurns.set(Number(data.burn_seq), Number(data.index));
    } else if (event === "card_resurrected") {
      if (data.previous == null) pendingRes.set(Number(data.resurrect_seq), Number(data.card_index));
    } else if (event === "pack_revealed") {
      const em = data.mechanics ?? {};
      const checks: Check[] = [];
      const missing: string[] = [];
      // Burns et résurrections appliqués jusqu'aux numéros journalisés.
      const wantBurn = mech?.burn ? em.burn_seq : null;
      while (wantBurn != null && burnSeq < wantBurn) {
        const i = pendingBurns.get(burnSeq + 1);
        if (i == null) {
          missing.push(`burn #${burnSeq + 1}`);
          break;
        }
        pendingBurns.delete(burnSeq + 1);
        burned[i] += 1;
        burnSeq += 1;
      }
      while (em.resurrect_seq != null && resurrectSeq < em.resurrect_seq) {
        const i = pendingRes.get(resurrectSeq + 1);
        if (i == null) {
          missing.push(`resurrection #${resurrectSeq + 1}`);
          break;
        }
        pendingRes.delete(resurrectSeq + 1);
        backed[i] = true;
        resurrectSeq += 1;
      }
      const burn: Burn | null = mech?.burn
        ? { burned: [...burned], backed: [...backed], floorBps: mech.burn.floor_bps, priorK: mech.burn.prior_k, resurrectable }
        : null;

      const report = onlyPack == null || Number(data.pack_id) === onlyPack;
      if (report) {
        // Le drapeau rush est figé à l'achat : sans le `pack_bought`, il n'est pas vérifiable (pas cru sur parole).
        if (mech?.rush && !rushOf.has(Number(data.pack_id))) missing.push("purchase event");
        if (missing.length) checks.push({ label: `Complete history (missing: ${missing.join(", ")})`, ok: false });
        checks.push(...(await checkPack(t, tableHashHex, data, minted, mm, burn, [...backed], {
          // Un type de pack n'a ni pitié ni gold pack.
          pityBefore: mech?.pity && data.kind == null ? (pity.get(String(data.owner_id)) ?? 0) : null,
          rush: mech?.rush ? (rushOf.has(Number(data.pack_id)) ? rushOf.get(Number(data.pack_id))! : null) : null,
          burnSeq: mech?.burn ? burnSeq : null,
          resurrectSeq,
        })));
        reports.push({ packId: Number(data.pack_id), checks });
      }
      // On avance avec les cartes journalisées, pour isoler une éventuelle erreur.
      for (const d of data.draws as Draw[]) {
        if (d.kind === "visible") minted[d.index] += 1;
        else mm[d.index] += 1;
      }
      if (mech?.pity && data.kind == null && Number.isInteger(em.pity?.after)) pity.set(String(data.owner_id), em.pity.after);
      if (onlyPack != null && Number(data.pack_id) === onlyPack) break;
    }
  }
  return reports;
}

async function checkPack(
  t: FullTable,
  tableHashHex: string,
  ev: Record<string, any>, // eslint-disable-line @typescript-eslint/no-explicit-any
  minted: number[],
  mm: number[],
  burn: Burn | null,
  backed: boolean[],
  exp: { pityBefore: number | null; rush: boolean | null; burnSeq: number | null; resurrectSeq: number },
): Promise<Check[]> {
  const checks: Check[] = [];
  const add = (label: string, ok: boolean) => (checks.push({ label, ok }), ok);
  if (!add("Draw used the published rate table", ev.table_hash === tableHashHex)) return checks;

  let acc = await initialAcc(Number(ev.pack_id), String(ev.owner_id), tableHashHex);
  let chain = hex(acc) === ev.initial_acc;
  for (const s of ev.seeds ?? []) {
    acc = await mix(acc, unhex(s.seed), Number(ev.pack_id), String(ev.owner_id));
    chain &&= hex(acc) === s.acc;
  }
  if (!add(`Random seeds (${(ev.seeds ?? []).length}) chain to the final draw state`, chain && hex(acc) === ev.acc)) return checks;

  // Pack d'un type (pack thématique) : tirage dans la vue de la table propre à ce type.
  if (ev.kind != null) {
    const known = ev.kind >= 0 && ev.kind < (t.kinds?.length ?? 0);
    if (!add(`Themed pack: ${known ? t.kinds![ev.kind].name : ev.kind}`, known)) return checks;
    t = kindTable(t, ev.kind);
  }
  const m = t.mechanics ?? null;
  const em = ev.mechanics ?? {};
  const rushFlag = !!em.rush;
  if (exp.rush != null) add("Gold rush status frozen at purchase", rushFlag === exp.rush);
  let goldDecision = false;
  if (m?.pity) {
    const pe = em.pity ?? {};
    const n = pe.before;
    if (exp.pityBefore != null && n !== exp.pityBefore) add("Gold pack odds replayed from history", false);
    else if (Number.isInteger(n)) {
      const r = (await roll(acc, 0, 2)) % PPB;
      const p = Math.min(m.pity.p_max_ppb, m.pity.p0_ppb + m.pity.k_ppb * n, Number(PPB));
      const guaranteed = m.pity.n_max != null && Math.min(n + 1, U32_MAX) >= m.pity.n_max;
      goldDecision = guaranteed || r < big(p);
      const after = goldDecision ? 0 : Math.min(n + 1, U32_MAX);
      add(
        `Gold pack decision (${goldDecision ? "gold" : "not gold"}) follows the random draw`,
        pe.gold_roll === Number(r) && pe.p_ppb === p && pe.gold === goldDecision && pe.after === after,
      );
    }
  }
  const mode = goldDecision ? "gold" : rushFlag ? "rush" : "base";
  if (m) add(`Pack type: ${mode}`, em.mode === mode);
  if (exp.burnSeq != null) add("Burn history is complete", em.burn_seq === exp.burnSeq);
  if (m) add("Resurrection history is complete", (em.resurrect_seq ?? 0) === exp.resurrectSeq);

  const expected = await drawPackMech(t, [...minted], [...mm], acc, mode, burn, backed);
  const got = ev.draws as Draw[];
  add(`${expected.length} cards drawn`, got.length === expected.length);
  for (const e of expected) {
    const d = got[e.slot];
    const same =
      !!d &&
      d.rarity_roll === e.rarity_roll &&
      d.rolled_rarity === e.rolled_rarity &&
      d.final_rarity === e.final_rarity &&
      d.card_roll === e.card_roll &&
      d.kind === e.kind &&
      d.index === e.index;
    add(`Slot ${e.slot + 1}: exact card recomputed (${e.final_rarity})`, same);
  }

  const v = m?.value;
  if (v) {
    const got = em.value ?? {};
    const tiers = mode === "base" ? v.normal : v[mode as "gold" | "rush"];
    const sum = tiers.reduce((s, [, w]) => s + big(w), 0n) || 1n;
    const r = (await roll(acc, 0, 3)) % sum;
    let cum = 0n;
    let tier = 0;
    let bps = tiers[0]?.[0] ?? 0;
    for (let i = 0; i < tiers.length; i++) {
      cum += big(tiers[i][1]);
      if (r < cum) {
        tier = i;
        bps = tiers[i][0];
        break;
      }
    }
    const totalV = (BigInt(t.price) * big(bps)) / 10_000n;
    add("Locked token value follows the published value table", got.roll === Number(r) && got.tier === tier && got.bps === bps && got.total === totalV.toString());
    const slots = got && ev.draws ? (ev.draws as Draw[]).map((d) => [d.final_rarity, d.kind === "visible" && backed[d.index]] as [R, boolean]) : [];
    const amounts = splitValue(totalV, slots, v.multipliers);
    add("Value split between the burnable cards", JSON.stringify(amounts) === JSON.stringify(got.amounts) && slots.some(([, b]) => b));
  }
  return checks;
}
