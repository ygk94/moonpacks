#!/usr/bin/env python3
"""Tous les memecoins de la liste 1Click /v0/tokens : chaîne, adresse, devis dry à 0,04 $, présence et rareté dans
docs/data/catalogue-v2.json, rareté proposée pour les absents. Ne change aucune série.

Usage (depuis la racine du dépôt) :
    python3 -I contract/scripts/intents_memes.py --tokens docs/data/intents-tokens-2026-11-12.json \
        --fetch-devis docs/data/intents-devis-memes-2026-11-12.json      # devis dry, aucun fonds engagé
    python3 -I contract/scripts/intents_memes.py --tokens docs/data/intents-tokens-2026-11-12.json \
        --devis docs/data/intents-devis-memes-2026-11-12.json --out docs/data/intents-memes-candidats.json

Memecoin : id CoinGecko de la catégorie meme (docs/data/coingecko-meme-2026-11-11.csv), ou jeton listé comme memecoin
dans docs/intents-couverture.md sans id de cette catégorie (MANUAL). Écartés comme non-memecoins : PONS (launchpad),
COCA (wallet) ; FMS et tMU, sans id CoinGecko ni source, ne sont pas retenus.

Présence dans le catalogue v2 : par adresse de contrat (règles de intents_brulables.norm_addr), sinon par id CoinGecko
(une même pièce sur une autre chaîne, ex. TURBO sur Solana). Rareté proposée pour un absent : règle du catalogue v2
(docs/catalogue-v2.md) appliquée au pic estimé de CoinGecko (`peak_mcap_est`) et à l'état (prix 1Click nul = mort) :
légendaire ≥ 1 Md$ seulement si le pic est sourcé, donc un pic seulement estimé ≥ 1 Md$ reste épique ; épique ≥ 100 M$ ;
rare 10 à 100 M$ et vivant ; commune sinon (pic inconnu compris).

Les actifs d'une carte scellée (docs/data/secrets/mythiques.json, ignoré par git) ne figurent pas dans la sortie :
une mythique n'est jamais brûlable. Sans ce fichier, le script refuse d'écrire (--sans-controle pour forcer).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import intents_brulables as ib  # noqa: E402

MANUAL = {"nep141:abg-966.meme-cooking.near", "nep141:gnear-229.meme-cooking.near",
          "nep141:noear-324.meme-cooking.near", "nep141:sol-bb27241c87aa401cc963c360c175dd7ca7035873.omft.near",
          "nep141:stjack.tkn.primitives.near"}
MANUAL_SYMBOLS = {"ABG", "GNEAR", "NOEAR", "LOUD", "STJACK"}
NOT_MEMES = {"PONS", "COCA"}
RARETES = ("légendaire", "épique", "rare", "commune")
DEVIS_USD = 0.04
SECRETS = os.path.join(REPO, "docs", "data", "secrets", "mythiques.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def meme_ids(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def is_meme(t, memes):
    if (t.get("symbol") or "") in NOT_MEMES:
        return False
    return t.get("coingeckoId") in memes or t["assetId"] in MANUAL or (t.get("symbol") or "") in MANUAL_SYMBOLS


def sealed(secrets_path):
    """Adresses et ids CoinGecko des cartes scellées (jamais écrits en sortie)."""
    if not os.path.exists(secrets_path):
        return None
    data = load(secrets_path)
    items = data.get("mythiques", data) if isinstance(data, dict) else data
    if isinstance(items, dict):
        items = list(items.values())
    return ({ib.norm_addr(e.get("adresse")) for e in items if e.get("adresse")},
            {e.get("coingecko_id") for e in items if e.get("coingecko_id") not in (None, "", "?")})


def proposed_rarity(peak, dead):
    if peak is None:
        return "commune", "pic inconnu"
    if peak >= 1e8:
        return "épique", f"pic estimé {peak / 1e6:,.0f} M$ (≥ 100 M$ ; ≥ 1 Md$ seulement estimé reste épique)".replace(",", " ")
    if peak >= 1e7 and not dead:
        return "rare", f"pic estimé {peak / 1e6:,.1f} M$, vivant".replace(",", " ")
    return "commune", f"pic estimé {peak / 1e6:,.2f} M${', mort' if dead else ''}".replace(",", " ")


def catalogue_index(v2):
    by_addr, by_cg = {}, {}
    for c in v2:
        for a in (c.get("adresse") or "").replace(";", ",").split(","):
            if a.strip():
                by_addr.setdefault(ib.norm_addr(a), c)
        if c.get("coingecko_id") not in (None, "", "?"):
            by_cg.setdefault(c["coingecko_id"], c)
    return by_addr, by_cg


def rows(tokens, v2, memes, quotes, sealed_sets):
    by_addr, by_cg = catalogue_index(v2)
    addrs, cgs = sealed_sets or (set(), set())
    out = []
    for t in tokens:
        if not is_meme(t, memes):
            continue
        a, g = ib.norm_addr(t.get("contractAddress")), t.get("coingeckoId")
        if (a and a in addrs) or (g and g in cgs):
            continue
        c, how = by_addr.get(a), "adresse"
        if c is None and g:
            c, how = by_cg.get(g), "id CoinGecko (autre chaîne)"
        q = (quotes or {}).get(t["assetId"])
        r = {"asset_id": t["assetId"], "symbol": t.get("symbol"), "blockchain": t["blockchain"],
             "contract_address": t.get("contractAddress"), "decimals": t.get("decimals"), "coingecko_id": g,
             "prix_usd_1click": t.get("price"),
             "devis_004": None if q is None else {k: q.get(k) for k in ("ok", "perte_pct", "erreur") if q.get(k) is not None}}
        if c is not None:
            r.update(catalogue_v2={"card_id": c["id"], "section": c.get("section"), "rarete": c["rarete"],
                                   "etat": c.get("etat"), "rapprochement": how})
            rar = c["rarete"]
            r["rarete_retenue"], r["source_rarete"] = rar, "catalogue v2" + (" (à décider)" if c.get("section") != "catalogue" else "")
        else:
            peak = memes.get(g, {}).get("peak_mcap_est") if g else None
            peak = float(peak) if peak not in (None, "") else None
            rar, why = proposed_rarity(peak, not t.get("price"))
            r.update(catalogue_v2=None, rarete_retenue=rar, source_rarete="proposée : " + why)
        r["brulable_possible"] = bool(q and q.get("ok")) and bool(t.get("price")) and r["rarete_retenue"] != "mythique"
        out.append(r)
    return out


def coin_key(r):
    c = r.get("catalogue_v2")
    return c["card_id"] if c else (r["coingecko_id"] or r["asset_id"])


def summary(rs):
    """Par rareté retenue : pièces (une carte = une pièce, quelle que soit la chaîne) et pièces brûlables."""
    s = {}
    for r in RARETES:
        coins = {coin_key(x) for x in rs if x["rarete_retenue"] == r}
        ok = {coin_key(x) for x in rs if x["rarete_retenue"] == r and x["brulable_possible"]}
        cat = {coin_key(x) for x in rs if x["rarete_retenue"] == r and x["brulable_possible"]
               and x.get("catalogue_v2") and x["catalogue_v2"]["section"] == "catalogue"}
        s[r] = {"pieces": len(coins), "brulables": len(ok), "brulables_au_catalogue": len(cat),
                "liste_brulables": sorted(ok)}
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--catalogue", default=os.path.join(REPO, "docs", "data", "catalogue-v2.json"))
    ap.add_argument("--memes", default=os.path.join(REPO, "docs", "data", "coingecko-meme-2026-11-11.csv"))
    ap.add_argument("--devis")
    ap.add_argument("--fetch-devis", metavar="FICHIER")
    ap.add_argument("--mythiques", default=SECRETS)
    ap.add_argument("--sans-controle", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    tokens, v2, memes = load(a.tokens), load(a.catalogue), meme_ids(a.memes)
    sealed_sets = sealed(a.mythiques)
    if sealed_sets is None and not a.sans_controle:
        raise SystemExit(f"{a.mythiques} absent : impossible d'exclure les cartes scellées (--sans-controle pour forcer)")
    near = next(t for t in tokens if t["assetId"] == "nep141:wrap.near")
    if a.fetch_devis:
        res = {"_doc": f"Devis 1Click dry: true à {DEVIS_USD} $ (aucun fonds engagé), wNEAR -> actif, INTENTS -> INTENTS. "
                       f"Cours wNEAR 1Click : {near['price']} $.",
               "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "devis": {}}
        for r in rows(tokens, v2, memes, None, sealed_sets):
            q = ib.quote(r["asset_id"], DEVIS_USD, near["price"])
            res["devis"][r["asset_id"]] = q
            print(r["symbol"], r["blockchain"], q.get("perte_pct", q.get("erreur")), flush=True)
            time.sleep(0.4)
        ib.dump(a.fetch_devis, res)
        return 0
    qd = load(a.devis) if a.devis else None
    rs = rows(tokens, v2, memes, qd["devis"] if qd else None, sealed_sets)
    rs.sort(key=lambda r: (RARETES.index(r["rarete_retenue"]) if r["rarete_retenue"] in RARETES else -1,
                           coin_key(r), r["blockchain"]))
    out = {"_doc": "Memecoins de 1Click /v0/tokens (hors cartes scellées), devis dry à 0,04 $, présence dans le "
                   "catalogue v2. Généré par contract/scripts/intents_memes.py : ne pas éditer à la main. Aucune "
                   "série n'est modifiée. Une pièce = une carte, quelle que soit la chaîne.",
           "tokens": os.path.relpath(os.path.abspath(a.tokens), REPO), "tokens_date": near.get("priceUpdatedAt"),
           "devis": os.path.relpath(os.path.abspath(a.devis), REPO) if a.devis else None,
           "devis_date": (qd or {}).get("date"), "resume": summary(rs), "actifs": rs}
    for r, s in out["resume"].items():
        print(f"{r:11} {s['brulables']:2} brûlables / {s['pieces']:2} pièces : {', '.join(s['liste_brulables'])}")
    if a.out:
        ib.dump(a.out, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
