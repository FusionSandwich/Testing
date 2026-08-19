#!/usr/bin/env python3
"""Exact leading-order audit for face-glued FCC tetrahedral grain complexes."""

from __future__ import annotations
from fractions import Fraction as Q

FCC_CUBE = Q(432)


def coefficient_cube(q: int, shared_faces: int) -> Q:
    if q <= 0:
        raise ValueError("q must be positive")
    if not 0 <= shared_faces <= 2 * q:
        raise ValueError("invalid shared-face count")
    return Q(243, 2) * Q((2 * q - shared_faces) ** 3, q * q)


records = [
    (1, 0, "single tetrahedron"),
    (2, 1, "coherent bipyramid"),
    (5, 4, "open five-tetrahedron fan"),
    (5, 5, "hypothetical closed five-cycle"),
    (20, 28, "twenty-grain complex with two cut faces"),
    (20, 29, "hypothetical twenty-grain complex with one cut face"),
    (20, 30, "formally fully glued icosahedral adjacency"),
]

assert coefficient_cube(5, 4) > FCC_CUBE
assert coefficient_cube(5, 5) > FCC_CUBE
assert coefficient_cube(20, 28) > FCC_CUBE
assert coefficient_cube(20, 29) < FCC_CUBE
assert coefficient_cube(20, 30) < FCC_CUBE
assert [s for s in range(31) if coefficient_cube(20, s) < FCC_CUBE] == [29, 30]

print("TETRAHEDRAL POLYCRYSTAL FALSIFICATION CERTIFICATE")
print("status: PASS")
print("FCC coefficient cube = 432")
print()
for q, shared, label in records:
    cube = coefficient_cube(q, shared)
    comparison = "below" if cube < FCC_CUBE else "equal" if cube == FCC_CUBE else "above"
    print(f"{label}: q={q}, shared={shared}, cube={cube} ({comparison} FCC)")
print()
print("twenty-tetrahedron threshold:")
print("  shared faces beating FCC = [29, 30]")
print("  two or more area-order cut faces force the model above FCC")
print()
print("Claim boundary:")
print("the fully glued icosahedral adjacency is geometrically incompatible for regular tetrahedra;")
print("this calculation does not replace the orientation-interface cell problem.")
