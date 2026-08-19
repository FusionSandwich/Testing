import Erdos1084.Phase1ContactNumber

open Erdos1084

/-! Smoke tests for the relational three-dimensional contact number. -/

example {n m₁ m₂ : ℕ}
    (h₁ : IsThreeDimensionalContactNumber n m₁)
    (h₂ : IsThreeDimensionalContactNumber n m₂) :
    m₁ = m₂ :=
  h₁.unique h₂

example {n m : ℕ}
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m)
    (hgeom : Phase1PackingCertificate X) :
    (m : ℝ) < 6 * (n : ℝ) - kpClean * hgeom.scale :=
  phase1_contact_number_lt_clean hmax hX hgeom

example {n m : ℕ}
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m)
    (hgeom : Phase1PackingCertificate X) :
    m ≤ 6 * n :=
  phase1_contact_number_le_six_card hmax hX hgeom
