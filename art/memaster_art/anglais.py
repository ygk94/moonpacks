"""Version anglaise des visuels (pour le front, dont l'interface est en anglais).

Traduit après coup les textes visibles d'un SVG rendu par `rendu.py` : seuls les nœuds texte dont le
contenu entier est un libellé connu changent, plus `<title>` et `<desc>`. Le ticker et le nom du coin sont des
données et ne sont pas traduits, sauf le ticker inconnu (« à vérifier » → « TBD ») et une précision française
entre parenthèses à la fin d'un nom, retirée.
"""

from __future__ import annotations

import re

from .carte import MENTION_COURTE

# Libellés exacts : contenu entier d'un nœud <text>.
LIBELLES = {
    "COMMUNE": "COMMON",
    "RARE": "RARE",
    "ÉPIQUE": "EPIC",
    "LÉGENDAIRE": "LEGENDARY",
    "MYTHIQUE": "MYTHIC",
    "MYTHIQUE · SECRÈTE": "MYTHIC · SECRET",
    "SCELLÉE": "SEALED",
    "CARTE SECRÈTE": "SECRET CARD",
    "à révéler à l'ouverture": "revealed at opening",
    "ICI REPOSE": "HERE LIES",
    "CIMETIÈRE DES MÈMES": "MEME GRAVEYARD",
    "actif": "active",
    "en déclin": "declining",
    "† mort": "† dead",
    "état ?": "status ?",
    "chaîne ?": "chain ?",
    "pic inconnu": "peak unknown",
    "blockchain prop…": "own chain",
    "blockchain propre": "own chain",
    MENTION_COURTE: "Not affiliated with the projects mentioned",
}

# Libellés à préfixe : « pic 2021 », « N° 0012 », « réf. memaster:12 ».
PREFIXES = (
    (re.compile(r"^pic (\d{4}|\?)$"), r"peak \1"),
    (re.compile(r"^N° (.+)$"), r"No. \1"),
    (re.compile(r"^réf\. (.+)$"), r"ref. \1"),
)

RARETES = {"commune": "common", "rare": "rare", "épique": "epic", "légendaire": "legendary", "mythique": "mythic"}

DESC = (
    "Memaster card. Ticker cited as factual data; abstract generative visual. "
    "Not affiliated with the projects, creators or rights holders mentioned."
)
DESC_DOS = (
    "Sealed back of a Memaster mythic card, identical for every mythic. "
    "Not affiliated with the projects, creators or rights holders mentioned."
)

_TEXTE = re.compile(r"(<text\b[^>]*>)([^<]*)(</text>)")


# Précision en français entre parenthèses dans un nom (« 財務自由 (Liberté financière) ») : retirée.
_PRECISION_FR = re.compile(r" \((?=[^)]*(?:[éèàêç]|\bne\b|\bde\b|\bla\b|\ble\b))[^)]*\)?$")


def _libelle(t: str) -> str:
    if t in LIBELLES:
        return LIBELLES[t]
    for motif, rempl in PREFIXES:
        if motif.match(t):
            return motif.sub(rempl, t)
    return t


def _noeud(m: re.Match) -> str:
    """Le nom et le ticker sont des données : seuls le ticker inconnu et une précision française changent."""
    balise, t = m.group(1), m.group(2)
    if 'opacity=".82"' in balise:  # nom du coin (bloc sous le ticker)
        t = _PRECISION_FR.sub("", t)
    elif re.search(r'font-size="(\d+(?:\.\d+)?)" font-weight="700" fill="[^"]+" text-anchor="middle"', balise) \
            and float(re.search(r'font-size="([\d.]+)"', balise).group(1)) >= 30 and not t.startswith("†"):
        t = "TBD" if t == "à vérifier" else t  # ticker
    else:
        t = _libelle(t)
    return m.group(1) + t + m.group(3)


def _titre(m: re.Match) -> str:
    t = m.group(1)
    if t == "Memaster · carte mythique scellée":
        return "<title>Memaster · sealed mythic card</title>"
    parties = t.rsplit(" · ", 1)
    if len(parties) == 2 and parties[1] in RARETES:
        # « TICKER · Nom (précision française) » : la précision part, comme sous le ticker de la carte.
        tete = parties[0].split(" · ", 1)
        tete[-1] = _PRECISION_FR.sub("", tete[-1])
        t = " · ".join(tete) + " · " + RARETES[parties[1]]
    # Ticker inconnu en tête du titre (« à vérifier · Nom · rareté ») : même libellé que sur la carte.
    if t.startswith("à vérifier · "):
        t = "TBD" + t[len("à vérifier"):]
    return f"<title>{t}</title>"


def en_anglais(svg: str) -> str:
    """Le même SVG, textes visibles en anglais."""
    dos = "carte mythique scellée" in svg[:600]
    svg = _TEXTE.sub(_noeud, svg)
    svg = re.sub(r"<title>([^<]*)</title>", _titre, svg, count=1)
    svg = re.sub(r"<desc>[^<]*</desc>", f"<desc>{DESC_DOS if dos else DESC}</desc>", svg, count=1)
    return svg
