import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Phase-I packing-to-contact theorem

This module connects the direct finite-packing/contact-graph model to the audited Kepler
surface-assembly theorem.

The five large published geometric inputs are not declared as project axioms.  Their concrete
consequences for one packing are carried by the fields of `Phase1PackingCertificate`:

* the Kepler/outer-parallel global surface lower bound;
* the finite-union boundary-to-exposed-patches inequality;
* the spherical-neighborhood local exposed-area inequalities;
* the kissing-number degree bound and degree-twelve coverage;
* the positive `n^(2/3)` normalization.

Consequently the theorem below is an end-to-end Lean proof from an actual finite contact graph to
the clean coefficient, relative to those visible geometric certificates.  Foundational Lean ports
of the named published theorems can later construct this certificate without changing the final
assembly theorem.
-/

noncomputable section

open scoped BigOperators

/--
All geometric consequences needed for the Phase-I theorem, stated for one actual finite packing.

`scale` is the positive real cube root of `n^2`; `boundaryArea` is the boundary/perimeter scalar
used in the global comparison; `exposure i` is an upper accounting variable for the exposed patch
owned by the `i`-th enlarged sphere.
-/
structure Phase1PackingCertificate {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) where
  /-- The positive `n^(2/3)` scale. -/
  scale : ℝ
  /-- Surface area/perimeter scalar for the enlarged union. -/
  boundaryArea : ℝ
  /-- The positive Kepler surface scale `(18 / π²)^(1/3)`. -/
  keplerScale : ℝ
  /-- Local exposed-patch accounting function. -/
  exposure : Fin n → ℝ
  /-- Exact positive-power normalization `scale^3 = n^2`. -/
  power : KeplerPowerScale (n : ℝ) scale
  /-- Kepler outer-parallel volume plus Euclidean isoperimetry. -/
  globalSurface : KeplerGlobalSurfaceInput scale boundaryArea keplerScale
  /-- Boundary ownership/subadditivity for the finite union of enlarged balls. -/
  boundary_le_exposure_sum : boundaryArea ≤ ∑ i, exposure i
  /-- No isolated point; this is supplied by the first-contact relocation of a maximizer. -/
  no_isolated : ∀ i, 1 ≤ X.contactDegree i
  /-- Kissing number twelve. -/
  degree_le_twelve : X.HasContactDegreeAtMostTwelve
  /--
  Tangent-cap geometry, spherical-neighborhood isoperimetry, optimized convex chord, and
  degree-twelve coverage.
  -/
  local_exposure_charge : ∀ i,
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ))

namespace Phase1PackingCertificate

variable {n : ℕ} {X : UnitSeparatedConfiguration (Fin n)}

/-- The certificate implies the local surface interface used by the scalar Kepler assembly. -/
theorem toKeplerLocalSurfaceInput
    (h : Phase1PackingCertificate X) :
    KeplerLocalSurfaceInput h.boundaryArea
      (6 * (n : ℝ) - (X.contactCount : ℝ)) := by
  have hdegree :
      (∑ i : Fin n, (X.contactDegree i : ℝ)) =
        2 * (X.contactCount : ℝ) := by
    exact_mod_cast X.sum_contactDegrees_eq_twice_contactCount
  exact kp_local_surface_input_of_charges
    (fun i : Fin n => (X.contactDegree i : ℝ))
    h.exposure
    (n : ℝ)
    (X.contactCount : ℝ)
    h.boundaryArea
    (by simp)
    hdegree
    h.boundary_le_exposure_sum
    h.local_exposure_charge

/--
Strict Phase-I contact bound for one certified finite packing.

The clean constant `kpClean` is exactly `4093/2000 = 2.0465`.
-/
theorem contactCount_lt_clean_bound
    (h : Phase1PackingCertificate X) :
    (X.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.scale := by
  exact kp_contact_upper_from_surface
    h.power h.globalSurface h.toKeplerLocalSurfaceInput

/-- The kissing-number field also gives the ordinary combinatorial bound `E ≤ 6n`. -/
theorem contactCount_le_six_card
    (h : Phase1PackingCertificate X) :
    X.contactCount ≤ 6 * n := by
  simpa using X.contactCount_le_six_card h.degree_le_twelve

/-- The natural and integer contact deficits agree for a Phase-I certified packing. -/
theorem contactDeficit_cast
    (h : Phase1PackingCertificate X) :
    (X.contactDeficit : ℤ) = X.contactDeficitZ :=
  X.contactDeficit_cast h.degree_le_twelve

end Phase1PackingCertificate

end

end Erdos1084
