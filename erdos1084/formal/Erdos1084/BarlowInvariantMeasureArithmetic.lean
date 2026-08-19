import Mathlib

namespace Erdos1084

/-!
# Gate B invariant-measure arithmetic

The measure-theoretic theorem sends a shift-invariant stacking measure to its one-symbol marginal
`p ∈ [0,1]`.  This module certifies the exact real-frequency volume and coefficient formulas,
the FCC equality case, the raw directionwise-infimum counterexample, and the convex-envelope
volume arithmetic.

The density of periodic orbit measures and the periodized-prefix seam theorem are proved in the
canonical mathematical dossier.  They are not hidden as Lean axioms here.
-/

/-- Physical Wulff volume for a stationary stacking marginal `p`. -/
def invariantBarlowWulffVolume (p : ℝ) : ℝ :=
  32 + 2 * p * (1 - p)

/-- Cube of the stationary particle-number Wulff coefficient. -/
def invariantBarlowCoefficientCube (p : ℝ) : ℝ :=
  432 + 27 * p * (1 - p)

/-- Exact conversion from physical volume to coefficient cube. -/
theorem invariantBarlow_cube_from_volume (p : ℝ) :
    invariantBarlowCoefficientCube p =
      (27 / 2 : ℝ) * invariantBarlowWulffVolume p := by
  unfold invariantBarlowCoefficientCube invariantBarlowWulffVolume
  ring

/-- Every invariant-measure marginal has coefficient at least FCC. -/
theorem invariantBarlow_cube_ge_fcc
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    (432 : ℝ) ≤ invariantBarlowCoefficientCube p := by
  have hprod : 0 ≤ p * (1 - p) :=
    mul_nonneg hp0 (sub_nonneg.mpr hp1)
  unfold invariantBarlowCoefficientCube
  nlinarith

/-- A nonconstant marginal has a strict coefficient gap. -/
theorem invariantBarlow_cube_gt_fcc
    {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    (432 : ℝ) < invariantBarlowCoefficientCube p := by
  have hprod : 0 < p * (1 - p) :=
    mul_pos hp0 (sub_pos.mpr hp1)
  unfold invariantBarlowCoefficientCube
  nlinarith

/-- Equality occurs only at the two constant-chirality marginals. -/
theorem invariantBarlow_cube_eq_fcc_iff
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    invariantBarlowCoefficientCube p = 432 ↔ p = 0 ∨ p = 1 := by
  unfold invariantBarlowCoefficientCube
  constructor
  · intro h
    have hprod : p * (1 - p) = 0 := by nlinarith
    rcases mul_eq_zero.mp hprod with hp | hp
    · exact Or.inl hp
    · exact Or.inr (by linarith)
  · intro h
    rcases h with rfl | rfl <;> norm_num

/-- The real-frequency coefficient formula is continuous. -/
theorem invariantBarlowCoefficientCube_continuous :
    Continuous invariantBarlowCoefficientCube := by
  unfold invariantBarlowCoefficientCube
  fun_prop

/-- Positive part on rationals. -/
def gateBPositivePart (x : ℚ) : ℚ := max 0 x

/--
Raw directionwise-infimum support after reducing a horizontal direction to
`H = h_Z`, `delta = h_T - h_{-T}`, and vertical component `t`.
-/
def gateBRawSupport (H delta t : ℚ) : ℚ :=
  H + max ((3 / 2 : ℚ) * |t|)
    (H / 2 + gateBPositivePart (|t| - |delta|) / 2)

/-- Support of the lower-semicontinuous convex envelope. -/
def gateBConvexEnvelopeSupport (H t : ℚ) : ℚ :=
  H + max (H / 2) ((3 / 2 : ℚ) * |t|)

/-- Exact non-subadditivity certificate for the raw infimum. -/
theorem gateB_raw_non_subadditivity_values :
    gateBRawSupport 3 1 1 = 9 / 2 ∧
    gateBRawSupport 3 (-1) 1 = 9 / 2 ∧
    gateBRawSupport 6 0 2 = 10 := by
  norm_num [gateBRawSupport, gateBPositivePart, abs_of_nonneg, abs_of_pos,
    abs_of_neg]

/-- The raw infimum violates the required support-function subadditivity. -/
theorem gateB_raw_non_subadditive :
    gateBRawSupport 6 0 2 >
      gateBRawSupport 3 1 1 + gateBRawSupport 3 (-1) 1 := by
  norm_num [gateBRawSupport, gateBPositivePart, abs_of_nonneg, abs_of_pos,
    abs_of_neg]

/-- The convex envelope is strictly below the raw infimum in a rational test direction. -/
theorem gateB_convex_envelope_strict_test :
    gateBConvexEnvelopeSupport 2 (1 / 4) = 3 ∧
    gateBRawSupport 2 0 (1 / 4) = 25 / 8 := by
  norm_num [gateBConvexEnvelopeSupport, gateBRawSupport, gateBPositivePart,
    abs_of_nonneg, abs_of_pos]

/-- Rationally scaled common-body volume. -/
def gateBCommonScaledVolume : ℚ := 57 / 4

/-- Physical common-body volume. -/
def gateBCommonPhysicalVolume : ℚ := 57 / 2

/-- Cube of the convex-envelope Wulff coefficient. -/
def gateBCommonCoefficientCube : ℚ := 1539 / 4

/-- Exact determinant and coefficient conversion. -/
theorem gateB_common_body_arithmetic :
    gateBCommonPhysicalVolume = 2 * gateBCommonScaledVolume ∧
    gateBCommonCoefficientCube =
      (27 / 2 : ℚ) * gateBCommonPhysicalVolume ∧
    gateBCommonCoefficientCube < 432 := by
  norm_num [gateBCommonScaledVolume, gateBCommonPhysicalVolume,
    gateBCommonCoefficientCube]

end Erdos1084
