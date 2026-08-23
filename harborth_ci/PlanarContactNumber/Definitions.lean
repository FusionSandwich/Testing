/-
Copyright (c) 2026 FusionSandwich. All rights reserved.
Released under the repository license.
-/
import Mathlib

/-!
# Planar contact-number definitions

This file states the optimization problem over the actual finite one-separated
configurations in the Euclidean plane. No lattice hypothesis is built into the
definition.
-/

open scoped EuclideanGeometry

namespace PlanarContactNumber

/-- The Euclidean plane used throughout the formalization. -/
abbrev Point := EuclideanSpace ℝ (Fin 2)

/-- A finite labelled configuration whose distinct points are at distance at least one. -/
def OneSeparated {n : ℕ} (x : Fin n → Point) : Prop :=
  ∀ i j, i ≠ j → (1 : ℝ) ≤ dist (x i) (x j)

/-- The unordered contact pairs, represented by their unique increasing orientation. -/
noncomputable def contactPairs {n : ℕ} (x : Fin n → Point) : Finset (Fin n × Fin n) := by
  classical
  exact Finset.univ.filter fun ij =>
    ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1

/-- The number of unit-distance pairs in a labelled configuration. -/
noncomputable def contactNumber {n : ℕ} (x : Fin n → Point) : ℕ :=
  (contactPairs x).card

/-- `k` is realized by an actual one-separated `n`-point configuration. -/
def RealizedContactNumber (n k : ℕ) : Prop :=
  ∃ x : Fin n → Point, OneSeparated x ∧ contactNumber x = k

/-- The planar contact number, as the greatest realized value below the trivial
ordered-pair bound `n*n`. -/
noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (RealizedContactNumber n) (n * n)

/-- Every contact count satisfies the trivial square bound used in `f₂`. -/
theorem contactNumber_le_square {n : ℕ} (x : Fin n → Point) :
    contactNumber x ≤ n * n := by
  classical
  unfold contactNumber contactPairs
  calc
    (Finset.univ.filter fun ij : Fin n × Fin n =>
        ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1).card
        ≤ (Finset.univ : Finset (Fin n × Fin n)).card := Finset.card_filter_le _ _
    _ = n * n := by simp

/-- Any actually realized contact count is bounded by `f₂`. -/
theorem realized_le_f₂ {n k : ℕ} (hk : RealizedContactNumber n k) : k ≤ f₂ n := by
  classical
  rcases hk with ⟨x, hxsep, hxnum⟩
  apply Nat.le_findGreatest
  · rw [← hxnum]
    exact contactNumber_le_square x
  · exact ⟨x, hxsep, hxnum⟩

end PlanarContactNumber
