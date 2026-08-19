import Mathlib
import Erdos1084.FiniteSpherePacking

namespace Erdos1084

/-!
# A finite-graph definition of the three-dimensional contact maximum

Only finitely many contact counts can occur on `Fin n`.  This module defines the maximum through
`Nat.findGreatest`, proves that every concrete packing lies below it, and recovers an actual
maximizing packing whenever the maximum is positive.  No compactness theorem for point
configurations is needed for existence of the discrete maximum.
-/

noncomputable section

namespace UnitSeparatedConfiguration

/-- Every contact count is bounded by the crude finite value `n²`. -/
theorem contactCount_le_card_sq {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) :
    X.contactCount ≤ n * n := by
  classical
  have hdeg : ∀ i : Fin n, X.contactDegree i ≤ n := by
    intro i
    simpa [contactDegree] using X.contactGraph.degree_le_card_verts i
  have hsum :
      (∑ i : Fin n, X.contactDegree i) ≤ ∑ _i : Fin n, n :=
    Finset.sum_le_sum fun i _ => hdeg i
  rw [X.sum_contactDegrees_eq_twice_contactCount] at hsum
  simp at hsum
  omega

/-- Attainability predicate with `0` included so the bounded search is always nonempty. -/
def IsAttainableContactCount (n k : ℕ) : Prop :=
  k = 0 ∨ ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = k

/-- Maximum contact count among all `n`-point unit-separated configurations. -/
def f3Nat (n : ℕ) : ℕ :=
  Nat.findGreatest (IsAttainableContactCount n) (n * n)

/-- Every concrete packing has contact count at most `f3Nat n`. -/
theorem contactCount_le_f3Nat {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) :
    X.contactCount ≤ f3Nat n := by
  apply Nat.le_findGreatest
  · exact X.contactCount_le_card_sq
  · exact Or.inr ⟨X, rfl⟩

/-- The formal contact maximum is itself within the crude finite bound. -/
theorem f3Nat_le_card_sq (n : ℕ) : f3Nat n ≤ n * n :=
  Nat.findGreatest_le _ _

/-- The maximum predicate is satisfied. -/
theorem f3Nat_attainable_or_zero (n : ℕ) :
    IsAttainableContactCount n (f3Nat n) := by
  apply Nat.findGreatest_spec
  exact ⟨0, Nat.zero_le _, Or.inl rfl⟩

/-- A positive maximum is attained by an actual finite packing. -/
theorem exists_contact_maximizer_of_f3Nat_pos {n : ℕ}
    (hpos : 0 < f3Nat n) :
    ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = f3Nat n := by
  rcases f3Nat_attainable_or_zero n with hzero | hreal
  · omega
  · exact hreal

/-- A packing attaining `f3Nat` dominates every other packing of the same size. -/
theorem maximal_of_contactCount_eq_f3Nat {n : ℕ}
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = f3Nat n) :
    ∀ Y : UnitSeparatedConfiguration (Fin n),
      Y.contactCount ≤ X.contactCount := by
  intro Y
  rw [hX]
  exact Y.contactCount_le_f3Nat

end UnitSeparatedConfiguration

end

end Erdos1084
