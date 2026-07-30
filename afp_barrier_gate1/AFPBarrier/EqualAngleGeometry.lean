import AFPBarrier.EqualAngleProduct
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic

/-!
# End-to-end trigonometric identities for the equal-angle AFP family

This file removes the main abstraction boundary left in the first Gate 3
formalization. The current latitude is `theta`, the half meridional step is
`h`, and the azimuthal step is `beta`, so the full polar step is `2*h`.

The definitions below are the actual trigonometric weights and shared-edge
conductances. The theorems prove the axial and both transverse coordinate
balances directly from the sine and cosine addition laws. Combined with the
normalization theorem in `EqualAngleProduct`, this proves exact preservation
of the complete degree-one eigenspace without assuming the local balance.
-/

namespace AFPBarrier

noncomputable section

/-- Exact spherical-cell weight at latitude `theta`. -/
def equalAngleTrigWeight (alpha theta h : ℝ) : ℝ :=
  equalAngleWeight alpha (Real.sin theta) (Real.sin h)

/-- Shared conductance to the ring at `theta - 2*h`. -/
def equalAngleMeridionalMinus (alpha theta h : ℝ) : ℝ :=
  alpha * Real.sin (theta - h) / Real.sin (2 * h)

/-- Shared conductance to the ring at `theta + 2*h`. -/
def equalAngleMeridionalPlus (alpha theta h : ℝ) : ℝ :=
  alpha * Real.sin (theta + h) / Real.sin (2 * h)

/-- Conductance of either azimuthal edge. -/
def equalAngleTrigAzimuthConductance
    (alpha theta h beta : ℝ) : ℝ :=
  equalAngleAzimuthConductance alpha (Real.sin h)
    (1 - Real.cos beta) (Real.sin theta)

/-- The exact cell weight is positive for positive angular factors. -/
theorem equalAngleTrigWeight_pos
    (alpha theta h : ℝ)
    (halpha : 0 < alpha)
    (htheta0 : 0 < theta) (hthetapi : theta < Real.pi)
    (hh0 : 0 < h) (hhpi : h < Real.pi) :
    0 < equalAngleTrigWeight alpha theta h := by
  apply equalAngleWeight_pos
  · exact halpha
  · exact Real.sin_pos_of_pos_of_lt_pi htheta0 hthetapi
  · exact Real.sin_pos_of_pos_of_lt_pi hh0 hhpi

/-- An actual lower meridional edge has positive conductance. -/
theorem equalAngleMeridionalMinus_pos
    (alpha theta h : ℝ)
    (halpha : 0 < alpha)
    (hlower0 : 0 < theta - h) (hlowerpi : theta - h < Real.pi)
    (hstep0 : 0 < 2 * h) (hsteppi : 2 * h < Real.pi) :
    0 < equalAngleMeridionalMinus alpha theta h := by
  unfold equalAngleMeridionalMinus
  exact div_pos
    (mul_pos halpha (Real.sin_pos_of_pos_of_lt_pi hlower0 hlowerpi))
    (Real.sin_pos_of_pos_of_lt_pi hstep0 hsteppi)

/-- An actual upper meridional edge has positive conductance. -/
theorem equalAngleMeridionalPlus_pos
    (alpha theta h : ℝ)
    (halpha : 0 < alpha)
    (hupper0 : 0 < theta + h) (hupperpi : theta + h < Real.pi)
    (hstep0 : 0 < 2 * h) (hsteppi : 2 * h < Real.pi) :
    0 < equalAngleMeridionalPlus alpha theta h := by
  unfold equalAngleMeridionalPlus
  exact div_pos
    (mul_pos halpha (Real.sin_pos_of_pos_of_lt_pi hupper0 hupperpi))
    (Real.sin_pos_of_pos_of_lt_pi hstep0 hsteppi)

/-- The azimuthal conductance is positive under the exact denominator
conditions used by the product grid. -/
theorem equalAngleTrigAzimuthConductance_pos
    (alpha theta h beta : ℝ)
    (halpha : 0 < alpha)
    (htheta0 : 0 < theta) (hthetapi : theta < Real.pi)
    (hh0 : 0 < h) (hhpi : h < Real.pi)
    (hbeta : 0 < 1 - Real.cos beta) :
    0 < equalAngleTrigAzimuthConductance alpha theta h beta := by
  apply equalAngleAzimuthConductance_pos
  · exact halpha
  · exact Real.sin_pos_of_pos_of_lt_pi hh0 hhpi
  · exact hbeta
  · exact Real.sin_pos_of_pos_of_lt_pi htheta0 hthetapi

/-- The two meridional conductances have the exact total required by the
algebraic rate and defect formulas. -/
theorem equalAngle_meridional_sum_trig
    (alpha theta h : ℝ)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0) :
    equalAngleMeridionalMinus alpha theta h
        + equalAngleMeridionalPlus alpha theta h
      = equalAngleMeridionalTotal alpha (Real.sin theta) (Real.sin h) := by
  unfold equalAngleMeridionalMinus equalAngleMeridionalPlus
    equalAngleMeridionalTotal
  simp only [Real.sin_sub, Real.sin_add, Real.sin_two_mul]
  field_simp [hs, hc]
  ring

/-- Direct trigonometric proof of the unnormalised axial-coordinate balance. -/
theorem equalAngle_axial_balance_trig
    (alpha theta h : ℝ)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0) :
    equalAngleMeridionalMinus alpha theta h
          * (Real.cos (theta - 2 * h) - Real.cos theta)
      + equalAngleMeridionalPlus alpha theta h
          * (Real.cos (theta + 2 * h) - Real.cos theta)
      = -2 * equalAngleTrigWeight alpha theta h * Real.cos theta := by
  unfold equalAngleMeridionalMinus equalAngleMeridionalPlus
    equalAngleTrigWeight equalAngleWeight
  simp only [Real.sin_sub, Real.sin_add, Real.sin_two_mul,
    Real.cos_sub, Real.cos_add, Real.cos_two_mul]
  field_simp [hs, hc]
  have hh := Real.sin_sq_add_cos_sq h
  ring_nf at hh ⊢
  linear_combination
    (4 * Real.cos h * alpha * Real.sin theta * Real.cos theta) * hh

/-- Direct trigonometric proof of the meridional part of either transverse
coordinate balance. -/
theorem equalAngle_transverse_meridional_balance_trig
    (alpha theta h : ℝ)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0) :
    equalAngleMeridionalMinus alpha theta h
          * (Real.sin (theta - 2 * h) - Real.sin theta)
      + equalAngleMeridionalPlus alpha theta h
          * (Real.sin (theta + 2 * h) - Real.sin theta)
      = 2 * alpha * Real.sin h * Real.cos (2 * theta) := by
  unfold equalAngleMeridionalMinus equalAngleMeridionalPlus
  simp only [Real.sin_sub, Real.sin_add, Real.sin_two_mul,
    Real.cos_two_mul]
  field_simp [hs, hc]
  have hh := Real.sin_sq_add_cos_sq h
  have ht := Real.sin_sq_add_cos_sq theta
  ring_nf at hh ht ⊢
  linear_combination
    (4 * alpha * Real.cos h * Real.sin theta ^ 2) * hh
      - (4 * alpha * Real.cos h * Real.sin h ^ 2) * ht

/-- The azimuthal second difference of the cosine transverse coordinate has
an exact closed form after multiplication by the shared conductance. -/
theorem equalAngle_azimuth_cos_balance_trig
    (alpha theta h beta phi : ℝ)
    (hst : Real.sin theta ≠ 0)
    (hv : 1 - Real.cos beta ≠ 0) :
    equalAngleTrigAzimuthConductance alpha theta h beta
          * (Real.sin theta * Real.cos (phi - beta)
            - Real.sin theta * Real.cos phi)
      + equalAngleTrigAzimuthConductance alpha theta h beta
          * (Real.sin theta * Real.cos (phi + beta)
            - Real.sin theta * Real.cos phi)
      = -2 * alpha * Real.sin h * Real.cos phi := by
  unfold equalAngleTrigAzimuthConductance equalAngleAzimuthConductance
  simp only [Real.cos_sub, Real.cos_add]
  field_simp [hst, hv]
  ring

/-- The same azimuthal identity for the sine transverse coordinate. -/
theorem equalAngle_azimuth_sin_balance_trig
    (alpha theta h beta phi : ℝ)
    (hst : Real.sin theta ≠ 0)
    (hv : 1 - Real.cos beta ≠ 0) :
    equalAngleTrigAzimuthConductance alpha theta h beta
          * (Real.sin theta * Real.sin (phi - beta)
            - Real.sin theta * Real.sin phi)
      + equalAngleTrigAzimuthConductance alpha theta h beta
          * (Real.sin theta * Real.sin (phi + beta)
            - Real.sin theta * Real.sin phi)
      = -2 * alpha * Real.sin h * Real.sin phi := by
  unfold equalAngleTrigAzimuthConductance equalAngleAzimuthConductance
  simp only [Real.sin_sub, Real.sin_add]
  field_simp [hst, hv]
  ring

/-- The actual trigonometric stencil preserves the axial coordinate with
Laplace--Beltrami eigenvalue `-2`. -/
theorem equalAngle_productNodeAction_cos_eq
    (alpha theta h beta : ℝ)
    (hq : equalAngleTrigWeight alpha theta h ≠ 0)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0) :
    productNodeAction
        (equalAngleTrigWeight alpha theta h)
        (equalAngleMeridionalMinus alpha theta h)
        (equalAngleMeridionalPlus alpha theta h)
        (equalAngleTrigAzimuthConductance alpha theta h beta)
        (Real.cos theta)
        (Real.cos (theta - 2 * h))
        (Real.cos (theta + 2 * h))
        (Real.cos theta) (Real.cos theta)
      = -2 * Real.cos theta := by
  apply productNodeAction_eq_of_balance
    (q := equalAngleTrigWeight alpha theta h)
    (bm := equalAngleMeridionalMinus alpha theta h)
    (bp := equalAngleMeridionalPlus alpha theta h)
    (c := equalAngleTrigAzimuthConductance alpha theta h beta)
    (f0 := Real.cos theta)
    (fm := Real.cos (theta - 2 * h))
    (fp := Real.cos (theta + 2 * h))
    (fl := Real.cos theta) (fr := Real.cos theta)
    (lam := 2) hq
  simpa using equalAngle_axial_balance_trig alpha theta h hs hc

/-- The actual trigonometric stencil preserves the cosine transverse
coordinate with eigenvalue `-2`. -/
theorem equalAngle_productNodeAction_sin_cos_eq
    (alpha theta h beta phi : ℝ)
    (hq : equalAngleTrigWeight alpha theta h ≠ 0)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0)
    (hst : Real.sin theta ≠ 0)
    (hv : 1 - Real.cos beta ≠ 0) :
    productNodeAction
        (equalAngleTrigWeight alpha theta h)
        (equalAngleMeridionalMinus alpha theta h)
        (equalAngleMeridionalPlus alpha theta h)
        (equalAngleTrigAzimuthConductance alpha theta h beta)
        (Real.sin theta * Real.cos phi)
        (Real.sin (theta - 2 * h) * Real.cos phi)
        (Real.sin (theta + 2 * h) * Real.cos phi)
        (Real.sin theta * Real.cos (phi - beta))
        (Real.sin theta * Real.cos (phi + beta))
      = -2 * (Real.sin theta * Real.cos phi) := by
  apply productNodeAction_eq_of_balance
    (q := equalAngleTrigWeight alpha theta h)
    (bm := equalAngleMeridionalMinus alpha theta h)
    (bp := equalAngleMeridionalPlus alpha theta h)
    (c := equalAngleTrigAzimuthConductance alpha theta h beta)
    (f0 := Real.sin theta * Real.cos phi)
    (fm := Real.sin (theta - 2 * h) * Real.cos phi)
    (fp := Real.sin (theta + 2 * h) * Real.cos phi)
    (fl := Real.sin theta * Real.cos (phi - beta))
    (fr := Real.sin theta * Real.cos (phi + beta))
    (lam := 2) hq
  have hmer :
      equalAngleMeridionalMinus alpha theta h
            * (Real.sin (theta - 2 * h) * Real.cos phi
              - Real.sin theta * Real.cos phi)
        + equalAngleMeridionalPlus alpha theta h
            * (Real.sin (theta + 2 * h) * Real.cos phi
              - Real.sin theta * Real.cos phi)
        = 2 * alpha * Real.sin h * Real.cos (2 * theta) * Real.cos phi := by
    calc
      _ = (equalAngleMeridionalMinus alpha theta h
              * (Real.sin (theta - 2 * h) - Real.sin theta)
            + equalAngleMeridionalPlus alpha theta h
              * (Real.sin (theta + 2 * h) - Real.sin theta))
            * Real.cos phi := by ring
      _ = _ := by
        rw [equalAngle_transverse_meridional_balance_trig alpha theta h hs hc]
  have hazi := equalAngle_azimuth_cos_balance_trig
    alpha theta h beta phi hst hv
  calc
    _ = (equalAngleMeridionalMinus alpha theta h
            * (Real.sin (theta - 2 * h) * Real.cos phi
              - Real.sin theta * Real.cos phi)
          + equalAngleMeridionalPlus alpha theta h
            * (Real.sin (theta + 2 * h) * Real.cos phi
              - Real.sin theta * Real.cos phi))
        + (equalAngleTrigAzimuthConductance alpha theta h beta
            * (Real.sin theta * Real.cos (phi - beta)
              - Real.sin theta * Real.cos phi)
          + equalAngleTrigAzimuthConductance alpha theta h beta
            * (Real.sin theta * Real.cos (phi + beta)
              - Real.sin theta * Real.cos phi)) := by ring
    _ = 2 * alpha * Real.sin h * Real.cos (2 * theta) * Real.cos phi
          + (-2 * alpha * Real.sin h * Real.cos phi) := by rw [hmer, hazi]
    _ = -2 * equalAngleTrigWeight alpha theta h
          * (Real.sin theta * Real.cos phi) := by
      unfold equalAngleTrigWeight equalAngleWeight
      rw [Real.cos_two_mul]
      have ht := Real.sin_sq_add_cos_sq theta
      ring_nf at ht ⊢
      linear_combination
        (4 * alpha * Real.cos phi * Real.sin h) * ht

/-- The actual trigonometric stencil preserves the sine transverse coordinate
with eigenvalue `-2`. -/
theorem equalAngle_productNodeAction_sin_sin_eq
    (alpha theta h beta phi : ℝ)
    (hq : equalAngleTrigWeight alpha theta h ≠ 0)
    (hs : Real.sin h ≠ 0) (hc : Real.cos h ≠ 0)
    (hst : Real.sin theta ≠ 0)
    (hv : 1 - Real.cos beta ≠ 0) :
    productNodeAction
        (equalAngleTrigWeight alpha theta h)
        (equalAngleMeridionalMinus alpha theta h)
        (equalAngleMeridionalPlus alpha theta h)
        (equalAngleTrigAzimuthConductance alpha theta h beta)
        (Real.sin theta * Real.sin phi)
        (Real.sin (theta - 2 * h) * Real.sin phi)
        (Real.sin (theta + 2 * h) * Real.sin phi)
        (Real.sin theta * Real.sin (phi - beta))
        (Real.sin theta * Real.sin (phi + beta))
      = -2 * (Real.sin theta * Real.sin phi) := by
  apply productNodeAction_eq_of_balance
    (q := equalAngleTrigWeight alpha theta h)
    (bm := equalAngleMeridionalMinus alpha theta h)
    (bp := equalAngleMeridionalPlus alpha theta h)
    (c := equalAngleTrigAzimuthConductance alpha theta h beta)
    (f0 := Real.sin theta * Real.sin phi)
    (fm := Real.sin (theta - 2 * h) * Real.sin phi)
    (fp := Real.sin (theta + 2 * h) * Real.sin phi)
    (fl := Real.sin theta * Real.sin (phi - beta))
    (fr := Real.sin theta * Real.sin (phi + beta))
    (lam := 2) hq
  have hmer :
      equalAngleMeridionalMinus alpha theta h
            * (Real.sin (theta - 2 * h) * Real.sin phi
              - Real.sin theta * Real.sin phi)
        + equalAngleMeridionalPlus alpha theta h
            * (Real.sin (theta + 2 * h) * Real.sin phi
              - Real.sin theta * Real.sin phi)
        = 2 * alpha * Real.sin h * Real.cos (2 * theta) * Real.sin phi := by
    calc
      _ = (equalAngleMeridionalMinus alpha theta h
              * (Real.sin (theta - 2 * h) - Real.sin theta)
            + equalAngleMeridionalPlus alpha theta h
              * (Real.sin (theta + 2 * h) - Real.sin theta))
            * Real.sin phi := by ring
      _ = _ := by
        rw [equalAngle_transverse_meridional_balance_trig alpha theta h hs hc]
  have hazi := equalAngle_azimuth_sin_balance_trig
    alpha theta h beta phi hst hv
  calc
    _ = (equalAngleMeridionalMinus alpha theta h
            * (Real.sin (theta - 2 * h) * Real.sin phi
              - Real.sin theta * Real.sin phi)
          + equalAngleMeridionalPlus alpha theta h
            * (Real.sin (theta + 2 * h) * Real.sin phi
              - Real.sin theta * Real.sin phi))
        + (equalAngleTrigAzimuthConductance alpha theta h beta
            * (Real.sin theta * Real.sin (phi - beta)
              - Real.sin theta * Real.sin phi)
          + equalAngleTrigAzimuthConductance alpha theta h beta
            * (Real.sin theta * Real.sin (phi + beta)
              - Real.sin theta * Real.sin phi)) := by ring
    _ = 2 * alpha * Real.sin h * Real.cos (2 * theta) * Real.sin phi
          + (-2 * alpha * Real.sin h * Real.sin phi) := by rw [hmer, hazi]
    _ = -2 * equalAngleTrigWeight alpha theta h
          * (Real.sin theta * Real.sin phi) := by
      unfold equalAngleTrigWeight equalAngleWeight
      rw [Real.cos_two_mul]
      have ht := Real.sin_sq_add_cos_sq theta
      ring_nf at ht ⊢
      linear_combination
        (4 * alpha * Real.sin phi * Real.sin h) * ht

end

end AFPBarrier
