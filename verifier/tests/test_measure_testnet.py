"""`contract/scripts/measure_testnet.py analyze` sur une vraie transaction `buy_pack` de app2
(testnet, 11/11/2026, lue en lecture seule et figée dans ``vectors/testnet_tx_buy_pack.json``) :
aucun appel réseau dans ces tests (``rpc`` est remplacé)."""

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

from tests import fake_secrets

sys.path.insert(0, str(fake_secrets.CONTRACT / "scripts"))

import measure_testnet as mt  # noqa: E402

FIX = json.loads((Path(__file__).parent / "vectors" / "testnet_tx_buy_pack.json").read_text(encoding="utf-8"))


class FakeRpc:
    """`rpc()` hors ligne : statut de transaction figé (ou erreur), en-têtes de blocs figés."""

    def __init__(self, statuses):
        self.statuses = statuses

    def __call__(self, method, params, url=None, tries=6):
        if method == "EXPERIMENTAL_tx_status":
            s = self.statuses[params["tx_hash"]]
            if isinstance(s, Exception):
                raise s
            return s
        if method == "block":
            h = FIX["blocks"][params["block_id"]]
            return {"result": {"header": h}}
        raise AssertionError(method)


def status_with(tx_hash, mutate=None):
    r = copy.deepcopy(FIX["tx_status"])
    if mutate:
        mutate(r["result"])
    return r


class Analyze(unittest.TestCase):
    def setUp(self):
        self.saved = mt.rpc
        mt._heights.clear()

    def tearDown(self):
        mt.rpc = self.saved
        mt._heights.clear()

    def run_analyze(self, statuses, txs):
        mt.rpc = FakeRpc(statuses)
        with tempfile.TemporaryDirectory() as d:
            inp, out, ev = Path(d) / "txs.jsonl", Path(d) / "m.json", Path(d) / "ev.jsonl"
            inp.write_text("".join(json.dumps(t) + "\n" for t in txs))
            buf = io.StringIO()
            with redirect_stdout(buf):
                mt.cmd_analyze(SimpleNamespace(inp=str(inp), out=str(out), events=str(ev)))
            return json.loads(out.read_text()), [json.loads(l) for l in ev.read_text().splitlines()], buf.getvalue()

    def tx(self, h, **kw):
        return dict({"tx": h, "signer": FIX["sender"], "series": 0, "mode": "parallel", "round": 0,
                     "sent_at": 0.0, "returned_at": 2.5}, **kw)

    def test_real_buy_pack_is_measured(self):
        m, ev, out = self.run_analyze({FIX["tx"]: status_with(FIX["tx"])}, [self.tx(FIX["tx"])])
        p = m["packs"][0]
        self.assertEqual(p["pack_id"], 0)
        self.assertEqual((p["buy_height"], p["reveal_height"], p["blocks_buy_to_reveal"]), (277270641, 277270644, 3))
        self.assertEqual(p["step_heights"], [277270642, 277270643, 277270644])
        self.assertEqual(p["gas_buy"], 8278177772048)
        self.assertEqual(p["gas_final"], 15439163278439)
        self.assertEqual(p["failed_receipts"], 0)
        self.assertEqual([e["event"] for e in ev][:1], ["pack_bought"])
        self.assertIn("pack_revealed", [e["event"] for e in ev])
        self.assertIn("1 transactions, 1 révélées", out)

    def test_refund_receipts_are_labelled(self):
        """Les remboursements de gaz sont exécutés chez l'expéditeur : ils étaient comptés « ? »."""
        r = mt.analyze_tx.__wrapped__ if hasattr(mt.analyze_tx, "__wrapped__") else mt.analyze_tx
        mt.rpc = FakeRpc({FIX["tx"]: status_with(FIX["tx"])})
        rows = r(FIX["tx"], FIX["sender"])["rows"]
        kinds = [x["kind"] for x in rows]
        self.assertEqual(kinds.count("refund"), 4, kinds)
        self.assertNotIn("?", kinds)

    def test_rpc_error_does_not_abort_the_batch(self):
        bad = {"jsonrpc": "2.0", "id": 1, "error": {"name": "HANDLER_ERROR", "cause": {"name": "UNKNOWN_TRANSACTION"}}}
        m, _, out = self.run_analyze(
            {FIX["tx"]: status_with(FIX["tx"]), "X" * 44: bad, "Y" * 44: RuntimeError("RPC injoignable")},
            [self.tx(FIX["tx"]), self.tx("X" * 44), self.tx("Y" * 44)],
        )
        self.assertEqual([p["status"] for p in m["packs"]], ["ok", "rpc_error", "rpc_error"])
        self.assertIn("3 transactions, 1 révélées", out)

    def test_summary_without_buy_pack_row(self):
        """Pack révélé sans ligne buy_pack identifiable (méthode absente des reçus) : pas de TypeError."""
        def drop_actions(res):
            for rc in res["receipts"]:
                rc["receipt"]["Action"]["actions"] = []
        m, _, out = self.run_analyze({FIX["tx"]: status_with(FIX["tx"], drop_actions)}, [self.tx(FIX["tx"])])
        self.assertIsNone(m["packs"][0]["buy_height"])
        self.assertIn("1 révélées", out)

    def test_failed_transaction_is_reported(self):
        def fail(res):
            res["status"] = {"Failure": {"ActionError": {}}}
            res["receipts_outcome"][0]["outcome"]["status"] = {"Failure": {}}
        m, _, _ = self.run_analyze({FIX["tx"]: status_with(FIX["tx"], fail)}, [self.tx(FIX["tx"])])
        self.assertEqual(m["packs"][0]["status"], "Failure")
        self.assertEqual(m["packs"][0]["failed_receipts"], 1)

    def test_fixture_events_verify_with_the_published_table(self):
        """Contrôle croisé : le pack 0 de app2 se revérifie avec la table publiée (aucun secret)."""
        from memaster_verifier import verify

        table = json.loads((fake_secrets.CONTRACT.parent / "docs" / "data" / "testnet-2026-11-11-v2" / "table.json").read_text(encoding="utf-8"))
        res = FIX["tx_status"]["result"]
        evs = [e for ro in res["receipts_outcome"] for e in mt.events_of(ro["outcome"]["logs"])]
        items = [(e["event"], e["data"][0]) for e in evs if e["event"] in ("pack_bought", "pack_revealed")]
        reports, _ = verify.replay_series(table, items)
        self.assertTrue(reports and all(r.ok for r in reports), [r.render() for r in reports if not r.ok])


if __name__ == "__main__":
    unittest.main()
