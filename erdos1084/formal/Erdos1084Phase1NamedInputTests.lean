import Erdos1084.Phase1NamedInputBuilder

open Erdos1084

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1RawF3Input n) :
    (UnitSeparatedConfiguration.f3Nat n : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  UnitSeparatedConfiguration.phase1_f3Nat_bound_of_raw_inputs h
