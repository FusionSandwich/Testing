import AFPBarrier.ExplicitEulerTransport
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

/-!
# Heat-kernel forward scattering and its Fokker--Planck limit

For a spherical heat-kernel scattering step of width `tau`, a Laplace--Beltrami
mode with nonnegative decay `lam` has scattering moment

  mu = exp (-tau * lam).

The corresponding continuous-time Boltzmann collision generator

  (K_tau - I) / tau

has modal decay

  beta_tau(lam) = (1 - exp (-tau * lam)) / tau.

This file verifies the basic comparison needed by the Gate 6 benchmark:

* the scattering moment lies in `[0,1]`;
* the Boltzmann modal decay is nonnegative;
* `beta_tau(lam) <= lam`, so the finite-width scattering model decays each
  nonconstant heat mode no faster than the Fokker--Planck limit;
* the Fokker--Planck modal amplitude is bounded by the finite-width Boltzmann
  modal amplitude for nonnegative time.

The sharper small-`tau` error rate is evaluated deterministically in Gate 6.
-/

namespace AFPBarrier

/-- Eigenvalue of one spherical heat-kernel scattering step. -/
def heatKernelScatterMoment (tau lam : ℝ) : ℝ :=
  Real.exp (-tau * lam)

/-- Positive decay rate of the heat-kernel Boltzmann collision generator. -/
def heatKernelBoltzmannDecay (tau lam : ℝ) : ℝ :=
  (1 - heatKernelScatterMoment tau lam) / tau

/-- A nonnegative heat mode has scattering moment at most one. -/
theorem heatKernelScatterMoment_le_one
    (tau lam : ℝ) (htau : 0 ≤ tau) (hlam : 0 ≤ lam) :
    heatKernelScatterMoment tau lam ≤ 1 := by
  unfold heatKernelScatterMoment
  have harg : -tau * lam ≤ 0 := by positivity
  have h := (Real.exp_le_exp).2 harg
  simpa using h

/-- Every heat-kernel scattering moment is strictly positive. -/
theorem heatKernelScatterMoment_pos (tau lam : ℝ) :
    0 < heatKernelScatterMoment tau lam := by
  unfold heatKernelScatterMoment
  exact Real.exp_pos _

/-- The affine tangent inequality for the heat-kernel moment. -/
theorem one_sub_tau_mul_le_heatKernelScatterMoment
    (tau lam : ℝ) :
    1 - tau * lam ≤ heatKernelScatterMoment tau lam := by
  unfold heatKernelScatterMoment
  have h := Real.add_one_le_exp (-tau * lam)
  nlinarith

/-- The finite-width Boltzmann modal decay is nonnegative. -/
theorem heatKernelBoltzmannDecay_nonneg
    (tau lam : ℝ) (htau : 0 < tau) (hlam : 0 ≤ lam) :
    0 ≤ heatKernelBoltzmannDecay tau lam := by
  unfold heatKernelBoltzmannDecay
  apply div_nonneg
  · exact sub_nonneg.mpr (heatKernelScatterMoment_le_one tau lam htau.le hlam)
  · exact htau.le

/-- A finite-width heat-kernel collision mode decays no faster than its
Fokker--Planck limit. -/
theorem heatKernelBoltzmannDecay_le_fp
    (tau lam : ℝ) (htau : 0 < tau) :
    heatKernelBoltzmannDecay tau lam ≤ lam := by
  unfold heatKernelBoltzmannDecay
  apply (div_le_iff₀ htau).2
  have h := one_sub_tau_mul_le_heatKernelScatterMoment tau lam
  linarith

/-- For nonnegative mode decay and time, the Fokker--Planck modal amplitude is
no larger than the finite-width Boltzmann modal amplitude. -/
theorem fp_amplitude_le_heatKernelBoltzmann_amplitude
    (tau lam time : ℝ)
    (htau : 0 < tau) (hlam : 0 ≤ lam) (htime : 0 ≤ time) :
    Real.exp (-time * lam)
      ≤ Real.exp (-time * heatKernelBoltzmannDecay tau lam) := by
  apply (Real.exp_le_exp).2
  have hdecay := heatKernelBoltzmannDecay_le_fp tau lam htau
  nlinarith

end AFPBarrier
