"""Concordance avec le Rust : vecteurs générés par `vectorgen/` (code de draw.rs et contrat en sandbox)."""

import copy
import json
import math
import unittest
from pathlib import Path

from memaster_verifier import canon, core, stats, verify

VEC = Path(__file__).parent / "vectors"


def load(name):
    with open(VEC / name, encoding="utf-8") as f:
        return json.load(f)


DRAW = load("draw_vectors.json")
SANDBOX = load("sandbox_vectors.json")


def series(label):
    return next(s for s in SANDBOX["series"] if s["label"] == label)


def table_of(s):
    return json.loads(s["table_raw"])


class DrawVectors(unittest.TestCase):
    """Code pur de `contract/src/draw.rs` sur 200 tables pseudo-aléatoires."""

    def test_table_serialization_and_hash(self):
        for c in DRAW["cases"]:
            self.assertEqual(canon.table_json(c["table"]), c["table_json"])
            self.assertEqual(core.table_hash(c["table"]).hex(), c["table_hash"])

    def test_acc_chain_and_rolls(self):
        for c in DRAW["cases"]:
            th = bytes.fromhex(c["table_hash"])
            acc = core.initial_acc(c["pack_id"], c["owner"], th)
            self.assertEqual(acc.hex(), c["initial_acc"])
            for s in c["seeds"]:
                acc = core.mix(acc, bytes.fromhex(s["seed"]), c["pack_id"], c["owner"])
                self.assertEqual(acc.hex(), s["acc"])
            self.assertEqual(acc.hex(), c["acc"])
            for r in c["rolls"]:
                self.assertEqual(str(core.roll(acc, r["slot"], r["tag"])), r["value"])

    def test_draw_pack_with_caps(self):
        falls = mythics = 0
        for c in DRAW["cases"]:
            m, mm = list(c["minted"]), list(c["mythic_minted"])
            got = [d.as_event() for d in core.draw_pack(c["table"], m, mm, bytes.fromhex(c["acc"]))]
            self.assertEqual(got, c["draws"])
            self.assertEqual(m, c["minted_after"])
            self.assertEqual(mm, c["mythic_minted_after"])
            falls += sum(d["rolled_rarity"] != d["final_rarity"] for d in got)
            mythics += sum(d["kind"] == "mythic" for d in got)
        # Les vecteurs couvrent bien la retombée et les mythiques.
        self.assertGreater(falls, 100)
        self.assertGreater(mythics, 20)

    def test_mythic_commitments(self):
        for x in DRAW["mythics"]:
            self.assertEqual(canon.content_json(x["content"]), x["content_json"])
            c, h = core.mythic_commitments(x["card_id"], bytes.fromhex(x["sel"]), x["content"])
            self.assertEqual(c.hex(), x["commitment"])
            self.assertEqual(h.hex(), x["content_hash"])


class SandboxVectors(unittest.TestCase):
    """Événements réels du contrat déployé dans near-sandbox."""

    def test_table_hash_is_sha256_of_view_bytes(self):
        for s in SANDBOX["series"]:
            raw = s["table_raw"].encode("utf-8")
            rep, table = verify.verify_table(raw, {"series_opened": s["table_hash"]})
            self.assertTrue(rep.ok, rep.render())
            self.assertEqual(canon.table_json_bytes(table), raw)
            self.assertEqual(s["get_series_table_hash"]["stored"], s["table_hash"])
            # Ancienne forme de la vue (vecteurs générés avant la pagination) : `recomputed` en plus.
            if "recomputed" in s["get_series_table_hash"]:
                self.assertEqual(s["get_series_table_hash"]["recomputed"], s["table_hash"])

    def test_each_pack_with_snapshot(self):
        n = 0
        for s in SANDBOX["series"]:
            t = table_of(s)
            for p in s["packs"]:
                rep = verify.verify_pack(p["event"], t, p["minted_before"], p["mythic_minted_before"])
                self.assertTrue(rep.ok, rep.render())
                n += 1
        self.assertEqual(n, 96)

    def test_replay_from_opening(self):
        for s in SANDBOX["series"]:
            t = table_of(s)
            reports, m, mm = verify.replay(t, [p["event"] for p in s["packs"]])
            self.assertTrue(all(r.ok for r in reports), [r.render() for r in reports if not r.ok])
            self.assertEqual(m, s["minted_final"])
            self.assertEqual(mm, s["mythic_minted_final"])
            # L'état rejoué avant chaque booster est celui que lisait le contrat.
            m, mm = [0] * len(t["cards"]), [0] * len(t["mythics"])
            for p in s["packs"]:
                self.assertEqual(m, p["minted_before"])
                self.assertEqual(mm, p["mythic_minted_before"])
                core.apply_event_draws(p["event"], m, mm)

    def test_caps_and_fallbacks_are_exercised(self):
        for label in ("distribution", "cascade"):
            draws = [d for p in series(label)["packs"] for d in p["event"]["draws"]]
            self.assertTrue(any(d["rolled_rarity"] != d["final_rarity"] for d in draws), label)
        casc = [d for p in series("cascade")["packs"] for d in p["event"]["draws"]]
        # Retombée sur plusieurs niveaux (légendaire → … → commune).
        self.assertTrue(any(d["rolled_rarity"] == "legendary" and d["final_rarity"] == "common" for d in casc))

    def test_state_matters(self):
        """Avec un mauvais état (compteurs à zéro), un booster tiré après un plafond n'est plus conforme."""
        s = series("cascade")
        t = table_of(s)
        last = s["packs"][-1]
        rep = verify.verify_pack(last["event"], t, [0] * len(t["cards"]), [])
        self.assertFalse(rep.ok)
        partial = verify.verify_pack(last["event"], t, None, None)
        self.assertTrue(partial.ok, partial.render())

    def test_tampering_is_detected(self):
        s = series("distribution")
        t = table_of(s)
        p = s["packs"][10]
        cases = []
        ev = copy.deepcopy(p["event"])
        ev["seeds"][1]["seed"] = ("0" if ev["seeds"][1]["seed"][0] != "0" else "1") + ev["seeds"][1]["seed"][1:]
        cases.append(ev)
        ev = copy.deepcopy(p["event"])
        ev["draws"][2]["index"] = (ev["draws"][2]["index"] + 1) % len(t["cards"])
        cases.append(ev)
        ev = copy.deepcopy(p["event"])
        ev["owner_id"] = "mallory.test.near"
        cases.append(ev)
        ev = copy.deepcopy(p["event"])
        ev["draws"][0]["card_roll"] = str(int(ev["draws"][0]["card_roll"]) + 1)
        cases.append(ev)
        for ev in cases:
            self.assertFalse(verify.verify_pack(ev, t, p["minted_before"], p["mythic_minted_before"]).ok)
        t2 = copy.deepcopy(t)
        t2["rarity_weights"]["mythic"] += 1
        self.assertFalse(verify.verify_pack(p["event"], t2, p["minted_before"], p["mythic_minted_before"]).ok)

    def test_mythic_reveal(self):
        s = series("distribution")
        t = table_of(s)
        ev = s["mythic_revealed"][0]
        m = t["mythics"][ev["mythic_index"]]
        self.assertEqual((ev["commitment"], ev["content_hash"]), (m["commitment"], m["content_hash"]))
        rep = verify.verify_mythic(ev["card_id"], ev["sel"], ev["content"], m["commitment"], m["content_hash"], "table")
        self.assertTrue(rep.ok, rep.render())
        bad = copy.deepcopy(ev["content"])
        bad["backing"]["amount"] = "778"
        self.assertFalse(verify.verify_mythic(ev["card_id"], ev["sel"], bad, m["commitment"], m["content_hash"], "t").ok)
        self.assertFalse(verify.verify_mythic("pepe-mythic2", ev["sel"], ev["content"], m["commitment"], m["content_hash"], "t").ok)
        # La vue get_mythic_commitments publie la même préimage.
        r = s["mythic_commitments"][0]["revealed"]
        self.assertEqual((r["card_id"], r["sel"], r["content"]), (ev["card_id"], ev["sel"], ev["content"]))

    def test_rates_view_matches_table(self):
        s = series("distribution")
        t = table_of(s)
        probs = stats.rarity_probs(t)
        for r in s["rates"]["rarities"]:
            self.assertEqual(r["rarity_ppm"], int(probs[r["rarity"]] * 1_000_000 + 1e-9))

    def test_stats_on_real_draws(self):
        s = series("distribution")
        ok, lines = stats.series_stats(table_of(s), [p["event"] for p in s["packs"]], 0.001)
        self.assertTrue(ok, "\n".join(lines))


class Chi2(unittest.TestCase):
    def test_survival_function(self):
        self.assertAlmostEqual(stats.chi2_sf(3.841458820694124, 1), 0.05, places=9)
        self.assertAlmostEqual(stats.chi2_sf(9.487729036781154, 4), 0.05, places=9)
        self.assertAlmostEqual(stats.chi2_sf(18.307038053275146, 10), 0.05, places=9)
        for x in (0.5, 2.0, 7.0, 40.0):
            self.assertAlmostEqual(stats.chi2_sf(x, 2), math.exp(-x / 2), places=12)

    def test_bias_is_detected(self):
        t = table_of(series("distribution"))
        draws = [{"rolled_rarity": "common", "final_rarity": "common", "kind": "visible", "index": 4}] * 500
        ok, _ = stats.series_stats(t, [{"draws": draws}], 0.001)
        self.assertFalse(ok)

    def test_impossible_category(self):
        chi2, _, p, _ = stats.chi2_test({"a": 10, "b": 1}, {"a": 1.0, "b": 0.0})
        self.assertEqual(p, 0.0)


if __name__ == "__main__":
    unittest.main()
