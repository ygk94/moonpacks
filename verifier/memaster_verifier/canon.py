"""Sérialisation JSON identique à `serde_json::to_vec` pour les types du contrat.

`table_hash = sha256(serde_json::to_vec(table))`. Pour recalculer ce hash à partir d'une table lue
ailleurs (fichier joli, réponse retraitée), on resérialise selon le schéma Rust :

- champs dans l'ordre de déclaration des structs (`contract/src/types.rs`), sans espace ;
- `U128` en chaîne décimale, `u8`/`u16`/`u32` en nombre, `Option::None` en `null` ;
- chaînes comme serde_json : seuls `"` `\\` et les caractères < 0x20 sont échappés
  (`\\b \\f \\n \\r \\t`, sinon `\\u00xx` en hexadécimal minuscule) ; tout le reste en UTF-8 brut
  (y compris `/`, DEL, U+2028 et les emojis).

Quand on dispose des octets bruts de la vue `get_series_table`, il faut hacher ces octets
directement : le CLI le fait, et vérifie en plus que la resérialisation retombe sur les mêmes octets.
"""

from __future__ import annotations

_ESC = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\f": "\\f", "\n": "\\n", "\r": "\\r", "\t": "\\t"}


def _str(s: str) -> str:
    if not isinstance(s, str):
        raise TypeError(f"chaîne attendue, reçu {type(s).__name__}")
    out = []
    for ch in s:
        e = _ESC.get(ch)
        if e is not None:
            out.append(e)
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def _int(n, lo: int = 0, hi: int = 1 << 64) -> str:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"entier attendu, reçu {n!r}")
    if not lo <= n < hi:
        raise ValueError(f"entier hors bornes : {n}")
    return str(n)


def _u128(v) -> str:
    """`U128` : chaîne décimale côté JSON. Accepte aussi un entier Python."""
    if isinstance(v, str):
        if not v.isdigit() or (len(v) > 1 and v[0] == "0"):
            raise ValueError(f"U128 invalide : {v!r}")
        n = int(v)
    else:
        n = v
    return '"' + _int(n, 0, 1 << 128) + '"'


def _opt(v, f) -> str:
    return "null" if v is None else f(v)


def _obj(pairs) -> str:
    return "{" + ",".join(_str(k) + ":" + v for k, v in pairs) + "}"


def _arr(items, f) -> str:
    return "[" + ",".join(f(x) for x in items) + "]"


RARITY_NAMES = ("mythic", "legendary", "epic", "rare", "common")


def _rarity(r) -> str:
    if r not in RARITY_NAMES:
        raise ValueError(f"rareté inconnue : {r!r}")
    return _str(r)


def backing_json(b: dict) -> str:
    return _obj([("asset_id", _str(b["asset_id"])), ("amount", _u128(b["amount"]))])


def card_json(c: dict) -> str:
    return _obj(
        [
            ("card_id", _str(c["card_id"])),
            ("title", _str(c["title"])),
            ("rarity", _rarity(c["rarity"])),
            ("weight", _int(c["weight"], 0, 1 << 32)),
            ("cap", _opt(c.get("cap"), lambda x: _int(x, 0, 1 << 32))),
            ("media", _opt(c.get("media"), _str)),
            ("reference", _opt(c.get("reference"), _str)),
            ("backing", _opt(c.get("backing"), backing_json)),
        ]
    )


def mythic_commitment_json(m: dict) -> str:
    return _obj(
        [
            ("commitment", _str(m["commitment"])),
            ("content_hash", _str(m["content_hash"])),
            ("weight", _int(m["weight"], 0, 1 << 32)),
            ("cap", _int(m["cap"], 0, 1 << 32)),
        ]
    )


def royalty_json(r: dict) -> str:
    return _obj([("account_id", _str(r["account_id"])), ("bps", _int(r["bps"], 0, 1 << 16))])


def rarity_weights_json(w: dict) -> str:
    return _obj([(r, _int(w[r], 0, 1 << 32)) for r in RARITY_NAMES])


def _u32(x) -> str:
    return _int(x, 0, 1 << 32)


def _u64(x) -> str:
    return _int(x, 0, 1 << 64)


def pity_json(p: dict) -> str:
    return _obj([("p0_ppm", _u32(p["p0_ppm"])), ("k_ppm", _u32(p["k_ppm"])), ("n_max", _u32(p["n_max"]))])


def burn_json(b: dict) -> str:
    return _obj([("floor_bps", _u32(b["floor_bps"])), ("prior_k", _u32(b["prior_k"]))])


def rush_json(r: dict) -> str:
    return _obj(
        [
            ("ratio_bps", _u32(r["ratio_bps"])),
            ("min_packs", _u32(r["min_packs"])),
            ("window_blocks", _u64(r["window_blocks"])),
            ("baseline_blocks", _u64(r["baseline_blocks"])),
            ("bucket_blocks", _u64(r["bucket_blocks"])),
            ("duration_blocks", _u64(r["duration_blocks"])),
            ("cooldown_blocks", _u64(r["cooldown_blocks"])),
            ("max_per_account", _u32(r["max_per_account"])),
            ("weights", rarity_weights_json(r["weights"])),
        ]
    )


def resurrection_json(r: dict) -> str:
    return _obj([("eligible", "[" + ",".join(_u32(i) for i in r["eligible"]) + "]")])


def mechanics_json(m: dict) -> str:
    """`Mechanics` : tous les champs, `null` pour une option absente, dans l'ordre de `types.rs`."""
    return _obj(
        [
            ("gold_weights", _opt(m.get("gold_weights"), rarity_weights_json)),
            ("pity", _opt(m.get("pity"), pity_json)),
            ("burn", _opt(m.get("burn"), burn_json)),
            ("rush", _opt(m.get("rush"), rush_json)),
            ("resurrection", _opt(m.get("resurrection"), resurrection_json)),
        ]
    )


def table_json(t: dict) -> str:
    """`SeriesTable`. `mechanics` vient en dernier et **n'apparaît pas** quand il vaut `None`
    (`skip_serializing_if`) : une table sans mécanique garde ses octets et son hash."""
    pairs = [
        ("name", _str(t["name"])),
        ("price", _u128(t["price"])),
        ("cards_per_pack", _int(t["cards_per_pack"], 0, 1 << 8)),
        ("rarity_weights", rarity_weights_json(t["rarity_weights"])),
        ("cards", _arr(t["cards"], card_json)),
        ("mythics", _arr(t["mythics"], mythic_commitment_json)),
        ("royalties", _arr(t["royalties"], royalty_json)),
    ]
    if t.get("mechanics") is not None:
        pairs.append(("mechanics", mechanics_json(t["mechanics"])))
    return _obj(pairs)


def content_json(c: dict) -> str:
    """`MythicContent` : title, media, reference, backing."""
    return _obj(
        [
            ("title", _str(c["title"])),
            ("media", _opt(c.get("media"), _str)),
            ("reference", _opt(c.get("reference"), _str)),
            ("backing", _opt(c.get("backing"), backing_json)),
        ]
    )


def cards_json_bytes(cards: list) -> bytes:
    """Une page de `get_series_cards` (`Vec<CardDef>`), comme `serde_json::to_vec`."""
    return _arr(cards, card_json).encode("utf-8")


def table_json_bytes(t: dict) -> bytes:
    return table_json(t).encode("utf-8")


def content_json_bytes(c: dict) -> bytes:
    return content_json(c).encode("utf-8")
