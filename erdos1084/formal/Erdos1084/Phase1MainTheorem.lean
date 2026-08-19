import Mathlib
import Erdos1084.Phase1ContactNumber

namespace Erdos1084

/-!
# Phase-I main theorem interface

This file isolates the remaining foundational ports of the five named geometric theorems.  A
`Phase1PublishedInput` is not an axiom declaration: it is ordinary data in the theorem signature.
Its sole field says that the named inputs construct a concrete geometric certificate for a
maximizing realization of the relational contact number.

Once such a provider is available, the strict `2.0465` theorem follows entirely inside Lean.
-/

noncomputable section

/--
Provider implemented by the five named geometric inputs and the first-contact no-isolated lemma.

A foundational formalization can replace this provider field theorem-by-theorem without changing
`phase1_main_relational`.
-/
structure Phase1PublishedInput where
  certificate_for_maximum :
    ∀ {n m : ℕ},
      2 ≤ n →
      IsThreeDimensionalContactNumber n m →
      ∃ X : UnitSeparatedConfiguration (Fin n),
        X.contactCount = m ∧ Phase1PackingCertificate X

/--
The complete Phase-I theorem in relational form.

`x` is the unique positive real with `x³=n²`; hence it is the real `n^(2/3)` scale.  The conclusion
uses the exact rational clean coefficient `kpClean = 4093/2000 = 2.0465`.
-/
theorem phase1_main_relational
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    ∃ x : ℝ,
      KeplerPowerScale (n : ℝ) x ∧
      (m : ℝ) < 6 * (n : ℝ) - kpClean * x := by
  obtain ⟨X, hX, hcertificate⟩ :=
    geometry.certificate_for_maximum hn hmax
  exact ⟨hcertificate.scale, hcertificate.power,
    phase1_contact_number_lt_clean hmax hX hcertificate⟩

/-- The clean coefficient appearing in the final theorem is exactly `2.0465`. -/
theorem kpClean_eq_20465 :
    kpClean = (2.0465 : ℝ) := by
  norm_num [kpClean]

/-- Decimal presentation of the complete relational theorem. -/
theorem phase1_main_relational_decimal
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    ∃ x : ℝ,
      KeplerPowerScale (n : ℝ) x ∧
      (m : ℝ) < 6 * (n : ℝ) - (2.0465 : ℝ) * x := by
  obtain ⟨x, hx, hbound⟩ := phase1_main_relational geometry hn hmax
  refine ⟨x, hx, ?_⟩
  simpa [kpClean_eq_20465] using hbound

end

end Erdos1084
