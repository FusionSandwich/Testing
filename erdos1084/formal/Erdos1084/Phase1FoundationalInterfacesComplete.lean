import Mathlib
import Erdos1084.Phase1CanonicalScale
import Erdos1084.MaximizerNoIsolated
import Erdos1084.KissingCoverage

namespace Erdos1084

/-!
# Complete granular Phase-I interfaces

Existence of `f₃(n)`, the no-isolated-maximizer theorem, the contact-direction spherical code, the
degree bound from kissing number twelve, and degree-twelve covering are formalized internally.
The remaining fields are the exact named geometric results not yet ported to Lean.
-/

noncomputable section

open scoped BigOperators

/-- Global enlarged-union surface data. -/
structure Phase1GlobalSurfaceDataComplete (scale : ℝ) where
  boundaryArea : ℝ
  keplerScale : ℝ
  globalSurface : KeplerGlobalSurfaceInput scale boundaryArea keplerScale

/-- Local exposed-patch data, split between degrees `1,...,11` and degree twelve. -/
structure Phase1LocalSurfaceDataComplete {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    (boundaryArea : ℝ) where
  exposure : Fin n → ℝ
  boundary_le_exposure_sum : boundaryArea ≤ ∑ i, exposure i
  charge_of_degree_le_eleven : ∀ i,
    1 ≤ X.contactDegree i →
    X.contactDegree i ≤ 11 →
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ))
  exposure_zero_of_degree_twelve : ∀ i,
    X.contactDegree i = 12 → exposure i = 0

/-- Exact remaining foundational geometric obligations. -/
structure Phase1FoundationalInputComplete where
  /-- The external three-dimensional kissing-number theorem itself. -/
  kissing_number : KissingNumberThreeAtMostTwelve
  /-- Kepler/Bezdek--Lángi outer-parallel density and Euclidean isoperimetry. -/
  global_surface_data :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        Phase1GlobalSurfaceDataComplete (phase1TwoThirdsScale n)
  /-- Boundary ownership and spherical-neighborhood exposed-area estimates. -/
  local_surface_data :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        (global : Phase1GlobalSurfaceDataComplete (phase1TwoThirdsScale n)) →
        Phase1LocalSurfaceDataComplete X global.boundaryArea

namespace Phase1FoundationalInputComplete

/-- The remaining geometric inputs construct the certificate consumed by the final assembly. -/
def toPublishedInput (foundation : Phase1FoundationalInputComplete) :
    Phase1PublishedInput where
  certificate_for_maximum := by
    intro n m hn hmax
    obtain ⟨X, hX⟩ := hmax.1
    let global := foundation.global_surface_data hn hmax hX
    let local := foundation.local_surface_data hn hmax hX global
    have hpos := contactDegree_pos_of_maximizer hn hmax hX
    have hle12 :=
      hasContactDegreeAtMostTwelve_of_kissing foundation.kissing_number X
    refine ⟨X, hX, ⟨?_⟩⟩
    exact
      { scale := phase1TwoThirdsScale n
        boundaryArea := global.boundaryArea
        keplerScale := global.keplerScale
        exposure := local.exposure
        power := phase1TwoThirdsScale_power (lt_of_lt_of_le (by omega) hn)
        globalSurface := global.globalSurface
        boundary_le_exposure_sum := local.boundary_le_exposure_sum
        no_isolated := hpos
        degree_le_twelve := hle12
        local_exposure_charge := by
          intro i
          by_cases h12 : X.contactDegree i = 12
          · rw [local.exposure_zero_of_degree_twelve i h12]
            simp [h12]
          · have h11 : X.contactDegree i ≤ 11 := by
              have := hle12 i
              omega
            exact local.charge_of_degree_le_eleven i (hpos i) h11 }

/-- Final canonical theorem for the actual function `contactNumber3`. -/
theorem contactNumber3_main_canonical
    (foundation : Phase1FoundationalInputComplete)
    {n : ℕ} (hn : 2 ≤ n) :
    (contactNumber3 n : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  phase1_main_canonical_decimal foundation.toPublishedInput hn
    (contactNumber3_isMaximum n)

end Phase1FoundationalInputComplete

end

end Erdos1084
