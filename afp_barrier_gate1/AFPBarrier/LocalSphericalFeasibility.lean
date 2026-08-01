import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic

/-!
# Constructive local spherical feasibility

At one spherical node, write every candidate neighbor as

  Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,

where `u_j` is tangent.  A degree-one-exact positive row must satisfy a tangent
balance and one scalar normal-loss balance.

This module formalizes the algebraic core of the corrected feasible-cone
theorem.  A nonnegative tangent dependence `b_j` with positive normal scale
can be rescaled into a degree-one-exact row, and every row induces such a
tangent dependence.  The convex-hull and relative-interior characterization is
kept separate from this finite algebraic scaling lemma.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*} [Fintype ι] [Fintype κ]

/-- Rescale a nonnegative tangent dependence into spherical row rates. -/
noncomputable def scaledSphericalRowRate
    (b sinTheta : ι → ℝ) (normalScale : ℝ) (j : ι) : ℝ :=
  2 * b j / (sinTheta j * normalScale)

/-- The dependence weight induced by a spherical row. -/
def tangentDependenceWeight
    (a sinTheta : ι → ℝ) (j : ι) : ℝ :=
  a j * sinTheta j

/-- Nonnegative tangent weights and positive angular factors produce
nonnegative row rates. -/
theorem scaledSphericalRowRate_nonneg
    (b sinTheta : ι → ℝ) (normalScale : ℝ)
    (hb : ∀ j, 0 ≤ b j)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : 0 < normalScale) :
    ∀ j, 0 ≤ scaledSphericalRowRate b sinTheta normalScale j := by
  intro j
  unfold scaledSphericalRowRate
  exact div_nonneg
    (mul_nonneg (by norm_num) (hb j))
    (le_of_lt (mul_pos (hsin j) hscale))

/-- Strictly positive tangent weights produce strictly positive row rates. -/
theorem scaledSphericalRowRate_pos
    (b sinTheta : ι → ℝ) (normalScale : ℝ)
    (hb : ∀ j, 0 < b j)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : 0 < normalScale) :
    ∀ j, 0 < scaledSphericalRowRate b sinTheta normalScale j := by
  intro j
  unfold scaledSphericalRowRate
  exact div_pos (mul_pos (by norm_num) (hb j)) (mul_pos (hsin j) hscale)

/-- Rescaling preserves a zero tangent dependence. -/
theorem scaledSphericalRowRate_tangent_balance
    (b sinTheta : ι → ℝ) (u : ι → κ → ℝ) (normalScale : ℝ)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : 0 < normalScale)
    (htangent : ∀ k, Finset.univ.sum (fun j => b j * u j k) = 0) :
    ∀ k,
      Finset.univ.sum
          (fun j => scaledSphericalRowRate b sinTheta normalScale j
            * sinTheta j * u j k)
        = 0 := by
  intro k
  have hterm : ∀ j,
      scaledSphericalRowRate b sinTheta normalScale j
          * sinTheta j * u j k
        = (2 / normalScale) * (b j * u j k) := by
    intro j
    unfold scaledSphericalRowRate
    field_simp [ne_of_gt (hsin j), ne_of_gt hscale]
  calc
    Finset.univ.sum
        (fun j => scaledSphericalRowRate b sinTheta normalScale j
          * sinTheta j * u j k)
        = Finset.univ.sum
            (fun j => (2 / normalScale) * (b j * u j k)) := by
              apply Finset.sum_congr rfl
              intro j hj
              exact hterm j
    _ = (2 / normalScale) *
          Finset.univ.sum (fun j => b j * u j k) := by
            rw [Finset.mul_sum]
    _ = 0 := by rw [htangent k]; ring

/-- The scalar normal-loss equation fixes the unique common scaling of a
chosen tangent dependence. -/
theorem scaledSphericalRowRate_normal_balance
    (b sinTheta loss : ι → ℝ) (normalScale : ℝ)
    (hsin : ∀ j, 0 < sinTheta j)
    (hscale : 0 < normalScale)
    (hnormal :
      normalScale =
        Finset.univ.sum (fun j => b j * loss j / sinTheta j)) :
    Finset.univ.sum
        (fun j => scaledSphericalRowRate b sinTheta normalScale j * loss j)
      = 2 := by
  have hterm : ∀ j,
      scaledSphericalRowRate b sinTheta normalScale j * loss j
        = (2 / normalScale) * (b j * loss j / sinTheta j) := by
    intro j
    unfold scaledSphericalRowRate
    field_simp [ne_of_gt (hsin j), ne_of_gt hscale]
  calc
    Finset.univ.sum
        (fun j => scaledSphericalRowRate b sinTheta normalScale j * loss j)
        = Finset.univ.sum
            (fun j => (2 / normalScale) *
              (b j * loss j / sinTheta j)) := by
                apply Finset.sum_congr rfl
                intro j hj
                exact hterm j
    _ = (2 / normalScale) *
          Finset.univ.sum (fun j => b j * loss j / sinTheta j) := by
            rw [Finset.mul_sum]
    _ = 2 := by rw [← hnormal]; field_simp [ne_of_gt hscale]

/-- Every nonnegative spherical row induces nonnegative tangent dependence
weights. -/
theorem tangentDependenceWeight_nonneg
    (a sinTheta : ι → ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hsin : ∀ j, 0 ≤ sinTheta j) :
    ∀ j, 0 ≤ tangentDependenceWeight a sinTheta j := by
  intro j
  exact mul_nonneg (ha j) (hsin j)

/-- The row tangent equation is exactly the tangent-dependence equation after
setting `b_j = a_j sin(theta_j)`. -/
theorem tangentDependenceWeight_balance
    (a sinTheta : ι → ℝ) (u : ι → κ → ℝ)
    (hrow : ∀ k,
      Finset.univ.sum (fun j => a j * sinTheta j * u j k) = 0) :
    ∀ k,
      Finset.univ.sum
          (fun j => tangentDependenceWeight a sinTheta j * u j k)
        = 0 := by
  intro k
  simpa [tangentDependenceWeight, mul_assoc] using hrow k

/-- The row normal-loss equation becomes the dependence normal scale. -/
theorem tangentDependenceWeight_normal_scale
    (a sinTheta loss : ι → ℝ)
    (hsin : ∀ j, sinTheta j ≠ 0)
    (hnormal : Finset.univ.sum (fun j => a j * loss j) = 2) :
    Finset.univ.sum
        (fun j => tangentDependenceWeight a sinTheta j * loss j / sinTheta j)
      = 2 := by
  calc
    Finset.univ.sum
        (fun j => tangentDependenceWeight a sinTheta j * loss j / sinTheta j)
        = Finset.univ.sum (fun j => a j * loss j) := by
            apply Finset.sum_congr rfl
            intro j hj
            unfold tangentDependenceWeight
            field_simp [hsin j]
    _ = 2 := hnormal

end AFPBarrier
