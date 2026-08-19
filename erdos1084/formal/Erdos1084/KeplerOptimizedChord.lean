import Mathlib
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Optimized convex-chord envelope at the Kepler radius

This file proves the new local algebra used at

`kpRadius = (40 + 22 * sqrt 3) / 37`.

For the equal-area comparison-cap cosine `x`, define

`H(x) = 1 + x cos(s) - sqrt(1-x^2) sin(s)`.

The degree-eleven and degree-one endpoint charges agree exactly at the optimized radius. The
upper semicircle is concave, so `H` lies below the affine chord through those endpoint values.
Concavity is proved algebraically from an exact unit-circle interpolation identity; no calculus,
trigonometric axiom, or project-specific axiom is introduced.
-/

noncomputable section

/-- Positive upper-semicircle height at the degree-eleven endpoint. -/
def kpLowerY : ℝ := Real.sqrt (1 - rtLower ^ 2)

/-- Upper-semicircle height at the degree-one endpoint. -/
def kpUpperY : ℝ := 1 / 2

/-- Cosine of the angular dilation `s = arccos(1/r_*) - pi/6`. -/
def kpCosShift : ℝ :=
  rtUpper / kpRadius + kpLowerY / 2

/-- Sine of the angular dilation `s = arccos(1/r_*) - pi/6`. -/
def kpSinShift : ℝ :=
  rtUpper * kpLowerY - (1 / kpRadius) / 2

/-- Normalized exposed-area quantity at the optimized radius. -/
def kpOptimizedH (x : ℝ) : ℝ :=
  1 + x * kpCosShift - Real.sqrt (1 - x ^ 2) * kpSinShift

/-- Chord through the degree-eleven and degree-one endpoint values. -/
def kpOptimizedChord (x : ℝ) : ℝ :=
  x + 11 - 6 * rtS

/-- Barycentric weight of the lower endpoint. -/
def kpWeightLower (x : ℝ) : ℝ :=
  (rtUpper - x) / (rtUpper - rtLower)

/-- Barycentric weight of the upper endpoint. -/
def kpWeightUpper (x : ℝ) : ℝ :=
  (x - rtLower) / (rtUpper - rtLower)

/-- Linear interpolation of the endpoint semicircle heights. -/
def kpInterpolatedY (x : ℝ) : ℝ :=
  kpWeightLower x * kpLowerY + kpWeightUpper x * kpUpperY

/-- `kpQ` is exactly `1 - rtUpper`. -/
theorem kpQ_eq_one_sub_rtUpper : kpQ = 1 - rtUpper := by
  rfl

/-- The optimized reciprocal radius is the negative lower endpoint. -/
theorem kpRadius_reciprocal_eq_neg_lower :
    1 / kpRadius = -rtLower := by
  rw [kpRadius_reciprocal]
  dsimp [kpS, rtLower, rtS]
  ring

/-- Formula for the cosine shift after substituting the optimized reciprocal radius. -/
theorem kpCosShift_formula :
    kpCosShift = rtUpper * (-rtLower) + kpLowerY / 2 := by
  have hinv : kpRadius⁻¹ = -rtLower := by
    simpa [one_div] using kpRadius_reciprocal_eq_neg_lower
  rw [kpCosShift, div_eq_mul_inv, hinv]

/-- Formula for the sine shift after substituting the optimized reciprocal radius. -/
theorem kpSinShift_formula :
    kpSinShift = rtUpper * kpLowerY + rtLower / 2 := by
  rw [kpSinShift, kpRadius_reciprocal_eq_neg_lower]
  ring

/-- The degree interval has positive width. -/
theorem kp_degree_interval_width_pos :
    0 < rtUpper - rtLower := by
  dsimp [rtUpper, rtLower]
  linarith [rtS_lt_two]

/-- The upper endpoint has square `3/4`. -/
theorem kp_rtUpper_sq : rtUpper ^ 2 = (3 / 4 : ℝ) := by
  dsimp [rtUpper]
  nlinarith [rtS_sq]

/-- The upper endpoint is positive. -/
theorem kp_rtUpper_pos : 0 < rtUpper := by
  dsimp [rtUpper]
  exact div_pos rtS_pos (by norm_num)

/-- The lower endpoint lies below zero. -/
theorem kp_rtLower_lt_zero : rtLower < 0 := by
  have hs0 : 0 ≤ rtS := rtS_nonneg
  have hs2 : rtS ^ 2 = 3 := rtS_sq
  have h20 : 11 * rtS < 20 := by
    nlinarith
  dsimp [rtLower]
  linarith

/-- The lower endpoint lies strictly above `-1/2`. -/
theorem kp_neg_half_lt_rtLower : (-1 / 2 : ℝ) < rtLower := by
  have h19 := nineteen_lt_eleven_sqrt_three
  dsimp [rtLower, rtS] at h19 ⊢
  linarith

/-- The lower endpoint has square strictly below one quarter. -/
theorem kp_rtLower_sq_lt_quarter :
    rtLower ^ 2 < (1 / 2 : ℝ) ^ 2 := by
  have hU : rtLower < (1 / 2 : ℝ) := by
    linarith [kp_rtLower_lt_zero]
  have hp : 0 < ((1 / 2 : ℝ) - rtLower) * ((1 / 2 : ℝ) + rtLower) :=
    mul_pos (sub_pos.mpr hU) (by linarith [kp_neg_half_lt_rtLower])
  nlinarith

@[simp] theorem kpLowerY_nonneg : 0 ≤ kpLowerY := by
  exact Real.sqrt_nonneg _

@[simp] theorem kpUpperY_nonneg : 0 ≤ kpUpperY := by
  norm_num [kpUpperY]

/-- The lower endpoint lies on the unit semicircle. -/
theorem kpLowerY_sq :
    kpLowerY ^ 2 = 1 - rtLower ^ 2 := by
  have hLU : rtLower ≤ rtUpper :=
    le_of_lt (sub_pos.mp kp_degree_interval_width_pos)
  have hrad : 0 ≤ 1 - rtLower ^ 2 :=
    rtRad_nonneg le_rfl hLU
  exact Real.sq_sqrt hrad

/-- The lower square root is definitionally `kpLowerY`. -/
theorem kp_sqrt_lower :
    Real.sqrt (1 - rtLower ^ 2) = kpLowerY := by
  rfl

/-- The upper endpoint lies on the unit semicircle. -/
theorem kpUpperY_sq :
    kpUpperY ^ 2 = 1 - rtUpper ^ 2 := by
  rw [kp_rtUpper_sq]
  norm_num [kpUpperY]

/-- The actual square root at the upper endpoint equals `1/2`. -/
theorem kp_sqrt_upper :
    Real.sqrt (1 - rtUpper ^ 2) = kpUpperY := by
  have hrad : 0 ≤ 1 - rtUpper ^ 2 := by
    have hLL : rtLower ≤ rtUpper :=
      le_of_lt (sub_pos.mp kp_degree_interval_width_pos)
    exact rtRad_nonneg hLL le_rfl
  have hsquare := Real.sq_sqrt hrad
  have hs0 := Real.sqrt_nonneg (1 - rtUpper ^ 2)
  have hy0 := kpUpperY_nonneg
  have hy2 := kpUpperY_sq
  nlinarith

/-- The lower semicircle height is strictly larger than `rtUpper`. -/
theorem kpLowerY_gt_rtUpper : rtUpper < kpLowerY := by
  have hsq : rtUpper ^ 2 < kpLowerY ^ 2 := by
    rw [kpLowerY_sq, kp_rtUpper_sq]
    nlinarith [kp_rtLower_sq_lt_quarter]
  by_contra hnot
  have hle : kpLowerY ≤ rtUpper := le_of_not_gt hnot
  have hprod : 0 ≤ (rtUpper - kpLowerY) * (rtUpper + kpLowerY) :=
    mul_nonneg (sub_nonneg.mpr hle)
      (add_nonneg (le_of_lt kp_rtUpper_pos) kpLowerY_nonneg)
  have hsqle : kpLowerY ^ 2 ≤ rtUpper ^ 2 := by
    nlinarith
  exact (not_lt_of_ge hsqle) hsq

/-- The lower semicircle height is larger than the upper endpoint height `1/2`. -/
theorem kpLowerY_gt_upperY : kpUpperY < kpLowerY := by
  have hUpperYlt : kpUpperY < rtUpper := by
    have hsOne : 1 < rtS := by
      have hs0 := rtS_nonneg
      have hs2 := rtS_sq
      nlinarith
    dsimp [kpUpperY, rtUpper]
    linarith
  exact lt_trans hUpperYlt kpLowerY_gt_rtUpper

/-- The angular dilation sine is strictly positive. -/
theorem kpSinShift_pos : 0 < kpSinShift := by
  have hprod : rtUpper ^ 2 < rtUpper * kpLowerY := by
    have h := mul_lt_mul_of_pos_left kpLowerY_gt_rtUpper kp_rtUpper_pos
    simpa [pow_two] using h
  rw [kpSinShift_formula]
  nlinarith [kp_rtUpper_sq, kp_neg_half_lt_rtLower]

/-- The lower endpoint value is exactly the common charge `q`. -/
theorem kpOptimizedH_lower :
    kpOptimizedH rtLower = kpQ := by
  rw [kpOptimizedH, kp_sqrt_lower, kpCosShift_formula, kpSinShift_formula]
  rw [kpQ_eq_one_sub_rtUpper]
  have hcircle : rtLower ^ 2 + kpLowerY ^ 2 = 1 := by
    rw [kpLowerY_sq]
    ring
  calc
    1 + rtLower * (rtUpper * -rtLower + kpLowerY / 2) -
        kpLowerY * (rtUpper * kpLowerY + rtLower / 2) =
      1 - rtUpper * (rtLower ^ 2 + kpLowerY ^ 2) := by ring
    _ = 1 - rtUpper := by rw [hcircle]; ring

/-- The lower endpoint is affine in the upper endpoint. -/
theorem kp_rtLower_linear : rtLower = 11 * rtUpper - 10 := by
  dsimp [rtLower, rtUpper]
  ring

/-- The upper endpoint value is exactly eleven times the common charge. -/
theorem kpOptimizedH_upper :
    kpOptimizedH rtUpper = 11 * kpQ := by
  rw [kpOptimizedH, kp_sqrt_upper, kpCosShift_formula, kpSinShift_formula]
  rw [kpQ_eq_one_sub_rtUpper]
  dsimp [kpUpperY]
  calc
    1 + rtUpper * (rtUpper * -rtLower + kpLowerY / 2) -
        (1 / 2 : ℝ) * (rtUpper * kpLowerY + rtLower / 2) =
      1 - rtLower * (rtUpper ^ 2 + 1 / 4) := by ring
    _ = 1 - rtLower := by rw [kp_rtUpper_sq]; ring
    _ = 11 * (1 - rtUpper) := by rw [kp_rtLower_linear]; ring

/-- The affine chord has the same lower endpoint value. -/
theorem kpOptimizedChord_lower :
    kpOptimizedChord rtLower = kpQ := by
  dsimp [kpOptimizedChord, kpQ, kpS, rtLower, rtUpper, rtS]
  ring

/-- The affine chord has the same upper endpoint value. -/
theorem kpOptimizedChord_upper :
    kpOptimizedChord rtUpper = 11 * kpQ := by
  dsimp [kpOptimizedChord, kpQ, kpS, rtUpper, rtS]
  ring

/-- The barycentric weights add to one. -/
theorem kp_weights_sum (x : ℝ) :
    kpWeightLower x + kpWeightUpper x = 1 := by
  have hwne : rtUpper - rtLower ≠ 0 :=
    ne_of_gt kp_degree_interval_width_pos
  dsimp [kpWeightLower, kpWeightUpper]
  field_simp [hwne]
  ring

/-- The cosine parameter is the barycentric interpolation of the two endpoints. -/
theorem kp_barycentric_x (x : ℝ) :
    kpWeightLower x * rtLower + kpWeightUpper x * rtUpper = x := by
  have hwne : rtUpper - rtLower ≠ 0 :=
    ne_of_gt kp_degree_interval_width_pos
  dsimp [kpWeightLower, kpWeightUpper]
  field_simp [hwne]
  ring

/-- The affine chord is its own endpoint interpolation. -/
theorem kp_chord_barycentric (x : ℝ) :
    kpWeightLower x * kpOptimizedChord rtLower +
        kpWeightUpper x * kpOptimizedChord rtUpper =
      kpOptimizedChord x := by
  have hs := kp_weights_sum x
  have hx := kp_barycentric_x x
  dsimp [kpOptimizedChord]
  calc
    kpWeightLower x * (rtLower + 11 - 6 * rtS) +
        kpWeightUpper x * (rtUpper + 11 - 6 * rtS) =
      (kpWeightLower x * rtLower + kpWeightUpper x * rtUpper) +
        (kpWeightLower x + kpWeightUpper x) * (11 - 6 * rtS) := by ring
    _ = x + 1 * (11 - 6 * rtS) := by rw [hx, hs]
    _ = x + 11 - 6 * rtS := by ring

/-- The barycentric weights are nonnegative on the degree interval. -/
theorem kp_weights_nonneg {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    0 ≤ kpWeightLower x ∧ 0 ≤ kpWeightUpper x := by
  have hw : 0 < rtUpper - rtLower := kp_degree_interval_width_pos
  constructor
  · exact div_nonneg (sub_nonneg.mpr hxU) (le_of_lt hw)
  · exact div_nonneg (sub_nonneg.mpr hxL) (le_of_lt hw)

/-- Pure algebraic unit-circle interpolation identity. -/
theorem kp_unit_circle_interpolation_identity
    {a b ya yb u v : ℝ}
    (huv : u + v = 1)
    (ha : a ^ 2 + ya ^ 2 = 1)
    (hb : b ^ 2 + yb ^ 2 = 1) :
    1 - (u * a + v * b) ^ 2 - (u * ya + v * yb) ^ 2 =
      u * v * ((a - b) ^ 2 + (ya - yb) ^ 2) := by
  have hv : v = 1 - u := by linarith
  rw [hv]
  have ha' : ya ^ 2 = 1 - a ^ 2 := by nlinarith [ha]
  have hb' : yb ^ 2 = 1 - b ^ 2 := by nlinarith [hb]
  ring_nf
  rw [ha', hb']
  ring

/-- The interpolated endpoint height lies below the unit semicircle. -/
theorem kp_interpolatedY_le_sqrt {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    kpInterpolatedY x ≤ Real.sqrt (1 - x ^ 2) := by
  rcases kp_weights_nonneg hxL hxU with ⟨hwL, hwU⟩
  have hsum := kp_weights_sum x
  have hxb := kp_barycentric_x x
  have hya : rtLower ^ 2 + kpLowerY ^ 2 = 1 := by
    rw [kpLowerY_sq]
    ring
  have hyb : rtUpper ^ 2 + kpUpperY ^ 2 = 1 := by
    rw [kpUpperY_sq]
    ring
  have hid := kp_unit_circle_interpolation_identity hsum hya hyb
  have hdist :
      0 ≤ (rtLower - rtUpper) ^ 2 + (kpLowerY - kpUpperY) ^ 2 := by
    positivity
  have huv : 0 ≤ kpWeightLower x * kpWeightUpper x :=
    mul_nonneg hwL hwU
  have hdeficit : 0 ≤
      1 -
        (kpWeightLower x * rtLower + kpWeightUpper x * rtUpper) ^ 2 -
        (kpWeightLower x * kpLowerY + kpWeightUpper x * kpUpperY) ^ 2 := by
    rw [hid]
    exact mul_nonneg huv hdist
  have hdeficit' : 0 ≤ 1 - x ^ 2 - kpInterpolatedY x ^ 2 := by
    simpa only [hxb, kpInterpolatedY] using hdeficit
  have hsq : kpInterpolatedY x ^ 2 ≤ 1 - x ^ 2 := by
    nlinarith
  have hyNonneg : 0 ≤ kpInterpolatedY x := by
    dsimp [kpInterpolatedY]
    exact add_nonneg
      (mul_nonneg hwL kpLowerY_nonneg)
      (mul_nonneg hwU kpUpperY_nonneg)
  have hrad : 0 ≤ 1 - x ^ 2 := rtRad_nonneg hxL hxU
  have hsqrtSq := Real.sq_sqrt hrad
  have hsqrt0 := Real.sqrt_nonneg (1 - x ^ 2)
  by_contra hnot
  have hlt : Real.sqrt (1 - x ^ 2) < kpInterpolatedY x :=
    lt_of_not_ge hnot
  have hsumPos :
      0 < kpInterpolatedY x + Real.sqrt (1 - x ^ 2) := by
    have hyPos : 0 < kpInterpolatedY x := lt_of_le_of_lt hsqrt0 hlt
    linarith
  have hprod :
      0 <
        (kpInterpolatedY x - Real.sqrt (1 - x ^ 2)) *
          (kpInterpolatedY x + Real.sqrt (1 - x ^ 2)) :=
    mul_pos (sub_pos.mpr hlt) hsumPos
  have hstrictSq :
      (Real.sqrt (1 - x ^ 2)) ^ 2 < kpInterpolatedY x ^ 2 := by
    nlinarith
  rw [hsqrtSq] at hstrictSq
  exact (not_lt_of_ge hsq) hstrictSq

/-- Endpoint interpolation of `H` equals the corresponding linearized expression. -/
theorem kp_optimizedH_endpoint_interpolation (x : ℝ) :
    kpWeightLower x * kpOptimizedH rtLower +
        kpWeightUpper x * kpOptimizedH rtUpper =
      1 + x * kpCosShift - kpInterpolatedY x * kpSinShift := by
  rw [kpOptimizedH, kpOptimizedH, kp_sqrt_lower, kp_sqrt_upper]
  have hs := kp_weights_sum x
  have hx := kp_barycentric_x x
  calc
    kpWeightLower x *
          (1 + rtLower * kpCosShift - kpLowerY * kpSinShift) +
        kpWeightUpper x *
          (1 + rtUpper * kpCosShift - kpUpperY * kpSinShift) =
      (kpWeightLower x + kpWeightUpper x) +
        (kpWeightLower x * rtLower + kpWeightUpper x * rtUpper) * kpCosShift -
        (kpWeightLower x * kpLowerY + kpWeightUpper x * kpUpperY) * kpSinShift := by
          ring
    _ = 1 + x * kpCosShift - kpInterpolatedY x * kpSinShift := by
      rw [hs, hx]
      rfl

/-- The optimized exposed-area function lies below its endpoint chord. -/
theorem kpOptimizedH_le_chord {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    kpOptimizedH x ≤ kpOptimizedChord x := by
  have hY := kp_interpolatedY_le_sqrt hxL hxU
  have hSin := kpSinShift_pos
  have hmul := mul_le_mul_of_nonneg_right hY (le_of_lt hSin)
  have hHweighted :
      kpOptimizedH x ≤
        kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper := by
    rw [kp_optimizedH_endpoint_interpolation]
    dsimp [kpOptimizedH]
    nlinarith
  have hChordWeights :
      kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper =
        kpOptimizedChord x := by
    calc
      kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper =
        kpWeightLower x * kpOptimizedChord rtLower +
          kpWeightUpper x * kpOptimizedChord rtUpper := by
            rw [kpOptimizedH_lower, kpOptimizedH_upper,
              kpOptimizedChord_lower, kpOptimizedChord_upper]
      _ = kpOptimizedChord x := kp_chord_barycentric x
  rw [hChordWeights] at hHweighted
  exact hHweighted

/-- The chord becomes the missing-contact charge after substituting the degree parameter. -/
theorem kpOptimizedChord_degree (d : ℝ) :
    kpOptimizedChord (rtX d) = kpQ * (12 - d) := by
  dsimp [kpOptimizedChord, rtX, kpQ, kpS, rtS]
  ring

/-- Optimized affine local charge for every real degree in `[1,11]`. -/
theorem kp_optimized_degree_charge {d : ℝ}
    (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    kpOptimizedH (rtX d) ≤ kpQ * (12 - d) := by
  rcases rtX_bounds hd1 hd11 with ⟨hxL, hxU⟩
  have h := kpOptimizedH_le_chord hxL hxU
  rw [kpOptimizedChord_degree d] at h
  exact h

end

end Erdos1084
