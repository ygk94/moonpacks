"""Métadonnées NEP-177 (NEAR NFT) par carte.

`extra` est une chaîne JSON, comme le veut NEP-177. `reference` pointe vers un JSON
hors chaîne plus complet, dont le hash est donné dans `reference_hash`.
"""

from __future__ import annotations

import base64
import hashlib
import json

from .carte import MENTION, VERSION_GENERATEUR, Carte


def hash_b64(donnees: bytes) -> str:
    return base64.b64encode(hashlib.sha256(donnees).digest()).decode("ascii")


def _json(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def reference_carte(carte: Carte) -> dict:
    ref = {
        "generateur": f"memaster_art {VERSION_GENERATEUR}",
        "numero": carte.numero,
        "identifiant": carte.identifiant,
        "ticker": carte.ticker,
        "nom": carte.nom,
        "chaine": carte.chaine or None,
        "rarete": carte.rarete,
        "etat": carte.etat,
        "annee_pic": carte.annee_pic,
        "visuel": "génératif abstrait, sans logo, personnage ni police imitée",
        "non_affiliation": MENTION,
    }
    if carte.cle:  # catalogue v2 : adresse et burn (null tant que « à définir »)
        ref["adresse"] = carte.adresse or None
        ref["burn"] = carte.burn or None
    return ref


def metadonnees_carte(carte: Carte, svg: bytes, base_url: str = "") -> tuple[dict, bytes]:
    """Renvoie (métadonnées NEP-177, octets du JSON de référence)."""
    ref = _json(reference_carte(carte))
    nom = carte.nom_fichier
    annee = carte.annee_pic or "inconnue"
    meta = {
        "title": f"{carte.ticker} · {carte.nom}"[:120],
        "description": (
            f"Carte Memaster {carte.rarete} ({carte.etat}). Memecoin {carte.ticker}, "
            f"chaîne {carte.chaine or 'à vérifier'}, année du pic {annee}. "
            f"Le ticker est cité comme donnée factuelle ; visuel génératif abstrait. {MENTION}"
        ),
        "media": f"{base_url}{nom}.svg",
        "media_hash": hash_b64(svg),
        "copies": None,
        "extra": json.dumps(
            {
                "rarete": carte.rarete,
                "etat": carte.etat,
                "chaine": carte.chaine or None,
                "annee_pic": carte.annee_pic,
                "identifiant": carte.identifiant,
                "numero": carte.numero,
                "non_affiliation": MENTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        "reference": f"{base_url}{nom}.ref.json",
        "reference_hash": hash_b64(ref),
    }
    return meta, ref


def metadonnees_dos(svg: bytes, base_url: str = "", carte: Carte | None = None) -> dict:
    """Métadonnées de toute mythique, avant comme après la révélation : titre « ? », description
    « ? », image « ? » (le dos commun). Rien qui trahisse le coin, et rien qui distingue une mythique
    d'une autre : `carte` est ignorée (ni id, ni N°), les JSON des mythiques sont identiques."""
    del carte
    extra = {"rarete": "mythique", "non_affiliation": MENTION}
    return {
        "title": "?",
        "description": "?",
        "media": f"{base_url}dos-mythique.svg",
        "media_hash": hash_b64(svg),
        "extra": json.dumps(extra, ensure_ascii=False, sort_keys=True),
        "reference": None,
        "reference_hash": None,
    }


def en_octets(obj) -> bytes:
    return _json(obj)
