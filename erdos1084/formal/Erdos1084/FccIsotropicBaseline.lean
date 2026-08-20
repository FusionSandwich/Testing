import Mathlib

namespace Erdos1084

/-!
# Sharp isotropic baseline of the FCC surface tension

After ordering the coordinate magnitudes as `M ≥ m ≥ l ≥ 0`, the FCC surface
tension is `2*M+m`. This module checks the sharp squared lower bound and the
continuum coefficient cube `54*pi*sqrt(3)`. The absolute-value sorting identity
is recorded in the human-readable selector proof.
-/

/-- FCC tension after sorting coordinate magnitudes. -/
def fccOrderedTension (M m : ℝ) : ℝ := 2 * M + m

/-- Exact nonnegative decomposition behind the sharp `sqrt(3)` lower bound. -/
theorem fccOrderedTension_square_difference
    (M m l : ℝ) :
    fccOrderedTension M m ^ 2 - 3 * (M ^ 2 + m ^ 2 + l ^ 2) =
      (M - m) ^ 2 +
      6 * (M - m) * (m - l) +
      6 * (M - m) * l +
      3 * (m - l) ^ 2 +
      6 * (m - l) * l := by
  unfold fccOrderedTension
  ring

/-- For ordered nonnegative magnitudes, the FCC tension is at least `sqrt(3)` times norm. -/
theorem fccOrderedTension_square_lower
    {M m l : ℝ}
    (hl : 0 ≤ l) (hlm : l ≤ m) (hmM : m ≤ M) :
    3 * (M ^ 2 + m ^ 2 + l ^ 2) ≤ fccOrderedTension M m ^ 2 := by
  have hMm : 0 ≤ M - m := sub_nonneg.mpr hmM
  have hml : 0 ≤ m - l := sub_nonneg.mpr hlm
  have h1 : 0 ≤ (M - m) ^ 2 := sq_nonneg _
  have h2 : 0 ≤ 6 * (M - m) * (m - l) := by positivity
  have h3 : 0 ≤ 6 * (M - m) * l := by positivity
  have h4 : 0 ≤ 3 * (m - l) ^ 2 := by positivity
  have h5 : 0 ≤ 6 * (m - l) * l := by positivity
  rw [← sub_nonneg]
  rw [fccOrderedTension_square_difference]
  positivity

/-- Equality in the ordered square bound forces all three magnitudes to agree. -/
theorem fccOrderedTension_square_eq_iff
    {M m l : ℝ}
    (hl : 0 ≤ l) (hlm : l ≤ m) (hmM : m ≤ M) :
    fccOrderedTension M m ^ 2 = 3 * (M ^ 2 + m ^ 2 + l ^ 2) ↔
      M = m ∧ m = l := by
  constructor
  · intro heq
    have hMm : 0 ≤ M - m := sub_nonneg.mpr hmM
    have hml : 0 ≤ m - l := sub_nonneg.mpr hlm
    have hsum :
        (M - m) ^ 2 +
          6 * (M - m) * (m - l) +
          6 * (M - m) * l +
          3 * (m - l) ^ 2 +
          6 * (m - l) * l = 0 := by
      rw [← fccOrderedTension_square_difference]
      linarith
    have hsquares : (M - m) ^ 2 + 3 * (m - l) ^ 2 ≤ 0 := by
      have hcross1 : 0 ≤ 6 * (M - m) * (m - l) := by positivity
      have hcross2 : 0 ≤ 6 * (M - m) * l := by positivity
      have hcross3 : 0 ≤ 6 * (m - l) * l := by positivity
      linarith
    have hM : M - m = 0 := by nlinarith [sq_nonneg (M - m)]
    have hm : m - l = 0 := by nlinarith [sq_nonneg (m - l)]
    exact ⟨sub_eq_zero.mp hM, sub_eq_zero.mp hm⟩
  · rintro ⟨rfl, rfl⟩
    unfold fccOrderedTension
    ring

/-- The exact isotropic continuum coefficient cube. -/
noncomputable def fccIsotropicCoeffCube : ℝ := 54 * Real.pi * Real.sqrt 3

/-- The isotropic baseline cube is positive. -/
theorem fccIsotropicCoeffCube_pos : 0 < fccIsotropicCoeffCube := by
  have hs : 0 < Real.sqrt (3 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  exact mul_pos (mul_pos (by norm_num) Real.pi_pos) hs

/-- The isotropic baseline is strictly below the homogeneous FCC cube `432`. -/
theorem fccIsotropicCoeffCube_lt_fcc : fccIsotropicCoeffCube < 432 := by
  have hs0 : 0 ≤ Real.sqrt (3 : ℝ) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by norm_num
  have hs : Real.sqrt (3 : ℝ) < 2 := by nlinarith
  have hp : Real.pi < 4 := Real.pi_lt_four
  have hprod : Real.pi * Real.sqrt 3 < 8 := by
    calc
      Real.pi * Real.sqrt 3 < 4 * Real.sqrt 3 :=
        mul_lt_mul_of_pos_right hp (Real.sqrt_pos.2 (by norm_num))
      _ < 4 * 2 := mul_lt_mul_of_pos_left hs (by norm_num)
      _ = 8 := by norm_num
  unfold fccIsotropicCoeffCube
  nlinarith

end Erdos1084
