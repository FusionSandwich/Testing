import Mathlib
import Mathlib.Combinatorics.SimpleGraph.DegreeSum

namespace Erdos1084

/-!
# Finite three-dimensional contact packings

This file begins the end-to-end formal model of Erdős Problem 1084.  It defines finite
minimum-separation configurations, their contact graphs, contact counts, and the contact deficit.
The definitions are stated directly in Euclidean three-space rather than through abstract surface
hypotheses.
-/

noncomputable section

open scoped BigOperators

/-- Euclidean three-space in mathlib's finite-coordinate model. -/
abbrev Point3 := EuclideanSpace ℝ (Fin 3)

/-- A labelled finite configuration whose pairwise distances are at least one. -/
structure UnitSeparatedConfiguration (ι : Type*) where
  point : ι → Point3
  separated : ∀ ⦃i j : ι⦄, i ≠ j → 1 ≤ dist (point i) (point j)

namespace UnitSeparatedConfiguration

variable {ι : Type*} (X : UnitSeparatedConfiguration ι)

/-- The contact graph: two distinct labels are adjacent exactly at distance one. -/
def contactGraph : SimpleGraph ι where
  Adj i j := i ≠ j ∧ dist (X.point i) (X.point j) = 1
  symm := by
    intro i j hij
    exact ⟨hij.1.symm, by simpa [dist_comm] using hij.2⟩
  loopless := by
    intro i hii
    exact hii.1 rfl

@[simp] theorem contactGraph_adj (i j : ι) :
    X.contactGraph.Adj i j ↔
      i ≠ j ∧ dist (X.point i) (X.point j) = 1 :=
  Iff.rfl

/-- A contact edge always satisfies the packing separation inequality with equality. -/
theorem dist_eq_one_of_adj {i j : ι} (h : X.contactGraph.Adj i j) :
    dist (X.point i) (X.point j) = 1 :=
  h.2

/-- Distinct non-contacting labels are strictly farther than one. -/
theorem one_lt_dist_of_not_adj {i j : ι}
    (hne : i ≠ j) (hnot : ¬X.contactGraph.Adj i j) :
    1 < dist (X.point i) (X.point j) := by
  have hsep := X.separated hne
  have hneone : dist (X.point i) (X.point j) ≠ 1 := by
    intro heq
    exact hnot ⟨hne, heq⟩
  exact lt_of_le_of_ne hsep (Ne.symm hneone)

section Finite

variable [Fintype ι]

/-- Number of unordered touching pairs. -/
noncomputable def contactCount : ℕ := by
  classical
  exact X.contactGraph.edgeFinset.card

/-- Contact degree of one labelled point. -/
noncomputable def contactDegree (i : ι) : ℕ := by
  classical
  exact X.contactGraph.degree i

/-- Integer-valued contact deficit, before invoking the kissing-number degree bound. -/
noncomputable def contactDeficitZ : ℤ :=
  6 * (Fintype.card ι : ℤ) - (X.contactCount : ℤ)

/-- Natural contact deficit.  It agrees with `contactDeficitZ` once `contactCount ≤ 6n`. -/
noncomputable def contactDeficit : ℕ :=
  6 * Fintype.card ι - X.contactCount

/-- The sum of contact degrees is twice the contact count. -/
theorem sum_contactDegrees_eq_twice_contactCount :
    (∑ i : ι, X.contactDegree i) = 2 * X.contactCount := by
  classical
  simpa [contactDegree, contactCount] using X.contactGraph.sum_degrees_eq_twice_card_edges

/-- Integer degree-deficit identity, valid without first proving every degree is at most twelve. -/
theorem degree_deficit_sum_Z :
    (∑ i : ι, ((12 : ℤ) - (X.contactDegree i : ℤ))) =
      2 * X.contactDeficitZ := by
  classical
  have hdegree :
      (∑ i : ι, (X.contactDegree i : ℤ)) =
        2 * (X.contactCount : ℤ) := by
    exact_mod_cast X.sum_contactDegrees_eq_twice_contactCount
  calc
    (∑ i : ι, ((12 : ℤ) - (X.contactDegree i : ℤ))) =
        12 * (Fintype.card ι : ℤ) -
          ∑ i : ι, (X.contactDegree i : ℤ) := by
            rw [Finset.sum_sub_distrib]
            simp
            ring
    _ = 12 * (Fintype.card ι : ℤ) - 2 * (X.contactCount : ℤ) := by
      rw [hdegree]
    _ = 2 * X.contactDeficitZ := by
      simp [contactDeficitZ]
      ring

/-- The geometric degree bound needed to turn the integer deficit into a natural deficit. -/
def HasContactDegreeAtMostTwelve : Prop :=
  ∀ i : ι, X.contactDegree i ≤ 12

/-- A twelve-degree bound implies the contact count is at most `6n`. -/
theorem contactCount_le_six_card
    (hdegree : X.HasContactDegreeAtMostTwelve) :
    X.contactCount ≤ 6 * Fintype.card ι := by
  have hsum :
      (∑ i : ι, X.contactDegree i) ≤
        ∑ _i : ι, 12 :=
    Finset.sum_le_sum fun i _ => hdegree i
  rw [X.sum_contactDegrees_eq_twice_contactCount] at hsum
  simp at hsum
  omega

/-- Under the kissing-number degree bound, the natural and integer deficits agree. -/
theorem contactDeficit_cast
    (hdegree : X.HasContactDegreeAtMostTwelve) :
    (X.contactDeficit : ℤ) = X.contactDeficitZ := by
  have hle := X.contactCount_le_six_card hdegree
  simp [contactDeficit, contactDeficitZ, Nat.cast_sub hle]

end Finite

end UnitSeparatedConfiguration

end

end Erdos1084
