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

/-! Radius-two algebra and assembly. -/

example : (82099 : ℝ) < 47400 * rtS :=
  rt_endpoint_root_margin

example : rtP rtUpper = 21 / 4 := rtP_upper

example : rtP rtLower = (47400 * rtS - 82099) / 4 := rtP_lower

example {x : ℝ} (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    0 < rtP x :=
  rtP_pos_on_interval hxL hxU

example {d : ℝ} (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    rtH (rtX d) < (3 / 20 : ℝ) * (12 - d) :=
  radiusTwo_degree_envelope hd1 hd11

example {x A D : ℝ}
    (hLower : 4 * Real.pi * x ≤ A)
    (hUpper : A < (12 * Real.pi / 5) * D) :
    (5 / 3 : ℝ) * x < D :=
  radiusTwo_surface_to_deficit hLower hUpper

/-! Explicit bridges from the external geometric inputs. -/

example (u v : RadiusTwoE3) : ‖u - v‖ = ‖v - u‖ :=
  radiusTwo_norm_sub_comm u v

example (u v : RadiusTwoE3) :
    ‖(2 : ℝ) • v - (2 : ℝ) • u‖ ≤ 2 ↔ ‖v - u‖ ≤ 1 :=
  radiusTwo_covering_ball_iff u v

example
    (hk : KissingNumberAtMostTwelve)
    (s : Finset RadiusTwoE3)
    (hcard : s.card = 12)
    (hunit : ∀ u ∈ s, ‖u‖ = 1)
    (hsep : ∀ u ∈ s, ∀ v ∈ s, u ≠ v → 1 ≤ ‖u - v‖)
    {w : RadiusTwoE3}
    (hw : ‖w‖ = 1) :
    ∃ u ∈ s, ‖w - u‖ ≤ 1 :=
  kissing_twelve_closed_cap_cover hk s hcard hunit hsep hw

example
    {n x V A : ℝ}
    (hn : 0 ≤ n)
    (hx : 0 ≤ x)
    (hroot : x ^ 3 = n ^ 2)
    (hV : (4 * Real.pi / 3) * n ≤ V)
    (hVnonneg : 0 ≤ V)
    (hAnonneg : 0 ≤ A)
    (hIso : 36 * Real.pi * V ^ 2 ≤ A ^ 3) :
    4 * Real.pi * x ≤ A :=
  euclidean_isoperimetric_to_radiusTwo_lower
    hn hx hroot hV hVnonneg hAnonneg hIso

example
    {d q H covered exposure : ℝ}
    (hCovered : 2 * Real.pi * (1 - q) ≤ covered)
    (hExposure : exposure ≤ 4 * (4 * Real.pi - covered))
    (hH : H = 1 + q)
    (hEnvelope : H < (3 / 20 : ℝ) * (12 - d)) :
    exposure < (6 * Real.pi / 5) * (12 - d) :=
  spherical_neighborhood_to_local_charge
    hCovered hExposure hH hEnvelope
