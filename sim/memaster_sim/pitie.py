"""Compteur de pitié : un gold pack (table « or ») avec la probabilité min(p_max, p0 + k·n), garanti à n = N − 1.

n = nombre de packs consécutifs ouverts sans gold pack par le compte. Après un gold pack, n repart à 0 (un pack rush
compte comme un pack sans gold : n + 1). Le compteur est par compte et persiste d'une session à l'autre ; un joueur
qui s'arrête laisse son compteur.

Deux régimes :
- séries 3 et 4 : garantie à N (`N` entier, `p_max` = 1 par défaut) ;
- série 5 : aucune garantie (`N = None`), chance plafonnée à `p_max` (atteint en (p_max − p0)/k packs), puis constante.
  La durée d'un cycle a alors une queue géométrique exacte : au-delà du plafond m, P(T > m + j) = S(m)·(1 − p_max)^j.

Deux parts de gold packs :
- g_∞ (stationnaire) : 1 / durée moyenne d'un cycle, celle d'un joueur qui ouvre une infinité de packs, ou d'un compteur
  revendable (variante nfts) qui finit toujours par être utilisé ;
- g_pop : celle d'une population réelle, où la plupart des joueurs ouvrent peu de packs et repartent avec un compteur bas.
Comme la chance croît avec n, g_pop < g_∞.
"""
from __future__ import annotations

import math

import numpy as np


def proba_gold(n: np.ndarray | int, p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> np.ndarray:
    """Chance que le pack suivant soit en or, après n packs sans gold pack (N = None : pas de garantie)."""
    n = np.asarray(n)
    h = np.minimum(min(1.0, p_max), p0 + k * n)
    if N is None:
        return h
    return np.where(n >= N - 1, 1.0, h)


def debut_plafond(p0: float, k: float, p_max: float = 1.0) -> tuple[int, float]:
    """Sans garantie : (m, h*) avec h(n) = h* pour tout n ≥ m (premier n où le plafond est atteint)."""
    h_max = min(1.0, p_max)
    if k <= 0:
        m = 0
    else:
        m = max(0, math.ceil((h_max - p0) / k))
        while float(proba_gold(m, p0, k, None, p_max)) < h_max:   # arrondi flottant
            m += 1
    h = float(proba_gold(m, p0, k, None, p_max))
    if h <= 0:
        raise ValueError("chance de gold nulle : le cycle ne finit jamais")
    return m, h


def survie(p0: float, k: float, N: int | None, p_max: float, n: int) -> np.ndarray:
    """S(j) = P(aucun gold dans les j premiers packs du cycle), j = 0..n."""
    h = proba_gold(np.arange(n), p0, k, N, p_max)
    return np.concatenate([[1.0], np.cumprod(1 - h)])


def loi_cycle(p0: float, k: float, N: int | None = None, p_max: float = 1.0, n_max: int | None = None) -> np.ndarray:
    """P(le gold pack est le (j+1)-ième pack du cycle), j = 0..N−1. Sans garantie (N = None), loi tronquée à
    j < n_max (par défaut : jusqu'au plafond inclus) : elle ne somme pas à 1, le reste est la queue géométrique."""
    if N is None:
        n = n_max if n_max is not None else debut_plafond(p0, k, p_max)[0] + 1
    else:
        n = N
    h = proba_gold(np.arange(n), p0, k, N, p_max)
    return survie(p0, k, N, p_max, n)[:-1] * h


def duree_moyenne_cycle(p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> float:
    """E[T] = Σ_j S(j). Avec garantie : somme finie sur N packs. Sans garantie : somme jusqu'au plafond m, plus la
    queue géométrique exacte S(m) / h*."""
    if N is not None:
        f = loi_cycle(p0, k, N, p_max)
        return float((np.arange(1, N + 1) * f).sum())
    m, h = debut_plafond(p0, k, p_max)
    S = survie(p0, k, None, p_max, m)
    return float(S[:-1].sum() + S[-1] / h)


def g_stationnaire(p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> float:
    return 1.0 / duree_moyenne_cycle(p0, k, N, p_max)


def part_garantie(p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> float:
    """Part des cycles qui vont jusqu'à la garantie (le gold pack arrive au N-ième pack) ; 0 sans garantie."""
    if N is None:
        return 0.0
    return float(loi_cycle(p0, k, N, p_max)[-1])


def golds_attendus(t_max: int, p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> np.ndarray:
    """E[nombre de gold packs dans les t premiers packs d'un compte neuf], t = 0..t_max (équation de renouvellement :
    a_t = f_t + Σ_{s<t} a_s f_{t−1−s}, a_t = P(le pack t est en or), f = loi du cycle)."""
    h = proba_gold(np.arange(t_max), p0, k, N, p_max)
    f = np.concatenate([[1.0], np.cumprod(1 - h)[:-1]]) * h
    a = np.zeros(t_max)
    for t in range(t_max):
        a[t] = f[t] + (a[:t] @ f[t - 1::-1] if t else 0.0)
    return np.concatenate([[0.0], np.cumsum(a)])


def g_pop_exact(packs: np.ndarray, p0: float, k: float, N: int | None = None, p_max: float = 1.0) -> float:
    """Part attendue de gold packs d'une population (packs[i] packs par joueur, compteurs neufs), sans tirage."""
    e = golds_attendus(int(packs.max()), p0, k, N, p_max)
    return float(e[packs].sum() / packs.sum())


def packs_par_joueur(n_joueurs: int, rng: np.random.Generator, mediane: float = 4, sigma: float = 1.4,
                     maximum: int = 5000) -> np.ndarray:
    """Packs ouverts par joueur sur la saison : loi lognormale (beaucoup de petits joueurs, quelques baleines)."""
    x = np.exp(np.log(mediane) + sigma * rng.standard_normal(n_joueurs))
    return np.clip(np.round(x), 1, maximum).astype(np.int64)


def simuler_population(packs: np.ndarray, p0: float, k: float, N: int | None, rng: np.random.Generator,
                       p_max: float = 1.0) -> dict:
    """Simule le compteur de chaque joueur pack par pack (vectorisé sur les joueurs)."""
    n = np.zeros(packs.size, dtype=np.int64)
    golds = np.zeros(packs.size, dtype=np.int64)
    garantis = 0
    for t in range(int(packs.max())):
        actifs = packs > t
        h = proba_gold(n[actifs], p0, k, N, p_max)
        gold = rng.random(h.size) < h
        if N is not None:
            garantis += int((gold & (n[actifs] >= N - 1)).sum())
        idx = np.flatnonzero(actifs)
        golds[idx[gold]] += 1
        n[idx] = np.where(gold, 0, n[idx] + 1)
    total = int(packs.sum())
    ordre = np.sort(packs)[::-1]
    top = max(1, packs.size // 20)
    return {
        "joueurs": int(packs.size), "packs": total, "packs_moyens": total / packs.size,
        "packs_medians": float(np.median(packs)),
        "part_packs_top5": float(ordre[:top].sum() / total),
        "g_pop": float(golds.sum() / total),
        "golds": int(golds.sum()),
        "part_joueurs_sans_gold": float((golds == 0).mean()),
        "part_gold_garantis": garantis / max(1, int(golds.sum())),
        "compteur_moyen_final": float(n.mean()),
    }


def mc_cycles(n_cycles: int, p0: float, k: float, p_max: float, rng: np.random.Generator,
              lot: int = 20_000) -> np.ndarray:
    """Sans garantie : durées de n_cycles cycles, tirées pack par pack (Bernoulli) jusqu'au plafond m, puis, pour les
    cycles encore ouverts, m + loi géométrique de paramètre h* (hasard constant). Contrôle de g_∞."""
    m, h_star = debut_plafond(p0, k, p_max)
    h = proba_gold(np.arange(m), p0, k, None, p_max)
    out = np.empty(n_cycles, dtype=np.int64)
    fait = 0
    while fait < n_cycles:
        c = min(lot, n_cycles - fait)
        T = np.full(c, -1, dtype=np.int64)
        for j in range(m):
            ouverts = np.flatnonzero(T < 0)
            g = rng.random(ouverts.size) < h[j]
            T[ouverts[g]] = j + 1
        reste = T < 0
        T[reste] = m + rng.geometric(h_star, int(reste.sum()))
        out[fait:fait + c] = T
        fait += c
    return out


def mc_flux_stationnaire(joueurs: int, packs: int, p0: float, k: float, p_max: float, rng: np.random.Generator
                         ) -> dict:
    """Sans garantie : `joueurs` comptes ouvrant chacun `packs` packs, compteurs initiaux tirés dans la loi
    stationnaire de l'âge du cycle (π(n) ∝ S(n)) : la part de gold mesurée estime g_∞ sans biais de démarrage."""
    m, h_star = debut_plafond(p0, k, p_max)
    S = survie(p0, k, None, p_max, m)
    masse_avant = S[:-1].sum()
    total = masse_avant + S[-1] / h_star
    avant = rng.random(joueurs) < masse_avant / total
    cdf = np.cumsum(S[:-1]) / masse_avant
    n = np.where(avant, np.searchsorted(cdf, rng.random(joueurs)),
                 m + rng.geometric(h_star, joueurs) - 1).astype(np.int64)
    golds = 0
    for _ in range(packs):
        gold = rng.random(joueurs) < proba_gold(n, p0, k, None, p_max)
        golds += int(gold.sum())
        n = np.where(gold, 0, n + 1)
    return {"joueurs": joueurs, "packs_par_joueur": packs, "packs": joueurs * packs, "golds": golds,
            "g": golds / (joueurs * packs)}


def k_pour_g(g_cible: float, p0: float, N: int | None, k_max: float = 1.0, p_max: float = 1.0) -> float:
    """k tel que g_∞ = g_cible (bissection ; g_∞ croît avec k)."""
    lo, hi = 0.0, k_max
    if g_stationnaire(p0, hi, N, p_max) < g_cible or g_stationnaire(p0, lo, N, p_max) > g_cible:
        raise ValueError("g_cible hors d'atteinte pour ces p0 et N")
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g_stationnaire(p0, mid, N, p_max) < g_cible else (lo, mid)
    return (lo + hi) / 2
