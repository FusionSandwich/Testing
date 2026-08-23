import Mathlib

open scoped EuclideanGeometry

namespace PlanarContactNumber

abbrev Point := EuclideanSpace ℝ (Fin 2)

def OneSeparated {n : ℕ} (x : Fin n → Point) : Prop :=
  ∀ i j, i ≠ j → (1 : ℝ) ≤ dist (x i) (x j)

noncomputable def contactPairs {n : ℕ} (x : Fin n → Point) : Finset (Fin n × Fin n) := by
  classical
  exact Finset.univ.filter fun ij =>
    ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1

noncomputable def contactNumber {n : ℕ} (x : Fin n → Point) : ℕ :=
  (contactPairs x).card

def RealizedContactNumber (n k : ℕ) : Prop :=
  ∃ x : Fin n → Point, OneSeparated x ∧ contactNumber x = k

noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (RealizedContactNumber n) (n * n)

theorem contactNumber_le_square {n : ℕ} (x : Fin n → Point) :
    contactNumber x ≤ n * n := by
  classical
  unfold contactNumber contactPairs
  calc
    (Finset.univ.filter fun ij : Fin n × Fin n =>
        ij.1 < ij.2 ∧ dist (x ij.1) (x ij.2) = 1).card
        ≤ (Finset.univ : Finset (Fin n × Fin n)).card := Finset.card_filter_le _ _
    _ = n * n := by simp

theorem realized_le_f₂ {n k : ℕ} (hk : RealizedContactNumber n k) : k ≤ f₂ n := by
  classical
  rcases hk with ⟨x, hxsep, hxnum⟩
  apply Nat.le_findGreatest
  · rw [← hxnum]
    exact contactNumber_le_square x
  · exact ⟨x, hxsep, hxnum⟩

end PlanarContactNumber
