import AFPBarrier.Quantitative

/-!
# Local loss bounds for quasi-uniform angular graphs

At a normalized peak, write the edge loss as

  ell_ij = f(i) - f(j).

If a positive jump generator reproduces the degree-one eigenvalue `-lam`, then

  sum_j a_ij ell_ij = lam.

When every active edge loss lies in `[ellMin, ellMax]`, the total rate and the
unavoidable square defect satisfy the sharp interval bounds

  ellMin * rate <= lam <= ellMax * rate,
  ellMin * lam  <= defect <= ellMax * lam.

For spherical zonal modes, `lam = 2` and `ell_ij = 1 - Omega_i dot Omega_j`.
Thus a quasi-uniform graph with `ell_ij = Theta(h^2)` automatically has
`rate = Theta(h^-2)` and peak defect `Theta(h^2)`.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The first positive loss moment equals the intended eigenvalue. -/
theorem lossMoment_eq_eigenvalue
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (hlinear : jumpGenerator a f i = -lam) :
    (offdiag i).sum (fun j => a i j * (f i - f j)) = lam := by
  unfold jumpGenerator at hlinear
  calc
    (offdiag i).sum (fun j => a i j * (f i - f j))
        = -((offdiag i).sum (fun j => a i j * (f j - f i))) := by
            rw [← Finset.sum_neg_distrib]
            apply Finset.sum_congr rfl
            intro j hj
            ring
    _ = lam := by rw [hlinear]; ring

/-- A lower edge-loss bound gives a lower bound on `lam` in terms of the rate. -/
theorem lossMin_mul_rate_le_eigenvalue
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam ellMin : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlower : ∀ j, j ≠ i → ellMin ≤ f i - f j)
    (hlinear : jumpGenerator a f i = -lam) :
    ellMin * jumpRate a i ≤ lam := by
  rw [← lossMoment_eq_eigenvalue (a := a) (f := f) (i := i) (lam := lam) hlinear]
  unfold jumpRate
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j hj
  have hji : j ≠ i := (Finset.mem_erase.mp hj).1
  have hrate : 0 ≤ a i j := ha j hji
  have h := mul_le_mul_of_nonneg_left (hlower j hji) hrate
  simpa [mul_comm, mul_left_comm, mul_assoc] using h

/-- An upper edge-loss bound gives an upper bound on `lam` in terms of the rate. -/
theorem eigenvalue_le_lossMax_mul_rate
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam ellMax : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hupper : ∀ j, j ≠ i → f i - f j ≤ ellMax)
    (hlinear : jumpGenerator a f i = -lam) :
    lam ≤ ellMax * jumpRate a i := by
  rw [← lossMoment_eq_eigenvalue (a := a) (f := f) (i := i) (lam := lam) hlinear]
  unfold jumpRate
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j hj
  have hji : j ≠ i := (Finset.mem_erase.mp hj).1
  have hrate : 0 ≤ a i j := ha j hji
  have h := mul_le_mul_of_nonneg_left (hupper j hji) hrate
  simpa [mul_comm, mul_left_comm, mul_assoc] using h

/-- The lower edge-loss bound also controls the unavoidable square defect. -/
theorem lossMin_mul_eigenvalue_le_peakDefect
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam ellMin : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hellMin : 0 ≤ ellMin)
    (hlower : ∀ j, j ≠ i → ellMin ≤ f i - f j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    ellMin * lam ≤ peakDefect a f i lam := by
  rw [peakDefect_eq_carreDuChamp
    (a := a) (f := f) (i := i) (lam := lam) hfi hlinear]
  rw [← lossMoment_eq_eigenvalue (a := a) (f := f) (i := i) (lam := lam) hlinear]
  unfold carreDuChamp
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j hj
  have hji : j ≠ i := (Finset.mem_erase.mp hj).1
  have hrate : 0 ≤ a i j := ha j hji
  have hloss : 0 ≤ f i - f j := le_trans hellMin (hlower j hji)
  have hprod : ellMin * (f i - f j) ≤ (f i - f j) * (f i - f j) :=
    mul_le_mul_of_nonneg_right (hlower j hji) hloss
  have hscaled := mul_le_mul_of_nonneg_left hprod hrate
  nlinarith

/-- The upper edge-loss bound gives the matching upper defect estimate. -/
theorem peakDefect_le_lossMax_mul_eigenvalue
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam ellMin ellMax : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hellMin : 0 ≤ ellMin)
    (hlower : ∀ j, j ≠ i → ellMin ≤ f i - f j)
    (hupper : ∀ j, j ≠ i → f i - f j ≤ ellMax)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    peakDefect a f i lam ≤ ellMax * lam := by
  rw [peakDefect_eq_carreDuChamp
    (a := a) (f := f) (i := i) (lam := lam) hfi hlinear]
  rw [← lossMoment_eq_eigenvalue (a := a) (f := f) (i := i) (lam := lam) hlinear]
  unfold carreDuChamp
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j hj
  have hji : j ≠ i := (Finset.mem_erase.mp hj).1
  have hrate : 0 ≤ a i j := ha j hji
  have hloss : 0 ≤ f i - f j := le_trans hellMin (hlower j hji)
  have hprod : (f i - f j) * (f i - f j) ≤ ellMax * (f i - f j) :=
    mul_le_mul_of_nonneg_right (hupper j hji) hloss
  have hscaled := mul_le_mul_of_nonneg_left hprod hrate
  nlinarith

/-- Combined local quasi-uniform bounds. -/
theorem quasiUniform_loss_rate_defect_bounds
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam ellMin ellMax : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hellMin : 0 ≤ ellMin)
    (hlower : ∀ j, j ≠ i → ellMin ≤ f i - f j)
    (hupper : ∀ j, j ≠ i → f i - f j ≤ ellMax)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    ellMin * jumpRate a i ≤ lam
      ∧ lam ≤ ellMax * jumpRate a i
      ∧ ellMin * lam ≤ peakDefect a f i lam
      ∧ peakDefect a f i lam ≤ ellMax * lam := by
  exact ⟨
    lossMin_mul_rate_le_eigenvalue a f i lam ellMin ha hlower hlinear,
    eigenvalue_le_lossMax_mul_rate a f i lam ellMax ha hupper hlinear,
    lossMin_mul_eigenvalue_le_peakDefect a f i lam ellMin ha hellMin hlower hfi hlinear,
    peakDefect_le_lossMax_mul_eigenvalue a f i lam ellMin ellMax
      ha hellMin hlower hupper hfi hlinear⟩

end AFPBarrier
