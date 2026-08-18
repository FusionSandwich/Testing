import Erdos1084

open Erdos1084

/-! Smoke tests for the audited Kepler / outer-parallel scalar bridge. -/

example : kpS ^ 2 = 3 := kpS_sq

example : 2 < kpRadius := two_lt_kpRadius

example : 1 < kpRadius - 1 := one_lt_kpOuterRadius

example : 1 / kpRadius = 10 - 11 * kpS / 2 :=
  kpRadius_reciprocal

example : kpRadius ^ 2 * kpQ * kpLocalCoeff = 1 :=
  kp_local_identity

example : (418756933 : ℝ) / 250000000 < kpLocalCoeff :=
  kp_local_compact_lower

example : kpClean ^ 3 * Real.pi ^ 2 < 18 * kpLocalCoeff ^ 3 :=
  kp_clean_cubed_certificate

example {K : ℝ} (hK : KeplerScaleSpec K) :
    kpClean < K * kpLocalCoeff :=
  kp_clean_lt_scale_mul_local hK

example {x A D K : ℝ}
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A D) :
    kpClean * x < D :=
  kp_surface_assembly_strict hg hl

example {n E x A K : ℝ}
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - kpClean * x :=
  kp_contact_upper_from_surface hg hl
