import Mathlib
import Erdos1084.FiniteSpherePacking

namespace Erdos1084

/-!
# Boundary ownership for a finite union of enlarged balls

This file formalizes the set-theoretic core of the Phase-I boundary lemma.  Every boundary point
of a finite union of equal closed balls belongs to a sphere patch that is not contained in the
open interior of any other ball.  Measure subadditivity and the codimension-two null-intersection
step are kept separate from this topological ownership theorem.
-/

noncomputable section

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Centers after the point problem is scaled to a unit-ball packing. -/
def doubledCenter (i : Fin n) : Point3 := (2 : ℝ) • X.point i

/-- Finite union of radius-`r` closed balls around the scaled packing centers. -/
def enlargedUnion (r : ℝ) : Set Point3 :=
  ⋃ i : Fin n, Metric.closedBall (X.doubledCenter i) r

/-- Union of all open enlarged balls except the ball indexed by `i`. -/
def otherOpenBalls (r : ℝ) (i : Fin n) : Set Point3 :=
  ⋃ j : {j : Fin n // j ≠ i}, Metric.ball (X.doubledCenter j.1) r

/-- The sphere patch owned by `i` after removing interiors of all other enlarged balls. -/
def exposedPatch (r : ℝ) (i : Fin n) : Set Point3 :=
  Metric.sphere (X.doubledCenter i) r \ X.otherOpenBalls r i

/-- A finite union of closed metric balls is closed. -/
theorem isClosed_enlargedUnion (r : ℝ) : IsClosed (X.enlargedUnion r) := by
  classical
  exact isClosed_iUnion fun i => Metric.isClosed_closedBall

/-- Every individual open enlarged ball is contained in the full enlarged union. -/
theorem ball_subset_enlargedUnion (r : ℝ) (i : Fin n) :
    Metric.ball (X.doubledCenter i) r ⊆ X.enlargedUnion r := by
  intro x hx
  exact Set.mem_iUnion.2 ⟨i, Metric.ball_subset_closedBall hx⟩

/-- A boundary point of the enlarged union cannot lie in the interior of any enlarged ball. -/
theorem frontier_not_mem_ball {r : ℝ} {x : Point3}
    (hx : x ∈ frontier (X.enlargedUnion r)) (i : Fin n) :
    x ∉ Metric.ball (X.doubledCenter i) r := by
  rw [frontier] at hx
  intro hball
  have hsubset := X.ball_subset_enlargedUnion r i
  have hxint : x ∈ interior (X.enlargedUnion r) :=
    (interior_maximal Metric.isOpen_ball hsubset) hball
  exact hx.2 hxint

/-- Exact topological boundary ownership by exposed sphere patches. -/
theorem frontier_enlargedUnion_subset_iUnion_exposedPatch (r : ℝ) :
    frontier (X.enlargedUnion r) ⊆ ⋃ i : Fin n, X.exposedPatch r i := by
  classical
  intro x hx
  have hclosed := X.isClosed_enlargedUnion r
  rw [frontier, hclosed.closure_eq] at hx
  rcases Set.mem_iUnion.1 hx.1 with ⟨i, hi⟩
  have hle : dist x (X.doubledCenter i) ≤ r := by
    simpa [Metric.mem_closedBall, dist_comm] using hi
  have hnotlt : ¬dist x (X.doubledCenter i) < r := by
    intro hlt
    have hball : x ∈ Metric.ball (X.doubledCenter i) r := by
      simpa [Metric.mem_ball, dist_comm] using hlt
    exact (X.frontier_not_mem_ball (by simpa [frontier, hclosed.closure_eq] using hx) i) hball
  have heq : dist x (X.doubledCenter i) = r :=
    le_antisymm hle (not_lt.mp hnotlt)
  have hsphere : x ∈ Metric.sphere (X.doubledCenter i) r := by
    simpa [Metric.mem_sphere, dist_comm] using heq
  have hother : x ∉ X.otherOpenBalls r i := by
    intro hmem
    rcases Set.mem_iUnion.1 hmem with ⟨j, hj⟩
    exact X.frontier_not_mem_ball
      (by simpa [frontier, hclosed.closure_eq] using hx) j.1 hj
  exact Set.mem_iUnion.2 ⟨i, ⟨hsphere, hother⟩⟩

end UnitSeparatedConfiguration

end

end Erdos1084
