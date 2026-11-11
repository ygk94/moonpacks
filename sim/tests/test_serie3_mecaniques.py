"""Série 3 : table or, pitié, gold rush, rareté par les burns, résurrection."""
import numpy as np
import pytest

from memaster_sim import catalogue as C
from memaster_sim import gold as G
from memaster_sim import modele as M
from memaster_sim import pitie as Pi
from memaster_sim import rarete_burn as RB
from memaster_sim import resurrection as Rs
from memaster_sim import rush as Ru
from memaster_sim import serie3 as S3
from memaster_sim import simulation as S


@pytest.fixture(scope="module")
def cfg():
    return S3.construire_config(0.20, 0.65)


# --------------------------------------------------------------------------- table or et mélange

def test_table_or_renforce_et_reste_une_loi(cfg):
    o = G.table_or(cfg, {"rare": 2, "epique": 3, "legendaire": 4, "mythique": 4})
    for nom, t in o["emplacements"]["tables"].items():
        assert sum(t.values()) == pytest.approx(1)
        base = cfg["emplacements"]["tables"][nom]
        assert t["epique"] == pytest.approx(3 * base["epique"])
        assert t["commune"] < base["commune"]
    with pytest.raises(ValueError):
        G.table_or(cfg, {"rare": 5, "epique": 5})


def test_calibrage_tient_la_couverture_moyenne(cfg):
    o = G.table_or(cfg)
    for g in (0.0, 0.05, 0.2):
        c = G.calibrer(cfg, o, g)
        assert c["couverture_moyenne"] == pytest.approx(0.65, rel=1e-9)
        assert c["couverture_or"] > c["couverture_std"]
    assert G.calibrer(cfg, o, 0.1)["couverture_std"] < G.calibrer(cfg, o, 0.05)["couverture_std"]


def test_melange_n_a_deux_tables_egale_melanger(cfg):
    o = G.table_or(cfg)
    a = G.melanger(cfg, o, 0.07)
    b = G.melanger_n(cfg, [(o, 0.07)])
    assert a["emplacements"] == b["emplacements"]


def test_pertes_max_n_suit_les_parts(cfg):
    o = G.table_or(cfg)
    kap = M.kappa(G.melanger(cfg, o, 0.3))
    apport = (cfg["beta"] + cfg["delta"]) * cfg["prix"]
    D = G.pertes_max_n(cfg, [(o, 0.3)], kap, [apport, cfg["v_cap"]], 50, 2000, seed=1)
    assert D.shape == (2, 50)
    assert np.all(D[1] == 0)            # apport ≥ V_cap : la réserve ne baisse jamais
    assert np.all(D[0] >= 0)
    # avec des drapeaux forcés (tout en or), l'adossement moyen est celui de la table or
    rng = np.random.default_rng(2)
    t_o = M.construire_tables(o)
    v = G.valeurs_packs_n([cfg, o], kap, np.ones(200_000, dtype=int), rng)
    assert v.mean() == pytest.approx(M.esperance_adossement(t_o, kap), rel=0.03)


# --------------------------------------------------------------------------- pitié

def test_loi_du_cycle_et_garantie():
    f = Pi.loi_cycle(0.02, 0.002, 20)
    assert f.sum() == pytest.approx(1)
    assert Pi.proba_gold(19, 0.02, 0.002, 20) == 1
    assert Pi.proba_gold(0, 0.02, 0.002, 20) == pytest.approx(0.02)
    # sans montée, la chance constante p donne un cycle géométrique tronqué
    p = 0.1
    L = Pi.duree_moyenne_cycle(p, 0.0, 1000)
    assert L == pytest.approx(1 / p, rel=1e-6)
    assert Pi.g_stationnaire(0.02, 0.0, 1) == 1          # N = 1 : chaque pack est en or


def test_k_pour_g_inverse_g_stationnaire():
    k = Pi.k_pour_g(0.0665, 0.02, 20)
    assert Pi.g_stationnaire(0.02, k, 20) == pytest.approx(0.0665, rel=1e-6)


def test_population_infinie_retrouve_g_stationnaire():
    rng = np.random.default_rng(3)
    r = Pi.simuler_population(np.full(2000, 500), 0.02, 0.002, 20, rng)
    assert r["g_pop"] == pytest.approx(Pi.g_stationnaire(0.02, 0.002, 20), rel=0.03)


def test_petits_joueurs_voient_moins_de_gold():
    rng = np.random.default_rng(4)
    pk = Pi.packs_par_joueur(20000, rng)
    assert pk.min() >= 1 and np.median(pk) == pytest.approx(4, abs=1)
    r = Pi.simuler_population(pk, 0.02, 0.002, 20, rng)
    assert r["g_pop"] < Pi.g_stationnaire(0.02, 0.002, 20)
    assert 0 < r["part_gold_garantis"] < 1


# --------------------------------------------------------------------------- gold rush

def test_rush_jamais_sous_le_palier():
    r = Ru.simuler({"jours": 2, "lambda_base_h": 50, "pics_par_jour": 0, "palier": 10_000}, 2, seed=1)
    assert r["moyennes"]["g_rush"] == 0
    assert r["moyennes"]["packs_par_jour"] == pytest.approx(1200, rel=0.1)


def test_rush_toujours_au_dessus_du_palier():
    r = Ru.simuler({"jours": 2, "lambda_base_h": 500, "pics_par_jour": 0, "palier": 1, "cooldown_s": 0}, 2, seed=1)
    assert r["moyennes"]["temps_en_rush"] > 0.95


def test_cooldown_et_palier_relatif_bornent_le_rush():
    base = {"jours": 10, "pics_par_jour": 1, "palier": 600}
    fort = Ru.simuler({**base, "lambda_base_h": 800}, 2, seed=2)["moyennes"]["g_rush"]
    borne = Ru.simuler({**base, "lambda_base_h": 800, "cooldown_s": 21600, "palier": 50, "palier_relatif": 2.5}, 2,
                       seed=2)["moyennes"]["g_rush"]
    assert fort > 0.5 and borne < 0.2


def test_suite_packs_respecte_les_ventes():
    f = Ru.simuler_flux({"jours": 1, "lambda_base_h": 300, "palier": 100}, np.random.default_rng(5))
    s = Ru.suite_packs(f)
    assert s.size == f["ventes"].sum()
    assert s.sum() == f["ventes"][f["rush"]].sum()


def test_table_rush_pour_couverture(cfg):
    t_p = G.table_or(cfg)
    t_r, kap, s = S3.table_rush_pour_couverture(cfg, t_p, 0.05, 0.05, G.FACTEURS_OR_DEFAUT, 0.80)
    assert 0 < s < 1
    assert M.esperance_adossement(M.construire_tables(t_r), kap) / cfg["prix"] == pytest.approx(0.80, rel=1e-4)


# --------------------------------------------------------------------------- rareté pilotée par les burns

def test_sans_burn_rien_ne_bouge(cfg):
    r = RB.simuler(cfg, {"taux_burn": 0, "horizon": 20_000})
    assert r["couverture_finale"] == pytest.approx(0.65)
    assert r["ratio_min_final"] == 1 and r["coins_au_plancher"] == 0


def test_formule_brute_fait_baisser_la_couverture(cfg):
    r = RB.simuler(cfg, {"taux_burn": 0.5, "horizon": 50_000})
    assert r["couverture_finale"] < 0.55
    assert r["brulables_par_pack_final"] < r["brulables_par_pack_initial"]


def test_recalibrage_tient_beta_mais_monte_la_variance(cfg):
    r = RB.simuler(cfg, {"taux_burn": 0.5, "horizon": 50_000, "kappa": "recalibre"})
    assert r["couverture_finale"] == pytest.approx(0.65, rel=1e-3)
    assert r["kappa_final_rel"] > 1.1 and r["sigma_final"] > r["sigma_initial"]


def test_variante_entre_brulables_et_plancher(cfg):
    r = RB.simuler(cfg, {"taux_burn": 0.8, "horizon": 50_000, "renormaliser": "brulables", "plancher": 0.25})
    assert r["couverture_finale"] == pytest.approx(0.65, rel=1e-3)
    assert r["sigma_final"] == pytest.approx(r["sigma_initial"], rel=1e-6)
    assert r["ratio_min_final"] >= 0.25
    with pytest.raises(ValueError):
        RB.simuler(cfg, {"renormaliser": "autre", "horizon": 500})


# --------------------------------------------------------------------------- résurrection

def test_coins_morts_du_catalogue():
    m = Rs.coins_morts(C.charger_catalogue_v2())
    assert m["mythique"] == 0 and m["rare"] == 0
    assert m["commune"] > 1000 and m["epique"] == 84 and m["legendaire"] == 2


def test_cout_resurrection_proportionnel(cfg):
    morts = {"commune": 0, "rare": 0, "epique": 100, "legendaire": 0, "mythique": 0}
    prm = {"p_an": 0.05, "mois": 12, "packs_par_mois": 10_000, "surcout_achat": 0.0}
    r = Rs.simuler(cfg, morts, prm, n_sim=50_000)
    ex = Rs.exemplaires_par_carte_et_pack(cfg)["epique"] * 120_000
    v = Rs.valeur_brulable_par_rarete(cfg)["epique"]
    # E[coût] = n · p · E[instant] · exemplaires · valeur, instant uniforme sur l'horizon
    assert r["cout_moyen_near"] == pytest.approx(100 * 0.05 * 0.5 * ex * v, rel=0.03)
    # le coût rapporté aux ventes ne dépend pas du volume
    r2 = Rs.simuler(cfg, morts, {**prm, "packs_par_mois": 40_000}, n_sim=50_000)
    assert r2["cout_moyen_par_pack_part_prix"] == pytest.approx(r["cout_moyen_par_pack_part_prix"], rel=0.03)


def test_enveloppe_borne_le_cout(cfg):
    morts = Rs.coins_morts(C.charger_catalogue_v2())
    r = Rs.simuler(cfg, morts, {"p_an": 0.02, "enveloppe_near": 1.0, "rho": 0.01}, n_sim=5000)
    assert r["enveloppe_cout_p99_near"] <= r["resurrections_p99"] * 1.0 + 1e-9
    assert r["enveloppe_cout_moyen_near"] < r["cout_moyen_near"]
    assert Rs.rho_pour_risque(cfg, morts, {"p_an": 0.02}, n_sim=5000) == pytest.approx(
        r["cout_p99_near"] / (r["ventes_totales"] * cfg["prix"]), rel=0.1)


def test_valeur_brulable_suit_kappa(cfg):
    v = Rs.valeur_brulable_par_rarete(cfg)
    assert v["commune"] < v["rare"] < v["epique"] < v["legendaire"]
    # cohérente avec le Monte-Carlo : moyenne d'une épique brûlable tirée
    t = M.construire_tables(cfg)
    iss = S.tirer_issues(t, 400_000, np.random.default_rng(6))
    val = M.valeurs_issues(t, M.kappa(cfg))[iss]
    sel = (t.issue_rarete[iss] == t.raretes.index("epique")) & t.issue_brulable[iss]
    assert val[sel].mean() == pytest.approx(v["epique"], rel=0.02)
