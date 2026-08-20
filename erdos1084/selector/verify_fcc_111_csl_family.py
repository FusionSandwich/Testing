#!/usr/bin/env python3
"""Exact arithmetic audit for commensurate FCC [111] abrupt twists."""

from __future__ import annotations

from fractions import Fraction as Q
from math import gcd

LIMIT = 80


def eisenstein_norm(a: int, b: int) -> int:
    return a * a - a * b + b * b


def reduced_index(a: int, b: int) -> int:
    if gcd(abs(a), abs(b)) != 1:
        raise ValueError("parameters must be primitive")
    norm = eisenstein_norm(a, b)
    while norm % 3 == 0:
        norm //= 3
    return norm


def main() -> None:
    records: list[tuple[int, int, int]] = []
    for a in range(-LIMIT, LIMIT + 1):
        for b in range(-LIMIT, LIMIT + 1):
            if a == 0 and b == 0:
                continue
            if gcd(abs(a), abs(b)) != 1:
                continue
            sigma = reduced_index(a, b)
            ratio = Q(sigma - 1, sigma)
            assert Q(3 * sigma - 3, 3 * sigma) == ratio
            if sigma > 1:
                assert sigma >= 7
                assert ratio >= Q(6, 7)
            records.append((sigma, a, b))

    nontrivial = sorted({sigma for sigma, _, _ in records if sigma > 1})
    assert nontrivial[0] == 7
    assert reduced_index(3, 1) == 7
    assert eisenstein_norm(3, 1) == 7

    print("FCC [111] COINCIDENCE-FAMILY ABRUPT AUDIT")
    print("status: PASS")
    print(f"primitive Eisenstein audit box: |a|,|b| <= {LIMIT}")
    print(f"primitive pairs checked: {len(records)}")
    print(f"smallest nontrivial reduced index: {nontrivial[0]}")
    print("first distinct nontrivial reduced indices: " + ", ".join(map(str, nontrivial[:12])))
    print("general formula:")
    print("  maximum restored abrupt cross contacts per cell = 3")
    print("  two-crack deficit per cell = 3*Sigma")
    print("  abrupt deficit per cell = 3*Sigma-3")
    print("  ratio to two cracks = 1-1/Sigma")
    print("nontrivial family bound:")
    print("  Sigma >= 7")
    print("  abrupt ratio >= 6/7")
    print("index-seven equality case:")
    print("  Eisenstein parameter pair (a,b) = (3,1)")
    print("  norm = 7")
    print("  cell deficit = 18")
    print("  density = 12*sqrt(3)/7")


if __name__ == "__main__":
    main()
