#!/usr/bin/env python3
"""Tests légers de consolider.py : parsing, dédoublonnage, règle de rareté.

Lancer : python3 -m unittest docs/recherche-v2/test_consolider.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consolider as C  # noqa: E402


class TestParsing(unittest.TestCase):
    def test_montants(self):
        self.assertEqual(C.parse_montant("≈ 88,8 Md$, mai 2021 (CoinGecko)"), 88.8e9)
        self.assertEqual(C.parse_montant("≈ 151 k$, 23/02/2014"), 151e3)
        self.assertEqual(C.parse_montant("≈ 85-100 M$, 31 juil. 2023"), 85e6)  # bas de fourchette
        self.assertEqual(C.parse_montant("> 7 à 11 Md$ (Cointelegraph)"), 7e9)
        self.assertIsNone(C.parse_montant("inconnu (≈ 1,7 M$, photo sans date)"))
        self.assertIsNone(C.parse_montant("ATH 0,00419 $ le 23/05/2023"))  # un prix n'est pas un pic

    def test_natures(self):
        self.assertEqual(C.norm_nature("sourcé (CMC historique)"), "sourcé")
        self.assertEqual(C.norm_nature("estimé (FDV)"), "estimé")
        self.assertEqual(C.norm_nature("estimé CG, au-dessus de la borne sourcée"), "estimé")
        self.assertEqual(C.norm_nature("corrigé"), "sourcé")
        self.assertEqual(C.norm_nature(""), "inconnu")

    def test_rarete_texte_libre(self):
        self.assertEqual(C.norm_rarete("épique*"), "épique")
        self.assertEqual(C.norm_rarete("rare (épique si l'on compte l'histoire)"), "rare")
        self.assertEqual(C.norm_rarete("légendaire selon la règle v2"), "légendaire")

    def test_segments_hors_parentheses(self):
        segs = C.split_segments("≈ 87 M$ (ATH × 156 T ; ≈ 435 M$ total) ; reste rare")
        self.assertEqual(segs, ["≈ 87 M$ (ATH × 156 T ; ≈ 435 M$ total)", "reste rare"])

    def test_correction(self):
        a = C.analyse_correction("Pic ; rareté ; état", "≈ 928 M$, 06/12/2017 ; épique ; en déclin (3,8 M$)")
        self.assertEqual(a["pic"], ("≈ 928 M$, 06/12/2017", "sourcé"))
        self.assertEqual(C.norm_rarete(a["rarete"]), "épique")
        self.assertTrue(a["etat"].startswith("en déclin"))
        b = C.analyse_correction("Pic / chaîne / rareté",
                                 "≈ 186 M$ en FDV (6 avr. 2024) / Solana `6D7N` / épique")
        self.assertEqual(b["pic"][1], "estimé")
        self.assertEqual(b["chaine"], "Solana")
        self.assertEqual(b["adresse"], "6D7N")
        d = C.analyse_correction("Pic", "ATH 0,00419 $ ; × 550 Md ≈ 2,3 Md$ (très douteux)")
        self.assertNotIn("pic", d)
        self.assertIn("pic_refuse", d)
        e = C.analyse_correction("Pic / rareté", "≈ 1,2 Md$ (estimation CoinGecko) ; légendaire")
        self.assertFalse(e["legende_histoire"])  # légendaire fondé sur un pic estimé
        t = C.analyse_correction("Pic / rareté", "≈ 0,99 Md$ (ATH × 69 Md, estimé) ; légendaire (mème culte)")
        self.assertTrue(t["legende_histoire"])

    def test_correction_r4_source_explicite(self):
        a = C.analyse_correction("Chaîne ; pic", "XRP Ledger ; ≈ 17,5 M$ (20 juil. 2025), sourcé (FDV CMC max ≈ 55 M$)")
        self.assertEqual(a["pic"][1], "sourcé")
        self.assertEqual(a["chaine"], "XRP Ledger")

    def test_borne_recente_ecarte_estimation_ancienne(self):
        c = C.Carte(nom="Hosky", ticker="HOSKY")
        c.ajoute_pic("≈ 368 M$ (estimé CG)", "estimé", 1)          # R5
        c.ajoute_pic("≥ 50 M$ (5 janv. 2025), sourcé", "sourcé", 5)  # r4, plus récent
        self.assertEqual(c.pic_retenu()[0], 50e6)

    def test_lot_sans_entete(self):
        ligne = ("| Invest Zone | IVFUN | Tron (SunPump) | 2024 | ≈ 42,6 M$ | estimé | mort | -99,7 % | "
                 "Histoire. | rare |  | https://www.coingecko.com/en/coins/invest-zone |\n"
                 "| 686 (Mooncoin) | Pic | inconnu | ≈ 179 M$ | https://x |\n")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(ligne)
        try:
            nouveaux, corr = C.lire_recherche(f.name, "extra")
        finally:
            os.unlink(f.name)
        self.assertEqual(len(nouveaux), 1)
        self.assertEqual(nouveaux[0]["ticker"], "IVFUN")
        self.assertEqual(corr[0]["num"], "686 (Mooncoin)")
        self.assertEqual(C.numeros_correction("669 / 11"), ["669", "11"])


class TestDedup(unittest.TestCase):
    def carte(self, nom, ticker, chaine="", lancement="", cg=()):
        c = C.Carte(nom=nom, ticker=ticker, cg_ids=list(cg))
        c.chaine, c.lancement = chaine, lancement
        return c

    def test_normalisation(self):
        self.assertEqual(C.nom_souple("Brett †"), "brett")
        self.assertEqual(C.nom_souple("Slerf [OLD]"), "slerf")
        self.assertEqual(C.nom_souple("Pépé Coin"), "pepe")
        self.assertEqual(C.norm_ticker("$TOAD"), "TOAD")
        self.assertEqual(C.norm_chaine("BSC"), "BNB Chain")
        self.assertEqual(C.norm_chaine("Dogecoin (blockchain propre)"), "blockchain propre")
        self.assertEqual(C.norm_chaine("à vérifier"), "")

    def test_meme_jeton(self):
        a = self.carte("Kabosu", "KABOSU", "Ethereum")
        self.assertTrue(C.meme_jeton(a, self.carte("Kabosu Inu", "KABOSU")))
        self.assertTrue(C.meme_jeton(a, self.carte("KABOSU (old)", "$KABOSU", "ETH")))
        self.assertFalse(C.meme_jeton(a, self.carte("Kabosu", "KABOSU", "Solana")))  # chaîne différente
        self.assertFalse(C.meme_jeton(self.carte("Hawk Tuah", "HAWK"), self.carte("Hawk", "HAWK")))

    def test_epoques_et_ids_distincts(self):
        self.assertFalse(C.meme_jeton(self.carte("Catcoin", "CAT", "", "nov. 2024"),
                                      self.carte("Catcoin (2013)", "CAT", "blockchain propre", "déc. 2013")))
        self.assertFalse(C.meme_jeton(self.carte("CatGPT", "CATGPT", cg=["catgpt"]),
                                      self.carte("CATGPT", "CATGPT", cg=["catgpt-3"])))
        self.assertTrue(C.meme_jeton(self.carte("X", "X", cg=["a"]), self.carte("Y", "Y", cg=["a"])))

    def test_parentheses_chaine_ne_font_pas_un_nom(self):
        self.assertFalse(C.homonyme(self.carte("Peepo (Solana)", "PEEP"), self.carte("GME (Solana)", "GME")))


class TestRarete(unittest.TestCase):
    R = staticmethod(C.rarete_v2)

    def test_pyramide(self):
        self.assertEqual(self.R(5e9, None, "actif", mythique=True), "mythique")
        self.assertEqual(self.R(2e9, 2e9, "en déclin"), "légendaire")       # sourcé ≥ 1 Md$
        self.assertEqual(self.R(3e9, None, "mort"), "épique")               # estimé ≥ 1 Md$ : plafonné
        self.assertEqual(self.R(3e9, 8e8, "mort"), "épique")                # borne sourcée < 1 Md$
        self.assertEqual(self.R(1.7e8, None, "mort", legende_histoire=True), "légendaire")
        self.assertEqual(self.R(2e8, None, "mort"), "épique")
        self.assertEqual(self.R(5e7, None, "en déclin"), "rare")
        self.assertEqual(self.R(5e7, None, "mort (absent de CoinGecko)"), "commune")  # mort < 100 M$
        self.assertEqual(self.R(5e6, None, "actif"), "commune")
        self.assertEqual(self.R(None, None, "actif"), "commune")

    def test_borne_basse_remplacee(self):
        c = C.Carte(nom="Turbo", ticker="TURBO")
        c.ajoute_pic("> 70 M$, mai 2023", "sourcé", 0)
        c.ajoute_pic("≈ 0,99 Md$ (estimé)", "estimé", 4)
        v, txt, nat, ms = c.pic_retenu()
        self.assertEqual((v, nat, ms), (0.99e9, "estimé", 70e6))
        self.assertIn("borne sourcée", txt)

    def test_priorite_sourcé(self):
        c = C.Carte(nom="A", ticker="A")
        c.ajoute_pic("≈ 50 M$", "sourcé", 0)
        c.ajoute_pic("≈ 40 M$", "estimé", 4)
        self.assertEqual(c.pic_retenu()[0], 50e6)
        c.ajoute_pic("≈ 60 M$", "sourcé", 3)  # sourcé plus récent
        self.assertEqual(c.pic_retenu()[0], 60e6)


class TestSurclassements(unittest.TestCase):
    def test_lecture_et_cible(self):
        txt = ("| Nom | Ticker | Rareté forcée | Raison | Source |\n|---|---|---|---|---|\n"
               "| Neiro (Ethereum) | NEIRO | légendaire | pic ≥ 1 Md$ largement rapporté | x |\n"
               "| Floki | FLOKI | légendaire | r | y |\n")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(txt)
        try:
            sc = C.lire_surclassements(f.name)
        finally:
            os.unlink(f.name)
        self.assertEqual([(s["nom"], s["chaine"], s["rarete"]) for s in sc],
                         [("Neiro", "Ethereum", "légendaire"), ("Floki", "", "légendaire")])
        eth = C.Carte(nom="Neiro †", ticker="NEIRO")
        eth.chaine = "Ethereum"
        sol = C.Carte(nom="Neiro", ticker="NEIRO")
        sol.chaine = "Solana"
        self.assertTrue(C.vise(sc[0], eth))
        self.assertFalse(C.vise(sc[0], sol))  # la chaîne restreint la cible

    def test_applique_en_dernier(self):
        c = C.Carte(nom="Floki", ticker="FLOKI")
        c.ajoute_pic("≥ 859 M$ (Etherscan)", "sourcé", 0)
        c.ajoute_pic("≈ 3,4 Md$ (estimé CG)", "estimé", 1)
        c.etat = "en déclin"
        sc = {"nom": "Floki", "ticker": "FLOKI", "chaine": "", "rarete": "légendaire", "raison": "r",
              "source": "s", "cartes": []}
        C.finaliser([c])
        self.assertEqual(c.rarete, "épique")  # sans surclassement : borne sourcée
        c2 = C.Carte(nom="Floki", ticker="FLOKI")
        c2.pics, c2.etat = list(c.pics), c.etat
        C.finaliser([c2], [sc])
        self.assertEqual(c2.rarete, "légendaire")
        self.assertFalse(c2.aberrant)
        self.assertEqual(sc["cartes"], [c2])


class TestPicsAberrants(unittest.TestCase):
    def test_estime_milliard_sans_source(self):
        # ShibaDoge : 12 769 Md$ estimé, aucune source -> pic inconnu -> commune
        self.assertEqual(C.rarete_carte(1.2769e13, "estimé", None, "en déclin"), ("commune", "aberrant"))
        self.assertEqual(C.rarete_carte(3.7e9, "estimé", None, "mort"), ("commune", "aberrant"))
        # sous 1 Md$ ou sourcé : règle normale
        self.assertEqual(C.rarete_carte(9.9e8, "estimé", None, "mort"), ("épique", ""))
        self.assertEqual(C.rarete_carte(3e9, "sourcé", 3e9, "mort"), ("légendaire", ""))

    def test_plancher_source(self):
        # Degen / Baby Doge : borne sourcée ≥ 100 M$ -> au moins épique
        self.assertEqual(C.rarete_carte(1.2e9, "estimé", 3.1e8, "en déclin"), ("épique", "plancher"))
        # LOBO : borne de 71 M$ -> rare si pas mort
        self.assertEqual(C.rarete_carte(3.59e9, "estimé", 7.1e7, "en déclin"), ("rare", "plancher"))
        # Bonk : borne ≥ 1 Md$ -> légendaire
        self.assertEqual(C.rarete_carte(5.1e9, "estimé", 2.6e9, "en déclin"), ("légendaire", "plancher"))

    def test_mention_affichee(self):
        c = C.Carte(nom="ShibaDoge", ticker="SHIBDOGE")
        c.ajoute_pic("≈ 12769,26 Md$ (estimé CG)", "estimé", 1)
        c.etat = "en déclin"
        C.finaliser([c])
        self.assertTrue(c.aberrant)
        self.assertEqual(c.rarete, "commune")
        self.assertIn("estimation aberrante, à vérifier", c.pic_txt)


class TestBout(unittest.TestCase):
    """Génération complète sur les vrais fichiers, dans un dossier temporaire."""

    def test_generation(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            C.main(["--out-dir", d])
            with open(os.path.join(d, "catalogue-v2.json"), encoding="utf-8") as f:
                data = json.load(f)
            with open(os.path.join(d, "catalogue-v2.md"), encoding="utf-8") as f:
                md = f.read()
        myth = [o for o in data if o["rarete"] == "mythique"]
        self.assertEqual(len(myth), 3)
        self.assertEqual(sorted(o["secret"]["ticker"] for o in myth), ["DOGE", "PEPE", "SHIB"])
        self.assertTrue(all(o["nom"] == "?" and o["visuel"] == "?" for o in myth))
        self.assertEqual(len({o["id"] for o in data}), len(data))
        self.assertTrue(all(o["burn"] == "à définir" for o in data))
        self.assertIn("3 mythiques scellés", md)
        self.assertNotIn("| Dogecoin | DOGE |", md)
        tick = {o["ticker"] for o in data if o["section"] == "catalogue"}
        self.assertNotIn("PUMP", tick)  # retrait R5
        self.assertNotIn("MEMETOON", {o["nom"] for o in data})
        par_tk = {}
        for o in data:
            if o["section"] == "catalogue":
                par_tk.setdefault(o["ticker"], []).append(o)
        for tk in ("FLOKI", "PNUT", "MEW", "NEIRO", "MEME"):
            surc = [o for o in par_tk[tk] if o["surclassement"]]
            self.assertEqual(len(surc), 1, tk)
            self.assertEqual(surc[0]["rarete"], "légendaire", tk)
        neiro = [o for o in par_tk["NEIRO"] if o["surclassement"]][0]
        self.assertEqual(neiro["chaine_normalisee"], "Ethereum")
        par_tk = {tk: v[0] for tk, v in par_tk.items()}
        self.assertEqual(par_tk["SHIBDOGE"]["rarete"], "commune")
        self.assertTrue(par_tk["SHIBDOGE"]["pic_aberrant"])
        self.assertEqual(par_tk["BABYDOGE"]["rarete"], "épique")
        self.assertIn("## Annexe 5 : pics aberrants", md)


if __name__ == "__main__":
    unittest.main()
