"""Validateur de série (`contract/scripts/validate_series.py`) : une table produite par
`build_series.py` passe ; chaque table que le contrat refuserait est refusée ; dossier de lots,
préimages des mythiques et fuites dans les fichiers publics. Faux noms de mythiques seulement."""

import copy
import os
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import fake_secrets

CONTRACT = fake_secrets.CONTRACT
sys.path.insert(0, str(CONTRACT / "scripts"))

import validate_series as vs  # noqa: E402


def build(d, params=None, names=None, reuse=None):
    """build_series.py sur le catalogue v2 (faux noms) ; renvoie (résultat, dossier, préimages, noms).
    `reuse` : fichier de préimages existant (sels réutilisés)."""
    pfile = CONTRACT / "scripts" / "serie-exemple.json"
    if params is not None:
        pfile = Path(d) / "params.json"
        pfile.write_text(json.dumps(params, ensure_ascii=False), encoding="utf-8")
    if names is None:
        names = fake_secrets.write_fake_mythics(d)
    else:
        p = Path(d) / "noms.json"
        p.write_text(json.dumps(names, ensure_ascii=False), encoding="utf-8")
        names = p
    out, sec = Path(d) / "out", Path(d) / "secrets" / "s.json"
    if reuse is not None:
        sec.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(reuse, sec)
    r = subprocess.run(
        [sys.executable, "-I", str(CONTRACT / "scripts" / "build_series.py"), str(pfile), "--mythiques", str(names),
         "--out", str(out), "--secrets", str(sec)],
        capture_output=True, text=True,
    )
    return r, out, sec, names


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="memaster-validate-")
        r, cls.out, cls.sec, cls.names = build(cls.tmp)
        assert r.returncode == 0, r.stderr
        cls.table = json.loads((cls.out / "table.json").read_text(encoding="utf-8"))
        cls.secrets = json.loads(cls.sec.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)


class ValidSeries(Base):
    def test_built_series_passes(self):
        res, summary = vs.validate(str(self.out), str(self.sec), str(self.names))
        self.assertTrue(res.ok, res.errors)
        self.assertEqual(summary["cards"], len(self.table["cards"]))
        self.assertAlmostEqual(summary["value_means"]["normal"], 0.75)
        self.assertLessEqual(summary["value_means"]["rush"], 0.8)
        self.assertAlmostEqual(sum(summary["rarity_probabilities"].values()), 1.0)

    def test_cli_exit_codes(self):
        cli = [sys.executable, "-I", str(CONTRACT / "scripts" / "validate_series.py")]
        ok = subprocess.run([*cli, str(self.out), "--secrets", str(self.sec), "--mythiques", str(self.names)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn("OK :", ok.stdout)
        with tempfile.TemporaryDirectory() as d:
            t = copy.deepcopy(self.table)
            t["cards_per_pack"] = 11
            p = Path(d) / "t.json"
            p.write_text(json.dumps(t), encoding="utf-8")
            bad = subprocess.run([*cli, str(p), "--json"], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("cards_per_pack", json.loads(bad.stdout)["errors"][0])

    def test_testnet_table_of_app2_passes(self):
        """Table réellement ouverte sur app2 (docs/data/testnet-2026-11-11-v2) : règles du contrat."""
        t = json.loads((CONTRACT.parent / "docs" / "data" / "testnet-2026-11-11-v2" / "table.json").read_text(encoding="utf-8"))
        res = vs.validate_table(t)
        self.assertTrue(res.ok, res.errors)
        h = (CONTRACT.parent / "docs" / "data" / "testnet-2026-11-11-v2" / "table_hash.txt").read_text().strip()
        self.assertEqual(vs.core.table_hash(t).hex(), h)


class RejectedTables(Base):
    """Une table que le contrat refuse (`src/series.rs`, `src/mechanics.rs`) est refusée hors ligne."""

    def rejected(self, mutate, msg):
        t = copy.deepcopy(self.table)
        mutate(t)
        res = vs.validate_table(t)
        if res.ok:
            res2 = vs.Result()
            vs.economics(t, res2, 0.8, 1.0)
            res = res2
        self.assertFalse(res.ok, f"acceptée (attendu : {msg})")
        self.assertTrue(any(msg in e for e in res.errors), f"{msg} absent de {res.errors}")

    def mech(self, t):
        return t["mechanics"]

    def test_header(self):
        self.rejected(lambda t: t.update(name="x" * 65), "name : longueur invalide")
        self.rejected(lambda t: t.update(price="0"), "Le prix doit être > 0")
        self.rejected(lambda t: t.update(price=1000), "Le prix doit être > 0")
        self.rejected(lambda t: t.update(cards_per_pack=0), "cards_per_pack")
        self.rejected(lambda t: t.update(cards_per_pack=11), "cards_per_pack")
        self.rejected(lambda t: t["rarity_weights"].update(mythic=0, legendary=0, epic=0, rare=0, common=0), "Poids de rareté nuls")
        self.rejected(lambda t: [m.update(weight=0) for m in t["mythics"]], "Poids mythique sans engagement")
        self.rejected(lambda t: t["mythics"][0].update(cap=500), "plafond de mythique hors bornes")
        self.rejected(lambda t: t["mythics"][0].update(cap=0), "plafond de mythique hors bornes")
        self.rejected(lambda t: t["mythics"][1].update(commitment=t["mythics"][0]["commitment"]), "engagement en double")
        self.rejected(lambda t: t["mythics"][1].update(content_hash=t["mythics"][0]["content_hash"]), "content_hash en double")
        self.rejected(lambda t: t["mythics"][0].update(commitment=t["mythics"][0]["commitment"].upper()), "hex minuscules")
        self.rejected(lambda t: t["mythics"][0].update(nom="?"), "rien d'autre")
        self.rejected(lambda t: t.update(royalties=[{"account_id": "a.testnet", "bps": 6000}]), "Redevances > 50 %")
        self.rejected(lambda t: t.update(royalties=[{"account_id": "a.testnet", "bps": 1}] * 11), "Trop de redevances")
        self.rejected(lambda t: t.update(mythics=t["mythics"] * 7), "Trop de mythiques")

    def test_field_order_is_part_of_the_hash(self):
        def swap(t):
            items = list(t.items())
            t.clear()
            t.update([items[1], items[0], *items[2:]])
        self.rejected(swap, "dans cet ordre")

    def test_cards_and_coverage(self):
        self.rejected(lambda t: t["cards"][0].update(card_id="x" * 65), "card_id : longueur invalide")
        self.rejected(lambda t: t["cards"][0].update(title=""), "title : longueur invalide")
        self.rejected(lambda t: t["cards"][0].update(rarity="mythic"), "les mythiques passent par des engagements")
        self.rejected(lambda t: t["cards"][1].update(card_id=t["cards"][0]["card_id"]), "card_id en double")
        self.rejected(lambda t: t["cards"][0].update(backing={"asset_id": "a", "amount": "0"}), "amount doit être")
        self.rejected(lambda t: t["rarity_weights"].update(legendary=0) or self.mech(t).update(rush=None, gold=None, pity=None), "rareté de poids nul")
        self.rejected(lambda t: [c.update(cap=1) for c in t["cards"] if c["rarity"] == "common"], "commune sans plafond")
        self.rejected(lambda t: [c.update(backing=None) for c in t["cards"]], "Brûlable garantie")
        self.rejected(lambda t: [c.update(weight=0) for c in t["cards"] if c["rarity"] == "epic"], "Rareté epic sans carte")

    def test_mechanics(self):
        self.rejected(lambda t: self.mech(t).update(gold=None), "pity exige gold")
        self.rejected(lambda t: self.mech(t)["burn"].update(floor_bps=20_000), "burn.floor_bps")
        self.rejected(lambda t: self.mech(t)["burn"].update(prior_k=2_000_000), "burn.prior_k")
        self.rejected(lambda t: self.mech(t)["pity"].update(p0_ppb=2 * 10**9), "ppb")
        self.rejected(lambda t: self.mech(t)["pity"].update(n_max=0), "n_max")
        self.rejected(lambda t: self.mech(t)["pity"].update(p0_ppb=50_000, p_max_ppb=40_000), "p0_ppb ≤ p_max_ppb")
        self.rejected(lambda t: self.mech(t)["pity"].update(p0_ppb=0, p_max_ppb=0, n_max=None), "inatteignable")
        r = lambda t: self.mech(t)["rush"]  # noqa: E731
        self.rejected(lambda t: r(t).update(window_blocks=r(t)["bucket_blocks"] + 1), "multiples de bucket_blocks")
        self.rejected(lambda t: r(t).update(min_packs=0), "min_packs")
        self.rejected(lambda t: r(t).update(max_per_account=0), "max_per_account")
        self.rejected(lambda t: r(t).update(ratio_bps=9_999), "ratio_bps ≥ 10 000")
        self.rejected(lambda t: r(t).update(ratio_bps=10_000 * r(t)["baseline_blocks"] // r(t)["window_blocks"]), "inatteignable")
        self.rejected(lambda t: r(t).update(baseline_blocks=r(t)["bucket_blocks"] * 97), "1 à 96 seaux")
        self.rejected(lambda t: r(t).update(window_blocks=r(t)["baseline_blocks"]), "plus courte")
        self.rejected(lambda t: r(t).update(duration_blocks=0), "durée")
        self.rejected(lambda t: self.mech(t)["gold"].update(slots=[]), "gold.slots : 1 à 10")
        self.rejected(lambda t: self.mech(t)["gold"]["slots"][0].update(floor="common", weights={"mythic": 0, "legendary": 0, "epic": 0, "rare": 0, "common": 0}), "poids nuls")
        self.rejected(lambda t: self.mech(t)["gold"]["slots"][0].update(floor="epic", weights={"mythic": 0, "legendary": 1, "epic": 1, "rare": 1, "common": 0}), "sous le plancher")
        self.rejected(lambda t: self.mech(t)["resurrection"].update(eligible=[5, 5]), "strictement croissants")
        self.rejected(lambda t: self.mech(t)["resurrection"].update(eligible=[10_000]), "index de carte inconnu")
        common = next(i for i, c in enumerate(self.table["cards"]) if c["rarity"] == "common")
        self.rejected(lambda t: self.mech(t)["resurrection"].update(eligible=[common]), "ni épique ni légendaire")
        backed = next(i for i, c in enumerate(self.table["cards"]) if c["backing"] and c["rarity"] in ("epic", "legendary"))
        self.rejected(lambda t: self.mech(t)["resurrection"].update(eligible=[backed]), "déjà adossée")

    def test_value(self):
        v = lambda t: self.mech(t)["value"]  # noqa: E731
        self.rejected(lambda t: v(t).update(normal=[[1_999, 1]]), "value.normal")
        self.rejected(lambda t: v(t).update(normal=[[20_001, 1]]), "value.normal")
        self.rejected(lambda t: v(t).update(normal=[[7_500, 0]]), "poids nuls interdits")
        self.rejected(lambda t: v(t).update(gold=[]), "paliers")
        self.rejected(lambda t: v(t).update(rush=[[1_000_001, 1]]), "value.rush")
        self.rejected(lambda t: v(t)["multipliers"].update(mythic=1), "mythic = 0")
        self.rejected(lambda t: v(t)["multipliers"].update(rare=0), "multipliers.rare")
        self.rejected(lambda t: t.update(price=str(2**127)), "dépassement de u128")
        # Valeur moyenne : rush > 80 % et normale > 100 % refusées (contrôle hors chaîne).
        self.rejected(lambda t: v(t).update(rush=[[9_000, 1]]), "table rush")
        self.rejected(lambda t: v(t).update(normal=[[15_000, 1]]), "table normale")


class OutDirAndSecrets(Base):
    def copy_out(self, d):
        dst = Path(d) / "out"
        shutil.copytree(self.out, dst)
        return dst

    def test_missing_or_reordered_batch_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            o = self.copy_out(d)
            p = o / "append_series_cards.03.json"
            a = json.loads(p.read_text(encoding="utf-8"))
            a["cards"] = a["cards"][:-1]
            p.write_text(json.dumps(a), encoding="utf-8")
            res, _ = vs.validate(str(o))
            self.assertTrue(any("lot manquant" in e for e in res.errors), res.errors)
        with tempfile.TemporaryDirectory() as d:
            o = self.copy_out(d)
            m = json.loads((o / "manifest.json").read_text(encoding="utf-8"))
            c = m["calls"]
            c[1], c[2] = c[2], c[1]
            (o / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
            res, _ = vs.validate(str(o))
            self.assertTrue(any("non strictement croissants" in e for e in res.errors), res.errors)
        with tempfile.TemporaryDirectory() as d:
            o = self.copy_out(d)
            (o / "table_hash.txt").write_text("00" * 32 + "\n")
            res, _ = vs.validate(str(o))
            self.assertTrue(any("table_hash.txt" in e for e in res.errors), res.errors)

    def check_secrets(self, mutate, msg):
        s = copy.deepcopy(self.secrets)
        mutate(s)
        res = vs.Result()
        vs.check_preimages(self.table, s, res)
        self.assertTrue(any(msg in e for e in res.errors), f"{msg} absent de {res.errors}")

    def test_preimages_must_be_revealable(self):
        res = vs.Result()
        vs.check_preimages(self.table, self.secrets, res)
        self.assertTrue(res.ok, res.errors)
        self.check_secrets(lambda s: s[0]["content"].update(title="T" * 65), "titre")
        self.check_secrets(lambda s: s[0].update(card_id="c" * 65), "card_id")
        self.check_secrets(lambda s: s[0]["content"].update(media="u" * 257), "media trop long")
        self.check_secrets(lambda s: s[0]["content"].update(backing={"asset_id": "a", "amount": "0"}), "amount")
        self.check_secrets(lambda s: s[0].update(sel="ab" * 16), "sel de 32 octets")
        self.check_secrets(lambda s: s[1].update(sel=s[0]["sel"]), "sel réutilisé")
        self.check_secrets(lambda s: s[0]["content"].update(title="Autre"), "content_hash")
        self.check_secrets(lambda s: s.pop(), "préimages pour")

    def test_build_series_refuses_unrevealable_mythic_and_contract_rejects(self):
        """Avant la revue, build_series.py acceptait ces paramètres (refus seulement on-chain)."""
        base = json.loads((CONTRACT / "scripts" / "serie-exemple.json").read_text(encoding="utf-8"))
        cases = [
            (lambda p: p["mechanics"].pop("gold"), "pity exige gold"),
            (lambda p: p["mechanics"]["burn"].update(floor_bps=20_000), "burn.floor_bps"),
            (lambda p: p["mechanics"]["rush"].update(min_packs=0), "min_packs"),
            (lambda p: p.update(cards_per_pack=11), "cards_per_pack"),
            (lambda p: p.update(name="N" * 100), "name"),
            (lambda p: p["mythic"].update(cap=500), "plafond de mythique"),
        ]
        for mutate, msg in cases:
            with self.subTest(msg=msg), tempfile.TemporaryDirectory() as d:
                p = copy.deepcopy(base)
                mutate(p)
                # Sels réutilisés : gen_mythics.py n'est pas relancé, seul le validateur contrôle.
                r, *_ = build(d, p, reuse=self.sec)
                self.assertNotEqual(r.returncode, 0, f"acceptée : {msg}")
                self.assertIn(msg, r.stderr)
                self.assertIn("table refusée", r.stderr)
        # Mythique dont le card_id ou le titre dépasse les bornes de reveal_mythic : jamais révélable.
        names = fake_secrets.fake_mythics()
        first = next(iter(names))
        for field, value, msg in (("id", "y" * 90, "card_id de 1 à 64 octets"), ("nom", "N" * 120, "titre de 1 à 64 octets")):
            with self.subTest(msg=msg), tempfile.TemporaryDirectory() as d:
                n = copy.deepcopy(names)
                n[first][field] = value
                r, *_ = build(d, names=n)
                self.assertNotEqual(r.returncode, 0, f"acceptée : {msg}")
                self.assertIn(msg, r.stderr)
                self.assertNotIn("Traceback", r.stderr)
                self.assertNotIn(value, r.stderr, "le secret n'est pas recopié")


    def test_build_series_input_errors_are_clear(self):
        """Montant en nombre flottant (1e24) ou en notation scientifique, secrets sous la sortie publique."""
        base = json.loads((CONTRACT / "scripts" / "serie-exemple.json").read_text(encoding="utf-8"))
        for amount in (1e24, "1e24", True, "-5"):
            with self.subTest(amount=amount), tempfile.TemporaryDirectory() as d:
                p = copy.deepcopy(base)
                p["burnables"][0]["amount"] = amount
                r, *_ = build(d, p, reuse=self.sec)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("amount invalide", r.stderr)
                self.assertNotIn("Traceback", r.stderr)
        with tempfile.TemporaryDirectory() as d:
            names = fake_secrets.write_fake_mythics(d)
            r = subprocess.run(
                [sys.executable, "-I", str(CONTRACT / "scripts" / "build_series.py"), str(CONTRACT / "scripts" / "serie-exemple.json"),
                 "--mythiques", str(names), "--out", str(Path(d) / "out"), "--secrets", str(Path(d) / "out" / "s" / "s.json")],
                capture_output=True, text=True,
            )
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("--secrets ne doit pas être sous --out", r.stderr)
            self.assertFalse((Path(d) / "out" / "s" / "s.json").exists(), "aucune préimage écrite dans la sortie publique")

class Leaks(Base):
    def scan(self, files, secrets=None):
        res = vs.Result()
        vs.scan_leaks([str(f) for f in files], secrets if secrets is not None else self.secrets,
                      vs.load_names(str(self.names)), res, rel="/")
        return res

    def test_build_output_has_no_secret(self):
        res = self.scan(sorted(self.out.iterdir()))
        self.assertTrue(res.ok, res.errors)

    def test_secrets_and_names_are_detected_without_being_printed(self):
        name, ticker = fake_secrets.FAKE[0], fake_secrets.FAKE_TICKERS[1]
        with tempfile.TemporaryDirectory() as d:
            f = {k: Path(d) / k for k in ("sel.txt", "doc.md", "ok.md", "card.json", "visible.json", "events.jsonl")}
            f["sel.txt"].write_text(f"préimage : {self.secrets[2]['sel']}\n")
            f["doc.md"].write_text(f"Les mythiques sont {name} et {ticker}.\n")
            f["ok.md"].write_text(f"{name} 2.0 est une commune ; {ticker} aussi.\nmythique : ?\n")
            f["card.json"].write_text(json.dumps({"rarity": "mythic", "title": f"{name} Coin"}))
            f["visible.json"].write_text(json.dumps([{"rarity": "common", "title": f"Baby {name}"}, {"rarity": "mythic", "title": "?"}]))
            f["events.jsonl"].write_text(json.dumps({"mythic_index": 0, "content": {"title": ticker}}) + "\n")
            res = self.scan(f.values())
            joined = "\n".join(res.errors)
            self.assertIn("sel de la mythique 2", joined)
            self.assertIn("doc.md:1", joined)
            self.assertIn("card.json", joined)
            self.assertIn("events.jsonl", joined)
            self.assertNotIn("ok.md", joined)
            self.assertNotIn("visible.json", joined)
            for x in (name, ticker, self.secrets[2]["sel"]):
                self.assertNotIn(x, joined, "le message ne recopie pas le secret")
            # Titre engagé recopié tel quel (chaîne JSON) : fuite, même sans le mot « mythique ».
            f["ok.md"].write_text(json.dumps({"title": self.secrets[0]["content"]["title"]}))
            self.assertIn("titre de la mythique 0", "\n".join(self.scan([f["ok.md"]]).errors))

    def test_common_mythic_media_is_not_a_leak(self):
        # build_series.py --media-base : le visuel « ? » commun est dans le contenu engagé de chaque
        # mythique et dans manifest.json["mythic_media"]. Il est public : ce n'est pas une fuite, mais
        # un média propre à une mythique en reste une.
        common = "ipfs://bafyX/mythique.svg"
        secrets = json.loads(json.dumps(self.secrets))
        for s in secrets:
            s["content"]["media"] = common
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "manifest.json"
            f.write_text(json.dumps({"mythic_media": common}))
            res = vs.Result()
            vs.scan_leaks([str(f)], secrets, [], res, rel="/", public_media=[common])
            self.assertTrue(res.ok, res.errors)
            res = vs.Result()
            vs.scan_leaks([str(f)], secrets, [], res, rel="/")
            self.assertIn("media de la mythique 0", "\n".join(res.errors))
            secrets[1]["content"]["media"] = "ipfs://bafyX/propre.svg"
            f.write_text(json.dumps({"mythic_media": common, "x": "ipfs://bafyX/propre.svg"}))
            res = vs.Result()
            vs.scan_leaks([str(f)], secrets, [], res, rel="/", public_media=[common])
            self.assertEqual(res.errors, ["FUITE : media de la mythique 1 dans " + os.path.relpath(str(f), "/")])


if __name__ == "__main__":
    unittest.main()
