import AFPBarrier.EqualAngleGeometry
import Mathlib.Tactic

/-!
# Spherical neighbour dot products for the equal-angle grid

The degree-two defect is expressed in terms of `1 - Ωᵢ·Ωⱼ`. This file proves
the two geometric loss formulas directly from the spherical-coordinate node
map, closing the gap between the explicit grid and the algebraic defect theorem.
-/

namespace AFPBarrier

noncomputable section

/-- Euclidean dot product of two unit-sphere points written in polar/azimuthal
coordinates. -/
def sphericalCoordinateDot
    (theta phi theta' phi' : ℝ) : ℝ :=
  Real.cos theta * Real.cos theta'
    + Real.sin theta * Real.sin theta'
      * (Real.cos phi * Real.cos phi' + Real.sin phi * Real.sin phi')

/-- Two meridional neighbours at common azimuth and separation `2h` have dot
product `cos(2h)`. -/
theorem sphericalCoordinateDot_meridional
    (theta phi h : ℝ) :
    sphericalCoordinateDot theta phi (theta + 2 * h) phi
      = Real.cos (2 * h) := by
  unfold sphericalCoordinateDot
  have hp : Real.cos phi * Real.cos phi + Real.sin phi * Real.sin phi = 1 := by
    nlinarith [Real.sin_sq_add_cos_sq phi]
  rw [hp, mul_one, ← Real.cos_sub]
  rw [show theta - (theta + 2 * h) = -(2 * h) by ring,
    Real.cos_neg]

/-- Two azimuthal neighbours on the same ring have dot product
`cos²(theta) + sin²(theta) cos(beta)`. -/
theorem sphericalCoordinateDot_azimuthal
    (theta phi beta : ℝ) :
    sphericalCoordinateDot theta phi theta (phi + beta)
      = Real.cos theta ^ 2 + Real.sin theta ^ 2 * Real.cos beta := by
  unfold sphericalCoordinateDot
  have hphi :
      Real.cos phi * Real.cos (phi + beta)
          + Real.sin phi * Real.sin (phi + beta)
        = Real.cos beta := by
    rw [← Real.cos_sub]
    rw [show phi - (phi + beta) = -beta by ring, Real.cos_neg]
  rw [hphi]
  ring

/-- The meridional dot-product loss is exactly `2 sin²(h)`. -/
theorem meridionalDotLoss_eq_two_sin_sq
    (theta phi h : ℝ) :
    1 - sphericalCoordinateDot theta phi (theta + 2 * h) phi
      = 2 * Real.sin h ^ 2 := by
  rw [sphericalCoordinateDot_meridional]
  rw [Real.cos_two_mul]
  have hh := Real.sin_sq_add_cos_sq h
  ring_nf at hh ⊢
  nlinarith

/-- The azimuthal dot-product loss is exactly
`sin²(theta) (1 - cos(beta))`. -/
theorem azimuthalDotLoss_eq_sin_sq_mul
    (theta phi beta : ℝ) :
    1 - sphericalCoordinateDot theta phi theta (phi + beta)
      = Real.sin theta ^ 2 * (1 - Real.cos beta) := by
  rw [sphericalCoordinateDot_azimuthal]
  have ht := Real.sin_sq_add_cos_sq theta
  ring_nf at ht ⊢
  nlinarith

/-- End-to-end peak-defect formula using the actual spherical-coordinate node
dot products, rather than abstract loss parameters. -/
theorem equalAngle_actual_peakDefect_formula
    (alpha theta phi h beta bm bp : ℝ)
    (halpha : alpha ≠ 0) (hst : Real.sin theta ≠ 0)
    (hsh : Real.sin h ≠ 0) (hv : 1 - Real.cos beta ≠ 0)
    (hsum : bm + bp
      = equalAngleMeridionalTotal alpha (Real.sin theta) (Real.sin h)) :
    productLocalPeakDefect
        (equalAngleTrigWeight alpha theta h)
        bm bp (equalAngleTrigAzimuthConductance alpha theta h beta)
        (1 - sphericalCoordinateDot theta phi (theta + 2 * h) phi)
        (1 - sphericalCoordinateDot theta phi theta (phi + beta))
      = 2 * Real.sin h ^ 2
          + Real.sin theta ^ 2 * (1 - Real.cos beta) := by
  rw [meridionalDotLoss_eq_two_sin_sq,
    azimuthalDotLoss_eq_sin_sq_mul]
  unfold equalAngleTrigWeight equalAngleTrigAzimuthConductance
  exact equalAngle_peakDefect_formula
    alpha (Real.sin theta) (Real.sin h) (1 - Real.cos beta)
    bm bp halpha hst hsh hv hsum

end

end AFPBarrier
