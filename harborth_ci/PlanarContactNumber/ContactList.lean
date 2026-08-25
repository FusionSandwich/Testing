import PlanarContactNumber.ContactSnoc

namespace PlanarContactNumber

/-- Enumerating a list after appending one point agrees with `Fin.snoc` of the
old enumeration. -/
theorem get_append_singleton_eq_snoc (l : List Axial) (p : Axial) :
    (l ++ [p]).get = Fin.snoc l.get p := by
  funext i
  by_cases h : i.1 < l.length
  · simp [Fin.snoc, h, List.get_eq_getElem, List.getElem_append_left]
  · have hi : i.1 = l.length := by
      have hil := i.2
      simp only [List.length_append, List.length_singleton] at hil
      omega
    have hiLast : i = Fin.last l.length := by
      apply Fin.ext
      exact hi
    subst i
    simp [List.get_eq_getElem]

/-- Appending one axial site to a list adds exactly its number of neighbours in
the old list. -/
theorem axialContactNumber_get_append_singleton (l : List Axial) (p : Axial) :
    axialContactNumber (l ++ [p]).get =
      axialContactNumber l.get + newAxialNeighborCount l.get p := by
  rw [get_append_singleton_eq_snoc, axialContactNumber_snoc]

end PlanarContactNumber
