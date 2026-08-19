import Mathlib
import Erdos1084.KeplerOneRadiusOptimality
import Erdos1084.KeplerOptimizedChord

namespace Erdos1084

/-!
# Concrete one-radius minimax theorem

The earlier minimax module kept strict decrease of the degree-eleven endpoint profile as an
ordinary theorem parameter.  This file discharges that parameter.

The trigonometric endpoint profile is written algebraically as

`B₁₁(r) = r² + A r - C r sqrt(r²-1)`,

where `A = cos(ρ₁₁-π/6)`, `C = sin(ρ₁₁-π/6)`, and `A²+C²=1`.
Its derivative is negative once

`A * r * (4*r²-3) < 1`.

Exact rational bounds prove that inequality uniformly on `[2,kpRadius]`.
-/

noncomputable section

/-- Cosine of `ρ₁₁-π/6`, written in the algebraic endpoint coordinates. -/
def kpEndpointElevenCos : ℝ :=
  (rtLower * rtS + kpLowerY) / 2

/-- Sine of `ρ₁₁-π/6`, written in the algebraic endpoint coordinates. -/
def kpEndpointElevenSin : ℝ :=
  (kpLowerY * rtS - rtLower) / 2

/-- Scaled degree-eleven endpoint profile. -/
def kpEndpointElevenProfile (r : ℝ) : ℝ :=
  r ^ 2 + kpEndpointElevenCos * r -
    kpEndpointElevenSin * (r * Real.sqrt (r ^ 2 - 1))

/-- Simplified derivative of the degree-eleven profile. -/
def kpEndpointElevenDerivative (r : ℝ) : ℝ :=
  2 * r + kpEndpointElevenCos -
    kpEndpointElevenSin * (2 * r ^ 2 - 1) / Real.sqrt (r ^ 2 - 1)

/-- The lower endpoint coordinates lie on the unit circle. -/
theorem kp_lower_endpoint_circle :
    rtLower ^ 2 + kpLowerY ^ 2 = 1 := by
  rw [kpLowerY_sq]
  ring

/-- The two rotated endpoint constants lie on the unit circle. -/
theorem kpEndpointElevenCosSin_sq :
    kpEndpointElevenCos ^ 2 + kpEndpointElevenSin ^ 2 = 1 := by
  calc
    kpEndpointElevenCos ^ 2 + kpEndpointElevenSin ^ 2 =
        (rtS ^ 2 + 1) * (rtLower ^ 2 + kpLowerY ^ 2) / 4 := by
          dsimp [kpEndpointElevenCos, kpEndpointElevenSin]
          ring
    _ = 1 := by
      rw [rtS_sq, kp_lower_endpoint_circle]
      norm_num

/-- The cosine constant is strictly positive. -/
theorem kpEndpointElevenCos_pos : 0 < kpEndpointElevenCos := by
  have hleft0 : 0 ≤ -rtLower * rtS :=
    mul_nonneg (neg_nonneg.mpr (le_of_lt kp_rtLower_lt_zero)) rtS_nonneg
  have hsq : (-rtLower * rtS) ^ 2 < kpLowerY ^ 2 := by
    calc
      (-rtLower * rtS) ^ 2 = 3 * rtLower ^ 2 := by
        rw [mul_pow, rtS_sq]
        ring
      _ < 1 - rtLower ^ 2 := by
        nlinarith [kp_rtLower_sq_lt_quarter]
      _ = kpLowerY ^ 2 := by rw [kpLowerY_sq]
  have hygt : -rtLower * rtS < kpLowerY := by
    by_contra hnot
    have hle : kpLowerY ≤ -rtLower * rtS := le_of_not_gt hnot
    have hprod :
        0 ≤ (-rtLower * rtS - kpLowerY) *
          (-rtLower * rtS + kpLowerY) :=
      mul_nonneg (sub_nonneg.mpr hle)
        (add_nonneg hleft0 kpLowerY_nonneg)
    have hsqle : kpLowerY ^ 2 ≤ (-rtLower * rtS) ^ 2 := by
      nlinarith
    exact (not_lt_of_ge hsqle) hsq
  dsimp [kpEndpointElevenCos]
  linarith

/-- The sine constant is strictly positive. -/
theorem kpEndpointElevenSin_pos : 0 < kpEndpointElevenSin := by
  have hprod : 0 ≤ kpLowerY * rtS :=
    mul_nonneg kpLowerY_nonneg rtS_nonneg
  dsimp [kpEndpointElevenSin]
  linarith [kp_rtLower_lt_zero]

/-- A convenient exact lower bound for `sqrt 3`. -/
theorem rtS_lower_433_div_250 :
    (433 : ℝ) / 250 < rtS := by
  have hq0 : 0 ≤ (433 : ℝ) / 250 := by norm_num
  have hq2 : ((433 : ℝ) / 250) ^ 2 < 3 := by norm_num
  by_contra hnot
  have hle : rtS ≤ (433 : ℝ) / 250 := le_of_not_gt hnot
  have hprod :
      0 ≤ ((433 : ℝ) / 250 - rtS) *
        ((433 : ℝ) / 250 + rtS) :=
    mul_nonneg (sub_nonneg.mpr hle) (add_nonneg hq0 rtS_nonneg)
  have hsle : rtS ^ 2 ≤ ((433 : ℝ) / 250) ^ 2 := by
    nlinarith
  rw [rtS_sq] at hsle
  linarith

/-- The absolute value of the lower cosine endpoint is above `0.4737`. -/
theorem kp_neg_rtLower_gt_4737 :
    (4737 : ℝ) / 10000 < -rtLower := by
  have hs : rtS < (1732050808 : ℝ) / 1000000000 := by
    simpa [rtS, kpS] using kpS_lt_compact
  dsimp [rtLower]
  linarith

/-- The lower endpoint sine is below `0.881`. -/
theorem kpLowerY_lt_881 :
    kpLowerY < (881 : ℝ) / 1000 := by
  let a : ℝ := (4737 : ℝ) / 10000
  let b : ℝ := (881 : ℝ) / 1000
  have ha0 : 0 ≤ a := by norm_num [a]
  have hL0 : 0 ≤ -rtLower := neg_nonneg.mpr (le_of_lt kp_rtLower_lt_zero)
  have hL : a < -rtLower := by
    simpa [a] using kp_neg_rtLower_gt_4737
  have hLsq : a ^ 2 < rtLower ^ 2 := by
    have hsum : 0 < -rtLower + a := by linarith
    have hprod : 0 < (-rtLower - a) * (-rtLower + a) :=
      mul_pos (sub_pos.mpr hL) hsum
    nlinarith
  by_contra hnot
  have hy : b ≤ kpLowerY := le_of_not_gt hnot
  have hb0 : 0 ≤ b := by norm_num [b]
  have hysq : b ^ 2 ≤ kpLowerY ^ 2 := by
    have hprod : 0 ≤ (kpLowerY - b) * (kpLowerY + b) :=
      mul_nonneg (sub_nonneg.mpr hy) (add_nonneg kpLowerY_nonneg hb0)
    nlinarith
  have hcircle := kp_lower_endpoint_circle
  have hsumRat : 1 < a ^ 2 + b ^ 2 := by norm_num [a, b]
  nlinarith

/-- A compact upper bound on the cosine constant. -/
theorem kpEndpointElevenCos_lt_31_div_1000 :
    kpEndpointElevenCos < (31 : ℝ) / 1000 := by
  have hLs : rtLower * rtS = (33 - 20 * rtS) / 2 := by
    calc
      rtLower * rtS = (11 * rtS ^ 2 - 20 * rtS) / 2 := by
        dsimp [rtLower]
        ring
      _ = (33 - 20 * rtS) / 2 := by
        rw [rtS_sq]
        norm_num
  have hs := rtS_lower_433_div_250
  have hy := kpLowerY_lt_881
  dsimp [kpEndpointElevenCos]
  rw [hLs]
  linarith

/-- The optimized radius is below `2.12`. -/
theorem kpRadius_lt_53_div_25 :
    kpRadius < (53 : ℝ) / 25 := by
  have hs := kpS_lt_compact
  dsimp [kpRadius, kpS] at hs ⊢
  linarith

/-- Uniform endpoint inequality controlling the derivative on `[2,r_*]`. -/
theorem kpEndpointEleven_product_lt_one
    {r : ℝ} (hr2 : 2 ≤ r) (hrStar : r ≤ kpRadius) :
    kpEndpointElevenCos * r * (4 * r ^ 2 - 3) < 1 := by
  have hA : kpEndpointElevenCos < (31 : ℝ) / 1000 :=
    kpEndpointElevenCos_lt_31_div_1000
  have hr0 : 0 < r := by linarith
  have hr : r < (53 : ℝ) / 25 :=
    lt_of_le_of_lt hrStar kpRadius_lt_53_div_25
  have hsum : 0 < r + (53 : ℝ) / 25 := by linarith
  have hrsq : r ^ 2 < ((53 : ℝ) / 25) ^ 2 := by
    have hprod :
        0 < ((53 : ℝ) / 25 - r) * (r + (53 : ℝ) / 25) :=
      mul_pos (sub_pos.mpr hr) hsum
    nlinarith
  have hfactor0 : 0 < 4 * r ^ 2 - 3 := by nlinarith
  have hfactor :
      4 * r ^ 2 - 3 < 4 * ((53 : ℝ) / 25) ^ 2 - 3 := by
    nlinarith
  have hAr :
      kpEndpointElevenCos * r <
        ((31 : ℝ) / 1000) * ((53 : ℝ) / 25) := by
    calc
      kpEndpointElevenCos * r < ((31 : ℝ) / 1000) * r :=
        mul_lt_mul_of_pos_right hA hr0
      _ < ((31 : ℝ) / 1000) * ((53 : ℝ) / 25) :=
        mul_lt_mul_of_pos_left hr (by norm_num)
  have hbound :
      kpEndpointElevenCos * r * (4 * r ^ 2 - 3) <
        ((31 : ℝ) / 1000) * ((53 : ℝ) / 25) *
          (4 * ((53 : ℝ) / 25) ^ 2 - 3) := by
    calc
      kpEndpointElevenCos * r * (4 * r ^ 2 - 3) <
          (((31 : ℝ) / 1000) * ((53 : ℝ) / 25)) *
            (4 * r ^ 2 - 3) :=
        mul_lt_mul_of_pos_right hAr hfactor0
      _ < ((31 : ℝ) / 1000) * ((53 : ℝ) / 25) *
            (4 * ((53 : ℝ) / 25) ^ 2 - 3) :=
        mul_lt_mul_of_pos_left hfactor (by norm_num)
  have hrat :
      ((31 : ℝ) / 1000) * ((53 : ℝ) / 25) *
          (4 * ((53 : ℝ) / 25) ^ 2 - 3) < 1 := by
    norm_num
  exact lt_trans hbound hrat

/-- Algebraic derivative-negativity lemma. -/
theorem endpointElevenDerivative_neg_of_product
    {A C r : ℝ}
    (hA : 0 < A) (hC : 0 < C)
    (hcircle : A ^ 2 + C ^ 2 = 1)
    (hr2 : 2 ≤ r)
    (hproduct : A * r * (4 * r ^ 2 - 3) < 1) :
    2 * r + A - C * (2 * r ^ 2 - 1) / Real.sqrt (r ^ 2 - 1) < 0 := by
  have hrad : 0 < r ^ 2 - 1 := by nlinarith
  have ht : 0 < Real.sqrt (r ^ 2 - 1) := Real.sqrt_pos.2 hrad
  have ht2 : Real.sqrt (r ^ 2 - 1) ^ 2 = r ^ 2 - 1 :=
    Real.sq_sqrt (le_of_lt hrad)
  have hnum : 0 < 2 * r ^ 2 - 1 := by nlinarith
  have hX : 0 < C * (2 * r ^ 2 - 1) := mul_pos hC hnum
  have hY : 0 < (2 * r + A) * Real.sqrt (r ^ 2 - 1) :=
    mul_pos (by nlinarith) ht
  have hC2 : C ^ 2 = 1 - A ^ 2 := by nlinarith [hcircle]
  have hid :
      (C * (2 * r ^ 2 - 1)) ^ 2 -
          ((2 * r + A) * Real.sqrt (r ^ 2 - 1)) ^ 2 =
        (A * r + 1) * (1 - A * r * (4 * r ^ 2 - 3)) := by
    rw [mul_pow, mul_pow, ht2, hC2]
    ring
  have hright :
      0 < (A * r + 1) * (1 - A * r * (4 * r ^ 2 - 3)) :=
    mul_pos (by positivity) (sub_pos.mpr hproduct)
  have hsq :
      ((2 * r + A) * Real.sqrt (r ^ 2 - 1)) ^ 2 <
        (C * (2 * r ^ 2 - 1)) ^ 2 := by
    nlinarith
  have hlinear :
      (2 * r + A) * Real.sqrt (r ^ 2 - 1) <
        C * (2 * r ^ 2 - 1) := by
    by_contra hnot
    have hle : C * (2 * r ^ 2 - 1) ≤
        (2 * r + A) * Real.sqrt (r ^ 2 - 1) := le_of_not_gt hnot
    have hprod :
        0 ≤
          ((2 * r + A) * Real.sqrt (r ^ 2 - 1) -
              C * (2 * r ^ 2 - 1)) *
            ((2 * r + A) * Real.sqrt (r ^ 2 - 1) +
              C * (2 * r ^ 2 - 1)) :=
      mul_nonneg (sub_nonneg.mpr hle)
        (add_nonneg (le_of_lt hY) (le_of_lt hX))
    have hsqle :
        (C * (2 * r ^ 2 - 1)) ^ 2 ≤
          ((2 * r + A) * Real.sqrt (r ^ 2 - 1)) ^ 2 := by
      nlinarith
    exact (not_lt_of_ge hsqle) hsq
  have hdiv :
      2 * r + A < C * (2 * r ^ 2 - 1) / Real.sqrt (r ^ 2 - 1) :=
    (lt_div_iff₀ ht).2 hlinear
  linarith

/-- Exact derivative of the concrete degree-eleven endpoint profile. -/
theorem kpEndpointElevenProfile_hasDerivAt
    {r : ℝ} (hr : 1 < r) :
    HasDerivAt kpEndpointElevenProfile (kpEndpointElevenDerivative r) r := by
  have hrad : 0 < r ^ 2 - 1 := by nlinarith
  have hradne : r ^ 2 - 1 ≠ 0 := ne_of_gt hrad
  have htne : Real.sqrt (r ^ 2 - 1) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 hrad)
  have hsqRaw := (hasDerivAt_id r).mul (hasDerivAt_id r)
  change HasDerivAt (fun x : ℝ => x * x) (r + r) r at hsqRaw
  have hsq : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
    simpa [pow_two, two_mul] using hsqRaw
  have hinner : HasDerivAt (fun x : ℝ => x ^ 2 - 1) (2 * r) r :=
    hsq.sub_const 1
  have hsqrt := hinner.sqrt hradne
  have hxsqrtRaw := (hasDerivAt_id r).mul hsqrt
  change HasDerivAt
    (fun x : ℝ => x * Real.sqrt (x ^ 2 - 1))
    (Real.sqrt (r ^ 2 - 1) +
      r * (2 * r / (2 * Real.sqrt (r ^ 2 - 1)))) r at hxsqrtRaw
  have hxsqrt := hxsqrtRaw
  have hlinearRaw := (hasDerivAt_id r).const_mul kpEndpointElevenCos
  change HasDerivAt (fun x : ℝ => kpEndpointElevenCos * x)
    kpEndpointElevenCos r at hlinearRaw
  have hlinear := hlinearRaw
  have hpolyRaw := hsq.add hlinear
  change HasDerivAt
    (fun x : ℝ => x ^ 2 + kpEndpointElevenCos * x)
    (2 * r + kpEndpointElevenCos) r at hpolyRaw
  have hpoly := hpolyRaw
  have hscaledRaw := hxsqrt.const_mul kpEndpointElevenSin
  change HasDerivAt
    (fun x : ℝ => kpEndpointElevenSin *
      (x * Real.sqrt (x ^ 2 - 1)))
    (kpEndpointElevenSin *
      (Real.sqrt (r ^ 2 - 1) +
        r * (2 * r / (2 * Real.sqrt (r ^ 2 - 1))))) r at hscaledRaw
  have hscaled := hscaledRaw
  have hrawRaw := hpoly.sub hscaled
  change HasDerivAt
    (fun x : ℝ =>
      x ^ 2 + kpEndpointElevenCos * x -
        kpEndpointElevenSin * (x * Real.sqrt (x ^ 2 - 1)))
    ((2 * r + kpEndpointElevenCos) -
      kpEndpointElevenSin *
        (Real.sqrt (r ^ 2 - 1) +
          r * (2 * r / (2 * Real.sqrt (r ^ 2 - 1))))) r at hrawRaw
  have hraw :
      HasDerivAt kpEndpointElevenProfile
        ((2 * r + kpEndpointElevenCos) -
          kpEndpointElevenSin *
            (Real.sqrt (r ^ 2 - 1) +
              r * (2 * r / (2 * Real.sqrt (r ^ 2 - 1))))) r := by
    simpa [kpEndpointElevenProfile] using hrawRaw
  have hderiv :
      (2 * r + kpEndpointElevenCos) -
          kpEndpointElevenSin *
            (Real.sqrt (r ^ 2 - 1) +
              r * (2 * r / (2 * Real.sqrt (r ^ 2 - 1)))) =
        kpEndpointElevenDerivative r := by
    dsimp [kpEndpointElevenDerivative]
    field_simp [htne]
    rw [Real.sq_sqrt (le_of_lt hrad)]
    ring
  simpa only [hderiv] using hraw

/-- The concrete derivative is negative throughout the optimized interval. -/
theorem kpEndpointElevenDerivative_neg
    {r : ℝ} (hr2 : 2 ≤ r) (hrStar : r ≤ kpRadius) :
    kpEndpointElevenDerivative r < 0 := by
  unfold kpEndpointElevenDerivative
  exact endpointElevenDerivative_neg_of_product
    kpEndpointElevenCos_pos kpEndpointElevenSin_pos kpEndpointElevenCosSin_sq
    hr2 (kpEndpointEleven_product_lt_one hr2 hrStar)

/-- The concrete degree-eleven endpoint profile is strictly decreasing on `[2,r_*]`. -/
theorem kpEndpointElevenProfile_strictAntiOn :
    StrictAntiOn kpEndpointElevenProfile (Set.Icc (2 : ℝ) kpRadius) := by
  refine strictAntiOn_of_deriv_neg (convex_Icc _ _) ?_ ?_
  · unfold kpEndpointElevenProfile
    fun_prop
  · intro r hr
    have hrIcc : r ∈ Set.Icc (2 : ℝ) kpRadius := interior_subset hr
    have hr1 : 1 < r := by linarith [hrIcc.1]
    rw [(kpEndpointElevenProfile_hasDerivAt hr1).deriv]
    exact kpEndpointElevenDerivative_neg hrIcc.1 hrIcc.2

/-- The optimized reciprocal relation in product form. -/
theorem kpRadius_mul_rtLower :
    kpRadius * rtLower = -1 := by
  have hrec := kpRadius_reciprocal_eq_neg_lower
  have hrne : kpRadius ≠ 0 := ne_of_gt kpRadius_pos
  have h : (1 : ℝ) = (-rtLower) * kpRadius :=
    (div_eq_iff hrne).mp hrec
  calc
    kpRadius * rtLower = -((-rtLower) * kpRadius) := by ring
    _ = -1 := by rw [← h]

/-- Projection of the rotated endpoint coordinates onto the lower endpoint. -/
theorem kpEndpointEleven_projection :
    kpEndpointElevenCos * rtLower +
      kpEndpointElevenSin * kpLowerY = rtS / 2 := by
  calc
    kpEndpointElevenCos * rtLower +
        kpEndpointElevenSin * kpLowerY =
      rtS * (rtLower ^ 2 + kpLowerY ^ 2) / 2 := by
        dsimp [kpEndpointElevenCos, kpEndpointElevenSin]
        ring
    _ = rtS / 2 := by rw [kp_lower_endpoint_circle]; ring

/-- The square root at the optimizer is `r_*` times the lower endpoint height. -/
theorem kpRadius_sqrt_sub_one :
    Real.sqrt (kpRadius ^ 2 - 1) = kpRadius * kpLowerY := by
  have hrad : 0 ≤ kpRadius ^ 2 - 1 := by
    nlinarith [two_lt_kpRadius]
  have hsqrt2 := Real.sq_sqrt hrad
  have htarget2 : (kpRadius * kpLowerY) ^ 2 = kpRadius ^ 2 - 1 := by
    calc
      (kpRadius * kpLowerY) ^ 2 =
          kpRadius ^ 2 * (1 - rtLower ^ 2) := by
            rw [mul_pow, kpLowerY_sq]
      _ = kpRadius ^ 2 - (kpRadius * rtLower) ^ 2 := by ring
      _ = kpRadius ^ 2 - 1 := by rw [kpRadius_mul_rtLower]; norm_num
  have hsqrt0 := Real.sqrt_nonneg (kpRadius ^ 2 - 1)
  have htarget0 : 0 ≤ kpRadius * kpLowerY :=
    mul_nonneg (le_of_lt kpRadius_pos) kpLowerY_nonneg
  nlinarith

/-- Exact crossing of the two concrete endpoint profiles. -/
theorem kpEndpointElevenProfile_at_optimizer :
    kpEndpointElevenProfile kpRadius = kpEndpointOneProfile kpRadius := by
  have hproj := kpEndpointEleven_projection
  have hrL := kpRadius_mul_rtLower
  have hsqrt := kpRadius_sqrt_sub_one
  have hQ := kpEndpointOneProfile_at_optimizer
  have hlin :
      kpEndpointElevenCos -
          kpRadius * kpEndpointElevenSin * kpLowerY =
        -kpRadius * rtS / 2 := by
    calc
      kpEndpointElevenCos -
          kpRadius * kpEndpointElevenSin * kpLowerY =
        -(kpEndpointElevenCos * (kpRadius * rtLower) +
            kpRadius * kpEndpointElevenSin * kpLowerY) := by
          rw [hrL]
          ring
      _ = -(kpRadius *
          (kpEndpointElevenCos * rtLower +
            kpEndpointElevenSin * kpLowerY)) := by ring
      _ = -(kpRadius * (rtS / 2)) := by rw [hproj]
      _ = -kpRadius * rtS / 2 := by ring
  rw [hQ]
  change kpEndpointElevenProfile kpRadius =
    kpRadius ^ 2 * (1 - rtS / 2)
  rw [kpEndpointElevenProfile, hsqrt]
  calc
    kpRadius ^ 2 + kpEndpointElevenCos * kpRadius -
        kpEndpointElevenSin *
          (kpRadius * (kpRadius * kpLowerY)) =
      kpRadius ^ 2 + kpRadius *
        (kpEndpointElevenCos -
          kpRadius * kpEndpointElevenSin * kpLowerY) := by ring
    _ = kpRadius ^ 2 + kpRadius * (-kpRadius * rtS / 2) := by
      rw [hlin]
    _ = kpRadius ^ 2 * (1 - rtS / 2) := by ring

/-- Fully concrete unique optimality theorem, with no degree-eleven monotonicity parameter. -/
theorem kpRadius_unique_oneRadius_optimum_concrete :
    ∀ ⦃r : ℝ⦄, 2 ≤ r → r ≠ kpRadius →
      max (kpEndpointOneProfile r) (kpEndpointElevenProfile r) >
        kpEndpointOneProfile kpRadius := by
  exact kpRadius_unique_oneRadius_optimum
    kpEndpointElevenProfile
    kpEndpointElevenProfile_strictAntiOn
    kpEndpointElevenProfile_at_optimizer

end

end Erdos1084
