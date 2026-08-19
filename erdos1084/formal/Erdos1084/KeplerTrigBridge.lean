import Mathlib
import Erdos1084.KeplerOptimizedChord
import Erdos1084.DegreeTwelveExposure

namespace Erdos1084

/-!
# Trigonometric bridge from the geometric cap expression to the optimized Lean envelope

The local geometry produces `1 + cos(arccos x + s_*)`.  The optimized chord module uses the
algebraic function `kpOptimizedH x`.  This file proves that the two are exactly equal at the
optimized radius and transfers the machine-checked affine charge to the geometric expression.
-/

noncomputable section

/-- Geometric hidden-cap angle. -/
def phase1Alpha : ℝ := Real.arccos (1 / kpRadius)
/-- Base-cap radius `π/6`. -/
def phase1Beta : ℝ := Real.pi / 6
/-- Spherical-neighborhood dilation angle. -/
def phase1Shift : ℝ := phase1Alpha - phase1Beta

private theorem phase1_reciprocal_bounds :
    (-1 : ℝ) ≤ 1 / kpRadius ∧ 1 / kpRadius ≤ 1 := by
  have hp : 0 < 1 / kpRadius := one_div_pos.mpr kpRadius_pos
  have hu : 1 / kpRadius < 1 / 2 := kpRadius_reciprocal_lt_half
  constructor <;> linarith

/-- Exact sine of the hidden-cap angle. -/
theorem phase1_sin_alpha :
    Real.sin phase1Alpha = kpLowerY := by
  rcases phase1_reciprocal_bounds with ⟨hl, hu⟩
  rw [phase1Alpha, Real.sin_arccos]
  · congr 1
    rw [kpRadius_reciprocal_eq_neg_lower]
    ring
  · exact hl
  · exact hu

/-- Exact cosine of the hidden-cap angle. -/
theorem phase1_cos_alpha :
    Real.cos phase1Alpha = 1 / kpRadius := by
  rcases phase1_reciprocal_bounds with ⟨hl, hu⟩
  exact Real.cos_arccos hl hu

/-- Exact cosine of the dilation shift. -/
theorem phase1_cos_shift :
    Real.cos phase1Shift = kpCosShift := by
  rw [phase1Shift, Real.cos_sub, phase1_cos_alpha, phase1_sin_alpha,
    phase1Beta, Real.cos_pi_div_six, Real.sin_pi_div_six]
  rw [kpCosShift, div_eq_mul_inv]
  ring

/-- Exact sine of the dilation shift. -/
theorem phase1_sin_shift :
    Real.sin phase1Shift = kpSinShift := by
  rw [phase1Shift, Real.sin_sub, phase1_cos_alpha, phase1_sin_alpha,
    phase1Beta, Real.cos_pi_div_six, Real.sin_pi_div_six]
  rw [kpSinShift]
  ring

/-- Geometric normalized exposed-cap expression. -/
def phase1GeometricH (x : ℝ) : ℝ :=
  1 + Real.cos (Real.arccos x + phase1Shift)

/-- The geometric cap expression is exactly the algebraic function used by the Lean chord proof. -/
theorem phase1GeometricH_eq_kpOptimizedH
    {x : ℝ} (hxL : -1 ≤ x) (hxU : x ≤ 1) :
    phase1GeometricH x = kpOptimizedH x := by
  rw [phase1GeometricH, Real.cos_add, Real.cos_arccos hxL hxU,
    Real.sin_arccos hxL hxU, phase1_cos_shift, phase1_sin_shift]
  rfl

/-- Geometric exposed-cap expression satisfies the optimized affine charge on the degree range. -/
theorem phase1_geometric_degree_charge
    {d : ℝ} (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    phase1GeometricH (rtX d) ≤ kpQ * (12 - d) := by
  rcases rtX_bounds hd1 hd11 with ⟨hxL, hxU⟩
  have hXmOne : (-1 : ℝ) ≤ rtX d :=
    le_trans (le_of_lt rtLower_gt_neg_one) hxL
  have hXOne : rtX d ≤ 1 :=
    le_trans hxU (le_of_lt rtUpper_lt_one)
  rw [phase1GeometricH_eq_kpOptimizedH hXmOne hXOne]
  exact kp_optimized_degree_charge hd1 hd11

end

end Erdos1084
