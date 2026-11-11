"""Client JSON-RPC NEAR minimal (bibliothèque standard uniquement)."""

from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.request

NETWORKS = {
    "mainnet": "https://rpc.mainnet.near.org",
    # rpc.testnet.near.org est déprécié (répond 429 « THIS ENDPOINT IS DEPRECATED »).
    "testnet": "https://rpc.testnet.fastnear.com",
}
# Reprise sur limite de débit (HTTP 429) : attentes successives en secondes, ou Retry-After si fourni.
RETRY_DELAYS = (1.0, 2.0, 4.0, 8.0)

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    pad = len(b) - len(b.lstrip(b"\0"))
    return "1" * pad + out


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + _B58.index(ch)
    pad = len(s) - len(s.lstrip("1"))
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * pad + body


class RpcError(Exception):
    pass


class Rpc:
    def __init__(self, url: str, timeout: float = 30.0, retry_delays=RETRY_DELAYS, sleep=time.sleep):
        self.url = NETWORKS.get(url, url)
        self.timeout = timeout
        self.retry_delays = tuple(retry_delays)
        self._sleep = sleep

    def call(self, method: str, params):
        body = json.dumps({"jsonrpc": "2.0", "id": "memaster-verifier", "method": method, "params": params})
        for attempt in range(len(self.retry_delays) + 1):
            try:
                return self._call_once(method, body)
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == len(self.retry_delays):
                    raise self._http_error(method, e) from e
                retry_after = e.headers.get("Retry-After") if e.headers else None
                try:
                    delay = min(float(retry_after), 60.0) if retry_after else self.retry_delays[attempt]
                except ValueError:
                    delay = self.retry_delays[attempt]
                self._sleep(delay)

    def _call_once(self, method: str, body: str):
        req = urllib.request.Request(
            self.url,
            data=body.encode(),
            headers={"Content-Type": "application/json", "User-Agent": "memaster-verifier"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                resp = json.loads(r.read())
        except urllib.error.HTTPError:
            raise  # traité par call() (reprise sur 429), avant URLError dont il hérite
        except urllib.error.URLError as e:
            raise RpcError(f"RPC injoignable ({self.url}) : {e}") from e
        if "error" in resp:
            raise RpcError(f"{method} : {json.dumps(resp['error'], ensure_ascii=False)}")
        return resp["result"]

    @staticmethod
    def _http_error(method: str, e: urllib.error.HTTPError) -> RpcError:
        detail = e.read()[:500].decode("utf-8", "replace")
        hint = " (transaction inconnue de ce nœud, ou trop ancienne : utilisez un nœud d'archive)" if e.code == 408 else ""
        if e.code == 429:
            hint = " (limite de débit du RPC, reprises épuisées)"
        return RpcError(f"{method} : HTTP {e.code}{hint} {detail}")

    def _block_ref(self, block_id) -> dict:
        return {"finality": "final"} if block_id is None else {"block_id": block_id}

    def view_raw(self, contract: str, method: str, args: dict | None = None, block_id=None) -> bytes:
        """Octets bruts renvoyés par une vue."""
        return self.view_raw_at(contract, method, args, block_id)[0]

    def view_raw_at(self, contract: str, method: str, args: dict | None = None, block_id=None) -> tuple[bytes, int]:
        """Octets bruts d'une vue et hauteur du bloc lu (pour lire plusieurs pages au même bloc)."""
        params = {
            "request_type": "call_function",
            "account_id": contract,
            "method_name": method,
            "args_base64": base64.b64encode(json.dumps(args or {}).encode()).decode(),
            **self._block_ref(block_id),
        }
        res = self.call("query", params)
        if "error" in res:
            raise RpcError(f"{method} : {res['error']}")
        return bytes(res["result"]), int(res.get("block_height", 0)) or None

    def view(self, contract: str, method: str, args: dict | None = None, block_id=None):
        return json.loads(self.view_raw(contract, method, args, block_id))

    def view_account(self, account: str) -> dict:
        return self.call("query", {"request_type": "view_account", "account_id": account, "finality": "final"})

    def tx_status(self, tx_hash: str, sender: str) -> dict:
        try:
            return self.call(
                "EXPERIMENTAL_tx_status",
                {"tx_hash": tx_hash, "sender_account_id": sender, "wait_until": "EXECUTED_OPTIMISTIC"},
            )
        except RpcError as e:
            if "HTTP 408" in str(e):
                raise
            # Anciens nœuds : paramètres positionnels.
            return self.call("EXPERIMENTAL_tx_status", [tx_hash, sender])

    def tx_logs(self, tx_hash: str, sender: str) -> list[str]:
        st = self.tx_status(tx_hash, sender)
        logs = list(st.get("transaction_outcome", {}).get("outcome", {}).get("logs", []))
        for ro in st.get("receipts_outcome", []):
            logs.extend(ro["outcome"].get("logs", []))
        return logs
