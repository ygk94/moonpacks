#!/usr/bin/env python3
"""Validateur de série, à lancer avant `open_series` (la table ouverte est figée pour toujours).

    python3 scripts/validate_series.py scripts/out/<slug>/ [--secrets scripts/secrets/<slug>.json]
        [--mythiques ../docs/data/secrets/mythiques.json] [--scan FICHIER_OU_DOSSIER …] [--git]
        [--max-rush-mean 0.8] [--max-normal-mean 1.0] [--json]
    python3 scripts/validate_series.py table.json …        # une table seule

Contrôles (code de sortie 1 s'il y a une erreur) :

1. **Règles du contrat**, réécrites ici indépendamment (`src/series.rs`, `src/mechanics.rs`) : bornes
   de l'en-tête, des cartes, des engagements mythiques, des redevances, couverture (une carte par
   rareté pondérée, une commune illimitée, brûlable garantie), mécaniques (gold pack, pitié, burns,
   rush, résurrection, valeur, dépassements de u128). Une table que le contrat refuserait est refusée
   ici, avant d'avoir payé le chargement.
2. **Poids et plafonds** : probabilités par rareté, cartes jamais tirables (poids nul), plafonds
   nuls, mythiques au plafond.
3. **Valeur moyenne** des tables de valeur (en multiples du prix) : table rush ≤ `--max-rush-mean`
   (80 %, erreur : acheter pendant un rush serait à espérance positive), table normale
   ≤ `--max-normal-mean` (100 %, erreur), gold ≥ normale (avertissement).
4. **Dossier de `build_series.py`** : lots dans l'ordre (create + append = table), `card_id`
   strictement croissants, `table_hash.txt` = sha256 de `table.json` = hash recalculé par le
   vérificateur, manifeste cohérent.
5. **Mythiques « ? »** : avec `--secrets`, chaque préimage est révélable (longueurs, montant > 0, sel
   de 32 octets, sels distincts) et redonne l'engagement et le `content_hash` de la table.
6. **Aucun secret dans les fichiers publics** (dossier de sortie, `--scan`, fichiers suivis par git
   avec `--git`) : sel, `card_id` et titre engagés, média engagé ; avec `--mythiques`, un vrai nom,
   ticker, id CoinGecko ou adresse sur la même ligne qu'un mot « mythique » (ou dans un objet JSON
   de mythique), un n° v1 de mythique (« n° X ») à côté de ce mot, et toute empreinte courte
   (≥ 10 hex, sha256/sha1/md5) d'un de ces mots, qu'une force brute retrouverait. Les messages ne
   citent jamais le secret trouvé (seulement le fichier, la ligne et le numéro de mythique).

    python3 scripts/validate_series.py --git     # contrôle anti-fuite seul, sur tout le dépôt
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.dirname(HERE)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, os.path.join(REPO, "verifier"))

from memaster_verifier import canon, core  # noqa: E402

# Limites du contrat (src/lib.rs).
MAX_CARDS_PER_SERIES = 2_000
MAX_CARDS_PER_CALL = 200
MAX_MYTHICS_PER_SERIES = 20
MAX_MYTHIC_CAP = 100
MAX_CARDS_PER_PACK = 10
MAX_ROYALTIES = 10
MAX_ROYALTY_BPS = 5_000
MAX_ID_LEN = 64
MAX_TITLE_LEN = 64
MAX_URL_LEN = 256
MAX_ASSET_ID_LEN = 128
MAX_RUSH_BUCKETS = 96
MAX_PITY_N = 10_000
MAX_RESURRECTABLE = 200
MAX_BURN_PRIOR_K = 1_000_000
PPB = 1_000_000_000
MAX_VALUE_TIERS = 32
MIN_NORMAL_VALUE_BPS = 2_000
MAX_NORMAL_VALUE_BPS = 20_000
MAX_VALUE_BPS = 1_000_000
MAX_VALUE_MULT = 1_000_000
U32 = (1 << 32) - 1
U64 = (1 << 64) - 1
U128 = (1 << 128) - 1
RARITIES = core.RARITIES  # mythic → common
VISIBLE = RARITIES[1:]
MECH_KEYS = ("gold", "pity", "burn", "rush", "resurrection", "value")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MYTHIC_WORD = re.compile(r"mythi|\bM[123]\b", re.I)


class Result:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


# ------------------------------------------------------------------ règles du contrat


def _is_uint(x, hi) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= hi


def _u128(x):
    """U128 du JSON : chaîne décimale."""
    if isinstance(x, str) and x.isdigit() and int(x) <= U128:
        return int(x)
    return None


def _check_len(res, s, mx, what):
    if not isinstance(s, str) or not 1 <= len(s.encode("utf-8")) <= mx:
        res.err(f"{what} : longueur invalide (1 à {mx} octets)")


def _check_backing(res, b, what):
    if b is None:
        return
    if not isinstance(b, dict):
        res.err(f"{what} : adossement mal formé")
        return
    _check_len(res, b.get("asset_id"), MAX_ASSET_ID_LEN, f"{what}.asset_id")
    a = _u128(b.get("amount"))
    if a is None or a == 0:
        res.err(f"{what}.amount doit être un U128 > 0")


def _weights(res, w, what) -> dict | None:
    if not isinstance(w, dict) or set(w) != set(RARITIES) or not all(_is_uint(w[r], U32) for r in RARITIES):
        res.err(f"{what} : poids des 5 raretés (entiers u32) attendus")
        return None
    return w


def _total(w) -> int:
    return sum(w[r] for r in RARITIES)


def _check_weights(res, t, w, what):
    if _total(w) == 0:
        res.err(f"{what} : poids nuls")
    if w["mythic"] > 0 and not any(m.get("weight", 0) > 0 for m in t.get("mythics", [])):
        res.err(f"{what} : poids mythique sans engagement de poids non nul")


def weight_tables(t) -> list[dict]:
    """Tables de poids de rareté (base, poids propres des emplacements or, rush), comme le contrat."""
    out = [t["rarity_weights"]]
    m = t.get("mechanics") or {}
    if m.get("gold"):
        out += [s["weights"] for s in m["gold"].get("slots", []) if s.get("weights") is not None]
    if m.get("rush"):
        out.append(m["rush"]["weights"])
    return out


def needs_burnable(t) -> bool:
    m = t.get("mechanics") or {}
    return bool(m.get("value")) or bool(m.get("gold") and any(s.get("burnable") for s in m["gold"].get("slots", [])))


def _check_tiers(res, tiers, what, lo, hi):
    if not isinstance(tiers, list) or not 1 <= len(tiers) <= MAX_VALUE_TIERS:
        res.err(f"value.{what} : 1 à {MAX_VALUE_TIERS} paliers")
        return
    for x in tiers:
        if not (isinstance(x, list) and len(x) == 2 and _is_uint(x[0], U32) and _is_uint(x[1], U32)):
            res.err(f"value.{what} : palier [bps, poids] attendu")
            return
        if x[1] == 0:
            res.err(f"value.{what} : poids nuls interdits")
        if not lo <= x[0] <= hi:
            res.err(f"value.{what} : valeur hors de [{lo}, {hi}] points de base")


def _validate_mechanics(res, t, price):
    m = t["mechanics"]
    if not isinstance(m, dict) or list(m) != list(MECH_KEYS):
        res.err(f"mechanics : champs {', '.join(MECH_KEYS)} attendus, dans cet ordre (ordre haché)")
        return
    base = t["rarity_weights"]
    if m["gold"] is not None:
        slots = m["gold"].get("slots") if isinstance(m["gold"], dict) else None
        if not isinstance(slots, list) or not 1 <= len(slots) <= MAX_CARDS_PER_PACK:
            res.err("gold.slots : 1 à 10 emplacements")
        else:
            for i, s in enumerate(slots):
                if s.get("floor") not in RARITIES or not isinstance(s.get("burnable"), bool):
                    res.err(f"gold.slots[{i}] : floor et burnable attendus")
                    continue
                if s.get("weights") is not None and _weights(res, s["weights"], f"gold.slots[{i}].weights") is None:
                    continue
                w = core.gold_slot_weights(base, s)
                _check_weights(res, t, w, f"gold.slots[{i}]")
                f = RARITIES.index(s["floor"])
                if any(w[r] for r in RARITIES[f + 1:]):
                    res.err(f"gold.slots[{i}] : poids sous le plancher {s['floor']}")
    v = m["value"]
    if v is not None:
        _check_tiers(res, v.get("normal"), "normal", MIN_NORMAL_VALUE_BPS, MAX_NORMAL_VALUE_BPS)
        _check_tiers(res, v.get("gold"), "gold", 1, MAX_VALUE_BPS)
        _check_tiers(res, v.get("rush"), "rush", 1, MAX_VALUE_BPS)
        mult = _weights(res, v.get("multipliers"), "value.multipliers")
        if mult is not None:
            if mult["mythic"] != 0:
                res.err("value.multipliers.mythic = 0 (une mythique garde l'adossement de son contenu)")
            for r in VISIBLE:
                if not 1 <= mult[r] <= MAX_VALUE_MULT:
                    res.err(f"value.multipliers.{r} : 1 à {MAX_VALUE_MULT}")
            if res.ok and price is not None:
                max_bps = max(x[0] for k in ("normal", "gold", "rush") for x in v[k])
                max_mult = max(mult[r] for r in VISIBLE)
                if price * max_bps > U128 or price * max_bps // 10_000 * max_mult > U128:
                    res.err("value : prix trop élevé pour ces valeurs et multiplicateurs (dépassement de u128)")
    p = m["pity"]
    if p is not None:
        if m["gold"] is None:
            res.err("pity exige gold")
        if "p0_ppm" in p:
            res.err("pity : ancien format en ppm refusé par le contrat (p0_ppb, k_ppb, p_max_ppb, n_max)")
        else:
            n = p.get("n_max")
            if n is not None and not (isinstance(n, int) and 1 <= n <= MAX_PITY_N):
                res.err("pity.n_max hors bornes (absent, ou 1 à 10 000)")
            if not all(_is_uint(p.get(k), PPB) for k in ("p0_ppb", "k_ppb", "p_max_ppb")):
                res.err("pity : probabilités en ppb (≤ 10⁹)")
            elif p["p0_ppb"] > p["p_max_ppb"]:
                res.err("pity : p0_ppb ≤ p_max_ppb")
            elif p["p_max_ppb"] == 0 and n is None:
                res.err("pity : gold pack inatteignable (p_max_ppb = 0 sans n_max)")
    r = m["resurrection"]
    if r is not None:
        el = r.get("eligible")
        if not isinstance(el, list) or not all(_is_uint(i, U32) for i in el):
            res.err("resurrection.eligible : liste d'index attendue")
        else:
            if len(el) > MAX_RESURRECTABLE:
                res.err("resurrection.eligible : 200 cartes au plus")
            if any(a >= b for a, b in zip(el, el[1:])):
                res.err("resurrection.eligible : index strictement croissants")
    b = m["burn"]
    if b is not None:
        if not _is_uint(b.get("floor_bps"), 10_000):
            res.err("burn.floor_bps ≤ 10 000")
        if not _is_uint(b.get("prior_k"), MAX_BURN_PRIOR_K):
            res.err("burn.prior_k ≤ 1 000 000")
    ru = m["rush"]
    if ru is not None:
        w = _weights(res, ru.get("weights"), "rush.weights")
        if w is not None:
            _check_weights(res, t, w, "rush.weights")
        k = {x: ru.get(x) for x in ("ratio_bps", "min_packs", "max_per_account")}
        blocks = {x: ru.get(x) for x in ("window_blocks", "baseline_blocks", "bucket_blocks", "duration_blocks", "cooldown_blocks")}
        if not all(_is_uint(x, U32) for x in k.values()) or not all(_is_uint(x, U64) for x in blocks.values()):
            res.err("rush : paramètres entiers attendus")
            return
        if k["ratio_bps"] < 10_000:
            res.err("rush.ratio_bps ≥ 10 000 (×1)")
        if k["min_packs"] < 1:
            res.err("rush.min_packs ≥ 1")
        if k["max_per_account"] < 1:
            res.err("rush.max_per_account ≥ 1")
        if blocks["bucket_blocks"] < 1 or blocks["duration_blocks"] < 1:
            res.err("rush : seaux et durée ≥ 1 bloc")
            return
        bb = blocks["bucket_blocks"]
        if blocks["window_blocks"] % bb or blocks["baseline_blocks"] % bb:
            res.err("rush : window_blocks et baseline_blocks multiples de bucket_blocks")
        mw, ml = blocks["window_blocks"] // bb, blocks["baseline_blocks"] // bb
        if not (mw >= 1 and ml <= MAX_RUSH_BUCKETS):
            res.err("rush : 1 à 96 seaux")
        if not mw < ml:
            res.err("rush : fenêtre courte plus courte que la fenêtre longue")
        elif k["ratio_bps"] * mw >= 10_000 * ml:
            res.err("rush.ratio_bps inatteignable pour ces fenêtres")


def validate_table(t: dict) -> Result:
    """Toutes les règles de `validate_table` du contrat (création complète et ouverture)."""
    res = Result()
    if not isinstance(t, dict):
        res.err("table : objet JSON attendu")
        return res
    expected = ["name", "price", "cards_per_pack", "rarity_weights", "cards", "mythics", "royalties"]
    keys = list(t)
    if keys[:7] != expected or keys[7:] not in ([], ["mechanics"]):
        res.err(f"table : champs {', '.join(expected)} (puis mechanics) attendus, dans cet ordre (ordre haché)")
        return res
    _check_len(res, t["name"], MAX_TITLE_LEN, "name")
    price = _u128(t["price"])
    if price is None or price == 0:
        res.err("Le prix doit être > 0 (U128 en chaîne décimale)")
    if not _is_uint(t["cards_per_pack"], 255) or not 1 <= t["cards_per_pack"] <= MAX_CARDS_PER_PACK:
        res.err("cards_per_pack hors bornes (1 à 10)")
    if _weights(res, t["rarity_weights"], "rarity_weights") is None:
        return res
    mythics = t["mythics"]
    if len(mythics) > MAX_MYTHICS_PER_SERIES:
        res.err("Trop de mythiques (20 au plus)")
    if _total(t["rarity_weights"]) == 0:
        res.err("Poids de rareté nuls")
    seen_c, seen_h = set(), set()
    for j, m in enumerate(mythics):
        if list(m) != ["commitment", "content_hash", "weight", "cap"]:
            res.err(f"mythics[{j}] : champs commitment, content_hash, weight, cap attendus (rien d'autre)")
            continue
        if not isinstance(m["commitment"], str) or not HEX64.match(m["commitment"]):
            res.err(f"mythics[{j}].commitment : 64 caractères hex minuscules")
        if not isinstance(m["content_hash"], str) or not HEX64.match(m["content_hash"]):
            res.err(f"mythics[{j}].content_hash : 64 caractères hex minuscules")
        if not _is_uint(m["weight"], U32):
            res.err(f"mythics[{j}].weight : entier u32")
        if not _is_uint(m["cap"], U32) or not 1 <= m["cap"] <= MAX_MYTHIC_CAP:
            res.err(f"mythics[{j}] : plafond de mythique hors bornes (1 à 100)")
        if m["commitment"] in seen_c:
            res.err(f"mythics[{j}] : engagement en double")
        if m["content_hash"] in seen_h:
            res.err(f"mythics[{j}] : content_hash en double")
        seen_c.add(m["commitment"])
        seen_h.add(m["content_hash"])
    if t["rarity_weights"]["mythic"] > 0 and not any(m.get("weight", 0) > 0 for m in mythics):
        res.err("Poids mythique sans engagement de poids non nul")
    roy = t["royalties"]
    if len(roy) > MAX_ROYALTIES:
        res.err("Trop de redevances (10 au plus)")
    if sum(int(r.get("bps", 0)) for r in roy) > MAX_ROYALTY_BPS:
        res.err("Redevances > 50 %")
    if t.get("mechanics") is not None:
        _validate_mechanics(res, t, price)
    if not res.ok:
        return res
    cards = t["cards"]
    if len(cards) > MAX_CARDS_PER_SERIES:
        res.err("Trop de cartes (2 000 au plus)")
    ids = set()
    card_keys = ["card_id", "title", "rarity", "weight", "cap", "media", "reference", "backing"]
    for i, c in enumerate(cards):
        what = f"cards[{i}]"
        if list(c) != card_keys:
            res.err(f"{what} : champs {', '.join(card_keys)} attendus, dans cet ordre")
            continue
        _check_len(res, c["card_id"], MAX_ID_LEN, f"{what}.card_id")
        _check_len(res, c["title"], MAX_TITLE_LEN, f"{what}.title")
        for k in ("media", "reference"):
            if c[k] is not None:
                _check_len(res, c[k], MAX_URL_LEN, f"{what}.{k}")
        _check_backing(res, c["backing"], what)
        if c["rarity"] not in RARITIES:
            res.err(f"{what} : rareté inconnue")
            continue
        if c["rarity"] == "mythic":
            res.err(f"{what} : les mythiques passent par des engagements")
            continue
        if not _is_uint(c["weight"], U32):
            res.err(f"{what}.weight : entier u32")
        if c["cap"] is not None and not _is_uint(c["cap"], U32):
            res.err(f"{what}.cap : entier u32 ou null")
        if not any(w[c["rarity"]] > 0 for w in weight_tables(t)):
            res.err(f"{what} : carte dans une rareté de poids nul")
        if c["card_id"] in ids:
            res.err(f"{what} : card_id en double")
        ids.add(c["card_id"])
    if not res.ok:
        return res
    # Couverture (validate_coverage).
    for w in weight_tables(t):
        for r in VISIBLE:
            if w[r] > 0 and not any(c["rarity"] == r and c["weight"] > 0 for c in cards):
                res.err(f"Rareté {r} sans carte de poids non nul")
    if not (t["rarity_weights"]["common"] > 0 and any(c["rarity"] == "common" and c["cap"] is None and c["weight"] > 0 for c in cards)):
        res.err("Il faut au moins une commune sans plafond et de poids non nul (et un poids commune non nul)")
    if needs_burnable(t) and not any(c["backing"] and c["cap"] is None and c["weight"] > 0 for c in cards):
        res.err("Brûlable garantie : il faut une carte adossée par la table, sans plafond et de poids non nul")
    for i in core.resurrectable(t):
        if i >= len(cards):
            res.err("resurrection.eligible : index de carte inconnu")
        elif cards[i]["rarity"] not in ("epic", "legendary"):
            res.err(f"resurrection.eligible : carte {i} ni épique ni légendaire")
        elif cards[i]["backing"] is not None:
            res.err(f"resurrection.eligible : carte {i} déjà adossée par la table")
    return res


# ------------------------------------------------------------------ poids, plafonds, valeur


def mean_value(tiers) -> float:
    return sum(b * w for b, w in tiers) / sum(w for _, w in tiers) / 10_000


def economics(t: dict, res: Result, max_rush_mean: float, max_normal_mean: float) -> dict:
    """Probabilités par rareté, cartes et plafonds suspects, valeur moyenne des tables."""
    w = t["rarity_weights"]
    tot = _total(w)
    probs = {r: w[r] / tot for r in RARITIES}
    res.info.append("raretés (table de base) : " + ", ".join(f"{r} {probs[r]:.6%}" for r in RARITIES))
    cards = t["cards"]
    dead = [i for i, c in enumerate(cards) if c["weight"] == 0]
    if dead:
        res.warn(f"{len(dead)} carte(s) de poids nul, jamais tirables (index {dead[:10]}…)")
    zero_cap = [i for i, c in enumerate(cards) if c["cap"] == 0]
    if zero_cap:
        res.warn(f"{len(zero_cap)} carte(s) au plafond 0, jamais tirables (index {zero_cap[:10]})")
    for j, m in enumerate(t["mythics"]):
        if m["weight"] == 0:
            res.warn(f"mythique {j} de poids nul : jamais tirable")
    if w["mythic"] and t["mythics"]:
        mw = sum(m["weight"] for m in t["mythics"])
        for j, m in enumerate(t["mythics"]):
            if m["weight"]:
                p = probs["mythic"] * m["weight"] / mw
                res.info.append(f"mythique {j} : 1 sur {1 / p:,.0f} par emplacement, plafond {m['cap']}")
    out = {"rarity_probabilities": probs}
    v = (t.get("mechanics") or {}).get("value")
    if v:
        means = {k: mean_value(v[k]) for k in ("normal", "gold", "rush")}
        out["value_means"] = means
        res.info.append("valeur moyenne (multiples du prix) : " + ", ".join(f"{k} {x:.3f}" for k, x in means.items()))
        if means["normal"] > max_normal_mean + 1e-12:
            res.err(f"valeur moyenne de la table normale {means['normal']:.3f} > {max_normal_mean} : la série paie plus qu'elle n'encaisse")
        if (t.get("mechanics") or {}).get("rush") and means["rush"] > max_rush_mean + 1e-12:
            res.err(f"valeur moyenne de la table rush {means['rush']:.3f} > {max_rush_mean} (acheter pendant un rush serait à espérance positive)")
        if means["gold"] < means["normal"]:
            res.warn(f"gold pack moins généreux ({means['gold']:.3f}) qu'un pack normal ({means['normal']:.3f})")
    return out


# ------------------------------------------------------------------ dossier de build_series.py


def check_out_dir(d: str, res: Result) -> dict:
    with open(os.path.join(d, "table.json"), "rb") as f:
        raw = f.read()
    table = json.loads(raw)
    h = core.table_hash(table).hex()
    if canon.table_json_bytes(table) != raw:
        res.err("table.json : octets différents de la sérialisation du contrat (serde_json)")
    if hashlib.sha256(raw).hexdigest() != h:
        res.err("table.json : sha256 des octets ≠ hash recalculé")
    hp = os.path.join(d, "table_hash.txt")
    if os.path.exists(hp):
        with open(hp) as f:
            if f.read().strip() != h:
                res.err("table_hash.txt ≠ sha256(table.json)")
    mp = os.path.join(d, "manifest.json")
    if not os.path.exists(mp):
        res.warn("manifest.json absent : lots non contrôlés")
        return table
    with open(mp, encoding="utf-8") as f:
        man = json.load(f)
    if man.get("table_hash") != h:
        res.err("manifest.json : table_hash ≠ sha256(table.json)")
    if man.get("cards") != len(table["cards"]):
        res.err("manifest.json : nombre de cartes ≠ table.json")
    calls = man.get("calls", [])
    cards, header, batched = [], None, False
    for name in calls:
        with open(os.path.join(d, name), encoding="utf-8") as f:
            args = json.load(f)
        if name in ("create_series.json", "create_series_batched.json"):
            header = args["table"]
            batched = name == "create_series_batched.json"
            cards += header["cards"]
        elif name.startswith("append_series_cards."):
            if len(args["cards"]) > MAX_CARDS_PER_CALL:
                res.err(f"{name} : plus de {MAX_CARDS_PER_CALL} cartes")
            cards += args["cards"]
        if "table" in args and len(args["table"]["cards"]) > MAX_CARDS_PER_CALL:
            res.err(f"{name} : plus de {MAX_CARDS_PER_CALL} cartes en un appel")
        if name != calls[-1] or not name.startswith("open_series"):
            if name.startswith("open_series"):
                res.err("open_series doit être le dernier appel")
        dep = (man.get("deposits") or {}).get(name)
        if dep is None or not str(dep).isdigit():
            res.err(f"manifest.json : dépôt de {name} absent")
    if not calls or not calls[-1].startswith("open_series"):
        res.err("manifest.json : open_series doit être le dernier appel")
    if header is None:
        res.err("aucun appel create_series(_batched)")
        return table
    if dict(header, cards=cards) != table:
        res.err("lots : create + append ≠ table.json (lot manquant, en double ou dans le désordre)")
    if batched:
        ids = [c["card_id"].encode("utf-8") for c in cards]
        if any(a >= b for a, b in zip(ids, ids[1:])):
            res.err("lots : card_id non strictement croissants (refusé par append_series_cards)")
    return table


# ------------------------------------------------------------------ mythiques et fuites


def load_secrets(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_preimages(t: dict, secrets: list[dict], res: Result) -> None:
    """Chaque préimage est révélable par `reveal_mythic` et redonne les hashs de la table."""
    if len(secrets) != len(t["mythics"]):
        res.err(f"secrets : {len(secrets)} préimages pour {len(t['mythics'])} engagements")
    sels = set()
    visible_ids = {c["card_id"] for c in t["cards"]}
    for j, (p, m) in enumerate(zip(secrets, t["mythics"])):
        what = f"mythique {j}"
        cid, content = p.get("card_id"), p.get("content") or {}
        _check_len(res, cid, MAX_ID_LEN, f"{what} : card_id")
        _check_len(res, content.get("title"), MAX_TITLE_LEN, f"{what} : titre")
        for k in ("media", "reference"):
            u = content.get(k)
            if u is not None and (not isinstance(u, str) or len(u.encode("utf-8")) > MAX_URL_LEN):
                res.err(f"{what} : {k} trop long (révélation refusée)")
        _check_backing(res, content.get("backing"), f"{what} : contenu")
        if list(content) != ["title", "media", "reference", "backing"]:
            res.err(f"{what} : contenu title, media, reference, backing attendu (dans cet ordre)")
            continue
        try:
            sel = bytes.fromhex(p.get("sel", ""))
        except ValueError:
            sel = b""
        if len(sel) != 32 or p.get("sel") != p.get("sel", "").lower():
            res.err(f"{what} : sel de 32 octets (64 hex minuscules) exigé par le contrat")
            continue
        if sel in sels:
            res.err(f"{what} : sel réutilisé")
        sels.add(sel)
        if not isinstance(cid, str):
            continue
        c, h = core.mythic_commitments(cid, sel, content)
        if c.hex() != m["commitment"]:
            res.err(f"{what} : sha256(card_id || sel) ≠ engagement de la table")
        if h.hex() != m["content_hash"]:
            res.err(f"{what} : sha256(json(contenu) || sel) ≠ content_hash de la table")
        if cid in visible_ids:
            res.warn(f"{what} : son card_id est aussi celui d'une carte visible")


NAME_KEYS = ("nom", "ticker", "coingecko_id", "adresse")
RE_V1 = re.compile(r"^v1 n° ?(\d+)$")
FP_LEN = 10  # 40 bits : une empreinte plus courte ne désigne plus rien, plus longue se force encore


def load_names(path: str) -> list[tuple[int, list[str]]]:
    """Vrais noms, tickers, ids CoinGecko et adresses (docs/data/secrets/mythiques.json, formats de
    build_series.py)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "mythiques" in data:
        items = data["mythiques"]
    elif isinstance(data, dict):
        items = list(data.values())
    else:
        items = data
    out = []
    for j, e in enumerate(items):
        e = e.get("secret", e) if isinstance(e, dict) else {}
        words = [e[k] for k in NAME_KEYS if isinstance(e.get(k), str) and len(e[k]) >= 2]
        out.append((j, words))
    return out


def load_v1_numbers(path: str) -> list[tuple[int, str]]:
    """N° v1 des mythiques (`origines` « v1 n° X » du fichier secret)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("mythiques", []) if isinstance(data, dict) else data
    out = []
    for j, e in enumerate(items):
        for o in (e.get("origines") or []) if isinstance(e, dict) else []:
            m = RE_V1.match(str(o).strip())
            if m:
                out.append((j, m.group(1)))
    return out


def fingerprints(names) -> list[tuple[int, str]]:
    """Préfixes hex (FP_LEN) des sha256, sha1 et md5 de chaque mot secret, sous plusieurs casses."""
    out = set()
    for j, ws in names or []:
        for w in ws:
            for v in {w, w.upper(), w.lower(), re.sub(r"[\s$]", "", w).upper()}:
                for algo in ("sha256", "sha1", "md5"):
                    out.add((j, hashlib.new(algo, v.encode("utf-8")).hexdigest()[:FP_LEN]))
    return sorted(out)


def _files(paths: list[str]) -> list[str]:
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                out += [os.path.join(root, n) for n in sorted(names)]
        elif os.path.exists(p):
            out.append(p)
    return out


def git_files() -> list[str]:
    r = subprocess.run(["git", "-C", REPO, "ls-files", "-z"], capture_output=True, check=True)
    return [os.path.join(REPO, x) for x in r.stdout.decode().split("\0") if x]


def scan_leaks(files: list[str], secrets: list[dict], names, res: Result, rel=REPO, public_media=(),
               v1_numbers=()) -> None:
    """Secrets exacts (sel, card_id et titre engagés en chaîne JSON, média) partout ; vrai nom ou
    ticker sur une ligne qui parle de mythique. Aucun secret n'est recopié dans les messages.
    `public_media` : médias publics par construction (le visuel « ? » commun à toutes les mythiques,
    `mythic_media` du manifeste), qui ne désignent aucune mythique et ne sont donc pas des fuites."""
    exact = []
    public_media = {m for m in public_media if m}
    for j, p in enumerate(secrets or []):
        c = p.get("content") or {}
        if p.get("sel"):
            exact.append((j, "sel", p["sel"].encode()))
        for k, v in (("card_id", p.get("card_id")), ("titre", c.get("title"))):
            if isinstance(v, str) and v:
                exact.append((j, k, json.dumps(v, ensure_ascii=False).encode("utf-8")))
        for k in ("media", "reference"):
            if isinstance(c.get(k), str) and c[k] and c[k] not in public_media:
                exact.append((j, k, c[k].encode("utf-8")))
    pats = [(j, re.compile(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", re.I)) for j, ws in (names or []) for w in ws]
    nums = [(j, re.compile(r"(?:\bn°|\bN°|\bnum[ée]ros?|\bno\.)\s*" + n + r"(?!\d)", re.I)) for j, n in v1_numbers]
    fps = fingerprints(names)
    for f in files:
        try:
            with open(f, "rb") as fh:
                data = fh.read()
        except OSError:
            continue
        name = os.path.relpath(f, rel)
        for j, k, needle in exact:
            if needle in data:
                res.err(f"FUITE : {k} de la mythique {j} dans {name}")
        if not pats:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        low = text.lower()
        for j, fp in fps:
            if fp in low:
                res.err(f"FUITE : empreinte courte d'un secret de la mythique {j} dans {name}")
                break
        docs = _json_docs(text)
        if docs is not None:
            for j in _json_leaks(docs, pats):
                res.err(f"FUITE : nom ou ticker de la mythique {j} rattaché à une mythique dans {name}")
            continue
        for n, line in enumerate(text.split("\n"), 1):
            if not MYTHIC_WORD.search(line):
                continue
            for j, p in pats:
                if p.search(line):
                    res.err(f"FUITE : nom ou ticker de la mythique {j} associé à « mythique » dans {name}:{n}")
                    break
            for j, p in nums:
                if p.search(line):
                    res.err(f"FUITE : n° v1 de la mythique {j} associé à « mythique » dans {name}:{n}")
                    break


def _json_docs(text: str):
    """Documents JSON du fichier (un document, ou un par ligne pour du JSONL), sinon None."""
    try:
        return [json.loads(text)]
    except ValueError:
        pass
    lines = [x for x in text.split("\n") if x.strip()]
    try:
        return [json.loads(x) for x in lines] if lines else None
    except ValueError:
        return None


def _json_leaks(docs, pats) -> set:
    """En JSON : un objet de mythique (rareté mythique, engagement, préimage `card_id` + `content`)
    dont une valeur contient un vrai nom ou ticker. Les cartes visibles d'autres coins qui partagent
    un mot ou un ticker (« Baby … ») ne sont pas des fuites."""
    found = set()

    def strings(x):
        if isinstance(x, dict):
            for v in x.values():
                yield from strings(v)
        elif isinstance(x, list):
            for v in x:
                yield from strings(v)
        elif isinstance(x, str):
            yield x

    def walk(x):
        if isinstance(x, dict):
            tag = " ".join(str(x.get(k, "")) for k in ("rarity", "rarete", "rareté", "kind", "type"))
            mythic = (bool(re.search(r"mythi", tag, re.I)) or "commitment" in x or "mythic_index" in x
                      or ("card_id" in x and isinstance(x.get("content"), dict)))
            if mythic:
                for sv in strings(x):
                    for j, p in pats:
                        if p.search(sv):
                            found.add(j)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for d in docs:
        walk(d)
    return found


# ------------------------------------------------------------------ CLI


def validate(path, secrets_path=None, names_path=None, scan=(), git=False, max_rush_mean=0.8, max_normal_mean=1.0) -> tuple[Result, dict]:
    res = Result()
    public = []
    if path is None:
        names = load_names(names_path) if names_path and os.path.exists(names_path) else []
        v1 = load_v1_numbers(names_path) if names else []
        if not names:
            res.warn("fichier des vrais noms absent : seuls les secrets exacts de --secrets sont cherchés")
        files = _files(list(scan)) + (git_files() if git else [])
        secrets = load_secrets(secrets_path) if secrets_path else []
        scan_leaks(sorted(set(files)), secrets, names, res, v1_numbers=v1)
        return res, {"files_scanned": len(set(files))}
    if os.path.isdir(path):
        table = check_out_dir(path, res)
        public.append(path)
    else:
        with open(path, encoding="utf-8") as f:
            table = json.load(f)
        public.append(path)
    v = validate_table(table)
    res.errors += v.errors
    res.warnings += v.warnings
    summary = {}
    if v.ok:
        summary = economics(table, res, max_rush_mean, max_normal_mean)
    secrets = load_secrets(secrets_path) if secrets_path else []
    if secrets_path:
        check_preimages(table, secrets, res)
    names = load_names(names_path) if names_path and os.path.exists(names_path) else []
    v1 = load_v1_numbers(names_path) if names else []
    files = _files(public + list(scan)) + (git_files() if git else [])
    # Visuel « ? » commun (build_series.py --media-base / mythic_media) : public par construction,
    # écrit dans le manifeste et identique pour toutes les mythiques.
    shared = []
    manifest = os.path.join(path, "manifest.json") if os.path.isdir(path) else None
    if manifest and os.path.exists(manifest):
        with open(manifest, encoding="utf-8") as f:
            shared.append(json.load(f).get("mythic_media"))
    scan_leaks(sorted(set(files)), secrets, names, res, public_media=shared, v1_numbers=v1)
    summary["table_hash"] = core.table_hash(table).hex()
    summary["cards"] = len(table.get("cards", []))
    summary["files_scanned"] = len(set(files))
    return res, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", help="dossier de build_series.py (scripts/out/<slug>) ou table.json ; "
                    "sans lui, seul le contrôle anti-fuite tourne (--git ou --scan)")
    ap.add_argument("--secrets", help="préimages des mythiques (scripts/secrets/<slug>.json)")
    ap.add_argument("--mythiques", default=os.path.join(REPO, "docs", "data", "secrets", "mythiques.json"),
                    help="vrais noms des mythiques (ignoré s'il n'existe pas)")
    ap.add_argument("--scan", nargs="*", default=[], help="fichiers ou dossiers publics à contrôler en plus")
    ap.add_argument("--git", action="store_true", help="contrôle aussi tous les fichiers suivis par git")
    ap.add_argument("--max-rush-mean", type=float, default=0.8)
    ap.add_argument("--max-normal-mean", type=float, default=1.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.path is None and not (a.git or a.scan):
        ap.error("donner une table, ou --git / --scan pour le seul contrôle anti-fuite")
    res, summary = validate(a.path, a.secrets, a.mythiques, a.scan, a.git, a.max_rush_mean, a.max_normal_mean)
    if a.json:
        print(json.dumps({"ok": res.ok, "errors": res.errors, "warnings": res.warnings, "info": res.info,
                          "summary": summary}, ensure_ascii=False, indent=2))
    else:
        for x in res.info:
            print(f"  {x}")
        for x in res.warnings:
            print(f"ATTENTION : {x}")
        for x in res.errors:
            print(f"ERREUR : {x}")
        print(f"{'OK' if res.ok else 'REFUSÉ'} : {summary.get('cards')} cartes, table_hash {summary.get('table_hash')}, "
              f"{summary.get('files_scanned')} fichiers contrôlés, {len(res.errors)} erreur(s), {len(res.warnings)} avertissement(s)")
    return 0 if res.ok else 1


if __name__ == "__main__":
    sys.exit(main())
