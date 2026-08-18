import Mathlib

namespace Erdos1084

/-- Physical Wulff volume for Barlow chirality frequency `p`. -/
def barlowWulffVolume (p : ℝ) : ℝ :=
  32 + 12 * p * (1 - p)

/-- Cube of the Barlow surface-order coefficient. -/
def barlowCoefficientCube (p : ℝ) : ℝ :=
  432 + 162 * p * (1 - p)

theorem barlowCoefficientCube_from_volume (p : ℝ) :
    barlowCoefficientCube p = (27 / 2 : ℝ) * barlowWulffVolume p := by
  simp [barlowCoefficientCube, barlowWulffVolume]
  ring

theorem barlowWulffVolume_ge_fcc
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    32 ≤ barlowWulffVolume p := by
  have hprod : 0 ≤ p * (1 - p) :=
    mul_nonneg hp0 (sub_nonneg.mpr hp1)
  simp [barlowWulffVolume]
  nlinarith

theorem barlowCoefficientCube_ge_fcc
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    432 ≤ barlowCoefficientCube p := by
  have hprod : 0 ≤ p * (1 - p) :=
    mul_nonneg hp0 (sub_nonneg.mpr hp1)
  simp [barlowCoefficientCube]
  nlinarith

theorem barlowWulffVolume_eq_fcc_iff
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    barlowWulffVolume p = 32 ↔ p = 0 ∨ p = 1 := by
  constructor
  · intro h
    have hprod : p * (1 - p) = 0 := by
      simp [barlowWulffVolume] at h
      nlinarith
    rcases mul_eq_zero.mp hprod with hp | hp
    · exact Or.inl hp
    · exact Or.inr (by linarith)
  · intro h
    rcases h with rfl | rfl <;> norm_num [barlowWulffVolume]

theorem barlowCoefficientCube_eq_fcc_iff
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    barlowCoefficientCube p = 432 ↔ p = 0 ∨ p = 1 := by
  constructor
  · intro h
    have hprod : p * (1 - p) = 0 := by
      simp [barlowCoefficientCube] at h
      nlinarith
    rcases mul_eq_zero.mp hprod with hp | hp
    · exact Or.inl hp
    · exact Or.inr (by linarith)
  · intro h
    rcases h with rfl | rfl <;> norm_num [barlowCoefficientCube]

theorem barlow_fcc_values :
    barlowWulffVolume 0 = 32 ∧
    barlowWulffVolume 1 = 32 ∧
    barlowCoefficientCube 0 = 432 ∧
    barlowCoefficientCube 1 = 432 := by
  norm_num [barlowWulffVolume, barlowCoefficientCube]

theorem barlow_hcp_values :
    barlowWulffVolume (1 / 2 : ℝ) = 35 ∧
    barlowCoefficientCube (1 / 2 : ℝ) = 945 / 2 := by
  norm_num [barlowWulffVolume, barlowCoefficientCube]

theorem barlow_hcp_strictly_worse_than_fcc :
    (432 : ℝ) < barlowCoefficientCube (1 / 2 : ℝ) := by
  norm_num [barlowCoefficientCube]

end Erdos1084
