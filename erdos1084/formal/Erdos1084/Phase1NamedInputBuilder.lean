import Mathlib
import Erdos1084.Phase1FiniteDensityIsoperimetry
import Erdos1084.Phase1CertifiedTheorem
import Erdos1084.Phase1F3Theorem

namespace Erdos1084

/-!
# Explicit builder for the five named Phase-I inputs

This file replaces an opaque final certificate by individually named conclusions corresponding to
finite outer-parallel density, Euclidean isoperimetry, finite-union boundary ownership, spherical
neighborhood isoperimetry, and kissing number twelve.  The builder proves that these source-level
conclusions imply the exact certificate consumed by the checked Phase-I theorem.
-/

noncomputable section

open scoped BigOperators

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Source-level Phase-I conclusions for one actual packing. -/
structure Phase1RawGeometricInputs where
  x : ℝ
  volume : ℝ
  surfaceArea : ℝ
  scale : ℝ
  exposure : Fin n → ℝ

  power : KeplerPowerScale (n : ℝ) x
  scaleSpec : KeplerScaleSpec scale

  volume_nonneg : 0 ≤ volume
  surface_nonneg : 0 ≤ surfaceArea

  /-- Bezdek--Langi plus Kepler at `r_*`: `4 sqrt(2) n ≤ volume(U_{r_*})`. -/
  finiteOuterParallel : 4 * Real.sqrt 2 * (n : ℝ) ≤ volume

  /-- Cubed Euclidean isoperimetry for the chosen surface quantity. -/
  euclideanIsoperimetric :
    36 * Real.pi * volume ^ 2 ≤ surfaceArea ^ 3

  /-- Boundary ownership/subadditivity by the per-sphere exposed patches. -/
  boundaryOwned : surfaceArea ≤ ∑ i, exposure i

  /-- Connected-maximizer reduction: no isolated contact-graph vertex. -/
  minimumDegree : ∀ i, 1 ≤ X.contactDegree i

  /-- Kissing number twelve. -/
  maximumDegree : ∀ i, X.contactDegree i ≤ 12

  /-- Spherical-neighborhood comparison for degrees `1,...,11`. -/
  sphericalNeighborhood : ∀ i, X.contactDegree i ≤ 11 →
    exposure i ≤
      (2 * Real.pi * kpRadius ^ 2) *
        kpOptimizedH (rtX (X.contactDegree i : ℝ))

  /-- Complete hidden-cap coverage at degree twelve. -/
  kissingCoverage : ∀ i, X.contactDegree i = 12 → exposure i ≤ 0

/-- The named raw inputs produce the checked local cap certificate. -/
def Phase1RawGeometricInputs.toLocalCapCertificate
    (h : X.Phase1RawGeometricInputs) :
    X.Phase1LocalCapCertificate where
  exposure := h.exposure
  minimumDegree := h.minimumDegree
  maximumDegree := h.maximumDegree
  capBound := h.sphericalNeighborhood
  coveredAtTwelve := h.kissingCoverage

/-- The named raw inputs produce the checked finite-density/isoperimetric input. -/
def Phase1RawGeometricInputs.toGlobalInput
    (h : X.Phase1RawGeometricInputs) :
    Phase1FiniteDensityIsoperimetricInput
      (n : ℝ) h.x h.volume h.surfaceArea h.scale where
  power := h.power
  scale := h.scaleSpec
  n_nonneg := by positivity
  volume_nonneg := h.volume_nonneg
  surface_nonneg := h.surface_nonneg
  finite_density := h.finiteOuterParallel
  isoperimetric_cube := h.euclideanIsoperimetric

/-- Build the final checked packing certificate from the individually named conclusions. -/
def Phase1RawGeometricInputs.toPublishedInputCertificate
    (h : X.Phase1RawGeometricInputs) :
    X.Phase1PublishedInputCertificate where
  x := h.x
  volume := h.volume
  surfaceArea := h.surfaceArea
  scale := h.scale
  globalGeometry := h.toGlobalInput
  localCaps := h.toLocalCapCertificate
  boundaryOwned := h.boundaryOwned

/-- A maximizing packing together with all individually named Phase-I inputs. -/
structure Phase1RawF3Input (n : ℕ) where
  packing : UnitSeparatedConfiguration (Fin n)
  realizes : packing.contactCount = f3Nat n
  geometry : packing.Phase1RawGeometricInputs

/-- Convert raw source-level data to the final formal `f₃` certificate. -/
def Phase1RawF3Input.toF3Certificate
    {n : ℕ} (h : Phase1RawF3Input n) :
    Phase1F3Certificate n where
  packing := h.packing
  realizes := h.realizes
  geometry := h.geometry.toPublishedInputCertificate

/-- Final clean bound directly from the individually named source conclusions. -/
theorem phase1_f3Nat_bound_of_raw_inputs
    {n : ℕ} (h : Phase1RawF3Input n) :
    (f3Nat n : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  phase1_f3Nat_bound h.toF3Certificate

end UnitSeparatedConfiguration

end

end Erdos1084
