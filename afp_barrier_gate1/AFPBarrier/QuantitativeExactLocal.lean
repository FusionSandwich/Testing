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

/-- Mix an arbitrary normalized dependence with uniform indexed mass.  This is
the finite coefficient construction used in the quantitative inball proof. -/
noncomputable def uniformDependenceMixture
    (tau : ℝ) (lambda : ι → ℝ) (j : ι) : ℝ :=
  tau / (Fintype.card ι : ℝ) + (1 - tau) * lambda j

/-- The uniform-mixture construction remains normalized. -/
theorem uniformDependenceMixture_sum [Nonempty ι]
    (tau : ℝ) (lambda : ι → ℝ)
    (hlambdaSum : Finset.univ.sum lambda = 1) :
    Finset.univ.sum (uniformDependenceMixture tau lambda) = 1 := by
  have hcardNat : Fintype.card ι ≠ 0 := Fintype.card_ne_zero
  have hcardReal : (Fintype.card ι : ℝ) ≠ 0 := by
    exact_mod_cast hcardNat
  unfold uniformDependenceMixture
  rw [Finset.sum_add_distrib]
  rw [Finset.sum_const, nsmul_eq_mul, Finset.card_univ,
    ← Finset.mul_sum, hlambdaSum]
  field_simp
  ring

/-- Every coordinate of the mixture receives the explicit uniform margin
`tau / card ι`. -/
theorem uniformDependenceMixture_lower [Nonempty ι]
    (tau : ℝ) (lambda : ι → ℝ)
    (htau : tau ≤ 1)
    (hlambda : ∀ j, 0 ≤ lambda j) :
    ∀ j,
      tau / (Fintype.card ι : ℝ) ≤
        uniformDependenceMixture tau lambda j := by
  intro j
  unfold uniformDependenceMixture
  exact le_add_of_nonneg_right
    (mul_nonneg (sub_nonneg.mpr htau) (hlambda j))

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

/-- A normalized nonnegative dependence transfers pointwise half-angle bounds
to the exact common angular scale. -/
theorem normalizedAngularScale_bounds
    (beta halfTan : ι → ℝ) (scaleLower scaleUpper : ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hlower : ∀ j, scaleLower ≤ halfTan j)
    (hupper : ∀ j, halfTan j ≤ scaleUpper) :
    scaleLower ≤ normalizedAngularScale beta halfTan ∧
      normalizedAngularScale beta halfTan ≤ scaleUpper := by
  exact normalizedWeightedSum_bounds beta halfTan scaleLower scaleUpper
    hbeta hbetaSum hlower hupper

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

/-- Explicit two-factor rate constants: a common-scale interval and a
reciprocal-sine interval combine with the exact rate identity. -/
theorem exactLocalRowRate_twoFactor_bounds
    (beta sinTheta halfTan : ι → ℝ)
    (scaleLower scaleUpper invLower invUpper : ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscaleLower : 0 < scaleLower)
    (hscaleUpper : scaleLower ≤ scaleUpper)
    (hhalfLower : ∀ j, scaleLower ≤ halfTan j)
    (hhalfUpper : ∀ j, halfTan j ≤ scaleUpper)
    (hinvLower : 0 ≤ invLower)
    (hinvUpper : 0 ≤ invUpper)
    (hinvPointLower : ∀ j, invLower ≤ 1 / sinTheta j)
    (hinvPointUpper : ∀ j, 1 / sinTheta j ≤ invUpper) :
    (2 / scaleUpper) * invLower ≤
        Finset.univ.sum (exactLocalRowRate beta sinTheta halfTan) ∧
      Finset.univ.sum (exactLocalRowRate beta sinTheta halfTan) ≤
        (2 / scaleLower) * invUpper := by
  have hscaleBounds := normalizedAngularScale_bounds beta halfTan
    scaleLower scaleUpper hbeta hbetaSum hhalfLower hhalfUpper
  have hscalePos : 0 < normalizedAngularScale beta halfTan :=
    lt_of_lt_of_le hscaleLower hscaleBounds.1
  have hscaleUpperPos : 0 < scaleUpper :=
    lt_of_lt_of_le hscaleLower hscaleUpper
  have havg := normalizedWeightedSum_bounds beta
    (fun j => 1 / sinTheta j) invLower invUpper
    hbeta hbetaSum hinvPointLower hinvPointUpper
  have havg' :
      invLower ≤ Finset.univ.sum (fun j => beta j / sinTheta j) ∧
        Finset.univ.sum (fun j => beta j / sinTheta j) ≤ invUpper := by
    simpa [div_eq_mul_inv] using havg
  have hfactorNonneg :
      0 ≤ 2 / normalizedAngularScale beta halfTan :=
    div_nonneg (by norm_num) (le_of_lt hscalePos)
  have hfactorLower :
      2 / scaleUpper ≤ 2 / normalizedAngularScale beta halfTan := by
    apply (div_le_div_iff₀ hscaleUpperPos hscalePos).2
    nlinarith [hscaleBounds.2]
  have hfactorUpper :
      2 / normalizedAngularScale beta halfTan ≤ 2 / scaleLower := by
    apply (div_le_div_iff₀ hscalePos hscaleLower).2
    nlinarith [hscaleBounds.1]
  have hid := exactLocalRowRate_sum beta sinTheta halfTan hsin
    (ne_of_gt hscalePos)
  rw [hid]
  constructor
  · calc
      (2 / scaleUpper) * invLower ≤
          (2 / normalizedAngularScale beta halfTan) * invLower :=
        mul_le_mul_of_nonneg_right hfactorLower hinvLower
      _ ≤ (2 / normalizedAngularScale beta halfTan) *
          Finset.univ.sum (fun j => beta j / sinTheta j) :=
        mul_le_mul_of_nonneg_left havg'.1 hfactorNonneg
  · calc
      (2 / normalizedAngularScale beta halfTan) *
          Finset.univ.sum (fun j => beta j / sinTheta j) ≤
          (2 / normalizedAngularScale beta halfTan) * invUpper :=
        mul_le_mul_of_nonneg_left havg'.2 hfactorNonneg
      _ ≤ (2 / scaleLower) * invUpper :=
        mul_le_mul_of_nonneg_right hfactorUpper hinvUpper

end AFPBarrier
