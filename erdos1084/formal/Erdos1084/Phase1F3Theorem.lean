import Mathlib
import Erdos1084.Phase1ContactMaximum
import Erdos1084.Phase1CertifiedTheorem

namespace Erdos1084

/-!
# Final Phase-I theorem stated for the formal contact maximum `f3Nat`

The only remaining ordinary hypothesis is the concrete geometric certificate for one packing
that realizes the finite maximum.  The theorem conclusion is stated directly in terms of the
formal maximum, rather than the contact count of an arbitrary selected packing.
-/

noncomputable section

namespace UnitSeparatedConfiguration

/-- A realization of `f3Nat n` together with the five named Phase-I geometric inputs. -/
structure Phase1F3Certificate (n : ℕ) where
  packing : UnitSeparatedConfiguration (Fin n)
  realizes : packing.contactCount = f3Nat n
  geometry : packing.Phase1PublishedInputCertificate

/-- The formal three-dimensional contact maximum satisfies the clean Phase-I bound. -/
theorem phase1_f3Nat_bound {n : ℕ}
    (h : Phase1F3Certificate n) :
    (f3Nat n : ℝ) < 6 * (n : ℝ) - kpClean * h.geometry.x := by
  rw [← h.realizes]
  exact h.packing.phase1_published_inputs_contact_bound h.geometry

/-- Equivalent normalized-deficit form. -/
theorem phase1_f3Nat_deficit_bound {n : ℕ}
    (h : Phase1F3Certificate n) :
    kpClean * h.geometry.x < 6 * (n : ℝ) - (f3Nat n : ℝ) := by
  linarith [phase1_f3Nat_bound h]

end UnitSeparatedConfiguration

end

end Erdos1084
