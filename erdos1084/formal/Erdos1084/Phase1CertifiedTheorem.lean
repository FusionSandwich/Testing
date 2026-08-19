import Mathlib
import Erdos1084.Phase1LocalCap
import Erdos1084.Phase1EndToEnd

namespace Erdos1084

/-!
# Complete Phase-I theorem from explicit named geometric conclusions

This file combines the direct global surface lower bound, boundary ownership, spherical
neighborhood comparison, kissing number coverage, and connected-maximizer degree range.  The
large published results are ordinary structure fields and are visible in the theorem signature.
-/

noncomputable section
open scoped BigOperators

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Decomposed geometric conclusions needed by the checked Phase-I proof. -/
structure Phase1PublishedInputCertificate where
  x : ℝ
  surfaceArea : ℝ
  scale : ℝ
  power : KeplerPowerScale (n : ℝ) x
  globalSurface : KeplerGlobalSurfaceInput x surfaceArea scale
  localCaps : X.Phase1LocalCapCertificate
  boundaryOwned : surfaceArea ≤ ∑ i, localCaps.exposure i

/-- Convert the decomposed named inputs to the compact assembly certificate. -/
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
  localDegreeCharge := by
    intro i
    simpa [realContactDegree] using X.phase1_local_degree_charge h.localCaps i

/-- Clean coefficient theorem for a concrete packing with the named inputs instantiated. -/
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
