#!/usr/bin/env python3
"""Écrit les paramètres des séries de démo « entrée » et « standard » pour scripts/build_series.py.

Usage (depuis contract/) :
    python3 -I scripts/series_demo.py --near-usd 3.62 --cours-source "CoinGecko simple/price, 2026-11-11 23:05 UTC" \
        [--media-base ipfs://<CID>] [--sans-appoint]
puis, pour chaque série (sels existants, aucun neuf) :
    python3 -I scripts/build_series.py scripts/serie-demo-entree.json --catalogue ../docs/data/catalogue-demo.json \
        --sels scripts/secrets/serie-v2.json [--media-base ipfs://<CID>]

Sources :
- mécaniques : scripts/serie-exemple.json (gold pack, pitié, burns, rush, résurrection, contrôle de couverture) ;
- tables de valeur : sim/resultats/serie5/tables-valeur.json (27 paliers, moyenne 75 %), recopiées dans
  mechanics.value pour que les paramètres se suffisent ;
- brûlables : docs/data/intents-brulables-demo.json (scripts/intents_brulables.py), cartes reliées, plus les communes
  d'appoint reliées sauf --sans-appoint. Le factice de l'exemple (mythique-m1) n'est pas repris : les mythiques
  restent non adossées ;
- prix : dollars convertis en NEAR au cours donné, arrondis au 1/10 000 de NEAR le plus proche.

`amount` des brûlables : quantité indicative du jeton (plus petite unité) qui vaut le prix du pack au cours 1Click du
relevé. Dans une série à table de valeur, le contrat ne le lit pas pour les exemplaires tirés (la part de valeur du pack,
en yoctoNEAR, la remplace : docs/mecaniques-spec.md, section 9), mais il doit être > 0.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.dirname(HERE)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, HERE)

import build_series  # noqa: E402  (sim_value_tables)

SERIES = (
    {"slug": "serie-demo-entree", "name": "Memaster Entry", "usd": "0.20"},
    {"slug": "serie-demo-standard", "name": "Memaster Standard", "usd": "0.50"},
)
YOCTO = 10 ** 24


def price_yocto(usd: str, near_usd: str) -> int:
    near = (Decimal(usd) / Decimal(near_usd)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    if near <= 0:
        raise SystemExit("prix nul après arrondi")
    return int(near * YOCTO)


def burnables(mapping: dict, usd: str, appoint: bool) -> list[dict]:
    rows = list(mapping["reliees"])
    if appoint:
        rows += [x for x in mapping.get("appoint", []) if x["statut"] == "reliée"]
    out = []
    for x in sorted(rows, key=lambda x: x["card_id"]):
        price = Decimal(str(x["prix_usd_1click"]))
        amount = int(Decimal(usd) / price * (10 ** int(x["decimals"])))
        if not 0 < amount < 1 << 128:
            raise SystemExit(f"amount hors bornes pour {x['card_id']}")
        out.append({"card_id": x["card_id"], "asset_id": x["asset_id"], "amount": str(amount),
                    "_rarete": x["rarete"], "_appoint": x in mapping.get("appoint", [])})
    if len({b["card_id"] for b in out}) != len(out):
        raise SystemExit("brûlable en double")
    return out


def make_params(example: dict, tables: dict, mapping: dict, serie: dict, near_usd: str, source: str,
                media_base: str | None, appoint: bool) -> dict:
    p = copy.deepcopy(example)
    py = price_yocto(serie["usd"], near_usd)
    p["_doc"] = (f"Série de démo {serie['name']} : pack à {serie['usd']} $ = {Decimal(py) / YOCTO} NEAR au cours de "
                 f"{near_usd} $/NEAR ({source}). Généré par scripts/series_demo.py : ne pas éditer à la main. "
                 "Mécaniques de serie-exemple.json, tables de valeur de sim/resultats/serie5/tables-valeur.json, "
                 "brûlables de docs/data/intents-brulables-demo.json. Testnet seulement.")
    p["slug"], p["name"], p["price_yocto"] = serie["slug"], serie["name"], str(py)
    p["prix_usd"], p["cours_near_usd"], p["cours_source"] = serie["usd"], near_usd, source
    if media_base:
        base = media_base.rstrip("/")
        p["media_template"], p["mythic_media"] = base + "/{id}.svg", base + "/mythique.svg"
    else:
        p["media_template"], p["mythic_media"] = "ipfs://TODO/{id}.svg", "ipfs://TODO/mythique.svg"
    bs = burnables(mapping, serie["usd"], appoint)
    p["burnables"] = [{k: v for k, v in b.items() if not k.startswith("_")} for b in bs]
    p["brulables_appoint"] = appoint
    p["_doc_burnables"] = (
        f"{len(bs)} brûlables reliées par adresse de contrat à un actif NEAR Intents coté (devis dry) : "
        + ", ".join(f"{b['card_id']} ({b['_rarete']}{', appoint' if b['_appoint'] else ''})" for b in bs)
        + ". amount = quantité indicative du jeton valant le prix du pack (non lue avec une table de valeur).")
    m = p["mechanics"]
    m["value"] = build_series.sim_value_tables(tables)
    m["value"]["_doc"] = "Tables de valeur de sim/resultats/serie5/tables-valeur.json (format de la sim converti)."
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--near-usd", required=True, help="cours NEAR en dollars (chaîne décimale)")
    ap.add_argument("--cours-source", required=True, help="source et heure du cours")
    ap.add_argument("--exemple", default=os.path.join(HERE, "serie-exemple.json"))
    ap.add_argument("--tables-valeur", default=os.path.join(REPO, "sim", "resultats", "serie5", "tables-valeur.json"))
    ap.add_argument("--correspondance", default=os.path.join(REPO, "docs", "data", "intents-brulables-demo.json"))
    ap.add_argument("--media-base", help="ipfs://<CID> du dossier des visuels (scripts/ipfs_media.py)")
    ap.add_argument("--sans-appoint", action="store_true", help="sans les communes d'appoint")
    ap.add_argument("--dest", default=HERE)
    a = ap.parse_args(argv)
    load = lambda path: json.load(open(path, encoding="utf-8"))  # noqa: E731
    example, tables, mapping = load(a.exemple), load(a.tables_valeur), load(a.correspondance)
    for s in SERIES:
        p = make_params(example, tables, mapping, s, a.near_usd, a.cours_source, a.media_base, not a.sans_appoint)
        path = os.path.join(a.dest, s["slug"] + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{s['slug']} : {s['usd']} $ = {Decimal(p['price_yocto']) / YOCTO} NEAR, "
              f"{len(p['burnables'])} brûlables -> {os.path.relpath(path, CONTRACT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
