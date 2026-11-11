"""Conformité des tirages aux probabilités de la config."""
import numpy as np
import pytest

from conftest import RACINE
from memaster_sim import modele as M
from memaster_sim import simulation as S

N = 1_000_000


@pytest.fixture(scope="module", params=["serie1-A-10near.yaml", "serie1-C-5near.yaml", "exemple-4-4.yaml"])
def tirage(request):
    cfg = M.charger_config(RACINE / "configs" / request.param)
    t = M.construire_tables(cfg)
    issues = S.tirer_issues(t, N, np.random.default_rng(7))
    return cfg, t, issues


def test_frequences_des_issues_par_emplacement(tirage):
    cfg, t, issues = tirage
    for j, s in enumerate(t.ordre):
        p = t.probas[s]
        f = np.bincount(issues[:, j], minlength=p.size) / N
        tol = 5 * np.sqrt(p * (1 - p) / N) + 1e-12
        assert np.all(np.abs(f - p) <= tol), (s, f, p)
        assert np.all(f[p == 0] == 0)


def test_frequences_par_rarete(tirage):
    cfg, t, issues = tirage
    for j, s in enumerate(t.ordre):
        table = cfg["emplacements"]["tables"][s]
        r = t.issue_rarete[issues[:, j]]
        for i, nom in enumerate(t.raretes):
            p = table.get(nom, 0.0)
            f = (r == i).mean()
            assert abs(f - p) <= 5 * np.sqrt(p * (1 - p) / N) + 1e-12, (s, nom, f, p)


def test_part_brulable_par_rarete(tirage):
    cfg, t, issues = tirage
    r = t.issue_rarete[issues].ravel()
    b = t.issue_brulable[issues].ravel()
    for i, nom in enumerate(t.raretes):
        sel = r == i
        if sel.sum() < 1000:
            continue
        pb = cfg["raretes"][nom]["part_brulable"]
        assert abs(b[sel].mean() - pb) <= 5 * np.sqrt(pb * (1 - pb) / sel.sum()) + 1e-12, nom


def test_chi2_global(tirage):
    cfg, t, issues = tirage
    for j, s in enumerate(t.ordre):
        p = t.probas[s]
        k = p > 0
        obs = np.bincount(issues[:, j], minlength=p.size)[k]
        att = N * p[k]
        chi2 = ((obs - att) ** 2 / att).sum()
        ddl = k.sum() - 1
        # seuil à ~5 écarts-types de la loi du χ² (moyenne ddl, variance 2·ddl)
        assert chi2 < ddl + 5 * np.sqrt(2 * ddl), (s, chi2, ddl)


def test_emplacement_favorable_plus_genereux():
    cfg = M.charger_config(RACINE / "configs" / "serie1-A-10near.yaml")
    tab = cfg["emplacements"]["tables"]
    assert tab["favorable"]["legendaire"] > tab["standard"]["legendaire"]
    assert tab["standard"]["mythique"] == 0


def test_seed_reproductible():
    cfg = M.charger_config(RACINE / "configs" / "serie1-A-10near.yaml")
    t = M.construire_tables(cfg)
    a = S.tirer_issues(t, 1000, np.random.default_rng(1))
    b = S.tirer_issues(t, 1000, np.random.default_rng(1))
    assert np.array_equal(a, b)
