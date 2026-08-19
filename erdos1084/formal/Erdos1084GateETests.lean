import Erdos1084

open Erdos1084

/-! Smoke tests for the Gate-E exact-mass recovery arithmetic. -/

example (t : ℤ) :
    gateEFccNumber (t + 1) - gateEFccNumber t =
      384 * t ^ 2 + 504 * t + 200 :=
  gateE_fcc_number_increment t

example (t : ℤ) :
    gateEFccDeficit (t + 1) - gateEFccDeficit t =
      384 * t + 252 :=
  gateE_fcc_deficit_increment t

example : (192 : ℤ) ^ 3 = 432 * (128 : ℤ) ^ 2 :=
  gateE_fcc_leading_cube

example (r : ℤ) :
    3 * gateETriHexNumber r - gateETriHexEdges r = 6 * r + 3 :=
  gateE_tri_hex_deficit r

example
    {r s d : ℝ}
    (hr : 1 ≤ r)
    (hs0 : 0 ≤ s)
    (hs : s ≤ 6 * r)
    (hd : d ≤ (6 * r - 3) + 2 * s) :
    d ≤ 18 * r - 3 :=
  gateE_partial_ring_bound hr hs0 hs hd

example
    {ε C cost : ℝ}
    (hε : 0 < ε)
    (hC : 0 ≤ C)
    (hcost : cost ≤ C / ε) :
    ε ^ 2 * cost ≤ C * ε :=
  gateE_scaled_mass_correction hε hC hcost

example : gateETetraComplexCube 5 5 = 1215 / 2 :=
  gateE_tetra_five_closed

example : (432 : ℚ) < gateETetraComplexCube 20 28 :=
  gateE_tetra_twenty_cut_two_above_fcc

example : gateETetraComplexCube 20 29 < (432 : ℚ) :=
  gateE_tetra_twenty_cut_one_below_fcc

example {a : ℕ → ℝ} {c : ℝ}
    (h : MatchingSurfaceBounds a c) :
    HasRealSequenceLimit a c :=
  hasRealSequenceLimit_of_matchingSurfaceBounds h
