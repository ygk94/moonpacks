"""Version anglaise des visuels (--langue en) : python3 -m unittest discover -s tests (depuis art/)."""

import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from dataclasses import replace

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))

from memaster_art.anglais import en_anglais  # noqa: E402
from memaster_art.carte import ETATS, RARETES, Carte  # noqa: E402
from memaster_art.rendu import rendre_carte, rendre_dos  # noqa: E402

SVG = "{http://www.w3.org/2000/svg}"
FRANCAIS = re.compile(r"COMMUNE|ÉPIQUE|LÉGENDAIRE|MYTHIQUE|SCELLÉE|SECRÈTE|CIMETIÈRE|REPOSE|\bpic\b|déclin|"
                      r"\bactif\b|\bmort\b|état|chaîne|N°|réf\.|Sans lien|vérifier|révéler")


def textes(svg: str) -> list[str]:
    racine = ET.fromstring(svg.split("\n", 1)[1])
    return [t.text or "" for t in racine.iter(SVG + "text")] + [
        racine.find(SVG + "title").text, racine.find(SVG + "desc").text]


class TestAnglais(unittest.TestCase):
    def carte(self, **kw):
        base = Carte(numero=7, nom="Exemple Coin", ticker="EXC", chaine="Solana", annee_pic=2021,
                     etat="actif", rarete="rare", identifiant="memaster:7", adresse="")
        return replace(base, **kw)

    def test_aucun_libelle_francais(self):
        for rarete in RARETES:
            for etat in ETATS:
                for annee in (2021, None):
                    svg = en_anglais(rendre_carte(self.carte(rarete=rarete, etat=etat, annee_pic=annee, chaine="")))
                    for t in textes(svg):
                        self.assertIsNone(FRANCAIS.search(t), f"{rarete}/{etat} : {t!r}")
        for t in textes(en_anglais(rendre_dos())):
            self.assertIsNone(FRANCAIS.search(t), t)

    def test_donnees_intactes(self):
        t = textes(en_anglais(rendre_carte(self.carte(ticker="COMMUNE", nom="actif"))))
        self.assertIn("COMMUNE", t)
        self.assertIn("actif", t)
        self.assertIn("No. 0007", t)
        self.assertIn("peak 2021", t)
        self.assertIn("Solana", t)

    def test_ticker_inconnu_et_precision(self):
        t = textes(en_anglais(rendre_carte(self.carte(ticker="à vérifier", nom="財務自由 (Liberté financière)"))))
        self.assertIn("TBD", t)
        self.assertIn("財務自由", t)

    def test_seuls_les_textes_changent(self):
        svg = rendre_carte(self.carte())
        sans_texte = lambda s: re.sub(r"<(text|title|desc)\b[^>]*>[^<]*</\1>", "", s)  # noqa: E731
        self.assertEqual(sans_texte(svg), sans_texte(en_anglais(svg)))


if __name__ == "__main__":
    unittest.main()
