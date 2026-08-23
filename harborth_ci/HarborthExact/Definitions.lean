import Mathlib

open scoped EuclideanGeometry

namespace HarborthExact

/-- The Euclidean plane. -/
abbrev Point2 := EuclideanSpace ℝ (Fin 2)

/-- A finite or infinite indexed configuration is one-separated. -/
def OneSeparated {ι : Type*} (x : ι → Point2) : Prop :=
  ∀ ⦃i j : ι⦄, i ≠ j → 1 ≤ dist (x i) (x j)

/-- The exact unit-contact graph of an indexed configuration. -/
def contactGraph {ι : Type*} (x : ι → Point2) : SimpleGraph ι where
  Adj i j := dist (x i) (x j) = 1
  symm i j hij := by simpa [dist_comm] using hij
  loopless := ⟨by
    intro i hii
    simpa using hii⟩

@[simp]
theorem contactGraph_adj {ι : Type*} (x : ι → Point2) (i j : ι) :
    (contactGraph x).Adj i j ↔ dist (x i) (x j) = 1 := by
  change (dist (x i) (x j) = 1) ↔ _
  rfl

/-- Number of unordered unit-distance pairs. -/
noncomputable def contactCount {ι : Type*} [Fintype ι] (x : ι → Point2) : ℕ :=
  (contactGraph x).edgeFinset.card

/-- An exact contact count attained by a one-separated `n`-point configuration. -/
def Achievable (n m : ℕ) : Prop :=
  ∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m

/-- The greatest attainable contact count below the universal pair bound. -/
noncomputable def f₂ (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (Achievable n) (n.choose 2)

/-- Harborth's real-valued expression. -/
noncomputable def harborthExpression (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

/-- The integer floor in the exact formula. -/
noncomputable def harborthFloor (n : ℕ) : ℤ :=
  ⌊harborthExpression n⌋

/-- The nonnegative natural-number representation of the exact candidate. -/
noncomputable def harborthValue (n : ℕ) : ℕ :=
  Int.toNat (harborthFloor n)

/-- Attainment together with a universal upper bound over actual planar configurations. -/
def IsMaximumContactNumber (n m : ℕ) : Prop :=
  (∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m) ∧
    ∀ x : Fin n → Point2, OneSeparated x → contactCount x ≤ m

end HarborthExact
