import Mathlib
import Erdos1084.Phase1ContactNumber

namespace Erdos1084

/-!
# Existence of the finite three-dimensional contact number

The set of possible contact counts is nonempty and finite. This file constructs a canonical
maximum and proves that it satisfies `IsThreeDimensionalContactNumber` for every `n`.
-/

noncomputable section

/-- An explicit line configuration, used only to prove nonemptiness of the configuration class. -/
def linePoint {n : ℕ} (i : Fin n) : Point3 :=
  !₂[2 * (i.val : ℝ), 0, 0]

/-- Squared distance in the explicit line configuration. -/
theorem linePoint_dist_sq {n : ℕ} (i j : Fin n) :
    dist (linePoint i) (linePoint j) ^ 2 =
      (2 * (i.val : ℝ) - 2 * (j.val : ℝ)) ^ 2 := by
  rw [EuclideanSpace.dist_sq_eq]
  norm_num [linePoint, Real.dist_eq]

/-- The explicit line configuration is unit-separated. -/
def lineConfiguration (n : ℕ) : UnitSeparatedConfiguration (Fin n) where
  point := linePoint
  separated := by
    intro i j hij
    have hval : i.val ≠ j.val := by
      intro h
      apply hij
      exact Fin.ext h
    have hdiffSq :
        (1 : ℝ) ≤ (2 * (i.val : ℝ) - 2 * (j.val : ℝ)) ^ 2 := by
      rcases lt_or_gt_of_ne hval with hijlt | hjilt
      · have hnat : i.val + 1 ≤ j.val := Nat.succ_le_iff.mpr hijlt
        have hreal : (i.val : ℝ) + 1 ≤ (j.val : ℝ) := by
          exact_mod_cast hnat
        nlinarith
      · have hnat : j.val + 1 ≤ i.val := Nat.succ_le_iff.mpr hjilt
        have hreal : (j.val : ℝ) + 1 ≤ (i.val : ℝ) := by
          exact_mod_cast hnat
        nlinarith
    have hsq := linePoint_dist_sq i j
    have hdist0 : 0 ≤ dist (linePoint i) (linePoint j) := dist_nonneg
    nlinarith

/-- Every simple contact graph has fewer edges than the successor of the ambient `Sym2` cardinal. -/
theorem contactCount_lt_sym2_card_succ
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    X.contactCount < Fintype.card (Sym2 (Fin n)) + 1 := by
  classical
  apply Nat.lt_succ_of_le
  have hle :
      X.contactGraph.edgeFinset.card ≤
        (Finset.univ : Finset (Sym2 (Fin n))).card :=
    Finset.card_le_card (Finset.subset_univ _)
  simpa [UnitSeparatedConfiguration.contactCount] using hle

/-- Finite set of all attainable contact counts for `n` labelled points. -/
noncomputable def attainableContactCounts (n : ℕ) : Finset ℕ := by
  classical
  exact (Finset.range (Fintype.card (Sym2 (Fin n)) + 1)).filter
    (fun m => ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = m)

/-- The attainable contact-count set is nonempty. -/
theorem attainableContactCounts_nonempty (n : ℕ) :
    (attainableContactCounts n).Nonempty := by
  classical
  let X := lineConfiguration n
  refine ⟨X.contactCount, ?_⟩
  simp [attainableContactCounts, contactCount_lt_sym2_card_succ X, X]

/-- Canonical maximum number of contacts among `n` unit-separated points in `R^3`. -/
noncomputable def contactNumber3 (n : ℕ) : ℕ :=
  (attainableContactCounts n).max' (attainableContactCounts_nonempty n)

/-- The canonical contact number is itself attainable. -/
theorem contactNumber3_mem (n : ℕ) :
    contactNumber3 n ∈ attainableContactCounts n := by
  exact Finset.max'_mem _ _

/-- The canonical value satisfies the relational definition of `f₃(n)`. -/
theorem contactNumber3_isMaximum (n : ℕ) :
    IsThreeDimensionalContactNumber n (contactNumber3 n) := by
  classical
  constructor
  · have hmem := contactNumber3_mem n
    simp [attainableContactCounts] at hmem
    exact hmem.2
  · intro X
    apply Finset.le_max' (attainableContactCounts n)
    simp [attainableContactCounts, contactCount_lt_sym2_card_succ X]

/-- A maximizing realization exists for every `n`. -/
theorem exists_contactNumber3_realizer (n : ℕ) :
    ∃ X : UnitSeparatedConfiguration (Fin n),
      X.contactCount = contactNumber3 n :=
  (contactNumber3_isMaximum n).1

end

end Erdos1084
