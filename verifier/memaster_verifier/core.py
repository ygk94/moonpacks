"""Réimplémentation indépendante de `contract/src/draw.rs`, du hash de table et des engagements mythiques.

Tout est calculé octet par octet comme le contrat :

- ``initial_acc = sha256("memaster:pack" || pack_id_le64 || owner_utf8 || table_hash)``
- ``mix(acc, seed) = sha256(acc || seed || pack_id_le64 || owner_utf8)``
- ``roll(acc, slot, tag) = u128_be(sha256(acc || slot_u8 || tag_u8)[0..16])``
- ``table_hash = sha256(serde_json::to_vec(table))`` (voir ``canon.py``)
- ``commitment = sha256(card_id_utf8 || sel)``, ``content_hash = sha256(json(content) || sel)``

Mécaniques (``docs/mecaniques-spec.md``), réimplémentées à part de ``draw.rs`` :

- ``gold_roll = roll(acc, 0, 2) mod 10⁹`` ; gold pack si ``gold_roll < min(p_max, p0 + k·n)`` (ppb), ou si la
  garantie optionnelle ``n_max`` est atteinte ; le compteur ne repart à 0 qu'après un gold pack (ancien format en ppm
  avec garantie à N et remise à 0 après un pack rush : encore lu, pour les séries déjà déployées) ;
- rareté pilotée par les burns : poids renormalisés entre brûlables de la rareté (``in_rarity_weight``) ;
- gold rush : ``rush_on_buy`` (palier relatif, pause, fenêtre glissante par seaux) ;
- gold pack : plancher de rareté par emplacement (``draw_slot_rule``, ``fallback_order``) ;
- valeur : ``value_roll = roll(acc, 0, 3)``, palier, ``⌊prix × V / 10⁴⌋`` réparti entre les
  brûlables au prorata des multiplicateurs (``split_value``) ; dernier emplacement d'un pack normal
  tiré parmi les brûlables.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .canon import content_json_bytes, table_json_bytes

# Ordre du contrat : de la plus haute à la plus basse. La retombée descend dans cet ordre.
RARITIES = ("mythic", "legendary", "epic", "rare", "common")


def sha256(*parts: bytes) -> bytes:
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.digest()


def u64_le(n: int) -> bytes:
    if not 0 <= n < 1 << 64:
        raise ValueError(f"pack_id hors de u64 : {n}")
    return n.to_bytes(8, "little")


def initial_acc(pack_id: int, owner: str, table_hash: bytes) -> bytes:
    return sha256(b"memaster:pack", u64_le(pack_id), owner.encode("utf-8"), table_hash)


def mix(acc: bytes, seed: bytes, pack_id: int, owner: str) -> bytes:
    if len(acc) != 32 or len(seed) != 32:
        raise ValueError("acc et seed font 32 octets")
    return sha256(acc, seed, u64_le(pack_id), owner.encode("utf-8"))


def roll(acc: bytes, slot: int, tag: int) -> int:
    h = sha256(acc, bytes([slot & 0xFF, tag & 0xFF]))
    return int.from_bytes(h[:16], "big")


def table_hash(table: dict) -> bytes:
    return sha256(table_json_bytes(table))


def mythic_commitments(card_id: str, sel: bytes, content: dict) -> tuple[bytes, bytes]:
    return sha256(card_id.encode("utf-8"), sel), sha256(content_json_bytes(content), sel)


def lower(rarity: str) -> str | None:
    i = RARITIES.index(rarity)
    return RARITIES[i + 1] if i + 1 < len(RARITIES) else None


def _available(weight: int, minted: int, cap: int | None) -> int:
    if weight == 0 or (cap is not None and minted >= cap):
        return 0
    return weight


def available_weight(table: dict, minted: list[int], mythic_minted: list[int], rarity: str) -> int:
    if rarity == "mythic":
        # zip : comme en Rust, s'arrête à la plus courte des deux listes.
        return sum(_available(m["weight"], n, m.get("cap")) for m, n in zip(table["mythics"], mythic_minted))
    return sum(
        _available(c["weight"], n, c.get("cap")) for c, n in zip(table["cards"], minted) if c["rarity"] == rarity
    )


def rarity_total(table: dict) -> int:
    return sum(table["rarity_weights"][r] for r in RARITIES)


@dataclass(frozen=True)
class SlotDraw:
    slot: int
    rarity_roll: int
    rolled_rarity: str
    final_rarity: str
    card_roll: int
    kind: str
    index: int

    def as_event(self) -> dict:
        """Mêmes clés et mêmes types que `DrawRecord` dans l'événement (sans `token_id`)."""
        return {
            "slot": self.slot,
            "rarity_roll": str(self.rarity_roll),
            "rolled_rarity": self.rolled_rarity,
            "final_rarity": self.final_rarity,
            "card_roll": str(self.card_roll),
            "kind": self.kind,
            "index": self.index,
        }


def _first_unlimited_common(table: dict) -> int:
    for i, c in enumerate(table["cards"]):
        if c["rarity"] == "common" and c.get("cap") is None and c["weight"] > 0:
            return i
    return 0


# ------------------------------------------------------------------ mécaniques

PPM = 1_000_000
PPB = 1_000_000_000
U32_MAX = (1 << 32) - 1
TAG_GOLD = 2


@dataclass(frozen=True)
class Burn:
    """État des burns pour un tirage : ``burned[i]``, ``backed[i]`` (adossée par la table ou
    ressuscitée), plancher en points de base, a priori ``K``, cartes ressuscitables de la table
    (``mechanics.resurrection.eligible``)."""

    burned: list
    backed: list
    floor_bps: int
    prior_k: int = 0
    resurrectable: tuple = ()

    def resurrected(self, i: int) -> bool:
        return self.backed[i] and i in self.resurrectable


def _floor_weight(w: int, floor_bps: int) -> int:
    return max(w * floor_bps // 10_000, 1)


def raw_burn_weight(w: int, minted: int, burned: int, cap, floor_bps: int, prior_k: int = 0) -> int:
    """``max(⌊w × (e − b + K) / (e + K)⌋, ⌊w × plancher⌋, 1)`` ; ``w`` si ``e = 0`` ; 0 si épuisée."""
    if w == 0 or (cap is not None and minted >= cap):
        return 0
    if minted == 0:
        return w
    circ = max(minted - burned, 0) + prior_k
    return max(w * circ // (minted + prior_k), _floor_weight(w, floor_bps))


@dataclass(frozen=True)
class BurnFactors:
    e: int
    b: int
    e0: int
    b0: int


def burnable_raw(table: dict, i: int, minted: int, burn: Burn, e0: int, b0: int) -> int:
    """Poids brut d'une brûlable ; une carte ressuscitée prend le ratio moyen ``e0 / b0`` des
    brûlables de la table dans sa rareté, borné par son propre poids brut."""
    c = table["cards"][i]
    own = raw_burn_weight(c["weight"], minted, burn.burned[i], c.get("cap"), burn.floor_bps, burn.prior_k)
    if own == 0 or b0 == 0 or not burn.resurrected(i):
        return own
    return min(own, max(c["weight"] * e0 // b0, _floor_weight(c["weight"], burn.floor_bps)))


def burn_factors(table: dict, minted: list[int], burn: Burn, rarity: str) -> BurnFactors:
    e0 = b0 = 0
    cards = table["cards"]
    for i, (c, n) in enumerate(zip(cards, minted)):
        if c["rarity"] != rarity or not burn.backed[i] or burn.resurrected(i):
            continue
        e0 += raw_burn_weight(c["weight"], n, burn.burned[i], c.get("cap"), burn.floor_bps, burn.prior_k)
        b0 += _available(c["weight"], n, c.get("cap"))
    e, b = e0, b0
    for i, (c, n) in enumerate(zip(cards, minted)):
        if c["rarity"] != rarity or not burn.resurrected(i):
            continue
        e += burnable_raw(table, i, n, burn, e0, b0)
        b += _available(c["weight"], n, c.get("cap"))
    return BurnFactors(e, b, e0, b0)


def in_rarity_weight(table: dict, i: int, minted: int, burn: Burn, f: BurnFactors) -> int:
    c = table["cards"][i]
    if burn.backed[i]:
        return 0 if f.e == 0 else burnable_raw(table, i, minted, burn, f.e0, f.b0) * f.b
    a = _available(c["weight"], minted, c.get("cap"))
    return a if f.e == 0 else a * f.e


def resurrectable(table: dict) -> tuple:
    r = (table.get("mechanics") or {}).get("resurrection")
    return tuple(r["eligible"]) if r else ()


def available_weight_mech(table, minted, mythic_minted, burn: Burn | None, rarity: str) -> int:
    if burn is None or rarity == "mythic":
        return available_weight(table, minted, mythic_minted, rarity)
    f = burn_factors(table, minted, burn, rarity)
    return sum(
        in_rarity_weight(table, i, n, burn, f)
        for i, (c, n) in enumerate(zip(table["cards"], minted))
        if c["rarity"] == rarity
    )


def pity_legacy(p: dict) -> bool:
    """Ancien format de pitié (ppm, garantie à N, remise à 0 après un pack rush)."""
    return "p0_ppm" in p


def pity_p(p: dict, n: int) -> int:
    """Probabilité d'un gold pack après n packs sans gold pack : ppb (ppm dans l'ancien format)."""
    if pity_legacy(p):
        return min(PPM, p["p0_ppm"] + p["k_ppm"] * n)
    return min(p["p_max_ppb"], p["p0_ppb"] + p["k_ppb"] * n, PPB)


def gold_roll(acc: bytes, unit: int = PPB) -> int:
    return roll(acc, 0, TAG_GOLD) % unit


def pity_is_gold(p: dict, n: int, acc: bytes) -> tuple[bool, int, int]:
    if pity_legacy(p):
        r, pp = gold_roll(acc, PPM), pity_p(p, n)
        return (n + 1 >= p["n_max"] or r < pp), r, pp
    r, pp = gold_roll(acc), pity_p(p, n)
    guaranteed = p.get("n_max") is not None and min(n + 1, U32_MAX) >= p["n_max"]
    return (guaranteed or r < pp), r, pp


def pity_after(p: dict, n: int, mode: str) -> int:
    """Compteur après le tirage : 0 après un gold pack seulement, n + 1 (saturé sur u32) sinon. Ancien
    format : 0 aussi après un pack rush."""
    if pity_legacy(p):
        return n + 1 if mode == "base" else 0
    return 0 if mode == "gold" else min(n + 1, U32_MAX)


def pack_mode(pity_gold: bool, rush: bool) -> str:
    return "gold" if pity_gold else ("rush" if rush else "base")


def mode_weights(table: dict, mode: str) -> dict:
    """Poids d'un pack normal (base ou rush). Un gold pack tire chaque emplacement avec
    ``gold_slot_weights``."""
    m = table.get("mechanics") or {}
    if mode == "rush" and m.get("rush"):
        return m["rush"]["weights"]
    return table["rarity_weights"]


# ------------------------------------------------------------------ gold pack et brûlable garantie

TAG_VALUE = 3


def gold_slot_weights(base: dict, s: dict) -> dict:
    """Poids propres de l'emplacement, ou poids de base mis à zéro sous le plancher."""
    if s.get("weights") is not None:
        return s["weights"]
    f = RARITIES.index(s["floor"])
    return {r: (base[r] if RARITIES.index(r) <= f else 0) for r in RARITIES}


def fallback_order(rolled: str, floor: str) -> list:
    """Visée, vers le bas jusqu'au plancher, puis vers le haut, puis sous le plancher."""
    f = RARITIES.index(floor)
    r = min(RARITIES.index(rolled), f)
    return [RARITIES[i] for i in range(r, f + 1)] + [RARITIES[i] for i in range(r - 1, -1, -1)] + [
        RARITIES[i] for i in range(f + 1, 5)
    ]


def burnable_weight(table: dict, minted, backed, burn, rarity: str) -> int:
    """Poids tirables des seules brûlables d'une rareté (jamais une mythique)."""
    if rarity == "mythic":
        return 0
    f = burn_factors(table, minted, burn, rarity) if burn is not None else None
    tot = 0
    for i, (c, n) in enumerate(zip(table["cards"], minted)):
        if c["rarity"] != rarity or not backed[i]:
            continue
        tot += in_rarity_weight(table, i, n, burn, f) if burn is not None else _available(c["weight"], n, c.get("cap"))
    return tot


def draw_slot_rule(table, minted, mythic_minted, acc, slot, weights, floor, burnable_only, backed, burn=None):
    """Même algorithme que ``draw::draw_slot_rule`` : rareté visée avec ``weights``, retombée selon
    ``fallback_order``, choix de la carte (restreint aux brûlables si ``burnable_only``).
    ``backed[i]`` : la carte ``i`` est brûlable au moment du tirage (table ou résurrection)."""
    total = max(sum(weights[r] for r in RARITIES), 1)
    rarity_roll = roll(acc, slot, 0) % total
    rolled = _rarity_from_roll(weights, rarity_roll)

    def avail(r):
        if burnable_only:
            return burnable_weight(table, minted, backed, burn, r)
        return available_weight_mech(table, minted, mythic_minted, burn, r)

    final, s = "common", 0
    for r in fallback_order(rolled, floor):
        a = avail(r)
        if a > 0:
            final, s = r, a
            break
    raw = roll(acc, slot, 1)
    card_roll = 0 if s == 0 else raw % s
    if final == "mythic" and s > 0:
        c = pick = 0
        for j, (m, n) in enumerate(zip(table["mythics"], mythic_minted)):
            c += _available(m["weight"], n, m.get("cap"))
            if card_roll < c:
                pick = j
                break
        return SlotDraw(slot, rarity_roll, rolled, final, card_roll, "mythic", pick)
    c = 0
    pick = _first_unlimited_common(table)
    f = burn_factors(table, minted, burn, final) if burn is not None else None
    for i, (card, n) in enumerate(zip(table["cards"], minted)):
        if card["rarity"] != final or (burnable_only and not backed[i]):
            continue
        c += in_rarity_weight(table, i, n, burn, f) if burn is not None else _available(card["weight"], n, card.get("cap"))
        if card_roll < c:
            pick = i
            break
    return SlotDraw(slot, rarity_roll, rolled, final, card_roll, "visible", pick)


# ------------------------------------------------------------------ valeur du pack


def value_table(v: dict, mode: str) -> list:
    return v["normal"] if mode == "base" else v[mode]


def value_tier(tiers: list, acc: bytes) -> tuple[int, int, int]:
    """``value_roll = roll(acc, 0, 3) mod Σpoids`` ; (value_roll, palier, valeur en points de base)."""
    total = max(sum(w for _, w in tiers), 1)
    r = roll(acc, 0, TAG_VALUE) % total
    cum = 0
    for i, (bps, w) in enumerate(tiers):
        cum += w
        if r < cum:
            return r, i, bps
    return r, 0, tiers[0][0] if tiers else 0


def value_total(price: int, bps: int) -> int:
    return price * bps // 10_000


def split_value(total: int, slots: list, mult: dict) -> list:
    """``slots[i] = (rareté, brûlable)`` ; ``⌊total × m_i / Σm⌋``, le reste au plus fort
    multiplicateur (premier emplacement en cas d'égalité) ; None hors brûlables."""
    s = sum(mult[r] for r, b in slots if b)
    if s == 0:
        return [None] * len(slots)
    out = [total * mult[r] // s if b else None for r, b in slots]
    best = None
    for i, (r, b) in enumerate(slots):
        if b and (best is None or mult[r] > mult[slots[best][0]]):
            best = i
    out[best] += total - sum(x for x in out if x is not None)
    return out


def draw_pack_mech(table, minted, mythic_minted, acc, mode: str, burn=None, backed=None):
    """Tous les emplacements comme ``finalize_pack`` : gold pack (un emplacement par plancher),
    sinon ``cards_per_pack`` emplacements dont le dernier parmi les brûlables si la série a une
    table de valeur. ``backed`` : brûlables au moment du tirage (par défaut : adossées par la table).
    Renvoie (tirages, brûlables par emplacement). ``minted`` et ``mythic_minted`` sont modifiés."""
    m = table.get("mechanics") or {}
    if backed is None:
        backed = burn.backed if burn is not None else [c.get("backing") is not None for c in table["cards"]]
    value = m.get("value")
    gold = m.get("gold") if mode == "gold" else None
    weights = mode_weights(table, mode)
    n = len(gold["slots"]) if gold else table["cards_per_pack"]
    out, slots = [], []
    for slot in range(n):
        if gold:
            gs = gold["slots"][slot]
            d = draw_slot_rule(table, minted, mythic_minted, acc, slot, gold_slot_weights(table["rarity_weights"], gs),
                               gs["floor"], gs["burnable"], backed, burn)
        elif value and slot == n - 1:
            d = draw_slot_rule(table, minted, mythic_minted, acc, slot, weights, "common", True, backed, burn)
        else:
            d = draw_slot(table, minted, mythic_minted, acc, slot, weights, burn)
        slots.append((d.final_rarity, d.kind == "visible" and bool(backed[d.index])))
        if d.kind == "visible":
            minted[d.index] += 1
        else:
            mythic_minted[d.index] += 1
        out.append(d)
    return out, slots


def slot_rules(table: dict, mode: str) -> list:
    """Règle de chaque emplacement d'un pack de cette table de taux :
    (poids, plancher, parmi les brûlables ?, emplacement à règle ?)."""
    m = table.get("mechanics") or {}
    gold = m.get("gold") if mode == "gold" else None
    if gold:
        return [(gold_slot_weights(table["rarity_weights"], s), s["floor"], s["burnable"], True) for s in gold["slots"]]
    w = mode_weights(table, mode)
    n = table["cards_per_pack"]
    last = bool(m.get("value"))
    return [(w, "common", last and i == n - 1, last and i == n - 1) for i in range(n)]


def pack_value(table: dict, acc: bytes, mode: str, slots: list) -> dict | None:
    """Valeur d'un pack, mêmes clés que ``pack_revealed.mechanics.value``."""
    v = (table.get("mechanics") or {}).get("value")
    if not v:
        return None
    r, tier, bps = value_tier(value_table(v, mode), acc)
    total = value_total(int(table["price"]), bps)
    amounts = split_value(total, slots, v["multipliers"])
    return {"roll": r, "tier": tier, "bps": bps, "total": str(total),
            "amounts": [None if a is None else str(a) for a in amounts]}


def new_rush_state() -> dict:
    return {"ring": [], "start_height": None, "last_trigger": None, "rush_count": 0}


def rush_on_buy(p: dict, st: dict, h: int) -> dict:
    """Même algorithme que ``draw::rush_on_buy`` ; ``st`` est modifié en place."""
    bsz = max(p["bucket_blocks"], 1)
    ml = max(p["baseline_blocks"] // bsz, 1)
    mw = min(max(p["window_blocks"] // bsz, 1), ml)
    if len(st["ring"]) != ml:
        st["ring"] = [[None, 0] for _ in range(ml)]
    if st["start_height"] is None:
        st["start_height"] = h
    start = st["start_height"]
    t = st["last_trigger"]
    in_period = t is not None and h <= t + p["duration_blocks"]
    active = in_period and h > t
    paused = t is not None and h <= t + p["duration_blocks"] + p["cooldown_blocks"]
    b = h // bsz
    e = st["ring"][b % ml]
    if e[0] != b:
        e[0], e[1] = b, 0
    e[1] += 1

    def count(m):
        return sum(c for bb, c in st["ring"] if bb is not None and bb <= b and b - bb < m)

    cw, cl = count(mw), count(ml)
    triggered = (
        not paused
        and h >= start + p["baseline_blocks"]
        and cw >= p["min_packs"]
        and cw * ml * 10_000 >= p["ratio_bps"] * cl * mw
    )
    if triggered:
        st["last_trigger"] = h
        st["rush_count"] += 1
    return {"active": active, "window_count": cw, "baseline_count": cl, "triggered": triggered}


def rush_account(p: dict, active: bool, trigger, prev):
    """Même règle que ``draw::rush_account`` : plafond de packs rush par compte et par rush.
    ``prev`` = (déclenchement, packs rush du compte) ou None. Renvoie (rush, plafonné, nouvel état)."""
    if not active or trigger is None:
        return False, False, prev
    n = prev[1] if prev is not None and prev[0] == trigger else 0
    if n >= p["max_per_account"]:
        return False, True, (trigger, n)
    return True, False, (trigger, n + 1)


def _rarity_from_roll(weights: dict, rarity_roll: int) -> str:
    cum = 0
    for r in RARITIES:
        cum += weights[r]
        if rarity_roll < cum:
            return r
    return "common"


def draw_slot(
    table: dict,
    minted: list[int],
    mythic_minted: list[int],
    acc: bytes,
    slot: int,
    weights: dict | None = None,
    burn: Burn | None = None,
) -> SlotDraw:
    """Un emplacement. ``weights`` : table de rareté du pack (base par défaut) ; ``burn`` : état des
    burns (rareté pilotée par les burns) ou ``None``. Sans les deux, identique au tirage d'origine."""
    weights = weights or table["rarity_weights"]
    total = max(sum(weights[r] for r in RARITIES), 1)
    rarity_roll = roll(acc, slot, 0) % total
    rolled = _rarity_from_roll(weights, rarity_roll)

    # Retombée sur la rareté inférieure si épuisée.
    final = rolled
    s = available_weight_mech(table, minted, mythic_minted, burn, final)
    while s == 0:
        low = lower(final)
        if low is None:
            break
        final = low
        s = available_weight_mech(table, minted, mythic_minted, burn, final)

    raw_card = roll(acc, slot, 1)
    card_roll = 0 if s == 0 else raw_card % s

    if final == "mythic":
        c = 0
        pick = 0
        for j, (m, n) in enumerate(zip(table["mythics"], mythic_minted)):
            c += _available(m["weight"], n, m.get("cap"))
            if card_roll < c:
                pick = j
                break
        kind = "mythic"
    else:
        c = 0
        pick = _first_unlimited_common(table)
        f = burn_factors(table, minted, burn, final) if burn is not None else None
        for i, (card, n) in enumerate(zip(table["cards"], minted)):
            if card["rarity"] != final:
                continue
            if burn is None:
                c += _available(card["weight"], n, card.get("cap"))
            else:
                c += in_rarity_weight(table, i, n, burn, f)
            if card_roll < c:
                pick = i
                break
        kind = "visible"
    return SlotDraw(slot, rarity_roll, rolled, final, card_roll, kind, pick)


def draw_pack(
    table: dict,
    minted: list[int],
    mythic_minted: list[int],
    acc: bytes,
    weights: dict | None = None,
    burn: Burn | None = None,
) -> list[SlotDraw]:
    """Tire tous les emplacements comme `finalize_pack` : les compteurs sont incrémentés entre deux
    emplacements. `minted` et `mythic_minted` sont modifiés en place."""
    out = []
    for slot in range(table["cards_per_pack"]):
        d = draw_slot(table, minted, mythic_minted, acc, slot, weights, burn)
        if d.kind == "visible":
            minted[d.index] += 1
        else:
            mythic_minted[d.index] += 1
        out.append(d)
    return out


def apply_event_draws(event: dict, minted: list[int], mythic_minted: list[int]) -> None:
    """Applique aux compteurs les cartes créées par un événement `pack_revealed` (tel que journalisé)."""
    for d in event["draws"]:
        if d["kind"] == "visible":
            minted[d["index"]] += 1
        else:
            mythic_minted[d["index"]] += 1
