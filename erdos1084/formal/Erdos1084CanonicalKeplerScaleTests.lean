import Erdos1084.CanonicalKeplerScale

open Erdos1084

/-! Smoke tests for the canonical Kepler scale. -/

example : 0 < phase1CanonicalKeplerScale :=
  phase1CanonicalKeplerScale_pos

example :
    phase1CanonicalKeplerScale ^ 3 * Real.pi ^ 2 = 18 :=
  phase1CanonicalKeplerScale_cube_pi

example : KeplerScaleSpec phase1CanonicalKeplerScale :=
  phase1CanonicalKeplerScale_spec

example {x A : ℝ}
    (hlower : 4 * Real.pi * phase1CanonicalKeplerScale * x ≤ A) :
    KeplerGlobalSurfaceInput x A phase1CanonicalKeplerScale :=
  phase1_globalSurface_of_lower hlower
