"""Tests du générateur : python3 -m unittest discover -s tests (depuis art/)."""

import json
import os
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from dataclasses import replace

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))

from memaster_art.carte import ETATS, MENTION, RARETES, Carte  # noqa: E402
from memaster_art.catalogue import lire_catalogue, lire_lignes, ligne_vers_carte  # noqa: E402
from memaster_art.cli import generer  # noqa: E402
from memaster_art.metadonnees import hash_b64, metadonnees_carte  # noqa: E402
from memaster_art.rendu import rendre_carte, rendre_dos  # noqa: E402

CATALOGUE = os.path.join(ICI, "..", "..", "docs", "catalogue-final.md")
SVG = "{http://www.w3.org/2000/svg}"

# Mots qui ne doivent jamais apparaître hors des champs de données (ticker, nom, chaîne, identifiant).
INTERDITS = [
    "logo", "frog", "grenouille", "dog", "chien", "shiba", "inu", "pepe", "kabosu", "furie",
    "cat", "chat", "face", "visage", "mascot", "mascotte", "official", "officiel", "partenaire officiel",
]
POLICES_OK = {"sans-serif", "serif", "monospace"}

BASE = Carte(
    identifiant="0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce", ticker="TEST", nom="Jeton de test",
    chaine="Ethereum", rarete="rare", etat="actif", annee_pic=2021, numero=42,
)


def toutes_variantes():
    for r in RARETES:
        for e in ETATS:
            yield replace(BASE, rarete=r, etat=e)


class Determinisme(unittest.TestCase):
    def test_meme_entree_meme_image(self):
        for c in toutes_variantes():
            self.assertEqual(rendre_carte(c), rendre_carte(replace(c)))

    def test_entrees_differentes_images_differentes(self):
        a = rendre_carte(BASE)
        self.assertNotEqual(a, rendre_carte(replace(BASE, identifiant="autre")))
        self.assertNotEqual(a, rendre_carte(replace(BASE, rarete="épique")))
        self.assertNotEqual(a, rendre_carte(replace(BASE, etat="mort")))

    def test_dos_identique_pour_toutes_les_mythiques(self):
        # Le dos ne doit rien révéler du recto.
        self.assertEqual(rendre_dos(), rendre_dos())
        self.assertNotIn("TEST", rendre_dos())

    def test_catalogue_entier_deux_fois(self):
        cartes = lire_catalogue(CATALOGUE)[:60]
        self.assertEqual([rendre_carte(c) for c in cartes], [rendre_carte(c) for c in cartes])


class Taille(unittest.TestCase):
    def test_moins_de_30_ko(self):
        for c in list(toutes_variantes()) + lire_catalogue(CATALOGUE):
            self.assertLess(len(rendre_carte(c).encode()), 30_000, c)
        self.assertLess(len(rendre_dos().encode()), 30_000)

    def test_format_5_7(self):
        racine = ET.fromstring(rendre_carte(BASE))
        _, _, w, h = map(float, racine.get("viewBox").split())
        self.assertAlmostEqual(w / h, 5 / 7)


class Juridique(unittest.TestCase):
    def verifier(self, svg: str, donnees: set):
        racine = ET.fromstring(svg)
        for el in racine.iter():
            balise = el.tag.replace(SVG, "")
            self.assertNotIn(balise, {"image", "font-face", "foreignObject", "style", "script", "a"})
            for k, v in el.attrib.items():
                if k == "font-family":
                    self.assertIn(v, POLICES_OK)
                if "href" in k:
                    self.assertTrue(v.startswith("#"), v)
                self.assertNotIn("http", v if k != "xmlns" else "")
        textes = []
        for el in racine.iter():
            t = (el.text or "").strip()
            if not t or t in donnees:
                continue
            if el.tag == SVG + "title":
                continue  # titre = données factuelles seulement
            for d in donnees:
                t = t.replace(d, "")
            textes.append(t.lower())
        corps = " ".join(textes)
        for mot in INTERDITS:
            self.assertIsNone(re.search(rf"\b{re.escape(mot)}", corps), (mot, corps))

    def test_aucun_texte_interdit(self):
        for c in toutes_variantes():
            svg = rendre_carte(c)
            self.verifier(svg, {c.ticker, c.nom, c.chaine})
        self.verifier(rendre_dos(), set())

    def test_aucun_texte_interdit_catalogue(self):
        from memaster_art.rendu import abreger_id, tronquer

        for c in lire_catalogue(CATALOGUE):
            donnees = {c.ticker, c.nom, tronquer(c.nom, 34), c.chaine, tronquer(c.chaine, 16),
                       abreger_id(c.identifiant)}
            self.verifier(rendre_carte(c), {d for d in donnees if d})

    def test_le_garde_fou_detecte_un_mot_interdit(self):
        svg = rendre_carte(BASE).replace("</svg>", "<text>un logo de grenouille</text></svg>")
        with self.assertRaises(AssertionError):
            self.verifier(svg, {BASE.ticker, BASE.nom, BASE.chaine})

    def test_mention_de_non_affiliation(self):
        for c in toutes_variantes():
            svg = rendre_carte(c)
            self.assertIn("Sans lien ni partenariat avec les projets cités", svg)
            self.assertIn(MENTION, svg)  # dans <desc>
        self.assertIn(MENTION, rendre_dos())


class RenduValide(unittest.TestCase):
    def test_xml_bien_forme(self):
        cas = list(toutes_variantes()) + [
            replace(BASE, ticker="A&B<\"'>", nom="Nom <script> & co"),
            replace(BASE, ticker="币安人生", nom="币安人生", chaine=""),
            replace(BASE, ticker="SUPERLONGTICKERNAME2026", annee_pic=None),
        ]
        for c in cas:
            racine = ET.fromstring(rendre_carte(c))
            self.assertEqual(racine.tag, SVG + "svg")
        ET.fromstring(rendre_dos())

    def test_ids_references_definis(self):
        for c in toutes_variantes():
            svg = rendre_carte(c)
            ids = set(re.findall(r'id="([^"]+)"', svg))
            for ref in re.findall(r"url\(#([^)]+)\)", svg):
                self.assertIn(ref, ids)


class Catalogue(unittest.TestCase):
    def test_lecture_catalogue_final(self):
        cartes = lire_catalogue(CATALOGUE)
        self.assertGreater(len(cartes), 500)
        self.assertEqual(cartes[0].ticker, "DOGE")
        self.assertTrue(all(c.rarete in RARETES and c.etat in ETATS for c in cartes))

    def test_format_v2_mythique(self):
        texte = (
            "## Cartes\n\n| N° | Nom | Ticker | Chaîne | Lancement | État actuel | Rareté proposée | Adresse |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| 1 | Dogecoin | DOGE | Dogecoin (blockchain propre) | déc. 2013 | actif | mythique | sans objet |\n"
            "| 2 | Vieux mème | OLD | Solana (à vérifier) | 2021 | mort | commune* | `So1aNa` |\n"
        )
        l1, l2 = [ligne_vers_carte(l, i + 1) for i, l in enumerate(lire_lignes(texte))]
        self.assertEqual((l1.rarete, l1.chaine, l1.annee_pic, l1.identifiant), ("mythique", "Dogecoin", 2013, "memaster:1"))
        self.assertEqual((l2.rarete, l2.etat, l2.chaine, l2.identifiant), ("commune", "mort", "Solana", "So1aNa"))


class Metadonnees(unittest.TestCase):
    def test_nep177(self):
        svg = rendre_carte(BASE).encode()
        meta, ref = metadonnees_carte(BASE, svg)
        for champ in ("title", "description", "media", "media_hash", "extra", "reference", "reference_hash"):
            self.assertIn(champ, meta)
        self.assertIn(MENTION, meta["description"])
        self.assertEqual(meta["media_hash"], hash_b64(svg))
        self.assertEqual(meta["reference_hash"], hash_b64(ref))
        self.assertIsInstance(meta["extra"], str)  # NEP-177 : extra est une chaîne
        self.assertEqual(json.loads(meta["extra"])["rarete"], "rare")

    def test_cli_sortie(self):
        cartes = [replace(BASE, rarete="mythique"), BASE]
        with tempfile.TemporaryDirectory() as d:
            stats = generer(cartes, d, planche=True)
            self.assertEqual(stats["cartes"], 2)
            fichiers = set(os.listdir(d))
            self.assertTrue({"dos-mythique.svg", "dos-mythique.json", "planche-01.html", "0042-test.svg"} <= fichiers)
            with open(os.path.join(d, "0042-test.json"), encoding="utf-8") as f:
                meta = json.load(f)
            with open(os.path.join(d, "0042-test.svg"), "rb") as f:
                octets = f.read()
            self.assertEqual(meta["media_hash"], hash_b64(octets))


if __name__ == "__main__":
    unittest.main()
