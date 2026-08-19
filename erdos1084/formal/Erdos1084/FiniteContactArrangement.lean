import Mathlib

namespace Erdos1084

/-!
# Finite weighted contact arrangements

A tangentially periodic abrupt interface reduces to finitely many candidate
site-orbit pairs. Each candidate has a contact locus in translation space and a
nonnegative integer multiplicity. This module certifies the finite support,
weight bound, and deficit-minimization bookkeeping. Construction of the circle
and conflict-disk arrangement remains geometric.
-/

section Arrangement

variable {ι α : Type*} [DecidableEq ι]

/-- Weighted number of active exact-contact candidates at one parameter value. -/
noncomputable def weightedContactCount
    (candidates : Finset ι) (weight : ι → ℕ)
    (active : ι → α → Prop) (t : α) : ℕ := by
  classical
  exact candidates.sum fun i => if active i t then weight i else 0

/-- The finite support of all candidate contact loci. -/
def contactArrangementSupport
    (candidates : Finset ι) (active : ι → α → Prop) : Set α :=
  {t | ∃ i, i ∈ candidates ∧ active i t}

/-- Outside the finite union of contact loci, the weighted count is zero. -/
theorem weightedContactCount_eq_zero_of_not_mem_support
    (candidates : Finset ι) (weight : ι → ℕ)
    (active : ι → α → Prop) (t : α)
    (ht : t ∉ contactArrangementSupport candidates active) :
    weightedContactCount candidates weight active t = 0 := by
  classical
  have hnone : ∀ i, i ∈ candidates → ¬ active i t := by
    intro i hi hactive
    exact ht ⟨i, hi, hactive⟩
  simp [weightedContactCount, hnone]

/-- The active contact count is bounded by the total candidate weight. -/
theorem weightedContactCount_le_totalWeight
    (candidates : Finset ι) (weight : ι → ℕ)
    (active : ι → α → Prop) (t : α) :
    weightedContactCount candidates weight active t ≤ candidates.sum weight := by
  classical
  unfold weightedContactCount
  apply Finset.sum_le_sum
  intro i hi
  by_cases hactive : active i t
  · simp [hactive]
  · simp [hactive]

/-- Unweighted contact count is bounded by the number of candidates. -/
theorem contactCount_le_candidateCard
    (candidates : Finset ι) (active : ι → α → Prop) (t : α) :
    weightedContactCount candidates (fun _ => 1) active t ≤ candidates.card := by
  simpa using
    weightedContactCount_le_totalWeight candidates (fun _ => 1) active t

/-- Integer abrupt deficit after recovering `recovered` cross contacts. -/
def abruptDeficitZ (twoCrack recovered : ℕ) : ℤ :=
  (twoCrack : ℤ) - (recovered : ℤ)

/-- More recovered exact cross contacts give no larger abrupt deficit. -/
theorem abruptDeficitZ_antitone
    {twoCrack recovered₁ recovered₂ : ℕ}
    (h : recovered₁ ≤ recovered₂) :
    abruptDeficitZ twoCrack recovered₂ ≤
      abruptDeficitZ twoCrack recovered₁ := by
  have hz : (recovered₁ : ℤ) ≤ (recovered₂ : ℤ) := by
    exact_mod_cast h
  simp [abruptDeficitZ]
  linarith

/-- Maximizing the finite weighted contact count minimizes the abrupt deficit. -/
theorem abruptDeficitZ_minimized_of_count_maximized
    (candidates : Finset ι) (weight : ι → ℕ)
    (active : ι → α → Prop)
    (twoCrack : ℕ) {tMax t : α}
    (hmax : weightedContactCount candidates weight active t ≤
      weightedContactCount candidates weight active tMax) :
    abruptDeficitZ twoCrack
        (weightedContactCount candidates weight active tMax) ≤
      abruptDeficitZ twoCrack
        (weightedContactCount candidates weight active t) :=
  abruptDeficitZ_antitone hmax

/-- A total candidate-weight bound gives a corresponding abrupt-deficit lower bound. -/
theorem abruptDeficitZ_ge_twoCrack_sub_totalWeight
    (candidates : Finset ι) (weight : ι → ℕ)
    (active : ι → α → Prop) (twoCrack : ℕ) (t : α) :
    abruptDeficitZ twoCrack (candidates.sum weight) ≤
      abruptDeficitZ twoCrack
        (weightedContactCount candidates weight active t) := by
  exact abruptDeficitZ_antitone
    (weightedContactCount_le_totalWeight candidates weight active t)

end Arrangement

end Erdos1084
