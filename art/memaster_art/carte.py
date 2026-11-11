"""Modèle de carte et normalisation des champs du catalogue."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass

VERSION_GENERATEUR = "1.0.0"

RARETES = ("commune", "rare", "épique", "légendaire", "mythique")
ETATS = ("actif", "en déclin", "mort", "à vérifier")

MENTION = "Sans lien ni partenariat avec les projets, créateurs ou titulaires cités."
MENTION_COURTE = "Sans lien ni partenariat avec les projets cités"


def _sans_accents(texte: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normaliser_rarete(brut: str) -> str:
    """'épique*' -> 'épique', 'Legendaire' -> 'légendaire', inconnu -> 'commune'."""
    t = _sans_accents((brut or "").replace("*", "").strip().lower())
    for r in RARETES:
        if t.startswith(_sans_accents(r)):
            return r
    return "commune"


def normaliser_etat(brut: str) -> str:
    """'en déclin (dérivé)' -> 'en déclin' ; tout le reste non reconnu -> 'à vérifier'."""
    t = _sans_accents((brut or "").strip().lower())
    if t.startswith("mort"):
        return "mort"
    if t.startswith("en declin"):
        return "en déclin"
    if t.startswith("actif"):
        return "actif"
    return "à vérifier"


def normaliser_chaine(brut: str) -> str:
    """Première chaîne citée, sans parenthèses. '' si inconnue."""
    t = re.sub(r"\(.*?\)", "", brut or "").strip()
    t = re.split(r"[,;/+]| et ", t)[0].strip()
    if not t or _sans_accents(t.lower()).startswith("a verifier"):
        return ""
    return t


def extraire_annee(*textes: str) -> int | None:
    for texte in textes:
        m = re.search(r"\b(20[0-4]\d|199\d)\b", texte or "")
        if m:
            return int(m.group(1))
    return None


def nettoyer_nom(brut: str) -> str:
    return re.sub(r"\s*†\s*", " ", brut or "").strip()


def nettoyer_adresse(brut: str) -> str:
    """Renvoie l'adresse si la cellule en contient une (entre backticks), sinon ''."""
    m = re.search(r"`([^`]+)`", brut or "")
    return m.group(1).strip() if m else ""


def slug(texte: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", _sans_accents(texte).lower()).strip("-")
    if not s:
        s = "x" + hashlib.sha256(texte.encode()).hexdigest()[:6]
    return s[:24]


@dataclass(frozen=True)
class Carte:
    """Entrée du générateur. Le visuel est une fonction pure de ces champs."""

    identifiant: str  # adresse du contrat, ou « memaster:N° » à défaut
    ticker: str
    nom: str
    chaine: str  # '' si inconnue
    rarete: str  # une valeur de RARETES
    etat: str  # une valeur de ETATS
    annee_pic: int | None
    numero: int | str | None = None  # int (v1), ou chaîne v2 (« 12 », « M1 », « AD3 »)
    cle: str = ""  # id stable v2 (slug) : nom de fichier et identifiant public
    adresse: str = ""  # adresse du contrat (v2), affichée en pied de carte si connue
    burn: str = ""  # règle de burn v2 ; « à définir » est ramené à ''
    scellee: bool = False  # mythique scellée : seul le dos « ? » est publié

    def __post_init__(self):
        if self.rarete not in RARETES:
            raise ValueError(f"rareté inconnue : {self.rarete!r}")
        if self.etat not in ETATS:
            raise ValueError(f"état inconnu : {self.etat!r}")
        if self.cle and not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", self.cle):
            raise ValueError(f"id de carte invalide : {self.cle!r}")

    @property
    def graine(self) -> bytes:
        """Graine de l'art : identifiant, ticker et chaîne (pas la rareté ni l'état,
        qui ne changent que le cadre et les effets)."""
        cle = f"memaster-art|{self.identifiant}|{self.ticker}|{self.chaine}"
        return hashlib.sha256(cle.encode("utf-8")).digest()

    @property
    def nom_fichier(self) -> str:
        if self.cle:
            return self.cle
        prefixe = f"{self.numero:04d}-" if isinstance(self.numero, int) else ""
        return prefixe + slug(self.ticker)
