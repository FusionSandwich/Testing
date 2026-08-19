import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Canonical Kepler surface scale

The scalar assembly uses the unique positive number `K` with `K³ π² = 18`.  This module defines
that number canonically as a real cube root and proves the exact specification.
-/

noncomputable section

/-- Canonical positive cube root of `18/π²`. -/
def phase1CanonicalKeplerScale : ℝ :=
  Real.cbrt (18 / Real.pi ^ 2)

/-- The canonical Kepler scale is positive. -/
theorem phase1CanonicalKeplerScale_pos :
    0 < phase1CanonicalKeplerScale := by
  apply Real.cbrt_pos.2
  positivity

/-- Exact scale equation. -/
theorem phase1CanonicalKeplerScale_cube_pi :
    phase1CanonicalKeplerScale ^ 3 * Real.pi ^ 2 = 18 := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  rw [phase1CanonicalKeplerScale, Real.cbrt_cubed]
  field_simp [hpi]

/-- The canonical scale satisfies the abstract Kepler scale specification. -/
theorem phase1CanonicalKeplerScale_spec :
    KeplerScaleSpec phase1CanonicalKeplerScale := by
  exact ⟨phase1CanonicalKeplerScale_pos,
    phase1CanonicalKeplerScale_cube_pi⟩

/-- Construct the global surface interface from its single geometric inequality. -/
theorem phase1_globalSurface_of_lower
    {x A : ℝ}
    (hlower : 4 * Real.pi * phase1CanonicalKeplerScale * x ≤ A) :
    KeplerGlobalSurfaceInput x A phase1CanonicalKeplerScale :=
  ⟨phase1CanonicalKeplerScale_spec, hlower⟩

end

end Erdos1084
