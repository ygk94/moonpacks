"""CLI : `python3 -m memaster_verifier {table,pack,mythic,stats,code} ...`"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

from . import core, stats, verify
from .rpc import Rpc, RpcError, b58encode


class UsageError(Exception):
    pass


def _rpc(args) -> Rpc | None:
    return Rpc(args.rpc) if args.rpc else None


def _need_rpc(args, what: str) -> Rpc:
    if not args.rpc or not args.contract:
        raise UsageError(f"{what} : --rpc et --contract sont requis")
    return Rpc(args.rpc)


def _read_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _table_bytes_from_file(path: str) -> bytes:
    """Fichier = la table seule (octets bruts de la vue de préférence), ou un objet `{"table": ...}`
    ou `{"table_raw": "..."}` (format des vecteurs)."""
    with open(path, "rb") as f:
        raw = f.read()
    obj = json.loads(raw)
    if isinstance(obj, dict) and "table_raw" in obj:
        return obj["table_raw"].encode("utf-8")
    if isinstance(obj, dict) and "table" in obj and "cards" not in obj:
        from .canon import table_json_bytes

        return table_json_bytes(obj["table"])
    return raw.strip()


MAX_PAGE = 200


def fetch_table_pages(rpc: Rpc, contract: str, series_id: int, page_size: int = MAX_PAGE) -> tuple[dict, list[bytes]]:
    """En-tête léger (`get_series_header`) puis pages brutes de `get_series_cards`, toutes lues au
    bloc de l'en-tête. Aucune vue ne relit la table entière : le coût par appel est borné quelle
    que soit la taille de la série (voir le README du contrat pour le gaz mesuré)."""
    raw, height = rpc.view_raw_at(contract, "get_series_header", {"series_id": series_id})
    header = json.loads(raw)
    page_size = max(1, min(page_size, int(header.get("max_page", MAX_PAGE))))
    n = int(header["card_count"])
    pages = []
    for start in range(0, n, page_size):
        pages.append(
            rpc.view_raw(
                contract, "get_series_cards", {"series_id": series_id, "from_index": start, "limit": page_size}, block_id=height
            )
        )
    return header, pages


def _load_table(args, series_id: int | None) -> tuple[dict, str]:
    if getattr(args, "table", None):
        return json.loads(_table_bytes_from_file(args.table)), f"fichier {args.table}"
    if args.rpc and args.contract and series_id is not None:
        header, pages = fetch_table_pages(Rpc(args.rpc), args.contract, series_id, getattr(args, "page_size", MAX_PAGE))
        table, problems = verify.table_from_pages(header, pages)
        if problems:
            raise ValueError("table lue par pages incohérente : " + " ; ".join(problems))
        th = core.table_hash(table).hex()
        if th != header.get("table_hash"):
            raise ValueError(f"table lue par pages : sha256 {th} ≠ hash enregistré {header.get('table_hash')}")
        return table, f"RPC get_series_header + {len(pages)} pages de get_series_cards({series_id}), hash = hash enregistré"
    raise UsageError("table introuvable : --table FICHIER, ou --rpc et --contract")


def _emit(reports: list[verify.Report], verbose: bool) -> int:
    for r in reports:
        print(r.render(verbose))
    bad = [r for r in reports if not r.ok]
    if len(reports) > 1:
        print(f"\n{len(reports) - len(bad)}/{len(reports)} vérifiés" + (f", {len(bad)} non conformes" if bad else ""))
    return 1 if bad else 0


# ------------------------------------------------------------------ table


def cmd_table(args) -> int:
    expected: dict[str, str | None] = {}
    on_chain = bool(args.rpc and args.contract and args.series is not None)
    if not args.file:
        _need_rpc(args, "table")
        if args.series is None:
            raise UsageError("table : --series requis avec --rpc")
    if on_chain:
        # Hash enregistré à l'ouverture : vue légère, le contrat ne recalcule rien.
        h = Rpc(args.rpc).view(args.contract, "get_series_table_hash", {"series_id": args.series})
        expected["get_series_table_hash.stored (enregistré à l'ouverture)"] = h["stored"]
    if args.expected_hash:
        expected["--expected-hash"] = args.expected_hash.lower()
    if args.file:
        if on_chain:
            # Le fichier doit avoir le hash enregistré sur la chaîne (aussi lu dans l'en-tête).
            hv = Rpc(args.rpc).view(args.contract, "get_series_header", {"series_id": args.series})
            expected["get_series_header.table_hash (enregistré à l'ouverture)"] = hv["table_hash"]
        rep, table = verify.verify_table(_table_bytes_from_file(args.file), expected)
    else:
        header, pages = fetch_table_pages(Rpc(args.rpc), args.contract, args.series, args.page_size)
        rep, table = verify.verify_table_pages(header, pages, expected)
        rep.note(f"pages de {min(args.page_size, int(header.get('max_page', MAX_PAGE)))} cartes ; hash recalculé localement, jamais par le contrat")
    for line in verify.table_summary(table):
        rep.note(line)
    return _emit([rep], True)


# ------------------------------------------------------------------ pack


def _load_snapshot(path: str) -> tuple[list[int], list[int]]:
    o = _read_json(path)
    m = o.get("minted", o.get("minted_before"))
    mm = o.get("mythic_minted", o.get("mythic_minted_before"))
    if m is None or mm is None:
        raise UsageError("instantané : clés minted et mythic_minted attendues (sortie de get_series)")
    return list(m), list(mm)


def cmd_pack(args) -> int:
    rpc = _rpc(args)
    if args.event:
        events = verify.load_events(args.event, "pack_revealed")
    elif args.tx_hash:
        rpc = _need_rpc(args, "pack --tx-hash")
        if not args.sender:
            raise UsageError("pack --tx-hash : --sender (signataire de buy_pack ou retry_reveal) requis")
        logs = rpc.tx_logs(args.tx_hash, args.sender)
        events = verify.events_from_logs(logs, "pack_revealed")
        if not events:
            raise UsageError("aucun événement pack_revealed dans cette transaction (tirage pas encore final ?)")
    else:
        raise UsageError("pack : --event FICHIER ou --tx-hash")
    if args.pack_id is not None:
        events = [e for e in events if int(e["pack_id"]) == args.pack_id]
        if not events:
            raise UsageError(f"booster {args.pack_id} absent des événements")
    series_ids = {e["series_id"] for e in events}
    if len(series_ids) != 1:
        raise UsageError(f"événements de plusieurs séries {sorted(series_ids)} : filtrez avec --pack-id")
    sid = series_ids.pop()
    table, tsrc = _load_table(args, sid)
    print(f"table : {tsrc}")

    if len(events) > 1:
        # Plusieurs événements : rejeu dans l'ordre fourni.
        m = mm = None
        if args.snapshot:
            m, mm = _load_snapshot(args.snapshot)
        print(f"rejeu de {len(events)} boosters dans l'ordre du fichier, compteurs initiaux : {'instantané' if m else 'zéro (ouverture)'}")
        reports, m, mm = verify.replay(table, events, None, m, mm)
        print(f"minted après rejeu : {m} / mythiques {mm}")
        return _emit(reports, args.verbose)

    ev = events[0]
    target = int(ev["pack_id"])
    if args.no_state:
        return _emit([verify.verify_pack(ev, table, None, None)], True)
    if args.snapshot:
        m, mm = _load_snapshot(args.snapshot)
        return _emit([verify.verify_pack(ev, table, m, mm, f"instantané {args.snapshot}")], True)
    if args.history:
        hist = [e for e in verify.load_events(args.history, "pack_revealed") if e["series_id"] == sid]
        before = []
        for e in hist:
            if int(e["pack_id"]) == target:
                break
            before.append(e)
        reports, m, mm = verify.replay(table, before)
        bad = sum(1 for r in reports if not r.ok)
        src = f"rejeu de {len(before)} boosters de {args.history}" + (f" (dont {bad} NON CONFORMES)" if bad else "")
        rep = verify.verify_pack(ev, table, m, mm, src)
        if bad:
            rep.errors.append(f"{bad} boosters antérieurs non conformes dans l'historique")
        return _emit([rep], True)
    if rpc and args.contract:
        h = verify.final_block_height(ev)
        view = rpc.view(args.contract, "get_series", {"series_id": sid}, block_id=h - 1)
        rep = verify.verify_pack(
            ev, table, view["minted"], view["mythic_minted"], f"RPC get_series({sid}) au bloc {h - 1} (veille du tirage, bloc {h})"
        )
        if not rep.ok:
            rep.note(
                "écart possible si un autre booster de la série a été tiré plus tôt dans le même bloc : "
                "relancez avec --history (rejeu) pour trancher"
            )
        return _emit([rep], True)
    print("aucun état des plafonds fourni : vérification partielle")
    return _emit([verify.verify_pack(ev, table, None, None)], True)


# ------------------------------------------------------------------ mythic


def cmd_mythic(args) -> int:
    rpc = _rpc(args)
    items = []  # (index, card_id, sel, content, source)
    series_id = args.series
    if args.event:
        for ev in verify.load_events(args.event, "mythic_revealed"):
            if "sel" in ev and "card_id" in ev:
                items.append((ev["mythic_index"], ev["card_id"], ev["sel"], ev["content"], ev, "événement"))
                series_id = ev["series_id"] if series_id is None else series_id
    elif args.card_id:
        if args.sel is None or args.content is None or args.index is None:
            raise UsageError("mythic : --card-id, --sel, --content FICHIER et --index ensemble")
        items.append((args.index, args.card_id, args.sel, _read_json(args.content), None, "arguments"))
    else:
        rpc = _need_rpc(args, "mythic")
        if series_id is None:
            raise UsageError("mythic : --series requis avec --rpc")
        for mv in rpc.view(args.contract, "get_mythic_commitments", {"series_id": series_id}):
            if args.index is not None and mv["index"] != args.index:
                continue
            r = mv.get("revealed")
            if r is None:
                print(f"mythique #{mv['index']} : pas encore révélée ({mv['minted']} sortie(s), engagement {mv['commitment']})")
                continue
            items.append((mv["index"], r["card_id"], r["sel"], r["content"], None, "get_mythic_commitments"))
    if args.index is not None:
        items = [x for x in items if x[0] == args.index]
    if not items:
        print("aucune révélation à vérifier")
        return 1 if args.event or args.card_id else 0

    table = None
    try:
        table, tsrc = _load_table(args, series_id)
        th = core.table_hash(table).hex()
        print(f"engagements de référence : {tsrc} (sha256 {th})")
    except UsageError:
        print("pas de table : engagements pris dans l'événement lui-même (auto-déclarés, à comparer à la table)")
    reports = []
    for index, card_id, sel, content, ev, src in items:
        if table is not None:
            m = table["mythics"][index]
            rep = verify.verify_mythic(card_id, sel, content, m["commitment"], m["content_hash"], "table", index)
            if ev is not None:
                rep.check(
                    ev.get("commitment") == m["commitment"] and ev.get("content_hash") == m["content_hash"],
                    "engagements de l'événement = ceux de la table",
                    "les engagements de l'événement diffèrent de ceux de la table",
                )
        elif ev is not None:
            rep = verify.verify_mythic(card_id, sel, content, ev["commitment"], ev["content_hash"], "événement", index)
        else:
            raise UsageError("mythic : table requise (--table ou --rpc/--contract/--series)")
        rep.note(f"source de la préimage : {src}")
        reports.append(rep)
    return _emit(reports, True)


# ------------------------------------------------------------------ stats


def cmd_stats(args) -> int:
    events = []
    for p in args.events:
        events.extend(verify.load_events(p, "pack_revealed"))
    if args.series is not None:
        events = [e for e in events if e["series_id"] == args.series]
    sids = {e["series_id"] for e in events}
    if len(sids) != 1:
        raise UsageError(f"il faut les événements d'une seule série (trouvé {sorted(sids)}) : --series")
    sid = sids.pop()
    table, tsrc = _load_table(args, sid)
    print(f"table : {tsrc}")
    code = 0
    if args.replay:
        reports, m, mm = verify.replay(table, events)
        bad = [r for r in reports if not r.ok]
        print(f"rejeu depuis l'ouverture : {len(reports) - len(bad)}/{len(reports)} boosters vérifiés ; minted final {m} / {mm}")
        for r in bad:
            print(r.render(False))
        code = 1 if bad else 0
    ok, lines = stats.series_stats(table, events, args.alpha)
    print("\n".join(lines))
    return code or (0 if ok else 1)


# ------------------------------------------------------------------ code


def cmd_code(args) -> int:
    rpc = _need_rpc(args, "code")
    with open(args.wasm, "rb") as f:
        wasm = f.read()
    local = b58encode(hashlib.sha256(wasm).digest())
    acct = rpc.view_account(args.contract)
    rep = verify.Report(f"Code déployé sur {args.contract}")
    rep.check(acct["code_hash"] == local, f"code_hash {local} = sha256({args.wasm})", f"code_hash déployé {acct['code_hash']} ≠ sha256 local {local}")
    rep.note("ne prouve le code source que si le wasm local vient d'un build reproductible (non configuré à ce jour)")
    return _emit([rep], True)


# ------------------------------------------------------------------ main


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--rpc", help="URL RPC NEAR, ou mainnet / testnet")
    common.add_argument("--contract", help="compte du contrat Memaster")

    p = argparse.ArgumentParser(prog="python3 -m memaster_verifier", description="Vérificateur public des tirages Memaster")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("table", parents=[common], help="recalcule le hash d'une table de série")
    t.add_argument("--series", type=int)
    t.add_argument("--file", help="table JSON (octets bruts de get_series_table de préférence)")
    t.add_argument("--expected-hash", help="hash hex attendu (sinon lu sur la chaîne avec --rpc)")
    t.add_argument("--page-size", type=int, default=MAX_PAGE, help="cartes par page de get_series_cards (200 au plus)")
    t.set_defaults(func=cmd_table)

    k = sub.add_parser("pack", parents=[common], help="recalcule acc et les tirages d'un pack_revealed")
    k.add_argument("--event", help="fichier : événement(s) pack_revealed (JSON, JSONL ou lignes EVENT_JSON:)")
    k.add_argument("--tx-hash", help="transaction buy_pack (ou retry_reveal) à lire par EXPERIMENTAL_tx_status")
    k.add_argument("--sender", help="signataire de la transaction")
    k.add_argument("--pack-id", type=int, help="booster à vérifier parmi plusieurs événements")
    k.add_argument("--table", help="table JSON (sinon lue par RPC)")
    g = k.add_mutually_exclusive_group()
    g.add_argument("--snapshot", help="minted / mythic_minted juste avant le tirage (sortie de get_series)")
    g.add_argument("--history", help="tous les pack_revealed de la série, dans l'ordre d'exécution, pour rejouer les plafonds")
    g.add_argument("--no-state", action="store_true", help="vérification sans l'état des plafonds")
    k.add_argument("-v", "--verbose", action="store_true")
    k.set_defaults(func=cmd_pack)

    m = sub.add_parser("mythic", parents=[common], help="vérifie la révélation d'une mythique")
    m.add_argument("--series", type=int)
    m.add_argument("--index", type=int, help="index de la mythique dans la table")
    m.add_argument("--event", help="fichier : événement(s) mythic_revealed")
    m.add_argument("--table", help="table JSON (engagements de référence)")
    m.add_argument("--card-id")
    m.add_argument("--sel", help="sel en hex (32 octets)")
    m.add_argument("--content", help="fichier JSON MythicContent")
    m.set_defaults(func=cmd_mythic)

    s = sub.add_parser("stats", parents=[common], help="fréquences observées contre taux annoncés (χ²)")
    s.add_argument("--events", nargs="+", required=True, help="fichiers d'événements pack_revealed")
    s.add_argument("--series", type=int)
    s.add_argument("--table", help="table JSON (sinon lue par RPC)")
    s.add_argument("--alpha", type=float, default=0.001, help="seuil du test (défaut 0.001)")
    s.add_argument("--replay", action="store_true", help="vérifie aussi chaque tirage en rejouant depuis l'ouverture")
    s.set_defaults(func=cmd_stats)

    c = sub.add_parser("code", parents=[common], help="compare le code déployé à un wasm local")
    c.add_argument("--wasm", required=True)
    c.set_defaults(func=cmd_code)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (UsageError, RpcError, OSError, ValueError, KeyError) as e:
        print(f"erreur : {e}", file=sys.stderr)
        return 2
