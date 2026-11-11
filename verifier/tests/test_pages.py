"""Lecture d'une table par pages (`get_series_header` + `get_series_cards`) : le vérificateur
reconstruit la table, recalcule le hash localement et le compare au hash enregistré.

Le RPC est simulé à partir de la table : les pages ont exactement la forme `serde_json` de
`Vec<CardDef>` (la concordance avec le vrai contrat est testée en sandbox, `contract/tests/sandbox.rs`,
tests `catalogue_v2_batched_load_and_packs` et `max_size_series_fits`)."""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from memaster_verifier import canon, cli, core

from tests import fake_secrets

HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent.parent / "contract"
VEC = HERE / "vectors"


class FakeRpc:
    """Vues `get_series_header`, `get_series_cards` et `get_series_table_hash` d'une série ouverte."""

    def __init__(self, table: dict, table_hash: str | None, series_id: int = 0, status: str = "open"):
        self.table, self.hash, self.sid, self.status = table, table_hash, series_id, status
        self.calls = []

    def view_raw_at(self, contract, method, args=None, block_id=None):
        self.calls.append(method)
        assert args["series_id"] == self.sid
        if method == "get_series_header":
            header = dict(self.table, cards=[])
            body = {
                "series_id": self.sid, "status": self.status, "table_hash": self.hash,
                "card_count": len(self.table["cards"]), "max_page": 200, "storage_deposit": "0", "header": header,
            }
            return json.dumps(body, ensure_ascii=False).encode("utf-8"), 1234
        if method == "get_series_cards":
            assert block_id == 1234, "pages lues au bloc de l'en-tête"
            start, limit = args["from_index"], min(args["limit"], 200)
            return canon.cards_json_bytes(self.table["cards"][start:start + limit]), 1234
        if method == "get_series_table_hash":
            return json.dumps({"stored": self.hash, "card_count": len(self.table["cards"])}).encode(), 1234
        raise AssertionError(f"vue inattendue : {method}")

    def view_raw(self, contract, method, args=None, block_id=None):
        return self.view_raw_at(contract, method, args, block_id)[0]

    def view(self, contract, method, args=None, block_id=None):
        return json.loads(self.view_raw(contract, method, args, block_id))


def run_cli(fake, *argv):
    out = io.StringIO()
    with mock.patch.object(cli, "Rpc", lambda url: fake), contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = cli.main(list(argv))
    return code, out.getvalue()


class SeriesV2Pages(unittest.TestCase):
    """Série v2 complète (`scripts/build_series.py scripts/serie-exemple.json`) : 1 646 cartes."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        res = subprocess.run(
            [sys.executable, "-I", str(CONTRACT / "scripts" / "build_series.py"), str(CONTRACT / "scripts" / "serie-exemple.json"),
             "--mythiques", str(fake_secrets.write_fake_mythics(d)),
             "--out", str(d / "out"), "--secrets", str(d / "secrets" / "s.json")],
            capture_output=True, text=True,
        )
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        cls.table_bytes = (d / "out" / "table.json").read_bytes()
        cls.table = json.loads(cls.table_bytes)
        cls.hash_before = (d / "out" / "table_hash.txt").read_text().strip()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_paged_hash_equals_full_table_hash(self):
        # « Avant » : hash de la table complète d'un seul tenant (script et vérificateur).
        self.assertEqual(core.table_hash(self.table).hex(), self.hash_before)
        self.assertEqual(core.sha256(self.table_bytes).hex(), self.hash_before)
        self.assertGreater(len(self.table["cards"]), 1600)
        for page in ("200", "37", "1"):
            with self.subTest(page=page):
                fake = FakeRpc(self.table, self.hash_before)
                code, out = run_cli(fake, "table", "--rpc", "fake", "--contract", "c", "--series", "0", "--page-size", page)
                self.assertEqual(code, 0, out)
                self.assertIn("VÉRIFIÉ", out)
                self.assertIn(f"sha256 calculé : {self.hash_before}", out)
                n = -(-len(self.table["cards"]) // int(page))
                self.assertEqual(fake.calls.count("get_series_cards"), n)
                self.assertNotIn("get_series_table", fake.calls)
                self.assertNotIn("get_rates", fake.calls)

    def test_draft_is_checked_before_open_series(self):
        """Avant `open_series` (deploy_testnet.sh) : le brouillon chargé doit redonner le hash local ;
        un lot manquant (reprise après une coupure) est refusé, au lieu d'ouvrir une table tronquée."""
        args = ["table", "--rpc", "fake", "--contract", "c", "--series", "0"]
        code, out = run_cli(FakeRpc(self.table, None, status="draft"), *args, "--draft", "--expected-hash", self.hash_before)
        self.assertEqual(code, 0, out)
        self.assertIn("VÉRIFIÉ", out)
        short = dict(self.table, cards=self.table["cards"][:-77])
        code, out = run_cli(FakeRpc(short, None, status="draft"), *args, "--draft", "--expected-hash", self.hash_before)
        self.assertEqual(code, 1, out)
        # Sans --draft, un brouillon n'a pas de hash publié : refus (comportement d'avant).
        code, out = run_cli(FakeRpc(self.table, None, status="draft"), *args, "--expected-hash", self.hash_before)
        self.assertEqual(code, 1, out)
        # --draft sur une série déjà ouverte : refus.
        code, out = run_cli(FakeRpc(self.table, self.hash_before), *args, "--draft", "--expected-hash", self.hash_before)
        self.assertEqual(code, 1, out)
        self.assertIn("pas un brouillon", out)

    def test_page_size_is_capped_at_200(self):
        fake = FakeRpc(self.table, self.hash_before)
        code, out = run_cli(fake, "table", "--rpc", "fake", "--contract", "c", "--series", "0", "--page-size", "5000")
        self.assertEqual(code, 0, out)
        self.assertEqual(fake.calls.count("get_series_cards"), -(-len(self.table["cards"]) // 200))

    def test_tampered_page_or_wrong_hash_fails(self):
        bad = json.loads(self.table_bytes)
        bad["cards"][777]["weight"] += 1
        code, out = run_cli(FakeRpc(bad, self.hash_before), "table", "--rpc", "fake", "--contract", "c", "--series", "0")
        self.assertEqual(code, 1, out)
        self.assertIn("NON CONFORME", out)
        code, out = run_cli(FakeRpc(self.table, "00" * 32), "table", "--rpc", "fake", "--contract", "c", "--series", "0")
        self.assertEqual(code, 1, out)

    def test_missing_cards_are_detected(self):
        fake = FakeRpc(self.table, self.hash_before)
        real = fake.view_raw_at

        def short(contract, method, args=None, block_id=None):
            raw, h = real(contract, method, args, block_id)
            if method == "get_series_cards" and args["from_index"] == 400:
                raw = canon.cards_json_bytes(json.loads(raw)[:-1])
            return raw, h

        fake.view_raw_at = short
        code, out = run_cli(fake, "table", "--rpc", "fake", "--contract", "c", "--series", "0")
        self.assertEqual(code, 1, out)
        self.assertIn("card_count", out)

    def test_published_v2_output_if_present(self):
        """`scripts/out/serie-v2/` (sels réels, non suivis) : même hash par pages qu'avant."""
        out = CONTRACT / "scripts" / "out" / "serie-v2"
        if not (out / "table.json").exists():
            self.skipTest("scripts/out/serie-v2 absent")
        table = json.loads((out / "table.json").read_bytes())
        h = (out / "table_hash.txt").read_text().strip()
        code, txt = run_cli(FakeRpc(table, h), "table", "--rpc", "fake", "--contract", "c", "--series", "0")
        self.assertEqual(code, 0, txt)
        self.assertIn(f"sha256 calculé : {h}", txt)


class LoadTableByPages(unittest.TestCase):
    def test_pack_reads_table_by_pages(self):
        """`pack` sans --table : la table vient des pages, pas de `get_series_table`."""
        sandbox = json.loads((VEC / "sandbox_vectors.json").read_text(encoding="utf-8"))
        s = next(x for x in sandbox["series"] if x["label"] == "distribution")
        fake = FakeRpc(json.loads(s["table_raw"]), s["table_hash"], s["series_id"])
        with tempfile.TemporaryDirectory() as d:
            ev = Path(d) / "ev.json"
            ev.write_text(json.dumps(s["packs"][3]["event"]), encoding="utf-8")
            code, out = run_cli(fake, "pack", "--rpc", "fake", "--contract", "c", "--event", str(ev), "--no-state")
        self.assertEqual(code, 0, out)
        self.assertIn("pages de get_series_cards", out)
        self.assertNotIn("get_series_table", fake.calls)


if __name__ == "__main__":
    unittest.main()
