"""Série 2 : grille (nombre de brûlables × prix) sur le catalogue v2.

    python -m memaster_sim.serie2 configs      # écrit configs/serie2-*.yaml
    python -m memaster_sim.serie2 run          # simule la grille, écrit resultats/serie2/

Hypothèses reprises de la série 1 (jeu A à 10 NEAR, jeu C à 5 NEAR) : β, δ, ε, poids, multiplicateurs, plafonds,
reventes, coûts, valeur et cote du mythique, V_cap. Ce qui change : les effectifs (catalogue v2), le nombre et la
place des brûlables, une part brûlable égale à brûlables / effectif (pas de faveur), et les tables de rareté.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml

from . import catalogue as C
from . import modele as M
from . import rapport as R
from . import simulation as S

RACINE = Path(__file__).resolve().parents[1]
TOTAUX = [30, 60, 90, 120, 150]
PRIX = [5, 10]
GRAINE_BRULABLES = 2026
FACTEUR_PALIER = 2.0   # un exemplaire d'un palier sort FACTEUR_PALIER fois moins qu'un exemplaire du palier du dessous

# Hypothèses de la série 1, par prix (jeu A pour 10 NEAR, jeu C pour 5 NEAR).
BASE = {
    10: {
        "serie1": "serie1-A-10near.yaml", "v_cap": 600, "valeur_mythique": 477, "cote_mythique": 5000,
        "poids": {"commune": 1, "rare": 1.4, "epique": 3.5, "legendaire": 10},
        "revente": {"commune": 0.05, "rare": 0.15, "epique": 0.5, "legendaire": 2.0, "mythique": 0},
        "multiplicateur": {"valeurs": [0.6, 1, 2.5], "probas": [0.5, 0.35, 0.15]},
    },
    5: {
        "serie1": "serie1-C-5near.yaml", "v_cap": 300, "valeur_mythique": 276, "cote_mythique": 10000,
        "poids": {"commune": 1, "rare": 1.2, "epique": 3, "legendaire": 9},
        "revente": {"commune": 0.03, "rare": 0.08, "epique": 0.25, "legendaire": 1.0, "mythique": 0},
        "multiplicateur": {"valeurs": [0.8, 1, 2], "probas": [0.5, 0.35, 0.15]},
    },
}
PLAFONDS = {"commune": 25, "rare": 30, "epique": 100, "legendaire": 280}
# part de chaque rareté (en cartes par booster) placée dans le 5e emplacement, le reste réparti sur les 4 autres
PART_FAVORABLE = {"rare": 0.5, "epique": 0.6, "legendaire": 0.8}


def tables_rarete(eff: dict[str, int], cote_mythique: float, facteur: float = FACTEUR_PALIER,
                  n_cartes: int = 5) -> dict:
    """Tables 4 × standard + 1 × favorable telles que la fréquence d'un exemplaire décroisse d'un facteur
    `facteur` à chaque palier (commune → rare → épique → légendaire). Le mythique garde sa cote par booster,
    tout entière dans l'emplacement 5."""
    paliers = ["commune", "rare", "epique", "legendaire"]
    poids = np.array([eff[r] / facteur**i for i, r in enumerate(paliers)])
    p_myth = 1 / cote_mythique
    par_booster = poids / poids.sum() * (n_cartes - p_myth)      # cartes de chaque rareté par booster
    fav, std = {}, {}
    for r, x in zip(paliers, par_booster):
        if r == "commune":
            continue
        fav[r] = round(float(x * PART_FAVORABLE[r]), 6)
        std[r] = round(float(x * (1 - PART_FAVORABLE[r]) / (n_cartes - 1)), 6)
    fav["mythique"] = p_myth
    std["mythique"] = 0.0
    fav["commune"] = 1 - sum(fav.values())
    std["commune"] = 1 - sum(std.values())
    ordre = ["commune", "rare", "epique", "legendaire", "mythique"]
    return {"standard": {r: std[r] for r in ordre}, "favorable": {r: fav[r] for r in ordre}}


def construire_config(total: int, prix: int, cartes: list[dict] | None = None,
                      facteur: float = FACTEUR_PALIER) -> dict:
    cartes = C.charger_catalogue_v2() if cartes is None else cartes
    b = BASE[prix]
    eff = C.effectifs(cartes)
    rep = C.repartir_brulables(total, cartes)
    choix = C.choisir_brulables(cartes, rep, GRAINE_BRULABLES)
    raretes = {}
    for r in ["commune", "rare", "epique", "legendaire"]:
        raretes[r] = {"poids": b["poids"][r], "part_brulable": round(rep[r] / eff[r], 6), "effectif": eff[r],
                      "brulables": rep[r], "revente": b["revente"][r], "plafond": PLAFONDS[r]}
    # mythique à valeur fixe : poids très grand, la valeur est le plafond (DOGE, SHIB, PEPE, scellés)
    raretes["mythique"] = {"poids": 100000, "part_brulable": 1.0, "effectif": eff["mythique"],
                           "brulables": rep["mythique"], "revente": 0, "plafond": b["valeur_mythique"],
                           "multiplicateur": {"valeurs": [1], "probas": [1]}}
    cfg = {
        "nom": f"Série 2 : {total} brûlables, {prix} NEAR",
        "prix": prix, "n_cartes": 5, "near_usd": 3.6,
        "beta": 0.60, "delta": 0.10, "epsilon": 0.15, "v_cap": b["v_cap"], "v_min_brulable": 1.4,
        "calibrer_avec_plafonds": True,
        "raretes": raretes,
        "emplacements": {"tables": tables_rarete(eff, b["cote_mythique"], facteur),
                         "ordre": ["standard"] * 4 + ["favorable"]},
        "multiplicateur": copy.deepcopy(b["multiplicateur"]),
        "couts": {"s_achat": 0.01, "f_burn": 0.002, "f_burn_fixe": 0.03, "s_vente": 0.03, "phi": 0.05},
        "ruine": {"horizon": 10000, "trajectoires": 10000, "z": 3},
        "catalogue": {"source": "docs/data/catalogue-v2.json", "graine_brulables": GRAINE_BRULABLES,
                      "facteur_palier": facteur, "brulables": {r: v for r, v in choix.items() if v}},
    }
    M.valider_config(cfg)
    return cfg


def nom_fichier(total: int, prix: int) -> str:
    return f"serie2-{total:03d}brul-{prix:02d}near"


EN_TETE = """\
# Série 2 (catalogue v2), générée par `python -m memaster_sim.serie2 configs`. Ne pas éditer à la main.
# Hypothèses de la série 1 ({serie1}) : β, δ, ε, poids, multiplicateurs, plafonds, reventes, coûts, mythique, V_cap.
# Effectifs : docs/data/catalogue-v2.json (section « catalogue »). part_brulable = brulables / effectif (pas de faveur).
# Brûlables : pyramide remplie par le haut (mythiques, légendaires, épiques ≤ 50 %, rares ≤ 25 %), parmi les jetons
# non morts et hors arnaques avérées, tirage à graine fixe. Mythique : valeur fixe = plafond (poids très grand).
# Tables : un exemplaire sort {facteur} fois moins souvent à chaque palier (commune → rare → épique → légendaire).
"""


def ecrire_configs(dossier: Path = RACINE / "configs") -> list[Path]:
    cartes = C.charger_catalogue_v2()
    out = []
    for prix in PRIX:
        for total in TOTAUX:
            cfg = construire_config(total, prix, cartes)
            chemin = dossier / f"{nom_fichier(total, prix)}.yaml"
            texte = EN_TETE.format(serie1=BASE[prix]["serie1"], facteur=_fr(FACTEUR_PALIER))
            texte += yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False, width=120)
            chemin.write_text(texte, encoding="utf-8")
            out.append(chemin)
    return out


def _fr(x: float) -> str:
    return f"{x:g}".replace(".", ",")


# --------------------------------------------------------------------------- calibrage réalisable

def rendre_realisable(cfg: dict) -> tuple[dict, bool]:
    """Si les plafonds par carte empêchent d'atteindre β·P, on baisse β au maximum atteignable (moins 0,1 %)."""
    vmax = M.adossement_max(cfg)
    if vmax >= cfg["beta"] * cfg["prix"]:
        return cfg, True
    return M.avec(cfg, beta=0.999 * vmax / cfg["prix"]), False


# --------------------------------------------------------------------------- exécution

def executer_point(cfg: dict, n_boosters: int, trajectoires: int, seed: int = 1) -> dict:
    beta_vise = cfg["beta"]
    cfg, realisable = rendre_realisable(cfg)
    res = R.executer(cfg, n_boosters, trajectoires, seed)
    s, r = res["simulation"], res["ruine"]
    P = cfg["prix"]
    res["serie2"] = {
        "realisable": realisable,
        "beta_vise": beta_vise,
        "beta_effectif": cfg["beta"],
        "adossement_max": M.adossement_max(cfg),
        "marge_par_booster": P - s["esperance_adossement"] - cfg["delta"] * P,
        "marge_par_booster_formule": P * (1 - cfg["beta"] - cfg["delta"]),
        "p_au_moins_une_brulable": 1 - s["p_aucune_brulable"],
        "p_au_moins_une_brulable_formule": 1 - res["analytique"]["p_aucune_brulable"],
        "r0_risque_5": r.get("r0_risque_0.05"),
        "r0_risque_1": r.get("r0_risque_0.01"),
        "brulable_min": min(v["min"] for v in res["analytique"]["valeur_par_rarete"].values()),
        "beta_max_simule": s.get("beta_max_simule"),
    }
    return res


def tableau(points: list[dict]) -> str:
    L = ["| Brûlables (myth / lég / ép / rare) | Prix | β effectif | Marge / booster | P(≥ 1 brûlable) | "
         "Brûlables / booster | Plus petite brûlable | σ booster | P(adossement ≥ prix) | R₀ 5 % | R₀ 1 % | R₀ normale (risque réel) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for p in points:
        cfg, s2, s, r = p["config"], p["serie2"], p["simulation"], p["ruine"]
        rr = cfg["raretes"]
        rep = f"{sum(x['brulables'] for x in rr.values())} ({rr['mythique']['brulables']} / {rr['legendaire']['brulables']} / " \
              f"{rr['epique']['brulables']} / {rr['rare']['brulables']})"
        beta = R._pct(s2["beta_effectif"], 0 if s2["realisable"] else 1)
        if not s2["realisable"]:
            beta = f"**{beta}**"
        L.append(f"| {rep} | {cfg['prix']} | {beta} | {R._n(s2['marge_par_booster'])} | "
                 f"{R._pct(s2['p_au_moins_une_brulable'])} | {R._n(s['cartes_brulables_moyennes'], 3)} | "
                 f"{R._n(s2['brulable_min'], 1)} | {R._n(s['sigma_booster'], 1)} | {R._pct(s['p_adossement_ge_prix'])} | "
                 f"{R._n(s2['r0_risque_5'], 0)} | {R._n(s2['r0_risque_1'], 0)} | "
                 f"{R._n(r['r0_normale'], 0)} ({R._pct(r['p_ruine_a_r0_normale'])}) |")
    return "\n".join(L) + "\n"


def lancer(n_boosters: int, trajectoires: int, sortie: Path, seed: int = 1) -> list[dict]:
    sortie.mkdir(parents=True, exist_ok=True)
    points = []
    for prix in PRIX:
        for total in TOTAUX:
            chemin = RACINE / "configs" / f"{nom_fichier(total, prix)}.yaml"
            cfg = M.charger_config(chemin)
            t0 = time.time()
            res = executer_point(cfg, n_boosters, trajectoires, seed)
            (sortie / f"{chemin.stem}.md").write_text(_md_point(res), encoding="utf-8")
            R.sauver_json(res, sortie / f"{chemin.stem}.json")
            points.append(res)
            print(f"[{chemin.name} : {time.time() - t0:.0f} s]", file=sys.stderr)
    (sortie / "grille.md").write_text("## Série 2 : grille\n\n" + tableau(points), encoding="utf-8")
    R.sauver_json([{"config": nom_fichier(sum(x["brulables"] for x in p["config"]["raretes"].values()),
                                          p["config"]["prix"]), **p["serie2"]} for p in points],
                  sortie / "grille.json")
    return points


def _md_point(res: dict) -> str:
    s2 = res["serie2"]
    entete = ""
    if not s2["realisable"]:
        entete = (f"> **Non réalisable à β = {R._pct(s2['beta_vise'], 0)}** : avec les plafonds par carte, l'adossement "
                  f"moyen ne dépasse pas {R._n(s2['adossement_max'])} NEAR. Simulé à β = {R._pct(s2['beta_effectif'], 1)}.\n\n")
    return entete + R.markdown(res) + (f"- Marge simulée (prix − adossement − δ·P) : {R._n(s2['marge_par_booster'])} NEAR "
                                       f"par booster.\n")


def sensibilite_facteur(total: int, prix: int, facteurs, n_boosters: int, trajectoires: int) -> list[dict]:
    cartes = C.charger_catalogue_v2()
    out = []
    for f in facteurs:
        res = executer_point(construire_config(total, prix, cartes, f), n_boosters, trajectoires)
        res["facteur"] = f
        out.append(res)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_sim.serie2")
    ap.add_argument("commande", choices=["configs", "run", "sensibilite"])
    ap.add_argument("--boosters", type=int, default=2_000_000)
    ap.add_argument("--trajectoires", type=int, default=10_000)
    ap.add_argument("--total", type=int, default=150)
    ap.add_argument("--prix", type=int, default=10)
    ap.add_argument("--sortie", type=Path, default=RACINE / "resultats" / "serie2")
    args = ap.parse_args(argv)
    if args.commande == "configs":
        for c in ecrire_configs():
            print(c)
    elif args.commande == "run":
        print(tableau(lancer(args.boosters, args.trajectoires, args.sortie)))
    else:
        args.sortie.mkdir(parents=True, exist_ok=True)
        pts = sensibilite_facteur(args.total, args.prix, (1.5, 2.0, 3.0), args.boosters, args.trajectoires)
        L = [f"## Série 2 : sensibilité au facteur entre paliers ({args.total} brûlables, {args.prix} NEAR)", "",
             "| Facteur | Légendaire / booster | Épique / booster | " + tableau(pts).split("\n")[0].lstrip("| "),
             "|---:|---:|---:|" + tableau(pts).split("\n")[1].lstrip("|")]
        for p, ligne in zip(pts, tableau(pts).split("\n")[2:]):
            a = p["analytique"]
            tab = p["config"]["emplacements"]["tables"]
            nl = 4 * tab["standard"]["legendaire"] + tab["favorable"]["legendaire"]
            ne = 4 * tab["standard"]["epique"] + tab["favorable"]["epique"]
            L.append(f"| {_fr(p['facteur'])} | {R._n(nl, 4)} | {R._n(ne, 3)} " + ligne)
        md = "\n".join(L) + "\n"
        nom = f"sensibilite-facteur-{args.total:03d}brul-{args.prix:02d}near"
        (args.sortie / f"{nom}.md").write_text(md, encoding="utf-8")
        R.sauver_json([{"facteur": p["facteur"], **p["serie2"]} for p in pts], args.sortie / f"{nom}.json")
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
