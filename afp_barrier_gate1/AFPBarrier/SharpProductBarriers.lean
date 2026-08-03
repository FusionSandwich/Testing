import AFPBarrier.EqualAngleRateMaximum
import AFPBarrier.SphericalNetScaling
import Mathlib.Tactic

/-!
# Sharp product-graph barriers and finite extremal algebra

This module formalizes the finite algebra used by Prompt 4:

* the exact polar quality formula;
* uniqueness of the square product-grid polar rates from the three coordinate
  balance equations;
* exact coefficient extraction for the polar asymptotic expansion;
* the universal rate--defect implication and the finite rate-capped extremal
  lower bound;
* a sharp two-loss anisotropy example; and
* the biregular incidence obstruction for one-to-one reduced-ring couplings.

The analytic Mittag--Leffler remainder estimate, finite-dimensional LP duality,
compactness, and spherical graph-class transfer are proved in the accompanying
ordinary mathematics document.  No analytic or geometric external theorem is
introduced as a Lean axiom.
-/

namespace AFPBarrier

noncomputable section

/-- Exact normalized polar quality for the square equal-angle product family. -/
def squarePolarQualityFromStep (h : ℝ) : ℝ :=
  squarePolarRateFromStep h
    * (2 * Real.sin h ^ 2 + 2 * Real.sin h ^ 4) / 4

/-- Closed form of the polar quality. -/
theorem squarePolarQualityFromStep_formula
    (h : ℝ) (hs : Real.sin h ≠ 0) :
    squarePolarQualityFromStep h
      = 1 / (4 * Real.sin h ^ 2)
        + 1 / 2 + Real.sin h ^ 2 / 4 := by
  unfold squarePolarQualityFromStep squarePolarRateFromStep
  field_simp [hs]
  ring

/-- The three polar coordinate balances force the meridional and two
azimuthal rates uniquely. The transverse hypothesis retains its nonzero
coordinate factor, so equality of the two azimuthal rates is derived rather
than assumed. The other displayed differences are the exact square-grid polar
coordinate differences after cancelling the stated nonzero factors. -/
theorem squarePolar_rates_forced
    (s transverseFactor aMer aLeft aRight : ℝ)
    (hs : s ≠ 0)
    (htransverseFactor : transverseFactor ≠ 0)
    (htransverse : transverseFactor * (aRight - aLeft) = 0)
    (hradial : aMer * (-4 * s ^ 2) = -2)
    (htangent :
      aLeft * (-2 * s ^ 2) + aRight * (-2 * s ^ 2)
          + aMer * (2 * (1 - 2 * s ^ 2)) = -2) :
    aMer = 1 / (2 * s ^ 2) ∧
      aLeft = 1 / (4 * s ^ 4) ∧
      aRight = 1 / (4 * s ^ 4) := by
  have heq : aRight = aLeft := by
    have hdiff : aRight - aLeft = 0 :=
      (mul_eq_zero.mp htransverse).resolve_left htransverseFactor
    linarith
  have hmer : aMer = 1 / (2 * s ^ 2) := by
    field_simp [hs] at hradial ⊢
    nlinarith
  have hleft : aLeft = 1 / (4 * s ^ 4) := by
    rw [heq, hmer] at htangent
    field_simp [hs] at htangent ⊢
    nlinarith
  exact ⟨hmer, hleft, heq.trans hleft⟩

/-- Consequently the total polar row rate is the exact expression used by the
product-grid construction; no ring-symmetry assumption is needed. -/
theorem squarePolar_totalRate_forced
    (s transverseFactor aMer aLeft aRight : ℝ)
    (hs : s ≠ 0)
    (htransverseFactor : transverseFactor ≠ 0)
    (htransverse : transverseFactor * (aRight - aLeft) = 0)
    (hradial : aMer * (-4 * s ^ 2) = -2)
    (htangent :
      aLeft * (-2 * s ^ 2) + aRight * (-2 * s ^ 2)
          + aMer * (2 * (1 - 2 * s ^ 2)) = -2) :
    aMer + aLeft + aRight
      = 1 / (2 * s ^ 2) + 1 / (2 * s ^ 4) := by
  obtain ⟨hmer, hleft, hright⟩ :=
    squarePolar_rates_forced
      s transverseFactor aMer aLeft aRight hs htransverseFactor htransverse
        hradial htangent
  rw [hmer, hleft, hright]
  ring

/-- The exact graph-class polar formula implies the quartic lower bound already
proved for the grid half-step. -/
theorem squarePolar_forced_quartic_lower
    (n r : ℝ) (hn : 2 ≤ n)
    (hr : r = squarePolarRateFromStep (equalAngleGridHalfStep n)) :
    8 * n ^ 4 / Real.pi ^ 4 ≤ r := by
  rw [hr]
  exact (squarePolarRate_grid_bounds n hn).1

/-- Truncation of `csc² x` sufficient to extract every coefficient through the
constant term of the polar-rate expansion. -/
def cscSquaredTruncation (x : ℝ) : ℝ :=
  1 / x ^ 2 + 1 / 3 + x ^ 2 / 15

/-- Main polar-rate expansion in the angular half-step variable. -/
def squarePolarRateMainStep (x : ℝ) : ℝ :=
  1 / (2 * x ^ 4) + 5 / (6 * x ^ 2) + 13 / 45

/-- Exact algebraic coefficient extraction before the analytic tail is added. -/
theorem cscSquaredTruncation_rate_identity
    (x : ℝ) (hx : x ≠ 0) :
    (1 / 2) * cscSquaredTruncation x
        + (1 / 2) * cscSquaredTruncation x ^ 2
      = squarePolarRateMainStep x + x ^ 2 / 18 + x ^ 4 / 450 := by
  unfold cscSquaredTruncation squarePolarRateMainStep
  field_simp [hx]
  ring

/-- Substitution `x=π/(2N)` gives the requested quartic, quadratic, and
constant coefficients exactly. -/
theorem squarePolarRateMainStep_grid
    (n : ℝ) (hn : n ≠ 0) :
    squarePolarRateMainStep (equalAngleGridHalfStep n)
      = (8 / Real.pi ^ 4) * n ^ 4
        + (10 / (3 * Real.pi ^ 2)) * n ^ 2
        + 13 / 45 := by
  unfold squarePolarRateMainStep equalAngleGridHalfStep
  field_simp [hn, Real.pi_ne_zero]
  ring

/-- Main polar-quality expansion in the angular half-step variable. -/
def squarePolarQualityMainStep (x : ℝ) : ℝ :=
  1 / (4 * x ^ 2) + 7 / 12

/-- Exact substitution for the polar-quality leading and constant terms. -/
theorem squarePolarQualityMainStep_grid
    (n : ℝ) (hn : n ≠ 0) :
    squarePolarQualityMainStep (equalAngleGridHalfStep n)
      = n ^ 2 / Real.pi ^ 2 + 7 / 12 := by
  unfold squarePolarQualityMainStep equalAngleGridHalfStep
  field_simp [hn, Real.pi_ne_zero]
  ring

/-- Self-contained universal rate barrier: `4 ≤ rate*defect` and an
`O(h²)` defect upper bound force an explicit inverse-quadratic rate. -/
theorem universal_rate_lower_of_defect_upper
    (rate defect C h : ℝ)
    (hproduct : 4 ≤ rate * defect)
    (hrate : 0 ≤ rate)
    (hdefect : defect ≤ C * h ^ 2)
    (hC : 0 < C) (hh : 0 < h) :
    4 / (C * h ^ 2) ≤ rate := by
  have hmul : rate * defect ≤ rate * (C * h ^ 2) :=
    mul_le_mul_of_nonneg_left hdefect hrate
  have hfour : 4 ≤ rate * (C * h ^ 2) := hproduct.trans hmul
  have hden : 0 < C * h ^ 2 := mul_pos hC (sq_pos_of_pos hh)
  apply (div_le_iff₀ hden).2
  simpa [mul_comm, mul_left_comm, mul_assoc] using hfour

/-- Finite-`K` lower bound for every nonempty rate-capped extremal class. -/
theorem finiteExtremal_defect_lower
    (rate defect R K : ℝ)
    (hproduct : 4 ≤ rate * defect)
    (hrateCap : rate ≤ R * K)
    (hdefect : 0 ≤ defect)
    (hR : 0 < R) (hK : 0 < K) :
    4 / (R * K) ≤ defect := by
  have hmul : rate * defect ≤ (R * K) * defect :=
    mul_le_mul_of_nonneg_right hrateCap hdefect
  have hfour : 4 ≤ (R * K) * defect := hproduct.trans hmul
  have hden : 0 < R * K := mul_pos hR hK
  apply (div_le_iff₀ hden).2
  simpa [mul_comm, mul_left_comm, mul_assoc] using hfour

/-- Exact scale-invariant quality transfer for an arbitrary positive normal
moment. At normal moment `lambda = 2`, the left side is the spherical
`rate * defect / 4` quality. -/
theorem projectiveQuality_from_fixedMoment
    (lambda m s2 rate defect : ℝ)
    (hlambda : lambda ≠ 0) (hm : m ≠ 0)
    (hrate : rate = lambda / m)
    (hdefect : defect = lambda * s2 / m) :
    rate * defect / lambda ^ 2 = s2 / m ^ 2 := by
  rw [hrate, hdefect]
  field_simp [hlambda, hm]
  ring

/-- Sharp anisotropy for two opposed tangent vectors whose magnitudes have
ratio `kappa`. The equal-magnitude result below is the case `kappa = 1`. -/
theorem twoLossWeightedQuality_sub_one
    (kappa ell₁ ell₂ : ℝ) (hkappa : 0 < kappa)
    (hden : kappa * ell₁ + ell₂ ≠ 0) :
    ((kappa * ell₁ ^ 2 + ell₂ ^ 2) / (kappa + 1))
          / (((kappa * ell₁ + ell₂) / (kappa + 1)) ^ 2) - 1
      = kappa * ((ell₁ - ell₂) / (kappa * ell₁ + ell₂)) ^ 2 := by
  have hkappaOne : kappa + 1 ≠ 0 := by positivity
  field_simp [hden, hkappaOne]
  ring

/-- Sharp anisotropy value when tangent balance forces equal mass on two
opposite directions with losses `ell₁` and `ell₂`. -/
theorem twoLossQuality_sub_one
    (ell₁ ell₂ : ℝ) (hsum : ell₁ + ell₂ ≠ 0) :
    ((ell₁ ^ 2 + ell₂ ^ 2) / 2)
          / (((ell₁ + ell₂) / 2) ^ 2) - 1
      = ((ell₁ - ell₂) / (ell₁ + ell₂)) ^ 2 := by
  field_simp [hsum]
  ring

/-- Incidence counting for a biregular coupling between two latitude rings. -/
theorem biregular_interRing_incidence
    (Mi Mj p q E : ℕ)
    (hleft : p * Mi = E) (hright : q * Mj = E) :
    p * Mi = q * Mj :=
  hleft.trans hright.symm

/-- A one-to-one inter-ring coupling is possible only between rings with the
same number of vertices. -/
theorem perfectMatching_ringCounts_eq
    (Mi Mj E : ℕ)
    (hleft : Mi = E) (hright : Mj = E) :
    Mi = Mj :=
  hleft.trans hright.symm

end

end AFPBarrier
