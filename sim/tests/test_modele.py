"""Propriétés du modèle et des jeux de paramètres de la série 1."""
import numpy as np
import pytest

from conftest import RACINE
from memaster_sim import modele as M
from memaster_sim import simulation as S

SERIE1 = ["serie1-A-10near.yaml", "serie1-B-10near.yaml", "serie1-C-5near.yaml"]


@pytest.mark.parametrize("nom", SERIE1)
def test_calibrage_atteint_beta_P(nom):
    cfg = M.charger_config(RACINE / "configs" / nom)
    t = M.construire_tables(cfg)
    assert M.esperance_adossement(t, M.kappa(cfg)) == pytest.approx(cfg["beta"] * cfg["prix"], rel=1e-9)


@pytest.mark.parametrize("nom", SERIE1)
def test_contraintes_serie1(nom):
    cfg = M.charger_config(RACINE / "configs" / nom)
    a = M.analytique(cfg)
    cote = 1 / a["p_au_moins_un_mythique"]
    assert 2000 * 0.999 <= cote <= 10000 * 1.001
    assert cfg["epsilon"] >= 0.15
    assert cfg["beta"] <= a["beta_max_formule"]
    assert a["gain_attaquant_moyen"] <= cfg["prix"] * (1 - cfg["epsilon"])
    # aucune carte brûlable sous la valeur minimale utile
    assert min(v["min"] for v in a["valeur_par_rarete"].values()) >= cfg["v_min_brulable"]
    # le mythique tient sous V_cap
    assert a["valeur_par_rarete"]["mythique"]["max"] <= cfg["v_cap"]


def test_plafond_par_carte_recalibre_kappa():
    cfg = M.charger_config(RACINE / "configs" / "exemple-4-4.yaml")
    c = M.avec(cfg, calibrer_avec_plafonds=True, **{"raretes.legendaire.plafond": 120})
    assert M.kappa(c) > M.kappa_formule(c)
    t = M.construire_tables(c)
    assert M.esperance_adossement(t, M.kappa(c)) == pytest.approx(6.0)
    assert M.valeurs_issues(t, M.kappa(c)).max() <= 120


def test_changer_cote_mythique():
    cfg = M.charger_config(RACINE / "configs" / "serie1-A-10near.yaml")
    for cote in (1000, 2000, 10000):
        c = M.changer_cote_mythique(cfg, 1 / cote)
        M.valider_config(c)
        assert 1 / M.analytique(c)["p_au_moins_un_mythique"] == pytest.approx(cote, rel=1e-6)


def test_vcap_borne_les_boosters():
    cfg = M.charger_config(RACINE / "configs" / "exemple-4-4.yaml")
    c = M.avec(cfg, v_cap=20)
    t = M.construire_tables(c)
    iss = S.tirer_issues(t, 100_000, np.random.default_rng(0))
    assert S.valeurs_boosters(c, t, iss).max() <= 20


def test_ruine_decroit_avec_r0():
    cfg = M.charger_config(RACINE / "configs" / "exemple-4-4.yaml")
    r = S.ruine(cfg, n_trajectoires=500, horizon=2000, grille_r0=[250, 400, 600, 900])
    ps = [p for _, p in r["courbe"]]
    assert ps == sorted(ps, reverse=True)
    assert ps[0] > ps[-1]


def test_config_invalide_refusee():
    cfg = M.charger_config(RACINE / "configs" / "exemple-4-4.yaml")
    with pytest.raises(ValueError):
        M.valider_config(M.avec(cfg, **{"emplacements.tables.standard.commune": 0.5}))
