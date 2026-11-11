"""Exécution complète d'une config, grilles de sensibilité, sortie en markdown et en JSON."""
from __future__ import annotations

import json
import math
from pathlib import Path

from . import modele as M
from . import simulation as S


def _pct(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f} %".replace(".", ",")


def _n(x: float, d: int = 2) -> str:
    if x is None or (isinstance(x, float) and math.isinf(x)):
        return "n/a"
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def _cote(p: float) -> str:
    return "jamais" if p <= 0 else f"1 sur {_n(1 / p, 0)}"


def executer(cfg: dict, n_boosters: int, trajectoires: int | None, seed: int = 1) -> dict:
    return {
        "nom": cfg["nom"],
        "config": cfg,
        "analytique": M.analytique(cfg),
        "simulation": S.statistiques(cfg, n_boosters, seed),
        "ruine": S.ruine(cfg, trajectoires, seed=seed + 1),
        "cartes": M.frequences_par_carte(cfg),
    }


def markdown(res: dict) -> str:
    cfg, a, s, r = res["config"], res["analytique"], res["simulation"], res["ruine"]
    P, usd = cfg["prix"], cfg.get("near_usd", 0)
    L = [f"### {res['nom']}", ""]
    L += ["| Grandeur | Formule exacte | Monte-Carlo |", "|---|---:|---:|"]
    L.append(f"| κ (NEAR par unité de poids) | {_n(a['kappa'], 3)} | |")
    L.append(f"| Adossement moyen par booster (NEAR) | {_n(a['esperance_adossement'])} | "
             f"{_n(s['esperance_adossement'])} ± {_n(s['erreur_type'], 3)} |")
    L.append(f"| Écart-type par booster (NEAR) | {_n(a['sigma_booster'], 1)} | {_n(s['sigma_booster'], 1)} |")
    L.append(f"| Cartes brûlables par booster | {_n(a['cartes_brulables_moyennes'])} | {_n(s['cartes_brulables_moyennes'])} |")
    L.append(f"| Booster sans carte brûlable | {_pct(a['p_aucune_brulable'])} | {_pct(s['p_aucune_brulable'])} |")
    L.append(f"| P(adossement ≥ prix) | | {_pct(s['p_adossement_ge_prix'])} |")
    L.append(f"| P(adossement + revente ≥ prix) | | {_pct(s['p_adossement_plus_revente_ge_prix'])} |")
    for nom in ("legendaire", "mythique"):
        if f"p_au_moins_un_{nom}" in a:
            L.append(f"| P(au moins un {nom}) | {_pct(a[f'p_au_moins_un_{nom}'], 2)} ({_cote(a[f'p_au_moins_un_{nom}'])}) | "
                     f"{_pct(s[f'p_au_moins_un_{nom}'], 2)} |")
            L.append(f"| P(au moins un {nom} brûlable) | {_pct(a[f'p_au_moins_un_{nom}_brulable'], 2)} | "
                     f"{_pct(s[f'p_au_moins_un_{nom}_brulable'], 2)} |")
    L.append(f"| Gain moyen « brûle tout » (NEAR) | {_n(a['gain_attaquant_moyen'])} | {_n(s['gain_attaquant_moyen'])} |")
    L.append(f"| Borne β (ε = {_pct(cfg['epsilon'], 0)}) | {_pct(a['beta_max_formule'])} | {_pct(s.get('beta_max_simule', float('nan')))} |")
    L.append(f"| Booster touché par V_cap = {_n(cfg['v_cap'], 0)} | | {_pct(s['p_vcap_actif'], 4)} |")
    if "part_brulables_sous_vmin" in s:
        L.append(f"| Cartes brûlables sous {_n(cfg['v_min_brulable'], 1)} NEAR | | {_pct(s['part_brulables_sous_vmin'])} |")
    L += ["", "**Percentiles de l'adossement d'un booster (NEAR)**", "",
          "| " + " | ".join(f"p{k}" for k in s["percentiles"]) + " | max |",
          "|" + "---:|" * (len(s["percentiles"]) + 1),
          "| " + " | ".join(_n(v, 1) for v in s["percentiles"].values()) + f" | {_n(s['max'], 1)} |", ""]
    L += ["**Valeur d'une carte brûlable (NEAR)**", "", "| Rareté | Min | Base (m = 1) | Max | Max en $ |", "|---|---:|---:|---:|---:|"]
    for nom, v in a["valeur_par_rarete"].items():
        L.append(f"| {nom} | {_n(v['min'])} | {_n(v['base'])} | {_n(v['max'])} | {_n(v['max'] * usd, 0)} |")
    L += ["", "**Fréquence des cartes sur 10 000 boosters**", "",
          "| Rareté | Cartes par booster | Exemplaires par brûlable | Par carte de collection | Faveur |",
          "|---|---:|---:|---:|---:|"]
    for nom, f in res["cartes"].items():
        L.append(f"| {nom} | {_n(f['cartes_par_booster'], 4)} | {_n(f['exemplaires_par_brulable'], 1)} | "
                 f"{_n(f['exemplaires_par_collection'], 1)} | {_n(f['faveur_brulable'], 1)} |")
    L += ["", f"**Réserve** ({r['trajectoires']} trajectoires de {r['horizon']} ventes, apport "
              f"(β + δ)·P = {_n(r['apport_par_booster'])} NEAR par booster)", "",
          "| R₀ (NEAR) | P(réserve < V_cap avant 10 000 ventes) |", "|---:|---:|"]
    for r0, p in r["courbe"]:
        L.append(f"| {_n(r0, 0)} | {_pct(p, 2)} |")
    L += ["", f"- Approximation normale (z = {r['z']}) : R₀ ≈ {_n(r['r0_normale'], 0)} NEAR. "
              f"Risque simulé à ce niveau : {_pct(r['p_ruine_a_r0_normale'], 2)} "
              f"(un mouvement brownien donnerait {_pct(r['p_ruine_brownien_equivalente'], 2)})."]
    for k in ("0.05", "0.01", "0.001"):
        if f"r0_risque_{k}" in r:
            L.append(f"- R₀ simulé pour un risque de {_pct(float(k), 1)} : {_n(r[f'r0_risque_{k}'], 0)} NEAR "
                     f"({_n(r[f'r0_risque_{k}'] * usd, 0)} $).")
    marge = 1 - cfg["beta"] - cfg["delta"]
    L.append(f"- Reste après jetons et réserve : {_pct(marge, 0)} du prix, soit {_n(marge * P)} NEAR par booster.")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- sensibilité

def _ligne(cfg: dict, n_boosters: int, trajectoires: int) -> dict:
    a = M.analytique(cfg)
    s = S.statistiques(cfg, n_boosters, avec_beta_max=False)
    r = S.ruine(cfg, trajectoires, grille_r0=[])
    return {"a": a, "s": s, "r": r}


def sensibilite(cfg: dict, n_boosters: int = 1_000_000, trajectoires: int = 3000) -> dict:
    P = cfg["prix"]
    res = {"beta": [], "legendaire": [], "mythique": []}
    for beta in (0.40, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85):
        res["beta"].append((beta, _ligne(M.avec(cfg, beta=beta), n_boosters, trajectoires)))
    for f in (0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
        res["legendaire"].append((f, _ligne(M.scaler_poids(cfg, "legendaire", f), n_boosters, trajectoires)))
    for cote in (1000, 2000, 5000, 10000, 20000):
        res["mythique"].append((cote, _ligne(M.changer_cote_mythique(cfg, 1 / cote), n_boosters, trajectoires)))
    return res


def markdown_sensibilite(cfg: dict, res: dict) -> str:
    P = cfg["prix"]
    vm = cfg.get("v_min_brulable", 0)
    L = [f"### Sensibilité : {cfg['nom']}", "",
         "**β** (le reste de la config ne change pas)", "",
         "| β | Adossement moyen | P(≥ prix) | Gain « brûle tout » / prix | Respecte ε | Reste après réserve | R₀ à 1 % | Commune brûlable min |",
         "|---:|---:|---:|---:|:---:|---:|---:|---:|"]
    for beta, x in res["beta"]:
        a, s, r = x["a"], x["s"], x["r"]
        ok = "oui" if a["gain_attaquant_moyen"] <= P * (1 - cfg["epsilon"]) else "**non**"
        cm = a["valeur_par_rarete"].get("commune", {}).get("min", float("nan"))
        L.append(f"| {_pct(beta, 0)} | {_n(s['esperance_adossement'])} | {_pct(s['p_adossement_ge_prix'])} | "
                 f"{_pct(a['gain_attaquant_moyen'] / P)} | {ok} | {_pct(1 - beta - cfg['delta'], 0)} | "
                 f"{_n(r.get('r0_risque_0.01'), 0)} | {_n(cm)}{' (sous v_min)' if cm < vm else ''} |")
    L += ["", "**Poids des légendaires** (κ est recalculé : les autres cartes rétrécissent)", "",
          "| Facteur | Poids | κ | Commune brûlable min | Légendaire min / max | Part de E[V] venant des légendaires | σ | P(≥ prix) | R₀ à 1 % |",
          "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for f, x in res["legendaire"]:
        a, s, r = x["a"], x["s"], x["r"]
        c2 = M.scaler_poids(cfg, "legendaire", f)
        part = _part_rarete(c2, "legendaire")
        vl = a["valeur_par_rarete"]["legendaire"]
        L.append(f"| ×{_n(f, 2)} | {_n(c2['raretes']['legendaire']['poids'], 1)} | {_n(a['kappa'], 3)} | "
                 f"{_n(a['valeur_par_rarete']['commune']['min'])} | {_n(vl['min'], 1)} / {_n(vl['max'], 1)} | "
                 f"{_pct(part)} | {_n(s['sigma_booster'], 1)} | {_pct(s['p_adossement_ge_prix'])} | {_n(r.get('r0_risque_0.01'), 0)} |")
    L += ["", "**Cote du mythique** (poids inchangé ; la probabilité est prise aux communes de l'emplacement 5)", "",
          "| Cote par booster | Valeur d'un mythique | Part de E[V] | σ | R₀ normale | Risque simulé à R₀ normale | R₀ à 1 % | Mythiques sur 10 000 boosters |",
          "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for cote, x in res["mythique"]:
        a, s, r = x["a"], x["s"], x["r"]
        c2 = M.changer_cote_mythique(cfg, 1 / cote)
        L.append(f"| 1 sur {_n(cote, 0)} | {_n(a['valeur_par_rarete']['mythique']['max'], 0)} | "
                 f"{_pct(_part_rarete(c2, 'mythique'))} | {_n(s['sigma_booster'], 1)} | {_n(r['r0_normale'], 0)} | "
                 f"{_pct(r['p_ruine_a_r0_normale'], 1)} | {_n(r.get('r0_risque_0.01'), 0)} | {_n(10000 / cote, 1)} |")
    return "\n".join(L) + "\n"


def _part_rarete(cfg: dict, rarete: str) -> float:
    t = M.construire_tables(cfg)
    pb = M.proba_issues_booster(t)
    v = M.valeurs_issues(t, M.kappa(cfg))
    i = t.raretes.index(rarete)
    return float((pb * v * (t.issue_rarete == i)).sum() / (pb * v).sum())


def sauver_json(obj, chemin: Path) -> None:
    def conv(o):
        if hasattr(o, "item"):
            return o.item()
        raise TypeError(type(o))
    chemin.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=conv), encoding="utf-8")
