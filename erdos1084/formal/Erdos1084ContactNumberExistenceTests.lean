import Erdos1084.ContactNumberExistence

open Erdos1084

/-! Smoke tests for existence of the finite three-dimensional contact number. -/

example (n : ℕ) : UnitSeparatedConfiguration (Fin n) :=
  lineConfiguration n

example (n : ℕ) :
    IsThreeDimensionalContactNumber n (contactNumber3 n) :=
  contactNumber3_isMaximum n

example (n : ℕ) :
    ∃ X : UnitSeparatedConfiguration (Fin n),
      X.contactCount = contactNumber3 n :=
  exists_contactNumber3_realizer n
