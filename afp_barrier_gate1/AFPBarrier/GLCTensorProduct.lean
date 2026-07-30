import AFPBarrier.Quantitative

/-!
# Algebraic structure of the Gauss--Legendre--Chebyshev AFP stencil

This module isolates the exact finite-dimensional identities used by the
three-dimensional product-quadrature AFP stencil.  It does not formalize the
analytic construction of Gauss--Legendre nodes.  Instead it proves that:

* the Morel interface-flux recurrence gives the exact `-2` coordinate balance;
* the azimuthal correction `K` gives exact transverse coordinate balance;
* `K` equals two minus the latitude chord loss;
* the peak second-harmonic defect decomposes into latitude and azimuth parts;
* the row-rate formula used in the stiffness analysis is exact.

These statements are the algebraic bridge between Radiant's implementation and
the asymptotic analysis in Gate 3.
-/

namespace AFPBarrier

/-- Two-neighbour latitude action at one polar ring. -/
def latitudePairAction
    (aMinus aPlus fMinus f fPlus : ℝ) : ℝ :=
  aMinus * (fMinus - f) + aPlus * (fPlus - f)

/-- Morel's transverse correction parameter. -/
def glcK (r c : ℝ) : ℝ :=
  2 * r ^ 2 + r * c

/-- One of the two equal azimuthal jump rates.

Here `d = 1 - cos(h)` and `r` is the radius of the polar ring.
-/
noncomputable def glcAzimuthRate (r c d : ℝ) : ℝ :=
  glcK r c / (2 * r ^ 2 * d)

/-- Peak defect of a four-neighbour tensor-product row. -/
def glcPeakDefect
    (aMinus aPlus q dMinus dPlus dPhi : ℝ) : ℝ :=
  aMinus * dMinus ^ 2 + aPlus * dPlus ^ 2 + 2 * q * dPhi ^ 2

/-- Multiplying the lower latitude rate by its signed coordinate increment
removes the coordinate gap. -/
theorem latitude_minus_flux_cancellation
    (betaMinus w xMinus x : ℝ)
    (hw : w ≠ 0) (hgap : x - xMinus ≠ 0) :
    (betaMinus / (w * (x - xMinus))) * (xMinus - x)
      = -betaMinus / w := by
  field_simp [hw, hgap]
  ring

/-- Multiplying the upper latitude rate by its coordinate increment removes
that coordinate gap. -/
theorem latitude_plus_flux_cancellation
    (betaPlus w x xPlus : ℝ)
    (hw : w ≠ 0) (hgap : xPlus - x ≠ 0) :
    (betaPlus / (w * (xPlus - x))) * (xPlus - x)
      = betaPlus / w := by
  field_simp [hw, hgap]

/-- The Morel interface recurrence implies exact degree-one balance in the
Gauss--Legendre coordinate. -/
theorem latitude_coordinate_exact_of_flux_recurrence
    (betaMinus betaPlus w xMinus x xPlus : ℝ)
    (hw : w ≠ 0)
    (hgapMinus : x - xMinus ≠ 0)
    (hgapPlus : xPlus - x ≠ 0)
    (hrecurrence : betaPlus - betaMinus = -2 * w * x) :
    latitudePairAction
        (betaMinus / (w * (x - xMinus)))
        (betaPlus / (w * (xPlus - x)))
        xMinus x xPlus
      = -2 * x := by
  unfold latitudePairAction
  rw [latitude_minus_flux_cancellation betaMinus w xMinus x hw hgapMinus]
  rw [latitude_plus_flux_cancellation betaPlus w x xPlus hw hgapPlus]
  field_simp [hw]
  nlinarith

/-- Two equal azimuthal rates reduce to one centered second difference. -/
theorem azimuth_pair_action_factor
    (q r uMinus u uPlus : ℝ) :
    q * (r * uMinus - r * u) + q * (r * uPlus - r * u)
      = q * r * (uMinus + uPlus - 2 * u) := by
  ring

/-- The Morel `K` correction makes each transverse Cartesian coordinate an
exact eigenmode with eigenvalue `-2`, provided the equispaced azimuthal second
difference has its exact first-Fourier-mode value. -/
theorem glc_transverse_coordinate_exact
    (r c d uMinus u uPlus : ℝ)
    (hr : r ≠ 0) (hd : d ≠ 0)
    (hfourier : uMinus + uPlus - 2 * u = -2 * d * u) :
    c * u
        + glcAzimuthRate r c d * (r * uMinus - r * u)
        + glcAzimuthRate r c d * (r * uPlus - r * u)
      = -2 * r * u := by
  rw [azimuth_pair_action_factor]
  rw [hfourier]
  unfold glcAzimuthRate glcK
  field_simp [hr, hd]
  ring

/-- Geometric identity for the transverse correction.

If `(r,x)` and its two latitude neighbours lie on the unit circle and the
latitude row is exact on `x`, then `K` is two minus the weighted latitude chord
loss.  This immediately gives `K ≤ 2` for nonnegative rates.
-/
theorem glcK_eq_two_sub_latitude_chordLoss
    (aMinus aPlus rMinus r rPlus xMinus x xPlus : ℝ)
    (hunit : r ^ 2 + x ^ 2 = 1)
    (hcoord : latitudePairAction aMinus aPlus xMinus x xPlus = -2 * x) :
    glcK r (latitudePairAction aMinus aPlus rMinus r rPlus)
      = 2 -
        (aMinus * (1 - (r * rMinus + x * xMinus))
          + aPlus * (1 - (r * rPlus + x * xPlus))) := by
  unfold glcK latitudePairAction
  nlinarith

/-- Nonnegative latitude rates and nonnegative chord deficits imply `K ≤ 2`. -/
theorem glcK_le_two
    (aMinus aPlus rMinus r rPlus xMinus x xPlus : ℝ)
    (haMinus : 0 ≤ aMinus) (haPlus : 0 ≤ aPlus)
    (hdefMinus : 0 ≤ 1 - (r * rMinus + x * xMinus))
    (hdefPlus : 0 ≤ 1 - (r * rPlus + x * xPlus))
    (hunit : r ^ 2 + x ^ 2 = 1)
    (hcoord : latitudePairAction aMinus aPlus xMinus x xPlus = -2 * x) :
    glcK r (latitudePairAction aMinus aPlus rMinus r rPlus) ≤ 2 := by
  rw [glcK_eq_two_sub_latitude_chordLoss
    aMinus aPlus rMinus r rPlus xMinus x xPlus hunit hcoord]
  have hloss :
      0 ≤ aMinus * (1 - (r * rMinus + x * xMinus))
        + aPlus * (1 - (r * rPlus + x * xPlus)) :=
    add_nonneg (mul_nonneg haMinus hdefMinus) (mul_nonneg haPlus hdefPlus)
  linarith

/-- Exact decomposition of the peak degree-two defect. -/
theorem glcPeakDefect_decomposition
    (aMinus aPlus r c d dMinus dPlus : ℝ)
    (hr : r ≠ 0) (hd : d ≠ 0) :
    glcPeakDefect aMinus aPlus (glcAzimuthRate r c d)
        dMinus dPlus (r ^ 2 * d)
      = aMinus * dMinus ^ 2 + aPlus * dPlus ^ 2
        + glcK r c * r ^ 2 * d := by
  unfold glcPeakDefect glcAzimuthRate
  field_simp [hr, hd]
  ring

/-- Exact total outgoing row rate of the four-neighbour tensor-product row. -/
theorem glc_rowRate_formula
    (aMinus aPlus r c d : ℝ)
    (hr : r ≠ 0) (hd : d ≠ 0) :
    aMinus + aPlus + 2 * glcAzimuthRate r c d
      = aMinus + aPlus + glcK r c / (r ^ 2 * d) := by
  unfold glcAzimuthRate
  field_simp [hr, hd]
  ring

/-- At the first polar ring, the interface recurrence cancels the first
Gauss--Legendre weight.  This is the algebraic starting point for the Bessel
zero asymptotic of the polar stiffness. -/
theorem outer_latitude_action_formula
    (w x xPlus r rPlus : ℝ)
    (hw : w ≠ 0) (hgap : xPlus - x ≠ 0) :
    ((-2 * w * x) / (w * (xPlus - x))) * (rPlus - r)
      = (-2 * x) * (rPlus - r) / (xPlus - x) := by
  field_simp [hw, hgap]
  ring

/-- Corresponding exact outer-ring formula for `K`. -/
theorem outer_glcK_formula
    (w x xPlus r rPlus : ℝ)
    (hw : w ≠ 0) (hgap : xPlus - x ≠ 0) :
    glcK r (((-2 * w * x) / (w * (xPlus - x))) * (rPlus - r))
      = 2 * r ^ 2 - 2 * x * r * (rPlus - r) / (xPlus - x) := by
  rw [outer_latitude_action_formula w x xPlus r rPlus hw hgap]
  unfold glcK
  ring

/-- The outer-ring correction is strictly positive whenever the first
latitude ring moves inward toward a nondecreasing transverse radius.  This
covers the southern and northern extreme Gauss--Legendre rings after the
obvious reflection. -/
theorem outer_glcK_pos
    (w x xPlus r rPlus : ℝ)
    (hw : w ≠ 0)
    (hxgap : x < xPlus)
    (hr : 0 < r)
    (hx : x ≤ 0)
    (hradius : r ≤ rPlus) :
    0 < glcK r (((-2 * w * x) / (w * (xPlus - x))) * (rPlus - r)) := by
  have hgap : xPlus - x ≠ 0 := ne_of_gt (sub_pos.mpr hxgap)
  rw [outer_glcK_formula w x xPlus r rPlus hw hgap]
  have hfirst : 0 < 2 * r ^ 2 := by positivity
  have hminusx : 0 ≤ -x := neg_nonneg.mpr hx
  have hradius' : 0 ≤ rPlus - r := sub_nonneg.mpr hradius
  have hnum : 0 ≤ -2 * x * r * (rPlus - r) := by
    calc
      -2 * x * r * (rPlus - r) = 2 * (-x) * r * (rPlus - r) := by ring
      _ ≥ 0 := mul_nonneg
        (mul_nonneg (mul_nonneg (by norm_num) hminusx) (le_of_lt hr))
        hradius'
  have hden : 0 ≤ xPlus - x := le_of_lt (sub_pos.mpr hxgap)
  have hsecond : 0 ≤ (-2 * x * r * (rPlus - r)) / (xPlus - x) :=
    div_nonneg hnum hden
  have hre :
      2 * r ^ 2 - 2 * x * r * (rPlus - r) / (xPlus - x)
        = 2 * r ^ 2 + (-2 * x * r * (rPlus - r)) / (xPlus - x) := by
    ring
  rw [hre]
  exact add_pos_of_pos_of_nonneg hfirst hsecond

/-- Exact rational value of `K` for the two-ring GLC case, expressed without
introducing square roots into the theorem statement. -/
theorem glcK_N2_of_radius_sq
    (r : ℝ) (hr2 : r ^ 2 = (2 : ℝ) / 3) :
    glcK r 0 = (4 : ℝ) / 3 := by
  unfold glcK
  rw [hr2]
  norm_num

end AFPBarrier
