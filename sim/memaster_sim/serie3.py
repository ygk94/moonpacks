"""Série 3 : packs à bas prix (0,15 à 1 $) et mécaniques (pitié, gold rush, rareté par les burns, résurrection).

    python -m memaster_sim.serie3 configs                   # écrit configs/serie3-*.yaml
    python -m memaster_sim.serie3 run [--rapide]            # tout simule, écrit resultats/serie3/

Base : le point recommandé de la série 2 (150 brûlables, facteur 2 entre paliers, hypothèses du jeu C), ramené à un
prix en dollars converti en NEAR au cours `near_usd`. Ce qui dépend du prix (mythique, V_cap, reventes) est mis à
l'échelle du prix, pour que seule la structure des coûts change. Les plafonds par carte (liquidité) restent en NEAR :
à ces prix, ils ne sont jamais atteints.
"""
from __future__ import annotations

import argparse
import copy
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
from . import rarete_burn as RB
from . import resurrection as Rs
from . import rush as Ru
from . import serie2 as S2
from . import simulation as S

RACINE = Path(__file__).resolve().parents[1]
PRIX_USD = [0.15, 0.20, 0.35, 0.50, 1.00]
COUVERTURES = [0.50, 0.65, 0.70]
NEAR_USD = 2.5
TOTAL_BRULABLES = 150
# rapports au prix repris de la série 2 à 5 NEAR : mythique 276 NEAR, V_cap 300 NEAR
MYTHIQUE_X_PRIX = 276 / 5
VCAP_X_PRIX = 300 / 5
CHEMIN_MECANIQUES = RACINE / "configs" / "serie3-mecaniques.yaml"


def construire_config(prix_usd: float, couverture: float, near_usd: float = NEAR_USD, delta: float = 0.05,
                      cartes: list[dict] | None = None, couts: dict | None = None) -> dict:
    cfg = S2.construire_config(TOTAL_BRULABLES, 5, cartes)
    P = K.prix_near(prix_usd, near_usd)
    k = {**K.PARAMS_DEFAUT, **(couts or {}), "near_usd": near_usd}
    echelle = P / 5
    cfg["nom"] = f"Série 3 : {_usd(prix_usd)} ({_n3(P)} NEAR), couverture {round(100 * couverture)} %"
    cfg["prix"] = P
    cfg["prix_usd"] = prix_usd
    cfg["near_usd"] = near_usd
    cfg["beta"] = couverture
    cfg["delta"] = delta
    cfg["v_cap"] = VCAP_X_PRIX * P
    cfg["raretes"]["mythique"]["plafond"] = MYTHIQUE_X_PRIX * P
    for r in cfg["raretes"].values():
        r["revente"] = r["revente"] * echelle
    # burn crédité sur le compte Intents du joueur : seul le gaz du burn reste, payé par le joueur
    cfg["couts"] = {"s_achat": k["frais_achat"], "f_burn": 0.002, "f_burn_fixe": 0.001, "s_vente": 0.03, "phi": 0.05}
    cfg["v_min_brulable"] = 0.02  # 0,05 $ : en dessous, une carte brûlable ne vaut pas le geste
    cfg["ruine"] = {"horizon": 10000, "trajectoires": 10000, "z": 3}
    cfg["serie3"] = {"couts": {x: k[x] for x in ("gaz_tgas", "near_par_tgas", "gaz_paye_par", "octets_par_pack",
                                                 "near_par_octet", "stockage_paye_par", "frais_achat")}}
    M.valider_config(cfg)
    return cfg


def _usd(x: float) -> str:
    return f"{x:.2f} $".replace(".", ",")


def _n3(x: float) -> str:
    return f"{x:.3f}".replace(".", ",")


def nom_fichier(prix_usd: float, couverture: float) -> str:
    return f"serie3-{round(100 * prix_usd):03d}c-{round(100 * couverture):02d}couv"


EN_TETE = """\
# Série 3 (packs à bas prix), générée par `python -m memaster_sim.serie3 configs`. Ne pas éditer à la main.
# Base : serie2-150brul-05near (150 brûlables, facteur 2, jeu C), prix converti à {near} $ le NEAR.
# Mythique = {myth} × prix, V_cap = {vcap} × prix, reventes à l'échelle du prix. Plafonds par carte inchangés (NEAR).
# β = couverture en jetons ; δ = part du prix versée à la réserve (prise sur la marge).
# Les paramètres des mécaniques sont dans serie3-mecaniques.yaml.
"""


def ecrire_configs(dossier: Path = RACINE / "configs") -> list[Path]:
    cartes = C.charger_catalogue_v2()
    out = []
    for x in PRIX_USD:
        for c in COUVERTURES:
            cfg = construire_config(x, c, cartes=cartes)
            chemin = dossier / f"{nom_fichier(x, c)}.yaml"
            texte = EN_TETE.format(near=str(NEAR_USD).replace(".", ","), myth=round(MYTHIQUE_X_PRIX, 1),
                                   vcap=round(VCAP_X_PRIX))
            texte += yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False, width=120)
            chemin.write_text(texte, encoding="utf-8")
            out.append(chemin)
    return out


def charger_mecaniques(chemin: Path = CHEMIN_MECANIQUES) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return yaml.safe_load(f)


# =========================================================================== exécution

def _pc(x, d=1):
    return R._pct(x, d)


def _d(x, d=3):
    """Dollars."""
    return R._n(x, d) + " $"


def _variantes_couts(mec: dict) -> dict[str, dict]:
    k = mec["couts"]
    base = {"gaz_tgas": k["gaz_tgas"], "near_par_tgas": k["near_par_tgas"], "near_par_octet": k["near_par_octet"],
            "frais_achat": k["frais_achat"][1], "delta": k["delta"], "near_usd": mec["near_usd"]}
    o4, o1 = k["octets_par_pack"]
    return {
        "prudent": {**base, "gaz_paye_par": "equipe", "stockage_paye_par": "acheteur", "octets_par_pack": o4},
        "gaz_acheteur": {**base, "gaz_paye_par": "acheteur", "stockage_paye_par": "acheteur", "octets_par_pack": o4},
        "stockage_equipe_4k": {**base, "gaz_paye_par": "equipe", "stockage_paye_par": "equipe", "octets_par_pack": o4},
        "stockage_equipe_1k": {**base, "gaz_paye_par": "equipe", "stockage_paye_par": "equipe", "octets_par_pack": o1},
        "acheteur_1k": {**base, "gaz_paye_par": "equipe", "stockage_paye_par": "acheteur", "octets_par_pack": o1},
    }


def section_rentabilite(mec: dict) -> tuple[str, dict]:
    V = _variantes_couts(mec)
    u = mec["near_usd"]
    k = mec["couts"]
    L = ["## Coûts réels et rentabilité", "",
         f"NEAR à {R._n(u, 2)} $. Gaz : {R._n(k['gaz_tgas'], 0)} Tgas × {R._n(k['near_par_tgas'], 4)} NEAR/Tgas = "
         f"{R._n(K.gaz_near(V['prudent']), 4)} NEAR ({_d(K.gaz_near(V['prudent']) * u)}). Stockage : "
         f"{R._n(k['octets_par_pack'][0], 0)} octets = {R._n(K.stockage_near(V['prudent']), 4)} NEAR "
         f"({_d(K.stockage_near(V['prudent']) * u)}), ou {R._n(k['octets_par_pack'][1], 0)} octets = "
         f"{R._n(K.stockage_near(V['acheteur_1k']), 4)} NEAR ({_d(K.stockage_near(V['acheteur_1k']) * u)}). "
         f"Achat groupé : {_pc(k['frais_achat'][1], 2)} de la couverture (fourchette "
         f"{_pc(k['frais_achat'][0], 1)} à {_pc(k['frais_achat'][2], 0)}).", "",
         "**Couverture 65 %.** « Prudent » : l'équipe paie le gaz (relais, ou par prudence), l'acheteur paie le stockage "
         "en plus du prix. Ancienne marge : tableau de `docs/mecaniques.md` (coûts de 0,05 $).", "",
         "| Prix | NEAR | Ancienne marge | Coûts équipe | **Marge (prudent)** | Marge, gaz payé par l'acheteur | "
         "Après réserve δ = 5 % | Marge si l'équipe paie le stockage, 4 Ko / 1 Ko | Débours acheteur, 4 Ko / 1 Ko |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = {"lignes": []}
    for x in PRIX_USD:
        p, g = K.couts_pack(x, 0.65, V["prudent"]), K.couts_pack(x, 0.65, V["gaz_acheteur"])
        s4, s1 = K.couts_pack(x, 0.65, V["stockage_equipe_4k"]), K.couts_pack(x, 0.65, V["stockage_equipe_1k"])
        a1 = K.couts_pack(x, 0.65, V["acheteur_1k"])
        ancienne = x * 0.35 - 0.05
        L.append(f"| {_usd(x)} | {R._n(p['prix_near'], 3)} | {_d(ancienne)} | {_d(p['cout_equipe_usd'])} | "
                 f"**{_d(p['marge_usd'])} ({_pc(p['marge_part'], 0)})** | {_d(g['marge_usd'])} ({_pc(g['marge_part'], 0)}) | "
                 f"{_d(p['marge_apres_reserve_near'] * u)} | {_d(s4['marge_usd'])} / {_d(s1['marge_usd'])} | "
                 f"{_d(p['debourse_acheteur_usd'])} (+{_pc(p['surcout_affiche_part'], 0)}) / "
                 f"{_d(a1['debourse_acheteur_usd'])} (+{_pc(a1['surcout_affiche_part'], 0)}) |")
        data["lignes"].append({"prudent": p, "gaz_acheteur": g, "stockage_equipe_4k": s4, "stockage_equipe_1k": s1,
                               "acheteur_1k": a1})
    L += ["", "**Marge (prudent) selon la couverture, et frais d'achat de 0,5 à 1 %**", "",
          "| Prix | " + " | ".join(f"couverture {round(100 * c)} %" for c in COUVERTURES) + " |",
          "|---:|" + "---:|" * len(COUVERTURES)]
    for x in PRIX_USD:
        cells = []
        for c in COUVERTURES:
            lo = K.couts_pack(x, c, {**V["prudent"], "frais_achat": k["frais_achat"][2]})
            hi = K.couts_pack(x, c, {**V["prudent"], "frais_achat": k["frais_achat"][0]})
            cells.append(f"{_d(lo['marge_usd'])} à {_d(hi['marge_usd'])} ({_pc(lo['marge_part'], 0)})")
        L.append(f"| {_usd(x)} | " + " | ".join(cells) + " |")
    L += ["", "**Prix de seuil (marge nulle)**", "", "| Variante | " +
          " | ".join(f"couverture {round(100 * c)} %" for c in COUVERTURES) + " |", "|---|" + "---:|" * len(COUVERTURES)]
    noms = {"prudent": "Équipe paie le gaz, acheteur le stockage", "gaz_acheteur": "Acheteur paie gaz et stockage",
            "stockage_equipe_4k": "Équipe paie gaz et stockage (4 Ko)", "stockage_equipe_1k": "Équipe paie gaz et stockage (1 Ko)"}
    data["seuils"] = {}
    for v, nom in noms.items():
        s = [K.prix_seuil_usd(c, V[v]) for c in COUVERTURES]
        data["seuils"][v] = s
        L.append(f"| {nom} | " + " | ".join(_d(x) for x in s) + " |")
    L += ["", "**Packs pour couvrir les coûts fixes** (prudent ; marge avant réserve / après δ = 5 %)", "",
          "| Prix | Couverture | Marge (NEAR) | 5 NEAR | 10 NEAR | 10 NEAR après δ |", "|---:|---:|---:|---:|---:|---:|"]
    data["couts_fixes"] = []
    for c in COUVERTURES:
        for x in PRIX_USD:
            p = K.couts_pack(x, c, V["prudent"])
            n5, n10 = (K.packs_pour_couts_fixes(f, p["marge_near"]) for f in k["couts_fixes_near"])
            n10d = K.packs_pour_couts_fixes(k["couts_fixes_near"][1], p["marge_apres_reserve_near"])
            data["couts_fixes"].append({"prix_usd": x, "couverture": c, "packs_5": n5, "packs_10": n10,
                                        "packs_10_apres_delta": n10d})
            L.append(f"| {_usd(x)} | {round(100 * c)} % | {R._n(p['marge_near'], 4)} | {R._n(n5, 0)} | {R._n(n10, 0)} | "
                     f"{R._n(n10d, 0)} |")
    return "\n".join(L) + "\n", data


def section_base(mec: dict, n_boosters: int) -> tuple[str, dict]:
    u = mec["near_usd"]
    L = ["## Le pack à chaque prix (sans mécanique)", "",
         "Même structure qu'en série 2 (150 brûlables) : tout est proportionnel au prix, sauf les plafonds par carte, "
         "jamais atteints ici.", "",
         "| Prix | Couverture | Adossement moyen | σ / prix | P(≥ 1 brûlable) | Plus petite brûlable | Légendaire brûlable | "
         "Mythique | P(adossement ≥ prix) | Gain « brûle tout » / prix | Borne β |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = []
    for c in COUVERTURES:
        for x in PRIX_USD:
            cfg = construire_config(x, c, u)
            a = M.analytique(cfg)
            s = S.statistiques(cfg, n_boosters, seed=11, avec_beta_max=False)
            vr = a["valeur_par_rarete"]
            P = cfg["prix"]
            ligne = {"prix_usd": x, "couverture": c, "analytique": a, "p_adossement_ge_prix": s["p_adossement_ge_prix"]}
            data.append(ligne)
            vmin = min(v["min"] for v in vr.values())
            L.append(f"| {_usd(x)} | {round(100 * c)} % | {_d(a['esperance_adossement'] * u)} | "
                     f"{R._n(a['sigma_booster'] / P, 2)} | {_pc(1 - a['p_aucune_brulable'])} | {_d(vmin * u, 2)} | "
                     f"{_d(vr['legendaire']['min'] * u, 2)} à {_d(vr['legendaire']['max'] * u, 2)} | "
                     f"{_d(vr['mythique']['max'] * u, 0)} | {_pc(s['p_adossement_ge_prix'])} | "
                     f"{_pc(a['gain_attaquant_moyen'] / P)} | {_pc(a['beta_max_formule'])} |")
    return "\n".join(L) + "\n", data


def _r0(D: np.ndarray, vcap: float, risque: float) -> float:
    return float(vcap + np.quantile(D, 1 - risque))


def section_reserve(mec: dict, rapide: bool) -> tuple[str, dict]:
    u = mec["near_usd"]
    ref = mec["point_reference"]["prix_usd"]
    rs = mec["reserve"]
    div = 10 if rapide else 1
    L = ["## Réserve et ruine", "",
         f"Monte-Carlo de la série 2 : la réserve reçoit (β + δ)·P par vente et paie l'adossement ; ruine = passer sous "
         f"V_cap. Simulé à {_usd(ref)}, puis converti : à structure égale, la réserve est proportionnelle au prix "
         f"(vérifié à 1 $ plus bas).", ""]
    data = {"points": []}
    lignes = []
    for c in COUVERTURES:
        cfg = construire_config(ref, c, u)
        kap = M.kappa(cfg)
        deltas = rs["deltas"] if c == 0.65 else [mec["couts"]["delta"]]
        for h in rs["horizons"]:
            n = max(200, rs["trajectoires"][h] // div)
            D = G.pertes_max_n(cfg, [], kap, [(c + d) * cfg["prix"] for d in deltas], n, h, seed=21)
            for d, Dd in zip(deltas, D):
                pt = {"couverture": c, "delta": d, "horizon": h, "trajectoires": n,
                      "r0_5_x_prix": _r0(Dd, cfg["v_cap"], 0.05) / cfg["prix"],
                      "r0_1_x_prix": _r0(Dd, cfg["v_cap"], 0.01) / cfg["prix"]}
                data["points"].append(pt)
                lignes.append(pt)
    L += ["**Réserve en multiples du prix du pack** (V_cap = 60 × prix compris)", "",
          "| Couverture | δ | Ventes | Trajectoires | R₀ 5 % | R₀ 1 % |", "|---:|---:|---:|---:|---:|---:|"]
    for pt in lignes:
        L.append(f"| {round(100 * pt['couverture'])} % | {_pc(pt['delta'], 0)} | {R._n(pt['horizon'], 0)} | "
                 f"{R._n(pt['trajectoires'], 0)} | {R._n(pt['r0_5_x_prix'], 0)} | {R._n(pt['r0_1_x_prix'], 0)} |")
    d0 = mec["couts"]["delta"]
    L += ["", f"**Réserve en dollars** (δ = {_pc(d0, 0)})", "",
          "| Prix | Couverture | R₀ 5 %, 10 000 ventes | R₀ 1 %, 10 000 | R₀ 5 %, 100 000 | R₀ 1 %, 100 000 |",
          "|---:|---:|---:|---:|---:|---:|"]
    sel = {(p["couverture"], p["horizon"]): p for p in lignes if p["delta"] == d0}
    for c in COUVERTURES:
        for x in PRIX_USD:
            a, b = sel[(c, 10000)], sel[(c, 100000)]
            L.append(f"| {_usd(x)} | {round(100 * c)} % | {_d(a['r0_5_x_prix'] * x, 0)} | {_d(a['r0_1_x_prix'] * x, 0)} | "
                     f"{_d(b['r0_5_x_prix'] * x, 0)} | {_d(b['r0_1_x_prix'] * x, 0)} |")
    # vérification de la proportionnalité à 1 $
    cfg1 = construire_config(1.0, 0.65, u)
    n = max(200, rs["trajectoires"][10000] // div)
    D1 = G.pertes_max_n(cfg1, [], M.kappa(cfg1), [(0.65 + d0) * cfg1["prix"]], n, 10000, seed=22)[0]
    v1 = _r0(D1, cfg1["v_cap"], 0.01) / cfg1["prix"]
    data["verification_1usd_r0_1_x_prix"] = v1
    L += ["", f"Vérification à 1 $ (65 %, 10 000 ventes) : R₀ 1 % = {R._n(v1, 0)} × prix, contre "
              f"{R._n(sel[(0.65, 10000)]['r0_1_x_prix'], 0)} × prix à {_usd(ref)}."]
    return "\n".join(L) + "\n", data


# --------------------------------------------------------------------------- pitié

def _population(mec: dict, seed: int = 31) -> np.ndarray:
    pp = mec["pitie"]["population"]
    return Pi.packs_par_joueur(pp["joueurs"], np.random.default_rng(seed), pp["mediane"], pp["sigma"], pp["maximum"])


def section_pitie(mec: dict) -> tuple[str, dict]:
    u = mec["near_usd"]
    ref = mec["point_reference"]
    cfg = construire_config(ref["prix_usd"], ref["couverture"], u)
    P = cfg["prix"]
    pk = _population(mec)
    pp = mec["pitie"]["population"]
    tables = {n: G.table_or(cfg, f) for n, f in mec["pitie"]["tables"].items()}
    L = ["## Compteur de pitié", "",
         f"Population : {R._n(pp['joueurs'], 0)} joueurs, packs par joueur lognormaux (médiane {pp['mediane']}, "
         f"σ = {R._n(pp['sigma'], 1)}, au plus {R._n(pp['maximum'], 0)}). Point {_usd(ref['prix_usd'])}, {round(100 * ref['couverture'])} %. "
         "κ est calibré sur g_∞ (colonne « couverture std / or »), puis on lit la couverture réalisée dans la "
         "population (g_pop).", "",
         "| N | p0 | k | g_∞ (1 sur) | g_pop | Joueurs sans gold | Gold garantis | Table | Couverture std / or | "
         "Part du budget | P(≥ 1 brûlable) en or | Gain « brûle tout » d'un gold / prix | Couverture réalisée (g_pop) |",
         "|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|"]
    data = {"grille": []}
    for N, p0, k in mec["pitie"]["grille"]:
        gi = Pi.g_stationnaire(p0, k, N)
        pop = Pi.simuler_population(pk, p0, k, N, np.random.default_rng(32))
        for nt, t_or in tables.items():
            c = G.calibrer(cfg, t_or, gi)
            reel = G.couverture_a_kappa(cfg, t_or, pop["g_pop"], c["kappa"])
            data["grille"].append({"N": N, "p0": p0, "k": k, "table": nt, "g_inf": gi, "population": pop,
                                   "calibrage": c, "couverture_realisee": reel})
            L.append(f"| {N} | {_pc(p0, 0)} | {_pc(k, 1)} | {R._n(1 / gi, 1)} | {_pc(pop['g_pop'], 2)} | "
                     f"{_pc(pop['part_joueurs_sans_gold'], 0)} | {_pc(pop['part_gold_garantis'], 0)} | {nt} | "
                     f"{_pc(c['couverture_std'])} / {_pc(c['couverture_or'], 0)} | {_pc(c['part_budget_or'], 0)} | "
                     f"{_pc(c['p_brulable_or'], 0)} | {_pc(c['gain_attaquant_or'] / P, 0)} | {_pc(reel)} |")
    # proposition : calibrée sur la population, avec la dérive vers g_∞
    pr = mec["pitie"]["proposition"]
    N, p0, k = pr["N"], pr["p0"], pr["k"]
    t_or = tables[pr["table"]]
    gi = Pi.g_stationnaire(p0, k, N)
    pop = Pi.simuler_population(pk, p0, k, N, np.random.default_rng(32))
    cpop = G.calibrer(cfg, t_or, pop["g_pop"])
    derive = G.couverture_a_kappa(cfg, t_or, gi, cpop["kappa"])
    # sensibilité à la population : petits joueurs / baleines
    sens = []
    for med, sig in ((2, 1.0), (4, 1.4), (8, 1.6), (20, 1.8)):
        pk2 = Pi.packs_par_joueur(pp["joueurs"], np.random.default_rng(33), med, sig, pp["maximum"])
        p2 = Pi.simuler_population(pk2, p0, k, N, np.random.default_rng(34))
        sens.append({"mediane": med, "sigma": sig, "g_pop": p2["g_pop"], "packs_moyens": p2["packs_moyens"],
                     "couverture": G.couverture_a_kappa(cfg, t_or, p2["g_pop"], cpop["kappa"])})
    # réserve : sans pitié contre avec pitié (mélange indépendant à g_pop)
    apport = (cfg["beta"] + cfg["delta"]) * P
    n = mec["_trajectoires_pitie"]
    D0 = G.pertes_max_n(cfg, [], M.kappa(cfg), [apport], n, 10000, seed=35)[0]
    D1 = G.pertes_max_n(cfg, [(t_or, pop["g_pop"])], cpop["kappa"], [apport], n, 10000, seed=35)[0]
    r0, r1 = _r0(D0, cfg["v_cap"], 0.01), _r0(D1, cfg["v_cap"], 0.01)
    vr = M.analytique(cfg)["valeur_par_rarete"]
    vmin_std = min(v["min"] for v in vr.values()) * cpop["kappa"] / M.kappa(cfg)
    data["proposition"] = {"N": N, "p0": p0, "k": k, "table": pr["table"], "facteurs": mec["pitie"]["tables"][pr["table"]],
                           "g_inf": gi, "population": pop, "calibrage_pop": cpop, "couverture_si_g_inf": derive,
                           "sensibilite_population": sens, "r0_1_sans_pitie": r0, "r0_1_avec_pitie": r1,
                           "trajectoires": n, "duree_moyenne_cycle": Pi.duree_moyenne_cycle(p0, k, N),
                           "part_cycles_garantis": Pi.part_garantie(p0, k, N)}
    L += ["", f"**Proposition : N = {N}, p0 = {_pc(p0, 0)}, k = {_pc(k, 1)}, table « {pr['table']} »** "
              f"(probabilités × {', '.join(f'{r} {R._n(v, 1)}' for r, v in mec['pitie']['tables'][pr['table']].items())}), "
              "κ calibré sur la population.", "",
          "| Grandeur | Valeur |", "|---|---:|",
          f"| Cycle moyen entre deux gold packs | {R._n(Pi.duree_moyenne_cycle(p0, k, N), 1)} packs |",
          f"| Cycles qui vont jusqu'à la garantie | {_pc(Pi.part_garantie(p0, k, N), 0)} |",
          f"| g_∞ / g_pop | {_pc(gi, 2)} / {_pc(pop['g_pop'], 2)} |",
          f"| Joueurs qui ne voient aucun gold pack | {_pc(pop['part_joueurs_sans_gold'], 0)} |",
          f"| Packs ouverts par les 5 % plus gros joueurs | {_pc(pop['part_packs_top5'], 0)} |",
          f"| Couverture d'un pack standard / d'un gold pack | {_pc(cpop['couverture_std'])} / {_pc(cpop['couverture_or'], 0)} |",
          f"| Valeur moyenne d'un pack standard / gold | {_d(cpop['esperance_std'] * u)} / {_d(cpop['esperance_or'] * u)} |",
          f"| Part du budget jetons prise par les gold packs | {_pc(cpop['part_budget_or'], 0)} |",
          f"| P(≥ 1 brûlable), standard / gold | {_pc(cpop['p_brulable_std'], 0)} / {_pc(cpop['p_brulable_or'], 0)} |",
          f"| Plus petite brûlable (κ baisse de {_pc(1 - cpop['kappa'] / cpop['kappa_sans_or'], 0)}) | {_d(vmin_std * u, 2)} |",
          f"| Couverture si tous les compteurs servent (g_∞ : baleines, compteur revendable) | {_pc(derive)} |",
          f"| R₀ 1 % sur 10 000 ventes, sans / avec pitié ({R._n(n, 0)} trajectoires) | {_d(r0 * u, 0)} / {_d(r1 * u, 0)} |",
          "", "**Sensibilité à la population** (κ de la proposition)", "",
          "| Médiane | σ | Packs moyens par joueur | g_pop | Couverture réalisée |", "|---:|---:|---:|---:|---:|"]
    for s in sens:
        L.append(f"| {s['mediane']} | {R._n(s['sigma'], 1)} | {R._n(s['packs_moyens'], 1)} | {_pc(s['g_pop'], 2)} | "
                 f"{_pc(s['couverture'])} |")
    return "\n".join(L) + "\n", data


# --------------------------------------------------------------------------- gold rush

def facteurs_echelle(base: dict[str, float], s: float) -> dict[str, float]:
    """Facteurs 1 + s·(f − 1) : s = 0 donne la table standard, s = 1 la table de base."""
    return {r: 1 + s * (f - 1) for r, f in base.items()}


def table_rush_pour_couverture(cfg: dict, t_pitie: dict, g_p: float, g_r: float, base: dict[str, float],
                               cible: float) -> tuple[dict, dict, float]:
    """Table du rush (facteurs de `base` mis à l'échelle) dont la couverture vaut `cible`, κ calibré sur le mélange."""
    def evaluer(s):
        t_r = G.table_or(cfg, facteurs_echelle(base, s))
        kap = M.kappa(G.melanger_n(cfg, [(t_pitie, g_p * (1 - g_r)), (t_r, g_r)]))
        return t_r, kap, M.esperance_adossement(M.construire_tables(t_r), kap) / cfg["prix"]
    lo, hi = 0.0, 1.0
    if evaluer(hi)[2] < cible:
        return (*evaluer(hi)[:2], hi)
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if evaluer(mid)[2] < cible else (lo, mid)
    t_r, kap, _ = evaluer(lo)
    return t_r, kap, lo


def _couv(cfg: dict, tables: list[tuple[dict, float]], kap: float) -> float:
    """Couverture moyenne réalisée d'un flux (std + tables spéciales de parts g) à κ donné."""
    reste = 1 - sum(g for _, g in tables)
    e = reste * M.esperance_adossement(M.construire_tables(cfg), kap)
    e += sum(g * M.esperance_adossement(M.construire_tables(t), kap) for t, g in tables)
    return e / cfg["prix"]


def section_rush(mec: dict, pitie: dict, rapide: bool) -> tuple[str, dict]:
    u = mec["near_usd"]
    ref = mec["point_reference"]
    cfg = construire_config(ref["prix_usd"], ref["couverture"], u)
    P = cfg["prix"]
    rc = mec["rush"]
    n_traj = max(3, rc["trajectoires"] // (4 if rapide else 1))
    pr = pitie["proposition"]
    t_p = G.table_or(cfg, pr["facteurs"])
    g_p = pr["population"]["g_pop"]
    couts = _variantes_couts(mec)["prudent"]
    cout_fixe = K.couts_pack(ref["prix_usd"], ref["couverture"], couts)["cout_equipe_near"]
    b = rc["base"]
    L = ["## Gold rush", "",
         f"Flux de base : {b['lambda_base_h']} packs/h (cycle de ±{_pc(b['amplitude_cycle'], 0)} sur la journée), "
         f"{R._n(b['pics_par_jour'], 1)} pic par jour en moyenne (× {R._n(b['pic_mult'], 0)} pendant {b['pic_duree_s'] // 60} min), "
         f"demande × {1 + b['boost_rush']:g} pendant un rush. Fenêtre glissante {b['fenetre_s'] // 60} min, rush de "
         f"{R._n(b['duree_blocs'], 0)} blocs ({R._n(b['duree_blocs'] * b['temps_bloc_s'] / 60, 0)} min à {R._n(b['temps_bloc_s'], 1)} s "
         f"par bloc). {n_traj} trajectoires de {b['jours']} jours par case.", "",
         "| Règle | Trafic | Packs / jour | Rushs / jour | Temps en rush | g_rush (part des packs en or) | g_rush p95 |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    data = {"grille": []}
    sims = {}
    for nom, regle in rc["regles"].items():
        for tr in rc["trafics"]:
            prm = {**b, **regle, "lambda_base_h": b["lambda_base_h"] * tr}
            r = Ru.simuler(prm, n_traj, seed=41)
            sims[(nom, tr)] = r
            m = r["moyennes"]
            data["grille"].append({"regle": nom, "trafic": tr, **m})
            L.append(f"| {nom} | × {R._n(tr, 1)} | {R._n(m['packs_par_jour'], 0)} | {R._n(m['rush_par_jour'], 2)} | "
                     f"{_pc(m['temps_en_rush'], 1)} | {_pc(m['g_rush'], 1)} | {_pc(m['g_rush_p95'], 1)} |")
    # table du rush sous la borne anti-arbitrage
    prop = rc["proposition"]
    g_r = sims[(prop, 1)]["moyennes"]["g_rush"]
    t_r, kap, s = table_rush_pour_couverture(cfg, t_p, g_p, g_r, pr["facteurs"], rc["couverture_cible_table_rush"])
    f_r = facteurs_echelle(pr["facteurs"], s)
    gain_r = float((M.proba_issues_booster(M.construire_tables(t_r)) @
                    M.gain_attaquant_issues(t_r, M.construire_tables(t_r), kap)).sum()) / P
    gain_or = float((M.proba_issues_booster(M.construire_tables(t_p)) @
                     M.gain_attaquant_issues(t_p, M.construire_tables(t_p), kap)).sum()) / P
    cov_std = M.esperance_adossement(M.construire_tables(cfg), kap) / P
    cov_or = M.esperance_adossement(M.construire_tables(t_p), kap) / P
    cov_r = M.esperance_adossement(M.construire_tables(t_r), kap) / P
    data["table_rush"] = {"facteurs": f_r, "echelle": s, "g_rush_prevu": g_r, "kappa": kap, "couverture_std": cov_std,
                          "couverture_or": cov_or, "couverture_rush": cov_r, "gain_rush_sur_prix": gain_r,
                          "gain_or_sur_prix": gain_or}
    # marge selon le trafic : κ calibré pour le trafic prévu (× 1)
    L += ["", f"**Effet sur la marge** ({_usd(ref['prix_usd'])}, κ calibré pour le trafic prévu × 1 et la pitié proposée). "
              f"« Table or » : le rush reprend la table de pitié ; « table rush » : facteurs × "
              f"{', '.join(f'{r} {R._n(v, 2)}' for r, v in f_r.items())}, couverture {_pc(cov_r, 0)}.", "",
          "| Règle | Table pendant le rush | Trafic | g_rush | Couverture réalisée | Marge / pack | Marge sur 30 jours |",
          "|---|---|---:|---:|---:|---:|---:|"]
    data["marges"] = []
    for nom in rc["regles"]:
        g_prevu = sims[(nom, 1)]["moyennes"]["g_rush"]
        for nt, t_x in (("or", t_p), ("rush", t_r)):
            k_x = M.kappa(G.melanger_n(cfg, [(t_p, g_p * (1 - g_prevu)), (t_x, g_prevu)]))
            for tr in rc["trafics"]:
                m = sims[(nom, tr)]["moyennes"]
                cov = _couv(cfg, [(t_p, g_p * (1 - m["g_rush"])), (t_x, m["g_rush"])], k_x)
                marge = P * (1 - cov) - cout_fixe
                data["marges"].append({"regle": nom, "table": nt, "trafic": tr, "g_rush": m["g_rush"],
                                       "couverture": cov, "marge_near": marge, "marge_30j_near": marge * m["packs"]})
                L.append(f"| {nom} | {nt} | × {R._n(tr, 1)} | {_pc(m['g_rush'], 1)} | {_pc(cov)} | {_d(marge * u)} | "
                         f"{_d(marge * m['packs'] * u, 0)} |")
    # réserve : gold packs groupés (suites simulées) contre indépendants
    n = mec["_trajectoires_pitie"]
    apport = (cfg["beta"] + cfg["delta"]) * P
    res = {}
    for nom, tr in ((prop, 1), ("fixe", 2)):
        suites = np.concatenate(sims[(nom, tr)]["suites"])
        g_obs = float(suites.mean())

        def drapeaux(rng, k, h, suites=suites):
            debuts = rng.integers(0, suites.size - h, k)
            F = suites[debuts[:, None] + np.arange(h)[None, :]]
            return np.where(F, 2, np.where(rng.random((k, h)) < g_p, 1, 0))
        k_x = M.kappa(G.melanger_n(cfg, [(t_p, g_p * (1 - g_obs)), (t_r, g_obs)]))
        Dg = G.pertes_max_n(cfg, [(t_p, g_p), (t_r, 0)], k_x, [apport], n, 10000, seed=43, drapeaux=drapeaux)[0]
        Di = G.pertes_max_n(cfg, [(t_p, g_p * (1 - g_obs)), (t_r, g_obs)], k_x, [apport], n, 10000, seed=43)[0]
        res[f"{nom}_x{tr:g}"] = {"g_rush": g_obs, "r0_1_groupes": _r0(Dg, cfg["v_cap"], 0.01),
                                 "r0_1_independants": _r0(Di, cfg["v_cap"], 0.01)}
    data["reserve"] = res
    L += ["", f"**Réserve** (R₀ 1 % sur 10 000 ventes, table rush, κ recalibré sur la part observée, {R._n(n, 0)} "
              "trajectoires). Les gold packs d'un rush arrivent groupés : on compare au même nombre de gold packs "
              "répartis au hasard.", "",
          "| Cas | g_rush | R₀ 1 %, rush groupés | R₀ 1 %, mêmes gold packs indépendants |", "|---|---:|---:|---:|"]
    for nom, x in res.items():
        L.append(f"| {nom} | {_pc(x['g_rush'], 1)} | {_d(x['r0_1_groupes'] * u, 0)} | {_d(x['r0_1_independants'] * u, 0)} |")
    L += ["", f"**Arbitrage pendant un rush.** Gain moyen « j'achète, je brûle tout » d'un pack : {_pc(gain_or, 0)} "
              f"du prix avec la table or, {_pc(gain_r, 0)} avec la table rush (borne : {_pc(1 - cfg['epsilon'], 0)}). "
              "Au-dessus de 100 %, chaque pack acheté pendant un rush rapporte en moyenne ; un gros joueur a alors "
              "intérêt à déclencher le rush lui-même."]
    return "\n".join(L) + "\n", data


# --------------------------------------------------------------------------- rareté pilotée par les burns

def section_rarete(mec: dict) -> tuple[str, dict]:
    u = mec["near_usd"]
    ref = mec["point_reference"]
    cfg = construire_config(ref["prix_usd"], ref["couverture"], u)
    rb = mec["rarete_burn"]
    L = ["## Rareté pilotée par les burns", "",
         f"Poids effectif = poids × en circulation / émises, sur {R._n(rb['horizon'], 0)} packs, délai moyen avant burn "
         f"{R._n(rb['delai_packs'], 0)} packs. « formule_brute » : la part perdue revient à toute la rareté, κ fixe. "
         "« formule_recalibree » : idem, κ recalculé pour tenir β. « entre_brulables » : la part perdue revient aux "
         "autres brûlables de la rareté. Le rapport (σ fin / σ début)² donne l'ordre de grandeur de la réserve "
         "(formule normale).", "",
         "| Variante | Taux de burn | Couverture finale | Couverture moyenne | Brûlables / pack, début → fin | κ fin / début | "
         "(σ fin / σ début)² | Coins au plancher (sur 150) | Jetons bloqués à la fin |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = []
    for nom, v in rb["variantes"].items():
        for tb in rb["taux_burn"]:
            r = RB.simuler(cfg, {**v, "taux_burn": tb, "horizon": rb["horizon"], "lot": rb["lot"],
                                 "delai_packs": rb["delai_packs"]})
            r.pop("histo")
            data.append({"variante": nom, **r})
            L.append(f"| {nom} | {_pc(tb, 0)} | {_pc(r['couverture_finale'])} | {_pc(r['couverture_moyenne'])} | "
                     f"{R._n(r['brulables_par_pack_initial'], 3)} → {R._n(r['brulables_par_pack_final'], 3)} | "
                     f"{R._n(r['kappa_final_rel'], 2)} | {R._n((r['sigma_final'] / r['sigma_initial']) ** 2, 2)} | "
                     f"{r['coins_au_plancher']} | {_d(r['engagements_finaux_near'] * u, 0)} |")
    return "\n".join(L) + "\n", data


# --------------------------------------------------------------------------- résurrection

def section_resurrection(mec: dict) -> tuple[str, dict]:
    u = mec["near_usd"]
    ref = mec["point_reference"]
    cfg = construire_config(ref["prix_usd"], ref["couverture"], u)
    P = cfg["prix"]
    rz = mec["resurrection"]
    cartes = C.charger_catalogue_v2()
    morts = Rs.coins_morts(cartes)
    sans_communes = {**morts, "commune": 0}
    L = ["## Résurrection des coins morts", "",
         f"Coins morts du catalogue v2 (hors arnaques) : {R._n(morts['commune'], 0)} communes, {morts['epique']} épiques, "
         f"{morts['legendaire']} légendaires. {R._n(rz['packs_par_mois'], 0)} packs par mois. Un exemplaire ressuscité "
         f"reçoit la valeur moyenne d'une brûlable de sa rareté, achetée avec {_pc(rz['surcout_achat'], 0)} de surcoût. "
         "Le coût rapporté au chiffre d'affaires ne dépend pas du volume (exemplaires et ventes croissent ensemble), "
         "mais il croît avec la durée.", "",
         "| p par coin et par an | Durée | Résurrections (moy. / p99) | Coût moyen | Coût p99 | En part du prix, moyen / p99 | "
         "Dont communes | Sans les communes, p99 |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    data = {"grille": [], "morts": morts}
    for pa in rz["p_an"]:
        for mois in rz["mois"]:
            prm = {"p_an": pa, "mois": mois, "packs_par_mois": rz["packs_par_mois"], "surcout_achat": rz["surcout_achat"]}
            r = Rs.simuler(cfg, morts, prm)
            r2 = Rs.simuler(cfg, sans_communes, prm)
            data["grille"].append({"p_an": pa, "mois": mois, "complet": r, "sans_communes": r2})
            pc = r["cout_moyen_part_prix_par_rarete"].get("commune", 0) / max(r["cout_moyen_par_pack_part_prix"], 1e-12)
            L.append(f"| {_pc(pa, 1)} | {mois} mois | {R._n(r['resurrections_moyennes'], 1)} / "
                     f"{R._n(r['resurrections_p99'], 0)} | {_d(r['cout_moyen_near'] * u, 0)} | "
                     f"{_d(r['cout_p99_near'] * u, 0)} | {_pc(r['cout_moyen_par_pack_part_prix'])} / "
                     f"{_pc(r['cout_p99_par_pack_part_prix'])} | {_pc(pc, 0)} | {_pc(r2['cout_p99_par_pack_part_prix'], 2)} |")
    # règle de plafond : fonds ρ, enveloppe = fonds / résurrections p99
    ventes = rz["packs_par_mois"] * 12
    fonds = rz["rho"] * P * ventes
    ex = Rs.exemplaires_par_carte_et_pack(cfg)
    vals = Rs.valeur_brulable_par_rarete(cfg)
    regle = []
    for pa in rz["p_an"]:
        r = Rs.simuler(cfg, morts, {"p_an": pa, "mois": 12, "packs_par_mois": rz["packs_par_mois"]})
        env = fonds / max(1.0, r["resurrections_p99"])
        regle.append({"p_an": pa, "enveloppe_near": env,
                      "valeur_commune_fin": env / (ex["commune"] * ventes),
                      "valeur_epique_fin": env / (ex["epique"] * ventes),
                      "couverte_commune_fin": env / (ex["commune"] * ventes) / vals["commune"],
                      "couverte_epique_fin": min(1.0, env / (ex["epique"] * ventes) / vals["epique"])})
    rho_ep = Rs.rho_pour_risque(cfg, sans_communes, {"p_an": 0.02, "mois": 12, "packs_par_mois": rz["packs_par_mois"],
                                                     "surcout_achat": rz["surcout_achat"]})
    data["regle_enveloppe"] = regle
    data["rho_sans_communes_p2"] = rho_ep
    L += ["", f"**Règle de plafond : enveloppe fixe par résurrection, fonds à {_pc(rz['rho'], 0)} du prix** "
              f"({_d(fonds * u, 0)} sur 12 mois). Enveloppe = fonds / nombre de résurrections p99, partagée entre les "
              "exemplaires en circulation. Valeur reçue par exemplaire au bout de 12 mois :", "",
          "| p par an | Enveloppe | Par commune (part de la valeur pleine) | Par épique (part de la valeur pleine) |",
          "|---:|---:|---:|---:|"]
    for x in regle:
        L.append(f"| {_pc(x['p_an'], 1)} | {_d(x['enveloppe_near'] * u, 0)} | {_d(x['valeur_commune_fin'] * u, 4)} "
                 f"({_pc(x['couverte_commune_fin'], 1)}) | {_d(x['valeur_epique_fin'] * u, 3)} "
                 f"({_pc(x['couverte_epique_fin'], 0)}) |")
    L += ["", f"Sans les communes, payer la pleine valeur à p = 2 %/an demande un fonds de {_pc(rho_ep, 2)} du prix "
              "(p99, 12 mois)."]
    return "\n".join(L) + "\n", data


# --------------------------------------------------------------------------- synthèse

def section_synthese(mec: dict, pitie: dict, rush: dict, rapide: bool) -> tuple[str, dict]:
    """Pitié et rush proposés ensemble, aux prix d'entrée et standard."""
    u = mec["near_usd"]
    pr = pitie["proposition"]
    tr = rush["table_rush"]
    g_p, g_r = pr["population"]["g_pop"], tr["g_rush_prevu"]
    V = _variantes_couts(mec)
    n = mec["_trajectoires_pitie"]
    L = ["## Synthèse : pitié et rush proposés, ensemble", "",
         f"Pitié N = {pr['N']}, p0 = {_pc(pr['p0'], 0)}, k = {_pc(pr['k'], 1)} (g_pop = {_pc(g_p, 2)}) ; rush à palier "
         f"relatif avec 6 h de pause (g_rush ≈ {_pc(g_r, 1)}), table rush à {_pc(tr['couverture_rush'], 0)}. "
         f"Couverture moyenne visée {_pc(0.65, 0)}, δ = {_pc(mec['couts']['delta'], 0)}. R₀ sur {R._n(n, 0)} trajectoires.", "",
         "| Prix | Couverture std / gold / rush | Marge / pack (prudent) | Débours acheteur 4 Ko / 1 Ko | "
         "R₀ 1 %, 10 000 ventes | R₀ 1 %, 100 000 ventes | Packs pour 10 NEAR de coûts fixes |",
         "|---:|---:|---:|---:|---:|---:|---:|"]
    data = []
    for x in (0.20, 0.50, 1.00):
        cfg = construire_config(x, 0.65, u)
        t_p = G.table_or(cfg, pr["facteurs"])
        t_r = G.table_or(cfg, tr["facteurs"])
        autres = [(t_p, g_p * (1 - g_r)), (t_r, g_r)]
        kap = M.kappa(G.melanger_n(cfg, autres))
        P = cfg["prix"]
        covs = [M.esperance_adossement(M.construire_tables(c), kap) / P for c in (cfg, t_p, t_r)]
        apport = (cfg["beta"] + cfg["delta"]) * P
        r0 = {}
        for h, nn in ((10000, n), (100000, max(200, n // 5))):
            D = G.pertes_max_n(cfg, autres, kap, [apport], nn, h, seed=51)[0]
            r0[h] = _r0(D, cfg["v_cap"], 0.01)
        c4, c1 = K.couts_pack(x, 0.65, V["prudent"]), K.couts_pack(x, 0.65, V["acheteur_1k"])
        fixes = K.packs_pour_couts_fixes(mec["couts"]["couts_fixes_near"][1], c4["marge_near"])
        data.append({"prix_usd": x, "couvertures": covs, "kappa": kap, "marge_usd": c4["marge_usd"],
                     "debours_4k_usd": c4["debourse_acheteur_usd"], "debours_1k_usd": c1["debourse_acheteur_usd"],
                     "r0_1_10k_usd": r0[10000] * u, "r0_1_100k_usd": r0[100000] * u, "packs_couts_fixes": fixes})
        L.append(f"| {_usd(x)} | {_pc(covs[0])} / {_pc(covs[1], 0)} / {_pc(covs[2], 0)} | {_d(c4['marge_usd'])} "
                 f"({_pc(c4['marge_part'], 0)}) | {_d(c4['debourse_acheteur_usd'])} / {_d(c1['debourse_acheteur_usd'])} | "
                 f"{_d(r0[10000] * u, 0)} | {_d(r0[100000] * u, 0)} | {R._n(fixes, 0)} |")
    return "\n".join(L) + "\n", data


SECTIONS = ["rentabilite", "base", "reserve", "pitie", "rush", "rarete-burn", "resurrection", "synthese"]


def lancer(sortie: Path, rapide: bool = False, seulement: list[str] | None = None) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    mec = charger_mecaniques()
    mec["_trajectoires_pitie"] = 1000 if rapide else 10000
    seulement = seulement or SECTIONS
    out, md = {}, []

    def faire(nom, f, *a):
        t0 = time.time()
        texte, data = f(*a)
        (sortie / f"{nom}.md").write_text(texte, encoding="utf-8")
        R.sauver_json(data, sortie / f"{nom}.json")
        out[nom] = data
        md.append(texte)
        print(f"[{nom} : {time.time() - t0:.0f} s]", file=sys.stderr)

    if "rentabilite" in seulement:
        faire("rentabilite", section_rentabilite, mec)
    if "base" in seulement:
        faire("base", section_base, mec, 100_000 if rapide else 1_000_000)
    if "reserve" in seulement:
        faire("reserve", section_reserve, mec, rapide)
    if {"pitie", "rush", "synthese"} & set(seulement):
        faire("pitie", section_pitie, mec)
    if {"rush", "synthese"} & set(seulement):
        faire("rush", section_rush, mec, out["pitie"], rapide)
    if "rarete-burn" in seulement:
        faire("rarete-burn", section_rarete, mec)
    if "resurrection" in seulement:
        faire("resurrection", section_resurrection, mec)
    if "synthese" in seulement:
        faire("synthese", section_synthese, mec, out["pitie"], out["rush"], rapide)
    if set(seulement) == set(SECTIONS):
        (sortie / "serie3.md").write_text("# Série 3 : packs à bas prix et mécaniques\n\n" + "\n".join(md),
                                          encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="memaster_sim.serie3")
    ap.add_argument("commande", choices=["configs", "run"])
    ap.add_argument("--rapide", action="store_true", help="10 fois moins de trajectoires (pour essayer)")
    ap.add_argument("--sections", nargs="*", choices=SECTIONS)
    ap.add_argument("--sortie", type=Path, default=RACINE / "resultats" / "serie3")
    args = ap.parse_args(argv)
    if args.commande == "configs":
        for c in ecrire_configs():
            print(c)
    else:
        lancer(args.sortie, args.rapide, args.sections)
    return 0


if __name__ == "__main__":
    sys.exit(main())
