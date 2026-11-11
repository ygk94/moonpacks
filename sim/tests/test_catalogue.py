"""Chargeur du catalogue v2 et configs de la série 2."""
import json

import pytest

from conftest import RACINE
from memaster_sim import catalogue as C
from memaster_sim import modele as M
from memaster_sim import serie2 as S2


@pytest.fixture(scope="module")
def cartes():
    return C.charger_catalogue_v2()


def test_effectifs_catalogue_v2(cartes):
    assert C.effectifs(cartes) == {"commune": 1160, "rare": 230, "epique": 235, "legendaire": 21, "mythique": 3}
    assert len(cartes) == 1649


def test_ignore_a_decider_et_normalise_les_accents(tmp_path):
    brut = [
        {"id": "a", "section": "catalogue", "rarete": "épique", "etat": "actif", "drapeau": ""},
        {"id": "b", "section": "catalogue", "rarete": "Légendaire", "etat": "mort", "drapeau": ""},
        {"id": "c", "section": "à décider", "rarete": "commune", "etat": "actif", "drapeau": ""},
        {"id": "d", "section": "catalogue", "rarete": "commune", "etat": "actif", "drapeau": "arnaque avérée"},
    ]
    chemin = tmp_path / "cat.json"
    chemin.write_text(json.dumps(brut, ensure_ascii=False), encoding="utf-8")
    cs = C.charger_catalogue_v2(chemin)
    assert [c["id"] for c in cs] == ["a", "b", "d"]
    assert C.effectifs(cs) == {"commune": 1, "rare": 0, "epique": 1, "legendaire": 1, "mythique": 0}
    # jeton mort et arnaque avérée exclus des candidates
    assert C.candidats(cs)["legendaire"] == [] and C.candidats(cs)["commune"] == []
    with pytest.raises(ValueError):
        C.normaliser_rarete("ultra")


@pytest.mark.parametrize("total", S2.TOTAUX)
def test_repartition_par_le_haut(cartes, total):
    rep = C.repartir_brulables(total, cartes)
    eff = C.effectifs(cartes)
    assert sum(rep.values()) == total
    assert rep["mythique"] == 3
    for r, k in rep.items():
        assert k <= C.PLAFONDS_PART_BRULABLE[r] * eff[r]
    # on ne descend d'un palier que si le palier du dessus est plein
    ordre = C.ORDRE_RARETES
    cand = C.candidats(cartes)
    for haut, bas in zip(ordre, ordre[1:]):
        if rep[bas] > 0:
            assert rep[haut] == min(len(cand[haut]), int(C.PLAFONDS_PART_BRULABLE[haut] * eff[haut]))


def test_choix_reproductible_emboite_et_valide(cartes):
    petit = C.choisir_brulables(cartes, C.repartir_brulables(60, cartes), graine=7)
    grand = C.choisir_brulables(cartes, C.repartir_brulables(150, cartes), graine=7)
    assert petit == C.choisir_brulables(cartes, C.repartir_brulables(60, cartes), graine=7)
    assert C.choisir_brulables(cartes, C.repartir_brulables(60, cartes), graine=8) != petit
    par_id = {c["id"]: c for c in cartes}
    for r, ids in grand.items():
        assert set(petit[r]) <= set(ids)
        assert len(set(ids)) == len(ids)
        for i in ids:
            assert par_id[i]["rarete"] == r and C.est_candidate_brulable(par_id[i])


def test_trop_de_brulables_refuse(cartes):
    with pytest.raises(ValueError):
        C.repartir_brulables(10_000, cartes)


@pytest.mark.parametrize("prix", S2.PRIX)
@pytest.mark.parametrize("total", S2.TOTAUX)
def test_configs_serie2_a_jour(cartes, total, prix):
    """Les fichiers configs/serie2-*.yaml correspondent au chargeur (sinon : python -m memaster_sim.serie2 configs)."""
    cfg = M.charger_config(RACINE / "configs" / f"{S2.nom_fichier(total, prix)}.yaml")
    attendu = S2.construire_config(total, prix, cartes)
    assert cfg == attendu
    for r, x in cfg["raretes"].items():
        assert x["part_brulable"] == pytest.approx(x["brulables"] / x["effectif"], abs=1e-6)
        assert len(cfg["catalogue"]["brulables"].get(r, [])) == x["brulables"]
    a = M.analytique(S2.rendre_realisable(cfg)[0])
    assert 1 / a["p_au_moins_un_mythique"] == pytest.approx(S2.BASE[prix]["cote_mythique"], rel=1e-6)
    assert a["valeur_par_rarete"]["mythique"]["max"] == S2.BASE[prix]["valeur_mythique"] <= cfg["v_cap"]


def test_tables_serie2_respectent_la_pyramide(cartes):
    eff = C.effectifs(cartes)
    tab = S2.tables_rarete(eff, 5000)
    par_booster = {r: 4 * tab["standard"][r] + tab["favorable"][r] for r in eff}
    par_exemplaire = [par_booster[r] / eff[r] for r in ["commune", "rare", "epique", "legendaire", "mythique"]]
    assert par_exemplaire == sorted(par_exemplaire, reverse=True)
    for a, b in zip(par_exemplaire[:3], par_exemplaire[1:4]):
        assert a / b == pytest.approx(S2.FACTEUR_PALIER, rel=1e-3)
