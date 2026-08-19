import Mathlib
import Erdos1084.Phase1BoundaryGeometry

namespace Erdos1084

/-!
# Measure upper bound for the finite enlarged-union boundary

Boundary ownership immediately yields the required surface-measure subadditivity.  No pairwise
disjointness and no subtraction of multiple-owned points is needed because the proof uses only an
upper bound.
-/

noncomputable section

open MeasureTheory
open scoped BigOperators ENNReal

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Any measure of the enlarged-union boundary is at most the sum of the exposed-patch measures. -/
theorem measure_frontier_le_sum_exposedPatch
    (μ : Measure Point3) (r : ℝ) :
    μ (frontier (X.enlargedUnion r)) ≤
      ∑ i : Fin n, μ (X.exposedPatch r i) := by
  calc
    μ (frontier (X.enlargedUnion r)) ≤
        μ (⋃ i : Fin n, X.exposedPatch r i) :=
      measure_mono (X.frontier_enlargedUnion_subset_iUnion_exposedPatch r)
    _ ≤ ∑' i : Fin n, μ (X.exposedPatch r i) := measure_iUnion_le
    _ = ∑ i : Fin n, μ (X.exposedPatch r i) := by
      rw [tsum_fintype]

end UnitSeparatedConfiguration

end

end Erdos1084
