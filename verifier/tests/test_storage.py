"""Bloc `storage` de `pack_revealed` (contrat v3) : montant rendu = prépayé − utilisé."""

import unittest

from memaster_verifier.verify import Report, verify_storage


class StorageBlock(unittest.TestCase):
    def check(self, st):
        rep = Report("t")
        verify_storage(rep, {"storage": st} if st is not None else {})
        return rep

    def test_refund_matches_prepaid_minus_used(self):
        rep = self.check({"prepaid_bytes": 1605, "used_bytes": 1034, "refund": str(571 * 10**19)})
        self.assertTrue(rep.ok, rep.render())

    def test_tampered_refund_is_detected(self):
        rep = self.check({"prepaid_bytes": 1605, "used_bytes": 1034, "refund": str(572 * 10**19)})
        self.assertFalse(rep.ok)

    def test_overuse_refunds_nothing(self):
        rep = self.check({"prepaid_bytes": 1000, "used_bytes": 1200, "refund": "0"})
        self.assertTrue(rep.ok, rep.render())
        self.assertTrue(any("relances" in n for n in rep.notes))

    def test_old_events_without_block(self):
        rep = self.check(None)
        self.assertTrue(rep.ok)
        self.assertTrue(rep.notes)


if __name__ == "__main__":
    unittest.main()
