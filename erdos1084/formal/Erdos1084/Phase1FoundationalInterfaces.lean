import Mathlib
import Erdos1084.Phase1CanonicalScale

namespace Erdos1084

/-!
# Granular foundational interfaces for Phase I

This module decomposes `Phase1PublishedInput` into the exact independent geometric obligations
that remain to be ported from the named published theorems. It prevents a single opaque
certificate field from obscuring which theorem supplies which inequality.
-/

noncomputable section

open scoped BigOperators

/-- Global enlarged-union surface data obtained from finite outer-parallel density and isoperimetry. -/
structure Phase1GlobalSurfaceData (scale : ℝ) where
  boundaryArea : ℝ
  keplerScale : ℝ
  globalSurface : KeplerGlobalSurfaceInput scale boundaryArea keplerScale

/-- Local exposed-patch data obtained from boundary ownership, cap geometry, and spherical isoperimetry. -/
structure Phase1LocalSurfaceData {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    (boundaryArea : ℝ) where
  exposure : Fin n → ℝ
  boundary_le_exposure_sum : boundaryArea ≤ ∑ i, exposure i
  local_exposure_charge : ∀ i,
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ))

/--
Exact foundational obligations that construct the Phase-I certificate.

No field is declared as a Lean axiom. A foundational development supplies a value of this
structure by proving the listed theorems.
-/
structure Phase1FoundationalInput where
  /-- First-contact relocation: a maximizing realization has no isolated point. -/
  no_isolated_maximizer :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        ∀ i, 1 ≤ X.contactDegree i
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
        Phase1GlobalSurfaceData (phase1TwoThirdsScale n)
  /-- Boundary ownership, tangent-cap geometry, spherical-neighborhood inequality, and chord. -/
  local_surface_data :
    ∀ {n m : ℕ},
      2 ≤ n →
      (hmax : IsThreeDimensionalContactNumber n m) →
      ∀ {X : UnitSeparatedConfiguration (Fin n)},
        X.contactCount = m →
        (global : Phase1GlobalSurfaceData (phase1TwoThirdsScale n)) →
        Phase1LocalSurfaceData X global.boundaryArea

namespace Phase1FoundationalInput

/-- Granular foundational inputs construct the provider used by the final theorem. -/
def toPublishedInput (foundation : Phase1FoundationalInput) :
    Phase1PublishedInput where
  certificate_for_maximum := by
    intro n m hn hmax
    obtain ⟨X, hX⟩ := hmax.1
    let global := foundation.global_surface_data hn hmax hX
    let local := foundation.local_surface_data hn hmax hX global
    refine ⟨X, hX, ⟨?_⟩⟩
    exact
      { scale := phase1TwoThirdsScale n
        boundaryArea := global.boundaryArea
        keplerScale := global.keplerScale
        exposure := local.exposure
        power := phase1TwoThirdsScale_power (lt_of_lt_of_le (by omega) hn)
        globalSurface := global.globalSurface
        boundary_le_exposure_sum := local.boundary_le_exposure_sum
        no_isolated := foundation.no_isolated_maximizer hn hmax hX
        degree_le_twelve := foundation.kissing_degree_bound X
        local_exposure_charge := local.local_exposure_charge }

/-- Final canonical Phase-I theorem directly from the granular foundational interfaces. -/
theorem main_canonical
    (foundation : Phase1FoundationalInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  phase1_main_canonical_decimal foundation.toPublishedInput hn hmax

end Phase1FoundationalInput

end

end Erdos1084
