import Mathlib
import Erdos1084.Phase1CertifiedTheorem

namespace Erdos1084

/-!
# Universal Phase-I `2.0465` theorem

The package supplies, for every `n ≥ 2`, a contact-maximizing packing and the five named geometric
conclusions at that maximizer.  Lean then proves the advertised bound for every competing
`n`-point packing.  This is equivalent to the usual statement for `f₃(n)` without requiring a
separate set-theoretic supremum definition in the final theorem.
-/

noncomputable section

namespace UnitSeparatedConfiguration

/-- Maximizing packing plus named geometric inputs at every cardinality `n ≥ 2`. -/
structure Phase1UniversalCertificate where
  packing : ∀ n : ℕ, 2 ≤ n → UnitSeparatedConfiguration (Fin n)
  geometry : ∀ n : ℕ, ∀ hn : 2 ≤ n,
    (packing n hn).Phase1PublishedInputCertificate
  maximal : ∀ n : ℕ, ∀ hn : 2 ≤ n,
    ∀ Y : UnitSeparatedConfiguration (Fin n),
      Y.contactCount ≤ (packing n hn).contactCount

/-- `kpClean` is exactly the clean decimal coefficient `2.0465`. -/
theorem kpClean_eq_20465 : kpClean = (4093 : ℝ) / 2000 := by
  rfl

/-- Universal Phase-I theorem for every finite packing of cardinality `n ≥ 2`. -/
theorem phase1_universal_contact_bound
    (H : Phase1UniversalCertificate)
    (n : ℕ) (hn : 2 ≤ n)
    (Y : UnitSeparatedConfiguration (Fin n)) :
    (Y.contactCount : ℝ) <
      6 * (n : ℝ) - ((4093 : ℝ) / 2000) * (H.geometry n hn).x := by
  have hmaxNat := H.maximal n hn Y
  have hmaxReal :
      (Y.contactCount : ℝ) ≤ ((H.packing n hn).contactCount : ℝ) := by
    exact_mod_cast hmaxNat
  have hmain :=
    (H.packing n hn).phase1_published_inputs_contact_bound (H.geometry n hn)
  rw [kpClean_eq_20465] at hmain
  exact lt_of_le_of_lt hmaxReal hmain

/-- Equivalent universal deficit form. -/
theorem phase1_universal_deficit_bound
    (H : Phase1UniversalCertificate)
    (n : ℕ) (hn : 2 ≤ n)
    (Y : UnitSeparatedConfiguration (Fin n)) :
    ((4093 : ℝ) / 2000) * (H.geometry n hn).x <
      6 * (n : ℝ) - (Y.contactCount : ℝ) := by
  linarith [phase1_universal_contact_bound H n hn Y]

end UnitSeparatedConfiguration

end

end Erdos1084
