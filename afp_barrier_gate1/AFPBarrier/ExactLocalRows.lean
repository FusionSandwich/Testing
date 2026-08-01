import AFPBarrier.LocalSphericalFeasibility
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Push

/-!
# Exact algebra for normalized local spherical rows

This file contains the finite algebra behind the non-antipodal local theorem.
It deliberately does not assert the separate convex-hull existence theorem.
The functions `sinTheta` and `halfTan` represent
`sin theta_j` and `tan (theta_j / 2)`, respectively.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*} [Fintype ι] [Fintype κ]

def normalizedAngularScale (beta halfTan : ι → ℝ) : ℝ :=
  Finset.univ.sum (fun j => beta j * halfTan j)

def tangentMass (a sinTheta : ι → ℝ) : ℝ :=
  Finset.univ.sum (fun j => a j * sinTheta j)

noncomputable def normalizedTangentWeight
    (a sinTheta : ι → ℝ) (j : ι) : ℝ :=
  a j * sinTheta j / tangentMass a sinTheta

noncomputable def exactLocalRowRate
    (beta sinTheta halfTan : ι → ℝ) (j : ι) : ℝ :=
  scaledSphericalRowRate beta sinTheta
    (normalizedAngularScale beta halfTan) j

theorem normalizedAngularScale_pos
    (beta halfTan : ι → ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hhalfTan : ∀ j, 0 < halfTan j) :
    0 < normalizedAngularScale beta halfTan := by
  have hex : ∃ j, 0 < beta j := by
    by_contra h
    push_neg at h
    have hzero : ∀ j, beta j = 0 := by
      intro j
      exact le_antisymm (h j) (hbeta j)
    have : Finset.univ.sum beta = 0 := by
      apply Finset.sum_eq_zero
      intro j hj
      exact hzero j
    linarith
  rcases hex with ⟨j, hj⟩
  unfold normalizedAngularScale
  refine Finset.sum_pos' ?_ ⟨j, Finset.mem_univ j, ?_⟩
  · intro k hk
    exact mul_nonneg (hbeta k) (le_of_lt (hhalfTan k))
  · exact mul_pos hj (hhalfTan j)

theorem exactLocalRowRate_nonneg
    (beta sinTheta halfTan : ι → ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hhalfTan : ∀ j, 0 < halfTan j) :
    ∀ j, 0 ≤ exactLocalRowRate beta sinTheta halfTan j := by
  apply scaledSphericalRowRate_nonneg
  · exact hbeta
  · exact hsin
  · exact normalizedAngularScale_pos beta halfTan hbeta hbetaSum hhalfTan

theorem exactLocalRowRate_pos
    (beta sinTheta halfTan : ι → ℝ)
    (hbeta : ∀ j, 0 < beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hhalfTan : ∀ j, 0 < halfTan j) :
    ∀ j, 0 < exactLocalRowRate beta sinTheta halfTan j := by
  apply scaledSphericalRowRate_pos
  · exact hbeta
  · exact hsin
  · apply normalizedAngularScale_pos beta halfTan
    · intro j
      exact le_of_lt (hbeta j)
    · exact hbetaSum
    · exact hhalfTan

theorem exactLocalRowRate_tangent_balance
    (beta sinTheta halfTan : ι → ℝ) (u : ι → κ → ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hhalfTan : ∀ j, 0 < halfTan j)
    (htangent : ∀ k,
      Finset.univ.sum (fun j => beta j * u j k) = 0) :
    ∀ k,
      Finset.univ.sum
          (fun j => exactLocalRowRate beta sinTheta halfTan j
            * sinTheta j * u j k) = 0 := by
  apply scaledSphericalRowRate_tangent_balance
  · exact hsin
  · exact normalizedAngularScale_pos beta halfTan hbeta hbetaSum hhalfTan
  · exact htangent

theorem exactLocalRowRate_normal_balance
    (beta sinTheta halfTan : ι → ℝ)
    (hbeta : ∀ j, 0 ≤ beta j)
    (hbetaSum : Finset.univ.sum beta = 1)
    (hsin : ∀ j, 0 < sinTheta j)
    (hhalfTan : ∀ j, 0 < halfTan j) :
    Finset.univ.sum
        (fun j => exactLocalRowRate beta sinTheta halfTan j
          * (sinTheta j * halfTan j)) = 2 := by
  apply scaledSphericalRowRate_normal_balance
      beta sinTheta (fun j => sinTheta j * halfTan j)
      (normalizedAngularScale beta halfTan)
  · exact hsin
  · exact normalizedAngularScale_pos beta halfTan hbeta hbetaSum hhalfTan
  · unfold normalizedAngularScale
    apply Finset.sum_congr rfl
    intro j hj
    field_simp [ne_of_gt (hsin j)]

theorem exactLocalRowRate_sum
    (beta sinTheta halfTan : ι → ℝ)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : normalizedAngularScale beta halfTan ≠ 0) :
    Finset.univ.sum (exactLocalRowRate beta sinTheta halfTan) =
      (2 / normalizedAngularScale beta halfTan) *
        Finset.univ.sum (fun j => beta j / sinTheta j) := by
  unfold exactLocalRowRate scaledSphericalRowRate
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  field_simp [ne_of_gt (hsin j), hscale]

theorem tangentMass_pos_of_normal_balance
    (a sinTheta halfTan : ι → ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hsin : ∀ j, 0 < sinTheta j)
    (hnormal : Finset.univ.sum
      (fun j => a j * (sinTheta j * halfTan j)) = 2) :
    0 < tangentMass a sinTheta := by
  have hex : ∃ j, 0 < a j := by
    by_contra h
    push_neg at h
    have hzero : ∀ j, a j = 0 := by
      intro j
      exact le_antisymm (h j) (ha j)
    have : Finset.univ.sum
        (fun j => a j * (sinTheta j * halfTan j)) = 0 := by
      apply Finset.sum_eq_zero
      intro j hj
      simp [hzero j]
    linarith
  rcases hex with ⟨j, hj⟩
  unfold tangentMass
  refine Finset.sum_pos' ?_ ⟨j, Finset.mem_univ j, ?_⟩
  · intro k hk
    exact mul_nonneg (ha k) (le_of_lt (hsin k))
  · exact mul_pos hj (hsin j)

theorem normalizedTangentWeight_nonneg
    (a sinTheta : ι → ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hsin : ∀ j, 0 ≤ sinTheta j)
    (hmass : 0 < tangentMass a sinTheta) :
    ∀ j, 0 ≤ normalizedTangentWeight a sinTheta j := by
  intro j
  unfold normalizedTangentWeight
  exact div_nonneg (mul_nonneg (ha j) (hsin j)) (le_of_lt hmass)

theorem normalizedTangentWeight_sum
    (a sinTheta : ι → ℝ)
    (hmass : tangentMass a sinTheta ≠ 0) :
    Finset.univ.sum (normalizedTangentWeight a sinTheta) = 1 := by
  unfold normalizedTangentWeight tangentMass
  rw [Finset.sum_div]
  exact div_self hmass

theorem normalizedTangentWeight_balance
    (a sinTheta : ι → ℝ) (u : ι → κ → ℝ)
    (hmass : tangentMass a sinTheta ≠ 0)
    (htangent : ∀ k,
      Finset.univ.sum (fun j => a j * sinTheta j * u j k) = 0) :
    ∀ k,
      Finset.univ.sum
          (fun j => normalizedTangentWeight a sinTheta j * u j k) = 0 := by
  intro k
  unfold normalizedTangentWeight
  calc
    Finset.univ.sum
        (fun j => a j * sinTheta j / tangentMass a sinTheta * u j k) =
        (Finset.univ.sum (fun j => a j * sinTheta j * u j k)) /
          tangentMass a sinTheta := by
            rw [Finset.sum_div]
            apply Finset.sum_congr rfl
            intro j hj
            ring
    _ = 0 := by rw [htangent k]; simp [hmass]

theorem normalizedAngularScale_normalizedTangentWeight
    (a sinTheta halfTan : ι → ℝ)
    (hmass : tangentMass a sinTheta ≠ 0)
    (hnormal : Finset.univ.sum
      (fun j => a j * (sinTheta j * halfTan j)) = 2) :
    normalizedAngularScale
        (normalizedTangentWeight a sinTheta) halfTan =
      2 / tangentMass a sinTheta := by
  unfold normalizedAngularScale normalizedTangentWeight
  calc
    Finset.univ.sum
        (fun j => a j * sinTheta j / tangentMass a sinTheta * halfTan j) =
        (Finset.univ.sum
          (fun j => a j * (sinTheta j * halfTan j))) /
            tangentMass a sinTheta := by
              rw [Finset.sum_div]
              apply Finset.sum_congr rfl
              intro j hj
              ring
    _ = 2 / tangentMass a sinTheta := by rw [hnormal]

theorem exactLocalRowRate_recover
    (a sinTheta halfTan : ι → ℝ)
    (hsin : ∀ j, 0 < sinTheta j)
    (hmass : tangentMass a sinTheta ≠ 0)
    (hnormal : Finset.univ.sum
      (fun j => a j * (sinTheta j * halfTan j)) = 2) :
    ∀ j,
      exactLocalRowRate (normalizedTangentWeight a sinTheta)
        sinTheta halfTan j = a j := by
  intro j
  unfold exactLocalRowRate scaledSphericalRowRate
  rw [normalizedAngularScale_normalizedTangentWeight
    a sinTheta halfTan hmass hnormal]
  unfold normalizedTangentWeight
  field_simp [ne_of_gt (hsin j), hmass]

end AFPBarrier
