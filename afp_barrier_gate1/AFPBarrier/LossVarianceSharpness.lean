import AFPBarrier.LossVariance
import Mathlib.Tactic

/-!
# Equality, stability, and dual optimality for the AFP loss variance

This module turns the exact Gate 5 variance identity into:

* a complete equality characterization on every strictly active edge;
* an exact quantitative near-equality estimate;
* a tangent-line dual certificate for the fixed-rate/fixed-moment positive LP;
* an explicit optimality theorem showing that `O(h^2)` peak defect forces
  `Omega(h^-2)` outgoing rate for the spherical degree-one eigenvalue.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The weighted loss variance vanishes exactly when every strictly active edge
has loss equal to the chosen center. -/
theorem lossVarianceAt_eq_zero_iff_active_losses_eq
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (m : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j) :
    lossVarianceAt a f i m = 0 ↔
      ∀ j, j ≠ i → 0 < a i j → f i - f j = m := by
  constructor
  · intro hzero j hji hpos
    have hjmem : j ∈ offdiag i := by
      exact Finset.mem_erase.mpr ⟨hji, Finset.mem_univ j⟩
    have hnonneg : ∀ k ∈ offdiag i,
        0 ≤ a i k * ((f i - f k) - m) ^ 2 := by
      intro k hk
      have hki : k ≠ i := (Finset.mem_erase.mp hk).1
      exact mul_nonneg (ha k hki) (sq_nonneg _)
    unfold lossVarianceAt at hzero
    have hterm : a i j * ((f i - f j) - m) ^ 2 = 0 :=
      ((Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp hzero) j hjmem
    have hsquare : ((f i - f j) - m) ^ 2 = 0 :=
      (mul_eq_zero.mp hterm).resolve_left (ne_of_gt hpos)
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp hsquare)
  · intro hactive
    unfold lossVarianceAt
    apply Finset.sum_eq_zero
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    by_cases hz : a i j = 0
    · simp [hz]
    · have hpos : 0 < a i j :=
        lt_of_le_of_ne (ha j hji) (Ne.symm hz)
      have heq := hactive j hji hpos
      rw [heq]
      simp

/-- Equality in the defect--stiffness inequality is equivalent to constant loss
on every strictly active edge, for any center satisfying `m * rate = lam`. -/
theorem rate_mul_peakDefect_eq_eigenvalue_sq_iff_active_losses_eq
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam m : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i)
    (hm : m * jumpRate a i = lam) :
    jumpRate a i * peakDefect a f i lam = lam ^ 2 ↔
      ∀ j, j ≠ i → 0 < a i j → f i - f j = m := by
  have hgap := rate_mul_peakDefect_sub_eigenvalue_sq_eq_rate_mul_lossVariance
    a f i lam m hfi hlinear hm
  constructor
  · intro heq
    have hprod : jumpRate a i * lossVarianceAt a f i m = 0 := by
      rw [← hgap, heq]
      ring
    have hvar : lossVarianceAt a f i m = 0 :=
      (mul_eq_zero.mp hprod).resolve_left (ne_of_gt hrate)
    exact (lossVarianceAt_eq_zero_iff_active_losses_eq a f i m ha).mp hvar
  · intro hactive
    have hvar : lossVarianceAt a f i m = 0 :=
      (lossVarianceAt_eq_zero_iff_active_losses_eq a f i m ha).mpr hactive
    rw [hvar] at hgap
    linarith

/-- Quotient form of the equality characterization. -/
theorem rate_mul_peakDefect_eq_eigenvalue_sq_iff_active_losses_eq_mean
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i) :
    jumpRate a i * peakDefect a f i lam = lam ^ 2 ↔
      ∀ j, j ≠ i → 0 < a i j →
        f i - f j = lam / jumpRate a i := by
  have hm : (lam / jumpRate a i) * jumpRate a i = lam := by
    field_simp [ne_of_gt hrate]
  exact rate_mul_peakDefect_eq_eigenvalue_sq_iff_active_losses_eq
    a f i lam (lam / jumpRate a i) ha hfi hlinear hrate hm

/-- Every one-edge weighted squared deviation is bounded by the full weighted
variance. -/
theorem active_weight_mul_loss_deviation_sq_le_variance
    (a : ι → ι → ℝ) (f : ι → ℝ) (i j : ι) (m : ℝ)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hji : j ≠ i) :
    a i j * ((f i - f j) - m) ^ 2 ≤ lossVarianceAt a f i m := by
  unfold lossVarianceAt
  have hjmem : j ∈ offdiag i := by
    exact Finset.mem_erase.mpr ⟨hji, Finset.mem_univ j⟩
  exact Finset.single_le_sum
    (s := offdiag i)
    (f := fun k => a i k * ((f i - f k) - m) ^ 2)
    (fun k hk => by
      have hki : k ≠ i := (Finset.mem_erase.mp hk).1
      exact mul_nonneg (ha k hki) (sq_nonneg _))
    hjmem

/-- Exact quantitative stability: if the Cauchy--Schwarz gap is at most `eta`,
then the weighted loss variance about the mean-loss center is at most
`eta / rate`. -/
theorem lossVarianceAt_le_gap_div_rate
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam m eta : ℝ)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i)
    (hm : m * jumpRate a i = lam)
    (hgap : jumpRate a i * peakDefect a f i lam - lam ^ 2 ≤ eta) :
    lossVarianceAt a f i m ≤ eta / jumpRate a i := by
  apply (le_div_iff₀ hrate).2
  have hid := rate_mul_peakDefect_sub_eigenvalue_sq_eq_rate_mul_lossVariance
    a f i lam m hfi hlinear hm
  calc
    lossVarianceAt a f i m * jumpRate a i
        = jumpRate a i * lossVarianceAt a f i m := by ring
    _ = jumpRate a i * peakDefect a f i lam - lam ^ 2 := hid.symm
    _ ≤ eta := hgap

/-- Per-edge near-equality stability under a positive lower bound on the active
rate. -/
theorem minActiveRate_mul_loss_deviation_sq_le_gap_div_rate
    (a : ι → ι → ℝ) (f : ι → ℝ) (i j : ι)
    (lam m eta amin : ℝ)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hji : j ≠ i)
    (hamin : amin ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i)
    (hm : m * jumpRate a i = lam)
    (hgap : jumpRate a i * peakDefect a f i lam - lam ^ 2 ≤ eta) :
    amin * ((f i - f j) - m) ^ 2 ≤ eta / jumpRate a i := by
  have hsq0 : 0 ≤ ((f i - f j) - m) ^ 2 := sq_nonneg _
  have hweight :
      amin * ((f i - f j) - m) ^ 2
        ≤ a i j * ((f i - f j) - m) ^ 2 :=
    mul_le_mul_of_nonneg_right hamin hsq0
  exact hweight.trans <| (active_weight_mul_loss_deviation_sq_le_variance
    a f i j m ha hji).trans <| lossVarianceAt_le_gap_div_rate
      a f i lam m eta hfi hlinear hrate hm hgap

/-- Tangent-line dual certificate for the positive fixed-rate/fixed-moment LP:
any center `m` gives a valid lower bound on the peak defect. -/
theorem peakDefect_dual_tangent_lower_bound
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam m : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    2 * m * lam - m ^ 2 * jumpRate a i ≤ peakDefect a f i lam := by
  have hid := peakDefect_centered_loss_identity
    a f i lam m hfi hlinear
  have hvar := lossVarianceAt_nonneg a f i m ha
  linarith

/-- The universal lower bound is the optimal value of the relaxed positive-rate
row problem with fixed total rate and fixed first loss moment. -/
theorem peakDefect_ge_eigenvalue_sq_div_rate_via_dual
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hrate : 0 < jumpRate a i) :
    lam ^ 2 / jumpRate a i ≤ peakDefect a f i lam := by
  have hdual := peakDefect_dual_tangent_lower_bound
    a f i lam (lam / jumpRate a i) ha hfi hlinear
  have hform :
      2 * (lam / jumpRate a i) * lam
          - (lam / jumpRate a i) ^ 2 * jumpRate a i
        = lam ^ 2 / jumpRate a i := by
    field_simp [ne_of_gt hrate]
    ring
  rw [hform] at hdual
  exact hdual

/-- Asymptotic optimality on `S²`: an `O(h²)` defect bound forces an
`Omega(h⁻²)` total outgoing rate. -/
theorem S2_rate_lower_of_peakDefect_upper
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (C h : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -(2 : ℝ))
    (hC : 0 < C) (hh : 0 < h)
    (hdef : peakDefect a f i 2 ≤ C * h ^ 2) :
    4 / (C * h ^ 2) ≤ jumpRate a i := by
  have hbase := eigenvalue_sq_le_rate_mul_peakDefect
    a f i 2 ha hfi hlinear
  have hrate0 := jumpRate_nonneg a i ha
  have hmul :
      jumpRate a i * peakDefect a f i 2
        ≤ jumpRate a i * (C * h ^ 2) :=
    mul_le_mul_of_nonneg_left hdef hrate0
  have hfour : 4 ≤ jumpRate a i * (C * h ^ 2) := by
    nlinarith
  have hden : 0 < C * h ^ 2 := mul_pos hC (sq_pos_of_pos hh)
  apply (div_le_iff₀ hden).2
  simpa [mul_comm, mul_left_comm, mul_assoc] using hfour

end AFPBarrier
