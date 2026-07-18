import AFPBarrier.NoGo
import AFPBarrier.Quantitative

/-!
# From a conservative forward AFP matrix to a finite jump generator

Transport papers typically state conservation and moment preservation for a
forward matrix `M`, whereas the no-go proof is most transparent for the weighted
backward adjoint. This module formalizes that conversion without using the
matrix API: all identities are stated componentwise as finite sums.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Off-diagonal jump rates of the weighted adjoint `A = W⁻¹ Mᵀ W`. -/
noncomputable def weightedAdjointRate
    (M : ι → ι → ℝ) (w : ι → ℝ) (i j : ι) : ℝ :=
  (w j * M j i) / w i

/-- Positive weights and nonnegative forward off-diagonal entries produce
nonnegative weighted-adjoint jump rates. -/
omit [Fintype ι] [DecidableEq ι] in
theorem weightedAdjointRate_nonneg
    (M : ι → ι → ℝ) (w : ι → ℝ)
    (hw : ∀ i, 0 < w i)
    (hM : ∀ i j, i ≠ j → 0 ≤ M i j)
    (i j : ι) (hji : j ≠ i) :
    0 ≤ weightedAdjointRate M w i j := by
  unfold weightedAdjointRate
  exact div_nonneg
    (mul_nonneg (le_of_lt (hw j)) (hM j i hji))
    (le_of_lt (hw i))

/-- Weighted conservation converts the full weighted-adjoint action into the
jump-generator form. -/
theorem jumpGenerator_weightedAdjointRate_eq
    (M : ι → ι → ℝ) (w f : ι → ℝ) (i : ι)
    (hconservation :
      Finset.univ.sum (fun j => w j * M j i) = 0) :
    jumpGenerator (weightedAdjointRate M w) f i
      = (Finset.univ.sum (fun j => w j * M j i * f j)) / w i := by
  classical
  have hfull :
      (offdiag i).sum
          (fun j => weightedAdjointRate M w i j * (f j - f i))
        =
      Finset.univ.sum
          (fun j => weightedAdjointRate M w i j * (f j - f i)) := by
    rw [← Finset.sum_erase_add
      Finset.univ
      (fun j => weightedAdjointRate M w i j * (f j - f i))
      (Finset.mem_univ i)]
    simp [offdiag]

  rw [jumpGenerator, hfull]
  simp only [weightedAdjointRate]
  calc
    Finset.univ.sum
        (fun j => ((w j * M j i) / w i) * (f j - f i))
        =
      Finset.univ.sum
        (fun j => (w j * M j i * f j) / w i
          - ((w j * M j i) * f i) / w i) := by
            apply Finset.sum_congr rfl
            intro j hj
            ring
    _ =
      (Finset.univ.sum (fun j => w j * M j i * f j)) / w i
        - (Finset.univ.sum (fun j => (w j * M j i) * f i)) / w i := by
          rw [Finset.sum_sub_distrib, Finset.sum_div, Finset.sum_div]
    _ =
      (Finset.univ.sum (fun j => w j * M j i * f j)) / w i := by
        rw [← Finset.sum_mul]
        rw [hconservation]
        simp

/-- A weighted forward moment equation becomes a pointwise eigenfunction
equation for the jump generator. -/
theorem jumpGenerator_weightedAdjointRate_eigen
    (M : ι → ι → ℝ) (w f : ι → ℝ) (i : ι) (lam : ℝ)
    (hw : ∀ i, 0 < w i)
    (hconservation :
      Finset.univ.sum (fun j => w j * M j i) = 0)
    (hmoment :
      Finset.univ.sum (fun j => w j * f j * M j i)
        = -lam * w i * f i) :
    jumpGenerator (weightedAdjointRate M w) f i = -lam * f i := by
  have hbase := jumpGenerator_weightedAdjointRate_eq
    (M := M) (w := w) (f := f) (i := i)
    hconservation
  rw [hbase]
  have hrewrite :
      Finset.univ.sum (fun j => w j * M j i * f j)
        = Finset.univ.sum (fun j => w j * f j * M j i) := by
    apply Finset.sum_congr rfl
    intro j hj
    ring
  rw [hrewrite, hmoment]
  field_simp [ne_of_gt (hw i)]

/-- Forward-matrix form of the generic square obstruction. -/
theorem no_exact_forward_linear_and_square_at_peak
    (M : ι → ι → ℝ) (w f : ι → ℝ) (i : ι) (lam : ℝ)
    (hw : ∀ i, 0 < w i)
    (hM : ∀ i j, i ≠ j → 0 ≤ M i j)
    (hconservation :
      ∀ k, Finset.univ.sum (fun j => w j * M j k) = 0)
    (hfi : f i = 1)
    (hlam : 0 < lam)
    (hlinearMoment :
      ∀ k, Finset.univ.sum (fun j => w j * f j * M j k)
        = -lam * w k * f k)
    (hsquareMoment :
      ∀ k, Finset.univ.sum (fun j => w j * (f j) ^ 2 * M j k)
        = (-2 * lam) * w k * (f k) ^ 2) :
    False := by
  let a := weightedAdjointRate M w
  have ha : ∀ j, j ≠ i → 0 ≤ a i j := by
    intro j hji
    exact weightedAdjointRate_nonneg M w hw hM i j hji
  have hlinear : jumpGenerator a f i = -lam := by
    have h := jumpGenerator_weightedAdjointRate_eigen
      (M := M) (w := w) (f := f) (i := i) (lam := lam)
      hw (hconservation i) (hlinearMoment i)
    rw [hfi] at h
    simpa [a] using h
  have hsquare :
      jumpGenerator a (fun j => (f j) ^ 2) i = -2 * lam := by
    have h := jumpGenerator_weightedAdjointRate_eigen
      (M := M) (w := w) (f := fun j => (f j) ^ 2)
      (i := i) (lam := 2 * lam)
      hw (hconservation i) (by
        simpa [mul_assoc] using hsquareMoment i)
    calc
      jumpGenerator a (fun j => (f j) ^ 2) i
          = -(2 * lam) * (f i) ^ 2 := by simpa [a] using h
      _ = -2 * lam := by rw [hfi]; ring
  exact no_exact_linear_and_square_at_peak
    (a := a) (f := f) (i := i) (lam := lam)
    ha hlam hfi hlinear hsquare

end AFPBarrier
