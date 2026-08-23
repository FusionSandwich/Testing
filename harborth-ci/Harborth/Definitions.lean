import Mathlib

open scoped BigOperators

namespace Harborth

/-- The Euclidean plane. -/
abbrev Point2 := EuclideanSpace ℝ (Fin 2)

/-- Pairwise separation by at least one. -/
def OneSeparated {n : ℕ} (x : Fin n → Point2) : Prop :=
  ∀ ⦃i j : Fin n⦄, i ≠ j → 1 ≤ dist (x i) (x j)

/-- Unordered unit-contact pairs, represented by ordered pairs `i < j`. -/
noncomputable def contactPairs {n : ℕ} (x : Fin n → Point2) : Finset (Fin n × Fin n) := by
  classical
  exact (Finset.univ.product Finset.univ).filter fun ij =>
    ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1

/-- Number of unordered unit contacts. -/
noncomputable def contactCount {n : ℕ} (x : Fin n → Point2) : ℕ :=
  (contactPairs x).card

/-- A coarse finite bound, used only to define the maximum. -/
theorem contactCount_le_square {n : ℕ} (x : Fin n → Point2) :
    contactCount x ≤ n * n := by
  classical
  unfold contactCount contactPairs
  calc
    ((Finset.univ.product Finset.univ).filter fun ij : Fin n × Fin n =>
        ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1).card
        ≤ (Finset.univ.product Finset.univ : Finset (Fin n × Fin n)).card :=
          Finset.card_filter_le _ _
    _ = n * n := by simp

/-- The greatest contact count achieved by an actual labelled one-separated configuration. -/
noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest
    (fun m => ∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m)
    (n * n)

/-- The real expression in Harborth's formula. -/
noncomputable def harborthExpression (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

/-- Its integer floor. -/
noncomputable def harborthFloor (n : ℕ) : ℤ :=
  ⌊harborthExpression n⌋

end Harborth
