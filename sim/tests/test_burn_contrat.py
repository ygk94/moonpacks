"""La rareté pilotée par les burns de la simulation, réglée comme le contrat (`PARAMS_CONTRAT` :
a priori K, plancher, part des brûlables constante), donne les mêmes parts que la règle exacte du
contrat, recalculée par le vérificateur (`verifier/memaster_verifier/core.py`, en entiers)."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verifier"))

from memaster_sim import rarete_burn as RB  # noqa: E402
from memaster_verifier import core  # noqa: E402


def contract_shares(n_coll, emis, brules, k, floor_bps, w=1_000_000):
    """Parts de chaque brûlable dans la rareté (poids égaux w), règle du contrat."""
    nb = len(emis)
    cards = [{"rarity": "epic", "weight": w, "cap": None} for _ in range(nb + n_coll)]
    table = {"cards": cards}
    minted = list(emis) + [0] * n_coll
    burn = core.Burn(list(brules) + [0] * n_coll, [True] * nb + [False] * n_coll, floor_bps, k)
    f = core.burn_factors(table, minted, burn, "epic")
    ws = [core.in_rarity_weight(table, i, minted[i], burn, f) for i in range(nb + n_coll)]
    tot = sum(ws)
    return np.array(ws[:nb]) / tot


def test_sim_matches_contract_rule():
    rng = np.random.default_rng(12)
    p = RB.PARAMS_CONTRAT
    for _ in range(200):
        nb, n_coll = int(rng.integers(1, 12)), int(rng.integers(0, 30))
        emis = rng.integers(0, 200, nb)
        brules = np.minimum(emis, rng.integers(0, 200, nb))
        s = {"effectif": nb + n_coll, "brulables": nb}
        sim = RB._part_brulable(s, RB.ratios_burn(emis, brules, p["prior_k"], p["plancher"]), p["renormaliser"])
        want = contract_shares(n_coll, emis, brules, p["prior_k"], int(p["plancher"] * 10_000))
        assert np.allclose(sim, want, atol=1e-5), (emis, brules, sim, want)
        # Part totale des brûlables inchangée par les burns (règle du contrat).
        assert abs(sim.sum() - nb / (nb + n_coll)) < 1e-9


def test_default_params_keep_published_results():
    """Les paramètres par défaut (K = 0, « rarete ») restent ceux des résultats publiés."""
    assert RB.PARAMS_DEFAUT["prior_k"] == 0 and RB.PARAMS_DEFAUT["renormaliser"] == "rarete"
    r = RB.ratios_burn(np.array([0, 10, 10]), np.array([0, 5, 10]), 0, 0.0)
    assert list(r) == [1.0, 0.5, 0.0]
    r = RB.ratios_burn(np.array([1, 60]), np.array([1, 60]), 20, 0.25)
    assert np.allclose(r, [20 / 21, 0.25])
