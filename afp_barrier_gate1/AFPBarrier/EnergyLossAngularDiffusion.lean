import AFPBarrier.ForwardPeakedHeatKernel
import Mathlib.Tactic

/-!
# Layered charged-particle energy loss and angular diffusion

Consider a charged particle that loses energy linearly inside one homogeneous
layer,

  E(s) = E_in - stopping * s,

and whose angular Fokker--Planck coefficient is `coeff / E(s)^2`.  The exact
angular diffusion depth accumulated over thickness `x` is

  coeff * x / (E_in * (E_in - stopping * x)).

This module verifies the algebraic and positivity facts needed by the Gate 6
layered charged-particle benchmark.  It also gives an exact formula for the
change in angular depth when two layers are reversed.  Thus layer order can
change angular broadening even though the final energy is order independent.
-/

namespace AFPBarrier

noncomputable section

/-- Energy after crossing one layer with constant stopping power. -/
def energyAfterLayer (energy stopping thickness : ℝ) : ℝ :=
  energy - stopping * thickness

/-- Exact integrated angular diffusion for coefficient `coeff / E^2` under
constant linear stopping. -/
def inverseSquareAngularDepth
    (coeff energy stopping thickness : ℝ) : ℝ :=
  coeff * thickness /
    (energy * energyAfterLayer energy stopping thickness)

/-- Equivalent antiderivative form of the inverse-square angular depth. -/
theorem inverseSquareAngularDepth_eq_reciprocal_difference
    (coeff energy stopping thickness : ℝ)
    (hstop : stopping ≠ 0)
    (henergy : energy ≠ 0)
    (hout : energyAfterLayer energy stopping thickness ≠ 0) :
    inverseSquareAngularDepth coeff energy stopping thickness
      = coeff / stopping *
          (1 / energyAfterLayer energy stopping thickness - 1 / energy) := by
  unfold inverseSquareAngularDepth
  unfold energyAfterLayer at hout ⊢
  field_simp [hstop, henergy, hout]
  ring

/-- Positive input coefficient, thickness, and endpoint energies give a
nonnegative accumulated angular depth. -/
theorem inverseSquareAngularDepth_nonneg
    (coeff energy stopping thickness : ℝ)
    (hcoeff : 0 ≤ coeff) (hthickness : 0 ≤ thickness)
    (henergy : 0 < energy)
    (hout : 0 < energyAfterLayer energy stopping thickness) :
    0 ≤ inverseSquareAngularDepth coeff energy stopping thickness := by
  unfold inverseSquareAngularDepth
  apply div_nonneg
  · exact mul_nonneg hcoeff hthickness
  · exact mul_nonneg henergy.le hout.le

/-- Final energy is independent of the order of two constant-stopping layers. -/
theorem twoLayer_energy_order_invariant
    (energy stopping₁ thickness₁ stopping₂ thickness₂ : ℝ) :
    energyAfterLayer
        (energyAfterLayer energy stopping₁ thickness₁)
        stopping₂ thickness₂
      = energyAfterLayer
          (energyAfterLayer energy stopping₂ thickness₂)
          stopping₁ thickness₁ := by
  unfold energyAfterLayer
  ring

/-- Angular depth for layer 1 followed by layer 2, written using energy drops
`drop₁, drop₂` and angular numerators `amount₁, amount₂`. -/
def twoLayerAngularDepth12
    (energy amount₁ drop₁ amount₂ drop₂ : ℝ) : ℝ :=
  amount₁ / (energy * (energy - drop₁))
    + amount₂ / ((energy - drop₁) * (energy - drop₁ - drop₂))

/-- Angular depth for the reversed layer order. -/
def twoLayerAngularDepth21
    (energy amount₁ drop₁ amount₂ drop₂ : ℝ) : ℝ :=
  amount₂ / (energy * (energy - drop₂))
    + amount₁ / ((energy - drop₂) * (energy - drop₂ - drop₁))

/-- Exact layer-order difference. -/
theorem twoLayerAngularDepth_order_difference
    (energy amount₁ drop₁ amount₂ drop₂ : ℝ)
    (hE : energy ≠ 0)
    (hE1 : energy - drop₁ ≠ 0)
    (hE2 : energy - drop₂ ≠ 0)
    (hE12 : energy - drop₁ - drop₂ ≠ 0) :
    twoLayerAngularDepth12 energy amount₁ drop₁ amount₂ drop₂
      - twoLayerAngularDepth21 energy amount₁ drop₁ amount₂ drop₂
      = ((amount₁ * drop₂ - amount₂ * drop₁)
          * (drop₁ + drop₂ - 2 * energy)) /
        (energy * (energy - drop₁) * (energy - drop₂)
          * (energy - drop₁ - drop₂)) := by
  unfold twoLayerAngularDepth12 twoLayerAngularDepth21
  have hE21 : energy - drop₂ - drop₁ ≠ 0 := by
    intro hzero
    apply hE12
    linarith
  field_simp [hE, hE1, hE2, hE12, hE21]
  ring

/-- If the first layer has the larger angular-diffusion amount per energy drop,
placing it first produces no more total angular depth than placing it second. -/
theorem twoLayerAngularDepth12_le_21
    (energy amount₁ drop₁ amount₂ drop₂ : ℝ)
    (ha₁ : 0 ≤ amount₁) (ha₂ : 0 ≤ amount₂)
    (hd₁ : 0 ≤ drop₁) (hd₂ : 0 ≤ drop₂)
    (hremain : drop₁ + drop₂ < energy)
    (hratio : amount₂ * drop₁ ≤ amount₁ * drop₂) :
    twoLayerAngularDepth12 energy amount₁ drop₁ amount₂ drop₂
      ≤ twoLayerAngularDepth21 energy amount₁ drop₁ amount₂ drop₂ := by
  have hE : 0 < energy := by nlinarith
  have hE1 : 0 < energy - drop₁ := by nlinarith
  have hE2 : 0 < energy - drop₂ := by nlinarith
  have hE12 : 0 < energy - drop₁ - drop₂ := by nlinarith
  rw [sub_nonpos.symm]
  rw [twoLayerAngularDepth_order_difference
    energy amount₁ drop₁ amount₂ drop₂
    hE.ne' hE1.ne' hE2.ne' hE12.ne']
  apply div_nonpos_of_nonpos_of_nonneg
  · have hfirst : 0 ≤ amount₁ * drop₂ - amount₂ * drop₁ := by linarith
    have hsecond : drop₁ + drop₂ - 2 * energy ≤ 0 := by nlinarith
    exact mul_nonpos_of_nonneg_of_nonpos hfirst hsecond
  · positivity

/-- Modal damping composes by adding layer angular depths. -/
theorem layeredAngularAmplitude_mul
    (lam depth₁ depth₂ : ℝ) :
    Real.exp (-lam * depth₁) * Real.exp (-lam * depth₂)
      = Real.exp (-lam * (depth₁ + depth₂)) := by
  rw [← Real.exp_add]
  congr 1
  ring

end

end AFPBarrier
