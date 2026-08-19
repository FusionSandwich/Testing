import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Uniqueness of the positive `n^(2/3)` scale

`KeplerPowerScale n x` records `n>0`, `x>=0`, and `x^3=n^2`.  This module proves that the scale is
unique, so the existential `x` in the relational Phase-I theorem is exactly the positive real
cube root of `n^2` and cannot encode a normalization ambiguity.
-/

noncomputable section

/-- Two positive cube-root witnesses for the same `n²` agree. -/
theorem KeplerPowerScale.unique
    {n x y : ℝ}
    (hx : KeplerPowerScale n x)
    (hy : KeplerPowerScale n y) :
    x = y := by
  rcases hx with ⟨hnx, hx0, hx3⟩
  rcases hy with ⟨hny, hy0, hy3⟩
  have hfactor :
      (x - y) * (x ^ 2 + x * y + y ^ 2) = 0 := by
    calc
      (x - y) * (x ^ 2 + x * y + y ^ 2) = x ^ 3 - y ^ 3 := by ring
      _ = 0 := by rw [hx3, hy3]; ring
  have hxpos : 0 < x := by
    by_contra hnot
    have hxle : x ≤ 0 := le_of_not_gt hnot
    have hxzero : x = 0 := le_antisymm hxle hx0
    rw [hxzero] at hx3
    nlinarith
  have hsumpos : 0 < x ^ 2 + x * y + y ^ 2 := by
    have hx2 : 0 < x ^ 2 := sq_pos_of_pos hxpos
    have hxy : 0 ≤ x * y := mul_nonneg hx0 hy0
    have hy2 : 0 ≤ y ^ 2 := sq_nonneg y
    nlinarith
  rcases mul_eq_zero.mp hfactor with hxy | hsum
  · linarith
  · exact (ne_of_gt hsumpos hsum).elim

end

end Erdos1084
