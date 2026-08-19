import Mathlib
import Erdos1084.Phase1ContactNumber

namespace Erdos1084

/-!
# Existence of the finite three-dimensional contact number

The set of possible contact counts is nonempty and finite.  This file constructs a canonical
maximum and proves that it satisfies `IsThreeDimensionalContactNumber` for every `n`.
-/

noncomputable section

/-- An explicit line configuration, used only to prove nonemptiness of the configuration class. -/
def linePoint {n : ℕ} (i : Fin n) : Point3 :=
  fun j : Fin 3 => if j = 0 then 2 * (i.val : ℝ) else 0

/-- The explicit line configuration is unit-separated. -/
def lineConfiguration (n : ℕ) : UnitSeparatedConfiguration (Fin n) where
  point := linePoint
  separated := by
    intro i j hij
    have hval : i.val ≠ j.val := by
      intro h
      apply hij
      exact Fin.ext h
    have hnat : 1 ≤ Nat.dist i.val j.val := Nat.one_le_iff_ne.mpr hval
    have habs : (1 : ℝ) ≤ |(i.val : ℝ) - (j.val : ℝ)| := by
      exact_mod_cast hnat
    have hcoord :
        (2 : ℝ) ≤ ‖(linePoint i - linePoint j) (0 : Fin 3)‖ := by
      simp [linePoint, Real.norm_eq_abs]
      nlinarith
    have hcoordle :
        ‖(linePoint i - linePoint j) (0 : Fin 3)‖ ≤
          ‖linePoint i - linePoint j‖ :=
      norm_apply_le_norm (linePoint i - linePoint j) 0
    rw [dist_eq_norm]
    linarith

/-- Every simple contact graph has fewer edges than the successor of the ambient `Sym2` cardinal. -/
theorem contactCount_lt_sym2_card_succ
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    X.contactCount < Fintype.card (Sym2 (Fin n)) + 1 := by
  classical
  apply Nat.lt_succ_of_le
  unfold UnitSeparatedConfiguration.contactCount
  exact Finset.card_le_univ_card

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
