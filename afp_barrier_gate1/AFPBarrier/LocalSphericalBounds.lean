import AFPBarrier.LocalSphericalFeasibility
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Quantitative local spherical loss bounds

The normal-loss equation alone bounds the outgoing rate whenever all active
edge losses lie in a fixed positive window. These estimates do not require a
cone margin; coefficientwise lower bounds do.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι]

/-- Product form of the outgoing-rate sandwich. -/
theorem normal_balance_outgoing_product_bounds
    (a loss : ι → ℝ) (lossLower lossUpper target : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hlower : ∀ j, lossLower ≤ loss j)
    (hupper : ∀ j, loss j ≤ lossUpper)
    (hnormal : Finset.univ.sum (fun j => a j * loss j) = target) :
    lossLower * Finset.univ.sum a ≤ target ∧
      target ≤ lossUpper * Finset.univ.sum a := by
  constructor
  · calc
      lossLower * Finset.univ.sum a =
          Finset.univ.sum (fun j => lossLower * a j) := by
            rw [Finset.mul_sum]
      _ ≤ Finset.univ.sum (fun j => a j * loss j) := by
            apply Finset.sum_le_sum
            intro j hj
            calc
              lossLower * a j = a j * lossLower := by ring
              _ ≤ a j * loss j :=
                mul_le_mul_of_nonneg_left (hlower j) (ha j)
      _ = target := hnormal
  · calc
      target = Finset.univ.sum (fun j => a j * loss j) := hnormal.symm
      _ ≤ Finset.univ.sum (fun j => lossUpper * a j) := by
            apply Finset.sum_le_sum
            intro j hj
            calc
              a j * loss j = loss j * a j := by ring
              _ ≤ lossUpper * a j :=
                mul_le_mul_of_nonneg_right (hupper j) (ha j)
      _ = lossUpper * Finset.univ.sum a := by
            rw [Finset.mul_sum]

/-- Division form specialized to spherical normal target two. -/
theorem normal_balance_outgoing_rate_bounds
    (a loss : ι → ℝ) (lossLower lossUpper : ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hlower : ∀ j, lossLower ≤ loss j)
    (hupper : ∀ j, loss j ≤ lossUpper)
    (hlowerPos : 0 < lossLower)
    (hupperPos : 0 < lossUpper)
    (hnormal : Finset.univ.sum (fun j => a j * loss j) = 2) :
    2 / lossUpper ≤ Finset.univ.sum a ∧
      Finset.univ.sum a ≤ 2 / lossLower := by
  have hprod := normal_balance_outgoing_product_bounds
    (a := a) (loss := loss)
    (lossLower := lossLower) (lossUpper := lossUpper) (target := 2)
    ha hlower hupper hnormal
  constructor
  · apply (div_le_iff₀ hupperPos).2
    nlinarith [hprod.2]
  · apply (le_div_iff₀ hlowerPos).2
    nlinarith [hprod.1]

end AFPBarrier
