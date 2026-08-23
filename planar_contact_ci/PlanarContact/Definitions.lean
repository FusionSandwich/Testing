import Mathlib

open scoped BigOperators NNReal

namespace PlanarContact

/-- The Euclidean plane, represented as two-dimensional Euclidean space. -/
abbrev Point := EuclideanSpace ℝ (Fin 2)

/-- A labelled finite configuration whose distinct points are at distance at least one. -/
structure Configuration (n : ℕ) where
  point : Fin n → Point
  oneSeparated : ∀ ⦃i j : Fin n⦄, i ≠ j → (1 : ℝ) ≤ dist (point i) (point j)

namespace Configuration

variable {n : ℕ}

/-- The contact graph: two labels are adjacent exactly when their points are one unit apart. -/
def contactGraph (C : Configuration n) : SimpleGraph (Fin n) :=
  SimpleGraph.fromRel fun i j => dist (C.point i) (C.point j) = 1

/-- The exact number of unordered unit-distance pairs in a configuration. -/
noncomputable def contactCount (C : Configuration n) : ℕ := by
  classical
  exact C.contactGraph.edgeFinset.card

@[simp] theorem contactGraph_adj (C : Configuration n) {i j : Fin n} :
    C.contactGraph.Adj i j ↔ i ≠ j ∧ dist (C.point i) (C.point j) = 1 := by
  simp [contactGraph, dist_comm]

end Configuration

/-- `Attainable n k` means that some one-separated `n`-point configuration has exactly `k` contacts. -/
def Attainable (n k : ℕ) : Prop := ∃ C : Configuration n, C.contactCount = k

/-- The real-valued Harborth expression before taking its floor. -/
noncomputable def harborthReal (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

/-- The proposed exact planar contact number. -/
noncomputable def harborthNumber (n : ℕ) : ℕ := ⌊harborthReal n⌋₊

/-- The extremal contact number, defined as the greatest attainable count below the
number of unordered pairs. -/
noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (Attainable n) (n.choose 2)

end PlanarContact
