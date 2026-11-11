"""L'exemple travaillé de la partie 4.4 de docs/marche-droits-economie.md doit être retrouvé."""
import math

import pytest

from conftest import RACINE
from memaster_sim import modele as M
from memaster_sim import simulation as S

CFG = M.charger_config(RACINE / "configs" / "exemple-4-4.yaml")


def test_kappa_formule_du_document():
    somme_pw = 0.70 * 1 + 0.20 * 2 + 0.08 * 8 + 0.018 * 30 + 0.002 * 110
    assert somme_pw == pytest.approx(2.50)
    assert M.kappa_doc(P=10, n=5, d=0.2, q=0.6, somme_pw=somme_pw, Em=1.0, beta=0.6) == pytest.approx(1.0)


def test_kappa_generalise_retrouve_la_formule_du_document():
    assert M.kappa_formule(CFG) == pytest.approx(1.0)
    assert M.kappa(CFG) == pytest.approx(1.0)


def test_kappa_proportionnel_a_beta_et_au_prix():
    assert M.kappa_formule(M.avec(CFG, beta=0.75)) == pytest.approx(1.25)
    assert M.kappa_formule(M.avec(CFG, prix=20)) == pytest.approx(2.0)


def test_adossement_moyen_6_near():
    a = M.analytique(CFG)
    assert a["esperance_adossement"] == pytest.approx(6.0)
    assert a["cartes_brulables_moyennes"] == pytest.approx(2.4)


def test_variance_du_document():
    # σ ≈ √(5 × 27,90) ≈ 11,8 NEAR
    assert M.analytique(CFG)["sigma_booster"] == pytest.approx(math.sqrt(5 * 27.9), rel=1e-3)
    assert M.analytique(CFG)["sigma_booster"] == pytest.approx(11.8, abs=0.05)


def test_probabilites_du_document():
    a = M.analytique(CFG)
    assert a["p_au_moins_un_legendaire"] == pytest.approx(1 - 0.998**5)
    assert a["p_au_moins_un_legendaire_brulable"] == pytest.approx(1 - (1 - 0.00096) ** 5)
    assert a["p_aucune_brulable"] == pytest.approx(0.52**5)


def test_gain_attaquant_et_borne_829():
    a = M.analytique(CFG)
    assert a["c"] == pytest.approx(0.985 * 0.98 * 0.97)
    assert a["revente_collection_nette"] == pytest.approx(5 * 0.52 * 0.3 * 0.95)
    assert a["gain_attaquant_moyen"] == pytest.approx(6.36, abs=0.005)
    assert round(a["beta_max_formule"], 3) == 0.829


def test_reserve_normale_564():
    assert M.analytique(CFG)["r0_normale"] == pytest.approx(564, abs=1)


def test_monte_carlo_retrouve_l_exemple():
    s = S.statistiques(M.avec(CFG, v_cap=1e9), n_boosters=1_000_000, seed=3)
    assert s["esperance_adossement"] == pytest.approx(6.0, abs=4 * s["erreur_type"])
    assert s["sigma_booster"] == pytest.approx(11.81, rel=0.02)
    # sans V_cap, la borne simulée doit coïncider avec la formule
    assert s["beta_max_simule"] == pytest.approx(0.829, abs=0.004)
