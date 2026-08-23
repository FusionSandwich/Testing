import Harborth.Definitions

/-!
# Elementary facts about the finite maximum
-/

namespace Harborth

/-- Every contact pair is, in particular, an ordered representative of an
unordered pair of distinct indices. -/
theorem contactPairs_subset_pairFinset {n : ℕ} (x : Fin n → Point) :
    contactPairs x ⊆ pairFinset n := by
  classical
  intro ij hij
  exact (Finset.mem_filter.mp hij).1

/-- The deliberately loose square bound used in the definition of `f₂`. -/
theorem contactCount_le_square {n : ℕ} (x : Fin n → Point) :
    contactCount x ≤ n * n := by
  classical
  unfold contactCount
  calc
    (contactPairs x).card ≤ (pairFinset n).card :=
      Finset.card_le_card (contactPairs_subset_pairFinset x)
    _ ≤ ((Finset.univ : Finset (Fin n)).product Finset.univ).card := by
      exact Finset.card_le_card (Finset.filter_subset _ _)
    _ = n * n := by simp

/-- Every realizable contact count lies inside the search interval defining
`f₂`. -/
theorem Realizable.le_square {n m : ℕ} (h : Realizable n m) : m ≤ n * n := by
  rcases h with ⟨x, _hx, rfl⟩
  exact contactCount_le_square x

/-- Every realizable contact count is at most the maximum. -/
theorem Realizable.le_f₂ {n m : ℕ} (h : Realizable n m) : m ≤ f₂ n := by
  classical
  unfold f₂
  exact Nat.le_findGreatest h.le_square h

/-- To bound `f₂`, it is enough to bound every realizable contact count. -/
theorem f₂_le_of_forall_realizable_le {n b : ℕ}
    (h : ∀ m, Realizable n m → m ≤ b) : f₂ n ≤ b := by
  classical
  by_contra hnb
  have hb : b < f₂ n := Nat.lt_of_not_ge hnb
  have hf0 : f₂ n ≠ 0 := Nat.ne_of_gt (lt_of_le_of_lt (Nat.zero_le b) hb)
  have hf : Realizable n (f₂ n) := by
    unfold f₂ at hf0 ⊢
    exact Nat.findGreatest_of_ne_zero rfl hf0
  exact (Nat.not_le_of_lt hb) (h _ hf)

end Harborth
