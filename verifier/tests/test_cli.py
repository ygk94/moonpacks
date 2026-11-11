"""Le CLI sur des fichiers tirés des vecteurs sandbox (le mode RPC est testé par `vectorgen/`)."""

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from memaster_verifier.cli import main

VEC = Path(__file__).parent / "vectors"
SANDBOX = json.loads((VEC / "sandbox_vectors.json").read_text(encoding="utf-8"))


def series(label):
    return next(s for s in SANDBOX["series"] if s["label"] == label)


class Cli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data, raw=False):
        p = self.dir / name
        if raw:
            p.write_bytes(data)
        else:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = main(list(argv))
        return code, out.getvalue()

    def files(self, label):
        s = series(label)
        table = self.write(f"{label}-table.json", s["table_raw"].encode("utf-8"), raw=True)
        jsonl = self.dir / f"{label}-events.jsonl"
        jsonl.write_text(
            "\n".join("EVENT_JSON:" + json.dumps({"standard": "memaster", "version": "1.0.0", "event": "pack_revealed", "data": [p["event"]]}, ensure_ascii=False) for p in s["packs"]),
            encoding="utf-8",
        )
        return s, table, str(jsonl)

    def test_table(self):
        s, table, _ = self.files("unicode")
        code, out = self.run_cli("table", "--file", table, "--expected-hash", s["table_hash"])
        self.assertEqual(code, 0, out)
        self.assertIn("VÉRIFIÉ", out)
        # Fichier reformaté (indentation) : le hash canonique reste le bon.
        pretty = self.write("pretty.json", json.loads(s["table_raw"]))
        code, out = self.run_cli("table", "--file", pretty, "--expected-hash", s["table_hash"])
        self.assertEqual(code, 0, out)
        code, out = self.run_cli("table", "--file", table, "--expected-hash", "00" * 32)
        self.assertEqual(code, 1, out)

    def test_pack_snapshot_history_replay(self):
        s, table, events = self.files("distribution")
        p = s["packs"][60]
        ev = self.write("ev.json", p["event"])
        snap = self.write("snap.json", {"minted": p["minted_before"], "mythic_minted": p["mythic_minted_before"]})
        code, out = self.run_cli("pack", "--event", ev, "--table", table, "--snapshot", snap)
        self.assertEqual(code, 0, out)
        code, out = self.run_cli("pack", "--event", ev, "--table", table, "--history", events)
        self.assertEqual(code, 0, out)
        self.assertIn("rejeu de 60 boosters", out)
        code, out = self.run_cli("pack", "--event", events, "--table", table)
        self.assertEqual(code, 0, out)
        self.assertIn("90/90 vérifiés", out)
        code, out = self.run_cli("pack", "--event", events, "--table", table, "--pack-id", str(p["event"]["pack_id"]), "--no-state")
        self.assertEqual(code, 0, out)

    def test_pack_tampered(self):
        s, table, _ = self.files("cascade")
        p = s["packs"][2]
        bad = copy.deepcopy(p["event"])
        bad["draws"][5]["final_rarity"] = "rare" if bad["draws"][5]["final_rarity"] != "rare" else "common"
        ev = self.write("bad.json", bad)
        snap = self.write("snap.json", {"minted": p["minted_before"], "mythic_minted": p["mythic_minted_before"]})
        code, out = self.run_cli("pack", "--event", ev, "--table", table, "--snapshot", snap)
        self.assertEqual(code, 1, out)
        self.assertIn("NON CONFORME", out)

    def test_mythic(self):
        s, table, _ = self.files("distribution")
        ev = self.write("myth.json", s["mythic_revealed"])
        code, out = self.run_cli("mythic", "--event", ev, "--table", table)
        self.assertEqual(code, 0, out)
        r = s["mythic_revealed"][0]
        content = self.write("content.json", r["content"])
        code, out = self.run_cli("mythic", "--table", table, "--index", "0", "--card-id", r["card_id"], "--sel", r["sel"], "--content", content)
        self.assertEqual(code, 0, out)
        code, out = self.run_cli("mythic", "--table", table, "--index", "0", "--card-id", "autre", "--sel", r["sel"], "--content", content)
        self.assertEqual(code, 1, out)

    def test_stats(self):
        _, table, events = self.files("distribution")
        code, out = self.run_cli("stats", "--events", events, "--table", table, "--replay")
        self.assertEqual(code, 0, out)
        self.assertIn("90/90 boosters vérifiés", out)
        self.assertIn("χ²", out)


if __name__ == "__main__":
    unittest.main()
