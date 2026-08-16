import Erdos1084

open Erdos1084

/-! Smoke tests for the formally certified arithmetic and algebraic spine. -/

example : (2 : ℚ) < rQ ^ 2 := rQ_sq_gt_two

example : (4 : ℚ) / rQ < 63 / 25 :=
  four_div_rQ_lt_two_point_five_two

example : (4 : ℚ) < 3 * rQ ^ 2 := three_rQ_sq_gt_four

example : (19 : ℝ) < 11 * Real.sqrt 3 :=
  nineteen_lt_eleven_sqrt_three

example : Real.sqrt 2 < rReal := sqrt_two_lt_rReal

example : (2 : ℝ) / Real.sqrt 3 < rReal :=
  two_div_sqrt_three_lt_rReal

example : ((4 * piUpperQ / 3) / dodecaVolumeLowerQ) < deltaQ :=
  dodeca_ratio_upper_lt_deltaQ

example (n E : ℤ) : 12 * n - 2 * E = 2 * (6 * n - E) :=
  degree_sum_arithmetic n E

example {H q δ : ℝ} (hH : 0 ≤ H) (hδ : 1 ≤ δ) :
    H + δ * q ≤ δ * (H + q) :=
  local_affine_charge hH hδ

example :
    h0Upper < h11Lower ∧
    h1Upper < h11Lower ∧
    h2Upper < h11Lower ∧
    h3Upper < h11Lower ∧
    h4Upper < h11Lower ∧
    h5Upper < h11Lower ∧
    h6Upper < h11Lower ∧
    h7Upper < h11Lower ∧
    h8Upper < h11Lower ∧
    h9Upper < h11Lower ∧
    h10Upper < h11Lower :=
  degree_eleven_unique_maximum

example : ((cleanQ * rQ ^ 2 * H11Upper) ^ 3 * deltaQ ^ 2) < 1 :=
  clean_coefficient_cubed_certificate

example :
    (((150797 : ℚ) / 125000) ^ 3 * ((7547 : ℚ) / 10000) ^ 2) < 1 :=
  fallback_degree_weighted_certificate
