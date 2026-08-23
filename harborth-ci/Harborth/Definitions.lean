import Mathlib

open scoped BigOperators

namespace Harborth

abbrev Point2 := EuclideanSpace ℝ (Fin 2)

def OneSeparated {n : ℕ} (x : Fin n → Point2) : Prop :=
  ∀ ⦃i j : Fin n⦄, i ≠ j → 1 ≤ dist (x i) (x j)

noncomputable def contactPairs {n : ℕ} (x : Fin n → Point2) : Finset (Fin n × Fin n) := by
  classical
  exact (Finset.univ.product Finset.univ).filter fun ij =>
    ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1

noncomputable def contactCount {n : ℕ} (x : Fin n → Point2) : ℕ :=
  (contactPairs x).card

theorem contactCount_le_choose {n : ℕ} (x : Fin n → Point2) :
    contactCount x ≤ n.choose 2 := by
  classical
  unfold contactCount contactPairs
  calc
    ((Finset.univ.product Finset.univ).filter fun ij : Fin n × Fin n =>
        ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1).card
        ≤ ((Finset.univ.product Finset.univ).filter fun ij : Fin n × Fin n =>
            ij.1 < ij.2).card := by
              apply Finset.card_le_card
              intro ij hij
              simp only [Finset.mem_filter, Finset.mem_product, Finset.mem_univ, true_and] at hij ⊢
              exact hij.1
    _ = n.choose 2 := by
      simpa using Finset.card_pairs_lt (Finset.univ : Finset (Fin n))

noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest
    (fun m => ∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m)
    (n.choose 2)

noncomputable def harborthExpression (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

noncomputable def harborthFloor (n : ℕ) : ℤ :=
  ⌊harborthExpression n⌋

end Harborth
