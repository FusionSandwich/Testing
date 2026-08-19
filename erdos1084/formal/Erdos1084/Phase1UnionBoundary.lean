import Mathlib
import Erdos1084.FiniteSpherePacking

namespace Erdos1084

/-!
# Boundary ownership for a finite union of congruent balls

This module formalizes the topological part of the Phase-I boundary bridge.  Every point of the
boundary of a finite union of closed balls belongs to an exposed patch of at least one generating
sphere.  No geometric-measure-theory theorem is assumed here.
-/

noncomputable section

open Set

/-- Union of the closed radius-`r` balls centered at the packing points. -/
def phase1EnlargedUnion
    {ι : Type*} (X : UnitSeparatedConfiguration ι) (r : ℝ) : Set Point3 :=
  ⋃ i, Metric.closedBall (X.point i) r

/-- The actual exposed patch of sphere `i`; points inside any other open ball are removed. -/
def phase1ExposedPatch
    {ι : Type*} (X : UnitSeparatedConfiguration ι) (r : ℝ) (i : ι) : Set Point3 :=
  Metric.sphere (X.point i) r \
    ⋃ j : {j : ι // j ≠ i}, Metric.ball (X.point j.1) r

/-- A finite enlarged union is closed. -/
theorem phase1EnlargedUnion_isClosed
    {ι : Type*} [Finite ι]
    (X : UnitSeparatedConfiguration ι) (r : ℝ) :
    IsClosed (phase1EnlargedUnion X r) := by
  exact isClosed_iUnion fun i => Metric.isClosed_closedBall

/-- Every generating closed ball is contained in the enlarged union. -/
theorem phase1_closedBall_subset_union
    {ι : Type*} (X : UnitSeparatedConfiguration ι) (r : ℝ) (i : ι) :
    Metric.closedBall (X.point i) r ⊆ phase1EnlargedUnion X r := by
  intro x hx
  exact mem_iUnion.2 ⟨i, hx⟩

/-- Every generating open ball lies in the interior of the enlarged union. -/
theorem phase1_ball_subset_interior_union
    {ι : Type*} (X : UnitSeparatedConfiguration ι) (r : ℝ) (i : ι) :
    Metric.ball (X.point i) r ⊆ interior (phase1EnlargedUnion X r) := by
  exact interior_maximal
    (fun _ hx => phase1_closedBall_subset_union X r i (Metric.ball_subset_closedBall hx))
    Metric.isOpen_ball

/-- Boundary ownership by exposed sphere patches. -/
theorem phase1_frontier_subset_iUnion_exposed
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι) (r : ℝ) :
    frontier (phase1EnlargedUnion X r) ⊆ ⋃ i, phase1ExposedPatch X r i := by
  classical
  intro x hx
  have hclosed := phase1EnlargedUnion_isClosed X r
  have hx' : x ∈ closure (phase1EnlargedUnion X r) ∧
      x ∉ interior (phase1EnlargedUnion X r) := by
    simpa [frontier] using hx
  have hxU : x ∈ phase1EnlargedUnion X r := by
    simpa [hclosed.closure_eq] using hx'.1
  rcases mem_iUnion.1 hxU with ⟨i, hxi⟩
  have hxnotball : ∀ j : ι, x ∉ Metric.ball (X.point j) r := by
    intro j hxball
    exact hx'.2 (phase1_ball_subset_interior_union X r j hxball)
  have hdist : dist x (X.point i) = r := by
    have hle : dist x (X.point i) ≤ r := by
      simpa [Metric.mem_closedBall, dist_comm] using hxi
    have hnlt : ¬ dist x (X.point i) < r := by
      simpa [Metric.mem_ball, dist_comm] using hxnotball i
    exact le_antisymm hle (le_of_not_gt hnlt)
  apply mem_iUnion.2
  refine ⟨i, ?_⟩
  constructor
  · simpa [Metric.mem_sphere] using hdist
  · intro hother
    rcases mem_iUnion.1 hother with ⟨j, hxj⟩
    exact hxnotball j.1 hxj

end

end Erdos1084
