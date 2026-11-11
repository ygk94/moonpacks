"""Monte-Carlo vectorisé : tirages de boosters, statistiques, borne anti-arbitrage, simulation de ruine."""
from __future__ import annotations

import math

import numpy as np

from . import modele as M

PERCENTILES = [1, 5, 10, 25, 50, 75, 90, 95, 99, 99.9, 99.99]
TAILLE_LOT = 1_000_000  # boosters par lot, pour borner la mémoire


def tirer_issues(t: M.Tables, n_boosters: int, rng: np.random.Generator) -> np.ndarray:
    """Matrice (n_boosters × n emplacements) d'indices d'issues, tirés par inversion de la fonction de répartition."""
    out = np.empty((n_boosters, len(t.ordre)), dtype=np.uint16)
    cdfs = {s: np.cumsum(p) for s, p in t.probas.items()}
    for j, s in enumerate(t.ordre):
        cdf = cdfs[s]
        cdf[-1] = 1.0 + 1e-12  # garde contre l'arrondi
        u = rng.random(n_boosters)
        out[:, j] = np.searchsorted(cdf, u, side="right")
    return out


def valeurs_boosters(cfg: dict, t: M.Tables, issues: np.ndarray, kap: float | None = None,
                     plafonner: bool = True) -> np.ndarray:
    kap = M.kappa(cfg) if kap is None else kap
    v = M.valeurs_issues(t, kap)[issues].sum(1)
    return np.minimum(v, cfg["v_cap"]) if plafonner else v


def statistiques(cfg: dict, n_boosters: int = 1_000_000, seed: int = 1, avec_beta_max: bool = True) -> dict:
    """Statistiques par booster sur n_boosters tirages."""
    rng = np.random.default_rng(seed)
    t = M.construire_tables(cfg)
    kap = M.kappa(cfg)
    issues = tirer_issues(t, n_boosters, rng)
    val_issue = M.valeurs_issues(t, kap)
    brut = val_issue[issues].sum(1)
    V = np.minimum(brut, cfg["v_cap"])
    P = cfg["prix"]
    att_issue = M.gain_attaquant_issues(cfg, t, kap)
    A_brut = att_issue[issues].sum(1)
    # avec V_cap : l'adossement est réduit au prorata, la revente de collection ne change pas
    burn_part = (val_issue[issues] * M.facteur_c(cfg)).sum(1)
    reduction = np.where(brut > 0, V / np.where(brut > 0, brut, 1), 1.0)
    A = A_brut - burn_part * (1 - reduction)

    revente = (t.issue_revente[issues]).sum(1)
    rarete = t.issue_rarete[issues]
    brul = t.issue_brulable[issues]
    out = {
        "n_boosters": n_boosters,
        "kappa": kap,
        "esperance_adossement": float(V.mean()),
        "esperance_adossement_sans_vcap": float(brut.mean()),
        "erreur_type": float(V.std() / math.sqrt(n_boosters)),
        "sigma_booster": float(V.std()),
        "percentiles": {str(q): float(x) for q, x in zip(PERCENTILES, np.percentile(V, PERCENTILES))},
        "max": float(V.max()),
        "p_vcap_actif": float((brut > cfg["v_cap"]).mean()),
        "p_adossement_ge_prix": float((V >= P).mean()),
        "p_adossement_plus_revente_ge_prix": float((V + revente >= P).mean()),
        "p_aucune_brulable": float((~brul.any(1)).mean()),
        "cartes_brulables_moyennes": float(brul.sum(1).mean()),
        "gain_attaquant_moyen": float(A.mean()),
    }
    for i, nom in enumerate(t.raretes):
        out[f"p_au_moins_un_{nom}"] = float((rarete == i).any(1).mean())
        out[f"p_au_moins_un_{nom}_brulable"] = float(((rarete == i) & brul).any(1).mean())
    # part des cartes brûlables sous la valeur minimale utile (coût fixe du retrait)
    vmin = cfg.get("v_min_brulable")
    if vmin:
        vb = val_issue[issues][brul]
        out["part_brulables_sous_vmin"] = float((vb < vmin).mean()) if vb.size else 0.0
    if avec_beta_max:
        out["beta_max_simule"] = beta_max_simule(cfg, t, issues)
    return out


def beta_max_simule(cfg: dict, t: M.Tables, issues: np.ndarray) -> float:
    """β tel que le gain moyen simulé de l'attaquant vaille P·(1−ε), avec plafonds et V_cap (bissection)."""
    cible = cfg["prix"] * (1 - cfg["epsilon"])

    def gain(beta: float) -> float:
        c = M.avec(cfg, beta=beta)
        kap = M.kappa(c)
        val = M.valeurs_issues(t, kap)[issues]
        brut = val.sum(1)
        V = np.minimum(brut, c["v_cap"])
        red = np.where(brut > 0, V / np.where(brut > 0, brut, 1), 1.0)
        att = M.gain_attaquant_issues(c, t, kap)[issues].sum(1)
        burn = (val * M.facteur_c(c)).sum(1)
        return float((att - burn * (1 - red)).mean())

    lo, hi = 0.0, 1.5
    if cfg.get("calibrer_avec_plafonds", True):
        # au-delà, les plafonds par carte rendent le calibrage impossible
        hi = min(hi, 0.999999 * M.adossement_max(cfg) / cfg["prix"])
    if gain(hi) < cible:
        return math.inf
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gain(mid) < cible else (lo, mid)
    return (lo + hi) / 2


# --------------------------------------------------------------------------- ruine

def pertes_max(cfg: dict, n_trajectoires: int, horizon: int, seed: int = 2) -> np.ndarray:
    """Pour chaque trajectoire de `horizon` ventes, la plus forte baisse de la réserve depuis R₀ :
    D = max(0, max_t Σ_{i≤t} (V_i − (β+δ)·P)). La réserve passe sous V_cap ssi R₀ − V_cap < D."""
    rng = np.random.default_rng(seed)
    t = M.construire_tables(cfg)
    kap = M.kappa(cfg)
    val_issue = M.valeurs_issues(t, kap)
    apport = (cfg["beta"] + cfg["delta"]) * cfg["prix"]
    par_lot = max(1, TAILLE_LOT // horizon)
    D = np.empty(n_trajectoires)
    fait = 0
    while fait < n_trajectoires:
        k = min(par_lot, n_trajectoires - fait)
        iss = tirer_issues(t, k * horizon, rng)
        V = np.minimum(val_issue[iss].sum(1), cfg["v_cap"]).reshape(k, horizon)
        S = np.cumsum(V - apport, axis=1)
        D[fait:fait + k] = np.maximum(S.max(1), 0.0)
        fait += k
    return D


def ruine(cfg: dict, n_trajectoires: int | None = None, horizon: int | None = None,
          seed: int = 2, grille_r0: list[float] | None = None) -> dict:
    r = cfg["ruine"]
    n_trajectoires = n_trajectoires or r.get("trajectoires", 4000)
    horizon = horizon or r.get("horizon", 10_000)
    D = pertes_max(cfg, n_trajectoires, horizon, seed)
    vcap = cfg["v_cap"]
    an = M.analytique(cfg)
    if grille_r0 is None:
        hauts = np.quantile(D, [0.5, 0.9, 0.99, 0.999]) + vcap
        grille_r0 = sorted({round(x, -1) for x in [vcap, *hauts, an["r0_normale"]]})

    def p_ruine(r0: float) -> float:
        return float((D > r0 - vcap).mean())

    out = {
        "trajectoires": n_trajectoires,
        "horizon": horizon,
        "apport_par_booster": (cfg["beta"] + cfg["delta"]) * cfg["prix"],
        "r0_normale": an["r0_normale"],
        "z": r.get("z", 3),
        "p_ruine_a_r0_normale": p_ruine(an["r0_normale"]),
        "p_ruine_brownien_equivalente": an["proba_ruine_brownien_equivalente"],
        "courbe": [(float(r0), p_ruine(r0)) for r0 in grille_r0],
    }
    for risque in (0.05, 0.01, 0.001):
        if n_trajectoires * risque >= 5:
            out[f"r0_risque_{risque}"] = float(vcap + np.quantile(D, 1 - risque))
    return out
