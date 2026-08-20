import Mathlib

namespace Erdos1084

/-!
# FCC `[111]` coincidence-family abrupt arithmetic

The human crystallographic theorem proves that a commensurate `[111]` twist of
reduced coincidence index `Sigma` restores at most three abrupt cross contacts
per cell. The two-crack deficit is `3*Sigma`, so the ratio is `1-1/Sigma` and
the physical density is `2*sqrt(3)*(1-1/Sigma)`.
-/

/-- Abrupt ratio to the two-crack value. -/
def fcc111AbruptRatio (sigma : ℝ) : ℝ :=
  1 - 1 / sigma

/-- Abrupt physical contact-deficit density. -/
def fcc111AbruptDensity (sigma : ℝ) : ℝ :=
  2 * Real.sqrt 3 * fcc111AbruptRatio sigma

/-- Exact reduced-index-seven ratio. -/
theorem fcc111AbruptRatio_seven :
    fcc111AbruptRatio 7 = 6 / 7 := by
  norm_num [fcc111AbruptRatio]

/-- Exact reduced-index-seven density. -/
theorem fcc111AbruptDensity_seven :
    fcc111AbruptDensity 7 = 12 * Real.sqrt 3 / 7 := by
  rw [fcc111AbruptDensity, fcc111AbruptRatio_seven]
  ring

/-- The abrupt ratio is monotone increasing on positive indices. -/
theorem fcc111AbruptRatio_mono
    {sigma₁ sigma₂ : ℝ}
    (hpositive : 0 < sigma₁)
    (horder : sigma₁ ≤ sigma₂) :
    fcc111AbruptRatio sigma₁ ≤ fcc111AbruptRatio sigma₂ := by
  have hpositive₂ : 0 < sigma₂ := lt_of_lt_of_le hpositive horder
  have hreciprocal : 1 / sigma₂ ≤ 1 / sigma₁ := by
    exact (div_le_div_iff₀ hpositive₂ hpositive).2 (by simpa using horder)
  unfold fcc111AbruptRatio
  linarith

/-- Every nontrivial reduced `[111]` index has ratio at least `6/7`. -/
theorem fcc111AbruptRatio_ge_sixSevenths
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    6 / 7 ≤ fcc111AbruptRatio sigma := by
  have hmono := fcc111AbruptRatio_mono
    (sigma₁ := (7 : ℝ)) (sigma₂ := sigma) (by norm_num) hindex
  simpa [fcc111AbruptRatio_seven] using hmono

/-- Every nontrivial reduced `[111]` index has density at least `12*sqrt(3)/7`. -/
theorem fcc111AbruptDensity_ge
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    12 * Real.sqrt 3 / 7 ≤ fcc111AbruptDensity sigma := by
  have hratio := fcc111AbruptRatio_ge_sixSevenths hindex
  have hsqrt : 0 ≤ Real.sqrt 3 := Real.sqrt_nonneg 3
  unfold fcc111AbruptDensity
  nlinarith

/-- The nontrivial `[111]` family is above the `11/30` selector threshold. -/
theorem fcc111AbruptRatio_nontrivial_gt_icosaThreshold
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    11 / 30 < fcc111AbruptRatio sigma := by
  have hratio := fcc111AbruptRatio_ge_sixSevenths hindex
  norm_num at hratio ⊢
  linarith

/-- Natural cell deficit formula. -/
def fcc111AbruptCellDeficit (sigma : ℕ) : ℕ :=
  3 * sigma - 3

/-- For positive index, the cell deficit is `3*(Sigma-1)`. -/
theorem fcc111AbruptCellDeficit_eq
    {sigma : ℕ} (hpositive : 1 ≤ sigma) :
    fcc111AbruptCellDeficit sigma = 3 * (sigma - 1) := by
  unfold fcc111AbruptCellDeficit
  omega

/-- Exact index-seven cell deficit. -/
theorem fcc111AbruptCellDeficit_seven :
    fcc111AbruptCellDeficit 7 = 18 := by
  norm_num [fcc111AbruptCellDeficit]

end Erdos1084
