"""Modèle économique d'un booster Memaster : configuration, tables de tirage, formules exactes.

Vocabulaire
-----------
- Emplacement (slot) : une des n cartes du booster. Chaque emplacement a sa table de raretés.
- Issue : (rareté, brûlable ou non, niveau de multiplicateur). Un emplacement tire une issue.
- Adossement v d'une carte brûlable : NEAR dépensés à l'ouverture pour acheter ses jetons.
  v = min(κ · w_r · m, plafond_r). Une carte de collection a v = 0.
- Valeur livrée en jetons : v · (1 − s_achat).

Formule de la partie 4.3, généralisée à une part brûlable b_r par rareté et à des emplacements différents :
    κ = β·P / ( E[m] · Σ_emplacements Σ_r p_{s,r} · b_r · w_r )
Avec b_r = (1−d)·q pour toutes les raretés et des emplacements identiques, on retrouve
    κ = β·P / ( n · (1−d) · q · Σ p_r·w_r · E[m] ).
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml


# --------------------------------------------------------------------------- configuration

def charger_config(chemin: str | Path) -> dict:
    with open(chemin, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    valider_config(cfg)
    return cfg


def valider_config(cfg: dict) -> None:
    raretes = cfg["raretes"]
    ordre = cfg["emplacements"]["ordre"]
    if len(ordre) != cfg["n_cartes"]:
        raise ValueError(f"emplacements.ordre a {len(ordre)} entrées, n_cartes = {cfg['n_cartes']}")
    for nom_table, table in cfg["emplacements"]["tables"].items():
        inconnues = set(table) - set(raretes)
        if inconnues:
            raise ValueError(f"table {nom_table} : raretés inconnues {inconnues}")
        total = sum(table.values())
        if abs(total - 1) > 1e-9:
            raise ValueError(f"table {nom_table} : les probabilités font {total}, pas 1")
    for t in ordre:
        if t not in cfg["emplacements"]["tables"]:
            raise ValueError(f"emplacement {t} sans table")
    for nom, r in raretes.items():
        if not 0 <= r["part_brulable"] <= 1:
            raise ValueError(f"{nom} : part_brulable hors de [0, 1]")
    _multiplicateur(cfg, next(iter(raretes)))


def _multiplicateur(cfg: dict, rarete: str) -> tuple[np.ndarray, np.ndarray]:
    m = cfg["raretes"][rarete].get("multiplicateur") or cfg["multiplicateur"]
    valeurs = np.asarray(m["valeurs"], dtype=float)
    probas = np.asarray(m["probas"], dtype=float)
    if valeurs.shape != probas.shape or abs(probas.sum() - 1) > 1e-9:
        raise ValueError(f"multiplicateur de {rarete} invalide")
    return valeurs, probas


def facteur_c(cfg: dict) -> float:
    """c = (1 − s_achat)(1 − f_burn)(1 − s_vente) : part de l'adossement qu'un attaquant récupère en NEAR."""
    k = cfg["couts"]
    return (1 - k["s_achat"]) * (1 - k["f_burn"]) * (1 - k["s_vente"])


# --------------------------------------------------------------------------- tables d'issues

@dataclass
class Tables:
    """Issues possibles et leurs probabilités par type d'emplacement."""
    raretes: list[str]            # noms, dans l'ordre de la config
    issue_rarete: np.ndarray      # indice de rareté de chaque issue
    issue_brulable: np.ndarray    # bool
    issue_m: np.ndarray           # multiplicateur (0 pour une carte de collection)
    issue_poids: np.ndarray       # w_r de l'issue
    issue_plafond: np.ndarray     # plafond de valeur par carte (inf si aucun)
    issue_revente: np.ndarray     # μ_r si carte de collection, 0 sinon
    probas: dict[str, np.ndarray]  # type d'emplacement -> probabilité de chaque issue
    ordre: list[str]              # type de chaque emplacement


def construire_tables(cfg: dict) -> Tables:
    noms = list(cfg["raretes"])
    ir, ib, im, iw, ic, iv = [], [], [], [], [], []
    blocs = []  # (indice rareté, liste des probas relatives d'issues)
    for i, nom in enumerate(noms):
        r = cfg["raretes"][nom]
        b = r["part_brulable"]
        vals, pis = _multiplicateur(cfg, nom)
        plafond = r.get("plafond")
        plafond = math.inf if plafond is None else float(plafond)
        rel = []
        # carte de collection
        ir.append(i); ib.append(False); im.append(0.0); iw.append(r["poids"]); ic.append(plafond)
        iv.append(float(r.get("revente", 0.0))); rel.append(1 - b)
        # cartes brûlables, une issue par niveau de multiplicateur
        for m, pi in zip(vals, pis):
            ir.append(i); ib.append(True); im.append(m); iw.append(r["poids"]); ic.append(plafond)
            iv.append(0.0); rel.append(b * pi)
        blocs.append((i, rel))
    probas = {}
    for nom_table, table in cfg["emplacements"]["tables"].items():
        p = []
        for i, rel in blocs:
            pr = table.get(noms[i], 0.0)
            p.extend(pr * x for x in rel)
        probas[nom_table] = np.asarray(p, dtype=float)
    return Tables(noms, np.asarray(ir), np.asarray(ib), np.asarray(im), np.asarray(iw, float),
                  np.asarray(ic, float), np.asarray(iv, float), probas, list(cfg["emplacements"]["ordre"]))


def proba_issues_booster(t: Tables) -> np.ndarray:
    """Matrice (n emplacements × issues)."""
    return np.vstack([t.probas[s] for s in t.ordre])


# --------------------------------------------------------------------------- κ et valeurs

def kappa_formule(cfg: dict) -> float:
    """κ de la partie 4.3, généralisé, sans plafonds."""
    t = construire_tables(cfg)
    pb = proba_issues_booster(t)
    somme = (pb * t.issue_brulable * t.issue_poids * t.issue_m).sum()
    return cfg["beta"] * cfg["prix"] / somme


def kappa_doc(P: float, n: int, d: float, q: float, somme_pw: float, Em: float, beta: float) -> float:
    """Formule exacte du document (partie 4.3)."""
    return beta * P / (n * (1 - d) * q * somme_pw * Em)


def valeurs_issues(t: Tables, kappa: float) -> np.ndarray:
    v = np.minimum(kappa * t.issue_poids * t.issue_m, t.issue_plafond)
    return np.where(t.issue_brulable, v, 0.0)


def esperance_adossement(t: Tables, kappa: float) -> float:
    return float((proba_issues_booster(t) * valeurs_issues(t, kappa)).sum())


def kappa_calibre(cfg: dict) -> float:
    """κ tel que E[adossement] = β·P en tenant compte des plafonds par carte (bissection).
    Sans plafond actif, c'est exactement kappa_formule."""
    t = construire_tables(cfg)
    cible = cfg["beta"] * cfg["prix"]
    k0 = kappa_formule(cfg)
    if esperance_adossement(t, k0) >= cible * (1 - 1e-12):
        return k0
    lo, hi = k0, k0
    while esperance_adossement(t, hi) < cible:
        hi *= 2
        if hi > k0 * 1e6:
            raise ValueError("plafonds trop bas : impossible d'atteindre β·P d'adossement moyen")
    for _ in range(200):
        mid = (lo + hi) / 2
        if esperance_adossement(t, mid) < cible:
            lo = mid
        else:
            hi = mid
    return hi


def adossement_max(cfg: dict) -> float:
    """Adossement moyen maximal par booster, toutes les cartes brûlables à leur plafond (sans V_cap).
    Au-delà de β = adossement_max / P, le calibrage avec plafonds est impossible."""
    t = construire_tables(cfg)
    pb = proba_issues_booster(t)
    return float((pb * np.where(t.issue_brulable, t.issue_plafond, 0.0)).sum())


def kappa(cfg: dict) -> float:
    return kappa_calibre(cfg) if cfg.get("calibrer_avec_plafonds", True) else kappa_formule(cfg)


# --------------------------------------------------------------------------- grandeurs exactes

def gain_attaquant_issues(cfg: dict, t: Tables, kap: float) -> np.ndarray:
    """Ce que rapporte chaque issue à quelqu'un qui brûle tout et revend le reste (NEAR)."""
    k = cfg["couts"]
    v = valeurs_issues(t, kap)
    burn = np.maximum(v * facteur_c(cfg) - k.get("f_burn_fixe", 0.0), 0.0)
    revente = t.issue_revente * (1 - k["phi"])
    return np.where(t.issue_brulable, burn, revente)


def analytique(cfg: dict) -> dict:
    """Grandeurs calculées exactement (sans V_cap, qui n'a pas de forme fermée simple)."""
    t = construire_tables(cfg)
    pb = proba_issues_booster(t)
    kap = kappa(cfg)
    v = valeurs_issues(t, kap)
    moy_slot = pb @ v
    var_slot = pb @ v**2 - moy_slot**2
    E = float(moy_slot.sum())
    sigma = float(math.sqrt(var_slot.sum()))
    P, k = cfg["prix"], cfg["couts"]
    c = facteur_c(cfg)
    att = gain_attaquant_issues(cfg, t, kap)
    revente_coll = float((pb * np.where(t.issue_brulable, 0.0, t.issue_revente)).sum() * (1 - k["phi"]))
    n_brul = float((pb * t.issue_brulable).sum())
    eps = cfg["epsilon"]
    beta_max = (P * (1 - eps) - revente_coll + n_brul * k.get("f_burn_fixe", 0.0)) / (P * c)

    out = {
        "kappa": kap,
        "kappa_sans_plafond": kappa_formule(cfg),
        "esperance_adossement": E,
        "sigma_booster": sigma,
        "c": c,
        "revente_collection_nette": revente_coll,
        "cartes_brulables_moyennes": n_brul,
        "gain_attaquant_moyen": float((pb @ att).sum()),
        "beta_max_formule": beta_max,
        "p_aucune_brulable": float(np.prod(1 - (pb * t.issue_brulable).sum(1))),
    }
    # au moins une carte de chaque rareté, par booster
    for i, nom in enumerate(t.raretes):
        p_slot = (pb * (t.issue_rarete == i)).sum(1)
        p_slot_b = (pb * ((t.issue_rarete == i) & t.issue_brulable)).sum(1)
        out[f"p_au_moins_un_{nom}"] = float(1 - np.prod(1 - p_slot))
        out[f"p_au_moins_un_{nom}_brulable"] = float(1 - np.prod(1 - p_slot_b))
    # valeur de base par rareté (m = 1, sans plafond) et bornes réelles
    out["valeur_par_rarete"] = {}
    for i, nom in enumerate(t.raretes):
        sel = (t.issue_rarete == i) & t.issue_brulable & (pb.sum(0) > 0)
        if sel.any():
            plafond = cfg["raretes"][nom].get("plafond")
            base = kap * cfg["raretes"][nom]["poids"]
            out["valeur_par_rarete"][nom] = {
                "base": base if plafond is None else min(base, float(plafond)),
                "min": float(v[sel].min()), "max": float(v[sel].max()),
            }
    # réserve, approximation normale du document
    delta = cfg["delta"] * P
    z = cfg["ruine"].get("z", 3)
    out["r0_normale"] = cfg["v_cap"] + (z * sigma) ** 2 / (4 * delta)
    out["proba_ruine_brownien_equivalente"] = math.exp(-z**2 / 2)
    return out


def frequences_par_carte(cfg: dict, n_boosters: int = 10_000) -> dict:
    """Nombre moyen d'exemplaires de chaque carte sur n_boosters, et facteur de faveur des brûlables.
    On suppose un tirage uniforme dans chaque groupe (brûlables / collection) d'une rareté."""
    t = construire_tables(cfg)
    pb = proba_issues_booster(t)
    out = {}
    for i, nom in enumerate(t.raretes):
        r = cfg["raretes"][nom]
        p_r = float((pb * (t.issue_rarete == i)).sum())
        nb = r.get("brulables", 0)
        nc = r.get("effectif", 0) - nb
        b = r["part_brulable"]
        par_brul = n_boosters * p_r * b / nb if nb else None
        par_coll = n_boosters * p_r * (1 - b) / nc if nc > 0 else None
        out[nom] = {
            "cartes_par_booster": p_r,
            "exemplaires_par_brulable": par_brul,
            "exemplaires_par_collection": par_coll,
            "faveur_brulable": (par_brul / par_coll) if (par_brul and par_coll) else None,
        }
    return out


# --------------------------------------------------------------------------- variantes de config

def avec(cfg: dict, **chemins) -> dict:
    """Copie de cfg avec des clés modifiées : avec(cfg, beta=0.7, **{"raretes.legendaire.poids": 50})."""
    c = copy.deepcopy(cfg)
    for chemin, val in chemins.items():
        cles = chemin.split(".")
        d = c
        for k in cles[:-1]:
            d = d[k]
        d[cles[-1]] = val
    return c


def changer_cote_mythique(cfg: dict, proba_booster: float, rarete: str = "mythique",
                          compensation: str = "commune") -> dict:
    """Règle la probabilité d'avoir au moins une carte `rarete` par booster. La probabilité est mise à
    l'échelle sur tous les emplacements qui en ont déjà, prise ou rendue à `compensation`."""
    c = copy.deepcopy(cfg)
    tables = c["emplacements"]["tables"]
    ordre = c["emplacements"]["ordre"]
    actuel = 1 - np.prod([1 - tables[s].get(rarete, 0.0) for s in ordre])
    if actuel <= 0:
        raise ValueError(f"aucun emplacement n'a de {rarete}")
    lo, hi = 0.0, 1.0 / max(tables[s].get(rarete, 0.0) for s in ordre)
    base = {s: tables[s].get(rarete, 0.0) for s in tables}
    for _ in range(200):
        mid = (lo + hi) / 2
        p = 1 - np.prod([1 - base[s] * mid for s in ordre])
        lo, hi = (mid, hi) if p < proba_booster else (lo, mid)
    f = (lo + hi) / 2
    for s, table in tables.items():
        if base[s] > 0:
            nouveau = base[s] * f
            table[compensation] -= nouveau - base[s]
            table[rarete] = nouveau
            if table[compensation] < 0:
                raise ValueError("compensation négative")
    return c


def scaler_poids(cfg: dict, rarete: str, facteur: float) -> dict:
    return avec(cfg, **{f"raretes.{rarete}.poids": cfg["raretes"][rarete]["poids"] * facteur})
