import Mathlib

namespace Erdos1084

/-!
# Calibration-deficit reduction for the developed-multiplicity selector

A developed grain complex has one reference jump cost on each interface, while
the physical model pays its relaxed interface cost.  Their positive difference
is the calibration deficit.  This module proves the facewise inequality, finite
sum assembly, sharp lower bound with a total deficit, and the necessary
area-order deficit for every below-FCC competitor.

The geometric definitions of the developed jump, physical interface cell, and
BV multiplicity perimeter remain explicit inputs.
-/

open scoped BigOperators

/-- Positive part of the amount by which a developed jump exceeds physical cost. -/
def calibrationUnderpayment (developed physical : ℝ) : ℝ :=
  max 0 (developed - physical)

/-- The calibration underpayment is nonnegative. -/
theorem calibrationUnderpayment_nonneg (developed physical : ℝ) :
    0 ≤ calibrationUnderpayment developed physical := by
  simp [calibrationUnderpayment]

/-- Every developed jump is bounded by physical cost plus its positive shortfall. -/
theorem developed_le_physical_add_underpayment
    (developed physical : ℝ) :
    developed ≤ physical + calibrationUnderpayment developed physical := by
  unfold calibrationUnderpayment
  by_cases h : developed ≤ physical
  · have hsub : developed - physical ≤ 0 := sub_nonpos.mpr h
    simp [max_eq_left (le_of_eq rfl), hsub]
    exact h
  · have hsub : 0 ≤ developed - physical := sub_nonneg.mpr (le_of_not_ge h)
    rw [max_eq_right hsub]
    ring_nf

/-- Vanishing underpayment is equivalent to physical domination. -/
theorem calibrationUnderpayment_eq_zero_iff
    (developed physical : ℝ) :
    calibrationUnderpayment developed physical = 0 ↔ developed ≤ physical := by
  unfold calibrationUnderpayment
  constructor
  · intro h
    have hmax : max 0 (developed - physical) = 0 := h
    have hle : developed - physical ≤ 0 := by
      exact le_of_max_eq_left hmax
    linarith
  · intro h
    have hsub : developed - physical ≤ 0 := sub_nonpos.mpr h
    simp [max_eq_left (le_of_eq rfl), hsub]

/-- Finite interface sum of developed jumps is bounded by physical costs plus deficits. -/
theorem sum_developed_le_physical_add_underpayment
    {ι : Type*} (s : Finset ι)
    (developed physical : ι → ℝ) :
    (∑ i ∈ s, developed i) ≤
      (∑ i ∈ s, physical i) +
        ∑ i ∈ s, calibrationUnderpayment (developed i) (physical i) := by
  calc
    (∑ i ∈ s, developed i) ≤
        ∑ i ∈ s, (physical i +
          calibrationUnderpayment (developed i) (physical i)) := by
      exact Finset.sum_le_sum fun i hi =>
        developed_le_physical_add_underpayment (developed i) (physical i)
    _ = (∑ i ∈ s, physical i) +
        ∑ i ∈ s, calibrationUnderpayment (developed i) (physical i) := by
      simp [Finset.sum_add_distrib]

/--
If developed perimeter is bounded by exterior plus developed jumps, and physical
energy equals exterior plus physical interface costs, then developed perimeter
is bounded by physical energy plus the total calibration deficit.
-/
theorem developedPerimeter_le_physicalEnergy_add_deficit
    {ι : Type*} (s : Finset ι)
    (developed physical : ι → ℝ)
    {exterior developedPerimeter physicalEnergy : ℝ}
    (hdeveloped : developedPerimeter ≤ exterior + ∑ i ∈ s, developed i)
    (hphysical : physicalEnergy = exterior + ∑ i ∈ s, physical i) :
    developedPerimeter ≤ physicalEnergy +
      ∑ i ∈ s, calibrationUnderpayment (developed i) (physical i) := by
  have hsum := sum_developed_le_physical_add_underpayment s developed physical
  rw [hphysical]
  linarith

/-- Sharp Wulff lower bound minus total calibration deficit. -/
theorem physicalEnergy_ge_sharp_sub_deficit
    {sharp developedPerimeter physicalEnergy deficit : ℝ}
    (hsharp : sharp ≤ developedPerimeter)
    (hcomparison : developedPerimeter ≤ physicalEnergy + deficit) :
    sharp - deficit ≤ physicalEnergy := by
  linarith

/-- Combined finite-interface calibration-deficit selector bound. -/
theorem calibrationDeficit_selector_bound
    {ι : Type*} (s : Finset ι)
    (developed physical : ι → ℝ)
    {exterior developedPerimeter physicalEnergy sharp : ℝ}
    (hsharp : sharp ≤ developedPerimeter)
    (hdeveloped : developedPerimeter ≤ exterior + ∑ i ∈ s, developed i)
    (hphysical : physicalEnergy = exterior + ∑ i ∈ s, physical i) :
    sharp - (∑ i ∈ s,
      calibrationUnderpayment (developed i) (physical i)) ≤ physicalEnergy := by
  apply physicalEnergy_ge_sharp_sub_deficit hsharp
  exact developedPerimeter_le_physicalEnergy_add_deficit
    s developed physical hdeveloped hphysical

/-- If every physical interface dominates its developed jump, the sharp bound follows. -/
theorem calibrationDeficit_selector_sharp
    {ι : Type*} (s : Finset ι)
    (developed physical : ι → ℝ)
    {exterior developedPerimeter physicalEnergy sharp : ℝ}
    (hdomination : ∀ i ∈ s, developed i ≤ physical i)
    (hsharp : sharp ≤ developedPerimeter)
    (hdeveloped : developedPerimeter ≤ exterior + ∑ i ∈ s, developed i)
    (hphysical : physicalEnergy = exterior + ∑ i ∈ s, physical i) :
    sharp ≤ physicalEnergy := by
  have hzero :
      (∑ i ∈ s, calibrationUnderpayment (developed i) (physical i)) = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    exact (calibrationUnderpayment_eq_zero_iff (developed i) (physical i)).2
      (hdomination i hi)
  have hbound := calibrationDeficit_selector_bound
    s developed physical hsharp hdeveloped hphysical
  simpa [hzero] using hbound

/-- Every competitor below the sharp value by `gap` needs at least that much deficit. -/
theorem subsharp_implies_calibrationDeficit
    {sharp physicalEnergy deficit gap : ℝ}
    (hlower : sharp - deficit ≤ physicalEnergy)
    (hbelow : physicalEnergy ≤ sharp - gap) :
    gap ≤ deficit := by
  linarith

/-- Finite-interface form of the necessary calibration-deficit condition. -/
theorem subsharp_implies_sum_underpayment
    {ι : Type*} (s : Finset ι)
    (developed physical : ι → ℝ)
    {exterior developedPerimeter physicalEnergy sharp gap : ℝ}
    (hsharp : sharp ≤ developedPerimeter)
    (hdeveloped : developedPerimeter ≤ exterior + ∑ i ∈ s, developed i)
    (hphysical : physicalEnergy = exterior + ∑ i ∈ s, physical i)
    (hbelow : physicalEnergy ≤ sharp - gap) :
    gap ≤ ∑ i ∈ s,
      calibrationUnderpayment (developed i) (physical i) := by
  apply subsharp_implies_calibrationDeficit
    (sharp := sharp) (physicalEnergy := physicalEnergy)
  · exact calibrationDeficit_selector_bound
      s developed physical hsharp hdeveloped hphysical
  · exact hbelow

/-- Exact FCC sharp particle coefficient cube. -/
theorem calibrationDeficit_fcc_coefficient_cube :
    (27 : ℝ) * 32 * (1 / 2) = 432 := by
  norm_num

end Erdos1084
