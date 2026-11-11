#!/usr/bin/env python3
"""Récupère depuis CoinGecko les images, chaînes et adresses des cartes du catalogue.

Usage : python3 docs/memecoin-booster/recuperer-images.py
Relançable : les images déjà présentes ne sont pas retéléchargées.

Sorties, à côté de ce script :
- images/<id coingecko>.<ext>
- images-manifest.csv : une ligne par carte, avec statut, image, chaînes et adresses

Usage interne : les logos restent soumis aux droits de leurs auteurs (voir visuels-droits.md).
"""
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
CATALOGUE = DOSSIER / "catalogue-final.md"
IMAGES = DOSSIER / "images"
MANIFESTE = DOSSIER / "images-manifest.csv"

API = "https://api.coingecko.com/api/v3"
CATEGORIE = "meme-token"
PAR_PAGE = 250
PAGES_MAX = 12
PAUSE_API = 15
PAUSE_IMAGE = 0.15
ESSAIS = 6
TAILLE_MAX = 5 * 1024 * 1024
HOTES_IMAGES = {"coin-images.coingecko.com", "assets.coingecko.com"}
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
ENTETES = {"User-Agent": "memecoin-catalogue-script/1.0", "Accept": "*/*"}


def lire(url):
    """Renvoie le corps de la réponse, en respectant les limites de débit."""
    for essai in range(1, ESSAIS + 1):
        try:
            requete = urllib.request.Request(url, headers=ENTETES)
            with urllib.request.urlopen(requete, timeout=60) as reponse:
                corps = reponse.read(TAILLE_MAX + 1)
                return corps, reponse.headers.get("Content-Type", "")
        except urllib.error.HTTPError as erreur:
            if erreur.code != 429 and erreur.code < 500:
                raise
            attente = int(erreur.headers.get("Retry-After") or 60) + 5
            print(f"  HTTP {erreur.code}, attente {attente} s (essai {essai}/{ESSAIS})", flush=True)
            time.sleep(min(attente, 120))
        except (urllib.error.URLError, TimeoutError) as erreur:
            print(f"  erreur réseau {erreur}, nouvel essai (essai {essai}/{ESSAIS})", flush=True)
            time.sleep(15)
    raise RuntimeError(f"échec après {ESSAIS} essais : {url}")


def lire_json(url):
    corps, _ = lire(url)
    return json.loads(corps)


def normaliser(texte):
    texte = unicodedata.normalize("NFKC", texte).casefold()
    return re.sub(r"[\W_]+", "", texte)


def cartes():
    """Lit le tableau « Cartes » du catalogue final."""
    lignes = CATALOGUE.read_text(encoding="utf-8").splitlines()
    debut = lignes.index("## Cartes")
    resultat = []
    for ligne in lignes[debut + 1:]:
        if ligne.startswith("## "):
            break
        colonnes = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(colonnes) >= 3 and colonnes[0].isdigit():
            resultat.append({"numero": colonnes[0], "nom": colonnes[1], "ticker": colonnes[2]})
    return resultat


def marche():
    """Toute la catégorie memecoins de CoinGecko, avec l'adresse des images."""
    pieces = []
    for page in range(1, PAGES_MAX + 1):
        requete = urllib.parse.urlencode({
            "vs_currency": "usd", "category": CATEGORIE, "order": "market_cap_desc",
            "per_page": PAR_PAGE, "page": page,
        })
        print(f"CoinGecko, page {page}", flush=True)
        lot = lire_json(f"{API}/coins/markets?{requete}")
        if not lot:
            break
        pieces.extend(lot)
        if len(lot) < PAR_PAGE:
            break
        time.sleep(PAUSE_API)
    return pieces


def indexer(pieces):
    exact, par_nom = {}, {}
    for piece in pieces:  # classées par capitalisation : la première rencontrée est la plus grosse
        nom = normaliser(piece.get("name") or "")
        symbole = normaliser(piece.get("symbol") or "")
        exact.setdefault((nom, symbole), piece)
        par_nom.setdefault(nom, []).append(piece)
    return exact, par_nom


def trouver(carte, exact, par_nom):
    nom = normaliser(carte["nom"])
    symbole = normaliser(carte["ticker"])
    if (nom, symbole) in exact:
        return exact[(nom, symbole)], "nom et ticker"
    candidats = par_nom.get(nom, [])
    if len(candidats) == 1:
        return candidats[0], "nom seul"
    return None, ""


def telecharger(piece):
    """Renvoie (statut, chemin relatif)."""
    url = piece.get("image") or ""
    decoupe = urllib.parse.urlsplit(url)
    if decoupe.scheme != "https" or decoupe.hostname not in HOTES_IMAGES:
        return "adresse d'image refusée", ""
    if "missing" in decoupe.path:
        return "pas d'image chez CoinGecko", ""
    extension = Path(decoupe.path).suffix.lower()
    if extension not in EXTENSIONS:
        extension = ".png"
    identifiant = re.sub(r"[^a-z0-9._-]", "-", piece["id"].lower())
    cible = IMAGES / f"{identifiant}{extension}"
    relatif = str(cible.relative_to(DOSSIER))
    if cible.exists() and cible.stat().st_size > 0:
        return "déjà là", relatif
    corps, type_contenu = lire(url)
    if len(corps) > TAILLE_MAX:
        return "image trop lourde", ""
    if not type_contenu.startswith("image/"):
        return f"type inattendu {type_contenu}", ""
    temporaire = cible.with_suffix(cible.suffix + ".part")
    temporaire.write_bytes(corps)
    os.replace(temporaire, cible)
    time.sleep(PAUSE_IMAGE)
    return "téléchargée", relatif


def principal():
    IMAGES.mkdir(exist_ok=True)
    liste = cartes()
    print(f"{len(liste)} cartes dans le catalogue", flush=True)

    pieces = marche()
    print(f"{len(pieces)} memecoins chez CoinGecko", flush=True)
    exact, par_nom = indexer(pieces)

    time.sleep(PAUSE_API)
    print("CoinGecko, chaînes et adresses", flush=True)
    plateformes = {p["id"]: p.get("platforms") or {} for p in lire_json(f"{API}/coins/list?include_platform=true")}

    totaux = {}
    with MANIFESTE.open("w", newline="", encoding="utf-8") as sortie:
        ecrivain = csv.writer(sortie)
        ecrivain.writerow(["numero", "nom", "ticker", "statut", "correspondance", "coingecko_id", "image_url", "fichier", "plateformes_json"])
        for rang, carte in enumerate(liste, 1):
            piece, correspondance = trouver(carte, exact, par_nom)
            if piece is None:
                statut, fichier, identifiant, url, chaines = "sans correspondance", "", "", "", ""
            else:
                try:
                    statut, fichier = telecharger(piece)
                except (urllib.error.URLError, RuntimeError, TimeoutError) as erreur:
                    statut, fichier = f"erreur : {erreur}", ""
                identifiant, url = piece["id"], piece.get("image") or ""
                chaines = json.dumps(plateformes.get(piece["id"], {}), ensure_ascii=False, sort_keys=True)
            cle = statut.split(" :")[0]
            totaux[cle] = totaux.get(cle, 0) + 1
            ecrivain.writerow([carte["numero"], carte["nom"], carte["ticker"], statut, correspondance, identifiant, url, fichier, chaines])
            if rang % 50 == 0:
                sortie.flush()
                print(f"{rang}/{len(liste)}", flush=True)

    print("Terminé :", json.dumps(totaux, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(principal())
