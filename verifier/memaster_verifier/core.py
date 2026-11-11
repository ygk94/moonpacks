"""Réimplémentation indépendante de `contract/src/draw.rs`, du hash de table et des engagements mythiques.

Tout est calculé octet par octet comme le contrat :

- ``initial_acc = sha256("memaster:pack" || pack_id_le64 || owner_utf8 || table_hash)``
- ``mix(acc, seed) = sha256(acc || seed || pack_id_le64 || owner_utf8)``
- ``roll(acc, slot, tag) = u128_be(sha256(acc || slot_u8 || tag_u8)[0..16])``
- ``table_hash = sha256(serde_json::to_vec(table))`` (voir ``canon.py``)
- ``commitment = sha256(card_id_utf8 || sel)``, ``content_hash = sha256(json(content) || sel)``
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


def draw_slot(table: dict, minted: list[int], mythic_minted: list[int], acc: bytes, slot: int) -> SlotDraw:
    total = max(rarity_total(table), 1)
    rarity_roll = roll(acc, slot, 0) % total
    cum = 0
    rolled = "common"
    for r in RARITIES:
        cum += table["rarity_weights"][r]
        if rarity_roll < cum:
            rolled = r
            break

    # Retombée sur la rareté inférieure si épuisée.
    final = rolled
    s = available_weight(table, minted, mythic_minted, final)
    while s == 0:
        low = lower(final)
        if low is None:
            break
        final = low
        s = available_weight(table, minted, mythic_minted, final)

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
        for i, (card, n) in enumerate(zip(table["cards"], minted)):
            if card["rarity"] != final:
                continue
            c += _available(card["weight"], n, card.get("cap"))
            if card_roll < c:
                pick = i
                break
        kind = "visible"
    return SlotDraw(slot, rarity_roll, rolled, final, card_roll, kind, pick)


def draw_pack(table: dict, minted: list[int], mythic_minted: list[int], acc: bytes) -> list[SlotDraw]:
    """Tire tous les emplacements comme `finalize_pack` : les compteurs sont incrémentés entre deux
    emplacements. `minted` et `mythic_minted` sont modifiés en place."""
    out = []
    for slot in range(table["cards_per_pack"]):
        d = draw_slot(table, minted, mythic_minted, acc, slot)
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
