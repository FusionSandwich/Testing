import Mathlib
import Erdos1084.ExternalConstants

namespace Erdos1084

noncomputable section

/-- The algebraic value `sqrt 3` used by the radius-two proof. -/
def rtS : ℝ := Real.sqrt 3

/-- Lower endpoint `x₁₁` for the degree parameter. -/
def rtLower : ℝ := (11 * rtS - 20) / 2

/-- Upper endpoint `x₁`. -/
def rtUpper : ℝ := rtS / 2

/-- The affine expression obtained after rearranging the local envelope. -/
def rtR (x : ℝ) : ℝ := 3 * rtS - 2 + 2 * (rtS - 3) * x

/-- The concave quadratic certificate for the local envelope. -/
def rtP (x : ℝ) : ℝ :=
  (24 * rtS - 73) * x ^ 2 + (44 * rtS - 60) * x + 12 * rtS - 6

/-- The normalized uncovered-area quantity at cosine parameter `x`. -/
def rtH (x : ℝ) : ℝ :=
  1 + rtS / 2 * x - Real.sqrt (1 - x ^ 2) / 2

/-- The continuous `3/20` envelope written in the cosine parameter. -/
def rtEnvelope (x : ℝ) : ℝ :=
  (3 / 20 : ℝ) * (8 - 2 * rtS + (4 + 2 * rtS) * x)

/-- Cosine of the equal-area comparison cap for real degree `d`. -/
def rtX (d : ℝ) : ℝ := 1 - d * (1 - rtS / 2)

@[simp] theorem rtS_sq : rtS ^ 2 = 3 := by
  norm_num [rtS]

@[simp] theorem rtS_nonneg : 0 ≤ rtS := by
  exact Real.sqrt_nonneg _

@[simp] theorem rtS_pos : 0 < rtS := by
  exact Real.sqrt_pos.2 (by norm_num)

@[simp] theorem rtS_lt_two : rtS < 2 := by
  have hs := rtS_nonneg
  have hs2 := rtS_sq
  nlinarith

/-- Exact integer-square margin at the difficult lower endpoint. -/
theorem rt_endpoint_square_margin :
    (82099 : ℝ) ^ 2 < (47400 * rtS) ^ 2 := by
  rw [mul_pow, rtS_sq]
  norm_num

/-- The square margin implies `82099 < 47400 sqrt 3`. -/
theorem rt_endpoint_root_margin :
    (82099 : ℝ) < 47400 * rtS := by
  have hA0 : 0 ≤ 47400 * rtS :=
    mul_nonneg (by norm_num) rtS_nonneg
  have hB0 : 0 ≤ (82099 : ℝ) := by norm_num
  by_contra hnot
  have hle : 47400 * rtS ≤ (82099 : ℝ) := le_of_not_gt hnot
  have hsqle :
      (47400 * rtS) * (47400 * rtS) ≤ (82099 : ℝ) * 82099 :=
    mul_le_mul hle hle hA0 hB0
  have hsq := rt_endpoint_square_margin
  nlinarith

/-- Exact value of the quadratic certificate at the upper endpoint. -/
theorem rtP_upper : rtP rtUpper = 21 / 4 := by
  have hfactor :
      rtP rtUpper - 21 / 4 =
        3 * (8 * rtS + 5) * (rtS ^ 2 - 3) / 4 := by
    dsimp [rtP, rtUpper]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor ⊢
  exact hfactor

/-- Exact value of the quadratic certificate at the lower endpoint. -/
theorem rtP_lower :
    rtP rtLower = (47400 * rtS - 82099) / 4 := by
  have hfactor :
      rtP rtLower - (47400 * rtS - 82099) / 4 =
        11 * (264 * rtS - 1675) * (rtS ^ 2 - 3) / 4 := by
    dsimp [rtP, rtLower]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor ⊢
  exact hfactor

/-- Linear-interpolation identity for the concave quadratic `rtP`. -/
theorem rtP_interpolation_identity (x : ℝ) :
    (rtUpper - rtLower) * rtP x =
      (rtUpper - x) * rtP rtLower +
      (x - rtLower) * rtP rtUpper -
      (24 * rtS - 73) * (x - rtLower) * (rtUpper - x) *
        (rtUpper - rtLower) := by
  simp only [rtP]
  ring

/-- The quadratic certificate is positive throughout the full degree interval. -/
theorem rtP_pos_on_interval {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    0 < rtP x := by
  have hwidth : 0 < rtUpper - rtLower := by
    dsimp [rtUpper, rtLower]
    linarith [rtS_lt_two]
  have hPL : 0 < rtP rtLower := by
    rw [rtP_lower]
    linarith [rt_endpoint_root_margin]
  have hPU : 0 < rtP rtUpper := by
    rw [rtP_upper]
    norm_num
  have hA : 24 * rtS - 73 < 0 := by
    linarith [rtS_lt_two]
  have hwL : 0 ≤ rtUpper - x := sub_nonneg.mpr hxU
  have hwU : 0 ≤ x - rtLower := sub_nonneg.mpr hxL
  have hweighted :
      0 < (rtUpper - x) * rtP rtLower +
        (x - rtLower) * rtP rtUpper := by
    by_cases hxEq : x = rtLower
    · subst x
      have hp : 0 < (rtUpper - rtLower) * rtP rtLower :=
        mul_pos hwidth hPL
      simpa using hp
    · have hxgt : rtLower < x :=
        lt_of_le_of_ne hxL (Ne.symm hxEq)
      have hleft : 0 ≤ (rtUpper - x) * rtP rtLower :=
        mul_nonneg hwL (le_of_lt hPL)
      have hright : 0 < (x - rtLower) * rtP rtUpper :=
        mul_pos (sub_pos.mpr hxgt) hPU
      exact add_pos_of_nonneg_of_pos hleft hright
  have hna : 0 ≤ -(24 * rtS - 73) := by linarith
  have hcurv1 : 0 ≤ -(24 * rtS - 73) * (x - rtLower) :=
    mul_nonneg hna hwU
  have hcurv2 :
      0 ≤ -(24 * rtS - 73) * (x - rtLower) * (rtUpper - x) :=
    mul_nonneg hcurv1 hwL
  have hcurv :
      0 ≤ -(24 * rtS - 73) * (x - rtLower) * (rtUpper - x) *
        (rtUpper - rtLower) :=
    mul_nonneg hcurv2 (le_of_lt hwidth)
  have hprod : 0 < (rtUpper - rtLower) * rtP x := by
    rw [rtP_interpolation_identity x]
    nlinarith
  by_contra hnot
  have hpnonpos : rtP x ≤ 0 := le_of_not_gt hnot
  have hmulnonpos : (rtUpper - rtLower) * rtP x ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (le_of_lt hwidth) hpnonpos
  linarith

/-- The lower endpoint lies strictly above `-1`. -/
theorem rtLower_gt_neg_one : -1 < rtLower := by
  have h := nineteen_lt_eleven_sqrt_three
  dsimp [rtLower, rtS]
  linarith

/-- The upper endpoint lies strictly below `1`. -/
theorem rtUpper_lt_one : rtUpper < 1 := by
  dsimp [rtUpper]
  linarith [rtS_lt_two]

/-- The square-root radicand is nonnegative on the degree interval. -/
theorem rtRad_nonneg {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    0 ≤ 1 - x ^ 2 := by
  have hxneg : -1 < x := lt_of_lt_of_le rtLower_gt_neg_one hxL
  have hxpos : x < 1 := lt_of_le_of_lt hxU rtUpper_lt_one
  have hprod : 0 ≤ (1 - x) * (1 + x) :=
    mul_nonneg (by linarith) (by linarith)
  nlinarith

/-- At the upper endpoint, the rearranged affine term is exactly one. -/
theorem rtR_upper : rtR rtUpper = 1 := by
  have hfactor : rtR rtUpper - 1 = rtS ^ 2 - 3 := by
    dsimp [rtR, rtUpper]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor ⊢
  exact hfactor

/-- The affine term is positive throughout the interval. -/
theorem rtR_ge_one {x : ℝ} (hxU : x ≤ rtUpper) :
    1 ≤ rtR x := by
  have hslope : 2 * (rtS - 3) ≤ 0 := by
    linarith [rtS_lt_two]
  have hmul :
      2 * (rtS - 3) * rtUpper ≤ 2 * (rtS - 3) * x :=
    mul_le_mul_of_nonpos_left hxU hslope
  calc
    1 = rtR rtUpper := by symm; exact rtR_upper
    _ ≤ rtR x := by
      dsimp [rtR]
      linarith

/-- The quadratic certificate equals the difference of the two relevant squares. -/
theorem rtP_identity (x : ℝ) :
    rtP x = 25 * (1 - x ^ 2) - (rtR x) ^ 2 := by
  have hfactor :
      rtP x - (25 * (1 - x ^ 2) - (rtR x) ^ 2) =
        (rtS ^ 2 - 3) * (2 * x + 3) ^ 2 := by
    dsimp [rtP, rtR]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor
  linarith

/-- Continuous radius-two local envelope on the entire degree interval. -/
theorem rt_continuous_envelope {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    rtH x < rtEnvelope x := by
  have hP := rtP_pos_on_interval hxL hxU
  have hR := rtR_ge_one hxU
  have hrad := rtRad_nonneg hxL hxU
  have hy0 : 0 ≤ Real.sqrt (1 - x ^ 2) := Real.sqrt_nonneg _
  have hy2 : (Real.sqrt (1 - x ^ 2)) ^ 2 = 1 - x ^ 2 :=
    Real.sq_sqrt hrad
  have hPid := rtP_identity x
  have hsqdiff :
      0 < (5 * Real.sqrt (1 - x ^ 2)) ^ 2 - (rtR x) ^ 2 := by
    nlinarith
  have hfactor :
      (5 * Real.sqrt (1 - x ^ 2) - rtR x) *
          (5 * Real.sqrt (1 - x ^ 2) + rtR x) =
        (5 * Real.sqrt (1 - x ^ 2)) ^ 2 - (rtR x) ^ 2 := by
    ring
  have hprod :
      0 < (5 * Real.sqrt (1 - x ^ 2) - rtR x) *
        (5 * Real.sqrt (1 - x ^ 2) + rtR x) := by
    rw [hfactor]
    exact hsqdiff
  have hsum : 0 < 5 * Real.sqrt (1 - x ^ 2) + rtR x := by
    nlinarith
  have hdiff : 0 < 5 * Real.sqrt (1 - x ^ 2) - rtR x := by
    rcases (mul_pos_iff.mp hprod) with h | h
    · exact h.1
    · linarith [h.2, hsum]
  dsimp [rtH, rtEnvelope, rtR]
  nlinarith

/-- Degrees from one through eleven map into the continuous interval. -/
theorem rtX_bounds {d : ℝ} (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    rtLower ≤ rtX d ∧ rtX d ≤ rtUpper := by
  have ha : 0 ≤ 1 - rtS / 2 := by
    linarith [rtS_lt_two]
  have hlowerMul : d * (1 - rtS / 2) ≤ 11 * (1 - rtS / 2) :=
    mul_le_mul_of_nonneg_right hd11 ha
  have hupperMul : 1 * (1 - rtS / 2) ≤ d * (1 - rtS / 2) :=
    mul_le_mul_of_nonneg_right hd1 ha
  constructor
  · dsimp [rtLower, rtX]
    linarith
  · dsimp [rtUpper, rtX]
    linarith

/-- Algebraic conversion from the cosine parameter back to degree deficit. -/
theorem rt_degree_rhs_identity (d : ℝ) :
    8 - 2 * rtS + (4 + 2 * rtS) * rtX d = 12 - d := by
  have hfactor :
      (8 - 2 * rtS + (4 + 2 * rtS) * rtX d) - (12 - d) =
        d * (rtS ^ 2 - 3) := by
    dsimp [rtX]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor
  linarith

/-- Exact local envelope for every real degree in `[1,11]`. -/
theorem radiusTwo_degree_envelope {d : ℝ}
    (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    rtH (rtX d) < (3 / 20 : ℝ) * (12 - d) := by
  rcases rtX_bounds hd1 hd11 with ⟨hxL, hxU⟩
  have h := rt_continuous_envelope hxL hxU
  rw [rt_degree_rhs_identity d] at h
  exact h

end

end Erdos1084
