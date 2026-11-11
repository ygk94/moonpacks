"""Série 3 : coûts réels d'un pack à bas prix, rentabilité et seuil des coûts fixes.

Tout est en NEAR, converti en dollars avec `near_usd` (paramètre). Sources des valeurs par défaut :
- gaz : 48 Tgas au plus pour `buy_pack` (mesure de l'équipe), brûlé à 1e8 yocto/gaz = 0,0001 NEAR/Tgas
  (`docs/faisabilite.md`, partie 3, RPC `gas_price`). Le prépaiement à 0,001 NEAR/Tgas est remboursé à l'écart près.
  Sur NEAR, le gaz est payé par le signataire, donc par l'acheteur (`faisabilite.md` 1.3), sauf relais ou méta-transaction.
- stockage : 4 040 octets au plus par pack aujourd'hui (1 Ko visé), à 0,00001 NEAR par octet (`storage_amount_per_byte`).
  Payé par l'acheteur dans le dépôt de `buy_pack`, en plus du prix, et rendu au burn.
- achat des jetons : groupé, 0,5 à 1 % de la couverture (1Click + écart).

« Couverture » = β : part du prix dépensée en jetons, en moyenne (gold packs compris).
"""
from __future__ import annotations

import math

PARAMS_DEFAUT = {
    "near_usd": 2.5,
    "gaz_tgas": 48.0,
    "near_par_tgas": 0.0001,        # 1e8 yocto par unité de gaz
    "gaz_paye_par": "equipe",       # "acheteur" (cas NEAR normal) ou "equipe" (relais, ou par prudence)
    "octets_par_pack": 4040,
    "near_par_octet": 1e-5,
    "stockage_paye_par": "acheteur",  # "acheteur" (en plus du prix, rendu au burn) ou "equipe"
    "frais_achat": 0.0075,          # part de la couverture : 0,5 à 1 %
    "delta": 0.05,                  # part du prix versée à la réserve (prise sur la marge)
    "cartes_par_pack": 5,
}


def prix_near(prix_usd: float, near_usd: float) -> float:
    return prix_usd / near_usd


def gaz_near(p: dict) -> float:
    return p["gaz_tgas"] * p["near_par_tgas"]


def stockage_near(p: dict) -> float:
    return p["octets_par_pack"] * p["near_par_octet"]


def couts_pack(prix_usd: float, couverture: float, params: dict | None = None) -> dict:
    """Décompte d'un pack : ce que paie l'acheteur, ce que coûte le pack à l'équipe, la marge."""
    p = {**PARAMS_DEFAUT, **(params or {})}
    u = p["near_usd"]
    P = prix_near(prix_usd, u)
    gaz, sto = gaz_near(p), stockage_near(p)
    achat = p["frais_achat"] * couverture * P
    cout_equipe = achat + (gaz if p["gaz_paye_par"] == "equipe" else 0.0) + \
        (sto if p["stockage_paye_par"] == "equipe" else 0.0)
    en_plus_acheteur = (gaz if p["gaz_paye_par"] == "acheteur" else 0.0) + \
        (sto if p["stockage_paye_par"] == "acheteur" else 0.0)
    marge = P * (1 - couverture) - cout_equipe
    return {
        "prix_usd": prix_usd, "prix_near": P, "couverture": couverture,
        "gaz_near": gaz, "stockage_near": sto, "achat_near": achat,
        "cout_equipe_near": cout_equipe, "cout_equipe_usd": cout_equipe * u,
        "marge_near": marge, "marge_usd": marge * u, "marge_part": marge / P,
        "marge_apres_reserve_near": marge - p["delta"] * P,
        "debourse_acheteur_near": P + en_plus_acheteur,
        "debourse_acheteur_usd": (P + en_plus_acheteur) * u,
        "surcout_affiche_part": en_plus_acheteur / P,
        "stockage_par_carte_near": sto / p["cartes_par_pack"],
    }


def prix_seuil_usd(couverture: float, params: dict | None = None) -> float:
    """Prix (en $) où la marge est nulle : P·(1 − β − s·β) = coûts fixes par pack."""
    p = {**PARAMS_DEFAUT, **(params or {})}
    fixe = (gaz_near(p) if p["gaz_paye_par"] == "equipe" else 0.0) + \
        (stockage_near(p) if p["stockage_paye_par"] == "equipe" else 0.0)
    return fixe / (1 - couverture * (1 + p["frais_achat"])) * p["near_usd"]


def packs_pour_couts_fixes(couts_fixes_near: float, marge_par_pack_near: float) -> float:
    """Nombre de packs dont la marge couvre les coûts fixes (déploiement, stockage du contrat et de la série)."""
    if marge_par_pack_near <= 0:
        return math.inf
    return math.ceil(couts_fixes_near / marge_par_pack_near)


def tableau_rentabilite(prix_usd: list[float], couvertures: list[float], variantes: dict[str, dict]) -> list[dict]:
    """Une ligne par (prix, couverture, variante de coûts)."""
    out = []
    for nom, params in variantes.items():
        for c in couvertures:
            for x in prix_usd:
                out.append({"variante": nom, **couts_pack(x, c, params)})
    return out


def remboursement_stockage(cartes_brulees: float, params: dict | None = None) -> float:
    """Stockage rendu (NEAR) quand on brûle `cartes_brulees` cartes d'un pack."""
    p = {**PARAMS_DEFAUT, **(params or {})}
    return stockage_near(p) * cartes_brulees / p["cartes_par_pack"]
