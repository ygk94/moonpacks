"""Fréquences observées contre taux annoncés : test du χ² d'adéquation (bibliothèque standard)."""

from __future__ import annotations

import math

from . import core


def _gammainc_lower_series(a: float, x: float) -> float:
    term = 1.0 / a
    s = term
    n = 0
    while abs(term) > abs(s) * 1e-15 and n < 10_000:
        n += 1
        term *= x / (a + n)
        s += term
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gammainc_upper_cf(a: float, x: float) -> float:
    # Fraction continue de Lentz pour Q(a, x).
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 10_000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_sf(x: float, dof: int) -> float:
    """P(χ²_dof ≥ x)."""
    if dof <= 0:
        return 1.0
    if x <= 0:
        return 1.0
    a, y = dof / 2.0, x / 2.0
    if y < a + 1.0:
        return max(0.0, 1.0 - _gammainc_lower_series(a, y))
    return _gammainc_upper_cf(a, y)


def chi2_test(observed: dict[str, int], probs: dict[str, float], min_expected: float = 5.0):
    """χ² d'adéquation. Les catégories d'effectif attendu < `min_expected` sont regroupées.
    Une observation dans une catégorie de probabilité nulle donne p = 0.
    Renvoie (chi2, ddl, p, lignes [(catégorie, observé, attendu)])."""
    n = sum(observed.values())
    impossible = [k for k, v in observed.items() if v > 0 and probs.get(k, 0.0) == 0.0]
    rows = [(k, observed.get(k, 0), n * p) for k, p in probs.items() if p > 0]
    if impossible:
        return math.inf, max(len(rows) - 1, 0), 0.0, rows + [(k, observed[k], 0.0) for k in impossible]
    big = [r for r in rows if r[2] >= min_expected]
    small = [r for r in rows if r[2] < min_expected]
    if small:
        merged = ("+".join(r[0] for r in small), sum(r[1] for r in small), sum(r[2] for r in small))
        if merged[2] < min_expected and big:
            big.sort(key=lambda r: r[2])
            b0 = big.pop(0)
            merged = (merged[0] + "+" + b0[0], merged[1] + b0[1], merged[2] + b0[2])
        big.append(merged)
    chi2 = sum((o - e) ** 2 / e for _, o, e in big if e > 0)
    dof = len(big) - 1
    return chi2, dof, chi2_sf(chi2, dof), big


def rarity_probs(table: dict) -> dict[str, float]:
    total = core.rarity_total(table)
    return {r: table["rarity_weights"][r] / total for r in core.RARITIES}


def series_stats(table: dict, events: list[dict], alpha: float) -> tuple[bool, list[str]]:
    """1. raretés visées (`rolled_rarity`), qui ne dépendent pas des plafonds : χ² contre les poids publics ;
    2. dans chaque rareté sans plafond, cartes choisies contre les poids des cartes ;
    3. raretés finales et retombées, pour information."""
    lines: list[str] = []
    ok = True
    draws = [d for ev in events for d in ev["draws"]]
    lines.append(f"{len(events)} boosters, {len(draws)} tirages")

    # Série à mécaniques : chaque booster a sa table de taux (base, or, rush). L'attendu est le
    # mélange des tables effectivement utilisées, booster par booster.
    probs = {r: 0.0 for r in core.RARITIES}
    for ev in events:
        mode = (ev.get("mechanics") or {}).get("mode", "base")
        w = core.mode_weights(table, mode)
        tot = max(sum(w[r] for r in core.RARITIES), 1)
        for r in core.RARITIES:
            probs[r] += len(ev["draws"]) * w[r] / tot
    probs = {r: (v / len(draws) if draws else 0.0) for r, v in probs.items()} if draws else rarity_probs(table)
    modes = {}
    for ev in events:
        k = (ev.get("mechanics") or {}).get("mode", "base")
        modes[k] = modes.get(k, 0) + 1
    if table.get("mechanics"):
        lines.append(f"tables de taux utilisées : {', '.join(f'{k} {v}' for k, v in sorted(modes.items()))}")
    obs = {r: 0 for r in core.RARITIES}
    fin = {r: 0 for r in core.RARITIES}
    for d in draws:
        obs[d["rolled_rarity"]] += 1
        fin[d["final_rarity"]] += 1
    chi2, dof, p, _ = chi2_test(obs, probs)
    lines.append("raretés visées (indépendantes des plafonds) :")
    lines.append(f"  {'rareté':<10}{'observé':>9}{'attendu':>11}{'taux annoncé':>15}{'finale':>9}")
    for r in core.RARITIES:
        lines.append(f"  {r:<10}{obs[r]:>9}{len(draws) * probs[r]:>11.1f}{100 * probs[r]:>14.4f}%{fin[r]:>9}")
    verdict = p >= alpha
    ok &= verdict
    lines.append(f"  χ² = {chi2:.3f}, ddl = {dof}, p = {p:.4g} -> {'conforme' if verdict else 'ÉCART SIGNIFICATIF'} (seuil {alpha})")
    falls = sum(1 for d in draws if d["rolled_rarity"] != d["final_rarity"])
    lines.append(f"  retombées dues aux plafonds : {falls}")

    if (table.get("mechanics") or {}).get("burn"):
        lines.append("rareté pilotée par les burns : test par carte omis (poids variables, voir pack --event avec rejeu)")
        return ok, lines
    for r in core.RARITIES[1:]:
        cards = [(i, c) for i, c in enumerate(table["cards"]) if c["rarity"] == r and c["weight"] > 0]
        if len(cards) < 2 or any(c.get("cap") is not None for _, c in cards):
            continue
        sub = [d for d in draws if d["final_rarity"] == r and d["kind"] == "visible"]
        if not sub:
            continue
        w = sum(c["weight"] for _, c in cards)
        probs_c = {c["card_id"]: c["weight"] / w for _, c in cards}
        obs_c = {c["card_id"]: 0 for _, c in cards}
        for d in sub:
            obs_c[table["cards"][d["index"]]["card_id"]] = obs_c.get(table["cards"][d["index"]]["card_id"], 0) + 1
        chi2, dof, p, _ = chi2_test(obs_c, probs_c)
        v = p >= alpha
        ok &= v
        detail = ", ".join(f"{k} {obs_c[k]}/{len(sub) * probs_c[k]:.1f}" for k in probs_c)
        lines.append(f"cartes {r} (sans plafond) : {detail} ; χ² = {chi2:.3f}, ddl = {dof}, p = {p:.4g} -> {'conforme' if v else 'ÉCART SIGNIFICATIF'}")
    return ok, lines
