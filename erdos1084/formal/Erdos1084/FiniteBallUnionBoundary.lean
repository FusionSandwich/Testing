import Mathlib

namespace Erdos1084

/-!
# Boundary ownership for a finite union of closed balls

This file formalizes the set-theoretic core of the finite-union boundary bridge used in Phase I.
Every boundary point of a finite union of closed balls lies on at least one generating sphere and
lies in no open generating ball. Hence the boundary is covered by the exposed sphere patches.

The theorem is valid in an arbitrary pseudo-metric topological space with finite index type. A
measure-theoretic corollary then bounds any measure of the boundary by the sum of the exposed-patch
measures.
-/

open Set Metric MeasureTheory

noncomputable section

variable {E ι : Type*} [PseudoMetricSpace E] [Fintype ι]

/-- Finite union of equal-radius closed balls. -/
def finiteClosedBallUnion (center : ι → E) (r : ℝ) : Set E :=
  ⋃ i, closedBall (center i) r

/--
The part of the `i`-th generating sphere that is not contained in any open generating ball.
Including the `i`-th open ball in the removed union does not change the patch.
-/
def exposedSpherePatch (center : ι → E) (r : ℝ) (i : ι) : Set E :=
  sphere (center i) r \ ⋃ j, ball (center j) r

/-- A finite union of closed balls is closed. -/
theorem finiteClosedBallUnion_isClosed
    (center : ι → E) (r : ℝ) :
    IsClosed (finiteClosedBallUnion center r) := by
  classical
  unfold finiteClosedBallUnion
  exact isClosed_iUnion_of_finite fun i => isClosed_closedBall

/-- A boundary point cannot lie in any open generating ball. -/
theorem not_mem_openBall_of_mem_frontier_finiteClosedBallUnion
    {center : ι → E} {r : ℝ} {x : E}
    (hx : x ∈ frontier (finiteClosedBallUnion center r)) :
    ∀ j : ι, x ∉ ball (center j) r := by
  classical
  rw [frontier] at hx
  intro j hxball
  apply hx.2
  exact interior_maximal
    (fun y hy => mem_iUnion_of_mem j (ball_subset_closedBall hy))
    isOpen_ball
    hxball

/-- Every boundary point is owned by at least one exposed generating sphere patch. -/
theorem frontier_finiteClosedBallUnion_subset_exposed
    (center : ι → E) (r : ℝ) :
    frontier (finiteClosedBallUnion center r) ⊆
      ⋃ i, exposedSpherePatch center r i := by
  classical
  intro x hx
  have hxFrontier := hx
  rw [frontier] at hx
  have hxUnion : x ∈ finiteClosedBallUnion center r := by
    have hclosed := finiteClosedBallUnion_isClosed center r
    rw [hclosed.closure_eq] at hx
    exact hx.1
  rcases mem_iUnion.mp hxUnion with ⟨i, hxi⟩
  have hnotball :=
    not_mem_openBall_of_mem_frontier_finiteClosedBallUnion hxFrontier i
  have hle : dist x (center i) ≤ r := by
    simpa [mem_closedBall, dist_comm] using hxi
  have hnlt : ¬dist x (center i) < r := by
    simpa [mem_ball, dist_comm] using hnotball
  have heq : dist x (center i) = r := le_antisymm hle (le_of_not_gt hnlt)
  apply mem_iUnion_of_mem i
  constructor
  · simpa [mem_sphere, dist_comm] using heq
  · intro hxOpen
    rcases mem_iUnion.mp hxOpen with ⟨j, hxj⟩
    exact not_mem_openBall_of_mem_frontier_finiteClosedBallUnion hxFrontier j hxj

/-- Measure subadditivity for the exposed-patch cover. -/
theorem measure_frontier_finiteClosedBallUnion_le_tsum_exposed
    [MeasurableSpace E]
    (μ : Measure E) (center : ι → E) (r : ℝ) :
    μ (frontier (finiteClosedBallUnion center r)) ≤
      ∑' i, μ (exposedSpherePatch center r i) := by
  calc
    μ (frontier (finiteClosedBallUnion center r)) ≤
        μ (⋃ i, exposedSpherePatch center r i) :=
      measure_mono (frontier_finiteClosedBallUnion_subset_exposed center r)
    _ ≤ ∑' i, μ (exposedSpherePatch center r i) :=
      measure_iUnion_le _

end

end Erdos1084
