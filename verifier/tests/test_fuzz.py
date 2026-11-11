"""Corpus de fuzz figé (graine fixe de ``contract/src/tests_fuzz.rs``) : le vérificateur doit retrouver
au bit près les tirages, la valeur, la pitié et le gold rush calculés par le contrat sur des tables
valides au hasard. Régénération :

    cd contract && MEMASTER_FUZZ_SEED=7882826988098184562 \\
      MEMASTER_FUZZ_OUT=../verifier/tests/vectors/fuzz_vectors.json cargo test --lib contract_and_python
"""

import copy
import json
import unittest
from pathlib import Path

from tests import crosscheck

DOC = json.loads((Path(__file__).parent / "vectors" / "fuzz_vectors.json").read_text(encoding="utf-8"))


class FuzzCorpus(unittest.TestCase):
    def test_corpus_matches_contract(self):
        self.assertEqual(crosscheck.check_corpus(DOC), [])
        self.assertGreaterEqual(len(DOC["cases"]), 300)

    def test_corpus_covers_edge_cases(self):
        modes = {c["input"]["mode"] for c in DOC["cases"]}
        self.assertEqual(modes, {"base", "gold", "rush"})
        falls = sum(
            d["rolled_rarity"] != d["final_rarity"] for c in DOC["cases"] for d in c["expected"]["draws"]
        )
        self.assertGreater(falls, 50)
        self.assertTrue(any(c["expected"]["value"] for c in DOC["cases"]))

    def test_crosscheck_detects_a_tampered_result(self):
        """Le contrôle croisé n'est pas vide : un tirage, une valeur ou un rush modifiés sont vus."""
        doc = copy.deepcopy(DOC)
        c = doc["cases"][0]
        c["expected"]["draws"][0]["card_roll"] = str(int(c["expected"]["draws"][0]["card_roll"]) + 1)
        v = next(x for x in doc["cases"] if x["expected"]["value"])
        v["expected"]["value"]["total"] = str(int(v["expected"]["value"]["total"]) + 1)
        r = next(x for x in doc["cases"] if x["expected"]["rush"])
        r["expected"]["rush"]["rush_count"] += 1
        errs = crosscheck.check_corpus(doc)
        self.assertTrue(any(f"cas {c['input']['case']} : tirage" in e for e in errs), errs)
        self.assertTrue(any(f"cas {v['input']['case']} : valeur" in e for e in errs), errs)
        self.assertTrue(any(f"cas {r['input']['case']} : rush_count" in e for e in errs), errs)


if __name__ == "__main__":
    unittest.main()
