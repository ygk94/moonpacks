"""Table « or » et mélange standard / or (pitié, gold rush).

Une carte vaut la même chose quel que soit le pack qui la sort : κ est commun aux deux tables. Le gold pack change
seulement les probabilités de rareté. Si une part g des packs est en or, l'adossement moyen est linéaire en g :
    E[V] = (1 − g)·E_std(κ) + g·E_or(κ)
donc on calibre κ sur la table mélangée p = (1 − g)·p_std + g·p_or, avec plafonds, pour tenir β·P en moyenne.
"""
from __future__ import annotations

import copy

import numpy as np

from . import modele as M
from . import simulation as S

# facteurs appliqués aux probabilités de chaque rareté, dans chaque emplacement ; la commune compense
FACTEURS_OR_DEFAUT = {"rare": 2.0, "epique": 3.0, "legendaire": 4.0, "mythique": 4.0}


def table_or(cfg: dict, facteurs: dict[str, float] = FACTEURS_OR_DEFAUT, compensation: str = "commune") -> dict:
    """Copie de cfg dont les tables d'emplacement ont des poids de rareté renforcés."""
    c = copy.deepcopy(cfg)
    for nom, table in c["emplacements"]["tables"].items():
        for r, f in facteurs.items():
            if r in table:
                table[r] = table[r] * f
        autres = sum(v for r, v in table.items() if r != compensation)
        if autres > 1:
            raise ValueError(f"table or {nom} : la {compensation} deviendrait négative ({1 - autres:.4f})")
        table[compensation] = 1 - autres
    c["nom"] = cfg["nom"] + " (table or)"
    M.valider_config(c)
    return c


def melanger(cfg_std: dict, cfg_or: dict, g: float) -> dict:
    """Config dont les tables valent (1 − g)·std + g·or : même espérance que le flux réel de packs."""
    c = copy.deepcopy(cfg_std)
    for nom, table in c["emplacements"]["tables"].items():
        t_or = cfg_or["emplacements"]["tables"][nom]
        for r in table:
            table[r] = (1 - g) * table[r] + g * t_or[r]
    return c


def melanger_n(cfg_std: dict, autres: list[tuple[dict, float]]) -> dict:
    """Mélange de la table standard avec plusieurs tables (or de pitié, table du rush...), parts g_i."""
    c = copy.deepcopy(cfg_std)
    reste = 1 - sum(g for _, g in autres)
    if reste < 0:
        raise ValueError("parts de packs spéciaux > 1")
    for nom, table in c["emplacements"]["tables"].items():
        for r in table:
            table[r] = reste * cfg_std["emplacements"]["tables"][nom][r] + \
                sum(g * x["emplacements"]["tables"][nom][r] for x, g in autres)
    return c


def calibrer(cfg_std: dict, cfg_or: dict, g: float) -> dict:
    """κ commun tel que l'adossement moyen vaille β·P avec une part g de gold packs."""
    kap = M.kappa(melanger(cfg_std, cfg_or, g))
    t_s, t_o = M.construire_tables(cfg_std), M.construire_tables(cfg_or)
    e_s, e_o = M.esperance_adossement(t_s, kap), M.esperance_adossement(t_o, kap)
    P = cfg_std["prix"]
    pb_s, pb_o = M.proba_issues_booster(t_s), M.proba_issues_booster(t_o)
    return {
        "g": g, "kappa": kap, "kappa_sans_or": M.kappa(cfg_std),
        "esperance_std": e_s, "esperance_or": e_o,
        "couverture_std": e_s / P, "couverture_or": e_o / P,
        "couverture_moyenne": ((1 - g) * e_s + g * e_o) / P,
        "part_budget_or": g * e_o / ((1 - g) * e_s + g * e_o),
        "p_brulable_std": 1 - float(np.prod(1 - (pb_s * t_s.issue_brulable).sum(1))),
        "p_brulable_or": 1 - float(np.prod(1 - (pb_o * t_o.issue_brulable).sum(1))),
        "gain_attaquant_or": float((pb_o @ M.gain_attaquant_issues(cfg_or, t_o, kap)).sum()),
    }


def couverture_a_kappa(cfg_std: dict, cfg_or: dict, g: float, kap: float) -> float:
    """Couverture moyenne réalisée quand κ a été fixé pour une autre part de gold packs."""
    e_s = M.esperance_adossement(M.construire_tables(cfg_std), kap)
    e_o = M.esperance_adossement(M.construire_tables(cfg_or), kap)
    return ((1 - g) * e_s + g * e_o) / cfg_std["prix"]


def valeurs_packs_n(cfgs: list[dict], kap: float, idx: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Adossement (plafonné à V_cap de cfgs[0]) de chaque pack ; idx[i] = table du pack i (0 = standard)."""
    out = np.empty(idx.size)
    for j, cfg in enumerate(cfgs):
        masque = idx == j
        k = int(masque.sum())
        if k == 0:
            continue
        t = M.construire_tables(cfg)
        v = M.valeurs_issues(t, kap)
        out[masque] = np.minimum(v[S.tirer_issues(t, k, rng)].sum(1), cfgs[0]["v_cap"])
    return out


def pertes_max_n(cfg_std: dict, autres: list[tuple[dict, float]], kap: float, apports: list[float],
                 n_trajectoires: int, horizon: int, seed: int = 2, lot: int = 1_000_000,
                 drapeaux=None) -> np.ndarray:
    """Plus forte baisse de la réserve, pour plusieurs apports par vente avec les mêmes tirages.
    Chaque vente prend la table i ≥ 1 avec la probabilité g_i (indépendamment), ou suit `drapeaux(rng, k, horizon)`,
    qui rend une matrice (k × horizon) d'indices de table (pour des gold packs groupés, comme un rush).
    Rend une matrice (len(apports) × n_trajectoires)."""
    rng = np.random.default_rng(seed)
    cfgs = [cfg_std] + [c for c, _ in autres]
    cum = np.cumsum([g for _, g in autres])
    par_lot = max(1, lot // horizon)
    D = np.empty((len(apports), n_trajectoires))
    fait = 0
    while fait < n_trajectoires:
        k = min(par_lot, n_trajectoires - fait)
        if drapeaux is not None:
            idx = np.asarray(drapeaux(rng, k, horizon)).reshape(-1)
        elif autres:
            # u < cum[0] → table 1, ..., cum[-2] ≤ u < cum[-1] → table L, u ≥ cum[-1] → table 0 (standard)
            j = np.searchsorted(cum, rng.random(k * horizon), side="right")
            idx = np.where(j < len(autres), j + 1, 0)
        else:
            idx = np.zeros(k * horizon, dtype=int)
        V = valeurs_packs_n(cfgs, kap, idx, rng).reshape(k, horizon)
        for a, apport in enumerate(apports):
            D[a, fait:fait + k] = np.maximum(np.cumsum(V - apport, axis=1).max(1), 0.0)
        fait += k
    return D


def reserves(D: np.ndarray, v_cap: float, risques=(0.05, 0.01)) -> dict:
    return {f"r0_risque_{r}": float(v_cap + np.quantile(D, 1 - r)) for r in risques if D.size * r >= 5}
