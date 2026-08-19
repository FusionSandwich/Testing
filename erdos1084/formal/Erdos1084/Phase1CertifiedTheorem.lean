import Mathlib
import Erdos1084.Phase1LocalCap
import Erdos1084.Phase1EndToEnd

namespace Erdos1084

/-!
# Complete Phase-I theorem from the five explicit geometric inputs

This is the final assembly theorem for the universal `2.0465` result.  It takes the global
outer-parallel/isoperimetric data and the local spherical-cap/kissing data in their concrete forms
for an actual finite contact packing, derives the optimized affine charge, and invokes the checked
Kepler scalar certificate.
-/

noncomputable section

open scoped BigOperators

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/--
All geometric information needed for Phase I, stated concretely for one finite packing.

* `power` fixes the positive cube root of `n²`.
* `globalSurface` is the finite Bezdek--Langi/Kepler volume lower bound followed by Euclidean
  isoperimetry.
* `boundaryOwned` is the finite-union exposed-patch upper bound.
* `localCaps` contains the spherical-neighborhood estimate, kissing-number coverage, and the
  degree range needed at each center.
-/
structure Phase1PublishedInputCertificate where
  x : ℝ
  surfaceArea : ℝ
  scale : ℝ
  power : KeplerPowerScale (n : ℝ) x
  globalSurface : KeplerGlobalSurfaceInput x surfaceArea scale
  localCaps : X.Phase1LocalCapCertificate
  boundaryOwned : surfaceArea ≤ ∑ i, localCaps.exposure i

/-- Build the older compact certificate from the decomposed published-input certificate. -/
def Phase1PublishedInputCertificate.toGeometryCertificate
    (h : X.Phase1PublishedInputCertificate) :
    X.Phase1GeometryCertificate where
  x := h.x
  surfaceArea := h.surfaceArea
  scale := h.scale
  exposure := h.localCaps.exposure
  power := h.power
  globalSurface := h.globalSurface
  boundaryOwned := h.boundaryOwned
  localDegreeCharge := X.phase1_all_local_degree_charges h.localCaps

/-- Universal clean Phase-I conclusion for one finite packing with the named inputs instantiated. -/
theorem phase1_published_inputs_contact_bound
    (h : X.Phase1PublishedInputCertificate) :
    (X.contactCount : ℝ) < 6 * (n : ℝ) - kpClean * h.x :=
  X.phase1_contactCount_lt h.toGeometryCertificate

/-- Equivalent deficit form. -/
theorem phase1_published_inputs_deficit_bound
    (h : X.Phase1PublishedInputCertificate) :
    kpClean * h.x < 6 * (n : ℝ) - (X.contactCount : ℝ) :=
  X.phase1_clean_deficit_lt h.toGeometryCertificate

end UnitSeparatedConfiguration

end

end Erdos1084
