#!/usr/bin/env python3
"""Relevé CoinGecko de la catégorie meme-token (API publique, sans clé).

Parcourt /coins/markets page par page (250 jetons), 15 s minimum entre deux appels,
nouvel essai après une erreur 429 ou 5xx en respectant l'en-tête Retry-After (15 à 120 s).
Usage : python3 crawl_coingecko.py [date]   (CG_CACHE=<dossier> pour reprendre après coupure)
Écrit docs/data/coingecko-meme-<date>.csv.
Pic estimé = market_cap / (1 + ath_change_percentage/100), vide si non calculable.
"""
import csv, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-11-11"
OUT = Path(__file__).resolve().parents[1] / "data" / f"coingecko-meme-{DATE}.csv"
URL = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
       "&category=meme-token&per_page=250&page={}")
UA = "Mozilla/5.0 (compatible; generic-research-client/1.0)"
DELAY = 15
# Cache facultatif des pages brutes (reprise après coupure) : variable CG_CACHE=<dossier>
CACHE = Path(os.environ["CG_CACHE"]) if os.environ.get("CG_CACHE") else None
FIELDS = ["id", "symbol", "name", "market_cap", "total_volume", "current_price",
          "ath", "ath_date", "ath_change_percentage", "atl", "atl_date"]

def fetch(page):
    if CACHE and (CACHE / f"page{page}.json").exists():
        return json.loads((CACHE / f"page{page}.json").read_text()), True
    for attempt in range(200):
        req = urllib.request.Request(URL.format(page), headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            if CACHE:
                CACHE.mkdir(parents=True, exist_ok=True)
                (CACHE / f"page{page}.json").write_text(json.dumps(data))
            return data, False
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                # on respecte l'en-tête Retry-After, sans descendre sous 15 s ni passer 120 s
                try:
                    wait = int(e.headers.get("Retry-After", "30"))
                except ValueError:
                    wait = 30
                wait = min(max(wait + 3, DELAY), 120)
                print(f"page {page}: HTTP {e.code}, nouvel essai dans {wait} s", file=sys.stderr)
                time.sleep(wait); continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"page {page}: {e}, nouvel essai dans 60 s", file=sys.stderr)
            time.sleep(60)
    raise RuntimeError(f"page {page}: échec après 200 essais")

def peak(mc, ch):
    try:
        mc, ch = float(mc), float(ch)
    except (TypeError, ValueError):
        return ""
    if mc <= 0 or ch <= -100 or ch >= 0:
        return ""
    return round(mc / (1 + ch / 100))

def main():
    rows, seen, page = [], set(), 1
    while True:
        data, cached = fetch(page)
        print(f"page {page}: {len(data)} jetons", file=sys.stderr)
        if not data:
            break
        for c in data:
            if c["id"] in seen:
                continue
            seen.add(c["id"])
            row = {k: c.get(k) for k in FIELDS}
            row["peak_mcap_est"] = peak(c.get("market_cap"), c.get("ath_change_percentage"))
            rows.append(row)
        if len(data) < 250:
            break
        page += 1
        if not cached:
            time.sleep(DELAY)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS + ["peak_mcap_est"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} jetons -> {OUT}", file=sys.stderr)

if __name__ == "__main__":
    main()
