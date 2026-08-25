import PlanarContactNumber.ContactFiberCount

namespace PlanarContactNumber

/-- Number of old labels adjacent to a proposed new axial point. -/
noncomputable def newAxialNeighborCount {n : ℕ} (a : Fin n → Axial) (p : Axial) : ℕ := by
  classical
  exact (Finset.univ.filter fun i => AxialAdjacent (a i) p).card

private theorem earlierAxialNeighbors_snoc_castSucc {n : ℕ}
    (a : Fin n → Axial) (p : Axial) (j : Fin n) :
    earlierAxialNeighbors (Fin.snoc a p) j.castSucc =
      (earlierAxialNeighbors a j).map Fin.castSuccEmb := by
  classical
  ext i
  refine Fin.lastCases ?_ (fun k => ?_) i
  · simp [earlierAxialNeighbors]
  · simp [earlierAxialNeighbors]

private theorem earlierAxialNeighbors_snoc_last {n : ℕ}
    (a : Fin n → Axial) (p : Axial) :
    earlierAxialNeighbors (Fin.snoc a p) (Fin.last n) =
      (Finset.univ.filter fun i => AxialAdjacent (a i) p).map Fin.castSuccEmb := by
  classical
  ext i
  refine Fin.lastCases ?_ (fun k => ?_) i
  · simp [earlierAxialNeighbors]
  · simp [earlierAxialNeighbors]

@[simp] theorem earlierAxialNeighbors_snoc_castSucc_card {n : ℕ}
    (a : Fin n → Axial) (p : Axial) (j : Fin n) :
    (earlierAxialNeighbors (Fin.snoc a p) j.castSucc).card =
      (earlierAxialNeighbors a j).card := by
  rw [earlierAxialNeighbors_snoc_castSucc]
  simp

@[simp] theorem earlierAxialNeighbors_snoc_last_card {n : ℕ}
    (a : Fin n → Axial) (p : Axial) :
    (earlierAxialNeighbors (Fin.snoc a p) (Fin.last n)).card =
      newAxialNeighborCount a p := by
  rw [earlierAxialNeighbors_snoc_last]
  simp [newAxialNeighborCount]

/-- Appending one labelled axial point adds exactly its old-neighbour count to
the contact number. -/
theorem axialContactNumber_snoc {n : ℕ} (a : Fin n → Axial) (p : Axial) :
    axialContactNumber (Fin.snoc a p) =
      axialContactNumber a + newAxialNeighborCount a p := by
  rw [axialContactNumber_eq_sum_fibers, axialContactNumber_eq_sum_fibers]
  rw [Fin.sum_univ_castSucc]
  simp

end PlanarContactNumber
