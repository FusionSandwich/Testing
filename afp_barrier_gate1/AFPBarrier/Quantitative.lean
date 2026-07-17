import AFPBarrier.JumpGenerator

/-!
# Quantitative defect and stiffness bounds
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Defect in the square relation at a peak for an intended eigenvalue
`-lam`. For the spherical application this is the degree-two defect. -/
def peakDefect
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ) : ℝ :=
  jumpGenerator a (fun j => (f j) ^ 2) i + 2 * lam

/-- Under exact degree-one preservation at a normalized peak, the defect
is exactly the carré du champ. -/
theorem peakDefect_eq_carreDuChamp
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    peakDefect a f i lam = carreDuChamp a f i := by
  calc
    peakDefect a f i lam
        = jumpGenerator a (fun j => (f j) ^ 2) i
            - 2 * f i * jumpGenerator a f i := by
              simp [peakDefect, hfi, hlinear]
    _ = carreDuChamp a f i :=
      jumpGenerator_square_identity (a := a) (f := f) (i := i)

/-- The unavoidable defect is nonnegative. -/
theorem peakDefect_nonneg
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    0 ≤ peakDefect a f i lam := by
  rw [peakDefect_eq_carreDuChamp
    (a := a) (f := f) (i := i) (lam := lam) hfi hlinear]
  exact carreDuChamp_nonneg (a := a) (f := f) (i := i) ha

/-- Sharp defect-stiffness inequality:
`lam^2 <= total_rate * defect`. -/
theorem eigenvalue_sq_le_rate_mul_peakDefect
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    lam ^ 2 ≤ jumpRate a i * peakDefect a f i lam := by
  have hcs := jumpGenerator_sq_le_rate_mul_carre
    (a := a) (f := f) (i := i) ha
  have hdef := peakDefect_eq_carreDuChamp
    (a := a) (f := f) (i := i) (lam := lam) hfi hlinear
  calc
    lam ^ 2 = (-lam) ^ 2 := by ring
    _ = (jumpGenerator a f i) ^ 2 := by rw [hlinear]
    _ ≤ jumpRate a i * carreDuChamp a f i := hcs
    _ = jumpRate a i * peakDefect a f i lam := by rw [hdef]

/-- If the intended eigenvalue is nonzero, the defect is strictly positive. -/
theorem peakDefect_pos
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlam : lam ≠ 0)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    0 < peakDefect a f i lam := by
  have hbound := eigenvalue_sq_le_rate_mul_peakDefect
    (a := a) (f := f) (i := i) (lam := lam) ha hfi hlinear
  have hrate := jumpRate_nonneg (a := a) (i := i) ha
  have hdef := peakDefect_nonneg
    (a := a) (f := f) (i := i) (lam := lam) ha hfi hlinear
  by_contra hnot
  have hle : peakDefect a f i lam ≤ 0 := le_of_not_gt hnot
  have hz : peakDefect a f i lam = 0 := le_antisymm hle hdef
  rw [hz] at hbound
  have hsq : 0 < lam ^ 2 := sq_pos_of_ne_zero hlam
  nlinarith

/-- Division form of the stiffness lower bound. -/
theorem peakDefect_lower_bound
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i) :
    lam ^ 2 / jumpRate a i ≤ peakDefect a f i lam := by
  apply (div_le_iff₀ hrate).2
  have hbound := eigenvalue_sq_le_rate_mul_peakDefect
    (a := a) (f := f) (i := i) (lam := lam) ha hfi hlinear
  simpa [mul_comm] using hbound

end AFPBarrier
