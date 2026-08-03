import AFPBarrier.SphericalQEqualityRigidity
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
# Quantitative graph-global near-rigidity

This module formalizes the finite scalar inequalities used before the ordinary
path, spectral-gap, effective-resistance, and spherical-angle arguments.
-/

namespace AFPBarrier

/-- A single positive weight controls one squared deviation in a nonnegative
weighted variance. -/
theorem weight_floor_mul_deviation_sq_le
    (p kappa x eta : ℝ)
    (hp : kappa ≤ p)
    (hsq : 0 ≤ (x - 1) ^ 2)
    (hweighted : p * (x - 1) ^ 2 ≤ eta) :
    kappa * (x - 1) ^ 2 ≤ eta := by
  exact (mul_le_mul_of_nonneg_right hp hsq).trans hweighted

/-- Explicit pointwise near-equality estimate in square form. -/
theorem pointwise_deviation_sq_le_eta_div_kappa
    (p kappa x eta : ℝ)
    (hkappa : 0 < kappa)
    (hp : kappa ≤ p)
    (hweighted : p * (x - 1) ^ 2 ≤ eta) :
    (x - 1) ^ 2 ≤ eta / kappa := by
  apply (le_div_iff₀ hkappa).2
  simpa [mul_comm] using
    weight_floor_mul_deviation_sq_le
      p kappa x eta hp (sq_nonneg _) hweighted

/-- Square control gives the advertised absolute deviation. -/
theorem pointwise_delta_bound
    (p kappa x eta delta : ℝ)
    (hkappa : 0 < kappa)
    (hp : kappa ≤ p)
    (hweighted : p * (x - 1) ^ 2 ≤ eta)
    (hdelta : 0 ≤ delta)
    (hdeltaSq : eta / kappa = delta ^ 2) :
    |x - 1| ≤ delta := by
  have hsquare : (x - 1) ^ 2 ≤ delta ^ 2 := by
    rw [← hdeltaSq]
    exact pointwise_deviation_sq_le_eta_div_kappa
      p kappa x eta hkappa hp hweighted
  nlinarith [sq_abs (x - 1)]

/-- Shared-edge normalized scales yield the cross-multiplied adjacent-rate
bounds. -/
theorem adjacent_rate_cross_bounds
    (rateI rateJ ell xI xJ delta : ℝ)
    (hrateI : 0 < rateI) (hrateJ : 0 < rateJ)
    (hell : 0 < ell)
    (hscaleI : xI = rateI * ell / 2)
    (hscaleJ : xJ = rateJ * ell / 2)
    (hxILo : 1 - delta ≤ xI) (hxIHi : xI ≤ 1 + delta)
    (hxJLo : 1 - delta ≤ xJ) (hxJHi : xJ ≤ 1 + delta) :
    (1 - delta) * rateJ ≤ (1 + delta) * rateI ∧
      (1 - delta) * rateI ≤ (1 + delta) * rateJ := by
  have hratioI : rateI = 2 * xI / ell := by
    rw [hscaleI]
    field_simp [ne_of_gt hell]
  have hratioJ : rateJ = 2 * xJ / ell := by
    rw [hscaleJ]
    field_simp [ne_of_gt hell]
  have hxIpos : 0 < xI := by
    rw [hscaleI]
    positivity
  have hxJpos : 0 < xJ := by
    rw [hscaleJ]
    positivity
  have hnumIJ : (1 - delta) * (2 * xJ) ≤ (1 + delta) * (2 * xI) := by
    have hleft : (1 - delta) * xJ ≤ xI * xJ :=
      mul_le_mul_of_nonneg_right hxILo (le_of_lt hxJpos)
    have hright : xI * xJ ≤ xI * (1 + delta) :=
      mul_le_mul_of_nonneg_left hxJHi (le_of_lt hxIpos)
    nlinarith
  have hnumJI : (1 - delta) * (2 * xI) ≤ (1 + delta) * (2 * xJ) := by
    have hleft : (1 - delta) * xI ≤ xJ * xI :=
      mul_le_mul_of_nonneg_right hxJLo (le_of_lt hxIpos)
    have hright : xJ * xI ≤ xJ * (1 + delta) :=
      mul_le_mul_of_nonneg_left hxIHi (le_of_lt hxJpos)
    nlinarith
  have hinv : 0 ≤ ell⁻¹ := le_of_lt (inv_pos.mpr hell)
  constructor
  · calc
      (1 - delta) * rateJ
          = ((1 - delta) * (2 * xJ)) * ell⁻¹ := by
              rw [hratioJ]
              ring
      _ ≤ ((1 + delta) * (2 * xI)) * ell⁻¹ :=
        mul_le_mul_of_nonneg_right hnumIJ hinv
      _ = (1 + delta) * rateI := by
              rw [hratioI]
              ring
  · calc
      (1 - delta) * rateI
          = ((1 - delta) * (2 * xI)) * ell⁻¹ := by
              rw [hratioI]
              ring
      _ ≤ ((1 + delta) * (2 * xJ)) * ell⁻¹ :=
        mul_le_mul_of_nonneg_right hnumJI hinv
      _ = (1 + delta) * rateJ := by
              rw [hratioJ]
              ring

/-- Ratio form of the adjacent-rate estimate. -/
theorem adjacent_rate_ratio_bounds
    (rateI rateJ ell xI xJ delta : ℝ)
    (hrateI : 0 < rateI) (hrateJ : 0 < rateJ)
    (hell : 0 < ell)
    (hdelta : 0 ≤ delta) (hdeltaOne : delta < 1)
    (hscaleI : xI = rateI * ell / 2)
    (hscaleJ : xJ = rateJ * ell / 2)
    (hxILo : 1 - delta ≤ xI) (hxIHi : xI ≤ 1 + delta)
    (hxJLo : 1 - delta ≤ xJ) (hxJHi : xJ ≤ 1 + delta) :
    (1 - delta) / (1 + delta) ≤ rateI / rateJ ∧
      rateI / rateJ ≤ (1 + delta) / (1 - delta) := by
  have hcross := adjacent_rate_cross_bounds
    rateI rateJ ell xI xJ delta hrateI hrateJ hell
    hscaleI hscaleJ hxILo hxIHi hxJLo hxJHi
  have hplus : 0 < 1 + delta := by linarith
  have hminus : 0 < 1 - delta := by linarith
  constructor
  · apply (div_le_div_iff₀ hplus hrateJ).2
    simpa [mul_comm] using hcross.1
  · apply (div_le_div_iff₀ hrateJ hminus).2
    simpa [mul_comm] using hcross.2

/-- Two normalized scales at one state give incident-edge loss control. -/
theorem incident_loss_cross_bounds
    (ell₁ ell₂ x₁ x₂ rate delta : ℝ)
    (hrate : 0 < rate)
    (hdelta : 0 ≤ delta) (hdeltaOne : delta < 1)
    (hbalance₁ : rate * ell₁ = 2 * x₁)
    (hbalance₂ : rate * ell₂ = 2 * x₂)
    (hx₁Lo : 1 - delta ≤ x₁) (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂) (hx₂Hi : x₂ ≤ 1 + delta) :
    (1 - delta) * ell₂ ≤ (1 + delta) * ell₁ ∧
      (1 - delta) * ell₁ ≤ (1 + delta) * ell₂ := by
  have hrne : rate ≠ 0 := ne_of_gt hrate
  have hell₁ : ell₁ = 2 * x₁ / rate := by
    apply (eq_div_iff hrne).2
    nlinarith [hbalance₁]
  have hell₂ : ell₂ = 2 * x₂ / rate := by
    apply (eq_div_iff hrne).2
    nlinarith [hbalance₂]
  have hminus : 0 ≤ 1 - delta := by linarith
  have hplus : 0 ≤ 1 + delta := by linarith
  have hnum₁ : (1 - delta) * (2 * x₂) ≤ (1 + delta) * (2 * x₁) := by
    have ha := mul_le_mul_of_nonneg_left hx₂Hi hminus
    have hb := mul_le_mul_of_nonneg_right hx₁Lo hplus
    nlinarith
  have hnum₂ : (1 - delta) * (2 * x₁) ≤ (1 + delta) * (2 * x₂) := by
    have ha := mul_le_mul_of_nonneg_left hx₁Hi hminus
    have hb := mul_le_mul_of_nonneg_right hx₂Lo hplus
    nlinarith
  have hinv : 0 ≤ rate⁻¹ := le_of_lt (inv_pos.mpr hrate)
  constructor
  · calc
      (1 - delta) * ell₂
          = ((1 - delta) * (2 * x₂)) * rate⁻¹ := by
              rw [hell₂]
              ring
      _ ≤ ((1 + delta) * (2 * x₁)) * rate⁻¹ :=
        mul_le_mul_of_nonneg_right hnum₁ hinv
      _ = (1 + delta) * ell₁ := by
              rw [hell₁]
              ring
  · calc
      (1 - delta) * ell₁
          = ((1 - delta) * (2 * x₁)) * rate⁻¹ := by
              rw [hell₁]
              ring
      _ ≤ ((1 + delta) * (2 * x₂)) * rate⁻¹ :=
        mul_le_mul_of_nonneg_right hnum₂ hinv
      _ = (1 + delta) * ell₂ := by
              rw [hell₂]
              ring

/-- Exact radial covariance error identity in terms of `Q-1`. -/
theorem radial_covariance_error_identity
    (Q rate : ℝ) (hrate : 0 < rate) :
    4 * Q / rate - 4 / rate = 4 * (Q - 1) / rate := by
  field_simp [ne_of_gt hrate]

/-- Near equality controls the radial covariance component, and only that
component without an additional tangential-isotropy hypothesis. -/
theorem radial_covariance_error_bounds
    (Q rate eta : ℝ)
    (hrate : 0 < rate)
    (hQlo : 1 ≤ Q) (hQhi : Q ≤ 1 + eta) :
    0 ≤ 4 * Q / rate - 4 / rate ∧
      4 * Q / rate - 4 / rate ≤ 4 * eta / rate := by
  rw [radial_covariance_error_identity Q rate hrate]
  constructor
  · exact div_nonneg (mul_nonneg (by norm_num) (sub_nonneg.mpr hQlo)) hrate.le
  · apply (div_le_div_iff₀ hrate hrate).2
    nlinarith

end AFPBarrier
