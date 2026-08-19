import Erdos1084.FiniteBallUnionBoundary

open Set Metric MeasureTheory
open Erdos1084

/-! Smoke tests for the finite-union boundary bridge. -/

example {E ι : Type*} [PseudoMetricSpace E] [Fintype ι]
    (center : ι → E) (r : ℝ) :
    IsClosed (finiteClosedBallUnion center r) :=
  finiteClosedBallUnion_isClosed center r

example {E ι : Type*} [PseudoMetricSpace E] [Fintype ι]
    (center : ι → E) (r : ℝ) :
    frontier (finiteClosedBallUnion center r) ⊆
      ⋃ i, exposedSpherePatch center r i :=
  frontier_finiteClosedBallUnion_subset_exposed center r

example {E ι : Type*} [PseudoMetricSpace E] [Fintype ι]
    (μ : Measure E) (center : ι → E) (r : ℝ) :
    μ (frontier (finiteClosedBallUnion center r)) ≤
      ∑' i, μ (exposedSpherePatch center r i) :=
  measure_frontier_finiteClosedBallUnion_le_tsum_exposed μ center r
