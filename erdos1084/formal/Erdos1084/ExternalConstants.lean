import Mathlib

namespace Erdos1084

def rQ : ℚ := 158731 / 100000
def deltaQ : ℚ := 7547 / 10000
def cleanQ : ℚ := 98639 / 50000
def piUpperQ : ℚ := 355 / 113
def dodecaVolumeLowerQ : ℚ :=
  5550291028515510269070432113661 / ((10 : ℚ) ^ 30)
def rReal : ℝ := (rQ : ℝ)

@[simp] theorem rQ_pos : 0 < rQ := by
  norm_num [rQ]

@[simp] theorem deltaQ_pos : 0 < deltaQ := by
  norm_num [deltaQ]

@[simp] theorem dodecaVolumeLowerQ_pos : 0 < dodecaVolumeLowerQ := by
  norm_num [dodecaVolumeLowerQ]

theorem rQ_sq_gt_two : (2 : ℚ) < rQ ^ 2 := by
  norm_num [rQ]

theorem four_div_rQ_lt_two_point_five_two :
    (4 : ℚ) / rQ < 63 / 25 := by
  norm_num [rQ]

theorem three_rQ_sq_gt_four : (4 : ℚ) < 3 * rQ ^ 2 := by
  norm_num [rQ]

theorem nineteen_lt_eleven_sqrt_three :
    (19 : ℝ) < 11 * Real.sqrt 3 := by
  have hs : 0 ≤ Real.sqrt (3 : ℝ) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by
    norm_num
  nlinarith

theorem sqrt_two_lt_rReal : Real.sqrt 2 < rReal := by
  have hs : 0 ≤ Real.sqrt (2 : ℝ) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (2 : ℝ)) ^ 2 = 2 := by
    norm_num
  have hr : (2 : ℝ) < rReal ^ 2 := by
    norm_num [rReal, rQ]
  have hrpos : 0 < rReal := by
    norm_num [rReal, rQ]
  nlinarith

theorem two_div_sqrt_three_lt_rReal :
    (2 : ℝ) / Real.sqrt 3 < rReal := by
  have hspos : 0 < Real.sqrt (3 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  have hs2 : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by
    norm_num
  have hrpos : 0 < rReal := by
    norm_num [rReal, rQ]
  have hrsq : (4 : ℝ) < 3 * rReal ^ 2 := by
    norm_num [rReal, rQ]
  have hprodSq : (4 : ℝ) < (rReal * Real.sqrt 3) ^ 2 := by
    calc
      (4 : ℝ) < 3 * rReal ^ 2 := hrsq
      _ = (rReal * Real.sqrt 3) ^ 2 := by
        rw [mul_pow, hs2]
        ring
  have hprod : (2 : ℝ) < rReal * Real.sqrt 3 := by
    have hnonneg : 0 ≤ rReal * Real.sqrt 3 :=
      mul_nonneg (le_of_lt hrpos) (le_of_lt hspos)
    nlinarith
  exact (div_lt_iff₀ hspos).2 hprod

theorem dodeca_ratio_upper_lt_deltaQ :
    ((4 * piUpperQ / 3) / dodecaVolumeLowerQ) < deltaQ := by
  norm_num [piUpperQ, dodecaVolumeLowerQ, deltaQ]

theorem dodeca_ratio_transfer
    {π₀ V : ℝ}
    (hπ : π₀ < (piUpperQ : ℝ))
    (hV : (dodecaVolumeLowerQ : ℝ) < V) :
    (4 * π₀ / 3) / V < (deltaQ : ℝ) := by
  let a : ℝ := 4 * π₀ / 3
  let b : ℝ := 4 * (piUpperQ : ℝ) / 3
  let L : ℝ := (dodecaVolumeLowerQ : ℝ)
  have hLpos : 0 < L := by
    norm_num [L, dodecaVolumeLowerQ]
  have hVpos : 0 < V := lt_trans hLpos hV
  have hb_pos : 0 < b := by
    norm_num [b, piUpperQ]
  have hab : a < b := by
    dsimp [a, b]
    nlinarith
  have hcross : a * L < b * V := by
    calc
      a * L ≤ b * L := mul_le_mul_of_nonneg_right (le_of_lt hab) (le_of_lt hLpos)
      _ < b * V := mul_lt_mul_of_pos_left hV hb_pos
  have hratio : a / V < b / L := (div_lt_div_iff₀ hVpos hLpos).2 hcross
  have hcert : b / L < (deltaQ : ℝ) := by
    norm_num [b, L, piUpperQ, dodecaVolumeLowerQ, deltaQ]
  exact lt_trans hratio hcert

end Erdos1084
