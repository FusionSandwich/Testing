import Erdos1084.KissingCoverage

open Erdos1084

/-! Smoke tests for the kissing-number consequences. -/

example
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    X.HasContactDegreeAtMostTwelve :=
  hasContactDegreeAtMostTwelve_of_kissing hk X

example
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (hdegree : X.contactDegree i = 12)
    (u : Point3) (hu : ‖u‖ = 1) :
    ∃ j : ContactNeighbor X i,
      1 / 2 ≤ ⟪u, contactNeighborDirection X i j⟫_ℝ :=
  degree_twelve_contact_directions_cover hk X i hdegree u hu
