import AFPBarrier.NoGo
import AFPBarrier.Quantitative

/-!
# The `S^2` numerical specialization

The analytic facts about spherical harmonics are deliberately passed as
hypotheses. This isolates the finite-dimensional theorem from a future
formalization of differential geometry on the sphere.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Exact degree-one and degree-two zonal AFP relations on `S^2` are
incompatible with nonnegative finite jump rates. -/
theorem no_exact_S2_degree_two_at_peak
    (a : ι → ι → ℝ) (g : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hgi : g i = 1)
    (hdegreeOne : jumpGenerator a g i = -2)
    (hdegreeTwo :
      jumpGenerator a (fun j => (g j) ^ 2 - ((1 : ℝ) / 3)) i
        = -6 * ((g i) ^ 2 - ((1 : ℝ) / 3))) :
    False := by
  exact no_exact_shifted_quadratic_at_peak
    (a := a) (g := g) (i := i)
    (lam := 2) (mu := 6) (c := (1 : ℝ) / 3)
    ha (by norm_num) (by norm_num) hgi hdegreeOne hdegreeTwo

/-- On `S^2`, exact degree-one preservation implies
`4 <= total_rate * degree_two_defect`. -/
theorem S2_four_le_rate_mul_defect
    (a : ι → ι → ℝ) (g : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hgi : g i = 1)
    (hdegreeOne : jumpGenerator a g i = -2) :
    4 ≤ jumpRate a i * peakDefect a g i 2 := by
  have h := eigenvalue_sq_le_rate_mul_peakDefect
    (a := a) (f := g) (i := i) (lam := 2)
    ha hgi hdegreeOne
  norm_num at h
  exact h

end AFPBarrier
