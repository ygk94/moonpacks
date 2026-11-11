"""Lecture directe du catalogue v2 (docs/data/catalogue-v2.json).

Règles :
- seules les entrées `section == "catalogue"` sont prises, sauf `inclure_a_decider=True`
  (ajoute la section « à décider ») ;
- l'identifiant de carte est l'`id` stable (slug), pas le numéro ;
- le JSON public n'a plus de champ `secret` (vrais noms dans docs/data/secrets/, hors git, jamais lu ici) ;
  par prudence, un `secret` d'un ancien JSON est retiré dès le décodage (`object_pairs_hook`), puis seuls
  les champs de `CHAMPS_LUS` sont consultés ;
- une mythique est toujours scellée : ticker et nom forcés à « ? », rien d'autre n'est gardé ;
- `drapeau` n'est pas lu (il ne s'affiche pas sur la carte) ; `burn = à définir` devient ''.
"""

from __future__ import annotations

import json
import re

from .carte import (
    Carte,
    extraire_annee,
    nettoyer_nom,
    normaliser_chaine,
    normaliser_etat,
    normaliser_rarete,
)

SECTION_CATALOGUE = "catalogue"
SECTION_A_DECIDER = "à décider"

# Liste blanche : le générateur ne consulte aucun autre champ (ni `secret`, ni `drapeau`).
CHAMPS_LUS = (
    "id", "numero", "section", "nom", "ticker", "chaine_normalisee",
    "lancement", "epoque", "pic", "etat", "rarete", "burn", "adresse",
)

_ADRESSE = re.compile(r"[A-Za-z0-9_.:-]{16,}")


def _sans_secret(paires):
    return {k: v for k, v in paires if k != "secret"}


def lire_entrees(chemin: str) -> list[dict]:
    """Entrées brutes du JSON, réduites à CHAMPS_LUS (le champ `secret` est jeté au décodage)."""
    with open(chemin, encoding="utf-8") as f:
        donnees = json.load(f, object_pairs_hook=_sans_secret)
    if not isinstance(donnees, list):
        raise ValueError("catalogue v2 : une liste d'entrées est attendue")
    return [{k: e.get(k) for k in CHAMPS_LUS} for e in donnees]


def _texte(v) -> str:
    return "" if v is None else str(v).strip()


def _numero(brut: str):
    return int(brut) if brut.isdigit() else (brut or None)


def _burn(brut: str) -> str:
    return "" if brut.lower() in ("", "?", "à définir", "a definir") else brut


def entree_vers_carte(e: dict) -> Carte:
    cle = _texte(e.get("id"))
    if not cle:
        raise ValueError(f"entrée sans id : N° {e.get('numero')!r}")
    rarete = normaliser_rarete(_texte(e.get("rarete")))
    numero = _numero(_texte(e.get("numero")))
    if rarete == "mythique":
        # Scellée : aucune donnée de recto n'est reprise, même si le JSON public en contenait.
        return Carte(identifiant=cle, ticker="?", nom="?", chaine="", rarete="mythique",
                     etat="à vérifier", annee_pic=None, numero=numero, cle=cle, scellee=True)
    adresse = _texte(e.get("adresse")).strip("`")
    return Carte(
        identifiant=cle,
        ticker=_texte(e.get("ticker")).replace("`", "") or "?",
        nom=nettoyer_nom(_texte(e.get("nom"))),
        chaine=normaliser_chaine(_texte(e.get("chaine_normalisee"))),
        rarete=rarete,
        etat=normaliser_etat(_texte(e.get("etat"))),
        annee_pic=extraire_annee(_texte(e.get("pic")), _texte(e.get("lancement"))),
        numero=numero,
        cle=cle,
        adresse=adresse if _ADRESSE.fullmatch(adresse) else "",
        burn=_burn(_texte(e.get("burn"))),
    )


def lire_catalogue_v2(chemin: str, inclure_a_decider: bool = False) -> list[Carte]:
    sections = {SECTION_CATALOGUE} | ({SECTION_A_DECIDER} if inclure_a_decider else set())
    cartes = [entree_vers_carte(e) for e in lire_entrees(chemin) if _texte(e.get("section")) in sections]
    vus: set[str] = set()
    for c in cartes:
        if c.cle in vus:
            raise ValueError(f"id en double : {c.cle}")
        vus.add(c.cle)
    return cartes
