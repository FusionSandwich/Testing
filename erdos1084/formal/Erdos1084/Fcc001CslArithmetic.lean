import Mathlib

namespace Erdos1084

/-!
# FCC `[001]` coincidence-family abrupt arithmetic

The human crystallographic theorem proves that a commensurate `[001]` twist of
reduced coincidence index `Sigma` restores at most four abrupt cross contacts per
cell.  The two-crack deficit is `4*Sigma`, so the density and ratio are

`4*(1-1/Sigma)` and `1-1/Sigma`.

This module certifies the formula arithmetic, monotonicity, the nontrivial
`Sigma>=5` lower bound, and comparison with the selector thresholds.
-/

/-- Abrupt ratio to the two-crack value as a function of positive index. -/
def fcc001AbruptRatio (sigma : ℝ) : ℝ :=
  1 - 1 / sigma

/-- Abrupt contact-deficit density in the physical coincidence cell. -/
def fcc001AbruptDensity (sigma : ℝ) : ℝ :=
  4 * fcc001AbruptRatio sigma

/-- Exact Sigma-5 ratio. -/
theorem fcc001AbruptRatio_five :
    fcc001AbruptRatio 5 = 4 / 5 := by
  norm_num [fcc001AbruptRatio]

/-- Exact Sigma-5 density. -/
theorem fcc001AbruptDensity_five :
    fcc001AbruptDensity 5 = 16 / 5 := by
  norm_num [fcc001AbruptDensity, fcc001AbruptRatio]

/-- The abrupt ratio is monotone increasing on positive indices. -/
theorem fcc001AbruptRatio_mono
    {sigma₁ sigma₂ : ℝ}
    (hpositive : 0 < sigma₁)
    (horder : sigma₁ ≤ sigma₂) :
    fcc001AbruptRatio sigma₁ ≤ fcc001AbruptRatio sigma₂ := by
  have hpositive₂ : 0 < sigma₂ := lt_of_lt_of_le hpositive horder
  have hreciprocal : 1 / sigma₂ ≤ 1 / sigma₁ := by
    exact (div_le_div_iff₀ hpositive₂ hpositive).2 (by simpa using horder)
  unfold fcc001AbruptRatio
  linarith

/-- Every nontrivial reduced `[001]` index has abrupt ratio at least `4/5`. -/
theorem fcc001AbruptRatio_ge_fourFifths
    {sigma : ℝ} (hindex : 5 ≤ sigma) :
    4 / 5 ≤ fcc001AbruptRatio sigma := by
  have hmono := fcc001AbruptRatio_mono
    (sigma₁ := (5 : ℝ)) (sigma₂ := sigma) (by norm_num) hindex
  simpa [fcc001AbruptRatio_five] using hmono

/-- Every nontrivial reduced `[001]` index has density at least `16/5`. -/
theorem fcc001AbruptDensity_ge_sixteenFifths
    {sigma : ℝ} (hindex : 5 ≤ sigma) :
    16 / 5 ≤ fcc001AbruptDensity sigma := by
  have hratio := fcc001AbruptRatio_ge_fourFifths hindex
  unfold fcc001AbruptDensity
  nlinarith

/-- The Sigma-5 ratio is well above the exact `11/30` spanning-tree threshold. -/
theorem fcc001AbruptRatio_nontrivial_gt_icosaThreshold
    {sigma : ℝ} (hindex : 5 ≤ sigma) :
    11 / 30 < fcc001AbruptRatio sigma := by
  have hratio := fcc001AbruptRatio_ge_fourFifths hindex
  norm_num at hratio ⊢
  linarith

/-- Cell deficit formula in natural arithmetic. -/
def fcc001AbruptCellDeficit (sigma : ℕ) : ℕ :=
  4 * sigma - 4

/-- For positive index, the natural deficit formula is exactly four times `Sigma-1`. -/
theorem fcc001AbruptCellDeficit_eq
    {sigma : ℕ} (hpositive : 1 ≤ sigma) :
    fcc001AbruptCellDeficit sigma = 4 * (sigma - 1) := by
  unfold fcc001AbruptCellDeficit
  omega

/-- Exact Sigma-5 cell deficit. -/
theorem fcc001AbruptCellDeficit_five :
    fcc001AbruptCellDeficit 5 = 16 := by
  norm_num [fcc001AbruptCellDeficit]

end Erdos1084
