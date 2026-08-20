import Mathlib

namespace Erdos1084

/-!
# Universal index-seven abrupt ratio arithmetic

The human Bravais-channel theorem proves that `B` crossing channels restore at
most `4*B` abrupt contacts in a tangential coincidence cell of reduced index
`Sigma`. The two-crack deficit is `B*Sigma`, so the ratio is bounded below by
`1-4/Sigma`. This module certifies the formula, monotonicity, the exact
index-seven threshold, and the triangular-channel improvement `1-3/Sigma`.
-/

noncomputable section

/-- Coarse Bravais-channel abrupt ratio lower envelope. -/
def bravaisAbruptRatioLower (sigma : ℝ) : ℝ :=
  1 - 4 / sigma

/-- Triangular-channel abrupt ratio lower envelope. -/
def triangularAbruptRatioLower (sigma : ℝ) : ℝ :=
  1 - 3 / sigma

/-- Exact index-seven Bravais lower ratio. -/
theorem bravaisAbruptRatioLower_seven :
    bravaisAbruptRatioLower 7 = 3 / 7 := by
  norm_num [bravaisAbruptRatioLower]

/-- Exact index-seven triangular lower ratio. -/
theorem triangularAbruptRatioLower_seven :
    triangularAbruptRatioLower 7 = 4 / 7 := by
  norm_num [triangularAbruptRatioLower]

/-- The Bravais lower envelope is monotone on positive indices. -/
theorem bravaisAbruptRatioLower_mono
    {sigma₁ sigma₂ : ℝ}
    (hpositive : 0 < sigma₁)
    (horder : sigma₁ ≤ sigma₂) :
    bravaisAbruptRatioLower sigma₁ ≤ bravaisAbruptRatioLower sigma₂ := by
  have hpositive₂ : 0 < sigma₂ := lt_of_lt_of_le hpositive horder
  have hreciprocal : 1 / sigma₂ ≤ 1 / sigma₁ := by
    exact (div_le_div_iff₀ hpositive₂ hpositive).2 (by simpa using horder)
  unfold bravaisAbruptRatioLower
  nlinarith

/-- The triangular lower envelope is monotone on positive indices. -/
theorem triangularAbruptRatioLower_mono
    {sigma₁ sigma₂ : ℝ}
    (hpositive : 0 < sigma₁)
    (horder : sigma₁ ≤ sigma₂) :
    triangularAbruptRatioLower sigma₁ ≤ triangularAbruptRatioLower sigma₂ := by
  have hpositive₂ : 0 < sigma₂ := lt_of_lt_of_le hpositive horder
  have hreciprocal : 1 / sigma₂ ≤ 1 / sigma₁ := by
    exact (div_le_div_iff₀ hpositive₂ hpositive).2 (by simpa using horder)
  unfold triangularAbruptRatioLower
  nlinarith

/-- Every index at least seven has Bravais abrupt ratio at least `3/7`. -/
theorem bravaisAbruptRatioLower_ge_threeSevenths
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    3 / 7 ≤ bravaisAbruptRatioLower sigma := by
  have hmono := bravaisAbruptRatioLower_mono
    (sigma₁ := (7 : ℝ)) (sigma₂ := sigma) (by norm_num) hindex
  simpa [bravaisAbruptRatioLower_seven] using hmono

/-- Every index at least seven has triangular abrupt ratio at least `4/7`. -/
theorem triangularAbruptRatioLower_ge_fourSevenths
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    4 / 7 ≤ triangularAbruptRatioLower sigma := by
  have hmono := triangularAbruptRatioLower_mono
    (sigma₁ := (7 : ℝ)) (sigma₂ := sigma) (by norm_num) hindex
  simpa [triangularAbruptRatioLower_seven] using hmono

/-- The universal index-seven Bravais bound is above the `11/30` selector threshold. -/
theorem bravaisAbruptRatioLower_indexSeven_gt_icosaThreshold
    {sigma : ℝ} (hindex : 7 ≤ sigma) :
    11 / 30 < bravaisAbruptRatioLower sigma := by
  have hratio := bravaisAbruptRatioLower_ge_threeSevenths hindex
  norm_num at hratio ⊢
  linarith

/-- The triangular bound is stronger than the general Bravais bound. -/
theorem bravais_le_triangular_ratioLower
    {sigma : ℝ} (hpositive : 0 < sigma) :
    bravaisAbruptRatioLower sigma ≤ triangularAbruptRatioLower sigma := by
  unfold bravaisAbruptRatioLower triangularAbruptRatioLower
  have hreciprocal : 0 < 1 / sigma := one_div_pos.mpr hpositive
  linarith

/-- Coarse natural abrupt deficit from `B*Sigma` broken bonds and at most `4*B` restored bonds. -/
def bravaisAbruptCellDeficitLower (channels sigma : ℕ) : ℕ :=
  channels * sigma - 4 * channels

/-- For `Sigma>=4`, the coarse deficit is exactly `B*(Sigma-4)`. -/
theorem bravaisAbruptCellDeficitLower_eq
    {channels sigma : ℕ} (hindex : 4 ≤ sigma) :
    bravaisAbruptCellDeficitLower channels sigma = channels * (sigma - 4) := by
  unfold bravaisAbruptCellDeficitLower
  omega

/-- Triangular-channel natural deficit lower bound. -/
def triangularAbruptCellDeficitLower (channels sigma : ℕ) : ℕ :=
  channels * sigma - 3 * channels

/-- For `Sigma>=3`, the triangular deficit is `B*(Sigma-3)`. -/
theorem triangularAbruptCellDeficitLower_eq
    {channels sigma : ℕ} (hindex : 3 ≤ sigma) :
    triangularAbruptCellDeficitLower channels sigma = channels * (sigma - 3) := by
  unfold triangularAbruptCellDeficitLower
  omega

end

end Erdos1084
