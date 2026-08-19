import Mathlib

namespace Erdos1084

/-!
# Gate-D combinatorial and algebraic core

This module verifies the finite-grid separator theorem and the exact energy-gap algebra used in the
orientation-interface coercivity proof. The Barlow crystallization radius, assignment of
orientations to zero-energy blocks, and geometric interface cell formula remain explicit external
inputs in the mathematical dossier; they are not introduced as Lean axioms.
-/

/-- A set meeting every vertical column of an `N × N × N` grid has at least `N²` cells. -/
theorem grid_separator_card
    {N : ℕ}
    (bad : Finset ((Fin N × Fin N) × Fin N))
    (hits : ∀ xy : Fin N × Fin N, ∃ z : Fin N, (xy, z) ∈ bad) :
    N * N ≤ bad.card := by
  classical
  let chooseCell : Fin N × Fin N → {q // q ∈ bad} := fun xy =>
    ⟨(xy, Classical.choose (hits xy)), Classical.choose_spec (hits xy)⟩
  have hinj : Function.Injective chooseCell := by
    intro x y hxy
    have hval : (chooseCell x).1 = (chooseCell y).1 :=
      congrArg Subtype.val hxy
    exact congrArg Prod.fst hval
  have hcard := Fintype.card_le_of_injective chooseCell hinj
  simpa using hcard

/--
Energy lower bound obtained from the separator cardinality and bounded overlap.

`c0` is the positive energy gap, `M` the overlap multiplicity, and `E` the total energy.
-/
theorem cutset_energy_lower
    {N : ℕ}
    (bad : Finset ((Fin N × Fin N) × Fin N))
    (hits : ∀ xy : Fin N × Fin N, ∃ z : Fin N, (xy, z) ∈ bad)
    {c0 M E : ℝ}
    (hc0 : 0 ≤ c0)
    (hM : 0 < M)
    (hcount : c0 * (bad.card : ℝ) ≤ M * E) :
    (c0 / M) * (N : ℝ) ^ 2 ≤ E := by
  have hnat : N * N ≤ bad.card := grid_separator_card bad hits
  have hnatPow : N ^ 2 ≤ bad.card := by
    simpa [pow_two] using hnat
  have hreal : (N : ℝ) ^ 2 ≤ (bad.card : ℝ) := by
    exact_mod_cast hnatPow
  have hgap : c0 * (N : ℝ) ^ 2 ≤ c0 * (bad.card : ℝ) :=
    mul_le_mul_of_nonneg_left hreal hc0
  have htotal : c0 * (N : ℝ) ^ 2 ≤ M * E :=
    le_trans hgap hcount
  have htotal' : c0 * (N : ℝ) ^ 2 ≤ E * M := by
    simpa [mul_comm] using htotal
  have htarget : (c0 * (N : ℝ) ^ 2) / M ≤ E :=
    (div_le_iff₀ hM).2 htotal'
  calc
    (c0 / M) * (N : ℝ) ^ 2 = (c0 * (N : ℝ) ^ 2) / M := by
      ring
    _ ≤ E := htarget

/-- Scalar inball implication used for interface calibration bodies. -/
theorem calibration_inball_scalar
    {dot qnorm nunorm kappa gamma : ℝ}
    (hdot : dot ≤ qnorm * nunorm)
    (hq : qnorm ≤ kappa)
    (hnorm : nunorm ≤ 1)
    (hqnonneg : 0 ≤ qnorm)
    (hgamma : kappa ≤ gamma) :
    dot ≤ gamma := by
  have hqn : qnorm * nunorm ≤ kappa := by
    calc
      qnorm * nunorm ≤ qnorm * 1 :=
        mul_le_mul_of_nonneg_left hnorm hqnonneg
      _ = qnorm := by ring
      _ ≤ kappa := hq
  exact le_trans (le_trans hdot hqn) hgamma

/--
Exact two-phase cancellation of the constant phase translations in a common calibration.
-/
theorem two_phase_translation_calibration
    {transport₁ transport₂ phase₁ phase₂ phaseInterface
      exteriorEnergy₁ exteriorEnergy₂ interfaceEnergy : ℝ}
    (hPhaseBalance : phase₁ + phase₂ + phaseInterface = 0)
    (hExterior₁ : transport₁ + phase₁ ≤ exteriorEnergy₁)
    (hExterior₂ : transport₂ + phase₂ ≤ exteriorEnergy₂)
    (hInterface : phaseInterface ≤ interfaceEnergy) :
    transport₁ + transport₂ ≤
      exteriorEnergy₁ + exteriorEnergy₂ + interfaceEnergy := by
  linarith

/-- A simple aggregate form of the same calibration algebra. -/
theorem two_phase_calibration_sum
    {bulk₁ bulk₂ exterior₁ exterior₂ interface energy : ℝ}
    (hGauss : bulk₁ + bulk₂ = exterior₁ + exterior₂ + interface)
    (hExterior₁ : exterior₁ ≤ energy)
    (hExterior₂ : exterior₂ ≤ energy)
    (hInterface : interface ≤ energy) :
    bulk₁ + bulk₂ ≤ 3 * energy := by
  rw [hGauss]
  linarith

end Erdos1084
