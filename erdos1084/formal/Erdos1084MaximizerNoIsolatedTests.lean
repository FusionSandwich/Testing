import Erdos1084.MaximizerNoIsolated

open Erdos1084

/-! Smoke tests for the no-isolated-vertex theorem. -/

example {n m : ℕ} (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m) :
    ∀ i, ¬IsContactIsolated X i :=
  no_isolated_of_contact_maximizer hn hmax hX

example {n m : ℕ} (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m) :
    ∀ i, 1 ≤ X.contactDegree i :=
  contactDegree_pos_of_maximizer hn hmax hX
