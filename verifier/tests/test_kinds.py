"""Types de packs (`SeriesTable.kinds`) : concordance avec le Rust (`vectorgen/` kind_vectors).

Sérialisation et hash d'une table à types de packs, puis tirage d'un pack d'un type : cartes hors du
`pool` à poids 0, mythiques exclues si le type les exclut, règles par emplacement, valeur au prix du
type, compteurs partagés avec la série.
"""

import copy
import json
import os
import unittest

from memaster_verifier import canon, core

ICI = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ICI, "vectors", "kind_vectors.json"), encoding="utf-8") as f:
    KINDS = json.load(f)


class TestKindVectors(unittest.TestCase):
    def test_serialization_and_hash(self):
        for c in KINDS["cases"]:
            self.assertEqual(canon.table_json(c["table"]), c["table_json"], f"cas {c['case']}")
            self.assertEqual(core.table_hash(c["table"]).hex(), c["table_hash"])

    def test_table_without_kinds_keeps_its_bytes(self):
        t = copy.deepcopy(KINDS["cases"][0]["table"])
        t["kinds"] = None
        self.assertNotIn('"kinds"', canon.table_json(t))

    def test_kind_draws_match_the_contract(self):
        rules = 0
        for c in KINDS["cases"]:
            t = c["table"]
            m = t["mechanics"]
            kt = core.kind_table(t, c["kind"])
            burn = (
                core.Burn(c["burned"], c["backed"], m["burn"]["floor_bps"], m["burn"]["prior_k"], core.resurrectable(t))
                if m["burn"]
                else None
            )
            minted, mm = list(c["minted"]), list(c["mythic_minted"])
            draws, slots = core.draw_pack_mech(kt, minted, mm, bytes.fromhex(c["acc"]), c["mode"], burn, c["backed"])
            self.assertEqual([d.as_event() for d in draws], [{k: v for k, v in d.items() if k != "token_id"} for d in c["draws"]], f"cas {c['case']}")
            self.assertEqual([list(s) for s in slots], c["slots"])
            self.assertEqual((minted, mm), (c["minted_after"], c["mythic_minted_after"]))
            self.assertEqual(core.pack_value(kt, bytes.fromhex(c["acc"]), c["mode"], slots), c["value"], f"cas {c['case']}")
            rules += t["kinds"][c["kind"]].get("slots") is not None
        self.assertGreater(rules, 20, "assez de cas avec des règles par emplacement")

    def test_kind_never_draws_outside_its_pool_nor_excluded_mythics(self):
        for c in KINDS["cases"]:
            k = c["table"]["kinds"][c["kind"]]
            for d in c["draws"]:
                if d["kind"] == "visible" and k["pool"]:
                    # Seule exception : la commune de secours d'un tirage impossible (table non validée).
                    if c["table"]["cards"][d["index"]]["weight"] and d["card_roll"] != "0":
                        self.assertIn(d["index"], k["pool"], f"cas {c['case']}")
                if not k["mythics"]:
                    self.assertEqual(d["kind"], "visible", f"cas {c['case']}")


if __name__ == "__main__":
    unittest.main()
