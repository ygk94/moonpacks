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
                self.assertEqual((g, r, pp), (c["pity_gold"], c["gold_roll"], c["p_ppb"]))
                mode = core.pack_mode(g, c["rush"])
                self.assertEqual(core.pity_after(m["pity"], c["pity_n"], mode), c["pity_after"])
                golds += g
            mode = core.pack_mode(c["pity_gold"] and m["gold"] is not None, c["rush"])
            self.assertEqual(mode, c["mode"])
        self.assertGreater(golds, 20)

    def test_draws_with_burns_and_resurrections(self):
        """Tirage complet (gold pack à planchers, brûlable garantie, burns, résurrections) et valeur
        du pack, au bit près contre `draw::draw_pack_mech` et `draw::pack_value`."""
        burns = golds = valued = ups = below = 0
        for c in MECH["cases"]:
            t, m = c["table"], c["table"]["mechanics"]
            burn = core.Burn(c["burned"], c["backed"], m["burn"]["floor_bps"], m["burn"]["prior_k"], core.resurrectable(t)) if m["burn"] else None
            burns += burn is not None and any(c["burned"])
            mm, mmm = list(c["minted"]), list(c["mythic_minted"])
            acc = bytes.fromhex(c["acc"])
            got, slots = core.draw_pack_mech(t, mm, mmm, acc, c["mode"], burn, c["backed"])
            self.assertEqual([d.as_event() for d in got], c["draws"], f"cas {c['case']}")
            self.assertEqual([[r, b] for r, b in slots], c["slots"], f"cas {c['case']}")
            self.assertEqual(mm, c["minted_after"])
            self.assertEqual(mmm, c["mythic_minted_after"])
            self.assertEqual(core.pack_value(t, acc, c["mode"], slots), c["value"], f"cas {c['case']}")
            valued += c["value"] is not None
            if c["mode"] == "gold":
                golds += 1
                for d, gs in zip(got, m["gold"]["slots"]):
                    ri, fi, li = (core.RARITIES.index(x) for x in (d.rolled_rarity, d.final_rarity, gs["floor"]))
                    ups += fi < ri
                    below += fi > li
        self.assertGreater(burns, 50)
        self.assertGreater(golds, 20)
        self.assertGreater(valued, 50)
        self.assertGreater(ups, 0, "retombée vers le haut jamais exercée")
        self.assertGreater(below, 0, "retombée sous le plancher jamais exercée")

    def test_value_split_vectors(self):
        """Arrondi vers le bas, reste au plus fort multiplicateur (premier en cas d'égalité)."""
        for c in MECH["splits"]:
            total = core.value_total(int(c["price"]), c["bps"])
            self.assertEqual(str(total), c["total"])
            got = core.split_value(total, [tuple(x) for x in c["slots"]], c["multipliers"])
            self.assertEqual([None if a is None else str(a) for a in got], c["amounts"])
            if any(b for _, b in c["slots"]) and any(c["multipliers"][r] for r, b in c["slots"] if b):
                self.assertEqual(sum(a for a in got if a is not None), total)

    def test_rush_sequences(self):
        triggered = 0
        capped = 0
        for r in MECH["rushes"]:
            st = core.new_rush_state()
            accounts = {}
            for b in r["buys"]:
                o = core.rush_on_buy(r["params"], st, b["height"])
                self.assertEqual(o, {k: b[k] for k in o})
                prev = accounts.get(b["account"]) if o["active"] else None
                rush, cap, entry = core.rush_account(r["params"], o["active"], st["last_trigger"], prev)
                if rush:
                    accounts[b["account"]] = entry
                self.assertEqual((rush, cap), (b["rush"], b["capped"]))
                triggered += o["triggered"]
                capped += cap
            self.assertEqual(st["rush_count"], r["rush_count"])
        self.assertGreater(triggered, 50)
        self.assertGreater(capped, 20)

    def test_renormalization_keeps_burnable_share(self):
        """La part des brûlables dans leur rareté est celle de leurs poids de base (produits croisés)."""
        for c in MECH["cases"]:
            t, m = c["table"], c["table"]["mechanics"]
            if not m["burn"]:
                continue
            burn = core.Burn(c["burned"], c["backed"], m["burn"]["floor_bps"], m["burn"]["prior_k"], core.resurrectable(t))
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

    def test_single_actor_rush_is_capped(self):
        """Après un creux, un acteur déclenche le rush par une rafale dans un bloc, puis achète :
        3 packs rush au plus pour son compte, le reste au taux normal."""
        p = dict(ratio_bps=25_000, min_packs=100, window_blocks=6_000, baseline_blocks=144_000,
                 bucket_blocks=1_500, duration_blocks=3_000, cooldown_blocks=36_000, max_per_account=3)
        st, acct = core.new_rush_state(), {}
        core.rush_on_buy(p, st, 0)
        h = 30 * 6_000
        trig = [core.rush_on_buy(p, st, h)["triggered"] for _ in range(100)]
        self.assertEqual(trig.index(True), 99, "min_packs = 100 : la 100e achat déclenche")
        rush = []
        for i in range(10):
            o = core.rush_on_buy(p, st, h + 1 + i)
            r, capped, e = core.rush_account(p, o["active"], st["last_trigger"], acct.get("acteur"))
            if r:
                acct["acteur"] = e
            rush.append(r)
        self.assertEqual(rush, [True] * 3 + [False] * 7)

    def test_resurrected_card_enters_with_mean_ratio(self):
        # 4 épiques adossées toutes brûlées, une morte (index 4) émise 100 fois puis ressuscitée.
        t = {"cards": [{"rarity": "epic", "weight": 100, "cap": None} for _ in range(5)],
             "mechanics": {"resurrection": {"eligible": [4]}}}
        minted = [100] * 5
        burn = core.Burn([100] * 4 + [0], [True] * 5, 2_500, 20, core.resurrectable(t))
        f = core.burn_factors(t, minted, burn, "epic")
        ws = [core.in_rarity_weight(t, i, minted[i], burn, f) for i in range(5)]
        self.assertEqual(ws[4] * 5, sum(ws))  # part de base : 20 %
        # Hors liste, elle compterait comme une adossée de la table, à poids plein : 50 %.
        full = core.Burn([100] * 4 + [0], [True] * 5, 2_500, 20, ())
        f = core.burn_factors(t, minted, full, "epic")
        ws = [core.in_rarity_weight(t, i, minted[i], full, f) for i in range(5)]
        self.assertGreater(ws[4] * 2, sum(ws) - 1)

    def test_resurrection_outside_hashed_list_is_rejected(self):
        table = json.loads(SBX["table_raw"])
        items = copy.deepcopy(items_of(SBX))
        for n, e in items:
            if n == "card_resurrected":
                e["card_index"] = 5  # la rare, absente de mechanics.resurrection.eligible
                break
        reports, _ = verify.replay_series(table, items)
        self.assertTrue(any("absente de mechanics.resurrection.eligible" in x for r in reports for x in r.errors))


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

    def test_missing_pack_bought_is_an_error(self):
        """Revue, point 5 : série à rush, `pack_bought` absent pour un booster (ou pour tous) :
        erreur explicite, le drapeau rush journalisé n'est pas accepté tel quel."""
        rushed = next(e["pack_id"] for n, e in self.items if n == "pack_revealed" and e["mechanics"]["rush"])
        for drop in (lambda e: e["pack_id"] == rushed, lambda e: True):
            items = [x for x in self.items if not (x[0] == "pack_bought" and drop(x[1]))]
            reports, _ = self.replay(items)
            errs = [x for r in reports for x in r.errors]
            self.assertTrue(any("pack_bought" in x and "absent" in x for x in errs), errs)

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


class PityFormats(unittest.TestCase):
    """Pitié en ppb sans garantie (contrat du 11/11) et ancien format en ppm (séries déjà déployées)."""

    def test_new_format(self):
        p = {"p0_ppb": 20_000, "k_ppb": 20, "p_max_ppb": 40_000, "n_max": None}
        self.assertEqual(canon.pity_json(p), '{"p0_ppb":20000,"k_ppb":20,"p_max_ppb":40000,"n_max":null}')
        self.assertEqual([core.pity_p(p, n) for n in (0, 1, 500, 1000, 10**6)], [20_000, 20_020, 30_000, 40_000, 40_000])
        acc = bytes(32)
        g, r, pp = core.pity_is_gold(p, 10**9, acc)
        self.assertEqual((g, pp), (r < 40_000, 40_000))
        self.assertLess(r, 10**9)
        self.assertEqual(core.pity_after(p, 7, "rush"), 8, "un pack rush fait monter le compteur")
        self.assertEqual(core.pity_after(p, 7, "gold"), 0)
        self.assertEqual(core.pity_after(p, core.U32_MAX, "base"), core.U32_MAX, "saturé comme le contrat")
        q = dict(p, n_max=3)
        self.assertTrue(canon.pity_json(q).endswith('"n_max":3}'))
        self.assertTrue(core.pity_is_gold(dict(q, p0_ppb=0, k_ppb=0, p_max_ppb=0), 2, acc)[0], "garantie optionnelle")

    def test_legacy_format(self):
        p = {"p0_ppm": 20_000, "k_ppm": 2_000, "n_max": 20}
        self.assertEqual(canon.pity_json(p), '{"p0_ppm":20000,"k_ppm":2000,"n_max":20}')
        self.assertEqual(core.pity_p(p, 10), 40_000)
        self.assertEqual(core.pity_after(p, 7, "rush"), 0)
        self.assertTrue(core.pity_is_gold(p, 19, bytes(32))[0])


if __name__ == "__main__":
    unittest.main()
