#!/usr/bin/env python3
"""Fusionne la recherche v2 en catalogue v2 (Memaster).

Entrées (relatives à la racine du dépôt) :
  docs/catalogue-final.md                 catalogue v1 (Cartes + À décider)
  docs/recherche-v2/r5-audit-catalogue.md audit de v1, doublons, candidats C1/C2
  docs/recherche-v2/r1..r3-*.md           nouveaux jetons + corrections
  docs/recherche-v2/r4-autres-chaines.md  pris s'il existe
  --extra FICHIER                         autre lot au même format (répétable)
  docs/data/coingecko-meme-2026-11-11.csv relevé CoinGecko (état, rapprochement)

Sorties : docs/catalogue-v2.md et docs/data/catalogue-v2.json (publics, sans le vrai nom des mythiques),
          docs/data/secrets/mythiques.json (vrais noms des mythiques, ignoré par git, mode 600).
  --demo : en plus, docs/catalogue-demo.md et docs/data/catalogue-demo.json (catalogue de démo filtré,
           champ `brulable_possible` et sa raison).

Relancer : python3 docs/recherche-v2/consolider.py [--demo] [--extra lot.md] [--out-dir DIR]
Python 3 stdlib uniquement, aucun appel réseau.
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATE = "11/11/2026"

RARETES = ["mythique", "légendaire", "épique", "rare", "commune"]
# Quelles cartes v1 sont mythiques : lu dans le fichier secret (ignoré par git), jamais écrit ici,
# ni en clair ni en empreinte (une empreinte courte d'un ticker se retrouve par force brute).
SECRETS = os.path.join(ROOT, "docs", "data", "secrets", "mythiques.json")
RE_ORIGINE_V1 = re.compile(r"^v1 n° ?(\d+)$")


def charger_mythiques_v1(path):
    """{n° v1 : ticker} des mythiques, d'après `origines` (« v1 n° X ») et `ticker` du fichier secret."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("mythiques", []) if isinstance(data, dict) else data
    out = {}
    for e in items:
        nums = [m.group(1) for m in (RE_ORIGINE_V1.match(o.strip()) for o in e.get("origines", [])) if m]
        if len(nums) != 1 or not e.get("ticker"):
            raise SystemExit("%s : chaque mythique doit avoir un ticker et une origine « v1 n° X »" % path)
        out[nums[0]] = e["ticker"]
    return out
BURN = "à définir"

# Doublons relevés par R5 : (gardé, absorbé)
FUSIONS_FORCEES = [
    ("99", "709", "R5 : même chaîne Pepecoin de 2016 (`pepecoin-network`)"),
    ("185", "558", "R5 : même ticker TYBG, même chaîne Base, un seul jeton CoinGecko (`base-god`)"),
    ("D59", "D41", "R5 : CoinGecko ne connaît que `trumpcoin` (ticker DJT)"),
    ("D26", "D24", "R5 : CoinGecko ne connaît que `red-kitten-crew` (ticker RKC)"),
]

# Candidats C1 dont la nature de mème est douteuse (jugement de consolidation) :
# envoyés dans « À décider », pas au catalogue.
C1_NATURE_DOUTEUSE = {
    "hatom": "protocole DeFi (MultiversX), pas un mème ?",
    "ahatoken": "jeton utilitaire, pas un mème ?",
    "aavegotchi": "jeu NFT / DeFi, pas un mème ?",
    "carrot-by-puffer": "jeton DeFi (Puffer), pas un mème ?",
    "araistotle": "agent IA présenté comme produit ?",
    "opus-2": "agent IA présenté comme produit ?",
    "tabbypos": "jeton de paiement, pas un mème ?",
    "up-token-2": "jeton utilitaire, pas un mème ?",
    "ftmtoken": "jeton utilitaire, pas un mème ?",
}

# Doutes explicites des chercheurs, hors motif « à trancher » détecté dans la ligne.
DOUTES_EXPLICITES = [
    # (fichier source commence par, ticker, motif, pic à traiter comme estimé)
    ("r3", "SKBDI", "r3 : peut-être la carte v1 n° 747 « Skibidi » (homonyme à vérifier)", False),
    ("r4", "SHIBTC", "r4 : capitalisation CMC ≈ 1 Md$ « très douteuse » (offre auto-déclarée) ; "
                     "pic traité comme estimé", True),
    ("r4", "AKUMA", "r4 : capitalisation CMC probablement fondée sur une offre mal déclarée ; "
                    "pic traité comme estimé", True),
    ("r4", "DUCKY", "r4 : capitalisation CMC probablement fondée sur une offre mal déclarée ; "
                    "pic traité comme estimé", True),
]
RE_DOUTE = re.compile(
    r"à trancher|nature (?:contradictoire|floue|à vérifier)|pas (?:forcément )?un mème|"
    r"peut-être (?:la carte|le même)|homonyme à vérifier", re.I)
RE_CANNABIS = re.compile(r"cannabis|weed|marijuana|ganja|hemp|kush|sativa", re.I)

# Drapeaux déduits du nom quand la source n'a pas de colonne Drapeau (v1, C1).
DRAPEAU_MOTS = OrderedDict([
    ("politique", r"trump|biden|boden|tremp|kamala|horris|maga|putin|putni|brandon|melania|obama|milei|"
                  r"burnie senders|bernie|djt|barron|agenda 47|america party"),
    ("personne réelle", r"elon|musk|tate|kardashian|jenner|logan paul|derulo|mbapp|sweeney|"
                        r"hulk hogan|doja|bitboy|rich the kid|askren|cr7|altman|mcafee|hawk tuah"),
    ("obscène", r"swasti|hitler|nazi|dick|cum|fap|cock|pussy|butt|assdaq|shit|gooner|goon|sperm|tit|"
                r"sex|porn|whore|retard|tardio|boner|testicle|groyper|chud"),
])

RE_MONTANT = re.compile(
    r"(\d{1,3}(?:[  ]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)\s*"
    r"(?:(?:à|-|–)\s*(\d{1,3}(?:[  ]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)\s*)?"
    r"(k|M|Mds|Md|B|Bn)\s?\$")
UNITES = {"k": 1e3, "M": 1e6, "Md": 1e9, "Mds": 1e9, "B": 1e9, "Bn": 1e9}


# ----------------------------------------------------------------- utilitaires

def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def nombre(txt):
    return float(txt.replace(" ", "").replace(" ", "").replace(",", "."))


def parse_montant(texte):
    """Premier montant en k$/M$/Md$ (bas de fourchette), en dollars. None si inconnu."""
    if not texte:
        return None
    t = texte.strip()
    if t.lower().startswith("inconnu") or t in ("—", "-"):
        return None
    m = RE_MONTANT.search(t)
    if not m:
        return None
    return nombre(m.group(1)) * UNITES[m.group(3)]


def est_borne_basse(texte):
    return bool(re.match(r"\s*(≥|>|plus de|au moins)", texte or ""))


def norm_nature(n):
    n = sans_accents((n or "").lower())
    if n.startswith("source") or n.startswith("corrige"):
        return "sourcé"
    if n.startswith("estime") or "plancher" in n:
        return "estimé"
    return "inconnu"


RANG_NATURE = {"sourcé": 2, "estimé": 1, "inconnu": 0}


def norm_rarete(r):
    """Premier mot de rareté trouvé dans un texte libre ('épique*', 'reste rare'…)."""
    if not r:
        return ""
    t = sans_accents(r.lower())
    best = None
    for nom in RARETES:
        m = re.search(r"\b" + sans_accents(nom) + r"\b", t)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), nom)
    return best[1] if best else ""


def norm_nom(nom, garder_parentheses=False):
    """Nom normalisé strict : minuscules, sans accents, †, [OLD], parenthèses, ponctuation."""
    s = sans_accents(nom or "").lower()
    s = s.replace("†", "")
    s = re.sub(r"\[[^\]]*\]", " ", s)
    if not garder_parentheses:
        s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^\w]+", " ", s, flags=re.U).strip()
    return re.sub(r"\s+", " ", s)


def nom_souple(nom):
    """Nom strict sans espaces et sans suffixe inu/coin/token (s'il reste quelque chose)."""
    s = norm_nom(nom).replace(" ", "")
    for suf in ("token", "coin", "inu"):
        if s.endswith(suf) and len(s) > len(suf) + 2:
            s = s[: -len(suf)]
            break
    return s


def cles_nom(nom):
    cles = {nom_souple(nom)}
    for inner in re.findall(r"\(([^)]*)\)", nom or ""):
        inner = re.sub(r"^(ex-|ex |aka )", "", inner.strip(), flags=re.I)
        # une année, une chaîne ou un ticker entre parenthèses ne sont pas un autre nom
        if not inner or re.fullmatch(r"\d{4}|old|new|v\d", inner.lower()) or est_chaine(inner) \
                or inner.isupper():
            continue
        cles.add(nom_souple(inner))
    return {c for c in cles if c}


def norm_ticker(t):
    s = sans_accents(t or "").upper().replace("$", "").replace("†", "")
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\s+", "", s)
    return "" if s in ("AVERIFIER", "INCONNU", "?") else s


def nettoie_ticker(t):
    """Ticker affiché : sans « $ » en tête ni mention « (à vérifier) »."""
    t = (t or "").strip()
    t = re.sub(r"\s*\(à vérifier\)\s*$", "", t, flags=re.I)
    t = re.sub(r"^\$(?=\S)", "", t)
    return t.strip()


def cles_ticker(t):
    out = {norm_ticker(t)}
    for inner in re.findall(r"\(([^)]*)\)", t or ""):
        out.add(norm_ticker(re.sub(r"^ex-", "", inner.strip(), flags=re.I)))
    return {x for x in out if x}


ALIAS_CHAINE = [
    (r"blockchain propre|\(propre\)", "blockchain propre"),
    (r"\bbsc\b|bnb|binance smart", "BNB Chain"),
    (r"ethereum|\beth\b|erc-?20", "Ethereum"),
    (r"solana|\bsol\b", "Solana"),
    (r"\bbase\b", "Base"),
    (r"\btron\b", "Tron"),
    (r"\bton\b", "TON"),
    (r"arbitrum", "Arbitrum"),
    (r"avalanche|avax", "Avalanche"),
    (r"polygon", "Polygon"),
    (r"\bsui\b", "Sui"),
    (r"hyperliquid|hyperevm", "Hyperliquid"),
    (r"\bnear\b", "NEAR"),
    (r"cardano", "Cardano"),
    (r"counterparty", "Counterparty (Bitcoin)"),
    (r"bitcoin|ordinals|runes|brc-?20", "Bitcoin"),
    (r"blast", "Blast"),
    (r"aptos", "Aptos"),
]


def est_chaine(t):
    t = sans_accents((t or "").lower())
    return "propre" in t or any(re.search(m, t) for m, _ in ALIAS_CHAINE)


def norm_chaine(c):
    """Chaîne canonique pour comparer et compter ; '' si inconnue."""
    t = sans_accents((c or "").lower())
    t = re.sub(r"\(a (verifier|confirmer)\)", "", t).strip()
    if not t or t.startswith("a verifier") or t.startswith("inconnu") or t == "?":
        return ""
    # première chaîne citée
    t1 = re.split(r",|;| et |/", t)[0]
    # « Dogecoin (blockchain propre) » -> blockchain propre
    if "blockchain propre" in t or "propre" in t1 or re.search(r"\bfork\b", t1):
        return "blockchain propre"
    for motif, nom in ALIAS_CHAINE:
        if re.search(motif, t1):
            return nom
    t1 = re.sub(r"\(.*?\)", "", t1).strip()
    return t1.title() or ""


def chaines_compatibles(a, b):
    na, nb = norm_chaine(a), norm_chaine(b)
    return not na or not nb or na == nb


def slug(s):
    s = sans_accents(s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if not s:  # noms CJK ou emoji
        s = "x" + "".join("%x" % ord(c) for c in (s or "")[:4])
    return s


def slug_unicode(s):
    base = slug(s)
    if base.startswith("x") and not re.sub(r"[^a-z0-9]", "", sans_accents(s or "").lower()):
        base = "u" + "-".join("%x" % ord(c) for c in (s or "").strip()[:6])
    return base


def annee(txt):
    m = re.search(r"\b(20[12]\d)\b", txt or "")
    return int(m.group(1)) if m else None


def epoque(txt):
    a = annee(txt)
    if a is None:
        return "inconnue"
    if a <= 2018:
        return "2013-2018"
    if a <= 2022:
        return "2019-2022"
    return "2023-2026"


def mort(etat):
    return sans_accents((etat or "").lower()).startswith("mort")


def ids_coingecko(texte):
    out = re.findall(r"coingecko\.com/(?:[a-z]{2}/)?coins/([a-z0-9][a-z0-9-]*)", texte or "")
    return list(OrderedDict.fromkeys(out))


def split_segments(texte):
    """Découpe sur ' ; ' et ' / ' hors parenthèses et hors `code`."""
    segs, cur, prof, code = [], [], 0, False
    i = 0
    while i < len(texte):
        c = texte[i]
        if c == "`":
            code = not code
        elif not code and c == "(":
            prof += 1
        elif not code and c == ")":
            prof = max(0, prof - 1)
        if not code and prof == 0 and texte[i:i + 3] in (" ; ", " / "):
            segs.append("".join(cur).strip())
            cur = []
            i += 3
            continue
        cur.append(c)
        i += 1
    segs.append("".join(cur).strip())
    return [s for s in segs if s]


# ----------------------------------------------------------------- tableaux md

def lignes_tableau(lignes):
    """Rend [(entête, [lignes])] pour chaque tableau markdown d'une liste de lignes."""
    tables, i = [], 0
    while i < len(lignes):
        l = lignes[i]
        if l.startswith("|") and i + 1 < len(lignes) and re.match(r"^\|\s*-{3}", lignes[i + 1]):
            entete = cellules(l)
            rows = []
            i += 2
            while i < len(lignes) and lignes[i].startswith("|"):
                rows.append(cellules(lignes[i]))
                i += 1
            tables.append((entete, rows))
        else:
            i += 1
    return tables


def cellules(ligne):
    l = ligne.strip()
    if l.startswith("|"):
        l = l[1:]
    if l.endswith("|"):
        l = l[:-1]
    return [c.strip() for c in l.split("|")]


def sections(texte):
    """{titre de section ## ou ###: lignes}"""
    out, titre, buf = OrderedDict(), "", []
    for l in texte.splitlines():
        m = re.match(r"^(#{2,3})\s+(.*)", l)
        if m:
            out.setdefault(titre, []).extend(buf)
            titre, buf = m.group(2).strip(), []
        else:
            buf.append(l)
    out.setdefault(titre, []).extend(buf)
    return out


def lire(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------------- modèle

class Carte:
    """Une carte en cours de fusion."""

    def __init__(self, **kw):
        self.nom = kw.get("nom", "")
        self.ticker = nettoie_ticker(kw.get("ticker", ""))
        self.chaine = kw.get("chaine", "")
        self.lancement = kw.get("lancement", "")
        self.histoire = kw.get("histoire", "")
        self.etat = kw.get("etat", "")
        self.etat_rang = kw.get("etat_rang", -1)
        self.drapeaux = list(kw.get("drapeaux", []))
        self.drapeau_auto = False
        self.sources = list(kw.get("sources", []))
        self.origines = list(kw.get("origines", []))
        self.adresse = kw.get("adresse", "")
        self.cg_ids = list(kw.get("cg_ids", []))
        self.pics = []  # (valeur, texte, nature, rang_source, borne)
        self.proposee = kw.get("proposee", "")
        self.proposee_rang = -1
        self.legende_histoire = False
        self.a_decider = kw.get("a_decider", False)
        self.motif = kw.get("motif", "")
        self.v1 = kw.get("v1", "")
        self.mythique = False
        self.retiree = False
        self.notes = []

    # --- mises à jour avec priorité de récence
    def ajoute_pic(self, texte, nature, rang):
        texte = (texte or "").strip()
        if not texte:
            return
        v = parse_montant(texte)
        nat = norm_nature(nature) if v is not None else "inconnu"
        self.pics.append((v, texte, nat, rang, est_borne_basse(texte)))

    def set_champ(self, champ, valeur, rang):
        if not valeur:
            return
        attr_rang = "_rang_" + champ
        if rang >= getattr(self, attr_rang, -1):
            setattr(self, champ, valeur)
            setattr(self, attr_rang, rang)

    def set_etat(self, etat, rang):
        if etat and rang >= self.etat_rang:
            self.etat, self.etat_rang = etat, rang

    def set_proposee(self, r, rang, histoire=False):
        r = norm_rarete(r)
        if r and rang >= self.proposee_rang:
            self.proposee, self.proposee_rang = r, rang
        if histoire:
            self.legende_histoire = True

    def ajoute_drapeau(self, d):
        for x in re.split(r"\s*[,;]\s*", d or ""):
            x = x.strip()
            if x and x not in self.drapeaux:
                self.drapeaux.append(x)

    # --- pic retenu
    def pic_retenu(self):
        """(valeur, texte, nature, plus haut pic sourcé)."""
        avec = [p for p in self.pics if p[0] is not None]
        if not avec:
            txt = self.pics[-1][1] if self.pics else "inconnu"
            return None, txt, "inconnu", None
        sources = [p for p in avec if p[2] == "sourcé"]
        max_source = max((p[0] for p in sources), default=None)
        # meilleure nature, puis la plus récente
        best = max(avec, key=lambda p: (RANG_NATURE[p[2]], p[3]))
        if best[2] == "sourcé" and best[4]:
            # borne basse sourcée dépassée par une estimation plus haute et plus récente ou égale
            # seulement une estimation au moins aussi récente que la borne (r4 Hosky : borne
            # sourcée qui écarte l'estimation CoinGecko de R5 jugée gonflée)
            plus_haut = [p for p in avec if p[2] != "sourcé" and p[0] > best[0] and p[3] >= best[3]]
            if plus_haut:
                e = max(plus_haut, key=lambda p: (p[3], p[0]))
                txt = e[1] if "borne sourcée" in e[1] else "%s (au-dessus de la borne sourcée %s)" % (e[1], best[1])
                return e[0], txt, "estimé", max_source
        return best[0], best[1], best[2], max_source

    def cles(self):
        return cles_nom(self.nom), cles_ticker(self.ticker)


def rarete_v2(valeur, max_source, etat, legende_histoire=False, mythique=False):
    """Pyramide v2 décidée par le porteur."""
    if mythique:
        return "mythique"
    if (max_source is not None and max_source >= 1e9) or legende_histoire:
        return "légendaire"
    if valeur is None:
        return "commune"
    if valeur >= 1e8:
        return "épique"  # y compris un pic ≥ 1 Md$ seulement estimé
    if valeur >= 1e7 and not mort(etat):
        return "rare"
    return "commune"


def raison_rarete(c, v, ms, r):
    if r == "mythique":
        return "mythique réservé"
    if r == "légendaire":
        return "pic sourcé ≥ 1 Md$" if ms and ms >= 1e9 else "histoire légendaire signalée"
    if v is None:
        return "pic inconnu"
    if r == "épique":
        return "pic ≥ 1 Md$ seulement estimé : plafonné à épique" if v >= 1e9 else "pic 100 M$ - 1 Md$"
    if r == "rare":
        return "pic 10 - 100 M$, pas mort"
    if v >= 1e7:
        return "mort au pic < 100 M$"
    return "pic < 10 M$"


# ----------------------------------------------------------------- lecture v1

def lire_v1(path):
    secs = sections(lire(path))
    cartes = OrderedDict()
    for titre, a_dec in (("Cartes", False), ("À décider (hors tableau et hors total)", True)):
        lignes = secs.get(titre)
        if lignes is None:
            lignes = next((v for k, v in secs.items() if k.startswith(titre.split(" (")[0])), [])
        for ent, rows in lignes_tableau(lignes):
            for r in rows:
                d = dict(zip(ent, r))
                num = d.get("N°", "").strip()
                if not num:
                    continue
                c = Carte(nom=d.get("Nom", ""), ticker=d.get("Ticker", ""), a_decider=a_dec, v1=num,
                          origines=["v1 n° %s" % num], motif=d.get("Motif", ""))
                c.set_champ("chaine", d.get("Chaîne", ""), 0)
                c.set_champ("lancement", d.get("Période de gloire", ""), 0)
                c.set_etat(d.get("État", ""), 0)
                c.ajoute_pic(d.get("Pic de capitalisation", ""), d.get("Nature du pic", ""), 0)
                c.set_proposee(d.get("Rareté", ""), 0)
                adr = d.get("Adresse", "")
                m = re.search(r"`([^`]+)`", adr)
                c.adresse = m.group(1) if m else ""
                if a_dec:
                    for drap, motif_re in (("arnaque avérée", r"arnaque avérée"),
                                           ("politique", r"politique|président"),
                                           ("obscène", r"obscène|sexuel|racist|insult|injurieux|nazie|"
                                                       r"grossier|extrême droite|chud")):
                        if re.search(motif_re, c.motif, re.I) or (drap == "arnaque avérée" and
                                                                  "arnaque avérée" in c.etat):
                            c.ajoute_drapeau(drap)
                cartes[num] = c
    return cartes


# ----------------------------------------------------------------- lecture R5

def lire_r5(path):
    texte = lire(path)
    secs = sections(texte)
    audit, c1, c2 = {}, [], []
    for titre, lignes in secs.items():
        for ent, rows in lignes_tableau(lignes):
            if "Verdict" in ent:
                for r in rows:
                    d = dict(zip(ent, r))
                    audit[d["N°"].strip()] = d
            elif ent and ent[0] == "CoinGecko id":
                cible = c1 if titre.startswith("C1") else c2
                for r in rows:
                    d = dict(zip(ent, r))
                    d["id"] = d["CoinGecko id"].strip("` ")
                    cible.append(d)
    return audit, c1, c2


def appliquer_r5(cartes, audit, rang=1):
    retraits = []
    for num, c in cartes.items():
        d = audit.get(num)
        if not d:
            c.notes.append("absent de l'audit R5")
            continue
        if d["Verdict"].strip() == "retirer":
            c.retiree = True
            retraits.append((num, c.nom, c.ticker, d.get("Motif si retrait", "")))
            continue
        c.set_etat(d.get("État v2", ""), rang)
        pic = d.get("Pic retenu", "")
        m = re.search(r"\(([^)]*)\)\s*$", pic)
        nat = m.group(1) if m else ("inconnu" if pic.startswith("inconnu") else "estimé")
        if not pic.startswith("inconnu"):
            c.ajoute_pic(pic, nat, rang)
        src = d.get("Source", "")
        hist = re.search(r"histoire : ([^;—]+)", src)
        if hist:
            c.set_champ("histoire", hist.group(1).strip(), rang)
        c.set_proposee(d.get("Rareté v2", ""), rang,
                       histoire=bool(hist) and norm_rarete(d.get("Rareté v2", "")) == "légendaire")
        m = re.search(r"CoinGecko `([^`]+)`", src)
        if m:
            c.cg_ids.append(m.group(1))
            c.sources.append("CG `%s`" % m.group(1))
    return retraits


# ----------------------------------------------------------------- lecture r1..r4

def lire_recherche(path, label):
    """Rend (nouveaux, corrections) d'un fichier de recherche au format consigne.

    Lecture par nombre de colonnes, pour accepter un lot sans en-tête : 12 cellules = nouveau
    jeton ; 5 ou 6 cellules commençant par un n° de carte = correction (6 = avec colonne Nom).
    """
    nouveaux, corrections = [], []
    for ligne in lire(path).splitlines():
        if not ligne.startswith("|") or re.match(r"^\|\s*:?-{3}", ligne):
            continue
        r = cellules(ligne)
        if len(r) == 12:
            if r[0] == "Nom" and r[1] == "Ticker":
                continue
            d = dict(zip(["nom", "ticker", "chaine", "lancement", "pic", "nature", "etat", "chute",
                          "histoire", "proposee", "drapeau", "source"], r))
            d["label"] = label
            nouveaux.append(d)
        elif len(r) in (5, 6) and re.match(r"^D?\d+", r[0]):
            if len(r) == 5:
                r = [r[0], ""] + r[1:]
            corrections.append({"num": r[0], "nom": r[1], "champ": r[2], "ancien": r[3],
                                "nouveau": r[4], "source": r[5], "label": label})
    return nouveaux, corrections


def numeros_correction(num):
    return re.findall(r"D?\d+", num or "")


CHAMPS = {"pic": "pic", "rareté": "rarete", "état": "etat", "chaîne": "chaine", "ticker": "ticker",
          "nom": "nom", "lancement": "lancement", "période de gloire": "lancement", "période": "lancement",
          "histoire": "histoire"}


def analyse_correction(champ, nouveau):
    """Extrait {champ: valeur} d'une correction en texte libre."""
    champs = [CHAMPS.get(x.strip().lower(), x.strip().lower())
              for x in re.split(r"\s*[;/]\s*", champ or "")]
    segs = split_segments(nouveau or "")
    out = {}
    douteux = bool(re.search(r"très douteux|pas appliqu|à vérifier avant", nouveau or "", re.I))
    # positionnel pour les champs texte
    for i, ch in enumerate(champs):
        if ch in ("chaine", "ticker", "nom", "lancement", "histoire") and i < len(segs):
            v = segs[i]
            if ch == "chaine":
                m = re.search(r"`([^`]+)`", v)
                if m:
                    out["adresse"] = m.group(1)
                v = re.sub(r"\s*`[^`]*`", "", v).strip()
            if ch == "lancement":
                v = re.sub(r"^(lancement|paire créée le)\s*", "", v, flags=re.I).strip()
            if ch == "ticker":
                # un segment qui contient un montant n'est pas un ticker (correction mal alignée)
                if parse_montant(v) is not None or len(v) > 24:
                    continue
                v = nettoie_ticker(v)
            out[ch] = v
    # sémantique pour pic, rareté, état
    if "pic" in champs and not douteux:
        for s in segs:
            if parse_montant(s) is not None:
                # « sourcé » écrit en toutes lettres l'emporte (r4 : « ≈ 17,5 M$, sourcé (FDV max …) »)
                nat = "sourcé" if re.search(r"\bsourcé", s) else (
                    "estimé" if re.search(r"estim|FDV|ATH|×", s) else "sourcé")
                out["pic"] = (re.sub(r"^confirmé\s*:\s*", "", s), nat)
                break
    elif "pic" in champs and douteux:
        out["pic_refuse"] = nouveau
    for s in segs:
        t = re.sub(r"^(reste|rareté v2|rareté|état\s*:)\s+", "", s.strip(), flags=re.I)
        t2 = sans_accents(t.lower())
        if "rarete" not in out and any(t2.startswith(sans_accents(r)) for r in RARETES):
            out["rarete"] = t
        if re.match(r"(mort|en declin|actif)\b", t2) and parse_montant(t.split("(")[0]) is None:
            out["etat"] = t
    if "rarete" in out:
        r = norm_rarete(out["rarete"])
        pic_estime_md = ("pic" in out and out["pic"][1] == "estimé" and
                         (parse_montant(out["pic"][0]) or 0) >= 1e9)
        out["legende_histoire"] = (r == "légendaire" and not pic_estime_md and
                                   not re.search(r"selon la règle|≥ 1 Md", out["rarete"]))
    return out


def appliquer_correction(c, corr, rang):
    a = analyse_correction(corr["champ"], corr["nouveau"])
    for ch in ("chaine", "ticker", "nom", "lancement", "histoire"):
        if ch in a:
            c.set_champ(ch, a[ch], rang)
    if "adresse" in a:
        c.adresse = a["adresse"]
    if "pic" in a:
        c.ajoute_pic(a["pic"][0], a["pic"][1], rang)
    if "etat" in a:
        c.set_etat(a["etat"], rang)
    if "rarete" in a:
        c.set_proposee(a["rarete"], rang, histoire=a.get("legende_histoire", False))
    for u in re.findall(r"https?://\S+", corr["source"]):
        if u not in c.sources:
            c.sources.append(u.rstrip(";,"))
    c.cg_ids.extend(ids_coingecko(corr["source"]))
    c.origines.append("correction %s" % corr["label"])
    return a


def carte_depuis_ligne(d, rang):
    c = Carte(nom=d["nom"], ticker=d["ticker"], origines=[d["label"]])
    c.set_champ("chaine", d["chaine"], rang)
    c.set_champ("lancement", d["lancement"], rang)
    c.set_champ("histoire", d["histoire"], rang)
    c.set_etat(d["etat"], rang)
    c.ajoute_pic(d["pic"], d["nature"], rang)
    v = parse_montant(d["pic"])
    nat = norm_nature(d["nature"])
    prop = norm_rarete(d["proposee"])
    c.set_proposee(d["proposee"], rang,
                   histoire=prop == "légendaire" and not (nat == "estimé" and v is not None and v >= 1e9))
    c.ajoute_drapeau(d["drapeau"])
    c.sources = [u.rstrip(";,") for u in re.findall(r"https?://\S+", d["source"])] or \
                ([d["source"]] if d["source"] else [])
    c.cg_ids = ids_coingecko(d["source"])
    return c


# ----------------------------------------------------------------- CoinGecko

def lire_cg(path):
    cg = {}
    if not os.path.exists(path):
        return cg
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cg[r["id"]] = r
    return cg


def etat_cg(r):
    """Règle R5 : mort si cap < 1 M$ et volume < 20 k$."""
    try:
        cap = float(r.get("market_cap") or 0)
        vol = float(r.get("total_volume") or 0)
        ecart = float(r.get("ath_change_percentage") or 0)
    except ValueError:
        return ""
    if cap < 1e6 and vol < 2e4:
        return "mort (CoinGecko 11/11)"
    if ecart <= -95:
        return "en déclin (-95 % ou pire, CoinGecko 11/11)"
    if ecart <= -80:
        return "en déclin (CoinGecko 11/11)"
    return "actif (CoinGecko 11/11)"


# ----------------------------------------------------------------- dédoublonnage

def meme_jeton(a, b):
    """Raison de fusion entre deux cartes, ou '' si distinctes."""
    if set(a.cg_ids) & set(b.cg_ids):
        return "même id CoinGecko"
    if a.cg_ids and b.cg_ids:
        return ""  # deux fiches CoinGecko distinctes : deux jetons
    ya, yb = annee(a.lancement), annee(b.lancement)
    if ya and yb and abs(ya - yb) >= 3:
        return ""  # homonymes d'époques différentes (Catcoin 2013 / 2024)
    na, ta = a.cles()
    nb, tb = b.cles()
    if na & nb and ta & tb and chaines_compatibles(a.chaine, b.chaine):
        return "même nom et ticker normalisés, chaîne compatible"
    return ""


def homonyme(a, b):
    na, ta = a.cles()
    nb, tb = b.cles()
    return bool(na & nb) and not (ta & tb)


def absorber(garde, autre, raison, journal):
    for p in autre.pics:
        garde.pics.append(p)
    for ch in ("chaine", "lancement", "histoire", "nom", "ticker"):
        v = getattr(autre, ch)
        r = getattr(autre, "_rang_" + ch, -1)
        if v and (not getattr(garde, ch) or r > getattr(garde, "_rang_" + ch, -1)) and ch not in ("nom", "ticker"):
            garde.set_champ(ch, v, r)
    if autre.etat:
        garde.set_etat(autre.etat, autre.etat_rang)
    if autre.proposee:
        garde.set_proposee(autre.proposee, autre.proposee_rang)
    garde.legende_histoire |= autre.legende_histoire
    for d in autre.drapeaux:
        garde.ajoute_drapeau(d)
    garde.sources += [s for s in autre.sources if s not in garde.sources]
    garde.cg_ids += [i for i in autre.cg_ids if i not in garde.cg_ids]
    garde.origines += [o for o in autre.origines if o not in garde.origines]
    garde.adresse = garde.adresse or autre.adresse
    if autre.a_decider and not garde.a_decider:
        garde.motif = garde.motif or autre.motif
    journal.append((garde, autre.nom, autre.ticker, ", ".join(autre.origines), raison))


# ----------------------------------------------------------------- fusion

def construire(root, extras=(), r4=True, mythiques=None):
    """`mythiques` : {n° v1 : ticker} (charger_mythiques_v1) ; la carte v1 doit porter ce ticker."""
    d = lambda *p: os.path.join(root, *p)
    journal_fusions, journal_ignores, homonymes, corr_refusees = [], [], [], []

    cartes = lire_v1(d("docs", "catalogue-final.md"))
    audit, c1, c2 = lire_r5(d("docs", "recherche-v2", "r5-audit-catalogue.md"))
    retraits = appliquer_r5(cartes, audit)
    cg = lire_cg(d("docs", "data", "coingecko-meme-2026-11-11.csv"))

    # fusions forcées R5
    for garde, abs_, raison in FUSIONS_FORCEES:
        if garde in cartes and abs_ in cartes and not cartes[abs_].retiree:
            absorber(cartes[garde], cartes[abs_], raison, journal_fusions)
            cartes[abs_].retiree = True
            cartes[abs_].notes.append("fusionnée")

    for num, tk in (mythiques or {}).items():
        if num not in cartes or norm_ticker(cartes[num].ticker) != norm_ticker(tk):
            raise SystemExit("mythique annoncée en v1 n° %s introuvable dans catalogue-final.md" % num)
        cartes[num].mythique = True

    # fichiers de recherche dans l'ordre de récence
    fichiers = []
    for i, nom in enumerate(["r1-2013-2018.md", "r2-2019-2022.md", "r3-2023-2026.md"]):
        fichiers.append((d("docs", "recherche-v2", nom), nom[:2], 2 + i))
    p4 = d("docs", "recherche-v2", "r4-autres-chaines.md")
    if r4 and os.path.exists(p4):
        fichiers.append((p4, "r4", 5))
    for j, e in enumerate(extras):
        fichiers.append((os.path.abspath(e), "extra:" + os.path.basename(e), 6 + j))
    lus = []

    actives = [c for c in cartes.values() if not c.retiree]
    retirees = {num: c for num, c in cartes.items() if c.retiree}

    for path, label, rang in fichiers:
        if not os.path.exists(path):
            continue
        nouveaux, corrections = lire_recherche(path, label)
        lus.append((os.path.relpath(path, root) if path.startswith(root) else path, len(nouveaux),
                    len(corrections)))
        # corrections
        for corr in corrections:
            nums = numeros_correction(corr["num"])
            for n in nums:
                c = cartes.get(n)
                if c is None:
                    corr_refusees.append((corr, "carte %s inconnue" % n))
                    continue
                if c.retiree:
                    fus = next((g for g, a_, _ in FUSIONS_FORCEES if a_ == n), None)
                    corr_refusees.append((corr, "carte %s fusionnée dans %s (R5) : correction non reportée, "
                                                "à revoir" % (n, fus) if fus else
                                          "carte %s retirée par R5 (non-mème)" % n))
                    continue
                a = appliquer_correction(c, corr, rang)
                if "pic_refuse" in a:
                    corr_refusees.append((corr, "pic jugé très douteux par la source, non appliqué"))
        # nouveaux jetons
        for ligne in nouveaux:
            c = carte_depuis_ligne(ligne, rang)
            # état à vérifier -> CoinGecko si rapproché
            if sans_accents(c.etat.lower()).startswith("a verifier"):
                for i in c.cg_ids:
                    if i in cg:
                        c.set_etat(etat_cg(cg[i]), rang)
                        break
            # doutes explicites
            motif = ""
            if RE_DOUTE.search(ligne["histoire"]) or RE_DOUTE.search(ligne["drapeau"]):
                motif = "doute du chercheur (%s) : « %s »" % (label, RE_DOUTE.search(
                    ligne["histoire"] + " " + ligne["drapeau"]).group(0))
            for pref, tk, m, pic_douteux in DOUTES_EXPLICITES:
                if label.startswith(pref) and norm_ticker(c.ticker) == tk:
                    motif = m
                    if pic_douteux:
                        c.pics = [(v, t + " (pic CMC douteux)", "estimé", r, b) for v, t, _, r, b in c.pics]
            if label == "r1" and RE_CANNABIS.search(ligne["nom"] + " " + ligne["histoire"]):
                motif = "coin cannabis : r1 les garde « par cohérence avec PotCoin » mais les dit « à trancher »"
            if motif:
                c.a_decider, c.motif = True, motif
            # doublon ?
            cible = None
            for e in list(actives) + list(retirees.values()):
                r = meme_jeton(e, c)
                if r:
                    cible = (e, r)
                    break
            if cible:
                e, r = cible
                if e.retiree:
                    journal_ignores.append((c, "doublon d'une carte v1 retirée ou fusionnée (%s)" %
                                            ", ".join(e.origines[:1])))
                    continue
                absorber(e, c, r, journal_fusions)
                continue
            for e in actives:
                if homonyme(e, c) and chaines_compatibles(e.chaine, c.chaine):
                    homonymes.append((c, e))
                    break
            actives.append(c)

    # candidats C1 / C2
    tous_cg = set(i for c in actives for i in c.cg_ids) | set(
        i for c in retirees.values() for i in c.cg_ids)
    reserve = []
    for row in c1:
        cid = row["id"]
        rem = row.get("Remarque", "")
        c = Carte(nom=row["Nom"], ticker=row["Ticker"], origines=["R5 C1 `%s`" % cid], cg_ids=[cid],
                  sources=["https://www.coingecko.com/en/coins/%s" % cid])
        c.set_champ("chaine", "à vérifier", 1)
        c.set_champ("lancement", "à vérifier (sommet le %s)" % row.get("Date du plus haut", ""), 1)
        c.ajoute_pic("%s, %s (CoinGecko, ATH × offre actuelle)" % (row["Pic estimé"],
                                                                   row.get("Date du plus haut", "")),
                     "estimé", 1)
        c.set_proposee(row.get("Rareté v2 indicative", ""), 1)
        c.set_etat("mort" if "mort" in rem else (etat_cg(cg[cid]) if cid in cg else ""), 1)
        if cid in tous_cg:
            journal_ignores.append((c, "C1 déjà présent (même id CoinGecko)"))
            continue
        if "copie ou ancienne version" in rem:
            journal_ignores.append((c, "C1 : « %s » selon R5" % rem.split(";")[0]))
            continue
        doublon = next((e for e in actives if meme_jeton(e, c)), None)
        if doublon:
            journal_ignores.append((c, "C1 déjà venu par %s" % ", ".join(doublon.origines[:2])))
            continue
        if "nature à vérifier" in rem:
            c.a_decider, c.motif = True, "R5 C1 : nature à vérifier"
        elif cid in C1_NATURE_DOUTEUSE:
            c.a_decider, c.motif = True, "consolidation : " + C1_NATURE_DOUTEUSE[cid]
        actives.append(c)
        tous_cg.add(cid)
    for row in c2:
        cid = row["id"]
        c = Carte(nom=row["Nom"], ticker=row["Ticker"], cg_ids=[cid])
        if cid in tous_cg or any(meme_jeton(e, c) for e in actives):
            continue
        reserve.append(row)

    # drapeaux automatiques (sources sans colonne Drapeau : v1 et C1)
    for c in actives:
        if any(o.startswith("v1") or o.startswith("R5 C1") for o in c.origines[:1]) and not c.drapeaux:
            nom = sans_accents((c.nom + " " + c.motif).lower())
            for drap, motif in DRAPEAU_MOTS.items():
                if re.search(r"\b(?:%s)" % motif, nom):
                    c.ajoute_drapeau(drap)
                    c.drapeau_auto = True

    return {
        "actives": actives, "retraits": retraits, "fusions": journal_fusions,
        "ignores": journal_ignores, "homonymes": homonymes, "corr_refusees": corr_refusees,
        "reserve": reserve, "lus": lus, "cg": cg,
        "surclassements": lire_surclassements(d("docs", "recherche-v2", "surclassements.md")),
    }


# ----------------------------------------------------------------- sortie

def lire_surclassements(path):
    """Tableau | Nom | Ticker | Rareté forcée | Raison | Source |. Un nom suivi d'une chaîne entre
    parenthèses (« Neiro (Ethereum) ») ne vise que la carte de cette chaîne."""
    out = []
    if not os.path.exists(path):
        return out
    for ent, rows in lignes_tableau(lire(path).splitlines()):
        if "Rareté forcée" not in ent:
            continue
        for r in rows:
            d = dict(zip(ent, r))
            nom = d.get("Nom", "")
            chaine = ""
            m = re.search(r"\(([^)]*)\)\s*$", nom)
            if m and est_chaine(m.group(1)):
                chaine, nom = norm_chaine(m.group(1)), nom[:m.start()].strip()
            rar = norm_rarete(d.get("Rareté forcée", ""))
            if nom and rar:
                out.append({"nom": nom, "ticker": d.get("Ticker", ""), "chaine": chaine, "rarete": rar,
                            "raison": d.get("Raison", ""), "source": d.get("Source", ""), "cartes": []})
    return out


def vise(s, c):
    if c.mythique or not (cles_nom(s["nom"]) & cles_nom(c.nom)):
        return False
    if s["ticker"] and not (cles_ticker(s["ticker"]) & cles_ticker(c.ticker)):
        return False
    return not s["chaine"] or norm_chaine(c.chaine) == s["chaine"]


def est_aberrant(v, nat):
    """Pic seulement estimé et ≥ 1 Md$ : estimation jugée aberrante pour la rareté."""
    return nat == "estimé" and v is not None and v >= 1e9


def rarete_carte(v, nat, ms, etat, legende=False, mythique=False, regle_aberrant=True):
    """Rareté v2 avec la règle des estimations aberrantes.

    Rend (rareté, règle) : règle = 'aberrant' (estimé ≥ 1 Md$ sans plancher sourcé, compté comme pic
    inconnu), 'plancher' (estimé ≥ 1 Md$ au-dessus d'une borne sourcée : rareté de la borne) ou ''.
    """
    if regle_aberrant and not mythique and est_aberrant(v, nat):
        return rarete_v2(ms, ms, etat, legende, mythique), ("plancher" if ms else "aberrant")
    return rarete_v2(v, ms, etat, legende, mythique), ""


def epiques_retombes(cartes):
    return sum(1 for c in cartes if c.regle_estim and c.rarete_avant_aberrant == "épique" and c.rarete != "épique")


def finaliser(actives, surclassements=()):
    """Calcule pic, rareté, tri, numéros et ids. Rend (catalogue, a_decider)."""
    for c in actives:
        v, txt, nat, ms = c.pic_retenu()
        c.pic_v, c.pic_txt, c.pic_nat, c.pic_ms = v, txt, nat, ms
        leg = c.legende_histoire and not c.mythique
        c.rarete_avant_aberrant = rarete_v2(v, ms, c.etat, leg, c.mythique)
        c.rarete, c.regle_estim = rarete_carte(v, nat, ms, c.etat, leg, c.mythique)
        c.raison = raison_rarete(c, v, ms, c.rarete)
        c.surclasse = None
        # surclassements manuels, appliqués en dernier
        for sc in surclassements:
            if vise(sc, c):
                c.surclasse = sc
                sc["cartes"].append(c)
                c.rarete_avant_surclassement = c.rarete
                c.rarete, c.regle_estim = sc["rarete"], ""
                c.raison = "surclassement manuel : " + sc["raison"]
                if sc["source"] and sc["source"] not in c.sources:
                    c.sources.append(sc["source"])
                break
        c.aberrant = c.regle_estim == "aberrant"
        if c.aberrant:
            c.raison = "estimation aberrante (pic estimé ≥ 1 Md$, aucune source) : traité comme pic inconnu"
            c.pic_txt = c.pic_txt + " — estimation aberrante, à vérifier"
        elif c.regle_estim == "plancher":
            c.raison = "pic estimé ≥ 1 Md$ non confirmé : rareté de la borne sourcée (%.0f M$)" % (ms / 1e6)
        c.epoque = epoque(c.lancement)

    def cle_tri(c):
        return (RARETES.index(c.rarete), -(c.pic_v or -1), norm_nom(c.nom), norm_ticker(c.ticker))

    cat = sorted([c for c in actives if not c.a_decider], key=cle_tri)
    dec = sorted([c for c in actives if c.a_decider], key=cle_tri)
    m, n = 0, 0
    for c in cat:
        if c.rarete == "mythique":
            m += 1
            c.numero = "M%d" % m
        else:
            n += 1
            c.numero = str(n)
    for i, c in enumerate(dec, 1):
        c.numero = "AD%d" % i
    # ids stables : slug nom-ticker, puis chaîne, puis origine
    vus = Counter()
    for c in sorted(actives, key=lambda c: ((c.origines or [""])[0], norm_nom(c.nom))):
        if c.mythique:
            c.id = "mythique-" + c.numero.lower()
            continue
        base = "-".join(x for x in (slug_unicode(c.nom), slug_unicode(c.ticker)) if x)
        cid = base
        if vus[cid]:
            cid = base + "-" + (slug(norm_chaine(c.chaine)) or "x")
        while vus[cid]:
            cid = "%s-%d" % (base, vus[base] + 1)
            vus[base] += 1
        vus[cid] += 1
        c.id = cid
    return cat, dec


def drapeau_txt(c):
    return ", ".join(c.drapeaux)


def objet_json(c):
    o = OrderedDict([
        ("id", c.id), ("numero", c.numero),
        ("section", "à décider" if c.a_decider else "catalogue"),
        ("nom", c.nom), ("ticker", c.ticker), ("chaine", c.chaine),
        ("chaine_normalisee", norm_chaine(c.chaine) or "à vérifier"),
        ("lancement", c.lancement), ("epoque", c.epoque),
        ("pic", c.pic_txt), ("pic_usd", c.pic_v), ("nature_pic", c.pic_nat),
        ("etat", c.etat or "à vérifier"), ("histoire", c.histoire),
        ("rarete", c.rarete), ("rarete_proposee", "mythique" if c.mythique else c.proposee),
        ("raison_rarete", c.raison), ("pic_aberrant", c.aberrant),
        ("surclassement", c.surclasse["rarete"] if c.surclasse else ""),
        ("drapeau", drapeau_txt(c)), ("drapeau_auto", c.drapeau_auto),
        ("burn", BURN), ("source", " ; ".join(c.sources[:4])),
        ("origines", c.origines), ("coingecko_id", c.cg_ids[0] if c.cg_ids else ""),
        ("adresse", c.adresse),
    ])
    if c.a_decider:
        o["motif"] = c.motif
    if c.mythique:
        # Scellée : aucun champ public ne révèle le jeton ; les vrais noms vont dans secret_json().
        for k in ("nom", "ticker", "chaine", "chaine_normalisee", "lancement", "epoque", "pic", "nature_pic",
                  "etat", "histoire", "source", "coingecko_id", "adresse"):
            o[k] = "?"
        o["pic_usd"] = None
        o["origines"] = []
        o["visuel"] = "?"
    return o


CHAMPS_SECRET = ("id", "numero", "nom", "ticker", "chaine", "chaine_normalisee", "lancement", "epoque", "pic",
                 "pic_usd", "nature_pic", "etat", "histoire", "source", "origines", "coingecko_id", "adresse")


def secret_json(c):
    """Vraie identité d'une mythique : uniquement pour docs/data/secrets/ (hors git)."""
    o = OrderedDict([
        ("id", c.id), ("numero", c.numero), ("nom", c.nom), ("ticker", c.ticker), ("chaine", c.chaine),
        ("chaine_normalisee", norm_chaine(c.chaine) or "à vérifier"), ("lancement", c.lancement),
        ("epoque", c.epoque), ("pic", c.pic_txt), ("pic_usd", c.pic_v), ("nature_pic", c.pic_nat),
        ("etat", c.etat or "à vérifier"), ("histoire", c.histoire), ("source", " ; ".join(c.sources[:4])),
        ("origines", c.origines), ("coingecko_id", c.cg_ids[0] if c.cg_ids else ""), ("adresse", c.adresse),
    ])
    return OrderedDict((k, o[k]) for k in CHAMPS_SECRET)


def ecrire_secrets(path, cartes):
    """Écrit les vrais noms des mythiques en mode 600 (dossier ignoré par git)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    donnees = OrderedDict([
        ("avertissement", "Vrais noms des mythiques scellées : ne jamais committer ni publier."),
        ("date", DATE),
        ("mythiques", [secret_json(c) for c in cartes if c.mythique]),
    ])
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.chmod(path, 0o600)


def cell(s):
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def ligne_md(c):
    if c.mythique:
        return "| %s | ? | ? | ? | ? | ? | ? | ? | ? | mythique | mythique |  | %s | ? |" % (c.numero, BURN)
    src = " ; ".join(c.origines[:2] + c.sources[:2])
    return "| " + " | ".join(cell(x) for x in [
        c.numero, c.nom, c.ticker, c.chaine or "à vérifier", c.lancement or "à vérifier", c.pic_txt,
        c.pic_nat, c.etat or "à vérifier", c.histoire, c.rarete, c.proposee,
        drapeau_txt(c), BURN, src]) + " |"


def bucket_etat(e):
    t = sans_accents((e or "").lower())
    if t.startswith("mort"):
        return "mort"
    if "arnaque" in t:
        return "arnaque avérée"
    if t.startswith("en declin") and ("-95" in t or "pire" in t):
        return "en déclin (-95 % ou pire)"
    if t.startswith("en declin"):
        return "en déclin"
    if t.startswith("actif"):
        return "actif"
    return "à vérifier"


def table_compte(titre, compteur, ordre=None):
    out = ["", "### " + titre, "", "| Valeur | Cartes |", "|---|---|"]
    cles = ordre or [k for k, _ in compteur.most_common()]
    for k in cles:
        if compteur.get(k):
            out.append("| %s | %d |" % (k, compteur[k]))
    out.append("| **Total** | **%d** |" % sum(compteur.values()))
    return out


def decomptes(cat):
    r = Counter(c.rarete for c in cat)
    ch = Counter("scellé (mythique)" if c.mythique else (norm_chaine(c.chaine) or "à vérifier") for c in cat)
    et = Counter("scellé (mythique)" if c.mythique else bucket_etat(c.etat) for c in cat)
    dr = Counter()
    for c in cat:
        if c.mythique:
            continue
        for d in (c.drapeaux or ["(aucun)"]):
            dr[d] += 1
    ep = Counter("scellé (mythique)" if c.mythique else c.epoque for c in cat)
    return r, ch, et, dr, ep


def ecrire_md(path, cat, dec, res, args_lus):
    r, ch, et, dr, ep = decomptes(cat)
    L = []
    L.append("# Catalogue v2 des cartes Memaster")
    L.append("")
    L.append("**Date :** %s. Généré par `docs/recherche-v2/consolider.py` : ne pas éditer à la main, "
             "relancer le script. Ce document n'est pas un conseil en investissement." % DATE)
    L.append("")
    L.append("**Total : %d cartes** (dont 3 mythiques scellés), plus %d jetons « À décider » hors total."
             % (len(cat), len(dec)))
    L.append("")
    L.append("## Sources")
    L.append("")
    L.append("- `docs/catalogue-final.md` (v1) ; `docs/recherche-v2/r5-audit-catalogue.md` (audit, doublons, "
             "candidats C1/C2) ; `docs/data/coingecko-meme-2026-11-11.csv` (état des jetons rapprochés).")
    for p, n, k in args_lus:
        L.append("- `%s` : %d nouveaux jetons lus, %d corrections." % (p, n, k))
    if not any("r4" in p for p, _, _ in args_lus):
        L.append("- `r4-autres-chaines.md` : absent à la génération, ignoré.")
    L.append("")
    L.append("## Règles appliquées")
    L.append("")
    L.append("- **100 %% mèmes** : les %d retraits de l'audit R5 sont appliqués (annexe 6). "
             "Aucun retrait pour disponibilité ou liquidité." % len(res["retraits"]))
    L.append("- **Doublons** : nom et ticker normalisés (casse, accents, †, [OLD], parenthèses, suffixe "
             "inu/coin/token) et chaîne compatible, ou même id CoinGecko ; doublons cités par R5 fusionnés. "
             "Pic retenu : sourcé > estimé > inconnu, puis la source la plus récente (v1 < R5 < r1 < r2 < r3 < r4). "
             "Une borne basse sourcée (« ≥ ») est remplacée par une estimation plus haute. Annexe 1.")
    L.append("- **Rareté v2** : mythique = 3 jetons scellés ; légendaire = pic sourcé ≥ 1 Md$ ou histoire "
             "légendaire signalée ; épique = pic ≥ 100 M$ (un pic ≥ 1 Md$ seulement estimé reste épique) ; "
             "rare = 10 à 100 M$ et pas mort ; commune = le reste (morts au pic < 100 M$, petits, inconnus). "
             "« Mort » = état commençant par « mort ». Bas de fourchette retenu. Écarts : annexe 2.")
    L.append("- **Pics aberrants** : un pic seulement estimé et ≥ 1 Md$ compte comme inconnu pour la rareté, "
             "ou comme son plancher sourcé s'il en a un (annexe 5). **Surclassements manuels** appliqués en "
             "dernier (annexe 4).")
    L.append("- **Drapeaux** gardés en colonne, carte gardée. Pour v1 et les candidats C1 (sources sans "
             "colonne Drapeau), drapeau déduit du nom par mots-clés (%d cartes, `drapeau_auto` dans le JSON)."
             % sum(1 for c in cat + dec if c.drapeau_auto))
    L.append("- **Burn** : `à définir` partout (financement non décidé).")
    L.append("- **Candidats R5** : C1 ajoutés s'ils ne sont pas déjà venus par v1 ou r1-r4 ; C2 en réserve (annexe 3).")
    L.append("- Colonne Lancement : date de lancement des chercheurs ; pour v1, la « période de gloire » ; "
             "pour C1, la date du plus haut (époque approximative). Histoire vide quand aucune source n'en donne.")
    L.append("")
    L.append("## Cartes")
    L.append("")
    L.append("3 mythiques scellés : nom et visuel remplacés par « ? ».")
    L.append("")
    entete = ("| N° | Nom | Ticker | Chaîne | Lancement | Pic | Nature du pic | État | Histoire | Rareté | "
              "Rareté proposée | Drapeau | Burn | Source |")
    L.append(entete)
    L.append("|" + "---|" * 14)
    L.extend(ligne_md(c) for c in cat)
    L.append("")
    L.append("## À décider (hors total)")
    L.append("")
    L.append("Lignes « À décider » de v1 encore valides, jetons mis en doute par les chercheurs, candidats C1 "
             "de nature douteuse. Le porteur tranche. Une mention ici ne vaut pas accusation.")
    L.append("")
    L.append(entete[:-1] + " Motif |")
    L.append("|" + "---|" * 15)
    for c in dec:
        L.append(ligne_md(c) + " %s |" % cell(c.motif))
    L.append("")
    L.append("## Décompte (catalogue, hors « À décider »)")
    L.extend(table_compte("Par rareté", r, RARETES))
    L.extend(table_compte("Par chaîne (première chaîne citée)", ch))
    L.extend(table_compte("Par état", et))
    L.append("")
    L.append("### Par drapeau")
    L.append("")
    L.append("| Valeur | Cartes |")
    L.append("|---|---|")
    for k, v in dr.most_common():
        L.append("| %s | %d |" % (k, v))
    L.append("| (hors mythiques ; une carte peut avoir plusieurs drapeaux) | |")
    L.extend(table_compte("Par époque de lancement", ep, ["2013-2018", "2019-2022", "2023-2026", "inconnue",
                                                            "scellé (mythique)"]))
    L.extend(table_compte("« À décider » par rareté", Counter(c.rarete for c in dec), RARETES))
    # annexes
    L.append("")
    L.append("## Annexe 1 : fusions et doublons")
    L.append("")
    L.append("| Carte gardée | Absorbé | Ticker | Origine absorbée | Raison |")
    L.append("|---|---|---|---|---|")
    for g, nom, tk, orig, raison in res["fusions"]:
        if g.mythique:
            L.append("| M? | (scellé) | ? | %s | %s |" % (cell(orig), cell(raison)))
            continue
        L.append("| %s %s | %s | %s | %s | %s |" % (g.numero, cell(g.nom), cell(nom), cell(tk), cell(orig),
                                                  cell(raison)))
    L.append("")
    L.append("**Lignes non reprises** (doublons d'une carte déjà présente ou retirée) :")
    L.append("")
    L.append("| Nom | Ticker | Origine | Raison |")
    L.append("|---|---|---|---|")
    for c, raison in res["ignores"]:
        L.append("| %s | %s | %s | %s |" % (cell(c.nom), cell(c.ticker), cell(", ".join(c.origines)),
                                            cell(raison)))
    L.append("")
    L.append("**Homonymes gardés distincts** (même nom normalisé, ticker différent) :")
    L.append("")
    L.append("| Nouveau | Ticker | Carte existante | Ticker |")
    L.append("|---|---|---|---|")
    # Un homonyme d'une mythique trahirait son nom : ces lignes sont seulement comptées.
    for c, e in res["homonymes"]:
        if not e.mythique:
            L.append("| %s %s | %s | %s %s | %s |" % (c.numero, cell(c.nom), cell(c.ticker), e.numero, cell(e.nom),
                                                     cell(e.ticker)))
    n_myth = sum(1 for _, e in res["homonymes"] if e.mythique)
    if n_myth:
        L.append("")
        L.append("%d homonymes d'une mythique scellée, non listés pour ne pas révéler son nom." % n_myth)
    L.append("")
    L.append("**Corrections non appliquées** :")
    L.append("")
    L.append("| Source | N° | Champ | Raison |")
    L.append("|---|---|---|---|")
    for corr, raison in res["corr_refusees"]:
        L.append("| %s | %s | %s | %s |" % (corr["label"], cell(corr["num"]), cell(corr["champ"]), raison))
    L.append("")
    L.append("## Annexe 2 : écarts entre rareté v2 et rareté proposée")
    L.append("")
    ecarts = [c for c in cat + dec if not c.mythique and c.proposee and c.proposee != c.rarete]
    L.append("%d écarts. « Proposée » = rareté de la dernière source (chercheur, correction ou audit R5)." %
             len(ecarts))
    L.append("")
    L.append("| N° | Nom | Ticker | Pic retenu | Nature | État | Proposée | v2 | Raison |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for c in ecarts:
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            c.numero, cell(c.nom), cell(c.ticker), cell(c.pic_txt), c.pic_nat, cell(c.etat), c.proposee,
            c.rarete, c.raison))
    L.append("")
    L.append("## Annexe 3 : réserve (candidats R5 C2, estimation fragile)")
    L.append("")
    L.append("%d jetons non présents au catalogue, écart ≤ -99,5 %% : pics estimés peu fiables. "
             "À reprendre un par un si le porteur veut grossir la masse des communes." % len(res["reserve"]))
    L.append("")
    L.append("| CoinGecko id | Nom | Ticker | Pic estimé | Date du plus haut | Remarque |")
    L.append("|---|---|---|---|---|---|")
    for row in res["reserve"]:
        L.append("| `%s` | %s | %s | %s | %s | %s |" % (row["id"], cell(row["Nom"]), cell(row["Ticker"]),
                                                       cell(row["Pic estimé"]),
                                                       cell(row.get("Date du plus haut", "")),
                                                       cell(row.get("Remarque", ""))))
    L.append("")
    L.append("## Annexe 4 : surclassements manuels (`docs/recherche-v2/surclassements.md`)")
    L.append("")
    L.append("Appliqués en dernier, après la pyramide et la règle des pics aberrants.")
    L.append("")
    L.append("| Nom | Ticker | Chaîne visée | Rareté forcée | Cartes visées | Rareté sans surclassement | Raison | Source |")
    L.append("|---|---|---|---|---|---|---|---|")
    for sc in res["surclassements"]:
        cartes = ", ".join("%s %s" % (c.numero, cell(c.nom)) for c in sc["cartes"]) or "**aucune carte trouvée**"
        avant = ", ".join(c.rarete_avant_surclassement for c in sc["cartes"]) or "—"
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            cell(sc["nom"]), cell(sc["ticker"]), sc["chaine"] or "toutes", sc["rarete"], cartes, avant,
            cell(sc["raison"]), cell(sc["source"])))
    L.append("")
    L.append("## Annexe 5 : pics aberrants")
    L.append("")
    ab = [c for c in cat + dec if c.aberrant]
    pl = [c for c in cat + dec if c.regle_estim == "plancher"]
    L.append("%d cartes dont le pic n'est qu'estimé et atteint 1 Md$ ou plus, sans surclassement. Le chiffre est "
             "affiché avec la mention « estimation aberrante, à vérifier ». Pour la rareté, il compte comme un "
             "pic inconnu. %d épiques retombent au total (pics aberrants et planchers ci-dessous)." % (
                 len(ab), epiques_retombes(cat + dec)))
    L.append("")
    L.append("| N° | Nom | Ticker | Pic estimé | Plancher sourcé | État | Rareté sans la règle | Rareté v2 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in ab:
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            c.numero, cell(c.nom), cell(c.ticker), cell(c.pic_txt), "%.0f M$" % (c.pic_ms / 1e6) if c.pic_ms
            else "—", cell(c.etat), c.rarete_avant_aberrant, c.rarete))
    L.append("")
    L.append("**Estimations ≥ 1 Md$ au-dessus d'une borne sourcée** (%d cartes) : pas aberrantes, mais la "
             "rareté suit la borne sourcée, pas l'estimation." % len(pl))
    L.append("")
    L.append("| N° | Nom | Ticker | Pic estimé | Borne sourcée | Rareté sans la règle | Rareté v2 |")
    L.append("|---|---|---|---|---|---|---|")
    for c in pl:
        L.append("| %s | %s | %s | %s | %.0f M$ | %s | %s |" % (c.numero, cell(c.nom), cell(c.ticker),
                                                           cell(c.pic_txt), c.pic_ms / 1e6,
                                                           c.rarete_avant_aberrant, c.rarete))
    L.append("")
    L.append("## Annexe 6 : retraits de l'audit R5 (non-mèmes)")
    L.append("")
    L.append("| N° v1 | Nom | Ticker | Motif |")
    L.append("|---|---|---|---|")
    for num, nom, tk, motif in res["retraits"]:
        L.append("| %s | %s | %s | %s |" % (num, cell(nom), cell(tk), cell(motif)))
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


# ----------------------------------------------------------------- catalogue de démo (--demo)

DRAPEAUX_DEMO = ("politique", "personne réelle", "obscène", "arnaque avérée")
MOTIF_POLITICIEN = "politicien (nom ou histoire, sans drapeau)"
MOTIF_ARNAQUE_ETAT = "arnaque avérée (état)"
MOTIF_A_DECIDER = "à décider"
# Politicien désigné par le nom, le ticker ou l'histoire d'une carte sans drapeau « politique ».
# Les noms longs et sans ambiguïté sont cherchés aussi en milieu de mot (HarryPotterObamaSonic10Inu).
RE_POLITICIEN = re.compile(r"\b(?:%s|kennedy|hillary|clinton|macron|bukele)|"
                           r"trump|biden|obama|melania|kamala|desantis|pelosi|zelensk|rfk|川普"
                           % DRAPEAU_MOTS["politique"], re.I)
SEUIL_VOLUME, SEUIL_CAP = 2e4, 1e6
MIN_BRULABLES = 150
BASES = ("commune", "rare")
# Réintégration si la matière manque : du moins problématique au plus problématique, jamais d'arnaque.
PALIERS_REINTEGRATION = [
    {"personne réelle"},
    {"personne réelle", MOTIF_POLITICIEN},
    {"personne réelle", MOTIF_POLITICIEN, "politique"},
    {"personne réelle", MOTIF_POLITICIEN, "politique", "obscène"},
    {"personne réelle", MOTIF_POLITICIEN, "politique", "obscène", MOTIF_A_DECIDER},
]


def usd(v):
    if v < 1e3:
        return "%.0f $" % v
    if v >= 1e9:
        return ("%.2f Md$" % (v / 1e9)).replace(".", ",")
    if v >= 1e6:
        return ("%.1f M$" % (v / 1e6)).replace(".", ",")
    return "%.0f k$" % (v / 1e3)


def liquidite(c, cg):
    """(id, volume 24 h, capitalisation) du premier id CoinGecko de la carte présent dans le relevé."""
    for cid in c.cg_ids:
        r = cg.get(cid)
        if r:
            try:
                return cid, float(r.get("total_volume") or 0), float(r.get("market_cap") or 0)
            except ValueError:
                return cid, 0.0, 0.0
    return None


def brulable(c, cg):
    """(brûlable possible, raison) : jeton encore achetable (pas mort, liquidité CoinGecko du 11/11)."""
    if c.mythique:
        return False, "mythique scellée : jamais brûlable"
    if mort(c.etat):
        return False, "état « mort »"
    if bucket_etat(c.etat) == "arnaque avérée":
        return False, "état « arnaque avérée »"
    liq = liquidite(c, cg)
    if not liq:
        return False, "aucun jeton du relevé CoinGecko du 11/11 rapproché : liquidité non documentée"
    cid, vol, cap = liq
    mesure = "CoinGecko `%s` : volume 24 h %s, capitalisation %s" % (cid, usd(vol), usd(cap))
    if vol < SEUIL_VOLUME or cap < SEUIL_CAP:
        return False, "liquidité insuffisante (%s ; seuils 20 k$ et 1 M$)" % mesure
    return True, "achetable : état « %s », %s" % (bucket_etat(c.etat), mesure)


def motifs_exclusion(c):
    if c.mythique:
        return []
    m = [MOTIF_A_DECIDER] if c.a_decider else []
    m += [d for d in DRAPEAUX_DEMO if d in c.drapeaux]
    texte = sans_accents(" ".join((c.nom, c.ticker, c.histoire)).lower())
    if "politique" not in c.drapeaux and RE_POLITICIEN.search(texte):
        m.append(MOTIF_POLITICIEN)
    if "arnaque avérée" not in c.drapeaux and bucket_etat(c.etat) == "arnaque avérée":
        m.append(MOTIF_ARNAQUE_ETAT)
    return m


def construire_demo(cat, dec, cg, min_brulables=MIN_BRULABLES):
    """Catalogue de démo : sans drapeau, sans politicien, sans « À décider » ; réintégration si besoin."""
    rang = {id(c): i for i, c in enumerate(cat + dec)}
    for c in cat + dec:
        c.brulable, c.raison_brulable = brulable(c, cg)
        c.liquidite = None if c.mythique else liquidite(c, cg)
        c.motifs_exclusion = motifs_exclusion(c)
        c.reintegree = ""
    garde = [c for c in cat if not c.motifs_exclusion]
    exclus = [c for c in cat + dec if c.motifs_exclusion]

    def assez():
        return (sum(c.brulable for c in garde) >= min_brulables
                and any(c.brulable and c.rarete in BASES for c in garde))

    for palier in PALIERS_REINTEGRATION:
        if assez():
            break
        candidats = sorted((c for c in exclus if c.brulable and not c.reintegree
                            and set(c.motifs_exclusion) <= palier),
                           key=lambda c: (c.rarete not in BASES, rang[id(c)]))
        for c in candidats:
            if assez():
                break
            c.reintegree = ", ".join(c.motifs_exclusion)
            garde.append(c)
    garde.sort(key=lambda c: (RARETES.index(c.rarete), rang[id(c)]))
    exclus = [c for c in exclus if not c.reintegree]
    return {"cartes": garde, "exclus": exclus, "atteint": assez(), "min": min_brulables}


def objet_json_demo(c):
    o = objet_json(c)
    o["section_v2"] = o["section"]
    o["section"] = "catalogue"  # lisible tel quel par art/memaster_art/catalogue_v2.py
    o["brulable_possible"] = c.brulable
    o["raison_brulable"] = c.raison_brulable
    if c.liquidite:
        cid, vol, cap = c.liquidite
        o["liquidite"] = OrderedDict([("coingecko_id", cid), ("volume_24h_usd", vol), ("capitalisation_usd", cap),
                                      ("releve", "docs/data/coingecko-meme-2026-11-11.csv")])
    else:
        o["liquidite"] = None
    o["reintegree"] = c.reintegree
    return o


def ecrire_md_demo(path, demo):
    cartes, exclus = demo["cartes"], demo["exclus"]
    r = Counter(c.rarete for c in cartes)
    b = Counter(c.rarete for c in cartes if c.brulable)
    nb = sum(b.values())
    L = ["# Catalogue de démo des cartes Memaster", ""]
    L.append("**Date :** %s. Généré par `python3 docs/recherche-v2/consolider.py --demo` à partir du catalogue v2 : "
             "ne pas éditer à la main. Ce document n'est pas un conseil en investissement." % DATE)
    L.append("")
    L.append("**Total : %d cartes** (dont %d mythiques scellées), **%d brûlables possibles** (objectif ≥ %d, "
             "dont au moins une commune ou une rare : %s)." % (
                 len(cartes), r["mythique"], nb, demo["min"], "atteint" if demo["atteint"] else "**non atteint**"))
    L.append("")
    L.append("## Règles")
    L.append("")
    L.append("- Base : section « catalogue » de `docs/data/catalogue-v2.json`. Aucune « À décider ».")
    L.append("- Exclues : toute carte à drapeau `politique`, `personne réelle`, `obscène` ou `arnaque avérée` ; "
             "toute carte sans drapeau dont le nom, le ticker ou l'histoire désigne un politicien (mots-clés "
             "du drapeau `politique`, plus RFK, Kennedy, 川普, etc.) ; tout état « arnaque avérée ».")
    L.append("- **Brûlable possible** (`brulable_possible` dans le JSON, raison dans `raison_brulable`) : état autre "
             "que « mort », et jeton rapproché dans `docs/data/coingecko-meme-2026-11-11.csv` avec volume 24 h "
             "≥ 20 000 $ **et** capitalisation ≥ 1 M$ (valeurs dans `liquidite`). Mythiques : jamais brûlables. "
             "Une carte sans id CoinGecko rapproché n'est pas brûlable (liquidité non documentée).")
    L.append("- Si moins de %d brûlables, ou aucune commune ni rare brûlable, les exclues brûlables reviennent par "
             "paliers : `personne réelle`, puis politicien sans drapeau, `politique`, `obscène`, « À décider » ; "
             "jamais `arnaque avérée`." % demo["min"])
    L.append("- N° et `id` : ceux du catalogue v2 (numérotation à trous, ids stables pour les visuels).")
    L.append("")
    L.append("## Décompte")
    L.append("")
    L.append("| Rareté | Cartes | Brûlables possibles |")
    L.append("|---|---|---|")
    for k in RARETES:
        L.append("| %s | %d | %d |" % (k, r[k], b[k]))
    L.append("| **Total** | **%d** | **%d** |" % (len(cartes), nb))
    L.append("")
    rein = [c for c in cartes if c.reintegree]
    L.append("## Réintégrées (%d)" % len(rein))
    L.append("")
    if rein:
        L.append("| N° v2 | Nom | Ticker | Rareté | Motif d'exclusion levé |")
        L.append("|---|---|---|---|---|")
        for c in rein:
            L.append("| %s | %s | %s | %s | %s |" % (c.numero, cell(c.nom), cell(c.ticker), c.rarete,
                                                    cell(c.reintegree)))
    else:
        L.append("Aucune : l'objectif est atteint sans réintégrer de carte exclue.")
    L.append("")
    par_motif = Counter(m for c in exclus for m in c.motifs_exclusion)
    L.append("## Exclues (%d)" % len(exclus))
    L.append("")
    L.append("| Motif | Cartes |")
    L.append("|---|---|")
    for k, v in par_motif.most_common():
        L.append("| %s | %d |" % (k, v))
    L.append("| (une carte peut avoir plusieurs motifs) | |")
    L.append("")
    pol = [c for c in exclus if MOTIF_POLITICIEN in c.motifs_exclusion]
    L.append("### Politiciens sans drapeau (%d)" % len(pol))
    L.append("")
    L.append("| N° v2 | Nom | Ticker | Rareté | Brûlable si gardée |")
    L.append("|---|---|---|---|---|")
    for c in pol:
        L.append("| %s | %s | %s | %s | %s |" % (c.numero, cell(c.nom), cell(c.ticker), c.rarete,
                                                "oui" if c.brulable else "non"))
    L.append("")
    L.append("### Liste complète")
    L.append("")
    L.append("| N° v2 | Nom | Ticker | Rareté | Motifs | Brûlable si gardée |")
    L.append("|---|---|---|---|---|---|")
    for c in exclus:
        L.append("| %s | %s | %s | %s | %s | %s |" % (c.numero, cell(c.nom), cell(c.ticker), c.rarete,
                                                     cell(", ".join(c.motifs_exclusion)),
                                                     "oui" if c.brulable else "non"))
    L.append("")
    L.append("## Cartes")
    L.append("")
    L.append("| N° v2 | Nom | Ticker | Chaîne | Rareté | État | Brûlable | Raison |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in cartes:
        if c.mythique:
            L.append("| %s | ? | ? | ? | mythique | ? | non | %s |" % (c.numero, c.raison_brulable))
            continue
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            c.numero, cell(c.nom), cell(c.ticker), cell(norm_chaine(c.chaine) or "à vérifier"), c.rarete,
            cell(c.etat or "à vérifier"), "oui" if c.brulable else "non", cell(c.raison_brulable)))
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT, help="racine du dépôt")
    ap.add_argument("--extra", action="append", default=[], help="lot supplémentaire au format consigne")
    ap.add_argument("--sans-r4", action="store_true", help="ignorer r4-autres-chaines.md même s'il existe")
    ap.add_argument("--out-dir", default=None,
                    help="dossier de sortie (défaut : docs/ et docs/data/ ; secrets dans DIR/secrets/)")
    ap.add_argument("--demo", action="store_true",
                    help="produire aussi catalogue-demo.md et catalogue-demo.json (catalogue de démo filtré)")
    ap.add_argument("--min-brulables", type=int, default=MIN_BRULABLES,
                    help="démo : brûlables possibles visés avant réintégration (défaut %d)" % MIN_BRULABLES)
    ap.add_argument("--mythiques", default=None,
                    help="fichier secret qui désigne les mythiques (défaut : docs/data/secrets/mythiques.json "
                         "de la racine) ; lu avant d'être réécrit")
    a = ap.parse_args(argv)

    src = a.mythiques or os.path.join(a.root, "docs", "data", "secrets", "mythiques.json")
    if not os.path.exists(src):
        raise SystemExit("%s absent : impossible de savoir quelles cartes sont mythiques (fichier hors git, "
                         "à demander au porteur)" % src)
    res = construire(a.root, a.extra, r4=not a.sans_r4, mythiques=charger_mythiques_v1(src))
    cat, dec = finaliser(res["actives"], res["surclassements"])
    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
        dmd, djs = a.out_dir, a.out_dir
        sec = os.path.join(a.out_dir, "secrets", "mythiques.json")
    else:
        dmd, djs = os.path.join(a.root, "docs"), os.path.join(a.root, "docs", "data")
        sec = os.path.join(a.root, "docs", "data", "secrets", "mythiques.json")
    md, js = os.path.join(dmd, "catalogue-v2.md"), os.path.join(djs, "catalogue-v2.json")
    ecrire_md(md, cat, dec, res, res["lus"])
    with open(js, "w", encoding="utf-8") as f:
        json.dump([objet_json(c) for c in cat + dec], f, ensure_ascii=False, indent=1)
        f.write("\n")
    ecrire_secrets(sec, cat)
    r = Counter(c.rarete for c in cat)
    ab = [c for c in cat + dec if c.aberrant]
    print("pics aberrants : %d (épiques retombés : %d) ; surclassements : %d cartes" % (
        len(ab), epiques_retombes(cat + dec),
        sum(len(s["cartes"]) for s in res["surclassements"])))
    print("catalogue : %d cartes (%s) ; à décider : %d ; fusions : %d ; non reprises : %d ; réserve : %d"
          % (len(cat), ", ".join("%s %d" % (k, r[k]) for k in RARETES), len(dec), len(res["fusions"]),
             len(res["ignores"]), len(res["reserve"])))
    print("écrit : %s\n        %s\n        %s (secrets, hors git)" % (md, js, sec))
    if a.demo:
        demo = construire_demo(cat, dec, res["cg"], a.min_brulables)
        dm, dj = os.path.join(dmd, "catalogue-demo.md"), os.path.join(djs, "catalogue-demo.json")
        ecrire_md_demo(dm, demo)
        with open(dj, "w", encoding="utf-8") as f:
            json.dump([objet_json_demo(c) for c in demo["cartes"]], f, ensure_ascii=False, indent=1)
            f.write("\n")
        rd = Counter(c.rarete for c in demo["cartes"])
        bd = Counter(c.rarete for c in demo["cartes"] if c.brulable)
        print("démo : %d cartes (%s) ; brûlables : %d (%s) ; exclues : %d ; réintégrées : %d%s"
              % (len(demo["cartes"]), ", ".join("%s %d" % (k, rd[k]) for k in RARETES), sum(bd.values()),
                 ", ".join("%s %d" % (k, bd[k]) for k in RARETES), len(demo["exclus"]),
                 sum(1 for c in demo["cartes"] if c.reintegree), "" if demo["atteint"] else " ; OBJECTIF NON ATTEINT"))
        print("écrit : %s\n        %s" % (dm, dj))
    return 0


if __name__ == "__main__":
    sys.exit(main())
