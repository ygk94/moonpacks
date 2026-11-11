"""Planches HTML de contact (50 cartes par page) pour relire les visuels."""

from __future__ import annotations

import re
from xml.sax.saxutils import escape

from .carte import MENTION

PAR_PAGE = 50


def planches(entrees: list[tuple[str, str]], titre: str = "Memaster : planche") -> list[tuple[str, str]]:
    """entrees : (fichier svg relatif, légende). Renvoie [(nom de fichier, html)]."""
    pages = [entrees[i : i + PAR_PAGE] for i in range(0, len(entrees), PAR_PAGE)] or [[]]
    sortie = []
    for k, page in enumerate(pages, 1):
        nom = f"planche-{k:02d}.html"
        nav = " ".join(
            f'<a href="planche-{j:02d}.html"{" class=ici" if j == k else ""}>{j}</a>'
            for j in range(1, len(pages) + 1)
        )
        cases = "\n".join(
            f'<figure><img src="{escape(f)}" loading="lazy" alt="{escape(l)}">'
            f"<figcaption>{escape(l)}</figcaption></figure>"
            for f, l in page
        )
        html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titre)} {k}/{len(pages)}</title>
<style>
:root{{--fond:#15161a;--texte:#e8e6e1;--doux:#9a9890}}
body{{margin:0;padding:16px;background:var(--fond);color:var(--texte);font:14px/1.4 sans-serif}}
h1{{font-size:18px;margin:0 0 4px}} p{{color:var(--doux);margin:0 0 12px}}
nav a{{color:var(--doux);margin-right:6px}} nav a.ici{{color:var(--texte);font-weight:700}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:12px}}
figure{{margin:0}} img{{width:100%;aspect-ratio:5/7;display:block;border-radius:8px;background:#000}}
figcaption{{font-size:12px;color:var(--doux);margin-top:4px;overflow-wrap:anywhere}}
</style></head><body>
<h1>{escape(titre)} — page {k}/{len(pages)} ({len(page)} cartes)</h1>
<p>{escape(MENTION)}</p>
<nav>{nav}</nav>
<main>
{cases}
</main></body></html>
"""
        sortie.append((nom, html))
    return sortie


# --------------------------------------------------------------------------- planche SVG (pour rendu PNG)

def _isoler_ids(svg: str, prefixe: str) -> str:
    """Préfixe les id d'un SVG de carte pour l'imbriquer sans collision (cadre, holo, fen…)."""
    svg = re.sub(r"^<\?xml[^>]*>\s*", "", svg)
    svg = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{prefixe}{m.group(1)}"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{prefixe}{m.group(1)})", svg)
    return re.sub(r'href="#([^"]+)"', lambda m: f'href="#{prefixe}{m.group(1)}"', svg)


def planche_svg(cartes: list[tuple[str, str]], titre: str, colonnes: int = 3) -> str:
    """cartes : (texte SVG 500 × 700, légende). Renvoie une planche SVG autonome."""
    marge, ecart, haut_titre, haut_leg = 40, 30, 70, 34
    lignes = -(-len(cartes) // colonnes)
    largeur = 2 * marge + colonnes * 500 + (colonnes - 1) * ecart
    hauteur = marge + haut_titre + lignes * (700 + haut_leg + ecart) - ecart + marge
    corps = [
        f'<rect width="{largeur}" height="{hauteur}" fill="#15161a"/>',
        f'<text x="{marge}" y="{marge + 34}" font-size="34" font-weight="700" fill="#e8e6e1">{escape(titre)}</text>',
        f'<text x="{largeur - marge}" y="{marge + 34}" font-size="16" fill="#9a9890" text-anchor="end">{escape(MENTION)}</text>',
    ]
    for k, (svg, legende) in enumerate(cartes):
        x0 = marge + (k % colonnes) * (500 + ecart)
        y0 = marge + haut_titre + (k // colonnes) * (700 + haut_leg + ecart)
        interne = _isoler_ids(svg, f"c{k}-").replace("<svg ", f'<svg x="{x0}" y="{y0}" ', 1)
        corps.append(interne)
        corps.append(f'<text x="{x0 + 250}" y="{y0 + 700 + 24}" font-size="18" fill="#c8c6c0" '
                     f'text-anchor="middle">{escape(legende)}</text>')
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" width="{largeur}" '
        f'height="{hauteur}" font-family="sans-serif">' + "".join(corps) + "</svg>\n"
    )
