"""Séries du contrat v4 (`contract/series-v4/`, construites par `contract/scripts/build_v4.py`) : elles passent
`validate_series.py`, leur hash est celui annoncé, les 9 types de packs ont les règles prévues, et chaque table à
types de packs que le contrat refuserait (E_KINDS) est refusée."""

import copy
import json
import sys
import unittest

from memaster_verifier import core
from memaster_verifier.canon import cards_json_bytes
from memaster_verifier.verify import verify_table_pages
from tests import fake_secrets

CONTRACT = fake_secrets.CONTRACT
sys.path.insert(0, str(CONTRACT / "scripts"))

import build_v4  # noqa: E402
import validate_series as vs  # noqa: E402

V4 = CONTRACT / "series-v4"


def load(slug):
    return json.loads((V4 / slug / "table.json").read_text(encoding="utf-8"))


class TestSeriesV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.classic, cls.moon = load("classic"), load("full-moon")

    def test_both_series_pass_and_match_their_hash(self):
        for slug, t in (("classic", self.classic), ("full-moon", self.moon)):
            res, _ = vs.validate(str(V4 / slug))
            self.assertTrue(res.ok, res.errors)
            self.assertEqual(core.table_hash(t).hex(), (V4 / slug / "table_hash.txt").read_text().strip())

    def test_the_nine_pack_types(self):
        kinds = self.classic["kinds"]
        self.assertEqual([(k["name"], k["cards_per_pack"]) for k in kinds], [
            ("Dog", 8), ("Cat", 5), ("Frog", 3), ("Solana", 5), ("BNB Chain", 10), ("Ethereum", 3),
            ("OG 1", 1), ("OG 2", 2), ("OG 5", 5)])
        self.assertIsNone(self.moon.get("kinds"))
        # Seul le pack Solana garde les mythiques ; les OG ont tous le même pool.
        self.assertEqual([k["name"] for k in kinds if k["mythics"]], ["Solana"])
        self.assertEqual(kinds[6]["pool"], kinds[8]["pool"])
        for k in kinds:
            self.assertLess(int(k["price"]), int(self.classic["price"]) * 3)

    def test_dog_pack_has_a_burnable_one_time_in_three(self):
        p = build_v4.dog_burnable_chance(self.classic, self.classic["kinds"][0])
        self.assertAlmostEqual(p, 1 / 3, delta=0.02)

    def test_same_mythics_and_cards_as_app3(self):
        self.assertEqual(len(self.classic["cards"]), len(self.moon["cards"]))
        self.assertEqual(self.classic["mythics"], self.moon["mythics"])
        for c in self.classic["cards"]:
            self.assertTrue(c["media"].endswith(f"/cards/{c['card_id']}.svg"))

    def test_paged_read_keeps_the_kinds(self):
        # Contrôle de deploy_testnet.sh avant open_series : en-tête + pages, comme get_series_header/get_series_cards.
        t = self.classic
        pages = [cards_json_bytes(t["cards"][i:i + 200]) for i in range(0, len(t["cards"]), 200)]
        hv = {"header": dict(t, cards=[]), "card_count": len(t["cards"]), "status": "draft", "table_hash": None}
        rep, _ = verify_table_pages(hv, pages, {"attendu": core.table_hash(t).hex()}, draft=True)
        self.assertFalse(rep.errors, rep.errors)

    def _errors(self, mutate):
        t = copy.deepcopy(self.classic)
        mutate(t)
        return vs.validate_table(t).errors

    def test_invalid_kinds_are_refused(self):
        cases = {
            "prix nul": lambda t: t["kinds"][0].update(price="0"),
            "nom vide": lambda t: t["kinds"][0].update(name=""),
            "pool hors table": lambda t: t["kinds"][1]["pool"].append(len(t["cards"])),
            "pool non trié": lambda t: t["kinds"][1]["pool"].reverse(),
            "brûlable impossible": lambda t: t["kinds"][2].update(
                slots=[{"floor": "common", "weights": None, "burnable": True}] * 3),
            "trop de slots": lambda t: t["kinds"][2].update(
                slots=[{"floor": "common", "weights": None, "burnable": False}] * 4),
            "trop de types": lambda t: t.update(kinds=t["kinds"] * 2),
        }
        for name, mutate in cases.items():
            with self.subTest(name):
                self.assertTrue(self._errors(mutate), name)


if __name__ == "__main__":
    unittest.main()
