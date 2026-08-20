import Mathlib

namespace Erdos1084

/-!
# Arithmetic spine for the universal two-crack interface upper bound

A geometric vacuum-slab competitor is the disjoint union of two solid-vacuum
competitors.  This module certifies the finite normalized addition, eta
bookkeeping, and fine-state relaxation implications.
-/

/-- Normalize the sum of two finite competitor costs. -/
theorem twoCrack_normalized_additivity
    {minusCost plusCost totalCost T : ℝ}
    (hT : 0 < T)
    (htotal : totalCost ≤ minusCost + plusCost) :
    totalCost / T ^ 2 ≤ minusCost / T ^ 2 + plusCost / T ^ 2 := by
  have hT2 : 0 ≤ T ^ 2 := sq_nonneg T
  have hdiv := div_le_div_of_nonneg_right htotal hT2
  calc
    totalCost / T ^ 2
        ≤ (minusCost + plusCost) / T ^ 2 := hdiv
    _ = minusCost / T ^ 2 + plusCost / T ^ 2 := by ring

/-- Two eta-near crack competitors give a `2*eta` solid-solid upper bound. -/
theorem twoCrack_eta_upper
    {minusCost plusCost totalCost T phiMinus phiPlus eta : ℝ}
    (hT : 0 < T)
    (htotal : totalCost ≤ minusCost + plusCost)
    (hminus : minusCost / T ^ 2 ≤ phiMinus + eta)
    (hplus : plusCost / T ^ 2 ≤ phiPlus + eta) :
    totalCost / T ^ 2 ≤ phiMinus + phiPlus + 2 * eta := by
  have hadd := twoCrack_normalized_additivity hT htotal
  linarith

/-- Strict near-minimizers yield the strict finite-cell version. -/
theorem twoCrack_eta_upper_strict
    {minusCost plusCost totalCost T phiMinus phiPlus eta : ℝ}
    (hT : 0 < T)
    (htotal : totalCost ≤ minusCost + plusCost)
    (hminus : minusCost / T ^ 2 < phiMinus + eta)
    (hplus : plusCost / T ^ 2 < phiPlus + eta) :
    totalCost / T ^ 2 < phiMinus + phiPlus + 2 * eta := by
  have hadd := twoCrack_normalized_additivity hT htotal
  linarith

/--
Abstract relaxed-infimum implication: one admissible solid-solid competitor whose
cost is at most the two selected crack costs gives the corresponding upper bound.
-/
theorem relaxedInterface_le_selectedCracks
    {gamma selectedMinus selectedPlus : ℝ}
    (hcompetitor : gamma ≤ selectedMinus + selectedPlus) :
    gamma ≤ selectedMinus + selectedPlus :=
  hcompetitor

/-- Independent upper bounds on the selected crack costs give the relaxed sum bound. -/
theorem relaxedInterface_le_twoCracks
    {gamma selectedMinus selectedPlus phiMinus phiPlus : ℝ}
    (hcompetitor : gamma ≤ selectedMinus + selectedPlus)
    (hminus : selectedMinus ≤ phiMinus)
    (hplus : selectedPlus ≤ phiPlus) :
    gamma ≤ phiMinus + phiPlus := by
  linarith

/-- Epsilon form used when each selected fine state is only near its relaxed infimum. -/
theorem relaxedInterface_le_twoCracks_add_epsilon
    {gamma selectedMinus selectedPlus phiMinus phiPlus eta : ℝ}
    (hcompetitor : gamma ≤ selectedMinus + selectedPlus)
    (hminus : selectedMinus ≤ phiMinus + eta)
    (hplus : selectedPlus ≤ phiPlus + eta) :
    gamma ≤ phiMinus + phiPlus + 2 * eta := by
  linarith

end Erdos1084
