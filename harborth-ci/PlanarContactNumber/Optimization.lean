import PlanarContactNumber.Definitions

namespace PlanarContactNumber

/-- Every realized contact count satisfies the search bound used to define `f₂`. -/
theorem realizedContactNumber_le_square {n k : ℕ}
    (hk : RealizedContactNumber n k) : k ≤ n * n := by
  rcases hk with ⟨x, _, rfl⟩
  exact contactNumber_le_square x

/-- As soon as one contact count is realized, the bounded maximum defining `f₂`
is itself realized. -/
theorem f₂_realized_of_realized {n k : ℕ}
    (hk : RealizedContactNumber n k) : RealizedContactNumber n (f₂ n) := by
  classical
  unfold f₂
  exact Nat.findGreatest_spec (realizedContactNumber_le_square hk) hk

/-- Optimization bridge: a realized value that bounds every realized value is
exactly the maximum `f₂`. The eventual exact theorem will discharge both
hypotheses by the explicit triangular-lattice construction and the geometric
Harborth upper bound; no geometric statement is hidden in this lemma. -/
theorem f₂_eq_of_realized_of_upper {n c : ℕ}
    (hc : RealizedContactNumber n c)
    (hupper : ∀ {k : ℕ}, RealizedContactNumber n k → k ≤ c) :
    f₂ n = c := by
  apply Nat.le_antisymm
  · exact hupper (f₂_realized_of_realized hc)
  · exact realized_le_f₂ hc

end PlanarContactNumber
