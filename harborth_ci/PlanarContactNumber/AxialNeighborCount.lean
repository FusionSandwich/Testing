import PlanarContactNumber.AxialNeighbors
import PlanarContactNumber.ContactSnoc

namespace PlanarContactNumber

/-- The old lattice sites adjacent to `p`, expressed as a coordinate finset
rather than a finset of labels. -/
noncomputable def listedAxialNeighbors (l : List Axial) (p : Axial) : Finset Axial := by
  classical
  exact l.toFinset.filter fun q => AxialAdjacent q p

private theorem image_newAxialNeighbors_get (l : List Axial) (p : Axial) :
    (newAxialNeighbors l.get p).image l.get = listedAxialNeighbors l p := by
  classical
  ext q
  constructor
  · intro h
    rcases Finset.mem_image.mp h with ⟨i, hi, rfl⟩
    have hadj : AxialAdjacent (l.get i) p := by
      simpa [newAxialNeighbors] using hi
    exact Finset.mem_filter.mpr ⟨by simp, hadj⟩
  · intro h
    have hmemFin : q ∈ l.toFinset := (Finset.mem_filter.mp h).1
    have hmem : q ∈ l := by simpa using hmemFin
    obtain ⟨i, hiq⟩ := List.mem_iff_get.mp hmem
    have hadj : AxialAdjacent q p := (Finset.mem_filter.mp h).2
    have hadj_i : AxialAdjacent (l.get i) p := by
      rw [hiq]
      exact hadj
    apply Finset.mem_image.mpr
    refine ⟨i, ?_, hiq⟩
    simpa [newAxialNeighbors] using hadj_i

/-- For a duplicate-free list, counting adjacent old labels agrees with
counting adjacent old lattice sites. -/
theorem newAxialNeighborCount_eq_listed_card (l : List Axial) (hl : l.Nodup)
    (p : Axial) :
    newAxialNeighborCount l.get p = (listedAxialNeighbors l p).card := by
  unfold newAxialNeighborCount
  rw [← image_newAxialNeighbors_get]
  symm
  exact Finset.card_image_of_injective _ hl.injective_get

/-- The coordinate old-neighbour finset is the intersection of the listed
sites with the universal six-neighbour finset. -/
theorem listedAxialNeighbors_eq_inter (l : List Axial) (p : Axial) :
    listedAxialNeighbors l p = l.toFinset ∩ axialNeighborFinset p := by
  classical
  ext q
  simp [listedAxialNeighbors, mem_axialNeighborFinset_iff]

/-- Usable form of the old-neighbour count: it is the cardinality of a six-site
intersection. -/
theorem newAxialNeighborCount_eq_inter_card (l : List Axial) (hl : l.Nodup)
    (p : Axial) :
    newAxialNeighborCount l.get p =
      (l.toFinset ∩ axialNeighborFinset p).card := by
  rw [newAxialNeighborCount_eq_listed_card l hl p,
    listedAxialNeighbors_eq_inter]

end PlanarContactNumber
