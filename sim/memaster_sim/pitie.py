"""Compteur de pitié : un gold pack (table « or ») avec la probabilité p0 + k·n, garanti à n = N − 1.

n = nombre de packs consécutifs ouverts sans gold pack par le compte. Après un gold pack, n repart à 0.
Le compteur est par compte et persiste d'une session à l'autre ; un joueur qui s'arrête laisse son compteur.

Deux parts de gold packs :
- g_∞ (stationnaire) : 1 / durée moyenne d'un cycle, celle d'un joueur qui ouvre une infinité de packs, ou d'un compteur
  revendable (variante nfts) qui finit toujours par être utilisé ;
- g_pop : celle d'une population réelle, où la plupart des joueurs ouvrent peu de packs et repartent avec un compteur bas.
Comme la chance croît avec n, g_pop < g_∞.
"""
from __future__ import annotations

import numpy as np


def proba_gold(n: np.ndarray | int, p0: float, k: float, N: int) -> np.ndarray:
    """Chance que le pack suivant soit en or, après n packs sans gold pack."""
    n = np.asarray(n)
    return np.where(n >= N - 1, 1.0, np.minimum(1.0, p0 + k * n))


def loi_cycle(p0: float, k: float, N: int) -> np.ndarray:
    """P(le gold pack est le (j+1)-ième pack du cycle), j = 0..N−1."""
    h = proba_gold(np.arange(N), p0, k, N)
    survie = np.concatenate([[1.0], np.cumprod(1 - h)[:-1]])
    return survie * h


def duree_moyenne_cycle(p0: float, k: float, N: int) -> float:
    f = loi_cycle(p0, k, N)
    return float((np.arange(1, N + 1) * f).sum())


def g_stationnaire(p0: float, k: float, N: int) -> float:
    return 1.0 / duree_moyenne_cycle(p0, k, N)


def part_garantie(p0: float, k: float, N: int) -> float:
    """Part des cycles qui vont jusqu'à la garantie (le gold pack arrive au N-ième pack)."""
    return float(loi_cycle(p0, k, N)[-1])


def packs_par_joueur(n_joueurs: int, rng: np.random.Generator, mediane: float = 4, sigma: float = 1.4,
                     maximum: int = 5000) -> np.ndarray:
    """Packs ouverts par joueur sur la saison : loi lognormale (beaucoup de petits joueurs, quelques baleines)."""
    x = np.exp(np.log(mediane) + sigma * rng.standard_normal(n_joueurs))
    return np.clip(np.round(x), 1, maximum).astype(np.int64)


def simuler_population(packs: np.ndarray, p0: float, k: float, N: int, rng: np.random.Generator) -> dict:
    """Simule le compteur de chaque joueur pack par pack (vectorisé sur les joueurs)."""
    n = np.zeros(packs.size, dtype=np.int64)
    golds = np.zeros(packs.size, dtype=np.int64)
    garantis = 0
    for t in range(int(packs.max())):
        actifs = packs > t
        h = proba_gold(n[actifs], p0, k, N)
        gold = rng.random(h.size) < h
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
        "part_joueurs_sans_gold": float((golds == 0).mean()),
        "part_gold_garantis": garantis / max(1, int(golds.sum())),
        "compteur_moyen_final": float(n.mean()),
    }


def k_pour_g(g_cible: float, p0: float, N: int, k_max: float = 1.0) -> float:
    """k tel que g_∞ = g_cible (bissection ; g_∞ croît avec k)."""
    lo, hi = 0.0, k_max
    if g_stationnaire(p0, hi, N) < g_cible or g_stationnaire(p0, lo, N) > g_cible:
        raise ValueError("g_cible hors d'atteinte pour ces p0 et N")
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g_stationnaire(p0, mid, N) < g_cible else (lo, mid)
    return (lo + hi) / 2
