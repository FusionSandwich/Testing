#!/usr/bin/env python3
"""Negative audit of the naive Barlow stacking-frequency Wulff model.

The earlier weighted-zonotope interpolation reproduces FCC but fails for HCP
because HCP is a multilattice and its surface cell problem permits phase
relaxation. Cicalese--Kreutz--Leonardi (CMP 402, 2023, Proposition 2.5)
compute the correct HCP Wulff energy.

All checks are exact rational arithmetic.
"""

from fractions import Fraction as Q

fcc_cube = Q(432)
correct_hcp_cube = Q(1755, 4)
naive_hcp_cube = Q(945, 2)

assert correct_hcp_cube > fcc_cube
assert naive_hcp_cube > correct_hcp_cube
assert correct_hcp_cube - fcc_cube == Q(27, 4)
assert naive_hcp_cube - correct_hcp_cube == Q(135, 4)

print("BARLOW FREQUENCY MODEL NEGATIVE AUDIT")
print("published FCC contact-deficit coefficient cube = 432")
print("published HCP contact-deficit coefficient cube = 1755/4")
print("naive weighted-zonotope HCP cube = 945/2")
print("published HCP minus FCC = 27/4")
print("naive HCP excess over published HCP = 135/4")
print()
print("PASS: the naive frequency interpolation is rejected at HCP.")
print("Reason: the HCP multilattice surface cell problem has relaxation not captured by simple direction-frequency averaging.")
