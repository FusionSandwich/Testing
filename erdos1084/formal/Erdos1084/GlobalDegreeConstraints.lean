import Mathlib
import Erdos1084.BulkTwelveCore

namespace Erdos1084

/-- Vertices of contact degree exactly eleven. -/
def degreeElevenVertices
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) : Finset ι :=
  Finset.univ.filter fun i => degree i = 11

/-- Every degree-eleven vertex consumes one unit of degree deficit. -/
theorem degreeEleven_card_le_degree_defect_sum
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) :
    (degreeElevenVertices degree).card ≤ ∑ i, (12 - degree i) := by
  calc
    (degreeElevenVertices degree).card =
        ∑ i : ι, if degree i = 11 then 1 else 0 := by
      simp [degreeElevenVertices]
    _ ≤ ∑ i : ι, (12 - degree i) := by
      apply Finset.sum_le_sum
      intro i _
      by_cases hi : degree i = 11
      · simp [hi]
      · simp [hi]

/-- If the total degree deficit is `2D`, at most `2D` vertices have degree eleven. -/
theorem degreeEleven_card_le_twice_contact_deficit
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (D : ℕ)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (degreeElevenVertices degree).card ≤ 2 * D := by
  calc
    (degreeElevenVertices degree).card ≤ ∑ i, (12 - degree i) :=
      degreeEleven_card_le_degree_defect_sum degree
    _ = 2 * D := hdeficit

/-- Abstract minimum-degree-two conclusion supplied by the geometric leaf-motion lemma. -/
def MinimumContactDegreeTwo
    {ι : Type*} (degree : ι → ℕ) : Prop :=
  ∀ i, 2 ≤ degree i

/-- Degree one is excluded under the minimum-degree-two property. -/
theorem degree_ne_one_of_minimum_two
    {ι : Type*} (degree : ι → ℕ)
    (h : MinimumContactDegreeTwo degree) :
    ∀ i, degree i ≠ 1 := by
  intro i hi
  have htwo := h i
  omega

/-- Of the two affine endpoint degrees, only eleven remains once degree one is excluded. -/
theorem endpoint_degree_reduction_of_minimum_two
    {d : ℕ} (hmin : 2 ≤ d)
    (hEndpoint : d = 1 ∨ d = 11) :
    d = 11 := by
  rcases hEndpoint with h1 | h11
  · omega
  · exact h11

end Erdos1084
