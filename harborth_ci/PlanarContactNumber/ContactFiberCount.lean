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
  simp [axialContactPairs, axialContactFiber, earlierAxialNeighbors,
    pairWithSecond]

private theorem pairwiseDisjoint_axialContactFiber {n : ℕ} (a : Fin n → Axial) :
    (Set.univ : Set (Fin n)).PairwiseDisjoint (axialContactFiber a) := by
  classical
  intro j _ k _ hjk
  rw [Finset.disjoint_left]
  intro p hpj hpk
  rcases Finset.mem_map.mp hpj with ⟨i, hi, hip⟩
  rcases Finset.mem_map.mp hpk with ⟨m, hm, hmp⟩
  have hsecond : j = k := by
    simpa [pairWithSecond] using congrArg Prod.snd (hip.trans hmp.symm)
  exact hjk hsecond

/-- The exact contact count is the sum of the numbers of earlier neighbours. -/
theorem axialContactNumber_eq_sum_fibers {n : ℕ} (a : Fin n → Axial) :
    axialContactNumber a =
      ∑ j : Fin n, (earlierAxialNeighbors a j).card := by
  classical
  rw [axialContactNumber, axialContactPairs_eq_biUnion_fibers]
  rw [Finset.card_biUnion]
  · simp
  · exact (pairwiseDisjoint_axialContactFiber a).subset (Set.subset_univ _)

end PlanarContactNumber
