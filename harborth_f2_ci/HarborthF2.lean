import Mathlib

/-!
# Harborth's exact planar contact number

This file defines finite one-separated configurations in the Euclidean plane,
their unit-contact count, the extremal contact number, and Harborth's target.
-/

noncomputable section

open scoped BigOperators

namespace HarborthF2

abbrev Point := EuclideanSpace ℝ (Fin 2)

def OneSeparated {n : ℕ} (x : Fin n → Point) : Prop :=
  ∀ ⦃i j : Fin n⦄, i ≠ j → (1 : ℝ) ≤ dist (x i) (x j)

noncomputable def contactPairs {n : ℕ} (x : Fin n → Point) : Finset (Fin n × Fin n) := by
  classical
  exact (Finset.univ.product Finset.univ).filter fun ij =>
    ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1

def contactCount {n : ℕ} (x : Fin n → Point) : ℕ :=
  (contactPairs x).card

def Attainable (n k : ℕ) : Prop :=
  ∃ x : Fin n → Point, OneSeparated x ∧ contactCount x = k

noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (Attainable n) (Nat.choose n 2)

def harborthReal (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

noncomputable def harborthNat (n : ℕ) : ℕ :=
  Int.toNat (⌊harborthReal n⌋ : ℤ)

end HarborthF2
