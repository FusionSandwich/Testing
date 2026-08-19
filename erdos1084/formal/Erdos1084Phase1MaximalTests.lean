import Erdos1084.Phase1MaximalTheorem

open Erdos1084

/-! Smoke tests for the universal Phase-I theorem from a certified maximizer. -/

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1CertifiedMaximizer n) :
    (h.packing.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  h.maximizer_bound

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1CertifiedMaximizer n)
    (Y : UnitSeparatedConfiguration (Fin n)) :
    (Y.contactCount : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  h.universal_bound Y
