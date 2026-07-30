import AFPBarrier.SphericalNetScaling
import AFPBarrier.EqualAngleAsymptotics
import Mathlib.Tactic

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Weighted squared deviation of edge losses from a center. -/
def lossVarianceAt
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (m : ℝ) : ℝ :=
  (offdiag i).sum (fun j => a i j * ((f i - f j) - m) ^ 2)

theorem lossVarianceAt_nonneg
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (m : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j) :
    0 ≤ lossVarianceAt a f i m := by
  unfold lossVarianceAt
  apply Finset.sum_nonneg
  intro j hj
  exact mul_nonneg (ha j (Finset.mem_erase.mp hj).1) (sq_nonneg _)

/-- Centered second-moment identity. -/
theorem carreDuChamp_centered_loss_identity
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (m : ℝ) :
    carreDuChamp a f i
        - 2 * m * (offdiag i).sum (fun j => a i j * (f i - f j))
        + m ^ 2 * jumpRate a i
      = lossVarianceAt a f i m := by
  classical
  unfold carreDuChamp jumpRate lossVarianceAt
  simp only [Finset.mul_sum]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- At an exact normalized eigenmode peak, the defect has a variance
 decomposition around every center `m`. -/
theorem peakDefect_centered_loss_identity
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam m : ℝ)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    peakDefect a f i lam - 2 * m * lam + m ^ 2 * jumpRate a i
      = lossVarianceAt a f i m := by
  rw [peakDefect_eq_carreDuChamp
    (a := a) (f := f) (i := i) (lam := lam) hfi hlinear]
  rw [← lossMoment_eq_eigenvalue
    (a := a) (f := f) (i := i) (lam := lam) hlinear]
  exact carreDuChamp_centered_loss_identity a f i m

/-- If `m` is the weighted mean loss, the Cauchy--Schwarz gap is exactly
 rate times weighted loss variance. -/
theorem rate_mul_peakDefect_sub_eigenvalue_sq_eq_rate_mul_lossVariance
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam m : ℝ)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hm : m * jumpRate a i = lam) :
    jumpRate a i * peakDefect a f i lam - lam ^ 2
      = jumpRate a i * lossVarianceAt a f i m := by
  have hid := peakDefect_centered_loss_identity
    a f i lam m hfi hlinear
  have hmsq : (m * jumpRate a i) ^ 2 = lam ^ 2 := by rw [hm]
  calc
    jumpRate a i * peakDefect a f i lam - lam ^ 2
        = jumpRate a i * peakDefect a f i lam
            - (m * jumpRate a i) ^ 2 := by rw [hmsq]
    _ = jumpRate a i *
          (peakDefect a f i lam - 2 * m * lam
            + m ^ 2 * jumpRate a i) := by
          rw [← hm]
          ring
    _ = jumpRate a i * lossVarianceAt a f i m := by rw [hid]

/-- Exact inefficiency gap for a square equal-angle ring. -/
theorem squareRing_rate_mul_defect_sub_four
    (h st : ℝ) (hsh : Real.sin h ≠ 0) (hst : st ≠ 0) :
    squareRingRate h st * squareRingDefect h st - 4
      = (st ^ 2 - 1) ^ 2 / st ^ 2 := by
  unfold squareRingRate squareRingDefect
  field_simp [hsh, hst]
  ring

theorem four_le_squareRing_rate_mul_defect
    (h st : ℝ) (hsh : Real.sin h ≠ 0) (hst : st ≠ 0) :
    4 ≤ squareRingRate h st * squareRingDefect h st := by
  have hgap := squareRing_rate_mul_defect_sub_four h st hsh hst
  have hnonneg : 0 ≤ (st ^ 2 - 1) ^ 2 / st ^ 2 := by positivity
  linarith

end AFPBarrier
