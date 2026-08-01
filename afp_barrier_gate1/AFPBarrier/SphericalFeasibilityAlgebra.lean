import AFPBarrier.LocalSphericalFeasibility
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Finite algebra for spherical feasibility with antipodes

This module extends the constructive row-rescaling checkpoint without encoding
antipodal edges as tangent directions.  The convex-hull and relative-interior
theorems are proved in the accompanying ordinary-mathematics theorem document;
here we formalize the finite scalar consequences used by those proofs.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι]

/-- Normal spend of a non-antipodal tangent dependence.  The quotient is used
only for indices whose sine is assumed strictly positive. -/
noncomputable def tangentNormalScale
    (b sinTheta loss : ι → ℝ) : ℝ :=
  Finset.univ.sum (fun j => b j * loss j / sinTheta j)

/-- A nonzero nonnegative dependence has strictly positive normal scale when
all non-antipodal angular factors are strictly positive. -/
theorem tangentNormalScale_pos
    (b sinTheta loss : ι → ℝ)
    (hb : ∀ j, 0 ≤ b j)
    (hbne : ∃ j, 0 < b j)
    (hsin : ∀ j, 0 < sinTheta j)
    (hloss : ∀ j, 0 < loss j) :
    0 < tangentNormalScale b sinTheta loss := by
  unfold tangentNormalScale
  rcases hbne with ⟨j0, hj0⟩
  apply Finset.sum_pos'
  · intro j hj
    exact div_nonneg
      (mul_nonneg (hb j) (le_of_lt (hloss j)))
      (le_of_lt (hsin j))
  · refine ⟨j0, Finset.mem_univ j0, ?_⟩
    exact div_pos (mul_pos hj0 (hloss j0)) (hsin j0)

/-- The scalar normal equation fixes the common multiplier of a chosen
normalized tangent dependence. -/
theorem commonScale_eq_two_div
    (Q c : ℝ) (hQ : Q ≠ 0) (hbalance : c * Q = 2) :
    c = 2 / Q := by
  exact (eq_div_iff hQ).2 hbalance

/-- The uniquely fixed common multiplier is positive when the normal scale is
positive. -/
theorem commonScale_pos
    (Q c : ℝ) (hQ : 0 < Q) (hbalance : c * Q = 2) :
    0 < c := by
  rw [commonScale_eq_two_div Q c (ne_of_gt hQ) hbalance]
  exact div_pos (by norm_num) hQ

/-- The checkpoint row formula is the common multiplier `2 / normalScale`
times `b_j / sin(theta_j)`. -/
theorem scaledSphericalRowRate_eq_commonScale
    (b sinTheta : ι → ℝ) (normalScale : ℝ)
    (hsin : ∀ j, sinTheta j ≠ 0)
    (hscale : normalScale ≠ 0) (j : ι) :
    scaledSphericalRowRate b sinTheta normalScale j
      = (2 / normalScale) * (b j / sinTheta j) := by
  unfold scaledSphericalRowRate
  field_simp [hsin j, hscale]

/-- Total antipodal rate left after a non-antipodal block spends `D` units of
normal loss.  Antipodes themselves are never divided by a sine. -/
noncomputable def antipodalTotalRate (D : ℝ) : ℝ :=
  1 - D / 2

/-- The mixed normal budget is identically reconstructed from the remaining
antipodal total rate. -/
theorem mixedNormalBudget_identity (D : ℝ) :
    D + 2 * antipodalTotalRate D = 2 := by
  unfold antipodalTotalRate
  ring

/-- Any solution of `D + 2 t = 2` has the stated antipodal total rate. -/
theorem antipodalTotalRate_eq_of_mixedNormalBudget
    (D t : ℝ) (hbudget : D + 2 * t = 2) :
    t = antipodalTotalRate D := by
  unfold antipodalTotalRate
  linarith

/-- Nonnegative antipodal budget is equivalent to spending at most two units
on the non-antipodal block. -/
theorem antipodalTotalRate_nonneg_iff (D : ℝ) :
    0 ≤ antipodalTotalRate D ↔ D ≤ 2 := by
  unfold antipodalTotalRate
  constructor <;> intro h <;> linarith

/-- Strictly positive antipodal budget is equivalent to spending strictly less
than two units on the non-antipodal block. -/
theorem antipodalTotalRate_pos_iff (D : ℝ) :
    0 < antipodalTotalRate D ↔ D < 2 := by
  unfold antipodalTotalRate
  constructor <;> intro h <;> linarith

/-- In an antipodal-only row, the normal equation is exactly that the
antipodal rates sum to one. -/
theorem antipodalOnly_normalBalance_iff
    (a : ι → ℝ) :
    Finset.univ.sum (fun j => 2 * a j) = 2 ↔
      Finset.univ.sum a = 1 := by
  rw [← Finset.mul_sum]
  constructor <;> intro h <;> linarith

end AFPBarrier
