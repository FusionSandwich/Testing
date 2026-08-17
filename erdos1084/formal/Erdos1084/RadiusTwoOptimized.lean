import Mathlib
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.RadiusTwoGeometricBridges

namespace Erdos1084

/-!
# A clean `1673/1000` strengthening of the radius-two coefficient

The original radius-two proof uses the transparent envelope `3/20`.  This file proves the
stronger continuous envelope `250/1673`, still by a single concave-quadratic certificate.
It yields the rational contact-deficit coefficient `1673/1000`.
-/

noncomputable section

/-- Affine term in the strengthened square-root comparison. -/
def rtQ1673 (x : ℝ) : ℝ :=
  (1000 * rtS - 654) + (673 * rtS - 2000) * x

/-- Concave quadratic certificate for the strengthened local envelope. -/
def rtP1673 (x : ℝ) : ℝ :=
  (2692000 * rtS - 8157716) * x ^ 2 +
  (4880284 * rtS - 6654000) * x +
  1308000 * rtS - 628787

/-- The clean strengthened envelope in the cosine parameter. -/
def rtEnvelope1673 (x : ℝ) : ℝ :=
  (250 / 1673 : ℝ) * (8 - 2 * rtS + (4 + 2 * rtS) * x)

/-- Exact square margin at the difficult lower endpoint. -/
theorem rt1673_endpoint_square_margin :
    (574502107 : ℝ) ^ 2 < (331688980 * rtS) ^ 2 := by
  rw [mul_pow, rtS_sq]
  norm_num

/-- The square margin gives the required strict radical comparison. -/
theorem rt1673_endpoint_root_margin :
    (574502107 : ℝ) < 331688980 * rtS := by
  have hA0 : 0 ≤ 331688980 * rtS :=
    mul_nonneg (by norm_num) rtS_nonneg
  have hB0 : 0 ≤ (574502107 : ℝ) := by norm_num
  by_contra hnot
  have hle : 331688980 * rtS ≤ (574502107 : ℝ) := le_of_not_gt hnot
  have hsqle :
      (331688980 * rtS) * (331688980 * rtS) ≤
        (574502107 : ℝ) * 574502107 :=
    mul_le_mul hle hle hA0 hB0
  have hsq := rt1673_endpoint_square_margin
  nlinarith

/-- The strengthened affine term at the upper endpoint. -/
theorem rtQ1673_upper : rtQ1673 rtUpper = 711 / 2 := by
  dsimp [rtQ1673, rtUpper]
  nlinarith [rtS_sq]

/-- The strengthened quadratic certificate at the upper endpoint. -/
theorem rtP1673_upper : rtP1673 rtUpper = 573352 := by
  have hfactor :
      rtP1673 rtUpper - 573352 =
        (673000 * rtS + 400713) * (rtS ^ 2 - 3) := by
    dsimp [rtP1673, rtUpper]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor
  linarith

/-- The strengthened quadratic certificate at the lower endpoint. -/
theorem rtP1673_lower :
    rtP1673 rtLower = 4 * (331688980 * rtS - 574502107) := by
  have hfactor :
      rtP1673 rtLower - 4 * (331688980 * rtS - 574502107) =
        11 * (7403000 * rtS - 46913577) * (rtS ^ 2 - 3) := by
    dsimp [rtP1673, rtLower]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor
  linarith

/-- Linear-interpolation identity for the strengthened concave quadratic. -/
theorem rtP1673_interpolation_identity (x : ℝ) :
    (rtUpper - rtLower) * rtP1673 x =
      (rtUpper - x) * rtP1673 rtLower +
      (x - rtLower) * rtP1673 rtUpper -
      (2692000 * rtS - 8157716) * (x - rtLower) *
        (rtUpper - x) * (rtUpper - rtLower) := by
  simp only [rtP1673]
  ring

/-- The strengthened quadratic is positive on the entire continuous degree interval. -/
theorem rtP1673_pos_on_interval {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    0 < rtP1673 x := by
  have hwidth : 0 < rtUpper - rtLower := by
    dsimp [rtUpper, rtLower]
    linarith [rtS_lt_two]
  have hPL : 0 < rtP1673 rtLower := by
    rw [rtP1673_lower]
    nlinarith [rt1673_endpoint_root_margin]
  have hPU : 0 < rtP1673 rtUpper := by
    rw [rtP1673_upper]
    norm_num
  have hA : 2692000 * rtS - 8157716 < 0 := by
    linarith [rtS_lt_two]
  have hwL : 0 ≤ rtUpper - x := sub_nonneg.mpr hxU
  have hwU : 0 ≤ x - rtLower := sub_nonneg.mpr hxL
  have hweighted :
      0 < (rtUpper - x) * rtP1673 rtLower +
        (x - rtLower) * rtP1673 rtUpper := by
    by_cases hxEq : x = rtLower
    · subst x
      have hp : 0 < (rtUpper - rtLower) * rtP1673 rtLower :=
        mul_pos hwidth hPL
      simpa using hp
    · have hxgt : rtLower < x :=
        lt_of_le_of_ne hxL (Ne.symm hxEq)
      have hleft : 0 ≤ (rtUpper - x) * rtP1673 rtLower :=
        mul_nonneg hwL (le_of_lt hPL)
      have hright : 0 < (x - rtLower) * rtP1673 rtUpper :=
        mul_pos (sub_pos.mpr hxgt) hPU
      exact add_pos_of_nonneg_of_pos hleft hright
  have hna : 0 ≤ -(2692000 * rtS - 8157716) := by linarith
  have hcurv1 :
      0 ≤ -(2692000 * rtS - 8157716) * (x - rtLower) :=
    mul_nonneg hna hwU
  have hcurv2 :
      0 ≤ -(2692000 * rtS - 8157716) * (x - rtLower) *
        (rtUpper - x) :=
    mul_nonneg hcurv1 hwL
  have hcurv :
      0 ≤ -(2692000 * rtS - 8157716) * (x - rtLower) *
        (rtUpper - x) * (rtUpper - rtLower) :=
    mul_nonneg hcurv2 (le_of_lt hwidth)
  have hprod : 0 < (rtUpper - rtLower) * rtP1673 x := by
    rw [rtP1673_interpolation_identity x]
    nlinarith
  by_contra hnot
  have hpnonpos : rtP1673 x ≤ 0 := le_of_not_gt hnot
  have hmulnonpos : (rtUpper - rtLower) * rtP1673 x ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (le_of_lt hwidth) hpnonpos
  linarith

/-- The strengthened affine term stays positive on the full interval. -/
theorem rtQ1673_pos_on_interval {x : ℝ} (hxU : x ≤ rtUpper) :
    0 < rtQ1673 x := by
  have hslope : 673 * rtS - 2000 ≤ 0 := by
    linarith [rtS_lt_two]
  have hmul :
      (673 * rtS - 2000) * rtUpper ≤
        (673 * rtS - 2000) * x :=
    mul_le_mul_of_nonpos_left hxU hslope
  calc
    0 < (711 / 2 : ℝ) := by norm_num
    _ = rtQ1673 rtUpper := by symm; exact rtQ1673_upper
    _ ≤ rtQ1673 x := by
      dsimp [rtQ1673]
      linarith

/-- The strengthened quadratic is exactly the difference of the relevant squares. -/
theorem rtP1673_identity (x : ℝ) :
    rtP1673 x = 1673 ^ 2 * (1 - x ^ 2) - (rtQ1673 x) ^ 2 := by
  have hfactor :
      rtP1673 x -
          (1673 ^ 2 * (1 - x ^ 2) - (rtQ1673 x) ^ 2) =
        (rtS ^ 2 - 3) * (673 * x + 1000) ^ 2 := by
    dsimp [rtP1673, rtQ1673]
    ring
  rw [rtS_sq] at hfactor
  norm_num at hfactor
  linarith

/-- Continuous strengthened envelope on the entire real degree interval. -/
theorem rt_continuous_envelope_1673 {x : ℝ}
    (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    rtH x < rtEnvelope1673 x := by
  have hP := rtP1673_pos_on_interval hxL hxU
  have hQ := rtQ1673_pos_on_interval hxU
  have hrad := rtRad_nonneg hxL hxU
  have hy0 : 0 ≤ Real.sqrt (1 - x ^ 2) := Real.sqrt_nonneg _
  have hy2 : (Real.sqrt (1 - x ^ 2)) ^ 2 = 1 - x ^ 2 :=
    Real.sq_sqrt hrad
  have hPid := rtP1673_identity x
  have hsqdiff :
      0 < (1673 * Real.sqrt (1 - x ^ 2)) ^ 2 - (rtQ1673 x) ^ 2 := by
    nlinarith
  have hfactor :
      (1673 * Real.sqrt (1 - x ^ 2) - rtQ1673 x) *
          (1673 * Real.sqrt (1 - x ^ 2) + rtQ1673 x) =
        (1673 * Real.sqrt (1 - x ^ 2)) ^ 2 - (rtQ1673 x) ^ 2 := by
    ring
  have hprod :
      0 < (1673 * Real.sqrt (1 - x ^ 2) - rtQ1673 x) *
        (1673 * Real.sqrt (1 - x ^ 2) + rtQ1673 x) := by
    rw [hfactor]
    exact hsqdiff
  have hsum :
      0 < 1673 * Real.sqrt (1 - x ^ 2) + rtQ1673 x := by
    nlinarith
  have hdiff :
      0 < 1673 * Real.sqrt (1 - x ^ 2) - rtQ1673 x := by
    rcases (mul_pos_iff.mp hprod) with h | h
    · exact h.1
    · linarith [h.2, hsum]
  have hrelation :
      rtEnvelope1673 x - rtH x =
        (1673 * Real.sqrt (1 - x ^ 2) - rtQ1673 x) / 3346 := by
    dsimp [rtH, rtEnvelope1673, rtQ1673]
    ring
  have hgap : 0 < rtEnvelope1673 x - rtH x := by
    rw [hrelation]
    exact div_pos hdiff (by norm_num)
  linarith

/-- Strengthened exact envelope for every real degree in `[1,11]`. -/
theorem radiusTwo_degree_envelope_1673 {d : ℝ}
    (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    rtH (rtX d) < (250 / 1673 : ℝ) * (12 - d) := by
  rcases rtX_bounds hd1 hd11 with ⟨hxL, hxU⟩
  have h := rt_continuous_envelope_1673 hxL hxU
  change rtH (rtX d) < (250 / 1673 : ℝ) *
    (8 - 2 * rtS + (4 + 2 * rtS) * rtX d) at h
  rw [rt_degree_rhs_identity d] at h
  exact h

/-- Local exposed-area charge corresponding to the strengthened envelope. -/
theorem spherical_neighborhood_to_local_charge_1673
    {d q H covered exposure : ℝ}
    (hCovered : 2 * Real.pi * (1 - q) ≤ covered)
    (hExposure : exposure ≤ 4 * (4 * Real.pi - covered))
    (hH : H = 1 + q)
    (hEnvelope : H < (250 / 1673 : ℝ) * (12 - d)) :
    exposure < (2000 * Real.pi / 1673) * (12 - d) := by
  have hToH : exposure ≤ 8 * Real.pi * H := by
    rw [hH]
    nlinarith [Real.pi_pos]
  calc
    exposure ≤ 8 * Real.pi * H := hToH
    _ < 8 * Real.pi * ((250 / 1673 : ℝ) * (12 - d)) :=
      mul_lt_mul_of_pos_left hEnvelope (by positivity)
    _ = (2000 * Real.pi / 1673) * (12 - d) := by ring

/-- Final cancellation for the clean strengthened coefficient `1673/1000`. -/
theorem radiusTwo_surface_to_deficit_1673
    {x A D : ℝ}
    (hLower : 4 * Real.pi * x ≤ A)
    (hUpper : A < (4000 * Real.pi / 1673) * D) :
    (1673 / 1000 : ℝ) * x < D := by
  have hchain :
      4 * Real.pi * x < (4000 * Real.pi / 1673) * D :=
    lt_of_le_of_lt hLower hUpper
  have hpiineq :
      Real.pi * (4 * x) < Real.pi * ((4000 / 1673 : ℝ) * D) := by
    calc
      Real.pi * (4 * x) = 4 * Real.pi * x := by ring
      _ < (4000 * Real.pi / 1673) * D := hchain
      _ = Real.pi * ((4000 / 1673 : ℝ) * D) := by ring
  have hcancel : 4 * x < (4000 / 1673 : ℝ) * D := by
    by_contra hnot
    have hle : (4000 / 1673 : ℝ) * D ≤ 4 * x := le_of_not_gt hnot
    have hmul :
        Real.pi * ((4000 / 1673 : ℝ) * D) ≤ Real.pi * (4 * x) :=
      mul_le_mul_of_nonneg_left hle (le_of_lt Real.pi_pos)
    linarith
  nlinarith

end

end Erdos1084
