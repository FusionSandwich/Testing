import Mathlib
import Erdos1084.Phase1CanonicalScale
import Erdos1084.MaximizerNoIsolated

namespace Erdos1084

/-!
# Final granular foundational interfaces for Phase I

Existence of `f₃(n)` and the no-isolated-vertex theorem are proved internally.  The remaining
fields are exactly the geometric ports still required: kissing number twelve, the global
outer-parallel/isoperimetric surface bound, and the local spherical-neighborhood exposed-area
bound.
-/

noncomputable section

open scoped BigOperators

/-- Global enlarged-union surface data from finite outer-parallel density and isoperimetry. -/
structure Phase1GlobalSurfaceDataFinal (scale : ℝ) where
  boundaryArea : ℝ
  keplerScale : ℝ
  globalSurface : KeplerGlobalSurfaceInput scale boundaryArea keplerScale

/-- Local exposed-patch data from boundary ownership, cap geometry, and spherical isoperimetry. -/
structure Phase1LocalSurfaceDataFinal {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    (boundaryArea : ℝ) where
  exposure : Fin n → ℝ
  boundary_le_exposure_sum : boundaryArea ≤ ∑ i, exposure i
  local_exposure_charge : ∀ i,
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ))

/-- Exact remaining foundational geometric obligations. -/
structure Phase1FoundationalInputFinal where
  /-- Three-dimensional kissing number twelve. -/
  kissing_degree_bound :
    ∀ {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)),
      X.HasContactDegreeAtMostTwelve
  /-- Kepler outer-parallel density and Euclidean isoperimetry. -/
  global_surface_data :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        Phase1GlobalSurfaceDataFinal (phase1TwoThirdsScale n)
  /-- Boundary ownership, tangent-cap geometry, spherical-neighborhood inequality, and chord. -/
  local_surface_data :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        (global : Phase1GlobalSurfaceDataFinal (phase1TwoThirdsScale n)) →
        Phase1LocalSurfaceDataFinal X global.boundaryArea

namespace Phase1FoundationalInputFinal

/-- The remaining geometric ports construct the provider consumed by the final assembly. -/
def toPublishedInput (foundation : Phase1FoundationalInputFinal) :
    Phase1PublishedInput where
  certificate_for_maximum := by
    intro n m hn hmax
    obtain ⟨X, hX⟩ := hmax.1
    let global := foundation.global_surface_data hn hmax hX
    let local := foundation.local_surface_data hn hmax hX global
    refine ⟨X, hX, ?_⟩
    exact
      { scale := phase1TwoThirdsScale n
        boundaryArea := global.boundaryArea
        keplerScale := global.keplerScale
        exposure := local.exposure
        power := phase1TwoThirdsScale_power (lt_of_lt_of_le (by omega) hn)
        globalSurface := global.globalSurface
        boundary_le_exposure_sum := local.boundary_le_exposure_sum
        no_isolated := contactDegree_pos_of_maximizer hn hmax hX
        degree_le_twelve := foundation.kissing_degree_bound X
        local_exposure_charge := local.local_exposure_charge }

/-- Canonical Phase-I theorem from the remaining foundational geometric ports. -/
theorem main_canonical
    (foundation : Phase1FoundationalInputFinal)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  phase1_main_canonical_decimal foundation.toPublishedInput hn hmax

/-- Final theorem stated for the canonical contact number `contactNumber3 n`. -/
theorem contactNumber3_main_canonical
    (foundation : Phase1FoundationalInputFinal)
    {n : ℕ} (hn : 2 ≤ n) :
    (contactNumber3 n : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  foundation.main_canonical hn (contactNumber3_isMaximum n)

end Phase1FoundationalInputFinal

end

end Erdos1084
