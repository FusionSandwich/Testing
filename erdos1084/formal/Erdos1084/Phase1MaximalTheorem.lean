import Mathlib
import Erdos1084.Phase1CertifiedTheorem

namespace Erdos1084

/-!
# Universal Phase-I contact bound from a certified maximizer

A contact maximum exists because only finitely many simple graphs occur on `Fin n`; the remaining
geometric connected-maximizer construction is separated from the analytic surface proof.  This
module packages a maximizing finite packing and derives the clean bound for every competing
packing of the same cardinality.
-/

noncomputable section

namespace UnitSeparatedConfiguration

/-- A finite packing whose contact count dominates every packing with the same labelled size. -/
structure Phase1CertifiedMaximizer (n : ℕ) where
  packing : UnitSeparatedConfiguration (Fin n)
  maximal : ∀ Y : UnitSeparatedConfiguration (Fin n),
    Y.contactCount ≤ packing.contactCount
  geometry : packing.Phase1PublishedInputCertificate

/-- The certified maximizer satisfies the clean Phase-I bound. -/
theorem Phase1CertifiedMaximizer.maximizer_bound
    {n : ℕ} (h : Phase1CertifiedMaximizer n) :
    (h.packing.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  h.packing.phase1_published_inputs_contact_bound h.geometry

/-- Every `n`-point packing satisfies the same clean Phase-I bound. -/
theorem Phase1CertifiedMaximizer.universal_bound
    {n : ℕ} (h : Phase1CertifiedMaximizer n)
    (Y : UnitSeparatedConfiguration (Fin n)) :
    (Y.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x := by
  have hmaxNat := h.maximal Y
  have hmaxReal : (Y.contactCount : ℝ) ≤ (h.packing.contactCount : ℝ) := by
    exact_mod_cast hmaxNat
  exact lt_of_le_of_lt hmaxReal h.maximizer_bound

end UnitSeparatedConfiguration

end

end Erdos1084
