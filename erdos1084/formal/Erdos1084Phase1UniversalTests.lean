import Erdos1084.Phase1UniversalTheorem

open Erdos1084

example
    (H : UnitSeparatedConfiguration.Phase1NamedInputPackage)
    (n : ℕ) (hn : 2 ≤ n) :
    (UnitSeparatedConfiguration.f3Nat n : ℝ) <
      6 * (n : ℝ) -
        ((4093 : ℝ) / 2000) * (H.certify n hn).geometry.x :=
  UnitSeparatedConfiguration.phase1_universal_20465 H n hn
