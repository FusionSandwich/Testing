import Erdos1084

open Erdos1084

/-! Smoke tests for the FCC Wulff and Barlow optimization arithmetic. -/

example (t : ℕ) :
    fccWulffD t = 6 * fccWulffB t :=
  fccWulff_deficit_eq_six_projection t

example (t : ℕ) :
    6 * fccWulffN t = fccWulffE t + fccWulffD t :=
  fccWulff_bulk_split t

example : (192 : ℕ) ^ 3 = 432 * (128 : ℕ) ^ 2 :=
  fccWulff_leading_cube

example : (192 : ℝ) ^ 3 / (128 : ℝ) ^ 2 = 432 :=
  fccWulff_leading_ratio_cube

example {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    32 ≤ barlowWulffVolume p :=
  barlowWulffVolume_ge_fcc hp0 hp1

example {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    432 ≤ barlowCoefficientCube p :=
  barlowCoefficientCube_ge_fcc hp0 hp1

example {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    barlowCoefficientCube p = 432 ↔ p = 0 ∨ p = 1 :=
  barlowCoefficientCube_eq_fcc_iff hp0 hp1

example :
    barlowWulffVolume (1 / 2 : ℝ) = 35 ∧
    barlowCoefficientCube (1 / 2 : ℝ) = 945 / 2 :=
  barlow_hcp_values
