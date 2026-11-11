"""Liste des memecoins Intents (contract/scripts/intents_memes.py). Données fictives, aucun réseau."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import intents_memes as im  # noqa: E402


def tok(asset, sym, cg, addr, price=1.0, chain="near"):
    return {"assetId": asset, "symbol": sym, "coingeckoId": cg, "contractAddress": addr, "price": price,
            "blockchain": chain, "decimals": 18}


class MemesTest(unittest.TestCase):
    def test_rarity_rule(self):
        self.assertEqual(im.proposed_rarity(None, False)[0], "commune")
        self.assertEqual(im.proposed_rarity(5e9, False)[0], "épique")      # estimé seulement : pas légendaire
        self.assertEqual(im.proposed_rarity(2e8, True)[0], "épique")
        self.assertEqual(im.proposed_rarity(5e7, False)[0], "rare")
        self.assertEqual(im.proposed_rarity(5e7, True)[0], "commune")      # mort
        self.assertEqual(im.proposed_rarity(5e6, False)[0], "commune")

    def test_rows_catalogue_sealed_and_non_memes(self):
        memes = {"m1": {"peak_mcap_est": "50000000"}, "m2": {}, "sealed": {}, "inv": {}}
        v2 = [{"id": "carte-m2", "section": "catalogue", "rarete": "épique", "adresse": "m2.near", "coingecko_id": "m2"}]
        toks = [tok("a1", "M1", "m1", "m1.near"), tok("a2", "M2", "m2", "m2.near"),
                tok("a3", "M2", "m2", "Sol222", chain="sol"), tok("a4", "S", "sealed", "s.near"),
                tok("a5", "USDC", "usd-coin", "usdc.near"), tok("a6", "PONS", "inv", "p.near")]
        quotes = {"a1": {"ok": True}, "a2": {"ok": False, "erreur": "x"}, "a3": {"ok": True}}
        rs = im.rows(toks, v2, memes, quotes, ({"s.near"}, set()))
        self.assertEqual([r["asset_id"] for r in rs], ["a1", "a2", "a3"])   # scellée, stablecoin, PONS exclus
        by = {r["asset_id"]: r for r in rs}
        self.assertEqual(by["a1"]["rarete_retenue"], "rare")
        self.assertEqual(by["a3"]["catalogue_v2"]["rapprochement"], "id CoinGecko (autre chaîne)")
        s = im.summary(rs)
        self.assertEqual((s["épique"]["pieces"], s["épique"]["brulables"]), (1, 1))  # une pièce, deux chaînes
        self.assertEqual(s["rare"]["brulables"], 1)


if __name__ == "__main__":
    unittest.main()
