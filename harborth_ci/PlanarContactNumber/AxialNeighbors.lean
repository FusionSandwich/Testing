import PlanarContactNumber.AxialBallMembership

namespace PlanarContactNumber

/-- The six nearest neighbours of an axial lattice point. -/
def axialNeighborFinset (p : Axial) : Finset Axial :=
  {(p.1 + 1, p.2), (p.1, p.2 + 1), (p.1 - 1, p.2 + 1),
    (p.1 - 1, p.2), (p.1, p.2 - 1), (p.1 + 1, p.2 - 1)}

/-- Membership in the explicit six-point neighbour finset is exactly axial
adjacency. -/
theorem mem_axialNeighborFinset_iff (p q : Axial) :
    q ∈ axialNeighborFinset p ↔ AxialAdjacent q p := by
  constructor
  · intro h
    simp only [axialNeighborFinset, Finset.mem_insert, Finset.mem_singleton] at h
    rcases h with h | h | h | h | h | h <;> subst q <;>
      simp [AxialAdjacent, axialNormSq] <;> ring
  · intro h
    rw [AxialAdjacent, axialNormSq_eq_one_iff] at h
    simp only [axialNeighborFinset, Finset.mem_insert, Finset.mem_singleton]
    rcases h with h | h | h | h | h | h
    · left
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega
    · right; left
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega
    · right; right; left
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega
    · right; right; right; left
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega
    · right; right; right; right; left
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega
    · right; right; right; right; right
      apply Prod.ext
      · have hx := congrArg Prod.fst h
        dsimp at hx ⊢
        omega
      · have hy := congrArg Prod.snd h
        dsimp at hy ⊢
        omega

/-- Every axial point has exactly six distinct nearest neighbours. -/
theorem axialNeighborFinset_card (p : Axial) :
    (axialNeighborFinset p).card = 6 := by
  rcases p with ⟨x, y⟩
  simp [axialNeighborFinset, Prod.ext_iff]
  all_goals omega

/-- Axial adjacency is symmetric. -/
theorem axialAdjacent_symm {p q : Axial} (h : AxialAdjacent p q) :
    AxialAdjacent q p := by
  rw [← mem_axialNeighborFinset_iff] at h ⊢
  simp only [axialNeighborFinset, Finset.mem_insert, Finset.mem_singleton] at h ⊢
  rcases h with h | h | h | h | h | h <;>
    rcases p with ⟨px, py⟩ <;> rcases q with ⟨qx, qy⟩ <;>
    simp only at h ⊢ <;> rcases h with ⟨rfl, rfl⟩ <;> omega

end PlanarContactNumber
