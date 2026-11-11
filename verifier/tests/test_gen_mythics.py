"""`contract/scripts/gen_mythics.py` : préimages en mode 600 même si le fichier existait, contenu
révélable exigé (bornes de `reveal_mythic`), messages d'erreur sans le secret."""

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import fake_secrets

SCRIPT = fake_secrets.CONTRACT / "scripts" / "gen_mythics.py"


def entry(card_id="fictif-secret-1", title="Fictif Secret", **content):
    c = {"title": title, "media": "ipfs://x/1.svg", "reference": None, "backing": {"asset_id": "nep141:f.near", "amount": "5"}}
    c.update(content)
    return {"card_id": card_id, "weight": 1, "cap": 1, "content": c}


def run(d, entries):
    src, pub, sec = Path(d) / "in.json", Path(d) / "pub.json", Path(d) / "s" / "sec.json"
    src.write_text(json.dumps(entries), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(src), str(pub), str(sec)], capture_output=True, text=True)
    return r, pub, sec


class GenMythics(unittest.TestCase):
    def test_existing_secret_file_becomes_0600(self):
        with tempfile.TemporaryDirectory() as d:
            sec = Path(d) / "s" / "sec.json"
            sec.parent.mkdir()
            sec.write_text("[]")
            os.chmod(sec, 0o644)
            r, pub, sec = run(d, [entry()])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(stat.S_IMODE(os.stat(sec).st_mode), 0o600)
            self.assertEqual(len(json.loads(pub.read_text())), 1)

    def test_unrevealable_content_is_refused_without_echoing_it(self):
        cases = [
            (entry(card_id="c" * 65), "card_id"),
            (entry(title="T" * 65), "titre"),
            (entry(media="u" * 257), "media"),
            (entry(backing={"asset_id": "a", "amount": "0"}), "adossement"),
            (entry(backing={"asset_id": "a", "amount": "-5"}), "adossement"),
            (dict(entry(), cap=101), "cap"),
            ([entry(), entry()], "en double"),
        ]
        for e, msg in cases:
            with self.subTest(msg=msg), tempfile.TemporaryDirectory() as d:
                r, _, sec = run(d, e if isinstance(e, list) else [e])
                self.assertNotEqual(r.returncode, 0)
                self.assertIn(msg, r.stderr)
                self.assertNotIn("fictif-secret-1", r.stderr, "le card_id secret n'est pas recopié")
                self.assertFalse(sec.exists())


if __name__ == "__main__":
    unittest.main()
