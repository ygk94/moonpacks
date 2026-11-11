"""Rapprochement brûlables -> actifs NEAR Intents (contract/scripts/intents_brulables.py).

Lancement : python3 -m unittest discover -s contract/scripts/tests
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(SCRIPTS))
sys.path.insert(0, SCRIPTS)

import intents_brulables as ib  # noqa: E402

EVM = "0xA35923162C49cF95e6BF26623385eb431ad920D3"
SOL = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"


def card(cid, rarete="légendaire", adresse="", chaine="Ethereum", ticker="X", cg="x", brulable=True):
    return {"id": cid, "section": "catalogue", "rarete": rarete, "adresse": adresse, "chaine_normalisee": chaine,
            "ticker": ticker, "coingecko_id": cg, "nom": cid, "numero": "1", "brulable_possible": brulable}


def token(asset, chain, addr, symbol="X", cg="x", price=1.0, decimals=18):
    return {"assetId": asset, "blockchain": chain, "contractAddress": addr, "symbol": symbol, "coingeckoId": cg,
            "price": price, "decimals": decimals, "priceUpdatedAt": "2026-11-12T00:00:00Z"}


NEAR = token("nep141:wrap.near", "near", "wrap.near", "wNEAR", "wrapped-near", 3.6, 24)


class MatchTest(unittest.TestCase):
    def test_evm_address_case_insensitive_and_chain_preferred(self):
        toks = [token("sol-turbo", "sol", "2Dyzu65QA9zdX1UeE7Gx71k7fiwyUK6sZdrvJ7auq5wm"),
                token("near-turbo", "near", EVM.lower()[2:] + ".factory.bridge.near"),
                token("eth-turbo", "eth", EVM.lower(), decimals=18)]
        m = ib.match_card(card("turbo", adresse=EVM), toks)
        self.assertEqual(m["statut"], "reliée")
        self.assertEqual(m["asset_id"], "eth-turbo")
        self.assertEqual(m["decimals"], 18)

    def test_solana_address_is_case_sensitive(self):
        toks = [token("sol-wif", "sol", SOL.lower())]
        m = ib.match_card(card("wif", adresse=SOL, chaine="Solana"), toks)
        self.assertEqual(m["statut"], "écartée")
        m = ib.match_card(card("wif", adresse=SOL, chaine="Solana"), [token("sol-wif", "sol", SOL)])
        self.assertEqual(m["statut"], "reliée")

    def test_ticker_alone_never_matches(self):
        toks = [token("sol-wif", "sol", SOL, symbol="$WIF", cg="dogwifcoin")]
        m = ib.match_card(card("world-is-flat-wif", rarete="commune", ticker="WIF", cg="wif-flat"), toks)
        self.assertEqual(m["statut"], "écartée")
        self.assertIn("ticker seul", m["raison"])

    def test_coingecko_id_alone_never_matches(self):
        toks = [token("sol-wif", "sol", SOL, cg="dogwifcoin")]
        m = ib.match_card(card("wif", adresse="", chaine="Solana", cg="dogwifcoin"), toks)
        self.assertEqual(m["statut"], "écartée")
        self.assertIn("id CoinGecko seul", m["raison"])

    def test_same_evm_address_on_other_chain_is_rejected(self):
        toks = [token("base-x", "base", EVM.lower())]
        m = ib.match_card(card("x", adresse=EVM, chaine="Ethereum"), toks)
        self.assertEqual(m["statut"], "écartée")
        self.assertIn("pas sur la chaîne du catalogue", m["raison"])

    def test_unknown_chain_evm_needs_same_coingecko_id(self):
        toks = [token("bsc-x", "bsc", EVM.lower(), cg="autre")]
        self.assertEqual(ib.match_card(card("x", adresse=EVM, chaine="à vérifier", cg="x"), toks)["statut"], "écartée")
        toks = [token("bsc-x", "bsc", EVM.lower(), cg="x")]
        self.assertEqual(ib.match_card(card("x", adresse=EVM, chaine="à vérifier", cg="x"), toks)["statut"], "reliée")

    def test_near_account_address_overrides_wrong_catalogue_chain(self):
        toks = [token("nep141:kat.token0.near", "near", "kat.token0.near")]
        m = ib.match_card(card("nearkat", rarete="commune", adresse="kat.token0.near", chaine="Solana"), toks)
        self.assertEqual(m["statut"], "reliée")

    def test_zero_price_is_dead(self):
        toks = [token("nep141:abg.near", "near", "abg.near", price=0)]
        m = ib.match_card(card("abg", adresse="abg.near", chaine="NEAR"), toks)
        self.assertEqual(m["statut"], "écartée")


class QuotesTest(unittest.TestCase):
    def test_failed_quote_excludes(self):
        row = {"statut": "reliée", "asset_id": "a"}
        out = ib.apply_quotes(row, {"a": [{"usd": 0.04, "ok": True, "perte_pct": 0.5},
                                          {"usd": 4, "ok": False, "erreur": "HTTP 400 : No liquidity available"}]})
        self.assertEqual(out["statut"], "écartée")
        self.assertIn("4 $", out["raison"])
        self.assertEqual(ib.apply_quotes(row, {})["statut"], "écartée")
        ok = ib.apply_quotes(row, {"a": [{"usd": 1, "ok": True, "perte_pct": 0.3}]})
        self.assertEqual(ok["statut"], "reliée")

    def test_old_raw_error_keeps_message(self):
        row = {"statut": "reliée", "asset_id": "a"}
        out = ib.apply_quotes(row, {"a": [{"usd": 1, "ok": False, "erreur": '{"message":"No liquidity available","x":1}'}]})
        self.assertTrue(out["raison"].endswith("No liquidity available"))

    def test_mapping_summary_and_appoint(self):
        cat = [card("a", adresse=EVM), card("b", rarete="rare"),
               card("c", rarete="commune", adresse="c.near", chaine="NEAR", brulable=False),
               dict(card("m", rarete="mythique", adresse=EVM), brulable_possible=True)]
        toks = [NEAR, token("eth-a", "eth", EVM.lower()), token("near-c", "near", "c.near")]
        quotes = {"eth-a": [{"usd": 1, "ok": True}], "near-c": [{"usd": 1, "ok": True}]}
        m = ib.build_mapping(cat, toks, quotes, appoint=True)
        self.assertEqual(m["resume"]["légendaire"], {"brulables": 1, "reliees": 1, "ecartees": 0})
        self.assertEqual(m["resume"]["rare"], {"brulables": 1, "reliees": 0, "ecartees": 1})
        self.assertEqual([x["card_id"] for x in m["appoint"]], ["c"])
        self.assertNotIn("m", [x["card_id"] for x in m["reliees"] + m["ecartees"]])  # mythique ignorée


class CommittedMappingTest(unittest.TestCase):
    """Le fichier versionné se régénère à l'identique depuis les relevés versionnés."""

    def test_committed_mapping_is_reproducible(self):
        path = os.path.join(REPO, "docs", "data", "intents-brulables-demo.json")
        if not os.path.exists(path):
            self.skipTest("correspondance absente")
        with open(path, encoding="utf-8") as f:
            committed = json.load(f)
        with open(os.path.join(REPO, committed["catalogue"]), encoding="utf-8") as f:
            cat = json.load(f)
        with open(os.path.join(REPO, committed["tokens"]), encoding="utf-8") as f:
            toks = json.load(f)
        with open(os.path.join(REPO, committed["devis"]), encoding="utf-8") as f:
            quotes = json.load(f)["devis"]
        meta = {k: committed[k] for k in ("_doc", "catalogue", "tokens", "tokens_date", "devis", "devis_date")}
        again = ib.build_mapping(cat, toks, quotes, appoint="appoint" in committed, meta=meta)
        self.assertEqual(json.loads(json.dumps(again, ensure_ascii=False)), committed)
        for x in committed["reliees"]:
            self.assertTrue(x["asset_id"] and x["contract_address"] and isinstance(x["decimals"], int))
            self.assertEqual(ib.norm_addr(x["adresse_catalogue"]), ib.norm_addr(x["contract_address"]))


if __name__ == "__main__":
    unittest.main()
