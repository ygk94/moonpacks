#!/usr/bin/env python3
"""Construit les séries du contrat v4 (types de packs) à partir des séries publiques de app3.

Usage (depuis contract/) :
    python3 scripts/build_v4.py [--source app3.memaster-demo-j7xg7z.testnet] [--out series-v4]
        [--catalog ../front/public/catalog.json] [--media-base https://moonpacks-ochre.vercel.app/cards]

Aucun secret n'est nécessaire : les mythiques sont reprises **telles quelles** de app3 (engagements publics,
mêmes sels), donc le fichier de secrets existant de Hugo (scripts/secrets/serie-demo-entree.json et
-standard.json) suffit pour les révéler. Les tables source sont relues sur la chaîne, et leur hash recalculé
(verifier/canon.py) doit être celui enregistré à l'ouverture : on part exactement de ce qui est déployé.

Changements par rapport à app3 :
- noms « Moonpacks Classic » (série 0, ex-Entry) et « Moonpacks Full Moon » (série 1, ex-Standard) ;
- `media` de chaque carte : visuel servi par le site (`--media-base`/<card_id>.svg), au lieu du CID IPFS jamais
  envoyé ;
- série 0 : les 9 types de packs de la boutique (`kinds`), cartes de chaque type d'après les filtres de
  front/src/lib/packTypes.ts, appliqués à front/public/catalog.json (npm run prepare-assets) ;
- série 0 : poids 4 pour les trois brûlables communes sans plafond (black-dragon, jambo, nearkat), pour qu'un
  pack Dog de 8 cartes ait une brûlable une fois sur trois (voir docs/front/packs-thematiques.md).

Sorties dans --out/classic et --out/full-moon (versionnées, sans secret), au format de build_series.py :
create_series_batched.json, append_series_cards.NN.json, open_series.json, table.json, table_hash.txt,
manifest.json (dépôts compris). deploy_testnet.sh les charge avec PREBUILT=1.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.dirname(HERE)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, os.path.join(REPO, "verifier"))
sys.path.insert(0, HERE)

from memaster_verifier import canon, core  # noqa: E402
import build_series  # noqa: E402
import validate_series  # noqa: E402

RPC = "https://rpc.testnet.fastnear.com"

# Filtres de front/src/lib/packTypes.ts (mêmes expressions ; re.ASCII pour les \b de JavaScript).
DOG = re.compile(r"dog|shib|\binu\b|inu\b|bonk|floki|\bwif\b|puppy|corgi|pup\b", re.ASCII)
CAT = re.compile(r"\bcat|cat\b|kitty|kitten|popcat|\bmew\b|meow|neko|\bnyan", re.ASCII)
FROG = re.compile(r"pepe|frog|toad|ribbit|\bkek\b", re.ASCII)
OG_ERA = "2013-2018"

# Brûlables communes sans plafond de app3, alourdies pour le pack Dog (1 pack sur 3 avec une brûlable).
DOG_BURNABLES = ["black-dragon-blackdragon", "jambo-meme-cooking-jambo", "nearkat-nearkat"]
DOG_BURNABLE_WEIGHT = 4

NEAR = 10 ** 24


def milli(near_thousandths: int) -> str:
    """Prix en millièmes de NEAR → yoctoNEAR."""
    return str(near_thousandths * 10 ** 21)


def view(contract: str, method: str, args: dict):
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "query",
        "params": {"request_type": "call_function", "finality": "final", "account_id": contract,
                   "method_name": method, "args_base64": base64.b64encode(json.dumps(args).encode()).decode()},
    }).encode()
    req = urllib.request.Request(RPC, body, {"content-type": "application/json", "user-agent": "memaster-build-v4"})
    r = json.load(urllib.request.urlopen(req, timeout=60))
    if "error" in r or "result" not in r.get("result", {}):
        raise SystemExit(f"RPC {method} : {r}")
    return json.loads(bytes(r["result"]["result"]))


def fetch_table(contract: str, sid: int) -> dict:
    """Table complète d'une série ouverte, vérifiée contre son hash enregistré."""
    h = view(contract, "get_series_header", {"series_id": sid})
    cards = []
    for f in range(0, h["card_count"], 200):
        cards += view(contract, "get_series_cards", {"series_id": sid, "from_index": f, "limit": 200})
    table = dict(h["header"], cards=cards)
    got = core.table_hash(table).hex()
    if got != h["table_hash"]:
        raise SystemExit(f"série {sid} : hash recalculé {got} ≠ hash enregistré {h['table_hash']}")
    return table


def text(e: dict) -> str:
    return f"{e['name']} {e['ticker']}".lower()


def pool_of(table: dict, catalog: dict, match) -> list[int]:
    return [i for i, c in enumerate(table["cards"]) if c["card_id"] in catalog and match(catalog[c["card_id"]])]


def slot(floor="common", burnable=False):
    return {"floor": floor, "weights": None, "burnable": burnable}


def kinds_for(table: dict, catalog: dict) -> list[dict]:
    """Les 9 types de packs de la boutique, règles de docs/front/packs-thematiques.md."""
    by_id = {c["card_id"]: i for i, c in enumerate(table["cards"])}
    dog = sorted(set(pool_of(table, catalog, lambda e: DOG.search(text(e)) and not CAT.search(text(e))))
                 | {by_id[b] for b in DOG_BURNABLES})
    cat = pool_of(table, catalog, lambda e: CAT.search(text(e)))
    frog = pool_of(table, catalog, lambda e: FROG.search(text(e)))
    sol = pool_of(table, catalog, lambda e: e["chain"] == "Solana")
    bnb = pool_of(table, catalog, lambda e: e["chain"] == "BNB Chain")
    eth = pool_of(table, catalog, lambda e: e["chain"] == "Ethereum")
    og = pool_of(table, catalog, lambda e: e.get("era") == OG_ERA)

    def unlimited_burnable(pool):
        return any(table["cards"][i]["backing"] and table["cards"][i]["cap"] is None and table["cards"][i]["weight"] > 0
                   for i in pool)

    def kind(name, price, n, pool, mythics=False, slots=None, value=False):
        return {"name": name, "price": price, "cards_per_pack": n, "pool": pool, "mythics": mythics,
                "slots": slots, "value": value}

    # Solana et Ethereum : une carte parmi les brûlables, et la valeur du pack, seulement si le pool contient
    # une brûlable sans plafond (règle du contrat : la brûlable garantie doit toujours exister).
    sol_burn = unlimited_burnable(sol)
    eth_burn = unlimited_burnable(eth)
    return [
        kind("Dog", milli(88), 8, dog),
        kind("Cat", milli(66), 5, cat, slots=[slot(), slot(), slot(), slot(), slot("rare")]),
        kind("Frog", milli(40), 3, frog, slots=[slot(), slot(), slot("rare")]),
        kind("Solana", milli(83), 5, sol, mythics=True,
             slots=[slot("epic"), slot(), slot(), slot(), slot(burnable=sol_burn)], value=sol_burn),
        kind("BNB Chain", milli(110), 10, bnb),
        kind("Ethereum", milli(66), 3, eth, slots=[slot("epic"), slot(), slot(burnable=eth_burn)], value=eth_burn),
        kind("OG 1", milli(11), 1, og),
        kind("OG 2", milli(22), 2, og),
        kind("OG 5", milli(55), 5, og),
    ]


def dog_burnable_chance(table: dict, kind: dict) -> float:
    """Probabilité qu'un pack Dog ait au moins une brûlable (poids de base, sans plafond atteint)."""
    w = table["rarity_weights"]
    tot = sum(w[r] for r in core.RARITIES if r != "mythic") or 1
    pool = set(kind["pool"])
    per_card = 0.0
    for r in ("legendary", "epic", "rare", "common"):
        cards = [c for i, c in enumerate(table["cards"]) if i in pool and c["rarity"] == r]
        s = sum(c["weight"] for c in cards)
        if s:
            per_card += w[r] / tot * sum(c["weight"] for c in cards if c["backing"]) / s
    return 1 - (1 - per_card) ** kind["cards_per_pack"]


def write_series(table: dict, out: str, sid: int) -> dict:
    """Arguments des appels de chargement, comme build_series.py (mêmes lots, mêmes dépôts)."""
    check = validate_series.validate_table(table)
    if not check.ok:
        raise SystemExit(f"table refusée :\n- " + "\n- ".join(check.errors))
    table_bytes = canon.table_json_bytes(table)
    assert json.loads(table_bytes) == table
    h = core.table_hash(table).hex()
    batch = build_series.MAX_CARDS_PER_CALL
    lots = [table["cards"][i:i + batch] for i in range(0, len(table["cards"]), batch)]
    os.makedirs(out, exist_ok=True)
    for name in os.listdir(out):
        os.remove(os.path.join(out, name))
    files = {"create_series_batched.json": {"table": dict(table, cards=lots[0])}}
    for i, lot in enumerate(lots[1:], start=1):
        files[f"append_series_cards.{i:02d}.json"] = {"series_id": sid, "cards": lot}
    files["open_series.json"] = {"series_id": sid}
    deposits, first_index = {}, 0
    for name, obj in files.items():
        build_series.write_json(os.path.join(out, name), obj)
        size = os.path.getsize(os.path.join(out, name))
        if name == "open_series.json":
            deposits[name] = "0"
            continue
        cards = obj["table"]["cards"] if "table" in obj else obj["cards"]
        bound = build_series.storage_bound(size, first_index, len(cards), name.startswith("create_series_batched"))
        deposits[name] = str(-(-bound * build_series.STORAGE_BYTE_COST // 10 ** 21) * 10 ** 21)
        first_index += len(cards)
    with open(os.path.join(out, "table.json"), "wb") as f:
        f.write(table_bytes)
    with open(os.path.join(out, "table_hash.txt"), "w") as f:
        f.write(h + "\n")
    manifest = {
        "table_hash": h,
        "table_bytes": len(table_bytes),
        "cards": len(table["cards"]),
        "per_rarity": {r: sum(1 for c in table["cards"] if c["rarity"] == r) for r in core.RARITIES[1:]} | {"mythic": len(table["mythics"])},
        "burnable_cards": sum(1 for c in table["cards"] if c["backing"]),
        "calls": list(files),
        "deposits": deposits,
        "deposit_total_near": f"{sum(int(d) for d in deposits.values()) / NEAR:.3f}",
        "kinds": [
            {"kind": i, "name": k["name"], "price_near": int(k["price"]) / NEAR, "cards_per_pack": k["cards_per_pack"],
             "pool": len(k["pool"]) or len(table["cards"]), "mythics": k["mythics"], "value": k["value"],
             "slots": k["slots"]}
            for i, k in enumerate(table.get("kinds") or [])
        ],
    }
    build_series.write_json(os.path.join(out, "manifest.json"), manifest)
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--source", default="app3.memaster-demo-j7xg7z.testnet")
    ap.add_argument("--out", default=os.path.join(CONTRACT, "series-v4"))
    ap.add_argument("--catalog", default=os.path.join(REPO, "front", "public", "catalog.json"))
    ap.add_argument("--media-base", default="https://moonpacks-ochre.vercel.app/cards")
    a = ap.parse_args(argv)
    if not os.path.exists(a.catalog):
        raise SystemExit(f"{a.catalog} absent : lancer d'abord `cd front && npm run prepare-assets`")
    with open(a.catalog, encoding="utf-8") as f:
        catalog = json.load(f)
    base = a.media_base.rstrip("/")

    for sid, name, slug in ((0, "Moonpacks Classic", "classic"), (1, "Moonpacks Full Moon", "full-moon")):
        t = fetch_table(a.source, sid)
        t["name"] = name
        for c in t["cards"]:
            c["media"] = f"{base}/{c['card_id']}.svg"
        if sid == 0:
            for c in t["cards"]:
                if c["card_id"] in DOG_BURNABLES:
                    if c["backing"] is None or c["cap"] is not None:
                        raise SystemExit(f"{c['card_id']} : brûlable commune sans plafond attendue")
                    c["weight"] = DOG_BURNABLE_WEIGHT
            t["kinds"] = kinds_for(t, catalog)
            dog = t["kinds"][0]
            p = dog_burnable_chance(t, dog)
            if not 0.30 <= p <= 0.37:
                raise SystemExit(f"pack Dog : {p:.1%} de packs avec une brûlable (1 sur 3 attendu)")
            print(f"pack Dog : {p:.1%} des packs ont au moins une brûlable")
        m = write_series(t, os.path.join(a.out, slug), sid)
        print(f"série {sid} {name} : {m['cards']} cartes, hash {m['table_hash']}, dépôt {m['deposit_total_near']} NEAR")
        for k in m["kinds"]:
            print(f"  type {k['kind']} {k['name']} : {k['cards_per_pack']} cartes, {k['pool']} possibles, "
                  f"{k['price_near']} NEAR, valeur {k['value']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
