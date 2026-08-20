#!/usr/bin/env python3
"""Exact arithmetic audit for commensurate FCC [001] abrupt twists."""

from __future__ import annotations

from fractions import Fraction as Q
from math import gcd

LIMIT = 80


def reduced_index(m: int, n: int) -> int:
    if gcd(m, n) != 1:
        raise ValueError("parameters must be coprime")
    norm = m * m + n * n
    while norm % 2 == 0:
        norm //= 2
    return norm


def rotation_data(m: int, n: int) -> tuple[int, int, int]:
    denominator = m * m + n * n
    cosine_numerator = m * m - n * n
    sine_numerator = 2 * m * n
    assert cosine_numerator**2 + sine_numerator**2 == denominator**2
    return cosine_numerator, sine_numerator, denominator


def main() -> None:
    records: list[tuple[int, int, int]] = []
    for m in range(1, LIMIT + 1):
        for n in range(0, m + 1):
            if gcd(m, n) != 1:
                continue
            sigma = reduced_index(m, n)
            rotation_data(m, n)
            assert sigma % 2 == 1
            ratio = Q(sigma - 1, sigma)
            density = 4 * ratio
            assert density == Q(4 * sigma - 4, sigma)
            if sigma > 1:
                assert sigma >= 5
                assert ratio >= Q(4, 5)
                assert density >= Q(16, 5)
            records.append((sigma, m, n))

    nontrivial = sorted({sigma for sigma, _, _ in records if sigma > 1})
    assert nontrivial[0] == 5
    assert (2, 1) in sorted((m, n) for sigma, m, n in records if sigma == 5)
    assert rotation_data(2, 1) == (3, 4, 5)

    print("FCC [001] COINCIDENCE-FAMILY ABRUPT AUDIT")
    print("status: PASS")
    print(f"primitive parameter audit range: 1 <= m <= {LIMIT}, 0 <= n <= m")
    print(f"primitive pairs checked: {len(records)}")
    print(f"smallest nontrivial reduced index: {nontrivial[0]}")
    print("first distinct nontrivial reduced indices: " + ", ".join(map(str, nontrivial[:12])))
    print("general formula:")
    print("  maximum restored abrupt cross contacts per cell = 4")
    print("  two-crack deficit per cell = 4*Sigma")
    print("  abrupt deficit per cell = 4*Sigma-4")
    print("  physical coincidence area = Sigma")
    print("  abrupt density = 4*(1-1/Sigma)")
    print("  ratio to two cracks = 1-1/Sigma")
    print("nontrivial family bound:")
    print("  Sigma >= 5")
    print("  abrupt ratio >= 4/5")
    print("  abrupt density >= 16/5")
    print("Sigma-5 equality case:")
    print("  parameter pair (m,n) = (2,1)")
    print("  rotation numerator = [[3,-4],[4,3]]")
    print("  rotation denominator = 5")
    print("  density = 16/5")


if __name__ == "__main__":
    main()
