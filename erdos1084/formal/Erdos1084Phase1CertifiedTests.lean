import Erdos1084.Phase1CertifiedTheorem

open Erdos1084
open scoped BigOperators

/-! Smoke tests for the decomposed Phase-I published-input theorem. -/

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

example {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))
    (h : X.Phase1PublishedInputCertificate) :
    kpClean * h.x < 6 * (n : ℝ) - (X.contactCount : ℝ) :=
  X.phase1_published_inputs_deficit_bound h
