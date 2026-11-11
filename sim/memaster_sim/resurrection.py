"""Résurrection des coins morts : si le cours d'un coin mort remonte, ses cartes existantes deviennent brûlables.

Ces cartes ont été vendues comme cartes de collection, sans jetons achetés. À la résurrection, il faut acheter d'un coup
les jetons de tous les exemplaires en circulation : c'est un engagement non provisionné, qui grossit avec les ventes.

Modèle :
- coins morts : cartes du catalogue v2 dont l'état commence par « mort » (hors arnaques avérées) ;
- un coin mort ressuscite avec la probabilité `p_an` par an, indépendamment des autres, à un instant uniforme ;
- exemplaires en circulation au moment t : ventes(t) × cartes de cette rareté par pack / effectif de la rareté
  (tirage uniforme dans la rareté, comme en série 2), moins une part `part_perdue` (comptes abandonnés) ;
- valeur d'un exemplaire ressuscité : celle d'une brûlable de la même rareté, E[min(κ·w·m, plafond)] ;
- surcoût d'achat `surcout_achat` : on achète un micro-cap qui vient de monter, avec peu de profondeur.

Deux règles :
- « pleine valeur » : chaque exemplaire reçoit la valeur d'une brûlable ;
- « enveloppe » : chaque résurrection reçoit au plus `enveloppe_near`, partagée entre les exemplaires, et le fonds de
  résurrection (alimenté à `rho` du prix) plafonne le total. L'engagement est alors borné par construction.
"""
from __future__ import annotations

import numpy as np

from . import catalogue as C
from . import modele as M

PARAMS_DEFAUT = {"p_an": 0.02, "mois": 12, "packs_par_mois": 50_000, "part_perdue": 0.0, "surcout_achat": 0.10,
                 "enveloppe_near": None, "rho": 0.0}


def coins_morts(cartes: list[dict]) -> dict[str, int]:
    out = {r: 0 for r in reversed(C.ORDRE_RARETES)}
    for c in cartes:
        etat = str(c.get("etat", "")).lower()
        drapeau = str(c.get("drapeau", "")).lower()
        if c["rarete"] != "mythique" and etat.startswith("mort") and "arnaque" not in drapeau:
            out[c["rarete"]] += 1
    return out


def valeur_brulable_par_rarete(cfg: dict) -> dict[str, float]:
    """E[v] d'une carte brûlable de chaque rareté (valeur qu'aurait un exemplaire ressuscité)."""
    t = M.construire_tables(cfg)
    pb = M.proba_issues_booster(t)
    v = M.valeurs_issues(t, M.kappa(cfg))
    out = {}
    for i, nom in enumerate(t.raretes):
        if nom == "mythique":
            continue
        sel = (t.issue_rarete == i) & t.issue_brulable
        poids = pb[:, sel].sum(0)
        if poids.sum() > 0:
            out[nom] = float((poids * v[sel]).sum() / poids.sum())
        else:  # aucune brûlable de cette rareté : même formule, poids et multiplicateur de la config
            vals, pis = M._multiplicateur(cfg, nom)
            r = cfg["raretes"][nom]
            out[nom] = float((pis * np.minimum(M.kappa(cfg) * r["poids"] * vals, r.get("plafond", np.inf))).sum())
    return out


def exemplaires_par_carte_et_pack(cfg: dict) -> dict[str, float]:
    t = M.construire_tables(cfg)
    pb = M.proba_issues_booster(t)
    out = {}
    for i, nom in enumerate(t.raretes):
        out[nom] = float((pb * (t.issue_rarete == i)).sum()) / cfg["raretes"][nom]["effectif"]
    return out


def simuler(cfg: dict, morts: dict[str, int], params: dict | None = None, n_sim: int = 20_000, seed: int = 9,
            risque: float = 0.01) -> dict:
    """Distribution du coût total des résurrections sur l'horizon."""
    p = {**PARAMS_DEFAUT, **(params or {})}
    rng = np.random.default_rng(seed)
    P = cfg["prix"]
    vals = valeur_brulable_par_rarete(cfg)
    ex = exemplaires_par_carte_et_pack(cfg)
    T = p["mois"]
    ventes_totales = p["packs_par_mois"] * T
    proba_horizon = 1 - (1 - p["p_an"]) ** (T / 12)
    cout = np.zeros(n_sim)
    cout_enveloppe = np.zeros(n_sim)
    n_res = np.zeros(n_sim)
    fonds = p["rho"] * P * ventes_totales
    par_rarete = {}
    for nom, n in morts.items():
        if n == 0:
            continue
        k = rng.binomial(n, proba_horizon, n_sim)
        n_res += k
        kmax = int(k.max()) if k.size else 0
        if kmax == 0:
            continue
        # instants de résurrection uniformes sur l'horizon : exemplaires ∝ ventes déjà faites
        instants = rng.random((n_sim, kmax))
        actif = np.arange(kmax)[None, :] < k[:, None]
        copies = instants * ventes_totales * ex[nom] * (1 - p["part_perdue"])
        par_res = copies * vals[nom] * (1 + p["surcout_achat"])
        c_r = (par_res * actif).sum(1)
        cout += c_r
        par_rarete[nom] = float(c_r.mean() / (ventes_totales * P))
        if p["enveloppe_near"] is not None:
            cout_enveloppe += (np.minimum(par_res, p["enveloppe_near"]) * actif).sum(1)
    out = {
        "params": p, "ventes_totales": ventes_totales, "proba_resurrection_horizon": proba_horizon,
        "coins_morts": morts, "valeur_par_rarete": vals,
        "exemplaires_par_coin_fin": {r: ex[r] * ventes_totales for r in morts},
        "resurrections_moyennes": float(n_res.mean()),
        "cout_moyen_near": float(cout.mean()),
        "cout_p95_near": float(np.quantile(cout, 0.95)), "cout_p99_near": float(np.quantile(cout, 0.99)),
        "cout_moyen_par_pack_part_prix": float(cout.mean() / (ventes_totales * P)),
        "cout_p99_par_pack_part_prix": float(np.quantile(cout, 0.99) / (ventes_totales * P)),
        "cout_quantile_near": float(np.quantile(cout, 1 - risque)),
        "cout_moyen_part_prix_par_rarete": par_rarete,
        "resurrections_p99": float(np.quantile(n_res, 0.99)),
    }
    if p["enveloppe_near"] is not None:
        plafonne = np.minimum(cout_enveloppe, fonds) if p["rho"] > 0 else cout_enveloppe
        out.update({
            "enveloppe_cout_moyen_near": float(plafonne.mean()),
            "enveloppe_cout_p99_near": float(np.quantile(plafonne, 0.99)),
            "enveloppe_part_prix_p99": float(np.quantile(plafonne, 0.99) / (ventes_totales * P)),
            "fonds_near": fonds,
            "p_fonds_insuffisant": float((cout_enveloppe > fonds).mean()) if p["rho"] > 0 else None,
        })
    return out


def rho_pour_risque(cfg: dict, morts: dict[str, int], params: dict, risque: float = 0.01, n_sim: int = 20_000) -> float:
    """Part du prix à verser au fonds pour payer les résurrections (pleine valeur) avec une probabilité 1 − risque."""
    r = simuler(cfg, morts, {**params, "enveloppe_near": None}, n_sim, risque=risque)
    return r["cout_quantile_near"] / (r["ventes_totales"] * cfg["prix"])
