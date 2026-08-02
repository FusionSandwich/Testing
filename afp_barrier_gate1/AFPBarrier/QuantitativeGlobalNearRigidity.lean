import AFPBarrier.SphericalQEqualityRigidity
import Mathlib.Tactic

/-!
# Finite algebra for quantitative global near-rigidity

This module checks the pointwise defect transfer and adjacent shared-edge
ratio algebra.  Path, logarithmic, Poincare, resistance, and spherical-angle
transfers are proved with explicit constants in the ordinary theorem document.
-/

namespace AFPBarrier

/-- A squared deviation bound gives the corresponding absolute bound. -/
theorem abs_sub_one_le_of_sq_le_delta_sq
    (x delta : ℝ)
    (hdelta : 0 ≤ delta)
    (hsq : (x - 1) ^ 2 ≤ delta ^ 2) :
    |x - 1| ≤ delta := by
  rw [abs_le]
  constructor <;>
    nlinarith [sq_nonneg (x - 1 - delta), sq_nonneg (x - 1 + delta)]

/-- One weighted variance term and a lower probability bound imply the Prompt 3
pointwise `delta` estimate. -/
theorem pointwise_delta_bound
    (p x kappa eta delta : ℝ)
    (hkappa : 0 < kappa)
    (hp : kappa ≤ p)
    (hterm : p * (x - 1) ^ 2 ≤ eta)
    (heta : eta = kappa * delta ^ 2)
    (hdelta : 0 ≤ delta) :
    |x - 1| ≤ delta := by
  have hweight :
      kappa * (x - 1) ^ 2 ≤ p * (x - 1) ^ 2 :=
    mul_le_mul_of_nonneg_right hp (sq_nonneg _)
  have hscaled : kappa * (x - 1) ^ 2 ≤ kappa * delta ^ 2 := by
    calc
      kappa * (x - 1) ^ 2 ≤ p * (x - 1) ^ 2 := hweight
      _ ≤ eta := hterm
      _ = kappa * delta ^ 2 := heta
  have hsq : (x - 1) ^ 2 ≤ delta ^ 2 :=
    (mul_le_mul_left hkappa).mp hscaled
  exact abs_sub_one_le_of_sq_le_delta_sq x delta hdelta hsq

/-- Absolute pointwise control is equivalent to the two-sided normalized edge
scale interval used throughout Prompt 3. -/
theorem normalized_scale_interval_of_abs
    (x delta : ℝ)
    (habs : |x - 1| ≤ delta) :
    1 - delta ≤ x ∧ x ≤ 1 + delta := by
  have h := (abs_le.mp habs)
  constructor <;> linarith

/-- Shared-edge balance plus local normalized-scale bounds gives the
cross-multiplied adjacent rate bounds. -/
theorem adjacent_rate_cross_bounds
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 ≤ r_i) (hrj : 0 ≤ r_j)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    (1 - delta) * r_j ≤ (1 + delta) * r_i ∧
      (1 - delta) * r_i ≤ (1 + delta) * r_j := by
  constructor
  · calc
      (1 - delta) * r_j ≤ x_ij * r_j :=
        mul_le_mul_of_nonneg_right hijLo hrj
      _ = x_ji * r_i := by
        simpa [mul_comm] using hbalance
      _ ≤ (1 + delta) * r_i :=
        mul_le_mul_of_nonneg_right hjiHi hri
  · calc
      (1 - delta) * r_i ≤ x_ji * r_i :=
        mul_le_mul_of_nonneg_right hjiLo hri
      _ = x_ij * r_j := by
        simpa [mul_comm] using hbalance.symm
      _ ≤ (1 + delta) * r_j :=
        mul_le_mul_of_nonneg_right hijHi hrj

/-- Division form of the adjacent Prompt 3 rate-ratio estimate. -/
theorem adjacent_rate_ratio_bounds
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    (1 - delta) / (1 + delta) ≤ r_i / r_j ∧
      r_i / r_j ≤ (1 + delta) / (1 - delta) := by
  have hcross := adjacent_rate_cross_bounds
    r_i r_j x_ij x_ji delta (le_of_lt hri) (le_of_lt hrj)
    hijLo hijHi hjiLo hjiHi hbalance
  have hplus : 0 < 1 + delta := by linarith
  have hminus : 0 < 1 - delta := by linarith
  constructor
  · apply (div_le_div_iff₀ hplus hrj).2
    simpa [mul_comm] using hcross.1
  · apply (div_le_div_iff₀ hrj hminus).2
    simpa [mul_comm] using hcross.2

/-- The local edge-loss ratio at one vertex is bounded by the same adjacent
normalized-scale cross inequalities. -/
theorem incident_loss_cross_bounds
    (ell₁ ell₂ x₁ x₂ rate delta : ℝ)
    (hrate : 0 < rate)
    (hbalance₁ : rate * ell₁ = 2 * x₁)
    (hbalance₂ : rate * ell₂ = 2 * x₂)
    (hx₁Lo : 1 - delta ≤ x₁)
    (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂)
    (hx₂Hi : x₂ ≤ 1 + delta) :
    (1 - delta) * ell₂ ≤ (1 + delta) * ell₁ ∧
      (1 - delta) * ell₁ ≤ (1 + delta) * ell₂ := by
  have hrnonneg : 0 ≤ rate := le_of_lt hrate
  constructor
  · have h : (1 - delta) * (rate * ell₂) ≤
        (1 + delta) * (rate * ell₁) := by
      rw [hbalance₁, hbalance₂]
      nlinarith
    nlinarith
  · have h : (1 - delta) * (rate * ell₁) ≤
        (1 + delta) * (rate * ell₂) := by
      rw [hbalance₁, hbalance₂]
      nlinarith
    nlinarith

/-- Algebraic radial near-equality estimate used by the covariance transfer. -/
theorem radial_covariance_error_bounds
    (Q rate eta : ℝ)
    (hrate : 0 < rate)
    (hQlower : 1 ≤ Q)
    (hQupper : Q ≤ 1 + eta) :
    0 ≤ 4 * Q / rate - 4 / rate ∧
      4 * Q / rate - 4 / rate ≤ 4 * eta / rate := by
  have hrne : rate ≠ 0 := ne_of_gt hrate
  have hrearrange :
      4 * Q / rate - 4 / rate = (4 * Q - 4) / rate := by
    field_simp [hrne]
    ring
  rw [hrearrange]
  constructor
  · exact div_nonneg (by nlinarith) (le_of_lt hrate)
  · apply (div_le_div_iff₀ hrate hrate).2
    nlinarith

end AFPBarrier
