import Mathlib
import Erdos1084.Phase1DecimalTheorem

namespace Erdos1084

/-!
# Universal Phase-I theorem relative to the named published input package

A foundational port of each large external theorem will construct `Phase1NamedInputPackage`.
Once such a package is available, the advertised theorem for every `n ≥ 2` is a closed Lean
consequence with no further geometric or combinatorial argument.
-/

noncomputable section

namespace UnitSeparatedConfiguration

/--
The five named geometric inputs, including the elementary maximizing-packing reduction, packaged
at exactly the specialization needed by Phase I.

A value of this structure is not a project axiom: it is an ordinary theorem argument whose full
construction remains visible in the final signature.
-/
structure Phase1NamedInputPackage where
  certify : ∀ n : ℕ, 2 ≤ n → Phase1F3Certificate n

/-- Final universal `2.0465` theorem in the positive-cube-root normalization. -/
theorem phase1_universal_20465
    (H : Phase1NamedInputPackage) (n : ℕ) (hn : 2 ≤ n) :
    (f3Nat n : ℝ) <
      6 * (n : ℝ) - ((4093 : ℝ) / 2000) * (H.certify n hn).geometry.x :=
  phase1_f3Nat_bound_20465 (H.certify n hn)

/-- Equivalent universal deficit form. -/
theorem phase1_universal_deficit_20465
    (H : Phase1NamedInputPackage) (n : ℕ) (hn : 2 ≤ n) :
    ((4093 : ℝ) / 2000) * (H.certify n hn).geometry.x <
      6 * (n : ℝ) - (f3Nat n : ℝ) :=
  phase1_f3Nat_deficit_bound_20465 (H.certify n hn)

end UnitSeparatedConfiguration

end

end Erdos1084
