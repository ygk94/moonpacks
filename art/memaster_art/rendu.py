"""Rendu SVG des cartes. Tout est une fonction pure de la carte (voir carte.Carte).

Format portrait 5:7 (500 x 700). Aucune image externe, aucune police embarquée :
les textes utilisent des familles génériques (sans-serif, serif, monospace).
"""

from __future__ import annotations

import colorsys
import math
from xml.sax.saxutils import escape

from .alea import Alea
from .carte import MENTION, MENTION_COURTE, Carte

L, H = 500, 700
# Fenêtre d'art (coordonnées de la carte)
AX, AY, AW, AH = 36, 80, 428, 392

POLICE = "sans-serif"
POLICE_MONO = "monospace"


# --------------------------------------------------------------------------- utilitaires

def n(v: float) -> str:
    """Nombre compact (1 décimale au plus)."""
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def hsl(h: float, s: float, l: float) -> str:
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l, s)
    return f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def x(t: str) -> str:
    return escape(t, {'"': "&quot;"})


def largeur_texte(t: str, taille: float) -> float:
    """Estimation grossière de la largeur d'un texte gras en sans-serif."""
    total = 0.0
    for c in t:
        if ord(c) > 0x2E80:  # idéogrammes : pleine chasse
            total += 1.0
        elif c in "MW":
            total += 0.9
        elif c.isupper() or c.isdigit():
            total += 0.70
        elif c in "il.,:;'|! ":
            total += 0.32
        else:
            total += 0.58
    return total * taille


def tronquer(t: str, nmax: int) -> str:
    return t if len(t) <= nmax else t[: nmax - 1] + "…"


def numero_affiche(numero) -> str:
    if numero is None or numero == "":
        return ""
    if isinstance(numero, int) or str(numero).isdigit():
        return f"N° {int(numero):04d}"
    return f"N° {numero}"


def abreger_id(ident: str) -> str:
    if ident.startswith("memaster:"):
        return "réf. " + ident
    return ident if len(ident) <= 22 else f"{ident[:10]}…{ident[-8:]}"


# --------------------------------------------------------------------------- palettes

SCHEMAS = {
    "analogue": (0, 32, -32, 64),
    "complément": (0, 180, 20, 200),
    "triade": (0, 120, 240, 60),
    "fendu": (0, 150, 210, 30),
}


def palette(r: Alea) -> dict:
    h0 = r.reel(0, 360)
    nom, ecarts = r.choix(list(SCHEMAS.items()))
    s = r.reel(0.62, 0.88)
    couleurs = [
        hsl(h0 + e, s - 0.08 * i, (0.52, 0.62, 0.46, 0.72)[i]) for i, e in enumerate(ecarts)
    ]
    return {
        "nom": nom,
        "teinte": h0,
        "c": couleurs,
        "fond": hsl(h0 + 200, 0.38, 0.13),
        "fond2": hsl(h0 + 230, 0.45, 0.22),
        "clair": hsl(h0, 0.35, 0.92),
    }


# --------------------------------------------------------------------------- motifs
# Chaque motif dessine dans un repère local 0..AW x 0..AH.

def motif_pavage(r: Alea, p: dict) -> str:
    nb = r.choix((6, 7, 8, 9))
    c = AW / nb
    rows = math.ceil(AH / c)
    d1, d2 = [], []
    for j in range(rows):
        for i in range(nb):
            x0, y0, h = i * c, j * c, c / 2
            if r.piece():
                a = f"M{n(x0 + h)} {n(y0)}A{n(h)} {n(h)} 0 0 1 {n(x0)} {n(y0 + h)}"
                b = f"M{n(x0 + c)} {n(y0 + h)}A{n(h)} {n(h)} 0 0 0 {n(x0 + h)} {n(y0 + c)}"
            else:
                a = f"M{n(x0 + h)} {n(y0)}A{n(h)} {n(h)} 0 0 0 {n(x0 + c)} {n(y0 + h)}"
                b = f"M{n(x0)} {n(y0 + h)}A{n(h)} {n(h)} 0 0 1 {n(x0 + h)} {n(y0 + c)}"
            ((d1 if (i + j) % 2 else d2)).append(a + b)
    w = n(c * r.reel(0.16, 0.26))
    pts = "".join(
        f'<circle cx="{n(i * c)}" cy="{n(j * c)}" r="{n(c * 0.14)}"/>'
        for j in range(rows + 1)
        for i in range(nb + 1)
        if r.piece(0.22)
    )
    return (
        f'<g fill="none" stroke-linecap="round" stroke-width="{w}">'
        f'<path stroke="{p["c"][0]}" d="{"".join(d1)}"/>'
        f'<path stroke="{p["c"][1]}" d="{"".join(d2)}"/></g>'
        f'<g fill="{p["c"][3]}">{pts}</g>'
    )


def motif_orbites(r: Alea, p: dict) -> str:
    cx, cy = r.reel(0.3, 0.7) * AW, r.reel(0.3, 0.7) * AH
    out = []
    rayon = r.reel(18, 30)
    k = 0
    while rayon < 420:
        coul = p["c"][k % 4]
        ep = r.reel(3, 14)
        tiret = "" if r.piece(0.4) else f' stroke-dasharray="{n(r.reel(4, 60))} {n(r.reel(6, 30))}"'
        out.append(
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(rayon)}" stroke="{coul}" '
            f'stroke-width="{n(ep)}"{tiret} opacity="{n(r.reel(0.55, 1))}"/>'
        )
        if r.piece(0.5):
            a = r.reel(0, 2 * math.pi)
            out.append(
                f'<circle cx="{n(cx + rayon * math.cos(a))}" cy="{n(cy + rayon * math.sin(a))}" '
                f'r="{n(ep * 0.9 + 3)}" fill="{p["clair"]}" stroke="none"/>'
            )
        rayon += ep + r.reel(8, 26)
        k += 1
    return f'<g fill="none">{"".join(out)}</g>'


def motif_ondes(r: Alea, p: dict) -> str:
    bandes = r.entier(6, 10)
    amp = r.reel(14, 40)
    freq = r.reel(1.0, 2.6)
    phase = r.reel(0, 6.3)
    derive = r.reel(-0.6, 0.6)
    out = []
    for b in range(bandes + 1):
        base = AH * b / (bandes + 1) - amp
        pts = []
        for s in range(13):
            t = s / 12
            y = base + amp * math.sin(2 * math.pi * freq * t + phase + b * derive)
            pts.append((t * AW, y))
        d = f"M0 {n(AH + 10)}L{n(pts[0][0])} {n(pts[0][1])}"
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            d += f"Q{n(x1)} {n(y1)} {n((x1 + x2) / 2)} {n((y1 + y2) / 2)}"
        d += f"L{AW} {n(pts[-1][1])}L{AW} {n(AH + 10)}Z"
        out.append(f'<path d="{d}" fill="{p["c"][b % 4]}"/>')
    return "".join(out)


def motif_eclats(r: Alea, p: dict) -> str:
    cx, cy = r.reel(0.25, 0.75) * AW, r.reel(0.25, 0.75) * AH
    nb = r.entier(11, 19)
    angles = sorted(r.reel(0, 2 * math.pi) for _ in range(nb))
    out = []
    for i, a in enumerate(angles):
        b = angles[(i + 1) % nb] + (2 * math.pi if i == nb - 1 else 0)
        r1, r2 = r.reel(180, 420), r.reel(180, 420)
        pts = [
            (cx, cy),
            (cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
            (cx + r2 * math.cos(b), cy + r2 * math.sin(b)),
        ]
        out.append(
            '<path d="M' + "L".join(f"{n(px)} {n(py)}" for px, py in pts) + 'Z" '
            f'fill="{p["c"][i % 4]}" opacity="{n(r.reel(0.7, 1))}"/>'
        )
    for _ in range(r.entier(3, 6)):
        a = r.reel(0, 2 * math.pi)
        rr = r.reel(40, 160)
        out.append(
            f'<path d="M{n(cx)} {n(cy)}L{n(cx + rr * math.cos(a))} {n(cy + rr * math.sin(a))}" '
            f'stroke="{p["clair"]}" stroke-width="2" opacity=".7"/>'
        )
    return "".join(out)


def motif_constellation(r: Alea, p: dict) -> str:
    nb = r.entier(16, 26)
    pts = [(r.reel(15, AW - 15), r.reel(15, AH - 15)) for _ in range(nb)]
    lignes = set()
    for i, (px, py) in enumerate(pts):
        proches = sorted(range(nb), key=lambda j: (pts[j][0] - px) ** 2 + (pts[j][1] - py) ** 2)
        for j in proches[1:3]:
            lignes.add((min(i, j), max(i, j)))
    d = "".join(
        f"M{n(pts[i][0])} {n(pts[i][1])}L{n(pts[j][0])} {n(pts[j][1])}" for i, j in sorted(lignes)
    )
    halos = "".join(
        f'<circle cx="{n(r.reel(0, AW))}" cy="{n(r.reel(0, AH))}" r="{n(r.reel(70, 170))}" '
        f'fill="{p["c"][k % 4]}" opacity=".35"/>'
        for k in range(3)
    )
    points = "".join(
        f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(r.reel(3, 11))}" fill="{p["c"][k % 4]}" '
        f'stroke="{p["clair"]}" stroke-width="1.5"/>'
        for k, (px, py) in enumerate(pts)
    )
    return f'{halos}<path d="{d}" stroke="{p["clair"]}" stroke-width="2" opacity=".75"/>{points}'


def motif_soleil(r: Alea, p: dict) -> str:
    cx, cy = r.reel(0.2, 0.8) * AW, r.reel(0.2, 0.8) * AH
    nb = r.choix((12, 16, 20, 24))
    out = []
    for i in range(nb):
        a1 = 2 * math.pi * i / nb
        a2 = 2 * math.pi * (i + 1) / nb
        out.append(
            f'<path d="M{n(cx)} {n(cy)}L{n(cx + 700 * math.cos(a1))} {n(cy + 700 * math.sin(a1))}'
            f'L{n(cx + 700 * math.cos(a2))} {n(cy + 700 * math.sin(a2))}Z" fill="{p["c"][i % 2]}"/>'
        )
    for k, rr in enumerate((r.reel(90, 130), r.reel(50, 80))):
        out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(rr)}" fill="{p["c"][2 + k]}"/>')
    return "".join(out)


MOTIFS = {
    "pavage": motif_pavage,
    "orbites": motif_orbites,
    "ondes": motif_ondes,
    "éclats": motif_eclats,
    "constellation": motif_constellation,
    "soleil": motif_soleil,
}


def embleme(r: Alea, p: dict) -> str:
    """Emblème géométrique central (étoile, polygones emboîtés ou anneau cranté)."""
    cx, cy = AW / 2 + r.reel(-30, 30), AH / 2 + r.reel(-25, 25)
    rr = r.reel(62, 88)
    rot = r.reel(0, 360)
    sorte = r.choix(("étoile", "polygones", "anneau"))
    fond = p["fond"]
    if sorte == "étoile":
        k = r.entier(5, 9)
        ratio = r.reel(0.42, 0.62)
        pts = []
        for i in range(2 * k):
            a = math.pi * i / k
            ri = rr if i % 2 == 0 else rr * ratio
            pts.append(f"{n(ri * math.cos(a))} {n(ri * math.sin(a))}")
        forme = f'<path d="M{"L".join(pts)}Z" fill="{p["clair"]}" stroke="{fond}" stroke-width="6"/>'
        coeur = f'<circle r="{n(rr * ratio * 0.5)}" fill="{p["c"][0]}"/>'
    elif sorte == "polygones":
        k = r.entier(3, 8)
        couches = []
        for j, f in enumerate((1.0, 0.68, 0.38)):
            pts = " ".join(
                f"{n(rr * f * math.cos(2 * math.pi * i / k + j * math.pi / k))},"
                f"{n(rr * f * math.sin(2 * math.pi * i / k + j * math.pi / k))}"
                for i in range(k)
            )
            couleur = (p["clair"], p["c"][1], fond)[j]
            couches.append(f'<polygon points="{pts}" fill="{couleur}" stroke="{fond}" stroke-width="5"/>')
        forme, coeur = "".join(couches), ""
    else:
        k = r.entier(6, 14)
        forme = (
            f'<circle r="{n(rr)}" fill="none" stroke="{p["clair"]}" stroke-width="{n(rr * 0.3)}" '
            f'stroke-dasharray="{n(2 * math.pi * rr / k * 0.62)} {n(2 * math.pi * rr / k * 0.38)}"/>'
        )
        coeur = f'<circle r="{n(rr * 0.42)}" fill="{p["c"][2]}" stroke="{fond}" stroke-width="5"/>'
    return (
        f'<g transform="translate({n(cx)} {n(cy)}) rotate({n(rot)})">'
        f'<circle r="{n(rr * 1.12)}" fill="{fond}" opacity=".55"/>{forme}{coeur}</g>'
    )


def fissures(r: Alea, nb: int, largeur: float = AW, hauteur: float = AH) -> str:
    d = []
    for _ in range(nb):
        bord = r.entier(0, 3)
        px, py = (
            (r.reel(0, largeur), 0),
            (largeur, r.reel(0, hauteur)),
            (r.reel(0, largeur), hauteur),
            (0, r.reel(0, hauteur)),
        )[bord]
        cap = math.atan2(hauteur / 2 - py, largeur / 2 - px)
        seg = f"M{n(px)} {n(py)}"
        for _ in range(r.entier(6, 10)):
            cap += r.reel(-0.7, 0.7)
            pas = r.reel(18, 42)
            px, py = px + pas * math.cos(cap), py + pas * math.sin(cap)
            seg += f"L{n(px)} {n(py)}"
            if r.piece(0.25):
                bx, by = px + 26 * math.cos(cap + 1.1), py + 26 * math.sin(cap + 1.1)
                seg += f"M{n(bx)} {n(by)}L{n(px)} {n(py)}"
        d.append(seg)
    chemin = "".join(d)
    return (
        f'<g fill="none" stroke-linejoin="round" stroke-linecap="round">'
        f'<path d="{chemin}" stroke="#f2efe6" stroke-width="4" opacity=".35" transform="translate(1.5 1.5)"/>'
        f'<path d="{chemin}" stroke="#141414" stroke-width="2.6"/></g>'
    )


# --------------------------------------------------------------------------- cadres par rareté

STYLES = {
    "commune": {"cadre": ("#a3a39b", "#6b6d68", "#4a4c49"), "texte": "#ece8dc", "accent": "#c9c4b4",
                "fond": "#262725", "label": "COMMUNE"},
    "rare": {"cadre": ("#a9d3ff", "#3d7cc9", "#1d3f73"), "texte": "#eef6ff", "accent": "#9fd0ff",
             "fond": "#0f1a2b", "label": "RARE"},
    "épique": {"cadre": ("#e7b6ff", "#9b3fe0", "#4a137f"), "texte": "#fbf2ff", "accent": "#e0a8ff",
               "fond": "#1c0d2b", "label": "ÉPIQUE"},
    "légendaire": {"cadre": ("#fff6c2", "#e3b230", "#8a5a00"), "texte": "#fffaf0", "accent": "#ffd65c",
                   "fond": "#1f1606", "label": "LÉGENDAIRE"},
    "mythique": {"cadre": ("#ffd75e", "#8f0d18", "#1a0204"), "texte": "#fff4e0", "accent": "#ffcf4a",
                 "fond": "#0b0507", "label": "MYTHIQUE"},
}

HOLO = (
    '<linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#ff5ea8"/><stop offset=".2" stop-color="#ffd84a"/>'
    '<stop offset=".4" stop-color="#5dffb0"/><stop offset=".6" stop-color="#4ad8ff"/>'
    '<stop offset=".8" stop-color="#9a6bff"/><stop offset="1" stop-color="#ff5ea8"/></linearGradient>'
    '<linearGradient id="reflet" x1="0" y1="0" x2="1" y2=".55">'
    '<stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/>'
    '<stop offset=".65" stop-color="#fff" stop-opacity="0"/></linearGradient>'
)


def forme_fenetre(rarete: str) -> str:
    """Chemin de la fenêtre d'art : arche de pierre tombale pour les communes."""
    if rarete == "commune":
        f = 96
        return (f"M{AX} {AY + f}A{AW / 2} {f} 0 0 1 {AX + AW} {AY + f}"
                f"V{AY + AH}H{AX}Z")
    rx = 14
    return (f"M{AX + rx} {AY}H{AX + AW - rx}A{rx} {rx} 0 0 1 {AX + AW} {AY + rx}V{AY + AH - rx}"
            f"A{rx} {rx} 0 0 1 {AX + AW - rx} {AY + AH}H{AX + rx}A{rx} {rx} 0 0 1 {AX} {AY + AH - rx}"
            f"V{AY + rx}A{rx} {rx} 0 0 1 {AX + rx} {AY}Z")


def etincelles(r: Alea, nb: int, couleur: str, zones) -> str:
    d = []
    for _ in range(nb):
        x0, y0, x1, y1 = r.choix(zones)
        cx, cy, t = r.reel(x0, x1), r.reel(y0, y1), r.reel(5, 11)
        q = t * 0.22
        d.append(
            f"M{n(cx)} {n(cy - t)}L{n(cx + q)} {n(cy - q)}L{n(cx + t)} {n(cy)}L{n(cx + q)} {n(cy + q)}"
            f"L{n(cx)} {n(cy + t)}L{n(cx - q)} {n(cy + q)}L{n(cx - t)} {n(cy)}L{n(cx - q)} {n(cy - q)}Z"
        )
    return f'<path d="{"".join(d)}" fill="{couleur}"/>'


def rayons_mythiques(r: Alea) -> str:
    """Aura dorée et rayons fins derrière l'emblème (recto mythique)."""
    cx, cy = AX + AW / 2, AY + AH / 2
    nb = 36
    d = "".join(
        f"M{n(cx)} {n(cy)}L{n(cx + 420 * math.cos(2 * math.pi * (i + .3) / nb))} "
        f"{n(cy + 420 * math.sin(2 * math.pi * (i + .3) / nb))}"
        f"L{n(cx + 420 * math.cos(2 * math.pi * (i + .7) / nb))} {n(cy + 420 * math.sin(2 * math.pi * (i + .7) / nb))}Z"
        for i in range(nb)
    )
    return (
        f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="url(#aura)" opacity=".75"/>'
        f'<path d="{d}" fill="#ffe9a8" opacity=".22"/>'
        f'<circle cx="{n(cx)}" cy="{n(cy)}" r="128" fill="none" stroke="#ffcf4a" stroke-width="3"/>'
        f'<circle cx="{n(cx)}" cy="{n(cy)}" r="138" fill="none" stroke="#ffcf4a" stroke-width="1" stroke-dasharray="2 6"/>'
    )


def sol_cimetiere(r: Alea) -> str:
    """Bande de terre et d'herbe abstraite au pied de l'arche (communes)."""
    y0 = AY + AH
    d = f"M{AX} {y0}V{y0 - 22}"
    xx = AX
    while xx < AX + AW:
        pas = r.reel(6, 12)
        d += f"L{n(xx + pas / 2)} {n(y0 - 22 - r.reel(6, 20))}L{n(xx + pas)} {n(y0 - 22)}"
        xx += pas
    d += f"L{AX + AW} {y0}Z"
    return f'<path d="{d}" fill="#1b1d19" opacity=".85"/>'


def ornements(rarete: str, st: dict, r: Alea) -> str:
    a = st["accent"]
    if rarete == "commune":
        # pierre : mouchetures et lierre abstrait (traits) en bas
        mouches = "".join(
            f'<circle cx="{n(r.reel(10, 490))}" cy="{n(r.reel(10, 690))}" r="{n(r.reel(0.8, 2.2))}"/>'
            for _ in range(70)
        )
        return f'<g fill="#1c1d1b" opacity=".35">{mouches}</g>'
    if rarete == "rare":
        coins = "".join(
            f'<rect x="{n(cx - 5)}" y="{n(cy - 5)}" width="10" height="10" transform="rotate(45 {cx} {cy})"/>'
            for cx, cy in ((26, 26), (474, 26), (26, 674), (474, 674))
        )
        return f'<g fill="{a}">{coins}</g>'
    if rarete == "épique":
        coins = []
        for cx, cy, sx, sy in ((24, 24, 1, 1), (476, 24, -1, 1), (24, 676, 1, -1), (476, 676, -1, -1)):
            coins.append(
                f'<path d="M{cx} {cy + sy * 46}V{cy}H{cx + sx * 46}" fill="none" stroke="{a}" stroke-width="4"/>'
                f'<circle cx="{cx + sx * 10}" cy="{cy + sy * 10}" r="5" fill="{a}"/>'
            )
        return "".join(coins)
    # légendaire et mythique : étincelles sur le cadre
    zones = ((20, 3, 480, 11), (20, 689, 480, 697), (3, 20, 11, 680), (489, 20, 497, 680))
    return etincelles(r, 14 if rarete == "légendaire" else 18, "#fff", zones)


# --------------------------------------------------------------------------- textes

def bloc_ticker(ticker: str, y: float, couleur: str, max_l: float = 420) -> str:
    taille = 64.0
    l = largeur_texte(ticker, taille)
    if l > max_l:
        taille = max(30.0, taille * max_l / l)
    extra = ""
    if largeur_texte(ticker, taille) > max_l:
        extra = f' textLength="{max_l}" lengthAdjust="spacingAndGlyphs"'
    return (
        f'<text x="250" y="{n(y)}" font-size="{n(taille)}" font-weight="700" fill="{couleur}" '
        f'text-anchor="middle"{extra}>{x(ticker)}</text>'
    )


def pastille_etat(etat: str, cx: float, cy: float) -> str:
    libelle, coul = {
        "actif": ("actif", "#2fbf71"),
        "en déclin": ("en déclin", "#f08c2e"),
        "mort": ("† mort", "#8d8d8d"),
        "à vérifier": ("état ?", "#7b8794"),
    }[etat]
    w = largeur_texte(libelle, 15) * 0.86 + 26
    return (
        f'<g transform="translate({n(cx - w / 2)} {n(cy - 13)})">'
        f'<rect width="{n(w)}" height="26" rx="13" fill="{coul}"/>'
        f'<text x="{n(w / 2)}" y="18" font-size="15" font-weight="700" fill="#101010" '
        f'text-anchor="middle">{x(libelle)}</text></g>'
    )


# --------------------------------------------------------------------------- carte complète

def choisir_motif(r: Alea) -> str:
    return r.choix(list(MOTIFS))


def rendre_carte(carte: Carte) -> str:
    """SVG du recto de la carte (y compris le recto révélé d'une mythique)."""
    r = Alea(carte.graine)
    p = palette(r)
    nom_motif = choisir_motif(r)
    art = MOTIFS[nom_motif](r, p)
    emb = embleme(r, p)
    # Les effets ont leur propre flux, pour que l'art ne dépende pas de la rareté.
    r2 = Alea(carte.graine[16:] + carte.rarete.encode() + carte.etat.encode())
    st = STYLES[carte.rarete]
    c1, c2, c3 = st["cadre"]
    holo = carte.rarete in ("légendaire", "mythique")
    annee = str(carte.annee_pic) if carte.annee_pic else "?"
    chaine = carte.chaine or "chaîne ?"

    defs = [
        f'<linearGradient id="cadre" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="{c1}"/>'
        f'<stop offset=".5" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/></linearGradient>',
        f'<clipPath id="fen"><path d="{forme_fenetre(carte.rarete)}"/></clipPath>',
    ]
    if holo:
        defs.append(HOLO)
    sat = {"actif": None, "à vérifier": None, "en déclin": ".42", "mort": "0"}[carte.etat]
    if carte.rarete == "commune" and sat is None:
        sat = ".7"  # pierre un peu passée même pour les communes vivantes
    if carte.etat == "mort":
        # gris de pierre légèrement chaud (sépia éteint)
        defs.append(
            '<filter id="ternir"><feColorMatrix type="matrix" values=".33 .5 .12 0 .04 '
            '.31 .48 .11 0 .03 .27 .42 .1 0 .02 0 0 0 1 0"/></filter>'
        )
    elif sat is not None:
        defs.append(f'<filter id="ternir"><feColorMatrix type="saturate" values="{sat}"/></filter>')
    if carte.rarete == "mythique":
        defs.append(
            '<radialGradient id="aura" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="#ffcf4a" stop-opacity=".95"/>'
            '<stop offset=".45" stop-color="#c1121f" stop-opacity=".55"/><stop offset="1" stop-color="#0b0507" stop-opacity="0"/></radialGradient>'
        )

    # ---- art
    filtre = ' filter="url(#ternir)"' if sat is not None else ""
    calques = [
        f'<g clip-path="url(#fen)">',
        f'<g{filtre}><rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="{p["fond"]}"/>',
        f'<g transform="translate({AX} {AY})">{art}</g>',
        rayons_mythiques(r2) if carte.rarete == "mythique" else "",
        f'<g transform="translate({AX} {AY})">{emb}</g></g>',
    ]
    if carte.etat == "mort":
        calques.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="#2e2c27" opacity=".4"/>')
    if carte.rarete == "commune":
        calques.append(sol_cimetiere(r2))
    if holo:
        calques.append(
            f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="url(#holo)" opacity=".3"/>'
            f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="url(#reflet)"/>'
        )
    nb_fissures = {"mort": 4, "en déclin": 1}.get(carte.etat, 0)
    if nb_fissures:
        calques.append(f'<g transform="translate({AX} {AY})">{fissures(r2, nb_fissures)}</g>')
    if carte.etat == "mort":
        calques.append(
            f'<text x="{AX + AW - 20}" y="{AY + AH - 24}" font-family="serif" '
            f'font-size="{46 if carte.annee_pic else 64}" font-weight="700" '
            f'fill="#efeae0" stroke="#111" stroke-width="1.5" text-anchor="end">'
            f'{"† " + annee if carte.annee_pic else "†"}</text>'
        )
    calques.append("</g>")
    contour = 3 if not holo else 4
    calques.append(
        f'<path d="{forme_fenetre(carte.rarete)}" fill="none" stroke="{st["accent"]}" stroke-width="{contour}"/>'
    )

    # ---- cadre
    cadre = [
        f'<rect width="{L}" height="{H}" rx="28" fill="url(#cadre)"/>',
    ]
    if holo:
        opa = ".22" if carte.rarete == "légendaire" else ".16"
        cadre.append(f'<rect width="{L}" height="{H}" rx="28" fill="url(#holo)" opacity="{opa}"/>')
    cadre.append(
        f'<rect x="14" y="14" width="472" height="672" rx="20" fill="{st["fond"]}" '
        f'stroke="{st["accent"]}" stroke-width="{2 if carte.rarete != "épique" else 3}"/>'
    )
    if carte.rarete == "mythique":
        cadre.append('<rect x="20" y="20" width="460" height="660" rx="16" fill="none" stroke="#c1121f" stroke-width="2"/>')
    cadre.append(ornements(carte.rarete, st, r2))

    # ---- textes
    t = st["texte"]
    num = numero_affiche(carte.numero)
    entete = st["label"] + (" · SECRÈTE" if carte.rarete == "mythique" else "")
    textes = [
        f'<text x="40" y="56" font-size="19" font-weight="700" letter-spacing="3" fill="{st["accent"]}">{x(entete)}</text>',
        f'<text x="460" y="56" font-size="16" fill="{t}" opacity=".75" text-anchor="end">{x(num)}</text>',
    ]
    y_ticker = 544
    if carte.rarete == "commune" or carte.etat == "mort":
        epitaphe = "ICI REPOSE" if carte.etat == "mort" else "CIMETIÈRE DES MÈMES"
        textes.append(
            f'<text x="250" y="492" font-family="serif" font-size="14" letter-spacing="4" fill="{st["accent"]}" '
            f'text-anchor="middle">{epitaphe}</text>'
        )
        y_ticker = 552
    textes.append(bloc_ticker(carte.ticker, y_ticker, t))
    textes.append(
        f'<text x="250" y="{y_ticker + 30}" font-size="19" fill="{t}" opacity=".82" text-anchor="middle">'
        f'{x(tronquer(carte.nom, 34))}</text>'
    )
    textes.append(
        f'<text x="40" y="620" font-size="17" fill="{t}">{x(tronquer(chaine, 16))}</text>'
        f'<text x="250" y="620" font-size="17" fill="{t}" text-anchor="middle">'
        f'{"pic " + annee if carte.annee_pic else "pic inconnu"}</text>'
    )
    textes.append(pastille_etat(carte.etat, 405, 614))
    textes.append(
        f'<text x="250" y="650" font-family="{POLICE_MONO}" font-size="12" fill="{t}" opacity=".6" '
        f'text-anchor="middle">{x(abreger_id(carte.adresse or carte.identifiant))}</text>'
        f'<text x="250" y="672" font-size="11" fill="{t}" opacity=".7" text-anchor="middle">{x(MENTION_COURTE)}</text>'
    )

    titre = f"{carte.ticker} · {carte.nom} · {carte.rarete}"
    desc = (
        f"Carte Memaster {carte.rarete}, état {carte.etat}, chaîne {chaine}, pic {annee}. "
        f"Ticker cité comme donnée factuelle ; visuel génératif abstrait (motif {nom_motif}, palette {p['nom']}). "
        + MENTION
    )
    return assembler(titre, desc, "".join(defs), "".join(cadre) + "".join(calques) + "".join(textes))


def assembler(titre: str, desc: str, defs: str, corps: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" height="{H}" '
        f'font-family="{POLICE}">'
        f"<title>{x(titre)}</title><desc>{x(desc)}</desc>"
        f"<defs>{defs}</defs>{corps}</svg>\n"
    )


# --------------------------------------------------------------------------- dos scellé (mythiques)

def rendre_dos() -> str:
    """Dos commun à toutes les mythiques avant révélation. Ne dépend d'aucune carte :
    il ne doit rien laisser deviner du recto."""
    st = STYLES["mythique"]
    r = Alea(b"memaster-dos-scelle-v1" + bytes(16))
    defs = (
        f'<linearGradient id="cadre" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#ffe28a"/>'
        f'<stop offset=".5" stop-color="#b8860b"/><stop offset="1" stop-color="#3b2600"/></linearGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#c1121f" stop-opacity=".9"/>'
        '<stop offset=".6" stop-color="#5a0610" stop-opacity=".5"/><stop offset="1" stop-color="#0b0507" stop-opacity="0"/></radialGradient>'
        '<ellipse id="pet" rx="150" ry="46" fill="none" stroke="#ffcf4a" stroke-width="1.4"/>'
        + HOLO
    )
    rosace = "".join(f'<use href="#pet" transform="rotate({k * 10})"/>' for k in range(18))
    rosace2 = "".join(
        f'<circle r="{rr}" fill="none" stroke="#ffcf4a" stroke-width="1" stroke-dasharray="3 5"/>'
        for rr in (176, 196, 212)
    )
    zones = ((40, 150, 460, 175), (40, 520, 460, 560))
    corps = (
        f'<rect width="{L}" height="{H}" rx="28" fill="url(#cadre)"/>'
        f'<rect width="{L}" height="{H}" rx="28" fill="url(#holo)" opacity=".3"/>'
        f'<rect x="14" y="14" width="472" height="672" rx="20" fill="{st["fond"]}" stroke="#ffcf4a" stroke-width="2"/>'
        '<rect x="22" y="22" width="456" height="656" rx="15" fill="none" stroke="#c1121f" stroke-width="2"/>'
        '<circle cx="250" cy="350" r="230" fill="url(#halo)"/>'
        f'<g transform="translate(250 350)" opacity=".75">{rosace}{rosace2}</g>'
        '<circle cx="250" cy="350" r="104" fill="#8f0d18" stroke="#ffcf4a" stroke-width="6"/>'
        '<circle cx="250" cy="350" r="88" fill="none" stroke="#ffcf4a" stroke-width="2" stroke-dasharray="6 6"/>'
        '<text x="250" y="400" font-family="serif" font-size="150" font-weight="700" fill="#fff4e0" '
        'text-anchor="middle">?</text>'
        + etincelles(r, 16, "#ffe9a8", zones)
        + f'<text x="250" y="88" font-size="22" font-weight="700" letter-spacing="6" fill="#ffcf4a" text-anchor="middle">MYTHIQUE</text>'
        '<text x="250" y="116" font-size="15" letter-spacing="3" fill="#fff4e0" opacity=".8" text-anchor="middle">CARTE SECRÈTE</text>'
        '<text x="250" y="602" font-size="26" font-weight="700" letter-spacing="5" fill="#fff4e0" text-anchor="middle">SCELLÉE</text>'
        '<text x="250" y="630" font-size="15" fill="#fff4e0" opacity=".75" text-anchor="middle">à révéler à l\'ouverture</text>'
        f'<text x="250" y="672" font-size="11" fill="#fff4e0" opacity=".7" text-anchor="middle">{x(MENTION_COURTE)}</text>'
    )
    return assembler(
        "Memaster · carte mythique scellée",
        "Dos scellé d'une carte mythique Memaster, identique pour toutes les mythiques. " + MENTION,
        defs,
        corps,
    )
