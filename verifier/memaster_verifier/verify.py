"""Vérifications de haut niveau : table, booster (`pack_revealed`), mythique, rejeu d'une série."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import core
from .canon import cards_json_bytes, table_json_bytes

# Champs de `SeriesTable` dans l'ordre du hash (contract/src/types.rs, verrouillé par un test du contrat).
# `mechanics` (dernier) n'apparaît que pour une série à mécaniques.
TABLE_FIELDS = ("name", "price", "cards_per_pack", "rarity_weights", "cards", "mythics", "royalties")
OPTIONAL_FIELDS = ("mechanics",)
# Événements utiles au rejeu d'une série à mécaniques.
SERIES_EVENTS = ("pack_bought", "pack_revealed", "card_redeemed", "card_resurrected")


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


def parse_any_event(obj, names=SERIES_EVENTS):
    """(nom, données) pour un événement memaster de `names`, ou None. Des données nues sans enveloppe
    sont lues comme un `pack_revealed` (format historique)."""
    if isinstance(obj, str):
        if not obj.startswith("EVENT_JSON:"):
            return None
        obj = json.loads(obj[len("EVENT_JSON:"):])
    if not isinstance(obj, dict):
        return None
    if "standard" in obj and "data" in obj:
        if obj.get("standard") != "memaster" or obj.get("event") not in names:
            return None
        return obj["event"], obj["data"][0]
    if "event" in obj and isinstance(obj["event"], dict):
        return parse_any_event(obj["event"], names)
    if "draws" in obj and "pack_revealed" in names:
        return "pack_revealed", obj
    return None


def load_series_events(path: str, names=SERIES_EVENTS) -> list[tuple[str, dict]]:
    """Comme `load_events`, mais garde plusieurs types d'événements dans l'ordre du fichier."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        data = json.loads(text)
        items = data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        items = []
        for line in text.splitlines():
            line = line.strip()
            if line:
                items.append(line if line.startswith("EVENT_JSON:") else json.loads(line))
    out = []
    for it in items:
        ev = parse_any_event(it, names)
        if ev is not None:
            out.append(ev)
    return out


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
    keys = list(header)
    if keys != list(TABLE_FIELDS) and keys != list(TABLE_FIELDS + OPTIONAL_FIELDS):
        problems.append(f"champs de l'en-tête inattendus : {keys}")
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
    if header.get("mechanics") is not None:
        table["mechanics"] = header["mechanics"]
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
    m = table.get("mechanics")
    if m:
        lines.append(f"  mécaniques : {json.dumps(m, ensure_ascii=False)}")
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


def verify_mechanics(rep: Report, ev: dict, table: dict, acc: bytes, mech: dict | None):
    """Contrôle le bloc `mechanics` d'un `pack_revealed` : gold_roll, probabilité, décision, table de
    taux, compteur de pitié. `mech` (rejeu) donne l'état attendu : `pity_before`, `rush`, `burn`
    (`core.Burn`), `burn_seq`, `resurrect_seq` ; une clé absente n'est pas vérifiée.
    Renvoie (poids de rareté, état des burns ou None, burns connus ?)."""
    m = table.get("mechanics")
    em = ev.get("mechanics")
    if m is None:
        rep.check(em is None, "série sans mécanique : aucun bloc mechanics", "bloc mechanics pour une série sans mécanique")
        return table["rarity_weights"], None, True
    if not rep.check(isinstance(em, dict), "bloc mechanics journalisé", "bloc mechanics absent de l'événement"):
        return table["rarity_weights"], None, False
    mech = mech or {}
    rush = bool(em.get("rush"))
    if "rush" in mech:
        rep.check(rush == mech["rush"], f"rush {rush} (figé à l'achat, rejoué depuis pack_bought)", f"rush journalisé {rush} ≠ rejoué {mech['rush']}")
    pity_gold = False
    if m.get("pity"):
        pe = em.get("pity") or {}
        n = pe.get("before")
        if "pity_before" in mech:
            rep.check(n == mech["pity_before"], f"compteur de pitié avant le tirage : {n}", f"compteur de pitié journalisé {n} ≠ rejoué {mech['pity_before']}")
        if isinstance(n, int):
            g, r, pp = core.pity_is_gold(m["pity"], n, acc)
            rep.check(pe.get("gold_roll") == r, f"gold_roll = roll(acc, 0, 2) mod 10⁶ = {r}", f"gold_roll {pe.get('gold_roll')} ≠ {r}")
            rep.check(pe.get("p_ppm") == pp, f"p = min(10⁶, p0 + k × {n}) = {pp} ppm", f"p journalisé {pe.get('p_ppm')} ≠ {pp}")
            rep.check(pe.get("gold") == g, f"gold pack (pitié) : {g}", f"décision de pitié {pe.get('gold')} ≠ {g}")
            pity_gold = g
        else:
            rep.errors.append("pitié : compteur 'before' absent")
    mode = core.pack_mode(pity_gold, rush)
    rep.check(em.get("mode") == mode, f"table de taux : {mode}", f"table de taux journalisée {em.get('mode')} ≠ {mode}")
    if m.get("pity") and isinstance((em.get("pity") or {}).get("before"), int):
        n = em["pity"]["before"]
        after = n + 1 if mode == "base" else 0
        rep.check(em["pity"].get("after") == after, f"compteur de pitié après : {after}", f"compteur après {em['pity'].get('after')} ≠ {after}")
    weights = core.mode_weights(table, mode)
    burn = None
    known = True
    if m.get("burn"):
        if "burn" in mech and mech["burn"] is not None:
            for k in ("burn_seq", "resurrect_seq"):
                if k in mech:
                    rep.check(em.get(k) == mech[k], f"{k} = {em.get(k)}", f"{k} journalisé {em.get(k)} ≠ rejoué {mech[k]}")
            burn = mech["burn"]
        else:
            known = False
            rep.note("rareté pilotée par les burns : compteurs de burn inconnus (rejeu des card_redeemed et card_resurrected nécessaire), choix de la carte non recalculé")
    return weights, burn, known


def verify_pack(
    ev: dict,
    table: dict,
    minted: list[int] | None,
    mythic_minted: list[int] | None,
    state_source: str = "",
    mech: dict | None = None,
) -> Report:
    """Vérifie un `pack_revealed`. Si `minted` est None, seules les parties indépendantes de l'état sont
    vérifiées (acc, rarity_roll, rareté visée, cohérence carte/rareté). Pour une série à mécaniques,
    `mech` porte l'état rejoué (voir `verify_mechanics`)."""
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
    weights, burn, burn_known = verify_mechanics(rep, ev, table, acc, mech)
    if not burn_known:
        minted = None
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
        expected = core.draw_pack(table, m, mm, acc, weights, burn)
        for d, e in zip(draws, expected):
            got = {k: d[k] for k in e.as_event()}
            label = _draw_label(table, e)
            rep.check(got == e.as_event(), f"emplacement {e.slot} : {label}", f"emplacement {e.slot} : attendu {e.as_event()}, journalisé {got}")
        if state_source:
            rep.note(f"état des plafonds : {state_source}")
    else:
        total = max(sum(weights[r] for r in core.RARITIES), 1)
        for d in draws:
            slot = d["slot"]
            rr = core.roll(acc, slot, 0) % total
            rep.check(str(rr) == d["rarity_roll"], f"emplacement {slot} : rarity_roll {rr}", f"emplacement {slot} : rarity_roll {rr} ≠ {d['rarity_roll']}")
            rolled = core._rarity_from_roll(weights, rr)
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


class SeriesReplay:
    """État d'une série rejoué depuis l'ouverture à partir des événements seuls : compteurs `minted`,
    pitié par compte, burns (`card_redeemed.burn_seq`), résurrections (`card_resurrected.resurrect_seq`)
    et gold rush (`pack_bought`, rejoué par `core.rush_on_buy`)."""

    def __init__(self, table: dict, minted=None, mythic_minted=None):
        self.table = table
        self.m = list(minted) if minted is not None else [0] * len(table["cards"])
        self.mm = list(mythic_minted) if mythic_minted is not None else [0] * len(table["mythics"])
        self.mech = table.get("mechanics")
        self.pity: dict[str, int] = {}
        self.burned = [0] * len(table["cards"])
        self.burn_seq = 0
        self.backed = [c.get("backing") is not None for c in table["cards"]]
        self.resurrect_seq = 0
        self.pending_burns: dict[int, int] = {}
        self.pending_res: dict[int, int] = {}
        self.rush_state = core.new_rush_state()
        self.rush_of: dict[int, bool] = {}
        self.saw_bought = False

    def on_bought(self, ev: dict) -> Report | None:
        if not (self.mech and self.mech.get("rush")):
            return None
        self.saw_bought = True
        rep = Report(f"Achat du booster {ev['pack_id']} (gold rush)")
        o = core.rush_on_buy(self.mech["rush"], self.rush_state, int(ev["block_height"]))
        self.rush_of[int(ev["pack_id"])] = o["active"]
        er = ev.get("rush") or {}
        for k in ("active", "window_count", "baseline_count", "triggered"):
            rep.check(er.get(k) == o[k], f"{k} = {o[k]}", f"{k} journalisé {er.get(k)} ≠ rejoué {o[k]}")
        return rep

    def on_redeemed(self, ev: dict) -> None:
        if ev.get("burn_seq") is not None and ev.get("kind") == "visible":
            self.pending_burns[int(ev["burn_seq"])] = int(ev["index"])

    def on_resurrected(self, ev: dict) -> None:
        if ev.get("previous") is None:
            self.pending_res[int(ev["resurrect_seq"])] = int(ev["card_index"])

    def _advance(self, burn_seq: int | None, res_seq: int | None) -> list[str]:
        missing = []
        while burn_seq is not None and self.burn_seq < burn_seq:
            s = self.burn_seq + 1
            if s not in self.pending_burns:
                missing.append(f"card_redeemed burn_seq {s} absent")
                break
            self.burned[self.pending_burns.pop(s)] += 1
            self.burn_seq = s
        while res_seq is not None and self.resurrect_seq < res_seq:
            s = self.resurrect_seq + 1
            if s not in self.pending_res:
                missing.append(f"card_resurrected resurrect_seq {s} absent")
                break
            self.backed[self.pending_res.pop(s)] = True
            self.resurrect_seq = s
        return missing

    def on_revealed(self, ev: dict) -> Report:
        mech = None
        missing = []
        if self.mech:
            em = ev.get("mechanics") or {}
            mech = {}
            if self.mech.get("pity"):
                mech["pity_before"] = self.pity.get(ev["owner_id"], 0)
            if self.mech.get("rush") and self.saw_bought:
                pid = int(ev["pack_id"])
                if pid in self.rush_of:
                    mech["rush"] = self.rush_of[pid]
            if self.mech.get("burn"):
                missing = self._advance(em.get("burn_seq"), em.get("resurrect_seq"))
                if not missing:
                    mech.update(
                        burn=core.Burn(list(self.burned), list(self.backed), self.mech["burn"]["floor_bps"]),
                        burn_seq=self.burn_seq,
                        resurrect_seq=self.resurrect_seq,
                    )
        rep = verify_pack(ev, self.table, self.m, self.mm, mech=mech)
        for x in missing:
            rep.errors.append(f"rejeu incomplet : {x}")
        core.apply_event_draws(ev, self.m, self.mm)
        em = ev.get("mechanics") or {}
        if self.mech and self.mech.get("pity") and isinstance((em.get("pity") or {}).get("after"), int):
            self.pity[ev["owner_id"]] = em["pity"]["after"]
        return rep

    def feed(self, name: str, ev: dict) -> Report | None:
        if name == "pack_bought":
            return self.on_bought(ev)
        if name == "card_redeemed":
            self.on_redeemed(ev)
        elif name == "card_resurrected":
            self.on_resurrected(ev)
        elif name == "pack_revealed":
            return self.on_revealed(ev)
        return None


def replay_series(table: dict, items: list[tuple[str, dict]], minted=None, mythic_minted=None):
    """Rejoue une série à partir d'événements de plusieurs types, dans l'ordre d'exécution.
    Renvoie (rapports, état)."""
    st = SeriesReplay(table, minted, mythic_minted)
    reports = []
    for name, ev in items:
        r = st.feed(name, ev)
        if r is not None:
            reports.append(r)
    return reports, st


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
