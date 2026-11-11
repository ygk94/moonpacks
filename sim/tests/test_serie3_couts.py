"""Série 3 : coûts d'un pack, rentabilité, configs à bas prix."""
import math

import pytest

from conftest import RACINE
from memaster_sim import couts as K
from memaster_sim import modele as M
from memaster_sim import serie3 as S3


def test_gaz_et_stockage_mesures():
    p = K.PARAMS_DEFAUT
    assert K.gaz_near(p) == pytest.approx(0.0048)          # 48 Tgas à 1e8 yocto/gaz
    assert K.stockage_near(p) == pytest.approx(0.0404)     # 4 040 octets à 1e-5 NEAR
    assert K.stockage_near({**p, "octets_par_pack": 1000}) == pytest.approx(0.01)


def test_marge_prudente_a_20_centimes():
    c = K.couts_pack(0.20, 0.65, {"gaz_paye_par": "equipe", "stockage_paye_par": "acheteur", "frais_achat": 0.0075})
    assert c["prix_near"] == pytest.approx(0.08)
    # 0,08 × 0,35 − 0,0048 − 0,0075 × 0,65 × 0,08
    assert c["marge_near"] == pytest.approx(0.08 * 0.35 - 0.0048 - 0.0075 * 0.65 * 0.08)
    assert c["debourse_acheteur_near"] == pytest.approx(0.08 + 0.0404)
    assert c["surcout_affiche_part"] == pytest.approx(0.0404 / 0.08)


def test_stockage_paye_par_l_equipe_rend_20_centimes_deficitaire():
    c = K.couts_pack(0.20, 0.65, {"stockage_paye_par": "equipe", "octets_par_pack": 4040})
    assert c["marge_near"] < 0
    assert c["debourse_acheteur_near"] == pytest.approx(c["prix_near"])


def test_prix_seuil_annule_la_marge():
    p = {"gaz_paye_par": "equipe", "stockage_paye_par": "equipe", "octets_par_pack": 1000}
    for c in (0.5, 0.65, 0.7):
        x = K.prix_seuil_usd(c, p)
        assert K.couts_pack(x, c, p)["marge_near"] == pytest.approx(0, abs=1e-12)
    assert K.prix_seuil_usd(0.65, {"gaz_paye_par": "acheteur", "stockage_paye_par": "acheteur"}) == 0


def test_packs_pour_couts_fixes():
    assert K.packs_pour_couts_fixes(10, 0.0228) == math.ceil(10 / 0.0228)
    assert K.packs_pour_couts_fixes(10, -0.01) == math.inf


def test_remboursement_stockage_au_burn():
    assert K.remboursement_stockage(1) == pytest.approx(0.0404 / 5)


@pytest.mark.parametrize("prix", S3.PRIX_USD)
@pytest.mark.parametrize("couv", S3.COUVERTURES)
def test_configs_generees_tiennent_la_couverture(prix, couv):
    chemin = RACINE / "configs" / f"{S3.nom_fichier(prix, couv)}.yaml"
    cfg = M.charger_config(chemin)
    assert cfg == {**S3.construire_config(prix, couv), "nom": cfg["nom"]}
    assert cfg["prix"] == pytest.approx(prix / 2.5)
    a = M.analytique(cfg)
    assert a["esperance_adossement"] == pytest.approx(couv * cfg["prix"], rel=1e-9)
    # aucune brûlable sous le minimum utile, borne anti-arbitrage loin
    assert min(v["min"] for v in a["valeur_par_rarete"].values()) >= cfg["v_min_brulable"]
    assert a["beta_max_formule"] > couv + 0.1


def test_structure_proportionnelle_au_prix():
    """À couverture égale, l'adossement et σ sont proportionnels au prix : la réserve aussi."""
    a1 = M.analytique(S3.construire_config(0.20, 0.65))
    a2 = M.analytique(S3.construire_config(1.00, 0.65))
    assert a2["sigma_booster"] / a1["sigma_booster"] == pytest.approx(5, rel=1e-6)
    assert a2["r0_normale"] / a1["r0_normale"] == pytest.approx(5, rel=1e-6)
