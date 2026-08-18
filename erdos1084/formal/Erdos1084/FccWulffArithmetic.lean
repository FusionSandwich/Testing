import Mathlib

namespace Erdos1084

/-- Number of points in the integer-coordinate FCC truncated-octahedral family. -/
def fccWulffN (t : ℕ) : ℕ :=
  128 * t ^ 3 + 60 * t ^ 2 + 12 * t + 1

/-- Missing positive-direction bonds in any one FCC contact direction. -/
def fccWulffB (t : ℕ) : ℕ :=
  32 * t ^ 2 + 10 * t + 1

/-- Contact deficit `6n-E` of the FCC truncated-octahedral family. -/
def fccWulffD (t : ℕ) : ℕ :=
  192 * t ^ 2 + 60 * t + 6

/-- Number of contacts in the FCC truncated-octahedral family. -/
def fccWulffE (t : ℕ) : ℕ :=
  768 * t ^ 3 + 168 * t ^ 2 + 12 * t

theorem fccWulff_deficit_eq_six_projection (t : ℕ) :
    fccWulffD t = 6 * fccWulffB t := by
  simp [fccWulffD, fccWulffB]
  ring

theorem fccWulff_bulk_split (t : ℕ) :
    6 * fccWulffN t = fccWulffE t + fccWulffD t := by
  simp [fccWulffN, fccWulffE, fccWulffD]
  ring

/-- Exact integer identity behind the limiting coefficient cube. -/
theorem fccWulff_leading_cube :
    (192 : ℕ) ^ 3 = 432 * (128 : ℕ) ^ 2 := by
  norm_num

/-- Real-valued version of the leading-coefficient identity. -/
theorem fccWulff_leading_ratio_cube :
    (192 : ℝ) ^ 3 / (128 : ℝ) ^ 2 = 432 := by
  norm_num

/-- The candidate FCC coefficient `6*cubert(2)` has cube `432`. -/
theorem fccWulff_coefficient_cube_arithmetic :
    (6 : ℝ) ^ 3 * 2 = 432 := by
  norm_num

/-- The old octahedral-family cube is larger than the FCC Wulff cube. -/
theorem fccWulff_improves_octahedral_cube :
    (432 : ℝ) < 486 := by
  norm_num

end Erdos1084
