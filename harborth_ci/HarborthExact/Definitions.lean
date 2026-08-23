import Mathlib

open scoped EuclideanGeometry

namespace HarborthExact

abbrev Point2 := EuclideanSpace ℝ (Fin 2)

def OneSeparated {ι : Type*} (x : ι → Point2) : Prop :=
  ∀ ⦃i j : ι⦄, i ≠ j → 1 ≤ dist (x i) (x j)

noncomputable def contactGraph {ι : Type*} (x : ι → Point2) : SimpleGraph ι where
  Adj i j := dist (x i) (x j) = 1
  symm i j hij := by simpa [dist_comm] using hij
  loopless i := by simp

@[simp]
theorem contactGraph_adj {ι : Type*} (x : ι → Point2) (i j : ι) :
    (contactGraph x).Adj i j ↔ dist (x i) (x j) = 1 :=
  Iff.rfl

noncomputable def contactCount {ι : Type*} [Fintype ι] (x : ι → Point2) : ℕ :=
  (contactGraph x).edgeFinset.card

def Achievable (n m : ℕ) : Prop :=
  ∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m

noncomputable def f₂ (n : ℕ) : ℕ :=
  Nat.findGreatest (Achievable n) (n.choose 2)

def harborthExpression (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

def harborthFloor (n : ℕ) : ℤ :=
  ⌊harborthExpression n⌋

def harborthValue (n : ℕ) : ℕ :=
  Int.toNat (harborthFloor n)

def IsMaximumContactNumber (n m : ℕ) : Prop :=
  (∃ x : Fin n → Point2, OneSeparated x ∧ contactCount x = m) ∧
    ∀ x : Fin n → Point2, OneSeparated x → contactCount x ≤ m

end HarborthExact
