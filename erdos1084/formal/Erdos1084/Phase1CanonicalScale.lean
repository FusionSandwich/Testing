import Mathlib
import Erdos1084.Phase1MainTheorem
import Erdos1084.PowerScaleUniqueness

namespace Erdos1084

/-!
# Canonical `n^(2/3)` scale and final Phase-I statement

The project represents `n^(2/3)` by the positive real cube root of `n^2`.  This avoids fragile
real-exponent rewriting while giving an exact canonical term in the final theorem.
-/

noncomputable section

/-- Canonical real `n^(2/3)` scale. -/
def phase1TwoThirdsScale (n : ℕ) : ℝ :=
  Real.cbrt ((n : ℝ) ^ 2)

/-- For positive `n`, the canonical scale satisfies `KeplerPowerScale`. -/
theorem phase1TwoThirdsScale_power
    {n : ℕ} (hn : 0 < n) :
    KeplerPowerScale (n : ℝ) (phase1TwoThirdsScale n) := by
  refine ⟨?_, ?_, ?_⟩
  · exact_mod_cast hn
  · exact Real.cbrt_nonneg (sq_nonneg (n : ℝ))
  · simpa [phase1TwoThirdsScale] using
      Real.cbrt_cubed ((n : ℝ) ^ 2)

/-- Every admissible Phase-I power witness equals the canonical cube-root scale. -/
theorem KeplerPowerScale.eq_phase1TwoThirdsScale
    {n : ℕ} {x : ℝ}
    (hx : KeplerPowerScale (n : ℝ) x) :
    x = phase1TwoThirdsScale n := by
  have hnreal : 0 < (n : ℝ) := hx.x_pos.trans_le (le_refl _)
  have hn : 0 < n := by exact_mod_cast hnreal
  exact hx.unique (phase1TwoThirdsScale_power hn)

/-- Final Phase-I theorem with the canonical `n^(2/3)` term. -/
theorem phase1_main_canonical
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - kpClean * phase1TwoThirdsScale n := by
  obtain ⟨x, hx, hbound⟩ := phase1_main_relational geometry hn hmax
  rw [hx.eq_phase1TwoThirdsScale] at hbound
  exact hbound

/-- Decimal presentation of the final canonical Phase-I theorem. -/
theorem phase1_main_canonical_decimal
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n := by
  simpa [kpClean_eq_20465] using
    phase1_main_canonical geometry hn hmax

end

end Erdos1084
