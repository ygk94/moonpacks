#!/usr/bin/env python3
"""Visuels des cartes pour IPFS : dossier à publier, CID calculé en local, envoi (jeton en variable d'environnement).

Usage (depuis contract/) :
    # 0. SVG anglais (art/out/ est ignoré par git)
    (cd ../art && python3 -m memaster_art --catalogue ../docs/data/catalogue-demo.json --out out/demo-en/ --langue en)
    # 1. dossier à publier : <card_id>.svg pour chaque carte visible de la table, mythique.svg (dos « ? » commun)
    python3 -I scripts/ipfs_media.py prepare --art ../art/out/demo-en --catalogue ../docs/data/catalogue-demo.json \
        --dest scripts/out/ipfs-demo-en
    # 2. CAR et CID racine, en local, sans rien envoyer (npx ipfs-car@3.1.0 pack)
    python3 -I scripts/ipfs_media.py cid --dir scripts/out/ipfs-demo-en
    # 3. envoi du CAR (même CID que l'étape 2) ; --dry-run n'envoie rien
    PINATA_JWT=… python3 -I scripts/ipfs_media.py upload --car scripts/out/ipfs-demo-en.car --provider pinata
    W3S_TOKEN=…  python3 -I scripts/ipfs_media.py upload --car scripts/out/ipfs-demo-en.car --provider w3s
puis `build_series.py … --media-base ipfs://<CID>` (media = ipfs://<CID>/<card_id>.svg, mythiques ipfs://<CID>/mythique.svg).

On envoie le CAR, pas les fichiers : le fournisseur garde alors le CID calculé ici (un envoi de fichiers laisserait le
fournisseur choisir version de CID, découpage et enveloppe de dossier). `upload` compare le CID renvoyé au CID racine du
CAR (`ipfs-car roots`) et échoue s'ils diffèrent. Le jeton n'est lu que dans l'environnement, jamais écrit ni affiché.

Les noms de fichiers sont les card_id de la table (build_series.short_id), jamais un vrai id de mythique : les trois
mythiques partagent mythique.svg. Si docs/data/secrets/mythiques.json existe, `prepare` vérifie qu'aucun vrai nom, id
ou adresse de mythique n'apparaît dans mythique.svg ni comme nom de fichier.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.dirname(HERE)
REPO = os.path.dirname(CONTRACT)
sys.path.insert(0, HERE)

IPFS_CAR = os.environ.get("IPFS_CAR", "ipfs-car@3.1.0")
MYTHIC_FILE = "mythique.svg"
MYTHIC_SRC = "dos-mythique.svg"
DEFAULT_SECRETS = os.path.join(REPO, "docs", "data", "secrets", "mythiques.json")
PROVIDERS = {
    # Pinata, API v3 : envoi d'un CAR (champ car=true), réseau public. Jeton : JWT « Admin » ou droits d'envoi.
    "pinata": {"env": "PINATA_JWT", "url": "https://uploads.pinata.cloud/v3/files", "kind": "multipart"},
    # web3.storage, ancienne API HTTP (POST /car) : peut avoir fermé, à vérifier avant usage.
    "w3s": {"env": "W3S_TOKEN", "url": "https://api.web3.storage/car", "kind": "car"},
}
CID_RE = re.compile(r"\b(bafy[a-z2-7]{50,})\b")


def visible_ids(catalogue):
    import build_series  # short_id : même raccourcissement que la table
    return [(c["id"], build_series.short_id(c["id"])) for c in catalogue
            if c.get("section") == "catalogue" and c.get("rarete") != "mythique"]


def leak_terms(secrets_path):
    if not secrets_path or not os.path.exists(secrets_path):
        return []
    with open(secrets_path, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("mythiques", data) if isinstance(data, dict) else data
    if isinstance(items, dict):
        items = list(items.values())
    terms = []
    for e in items:
        for k in ("nom", "id", "adresse", "coingecko_id"):
            v = (e.get(k) or "").strip()
            if len(v) >= 4 and v != "?":
                terms.append(v)
    return terms


def prepare(art, catalogue, dest, secrets_path=DEFAULT_SECRETS):
    ids = visible_ids(catalogue)
    missing = [cid for cid, _ in ids if not os.path.exists(os.path.join(art, cid + ".svg"))]
    if missing or not os.path.exists(os.path.join(art, MYTHIC_SRC)):
        raise SystemExit(f"SVG manquants dans {art} : {(missing + [MYTHIC_SRC])[:5]}… ({len(missing)} cartes)")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for cid, tid in ids:
        shutil.copyfile(os.path.join(art, cid + ".svg"), os.path.join(dest, tid + ".svg"))
    shutil.copyfile(os.path.join(art, MYTHIC_SRC), os.path.join(dest, MYTHIC_FILE))
    names = sorted(os.listdir(dest))
    if len(names) != len(ids) + 1:
        raise SystemExit("noms de fichiers en double après raccourcissement")
    # Fuite possible : un fichier nommé d'après un vrai id de mythique, ou le visuel « ? » qui en contiendrait un
    # élément. (Une carte visible peut légitimement porter un nom proche : on ne la contrôle pas.)
    terms = leak_terms(secrets_path)
    with open(os.path.join(dest, MYTHIC_FILE), encoding="utf-8") as f:
        mythic_svg = f.read().lower()
    for t in terms:
        if t + ".svg" in names or t.lower() in mythic_svg:
            raise SystemExit("FUITE : un élément de mythique apparaît dans le dossier à publier")
    return {"files": len(names), "cards": len(ids), "bytes": sum(os.path.getsize(os.path.join(dest, n)) for n in names),
            "leak_check": bool(terms)}


def run_ipfs_car(*args):
    r = subprocess.run(["npx", "--yes", IPFS_CAR, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ipfs-car {' '.join(args)} : {r.stderr.strip()[:300]}")
    return r.stdout


def parse_cid(text):
    m = CID_RE.search(text)
    if not m:
        raise SystemExit(f"CID introuvable dans : {text.strip()[:200]}")
    return m.group(1)


def pack(directory, car=None):
    """CAR du dossier (enveloppé : la racine est le dossier, ses fichiers à la racine) et CID racine."""
    car = car or directory.rstrip("/") + ".car"
    cid = parse_cid(run_ipfs_car("pack", directory, "--output", car))
    root = parse_cid(run_ipfs_car("roots", car))
    if root != cid:
        raise SystemExit(f"CID de pack {cid} différent de la racine du CAR {root}")
    return cid, car


def multipart(fields, file_field, filename, data, ctype):
    boundary = "----memaster" + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
                 f"Content-Type: {ctype}\r\n\r\n".encode() + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def build_request(provider, car_path, token, name):
    p = PROVIDERS[provider]
    with open(car_path, "rb") as f:
        data = f.read()
    headers = {"authorization": f"Bearer {token}", "user-agent": "curl/8.7.1", "accept": "application/json"}
    if p["kind"] == "multipart":
        body, ctype = multipart({"network": "public", "car": "true", "name": name}, "file",
                                os.path.basename(car_path), data, "application/vnd.ipld.car")
    else:
        body, ctype = data, "application/vnd.ipld.car"
        headers["x-name"] = name
    headers["content-type"] = ctype
    return urllib.request.Request(p["url"], body, headers, method="POST")


def returned_cid(provider, resp):
    if provider == "pinata":
        return (resp.get("data") or {}).get("cid")
    return resp.get("cid")


def upload(provider, car_path, name, dry_run=False, expected=None, opener=urllib.request.urlopen):
    p = PROVIDERS[provider]
    expected = expected or parse_cid(run_ipfs_car("roots", car_path))
    token = os.environ.get(p["env"])
    size = os.path.getsize(car_path)
    plan = {"provider": provider, "url": p["url"], "car": car_path, "bytes": size, "expected_cid": expected,
            "token_env": p["env"], "token_present": bool(token)}
    if dry_run:
        req = build_request(provider, car_path, token or "<absent>", name)
        plan["request"] = {"method": req.get_method(), "content_type": req.get_header("Content-type"),
                           "body_bytes": len(req.data), "authorization": "Bearer ***"}
        return plan
    if not token:
        raise SystemExit(f"{p['env']} absent de l'environnement : rien n'est envoyé")
    with opener(build_request(provider, car_path, token, name), timeout=300) as r:
        resp = json.load(r)
    got = returned_cid(provider, resp)
    if got != expected:
        raise SystemExit(f"CID renvoyé {got!r} différent du CID local {expected} : ne pas utiliser")
    plan["uploaded_cid"] = got
    return plan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("prepare")
    p1.add_argument("--art", required=True, help="sortie de memaster_art (SVG nommés par id du catalogue)")
    p1.add_argument("--catalogue", default=os.path.join(REPO, "docs", "data", "catalogue-demo.json"))
    p1.add_argument("--dest", required=True)
    p1.add_argument("--mythiques", default=DEFAULT_SECRETS, help="contrôle anti-fuite (fichier secret, facultatif)")
    p2 = sub.add_parser("cid")
    p2.add_argument("--dir", required=True)
    p2.add_argument("--car")
    p3 = sub.add_parser("upload")
    p3.add_argument("--car", required=True)
    p3.add_argument("--provider", choices=sorted(PROVIDERS), default="pinata")
    p3.add_argument("--name", default="memaster-demo-en")
    p3.add_argument("--dry-run", action="store_true", help="prépare la requête sans rien envoyer")
    a = ap.parse_args(argv)
    if a.cmd == "prepare":
        with open(a.catalogue, encoding="utf-8") as f:
            cat = json.load(f)
        print(json.dumps(prepare(a.art, cat, a.dest, a.mythiques)))
    elif a.cmd == "cid":
        cid, car = pack(a.dir, a.car)
        print(json.dumps({"cid": cid, "car": car, "media_base": f"ipfs://{cid}"}))
    else:
        print(json.dumps(upload(a.provider, a.car, a.name, a.dry_run), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
