"""Rareté pilotée par les burns : poids de tirage effectif d'une carte = poids × en_circulation / émises.

Le poids ici est celui du tirage de la carte dans sa rareté (sa fréquence), pas son adossement. Les cartes de
collection ne brûlent pas : leur rapport reste 1. La probabilité de chaque rareté ne change pas : la part perdue par
une carte très brûlée revient aux autres cartes de la même rareté (`renormaliser = "rarete"`, lecture directe de la
formule), ou aux seules autres brûlables de la rareté (`"brulables"`, variante à budget constant).

Burn : chaque exemplaire brûlable émis est destiné au burn avec la probabilité `taux_burn`, puis brûlé après un délai
géométrique de moyenne `delai_packs` (en packs vendus). `plancher` borne le rapport par le bas : sans plancher, un coin
entièrement brûlé n'est plus jamais tiré.

Deux réglages de κ :
- `fixe` : les cartes gardent leur valeur ; moins de brûlables sortent, la couverture réelle baisse sous β ;
- `recalibre` : κ est recalculé à chaque lot pour tenir β ; chaque brûlable vaut plus, la variance d'un pack monte.
"""
from __future__ import annotations

import numpy as np

from . import modele as M

PARAMS_DEFAUT = {"taux_burn": 0.5, "delai_packs": 5000, "plancher": 0.0, "horizon": 100_000, "lot": 500,
                 "kappa": "fixe",
                 "renormaliser": "rarete", "prior_k": 0}
# Règle du contrat (`draw::raw_burn_weight`, `in_rarity_weight`) : a priori K = 20, part des brûlables
# constante dans la rareté. Les résultats publiés (série 3) utilisent PARAMS_DEFAUT (K = 0, « rarete »).
PARAMS_CONTRAT = {"renormaliser": "brulables", "prior_k": 20, "plancher": 0.25}


def _structure(cfg: dict) -> dict:
    t = M.construire_tables(cfg)
    pb = M.proba_issues_booster(t)
    out = {}
    for i, nom in enumerate(t.raretes):
        r = cfg["raretes"][nom]
        nb = int(r.get("brulables", 0))
        if nb == 0:
            continue
        sel = (t.issue_rarete == i) & t.issue_brulable
        p_r = float((pb * (t.issue_rarete == i)).sum())          # cartes de cette rareté par pack
        # loi du multiplicateur conditionnelle à « brûlable de rareté r »
        poids_m = (pb[:, sel]).sum(0)
        out[nom] = {"cartes_par_pack": p_r, "effectif": int(r["effectif"]), "brulables": nb,
                    "m": t.issue_m[sel], "pi_m": poids_m / poids_m.sum(), "w": float(r["poids"]),
                    "plafond": float(t.issue_plafond[sel][0])}
    return out


def _valeurs(struct: dict, kap: float) -> dict[str, tuple[float, float]]:
    """E[v] et E[v²] d'un exemplaire brûlable de chaque rareté."""
    out = {}
    for nom, s in struct.items():
        v = np.minimum(kap * s["w"] * s["m"], s["plafond"])
        out[nom] = (float((s["pi_m"] * v).sum()), float((s["pi_m"] * v * v).sum()))
    return out


def _part_brulable(s: dict, ratio: np.ndarray, renormaliser: str) -> np.ndarray:
    """Probabilité, pour une carte de la rareté, d'être chacun des brûlables.
    - "rarete" : la part perdue revient à toutes les cartes de la rareté (collection comprise) ;
    - "brulables" : elle revient aux seules autres brûlables de la rareté (le nombre de brûlables par pack ne bouge pas) ;
    - "aucune" : elle est perdue pour la rareté (la carte tirée à la place est une commune de collection, en pratique)."""
    n_coll = s["effectif"] - s["brulables"]
    if renormaliser == "aucune":
        return ratio / s["effectif"]
    if ratio.sum() <= 0:  # tous les coins de la rareté éteints
        return np.full(ratio.size, 1 / ratio.size) * (s["brulables"] / s["effectif"] if n_coll else 1.0)
    if renormaliser == "brulables":
        return ratio / ratio.sum() * s["brulables"] / s["effectif"]
    if renormaliser == "rarete":
        return ratio / (n_coll + ratio.sum())
    raise ValueError(f"renormaliser inconnu : {renormaliser}")


def ratios_burn(e: np.ndarray, b: np.ndarray, prior_k: float = 0.0, plancher: float = 0.0) -> np.ndarray:
    """Rapport du poids d'une brûlable à son poids de base : `(e − b + K) / (e + K)` (1 si rien n'est
    émis), borné par `plancher` (le contrat borne le poids par `⌊w × floor_bps / 10⁴⌋`, même rapport)."""
    r = np.where(e > 0, (e - b + prior_k) / np.where(e > 0, e + prior_k, 1), 1.0)
    return np.maximum(r, plancher)


def simuler(cfg: dict, params: dict | None = None, seed: int = 5) -> dict:
    p = {**PARAMS_DEFAUT, **(params or {})}
    renormaliser = p["renormaliser"]
    rng = np.random.default_rng(seed)
    struct = _structure(cfg)
    P, beta = cfg["prix"], cfg["beta"]
    kap0 = M.kappa(cfg)
    emis = {n: np.zeros(s["brulables"]) for n, s in struct.items()}
    brules = {n: np.zeros(s["brulables"]) for n, s in struct.items()}
    en_attente = {n: np.zeros(s["brulables"]) for n, s in struct.items()}
    h = 1 - np.exp(-p["lot"] / p["delai_packs"])
    lot = p["lot"]

    def ratios(n):
        return ratios_burn(emis[n], brules[n], p["prior_k"], p["plancher"])

    def couverture(kap, parts):
        vals = _valeurs(struct, kap)
        return sum(struct[n]["cartes_par_pack"] * parts[n].sum() * vals[n][0] for n in struct) / P

    def couverture_sans_burn(kap):
        return couverture(kap, {n: _part_brulable(s, np.ones(s["brulables"]), renormaliser) for n, s in struct.items()})

    # couverture « hors mythique » du modèle sans burn = β (κ de la config)
    base = couverture_sans_burn(kap0)
    kap = kap0
    histo = []
    paye = 0.0
    for etape in range(int(p["horizon"] // lot)):
        parts = {n: _part_brulable(s, ratios(n), renormaliser) for n, s in struct.items()}
        if p["kappa"] == "recalibre":
            lo, hi = kap0 * 0.1, kap0 * 1000
            for _ in range(60):
                mid = (lo * hi) ** 0.5
                lo, hi = (mid, hi) if couverture(mid, parts) < base else (lo, mid)
            kap = hi
        vals = _valeurs(struct, kap)
        cov = couverture(kap, parts)
        var = sum(struct[n]["cartes_par_pack"] * parts[n].sum() * vals[n][1] for n in struct)
        engage = 0.0
        brul_par_pack = 0.0
        for n, s in struct.items():
            lam = lot * s["cartes_par_pack"] * parts[n]
            k = rng.poisson(lam).astype(float)
            emis[n] += k
            en_attente[n] += rng.binomial(k.astype(np.int64), p["taux_burn"])
            b = rng.binomial(en_attente[n].astype(np.int64), h).astype(float)
            en_attente[n] -= b
            brules[n] += b
            paye += float(k.sum()) * vals[n][0]
            engage += float((emis[n] - brules[n]).sum()) * vals[n][0]
            brul_par_pack += s["cartes_par_pack"] * parts[n].sum()
        tous = np.concatenate([ratios(n) for n in struct])
        histo.append({"packs": (etape + 1) * lot, "couverture": cov * beta / base, "kappa_rel": kap / kap0,
                      "sigma": float(np.sqrt(var)), "brulables_par_pack": brul_par_pack,
                      "engagements_near": engage, "ratio_min": float(tous.min()),
                      "ratio_median": float(np.median(tous)),
                      "coins_au_plancher": int((tous <= p["plancher"] + 1e-12).sum())})
    total = histo[-1]["packs"]
    sigma0 = float(np.sqrt(sum(struct[n]["cartes_par_pack"] * _part_brulable(s, np.ones(s["brulables"]), renormaliser).sum()
                               * _valeurs(struct, kap0)[n][1] for n, s in struct.items())))
    return {
        "params": p, "histo": histo, "couverture_finale": histo[-1]["couverture"],
        "couverture_moyenne": paye / (total * P) * beta / base,
        "sigma_initial": sigma0, "sigma_final": histo[-1]["sigma"],
        "kappa_final_rel": histo[-1]["kappa_rel"], "engagements_finaux_near": histo[-1]["engagements_near"],
        "brulables_par_pack_initial": sum(s["cartes_par_pack"] * s["brulables"] / s["effectif"] for s in struct.values()),
        "brulables_par_pack_final": histo[-1]["brulables_par_pack"],
        "ratio_min_final": histo[-1]["ratio_min"], "coins_au_plancher": histo[-1]["coins_au_plancher"],
    }
