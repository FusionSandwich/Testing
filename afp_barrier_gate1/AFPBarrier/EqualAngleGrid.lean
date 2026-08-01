import AFPBarrier.EqualAngleGeometry
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic

/-!
# All-order parameter theorem for the equal-angle grid

The local trigonometric identities are now instantiated with the actual grid
parameters. We use real-valued order and index parameters; every integer grid
with `N ≥ 2`, `M ≥ 3`, and ring index `i = 0, …, N-1` is an immediate
special case. This avoids hiding any analytic step behind a numerical test.
-/

namespace AFPBarrier

noncomputable section

/-- Half of the polar spacing `π / N`. -/
def equalAngleGridHalfStep (n : ℝ) : ℝ := Real.pi / (2 * n)

/-- Latitude of the cell-centred ring with index `i`. -/
def equalAngleGridTheta (n i : ℝ) : ℝ :=
  (2 * i + 1) * equalAngleGridHalfStep n

/-- Azimuthal spacing for `m` equally spaced directions per ring. -/
def equalAngleGridAzimuthStep (m : ℝ) : ℝ := 2 * Real.pi / m

/-- Azimuth of the direction with real index `j`; integer indices are the
intended specialization. -/
def equalAngleGridPhi (m j : ℝ) : ℝ :=
  j * equalAngleGridAzimuthStep m

/-- The half polar step is positive. -/
theorem equalAngleGridHalfStep_pos
    (n : ℝ) (hn : 0 < n) :
    0 < equalAngleGridHalfStep n := by
  unfold equalAngleGridHalfStep
  positivity

/-- For every order `n ≥ 2`, the half polar step lies below `π/2`. -/
theorem equalAngleGridHalfStep_lt_pi_div_two
    (n : ℝ) (hn : 2 ≤ n) :
    equalAngleGridHalfStep n < Real.pi / 2 := by
  have hn0 : 0 < n := by linarith
  unfold equalAngleGridHalfStep
  apply (div_lt_iff₀ (mul_pos (by norm_num) hn0)).2
  nlinarith [Real.pi_pos]

/-- Every cell-centred latitude is strictly between the poles. -/
theorem equalAngleGridTheta_pos
    (n i : ℝ) (hn : 0 < n) (hi0 : 0 ≤ i) :
    0 < equalAngleGridTheta n i := by
  unfold equalAngleGridTheta
  exact mul_pos (by nlinarith) (equalAngleGridHalfStep_pos n hn)

/-- The upper ring-index bound places every cell centre below the south pole. -/
theorem equalAngleGridTheta_lt_pi
    (n i : ℝ) (hn : 0 < n) (hi : i ≤ n - 1) :
    equalAngleGridTheta n i < Real.pi := by
  have hden : 0 < 2 * n := mul_pos (by norm_num) hn
  unfold equalAngleGridTheta equalAngleGridHalfStep
  rw [← mul_div_assoc]
  apply (div_lt_iff₀ hden).2
  nlinarith [Real.pi_pos]

/-- The azimuthal step is positive. -/
theorem equalAngleGridAzimuthStep_pos
    (m : ℝ) (hm : 0 < m) :
    0 < equalAngleGridAzimuthStep m := by
  unfold equalAngleGridAzimuthStep
  positivity

/-- For `m > 1`, the azimuthal step is strictly below one full turn. -/
theorem equalAngleGridAzimuthStep_lt_two_pi
    (m : ℝ) (hm : 1 < m) :
    equalAngleGridAzimuthStep m < 2 * Real.pi := by
  have hm0 : 0 < m := lt_trans zero_lt_one hm
  unfold equalAngleGridAzimuthStep
  apply (div_lt_iff₀ hm0).2
  nlinarith [Real.pi_pos]

/-- A nontrivial angular step inside one full turn has positive
`1 - cos beta`. -/
theorem one_sub_cos_pos_of_pos_of_lt_two_pi
    (beta : ℝ) (hb0 : 0 < beta) (hb2pi : beta < 2 * Real.pi) :
    0 < 1 - Real.cos beta := by
  have hhalf0 : 0 < beta / 2 := by linarith
  have hhalfpi : beta / 2 < Real.pi := by linarith
  have hs : 0 < Real.sin (beta / 2) :=
    Real.sin_pos_of_pos_of_lt_pi hhalf0 hhalfpi
  have hs2 : 0 < Real.sin (beta / 2) ^ 2 := sq_pos_of_pos hs
  have htrig := Real.sin_sq_add_cos_sq (beta / 2)
  rw [show beta = 2 * (beta / 2) by ring, Real.cos_two_mul]
  ring_nf at htrig hs2 ⊢
  nlinarith

/-- The grid assumptions imply all nonvanishing denominator facts required by
the end-to-end coordinate proofs. -/
theorem equalAngleGrid_parameter_facts
    (n m i : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    let h := equalAngleGridHalfStep n
    let theta := equalAngleGridTheta n i
    let beta := equalAngleGridAzimuthStep m
    0 < h ∧ h < Real.pi / 2 ∧
    0 < theta ∧ theta < Real.pi ∧
    0 < beta ∧ beta < 2 * Real.pi ∧
    Real.sin h ≠ 0 ∧ Real.cos h ≠ 0 ∧
    Real.sin theta ≠ 0 ∧ 1 - Real.cos beta ≠ 0 := by
  dsimp
  have hn0 : 0 < n := by linarith
  have hm0 : 0 < m := by linarith
  have hm1 : 1 < m := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hhhalf := equalAngleGridHalfStep_lt_pi_div_two n hn
  have ht0 := equalAngleGridTheta_pos n i hn0 hi0
  have htpi := equalAngleGridTheta_lt_pi n i hn0 hiN
  have hb0 := equalAngleGridAzimuthStep_pos m hm0
  have hb2pi := equalAngleGridAzimuthStep_lt_two_pi m hm1
  have hsin_h_pos : 0 < Real.sin (equalAngleGridHalfStep n) :=
    Real.sin_pos_of_pos_of_lt_pi hh0 (by linarith [Real.pi_pos])
  have hcos_h_pos : 0 < Real.cos (equalAngleGridHalfStep n) :=
    Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], hhhalf⟩
  have hsin_t_pos : 0 < Real.sin (equalAngleGridTheta n i) :=
    Real.sin_pos_of_pos_of_lt_pi ht0 htpi
  have hv_pos := one_sub_cos_pos_of_pos_of_lt_two_pi
    (equalAngleGridAzimuthStep m) hb0 hb2pi
  exact ⟨hh0, hhhalf, ht0, htpi, hb0, hb2pi,
    hsin_h_pos.ne', hcos_h_pos.ne', hsin_t_pos.ne', hv_pos.ne'⟩

/-- Every admissible grid node has positive quadrature weight. -/
theorem equalAngleGrid_weight_pos
    (n m i : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    0 < equalAngleTrigWeight
      (equalAngleGridAzimuthStep m)
      (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) := by
  obtain ⟨hh0, hhhalf, ht0, htpi, hb0, hb2pi,
      hs, hc, hst, hv⟩ :=
    equalAngleGrid_parameter_facts n m i hn hm hi0 hiN
  apply equalAngleTrigWeight_pos
  · exact hb0
  · exact ht0
  · exact htpi
  · exact hh0
  · linarith [hhhalf, Real.pi_pos]

/-- Complete degree-one exactness at every admissible grid node. This theorem
contains no externally supplied balance equation: all balances are supplied by
the trigonometric theorems in `EqualAngleGeometry`. -/
theorem equalAngleGrid_coordinate_exact
    (n m i j : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    let h := equalAngleGridHalfStep n
    let theta := equalAngleGridTheta n i
    let beta := equalAngleGridAzimuthStep m
    let phi := equalAngleGridPhi m j
    productNodeAction
        (equalAngleTrigWeight beta theta h)
        (equalAngleMeridionalMinus beta theta h)
        (equalAngleMeridionalPlus beta theta h)
        (equalAngleTrigAzimuthConductance beta theta h beta)
        (Real.cos theta)
        (Real.cos (theta - 2 * h))
        (Real.cos (theta + 2 * h))
        (Real.cos theta) (Real.cos theta)
      = -2 * Real.cos theta
    ∧
    productNodeAction
        (equalAngleTrigWeight beta theta h)
        (equalAngleMeridionalMinus beta theta h)
        (equalAngleMeridionalPlus beta theta h)
        (equalAngleTrigAzimuthConductance beta theta h beta)
        (Real.sin theta * Real.cos phi)
        (Real.sin (theta - 2 * h) * Real.cos phi)
        (Real.sin (theta + 2 * h) * Real.cos phi)
        (Real.sin theta * Real.cos (phi - beta))
        (Real.sin theta * Real.cos (phi + beta))
      = -2 * (Real.sin theta * Real.cos phi)
    ∧
    productNodeAction
        (equalAngleTrigWeight beta theta h)
        (equalAngleMeridionalMinus beta theta h)
        (equalAngleMeridionalPlus beta theta h)
        (equalAngleTrigAzimuthConductance beta theta h beta)
        (Real.sin theta * Real.sin phi)
        (Real.sin (theta - 2 * h) * Real.sin phi)
        (Real.sin (theta + 2 * h) * Real.sin phi)
        (Real.sin theta * Real.sin (phi - beta))
        (Real.sin theta * Real.sin (phi + beta))
      = -2 * (Real.sin theta * Real.sin phi) := by
  dsimp
  obtain ⟨hh0, hhhalf, ht0, htpi, hb0, hb2pi,
      hs, hc, hst, hv⟩ :=
    equalAngleGrid_parameter_facts n m i hn hm hi0 hiN
  have hq : equalAngleTrigWeight
      (equalAngleGridAzimuthStep m)
      (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) ≠ 0 :=
    (equalAngleGrid_weight_pos n m i hn hm hi0 hiN).ne'
  constructor
  · exact equalAngle_productNodeAction_cos_eq
      (equalAngleGridAzimuthStep m) (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) (equalAngleGridAzimuthStep m)
      hq hs hc
  constructor
  · exact equalAngle_productNodeAction_sin_cos_eq
      (equalAngleGridAzimuthStep m) (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) (equalAngleGridAzimuthStep m)
      (equalAngleGridPhi m j) hq hs hc hst hv
  · exact equalAngle_productNodeAction_sin_sin_eq
      (equalAngleGridAzimuthStep m) (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) (equalAngleGridAzimuthStep m)
      (equalAngleGridPhi m j) hq hs hc hst hv

end

end AFPBarrier
