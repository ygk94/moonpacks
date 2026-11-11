"""Générateur pseudo-aléatoire déterministe (splitmix64), indépendant de la
version de Python : même graine, même suite, partout."""

from __future__ import annotations

_M = (1 << 64) - 1


class Alea:
    def __init__(self, graine: bytes):
        self.etat = int.from_bytes(graine[:8], "big") ^ int.from_bytes(graine[8:16], "big")

    def _suivant(self) -> int:
        self.etat = (self.etat + 0x9E3779B97F4A7C15) & _M
        z = self.etat
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _M
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _M
        return z ^ (z >> 31)

    def reel(self, a: float = 0.0, b: float = 1.0) -> float:
        return a + (b - a) * (self._suivant() >> 11) / float(1 << 53)

    def entier(self, a: int, b: int) -> int:
        """Entier dans [a, b] inclus."""
        return a + self._suivant() % (b - a + 1)

    def choix(self, suite):
        return suite[self._suivant() % len(suite)]

    def piece(self, p: float = 0.5) -> bool:
        return self.reel() < p
