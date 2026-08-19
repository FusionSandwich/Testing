import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Phase-I end-to-end assembly on an actual finite packing

All large geometric inputs remain explicit ordinary hypotheses.  This file checks the complete
new local-to-global algebra on the direct contact graph of a finite packing.
-/

noncomputable section
open scoped BigOperators

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Real-valued contact degree. -/
def realContactDegree (i : Fin n) : ℝ := X.contactDegree i

/-- Real handshaking identity for the actual contact graph. -/
theorem sum_realContactDegree_eq_twice_contactCount :
    (∑ i : Fin n, X.realContactDegree i) = 2 * (X.contactCount : ℝ) := by
  exact_mod_cast X.sum_contactDegrees_eq_twice_contactCount

/-- Concrete global and local surface data at one finite packing. -/
structure Phase1GeometryCertificate where
  x : ℝ
  surfaceArea : ℝ
  scale : ℝ
  exposure : Fin n → ℝ
  power : KeplerPowerScale (n : ℝ) x
  globalSurface : KeplerGlobalSurfaceInput x surfaceArea scale
  boundaryOwned : surfaceArea ≤ ∑ i, exposure i
  localDegreeCharge : ∀ i,
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - X.realContactDegree i)

/-- Build the exact local surface input from the concrete handshaking identity. -/
theorem phase1_local_surface_input
    (h : X.Phase1GeometryCertificate) :
    KeplerLocalSurfaceInput h.surfaceArea
      (6 * (n : ℝ) - (X.contactCount : ℝ)) := by
  refine kp_local_surface_input_of_charges
    X.realContactDegree h.exposure (n : ℝ) (X.contactCount : ℝ) h.surfaceArea
    ?_ ?_ h.boundaryOwned h.localDegreeCharge
  · simp
  · exact X.sum_realContactDegree_eq_twice_contactCount

/-- Checked clean coefficient theorem for one finite packing carrying the geometric certificate. -/
theorem phase1_contactCount_lt
    (h : X.Phase1GeometryCertificate) :
    (X.contactCount : ℝ) < 6 * (n : ℝ) - kpClean * h.x := by
  exact kp_contact_upper_from_surface h.power h.globalSurface
    (X.phase1_local_surface_input h)

/-- Equivalent deficit form. -/
theorem phase1_clean_deficit_lt
    (h : X.Phase1GeometryCertificate) :
    kpClean * h.x < 6 * (n : ℝ) - (X.contactCount : ℝ) := by
  linarith [X.phase1_contactCount_lt h]

end UnitSeparatedConfiguration
end
end Erdos1084
