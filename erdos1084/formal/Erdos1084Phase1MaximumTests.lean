import Erdos1084.Phase1ContactMaximum

open Erdos1084

/-! Smoke tests for the finite definition of `f₃(n)`. -/

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    X.contactCount ≤ UnitSeparatedConfiguration.f3Nat n :=
  X.contactCount_le_f3Nat

example {n : ℕ}
    (hpos : 0 < UnitSeparatedConfiguration.f3Nat n) :
    ∃ X : UnitSeparatedConfiguration (Fin n),
      X.contactCount = UnitSeparatedConfiguration.f3Nat n :=
  UnitSeparatedConfiguration.exists_contact_maximizer_of_f3Nat_pos hpos
