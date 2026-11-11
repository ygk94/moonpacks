"""CLI : python3 -m memaster_art --catalogue docs/catalogue-final.md --out art/out/"""

from __future__ import annotations

import argparse
import json
import os

from .catalogue import lire_catalogue
from .catalogue_v2 import lire_catalogue_v2
from .metadonnees import en_octets, metadonnees_carte, metadonnees_dos
from .planche import planches
from .rendu import rendre_carte, rendre_dos


def _ecrire(chemin: str, donnees: bytes) -> None:
    with open(chemin, "wb") as f:
        f.write(donnees)


def generer(cartes, out: str, base_url: str = "", planche: bool = False) -> dict:
    os.makedirs(out, exist_ok=True)
    entrees = []
    stats = {"cartes": 0, "octets_max": 0, "mythiques": 0, "scellees": 0}
    dos = None
    if any(c.rarete == "mythique" for c in cartes):
        dos = rendre_dos().encode("utf-8")
        _ecrire(os.path.join(out, "dos-mythique.svg"), dos)
        _ecrire(os.path.join(out, "dos-mythique.json"), en_octets(metadonnees_dos(dos, base_url)))
        entrees.append(("dos-mythique.svg", "dos scellé · mythique"))
    for c in cartes:
        if c.scellee:
            # Mythique scellée : le public ne voit que le dos commun, pas de recto ni de référence.
            meta = metadonnees_dos(dos, base_url, carte=c)
            _ecrire(os.path.join(out, c.nom_fichier + ".json"), en_octets(meta))
            stats["cartes"] += 1
            stats["mythiques"] += 1
            stats["scellees"] += 1
            continue
        svg = rendre_carte(c).encode("utf-8")
        meta, ref = metadonnees_carte(c, svg, base_url)
        base = os.path.join(out, c.nom_fichier)
        _ecrire(base + ".svg", svg)
        _ecrire(base + ".json", en_octets(meta))
        _ecrire(base + ".ref.json", ref)
        entrees.append((c.nom_fichier + ".svg", f"{c.numero} · {c.ticker} · {c.rarete} · {c.etat}"))
        stats["cartes"] += 1
        stats["mythiques"] += c.rarete == "mythique"
        stats["octets_max"] = max(stats["octets_max"], len(svg))
    if planche:
        for nom, html in planches(entrees):
            _ecrire(os.path.join(out, nom), html.encode("utf-8"))
            stats.setdefault("planches", []).append(nom)
    return stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_art", description="Génère les visuels SVG et les métadonnées NEP-177.")
    ap.add_argument("--catalogue", required=True,
                    help="catalogue markdown (tableau « Cartes ») ou JSON v2 (docs/data/catalogue-v2.json)")
    ap.add_argument("--inclure-a-decider", action="store_true",
                    help="JSON v2 : ajouter la section « à décider » (par défaut : section « catalogue » seule)")
    ap.add_argument("--out", required=True, help="dossier de sortie (ex. art/out/)")
    ap.add_argument("--limit", type=int, default=None, help="ne générer que les N premières cartes")
    ap.add_argument("--planche", action="store_true", help="produire des planches HTML de 50 cartes")
    ap.add_argument("--base-url", default="", help="préfixe des champs media et reference (ex. https://…/)")
    ap.add_argument("--mythiques", default="",
                    help="N° (ou tickers) à passer en mythique (règle v2), ex. 1,2,3 ; un ticker vise toutes les cartes qui le portent")
    a = ap.parse_args(argv)

    v2 = a.catalogue.lower().endswith(".json")
    if v2:
        cartes = lire_catalogue_v2(a.catalogue, inclure_a_decider=a.inclure_a_decider)
    else:
        if a.inclure_a_decider:
            ap.error("--inclure-a-decider ne vaut que pour le catalogue JSON v2")
        cartes = lire_catalogue(a.catalogue)
    if a.mythiques and v2:
        ap.error("--mythiques ne vaut que pour un catalogue markdown : le JSON v2 porte déjà ses mythiques")
    if a.mythiques:
        from dataclasses import replace

        cibles = {t.strip().upper() for t in a.mythiques.split(",") if t.strip()}
        cartes = [
            replace(c, rarete="mythique") if (str(c.numero) in cibles or c.ticker.upper() in cibles) else c
            for c in cartes
        ]
    if a.limit is not None:
        cartes = cartes[: a.limit]
    stats = generer(cartes, a.out, a.base_url, a.planche)
    print(json.dumps(stats, ensure_ascii=False))
    return 0
