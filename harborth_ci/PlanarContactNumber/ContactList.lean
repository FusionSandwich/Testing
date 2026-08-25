import PlanarContactNumber.ContactSnoc

namespace PlanarContactNumber

/-- Contact number is unchanged when the finite index type is transported along
an equality of cardinalities. -/
theorem axialContactNumber_finCast {m n : ℕ} (h : m = n)
    (a : Fin n → Axial) :
    axialContactNumber (fun i : Fin m => a (Fin.cast h i)) =
      axialContactNumber a := by
  subst n
  rfl

/-- After transporting the index type along the length identity, enumerating a
list with one appended point is exactly `Fin.snoc` of the old enumeration. -/
theorem get_append_singleton_eq_snoc_cast (l : List Axial) (p : Axial) :
    (fun i : Fin (l.length + 1) =>
      (l ++ [p]).get (Fin.cast (by simp) i)) = Fin.snoc l.get p := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [List.get_eq_getElem]
  · simp [List.get_eq_getElem, List.getElem_append_left]

/-- Appending one axial site to a list adds exactly its number of neighbours in
the old list. -/
theorem axialContactNumber_get_append_singleton (l : List Axial) (p : Axial) :
    axialContactNumber (l ++ [p]).get =
      axialContactNumber l.get + newAxialNeighborCount l.get p := by
  let hlen : l.length + 1 = (l ++ [p]).length := by simp
  calc
    axialContactNumber (l ++ [p]).get =
        axialContactNumber (fun i : Fin (l.length + 1) =>
          (l ++ [p]).get (Fin.cast hlen i)) := by
            symm
            exact axialContactNumber_finCast hlen (l ++ [p]).get
    _ = axialContactNumber (Fin.snoc l.get p) := by
          rw [get_append_singleton_eq_snoc_cast]
    _ = axialContactNumber l.get + newAxialNeighborCount l.get p :=
          axialContactNumber_snoc l.get p

end PlanarContactNumber
