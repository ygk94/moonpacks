"""Valeur aléatoire par pack et gold pack à planchers (décisions du 11/11) : règles recalculées en
Python, événements réels du sandbox falsifiés, et options de `contract/scripts/build_series.py`
(fichier secret des mythiques, `--tables-valeur`)."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from memaster_verifier import core, verify

from tests import fake_secrets

VEC = Path(__file__).parent / "vectors"
CONTRACT = Path(__file__).resolve().parents[2] / "contract"
CATALOGUE = CONTRACT.parent / "docs" / "data" / "catalogue-v2.json"

with open(VEC / "sandbox_mech_vectors.json", encoding="utf-8") as f:
    SBX = json.load(f)

MULT = {"mythic": 0, "legendary": 20, "epic": 5, "rare": 2, "common": 1}


def items():
    return copy.deepcopy([(e["event"], e["data"][0]) for e in SBX["events"]])


class Rules(unittest.TestCase):
    def test_fallback_order(self):
        self.assertEqual(core.fallback_order("epic", "common"), ["epic", "rare", "common", "legendary", "mythic"])
        self.assertEqual(core.fallback_order("legendary", "legendary"), ["legendary", "mythic", "epic", "rare", "common"])
        self.assertEqual(core.fallback_order("mythic", "legendary"), ["mythic", "legendary", "epic", "rare", "common"])
        self.assertEqual(core.fallback_order("epic", "rare"), ["epic", "rare", "legendary", "mythic", "common"])

    def test_gold_slot_weights_truncate_below_floor(self):
        base = {"mythic": 2, "legendary": 20, "epic": 180, "rare": 800, "common": 8998}
        w = core.gold_slot_weights(base, {"floor": "epic", "weights": None, "burnable": False})
        self.assertEqual(w, {"mythic": 2, "legendary": 20, "epic": 180, "rare": 0, "common": 0})
        own = {"mythic": 20, "legendary": 80, "epic": 0, "rare": 0, "common": 0}
        self.assertIs(core.gold_slot_weights(base, {"floor": "legendary", "weights": own, "burnable": False}), own)

    def test_split_rounding(self):
        total = 10**24 + 7
        slots = [("common", True), ("epic", True), ("rare", False), ("epic", True), ("common", True)]
        a = core.split_value(total, slots, MULT)
        self.assertEqual(sum(x for x in a if x is not None), total)
        self.assertEqual(a[3], total * 5 // 12)
        self.assertGreater(a[1], a[3], "le reste va au premier plus fort multiplicateur")
        self.assertIsNone(a[2])
        self.assertEqual(core.split_value(1, [("common", True), ("legendary", True)], MULT), [0, 1])
        self.assertEqual(core.split_value(5, [("rare", False)], MULT), [None])

    def test_single_tier(self):
        acc = bytes(32)
        self.assertEqual(core.value_tier([[7_500, 9]], acc)[1:], (0, 7_500))
        self.assertEqual(core.value_total(10**23 + 3, 7_777), (10**23 + 3) * 7_777 // 10_000)

    def test_exhausted_legendary_climbs_then_falls_below_floor(self):
        """Gold, emplacement 5 (plancher légendaire) : légendaire épuisée → mythique ; les deux
        épuisées → épique (sous le plancher)."""
        table = {
            "cards_per_pack": 1,
            "rarity_weights": {"mythic": 0, "legendary": 1, "epic": 1, "rare": 1, "common": 1},
            "cards": [
                {"card_id": "l", "rarity": "legendary", "weight": 1, "cap": 0, "backing": None},
                {"card_id": "e", "rarity": "epic", "weight": 1, "cap": None, "backing": None},
                {"card_id": "c", "rarity": "common", "weight": 1, "cap": None, "backing": {"asset_id": "a", "amount": "1"}},
            ],
            "mythics": [{"commitment": "0" * 64, "content_hash": "1" * 64, "weight": 1, "cap": 1}],
        }
        w = {"mythic": 0, "legendary": 1, "epic": 0, "rare": 0, "common": 0}
        backed = [False, False, True]
        d = core.draw_slot_rule(table, [0, 0, 0], [0], bytes(32), 4, w, "legendary", False, backed)
        self.assertEqual((d.rolled_rarity, d.final_rarity, d.kind), ("legendary", "mythic", "mythic"))
        d = core.draw_slot_rule(table, [0, 0, 0], [1], bytes(32), 4, w, "legendary", False, backed)
        self.assertEqual(d.final_rarity, "epic")
        # Parmi les brûlables : seule la commune l'est.
        d = core.draw_slot_rule(table, [0, 0, 0], [1], bytes(32), 4, w, "legendary", True, backed)
        self.assertEqual((d.final_rarity, d.index), ("common", 2))


class SandboxValue(unittest.TestCase):
    """Événements réels de `mechanics_end_to_end` (gold pack v2 sans mythique, table de valeur)."""

    def replay(self, its):
        reports, st = verify.replay_series(json.loads(SBX["table_raw"]), its)
        return [r for r in reports if not r.ok], reports

    def test_value_and_gold_packs_are_replayed(self):
        bad, reports = self.replay(items())
        self.assertFalse(bad, "\n".join(r.render() for r in bad))
        lines = [x for r in reports for x in r.ok_lines]
        self.assertTrue(any(x.startswith("valeur : roll(acc, 0, 3)") and "table gold" in x for x in lines))
        self.assertTrue(any("[parmi les brûlables]" in x for x in lines))
        self.assertTrue(any("[plancher epic]" in x for x in lines))
        golds = [e for n, e in items() if n == "pack_revealed" and e["mechanics"]["mode"] == "gold"]
        self.assertTrue(golds)
        for e in golds:
            self.assertEqual(len(e["draws"]), 5)
            self.assertNotIn("common", [d["final_rarity"] for d in e["draws"]])

    def _tamper(self, change, mode=None):
        its = items()
        for n, e in its:
            if n == "pack_revealed" and (mode is None or e["mechanics"]["mode"] == mode):
                change(e)
                break
        return self.replay(its)[0]

    def test_tampered_value_is_detected(self):
        def bps(e):
            e["mechanics"]["value"]["bps"] += 1
        def amounts(e):
            a = e["mechanics"]["value"]["amounts"]
            i = next(i for i, x in enumerate(a) if x is not None)
            a[i] = str(int(a[i]) + 1)
        def tier(e):
            e["mechanics"]["value"]["tier"] += 1
        for f in (bps, amounts, tier):
            self.assertTrue(self._tamper(f), f.__name__)

    def test_tampered_gold_slot_is_detected(self):
        def ch(e):
            d = e["draws"][4]
            d["final_rarity"] = "epic"
        self.assertTrue(self._tamper(ch, "gold"))

    def test_missing_slot_is_detected(self):
        def ch(e):
            e["draws"].pop()
        self.assertTrue(self._tamper(ch))

    def test_partial_check_without_state(self):
        """Sans rejeu : `rarity_roll` avec les poids de chaque emplacement (gold), valeur tirée."""
        table = json.loads(SBX["table_raw"])
        gold = next(e for n, e in items() if n == "pack_revealed" and e["mechanics"]["mode"] == "gold")
        rep = verify.verify_pack(gold, table, None, None)
        self.assertTrue(rep.ok, rep.render())
        self.assertTrue(any(x.startswith("valeur :") for x in rep.ok_lines))


_FAKE_DIR = tempfile.mkdtemp(prefix="memaster-fake-mythics-")
FAKE_MYTHICS = fake_secrets.write_fake_mythics(_FAKE_DIR)


def run_script(*args):
    """build_series.py avec un faux fichier de mythiques (jamais le fichier secret), sauf
    `--mythiques` explicite."""
    extra = [] if "--mythiques" in args else ["--mythiques", str(FAKE_MYTHICS)]
    return subprocess.run(
        [sys.executable, "-I", str(CONTRACT / "scripts" / "build_series.py"), str(CONTRACT / "scripts" / "serie-exemple.json"), *extra, *args],
        capture_output=True, text=True,
    )


class BuildSeriesScript(unittest.TestCase):
    """Fichier secret des mythiques (et repli), tables de valeur."""

    @classmethod
    def setUpClass(cls):
        with open(CATALOGUE, encoding="utf-8") as f:
            cls.catalogue = json.load(f)

    def out(self, d, name):
        return ["--out", str(Path(d) / name), "--secrets", str(Path(d) / "secrets" / f"{name}.json")]

    def test_mythic_file_and_fallback(self):
        """Fichier des vrais noms (faux noms ici), repli sur un champ `secret` du catalogue, format
        liste avec `catalogue_id`, fichier absent ou incomplet, garde-fou anti-fuite."""
        with tempfile.TemporaryDirectory() as d:
            secrets = fake_secrets.fake_mythics()
            sf = Path(d) / "mythiques.json"
            sf.write_text(json.dumps(secrets, ensure_ascii=False), encoding="utf-8")
            cat = Path(d) / "cat.json"
            cat.write_text(json.dumps([{k: v for k, v in c.items() if k != "secret"} for c in self.catalogue], ensure_ascii=False), encoding="utf-8")
            r = run_script("--catalogue", str(cat), "--mythiques", str(sf), *self.out(d, "a"))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn("repli", r.stderr)
            # Même table par le repli sur le champ secret (mêmes sels réutilisés).
            cat_secret = Path(d) / "cat-secret.json"
            cat_secret.write_text(json.dumps([dict(c, secret=secrets[c["id"]]) if c["id"] in secrets else c for c in self.catalogue], ensure_ascii=False), encoding="utf-8")
            (Path(d) / "secrets" / "b.json").write_bytes((Path(d) / "secrets" / "a.json").read_bytes())
            r2 = run_script("--catalogue", str(cat_secret), "--mythiques", str(Path(d) / "absent.json"), *self.out(d, "b"))
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn("repli", r2.stderr)
            ha = (Path(d) / "a" / "table_hash.txt").read_text()
            self.assertEqual(ha, (Path(d) / "b" / "table_hash.txt").read_text())
            # Aucun vrai nom dans les sorties publiques.
            for name in secrets.values():
                for p in (Path(d) / "a").iterdir():
                    self.assertNotIn(json.dumps(name["nom"], ensure_ascii=False), p.read_text(encoding="utf-8"))
            # Liste avec catalogue_id : acceptée aussi, même table.
            sf.write_text(json.dumps([dict(v, catalogue_id=k) for k, v in secrets.items()], ensure_ascii=False), encoding="utf-8")
            (Path(d) / "secrets" / "c.json").write_bytes((Path(d) / "secrets" / "a.json").read_bytes())
            r3 = run_script("--catalogue", str(cat), "--mythiques", str(sf), *self.out(d, "c"))
            self.assertEqual(r3.returncode, 0, r3.stderr)
            self.assertEqual(ha, (Path(d) / "c" / "table_hash.txt").read_text())
            # Ni fichier ni champ secret : message clair.
            r4 = run_script("--catalogue", str(cat), "--mythiques", str(Path(d) / "absent.json"), *self.out(d, "e"))
            self.assertNotEqual(r4.returncode, 0)
            self.assertIn("Vrais noms des mythiques introuvables", r4.stderr)
            # Fichier incomplet : refusé.
            sf.write_text(json.dumps({k: v for k, v in list(secrets.items())[:1]}, ensure_ascii=False), encoding="utf-8")
            r5 = run_script("--catalogue", str(cat), "--mythiques", str(sf), *self.out(d, "f"))
            self.assertNotEqual(r5.returncode, 0)
            self.assertIn("mythiques absentes", r5.stderr)
            # Garde-fou : un vrai nom (ici fictif) recopié dans une carte visible est refusé.
            leak = Path(d) / "leak.json"
            params = json.loads((CONTRACT / "scripts" / "serie-exemple.json").read_text(encoding="utf-8"))
            first_visible = next(c["id"] for c in self.catalogue if c.get("section") == "catalogue" and c["rarete"] != "mythique")
            params.setdefault("card_overrides", {})[first_visible] = {"title": fake_secrets.FAKE[0]}
            leak.write_text(json.dumps(params, ensure_ascii=False), encoding="utf-8")
            sf.write_text(json.dumps(secrets, ensure_ascii=False), encoding="utf-8")
            (Path(d) / "secrets" / "g.json").write_bytes((Path(d) / "secrets" / "a.json").read_bytes())
            r6 = subprocess.run([sys.executable, "-I", str(CONTRACT / "scripts" / "build_series.py"), str(leak), "--catalogue", str(cat),
                                 "--mythiques", str(sf), *self.out(d, "g")], capture_output=True, text=True)
            self.assertNotEqual(r6.returncode, 0)
            self.assertIn("FUITE", r6.stderr)

    def test_value_tables_option(self):
        with tempfile.TemporaryDirectory() as d:
            tv = {"normale": [[2000, 1], [20000, 1]], "gold": [[30000, 1]], "rush": [[7000, 1]],
                  "multiplicateurs": {"commune": 1, "rare": 1.5, "épique": 4, "légendaire": 10}}
            f = Path(d) / "tv.json"
            f.write_text(json.dumps(tv, ensure_ascii=False), encoding="utf-8")
            r = run_script("--tables-valeur", str(f), *self.out(d, "v"))
            self.assertEqual(r.returncode, 0, r.stderr)
            m = json.loads((Path(d) / "v" / "manifest.json").read_text(encoding="utf-8"))
            v = m["mechanics"]["value"]
            self.assertEqual(v["normal"], [[2000, 1], [20000, 1]])
            # Décimales : tous les multiplicateurs × 1 000.
            self.assertEqual(v["multipliers"], {"mythic": 0, "legendary": 10_000, "epic": 4_000, "rare": 1_500, "common": 1_000})
            self.assertAlmostEqual(m["coverage"]["base"], 1.1)
            table = json.loads((Path(d) / "v" / "table.json").read_text(encoding="utf-8"))
            self.assertEqual(core.table_hash(table).hex(), m["table_hash"])
            # Bornes du contrat appliquées hors ligne.
            for bad, msg in (({"normale": [[1999, 1]]}, "hors bornes"), ({"rush": [[9000, 1]]}, "table de valeur rush refusée"),
                             ({"multiplicateurs": {"mythique": 1, "commune": 1, "rare": 1, "épique": 1, "légendaire": 1}}, "mythique = 0")):
                f.write_text(json.dumps(dict(tv, **bad), ensure_ascii=False), encoding="utf-8")
                r = run_script("--tables-valeur", str(f), *self.out(d, "w"))
                self.assertNotEqual(r.returncode, 0)
                self.assertIn(msg, r.stderr)

    def test_example_tables_are_provisional_20_to_200_mean_75(self):
        with open(CONTRACT / "scripts" / "serie-exemple.json", encoding="utf-8") as f:
            v = json.load(f)["mechanics"]["value"]
        bps = [b for b, _ in v["normale"]]
        self.assertEqual((min(bps), max(bps)), (2_000, 20_000))
        self.assertAlmostEqual(sum(b * w for b, w in v["normale"]) / sum(w for _, w in v["normale"]), 7_500)


if __name__ == "__main__":
    unittest.main()
