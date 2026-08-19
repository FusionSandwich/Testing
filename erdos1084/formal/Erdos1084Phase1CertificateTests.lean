import Erdos1084

open Erdos1084

/-! Smoke tests for the direct Phase-I geometric-certificate bridge. -/

example {n x : ℝ} (h : TwoThirdPowerScale n x) : 0 < x :=
  h.x_pos

example
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    KeplerLocalSurfaceInput A (6 * n - E) :=
  phase1_local_surface_of_certificate X h

example
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    KeplerGlobalSurfaceInput x A K :=
  phase1_global_surface_of_certificate X h

example
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    E < 6 * n - kpClean * x :=
  phase1_contact_upper_from_certificate X h
