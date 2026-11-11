"""Régénère les exemples versionnés de art/exemples/.

    python3 -m memaster_art.exemples --catalogue ../docs/catalogue-final.md --dest exemples/ [--png]
    python3 -m memaster_art.exemples --catalogue ../docs/data/catalogue-v2.json --dest exemples/v2 --png

Avec le JSON v2 : 2 cartes par rareté (une vivante et une morte quand il y en a) et le dos
mythique scellé, plus une planche `planche-v2.svg` (et `planche-v2.png` avec --png).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import replace

from .catalogue import lire_catalogue
from .catalogue_v2 import lire_catalogue_v2
from .cli import generer
from .planche import planche_svg

# Mythiques (règle v2) : N° 1 et 3 du catalogue. Les autres couvrent chaque rareté et
# chaque état : légendaire, épique actif et en déclin, rare actif et en déclin, communes
# mortes, commune en déclin, commune à vérifier avec un ticker en idéogrammes.
MYTHIQUES = {1, 3}
CHOIX = [1, 3, 4, 10, 8, 78, 51, 804, 805, 190, 801]


def selection(chemin: str):
    cartes = {c.numero: c for c in lire_catalogue(chemin)}
    choisies = []
    for num in CHOIX:
        c = cartes.get(num)
        if c is None:
            continue
        choisies.append(replace(c, rarete="mythique") if num in MYTHIQUES else c)
    return choisies  # 11 cartes + le dos scellé = 12 visuels


# Les exemples évitent les noms qui renvoient à une mascotte animale ou à un mythique.
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
