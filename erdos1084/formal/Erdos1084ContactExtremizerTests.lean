import Erdos1084

open Erdos1084

/-! Smoke tests for the finite contact extremizer. -/

example (a b : ℝ) :
    dist (phase1LinePoint a) (phase1LinePoint b) = |a - b| :=
  phase1LinePoint_dist a b

example (n : ℕ) :
    AttainableContactCount n (phase1SeparatedLineConfiguration n).contactCount :=
  ⟨phase1SeparatedLineConfiguration n, rfl⟩

example (n : ℕ) : f3 n ≤ n.choose 2 :=
  f3_le_choose n

example (n : ℕ) :
    ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = f3 n :=
  exists_contact_extremizer n

example (n : ℕ) :
    (contactExtremizer n).contactCount = f3 n :=
  contactExtremizer_contactCount n
