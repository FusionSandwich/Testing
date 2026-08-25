import PlanarContactNumber.LatticeRealization

namespace PlanarContactNumber

/-- Earlier neighbours of a labelled axial point.  The label inequality chooses
one orientation of every unordered contact. -/
noncomputable def earlierAxialNeighbors {n : ℕ} (a : Fin n → Axial) (j : Fin n) :
    Finset (Fin n) := by
  classical
  exact Finset.univ.filter fun i => i < j ∧ AxialAdjacent (a i) (a j)

/-- The embedding that records a fixed second endpoint. -/
def pairWithSecond {n : ℕ} (j : Fin n) : Fin n ↪ Fin n × Fin n where
  toFun i := (i, j)
  inj' := by
    intro i k h
    exact congrArg Prod.fst h

/-- The contact pairs whose second endpoint is `j`. -/
noncomputable def axialContactFiber {n : ℕ} (a : Fin n → Axial) (j : Fin n) :
    Finset (Fin n × Fin n) :=
  (earlierAxialNeighbors a j).map (pairWithSecond j)

@[simp] theorem axialContactFiber_card {n : ℕ} (a : Fin n → Axial) (j : Fin n) :
    (axialContactFiber a j).card = (earlierAxialNeighbors a j).card := by
  simp [axialContactFiber]

/-- Contact pairs are the disjoint union of their second-endpoint fibres. -/
theorem axialContactPairs_eq_biUnion_fibers {n : ℕ} (a : Fin n → Axial) :
    axialContactPairs a =
      Finset.univ.biUnion (axialContactFiber a) := by
  classical
  ext p
  constructor
  · intro hp
    have hp' : p.1 < p.2 ∧ AxialAdjacent (a p.1) (a p.2) := by
      simpa [axialContactPairs] using hp
    apply Finset.mem_biUnion.mpr
    refine ⟨p.2, Finset.mem_univ _, ?_⟩
    apply Finset.mem_map.mpr
    refine ⟨p.1, ?_, rfl⟩
    simpa [earlierAxialNeighbors] using hp'
  · intro hp
    rcases Finset.mem_biUnion.mp hp with ⟨j, _hj, hpj⟩
    rcases Finset.mem_map.mp hpj with ⟨i, hi, hip⟩
    have hi' : i < j ∧ AxialAdjacent (a i) (a j) := by
      simpa [earlierAxialNeighbors] using hi
    have hp_eq : p = (i, j) := by
      simpa [pairWithSecond] using hip.symm
    subst p
    simpa [axialContactPairs] using hi'

private theorem pairwiseDisjoint_axialContactFiber {n : ℕ} (a : Fin n → Axial) :
    ∀ j ∈ (Finset.univ : Finset (Fin n)),
      ∀ k ∈ (Finset.univ : Finset (Fin n)),
        j ≠ k → Disjoint (axialContactFiber a j) (axialContactFiber a k) := by
  classical
  intro j _ k _ hjk
  apply Finset.disjoint_left.mpr
  intro p hpj hpk
  rcases Finset.mem_map.mp hpj with ⟨i, _hi, hip⟩
  rcases Finset.mem_map.mp hpk with ⟨m, _hm, hmp⟩
  have hpair : (i, j) = (m, k) := by
    simpa [pairWithSecond] using hip.trans hmp.symm
  exact hjk (congrArg Prod.snd hpair)

/-- The exact contact count is the sum of the numbers of earlier neighbours. -/
theorem axialContactNumber_eq_sum_fibers {n : ℕ} (a : Fin n → Axial) :
    axialContactNumber a =
      ∑ j : Fin n, (earlierAxialNeighbors a j).card := by
  classical
  rw [axialContactNumber, axialContactPairs_eq_biUnion_fibers]
  rw [Finset.card_biUnion (pairwiseDisjoint_axialContactFiber a)]
  simp

end PlanarContactNumber
