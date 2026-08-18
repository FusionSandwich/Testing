import Mathlib

namespace Erdos1084

/-- Vertices whose contact degree is strictly below the kissing-number ceiling. -/
def defectiveVertices
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) : Finset ι :=
  Finset.univ.filter fun i => degree i < 12

/--
Every defective vertex consumes at least one unit of the total degree deficit.
This is the combinatorial first step in the surface-order crystallization program.
-/
theorem defective_card_le_degree_defect_sum
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) :
    (defectiveVertices degree).card ≤ ∑ i, (12 - degree i) := by
  calc
    (defectiveVertices degree).card =
        ∑ i : ι, if degree i < 12 then 1 else 0 := by
      simp [defectiveVertices]
    _ ≤ ∑ i : ι, (12 - degree i) := by
      apply Finset.sum_le_sum
      intro i _
      by_cases hi : degree i < 12
      · simp [hi]
        omega
      · simp [hi]

/--
If the total degree deficit is `2D`, at most `2D` vertices fail to have
full degree twelve.
-/
theorem defective_card_le_twice_contact_deficit
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (D : ℕ)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (defectiveVertices degree).card ≤ 2 * D := by
  calc
    (defectiveVertices degree).card ≤ ∑ i, (12 - degree i) :=
      defective_card_le_degree_defect_sum degree
    _ = 2 * D := hdeficit

/--
Abstract closed-neighborhood conversion. In a contact graph, each defective
vertex has degree at most eleven, so its closed neighborhood has at most
twelve vertices. Once that geometric-graph counting fact is supplied as
`hhalo`, the complement of the radius-one twelve-regular core has size at
most `24D`.
-/
theorem defective_halo_card_le_twentyfour_deficit
    {ι : Type*} [DecidableEq ι]
    (bad halo : Finset ι) (D : ℕ)
    (hbad : bad.card ≤ 2 * D)
    (hhalo : halo.card ≤ 12 * bad.card) :
    halo.card ≤ 24 * D := by
  omega

/--
A fixed-radius version used after a separate graph-ball counting estimate.
The factor `growth` can be instantiated by
`1 + 11 * sum_{k=0}^{r-1} 12^k` for a radius-`r` contact-graph neighborhood.
-/
theorem defective_fixed_radius_halo_bound
    {ι : Type*} [DecidableEq ι]
    (bad halo : Finset ι) (D growth : ℕ)
    (hbad : bad.card ≤ 2 * D)
    (hhalo : halo.card ≤ growth * bad.card) :
    halo.card ≤ 2 * growth * D := by
  omega

end Erdos1084
