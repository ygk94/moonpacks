"""Rend des SVG de cartes en PNG pour relecture (macOS : qlmanage + sips ;
sinon rsvg-convert ou cairosvg s'ils sont installés).

    python3 outils/rendre_png.py out/0010-bonk.svg out/0007-wif.svg --dest /tmp/png
"""

import argparse
import os
import re
import shutil
import subprocess
import tempfile


def rendre(svg: str, dest: str, largeur: int = 500) -> str:
    os.makedirs(dest, exist_ok=True)
    base = os.path.splitext(os.path.basename(svg))[0]
    png = os.path.join(dest, base + ".png")
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", str(largeur), "-o", png, svg], check=True)
        return png
    try:
        import cairosvg  # type: ignore

        cairosvg.svg2png(url=svg, write_to=png, output_width=largeur)
        return png
    except ImportError:
        pass
    if not shutil.which("qlmanage"):
        raise SystemExit("aucun moteur de rendu : installer rsvg-convert ou cairosvg")
    # qlmanage produit une vignette carrée : on centre l'image dans un carré, puis on recadre.
    contenu = open(svg, encoding="utf-8").read()
    contenu = re.sub(r"^<\?xml[^>]*>\s*", "", contenu)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', contenu)
    w, h = (round(float(m.group(1))), round(float(m.group(2)))) if m else (500, 700)
    cote = max(w, h)
    contenu = contenu.replace("<svg ", f'<svg x="{(cote - w) // 2}" y="{(cote - h) // 2}" ', 1)
    carre = ('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" '
             f'viewBox="0 0 {cote} {cote}" width="{cote}" height="{cote}">' + contenu + "</svg>")
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, base + ".svg")
        open(f, "w", encoding="utf-8").write(carre)
        subprocess.run(["qlmanage", "-t", "-s", str(cote), "-o", tmp, f], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        brut = f + ".png"
        subprocess.run(["sips", "-c", str(h), str(w), brut, "--out", png], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if largeur != w:
            subprocess.run(["sips", "-Z", str(round(largeur * max(w, h) / w)), png], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--largeur", type=int, default=500)
    a = ap.parse_args()
    for s in a.svg:
        print(rendre(s, a.dest, a.largeur))
