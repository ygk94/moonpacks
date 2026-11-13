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

# Fichier secret (hors git). Sur un clone qui ne l'a pas, trois cartes v1 ordinaires jouent les mythiques :
# le chemin de code est le même, et aucun vrai nom n'est nécessaire.
SECRET = os.path.join(C.ROOT, "docs", "data", "secrets", "mythiques.json")
_FICTIF = tempfile.TemporaryDirectory()


def args_mythiques():
    if os.path.exists(SECRET):
        return ["--mythiques", SECRET]
    import json
    v1 = C.lire_v1(os.path.join(C.ROOT, "docs", "catalogue-final.md"))
    items = [{"ticker": v1[n].ticker, "origines": ["v1 n° %s" % n]} for n in ("7", "10", "12")]
    p = os.path.join(_FICTIF.name, "mythiques.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"mythiques": items}, f)
    return ["--mythiques", p]


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
            C.main(["--out-dir", d] + args_mythiques())
            with open(os.path.join(d, "catalogue-v2.json"), encoding="utf-8") as f:
                data = json.load(f)
            with open(os.path.join(d, "catalogue-v2.md"), encoding="utf-8") as f:
                md = f.read()
        myth = [o for o in data if o["rarete"] == "mythique"]
        self.assertEqual(len(myth), 3)
        self.assertTrue(all(o["nom"] == "?" and o["visuel"] == "?" for o in myth))
        self.assertEqual(len({o["id"] for o in data}), len(data))
        self.assertTrue(all(o["burn"] == "à définir" for o in data))
        self.assertIn("3 mythiques scellés", md)
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

    def test_secrets_hors_json_public(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            C.main(["--out-dir", d, "--demo"] + args_mythiques())
            chemin = os.path.join(d, "secrets", "mythiques.json")
            self.assertEqual(os.stat(chemin).st_mode & 0o777, 0o600)
            with open(chemin, encoding="utf-8") as f:
                secrets = json.load(f)["mythiques"]
            publics = {}
            for nom in ("catalogue-v2.json", "catalogue-demo.json", "catalogue-v2.md", "catalogue-demo.md"):
                with open(os.path.join(d, nom), encoding="utf-8") as f:
                    publics[nom] = f.read()
        # Les mythiques viennent du fichier secret : ni nom, ni ticker, ni empreinte dans le code suivi.
        attendu = C.charger_mythiques_v1(args_mythiques()[1])
        self.assertEqual(sorted(C.norm_ticker(m["ticker"]) for m in secrets),
                         sorted(C.norm_ticker(t) for t in attendu.values()))
        self.assertFalse(hasattr(C, "MYTHIQUES_V1") or hasattr(C, "empreinte_ticker"))
        self.assertEqual([m["id"] for m in secrets], ["mythique-m1", "mythique-m2", "mythique-m3"])
        self.assertNotIn("| (scellé) |", publics["catalogue-v2.md"])  # homonymes d'une mythique non listés
        for nom, texte in publics.items():
            self.assertNotIn('"secret"', texte, nom)
            for m in secrets:
                self.assertNotIn("| %s | %s |" % (m["nom"], m["ticker"]), texte, nom)
                if m["coingecko_id"]:
                    self.assertNotIn("`%s`" % m["coingecko_id"], texte, nom)
                    self.assertNotIn('"%s"' % m["coingecko_id"], texte, nom)
        for nom in ("catalogue-v2.json", "catalogue-demo.json"):
            for o in json.loads(publics[nom]):
                self.assertNotIn("secret", o)
                if o["rarete"] == "mythique":
                    self.assertTrue(all(o[k] in ("?", None, [], False) for k in C.CHAMPS_SECRET[2:]
                                        if k in o), o["id"])


class TestDemo(unittest.TestCase):
    def test_demo(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            C.main(["--out-dir", d, "--demo"] + args_mythiques())
            with open(os.path.join(d, "catalogue-demo.json"), encoding="utf-8") as f:
                demo = json.load(f)
            with open(os.path.join(d, "catalogue-v2.json"), encoding="utf-8") as f:
                v2 = {o["id"]: o for o in json.load(f)}
            with open(os.path.join(d, "catalogue-demo.md"), encoding="utf-8") as f:
                md = f.read()
        ids = [o["id"] for o in demo]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(o["section"] == "catalogue" for o in demo))
        rein = [o for o in demo if o["reintegree"]]
        self.assertEqual(rein, [])  # assez de matière : aucune exclue réintégrée
        for o in demo:
            self.assertEqual(o["section_v2"], "catalogue", o["id"])
            self.assertFalse(any(x in o["drapeau"] for x in C.DRAPEAUX_DEMO), o["id"])
            self.assertIsInstance(o["brulable_possible"], bool)
            self.assertTrue(o["raison_brulable"])
            self.assertEqual(o["numero"], v2[o["id"]]["numero"])
            if o["brulable_possible"]:
                self.assertFalse(o["etat"].startswith("mort"), o["id"])
                self.assertGreaterEqual(o["liquidite"]["volume_24h_usd"], 2e4)
                self.assertGreaterEqual(o["liquidite"]["capitalisation_usd"], 1e6)
        noms = {o["nom"] for o in demo}
        for exclu in ("HarryPotterObamaSonic10Inu", "HarryPotterTrumpHomerSimpson777Inu", "Official Trump"):
            self.assertNotIn(exclu, noms)
        myth = [o for o in demo if o["rarete"] == "mythique"]
        self.assertEqual(len(myth), 3)
        self.assertTrue(all(not o["brulable_possible"] and o["liquidite"] is None for o in myth))
        brul = [o for o in demo if o["brulable_possible"]]
        self.assertGreaterEqual(len(brul), C.MIN_BRULABLES)
        self.assertTrue(any(o["rarete"] in ("commune", "rare") for o in brul))
        self.assertIn("### Politiciens sans drapeau", md)

    def test_reintegration_par_paliers(self):
        def carte(nom, drap="", a_dec=False, cid="x"):
            c = C.Carte(nom=nom, ticker=nom.upper(), etat="actif", cg_ids=[cid], drapeaux=[drap] if drap else [],
                        a_decider=a_dec)
            c.rarete, c.numero, c.id = "commune", nom, nom
            return c
        cg = {"x": {"total_volume": "50000", "market_cap": "2000000"}}
        cat = [carte("propre"), carte("star", "personne réelle"), carte("sale", "obscène"),
               carte("escroc", "arnaque avérée"), carte("mort", cid="absent")]
        dec = [carte("suspens", a_dec=True)]
        demo = C.construire_demo(cat, dec, cg, min_brulables=3)
        # « mort » reste (sans drapeau) mais ne compte pas ; « star » puis « sale » comblent le manque.
        self.assertEqual([c.nom for c in demo["cartes"]], ["propre", "star", "sale", "mort"])
        self.assertEqual([c.brulable for c in demo["cartes"]], [True, True, True, False])
        self.assertTrue(demo["atteint"])
        demo = C.construire_demo(cat, dec, cg, min_brulables=10)
        self.assertNotIn("escroc", [c.nom for c in demo["cartes"]])  # jamais d'arnaque avérée
        self.assertIn("suspens", [c.nom for c in demo["cartes"]])
        self.assertFalse(demo["atteint"])


if __name__ == "__main__":
    unittest.main()
