import AFPBarrier.EqualAngleGrid
import Mathlib.Tactic

/-!
# Edge positivity and polar boundary closure for the equal-angle grid

The local geometry file proves positivity when its angular hypotheses are
supplied. This file discharges those hypotheses from the actual all-order grid
indices. It therefore proves that every edge which is present has a strictly
positive shared conductance, while the two omitted polar meridional edges have
exactly zero conductance.
-/

namespace AFPBarrier

noncomputable section

/-- The north-polar missing meridional edge has exactly zero conductance. -/
@[simp] theorem equalAngleGrid_meridionalMinus_zero_north
    (n alpha : ℝ) :
    equalAngleMeridionalMinus alpha
        (equalAngleGridTheta n 0) (equalAngleGridHalfStep n) = 0 := by
  unfold equalAngleGridTheta equalAngleGridHalfStep
    equalAngleMeridionalMinus
  ring_nf
  simp

/-- The south-polar missing meridional edge has exactly zero conductance. -/
@[simp] theorem equalAngleGrid_meridionalPlus_zero_south
    (n alpha : ℝ) (hn : n ≠ 0) :
    equalAngleMeridionalPlus alpha
        (equalAngleGridTheta n (n - 1))
        (equalAngleGridHalfStep n) = 0 := by
  have hangle :
      equalAngleGridTheta n (n - 1) + equalAngleGridHalfStep n
        = Real.pi := by
    unfold equalAngleGridTheta equalAngleGridHalfStep
    field_simp [hn]
    ring
  unfold equalAngleMeridionalPlus
  rw [hangle, Real.sin_pi]
  simp

/-- Every actual lower meridional edge has strictly positive conductance. -/
theorem equalAngleGrid_meridionalMinus_pos
    (n m i : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 < i) (hiN : i ≤ n - 1) :
    0 < equalAngleMeridionalMinus
      (equalAngleGridAzimuthStep m)
      (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) := by
  have hn0 : 0 < n := by linarith
  have hm0 : 0 < m := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hhhalf := equalAngleGridHalfStep_lt_pi_div_two n hn
  have halpha := equalAngleGridAzimuthStep_pos m hm0
  have hlower0 :
      0 < equalAngleGridTheta n i - equalAngleGridHalfStep n := by
    unfold equalAngleGridTheta
    nlinarith
  have hlowerpi :
      equalAngleGridTheta n i - equalAngleGridHalfStep n < Real.pi := by
    unfold equalAngleGridTheta equalAngleGridHalfStep
    have hden : 0 < 2 * n := by positivity
    rw [← sub_div]
    apply (div_lt_iff₀ hden).2
    nlinarith [Real.pi_pos]
  apply equalAngleMeridionalMinus_pos
  · exact halpha
  · exact hlower0
  · exact hlowerpi
  · linarith
  · linarith

/-- Every actual upper meridional edge has strictly positive conductance. -/
theorem equalAngleGrid_meridionalPlus_pos
    (n m i : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 ≤ i) (hiN : i < n - 1) :
    0 < equalAngleMeridionalPlus
      (equalAngleGridAzimuthStep m)
      (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n) := by
  have hn0 : 0 < n := by linarith
  have hm0 : 0 < m := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hhhalf := equalAngleGridHalfStep_lt_pi_div_two n hn
  have halpha := equalAngleGridAzimuthStep_pos m hm0
  have hupper0 :
      0 < equalAngleGridTheta n i + equalAngleGridHalfStep n := by
    unfold equalAngleGridTheta
    nlinarith
  have hupperpi :
      equalAngleGridTheta n i + equalAngleGridHalfStep n < Real.pi := by
    unfold equalAngleGridTheta equalAngleGridHalfStep
    have hden : 0 < 2 * n := by positivity
    rw [← add_div]
    apply (div_lt_iff₀ hden).2
    nlinarith [Real.pi_pos]
  apply equalAngleMeridionalPlus_pos
  · exact halpha
  · exact hupper0
  · exact hupperpi
  · linarith
  · linarith

/-- Every azimuthal edge at every admissible ring has strictly positive
conductance. -/
theorem equalAngleGrid_azimuthConductance_pos
    (n m i : ℝ)
    (hn : 2 ≤ n) (hm : 3 ≤ m)
    (hi0 : 0 ≤ i) (hiN : i ≤ n - 1) :
    0 < equalAngleTrigAzimuthConductance
      (equalAngleGridAzimuthStep m)
      (equalAngleGridTheta n i)
      (equalAngleGridHalfStep n)
      (equalAngleGridAzimuthStep m) := by
  obtain ⟨hh0, hhhalf, ht0, htpi, hb0, hb2pi,
      hs, hc, hst, hv⟩ :=
    equalAngleGrid_parameter_facts n m i hn hm hi0 hiN
  apply equalAngleTrigAzimuthConductance_pos
  · exact hb0
  · exact ht0
  · exact htpi
  · exact hh0
  · linarith [hhhalf, Real.pi_pos]
  · exact one_sub_cos_pos_of_pos_of_lt_two_pi
      (equalAngleGridAzimuthStep m) hb0 hb2pi

end

end AFPBarrier
