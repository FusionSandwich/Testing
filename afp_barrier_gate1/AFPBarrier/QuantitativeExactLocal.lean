import AFPBarrier.ExactLocalRows

/-!
# Finite quantitative bounds for exact local rows

This file isolates the weighted-average inequalities used when the exact rate
identity is combined with angular lower and upper bounds.  Trigonometric
specialization is recorded in the mathematical theorem package.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι]

theorem normalizedWeightedSum_bounds
    (beta f : ι → ℝ) (lower upper : ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hlower : ∀ j, lower ≤ f j)
    (hupper : ∀ j, f j ≤ upper) :
    lower ≤ Finset.univ.sum (fun j => beta j * f j) ∧
      Finset.univ.sum (fun j => beta j * f j) ≤ upper := by
  constructor
  · calc
      lower = Finset.univ.sum (fun j => beta j * lower) := by
        rw [← Finset.sum_mul, hbetaSum, one_mul]
      _ ≤ Finset.univ.sum (fun j => beta j * f j) := by
        apply Finset.sum_le_sum
        intro j hj
        exact mul_le_mul_of_nonneg_left (hlower j) (hbeta j)
  · calc
      Finset.univ.sum (fun j => beta j * f j) ≤
          Finset.univ.sum (fun j => beta j * upper) := by
        apply Finset.sum_le_sum
        intro j hj
        exact mul_le_mul_of_nonneg_left (hupper j) (hbeta j)
      _ = upper := by
        rw [← Finset.sum_mul, hbetaSum, one_mul]

/-- Quantitative rate bounds obtained directly from the exact rate identity
and pointwise reciprocal-sine bounds. -/
theorem exactLocalRowRate_sum_bounds
    (beta sinTheta halfTan : ι → ℝ)
    (invLower invUpper : ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : 0 < normalizedAngularScale beta halfTan)
    (hlower : ∀ j, invLower ≤ 1 / sinTheta j)
    (hupper : ∀ j, 1 / sinTheta j ≤ invUpper) :
    (2 / normalizedAngularScale beta halfTan) * invLower ≤
        Finset.univ.sum (exactLocalRowRate beta sinTheta halfTan) ∧
      Finset.univ.sum (exactLocalRowRate beta sinTheta halfTan) ≤
        (2 / normalizedAngularScale beta halfTan) * invUpper := by
  have havg := normalizedWeightedSum_bounds beta
    (fun j => 1 / sinTheta j) invLower invUpper
    hbeta hbetaSum hlower hupper
  have havg' :
      invLower ≤ Finset.univ.sum (fun j => beta j / sinTheta j) ∧
        Finset.univ.sum (fun j => beta j / sinTheta j) ≤ invUpper := by
    simpa [div_eq_mul_inv] using havg
  have hfactor : 0 ≤ 2 / normalizedAngularScale beta halfTan :=
    div_nonneg (by norm_num) (le_of_lt hscale)
  have hid := exactLocalRowRate_sum beta sinTheta halfTan hsin
    (ne_of_gt hscale)
  constructor
  · rw [hid]
    exact mul_le_mul_of_nonneg_left havg'.1 hfactor
  · rw [hid]
    exact mul_le_mul_of_nonneg_left havg'.2 hfactor

end AFPBarrier
