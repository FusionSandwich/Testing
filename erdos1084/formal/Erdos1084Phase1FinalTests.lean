import Erdos1084

open Erdos1084
open scoped BigOperators

/-! Smoke tests for the clean Phase-I theorem stack. -/

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    (∑ i : Fin n, X.realContactDegree i) = 2 * (X.contactCount : ℝ) :=
  X.sum_realContactDegree_eq_twice_contactCount

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))
    (h : X.Phase1LocalCapCertificate) (i : Fin n) :
    h.exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ)) :=
  X.phase1_local_degree_charge h i

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))
    (h : X.Phase1PublishedInputCertificate) :
    (X.contactCount : ℝ) < 6 * (n : ℝ) - kpClean * h.x :=
  X.phase1_published_inputs_contact_bound h

example
    (H : UnitSeparatedConfiguration.Phase1UniversalCertificate)
    (n : ℕ) (hn : 2 ≤ n)
    (Y : UnitSeparatedConfiguration (Fin n)) :
    (Y.contactCount : ℝ) <
      6 * (n : ℝ) - ((4093 : ℝ) / 2000) * (H.geometry n hn).x :=
  UnitSeparatedConfiguration.phase1_universal_contact_bound H n hn Y
