"""Séries de démo (scripts/series_demo.py) et options de build_series.py (--media-base, --sels, mythic_media).

Lancement : python3 -m unittest discover -s contract/scripts/tests
Aucun vrai secret : les mythiques, sels et noms sont fictifs et écrits dans un dossier temporaire.
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
CONTRACT = os.path.dirname(SCRIPTS)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, SCRIPTS)

import build_series  # noqa: E402
import series_demo  # noqa: E402


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


MAPPING = {
    "reliees": [{"card_id": "leg-a", "rarete": "légendaire", "asset_id": "nep141:a.near", "decimals": 6,
                 "prix_usd_1click": 0.5, "statut": "reliée"}],
    "appoint": [{"card_id": "com-b", "rarete": "commune", "asset_id": "nep141:b.near", "decimals": 18,
                 "prix_usd_1click": 0.0001, "statut": "reliée"},
                {"card_id": "com-dead", "rarete": "commune", "asset_id": "nep141:d.near", "decimals": 18,
                 "prix_usd_1click": 0, "statut": "écartée"}],
}


class ParamsTest(unittest.TestCase):
    def test_price_rounding(self):
        self.assertEqual(series_demo.price_yocto("0.20", "3.62"), 552 * 10 ** 20)    # 0,0552 NEAR
        self.assertEqual(series_demo.price_yocto("0.50", "3.62"), 1381 * 10 ** 20)   # 0,1381 NEAR

    def test_burnables_and_appoint(self):
        b = series_demo.burnables(MAPPING, "0.20", appoint=True)
        self.assertEqual([x["card_id"] for x in b], ["com-b", "leg-a"])
        self.assertEqual(b[1]["amount"], str(400_000))            # 0,20 $ / 0,5 $ × 10⁶
        self.assertEqual(b[0]["amount"], str(2000 * 10 ** 18))    # 0,20 $ / 0,0001 $ × 10¹⁸
        self.assertEqual([x["card_id"] for x in series_demo.burnables(MAPPING, "0.20", appoint=False)], ["leg-a"])

    def test_make_params_keeps_mechanics_and_uses_sim_tables(self):
        ex = load(os.path.join(SCRIPTS, "serie-exemple.json"))
        tv = load(os.path.join(REPO, "sim", "resultats", "serie5", "tables-valeur.json"))
        p = series_demo.make_params(ex, tv, MAPPING, series_demo.SERIES[0], "3.62", "test", "ipfs://bafyX/", True)
        for k in ("gold", "pity", "burn", "rush", "resurrection", "coverage_check"):
            self.assertEqual(p["mechanics"][k], ex["mechanics"][k])
        self.assertEqual(p["mechanics"]["value"]["normale"], tv["value_tables"]["base"]["tiers"])
        self.assertEqual(p["mechanics"]["value"]["multiplicateurs"], tv["split_multipliers"])
        self.assertNotIn("mythique-m1", [b["card_id"] for b in p["burnables"]])
        self.assertEqual(p["media_template"], "ipfs://bafyX/{id}.svg")
        self.assertEqual(p["mythic_media"], "ipfs://bafyX/mythique.svg")
        self.assertEqual(p["price_yocto"], str(552 * 10 ** 20))

    def test_committed_params_are_reproducible(self):
        ex = load(os.path.join(SCRIPTS, "serie-exemple.json"))
        tv = load(os.path.join(REPO, "sim", "resultats", "serie5", "tables-valeur.json"))
        mapping = load(os.path.join(REPO, "docs", "data", "intents-brulables-demo.json"))
        for s in series_demo.SERIES:
            path = os.path.join(SCRIPTS, s["slug"] + ".json")
            if not os.path.exists(path):
                self.skipTest("paramètres absents")
            got = load(path)
            base = got["media_template"][: -len("/{id}.svg")]
            base = None if base == "ipfs://TODO" else base
            again = series_demo.make_params(ex, tv, mapping, s, got["cours_near_usd"], got["cours_source"], base,
                                            got["brulables_appoint"])
            self.assertEqual(again, got)
            self.assertTrue(any(b["card_id"] for b in got["burnables"]))


FAKE_CATALOGUE = [
    {"id": "aaa-com", "section": "catalogue", "rarete": "commune", "nom": "Aaa", "etat": "actif"},
    {"id": "bbb-leg", "section": "catalogue", "rarete": "légendaire", "nom": "Bbb", "etat": "actif"},
    {"id": "mythique-m1", "section": "catalogue", "rarete": "mythique", "nom": "?", "etat": "?"},
]
FAKE_NAME = "Nom Fictif Zzq"


class BuildSeriesOptionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.d = d
        self.cat = os.path.join(d, "cat.json")
        self.myth = os.path.join(d, "mythiques.json")
        self.params = os.path.join(d, "params.json")
        with open(self.cat, "w") as f:
            json.dump(FAKE_CATALOGUE, f)
        with open(self.myth, "w") as f:
            json.dump({"mythiques": [{"id": "fictif-zzq", "nom": FAKE_NAME, "catalogue_id": "mythique-m1"}]}, f)
        p = load(os.path.join(SCRIPTS, "serie-exemple.json"))
        p.pop("mechanics")
        p.update(slug="t", burnables=[{"card_id": "aaa-com", "asset_id": "nep141:a.near", "amount": "5"}],
                 card_weights={"legendary": 1, "epic": 1, "rare": 1, "common": 1})
        with open(self.params, "w") as f:
            json.dump(p, f)
        self.sel = "11" * 32
        self.old = os.path.join(d, "old-secrets.json")
        with open(self.old, "w") as f:
            json.dump([{"mythic_index": 0, "card_id": "fictif-zzq", "sel": self.sel, "content": {}}], f)

    def tearDown(self):
        self.tmp.cleanup()

    def run_build(self, *extra):
        out = os.path.join(self.d, "out")
        args = [self.params, "--catalogue", self.cat, "--mythiques", self.myth, "--out", out,
                "--secrets", os.path.join(self.d, "sec", "t.json"), *extra]
        with contextlib.redirect_stdout(io.StringIO()):
            build_series.main(args)
        return out, load(os.path.join(out, "table.json"))

    def test_media_base_and_reused_salt(self):
        out, table = self.run_build("--media-base", "ipfs://bafyTEST/", "--sels", self.old)
        self.assertEqual({c["card_id"]: c["media"] for c in table["cards"]},
                         {"aaa-com": "ipfs://bafyTEST/aaa-com.svg", "bbb-leg": "ipfs://bafyTEST/bbb-leg.svg"})
        sec = load(os.path.join(self.d, "sec", "t.json"))
        self.assertEqual(sec[0]["sel"], self.sel)
        self.assertEqual(sec[0]["content"]["media"], "ipfs://bafyTEST/mythique.svg")   # visuel « ? » commun
        want = hashlib.sha256(b"fictif-zzq" + bytes.fromhex(self.sel)).hexdigest()
        self.assertEqual(table["mythics"][0]["commitment"], want)
        for name in os.listdir(out):
            with open(os.path.join(out, name), encoding="utf-8") as f:
                txt = f.read()
            self.assertNotIn(FAKE_NAME, txt)
            self.assertNotIn("fictif-zzq", txt)
        # Même sels, même contenu : même table d'une exécution à l'autre.
        _, again = self.run_build("--media-base", "ipfs://bafyTEST", "--sels", self.old)
        self.assertEqual(again, table)

    def test_sels_and_new_secrets_are_exclusive(self):
        with self.assertRaises(SystemExit):
            self.run_build("--sels", self.old, "--new-secrets")

    def test_missing_salt_is_refused(self):
        with open(self.old, "w") as f:
            json.dump([{"mythic_index": 0, "card_id": "autre", "sel": self.sel}], f)
        with self.assertRaises(SystemExit):
            self.run_build("--sels", self.old)


if __name__ == "__main__":
    unittest.main()
