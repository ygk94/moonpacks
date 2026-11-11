"""Lecture du tableau « Cartes » d'un catalogue markdown (format actuel et v2)."""

from __future__ import annotations

import re
import unicodedata

from .carte import (
    Carte,
    extraire_annee,
    nettoyer_adresse,
    nettoyer_nom,
    normaliser_chaine,
    normaliser_etat,
    normaliser_rarete,
)

# Noms de colonnes acceptés (sans accents, en minuscules) -> champ interne.
ALIAS = {
    "n°": "numero", "no": "numero", "n": "numero", "numero": "numero", "#": "numero",
    "nom": "nom",
    "ticker": "ticker",
    "chaine": "chaine",
    "periode de gloire": "periode", "lancement": "periode",
    "pic de capitalisation": "pic", "pic de capitalisation (date)": "pic",
    "etat": "etat", "etat actuel": "etat",
    "rarete": "rarete", "rarete proposee": "rarete", "rarete v2": "rarete",
    "adresse": "adresse", "contrat": "adresse",
}


def _cle(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.strip().lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("*", "").strip()


def _cellules(ligne: str) -> list[str]:
    ligne = ligne.strip()
    if ligne.startswith("|"):
        ligne = ligne[1:]
    if ligne.endswith("|"):
        ligne = ligne[:-1]
    # Les « | » échappés (\|) restent dans la cellule.
    return [c.replace("\\|", "|").strip() for c in re.split(r"(?<!\\)\|", ligne)]


def lire_lignes(texte: str, section: str = "Cartes") -> list[dict]:
    """Renvoie les lignes du premier tableau de la section `## <section>`."""
    lignes = texte.splitlines()
    debut = None
    for i, l in enumerate(lignes):
        if re.match(rf"^##\s+{re.escape(section)}\s*$", l.strip()):
            debut = i + 1
            break
    if debut is None:
        raise ValueError(f"section « {section} » introuvable")
    entete, sortie = None, []
    for l in lignes[debut:]:
        s = l.strip()
        if s.startswith("## "):
            break
        if not s.startswith("|"):
            if entete is not None and sortie:
                break
            continue
        cells = _cellules(s)
        if entete is None:
            entete = [ALIAS.get(_cle(c), _cle(c)) for c in cells]
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        sortie.append(dict(zip(entete, cells)))
    if entete is None:
        raise ValueError(f"aucun tableau dans la section « {section} »")
    manquantes = {"nom", "ticker", "rarete"} - set(entete)
    if manquantes:
        raise ValueError(f"colonnes manquantes : {sorted(manquantes)}")
    return sortie


def ligne_vers_carte(l: dict, index: int) -> Carte:
    try:
        numero = int(re.sub(r"\D", "", l.get("numero", "")) or index)
    except ValueError:
        numero = index
    adresse = nettoyer_adresse(l.get("adresse", ""))
    return Carte(
        identifiant=adresse or f"memaster:{numero}",
        ticker=(l.get("ticker") or "?").replace("`", "").strip(),
        nom=nettoyer_nom(l.get("nom", "")),
        chaine=normaliser_chaine(l.get("chaine", "")),
        rarete=normaliser_rarete(l.get("rarete", "")),
        etat=normaliser_etat(l.get("etat", "")),
        annee_pic=extraire_annee(l.get("periode", ""), l.get("pic", "")),
        numero=numero,
    )


def lire_catalogue(chemin: str) -> list[Carte]:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    return [ligne_vers_carte(l, i + 1) for i, l in enumerate(lire_lignes(texte))]
