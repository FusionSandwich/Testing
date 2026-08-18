import Mathlib
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Optimized convex-chord envelope at the Kepler radius

This file proves the genuinely new local algebra used at

`kpRadius = (40 + 22 * sqrt 3) / 37`.

For the equal-area comparison-cap cosine `x`, define

`H(x) = 1 + x cos(s) - sqrt(1-x^2) sin(s)`.

The two endpoint degree charges (`d = 11` and `d = 1`) agree exactly at the optimized radius.
The upper semicircle is concave, hence `H` lies below the chord through those endpoints.  The
proof below is algebraic: concavity of the semicircle is derived from the exact unit-disk
interpolation identity, with no calculus or trigonometric axiom.
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

/-- `kpQ` is the same exact quantity as `1 - rtUpper`. -/
theorem kpQ_eq_one_sub_rtUpper : kpQ = 1 - rtUpper := by
  rfl

/-- The optimized reciprocal radius is the negative lower endpoint. -/
theorem kpRadius_reciprocal_eq_neg_lower :
    1 / kpRadius = -rtLower := by
  rw [kpRadius_reciprocal]
  rfl

/-- The degree interval has positive width. -/
theorem kp_degree_interval_width_pos :
    0 < rtUpper - rtLower := by
  dsimp [rtUpper, rtLower]
  linarith [rtS_lt_two]

/-- The lower endpoint lies below zero. -/
theorem kp_rtLower_lt_zero : rtLower < 0 := by
  have hs0 : 0 ≤ rtS := rtS_nonneg
  have hs2 : rtS ^ 2 = 3 := rtS_sq
  have h20 : 11 * rtS < 20 := by
    nlinarith
  dsimp [rtLower]
  linarith

/-- The lower endpoint has square strictly below one quarter. -/
theorem kp_rtLower_sq_lt_quarter :
    rtLower ^ 2 < (1 / 2 : ℝ) ^ 2 := by
  have hL : (-1 / 2 : ℝ) < rtLower := by
    have h := rtLower_gt_neg_one
    have h19 := nineteen_lt_eleven_sqrt_three
    dsimp [rtLower, rtS] at h19 ⊢
    linarith
  have hU : rtLower < (1 / 2 : ℝ) := by
    linarith [kp_rtLower_lt_zero]
  have hp : 0 < ((1 / 2 : ℝ) - rtLower) * ((1 / 2 : ℝ) + rtLower) :=
    mul_pos (sub_pos.mpr hU) (by linarith)
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

/-- The upper endpoint lies on the unit semicircle. -/
theorem kpUpperY_sq :
    kpUpperY ^ 2 = 1 - rtUpper ^ 2 := by
  dsimp [kpUpperY, rtUpper]
  rw [rtS_sq]
  norm_num

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

/-- The lower semicircle height is strictly larger than the upper endpoint height. -/
theorem kpLowerY_gt_upperY : kpUpperY < kpLowerY := by
  have hsq : kpUpperY ^ 2 < kpLowerY ^ 2 := by
    rw [kpLowerY_sq, kpUpperY_sq]
    nlinarith [kp_rtLower_sq_lt_quarter]
  by_contra hnot
  have hle : kpLowerY ≤ kpUpperY := le_of_not_gt hnot
  have hmul := mul_le_mul hle hle kpLowerY_nonneg kpUpperY_nonneg
  have hsqle : kpLowerY ^ 2 ≤ kpUpperY ^ 2 := by
    simpa [pow_two] using hmul
  exact (not_lt_of_ge hsqle) hsq

/-- The angular dilation sine is strictly positive. -/
theorem kpSinShift_pos : 0 < kpSinShift := by
  have hUpperPos : 0 < rtUpper := by
    dsimp [rtUpper]
    positivity
  have hY : rtUpper < kpLowerY := by
    have hUpperEq : rtUpper = kpUpperY + (rtS - 1) / 2 := by
      dsimp [rtUpper, kpUpperY]
      ring
    have hsOne : 1 < rtS := by
      have hs0 := rtS_nonneg
      have hs2 := rtS_sq
      nlinarith
    have hUpperYlt : kpUpperY < rtUpper := by
      rw [hUpperEq]
      linarith
    exact lt_trans hUpperYlt kpLowerY_gt_upperY
  have hprod : rtUpper ^ 2 < rtUpper * kpLowerY := by
    have h := mul_lt_mul_of_pos_left hY hUpperPos
    simpa [pow_two] using h
  have hUpperSq : rtUpper ^ 2 = (3 / 4 : ℝ) := by
    dsimp [rtUpper]
    rw [rtS_sq]
    ring
  have hLower : (-1 / 2 : ℝ) < rtLower := by
    have h19 := nineteen_lt_eleven_sqrt_three
    dsimp [rtLower, rtS] at h19 ⊢
    linarith
  rw [kpSinShift, kpRadius_reciprocal_eq_neg_lower]
  nlinarith

/-- The lower endpoint value is exactly the common charge `q`. -/
theorem kpOptimizedH_lower :
    kpOptimizedH rtLower = kpQ := by
  have hrec := kpRadius_reciprocal_eq_neg_lower
  have hY2 := kpLowerY_sq
  have hQ := kpQ_eq_one_sub_rtUpper
  rw [kpOptimizedH, kpCosShift, kpSinShift, hrec]
  change
    1 + rtLower * (rtUpper * (-rtLower) + kpLowerY / 2) -
      kpLowerY * (rtUpper * kpLowerY + rtLower / 2) = kpQ
  rw [hQ]
  nlinarith

/-- The upper endpoint value is exactly eleven times the common charge. -/
theorem kpOptimizedH_upper :
    kpOptimizedH rtUpper = 11 * kpQ := by
  have hrec := kpRadius_reciprocal_eq_neg_lower
  have hsqrt := kp_sqrt_upper
  have hUpperSq : rtUpper ^ 2 = (3 / 4 : ℝ) := by
    dsimp [rtUpper]
    rw [rtS_sq]
    ring
  have hLowerLinear : rtLower = 11 * rtUpper - 10 := by
    rfl
  have hQ := kpQ_eq_one_sub_rtUpper
  rw [kpOptimizedH, kpCosShift, kpSinShift, hrec, hsqrt]
  rw [hQ]
  nlinarith

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
  have hsq : kpInterpolatedY x ^ 2 ≤ 1 - x ^ 2 := by
    rw [kpInterpolatedY, hxb] at hdeficit
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

/-- The optimized exposed-area function lies below its endpoint chord. -/
theorem kpOptimizedH_le_chord {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    kpOptimizedH x ≤ kpOptimizedChord x := by
  have hY := kp_interpolatedY_le_sqrt hxL hxU
  have hSin := kpSinShift_pos
  have hlinear :
      kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper =
        1 + x * kpCosShift - kpInterpolatedY x * kpSinShift := by
    rw [kpOptimizedH, kpOptimizedH]
    rw [kp_sqrt_upper]
    change
      kpWeightLower x *
          (1 + rtLower * kpCosShift - kpLowerY * kpSinShift) +
        kpWeightUpper x *
          (1 + rtUpper * kpCosShift - kpUpperY * kpSinShift) =
        1 + x * kpCosShift - kpInterpolatedY x * kpSinShift
    rw [kpInterpolatedY]
    have hs := kp_weights_sum x
    have hx := kp_barycentric_x x
    linear_combination
      kpCosShift * hx +
      (-kpSinShift) * rfl +
      hs
  have hHweighted :
      kpOptimizedH x ≤
        kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper := by
    rw [hlinear]
    dsimp [kpOptimizedH]
    nlinarith
  have hChordWeights :
      kpWeightLower x * kpOptimizedH rtLower +
          kpWeightUpper x * kpOptimizedH rtUpper =
        kpOptimizedChord x := by
    rw [kpOptimizedH_lower, kpOptimizedH_upper]
    have hwne : rtUpper - rtLower ≠ 0 :=
      ne_of_gt kp_degree_interval_width_pos
    dsimp [kpWeightLower, kpWeightUpper, kpOptimizedChord, kpQ, kpS,
      rtUpper, rtLower, rtS]
    field_simp [hwne]
    ring
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
  simpa [kpOptimizedChord_degree d] using h

end

end Erdos1084
