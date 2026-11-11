"""Contrôle croisé contrat / vérificateur sur un corpus de cas aléatoires.

Le corpus est produit par ``contract/src/tests_fuzz.rs`` (code ``memaster::draw`` du contrat) : chaque
cas donne une table valide, un état (``minted``, burns, résurrections), une table de taux, un ``acc``,
et le résultat du contrat. Ce module recalcule tout avec ``memaster_verifier.core`` et liste les
écarts.

    python3 -I verifier/tests/crosscheck.py corpus.json     # code de sortie 1 en cas d'écart

Le test ``test_fuzz.py`` rejoue le corpus figé ``vectors/fuzz_vectors.json`` (graine fixe) ; le test
Rust ``contract_and_python_verifier_agree_on_random_inputs`` appelle ce script sur des graines neuves.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from memaster_verifier import core  # noqa: E402


def check_case(c: dict) -> list[str]:
    i, e = c["input"], c["expected"]
    t = i["table"]
    m = t.get("mechanics") or {}
    acc = bytes.fromhex(i["acc"])
    mode = i["mode"]
    errs: list[str] = []
    burn = None
    if m.get("burn"):
        burn = core.Burn(
            list(i["burned"]), list(i["backed"]), m["burn"]["floor_bps"], m["burn"]["prior_k"], core.resurrectable(t)
        )
    minted, mm = list(i["minted"]), list(i["mythic_minted"])
    draws, slots = core.draw_pack_mech(t, minted, mm, acc, mode, burn, list(i["backed"]))
    got = [d.as_event() for d in draws]
    if got != e["draws"]:
        for a, b in zip(got, e["draws"]):
            if a != b:
                errs.append(f"tirage : vérificateur {a} ≠ contrat {b}")
                break
        if len(got) != len(e["draws"]):
            errs.append(f"{len(got)} tirages au lieu de {len(e['draws'])}")
    if [list(s) for s in slots] != e["slots"]:
        errs.append(f"brûlables par emplacement : {slots} ≠ {e['slots']}")
    if minted != e["minted_after"] or mm != e["mythic_minted_after"]:
        errs.append("compteurs après le pack différents")
    v = core.pack_value(t, acc, mode, [tuple(s) for s in e["slots"]])
    if v != e["value"]:
        errs.append(f"valeur : {v} ≠ {e['value']}")
    if e.get("pity") is not None:
        p, n = m["pity"], i["pity_n"]
        g, r, pp = core.pity_is_gold(p, n, acc)
        after = core.pity_after(p, n, "gold" if g else "base")
        want = e["pity"]
        if (g, r, pp, after) != (want["gold"], want["gold_roll"], want["p_ppb"], want["after"]):
            errs.append(f"pitié n={n} : ({g}, {r}, {pp}, {after}) ≠ contrat {want}")
    if e.get("rush") is not None:
        p = m["rush"]
        st = core.new_rush_state()
        accounts: dict = {}
        for (h, who), want in zip(i["rush_heights"], e["rush"]["buys"]):
            o = core.rush_on_buy(p, st, h)
            prev = accounts.get(who) if o["active"] else None
            rush, capped, entry = core.rush_account(p, o["active"], st["last_trigger"], prev)
            if rush:
                accounts[who] = entry
            mine = {
                "h": h, "who": who, "active": o["active"], "window_count": o["window_count"],
                "baseline_count": o["baseline_count"], "triggered": o["triggered"], "rush": rush,
                "capped": capped, "last_trigger": st["last_trigger"],
            }
            if mine != want:
                errs.append(f"rush à la hauteur {h} : {mine} ≠ contrat {want}")
                break
        if st["rush_count"] != e["rush"]["rush_count"]:
            errs.append(f"rush_count {st['rush_count']} ≠ {e['rush']['rush_count']}")
    return errs


def check_corpus(doc: dict) -> list[str]:
    out = []
    for c in doc["cases"]:
        for err in check_case(c):
            out.append(f"cas {c['input']['case']} : {err}")
    return out


def main(argv: list[str]) -> int:
    with open(argv[1], encoding="utf-8") as f:
        doc = json.load(f)
    errs = check_corpus(doc)
    for x in errs[:20]:
        print(x)
    print(f"{len(doc['cases'])} cas, {len(errs)} écarts")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
