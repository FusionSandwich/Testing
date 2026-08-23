import Mathlib.Analysis.Complex.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Nat.Find
import Mathlib.Tactic

/-!
# The planar contact-number problem

We identify `ℝ²` with `ℂ`; the metric and norm on `ℂ` are the ordinary Euclidean
metric and norm. All finite configurations in the final theorem are functions
`Fin n → Point`, so repetitions are not hidden by a finite-set quotient.
-/

namespace Harborth

/-- The Euclidean plane, represented by the complex numbers. -/
abbrev Point := ℂ

/-- Unordered index pairs, represented by the unique ordering `i < j`. -/
def pairFinset (n : ℕ) : Finset (Fin n × Fin n) :=
  (Finset.univ.product Finset.univ).filter fun ij => ij.1 < ij.2

/-- The set of pairs at Euclidean distance exactly one. -/
noncomputable def contactPairs {n : ℕ} (x : Fin n → Point) : Finset (Fin n × Fin n) :=
  (pairFinset n).filter fun ij => dist (x ij.1) (x ij.2) = 1

/-- The number of contacts in a labelled finite configuration. -/
noncomputable def contactCount {n : ℕ} (x : Fin n → Point) : ℕ :=
  (contactPairs x).card

/-- A configuration is one-separated when distinct labelled points have distance at least one. -/
def OneSeparated {n : ℕ} (x : Fin n → Point) : Prop :=
  ∀ ⦃i j : Fin n⦄, i ≠ j → 1 ≤ dist (x i) (x j)

/-- `m` is a contact number realized by an actual one-separated `n`-point configuration. -/
def Realizable (n m : ℕ) : Prop :=
  ∃ x : Fin n → Point, OneSeparated x ∧ contactCount x = m

/-- The exact maximum contact number. The search bound `n*n` is deliberately
loose; `contactCount_le_square` later proves that every realizable value lies
below it. -/
noncomputable def f₂ (n : ℕ) : ℕ :=
  Nat.findGreatest (Realizable n) (n * n)

/-- The real quantity occurring under the floor in Harborth's formula. -/
noncomputable def harborthValue (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

end Harborth
