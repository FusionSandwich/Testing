import Erdos1084.Phase1BoundaryMeasure

open Erdos1084
open MeasureTheory
open scoped BigOperators ENNReal

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))
    (μ : Measure Point3) (r : ℝ) :
    μ (frontier (X.enlargedUnion r)) ≤
      ∑ i : Fin n, μ (X.exposedPatch r i) :=
  X.measure_frontier_le_sum_exposedPatch μ r
