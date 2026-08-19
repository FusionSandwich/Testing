import Mathlib
import Erdos1084.Phase1F3Theorem

namespace Erdos1084

/-! User-facing decimal form of the Phase-I theorem. -/

noncomputable section

namespace UnitSeparatedConfiguration

/-- `kpClean` is exactly the rational decimal `2.0465`. -/
theorem kpClean_eq_20465 : kpClean = (4093 : ℝ) / 2000 := by
  rfl

/-- Final formal theorem with the advertised rational decimal written explicitly. -/
theorem phase1_f3Nat_bound_20465 {n : ℕ}
    (h : Phase1F3Certificate n) :
    (f3Nat n : ℝ) <
      6 * (n : ℝ) - ((4093 : ℝ) / 2000) * h.geometry.x := by
  simpa [kpClean_eq_20465] using phase1_f3Nat_bound h

/-- Equivalent deficit statement with the explicit clean coefficient. -/
theorem phase1_f3Nat_deficit_bound_20465 {n : ℕ}
    (h : Phase1F3Certificate n) :
    ((4093 : ℝ) / 2000) * h.geometry.x <
      6 * (n : ℝ) - (f3Nat n : ℝ) := by
  simpa [kpClean_eq_20465] using phase1_f3Nat_deficit_bound h

end UnitSeparatedConfiguration

end

end Erdos1084
