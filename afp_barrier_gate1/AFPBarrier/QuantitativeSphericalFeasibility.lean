import AFPBarrier.SphericalFeasibilityAlgebra
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Quantitative finite loss-window bounds

The geometric margin and perturbation constants are proved in the ordinary
stage theorem.  This module formalizes the finite inequalities that turn a
normal-loss window into explicit outgoing-rate bounds.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι]

/-- Total outgoing rate of one finite row. -/
def sphericalOutgoingRate (a : ι → ℝ) : ℝ :=
  Finset.univ.sum a

/-- Nonnegative coefficients have nonnegative outgoing rate. -/
theorem sphericalOutgoingRate_nonneg
    (a : ι → ℝ) (ha : ∀ j, 0 ≤ a j) :
    0 ≤ sphericalOutgoingRate a := by
  unfold sphericalOutgoingRate
  exact Finset.sum_nonneg (fun j hj => ha j)

/-- If every edge loss is at most `Lmax`, the normal equation gives the
cross-multiplied lower outgoing-rate bound `2 ≤ Lmax * R`. -/
theorem normalBalance_lossUpper_crossBound
    (a loss : ι → ℝ) (Lmax : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hloss : ∀ j, loss j ≤ Lmax)
    (hbalance : Finset.univ.sum (fun j => a j * loss j) = 2) :
    2 ≤ Lmax * sphericalOutgoingRate a := by
  have hsum :
      Finset.univ.sum (fun j => a j * loss j)
        ≤ Finset.univ.sum (fun j => a j * Lmax) := by
    apply Finset.sum_le_sum
    intro j hj
    exact mul_le_mul_of_nonneg_left (hloss j) (ha j)
  have hfactor :
      Finset.univ.sum (fun j => a j * Lmax)
        = Lmax * sphericalOutgoingRate a := by
    unfold sphericalOutgoingRate
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    exact mul_comm (a j) Lmax
  rw [hbalance, hfactor] at hsum
  exact hsum

/-- If every edge loss is at least `Lmin`, the normal equation gives the
cross-multiplied upper outgoing-rate bound `Lmin * R ≤ 2`. -/
theorem normalBalance_lossLower_crossBound
    (a loss : ι → ℝ) (Lmin : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hloss : ∀ j, Lmin ≤ loss j)
    (hbalance : Finset.univ.sum (fun j => a j * loss j) = 2) :
    Lmin * sphericalOutgoingRate a ≤ 2 := by
  have hsum :
      Finset.univ.sum (fun j => a j * Lmin)
        ≤ Finset.univ.sum (fun j => a j * loss j) := by
    apply Finset.sum_le_sum
    intro j hj
    exact mul_le_mul_of_nonneg_left (hloss j) (ha j)
  have hfactor :
      Finset.univ.sum (fun j => a j * Lmin)
        = Lmin * sphericalOutgoingRate a := by
    unfold sphericalOutgoingRate
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    exact mul_comm (a j) Lmin
  rw [hfactor, hbalance] at hsum
  exact hsum

/-- Divided lower outgoing-rate bound. -/
theorem normalBalance_outgoingRate_lower
    (a loss : ι → ℝ) (Lmax : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hloss : ∀ j, loss j ≤ Lmax)
    (hLmax : 0 < Lmax)
    (hbalance : Finset.univ.sum (fun j => a j * loss j) = 2) :
    2 / Lmax ≤ sphericalOutgoingRate a := by
  apply (div_le_iff₀ hLmax).2
  have hcross := normalBalance_lossUpper_crossBound
    (a := a) (loss := loss) (Lmax := Lmax) ha hloss hbalance
  nlinarith

/-- Divided upper outgoing-rate bound. -/
theorem normalBalance_outgoingRate_upper
    (a loss : ι → ℝ) (Lmin : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hloss : ∀ j, Lmin ≤ loss j)
    (hLmin : 0 < Lmin)
    (hbalance : Finset.univ.sum (fun j => a j * loss j) = 2) :
    sphericalOutgoingRate a ≤ 2 / Lmin := by
  apply (le_div_iff₀ hLmin).2
  have hcross := normalBalance_lossLower_crossBound
    (a := a) (loss := loss) (Lmin := Lmin) ha hloss hbalance
  nlinarith

end AFPBarrier
