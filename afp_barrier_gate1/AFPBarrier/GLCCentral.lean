import AFPBarrier.GLCTensorProduct

/-!
# Exact equatorial-ring formulas for odd-order GLC quadratures

For odd Gauss--Legendre order there is a central node `mu = 0`, hence a polar
ring of radius one. Symmetry gives equal latitude rates and equal chord
deficits on the two sides. The theorems below isolate the exact finite algebra
used in the central-ring asymptotic analysis.
-/

namespace AFPBarrier

/-- At a symmetric equatorial ring with radius one and equal latitude rates,
`K` has a one-parameter exact form. Here `dLat = 1 - rNeighbor` is the
latitude chord deficit. -/
theorem central_glcK_formula
    (a dLat : ℝ) :
    glcK 1 (-2 * a * dLat) = 2 - 2 * a * dLat := by
  unfold glcK
  ring

/-- Exact peak-defect formula at a symmetric equatorial ring. -/
theorem central_glcPeakDefect_formula
    (a dLat dPhi : ℝ)
    (hdPhi : dPhi ≠ 0) :
    glcPeakDefect a a (glcAzimuthRate 1 (-2 * a * dLat) dPhi)
        dLat dLat dPhi
      = 2 * a * dLat ^ 2 + (2 - 2 * a * dLat) * dPhi := by
  unfold glcPeakDefect glcAzimuthRate glcK
  field_simp [hdPhi]
  ring

/-- Exact outgoing-rate formula at the same symmetric equatorial ring. -/
theorem central_glcRowRate_formula
    (a dLat dPhi : ℝ)
    (hdPhi : dPhi ≠ 0) :
    2 * a + 2 * glcAzimuthRate 1 (-2 * a * dLat) dPhi
      = 2 * a + (2 - 2 * a * dLat) / dPhi := by
  unfold glcAzimuthRate glcK
  field_simp [hdPhi]
  ring

/-- The central defect is bounded below by its azimuthal contribution whenever
both the latitude rate and latitude deficit are nonnegative. -/
theorem central_glcPeakDefect_lower_bound
    (a dLat dPhi : ℝ)
    (ha : 0 ≤ a) (hdLat : 0 ≤ dLat)
    (hK : 0 ≤ 2 - 2 * a * dLat) :
    (2 - 2 * a * dLat) * dPhi
      ≤ 2 * a * dLat ^ 2 + (2 - 2 * a * dLat) * dPhi := by
  have hlat : 0 ≤ 2 * a * dLat ^ 2 := by
    positivity
  linarith

end AFPBarrier
