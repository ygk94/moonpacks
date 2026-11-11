#!/usr/bin/env python3
"""Génère hors ligne les engagements des mythiques secrètes d'une série Memaster.

Usage :
    python3 scripts/gen_mythics.py ENTREE.json PUBLIC.json SECRETS.json

ENTREE.json : liste de mythiques
    [{"card_id": "pepe", "weight": 1, "cap": 3,
      "content": {"title": "PEPE", "media": "ipfs://…", "reference": null,
                  "backing": {"asset_id": "nep141:…", "amount": "1000"}}}]

PUBLIC.json  : liste `mythics` à mettre dans la table (commitment, content_hash, weight, cap).
SECRETS.json : préimages (card_id, sel, content) à garder secrètes jusqu'à la révélation.
               Écrit par défaut sous scripts/secrets/, ignoré par git. Ne jamais le committer.

Un sel aléatoire de 32 octets est tiré pour CHAQUE mythique (secrets.token_bytes) : un sel court
ou partagé permettrait de retrouver les autres mythiques par force brute après une révélation.

Hashs (identiques au contrat, src/mythic.rs) :
    commitment   = sha256(card_id_utf8 || sel)
    content_hash = sha256(json_compact(content) || sel)
avec json_compact = sérialisation serde_json : champs dans l'ordre title, media, reference,
backing{asset_id, amount}, `null` pour les absents, amount en chaîne, sans espaces, UTF-8 brut.
"""
import hashlib
import json
import os
import secrets
import sys


def canonical_content(c):
    backing = c.get("backing")
    if backing is not None:
        backing = {"asset_id": str(backing["asset_id"]), "amount": str(int(backing["amount"]))}
    return {
        "title": c["title"],
        "media": c.get("media"),
        "reference": c.get("reference"),
        "backing": backing,
    }


def content_json(c):
    return json.dumps(canonical_content(c), separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    src, public_path, secrets_path = argv[1:]
    with open(src, encoding="utf-8") as f:
        entries = json.load(f)
    seen = set()
    public, private = [], []
    for i, e in enumerate(entries):
        card_id = e["card_id"]
        if card_id in seen:
            raise SystemExit(f"card_id en double : {card_id}")
        seen.add(card_id)
        if not (1 <= int(e["cap"]) <= 100):
            raise SystemExit(f"cap hors bornes pour {card_id}")
        sel = secrets.token_bytes(32)
        content = canonical_content(e["content"])
        commitment = hashlib.sha256(card_id.encode("utf-8") + sel).hexdigest()
        content_hash = hashlib.sha256(content_json(content) + sel).hexdigest()
        public.append({"commitment": commitment, "content_hash": content_hash,
                       "weight": int(e["weight"]), "cap": int(e["cap"])})
        private.append({"mythic_index": i, "card_id": card_id, "sel": sel.hex(), "content": content,
                        "commitment": commitment, "content_hash": content_hash})
    if len({p["commitment"] for p in public}) != len(public):
        raise SystemExit("engagement en double")
    os.makedirs(os.path.dirname(os.path.abspath(secrets_path)), exist_ok=True)
    fd = os.open(secrets_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(private, f, ensure_ascii=False, indent=2)
    with open(public_path, "w", encoding="utf-8") as f:
        json.dump(public, f, indent=2)
    print(f"{len(public)} engagements -> {public_path} ; secrets -> {secrets_path} (ne pas committer)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
