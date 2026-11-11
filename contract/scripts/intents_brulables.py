#!/usr/bin/env python3
"""Relie les brûlables du catalogue de démo à de vrais actifs NEAR Intents, par adresse de contrat.

Usage (depuis la racine du dépôt) :
    # 1. relevé public des actifs (aucune clé) ; sans --tokens, le script le télécharge et l'écrit
    python3 -I contract/scripts/intents_brulables.py --fetch-tokens docs/data/intents-tokens-AAAA-MM-JJ.json
    # 2. devis dry (lecture publique, aucun fonds engagé) pour les actifs reliés, écrits dans un fichier
    python3 -I contract/scripts/intents_brulables.py --tokens docs/data/intents-tokens-AAAA-MM-JJ.json \
        --fetch-devis docs/data/intents-devis-demo-AAAA-MM-JJ.json
    # 3. correspondance, reproductible hors ligne à partir des deux relevés
    python3 -I contract/scripts/intents_brulables.py --tokens docs/data/intents-tokens-AAAA-MM-JJ.json \
        --devis docs/data/intents-devis-demo-AAAA-MM-JJ.json --out docs/data/intents-brulables-demo.json

Règles (testées dans contract/scripts/tests/test_intents_brulables.py) :
- Rapprochement **par adresse de contrat uniquement** : `adresse` du catalogue = `contractAddress` de 1Click
  (adresses EVM 0x… comparées en minuscules, les autres à l'identique : Solana est sensible à la casse).
  Le ticker et l'id CoinGecko ne servent qu'à signaler un candidat écarté (« ticker seul », « id CoinGecko seul »).
- Chaîne : une adresse de compte NEAR (« ….near ») vaut chaîne NEAR (le catalogue se trompe parfois de chaîne).
  Sinon, si la chaîne du catalogue est connue, l'actif doit être sur cette chaîne (une même adresse EVM peut
  désigner un autre jeton sur une autre chaîne). Si elle est « à vérifier », l'adresse EVM doit en plus avoir le même
  id CoinGecko des deux côtés.
- Plusieurs actifs pour une carte (ex. jeton présent sur plusieurs chaînes) : celui de la chaîne du catalogue.
- Une carte reliée doit avoir un prix 1Click > 0 et, si des devis sont fournis, tous ses devis dry réussis. Sinon elle
  est **écartée** et redevient une carte de collection pour la démo, avec sa raison.
- `--appoint` : liste aussi les communes et rares du catalogue **non** marquées brûlables dont l'adresse correspond à un
  actif coté (candidates « d'appoint », voir docs/series-demo.md). Elles ne sont pas reliées d'office.

Bibliothèque standard uniquement. Aucun secret : ni clé, ni nom de mythique (les mythiques sont ignorées).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TOKENS_URL = "https://1click.chaindefuser.com/v0/tokens"
QUOTE_URL = "https://1click.chaindefuser.com/v0/quote"
# Cloudflare refuse l'en-tête User-Agent par défaut de Python (erreur 1010) : en-tête générique explicite.
HEADERS = {"content-type": "application/json", "user-agent": "curl/8.7.1", "accept": "*/*"}
# Compte public servant seulement à valider la forme des devis dry (même valeur que docs/devis-intents.py).
DRY_ACCOUNT = "memaster-test.near"
# Montants des devis, en dollars : bas et haut d'une part de valeur d'un pack d'entrée (20 % à 200 % de 0,20 $),
# haut d'un pack standard (200 % de 0,50 $) et gros gold pack (8 × 0,50 $).
DEFAULT_DEVIS_USD = (0.04, 0.40, 1.0, 4.0)

# chaine_normalisee du catalogue -> blockchain de 1Click
CHAIN = {
    "Ethereum": "eth", "Solana": "sol", "Base": "base", "BNB Chain": "bsc", "Arbitrum": "arb",
    "Avalanche": "avax", "Polygon": "pol", "Robinhood Chain": "hood", "NEAR": "near", "TON": "ton",
    "Tron": "tron", "Sui": "sui", "Aptos": "aptos", "Cardano": "cardano", "Xrp Ledger": "xrp",
    "Berachain": "bera", "Monad": "monad", "Abstract": "abs", "Bitcoin": "btc", "Optimism": "op",
    "Gnosis": "gnosis", "Starknet": "starknet", "Scroll": "scroll", "Stellar": "stellar",
}
UNKNOWN_CHAINS = {"", "?", "à vérifier"}
EVM = re.compile(r"^0x[0-9a-fA-F]{40}$")
RARETES = ("légendaire", "épique", "rare", "commune")


def norm_addr(a: str | None) -> str:
    a = (a or "").strip()
    return a.lower() if EVM.match(a) else a


NEAR_ACCOUNT = re.compile(r"^[a-z0-9_.-]+\.near$")


def intents_chain(card: dict) -> str | None:
    """Chaîne 1Click attendue pour la carte, None si inconnue (ou multiple, « A, B »). Une adresse qui est un
    compte NEAR (« ….near ») désigne sans ambiguïté la chaîne NEAR, quelle que soit la chaîne du catalogue."""
    if NEAR_ACCOUNT.match((card.get("adresse") or "").strip()):
        return "near"
    c = (card.get("chaine_normalisee") or "").strip()
    if c in UNKNOWN_CHAINS or "," in c:
        return None
    return CHAIN.get(c, "?" + c)


def http_json(url, body=None, timeout=40):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data, HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def match_card(card: dict, tokens: list[dict]) -> dict:
    """Actif Intents d'une carte, ou raison de l'écart. Ne cote rien (voir apply_quotes)."""
    addr = norm_addr(card.get("adresse"))
    want = intents_chain(card)
    by_addr = [t for t in tokens if addr and norm_addr(t.get("contractAddress")) == addr]
    hint = []
    if not by_addr:
        cg = card.get("coingecko_id")
        if cg and cg != "?" and any(t.get("coingeckoId") == cg for t in tokens):
            hint.append("id CoinGecko seul")
        tick = (card.get("ticker") or "").upper().lstrip("$")
        if tick and any((t.get("symbol") or "").upper().lstrip("$") == tick for t in tokens):
            hint.append("ticker seul")
        reason = "adresse de contrat absente du catalogue" if not addr else "adresse absente de la liste 1Click"
        if hint:
            reason += f" (homonyme Intents par {' et '.join(hint)}, non retenu)"
        else:
            reason += " ; aucun actif 1Click de même id CoinGecko ni de même ticker"
        return {"statut": "écartée", "raison": reason}
    if want is not None:
        same = [t for t in by_addr if t["blockchain"] == want]
        if not same:
            return {"statut": "écartée",
                    "raison": f"adresse trouvée sur {', '.join(sorted({t['blockchain'] for t in by_addr}))}, "
                              f"pas sur la chaîne du catalogue ({card.get('chaine_normalisee')})"}
        chosen = same[0]
    else:
        cg = card.get("coingecko_id")
        ok = [t for t in by_addr if not EVM.match(addr) or (cg and t.get("coingeckoId") == cg)]
        if not ok:
            return {"statut": "écartée",
                    "raison": "chaîne du catalogue inconnue et adresse EVM sans id CoinGecko commun (risque d'homonymie entre chaînes)"}
        chosen = ok[0]
    autres = [t["assetId"] for t in by_addr if t is not chosen]
    out = {
        "statut": "reliée",
        "asset_id": chosen["assetId"],
        "blockchain": chosen["blockchain"],
        "contract_address": chosen.get("contractAddress"),
        "decimals": int(chosen["decimals"]),
        "symbol": chosen.get("symbol"),
        "coingecko_id_intents": chosen.get("coingeckoId"),
        "prix_usd_1click": chosen.get("price"),
        "prix_date_1click": chosen.get("priceUpdatedAt"),
    }
    if autres:
        out["autres_actifs_meme_adresse"] = autres
    if not chosen.get("price"):
        out.update(statut="écartée", raison="actif listé avec un prix nul (jeton mort)")
    return out


def quote(asset_id, usd, near_price, deadline=None):
    """Devis 1Click `dry: true`, wNEAR -> actif, INTENTS -> INTENTS. Aucun fonds engagé."""
    amount = str(int(usd / near_price * 10 ** 24))
    deadline = deadline or (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
                            ).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = {"dry": True, "swapType": "EXACT_INPUT", "slippageTolerance": 100, "originAsset": "nep141:wrap.near",
            "depositType": "INTENTS", "destinationAsset": asset_id, "amount": amount, "refundTo": DRY_ACCOUNT,
            "refundType": "INTENTS", "recipient": DRY_ACCOUNT, "recipientType": "INTENTS", "deadline": deadline}
    try:
        q = http_json(QUOTE_URL, body)["quote"]
        out_usd = float(q.get("amountOutUsd") or 0)
        return {"usd": usd, "ok": out_usd > 0, "amount_in": amount, "amount_out": q.get("amountOut"),
                "usd_out": out_usd, "perte_pct": round((1 - out_usd / usd) * 100, 2)}
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            msg = json.loads(raw).get("message") or raw
        except ValueError:
            msg = raw
        return {"usd": usd, "ok": False, "erreur": f"HTTP {e.code} : {str(msg)[:200]}"}
    except Exception as e:  # réseau
        return {"usd": usd, "ok": False, "erreur": str(e)[:200]}


def apply_quotes(row: dict, quotes: dict | None) -> dict:
    """Écarte une carte reliée dont un devis a échoué (pas de liquidité, montant trop bas…)."""
    if row["statut"] != "reliée" or quotes is None:
        return row
    qs = quotes.get(row["asset_id"])
    if qs is None:
        return dict(row, statut="écartée", raison="aucun devis dry pour cet actif")
    row = dict(row, devis=[{k: q.get(k) for k in ("usd", "ok", "perte_pct", "erreur") if q.get(k) is not None}
                           for q in qs])
    bad = [q for q in qs if not q.get("ok")]
    if bad:
        err = (bad[0].get("erreur") or "valeur reçue nulle").replace("\n", " ")
        if err.startswith("{"):  # relevé brut d'une ancienne version : on garde le message
            try:
                err = json.loads(err).get("message") or err
            except ValueError:
                pass
        row.update(statut="écartée", raison=f"devis dry en échec à {', '.join('%g $' % q['usd'] for q in bad)} : {err}")
    return row


def public_fields(card):
    return {"card_id": card["id"], "numero": card.get("numero"), "nom": card.get("nom"), "ticker": card.get("ticker"),
            "rarete": card["rarete"], "chaine_catalogue": card.get("chaine_normalisee"),
            "adresse_catalogue": card.get("adresse") or None, "coingecko_id": card.get("coingecko_id")}


def build_mapping(catalogue, tokens, quotes=None, appoint=False, meta=None):
    cards = [c for c in catalogue if c.get("section") == "catalogue" and c.get("rarete") != "mythique"]
    rows, extra = [], []
    for c in cards:
        if c.get("brulable_possible"):
            rows.append(dict(public_fields(c), **apply_quotes(match_card(c, tokens), quotes)))
        elif appoint and c["rarete"] in ("commune", "rare") and c.get("adresse"):
            m = apply_quotes(match_card(c, tokens), quotes)
            if m.get("asset_id") or m["statut"] == "reliée":
                extra.append(dict(public_fields(c), raison_catalogue=c.get("raison_brulable"), **m))
    summary = {r: {"brulables": sum(1 for x in rows if x["rarete"] == r),
                   "reliees": sum(1 for x in rows if x["rarete"] == r and x["statut"] == "reliée")}
               for r in RARETES}
    for r in RARETES:
        summary[r]["ecartees"] = summary[r]["brulables"] - summary[r]["reliees"]
    out = dict(meta or {})
    out.update({
        "resume": summary,
        "reliees": [x for x in rows if x["statut"] == "reliée"],
        "ecartees": [x for x in rows if x["statut"] != "reliée"],
    })
    if appoint:
        out["appoint"] = extra
    return out


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--catalogue", default=os.path.join(REPO, "docs", "data", "catalogue-demo.json"))
    ap.add_argument("--tokens", help="relevé /v0/tokens (JSON)")
    ap.add_argument("--fetch-tokens", metavar="FICHIER", help="télécharge /v0/tokens dans FICHIER, puis s'arrête")
    ap.add_argument("--devis", help="devis dry déjà relevés ({asset_id: [devis…]})")
    ap.add_argument("--fetch-devis", metavar="FICHIER",
                    help="relève les devis dry des actifs reliés (et d'appoint) dans FICHIER, puis s'arrête")
    ap.add_argument("--devis-usd", default=",".join(f"{x:g}" for x in DEFAULT_DEVIS_USD))
    ap.add_argument("--appoint", action="store_true", help="liste les communes et rares d'appoint")
    ap.add_argument("--out", help="correspondance (JSON) ; sans --out, résumé seulement")
    a = ap.parse_args(argv)

    if a.fetch_tokens:
        tokens = http_json(TOKENS_URL)
        dump(a.fetch_tokens, tokens)
        print(f"{len(tokens)} actifs -> {a.fetch_tokens}")
        return 0
    if not a.tokens:
        ap.error("--tokens requis (ou --fetch-tokens)")
    tokens = load(a.tokens)
    catalogue = load(a.catalogue)
    near = next(t for t in tokens if t["assetId"] == "nep141:wrap.near")

    if a.fetch_devis:
        m = build_mapping(catalogue, tokens, None, appoint=True)
        assets = sorted({x["asset_id"] for x in m["reliees"] + m["appoint"] if x.get("asset_id")})
        usds = [float(x) for x in a.devis_usd.split(",")]
        res = {"_doc": "Devis 1Click dry: true (aucun fonds engagé), wNEAR -> actif, INTENTS -> INTENTS, "
                       f"slippage 1 %. Cours wNEAR 1Click : {near['price']} $ ({near.get('priceUpdatedAt')}).",
               "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "near_usd": near["price"], "devis": {}}
        for asset in assets:
            res["devis"][asset] = []
            for usd in usds:
                res["devis"][asset].append(quote(asset, usd, near["price"]))
                time.sleep(0.4)
            print(asset, [q.get("perte_pct", (q.get("erreur") or "")[:50]) for q in res["devis"][asset]], flush=True)
        dump(a.fetch_devis, res)
        return 0

    quotes_doc = load(a.devis) if a.devis else None
    meta = {
        "_doc": "Correspondance brûlables du catalogue de démo -> actifs NEAR Intents (1Click /v0/tokens), par adresse "
                "de contrat. Généré par contract/scripts/intents_brulables.py : ne pas éditer à la main. Écartées = "
                "cartes de collection pour la démo. Aucun secret.",
        "catalogue": os.path.relpath(os.path.abspath(a.catalogue), REPO),
        "tokens": os.path.relpath(os.path.abspath(a.tokens), REPO),
        "tokens_date": near.get("priceUpdatedAt"),
        "devis": os.path.relpath(os.path.abspath(a.devis), REPO) if a.devis else None,
        "devis_date": (quotes_doc or {}).get("date"),
    }
    m = build_mapping(catalogue, tokens, (quotes_doc or {}).get("devis") if quotes_doc else None,
                      appoint=a.appoint, meta=meta)
    for r, s in m["resume"].items():
        print(f"{r:11} {s['reliees']:3} reliées / {s['brulables']:3} brûlables ({s['ecartees']} écartées)")
    for x in m["reliees"]:
        print(f"  + {x['card_id']} ({x['rarete']}) -> {x['asset_id']}")
    for x in m.get("appoint", []):
        print(f"  appoint {x['card_id']} ({x['rarete']}) -> {x.get('asset_id')} : {x['statut']} {x.get('raison', '')}")
    if a.out:
        dump(a.out, m)
        print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
