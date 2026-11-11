#!/usr/bin/env python3
"""Mesures Memaster sur NEAR testnet (bibliothèque standard + near-cli-rs pour signer).

    python3 scripts/measure_testnet.py buy --contract C --series 0 --buyers b1,b2,b3 --rounds 10 --out txs.jsonl
        Achète des boosters : à chaque tour, un buy_pack par acheteur, lancés en même temps
        (plusieurs achats tombent alors souvent dans le même bloc). --serial : un achat à la fois,
        avec le stockage du contrat lu avant et après (stockage par pack).
    python3 scripts/measure_testnet.py analyze --in txs.jsonl --out measures.json --events events.jsonl
        Relit chaque transaction (EXPERIMENTAL_tx_status), hauteurs des reçus, gaz et NEAR brûlés,
        événements ; écrit les événements EVENT_JSON dans l'ordre d'exécution (pour le vérificateur).
    python3 scripts/measure_testnet.py blocktime [--span 10000]
    python3 scripts/measure_testnet.py tx --hash H --sender S      (une transaction quelconque)

Testnet seulement : refuse un compte qui ne finit pas par .testnet. Aucune clé n'est lue ici :
near-cli-rs signe avec ~/.near-credentials (sign-with-legacy-keychain).
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

RPC = "https://rpc.testnet.fastnear.com"
FALLBACK = "https://archival-rpc.testnet.fastnear.com"
TX_RE = re.compile(r"Transaction ID: ([1-9A-HJ-NP-Za-km-z]{43,44})")


def rpc(method, params, url=None, tries=6):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    last = None
    for i in range(tries):
        u = url or (RPC if i < tries - 2 else FALLBACK)
        try:
            r = json.load(urllib.request.urlopen(
                urllib.request.Request(u, body, {"content-type": "application/json"}), timeout=30))
            if "error" in r:
                last = r["error"]
                if "UNKNOWN_TRANSACTION" in json.dumps(last) or "TIMEOUT" in json.dumps(last):
                    time.sleep(2 + i * 2)
                    continue
                return r
            return r
        except Exception as e:  # réseau, 429
            last = str(e)
            time.sleep(2 + i * 2)
    raise RuntimeError(f"RPC {method} : {last}")


def view(contract, method, args=None, block=None):
    p = {"request_type": "call_function", "account_id": contract, "method_name": method,
         "args_base64": base64.b64encode(json.dumps(args or {}).encode()).decode()}
    p.update({"block_id": block} if block else {"finality": "final"})
    return json.loads(bytes(rpc("query", p)["result"]["result"]).decode())


def account(acc, block=None):
    p = {"request_type": "view_account", "account_id": acc}
    p.update({"block_id": block} if block else {"finality": "final"})
    return rpc("query", p)["result"]


_heights = {}


def height(block_hash):
    if block_hash not in _heights:
        h = rpc("block", {"block_id": block_hash})["result"]["header"]
        _heights[block_hash] = (h["height"], int(h["timestamp_nanosec"]), h["gas_price"])
    return _heights[block_hash]


def near_call(contract, method, args, signer, gas_tgas, deposit_yocto):
    cmd = ["near", "contract", "call-function", "as-transaction", contract, method, "json-args",
           json.dumps(args), "prepaid-gas", f"{gas_tgas} Tgas", "attached-deposit", f"{deposit_yocto} yoctonear",
           "sign-as", signer, "network-config", "testnet", "sign-with-legacy-keychain", "send"]
    # Le RPC de near-cli-rs (fastnear) limite le débit : une erreur de lecture de clé ou de nonce
    # survient avant la signature, aucune transaction n'est envoyée, on peut donc réessayer.
    for i in range(6):
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = p.stdout + p.stderr
        m = TX_RE.search(out)
        if m or "rate limit" not in out:
            break
        time.sleep(15 * (i + 1))
    return {"signer": signer, "method": method, "args": args, "tx": m.group(1) if m else None,
            "sent_at": t0, "returned_at": time.time(), "ok": p.returncode == 0,
            "err": None if p.returncode == 0 else out[-600:]}


def cmd_buy(a):
    buyers = a.buyers.split(",")
    for b in buyers + [a.contract]:
        if not b.endswith(".testnet"):
            sys.exit("testnet seulement")
    s = view(a.contract, "get_series", {"series_id": a.series})
    dep, gas = int(s["required_deposit"]), int(s["min_gas"]) // 10 ** 12
    gas = max(gas, a.gas)
    with open(a.out, "a") as f:
        for r in range(a.rounds):
            if a.serial:
                for b in buyers:
                    before = account(a.contract)
                    x = near_call(a.contract, "buy_pack", {"series_id": a.series}, b, gas, dep)
                    time.sleep(a.settle)  # laisser finir les reçus chaînés
                    after = account(a.contract)
                    x.update(round=r, series=a.series, mode="serial", storage_before=before["storage_usage"],
                             storage_after=after["storage_usage"], storage_height_after=after["block_height"])
                    f.write(json.dumps(x) + "\n"); f.flush()
                    print(r, b, x["tx"], x["storage_after"] - x["storage_before"], x["err"] and x["err"][-200:])
            else:
                with ThreadPoolExecutor(len(buyers)) as ex:
                    res = list(ex.map(lambda b: near_call(a.contract, "buy_pack", {"series_id": a.series}, b, gas, dep),
                                      buyers))
                for x in res:
                    x.update(round=r, series=a.series, mode="parallel")
                    f.write(json.dumps(x) + "\n"); f.flush()
                    print(r, x["signer"], x["tx"], x["err"] and x["err"][-200:])
                time.sleep(a.pause)


def events_of(logs):
    out = []
    for l in logs:
        if l.startswith("EVENT_JSON:"):
            out.append(json.loads(l[len("EVENT_JSON:"):]))
    return out


def analyze_tx(tx, sender):
    """Reçus, hauteurs, gaz et événements d'une transaction. Une erreur RPC (transaction inconnue,
    RPC injoignable) donne un enregistrement `rpc_error` au lieu d'interrompre tout le lot."""
    try:
        r = rpc("EXPERIMENTAL_tx_status", {"tx_hash": tx, "sender_account_id": sender, "wait_until": "FINAL"})
    except RuntimeError as e:
        r = {"error": str(e)}
    if "result" not in r:
        return {"tx": tx, "sender": sender, "tx_height": None, "tx_ts": None, "gas_price": None,
                "status": "rpc_error", "error": r.get("error"), "rows": [], "events": []}
    res = r["result"]
    to = res["transaction_outcome"]
    th, tts, gp = height(to["block_hash"])
    rows = [{"kind": "tx", "height": th, "gas": to["outcome"]["gas_burnt"],
             "tokens": int(to["outcome"]["tokens_burnt"]), "executor": to["outcome"]["executor_id"]}]
    methods = {}
    for rc in res.get("receipts", []):
        for act in rc["receipt"].get("Action", {}).get("actions", []):
            if isinstance(act, dict) and "FunctionCall" in act:
                methods[rc["receipt_id"]] = act["FunctionCall"]["method_name"]
    evs = []
    for ro in res["receipts_outcome"]:
        h, ts, _ = height(ro["block_hash"])
        o = ro["outcome"]
        e = events_of(o["logs"])
        evs.extend((h, x) for x in e)
        status = o["status"]
        # Remboursement (gaz, dépôt) : reçu système exécuté chez l'expéditeur, sans journal.
        rows.append({"kind": methods.get(ro["id"], "refund" if o["executor_id"] == sender and not o["logs"]
                                         and o["gas_burnt"] < 300_000_000_000 else "?"),
                     "height": h, "ts": ts, "gas": o["gas_burnt"], "tokens": int(o["tokens_burnt"]),
                     "executor": o["executor_id"], "failed": "Failure" in status,
                     "events": [x.get("event") for x in e]})
    return {"tx": tx, "sender": sender, "tx_height": th, "tx_ts": tts, "gas_price": gp,
            "status": "Failure" if "Failure" in res["status"] else "ok", "rows": rows, "events": evs}


def cmd_analyze(a):
    txs = [json.loads(l) for l in open(a.inp) if l.strip()]
    txs = [t for t in txs if t.get("tx")]
    out = []
    with ThreadPoolExecutor(4) as ex:
        out = list(ex.map(lambda t: (t, analyze_tx(t["tx"], t["signer"])), txs))
    packs, all_events = [], []
    for t, r in out:
        rows = r["rows"]
        buy = next((x for x in rows if x["kind"] == "buy_pack"), None)
        steps = [x for x in rows if x["kind"] == "reveal_step"]
        rev = next((x for x in rows if "pack_revealed" in x.get("events", [])), None)
        pid = next((e["data"][0]["pack_id"] if isinstance(e.get("data"), list) else e["data"].get("pack_id")
                    for _, e in r["events"] if e.get("event") == "pack_bought"), None)
        p = {"tx": r["tx"], "signer": t["signer"], "series": t.get("series"), "mode": t.get("mode"),
             "round": t.get("round"), "pack_id": pid, "status": r["status"], "tx_height": r["tx_height"],
             "buy_height": buy and buy["height"], "step_heights": [x["height"] for x in steps],
             "reveal_height": rev and rev["height"],
             "blocks_buy_to_reveal": (rev["height"] - buy["height"]) if (rev and buy) else None,
             "gas_total": sum(x["gas"] for x in rows), "near_burnt": sum(x["tokens"] for x in rows) / 1e24,
             "gas": {x["kind"] + (f"#{i}" if x["kind"] == "reveal_step" else ""): x["gas"]
                     for i, x in enumerate(rows)},
             "gas_buy": buy and buy["gas"], "gas_final": rev and rev["gas"],
             "gas_steps": [x["gas"] for x in steps], "failed_receipts": sum(x.get("failed", False) for x in rows),
             "latency_s": (t["returned_at"] - t["sent_at"]),
             "storage_delta": (t["storage_after"] - t["storage_before"]) if "storage_after" in t else None}
        packs.append(p)
        all_events.extend(r["events"])
    # Ordre d'exécution : bloc, puis pack_id (attribué séquentiellement par buy_pack, donc ordre
    # réel de plusieurs achats d'un même bloc ; l'ordre des transactions lues ne l'est pas).
    def _pid(e):
        d = e.get("data")
        d = d[0] if isinstance(d, list) and d else (d or {})
        return d.get("pack_id", -1) if isinstance(d, dict) else -1
    all_events.sort(key=lambda he: (he[0], _pid(he[1])))
    if a.events:
        with open(a.events, "w") as f:
            for _, e in all_events:
                f.write(json.dumps(e, separators=(",", ":")) + "\n")
    json.dump({"packs": packs}, open(a.out, "w"), indent=1)
    summarize(packs)


def summarize(packs):
    ok = [p for p in packs if p["reveal_height"]]
    print(f"{len(packs)} transactions, {len(ok)} révélées")
    errs = [p["tx"] for p in packs if p["status"] == "rpc_error"]
    if errs:
        print(f"{len(errs)} transaction(s) illisible(s) par le RPC : {errs}")
    if not ok:
        return
    d = [p["blocks_buy_to_reveal"] for p in ok if p["blocks_buy_to_reveal"] is not None]
    print("blocs buy_pack -> pack_revealed :", {k: d.count(k) for k in sorted(set(d))})
    print("blocs tx -> buy_pack :", sorted({p["buy_height"] - p["tx_height"] for p in ok if p["buy_height"] is not None}))
    g = sorted(p["gas_total"] for p in ok)
    print(f"gaz total : min {g[0]/1e12:.2f} méd {g[len(g)//2]/1e12:.2f} max {g[-1]/1e12:.2f} Tgas")
    for k in ("gas_buy", "gas_final"):
        v = sorted(p[k] for p in ok if p[k] is not None)
        if v:
            print(f"{k} : min {v[0]/1e12:.2f} max {v[-1]/1e12:.2f} Tgas")
    nb = sorted(p["near_burnt"] for p in ok)
    print(f"NEAR brûlés : min {nb[0]:.5f} max {nb[-1]:.5f}")
    by_block = {}
    for p in ok:
        if p["buy_height"] is not None:
            by_block.setdefault(p["buy_height"], []).append(p)
    same = {h: len(v) for h, v in by_block.items() if len(v) > 1}
    print("buy_pack dans le même bloc :", same)


def cmd_blocktime(a):
    top = rpc("block", {"finality": "final"})["result"]["header"]
    old = rpc("block", {"block_id": top["height"] - a.span}, url=FALLBACK)["result"]["header"]
    dt = (int(top["timestamp_nanosec"]) - int(old["timestamp_nanosec"])) / 1e9
    dh = top["height"] - old["height"]
    print(json.dumps({"from": old["height"], "to": top["height"], "seconds": dt,
                      "avg_block_s": dt / dh, "blocks_per_s": dh / dt}))


def cmd_tx(a):
    r = analyze_tx(a.hash, a.sender)
    r["events"] = [e for _, e in r["events"]]
    print(json.dumps(r, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("buy")
    b.add_argument("--contract", required=True); b.add_argument("--series", type=int, default=0)
    b.add_argument("--buyers", required=True); b.add_argument("--rounds", type=int, default=1)
    b.add_argument("--gas", type=int, default=160); b.add_argument("--out", required=True)
    b.add_argument("--serial", action="store_true"); b.add_argument("--settle", type=float, default=8)
    b.add_argument("--pause", type=float, default=2)
    an = sp.add_parser("analyze")
    an.add_argument("--in", dest="inp", required=True); an.add_argument("--out", required=True)
    an.add_argument("--events")
    bt = sp.add_parser("blocktime"); bt.add_argument("--span", type=int, default=10000)
    t = sp.add_parser("tx"); t.add_argument("--hash", required=True); t.add_argument("--sender", required=True)
    a = ap.parse_args()
    {"buy": cmd_buy, "analyze": cmd_analyze, "blocktime": cmd_blocktime, "tx": cmd_tx}[a.cmd](a)


if __name__ == "__main__":
    main()
