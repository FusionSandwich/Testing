import PlanarContactNumber.TriangularLattice

namespace PlanarContactNumber

/-- Two axial lattice sites are adjacent when their difference has triangular
quadratic norm one. -/
def AxialAdjacent (p q : Axial) : Prop :=
  axialNormSq (p.1 - q.1, p.2 - q.2) = 1

/-- The unordered adjacent pairs in a labelled finite axial configuration. -/
noncomputable def axialContactPairs {n : ℕ} (a : Fin n → Axial) :
    Finset (Fin n × Fin n) := by
  classical
  exact Finset.univ.filter fun ij =>
    ij.1 < ij.2 ∧ AxialAdjacent (a ij.1) (a ij.2)

/-- The number of adjacent pairs in a labelled finite axial configuration. -/
noncomputable def axialContactNumber {n : ℕ} (a : Fin n → Axial) : ℕ :=
  (axialContactPairs a).card

/-- Axial adjacency is exactly Euclidean unit distance after the standard
triangular-lattice embedding. -/
theorem dist_triangularPoint_eq_one_iff_axialAdjacent (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) = 1 ↔ AxialAdjacent p q := by
  exact triangularPoint_dist_eq_one_iff p q

/-- The Euclidean contact-pair finset of an embedded axial enumeration is
literally its axial adjacent-pair finset. -/
theorem contactPairs_triangularPoint_comp {n : ℕ} (a : Fin n → Axial) :
    contactPairs (fun i => triangularPoint (a i)) = axialContactPairs a := by
  classical
  apply Finset.ext
  intro ij
  simp [contactPairs, axialContactPairs, AxialAdjacent,
    triangularPoint_dist_eq_one_iff]

/-- Contact counting commutes with the triangular-lattice embedding. -/
theorem contactNumber_triangularPoint_comp {n : ℕ} (a : Fin n → Axial) :
    contactNumber (fun i => triangularPoint (a i)) = axialContactNumber a := by
  rw [contactNumber, axialContactNumber, contactPairs_triangularPoint_comp]

/-- Every injective finite axial enumeration realizes its exact combinatorial
adjacency count in the original Euclidean optimization problem. -/
theorem realizedContactNumber_of_axialEnumeration {n k : ℕ}
    {a : Fin n → Axial} (ha : Function.Injective a)
    (hk : axialContactNumber a = k) :
    RealizedContactNumber n k := by
  refine ⟨fun i => triangularPoint (a i), oneSeparated_triangularPoint_comp ha, ?_⟩
  rw [contactNumber_triangularPoint_comp, hk]

/-- A duplicate-free axial list, enumerated by its positions, realizes its
exact axial contact count in the original Euclidean problem. -/
theorem realizedContactNumber_of_axialList (l : List Axial) (hl : l.Nodup) :
    RealizedContactNumber l.length (axialContactNumber l.get) := by
  exact realizedContactNumber_of_axialEnumeration hl.injective_get rfl

end PlanarContactNumber
