import Erdos1084

open Erdos1084

/-! Smoke tests for the finite publication coefficient `2.0207`. -/

example :
    dodecahedralSurfaceScale ^ 3 * dodecahedralDensityUpper ^ 2 < 1 :=
  dodecahedral_surface_scale_cubed_certificate

example :
    dodecahedralClean < dodecahedralSurfaceScale * kpLocalCoeff :=
  dodecahedral_clean_lt_scale_mul_local

example
    {n E x A : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : DodecahedralGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - dodecahedralClean * x :=
  dodecahedral_contact_upper_from_surface hpower hg hl
