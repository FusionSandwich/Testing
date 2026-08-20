import Mathlib

namespace Erdos1084

/-!
# Surface-order defect halo

For a finite degree function, vertices of degree below twelve consume at least one
unit of degree deficit. If every vertex has at most twelve listed neighbors, the
closed one-step halo of the defective vertices has cardinality at most thirteen
times the defective set, hence at most `26 D` when the total degree deficit is
`2 D`.

The geometric contact graph supplies the degree function and neighbor finsets.
This module certifies the finite combinatorial estimate independently of the
FCC/HCP recognition theorem.
-/

/-- Vertices whose degree is strictly below twelve. -/
def degreeDefectVertices
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) : Finset ι :=
  Finset.univ.filter fun i => degree i < 12

/-- Closed one-step halo of the degree-defect set for an abstract neighbor list. -/
def degreeDefectHalo
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (neighbors : ι → Finset ι) : Finset ι :=
  degreeDefectVertices degree ∪
    (degreeDefectVertices degree).biUnion neighbors

/-- Every degree-defect vertex consumes at least one unit of degree deficit. -/
theorem degreeDefectVertices_card_le_deficit_sum
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) :
    (degreeDefectVertices degree).card ≤ ∑ i, (12 - degree i) := by
  calc
    (degreeDefectVertices degree).card =
        ∑ i : ι, if degree i < 12 then 1 else 0 := by
      simp [degreeDefectVertices]
    _ ≤ ∑ i : ι, (12 - degree i) := by
      apply Finset.sum_le_sum
      intro i _
      by_cases hi : degree i < 12
      · simp [hi]
        omega
      · simp [hi]

/-- A one-step halo has size at most thirteen times the defective set. -/
theorem degreeDefectHalo_card_le_thirteen_mul
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (neighbors : ι → Finset ι)
    (hneighbors : ∀ i, (neighbors i).card ≤ 12) :
    (degreeDefectHalo degree neighbors).card ≤
      13 * (degreeDefectVertices degree).card := by
  let bad := degreeDefectVertices degree
  have hUnion :
      (bad ∪ bad.biUnion neighbors).card ≤
        bad.card + (bad.biUnion neighbors).card :=
    Finset.card_union_le _ _
  have hBiUnion :
      (bad.biUnion neighbors).card ≤
        ∑ i ∈ bad, (neighbors i).card :=
    Finset.card_biUnion_le
  have hNeighborSum :
      (∑ i ∈ bad, (neighbors i).card) ≤
        ∑ _i ∈ bad, 12 := by
    apply Finset.sum_le_sum
    intro i _
    exact hneighbors i
  change (bad ∪ bad.biUnion neighbors).card ≤ 13 * bad.card
  calc
    (bad ∪ bad.biUnion neighbors).card
        ≤ bad.card + (bad.biUnion neighbors).card := hUnion
    _ ≤ bad.card + ∑ i ∈ bad, (neighbors i).card :=
      Nat.add_le_add_left hBiUnion _
    _ ≤ bad.card + ∑ _i ∈ bad, 12 :=
      Nat.add_le_add_left hNeighborSum _
    _ = 13 * bad.card := by
      simp
      omega

/-- If the total degree deficit is `2 D`, the one-step defect halo has size at most `26 D`. -/
theorem degreeDefectHalo_card_le_twentySix_mul
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (neighbors : ι → Finset ι) (D : ℕ)
    (hneighbors : ∀ i, (neighbors i).card ≤ 12)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (degreeDefectHalo degree neighbors).card ≤ 26 * D := by
  have hbad : (degreeDefectVertices degree).card ≤ 2 * D := by
    calc
      (degreeDefectVertices degree).card
          ≤ ∑ i, (12 - degree i) :=
        degreeDefectVertices_card_le_deficit_sum degree
      _ = 2 * D := hdeficit
  calc
    (degreeDefectHalo degree neighbors).card
        ≤ 13 * (degreeDefectVertices degree).card :=
      degreeDefectHalo_card_le_thirteen_mul degree neighbors hneighbors
    _ ≤ 13 * (2 * D) := Nat.mul_le_mul_left 13 hbad
    _ = 26 * D := by omega

end Erdos1084
