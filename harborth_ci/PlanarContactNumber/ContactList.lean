import PlanarContactNumber.ContactSnoc

namespace PlanarContactNumber

/-- Enumerating a list after appending one point agrees with `Fin.snoc` of the
old enumeration. -/
theorem get_append_singleton_eq_snoc (l : List Axial) (p : Axial) :
    (l ++ [p]).get = Fin.snoc l.get p := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp
  · simp

/-- Appending one axial site to a list adds exactly its number of neighbours in
the old list. -/
theorem axialContactNumber_get_append_singleton (l : List Axial) (p : Axial) :
    axialContactNumber (l ++ [p]).get =
      axialContactNumber l.get + newAxialNeighborCount l.get p := by
  rw [get_append_singleton_eq_snoc, axialContactNumber_snoc]

end PlanarContactNumber
