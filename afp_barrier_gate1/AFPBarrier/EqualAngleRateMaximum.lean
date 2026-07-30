import AFPBarrier.EqualAngleAsymptotics
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# Polar-ring maximum of the square-grid jump rate

The deterministic audit observed that the largest rate occurs on the two polar
rings.  This file proves that statement for every order.  The key geometric
fact is that every cell-centred latitude lies in `[h, π-h]`, so its sine is at
least `sin h`.
-/

namespace AFPBarrier

noncomputable section

/-- Sine attains its minimum at the endpoints of a symmetric interval
`[h, π-h]` contained in `[0,π]`. -/
theorem sin_halfStep_le_of_mem_symmetric_interval
    (h theta : ℝ)
    (hh0 : 0 ≤ h) (hhhalf : h ≤ Real.pi / 2)
    (htlo : h ≤ theta) (hthi : theta ≤ Real.pi - h) :
    Real.sin h ≤ Real.sin theta := by
  by_cases hleft : theta ≤ Real.pi / 2
  · exact Real.sin_le_sin_of_le_of_le_pi_div_two
      (by linarith [Real.pi_pos]) hleft htlo
  · have hreflo : h ≤ Real.pi - theta := by linarith
    have hrefhalf : Real.pi - theta ≤ Real.pi / 2 := by linarith
    have href := Real.sin_le_sin_of_le_of_le_pi_div_two
      (by linarith [Real.pi_pos]) hrefhalf hreflo
    rwa [Real.sin_pi_sub] at href

/-- Every cell-centred grid latitude belongs to `[h,π-h]`. -/
theorem equalAngleGridTheta_mem_symmetric_interval
    (n i : ℝ) (hn : 2 ≤ n) (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    equalAngleGridHalfStep n ≤ equalAngleGridTheta n i
      ∧ equalAngleGridTheta n i
          ≤ Real.pi - equalAngleGridHalfStep n := by
  have hn0 : 0 < n := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hscale :
      2 * n * equalAngleGridHalfStep n = Real.pi := by
    unfold equalAngleGridHalfStep
    field_simp [hn0.ne']
    ring
  have hleftcoef : 1 ≤ 2 * i + 1 := by nlinarith
  have hrightcoef : 2 * i + 2 ≤ 2 * n := by nlinarith
  have hleftmul := mul_le_mul_of_nonneg_right hleftcoef hh0.le
  have hrightmul := mul_le_mul_of_nonneg_right hrightcoef hh0.le
  unfold equalAngleGridTheta
  constructor
  · nlinarith
  · nlinarith

/-- The polar latitude sine is no larger than the sine on any ring. -/
theorem equalAngleGrid_sin_halfStep_le_sin_theta
    (n i : ℝ) (hn : 2 ≤ n) (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    Real.sin (equalAngleGridHalfStep n)
      ≤ Real.sin (equalAngleGridTheta n i) := by
  have hn0 : 0 < n := by linarith
  have hh0 := (equalAngleGridHalfStep_pos n hn0).le
  have hhhalf := (equalAngleGridHalfStep_lt_pi_div_two n hn).le
  obtain ⟨htlo, hthi⟩ :=
    equalAngleGridTheta_mem_symmetric_interval n i hn hi0 hiN
  exact sin_halfStep_le_of_mem_symmetric_interval
    (equalAngleGridHalfStep n) (equalAngleGridTheta n i)
    hh0 hhhalf htlo hthi

/-- Algebraically, increasing the squared latitude sine can only decrease the
square-grid ring rate. -/
theorem squareRingRate_le_polar_of_sin_sq
    (h st : ℝ)
    (hs : 0 < Real.sin h)
    (hst : Real.sin h ^ 2 ≤ st ^ 2) :
    squareRingRate h st ≤ squarePolarRateFromStep h := by
  have hs2pos : 0 < Real.sin h ^ 2 := sq_pos_of_pos hs
  have hst2pos : 0 < st ^ 2 := lt_of_lt_of_le hs2pos hst
  have hden :
      2 * Real.sin h ^ 4
        ≤ 2 * Real.sin h ^ 2 * st ^ 2 := by
    have hp := mul_le_mul_of_nonneg_left hst
      (by positivity : 0 ≤ 2 * Real.sin h ^ 2)
    nlinarith
  have hrec :
      1 / (2 * Real.sin h ^ 2 * st ^ 2)
        ≤ 1 / (2 * Real.sin h ^ 4) := by
    apply (div_le_div_iff₀
      (by positivity : 0 < 2 * Real.sin h ^ 2 * st ^ 2)
      (by positivity : 0 < 2 * Real.sin h ^ 4)).2
    nlinarith
  unfold squareRingRate squarePolarRateFromStep
  linarith

/-- At every ring of every square equal-angle grid, the total rate is bounded
above by the polar-ring rate.  Equality holds on the polar rings themselves. -/
theorem equalAngleGrid_squareRingRate_le_polar
    (n i : ℝ) (hn : 2 ≤ n) (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    squareRingRate (equalAngleGridHalfStep n)
        (Real.sin (equalAngleGridTheta n i))
      ≤ squarePolarRateFromStep (equalAngleGridHalfStep n) := by
  have hn0 : 0 < n := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hhhalf := equalAngleGridHalfStep_lt_pi_div_two n hn
  have hspos : 0 < Real.sin (equalAngleGridHalfStep n) :=
    Real.sin_pos_of_pos_of_lt_pi hh0 (by linarith [Real.pi_pos])
  have ht0 := equalAngleGridTheta_pos n i hn0 hi0
  have htpi := equalAngleGridTheta_lt_pi n i hn0 hiN
  have htpos : 0 < Real.sin (equalAngleGridTheta n i) :=
    Real.sin_pos_of_pos_of_lt_pi ht0 htpi
  have hsle := equalAngleGrid_sin_halfStep_le_sin_theta
    n i hn hi0 hiN
  have hsq :
      Real.sin (equalAngleGridHalfStep n) ^ 2
        ≤ Real.sin (equalAngleGridTheta n i) ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hsle)
      (add_nonneg hspos.le htpos.le)
    nlinarith
  exact squareRingRate_le_polar_of_sin_sq
    (equalAngleGridHalfStep n)
    (Real.sin (equalAngleGridTheta n i)) hspos hsq

end

end AFPBarrier
