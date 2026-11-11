#!/usr/bin/env python3
"""Construit les arguments des méthodes de série du contrat Memaster à partir du catalogue v2.

Usage (depuis contract/) :
    python3 scripts/build_series.py scripts/serie-exemple.json
        [--catalogue ../docs/data/catalogue-v2.json] [--out scripts/out/<slug>]
        [--secrets scripts/secrets/<slug>.json] [--series-id 0] [--new-secrets]
        [--mythiques ../docs/data/secrets/mythiques.json] [--tables-valeur fichier.json]

Vrais noms des mythiques : lus dans docs/data/secrets/mythiques.json (ignoré par git, --mythiques),
au format {"<id catalogue>": {"id": …, "nom": …, …}} (ou une liste d'objets portant "catalogue_id").
Si ce fichier manque, le script se replie sur le champ "secret" du catalogue s'il existe encore,
et s'arrête avec un message clair sinon.

Tables de valeur (mechanics.value, voir docs/mecaniques-spec.md) : dans les paramètres
("mechanics": {"value": …}) ou dans --tables-valeur, qui les remplace, au format
{"normale": [[bps, poids], …], "gold": […], "rush": […], "multiplicateurs": {"commune": x, …}}.

Bibliothèque standard uniquement. Produit, dans --out (aucun secret) :
    create_series_batched.json  {"table": …} : en-tête, mythiques et 1er lot de cartes
                                (create_series.json si la table tient en un lot)
    append_series_cards.NN.json {"series_id": …, "cards": […]} : lots suivants (batch_size cartes au plus)
    open_series.json            {"series_id": …}
    table.json                  table complète, octets exacts de `get_series_table` après chargement
    table_hash.txt              sha256 de table.json, calculé par le vérificateur (verifier/)
    manifest.json               résumé : nombre de cartes par rareté, lots, tailles, hash, et
                                `deposits` : dépôt (yoctoNEAR) à joindre à chaque appel
et, sous scripts/secrets/ (ignoré par git, mode 600) :
    <slug>.json                 préimages des mythiques (card_id, sel, contenu), écrit par gen_mythics.py
    <slug>.mythics-input.json   entrée de gen_mythics.py (contient les vrais noms)

Les mythiques ne figurent dans la table que par leurs engagements (commitment, content_hash, poids,
plafond). Les engagements et les sels sont produits par scripts/gen_mythics.py. Si le fichier de secrets
existe déjà, ses sels sont réutilisés (même table, même hash d'une exécution à l'autre) ; --new-secrets
en tire de nouveaux, ce qui change le hash.

Dépôts : create_series_batched et append_series_cards sont payables, et le contrat exige un dépôt au
moins égal au stockage qu'ils ajoutent (mesuré par env::storage_usage()), puis rend l'excédent. Le
script écrit dans manifest.json["deposits"] une borne haute par appel (voir storage_bound) : la taille
JSON des arguments majore la taille borsh stockée, plus une marge par bloc de 50 cartes et par série.
Exemple (near-cli-rs) :
    near contract call-function as-transaction <contrat> append_series_cards \
        file-args scripts/out/<slug>/append_series_cards.01.json prepaid-gas '300 Tgas' \
        attached-deposit '<deposits[nom] en yoctoNEAR> yoctonear' sign-as <owner> network-config testnet sign-with-keychain send

Mécaniques (`"mechanics"` dans les paramètres, voir docs/mecaniques-spec.md) : gold pack à plancher de
rareté par emplacement (`gold.slots`), table rush
donnée en poids ou en multiplicateurs des poids de base (la commune compense), pitié, plancher des
burns (plancher et a priori K), paramètres du rush, cartes ressuscitables (`resurrection` : liste de
card_id, ou règle `dead_epic_legendary` = épiques et légendaires mortes du catalogue, non adossées). Le contrat ne connaît pas la valeur des cartes : c'est ce script qui
contrôle la couverture (`coverage_check`, valeurs moyennes par rareté en multiples du prix) et refuse
une table rush au-delà de `max_rush` (80 %). Les couvertures calculées vont dans manifest.json.

Les cartes visibles sont triées par card_id (ordre exigé par le chargement par lots).
Un card_id du catalogue de plus de 64 octets (limite du contrat) est raccourci de façon déterministe :
55 premiers octets + "-" + 8 caractères hex de sha256(id). La correspondance est dans manifest.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.dirname(HERE)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "verifier"))

import gen_mythics  # noqa: E402  (canonical_content, content_json)
import validate_series  # noqa: E402  (règles du contrat, préimages révélables)
from memaster_verifier import canon, core  # noqa: E402

# Limites du contrat (src/lib.rs)
MAX_ID_LEN = 64
MAX_TITLE_LEN = 64
MAX_URL_LEN = 256
MAX_ASSET_ID_LEN = 128
MAX_CARDS_PER_CALL = 200
CARDS_PER_CHUNK = 50
MAX_RESURRECTABLE = 200
STORAGE_BYTE_COST = 10 ** 19          # yoctoNEAR par octet (protocole NEAR)
# Marges de storage_bound (octets) : enregistrement de série (champs fixes, flux de hachage,
# compteurs des mythiques) à la création, dernier card_id réécrit à chaque appel, et par bloc de
# cartes neuf (clé, 40 o d'enregistrement, longueur du vecteur).
CREATE_MARGIN = 2048
CALL_MARGIN = 512
CHUNK_MARGIN = 128

RARITY_FR = {"mythique": "mythic", "légendaire": "legendary", "épique": "epic", "rare": "rare",
             "commune": "common"}
# Bornes de la table de valeur (src/lib.rs).
MAX_VALUE_TIERS = 32
MIN_NORMAL_VALUE_BPS = 2_000
MAX_NORMAL_VALUE_BPS = 20_000
MAX_VALUE_BPS = 1_000_000
MAX_VALUE_MULT = 1_000_000
# Pitié (src/lib.rs) : probabilités en parties par milliard, garantie optionnelle bornée.
PPB = 1_000_000_000
MAX_PITY_N = 10_000
DEFAULT_MYTHICS = os.path.join(REPO, "docs", "data", "secrets", "mythiques.json")
VISIBLE = ("legendary", "epic", "rare", "common")


def short_id(cid: str) -> str:
    if len(cid.encode("utf-8")) <= MAX_ID_LEN:
        return cid
    return cid.encode("utf-8")[:55].decode("utf-8", "ignore").rstrip("-") + "-" + \
        hashlib.sha256(cid.encode("utf-8")).hexdigest()[:8]


def check_len(s, mx, what):
    if s is None:
        return
    n = len(s.encode("utf-8"))
    if not 1 <= n <= mx:
        raise SystemExit(f"{what} : longueur {n} hors de [1, {mx}] : {s!r}")


def fmt(template, cid):
    return None if template is None else template.replace("{id}", cid)


def backing_of(b):
    if b is None:
        return None
    amount = int(b["amount"])
    if amount <= 0 or amount >= 1 << 128:
        raise SystemExit(f"amount invalide pour {b.get('card_id')}")
    check_len(b["asset_id"], MAX_ASSET_ID_LEN, "asset_id")
    return {"asset_id": str(b["asset_id"]), "amount": str(amount)}


def storage_bound(args_bytes, first_index, count, create):
    """Borne haute du stockage (octets) ajouté par un appel de chargement par lots.

    Une carte est stockée en borsh dans son bloc (chaînes préfixées par 4 octets, options sur 1,
    `amount` sur 16) et laisse 14 o au plus dans la série (rareté, poids, plafond, compteur) : c'est
    moins que sa forme JSON, dont les noms de champs et les `null` coûtent à eux seuls plus de 90 o.
    Idem pour l'en-tête. Le contrat rend l'excédent, une borne large ne coûte rien."""
    new_chunks = sum(1 for i in range(first_index, first_index + count) if i % CARDS_PER_CHUNK == 0)
    return args_bytes + CALL_MARGIN + CHUNK_MARGIN * new_chunks + (CREATE_MARGIN if create else 0)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def write_secret(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.chmod(path, 0o600)


def mythic_commitments(entries, secrets_path, new_secrets):
    """Engagements publics des mythiques, via gen_mythics.py. Réutilise les sels existants."""
    input_path = secrets_path[: -len(".json")] + ".mythics-input.json"
    write_secret(input_path, entries)
    if new_secrets or not os.path.exists(secrets_path):
        public_tmp = secrets_path[: -len(".json")] + ".public.json"
        subprocess.run([sys.executable, os.path.join(HERE, "gen_mythics.py"), input_path, public_tmp,
                        secrets_path], check=True, stdout=subprocess.DEVNULL)
        os.remove(public_tmp)
    with open(secrets_path, encoding="utf-8") as f:
        private = json.load(f)
    if len(private) != len(entries):
        raise SystemExit(f"{secrets_path} : {len(private)} mythiques au lieu de {len(entries)} (--new-secrets ?)")
    public = []
    for e, p in zip(entries, private):
        content = gen_mythics.canonical_content(e["content"])
        if p["card_id"] != e["card_id"] or p["content"] != content:
            raise SystemExit(f"{secrets_path} ne correspond plus au catalogue ou aux paramètres "
                             f"(mythique {p['mythic_index']}) : relancer avec --new-secrets")
        sel = bytes.fromhex(p["sel"])
        if len(sel) != 32:
            raise SystemExit("sel de 32 octets attendu")
        commitment = hashlib.sha256(e["card_id"].encode("utf-8") + sel).hexdigest()
        content_hash = hashlib.sha256(gen_mythics.content_json(content) + sel).hexdigest()
        # Contrôle croisé avec l'implémentation indépendante du vérificateur.
        c2, h2 = core.mythic_commitments(e["card_id"], sel, content)
        assert (c2.hex(), h2.hex()) == (commitment, content_hash)
        assert (p["commitment"], p["content_hash"]) == (commitment, content_hash)
        public.append({"commitment": commitment, "content_hash": content_hash,
                       "weight": int(e["weight"]), "cap": int(e["cap"])})
    return public


def rarity_key(r):
    """Rareté en anglais (forme du contrat) depuis le français ou l'anglais."""
    r2 = RARITY_FR.get(r, r)
    if r2 not in canon.RARITY_NAMES:
        raise SystemExit(f"rareté inconnue : {r!r}")
    return r2


def load_mythic_secrets(path, catalogue):
    """Vrais noms des mythiques, par id du catalogue : `path` (docs/data/secrets/mythiques.json), ou
    repli sur le champ `secret` du catalogue s'il existe encore. Erreur claire sinon."""
    mythic_ids = [c["id"] for c in catalogue if c.get("section") == "catalogue" and RARITY_FR.get(c["rarete"]) == "mythic"]
    if not mythic_ids:
        return {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("mythiques"), list):
            data = data["mythiques"]
        if isinstance(data, list):
            by_id = {}
            for e in data:
                key = e.get("catalogue_id") or e.get("id_catalogue")
                if key is None and e.get("id") in mythic_ids:
                    # format écrit par consolider.py : {"mythiques": [{"id": "<id catalogue>", "nom": …}]}
                    key = e["id"]
                if key is None:
                    raise SystemExit(f"{path} : chaque mythique doit porter \"catalogue_id\" (id du catalogue)")
                by_id[key] = e.get("secret", e)
            data = by_id
        missing = [i for i in mythic_ids if i not in data]
        if missing:
            raise SystemExit(f"{path} : mythiques absentes {missing} (attendu : {{\"<id catalogue>\": {{\"id\": …, \"nom\": …}}}})")
        for i in mythic_ids:
            if not data[i].get("id") or not data[i].get("nom"):
                raise SystemExit(f"{path} : {i} sans \"id\" ni \"nom\"")
        return {i: data[i] for i in mythic_ids}
    secrets = {c["id"]: c.get("secret") for c in catalogue if c["id"] in mythic_ids}
    if all(secrets.values()):
        print(f"attention : {os.path.relpath(path, REPO)} introuvable, vrais noms des mythiques lus dans le "
              "champ \"secret\" du catalogue (repli, à retirer quand le fichier sera en place)", file=sys.stderr)
        return secrets
    raise SystemExit(
        f"Vrais noms des mythiques introuvables : {path} n'existe pas (fichier secret, ignoré par git, au format "
        "{\"<id catalogue>\": {\"id\": …, \"nom\": …}}) et le catalogue n'a plus de champ \"secret\" "
        f"pour {[i for i, v in secrets.items() if not v]}. Récupérer le fichier auprès du porteur, ou passer --mythiques.")


def build(params, catalogue, secrets_path, new_secrets, mythic_secrets=None):
    cards_src = [c for c in catalogue if c.get("section") == "catalogue"]
    ids = [c["id"] for c in cards_src]
    if len(set(ids)) != len(ids):
        raise SystemExit("id en double dans le catalogue")
    burn = {}
    for b in params.get("burnables", []):
        if b["card_id"] not in ids:
            raise SystemExit(f"brûlable inconnu du catalogue : {b['card_id']}")
        if b["card_id"] in burn:
            raise SystemExit(f"brûlable en double : {b['card_id']}")
        burn[b["card_id"]] = backing_of(b)
    overrides = params.get("card_overrides", {})
    media_t, ref_t = params.get("media_template"), params.get("reference_template")

    cards, mythic_entries, renamed, etat = [], [], {}, {}
    for c in cards_src:
        rarity = RARITY_FR[c["rarete"]]
        if rarity == "mythic":
            s = (mythic_secrets or {}).get(c["id"]) or c.get("secret")
            if not s:
                raise SystemExit(f"vrai nom de la mythique {c['id']} introuvable (load_mythic_secrets)")
            m = params.get("mythic", {})
            mythic_entries.append({
                "card_id": s["id"],
                "weight": int(m.get("weight", 1)),
                "cap": int(m.get("cap", 1)),
                "content": {"title": s["nom"], "media": fmt(media_t, s["id"]),
                            "reference": fmt(ref_t, s["id"]), "backing": burn.get(c["id"])},
            })
            continue
        cid = short_id(c["id"])
        if cid != c["id"]:
            renamed[c["id"]] = cid
        o = overrides.get(c["id"], {})
        card = {
            "card_id": cid,
            "title": o.get("title", c["nom"]),
            "rarity": rarity,
            "weight": int(o.get("weight", params["card_weights"][rarity])),
            "cap": o.get("cap", params.get("caps", {}).get(rarity)),
            "media": fmt(media_t, cid),
            "reference": fmt(ref_t, cid),
            "backing": burn.get(c["id"]),
        }
        etat[cid] = c.get("etat") or ""
        check_len(card["card_id"], MAX_ID_LEN, "card_id")
        check_len(card["title"], MAX_TITLE_LEN, f"title de {cid}")
        check_len(card["media"], MAX_URL_LEN, "media")
        check_len(card["reference"], MAX_URL_LEN, "reference")
        cards.append(card)
    if len({c["card_id"] for c in cards}) != len(cards):
        raise SystemExit("card_id en double après raccourcissement")
    # Par lots, le contrat exige des card_id strictement croissants (octets UTF-8) : c'est ainsi
    # qu'il garantit leur unicité sans relire la table. L'ordre de la table n'a pas d'autre effet.
    cards.sort(key=lambda c: c["card_id"].encode("utf-8"))

    mythics = mythic_commitments(mythic_entries, secrets_path, new_secrets) if mythic_entries else []
    table = {
        "name": params["name"],
        "price": str(int(params["price_yocto"])),
        "cards_per_pack": int(params["cards_per_pack"]),
        "rarity_weights": {r: int(params["rarity_weights"][r]) for r in canon.RARITY_NAMES},
        "cards": cards,
        "mythics": mythics,
        "royalties": params.get("royalties", []),
    }
    coverage = None
    if params.get("mechanics"):
        table["mechanics"], coverage = build_mechanics(params, table, etat)
    return table, renamed, coverage


def scaled_weights(base, mult):
    """Poids de rareté multipliés (`mult` : rareté → facteur, arrondi au plus proche) ; la commune
    compense, pour garder le même total."""
    total = sum(base[r] for r in canon.RARITY_NAMES)
    out = {r: int(round(base[r] * float(mult.get(r, 1)))) for r in canon.RARITY_NAMES if r != "common"}
    out["common"] = total - sum(out.values())
    if out["common"] <= 0:
        raise SystemExit(f"multiplicateurs trop forts : plus de poids pour la commune ({mult})")
    return {r: out[r] for r in canon.RARITY_NAMES}


def table_coverage(weights, cards_per_pack, value):
    """Couverture d'une table de taux : espérance de valeur brûlable d'un pack, en multiples du prix.
    `value[r]` = valeur moyenne d'un emplacement de rareté r (brûlables et cartes de collection
    confondues), en multiples du prix du pack."""
    total = sum(weights[r] for r in canon.RARITY_NAMES)
    return cards_per_pack * sum(weights[r] / total * float(value.get(r, 0)) for r in canon.RARITY_NAMES)


def resurrectable_indices(spec, cards, etat):
    """Index (croissants) des cartes ressuscitables : `card_ids` explicites, ou la règle
    `dead_epic_legendary` (épiques et légendaires « mort… » dans le catalogue, non adossées).
    Le contrat refuse toute autre carte (rare, commune, adossée par la table)."""
    index = {c["card_id"]: i for i, c in enumerate(cards)}
    if "card_ids" in spec:
        out = []
        for cid in spec["card_ids"]:
            if cid not in index:
                raise SystemExit(f"resurrection : carte inconnue {cid}")
            out.append(index[cid])
    elif spec.get("rule") == "dead_epic_legendary":
        out = [i for i, c in enumerate(cards) if c["rarity"] in ("epic", "legendary")
               and etat.get(c["card_id"], "").startswith("mort")]
    else:
        raise SystemExit("mechanics.resurrection : card_ids ou rule = dead_epic_legendary")
    out = sorted(set(out))
    for i in out:
        c = cards[i]
        if c["rarity"] not in ("epic", "legendary") or c["backing"] is not None:
            raise SystemExit(f"resurrection : {c['card_id']} n'est pas une épique ou légendaire non adossée")
    if len(out) > MAX_RESURRECTABLE:
        raise SystemExit(f"resurrection : {len(out)} cartes, {MAX_RESURRECTABLE} au plus")
    return out


def gold_slots(spec, base):
    """Gold pack : un emplacement par entrée, `floor` (plancher), `weights` (poids propres, nuls sous
    le plancher ; absents = poids de base tronqués), `burnable` (tiré parmi les brûlables)."""
    slots = []
    if not 1 <= len(spec.get("slots", [])) <= 10:
        raise SystemExit("mechanics.gold.slots : 1 à 10 emplacements")
    for i, x in enumerate(spec["slots"]):
        floor = rarity_key(x["floor"])
        f = canon.RARITY_NAMES.index(floor)
        w = None
        if x.get("weights") is not None:
            w = {r: 0 for r in canon.RARITY_NAMES}
            for k, v in x["weights"].items():
                w[rarity_key(k)] = int(v)
            if any(w[r] for r in canon.RARITY_NAMES[f + 1:]):
                raise SystemExit(f"gold.slots[{i}] : poids sous le plancher {floor}")
        eff = w or {r: (base[r] if canon.RARITY_NAMES.index(r) <= f else 0) for r in canon.RARITY_NAMES}
        if sum(eff.values()) == 0:
            raise SystemExit(f"gold.slots[{i}] : aucun poids au-dessus du plancher {floor}")
        slots.append({"floor": floor, "weights": w, "burnable": bool(x.get("burnable", False))})
    return {"slots": slots}


def value_tables(spec, price):
    """Tables de valeur au format {"normale": [[bps, poids], …], "gold": […], "rush": […],
    "multiplicateurs": {"commune": x, …}} (clés anglaises acceptées). Mêmes contrôles que le contrat.
    Multiplicateurs : entiers gardés tels quels ; s'il y a des décimales, tous sont multipliés par
    1 000 et arrondis (seuls leurs rapports comptent). Mythique : 0 (adossement de son contenu)."""
    def tiers(key, alt, lo, hi):
        t = spec.get(key, spec.get(alt))
        if not isinstance(t, list) or not 1 <= len(t) <= MAX_VALUE_TIERS:
            raise SystemExit(f"tables de valeur : « {key} » doit avoir 1 à {MAX_VALUE_TIERS} paliers [bps, poids]")
        out = []
        for bps, w in t:
            bps, w = int(bps), int(w)
            if w <= 0 or not lo <= bps <= hi:
                raise SystemExit(f"tables de valeur : palier {key} [{bps}, {w}] hors bornes ([{lo}, {hi}] pb, poids > 0)")
            out.append([bps, w])
        return out
    v = {
        "normal": tiers("normale", "normal", MIN_NORMAL_VALUE_BPS, MAX_NORMAL_VALUE_BPS),
        "gold": tiers("gold", "or", 1, MAX_VALUE_BPS),
        "rush": tiers("rush", "rush", 1, MAX_VALUE_BPS),
    }
    raw = spec.get("multiplicateurs", spec.get("multipliers"))
    if not isinstance(raw, dict):
        raise SystemExit("tables de valeur : « multiplicateurs » manquant")
    mult = {r: 0.0 for r in canon.RARITY_NAMES}
    for k, x in raw.items():
        mult[rarity_key(k)] = float(x)
    if mult["mythic"]:
        raise SystemExit("tables de valeur : multiplicateur mythique = 0 (une mythique garde l'adossement de son contenu)")
    scale = 1 if all(float(x).is_integer() for x in mult.values()) else 1000
    v["multipliers"] = {r: int(round(mult[r] * scale)) for r in canon.RARITY_NAMES}
    for r in ("legendary", "epic", "rare", "common"):
        if not 1 <= v["multipliers"][r] <= MAX_VALUE_MULT:
            raise SystemExit(f"tables de valeur : multiplicateur {r} hors de [1, {MAX_VALUE_MULT}]")
    max_bps = max(b for t in (v["normal"], v["gold"], v["rush"]) for b, _ in t)
    if int(price) * max_bps // 10_000 * max(v["multipliers"].values()) >= 1 << 128:
        raise SystemExit("tables de valeur : prix trop élevé (dépassement de u128 au tirage)")
    return v


def pity_params(spec):
    """Pitié en ppb (10⁹) : `p0_ppb`, `k_ppb`, `p_max_ppb`, `n_max` (optionnel, `null` = aucune
    garantie). Mêmes contrôles que le contrat (src/mechanics.rs)."""
    if "p0_ppm" in spec or "k_ppm" in spec:
        raise SystemExit("mechanics.pity : p0_ppm / k_ppm retirés, la pitié est en ppb (p0_ppb, k_ppb, p_max_ppb, n_max)")
    p = {k: int(spec[k]) for k in ("p0_ppb", "k_ppb", "p_max_ppb")}
    n = spec.get("n_max")
    p["n_max"] = None if n is None else int(n)
    if any(not 0 <= p[k] <= PPB for k in ("p0_ppb", "k_ppb", "p_max_ppb")):
        raise SystemExit("mechanics.pity : probabilités en ppb, dans [0, 10⁹]")
    if p["p0_ppb"] > p["p_max_ppb"]:
        raise SystemExit("mechanics.pity : p0_ppb ≤ p_max_ppb")
    if p["n_max"] is not None and not 1 <= p["n_max"] <= MAX_PITY_N:
        raise SystemExit(f"mechanics.pity.n_max : absent, ou 1 à {MAX_PITY_N}")
    if p["p_max_ppb"] == 0 and p["n_max"] is None:
        raise SystemExit("mechanics.pity : gold pack inatteignable (p_max_ppb = 0 sans n_max)")
    return {k: p[k] for k in ("p0_ppb", "k_ppb", "p_max_ppb", "n_max")}


def mean_value(tiers):
    """Valeur moyenne d'une table, en multiples du prix."""
    return sum(b * w for b, w in tiers) / sum(w for _, w in tiers) / 10_000


def build_mechanics(params, table, etat=None):
    """Mécaniques de la table (hachées avec elle). Contrôle hors chaîne de la couverture : le contrat
    ne sait pas ce que vaut une carte de collection, c'est ce script qui refuse une table rush trop
    généreuse."""
    m = params["mechanics"]
    base = table["rarity_weights"]
    out = {"gold": None, "pity": None, "burn": None, "rush": None, "resurrection": None, "value": None}
    if m.get("gold_weights") or m.get("gold_multipliers"):
        raise SystemExit("gold_weights / gold_multipliers retirés : le gold pack se décrit par mechanics.gold.slots (plancher par emplacement)")
    if m.get("gold"):
        out["gold"] = gold_slots(m["gold"], base)
    if m.get("pity"):
        out["pity"] = pity_params(m["pity"])
    if m.get("burn"):
        out["burn"] = {"floor_bps": int(m["burn"]["floor_bps"]), "prior_k": int(m["burn"]["prior_k"])}
    if m.get("rush"):
        r = m["rush"]
        weights = r.get("weights") or scaled_weights(base, r["multipliers"])
        out["rush"] = {k: int(r[k]) for k in ("ratio_bps", "min_packs", "window_blocks", "baseline_blocks",
                                               "bucket_blocks", "duration_blocks", "cooldown_blocks",
                                               "max_per_account")}
        out["rush"]["weights"] = weights
    if m.get("resurrection"):
        out["resurrection"] = {"eligible": resurrectable_indices(m["resurrection"], table["cards"], etat or {})}
    if m.get("value"):
        out["value"] = value_tables(m["value"], table["price"])
    if out["value"] or (out["gold"] and any(s["burnable"] for s in out["gold"]["slots"])):
        # Brûlable garantie : même règle que le contrat (refusé à l'ouverture sinon).
        if not any(c["backing"] and c["cap"] is None and c["weight"] > 0 for c in table["cards"]):
            raise SystemExit("brûlable garantie : il faut une carte adossée, sans plafond et de poids non nul "
                             "(par exemple une commune ou une rare brûlable illimitée)")
    coverage = None
    chk = m.get("coverage_check")
    if out["value"]:
        # Valeur tirée par pack : la couverture est la valeur moyenne de chaque table.
        v = out["value"]
        coverage = {"base": mean_value(v["normal"]), "gold": mean_value(v["gold"]), "rush": mean_value(v["rush"]),
                    "source": "tables de valeur (valeur moyenne en multiples du prix)"}
        max_rush = float((chk or {}).get("max_rush", 0.8))
        if out["rush"] and coverage["rush"] > max_rush + 1e-9:
            raise SystemExit(f"table de valeur rush refusée : moyenne {coverage['rush']:.3f} > plafond {max_rush} "
                             "(acheter pendant un rush serait à espérance positive)")
    elif chk:
        n = table["cards_per_pack"]
        coverage = {"base": table_coverage(base, n, chk["rarity_value"])}
        if out["gold"]:
            coverage["gold"] = sum(
                table_coverage(core.gold_slot_weights(base, s), 1, chk["rarity_value"]) for s in out["gold"]["slots"])
        if out["rush"]:
            coverage["rush"] = table_coverage(out["rush"]["weights"], n, chk["rarity_value"])
            if coverage["rush"] > float(chk["max_rush"]) + 1e-9:
                raise SystemExit(
                    f"table rush refusée : couverture {coverage['rush']:.3f} > plafond {chk['max_rush']} "
                    "(acheter pendant un rush serait à espérance positive)")
    if out["rush"] and coverage is None:
        raise SystemExit("mechanics.rush exige mechanics.value ou mechanics.coverage_check (contrôle de la couverture hors chaîne)")
    return out, coverage


def sim_value_tables(tv):
    """Tables de valeur de --tables-valeur : format de ce script ({"normale": …, "multiplicateurs": …}),
    ou format publié par la simulation (sim/resultats/serie*/tables-valeur.json :
    {"value_tables": {"base"|"gold"|"rush": {"tiers": […]}}, "split_multipliers": {…}})."""
    if "value_tables" not in tv:
        return tv
    vt = tv["value_tables"]
    try:
        return {"normale": vt["base"]["tiers"], "gold": vt["gold"]["tiers"], "rush": vt["rush"]["tiers"],
                "multiplicateurs": tv["split_multipliers"]}
    except KeyError as e:
        raise SystemExit(f"--tables-valeur : format de la simulation incomplet ({e})")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("params")
    ap.add_argument("--catalogue", default=os.path.join(REPO, "docs", "data", "catalogue-v2.json"))
    ap.add_argument("--out")
    ap.add_argument("--secrets")
    ap.add_argument("--series-id", type=int, default=0,
                    help="identifiant renvoyé par create_series (get_series_count avant la création)")
    ap.add_argument("--new-secrets", action="store_true", help="tire de nouveaux sels (change le hash)")
    ap.add_argument("--mythiques", default=DEFAULT_MYTHICS,
                    help="vrais noms des mythiques (fichier secret, ignoré par git)")
    ap.add_argument("--tables-valeur", help="tables de valeur (remplacent mechanics.value des paramètres)")
    a = ap.parse_args(argv)

    with open(a.params, encoding="utf-8") as f:
        params = json.load(f)
    with open(a.catalogue, encoding="utf-8") as f:
        catalogue = json.load(f)
    if a.tables_valeur:
        with open(a.tables_valeur, encoding="utf-8") as f:
            tv = json.load(f)
        if not params.get("mechanics"):
            raise SystemExit("--tables-valeur exige des mécaniques dans les paramètres")
        params["mechanics"]["value"] = sim_value_tables(tv)
    mythic_secrets = load_mythic_secrets(a.mythiques, catalogue)
    slug = params.get("slug", "serie")
    out = a.out or os.path.join(HERE, "out", slug)
    secrets_path = a.secrets or os.path.join(HERE, "secrets", f"{slug}.json")
    if not secrets_path.endswith(".json"):
        raise SystemExit("--secrets doit finir par .json")
    if os.path.commonpath([os.path.abspath(out), os.path.join(HERE, "secrets")]) == os.path.join(HERE, "secrets"):
        raise SystemExit("--out ne doit pas être sous scripts/secrets/")

    table, renamed, coverage = build(params, catalogue, secrets_path, a.new_secrets, mythic_secrets)
    # Mêmes règles que le contrat (validate_table, à l'ouverture) et préimages révélables : une table
    # refusée l'est ici, avant d'avoir payé le chargement, et jamais après l'ouverture.
    check = validate_series.validate_table(table)
    if table["mythics"] and os.path.exists(secrets_path):
        validate_series.check_preimages(table, validate_series.load_secrets(secrets_path), check)
    if not check.ok:
        raise SystemExit("table refusée (règles du contrat, voir validate_series.py) :\n- " + "\n- ".join(check.errors))

    # Hash : vérificateur Python (canon.py reproduit serde_json::to_vec).
    table_bytes = canon.table_json_bytes(table)
    h = core.table_hash(table).hex()
    assert json.loads(table_bytes) == table

    batch = int(params.get("batch_size", MAX_CARDS_PER_CALL))
    if not 1 <= batch <= MAX_CARDS_PER_CALL:
        raise SystemExit(f"batch_size dans [1, {MAX_CARDS_PER_CALL}]")
    lots = [table["cards"][i:i + batch] for i in range(0, len(table["cards"]), batch)] or [[]]
    os.makedirs(out, exist_ok=True)
    for name in os.listdir(out):
        if name.startswith("append_series_cards."):
            os.remove(os.path.join(out, name))
    first = dict(table, cards=lots[0])
    for name in ("create_series.json", "create_series_batched.json"):
        if os.path.exists(os.path.join(out, name)):
            os.remove(os.path.join(out, name))
    files = {("create_series_batched.json" if len(lots) > 1 else "create_series.json"): {"table": first}}
    for i, lot in enumerate(lots[1:], start=1):
        files[f"append_series_cards.{i:02d}.json"] = {"series_id": a.series_id, "cards": lot}
    files["open_series.json"] = {"series_id": a.series_id}
    sizes, deposits = {}, {}
    first_index = 0
    for name, obj in files.items():
        write_json(os.path.join(out, name), obj)
        sizes[name] = os.path.getsize(os.path.join(out, name))
        if name.startswith("create_series_batched") or name.startswith("append_series_cards."):
            cards = obj["table"]["cards"] if "table" in obj else obj["cards"]
            create = name.startswith("create_series_batched")
            bound = storage_bound(sizes[name], first_index, len(cards), create)
            # Arrondi au millième de NEAR supérieur.
            deposits[name] = str(-(-bound * STORAGE_BYTE_COST // 10 ** 21) * 10 ** 21)
            first_index += len(cards)
        else:
            # create_series (table en un lot) et open_series ne sont pas payables.
            deposits[name] = "0"
    with open(os.path.join(out, "table.json"), "wb") as f:
        f.write(table_bytes)
    with open(os.path.join(out, "table_hash.txt"), "w") as f:
        f.write(h + "\n")

    counts = {r: sum(1 for c in table["cards"] if c["rarity"] == r) for r in VISIBLE}
    counts["mythic"] = len(table["mythics"])
    manifest = {
        "table_hash": h,
        "table_bytes": len(table_bytes),
        "cards": len(table["cards"]),
        "per_rarity": counts,
        "burnable_cards": sum(1 for c in table["cards"] if c["backing"]),
        "batch_size": batch,
        "calls": list(files),
        "args_bytes": sizes,
        "deposits": deposits,
        "deposit_total_near": f"{sum(int(d) for d in deposits.values()) / 10 ** 24:.3f}",
        "renamed_ids": renamed,
        "mechanics": table.get("mechanics"),
        "resurrectable": [table["cards"][i]["card_id"] for i in
                          ((table.get("mechanics") or {}).get("resurrection") or {}).get("eligible", [])],
        "coverage": coverage,
        "secrets_file": os.path.relpath(secrets_path, CONTRACT),
    }
    write_json(os.path.join(out, "manifest.json"), manifest)

    # Garde-fou : aucun vrai nom de mythique (titre exact, en chaîne JSON) dans les sorties publiques.
    names = [json.dumps(x["nom"], ensure_ascii=False).encode("utf-8") for x in mythic_secrets.values()]
    if os.path.exists(secrets_path):
        with open(secrets_path, encoding="utf-8") as f:
            names += [json.dumps(p["content"]["title"], ensure_ascii=False).encode("utf-8")
                      for p in json.load(f)]
    if names:
        for name in os.listdir(out):
            with open(os.path.join(out, name), "rb") as f:
                data = f.read()
            for n in names:
                if n in data:
                    raise SystemExit(f"FUITE : un nom de mythique apparaît dans {name}")
    print(f"{manifest['cards']} cartes visibles + {counts['mythic']} engagements mythiques, "
          f"{len(files)} appels -> {out}")
    print(f"table_hash = {h} ({len(table_bytes)} octets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
