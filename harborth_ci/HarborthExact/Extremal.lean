import HarborthExact.Definitions

namespace HarborthExact

/-- Every contact graph has at most all unordered pairs as edges. -/
theorem contactCount_le_choose {ι : Type*} [Fintype ι] (x : ι → Point2) :
    contactCount x ≤ (Fintype.card ι).choose 2 := by
  classical
  simpa [contactCount] using (contactGraph x).card_edgeFinset_le_card_choose_two

/-- An attained universal upper bound is the value selected by `f₂`. -/
theorem f₂_eq_of_isMaximum {n m : ℕ} (h : IsMaximumContactNumber n m) : f₂ n = m := by
  rcases h with ⟨⟨x, hxSep, hxCount⟩, hUpper⟩
  have hmBound : m ≤ n.choose 2 := by
    rw [← hxCount]
    simpa using contactCount_le_choose x
  apply le_antisymm
  · have hAch : Achievable n (f₂ n) := by
      unfold f₂
      exact Nat.findGreatest_spec hmBound ⟨x, hxSep, hxCount⟩
    rcases hAch with ⟨y, hySep, hyCount⟩
    simpa [hyCount] using hUpper y hySep
  · unfold f₂
    exact Nat.le_findGreatest hmBound ⟨x, hxSep, hxCount⟩

end HarborthExact
