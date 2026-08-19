import Erdos1084

open Erdos1084 Set

/-! Smoke tests for the finite-union boundary ownership theorem. -/

example
    {ι : Type*} [Finite ι]
    (X : UnitSeparatedConfiguration ι) (r : ℝ) :
    IsClosed (phase1EnlargedUnion X r) :=
  phase1EnlargedUnion_isClosed X r

example
    {ι : Type*} (X : UnitSeparatedConfiguration ι) (r : ℝ) (i : ι) :
    Metric.ball (X.point i) r ⊆ interior (phase1EnlargedUnion X r) :=
  phase1_ball_subset_interior_union X r i

example
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι) (r : ℝ) :
    frontier (phase1EnlargedUnion X r) ⊆
      ⋃ i, phase1ExposedPatch X r i :=
  phase1_frontier_subset_iUnion_exposed X r
