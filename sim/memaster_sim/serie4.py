"""Série 4 : valeur aléatoire en jetons par pack (table V publiée), gold pack redéfini.

    python -m memaster_sim.serie4 configs          # écrit configs/serie4-PPPc.yaml
    python -m memaster_sim.serie4 run [--rapide]   # écrit resultats/serie4/ (dont tables-valeur.json)

Base : la config de la série 3 au même prix (catalogue v2, 150 brûlables, tables de rareté 4 × standard + favorable),
plus des communes brûlables pour que le 5ᵉ emplacement, tiré parmi les brûlables, retombe vers le bas. κ et les
multiplicateurs de valeur de la série 3 ne servent plus : la valeur d'un pack est V, tiré dans une table publiée.
Modèle et formules : `valeur.py`. Paramètres : `configs/serie4-valeur.yaml`.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import yaml

from . import catalogue as C
from . import couts as K
from . import gold as G
from . import modele as M
from . import pitie as Pi
from . import rapport as R
from . import serie3 as S3
from . import valeur as V

RACINE = Path(__file__).resolve().parents[1]
CHEMIN_PARAMS = RACINE / "configs" / "serie4-valeur.yaml"
SORTIE = RACINE / "resultats" / "serie4"
TYPES = ["normal", "gold", "rush"]


# =========================================================================== configs

def charger_parametres(chemin: Path = CHEMIN_PARAMS) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return yaml.safe_load(f)


def construire_config(prix_usd: float, near_usd: float = 2.5, communes: int = 20,
                      cartes: list[dict] | None = None) -> dict:
    """Config de la série 3 au même prix, avec `communes` communes brûlables (tirées parmi les vivantes)."""
    cartes = C.charger_catalogue_v2() if cartes is None else cartes
    cfg = S3.construire_config(prix_usd, 0.75, near_usd, cartes=cartes)
    eff = cfg["raretes"]["commune"]["effectif"]
    rep = {r: cfg["raretes"][r]["brulables"] for r in V.RARETES}
    rep["commune"] = communes
    choix = C.choisir_brulables(cartes, rep, cfg["catalogue"]["graine_brulables"])
    cfg["raretes"]["commune"]["brulables"] = communes
    cfg["raretes"]["commune"]["part_brulable"] = round(communes / eff, 6)
    cfg["catalogue"]["brulables"] = {r: v for r, v in choix.items() if v}
    cfg["nom"] = f"Série 4 : {S3._usd(prix_usd)} ({S3._n3(cfg['prix'])} NEAR), valeur V tirée par pack"
    cfg["serie4"] = {"note": "beta, kappa et multiplicateur ne servent pas : V vient de tables-valeur.json"}
    M.valider_config(cfg)
    return cfg


def nom_fichier(prix_usd: float) -> str:
    return f"serie4-{round(100 * prix_usd):03d}c"


EN_TETE = """\
# Série 4 (valeur V tirée par pack), générée par `python -m memaster_sim.serie4 configs`. Ne pas éditer à la main.
# Base : serie3 au même prix (catalogue v2, 150 brûlables), plus {communes} communes brûlables (parmi les vivantes,
# graine fixe) pour le 5e emplacement tiré parmi les brûlables. Paramètres de la série 4 : serie4-valeur.yaml.
"""


def ecrire_configs(dossier: Path = RACINE / "configs") -> list[Path]:
    par = charger_parametres()
    cartes = C.charger_catalogue_v2()
    out = []
    for x in par["prix_usd"]:
        cfg = construire_config(x, par["near_usd"], par["catalogue"]["brulables_communes"], cartes)
        chemin = dossier / f"{nom_fichier(x)}.yaml"
        chemin.write_text(EN_TETE.format(communes=par["catalogue"]["brulables_communes"]) +
                          yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
        out.append(chemin)
    return out


# =========================================================================== tables et types de packs

def construire_tables(par: dict, variante: str) -> dict:
    """Tables normal / gold / rush d'une variante. Le rush est simplifié (table normale) si la table normale
    dépasse déjà la couverture maximale du rush."""
    sur = par["variantes"][variante]["sur"]
    tot = par["tables"]["total_poids"]
    out = {}
    for k in ("normal", "gold"):
        d = par["tables"][k]
        out[k] = V.table_lognormale(V.paliers(*map(tuple, d["paliers"])), d["cible"], sur, d["sigma"], tot)
    d = par["tables"]["rush"]
    cmax = par["rush"]["couverture_max"]
    if out["normal"].moyenne() >= cmax:
        out["rush"] = out["normal"]
        out["_rush_simplifie"] = True
    else:
        out["rush"] = V.table_lognormale(V.paliers(*map(tuple, d["paliers"])), min(d["cible"], cmax), "moyenne",
                                         d["sigma"], tot)
        out["_rush_simplifie"] = False
    return out


def construire_types(cfg: dict, tables: dict, par: dict) -> dict[str, V.TypePack]:
    cfg_rush = G.table_or(cfg, par["rush"]["facteurs"])
    gp = par["gold_pack"]
    return {
        "normal": V.pack_normal(cfg, tables["normal"]),
        "gold": V.pack_gold(cfg, tables["gold"], tuple(gp["minimums"]), gp["dernier"], gp.get("brulable")),
        "rush": V.pack_normal(cfg, tables["rush"], cfg_rush["emplacements"]["tables"], "rush"),
    }


def population(par: dict, seed: int = 31) -> dict:
    pp, pi = par["population"], par["pitie"]
    pk = Pi.packs_par_joueur(pp["joueurs"], np.random.default_rng(seed), pp["mediane"], pp["sigma"], pp["maximum"])
    N, p_max = pi.get("N"), pi.get("p_max", 1.0)   # série 5 : N = None (pas de garantie), plafond p_max
    pop = Pi.simuler_population(pk, pi["p0"], pi["k"], N, np.random.default_rng(seed + 1), p_max)
    pop["g_inf"] = Pi.g_stationnaire(pi["p0"], pi["k"], N, p_max)
    return pop


# =========================================================================== mise en forme

def _pc(x, d=1):
    return R._pct(x, d)


def _x(x, d=2):
    return R._n(x, d)


def _d(x, d=3):
    return R._n(x, d) + " $"


def _params_couts(par: dict, frais: float | None = None, gaz: str | None = None) -> dict:
    k = par["couts"]
    return {"near_usd": par["near_usd"], "gaz_tgas": k["gaz_tgas"], "near_par_tgas": k["near_par_tgas"],
            "gaz_paye_par": gaz or k["gaz_paye_par"], "octets_par_pack": k["octets_par_pack"],
            "near_par_octet": k["near_par_octet"], "stockage_paye_par": k["stockage_paye_par"],
            "frais_achat": k["frais_achat"][1] if frais is None else frais, "delta": k["delta"]}


# =========================================================================== analyse d'une variante

def analyser(par: dict, variante: str, pop: dict, cfg: dict) -> dict:
    """Grandeurs exactes d'une variante (tables, couvertures, mythique, arbitrage, stocks) ; cfg au premier prix."""
    tb = construire_tables(par, variante)
    tables = {k: tb[k] for k in TYPES}
    types = construire_types(cfg, tables, par)
    g, gi, r = pop["g_pop"], pop["g_inf"], par["rush"]["part"]
    parts = V.parts_types(g, r)
    cov = V.couverture_globale(tables, parts)
    sans_rush = V.couverture_globale(tables, V.parts_types(g, 0.0))
    loi = V.melange([(tables[k], parts[k]) for k in TYPES])
    P = cfg["prix"]
    c = M.facteur_c(cfg)
    f_fixe = cfg["couts"]["f_burn_fixe"]
    eps = par["couts"]["epsilon"]

    def gain(cov_type, tp_list):
        """Gain « brûle tout, revend le reste » en part du prix, pour une couverture et des types de packs."""
        rev = sum(w * V.revente_collection(tp, cfg) for tp, w in tp_list) / P
        nb = sum(w * _brulables_moyennes(tp, cfg) for tp, w in tp_list)
        return c * cov_type + rev - nb * f_fixe / P

    arbitrage = {
        "normal": gain(tables["normal"].moyenne(), [(types["normal"], 1)]),
        "rush": gain(tables["rush"].moyenne(), [(types["rush"], 1)]),
        "cycle_pitie": gain(V.cycle_pitie(tables, gi), [(types["normal"], 1 - gi), (types["gold"], gi)]),
        "gold_seul": gain(tables["gold"].moyenne(), [(types["gold"], 1)]),
        "borne": 1 - eps,
    }
    # poids du gold pack et du mythique
    myth_in = V.cout_mythique_hors_v(types, parts, 0.0)
    hv = par["mythique"]["hors_v_x_prix"]
    myth_hors = V.cout_mythique_hors_v(types, parts, hv)
    myth_hors_inf = V.cout_mythique_hors_v(types, V.parts_types(gi, r), hv)
    er = {k: V.esperance_raretes(tp) for k, tp in types.items()}
    par_pack = {rr: sum(parts[k] * er[k][rr] for k in TYPES) for rr in ("legendaire", "mythique")}
    stocks = {
        "mythiques_par_pack": par_pack["mythique"], "legendaires_par_pack": par_pack["legendaire"],
        "mythiques_par_pack_sans_gold": er["normal"]["mythique"],
        "legendaires_par_pack_sans_gold": er["normal"]["legendaire"],
        "stock_mythiques": 3 * par["mythique"]["stock_par_mythique"],
        "stock_legendaires": cfg["raretes"]["legendaire"]["effectif"] * par["mythique"]["stock_par_legendaire"],
    }
    stocks["epuisement_mythiques"] = V.epuisement(par_pack["mythique"], stocks["stock_mythiques"])
    stocks["epuisement_legendaires"] = V.epuisement(par_pack["legendaire"], stocks["stock_legendaires"])
    stocks["epuisement_mythiques_sans_gold"] = V.epuisement(er["normal"]["mythique"], stocks["stock_mythiques"])
    # moyenne de la table normale qui donnerait 75 % au global (pour comparaison)
    autre = parts["gold"] * tables["gold"].moyenne() + parts["rush"] * tables["rush"].moyenne()
    normal_pour_global = (par["tables"]["normal"]["cible"] - autre) / parts["normal"]
    return {
        "variante": variante, "sur": par["variantes"][variante]["sur"], "tables": tables,
        "rush_simplifie": tb["_rush_simplifie"], "types": types, "parts": parts,
        "resume": {k: tables[k].resume() for k in TYPES}, "global": V.resume_loi(*loi),
        "couverture": {"normal_seul": tables["normal"].moyenne(), "avec_pitie": sans_rush, "avec_pitie_et_rush": cov,
                       "cycle_pitie_g_inf": V.cycle_pitie(tables, gi),
                       "avec_pitie_g_inf_et_rush": V.couverture_globale(tables, V.parts_types(gi, r)),
                       "effet_gold": parts["gold"] * (tables["gold"].moyenne() - tables["normal"].moyenne()),
                       "effet_rush": parts["rush"] * (tables["rush"].moyenne() - tables["normal"].moyenne()),
                       "part_budget_gold": parts["gold"] * tables["gold"].moyenne() / cov,
                       "normal_pour_75_global": normal_pour_global},
        "mythique": {"dans_v": myth_in, "hors_v": myth_hors, "hors_v_g_inf": myth_hors_inf, "valeur_x_prix": hv},
        "stocks": stocks, "arbitrage": arbitrage, "c": c,
    }


def _brulables_moyennes(tp: V.TypePack, cfg: dict) -> float:
    b = V.proba_brulable(cfg)
    return float(sum(1.0 if f else sum(loi[r] * b[i] for i, r in enumerate(V.RARETES))
                     for loi, f in zip(tp.emplacements, tp.force_brulable)))


# =========================================================================== sections

def section_tables(par: dict, an: dict) -> tuple[str, dict]:
    L = ["## Tables de valeur V", "",
         "V en multiples du prix du pack. Paliers : normal et rush de 20 à 100 % par pas de 5 %, puis de 110 à 200 % "
         "par pas de 10 % (27 paliers) ; gold de 100 à 500 % (18 paliers). Forme lognormale discrétisée "
         f"(σ = {_x(par['tables']['normal']['sigma'], 1)} pour normal et rush, {_x(par['tables']['gold']['sigma'], 1)} "
         "pour le gold), poids entiers sur 1 000 000. (a) : la cible est la moyenne ; (b) : la cible est la médiane.", "",
         "| Variante | Table | Min | Max | q10 | Médiane | q90 | **Moyenne** | Écart-type | Sous 50 % | Au-dessus de 100 % |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = {}
    for v, a in an.items():
        data[v] = {"resume": a["resume"], "global": a["global"], "rush_simplifie": a["rush_simplifie"],
                   "tables": {k: a["tables"][k].en_json() for k in TYPES}}
        for k in TYPES + ["global"]:
            s = a["global"] if k == "global" else a["resume"][k]
            nom = {"normal": "normale", "gold": "gold", "rush": "rush" + (" (= normale)" if a["rush_simplifie"] else ""),
                   "global": "**flux réel** (pitié + rush)"}[k]
            L.append(f"| ({v}) | {nom} | {_pc(s['min'], 0)} | {_pc(s['max'], 0)} | {_pc(s['q10'], 0)} | "
                     f"{_pc(s['q50'], 0)} | {_pc(s['q90'], 0)} | **{_pc(s['moyenne'])}** | {_pc(s['ecart_type'], 0)} | "
                     f"{_pc(s['sous_50'])} | {_pc(s['au_dessus_100'])} |")
    L += ["", "Médiane d'une table discrète : plus petit palier où la fonction de répartition atteint 50 %."]
    return "\n".join(L) + "\n", data


def section_couverture(par: dict, an: dict, pop: dict) -> tuple[str, dict]:
    L = ["## Effet de la pitié, du gold pack et du rush sur la moyenne", "",
         f"Pitié N = {par['pitie']['N']}, p0 = {_pc(par['pitie']['p0'], 0)}, k = {_pc(par['pitie']['k'], 1)} ; "
         f"population de {R._n(pop['joueurs'], 0)} joueurs (médiane {par['population']['mediane']} packs) : "
         f"g_pop = {_pc(pop['g_pop'], 2)} des packs en gold, g_∞ = {_pc(pop['g_inf'], 2)} pour un joueur qui ne s'arrête "
         f"pas (ou un compteur revendable). Rush : {_pc(par['rush']['part'], 0)} des packs non gold. La pitié l'emporte "
         "sur le rush.", "",
         "| Variante | Normal seul | + gold de pitié (g_pop) | **+ rush (flux réel)** | Flux avec g_∞ | Poids du gold | "
         "Poids du rush | Part du budget en gold | Moyenne normale pour 75 % au global |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = {}
    for v, a in an.items():
        c = a["couverture"]
        data[v] = c
        L.append(f"| ({v}) | {_pc(c['normal_seul'])} | {_pc(c['avec_pitie'])} | **{_pc(c['avec_pitie_et_rush'])}** | "
                 f"{_pc(c['avec_pitie_g_inf_et_rush'])} | +{_x(100 * c['effet_gold'], 1)} pts | "
                 f"{'+' if c['effet_rush'] >= 0 else ''}{_x(100 * c['effet_rush'], 1)} pts | {_pc(c['part_budget_gold'], 0)} | "
                 f"{_pc(c['normal_pour_75_global'])} |")
    a = an[par["recommandee"]]
    m = a["mythique"]
    s = a["stocks"]
    L += ["", "### Le mythique du gold pack (20 %)", "",
          f"Un gold pack sort un mythique avec la probabilité {_pc(a['types']['gold'].emplacements[-1]['mythique'], 0)}, "
          f"un pack normal avec {_pc(m['dans_v']['mythiques_par_pack']['normal'], 3)} (1 sur "
          f"{R._n(1 / m['dans_v']['mythiques_par_pack']['normal'], 0)}). En moyenne sur le flux : "
          f"{_pc(s['mythiques_par_pack'], 2)} des packs, soit **1 mythique tous les {R._n(1 / s['mythiques_par_pack'], 0)} "
          f"packs, {R._n(s['mythiques_par_pack'] / s['mythiques_par_pack_sans_gold'], 0)} fois plus qu'avant**.", "",
          "| Lecture | Coût en jetons d'un gold pack | Coût moyen par pack vendu (g_pop) | Avec g_∞ |",
          "|---|---:|---:|---:|",
          f"| **Mythique dans V** (multiplicateur, recommandé) | 0 en plus de V | 0 | 0 |",
          f"| Mythique à valeur fixe hors V ({_x(m['valeur_x_prix'], 1)} × prix, comme en série 3) | "
          f"+{_pc(m['hors_v']['cout_par_pack_du_type']['gold'], 0)} du prix | +{_pc(m['hors_v']['cout_moyen'], 1)} du prix | "
          f"+{_pc(m['hors_v_g_inf']['cout_moyen'], 1)} du prix |", "",
          "**Coût d'un mythique hors V, en points de couverture du flux réel** (part du mythique dans le 5e emplacement "
          "du gold × valeur fixe ; les mythiques des packs normaux et rush comptés aussi) :", "",
          "| Valeur fixe du mythique | " + " | ".join(f"mythique à {_pc(q, 0)} dans le gold"
                                                    for q in par["mythique"]["grille_part_mythique_gold"]) + " |",
          "|---:|" + "---:|" * len(par["mythique"]["grille_part_mythique_gold"])]
    grille = []
    pn = m["dans_v"]["mythiques_par_pack"]
    for M_ in par["mythique"]["grille_jackpot_x_prix"]:
        cells = []
        for q in par["mythique"]["grille_part_mythique_gold"]:
            cout = M_ * (a["parts"]["gold"] * q + a["parts"]["normal"] * pn["normal"] + a["parts"]["rush"] * pn["rush"])
            grille.append({"valeur_x_prix": M_, "part_gold": q, "cout": cout})
            cells.append(f"+{_x(100 * cout, 1)} pts")
        L.append(f"| {_x(M_, 1)} × prix | " + " | ".join(cells) + " |")
    data["grille_jackpot"] = grille
    L += ["",
          f"Hors V à {_x(m['valeur_x_prix'], 1)} × prix, le flux paierait {_pc(a['couverture']['avec_pitie_et_rush'] + m['hors_v']['cout_moyen'], 0)} "
          "du prix en jetons : la maison perd à chaque pack et la ruine est certaine, quelle que soit la réserve. Seul le "
          f"stock borne la perte : {s['stock_mythiques']} mythiques × {_x(m['valeur_x_prix'], 1)} = "
          f"{R._n(s['stock_mythiques'] * m['valeur_x_prix'], 0)} × prix ("
          + " / ".join(_d(s['stock_mythiques'] * m['valeur_x_prix'] * x, 0) for x in par["prix_usd"]) +
          "), dépensés presque tous dans les premiers milliers de packs.", "",
          f"Stock : avec {par['mythique']['stock_par_mythique']} exemplaires par mythique "
          f"(`serie-exemple.json`, {s['stock_mythiques']} au total), les mythiques sont épuisés après "
          f"**{R._n(s['epuisement_mythiques'], 0)} packs** (contre {R._n(s['epuisement_mythiques_sans_gold'], 0)} sans le gold "
          f"pack) ; le 5e emplacement du gold retombe alors sur le légendaire. Légendaires : "
          f"{_pc(s['legendaires_par_pack'], 2)} par pack (contre {_pc(s['legendaires_par_pack_sans_gold'], 2)}), stock de "
          f"{R._n(s['stock_legendaires'], 0)} épuisé après {R._n(s['epuisement_legendaires'], 0)} packs."]
    data["mythique"] = m
    data["stocks"] = s
    return "\n".join(L) + "\n", data


def section_composition(par: dict, an: dict, cfgs: dict, n: int) -> tuple[str, dict]:
    v = par["recommandee"]
    a = an[v]
    mult = par["multiplicateurs"]
    L = ["## Répartition de V entre les cartes", "",
         f"Variante ({v}). Multiplicateurs : " + ", ".join(f"{r} {mult[r]}" for r in V.RARETES) +
         f". {par['catalogue']['brulables_communes']} communes brûlables (sur 91 vivantes) : sans elles, le 5e emplacement "
         "ne peut pas retomber vers le bas et 65 % des packs auraient une rare brûlable comme seule brûlable "
         f"(11 rares brûlables seulement). {R._n(n, 0)} packs par type.", ""]
    data = {}
    x0 = par["prix_usd"][0]
    cfg0 = cfgs[x0]
    seuil = par["couts"]["seuil_brulable_near"] / cfg0["prix"]
    for k in TYPES:
        st = V.stats_composition(a["types"][k], cfg0, mult, n, np.random.default_rng(51 + TYPES.index(k)), seuil)
        data[k] = st
        L += [f"**Pack {k}** : {_x(st['brulables_moyennes'], 2)} brûlables par pack (1 seule : "
              f"{_pc(st['brulables_loi']['1'], 0)}). Cartes par pack : " +
              ", ".join(f"{r} {_x(st['cartes_par_pack'][r], 2)}" for r in V.RARETES if st['cartes_par_pack'][r] > 0) + ".", "",
              "| Rareté | Brûlables par pack | Part de V | Valeur moyenne (× prix) | q10 / médiane / q90 | Min / max | "
              + " | ".join(f"Moyenne à {S3._usd(x)}" for x in par["prix_usd"]) + " |",
              "|---|---:|---:|---:|---:|---:|" + "---:|" * len(par["prix_usd"])]
        for r, e in st["par_rarete"].items():
            L.append(f"| {r} | {_x(e['brulables_par_pack'], 3)} | {_pc(e['part_de_V'], 1)} | {_x(e['moyenne'], 2)} | "
                     f"{_x(e['q10'], 2)} / {_x(e['q50'], 2)} / {_x(e['q90'], 2)} | {_x(e['min'], 3)} / {_x(e['max'], 2)} | "
                     + " | ".join(_d(e["moyenne"] * x, 3) for x in par["prix_usd"]) + " |")
        L += ["", f"Cartes brûlables sous 0,02 NEAR (0,05 $) à {S3._usd(x0)} : {_pc(st['cartes_sous_seuil'], 1)} ; "
              f"plus petite carte : {_x(st['carte_min'], 3)} × prix ({_d(st['carte_min'] * x0, 3)}), "
              f"{_d(st['carte_min'] * par['prix_usd'][-1], 3)} à {S3._usd(par['prix_usd'][-1])}.", ""]
    return "\n".join(L) + "\n", data


def section_marge(par: dict, an: dict) -> tuple[str, dict]:
    k = par["couts"]
    L = ["## Marge par pack", "",
         f"NEAR à {_x(par['near_usd'], 1)} $. Gaz {_x(k['gaz_tgas'], 0)} Tgas = {_d(k['gaz_tgas'] * k['near_par_tgas'] * par['near_usd'])}, "
         "payé par l'équipe (cas prudent) ; stockage ~1 Ko payé par l'acheteur en plus du prix (dépôt) ; achat groupé "
         f"des jetons {_pc(k['frais_achat'][0], 1)} à {_pc(k['frais_achat'][2], 0)} de la valeur (0,75 % au centre). "
         "Couverture = flux réel (pitié g_pop et rush).", "",
         "| Variante | Prix | Couverture | **Marge** | Fourchette (frais 1 % → 0,5 %) | Marge si l'acheteur paie le gaz | "
         "Après réserve δ = 5 % | Débours de l'acheteur | Packs pour 10 NEAR de coûts fixes |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = []
    for v, a in an.items():
        cov = a["couverture"]["avec_pitie_et_rush"]
        for x in par["prix_usd"]:
            p = K.couts_pack(x, cov, _params_couts(par))
            lo = K.couts_pack(x, cov, _params_couts(par, k["frais_achat"][2]))
            hi = K.couts_pack(x, cov, _params_couts(par, k["frais_achat"][0]))
            ga = K.couts_pack(x, cov, _params_couts(par, gaz="acheteur"))
            n10 = K.packs_pour_couts_fixes(10, p["marge_near"])
            data.append({"variante": v, "prix_usd": x, "couverture": cov, "prudent": p, "frais_1": lo, "frais_05": hi,
                         "gaz_acheteur": ga, "packs_10_near": n10})
            L.append(f"| ({v}) | {S3._usd(x)} | {_pc(cov)} | **{_d(p['marge_usd'])} ({_pc(p['marge_part'], 0)})** | "
                     f"{_d(lo['marge_usd'])} à {_d(hi['marge_usd'])} | {_d(ga['marge_usd'])} ({_pc(ga['marge_part'], 0)}) | "
                     f"{_d(p['marge_apres_reserve_near'] * par['near_usd'])} | {_d(p['debourse_acheteur_usd'])} | "
                     f"{R._n(n10, 0)} |")
    L += ["", "Rappel série 3 (couverture 65 %) : 0,057 $ (29 %) à 0,20 $, 0,161 $ (32 %) à 0,50 $."]
    return "\n".join(L) + "\n", data


def section_reserve(par: dict, an: dict, rapide: bool) -> tuple[str, dict]:
    rs = par["reserve"]
    d0 = par["couts"]["delta"]
    div = 10 if rapide else 1
    L = ["## Réserve et ruine", "",
         f"La réserve reçoit (couverture + δ) × prix par vente (δ = {_pc(d0, 0)}) et paie V. Packs indépendants, type tiré "
         "avec les parts du flux réel. R₀ = plus gros V possible + quantile de la plus forte baisse : la réserve peut "
         "toujours payer le pack suivant, sauf avec la probabilité visée. En multiples du prix (tout est proportionnel "
         "au prix), puis en dollars.", "",
         "| Cas | Couverture | Ventes | Trajectoires | V max | R₀ 5 % | **R₀ 1 %** | " +
         " | ".join(f"R₀ 1 % à {S3._usd(x)}" for x in par["prix_usd"]) + " |",
         "|---|---:|---:|---:|---:|---:|---:|" + "---:|" * len(par["prix_usd"])]
    data = []
    cas = [(v, f"({v})", None) for v in an]
    rec = an[par["recommandee"]]
    # mythique hors V, mais petit (5 × prix) et rare dans le gold (2 %) : la seule lecture « jackpot » tenable
    q = par["mythique"]["grille_part_mythique_gold"][-1]
    M_ = par["mythique"]["grille_jackpot_x_prix"][0]
    pn = rec["mythique"]["dans_v"]["mythiques_par_pack"]
    cas.append((par["recommandee"], f"({par['recommandee']}) + mythique hors V à {_x(M_, 0)} × prix, {_pc(q, 0)} du gold",
                {"valeur": M_, "p": {"normal": pn["normal"], "rush": pn["rush"], "gold": q}}))
    for i, (v, nom, jack) in enumerate(cas):
        a = an[v]
        vals, prs = V.loi_paiement(a["tables"], a["parts"], jack)
        moy = float((vals * prs).sum())
        for h in rs["horizons"]:
            n = max(200, rs["trajectoires"][h] // div)
            res = V.reserve_ruine(vals, prs, moy + d0, h, n, tuple(rs["risques"]), seed=61 + 7 * i + h % 97)
            res.update({"cas": nom, "variante": v, "jackpot": jack is not None, "couverture": moy})
            data.append(res)
            L.append(f"| {nom} | {_pc(moy)} | {R._n(h, 0)} | {R._n(n, 0)} | {_x(res['v_max'], 1)} | {_x(res['r0_0.05'], 1)} × P | "
                     f"**{_x(res['r0_0.01'], 1)} × P** | " + " | ".join(_d(res["r0_0.01"] * x, 0) for x in par["prix_usd"]) + " |")
    L += ["", "Série 3 (65 %, mythique 55 × prix, V_cap 60 × prix) : 308 × P pour 1 % sur 100 000 ventes. "
              "La réserve s'effondre parce que V est borné (5 × P au plus) : il n'y a plus de jackpot à couvrir."]
    return "\n".join(L) + "\n", data


def section_arbitrage(par: dict, an: dict) -> tuple[str, dict]:
    L = ["## Borne anti-arbitrage", "",
         "Gain moyen de « j'achète, je brûle tout, je revends le reste », en part du prix : c × couverture + reventes − "
         f"gaz des burns, avec c = {_x(next(iter(an.values()))['c'], 3)} (achat, burn, revente). Borne : "
         f"{_pc(1 - par['couts']['epsilon'], 0)} (ε = {_pc(par['couts']['epsilon'], 0)}). Le cycle de pitié est celui d'un "
         "joueur qui ouvre jusqu'au gold pack (g_∞) ; le gold pack seul n'est choisissable qu'au 20e pack, après 19 packs "
         "normaux.", "",
         "| Variante | Pack normal | Pack rush | Cycle de pitié | Gold pack seul | Borne |", "|---|---:|---:|---:|---:|---:|"]
    data = {}
    for v, a in an.items():
        b = a["arbitrage"]
        data[v] = b

        def f(x):
            return f"**{_pc(x)}**" if x > b["borne"] else _pc(x)
        L.append(f"| ({v}) | {f(b['normal'])} | {f(b['rush'])} | {f(b['cycle_pitie'])} | {_pc(b['gold_seul'], 0)} | "
                 f"{_pc(b['borne'], 0)} |")
    L += ["", "En gras : au-dessus de la borne."]
    return "\n".join(L) + "\n", data


def tables_json(par: dict, a: dict) -> dict:
    gp = par["gold_pack"]
    meta = {
        "variant": a["variante"], "target": f"{a['sur']} {round(par['tables']['normal']['cible'] * 100)} %",
        "rush_simplified": a["rush_simplifie"],
        "expected_coverage": {"base": round(a["tables"]["normal"].moyenne(), 6),
                              "gold": round(a["tables"]["gold"].moyenne(), 6),
                              "rush": round(a["tables"]["rush"].moyenne(), 6),
                              "flow": round(a["couverture"]["avec_pitie_et_rush"], 6)},
    }
    gold = {"slot_min_rarity": [V.NOMS_CONTRAT[r] for r in gp["minimums"]],
            "last_slot_weights_ppm": {V.NOMS_CONTRAT[r]: round(p * 1_000_000) for r, p in gp["dernier"].items()},
            "no_common": True}
    return V.export_json({"base": a["tables"]["normal"], "gold": a["tables"]["gold"], "rush": a["tables"]["rush"]},
                         par["multiplicateurs"], gold, meta)


# =========================================================================== exécution

def lancer(sortie: Path = SORTIE, rapide: bool = False) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    par = charger_parametres()
    cartes = C.charger_catalogue_v2()
    cfgs = {x: construire_config(x, par["near_usd"], par["catalogue"]["brulables_communes"], cartes)
            for x in par["prix_usd"]}
    t0 = time.time()
    pop = population(par)
    print(f"[population : {time.time() - t0:.0f} s, g_pop = {pop['g_pop']:.4f}]", file=sys.stderr)
    an = {v: analyser(par, v, pop, cfgs[par["prix_usd"][0]]) for v in par["variantes"]}
    md, out = [], {"population": pop}

    def faire(nom, f, *args):
        t = time.time()
        texte, data = f(*args)
        (sortie / f"{nom}.md").write_text(texte, encoding="utf-8")
        R.sauver_json(data, sortie / f"{nom}.json")
        out[nom] = data
        md.append(texte)
        print(f"[{nom} : {time.time() - t:.0f} s]", file=sys.stderr)

    faire("tables", section_tables, par, an)
    faire("couverture", section_couverture, par, an, pop)
    faire("composition", section_composition, par, an, cfgs, par["composition"]["packs"] // (10 if rapide else 1))
    faire("marge", section_marge, par, an)
    faire("arbitrage", section_arbitrage, par, an)
    faire("reserve", section_reserve, par, an, rapide)
    for v, a in an.items():
        nom = "tables-valeur.json" if v == par["recommandee"] else f"tables-valeur-{v}.json"
        R.sauver_json(tables_json(par, a), sortie / nom)
    (sortie / "serie4.md").write_text("# Série 4 : valeur aléatoire par pack, gold pack redéfini\n\n" + "\n".join(md),
                                      encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_sim.serie4")
    ap.add_argument("commande", choices=["configs", "run"])
    ap.add_argument("--rapide", action="store_true", help="10 fois moins de tirages et de trajectoires")
    ap.add_argument("--sortie", type=Path, default=SORTIE)
    args = ap.parse_args(argv)
    if args.commande == "configs":
        for c in ecrire_configs():
            print(c)
    else:
        lancer(args.sortie, args.rapide)
    return 0


if __name__ == "__main__":
    sys.exit(main())
