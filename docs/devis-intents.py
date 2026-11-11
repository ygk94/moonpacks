"""Devis dry 1Click pour chaque memecoin d'Intents : wNEAR -> token, à 1, 10, 100, 1000 $.
Usage : curl -s https://1click.chaindefuser.com/v0/tokens -o t.json && python3 -I docs/devis-intents.py t.json sortie.json
Aucun fonds engagé : devis dry=True uniquement. Les adresses de destination servent seulement à la validation du devis."""
import json, sys, time, urllib.request, datetime

API = "https://1click.chaindefuser.com/v0/quote"
MEMES = {"PEPE", "SHIB", "SPX", "MOG", "TURBO", "BRETT", "$WIF", "BOME", "PENGU", "TRUMP", "MELANIA", "LOUD",
         "NEARKAT", "NearKat", "wNEARKAT", "BLACKDRAGON", "SHITZU", "ABG", "GNEAR", "JAMBO", "NOEAR", "PURGE",
         "CASHCAT", "STJACK", "PONS", "DOGE", "COCA"}
DEST = {"eth": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e", "base": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "hood": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e", "aptos": None, "doge": None,
        "sol": "So11111111111111111111111111111111111111112", "near": "memaster-test.near"}
NEAR_PRICE = None
ACCOUNT = "memaster-test.near"


def quote(asset, usd, dest_chain=None):
    amount = str(int(usd / NEAR_PRICE * 1e24))
    deadline = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = {"dry": True, "swapType": "EXACT_INPUT", "slippageTolerance": 100, "originAsset": "nep141:wrap.near",
            "depositType": "INTENTS", "destinationAsset": asset, "amount": amount, "refundTo": ACCOUNT,
            "refundType": "INTENTS", "recipient": ACCOUNT, "recipientType": "INTENTS", "deadline": deadline}
    if dest_chain:
        body["recipient"] = DEST[dest_chain]
        body["recipientType"] = "DESTINATION_CHAIN"
    req = urllib.request.Request(API, json.dumps(body).encode(), {"content-type": "application/json", "user-agent": "curl/8.7.1", "accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            q = json.load(r)["quote"]
            out = float(q.get("amountOutUsd") or 0)
            return {"usd_out": out, "perte_pct": round((1 - out / usd) * 100, 2), "withdrawFee": q.get("withdrawFee"),
                    "temps_s": q.get("timeEstimate")}
    except urllib.error.HTTPError as e:
        return {"erreur": e.read().decode()[:200]}
    except Exception as e:
        return {"erreur": str(e)[:200]}


def main():
    global NEAR_PRICE
    tokens = json.load(open(sys.argv[1]))
    NEAR_PRICE = next(t["price"] for t in tokens if t["assetId"] == "nep141:wrap.near")
    res = []
    for t in tokens:
        if t["symbol"] not in MEMES:
            continue
        ligne = {k: t.get(k) for k in ("symbol", "blockchain", "assetId", "price", "coingeckoId", "contractAddress")}
        for usd in (1, 10, 100, 1000):
            ligne[f"q{usd}"] = quote(t["assetId"], usd)
            time.sleep(0.4)
        if DEST.get(t["blockchain"]) and t["blockchain"] != "near":
            ligne["retrait10"] = quote(t["assetId"], 10, t["blockchain"])
        res.append(ligne)
        print(t["symbol"], t["blockchain"], {k: v.get("perte_pct", v.get("erreur", "")[:60]) for k, v in ligne.items() if isinstance(v, dict)}, flush=True)
    json.dump(res, open(sys.argv[2], "w"), indent=1)


main()
