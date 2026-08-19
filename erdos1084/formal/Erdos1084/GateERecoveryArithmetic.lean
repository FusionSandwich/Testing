import Mathlib

namespace Erdos1084

/-!
# Gate-E exact recovery arithmetic

This module checks the exact FCC leading constants, the triangular-layer mass-reservoir formulas,
the surface-order shell increments, and the finite tetrahedral-complex falsification values.
The geometric lattice-count and Gamma-convergence arguments remain theorem-level inputs in the
canonical mathematical dossier rather than hidden axioms.
-/

/-- Exact FCC Wulff-family point count polynomial. -/
def gateEFccNumber (t : ℤ) : ℤ :=
  128 * t ^ 3 + 60 * t ^ 2 + 12 * t + 1

/-- Exact FCC Wulff-family contact-deficit polynomial. -/
def gateEFccDeficit (t : ℤ) : ℤ :=
  192 * t ^ 2 + 60 * t + 6

/-- Exact point-count shell increment. -/
theorem gateE_fcc_number_increment (t : ℤ) :
    gateEFccNumber (t + 1) - gateEFccNumber t =
      384 * t ^ 2 + 504 * t + 200 := by
  simp [gateEFccNumber]
  ring

/-- Exact contact-deficit shell increment. -/
theorem gateE_fcc_deficit_increment (t : ℤ) :
    gateEFccDeficit (t + 1) - gateEFccDeficit t =
      384 * t + 252 := by
  simp [gateEFccDeficit]
  ring

/-- The FCC leading coefficient has cube `432`. -/
theorem gateE_fcc_leading_cube :
    (192 : ℤ) ^ 3 = 432 * (128 : ℤ) ^ 2 := by
  norm_num

/-- The closed-form coefficient cube identity `6^3 * 2 = 432`. -/
theorem gateE_fcc_closed_cube :
    (6 : ℤ) ^ 3 * 2 = 432 := by
  norm_num

/-- Number of sites in a triangular-lattice hexagon of radius `r`. -/
def gateETriHexNumber (r : ℤ) : ℤ :=
  3 * r ^ 2 + 3 * r + 1

/-- Number of in-plane nearest-neighbor edges in the same hexagon. -/
def gateETriHexEdges (r : ℤ) : ℤ :=
  9 * r ^ 2 + 3 * r

/-- Exact contact-deficit cost of one complete triangular-layer reservoir patch. -/
theorem gateE_tri_hex_deficit (r : ℤ) :
    3 * gateETriHexNumber r - gateETriHexEdges r = 6 * r + 3 := by
  simp [gateETriHexNumber, gateETriHexEdges]
  ring

/--
Abstract bound for a partial outer ring.

The complete inner hexagon has deficit `6r-3`; at most `6r` outer-ring sites are added, and each
site increases the deficit by at most two because it has at least one previous in-plane neighbor.
-/
theorem gateE_partial_ring_bound
    {r s d : ℝ}
    (hs : s ≤ 6 * r)
    (hd : d ≤ (6 * r - 3) + 2 * s) :
    d ≤ 18 * r - 3 := by
  linarith

/-- An `O(ε⁻¹)` mass-correction cost is negligible after surface scaling by `ε²`. -/
theorem gateE_scaled_mass_correction
    {ε C cost : ℝ}
    (hε : 0 < ε)
    (hcost : cost ≤ C / ε) :
    ε ^ 2 * cost ≤ C * ε := by
  have hεsq : 0 ≤ ε ^ 2 := sq_nonneg ε
  have hmul := mul_le_mul_of_nonneg_left hcost hεsq
  calc
    ε ^ 2 * cost ≤ ε ^ 2 * (C / ε) := hmul
    _ = C * ε := by
      field_simp [ne_of_gt hε]

/-- Leading coefficient cube for a face-glued tetrahedral complex. -/
def gateETetraComplexCube (q s : ℚ) : ℚ :=
  (243 / 2) * (2 * q - s) ^ 3 / q ^ 2

@[simp] theorem gateE_tetra_single :
    gateETetraComplexCube 1 0 = 972 := by
  norm_num [gateETetraComplexCube]

@[simp] theorem gateE_tetra_five_open :
    gateETetraComplexCube 5 4 = 26244 / 25 := by
  norm_num [gateETetraComplexCube]

@[simp] theorem gateE_tetra_five_closed :
    gateETetraComplexCube 5 5 = 1215 / 2 := by
  norm_num [gateETetraComplexCube]

@[simp] theorem gateE_tetra_twenty_cut_two :
    gateETetraComplexCube 20 28 = 13122 / 25 := by
  norm_num [gateETetraComplexCube]

@[simp] theorem gateE_tetra_twenty_cut_one :
    gateETetraComplexCube 20 29 = 323433 / 800 := by
  norm_num [gateETetraComplexCube]

@[simp] theorem gateE_tetra_twenty_formal_closed :
    gateETetraComplexCube 20 30 = 1215 / 4 := by
  norm_num [gateETetraComplexCube]

/-- Two cut faces keep the twenty-tetrahedron model above FCC. -/
theorem gateE_tetra_twenty_cut_two_above_fcc :
    (432 : ℚ) < gateETetraComplexCube 20 28 := by
  norm_num [gateETetraComplexCube]

/-- One formal cut face would put the face-count model below FCC. -/
theorem gateE_tetra_twenty_cut_one_below_fcc :
    gateETetraComplexCube 20 29 < (432 : ℚ) := by
  norm_num [gateETetraComplexCube]

end Erdos1084
