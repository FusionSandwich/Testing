import Mathlib

namespace Erdos1084

/-- Vertices whose contact degree is strictly below the kissing-number ceiling. -/
def defectiveVertices
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) : Finset ι :=
  Finset.univ.filter fun i => degree i < 12

/-- Every defective vertex consumes at least one unit of total degree deficit. -/
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

/-- If the total degree deficit is `2D`, at most `2D` vertices have degree below twelve. -/
theorem defective_card_le_twice_contact_deficit
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (D : ℕ)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (defectiveVertices degree).card ≤ 2 * D := by
  calc
    (defectiveVertices degree).card ≤ ∑ i, (12 - degree i) :=
      defective_card_le_degree_defect_sum degree
    _ = 2 * D := hdeficit

/-- Abstract radius-one core conversion. -/
theorem defective_halo_card_le_twentyfour_deficit
    {ι : Type*} [DecidableEq ι]
    (bad halo : Finset ι) (D : ℕ)
    (hbad : bad.card ≤ 2 * D)
    (hhalo : halo.card ≤ 12 * bad.card) :
    halo.card ≤ 24 * D := by
  calc
    halo.card ≤ 12 * bad.card := hhalo
    _ ≤ 12 * (2 * D) := Nat.mul_le_mul_left 12 hbad
    _ = 24 * D := by ring

/-- Fixed-radius version after a separate contact-graph ball-growth estimate. -/
theorem defective_fixed_radius_halo_bound
    {ι : Type*} [DecidableEq ι]
    (bad halo : Finset ι) (D growth : ℕ)
    (hbad : bad.card ≤ 2 * D)
    (hhalo : halo.card ≤ growth * bad.card) :
    halo.card ≤ 2 * growth * D := by
  calc
    halo.card ≤ growth * bad.card := hhalo
    _ ≤ growth * (2 * D) := Nat.mul_le_mul_left growth hbad
    _ = 2 * growth * D := by ring

end Erdos1084
