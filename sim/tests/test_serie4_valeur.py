"""Série 4 : tables de valeur V par pack, répartition entre brûlables, gold pack redéfini."""
import json

import numpy as np
import pytest

from memaster_sim import serie3 as S3
from memaster_sim import serie4 as S4
from memaster_sim import valeur as V


@pytest.fixture(scope="module")
def par():
    return S4.charger_parametres()


@pytest.fixture(scope="module")
def cfg(par):
    return S4.construire_config(0.20, par["near_usd"], par["catalogue"]["brulables_communes"])


@pytest.fixture(scope="module")
def pop(par):
    # petite population : g_pop varie peu
    p = dict(par, population={**par["population"], "joueurs": 20000})
    return S4.population(p)


@pytest.fixture(scope="module")
def analyses(par, pop, cfg):
    return {v: S4.analyser(par, v, pop, cfg) for v in par["variantes"]}


# --------------------------------------------------------------------------- TableValeur

def test_table_grandeurs_exactes():
    t = V.TableValeur((2000, 5000, 10000, 20000), (1, 2, 4, 1))
    assert t.total == 8
    assert t.moyenne() == pytest.approx((2000 + 10000 + 40000 + 20000) / 8 / 10000)
    assert t.mediane() == 1.0          # P(V ≤ 0,5) = 3/8 < 1/2 ≤ P(V ≤ 1) = 7/8
    assert t.quantile(0.10) == 0.2 and t.quantile(0.9) == 2.0
    assert t.part_sous(0.5) == pytest.approx(1 / 8)
    assert t.part_au_dessus(1.0) == pytest.approx(1 / 8)
    assert (t.minimum(), t.maximum()) == (0.2, 2.0)


@pytest.mark.parametrize("paliers,poids", [((2000, 2000), (1, 1)), ((3000, 2000), (1, 1)), ((2000,), (0,)),
                                           ((2000, 3000), (1,)), ((2000.0,), (1,))])
def test_table_invalide(paliers, poids):
    with pytest.raises(ValueError):
        V.TableValeur(paliers, poids)


def test_json_aller_retour_et_empreinte():
    t = V.TableValeur((2000, 7500, 20000), (5, 3, 2))
    j = t.en_json()
    assert j == [[2000, 5], [7500, 3], [20000, 2]]
    assert V.TableValeur.depuis_json(j) == t
    assert t.empreinte() == V.TableValeur.depuis_json(json.loads(json.dumps(j))).empreinte()
    assert t.empreinte() != V.TableValeur((2000, 7500, 20000), (5, 3, 3)).empreinte()


def test_paliers():
    p = V.paliers((2000, 10000, 500), (11000, 20000, 1000))
    assert p[0] == 2000 and p[-1] == 20000 and 7500 in p and len(p) == 27
    assert all(b > a for a, b in zip(p, p[1:]))


def test_calibrage_moyenne_exacte():
    p = V.paliers((2000, 10000, 500), (11000, 20000, 1000))
    t = V.table_lognormale(p, 0.75, "moyenne", 0.6)
    assert t.total == 1_000_000
    assert t.moyenne() == pytest.approx(0.75, abs=1e-6)
    assert (t.minimum(), t.maximum()) == (0.2, 2.0)
    assert t.mediane() < 0.75          # asymétrie à droite : beaucoup de petits packs, quelques gros


def test_calibrage_mediane():
    p = V.paliers((2000, 10000, 500), (11000, 20000, 1000))
    t = V.table_lognormale(p, 0.75, "mediane", 0.6)
    assert t.mediane() == 0.75
    assert t.moyenne() > 0.80          # la moyenne monte
    with pytest.raises(ValueError):    # médiane visée hors des paliers
        V.table_lognormale(p, 0.77, "mediane", 0.6)


def test_melange_exact():
    a = V.TableValeur((2000, 10000), (1, 1))
    b = V.TableValeur((10000, 30000), (1, 1))
    vals, prs = V.melange([(a, 0.75), (b, 0.25)])
    assert list(vals) == [0.2, 1.0, 3.0]
    assert prs == pytest.approx([0.375, 0.5, 0.125])
    assert V.resume_loi(vals, prs)["moyenne"] == pytest.approx(0.75 * a.moyenne() + 0.25 * b.moyenne())


# --------------------------------------------------------------------------- composition

def test_retombee_vers_le_bas_puis_le_haut():
    loi = {"commune": 0.6, "rare": 0.2, "epique": 0.1, "legendaire": 0.09, "mythique": 0.01}
    # pas de commune ni de légendaire brûlable : la commune monte à la rare, la légendaire descend à l'épique
    out = V.retombee(loi, {"commune": 0, "rare": 3, "epique": 5, "legendaire": 0, "mythique": 1})
    assert out == pytest.approx({"commune": 0, "rare": 0.8, "epique": 0.19, "legendaire": 0, "mythique": 0.01})
    with pytest.raises(ValueError):
        V.retombee(loi, {})


def test_config_communes_brulables(cfg):
    base = S3.construire_config(0.20, 0.65)
    assert cfg["raretes"]["commune"]["brulables"] == 20
    assert len(cfg["catalogue"]["brulables"]["commune"]) == 20
    assert cfg["raretes"]["commune"]["part_brulable"] == pytest.approx(20 / 1160, abs=1e-6)
    for r in ("rare", "epique", "legendaire", "mythique"):
        assert cfg["catalogue"]["brulables"][r] == base["catalogue"]["brulables"][r]


def test_gold_pack_redefini(par, analyses):
    g = analyses["a"]["types"]["gold"]
    assert len(g.emplacements) == 5 and g.force_brulable == [False] * 4 + [True]
    assert all(loi["commune"] == 0 for loi in g.emplacements)
    assert all(loi["rare"] + loi["epique"] + loi["legendaire"] + loi["mythique"] == pytest.approx(1)
               for loi in g.emplacements)
    assert g.emplacements[2]["rare"] == 0 and g.emplacements[3]["rare"] == 0
    assert g.emplacements[4] == pytest.approx({"commune": 0, "rare": 0, "epique": 0, "legendaire": 0.8, "mythique": 0.2})


def test_tirage_au_moins_une_brulable_et_repartition(par, cfg, analyses):
    mult = par["multiplicateurs"]
    for k, tp in analyses["a"]["types"].items():
        d = V.tirer_packs(tp, cfg, mult, 20000, np.random.default_rng(3))
        assert d["brulable"].sum(1).min() >= 1
        assert d["valeur_carte"].sum(1) == pytest.approx(d["V"])
        assert (d["valeur_carte"][~d["brulable"]] == 0).all()
        assert set(np.unique(d["V"])) <= set(tp.table.valeurs)
        if k == "gold":
            assert (d["rarete"] > 0).all()           # aucune commune
    # au prorata des multiplicateurs : deux brûlables d'un même pack ont des valeurs dans le rapport m_i / m_j
    d = V.tirer_packs(analyses["a"]["types"]["gold"], cfg, mult, 5000, np.random.default_rng(4))
    m = V.multiplicateurs_vec(mult)
    i = np.flatnonzero(d["brulable"].sum(1) >= 2)[0]
    j = np.flatnonzero(d["brulable"][i])
    a, b = j[0], j[1]
    ra, rb = d["rarete"][i, a], d["rarete"][i, b]
    assert d["valeur_carte"][i, a] / d["valeur_carte"][i, b] == pytest.approx(m[ra] / m[rb])


def test_moyenne_simulee_egale_table(par, cfg, analyses):
    tp = analyses["a"]["types"]["normal"]
    d = V.tirer_packs(tp, cfg, par["multiplicateurs"], 400_000, np.random.default_rng(5))
    assert d["V"].mean() == pytest.approx(tp.table.moyenne(), abs=0.004)


# --------------------------------------------------------------------------- couverture, mythique, réserve

def test_couverture_globale(analyses, pop):
    a = analyses["a"]
    parts = a["parts"]
    assert sum(parts.values()) == pytest.approx(1)
    attendu = sum(parts[k] * a["tables"][k].moyenne() for k in S4.TYPES)
    assert a["couverture"]["avec_pitie_et_rush"] == pytest.approx(attendu)
    assert a["global"]["moyenne"] == pytest.approx(attendu)
    assert a["couverture"]["effet_gold"] == pytest.approx(pop["g_pop"] * (a["tables"]["gold"].moyenne() - 0.75), abs=1e-6)
    # la table normale qui donnerait 75 % au global
    t = a["couverture"]["normal_pour_75_global"]
    assert parts["normal"] * t + parts["gold"] * a["tables"]["gold"].moyenne() + \
        parts["rush"] * a["tables"]["rush"].moyenne() == pytest.approx(0.75)


def test_rush_sous_80_ou_simplifie(analyses):
    a, b = analyses["a"], analyses["b"]
    assert not a["rush_simplifie"] and a["tables"]["rush"].moyenne() == pytest.approx(0.80, abs=1e-6)
    assert b["rush_simplifie"] and b["tables"]["rush"] == b["tables"]["normal"]


def test_mythique_hors_v(analyses):
    m = analyses["a"]["mythique"]
    assert m["dans_v"]["cout_moyen"] == 0
    assert m["hors_v"]["cout_par_pack_du_type"]["gold"] == pytest.approx(0.2 * m["valeur_x_prix"])
    assert m["hors_v"]["cout_moyen"] > 0.4         # hors V à 55 × prix : intenable
    s = analyses["a"]["stocks"]
    assert s["epuisement_mythiques"] < 5000 < s["epuisement_mythiques_sans_gold"]


def test_reserve_sans_alea():
    vals, prs = np.array([0.75]), np.array([1.0])
    r = V.reserve_ruine(vals, prs, 0.75, 1000, 20)
    assert r["r0_0.01"] == pytest.approx(0.75)
    r = V.reserve_ruine(np.array([0.5, 1.0]), np.array([0.5, 0.5]), 0.80, 10_000, 200, seed=1)
    assert 1.0 < r["r0_0.01"] < 20


def test_variantes_marge_et_arbitrage(par, analyses):
    import memaster_sim.couts as K
    ca = analyses["a"]["couverture"]["avec_pitie_et_rush"]
    cb = analyses["b"]["couverture"]["avec_pitie_et_rush"]
    assert cb > ca
    ma = K.couts_pack(0.20, ca, S4._params_couts(par))["marge_usd"]
    mb = K.couts_pack(0.20, cb, S4._params_couts(par))["marge_usd"]
    assert ma > 0.02 and mb < 0.01
    ba, bb = analyses["a"]["arbitrage"], analyses["b"]["arbitrage"]
    assert max(ba["normal"], ba["rush"], ba["cycle_pitie"]) < ba["borne"]
    assert bb["cycle_pitie"] > bb["borne"]


def test_json_publie(par, analyses):
    j = S4.tables_json(par, analyses["a"])
    assert set(j["value_tables"]) == {"base", "gold", "rush"}
    assert j["weight_total"] == 1_000_000 and "_format" in j
    assert set(j["split_multipliers"]) == {"common", "rare", "epic", "legendary", "mythic"}
    assert all(isinstance(x, int) for x in j["split_multipliers"].values())
    assert j["gold_pack"]["last_slot_weights_ppm"] == {"legendary": 800_000, "mythic": 200_000}
    for k, t in j["value_tables"].items():
        tv = V.TableValeur.depuis_json(t["tiers"])
        assert tv.total == j["weight_total"]
        assert t["sha256"] == tv.empreinte()
    assert j["value_tables"]["base"]["min_bps"] == 2000 and j["value_tables"]["base"]["max_bps"] == 20000
    assert j["value_tables"]["rush"]["mean_bps"] <= 8000


def test_json_du_depot_a_jour(par, analyses):
    """resultats/serie4/tables-valeur.json correspond aux paramètres actuels (relancer `serie4 run` sinon)."""
    chemin = S4.SORTIE / "tables-valeur.json"
    if not chemin.exists():
        pytest.skip("série 4 pas encore lancée")
    publie = json.loads(chemin.read_text(encoding="utf-8"))
    attendu = S4.tables_json(par, analyses[par["recommandee"]])
    for k in ("base", "gold", "rush"):
        assert publie["value_tables"][k]["tiers"] == attendu["value_tables"][k]["tiers"]
    assert publie["split_multipliers"] == attendu["split_multipliers"]
