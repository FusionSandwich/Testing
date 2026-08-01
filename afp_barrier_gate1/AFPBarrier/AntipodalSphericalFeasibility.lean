import AFPBarrier.LocalSphericalFeasibility
import Mathlib.Tactic

/-!
# Antipodal spherical normal budgets

Antipodal neighbors have no tangent direction and contribute normal loss two.
This module records the scalar algebra needed to keep them separate from the
non-antipodal formulas, which divide by `sin(theta)`.
-/

namespace AFPBarrier

/-- The non-antipodal contribution to the normal budget after setting
`b_j = a_j sin(theta_j)`. -/
def nonAntipodalNormalBudget {ι : Type*} [Fintype ι]
    (b loss sinTheta : ι → ℝ) : ℝ :=
  Finset.univ.sum (fun j => b j * loss j / sinTheta j)

/-- The antipodal total rate required after the non-antipodal part consumes
normal budget `D`. -/
def requiredAntipodalTotalRate (D : ℝ) : ℝ :=
  1 - D / 2

/-- The mixed normal equation is exactly the remaining-budget formula. -/
theorem mixed_normal_budget_iff
    (D antipodalTotal : ℝ) :
    D + 2 * antipodalTotal = 2 ↔
      antipodalTotal = requiredAntipodalTotalRate D := by
  unfold requiredAntipodalTotalRate
  constructor <;> intro h <;> linarith

/-- A nonnegative antipodal budget exists exactly when the non-antipodal
normal contribution does not exceed two. -/
theorem requiredAntipodalTotalRate_nonneg_iff (D : ℝ) :
    0 ≤ requiredAntipodalTotalRate D ↔ D ≤ 2 := by
  unfold requiredAntipodalTotalRate
  constructor <;> intro h <;> linarith

/-- A strictly positive antipodal budget exists exactly when the
non-antipodal normal contribution is strictly below two. -/
theorem requiredAntipodalTotalRate_pos_iff (D : ℝ) :
    0 < requiredAntipodalTotalRate D ↔ D < 2 := by
  unfold requiredAntipodalTotalRate
  constructor <;> intro h <;> linarith

/-- With only antipodal neighbors, exact normal loss is equivalent to total
antipodal rate one. -/
theorem only_antipodal_normal_iff (antipodalTotal : ℝ) :
    2 * antipodalTotal = 2 ↔ antipodalTotal = 1 := by
  constructor <;> intro h <;> linarith

/-- Once a positive tangent-dependence normal functional `D` is selected, the
normal equation fixes the common scale uniquely. -/
theorem spherical_commonScale_eq
    (D commonScale : ℝ)
    (hD : 0 < D)
    (hbalance : commonScale * D = 2) :
    commonScale = 2 / D := by
  exact (eq_div_iff (ne_of_gt hD)).2 hbalance

/-- The uniquely fixed common scale is positive. -/
theorem spherical_commonScale_pos
    (D commonScale : ℝ)
    (hD : 0 < D)
    (hbalance : commonScale * D = 2) :
    0 < commonScale := by
  rw [spherical_commonScale_eq D commonScale hD hbalance]
  exact div_pos (by norm_num) hD

end AFPBarrier
