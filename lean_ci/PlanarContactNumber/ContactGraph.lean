import PlanarContactNumber.TriangularLattice
import Mathlib.Combinatorics.SimpleGraph.Finite

namespace PlanarContactNumber

/-- The contact graph of an arbitrary labelled planar configuration. -/
noncomputable def contactGraph {α : Type*} (x : α → Point) : SimpleGraph α where
  Adj i j := i ≠ j ∧ dist (x i) (x j) = 1
  symm := by
    intro i j h
    exact ⟨h.1.symm, by simpa [dist_comm] using h.2⟩
  loopless := ⟨by simp⟩

@[simp]
theorem contactGraph_adj {α : Type*} (x : α → Point) (i j : α) :
    (contactGraph x).Adj i j ↔ i ≠ j ∧ dist (x i) (x j) = 1 := Iff.rfl

/-- The number of contacts on any finite label type. -/
noncomputable def finiteContactNumber {α : Type*} [Fintype α] (x : α → Point) : ℕ :=
  (contactGraph x).edgeFinset.card

/-- One-separation on an arbitrary label type. -/
def OneSeparatedOn {α : Type*} (x : α → Point) : Prop :=
  ∀ i j, i ≠ j → (1 : ℝ) ≤ dist (x i) (x j)

/-- A one-separated labelled configuration has no repeated point. -/
theorem OneSeparatedOn.injective {α : Type*} {x : α → Point}
    (hx : OneSeparatedOn x) : Function.Injective x := by
  intro i j hij
  by_contra hne
  have hsep := hx i j hne
  rw [hij, dist_self] at hsep
  norm_num at hsep

/-- The finite-type contact count agrees with the original `Fin n` definition once the
pair-orientation bridge is established below. -/
noncomputable def finContactNumber (n : ℕ) (x : Fin n → Point) : ℕ :=
  finiteContactNumber x

/-- Every finite contact graph has at most all unordered vertex pairs. -/
theorem finiteContactNumber_le_choose {α : Type*} [Fintype α] (x : α → Point) :
    finiteContactNumber x ≤ (Fintype.card α).choose 2 := by
  classical
  exact (contactGraph x).card_edgeFinset_le_card_choose_two

end PlanarContactNumber
