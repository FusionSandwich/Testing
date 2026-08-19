import Mathlib
import Erdos1084.Phase1EndToEnd

namespace Erdos1084

/-!
# Relational definition of the three-dimensional contact number

The analytic configuration space is uncountable, but every contact count is a natural number.
For the Phase-I theorem it is convenient to avoid making an arbitrary choice of maximizer and to
state directly what it means for `m` to be the maximum contact count among `n`-point packings.
-/

noncomputable section

/-- `m` is the maximum contact count among all unit-separated labelled `n`-point configurations. -/
def IsThreeDimensionalContactNumber (n m : ℕ) : Prop :=
  (∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = m) ∧
    ∀ X : UnitSeparatedConfiguration (Fin n), X.contactCount ≤ m

/-- The relational contact number is unique. -/
theorem IsThreeDimensionalContactNumber.unique
    {n m₁ m₂ : ℕ}
    (h₁ : IsThreeDimensionalContactNumber n m₁)
    (h₂ : IsThreeDimensionalContactNumber n m₂) :
    m₁ = m₂ := by
  obtain ⟨X₁, hX₁⟩ := h₁.1
  obtain ⟨X₂, hX₂⟩ := h₂.1
  have hle₁ : m₁ ≤ m₂ := by
    rw [← hX₁]
    exact h₂.2 X₁
  have hle₂ : m₂ ≤ m₁ := by
    rw [← hX₂]
    exact h₁.2 X₂
  omega

/-- Every realizing configuration of the contact number is a contact maximizer. -/
theorem IsThreeDimensionalContactNumber.maximal_realizer
    {n m : ℕ}
    (h : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m) :
    ∀ Y : UnitSeparatedConfiguration (Fin n),
      Y.contactCount ≤ X.contactCount := by
  intro Y
  rw [hX]
  exact h.2 Y

/--
Phase-I theorem in relational `f₃(n)` form.

The theorem takes a maximizing realization and its visible geometric certificate.  The latter is
exactly what the named published geometric inputs construct in the ordinary mathematical proof.
-/
theorem phase1_contact_number_lt_clean
    {n m : ℕ}
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m)
    (hgeom : Phase1PackingCertificate X) :
    (m : ℝ) < 6 * (n : ℝ) - kpClean * hgeom.scale := by
  rw [← hX]
  exact hgeom.contactCount_lt_clean_bound

/-- The same relational contact number satisfies the elementary `m ≤ 6n` bound. -/
theorem phase1_contact_number_le_six_card
    {n m : ℕ}
    (hmax : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m)
    (hgeom : Phase1PackingCertificate X) :
    m ≤ 6 * n := by
  rw [← hX]
  exact hgeom.contactCount_le_six_card

end

end Erdos1084
