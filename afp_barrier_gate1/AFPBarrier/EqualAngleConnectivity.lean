import AFPBarrier.EqualAngleEdges
import Mathlib.Tactic

/-!
# Shared-edge compatibility of the equal-angle grid

A reversible graph operator requires the two endpoints of an undirected edge
to assign the same conductance. The explicit construction has this property
identically: the upper conductance of ring `i` is the lower conductance of ring
`i+1`. This file proves that statement directly from the grid formulas.
-/

namespace AFPBarrier

noncomputable section

/-- Successive cell-centred latitude rings differ by one full polar step. -/
theorem equalAngleGridTheta_add_one
    (n i : ℝ) :
    equalAngleGridTheta n (i + 1)
      = equalAngleGridTheta n i + 2 * equalAngleGridHalfStep n := by
  unfold equalAngleGridTheta
  ring

/-- The shared meridional edge receives exactly the same conductance from its
two endpoint rings. -/
theorem equalAngleGrid_meridional_shared
    (n i alpha : ℝ) :
    equalAngleMeridionalPlus alpha
        (equalAngleGridTheta n i) (equalAngleGridHalfStep n)
      = equalAngleMeridionalMinus alpha
        (equalAngleGridTheta n (i + 1)) (equalAngleGridHalfStep n) := by
  unfold equalAngleMeridionalPlus equalAngleMeridionalMinus
  rw [equalAngleGridTheta_add_one]
  congr 2
  ring_nf

/-- Reflection of a ring index across the equator reflects its latitude across
`π/2`. -/
theorem equalAngleGridTheta_reflect
    (n i : ℝ) (hn : n ≠ 0) :
    equalAngleGridTheta n (n - 1 - i)
      = Real.pi - equalAngleGridTheta n i := by
  unfold equalAngleGridTheta equalAngleGridHalfStep
  field_simp [hn]
  ring

/-- Reflected rings have identical sine latitude and therefore identical cell
weights. -/
theorem equalAngleGrid_weight_reflect
    (n m i : ℝ) (hn : n ≠ 0) :
    equalAngleTrigWeight
        (equalAngleGridAzimuthStep m)
        (equalAngleGridTheta n (n - 1 - i))
        (equalAngleGridHalfStep n)
      = equalAngleTrigWeight
        (equalAngleGridAzimuthStep m)
        (equalAngleGridTheta n i)
        (equalAngleGridHalfStep n) := by
  rw [equalAngleGridTheta_reflect n i hn]
  unfold equalAngleTrigWeight equalAngleWeight
  rw [Real.sin_pi_sub]

/-- Reflected axial coordinates have opposite signs. -/
theorem equalAngleGrid_cos_reflect
    (n i : ℝ) (hn : n ≠ 0) :
    Real.cos (equalAngleGridTheta n (n - 1 - i))
      = -Real.cos (equalAngleGridTheta n i) := by
  rw [equalAngleGridTheta_reflect n i hn, Real.cos_pi_sub]

end

end AFPBarrier
