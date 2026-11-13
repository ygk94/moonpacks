"""Régénère les exemples versionnés de art/exemples/.

    python3 -m memaster_art.exemples --catalogue ../docs/catalogue-final.md --dest exemples/ [--png]
    python3 -m memaster_art.exemples --catalogue ../docs/data/catalogue-v2.json --dest exemples/v2 --png

Avec le JSON v2 : 2 cartes par rareté (une vivante et une morte quand il y en a) et le dos
mythique scellé, plus une planche `planche-v2.svg` (et `planche-v2.png` avec --png).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

from .catalogue import lire_catalogue
from .catalogue_v2 import lire_catalogue_v2
from .cli import generer, sceller
from .planche import planche_svg

# Cartes v1 qui couvrent chaque rareté et chaque état : légendaire, épique actif et en déclin,
# rare actif et en déclin, communes mortes, commune en déclin, commune à vérifier avec un ticker
# en idéogrammes. Les mythiques ne sont désignées que par le fichier secret (hors git) : elles
# s'ajoutent en tête, scellées, quand il est présent.
CHOIX = [4, 10, 8, 78, 51, 804, 805, 190, 801]
SECRETS = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "data", "secrets", "mythiques.json")


def numeros_mythiques_v1(chemin: str = SECRETS) -> list[int]:
    """N° v1 des mythiques (`origines` « v1 n° X » du fichier secret), [] sans le fichier."""
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)
    nums = []
    for e in data.get("mythiques", []) if isinstance(data, dict) else data:
        for o in e.get("origines", []):
            m = re.match(r"^v1 n° ?(\d+)$", o.strip())
            if m:
                nums.append(int(m.group(1)))
    return nums


def selection(chemin: str, secrets: str = SECRETS):
    cartes = {c.numero: c for c in lire_catalogue(chemin)}
    choisies = [sceller(cartes[n]) for n in numeros_mythiques_v1(secrets)[:2] if n in cartes]
    choisies += [cartes[n] for n in CHOIX if n in cartes]
    return choisies  # 9 cartes, plus 2 mythiques scellées et le dos commun avec le fichier secret


# Les exemples évitent les noms qui renvoient à une mascotte animale ou à une personne réelle.
_EVITER = re.compile(r"dog|shib|inu|pepe|frog|cat|meow|wolf|monkey|pox|pig|official|trump", re.I)


def selection_v2(chemin: str):
    """2 cartes par rareté visible (la 1re vivante et la 1re morte, sinon les 2 premières),
    plus la 1re mythique (scellée : seul le dos sera produit)."""
    cartes = [c for c in lire_catalogue_v2(chemin) if c.scellee or not _EVITER.search(c.ticker + " " + c.nom)]
    choisies = []
    for r in ("commune", "rare", "épique", "légendaire"):
        de_r = [c for c in cartes if c.rarete == r]
        vivante = next((c for c in de_r if c.etat != "mort"), None)
        morte = next((c for c in de_r if c.etat == "mort"), None)
        duo = [c for c in (vivante, morte) if c is not None]
        duo += [c for c in de_r if c not in duo][: 2 - len(duo)]
        choisies += duo
    choisies += [c for c in cartes if c.scellee][:1]
    return choisies


def _rendre_png(fichiers, dest):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
    from rendre_png import rendre  # type: ignore

    return [rendre(f, dest) if not f.endswith("planche-v2.svg") else rendre(f, dest, largeur=1640) for f in fichiers]


def main_v2(a) -> int:
    cartes = selection_v2(a.catalogue)
    generer(cartes, a.dest)
    vignettes = []
    for c in cartes:
        if c.scellee:
            continue
        with open(os.path.join(a.dest, c.nom_fichier + ".svg"), encoding="utf-8") as f:
            vignettes.append((f.read(), f"{c.rarete} · {c.etat} · {c.ticker}"))
    if any(c.scellee for c in cartes):
        with open(os.path.join(a.dest, "dos-mythique.svg"), encoding="utf-8") as f:
            vignettes.append((f.read(), "mythique · dos scellé"))
    planche = os.path.join(a.dest, "planche-v2.svg")
    with open(planche, "w", encoding="utf-8") as f:
        f.write(planche_svg(vignettes, "Memaster · catalogue v2 · exemples"))
    if a.png:
        svgs = sorted(os.path.join(a.dest, n) for n in os.listdir(a.dest) if n.endswith(".svg"))
        _rendre_png(svgs, a.dest)
    for c in cartes:
        print(c.numero, c.cle, c.rarete, c.etat)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--png", action="store_true", help="rendre aussi les PNG (outils/rendre_png.py)")
    a = ap.parse_args(argv)
    if a.catalogue.lower().endswith(".json"):
        return main_v2(a)
    cartes = selection(a.catalogue)
    generer(cartes, a.dest, planche=True)
    if a.png:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
        from rendre_png import rendre  # type: ignore

        for f in sorted(os.listdir(a.dest)):
            if f.endswith(".svg"):
                rendre(os.path.join(a.dest, f), a.dest)
    for c in cartes:
        print(c.numero, c.ticker, c.rarete, c.etat)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
