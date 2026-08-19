import Erdos1084.DegreeTwelveExposure

open Erdos1084

/-! Smoke tests for degree-twelve exposure. -/

example : 1 / kpRadius < (1 / 2 : ℝ) :=
  kpRadius_reciprocal_lt_half

example
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (hdegree : X.contactDegree i = 12) :
    phase1TangentExposedDirections X i = ∅ :=
  phase1TangentExposedDirections_eq_empty_of_degree_twelve
    hk X i hdegree
