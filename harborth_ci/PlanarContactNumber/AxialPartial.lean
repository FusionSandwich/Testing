import PlanarContactNumber.AxialBall
import PlanarContactNumber.LatticeRealization

namespace PlanarContactNumber

/-- A centered axial hexagon followed by a prefix of the next shell. -/
def axialPartial (s q : ℕ) : List Axial :=
  axialBall s ++ (axialShell (s + 1)).take q

/-- The same partial-shell construction in the arithmetic parameters used by
Harborth's exact floor decomposition. -/
def axialPartialN (s i j : ℕ) : List Axial :=
  axialPartial s ((s + 1) * i + j)

private theorem mem_of_mem_take {α : Type*} {x : α} {l : List α} {q : ℕ}
    (h : x ∈ l.take q) : x ∈ l := by
  induction q generalizing l with
  | zero => simp at h
  | succ q ih =>
      cases l with
      | nil => simp at h
      | cons a l =>
          simp only [List.take_succ_cons, List.mem_cons] at h ⊢
          exact h.elim Or.inl (fun hx => Or.inr (ih hx))

private theorem axialBall_disjoint_shellTake (s q : ℕ) :
    Disjoint (axialBall s) ((axialShell (s + 1)).take q) := by
  rw [List.disjoint_iff_ne]
  intro p hp q' hq' hpq
  exact (List.disjoint_iff_ne.mp (axialBall_disjoint_nextShell s))
    p hp q' (mem_of_mem_take hq') hpq

/-- The partial-shell listing never repeats a lattice site. -/
theorem axialPartial_nodup (s q : ℕ) : (axialPartial s q).Nodup := by
  exact (axialBall_nodup s).append
    ((axialShell_nodup (s + 1)).take q)
    (axialBall_disjoint_shellTake s q)

/-- Exact cardinality of a partial shell, provided the prefix does not exceed
the next shell. -/
theorem axialPartial_length (s q : ℕ) (hq : q ≤ 6 * (s + 1)) :
    (axialPartial s q).length = shellN s + q := by
  simp only [axialPartial, List.length_append, axialBall_length,
    List.length_take, axialShell_length]
  rw [Nat.min_eq_left hq]

/-- The arithmetic parameters `s,i,j` give exactly `partialN s i j` points. -/
theorem axialPartialN_length (s i j : ℕ) (hi : i ≤ 5) (hj : j ≤ s) :
    (axialPartialN s i j).length = partialN s i j := by
  unfold axialPartialN partialN
  apply axialPartial_length
  omega

/-- Every partial shell already gives an actual Euclidean one-separated
configuration with its exact axial adjacency count. -/
theorem realizedContactNumber_axialPartial (s q : ℕ) :
    RealizedContactNumber (axialPartial s q).length
      (axialContactNumber (axialPartial s q).get) :=
  realizedContactNumber_of_axialList _ (axialPartial_nodup s q)

end PlanarContactNumber
