import Mathlib

namespace Erdos1084

/-!
# Finite cap-union neighborhood inclusion

For the Phase-I local argument one only needs that the closed `s`-neighborhood of the union of
radius-`β` caps is contained in the union of radius-`β+s` caps.  Equality is unnecessary: the
actual hidden region may only be larger.  The inclusion is a direct triangle-inequality theorem
valid in every pseudo-metric space.
-/

namespace Phase1CapNeighborhood

variable {α ι : Type*} [PseudoMetricSpace α]

/-- A finite or indexed union of closed metric balls. -/
def capUnion (center : ι → α) (β : ℝ) : Set α :=
  ⋃ i, Metric.closedBall (center i) β

/-- Elementary closed neighborhood, written with an explicit witness point. -/
def closedNeighborhood (s : ℝ) (A : Set α) : Set α :=
  {x | ∃ y ∈ A, dist x y ≤ s}

/-- The neighborhood of a union of radius-`β` caps lies in the radius-`β+s` cap union. -/
theorem closedNeighborhood_capUnion_subset
    (center : ι → α) (β s : ℝ) :
    closedNeighborhood s (capUnion center β) ⊆
      capUnion center (β + s) := by
  intro x hx
  rcases hx with ⟨y, hy, hxy⟩
  rcases Set.mem_iUnion.1 hy with ⟨i, hyi⟩
  refine Set.mem_iUnion.2 ⟨i, ?_⟩
  have hyc : dist y (center i) ≤ β := by
    simpa [Metric.mem_closedBall] using hyi
  have htri : dist x (center i) ≤ dist x y + dist y (center i) :=
    dist_triangle _ _ _
  have : dist x (center i) ≤ β + s := by
    linarith
  simpa [Metric.mem_closedBall] using this

/-- Monotonicity in the neighborhood radius. -/
theorem closedNeighborhood_mono_radius
    {A : Set α} {s t : ℝ} (hst : s ≤ t) :
    closedNeighborhood s A ⊆ closedNeighborhood t A := by
  rintro x ⟨y, hy, hxy⟩
  exact ⟨y, hy, le_trans hxy hst⟩

/-- Monotonicity in the underlying set. -/
theorem closedNeighborhood_mono_set
    {A B : Set α} (hAB : A ⊆ B) (s : ℝ) :
    closedNeighborhood s A ⊆ closedNeighborhood s B := by
  rintro x ⟨y, hy, hxy⟩
  exact ⟨y, hAB hy, hxy⟩

end Phase1CapNeighborhood

end Erdos1084
