"""Série 5 : décisions du porteur appliquées par le contrat (11/11/2026).

    python -m memaster_sim.serie5 [--rapide]   # écrit resultats/serie5/ (dont tables-valeur.json)

Changements par rapport à la série 4 (`configs/serie5.yaml`) :
1. pitié sans garantie : p(n) = min(p_max, p0 + k·n), p0 = 1/50 000, p_max = 1/25 000, plafond en 1 000 packs ;
   le compteur revient à 0 seulement après un gold pack (un pack rush compte comme un pack sans gold) ;
2. mythique ~1 pour 10⁶ packs classiques : 5 / 2·10⁷ par emplacement (poids du contrat), sur les emplacements 1 à 4 ;
   le 5ᵉ, tiré parmi les brûlables, ne peut pas être mythique (une mythique n'est jamais brûlable, multiplicateur 0) ;
3. gold pack : 5ᵉ emplacement légendaire 99 %, mythique 1 % ; l'emplacement tiré parmi les brûlables est le 2ᵉ ;
4. V moyenne 75 % pour le normal et le rush (même forme), gold inchangé (200 %).
Tout le calcul vient de `serie4.py` (tables, types de packs, couverture, marge, arbitrage) ; ce module ajoute
l'alignement des mythiques, les fréquences (gold et mythique) et leurs contrôles Monte-Carlo.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from . import catalogue as C
from . import modele as M
from . import pitie as Pi
from . import rapport as R
from . import serie4 as S4
from . import valeur as V

RACINE = S4.RACINE
CHEMIN_PARAMS = RACINE / "configs" / "serie5.yaml"
SORTIE = RACINE / "resultats" / "serie5"
TYPES = S4.TYPES


def charger_parametres(chemin: Path = CHEMIN_PARAMS) -> dict:
    return S4.charger_parametres(chemin)


def proba_mythique_emplacement(par: dict) -> float:
    w = par["raretes_contrat"]["poids"]
    return w["mythique"] / sum(w.values())


def aligner_mythiques(cfg: dict, p_emplacement: float) -> dict:
    """Mythique à p_emplacement dans chaque table d'emplacement (la commune compense) et jamais brûlable : le 5ᵉ
    emplacement d'un pack normal ou rush, tiré parmi les brûlables, retombe alors sur la légendaire."""
    for t in cfg["emplacements"]["tables"].values():
        t["commune"] -= p_emplacement - t.get("mythique", 0.0)
        t["mythique"] = p_emplacement
    cfg["raretes"]["mythique"]["brulables"] = 0
    cfg["raretes"]["mythique"]["part_brulable"] = 0.0
    cfg["catalogue"]["brulables"].pop("mythique", None)
    cfg["nom"] = cfg["nom"].replace("Série 4", "Série 5")
    M.valider_config(cfg)
    return cfg


def construire_config(prix_usd: float, par: dict, cartes: list[dict] | None = None) -> dict:
    cfg = S4.construire_config(prix_usd, par["near_usd"], par["catalogue"]["brulables_communes"], cartes)
    return aligner_mythiques(cfg, proba_mythique_emplacement(par))


# =========================================================================== fréquences

def frequences(par: dict, pop: dict, an: dict, rapide: bool = False) -> dict:
    pi = par["pitie"]
    p0, k, N, pm = pi["p0"], pi["k"], pi.get("N"), pi.get("p_max", 1.0)
    pp = par["population"]
    pk = Pi.packs_par_joueur(pp["joueurs"], np.random.default_rng(31), pp["mediane"], pp["sigma"], pp["maximum"])
    g_pop_exact = Pi.g_pop_exact(pk, p0, k, N, pm)
    m, h_star = Pi.debut_plafond(p0, k, pm)
    S = Pi.survie(p0, k, None, pm, m)
    div = 10 if rapide else 1
    mc = par["monte_carlo"]
    t = time.time()
    T = Pi.mc_cycles(mc["cycles"] // div, p0, k, pm, np.random.default_rng(71))
    fl = Pi.mc_flux_stationnaire(mc["flux"]["joueurs"] // div, mc["flux"]["packs"], p0, k, pm,
                                 np.random.default_rng(72))
    print(f"[Monte-Carlo gold : {time.time() - t:.0f} s]", file=sys.stderr)
    gi = pop["g_inf"]
    e_cycle = T.mean()
    gold = {
        "p0": p0, "k": k, "p_max": pm, "N": N, "plafond_atteint_au_pack": m, "survie_au_plafond": float(S[-1]),
        "duree_moyenne_cycle": 1 / gi, "g_inf": gi, "g_pop_mc": pop["g_pop"], "golds_population_mc": pop["golds"],
        "g_pop_exact": g_pop_exact, "packs_population": pop["packs"],
        "part_joueurs_sans_gold": pop["part_joueurs_sans_gold"],
        "mc_cycles": {"cycles": int(T.size), "duree_moyenne": float(e_cycle),
                      "erreur_type": float(T.std() / np.sqrt(T.size)), "g": float(1 / e_cycle)},
        "mc_flux": {**fl, "erreur_type_relative": float(1 / np.sqrt(max(1, fl["golds"])))},
    }
    a = an[par["recommandee"]]
    er = {kk: V.esperance_raretes(tp) for kk, tp in a["types"].items()}
    pm_type = {kk: er[kk]["mythique"] for kk in TYPES}
    r = par["rush"]["part"]

    def flux(g):
        p = V.parts_types(g, r)
        return float(sum(p[kk] * pm_type[kk] for kk in TYPES))
    classiques = (1 - r) * pm_type["normal"] + r * pm_type["rush"]
    myth = {"par_emplacement": proba_mythique_emplacement(par), "par_pack": pm_type,
            "classiques": classiques, "flux_g_pop": flux(g_pop_exact), "flux_g_inf": flux(gi),
            "part_gold_dans_flux_g_inf": gi * pm_type["gold"] / flux(gi)}
    return {"gold": gold, "mythique": myth}


# =========================================================================== mise en forme

def _pc(x, d=1):
    return R._pct(x, d)


def _un_pour(p):
    return R._n(1 / p, 0) if p > 0 else "∞"


def section_frequences(par: dict, fr: dict) -> str:
    g, my = fr["gold"], fr["mythique"]
    mcc, mcf = g["mc_cycles"], g["mc_flux"]
    L = ["## Fréquence des gold packs (pitié sans garantie)", "",
         f"p(n) = min(p_max, p0 + k·n), p0 = 1/{R._n(1 / g['p0'], 0)}, p_max = 1/{R._n(1 / g['p_max'], 0)}, "
         f"k = {g['k']:.1e} : plafond atteint au pack {g['plafond_atteint_au_pack']} du cycle (1 000 + 1 par l'arrondi "
         f"flottant, sans effet), atteint par {_pc(g['survie_au_plafond'], 1)} des cycles. Au-delà, chance constante : "
         "queue géométrique exacte, E[T] = Σ_{j<m} S(j) + S(m) / p_max. Aucun gold garanti. Un pack rush compte comme "
         "un pack sans gold (n + 1).", "",
         "| Mesure | Part des packs en gold | **1 gold pour** |", "|---|---:|---:|",
         f"| g_∞ (joueur qui ne s'arrête pas), exact | {g['g_inf']:.3e} | **{_un_pour(g['g_inf'])} packs** |",
         f"| g_∞, Monte-Carlo : {R._n(mcc['cycles'], 0)} cycles | {mcc['g']:.3e} | {_un_pour(mcc['g'])} "
         f"(± {R._n(mcc['erreur_type'], 0)}) |",
         f"| g_∞, Monte-Carlo : flux stationnaire de {R._n(mcf['packs'], 0)} packs-joueurs ({R._n(mcf['golds'], 0)} golds) | "
         f"{mcf['g']:.3e} | {_un_pour(mcf['g'])} (± {_pc(mcf['erreur_type_relative'], 1)}) |",
         f"| g_pop (population de la série 4, {R._n(par['population']['joueurs'], 0)} joueurs, "
         f"{R._n(g['packs_population'], 0)} packs), exact | {g['g_pop_exact']:.3e} | **{_un_pour(g['g_pop_exact'])} packs** |",
         f"| g_pop, une simulation de cette population ({g['golds_population_mc']} golds) | {g['g_pop_mc']:.3e} | "
         f"{_un_pour(g['g_pop_mc'])} |", "",
         f"Avec cette population (médiane {par['population']['mediane']} packs par joueur), "
         f"{_pc(g['part_joueurs_sans_gold'], 2)} des joueurs ne voient aucun gold pack. g_pop exact : espérance des "
         "golds par joueur par l'équation de renouvellement (sans tirage) ; la simulation compte une poignée de golds.", "",
         "## Fréquence des mythiques", "",
         f"Mythique à {my['par_emplacement']:.2e} par emplacement (poids 5 sur 2·10⁷ du contrat), emplacements 1 à 4 ; "
         "le 5e (tiré parmi les brûlables) ne peut pas être mythique. Gold pack : 5e emplacement mythique 1 %, plus les "
         "planchers rare/épique (table standard restreinte).", "",
         "| Flux | Mythiques par pack | **1 mythique pour** |", "|---|---:|---:|"]
    for k in TYPES:
        L.append(f"| pack {k} | {my['par_pack'][k]:.3e} | {_un_pour(my['par_pack'][k])} packs |")
    L += [f"| **packs classiques** (normal + rush {_pc(par['rush']['part'], 0)}) | {my['classiques']:.3e} | "
          f"**{_un_pour(my['classiques'])} packs** |",
          f"| flux avec gold (g_pop) | {my['flux_g_pop']:.3e} | **{_un_pour(my['flux_g_pop'])} packs** |",
          f"| flux avec gold (g_∞) | {my['flux_g_inf']:.3e} | {_un_pour(my['flux_g_inf'])} packs |", "",
          f"Avec g_∞, {_pc(my['part_gold_dans_flux_g_inf'], 0)} des mythiques sortent d'un gold pack."]
    return "\n".join(L) + "\n"


def section_couverture(par: dict, a: dict, fr: dict) -> tuple[str, dict]:
    t = a["tables"]
    g_ex, gi = fr["gold"]["g_pop_exact"], fr["gold"]["g_inf"]
    r = par["rush"]["part"]
    d = {"normal": t["normal"].moyenne(), "rush": t["rush"].moyenne(), "gold": t["gold"].moyenne(),
         "flux_g_pop_mc": a["couverture"]["avec_pitie_et_rush"],
         "flux_g_pop_exact": V.couverture_globale(t, V.parts_types(g_ex, r)),
         "flux_g_inf": V.couverture_globale(t, V.parts_types(gi, r)),
         "rush_identique_au_normal": t["rush"] == t["normal"]}
    L = ["## Valeur moyenne V", "",
         "| Pack normal | Pack rush | Gold pack | **Flux réel** (g_pop exact, rush 5 %) | Flux g_pop simulé | Flux g_∞ |",
         "|---:|---:|---:|---:|---:|---:|",
         f"| {_pc(d['normal'], 2)} | {_pc(d['rush'], 2)} | {_pc(d['gold'], 2)} | **{_pc(d['flux_g_pop_exact'], 4)}** | "
         f"{_pc(d['flux_g_pop_mc'], 4)} | {_pc(d['flux_g_inf'], 4)} |", "",
         "Rush : même paliers et même σ que le normal, calibré sur la même moyenne : "
         + ("les deux tables sont identiques." if d["rush_identique_au_normal"] else "tables proches.")
         + " Le gold pack (200 %) pèse moins de 0,01 point sur le flux."]
    return "\n".join(L) + "\n", d


def section_arbitrage(par: dict, a: dict) -> tuple[str, dict]:
    b = a["arbitrage"]
    L = ["## Borne anti-arbitrage", "",
         f"Gain moyen de « j'achète, je brûle tout, je revends le reste », en part du prix (c = {R._n(a['c'], 3)}). "
         f"Borne {_pc(b['borne'], 0)}. Sans garantie, le gold pack n'est jamais choisissable ; le cycle de pitié est "
         "celui d'un joueur qui ouvre jusqu'au gold (g_∞).", "",
         "| Pack normal | Pack rush | Cycle de pitié | Gold pack seul (non choisissable) | Borne |",
         "|---:|---:|---:|---:|---:|",
         f"| {_pc(b['normal'])} | {_pc(b['rush'])} | {_pc(b['cycle_pitie'])} | {_pc(b['gold_seul'], 0)} | "
         f"{_pc(b['borne'], 0)} |"]
    return "\n".join(L) + "\n", b


# =========================================================================== exécution

def lancer(sortie: Path = SORTIE, rapide: bool = False) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    par = charger_parametres()
    cartes = C.charger_catalogue_v2()
    cfgs = {x: construire_config(x, par, cartes) for x in par["prix_usd"]}
    t0 = time.time()
    pop = S4.population(par)
    print(f"[population : {time.time() - t0:.0f} s, g_pop = {pop['g_pop']:.3e}]", file=sys.stderr)
    an = {v: S4.analyser(par, v, pop, cfgs[par["prix_usd"][0]]) for v in par["variantes"]}
    a = an[par["recommandee"]]
    fr = frequences(par, pop, an, rapide)
    # marge sur le flux réel avec g_pop exact (la simulation de la population ne compte qu'une poignée de golds)
    a["couverture"]["avec_pitie_et_rush_simule"] = a["couverture"]["avec_pitie_et_rush"]
    a["couverture"]["avec_pitie_et_rush"] = V.couverture_globale(
        a["tables"], V.parts_types(fr["gold"]["g_pop_exact"], par["rush"]["part"]))
    md_tables, d_tables = S4.section_tables(par, an)
    md_cov, d_cov = section_couverture(par, a, fr)
    md_marge, d_marge = S4.section_marge(par, an)
    md_arb, d_arb = section_arbitrage(par, a)
    md_freq = section_frequences(par, fr)
    tj = S4.tables_json(par, a)
    tj["target"] = "moyenne 75 % (normal et rush)"
    R.sauver_json(tj, sortie / "tables-valeur.json")
    serie4_gold = S4.SORTIE / "tables-valeur.json"
    gold_identique = None
    if serie4_gold.exists():
        import json
        gold_identique = json.loads(serie4_gold.read_text())["value_tables"]["gold"]["tiers"] == \
            tj["value_tables"]["gold"]["tiers"]
    k = par["couts"]
    entete = ["# Série 5 : pitié sans garantie, mythique 1 pour 10⁶, gold 99/1, V moyenne 75 %", "",
              f"Paramètres : `configs/serie5.yaml`. Coûts de la série 4, sauf {k['octets_par_pack']} octets par pack "
              f"(stockage payé par l'acheteur) ; gaz {k['gaz_tgas']} Tgas (valeur de la série 4, pas de meilleure mesure). "
              f"Tables publiées : `tables-valeur.json` (gold identique à la série 4 : "
              f"{'oui' if gold_identique else 'non' if gold_identique is not None else 'non vérifié'}).", ""]
    texte = "\n".join(entete) + "\n" + "\n".join([md_cov, md_freq, md_marge, md_arb, md_tables])
    (sortie / "serie5.md").write_text(texte, encoding="utf-8")
    out = {"couverture": d_cov, "frequences": fr, "marge": d_marge, "arbitrage": d_arb, "tables": d_tables,
           "population": pop, "gold_identique_serie4": gold_identique,
           "couts": {"octets_par_pack": k["octets_par_pack"], "gaz_tgas": k["gaz_tgas"]}}
    R.sauver_json(out, sortie / "serie5.json")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_sim.serie5")
    ap.add_argument("--rapide", action="store_true", help="10 fois moins de tirages Monte-Carlo")
    ap.add_argument("--sortie", type=Path, default=SORTIE)
    args = ap.parse_args(argv)
    lancer(args.sortie, args.rapide)
    return 0


if __name__ == "__main__":
    sys.exit(main())
