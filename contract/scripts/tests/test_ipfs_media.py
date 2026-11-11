"""Dossier IPFS des visuels et envoi à sec (contract/scripts/ipfs_media.py). Aucun réseau, aucun jeton.

Lancement : python3 -m unittest discover -s contract/scripts/tests
"""
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import ipfs_media  # noqa: E402

LONG = "x" * 70  # card_id raccourci par build_series.short_id
CAT = [{"id": "aaa-a", "section": "catalogue", "rarete": "commune"},
       {"id": LONG, "section": "catalogue", "rarete": "rare"},
       {"id": "mythique-m1", "section": "catalogue", "rarete": "mythique"}]
CID = "bafybeifejdd5hvm44qa6qv5s3m2avywhdrydhn2rwypccttz52eu5viuia"


class PrepareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.art = os.path.join(self.tmp.name, "art")
        os.makedirs(self.art)
        for n in ("aaa-a", LONG, "dos-mythique"):
            with open(os.path.join(self.art, n + ".svg"), "w") as f:
                f.write(f"<svg>{'?' if n == 'dos-mythique' else n}</svg>")
        self.dest = os.path.join(self.tmp.name, "dest")
        self.secrets = os.path.join(self.tmp.name, "mythiques.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_names_are_table_card_ids_and_common_mythic(self):
        r = ipfs_media.prepare(self.art, CAT, self.dest, secrets_path=None)
        import build_series
        self.assertEqual(sorted(os.listdir(self.dest)),
                         sorted(["aaa-a.svg", build_series.short_id(LONG) + ".svg", "mythique.svg"]))
        self.assertEqual((r["files"], r["cards"]), (3, 2))

    def test_missing_svg_is_refused(self):
        os.remove(os.path.join(self.art, "aaa-a.svg"))
        with self.assertRaises(SystemExit):
            ipfs_media.prepare(self.art, CAT, self.dest, secrets_path=None)

    def test_leak_in_mythic_visual_is_refused(self):
        with open(self.secrets, "w") as f:
            json.dump({"mythiques": [{"id": "fictif-zzq", "nom": "Fictif Zzq"}]}, f)
        self.assertTrue(ipfs_media.prepare(self.art, CAT, self.dest, self.secrets)["leak_check"])
        with open(os.path.join(self.art, "dos-mythique.svg"), "w") as f:
            f.write("<svg>Fictif Zzq</svg>")
        with self.assertRaises(SystemExit):
            ipfs_media.prepare(self.art, CAT, self.dest, self.secrets)


class UploadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.car = os.path.join(self.tmp.name, "x.car")
        with open(self.car, "wb") as f:
            f.write(b"\x00CAR")

    def tearDown(self):
        self.tmp.cleanup()

    def never(self, *a, **k):
        raise AssertionError("aucun appel réseau attendu")

    def test_dry_run_sends_nothing_and_hides_token(self):
        for provider in ("pinata", "w3s"):
            env = ipfs_media.PROVIDERS[provider]["env"]
            with mock.patch.dict(os.environ, {env: "SECRET-TOKEN"}):
                plan = ipfs_media.upload(provider, self.car, "t", dry_run=True, expected=CID, opener=self.never)
            self.assertTrue(plan["token_present"])
            self.assertNotIn("SECRET-TOKEN", json.dumps(plan))
            self.assertEqual(plan["request"]["method"], "POST")

    def test_missing_token_refuses(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                ipfs_media.upload("pinata", self.car, "t", expected=CID, opener=self.never)

    def fake(self, payload):
        def opener(req, timeout=None):
            self.req = req
            return io.BytesIO(json.dumps(payload).encode())
        return opener

    def test_pinata_request_and_cid_check(self):
        with mock.patch.dict(os.environ, {"PINATA_JWT": "tok"}):
            plan = ipfs_media.upload("pinata", self.car, "t", expected=CID, opener=self.fake({"data": {"cid": CID}}))
            self.assertEqual(plan["uploaded_cid"], CID)
            self.assertEqual(self.req.get_header("Authorization"), "Bearer tok")
            self.assertIn(b'name="car"\r\n\r\ntrue', self.req.data)
            with self.assertRaises(SystemExit):
                ipfs_media.upload("pinata", self.car, "t", expected=CID, opener=self.fake({"data": {"cid": "bafyautre"}}))

    def test_w3s_sends_raw_car(self):
        with mock.patch.dict(os.environ, {"W3S_TOKEN": "tok"}):
            ipfs_media.upload("w3s", self.car, "t", expected=CID, opener=self.fake({"cid": CID}))
        self.assertEqual(self.req.data, b"\x00CAR")
        self.assertEqual(self.req.get_header("Content-type"), "application/vnd.ipld.car")

    def test_parse_cid(self):
        self.assertEqual(ipfs_media.parse_cid(f"\n{CID}\n"), CID)
        with self.assertRaises(SystemExit):
            ipfs_media.parse_cid("rien")


if __name__ == "__main__":
    unittest.main()
