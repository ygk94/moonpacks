"""Client RPC : alias testnet et reprise sur limite de débit (HTTP 429), sans réseau."""

import io
import json
import unittest
import urllib.error
from unittest import mock

from memaster_verifier import rpc


def _http_error(code, headers=None):
    return urllib.error.HTTPError("https://x", code, "err", headers or {}, io.BytesIO(b"rate limit"))


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _ok(result):
    return _Resp(json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}).encode())


class RpcTest(unittest.TestCase):
    def test_testnet_alias_is_fastnear(self):
        self.assertEqual(rpc.Rpc("testnet").url, "https://rpc.testnet.fastnear.com")

    def test_retries_on_429_then_succeeds(self):
        sleeps = []
        r = rpc.Rpc("testnet", retry_delays=(1, 2, 4), sleep=sleeps.append)
        side = [_http_error(429), _http_error(429, {"Retry-After": "3"}), _ok({"v": 1})]
        with mock.patch("urllib.request.urlopen", side_effect=side) as m:
            self.assertEqual(r.call("block", {"finality": "final"}), {"v": 1})
        self.assertEqual(m.call_count, 3)
        self.assertEqual(sleeps, [1, 3.0])

    def test_gives_up_after_retries(self):
        r = rpc.Rpc("testnet", retry_delays=(1, 1), sleep=lambda s: None)
        with mock.patch("urllib.request.urlopen", side_effect=[_http_error(429)] * 3) as m:
            with self.assertRaisesRegex(rpc.RpcError, "HTTP 429"):
                r.call("block", {})
        self.assertEqual(m.call_count, 3)

    def test_no_retry_on_other_http_errors(self):
        r = rpc.Rpc("testnet", sleep=lambda s: self.fail("pas de reprise"))
        with mock.patch("urllib.request.urlopen", side_effect=[_http_error(408)]) as m:
            with self.assertRaisesRegex(rpc.RpcError, "HTTP 408"):
                r.call("EXPERIMENTAL_tx_status", {})
        self.assertEqual(m.call_count, 1)


if __name__ == "__main__":
    unittest.main()
