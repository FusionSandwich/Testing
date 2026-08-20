import Mathlib

namespace Erdos1084

/-!
# Arithmetic for the icosahedral holonomy-cut obstruction

The human proof shows that every one of the twelve radial fivefold axes must be
incident to a noncoherent cut, while one triangular cut face has only two radial
endpoints. This module certifies the resulting six-cut count and the exact
surface-coefficient comparisons for the twenty-tetrahedron model.
-/

/-- Twelve covered axes and at most two axes per cut force at least six cuts. -/
theorem icosahedral_six_cuts_of_two_endpoint_cover
    {cuts : ℕ} (hcover : 12 ≤ 2 * cuts) :
    6 ≤ cuts := by
  omega

/-- At least six cuts leave at most twenty-four coherent adjacencies. -/
theorem icosahedral_coherent_faces_le_twentyFour
    {cuts coherent : ℕ}
    (htotal : coherent + cuts = 30)
    (hcuts : 6 ≤ cuts) :
    coherent ≤ 24 := by
  omega

/-- Effective triangular-face count when six compulsory cuts have cost ratio `lambda`. -/
def icosahedralEffectiveFaces (lambda : ℝ) : ℝ :=
  20 + 12 * lambda

/-- Leading coefficient cube of the equal-tetrahedron icosahedral face model. -/
noncomputable def icosahedralCoeffCube (lambda : ℝ) : ℝ :=
  (243 / 16) * icosahedralEffectiveFaces lambda ^ 3 / 20 ^ 2

/-- Six full two-crack cuts have exact cube `31104/25`. -/
theorem icosahedral_six_twoCrack_cube :
    icosahedralCoeffCube 1 = (31104 : ℝ) / 25 := by
  norm_num [icosahedralCoeffCube, icosahedralEffectiveFaces]

/-- The six-cut two-crack model is strictly above the FCC cube `432`. -/
theorem icosahedral_six_twoCrack_cube_gt_fcc :
    432 < icosahedralCoeffCube 1 := by
  rw [icosahedral_six_twoCrack_cube]
  norm_num

/-- The certified Sigma-5 interface costs four fifths of two independent cracks. -/
theorem sigma5_twoCrack_ratio :
    ((16 : ℝ) / 5) / 4 = 4 / 5 := by
  norm_num

/-- Rational upper certificate for the critical cut-cost ratio. -/
noncomputable def icosahedralCriticalUpper : ℝ := 207629 / 1000000

/-- At the rational ratio `0.207629`, the icosahedral cube is already above FCC. -/
theorem icosahedral_criticalUpper_cube_gt_fcc :
    432 < icosahedralCoeffCube icosahedralCriticalUpper := by
  norm_num [icosahedralCoeffCube, icosahedralEffectiveFaces,
    icosahedralCriticalUpper]

/-- The coefficient cube is monotone once the effective face count is nonnegative. -/
theorem icosahedralCoeffCube_mono
    {lambda₁ lambda₂ : ℝ}
    (hface : 0 ≤ icosahedralEffectiveFaces lambda₁)
    (hlambda : lambda₁ ≤ lambda₂) :
    icosahedralCoeffCube lambda₁ ≤ icosahedralCoeffCube lambda₂ := by
  have hfaces :
      icosahedralEffectiveFaces lambda₁ ≤
        icosahedralEffectiveFaces lambda₂ := by
    dsimp [icosahedralEffectiveFaces]
    linarith
  have hface₂ : 0 ≤ icosahedralEffectiveFaces lambda₂ :=
    hface.trans hfaces
  have hcube :
      icosahedralEffectiveFaces lambda₁ ^ 3 ≤
        icosahedralEffectiveFaces lambda₂ ^ 3 := by
    have hdiff : 0 ≤
        (icosahedralEffectiveFaces lambda₂ -
          icosahedralEffectiveFaces lambda₁) *
        (icosahedralEffectiveFaces lambda₂ ^ 2 +
          icosahedralEffectiveFaces lambda₂ *
            icosahedralEffectiveFaces lambda₁ +
          icosahedralEffectiveFaces lambda₁ ^ 2) := by
      positivity
    nlinarith
  dsimp [icosahedralCoeffCube]
  norm_num
  nlinarith

/-- Any average cut ratio at least `0.207629` cannot beat the FCC cube. -/
theorem icosahedral_not_below_fcc_of_ratio_ge_criticalUpper
    {lambda : ℝ}
    (hlambda : icosahedralCriticalUpper ≤ lambda) :
    432 < icosahedralCoeffCube lambda := by
  have hface : 0 ≤ icosahedralEffectiveFaces icosahedralCriticalUpper := by
    norm_num [icosahedralEffectiveFaces, icosahedralCriticalUpper]
  have hmono := icosahedralCoeffCube_mono hface hlambda
  exact lt_of_lt_of_le icosahedral_criticalUpper_cube_gt_fcc hmono

end Erdos1084
