"""Série 5 : pitié sans garantie (plafond p_max), mythique ~1e-6 par pack classique, gold 99/1, V moyenne 75 %."""
import numpy as np
import pytest

from memaster_sim import pitie as Pi
from memaster_sim import serie4 as S4
from memaster_sim import serie5 as S5
from memaster_sim import valeur as V

P0, PMAX = 1 / 50_000, 1 / 25_000
K = (PMAX - P0) / 1000


@pytest.fixture(scope="module")
def par():
    return S5.charger_parametres()


@pytest.fixture(scope="module")
def cfg(par):
    return S5.construire_config(0.20, par)


@pytest.fixture(scope="module")
def analyse(par, cfg):
    p = dict(par, population={**par["population"], "joueurs": 5000})
    pop = S4.population(p)
    return S4.analyser(par, par["recommandee"], pop, cfg)


# --------------------------------------------------------------------------- pitié sans N

def test_parametres_pitie(par):
    pi = par["pitie"]
    assert pi["N"] is None
    assert (pi["p0"], pi["p_max"], pi["k"]) == pytest.approx((P0, PMAX, K))


def test_proba_gold_sans_garantie_plafonnee():
    n = np.array([0, 500, 999, 1000, 1001, 10**6])
    h = Pi.proba_gold(n, P0, K, None, PMAX)
    assert h[0] == pytest.approx(P0)
    assert h[1] == pytest.approx(P0 + 500 * K)
    assert h[3:] == pytest.approx(PMAX)
    assert (h <= PMAX).all() and (h < 1).all()      # jamais de garantie
    assert Pi.part_garantie(P0, K, None, PMAX) == 0.0
    m, hs = Pi.debut_plafond(P0, K, PMAX)
    assert 1000 <= m <= 1001 and hs == PMAX


def test_g_inf_queue_geometrique_exacte():
    """E[T] analytique = somme tronquée très longue de S(j) (la queue au-delà est négligeable)."""
    e = Pi.duree_moyenne_cycle(P0, K, None, PMAX)
    S = Pi.survie(P0, K, None, PMAX, 3_000_000)
    assert S[-1] < 1e-40
    assert e == pytest.approx(S.sum(), rel=1e-9)
    assert 25_000 < e < 25_500
    # hasard constant : cycle géométrique
    assert Pi.duree_moyenne_cycle(0.01, 0.0, None) == pytest.approx(100)
    # avec un N très grand et le même plafond, l'ancien calcul retrouve la même valeur
    assert Pi.duree_moyenne_cycle(0.02, 0.0002, None, 0.05) == pytest.approx(
        Pi.duree_moyenne_cycle(0.02, 0.0002, 5000, 0.05), rel=1e-9)


def test_g_inf_coherent_avec_monte_carlo():
    gi = Pi.g_stationnaire(P0, K, None, PMAX)
    T = Pi.mc_cycles(100_000, P0, K, PMAX, np.random.default_rng(5))
    assert 1 / T.mean() == pytest.approx(gi, rel=4 * T.std() / np.sqrt(T.size) / T.mean())
    fl = Pi.mc_flux_stationnaire(20_000, 1000, P0, K, PMAX, np.random.default_rng(6))
    assert fl["g"] == pytest.approx(gi, rel=4 / np.sqrt(fl["golds"]))


def test_g_pop_exact_et_simulation():
    """Équation de renouvellement contre simulation pack par pack (hasard élevé pour avoir des golds)."""
    pk = Pi.packs_par_joueur(20_000, np.random.default_rng(3), 30, 1.0, 400)
    ex = Pi.g_pop_exact(pk, 0.002, 0.0001, None, 0.02)
    mc = Pi.simuler_population(pk, 0.002, 0.0001, None, np.random.default_rng(4), 0.02)
    assert mc["g_pop"] == pytest.approx(ex, rel=4 / np.sqrt(mc["golds"]))
    assert ex < Pi.g_stationnaire(0.002, 0.0001, None, 0.02)
    # avec garantie, golds_attendus retrouve g_∞ sur un très long horizon
    e = Pi.golds_attendus(4000, 0.02, 0.002, 20)
    assert e[-1] / 4000 == pytest.approx(Pi.g_stationnaire(0.02, 0.002, 20), rel=0.01)


# --------------------------------------------------------------------------- tables de valeur

def test_moyennes_exactes(analyse):
    t = analyse["tables"]
    for k in ("normal", "rush"):
        assert sum(p * w for p, w in zip(t[k].paliers, t[k].poids)) == 7500 * 1_000_000
        assert t[k].total == 1_000_000
        assert t[k].minimum() == 0.2 and t[k].maximum() == 2.0
    assert t["rush"].moyenne() <= 0.80
    assert t["gold"].moyenne() == pytest.approx(2.0, abs=1e-6)


def test_tables_json(par, analyse):
    d = S4.tables_json(par, analyse)
    vt = d["value_tables"]
    assert vt["base"]["mean_bps"] == 7500 and vt["rush"]["mean_bps"] == 7500
    assert d["gold_pack"]["last_slot_weights_ppm"] == {"legendary": 990000, "mythic": 10000}
    assert d["split_multipliers"]["mythic"] == 0
    s4 = S4.tables_json(S4.charger_parametres(), S4.analyser(
        S4.charger_parametres(), "a", {"g_pop": 0.07, "g_inf": 0.08},
        S4.construire_config(0.20, 2.5, 20)))
    assert vt["gold"] == s4["value_tables"]["gold"]


# --------------------------------------------------------------------------- mythiques

def test_mythique_un_par_million_de_packs_classiques(analyse, par):
    er = {k: V.esperance_raretes(tp)["mythique"] for k, tp in analyse["types"].items()}
    assert er["normal"] == pytest.approx(1e-6, rel=1e-9)
    assert er["rush"] == pytest.approx(1e-6, rel=1e-9)
    assert er["gold"] == pytest.approx(0.01, rel=0.01)
    # le 5e emplacement des packs classiques et l'emplacement brûlable du gold ne sont jamais mythiques
    for k in ("normal", "rush"):
        assert analyse["types"][k].emplacements[-1]["mythique"] == 0
    g = analyse["types"]["gold"]
    assert g.force_brulable == [False, True, False, False, False]
    assert g.emplacements[1]["mythique"] == 0
    assert g.emplacements[-1]["legendaire"] == pytest.approx(0.99)


def test_config_mythique_non_brulable(cfg):
    assert cfg["raretes"]["mythique"]["part_brulable"] == 0
    assert cfg["raretes"]["mythique"]["brulables"] == 0
    for t in cfg["emplacements"]["tables"].values():
        assert t["mythique"] == pytest.approx(5 / 2e7)
        assert sum(t.values()) == pytest.approx(1)


def test_composition_mythique_sans_valeur(analyse, cfg, par):
    d = V.tirer_packs(analyse["types"]["gold"], cfg, par["multiplicateurs"], 20_000, np.random.default_rng(8))
    myth = d["rarete"] == V.RARETES.index("mythique")
    assert myth.any()
    assert (d["valeur_carte"][myth] == 0).all() and not d["brulable"][myth].any()
    assert d["valeur_carte"].sum(1) == pytest.approx(d["V"])


def test_arbitrage_sous_la_borne(analyse):
    b = analyse["arbitrage"]
    for k in ("normal", "rush", "cycle_pitie"):
        assert b[k] < b["borne"]
