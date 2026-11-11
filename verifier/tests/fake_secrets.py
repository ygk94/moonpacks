"""Faux fichier des vrais noms des mythiques pour les tests de ``build_series.py`` : les tests ne
dépendent plus de ``docs/data/secrets/mythiques.json`` (ignoré par git, absent d'un clone propre) et
n'utilisent jamais les vrais noms."""

import json
from pathlib import Path

CONTRACT = Path(__file__).resolve().parents[2] / "contract"
CATALOGUE = CONTRACT.parent / "docs" / "data" / "catalogue-v2.json"

FAKE = ["Fictif Alpha", "Fictif Beta", "Fictif Gamma"]
FAKE_TICKERS = ["FKALP", "FKBET", "FKGAM"]


def mythic_ids() -> list[str]:
    cat = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    return [c["id"] for c in cat if c.get("rarete") == "mythique" and c.get("section") == "catalogue"]


def fake_mythics() -> dict:
    """Format attendu par build_series.py : {"<id catalogue>": {"id": …, "nom": …, "ticker": …}}."""
    return {
        cid: {"id": f"fictif-{i + 1}", "nom": FAKE[i % len(FAKE)], "ticker": FAKE_TICKERS[i % len(FAKE)]}
        for i, cid in enumerate(mythic_ids())
    }


def write_fake_mythics(d) -> Path:
    p = Path(d) / "mythiques-fictives.json"
    p.write_text(json.dumps(fake_mythics(), ensure_ascii=False), encoding="utf-8")
    return p
