"""Vérifications de haut niveau : table, booster (`pack_revealed`), mythique, rejeu d'une série."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import core
from .canon import cards_json_bytes, table_json_bytes

# Champs de `SeriesTable` dans l'ordre du hash (contract/src/types.rs, verrouillé par un test du contrat).
TABLE_FIELDS = ("name", "price", "cards_per_pack", "rarity_weights", "cards", "mythics", "royalties")


@dataclass
class Report:
    title: str
    ok_lines: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def check(self, cond: bool, ok: str, ko: str) -> bool:
        (self.ok_lines if cond else self.errors).append(ok if cond else ko)
        return cond

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self, verbose: bool = True) -> str:
        out = [f"== {self.title}"]
        if verbose:
            out += [f"  OK   {x}" for x in self.ok_lines]
        out += [f"  ÉCHEC {x}" for x in self.errors]
        out += [f"  note {x}" for x in self.notes]
        out.append(f"  => {'VÉRIFIÉ' if self.ok else 'NON CONFORME'}")
        return "\n".join(out)


def _hex(b: bytes) -> str:
    return b.hex()


def _unhex32(s: str, what: str) -> bytes:
    b = bytes.fromhex(s)
    if len(b) != 32 or s != s.lower():
        raise ValueError(f"{what} : 32 octets en hex minuscule attendus")
    return b


# ------------------------------------------------------------------ événements


def parse_event_obj(obj, name: str | None = None):
    """Accepte : données d'événement, enveloppe NEP-297, ligne `EVENT_JSON:...`, ou enregistrement
    `{"event": {...}}` (format des vecteurs). Renvoie les données, ou None si ce n'est pas l'événement voulu."""
    if isinstance(obj, str):
        if not obj.startswith("EVENT_JSON:"):
            return None
        obj = json.loads(obj[len("EVENT_JSON:"):])
    if not isinstance(obj, dict):
        return None
    if "standard" in obj and "data" in obj:
        if obj.get("standard") != "memaster" or (name and obj.get("event") != name):
            return None
        return obj["data"][0]
    if "event" in obj and isinstance(obj["event"], dict):
        return parse_event_obj(obj["event"], name)
    return obj


def events_from_logs(logs: list[str], name: str) -> list[dict]:
    out = []
    for line in logs:
        ev = parse_event_obj(line, name) if line.startswith("EVENT_JSON:") else None
        if ev is not None:
            out.append(ev)
    return out


def load_events(path: str, name: str = "pack_revealed") -> list[dict]:
    """Fichier JSON (objet ou liste) ou JSONL / lignes de logs `EVENT_JSON:`."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        data = json.loads(text)
        items = data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            items.append(line if line.startswith("EVENT_JSON:") else json.loads(line))
    out = []
    for it in items:
        ev = parse_event_obj(it, name)
        if ev is not None:
            out.append(ev)
    return out


# ------------------------------------------------------------------ table


def verify_table(table_bytes: bytes, expected_hex: dict[str, str | None]) -> tuple[Report, dict]:
    """`table_bytes` : octets de la table (idéalement la réponse brute de `get_series_table`).
    `expected_hex` : {source: hash hex} à comparer (vue `get_series`, événement, argument)."""
    rep = Report("Table de série")
    table = json.loads(table_bytes)
    raw_hash = core.sha256(table_bytes)
    canon = table_json_bytes(table)
    canon_hash = core.sha256(canon)
    if canon == table_bytes:
        rep.check(True, "les octets reçus sont exactement la sérialisation serde_json de la table", "")
    else:
        rep.note("les octets fournis ne sont pas la forme serde_json (fichier reformaté ?) : on hache la forme canonique")
    rep.ok_lines.append(f"sha256 calculé : {_hex(canon_hash)}")
    if not expected_hex:
        rep.note("aucun hash de référence fourni : rien à comparer (--expected-hash ou --rpc)")
    for src, h in expected_hex.items():
        if h is None:
            rep.errors.append(f"{src} : aucun hash publié (série non ouverte ?)")
            continue
        rep.check(h == _hex(canon_hash), f"{src} = {h}", f"{src} = {h} ≠ {_hex(canon_hash)}")
    if canon != table_bytes and raw_hash != canon_hash:
        rep.note(f"sha256 des octets bruts du fichier : {_hex(raw_hash)}")
    return rep, table


def table_from_pages(header_view: dict, pages: list[bytes]) -> tuple[dict, list[str]]:
    """Table reconstruite à partir de `get_series_header` et des pages brutes de `get_series_cards`.
    Renvoie (table, problèmes de forme)."""
    problems = []
    header = header_view["header"]
    if list(header) != list(TABLE_FIELDS):
        problems.append(f"champs de l'en-tête inattendus : {list(header)}")
    if header.get("cards"):
        problems.append("l'en-tête contient des cartes")
    cards = []
    for i, raw in enumerate(pages):
        page = json.loads(raw)
        if cards_json_bytes(page) != raw:
            problems.append(f"page {i} : octets différents de la forme serde_json")
        cards.extend(page)
    if len(cards) != int(header_view["card_count"]):
        problems.append(f"{len(cards)} cartes lues, card_count = {header_view['card_count']}")
    table = {k: header.get(k) for k in TABLE_FIELDS}
    table["cards"] = cards
    return table, problems


def verify_table_pages(
    header_view: dict, pages: list[bytes], expected_hex: dict[str, str | None]
) -> tuple[Report, dict]:
    """Vérification d'une table lue par pages : en-tête léger (`get_series_header`) et pages brutes
    de `get_series_cards`. Le hash est recalculé ici, sur la table reconstruite, puis comparé au
    hash enregistré à l'ouverture (`header_view["table_hash"]`) et aux autres sources."""
    table, problems = table_from_pages(header_view, pages)
    rep, table = verify_table(
        table_json_bytes(table), {"get_series_header.table_hash (enregistré à l'ouverture)": header_view.get("table_hash"), **expected_hex}
    )
    rep.title = "Table de série (lue par pages)"
    rep.ok_lines = [x for x in rep.ok_lines if not x.startswith("les octets reçus")]
    for p in problems:
        rep.errors.append(p)
    if not problems:
        rep.ok_lines.insert(
            0,
            f"{len(pages)} pages de get_series_cards, {header_view['card_count']} cartes : chaque page est exactement la forme serde_json",
        )
    return rep, table


def table_summary(table: dict) -> list[str]:
    total = core.rarity_total(table)
    lines = [f"{table['name']!r} : {table['cards_per_pack']} cartes par booster, prix {table['price']} yocto"]
    for r in core.RARITIES:
        w = table["rarity_weights"][r]
        lines.append(f"  {r:<9} poids {w:>6}  ({100 * w / total:.4f} %)")
    return lines


# ------------------------------------------------------------------ booster


def verify_acc(rep: Report, ev: dict, table_hash: bytes) -> bytes | None:
    pack_id = int(ev["pack_id"])
    owner = ev["owner_id"]
    acc = core.initial_acc(pack_id, owner, table_hash)
    if not rep.check(
        _hex(acc) == ev["initial_acc"],
        f"initial_acc = sha256('memaster:pack' || {pack_id} || {owner} || table_hash)",
        f"initial_acc recalculé {_hex(acc)} ≠ {ev['initial_acc']}",
    ):
        return None
    for s in ev["seeds"]:
        acc = core.mix(acc, _unhex32(s["seed"], "seed"), pack_id, owner)
        if not rep.check(
            _hex(acc) == s["acc"],
            f"tentative {s.get('attempt', '?')} étape {s.get('step', '?')} (bloc {s.get('block_height', '?')}) : acc enchaîné",
            f"tentative {s.get('attempt', '?')} étape {s.get('step', '?')} : acc recalculé {_hex(acc)} ≠ {s['acc']}",
        ):
            return None
    if not rep.check(_hex(acc) == ev["acc"], f"acc final {ev['acc']}", f"acc final recalculé {_hex(acc)} ≠ {ev['acc']}"):
        return None
    return acc


def final_block_height(ev: dict) -> int | None:
    """Hauteur du bloc du dernier reçu (celui qui tire) : la dernière graine journalisée y a été lue."""
    return ev["seeds"][-1]["block_height"] if ev.get("seeds") else None


def verify_pack(
    ev: dict,
    table: dict,
    minted: list[int] | None,
    mythic_minted: list[int] | None,
    state_source: str = "",
) -> Report:
    """Vérifie un `pack_revealed`. Si `minted` est None, seules les parties indépendantes de l'état sont
    vérifiées (acc, rarity_roll, rareté visée, cohérence carte/rareté)."""
    rep = Report(f"Booster {ev['pack_id']} (série {ev['series_id']}, {ev['owner_id']})")
    th = core.table_hash(table)
    if not rep.check(
        ev.get("table_hash") == _hex(th),
        "table_hash de l'événement = sha256(table)",
        f"table_hash de l'événement {ev.get('table_hash')} ≠ sha256(table) {_hex(th)}",
    ):
        return rep
    acc = verify_acc(rep, ev, th)
    if acc is None:
        return rep
    draws = ev["draws"]
    n = table["cards_per_pack"]
    rep.check(len(draws) == n, f"{n} tirages", f"{len(draws)} tirages au lieu de {n}")
    rep.check(
        [d["slot"] for d in draws] == list(range(len(draws))),
        "emplacements 0..n-1 dans l'ordre",
        "emplacements non consécutifs",
    )
    if minted is not None:
        m = list(minted)
        mm = list(mythic_minted or [])
        if len(m) != len(table["cards"]) or len(mm) != len(table["mythics"]):
            rep.errors.append("instantané minted de longueur incompatible avec la table")
            return rep
        expected = core.draw_pack(table, m, mm, acc)
        for d, e in zip(draws, expected):
            got = {k: d[k] for k in e.as_event()}
            label = _draw_label(table, e)
            rep.check(got == e.as_event(), f"emplacement {e.slot} : {label}", f"emplacement {e.slot} : attendu {e.as_event()}, journalisé {got}")
        if state_source:
            rep.note(f"état des plafonds : {state_source}")
    else:
        total = max(core.rarity_total(table), 1)
        for d in draws:
            slot = d["slot"]
            rr = core.roll(acc, slot, 0) % total
            rep.check(str(rr) == d["rarity_roll"], f"emplacement {slot} : rarity_roll {rr}", f"emplacement {slot} : rarity_roll {rr} ≠ {d['rarity_roll']}")
            rolled = _rolled(table, rr)
            rep.check(rolled == d["rolled_rarity"], f"emplacement {slot} : rareté visée {rolled}", f"emplacement {slot} : rareté visée {rolled} ≠ {d['rolled_rarity']}")
            ok_down = core.RARITIES.index(d["final_rarity"]) >= core.RARITIES.index(d["rolled_rarity"])
            rep.check(ok_down, f"emplacement {slot} : retombée vers le bas seulement", f"emplacement {slot} : rareté finale plus haute que la rareté visée")
            if d["kind"] == "visible":
                ok = d["index"] < len(table["cards"]) and table["cards"][d["index"]]["rarity"] == d["final_rarity"]
            else:
                ok = d["final_rarity"] == "mythic" and d["index"] < len(table["mythics"])
            rep.check(ok, f"emplacement {slot} : carte de la bonne rareté", f"emplacement {slot} : carte incohérente avec la rareté finale")
        rep.note("sans état des plafonds (--snapshot, --history ou --rpc) : card_roll et le choix de la carte ne sont pas recalculés")
    return rep


def _rolled(table: dict, rarity_roll: int) -> str:
    cum = 0
    for r in core.RARITIES:
        cum += table["rarity_weights"][r]
        if rarity_roll < cum:
            return r
    return "common"


def _draw_label(table: dict, d: core.SlotDraw) -> str:
    if d.kind == "visible":
        name = table["cards"][d.index]["card_id"]
    else:
        name = f"mythique #{d.index} ({table['mythics'][d.index]['commitment'][:12]}…)"
    fall = "" if d.rolled_rarity == d.final_rarity else f" (retombée depuis {d.rolled_rarity})"
    return f"{d.final_rarity} {name}{fall}"


def replay(table: dict, events: list[dict], until_pack: int | None = None, minted=None, mythic_minted=None):
    """Rejoue des `pack_revealed` dans l'ordre d'exécution, à partir de compteurs nuls (ouverture) ou fournis.
    Renvoie (rapports, minted, mythic_minted). S'arrête après `until_pack` s'il est donné."""
    m = list(minted) if minted is not None else [0] * len(table["cards"])
    mm = list(mythic_minted) if mythic_minted is not None else [0] * len(table["mythics"])
    reports = []
    for ev in events:
        rep = verify_pack(ev, table, m, mm)
        reports.append(rep)
        # On avance avec les cartes journalisées (pas les recalculées) pour isoler une éventuelle erreur.
        core.apply_event_draws(ev, m, mm)
        if until_pack is not None and int(ev["pack_id"]) == until_pack:
            break
    return reports, m, mm


# ------------------------------------------------------------------ mythiques


def verify_mythic(
    card_id: str,
    sel_hex: str,
    content: dict,
    commitment: str,
    content_hash: str,
    source: str,
    index: int | None = None,
) -> Report:
    rep = Report(f"Mythique {'#' + str(index) + ' ' if index is not None else ''}{card_id!r}")
    try:
        sel = bytes.fromhex(sel_hex)
    except ValueError:
        rep.errors.append("sel : hex invalide")
        return rep
    rep.check(len(sel) == 32 and sel_hex == sel_hex.lower(), "sel de 32 octets", f"sel de {len(sel)} octets (le contrat exige 32)")
    c, h = core.mythic_commitments(card_id, sel, content)
    rep.check(_hex(c) == commitment, f"sha256(card_id || sel) = engagement ({source})", f"sha256(card_id || sel) = {_hex(c)} ≠ {commitment} ({source})")
    rep.check(_hex(h) == content_hash, f"sha256(json(content) || sel) = content_hash ({source})", f"sha256(json(content) || sel) = {_hex(h)} ≠ {content_hash} ({source})")
    b = content.get("backing")
    rep.note(f"contenu lié : titre {content['title']!r}, adossement {b['asset_id'] + ' × ' + str(b['amount']) if b else 'aucun'}")
    return rep
