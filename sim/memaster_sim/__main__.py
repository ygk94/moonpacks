"""Ligne de commande.

    python -m memaster_sim run configs/serie1-A-10near.yaml [--boosters 1000000] [--trajectoires 10000]
    python -m memaster_sim sensibilite configs/serie1-A-10near.yaml
    python -m memaster_sim tout          # toutes les configs de configs/, résultats dans resultats/
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from . import modele as M
from . import rapport as R

RACINE = Path(__file__).resolve().parents[1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_sim")
    ap.add_argument("commande", choices=["run", "sensibilite", "tout"])
    ap.add_argument("config", nargs="?")
    ap.add_argument("--boosters", type=int, default=1_000_000)
    ap.add_argument("--trajectoires", type=int, default=None)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--sortie", type=Path, default=RACINE / "resultats")
    args = ap.parse_args(argv)
    args.sortie.mkdir(parents=True, exist_ok=True)

    if args.commande in ("run", "sensibilite") and not args.config:
        ap.error("config manquante")
    # les séries 2 et 3 ont leur propre commande (python -m memaster_sim.serie2 run, .serie3 run)
    configs = [Path(args.config)] if args.config else sorted(
        c for c in (RACINE / "configs").glob("*.yaml") if not c.name.startswith(("serie2-", "serie3-", "serie4-")))

    for chemin in configs:
        cfg = M.charger_config(chemin)
        t0 = time.time()
        if args.commande in ("run", "tout"):
            res = R.executer(cfg, args.boosters, args.trajectoires, args.seed)
            md = R.markdown(res)
            print(md)
            (args.sortie / f"{chemin.stem}.md").write_text(md, encoding="utf-8")
            R.sauver_json(res, args.sortie / f"{chemin.stem}.json")
        if args.commande == "sensibilite" or (args.commande == "tout" and "mythique" in cfg["raretes"]):
            sens = R.sensibilite(cfg, args.boosters)
            md = R.markdown_sensibilite(cfg, sens)
            print(md)
            (args.sortie / f"{chemin.stem}-sensibilite.md").write_text(md, encoding="utf-8")
        print(f"[{chemin.name} : {time.time() - t0:.0f} s]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
