import Erdos1084

open Erdos1084

/-! Smoke tests for the Gate-D separator and calibration algebra. -/

example
    {N : ℕ}
    (bad : Finset ((Fin N × Fin N) × Fin N))
    (hits : ∀ xy : Fin N × Fin N, ∃ z : Fin N, (xy, z) ∈ bad) :
    N * N ≤ bad.card :=
  grid_separator_card bad hits

example
    {N : ℕ}
    (bad : Finset ((Fin N × Fin N) × Fin N))
    (hits : ∀ xy : Fin N × Fin N, ∃ z : Fin N, (xy, z) ∈ bad)
    {c0 M E : ℝ}
    (hc0 : 0 ≤ c0)
    (hM : 0 < M)
    (hcount : c0 * (bad.card : ℝ) ≤ M * E) :
    (c0 / M) * (N : ℝ) ^ 2 ≤ E :=
  cutset_energy_lower bad hits hc0 hM hcount

example
    {dot qnorm nunorm kappa gamma : ℝ}
    (hdot : dot ≤ qnorm * nunorm)
    (hq : qnorm ≤ kappa)
    (hnorm : nunorm ≤ 1)
    (hqnonneg : 0 ≤ qnorm)
    (hgamma : kappa ≤ gamma) :
    dot ≤ gamma :=
  calibration_inball_scalar hdot hq hnorm hqnonneg hgamma

example
    {transport₁ transport₂ phase₁ phase₂ phaseInterface
      exteriorEnergy₁ exteriorEnergy₂ interfaceEnergy : ℝ}
    (hPhaseBalance : phase₁ + phase₂ + phaseInterface = 0)
    (hExterior₁ : transport₁ + phase₁ ≤ exteriorEnergy₁)
    (hExterior₂ : transport₂ + phase₂ ≤ exteriorEnergy₂)
    (hInterface : phaseInterface ≤ interfaceEnergy) :
    transport₁ + transport₂ ≤
      exteriorEnergy₁ + exteriorEnergy₂ + interfaceEnergy :=
  two_phase_translation_calibration
    hPhaseBalance hExterior₁ hExterior₂ hInterface

example
    {bulk₁ bulk₂ exterior₁ exterior₂ interface energy : ℝ}
    (hGauss : bulk₁ + bulk₂ = exterior₁ + exterior₂ + interface)
    (hExterior₁ : exterior₁ ≤ energy)
    (hExterior₂ : exterior₂ ≤ energy)
    (hInterface : interface ≤ energy) :
    bulk₁ + bulk₂ ≤ 3 * energy :=
  two_phase_calibration_sum hGauss hExterior₁ hExterior₂ hInterface
