"""Série 4 : valeur aléatoire en jetons par pack, gold pack redéfini.

Schéma (décision du porteur, 11/11/2026)
----------------------------------------
- Chaque pack tire une valeur V dans une **table discrète publiée et hachée** de paliers `(bps du prix, poids)`.
  La couverture d'un type de pack est donc exactement la moyenne de sa table : elle ne dépend plus des raretés tirées.
- V est réparti entre les cartes brûlables du pack au prorata d'un multiplicateur par rareté :
  `valeur(carte i) = V · m_{r(i)} / Σ_{j brûlable} m_{r(j)}`.
- Chaque pack a au moins une brûlable : le 5ᵉ emplacement est tiré parmi les brûlables. Sa rareté suit la table
  normale de l'emplacement ; si la rareté tirée n'a aucune brûlable, on retombe vers le bas (puis, s'il n'y a rien
  en dessous, vers le haut).
- Gold pack (pitié, garanti au 20ᵉ pack) : aucune commune. Emplacements 1 et 2 rare ou mieux, 3 et 4 épique ou mieux
  (raretés tirées dans la table standard restreinte), emplacement 5 légendaire (80 %) ou mythique (20 %), brûlable.
  Il a sa propre table de valeur.
- Pack rush : tables de raretés du rush (série 3), sa propre table de valeur, couverture ≤ 80 %.

Une table est une `TableValeur` : paliers en points de base du prix (10 000 = le prix), poids entiers.
Les mythiques sont dans V par défaut ; `cout_mythique_hors_v` chiffre l'autre lecture (jackpot fixe en plus de V).
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass

import numpy as np

# du bas vers le haut de la pyramide, comme les configs
RARETES = ["commune", "rare", "epique", "legendaire", "mythique"]
NOMS_CONTRAT = {"commune": "common", "rare": "rare", "epique": "epic", "legendaire": "legendary", "mythique": "mythic"}
BPS = 10_000


# =========================================================================== tables de valeur

@dataclass(frozen=True)
class TableValeur:
    """Table discrète : V = paliers[i] / 10 000 × prix avec la probabilité poids[i] / Σ poids."""
    paliers: tuple[int, ...]
    poids: tuple[int, ...]

    def __post_init__(self):
        if len(self.paliers) != len(self.poids) or not self.paliers:
            raise ValueError("paliers et poids de tailles différentes, ou vides")
        if any(not isinstance(x, (int, np.integer)) for x in self.paliers + self.poids):
            raise ValueError("paliers et poids doivent être des entiers")
        if any(b <= a for a, b in zip(self.paliers, self.paliers[1:])):
            raise ValueError("paliers non strictement croissants")
        if self.paliers[0] < 0 or any(w <= 0 for w in self.poids):
            raise ValueError("palier négatif ou poids nul")

    # --- grandeurs exactes
    @property
    def total(self) -> int:
        return int(sum(self.poids))

    @property
    def valeurs(self) -> np.ndarray:
        """Valeurs en multiples du prix."""
        return np.asarray(self.paliers, dtype=float) / BPS

    @property
    def probas(self) -> np.ndarray:
        return np.asarray(self.poids, dtype=float) / self.total

    def moyenne(self) -> float:
        return float(sum(p * w for p, w in zip(self.paliers, self.poids)) / self.total / BPS)

    def ecart_type(self) -> float:
        return float(math.sqrt(max(0.0, (self.probas * self.valeurs**2).sum() - self.moyenne()**2)))

    def quantile(self, q: float) -> float:
        """Plus petit palier x tel que P(V ≤ x) ≥ q (quantile inférieur, comme une médiane de table discrète)."""
        cum = np.cumsum(self.poids)
        i = int(np.searchsorted(cum, q * self.total - 1e-9, side="left"))
        return self.paliers[min(i, len(self.paliers) - 1)] / BPS

    def mediane(self) -> float:
        return self.quantile(0.5)

    def part_sous(self, x: float) -> float:
        """P(V < x), x en multiples du prix."""
        return float(self.probas[self.valeurs < x - 1e-12].sum())

    def part_au_dessus(self, x: float) -> float:
        """P(V > x)."""
        return float(self.probas[self.valeurs > x + 1e-12].sum())

    def minimum(self) -> float:
        return self.paliers[0] / BPS

    def maximum(self) -> float:
        return self.paliers[-1] / BPS

    def resume(self) -> dict:
        return {
            "min": self.minimum(), "max": self.maximum(), "moyenne": self.moyenne(), "ecart_type": self.ecart_type(),
            "q10": self.quantile(0.10), "q50": self.mediane(), "q90": self.quantile(0.90),
            "sous_50": self.part_sous(0.5), "au_dessus_100": self.part_au_dessus(1.0),
            "paliers": len(self.paliers), "total_poids": self.total,
        }

    # --- format publié
    def en_json(self) -> list[list[int]]:
        return [[int(p), int(w)] for p, w in zip(self.paliers, self.poids)]

    def empreinte(self) -> str:
        """sha256 du JSON compact `[[bps,poids],…]` (informative : le contrat hache la table de série entière)."""
        return hashlib.sha256(json.dumps(self.en_json(), separators=(",", ":")).encode()).hexdigest()

    @classmethod
    def depuis_json(cls, paires: list[list[int]]) -> "TableValeur":
        return cls(tuple(int(p) for p, _ in paires), tuple(int(w) for _, w in paires))


def melange(tables: list[tuple[TableValeur, float]]) -> tuple[np.ndarray, np.ndarray]:
    """Loi exacte d'un mélange de tables (parts sommant à 1) : (valeurs triées, probabilités)."""
    vals: dict[int, float] = {}
    for t, g in tables:
        for p, pr in zip(t.paliers, t.probas):
            vals[p] = vals.get(p, 0.0) + g * pr
    cles = sorted(vals)
    return np.asarray(cles, float) / BPS, np.asarray([vals[c] for c in cles])


def resume_loi(valeurs: np.ndarray, probas: np.ndarray) -> dict:
    cum = np.cumsum(probas)

    def q(x):
        return float(valeurs[min(int(np.searchsorted(cum, x - 1e-12)), len(valeurs) - 1)])
    m = float((valeurs * probas).sum())
    return {"min": float(valeurs[probas > 0].min()), "max": float(valeurs[probas > 0].max()), "moyenne": m,
            "ecart_type": float(math.sqrt(max(0.0, (valeurs**2 * probas).sum() - m * m))),
            "q10": q(0.10), "q50": q(0.50), "q90": q(0.90),
            "sous_50": float(probas[valeurs < 0.5 - 1e-12].sum()), "au_dessus_100": float(probas[valeurs > 1 + 1e-12].sum())}


# --------------------------------------------------------------------------- calibrage

def _phi(x: np.ndarray) -> np.ndarray:
    return 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))


def masses_lognormales(paliers_bps: list[int], mu: float, sigma: float) -> np.ndarray:
    """Masse de chaque palier : loi lognormale (μ, σ sur ln V) discrétisée au milieu (en log) de deux paliers.
    Les queues au-delà du premier et du dernier palier vont aux paliers extrêmes (V est borné)."""
    l = np.log(np.asarray(paliers_bps, float) / BPS)
    bornes = (l[:-1] + l[1:]) / 2
    cdf = np.concatenate([[0.0], _phi((bornes - mu) / sigma), [1.0]])
    return np.diff(cdf)


def arrondir_poids(masses: np.ndarray, total: int) -> tuple[int, ...]:
    """Poids entiers sommant à `total` (plus forts restes), au moins 1 par palier."""
    brut = masses / masses.sum() * total
    w = np.floor(brut).astype(np.int64)
    reste = total - int(w.sum())
    for i in np.argsort(-(brut - w))[:reste]:
        w[i] += 1
    while (w < 1).any():
        i, j = int(np.argmin(w)), int(np.argmax(w))
        w[i] += 1
        w[j] -= 1
    return tuple(int(x) for x in w)


def ajuster_moyenne(table: TableValeur, cible: float) -> TableValeur:
    """Déplace quelques unités de poids entre paliers voisins pour que Σ bps·poids soit le plus proche possible de
    cible·10 000·total (effet de l'arrondi des poids ; change la moyenne de moins de 0,01 point)."""
    w = list(table.poids)
    p = table.paliers
    objectif = round(cible * BPS * table.total)
    for _ in range(10_000):
        ecart = objectif - sum(a * b for a, b in zip(p, w))
        if ecart == 0:
            break
        # meilleur déplacement d'une unité du palier i vers i ± 1
        meilleur = None
        for i in range(len(p)):
            for j in (i - 1, i + 1):
                if 0 <= j < len(p) and w[i] > 1:
                    d = p[j] - p[i]
                    if abs(ecart - d) < abs(ecart) and (meilleur is None or abs(ecart - d) < meilleur[0]):
                        meilleur = (abs(ecart - d), i, j)
        if meilleur is None:
            break
        _, i, j = meilleur
        w[i] -= 1
        w[j] += 1
    return TableValeur(p, tuple(w))


def table_lognormale(paliers_bps: list[int], cible: float, sur: str = "moyenne", sigma: float = 0.6,
                     total: int = 1_000_000) -> TableValeur:
    """Table aux paliers donnés, de forme lognormale (σ), calibrée pour que sa moyenne (`sur="moyenne"`) ou sa
    médiane (`sur="mediane"`) vaille `cible` (en multiples du prix)."""
    if sur not in ("moyenne", "mediane"):
        raise ValueError(sur)
    if not paliers_bps[0] / BPS < cible < paliers_bps[-1] / BPS:
        raise ValueError("cible hors des paliers")
    if sur == "mediane":
        if round(cible * BPS) not in paliers_bps:
            raise ValueError("la médiane visée doit être un palier")
        t = TableValeur(tuple(paliers_bps), arrondir_poids(masses_lognormales(paliers_bps, math.log(cible), sigma), total))
        if abs(t.mediane() - cible) > 1e-9:
            raise ValueError(f"médiane {t.mediane()} au lieu de {cible}")
        return t
    v = np.asarray(paliers_bps, float) / BPS
    lo, hi = math.log(v[0]) - 3 * sigma, math.log(v[-1]) + 3 * sigma
    for _ in range(200):
        mu = (lo + hi) / 2
        m = masses_lognormales(paliers_bps, mu, sigma)
        lo, hi = (mu, hi) if (m * v).sum() < cible else (lo, mu)
    t = TableValeur(tuple(paliers_bps), arrondir_poids(masses_lognormales(paliers_bps, (lo + hi) / 2, sigma), total))
    return ajuster_moyenne(t, cible)


def paliers(*segments: tuple[int, int, int]) -> list[int]:
    """paliers((2000, 10000, 500), (11000, 20000, 1000)) : bornes incluses, sans doublon."""
    out: list[int] = []
    for a, b, pas in segments:
        out += [x for x in range(a, b + 1, pas) if not out or x > out[-1]]
    return out


# =========================================================================== composition des packs

@dataclass
class TypePack:
    """Un type de pack : loi de rareté de chaque emplacement, emplacements forcés brûlables, table de valeur."""
    nom: str
    emplacements: list[dict[str, float]]   # une loi de rareté par emplacement
    force_brulable: list[bool]
    table: TableValeur


def retombee(loi: dict[str, float], brulables: dict[str, int]) -> dict[str, float]:
    """Loi de rareté d'un emplacement tiré parmi les brûlables : la masse d'une rareté sans brûlable va à la première
    rareté inférieure qui en a, sinon à la première supérieure."""
    out = {r: 0.0 for r in RARETES}
    for r, p in loi.items():
        if p <= 0:
            continue
        i = RARETES.index(r)
        cible = next((RARETES[j] for j in range(i, -1, -1) if brulables.get(RARETES[j], 0) > 0), None)
        if cible is None:
            cible = next((RARETES[j] for j in range(i + 1, len(RARETES)) if brulables.get(RARETES[j], 0) > 0), None)
        if cible is None:
            raise ValueError("aucune rareté n'a de brûlable")
        out[cible] += p
    return out


def restreindre(loi: dict[str, float], minimum: str) -> dict[str, float]:
    """Loi conditionnée à « `minimum` ou mieux »."""
    i0 = RARETES.index(minimum)
    sel = {r: p for r, p in loi.items() if RARETES.index(r) >= i0 and p > 0}
    s = sum(sel.values())
    if s <= 0:
        raise ValueError(f"aucune masse au-dessus de {minimum}")
    return {r: sel.get(r, 0.0) / s for r in RARETES}


def _complete(loi: dict[str, float]) -> dict[str, float]:
    return {r: float(loi.get(r, 0.0)) for r in RARETES}


def pack_normal(cfg: dict, table: TableValeur, tables_rarete: dict | None = None, nom: str = "normal") -> TypePack:
    """Emplacements de la config (4 standard + favorable) ; le dernier est tiré parmi les brûlables."""
    tr = tables_rarete or cfg["emplacements"]["tables"]
    ordre = cfg["emplacements"]["ordre"]
    brul = {r: cfg["raretes"][r].get("brulables", 0) for r in RARETES}
    emp = [_complete(tr[s]) for s in ordre]
    emp[-1] = retombee(emp[-1], brul)
    return TypePack(nom, emp, [False] * (len(ordre) - 1) + [True], table)


def pack_gold(cfg: dict, table: TableValeur, minimums=("rare", "rare", "epique", "epique"),
              dernier: dict[str, float] | None = None, brulable: int | None = None) -> TypePack:
    """Gold pack redéfini : aucune commune ; emplacements 1-4 « rareté minimale ou mieux » dans la table standard ;
    emplacement 5 légendaire 80 % / mythique 20 %. `brulable` = indice de l'emplacement tiré parmi les brûlables
    (défaut, série 4 : le dernier ; série 5 : le 2ᵉ, comme le contrat, car une mythique n'est jamais brûlable)."""
    std = cfg["emplacements"]["tables"][cfg["emplacements"]["ordre"][0]]
    dernier = dernier or {"legendaire": 0.8, "mythique": 0.2}
    brul = {r: cfg["raretes"][r].get("brulables", 0) for r in RARETES}
    emp = [restreindre(_complete(std), m) for m in minimums] + [_complete(dernier)]
    b = len(emp) - 1 if brulable is None else brulable
    emp[b] = retombee(emp[b], brul)
    return TypePack("gold", emp, [i == b for i in range(len(emp))], table)


def proba_brulable(cfg: dict) -> np.ndarray:
    return np.asarray([cfg["raretes"][r]["part_brulable"] for r in RARETES])


def multiplicateurs_vec(mult: dict[str, float]) -> np.ndarray:
    return np.asarray([float(mult[r]) for r in RARETES])


def tirer_packs(tp: TypePack, cfg: dict, mult: dict[str, float], n: int, rng: np.random.Generator) -> dict:
    """n packs : rareté (n × k), brûlable (n × k), V (n), valeur de chaque carte en multiples du prix (n × k)."""
    k = len(tp.emplacements)
    rar = np.empty((n, k), dtype=np.int8)
    for j, loi in enumerate(tp.emplacements):
        cdf = np.cumsum([loi[r] for r in RARETES])
        cdf[-1] = 1.0 + 1e-12
        rar[:, j] = np.searchsorted(cdf, rng.random(n), side="right")
    b = proba_brulable(cfg)
    brul = rng.random((n, k)) < b[rar]
    brul[:, np.asarray(tp.force_brulable)] = True
    cdf_v = np.cumsum(tp.table.probas)
    cdf_v[-1] = 1.0 + 1e-12
    V = tp.table.valeurs[np.searchsorted(cdf_v, rng.random(n), side="right")]
    m = multiplicateurs_vec(mult)[rar] * brul
    part = m / m.sum(1, keepdims=True)
    return {"rarete": rar, "brulable": brul, "V": V, "valeur_carte": part * V[:, None]}


def stats_composition(tp: TypePack, cfg: dict, mult: dict[str, float], n: int, rng: np.random.Generator,
                      seuil_x_prix: float | None = None) -> dict:
    """Brûlables par pack, part de V par rareté, valeur d'une carte brûlable par rareté (multiples du prix)."""
    d = tirer_packs(tp, cfg, mult, n, rng)
    rar, brul, vc = d["rarete"], d["brulable"], d["valeur_carte"]
    nb = brul.sum(1)
    out = {"brulables_moyennes": float(nb.mean()),
           "brulables_loi": {str(i): float((nb == i).mean()) for i in range(1, rar.shape[1] + 1)},
           "cartes_par_pack": {r: float((rar == i).sum(1).mean()) for i, r in enumerate(RARETES)},
           "par_rarete": {}}
    tot = vc.sum()
    for i, r in enumerate(RARETES):
        sel = brul & (rar == i)
        if not sel.any():
            continue
        x = vc[sel]
        e = {"brulables_par_pack": float(sel.sum() / n), "part_de_V": float(x.sum() / tot),
             "moyenne": float(x.mean()), "min": float(x.min()), "max": float(x.max()),
             "q10": float(np.quantile(x, 0.1)), "q50": float(np.quantile(x, 0.5)), "q90": float(np.quantile(x, 0.9))}
        if seuil_x_prix is not None:
            e["sous_seuil"] = float((x < seuil_x_prix).mean())
        out["par_rarete"][r] = e
    x = vc[brul]
    out["carte_min"] = float(x.min())
    if seuil_x_prix is not None:
        out["cartes_sous_seuil"] = float((x < seuil_x_prix).mean())
    return out


def esperance_raretes(tp: TypePack) -> dict[str, float]:
    """Nombre moyen de cartes de chaque rareté par pack (exact)."""
    return {r: float(sum(loi[r] for loi in tp.emplacements)) for r in RARETES}


def revente_collection(tp: TypePack, cfg: dict) -> float:
    """Revente moyenne (nette de φ) des cartes de collection d'un pack, en NEAR."""
    phi = cfg["couts"]["phi"]
    s = 0.0
    for loi, force in zip(tp.emplacements, tp.force_brulable):
        if force:
            continue
        for r in RARETES:
            s += loi[r] * (1 - cfg["raretes"][r]["part_brulable"]) * cfg["raretes"][r].get("revente", 0.0)
    return s * (1 - phi)


# =========================================================================== mélange, mythique, réserve

def parts_types(g: float, r: float) -> dict[str, float]:
    """Gold de pitié g ; un pack non gold est rush avec la probabilité r (la pitié l'emporte sur le rush)."""
    return {"normal": (1 - g) * (1 - r), "gold": g, "rush": (1 - g) * r}


def couverture_globale(tables: dict[str, TableValeur], parts: dict[str, float]) -> float:
    return float(sum(parts[k] * tables[k].moyenne() for k in parts if parts[k] > 0))


def cout_mythique_hors_v(types: dict[str, TypePack], parts: dict[str, float], valeur_x_prix: float) -> dict:
    """Si un mythique valait un jackpot fixe (valeur_x_prix × prix) en plus de V : coût moyen par pack, par type."""
    p = {k: esperance_raretes(tp)["mythique"] for k, tp in types.items()}
    par_type = {k: p[k] * valeur_x_prix for k in types}
    return {"mythiques_par_pack": p, "cout_par_pack_du_type": par_type,
            "cout_moyen": float(sum(parts[k] * par_type[k] for k in parts)),
            "mythiques_par_pack_moyen": float(sum(parts[k] * p[k] for k in parts))}


def loi_paiement(tables: dict[str, TableValeur], parts: dict[str, float], jackpot: dict | None = None
                 ) -> tuple[np.ndarray, np.ndarray]:
    """Loi du paiement d'un pack (multiples du prix), packs indépendants. `jackpot` = {"valeur": M,
    "p": {type: proba d'un mythique}} ajoute M avec cette probabilité (mythique hors V)."""
    vals, prs = [], []
    for k, g in parts.items():
        if g <= 0:
            continue
        t = tables[k]
        pj = (jackpot or {}).get("p", {}).get(k, 0.0)
        for v, pr in zip(t.valeurs, t.probas):
            vals.append(v); prs.append(g * pr * (1 - pj))
            if pj > 0:
                vals.append(v + jackpot["valeur"]); prs.append(g * pr * pj)
    return np.asarray(vals), np.asarray(prs)


def pertes_max(valeurs: np.ndarray, probas: np.ndarray, apport: float, horizon: int, trajectoires: int,
               seed: int = 41, lot: int = 10_000_000) -> np.ndarray:
    """Plus forte baisse de la réserve (multiples du prix) : elle reçoit `apport` par vente et paie le pack."""
    rng = np.random.default_rng(seed)
    cdf = np.cumsum(probas / probas.sum())
    cdf[-1] = 1.0 + 1e-12
    x = (valeurs - apport).astype(np.float64)
    par_lot = max(1, lot // horizon)
    D = np.empty(trajectoires)
    fait = 0
    while fait < trajectoires:
        k = min(par_lot, trajectoires - fait)
        idx = np.searchsorted(cdf, rng.random((k, horizon)), side="right")
        D[fait:fait + k] = np.maximum(np.cumsum(x[idx], axis=1).max(1), 0.0)
        fait += k
    return D


def reserve_ruine(valeurs: np.ndarray, probas: np.ndarray, apport: float, horizon: int, trajectoires: int,
                  risques=(0.05, 0.01), seed: int = 41) -> dict:
    """R₀ = plus gros paiement possible + quantile de la plus forte baisse : la réserve peut toujours payer le pack
    suivant, sauf avec la probabilité `risque` sur l'horizon."""
    D = pertes_max(valeurs, probas, apport, horizon, trajectoires, seed)
    vmax = float(valeurs[probas > 0].max())
    return {"trajectoires": trajectoires, "horizon": horizon, "v_max": vmax, "baisse_moyenne": float(D.mean()),
            **{f"r0_{r}": vmax + float(np.quantile(D, 1 - r)) for r in risques}}


def cycle_pitie(tables: dict[str, TableValeur], g_inf: float) -> float:
    """Couverture d'un cycle complet de pitié (joueur qui ouvre jusqu'au gold pack, sans rush) : g = g_∞."""
    return (1 - g_inf) * tables["normal"].moyenne() + g_inf * tables["gold"].moyenne()


def epuisement(par_pack: float, stock: float) -> float:
    """Packs vendus avant d'épuiser un stock de cartes (par_pack exemplaires en moyenne par pack)."""
    return math.inf if par_pack <= 0 else stock / par_pack


def export_json(tables: dict[str, TableValeur], mult: dict[str, float], gold: dict, meta: dict) -> dict:
    """Format publié des tables (voir la clé `_format`)."""
    return {
        "_format": (
            "Tables de valeur V par pack (série 4, sim/memaster_sim/valeur.py). value_tables.<type>.tiers = liste de "
            "[bps, poids] : V = prix du pack × bps / 10 000, tiré avec la probabilité poids / weight_total ; bps "
            "strictement croissants, poids entiers > 0, Σ poids = weight_total. <type> = base (pack normal), gold "
            "(gold pack de pitié), rush (pack rush). split_multipliers = multiplicateur entier par rareté : la carte "
            "brûlable i du pack reçoit V × m_i / Σ m_j (j brûlables du pack), arrondi vers le bas, le reste à la carte "
            "du dernier emplacement. Tout pack a au moins une brûlable : le dernier emplacement est tiré parmi les "
            "brûlables (rareté de la table de l'emplacement, retombée vers le bas, puis vers le haut s'il n'y a rien en "
            "dessous). gold_pack décrit le gold pack : rareté minimale des emplacements 1 à 4 (table standard restreinte "
            "à cette rareté et au-dessus), poids du dernier emplacement (ppm). mean_bps / median_bps / sha256 sont "
            "informatifs (sha256 du JSON compact des tiers) : le contrat hache la table de série entière."),
        "format_version": 1,
        "unit": "bps_of_pack_price",
        "weight_total": next(iter(tables.values())).total,
        **meta,
        "value_tables": {k: {"tiers": t.en_json(), "mean_bps": round(t.moyenne() * BPS, 2),
                             "median_bps": round(t.mediane() * BPS), "min_bps": t.paliers[0],
                             "max_bps": t.paliers[-1], "sha256": t.empreinte()} for k, t in tables.items()},
        "split_multipliers": {NOMS_CONTRAT[r]: int(mult[r]) for r in RARETES},
        "gold_pack": gold,
    }
