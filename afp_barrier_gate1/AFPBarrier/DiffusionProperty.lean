import AFPBarrier.JumpGenerator

/-!
# Finite jump generators and the diffusion chain rule

This module isolates the general mechanism behind the AFP second-harmonic
barrier. A nontrivial finite jump generator cannot satisfy an exact first-order
chain rule for a strictly supporting tangent of a nonlinear observable.

The statement is formulated through a nonnegative tangent gap rather than a
particular differentiability or convexity API. It therefore applies directly
to any strictly convex function once its supporting-line inequality is supplied.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The gap between `phi x` and the affine tangent model based at `y` with
slope `slope`. -/
def tangentGap (phi : ℝ → ℝ) (slope x y : ℝ) : ℝ :=
  phi x - phi y - slope * (x - y)

/-- Exact finite-sum chain-rule defect for a jump generator. -/
theorem jumpGenerator_chain_rule_defect
    (a : ι → ι → ℝ) (f : ι → ℝ) (phi : ℝ → ℝ)
    (slope : ℝ) (i : ι) :
    jumpGenerator a (fun j => phi (f j)) i
        - slope * jumpGenerator a f i
      =
    (offdiag i).sum
      (fun j => a i j * tangentGap phi slope (f j) (f i)) := by
  classical
  simp only [jumpGenerator, tangentGap]
  rw [Finset.mul_sum]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- If every tangent gap is nonnegative and vanishes only when the sampled
value is unchanged, then exact chain-rule equality forces the generator to
vanish on `f` at the selected state. -/
theorem strict_tangent_chain_rule_forces_generator_zero
    (a : ι → ι → ℝ) (f : ι → ℝ) (phi : ℝ → ℝ)
    (slope : ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hgap_nonneg : ∀ j, j ≠ i →
      0 ≤ tangentGap phi slope (f j) (f i))
    (hgap_strict : ∀ j, j ≠ i →
      tangentGap phi slope (f j) (f i) = 0 → f j = f i)
    (hchain :
      jumpGenerator a (fun j => phi (f j)) i
        = slope * jumpGenerator a f i) :
    jumpGenerator a f i = 0 := by
  classical
  have hsum :
      (offdiag i).sum
        (fun j => a i j * tangentGap phi slope (f j) (f i)) = 0 := by
    calc
      (offdiag i).sum
          (fun j => a i j * tangentGap phi slope (f j) (f i))
          = jumpGenerator a (fun j => phi (f j)) i
              - slope * jumpGenerator a f i :=
            (jumpGenerator_chain_rule_defect
              (a := a) (f := f) (phi := phi) (slope := slope) (i := i)).symm
      _ = 0 := by rw [hchain]; ring

  have hnonneg :
      ∀ j ∈ offdiag i,
        0 ≤ a i j * tangentGap phi slope (f j) (f i) := by
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    exact mul_nonneg (ha j hji) (hgap_nonneg j hji)

  have hterm :
      ∀ j ∈ offdiag i,
        a i j * tangentGap phi slope (f j) (f i) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp hsum

  unfold jumpGenerator
  apply Finset.sum_eq_zero
  intro j hj
  have hji : j ≠ i := (Finset.mem_erase.mp hj).1
  rcases mul_eq_zero.mp (hterm j hj) with hrate | hgap
  · simp [hrate]
  · have hsame : f j = f i := hgap_strict j hji hgap
    simp [hsame]

/-- The square observable is the canonical strictly convex specialization of
the general chain-rule barrier. -/
theorem square_chain_rule_forces_generator_zero
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hchain :
      jumpGenerator a (fun j => (f j) ^ 2) i
        = 2 * f i * jumpGenerator a f i) :
    jumpGenerator a f i = 0 := by
  apply strict_tangent_chain_rule_forces_generator_zero
    (a := a) (f := f) (phi := fun x => x ^ 2)
    (slope := 2 * f i) (i := i) ha
  · intro j hji
    dsimp [tangentGap]
    nlinarith [sq_nonneg (f j - f i)]
  · intro j hji hgap
    dsimp [tangentGap] at hgap
    have hsquare : (f j - f i) ^ 2 = 0 := by
      nlinarith
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp hsquare)
  · simpa using hchain

end AFPBarrier
