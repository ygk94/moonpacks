"""Tests du catalogue JSON v2 : python3 -m unittest discover -s tests (depuis art/)."""

import json
import os
import re
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))

from memaster_art import catalogue_v2  # noqa: E402
from memaster_art.catalogue_v2 import lire_catalogue_v2, lire_entrees  # noqa: E402
from memaster_art.cli import generer, main  # noqa: E402
from memaster_art.rendu import rendre_carte, rendre_dos  # noqa: E402

DATA = os.path.join(ICI, "..", "..", "docs", "data")
CATALOGUE_V2 = os.path.join(DATA, "catalogue-v2.json")
CATALOGUE_DEMO = os.path.join(DATA, "catalogue-demo.json")
# Vrais noms des mythiques : hors git (docs/data/secrets/, écrit par consolider.py), jamais dans ce dépôt.
SECRETS = os.path.join(DATA, "secrets", "mythiques.json")


def vrais_noms():
    """Motif des vrais noms, tickers, ids CoinGecko et adresses des mythiques, ou None sans fichier secret."""
    if not os.path.exists(SECRETS):
        return None
    with open(SECRETS, encoding="utf-8") as f:
        mythiques = json.load(f)["mythiques"]
    mots = {v for m in mythiques for k in ("nom", "ticker", "coingecko_id", "adresse")
            for v in [str(m.get(k) or "").strip("`")] if len(v) >= 3}
    return re.compile("|".join(re.escape(m) for m in sorted(mots, key=len, reverse=True)), re.I)

MINI = [
    {"id": "vieux-meme-old", "numero": "7", "section": "catalogue", "nom": "Vieux mème †", "ticker": "OLD",
     "chaine_normalisee": "Solana", "lancement": "2021", "epoque": "2019-2022", "pic": "≈ 3 M$ le 04/03/2022",
     "etat": "mort (absent de CoinGecko)", "rarete": "commune", "drapeau": "arnaque avérée", "burn": "à définir",
     "adresse": "So1aNaAdresseDeTest1234567890"},
    {"id": "en-suspens-sus", "numero": "AD1", "section": "à décider", "nom": "Suspens", "ticker": "SUS",
     "chaine_normalisee": "à vérifier", "lancement": "à vérifier", "epoque": "inconnue", "pic": "?",
     "etat": "à vérifier (source muette)", "rarete": "rare", "drapeau": "politique", "burn": "à définir", "adresse": ""},
    {"id": "mythique-m1", "numero": "M1", "section": "catalogue", "nom": "?", "ticker": "?", "etat": "?",
     "rarete": "mythique", "burn": "à définir", "adresse": "?", "visuel": "?",
     # Ancien format (avant le 11/11) : un champ `secret` éventuel doit toujours être jeté au décodage.
     "secret": {"nom": "Nom Caché", "ticker": "CACHE", "adresse": "0xSECRETSECRETSECRET"}},
]


def _ecrire_mini(d):
    chemin = os.path.join(d, "mini.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(MINI, f, ensure_ascii=False)
    return chemin


class LectureV2(unittest.TestCase):
    def test_section_et_id_stable(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = _ecrire_mini(d)
            cartes = lire_catalogue_v2(chemin)
            self.assertEqual([c.cle for c in cartes], ["vieux-meme-old", "mythique-m1"])
            tout = lire_catalogue_v2(chemin, inclure_a_decider=True)
            self.assertEqual(len(tout), 3)
        old = cartes[0]
        self.assertEqual((old.identifiant, old.nom_fichier, old.numero), ("vieux-meme-old", "vieux-meme-old", 7))
        self.assertEqual((old.etat, old.chaine, old.annee_pic, old.nom, old.burn), ("mort", "Solana", 2022, "Vieux mème", ""))
        self.assertEqual(tout[1].etat, "à vérifier")
        self.assertEqual(tout[1].nom_fichier, "en-suspens-sus")

    def test_etats_v2(self):
        e = {"id": "x", "numero": "1", "section": "catalogue", "rarete": "rare", "ticker": "X", "nom": "X"}
        attendu = {"mort": "mort", "mort (≈ 13 k$)": "mort", "en déclin (-95 % ou pire)": "en déclin",
                   "actif": "actif", "à vérifier (sommet 2026)": "à vérifier"}
        for brut, etat in attendu.items():
            self.assertEqual(catalogue_v2.entree_vers_carte(dict(e, etat=brut)).etat, etat)

    def test_carte_morte_style_cimetiere_sans_drapeau_ni_burn(self):
        with tempfile.TemporaryDirectory() as d:
            old = lire_catalogue_v2(_ecrire_mini(d))[0]
        svg = rendre_carte(old)
        self.assertIn("ICI REPOSE", svg)
        self.assertIn("† 2022", svg)
        for absent in ("arnaque", "drapeau", "à définir", "burn"):
            self.assertNotIn(absent, svg.lower())

    def test_secret_jamais_lu(self):
        with tempfile.TemporaryDirectory() as d:
            entrees = lire_entrees(_ecrire_mini(d))
        self.assertTrue(all("secret" not in e and "drapeau" not in e for e in entrees))
        texte = json.dumps(entrees, ensure_ascii=False)
        self.assertNotIn("Nom Caché", texte)
        self.assertNotIn("0xSECRET", texte)

    def test_json_publics_sans_secret(self):
        for chemin in (CATALOGUE_V2, CATALOGUE_DEMO):
            with open(chemin, encoding="utf-8") as f:
                texte = f.read()
            self.assertNotIn('"secret"', texte, chemin)
            motif = vrais_noms()
            for e in json.loads(texte):
                self.assertNotIn("secret", e)
                if e["rarete"] == "mythique":
                    self.assertEqual((e["nom"], e["ticker"], e["coingecko_id"], e["adresse"]), ("?",) * 4)
                    if motif:
                        self.assertIsNone(motif.search(json.dumps(e, ensure_ascii=False)), e["id"])


class MythiquesScellees(unittest.TestCase):
    def test_sorties_m1_m3_sans_vrai_nom(self):
        cartes = lire_catalogue_v2(CATALOGUE_V2)
        mythiques = [c for c in cartes if c.rarete == "mythique"]
        self.assertEqual([c.numero for c in mythiques], ["M1", "M2", "M3"])
        self.assertTrue(all(c.scellee and c.ticker == "?" and c.nom == "?" for c in mythiques))
        with tempfile.TemporaryDirectory() as d:
            generer(mythiques, d, planche=True)
            fichiers = sorted(os.listdir(d))
            # Seuls le dos commun, ses métadonnées et un JSON par mythique : aucun recto.
            self.assertEqual(fichiers, ["dos-mythique.json", "dos-mythique.svg", "mythique-m1.json",
                                        "mythique-m2.json", "mythique-m3.json", "planche-01.html"])
            dos = rendre_dos().encode()
            with open(os.path.join(d, "dos-mythique.svg"), "rb") as f:
                self.assertEqual(f.read(), dos)
            motif = vrais_noms()
            for nom in fichiers:
                with open(os.path.join(d, nom), encoding="utf-8") as f:
                    contenu = f.read()
                self.assertNotIn("secret", contenu.lower(), nom)
                if motif:
                    self.assertIsNone(motif.search(contenu), nom)
            for c in mythiques:
                with open(os.path.join(d, c.nom_fichier + ".json"), encoding="utf-8") as f:
                    meta = json.load(f)
                self.assertEqual(meta["media"], "dos-mythique.svg")
                self.assertIsNone(meta["reference"])
                self.assertEqual(json.loads(meta["extra"])["identifiant"], c.cle)

    def test_le_lecteur_ne_touche_pas_au_champ_secret(self):
        # Le code du générateur ne référence « secret » qu'à un seul endroit : le filtre qui le jette.
        dossier = os.path.join(ICI, "..", "memaster_art")
        for nom in os.listdir(dossier):
            if nom.endswith(".py"):
                with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                    code = f.read()
                occurrences = re.findall(r"[\"']secret[\"']", code)
                self.assertEqual(len(occurrences), 1 if nom == "catalogue_v2.py" else 0, nom)


class CliV2(unittest.TestCase):
    def test_cli_json(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = _ecrire_mini(d)
            out = os.path.join(d, "out")
            self.assertEqual(main(["--catalogue", chemin, "--out", out]), 0)
            self.assertEqual(sorted(os.listdir(out)), ["dos-mythique.json", "dos-mythique.svg", "mythique-m1.json",
                                                       "vieux-meme-old.json", "vieux-meme-old.ref.json", "vieux-meme-old.svg"])
            with open(os.path.join(out, "vieux-meme-old.ref.json"), encoding="utf-8") as f:
                ref = json.load(f)
            self.assertEqual((ref["identifiant"], ref["burn"], ref["numero"]), ("vieux-meme-old", None, 7))
            self.assertNotIn("drapeau", ref)
            out2 = os.path.join(d, "out2")
            main(["--catalogue", chemin, "--out", out2, "--inclure-a-decider"])
            self.assertIn("en-suspens-sus.svg", os.listdir(out2))

    def test_catalogue_v2_complet(self):
        cartes = lire_catalogue_v2(CATALOGUE_V2)
        self.assertEqual(len(cartes), 1649)
        self.assertEqual(len({c.cle for c in cartes}), len(cartes))
        self.assertEqual(len(lire_catalogue_v2(CATALOGUE_V2, inclure_a_decider=True)), 1750)
        for c in cartes[:80]:
            if not c.scellee:
                self.assertLess(len(rendre_carte(c).encode()), 30_000)


class CatalogueDemo(unittest.TestCase):
    def test_demo_lisible(self):
        cartes = lire_catalogue_v2(CATALOGUE_DEMO)
        with open(CATALOGUE_DEMO, encoding="utf-8") as f:
            brut = json.load(f)
        self.assertEqual(len(cartes), len(brut))
        self.assertEqual(sum(c.rarete == "mythique" for c in cartes), 3)
        self.assertTrue(all(c.scellee for c in cartes if c.rarete == "mythique"))
        self.assertGreaterEqual(sum(e["brulable_possible"] for e in brut), 150)


if __name__ == "__main__":
    unittest.main()
