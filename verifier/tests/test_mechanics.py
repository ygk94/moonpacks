"""Mécaniques : concordance avec le Rust (`vectorgen/` mech_vectors) et rejeu d'événements réels du
sandbox (`contract/tests/sandbox.rs`, mechanics_end_to_end), y compris des événements falsifiés."""

import copy
import json
import unittest
from pathlib import Path

from memaster_verifier import canon, core, verify

VEC = Path(__file__).parent / "vectors"


def load(name):
    with open(VEC / name, encoding="utf-8") as f:
        return json.load(f)


MECH = load("mech_vectors.json")
SBX = load("sandbox_mech_vectors.json")


def items_of(doc):
    return [(e["event"], e["data"][0]) for e in doc["events"]]


class MechVectors(unittest.TestCase):
    """Code pur de `draw.rs` sur 120 tables à mécaniques et 30 séquences de rush."""

    def test_table_with_mechanics_serialization_and_hash(self):
        for c in MECH["cases"]:
            self.assertEqual(canon.table_json(c["table"]), c["table_json"])
            self.assertEqual(core.table_hash(c["table"]).hex(), c["table_hash"])

    def test_table_without_mechanics_has_no_field(self):
        t = copy.deepcopy(MECH["cases"][0]["table"])
        t["mechanics"] = None
        self.assertNotIn('"mechanics"', canon.table_json(t))
        del t["mechanics"]
        self.assertNotIn('"mechanics"', canon.table_json(t))

    def test_pity_and_mode(self):
        golds = 0
        for c in MECH["cases"]:
            acc = bytes.fromhex(c["acc"])
            self.assertEqual(core.gold_roll(acc), c["gold_roll"])
            m = c["table"]["mechanics"]
            if m["pity"]:
                g, r, pp = core.pity_is_gold(m["pity"], c["pity_n"], acc)
                self.assertEqual((g, r, pp), (c["pity_gold"], c["gold_roll"], c["p_ppm"]))
                golds += g
            mode = core.pack_mode(c["pity_gold"] and m["gold_weights"] is not None, c["rush"])
            self.assertEqual(mode, c["mode"])
        self.assertGreater(golds, 20)

    def test_draws_with_burns_and_resurrections(self):
        burns = 0
        for c in MECH["cases"]:
            t, m = c["table"], c["table"]["mechanics"]
            burn = core.Burn(c["burned"], c["backed"], m["burn"]["floor_bps"], m["burn"]["prior_k"]) if m["burn"] else None
            burns += burn is not None and any(c["burned"])
            mm, mmm = list(c["minted"]), list(c["mythic_minted"])
            got = core.draw_pack(t, mm, mmm, bytes.fromhex(c["acc"]), core.mode_weights(t, c["mode"]), burn)
            self.assertEqual([d.as_event() for d in got], c["draws"], f"cas {c['case']}")
            self.assertEqual(mm, c["minted_after"])
            self.assertEqual(mmm, c["mythic_minted_after"])
        self.assertGreater(burns, 50)

    def test_rush_sequences(self):
        triggered = 0
        for r in MECH["rushes"]:
            st = core.new_rush_state()
            for b in r["buys"]:
                o = core.rush_on_buy(r["params"], st, b["height"])
                self.assertEqual(o, {k: b[k] for k in o})
                triggered += o["triggered"]
            self.assertEqual(st["rush_count"], r["rush_count"])
        self.assertGreater(triggered, 50)

    def test_renormalization_keeps_burnable_share(self):
        """La part des brûlables dans leur rareté est celle de leurs poids de base (produits croisés)."""
        for c in MECH["cases"]:
            t, m = c["table"], c["table"]["mechanics"]
            if not m["burn"]:
                continue
            burn = core.Burn(c["burned"], c["backed"], m["burn"]["floor_bps"], m["burn"]["prior_k"])
            for r in ("legendary", "epic", "rare", "common"):
                f = core.burn_factors(t, c["minted"], burn, r)
                idx = [i for i, x in enumerate(t["cards"]) if x["rarity"] == r]
                ws = {i: core.in_rarity_weight(t, i, c["minted"][i], burn, f) for i in idx}
                base = {i: core._available(t["cards"][i]["weight"], c["minted"][i], t["cards"][i].get("cap")) for i in idx}
                wb, wt = sum(ws[i] for i in idx if c["backed"][i]), sum(ws.values())
                bb, bt = sum(base[i] for i in idx if c["backed"][i]), sum(base.values())
                self.assertEqual(wb * bt, bb * wt)


class ReviewFixes(unittest.TestCase):
    """Correctifs de la revue de sécurité, recalculés en Python comme dans le contrat."""

    def test_early_burns_are_smoothed_by_prior(self):
        # 10 épiques brûlables de poids 100 ; les 9 premières émises une fois et brûlées.
        t = {"cards": [{"rarity": "epic", "weight": 100, "cap": None} for _ in range(10)]}
        minted = [1] * 9 + [0]
        share = {}
        for k in (0, 20):
            burn = core.Burn([1] * 9 + [0], [True] * 10, 2_500, k)
            f = core.burn_factors(t, minted, burn, "epic")
            ws = [core.in_rarity_weight(t, i, minted[i], burn, f) for i in range(10)]
            share[k] = ws[9] / sum(ws)
        self.assertAlmostEqual(share[0], 100 / 325)  # sans lissage : 30,8 %
        self.assertLess(share[20], 0.11)
        self.assertEqual(core.raw_burn_weight(100, 1, 1, None, 2_500, 20), 95)
        self.assertEqual(core.raw_burn_weight(100, 60, 60, None, 2_500, 20), 25)


class SandboxMechanics(unittest.TestCase):
    """Événements réels : pitié (N = 3), gold rush, burns jusqu'à la dernière carte, résurrection."""

    def setUp(self):
        self.table = json.loads(SBX["table_raw"])
        self.items = copy.deepcopy(items_of(SBX))

    def replay(self, items):
        reports, st = verify.replay_series(self.table, items)
        return reports, st

    def test_full_replay_is_verified(self):
        reports, st = self.replay(self.items)
        bad = [r.render() for r in reports if not r.ok]
        self.assertFalse(bad, "\n".join(bad))
        names = {n for n, _ in self.items}
        self.assertEqual(names, {"pack_bought", "pack_revealed", "card_redeemed", "card_resurrected"})
        modes = [e["mechanics"]["mode"] for n, e in self.items if n == "pack_revealed"]
        self.assertIn("gold", modes)
        self.assertIn("rush", modes)
        self.assertGreater(st.burn_seq, 5)
        self.assertEqual(st.resurrect_seq, 1)
        self.assertEqual(sum(1 for n, _ in self.items if n == "pack_bought"), len(modes))

    def test_table_bytes_and_hash(self):
        raw = SBX["table_raw"].encode("utf-8")
        self.assertEqual(canon.table_json_bytes(self.table), raw)
        ev = next(e for n, e in self.items if n == "pack_revealed")
        self.assertEqual(core.table_hash(self.table).hex(), ev["table_hash"])

    def _tamper(self, pred, change):
        items = copy.deepcopy(self.items)
        for n, e in items:
            if pred(n, e):
                change(e)
                break
        else:
            self.fail("aucun événement à falsifier")
        reports, _ = self.replay(items)
        return [r for r in reports if not r.ok]

    def test_tampered_pity_counter_is_detected(self):
        def ch(e):
            e["mechanics"]["pity"]["before"] += 1
        bad = self._tamper(lambda n, e: n == "pack_revealed" and e["mechanics"]["pity"]["before"] == 1, ch)
        self.assertTrue(bad)

    def test_tampered_gold_decision_is_detected(self):
        def ch(e):
            e["mechanics"]["pity"]["gold"] = not e["mechanics"]["pity"]["gold"]
            e["mechanics"]["mode"] = "base" if e["mechanics"]["mode"] == "gold" else "gold"
        self.assertTrue(self._tamper(lambda n, e: n == "pack_revealed", ch))

    def test_tampered_rush_flag_is_detected(self):
        def ch(e):
            e["rush"]["active"] = not e["rush"]["active"]
        self.assertTrue(self._tamper(lambda n, e: n == "pack_bought" and e["rush"]["active"], ch))

    def test_missing_burn_event_is_detected(self):
        items = [x for x in self.items if not (x[0] == "card_redeemed" and x[1].get("burn_seq") == 3)]
        reports, _ = self.replay(items)
        bad = [r for r in reports if not r.ok]
        self.assertTrue(bad)
        self.assertTrue(any("burn_seq 3 absent" in e for r in bad for e in r.errors))

    def test_burns_change_card_choice(self):
        """Sans les burns (compteurs à zéro), au moins un tirage après les burns n'est plus conforme :
        les compteurs de burn comptent vraiment dans le tirage."""
        items = [x for x in self.items if x[0] != "card_redeemed"]
        for n, e in items:
            if n == "pack_revealed" and e["mechanics"]["burn_seq"]:
                e["mechanics"]["burn_seq"] = 0
        reports, _ = self.replay(items)
        self.assertTrue(any(not r.ok for r in reports))

    def test_cli_replays_event_file(self):
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            ev = Path(d) / "events.jsonl"
            ev.write_text("\n".join("EVENT_JSON:" + json.dumps(e, ensure_ascii=False) for e in SBX["events"]), encoding="utf-8")
            tb = Path(d) / "table.json"
            tb.write_bytes(SBX["table_raw"].encode("utf-8"))
            out = subprocess.run(
                [sys.executable, "-m", "memaster_verifier", "pack", "--event", str(ev), "--table", str(tb)],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
            )
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertIn("série à mécaniques", out.stdout)
            self.assertNotIn("NON CONFORME", out.stdout)


if __name__ == "__main__":
    unittest.main()
