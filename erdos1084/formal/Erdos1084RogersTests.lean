import Erdos1084

open Erdos1084

/-! Smoke tests for the corrected Rogers finite coefficient. -/

example :
    rogersSurfaceScale ^ 3 * rogersSigmaUpper ^ 2 < 1 :=
  rogers_surface_scale_cubed_certificate

example : rogersClean < rogersSurfaceScale * kpLocalCoeff :=
  rogers_clean_lt_scale_mul_local

example
    {n E x A : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : RogersGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - rogersClean * x :=
  rogers_contact_upper_from_surface hpower hg hl
