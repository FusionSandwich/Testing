import Mathlib

namespace Erdos1084

/-!
# Arithmetic for coherent-twin platelet arrays

The geometric dossier proves that a fixed-thickness platelet has rim cost
proportional to its footprint perimeter, and that a transverse boundary section
is controlled by the same lateral area.  This module checks the scaling and
coverage consequences used in the branching audit.
-/

/--
If `N` footprints of scale `ell` occupy total area at most `T²` and the total rim
cost is at most `C*N*ell`, then the cost is at most `C*T²/ell`.
-/
theorem plateletArray_cost_le_area_div_scale
    {N ell T C cost : ℝ}
    (hell : 0 < ell)
    (hC : 0 ≤ C)
    (hpacking : N * ell ^ 2 ≤ T ^ 2)
    (hcost : cost ≤ C * N * ell) :
    cost ≤ C * T ^ 2 / ell := by
  have hfactor : 0 ≤ C / ell :=
    div_nonneg hC (le_of_lt hell)
  have hmul := mul_le_mul_of_nonneg_left hpacking hfactor
  calc
    cost ≤ C * N * ell := hcost
    _ = (C / ell) * (N * ell ^ 2) := by
      field_simp [ne_of_gt hell]
    _ ≤ (C / ell) * T ^ 2 := hmul
    _ = C * T ^ 2 / ell := by ring

/-- Surface-scaled platelet rim cost is at most `C/ell`. -/
theorem plateletArray_surfaceDensity_le_invScale
    {N ell T C cost : ℝ}
    (hell : 0 < ell)
    (hT : 0 < T)
    (hC : 0 ≤ C)
    (hpacking : N * ell ^ 2 ≤ T ^ 2)
    (hcost : cost ≤ C * N * ell) :
    cost / T ^ 2 ≤ C / ell := by
  have hcost' := plateletArray_cost_le_area_div_scale
    hell hC hpacking hcost
  have hT2 : 0 < T ^ 2 := sq_pos_of_pos hT
  apply (div_le_iff₀ hT2).2
  calc
    cost ≤ C * T ^ 2 / ell := hcost'
    _ = (C / ell) * T ^ 2 := by ring

/-- The common factor-four square-perimeter version. -/
theorem squarePlateletArray_surfaceDensity
    {N ell T C cost : ℝ}
    (hell : 0 < ell)
    (hT : 0 < T)
    (hC : 0 ≤ C)
    (hpacking : N * ell ^ 2 ≤ T ^ 2)
    (hcost : cost ≤ 4 * C * N * ell) :
    cost / T ^ 2 ≤ 4 * C / ell := by
  have h4C : 0 ≤ 4 * C := by positivity
  simpa [mul_assoc] using
    plateletArray_surfaceDensity_le_invScale
      (N := N) (ell := ell) (T := T) (C := 4 * C) (cost := cost)
      hell hT h4C hpacking (by simpa [mul_assoc] using hcost)

/--
Abstract form of the transverse-section inequality: if covered area is at most
`lateral/(2*s)`, then lateral area is at least `2*s*covered`.
-/
theorem transverseCoverage_forces_lateralArea
    {covered lateral s : ℝ}
    (hs : 0 < s)
    (hcoverage : covered ≤ lateral / (2 * s)) :
    2 * s * covered ≤ lateral := by
  have hden : 0 < 2 * s := by positivity
  have hraw : covered * (2 * s) ≤ lateral :=
    (le_div_iff₀ hden).mp hcoverage
  simpa [mul_comm, mul_left_comm, mul_assoc] using hraw

/-- Area-order coverage at a fixed transverse angle forces area-order lateral wall. -/
theorem macroscopicCoverage_forces_areaOrder_lateral
    {covered lateral s c T : ℝ}
    (hs : 0 < s)
    (hcovered : c * T ^ 2 ≤ covered)
    (hcoverage : covered ≤ lateral / (2 * s)) :
    2 * s * c * T ^ 2 ≤ lateral := by
  have hfirst : 2 * s * covered ≤ lateral :=
    transverseCoverage_forces_lateralArea hs hcoverage
  have hfactor : 0 ≤ 2 * s := by positivity
  have hmul := mul_le_mul_of_nonneg_left hcovered hfactor
  nlinarith

/-- If the active angle sine is bounded below, vanishing lateral density forbids positive coverage. -/
theorem coverageDensity_le_lateralDensity
    {covered lateral s₀ T : ℝ}
    (hs₀ : 0 < s₀)
    (hT : 0 < T)
    (hcoverage : covered ≤ lateral / (2 * s₀)) :
    covered / T ^ 2 ≤ lateral / T ^ 2 / (2 * s₀) := by
  have hT2 : 0 < T ^ 2 := sq_pos_of_pos hT
  have hdiv := div_le_div_of_nonneg_right hcoverage (le_of_lt hT2)
  calc
    covered / T ^ 2 ≤ (lateral / (2 * s₀)) / T ^ 2 := hdiv
    _ = lateral / T ^ 2 / (2 * s₀) := by
      field_simp [ne_of_gt hs₀, ne_of_gt hT]

end Erdos1084
