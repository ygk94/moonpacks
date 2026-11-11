"""Gold rush : quand les packs vendus dans une fenêtre glissante atteignent un palier, les D blocs suivants sont en or.

Flux d'achats : processus de Poisson non homogène, par pas de temps de `pas_s` secondes :
    λ(t) = λ_base × cycle(t) × pic(t) × (1 + boost si rush en cours)
- cycle(t) = 1 + amplitude·sin(2πt / 1 jour) : creux et heures de pointe ;
- pic(t) : des pics arrivent au hasard (`pics_par_jour`), chacun multiplie le flux par `pic_mult` pendant `pic_duree_s` ;
- boost : les joueurs se ruent sur les packs pendant un rush (jeu de coordination). C'est ce qui peut l'entretenir.
Règle : rush déclenché si la somme des ventes sur `fenetre_s` atteint le palier, et si le dernier rush est fini depuis
`cooldown_s` au moins. Le palier est fixe (`palier`) ou relatif au trafic des dernières 24 h (`palier_relatif`).
Le rush dure `duree_blocs` × `temps_bloc_s`. Un pack vendu pendant un rush est un gold pack.
"""
from __future__ import annotations

import math

import numpy as np

PARAMS_DEFAUT = {
    "jours": 30,
    "pas_s": 30,
    "temps_bloc_s": 0.6,
    "lambda_base_h": 200.0,     # packs par heure, en moyenne hors pics
    "amplitude_cycle": 0.5,
    "pics_par_jour": 0.5,
    "pic_mult": 6.0,
    "pic_duree_s": 1800,
    "boost_rush": 1.0,          # +100 % de demande pendant un rush
    "fenetre_s": 3600,
    "palier": 600,
    "duree_blocs": 3000,        # 30 min à 0,6 s par bloc
    "cooldown_s": 0,
    "palier_relatif": 0.0,      # si > 0 : palier = max(palier, palier_relatif × ventes moyennes par fenêtre sur 24 h)
}


def simuler_flux(params: dict, rng: np.random.Generator) -> dict:
    """Une trajectoire : ventes par pas, état de rush par pas."""
    p = {**PARAMS_DEFAUT, **params}
    dt = p["pas_s"]
    n = int(p["jours"] * 86400 / dt)
    t = np.arange(n) * dt
    base = p["lambda_base_h"] / 3600 * dt * (1 + p["amplitude_cycle"] * np.sin(2 * math.pi * t / 86400))
    pic = np.ones(n)
    n_pics = rng.poisson(p["pics_par_jour"] * p["jours"])
    for debut in rng.uniform(0, n * dt, n_pics):
        i0 = int(debut / dt)
        pic[i0:i0 + int(p["pic_duree_s"] / dt)] *= p["pic_mult"]
    lam = base * pic
    w = max(1, int(round(p["fenetre_s"] / dt)))
    duree = max(1, int(round(p["duree_blocs"] * p["temps_bloc_s"] / dt)))
    cooldown = int(round(p["cooldown_s"] / dt))
    ventes = np.zeros(n, dtype=np.int64)
    rush = np.zeros(n, dtype=bool)
    jour = max(w, int(round(86400 / dt)))
    somme = 0
    somme_jour = 0
    fin_rush = -1          # dernier pas du rush en cours (inclus)
    n_rush = 0
    for i in range(n):
        en_rush = i <= fin_rush
        ventes[i] = rng.poisson(lam[i] * (1 + p["boost_rush"]) if en_rush else lam[i])
        rush[i] = en_rush
        somme += ventes[i]
        somme_jour += ventes[i]
        if i >= w:
            somme -= ventes[i - w]
        if i >= jour:
            somme_jour -= ventes[i - jour]
        palier = p["palier"]
        if p["palier_relatif"] > 0:
            palier = max(palier, p["palier_relatif"] * somme_jour * w / min(i + 1, jour))
        if not en_rush and somme >= palier and i - fin_rush > cooldown:
            fin_rush = i + duree     # les ventes à partir du pas suivant sont en or
            n_rush += 1
    return {"ventes": ventes, "rush": rush, "n_rush": n_rush, "pas_s": dt}


def resumer(flux: dict, jours: float) -> dict:
    v, r = flux["ventes"], flux["rush"]
    total = int(v.sum())
    return {
        "packs": total,
        "packs_par_jour": total / jours,
        "g_rush": float(v[r].sum() / total) if total else 0.0,
        "temps_en_rush": float(r.mean()),
        "rush_par_jour": flux["n_rush"] / jours,
    }


def suite_packs(flux: dict) -> np.ndarray:
    """Drapeau « or » de chaque pack, dans l'ordre des ventes (pour la réserve : les gold packs sont groupés)."""
    return np.repeat(flux["rush"], flux["ventes"])


def simuler(params: dict, n_traj: int, seed: int = 3) -> dict:
    """Moyennes sur n_traj trajectoires, plus les suites de packs pour la réserve."""
    p = {**PARAMS_DEFAUT, **params}
    rng = np.random.default_rng(seed)
    res, suites = [], []
    for _ in range(n_traj):
        f = simuler_flux(p, rng)
        res.append(resumer(f, p["jours"]))
        suites.append(suite_packs(f))
    moy = {k: float(np.mean([x[k] for x in res])) for k in res[0]}
    moy["g_rush_p95"] = float(np.quantile([x["g_rush"] for x in res], 0.95))
    return {"params": p, "moyennes": moy, "suites": suites}
