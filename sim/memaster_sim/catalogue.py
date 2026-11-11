"""Chargeur du catalogue v2 (`docs/data/catalogue-v2.json`) : effectifs par rareté et choix des cartes brûlables.

Le fichier mélange les cartes retenues (`section == "catalogue"`) et des cartes « à décider », ignorées ici.
Les raretés du JSON sont accentuées (« épique », « légendaire ») ; on les ramène aux noms des configs
(`epique`, `legendaire`). Le burn n'est pas décidé (`burn = "à définir"` partout) : le choix des brûlables est
donc simulé, avec une graine fixe, parmi les cartes dont le jeton peut encore être acheté.

Ce module ne touche pas au format des configs : il produit seulement les effectifs et les listes à y recopier.
"""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import numpy as np

RACINE_REPO = Path(__file__).resolve().parents[2]
CHEMIN_CATALOGUE_V2 = RACINE_REPO / "docs" / "data" / "catalogue-v2.json"

# du haut vers le bas de la pyramide
ORDRE_RARETES = ["mythique", "legendaire", "epique", "rare", "commune"]

# part maximale d'une rareté qui peut être brûlable (voir repartir_brulables)
PLAFONDS_PART_BRULABLE = {"mythique": 1.0, "legendaire": 1.0, "epique": 0.5, "rare": 0.25, "commune": 0.1}


def normaliser_rarete(nom: str) -> str:
    sans_accent = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    r = sans_accent.strip().lower()
    if r not in ORDRE_RARETES:
        raise ValueError(f"rareté inconnue : {nom!r}")
    return r


def charger_catalogue_v2(chemin: str | Path = CHEMIN_CATALOGUE_V2) -> list[dict]:
    """Cartes de la section « catalogue », avec la rareté normalisée dans `rarete`."""
    with open(chemin, encoding="utf-8") as f:
        brut = json.load(f)
    cartes = []
    for x in brut:
        if x.get("section") != "catalogue":
            continue
        c = dict(x)
        c["rarete"] = normaliser_rarete(x["rarete"])
        cartes.append(c)
    ids = [c["id"] for c in cartes]
    if len(set(ids)) != len(ids):
        raise ValueError("identifiants en double dans le catalogue")
    return cartes


def effectifs(cartes: list[dict]) -> dict[str, int]:
    """Nombre de cartes par rareté, dans l'ordre de la pyramide (du bas vers le haut, comme les configs)."""
    out = {r: 0 for r in reversed(ORDRE_RARETES)}
    for c in cartes:
        out[c["rarete"]] += 1
    return out


def est_candidate_brulable(carte: dict) -> bool:
    """Une carte peut être brûlable si son jeton s'achète encore : on écarte les jetons morts et les arnaques
    avérées. Les mythiques (scellés, champs masqués « ? ») sont toujours candidats."""
    if carte["rarete"] == "mythique":
        return True
    etat = str(carte.get("etat", "")).lower()
    drapeau = str(carte.get("drapeau", "")).lower()
    return not etat.startswith("mort") and "arnaque" not in drapeau


def candidats(cartes: list[dict]) -> dict[str, list[str]]:
    out = {r: [] for r in reversed(ORDRE_RARETES)}
    for c in cartes:
        if est_candidate_brulable(c):
            out[c["rarete"]].append(c["id"])
    return {r: sorted(v) for r, v in out.items()}


def repartir_brulables(total: int, cartes: list[dict],
                       plafonds: dict[str, float] = PLAFONDS_PART_BRULABLE) -> dict[str, int]:
    """Répartit `total` cartes brûlables en remplissant la pyramide par le haut.

    Chaque rareté reçoit au plus min(candidats, ⌊part max × effectif⌋) brûlables, mythiques d'abord, puis
    légendaires, épiques, rares, communes. Raisons : le plafond d'adossement par carte (la liquidité) croît avec la
    rareté, les communes sont surtout des mèmes morts, et une carte du haut garde une grosse valeur unitaire."""
    eff = effectifs(cartes)
    cand = candidats(cartes)
    reste = total
    out = {r: 0 for r in reversed(ORDRE_RARETES)}
    for r in ORDRE_RARETES:
        cap = min(len(cand[r]), int(plafonds.get(r, 0.0) * eff[r]))
        k = min(cap, reste)
        out[r] = k
        reste -= k
    if reste > 0:
        raise ValueError(f"impossible de placer {total} brûlables : {reste} de trop pour les plafonds")
    return out


def choisir_brulables(cartes: list[dict], repartition: dict[str, int], graine: int = 2026) -> dict[str, list[str]]:
    """Tire, pour chaque rareté, `repartition[r]` cartes parmi les candidates, avec une graine fixe.
    Le tirage est reproductible (candidats triés par identifiant, un générateur par rareté) et emboîté : on mélange
    les candidates une fois, puis on prend les k premières, donc les brûlables d'un petit total sont aussi celles
    d'un total plus grand."""
    cand = candidats(cartes)
    out = {}
    for i, r in enumerate(reversed(ORDRE_RARETES)):
        k = repartition.get(r, 0)
        if k > len(cand[r]):
            raise ValueError(f"{r} : {k} brûlables demandées, {len(cand[r])} candidates")
        rng = np.random.default_rng([graine, i])
        ordre = rng.permutation(len(cand[r]))
        out[r] = sorted(cand[r][j] for j in ordre[:k])
    return out
