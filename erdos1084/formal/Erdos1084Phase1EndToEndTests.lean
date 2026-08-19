import Erdos1084

open Erdos1084

/-! Smoke tests for the direct Phase-I finite-packing theorem. -/

example {n : ℕ} {X : UnitSeparatedConfiguration (Fin n)}
    (h : Phase1PackingCertificate X) :
    KeplerLocalSurfaceInput h.boundaryArea
      (6 * (n : ℝ) - (X.contactCount : ℝ)) :=
  h.toKeplerLocalSurfaceInput

example {n : ℕ} {X : UnitSeparatedConfiguration (Fin n)}
    (h : Phase1PackingCertificate X) :
    (X.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.scale :=
  h.contactCount_lt_clean_bound

example {n : ℕ} {X : UnitSeparatedConfiguration (Fin n)}
    (h : Phase1PackingCertificate X) :
    X.contactCount ≤ 6 * n :=
  h.contactCount_le_six_card

example {n : ℕ} {X : UnitSeparatedConfiguration (Fin n)}
    (h : Phase1PackingCertificate X) :
    (X.contactDeficit : ℤ) = X.contactDeficitZ :=
  h.contactDeficit_cast
