import PlanarContactNumber.AxialBallMembership

namespace PlanarContactNumber

/-- The six nearest neighbours of an axial lattice point. -/
def axialNeighborFinset (p : Axial) : Finset Axial :=
  {(p.1 + 1, p.2), (p.1, p.2 + 1), (p.1 - 1, p.2 + 1),
    (p.1 - 1, p.2), (p.1, p.2 - 1), (p.1 + 1, p.2 - 1)}

/-- The six unit differences in axial coordinates. -/
def axialUnitNeighborFinset : Finset Axial :=
  {(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)}

/-- Translation by an axial lattice site. -/
def axialTranslateEquiv (p : Axial) : Axial ≃ Axial where
  toFun d := (p.1 + d.1, p.2 + d.2)
  invFun q := (q.1 - p.1, q.2 - p.2)
  left_inv := by
    intro d
    apply Prod.ext <;> simp <;> omega
  right_inv := by
    intro q
    apply Prod.ext <;> simp <;> omega

/-- The neighbour finset is the translate of the six unit differences. -/
theorem axialNeighborFinset_eq_map_unit (p : Axial) :
    axialNeighborFinset p =
      axialUnitNeighborFinset.map (axialTranslateEquiv p).toEmbedding := by
  classical
  ext q
  simp [axialNeighborFinset, axialUnitNeighborFinset, axialTranslateEquiv,
    Prod.ext_iff]
  omega

/-- Membership in the explicit six-point neighbour finset is exactly axial
adjacency. -/
theorem mem_axialNeighborFinset_iff (p q : Axial) :
    q ∈ axialNeighborFinset p ↔ AxialAdjacent q p := by
  constructor
  · intro h
    simp only [axialNeighborFinset, Finset.mem_insert, Finset.mem_singleton] at h
    rcases h with h | h | h | h | h | h <;> subst q <;>
      simp [AxialAdjacent, axialNormSq]
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
  rw [axialNeighborFinset_eq_map_unit]
  simp [axialUnitNeighborFinset]

/-- Axial adjacency is symmetric. -/
theorem axialAdjacent_symm {p q : Axial} (h : AxialAdjacent p q) :
    AxialAdjacent q p := by
  have hnorm :
      axialNormSq (q.1 - p.1, q.2 - p.2) =
        axialNormSq (p.1 - q.1, p.2 - q.2) := by
    rcases p with ⟨px, py⟩
    rcases q with ⟨qx, qy⟩
    simp [axialNormSq]
    ring
  unfold AxialAdjacent at h ⊢
  rw [hnorm]
  exact h

end PlanarContactNumber
