import Mathlib
import Erdos1084.ContactNumberExistence

namespace Erdos1084

/-!
# A contact maximizer has no isolated vertex

For a purported isolated point `i`, choose among the remaining centers a point `j` with maximal
first coordinate. Replace `i` by `j + e₀`, where `e₀` is the first coordinate unit vector. The
supporting-coordinate choice guarantees that the new point remains at distance at least one from
every old point, while it is at distance exactly one from `j`. All old contacts are preserved and
one new contact is created, contradicting maximality.

This formalizes the first-contact/no-isolated bridge without compactness or a continuous-motion
argument.
-/

noncomputable section

/-- First coordinate of a point in Euclidean three-space. -/
def phase1Coord0 (x : Point3) : ℝ := x (0 : Fin 3)

/-- First coordinate unit vector. -/
def phase1Axis0 : Point3 :=
  fun j : Fin 3 => if j = 0 then 1 else 0

@[simp] theorem phase1Axis0_norm : ‖phase1Axis0‖ = 1 := by
  rw [EuclideanSpace.norm_eq]
  simp [phase1Axis0]

@[simp] theorem inner_phase1Axis0 (x : Point3) :
    ⟪x, phase1Axis0⟫_ℝ = phase1Coord0 x := by
  rw [EuclideanSpace.inner_eq_star_dotProduct]
  simp [phase1Axis0, phase1Coord0]

/-- Among the centers other than `i`, one has maximal first coordinate. -/
theorem exists_phase1Coord0_max_other {n : ℕ} (hn : 2 ≤ n)
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) :
    ∃ j : Fin n, j ≠ i ∧
      ∀ k : Fin n, k ≠ i →
        phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j) := by
  classical
  let T : Finset (Fin n) := Finset.univ.erase i
  have hcard : T.card = n - 1 := by simp [T]
  have hT : T.Nonempty := by
    rw [Finset.nonempty_iff_ne_empty]
    intro hzero
    have : T.card = 0 := by simp [hzero]
    omega
  let S : Finset ℝ := T.image (fun k => phase1Coord0 (X.point k))
  have hS : S.Nonempty := hT.image _
  let M : ℝ := S.max' hS
  have hMmem : M ∈ S := Finset.max'_mem S hS
  rcases Finset.mem_image.mp hMmem with ⟨j, hjT, hjM⟩
  refine ⟨j, (Finset.mem_erase.mp hjT).1, ?_⟩
  intro k hk
  have hkT : k ∈ T := by simp [T, hk]
  have hkS : phase1Coord0 (X.point k) ∈ S :=
    Finset.mem_image.mpr ⟨k, hkT, rfl⟩
  have hle : phase1Coord0 (X.point k) ≤ M :=
    Finset.le_max' S _ hkS
  simpa [hjM] using hle

/-- Move label `i` to one unit beyond label `j` in the first coordinate direction. -/
def phase1RelocatedPoint {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    (i j k : Fin n) : Point3 :=
  if k = i then X.point j + phase1Axis0 else X.point k

/-- Distance from the relocated point to every unchanged point remains at least one. -/
theorem phase1_relocated_distance_from_i {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    {i j k : Fin n}
    (hki : k ≠ i)
    (hmax : phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j)) :
    1 ≤ dist (phase1RelocatedPoint X i j i)
      (phase1RelocatedPoint X i j k) := by
  have hinner : 0 ≤ ⟪X.point j - X.point k, phase1Axis0⟫_ℝ := by
    rw [inner_phase1Axis0]
    simp [phase1Coord0]
    linarith
  have hsq :
      ‖(X.point j - X.point k) + phase1Axis0‖ ^ 2 =
        ‖X.point j - X.point k‖ ^ 2 + ‖phase1Axis0‖ ^ 2 +
          2 * ⟪X.point j - X.point k, phase1Axis0⟫_ℝ := by
    exact norm_add_sq_real _ _
  have hnormsq :
      1 ≤ ‖(X.point j - X.point k) + phase1Axis0‖ ^ 2 := by
    rw [hsq, phase1Axis0_norm]
    nlinarith [sq_nonneg ‖X.point j - X.point k‖]
  have hnorm :
      1 ≤ ‖(X.point j - X.point k) + phase1Axis0‖ := by
    have hn := norm_nonneg ((X.point j - X.point k) + phase1Axis0)
    nlinarith
  simp [phase1RelocatedPoint, hki, dist_eq_norm]
  convert hnorm using 1 <;> abel

/-- The relocation determined by a supporting first-coordinate point is unit-separated. -/
def phase1RelocatedConfiguration {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    (i j : Fin n)
    (hmax : ∀ k : Fin n, k ≠ i →
      phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j)) :
    UnitSeparatedConfiguration (Fin n) where
  point := phase1RelocatedPoint X i j
  separated := by
    intro a b hab
    by_cases hai : a = i
    · subst a
      exact phase1_relocated_distance_from_i X
        (by simpa using hab.symm) (hmax b (by simpa using hab.symm))
    · by_cases hbi : b = i
      · subst b
        rw [dist_comm]
        exact phase1_relocated_distance_from_i X
          (by simpa using hab) (hmax a (by simpa using hab))
      · simpa [phase1RelocatedConfiguration, phase1RelocatedPoint, hai, hbi]
          using X.separated hab

/-- Direct adjacency formulation of an isolated contact vertex. -/
def IsContactIsolated {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) : Prop :=
  ∀ k : Fin n, ¬X.contactGraph.Adj i k

/-- Every old contact survives the relocation of an isolated vertex. -/
theorem contactGraph_le_phase1Relocated {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    {i j : Fin n}
    (hiso : IsContactIsolated X i)
    (hmax : ∀ k : Fin n, k ≠ i →
      phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j)) :
    X.contactGraph ≤
      (phase1RelocatedConfiguration X i j hmax).contactGraph := by
  intro a b hab
  have hai : a ≠ i := by
    intro h
    subst a
    exact hiso b hab
  have hbi : b ≠ i := by
    intro h
    subst b
    exact hiso a hab.symm
  exact ⟨hab.1, by
    simpa [phase1RelocatedConfiguration, phase1RelocatedPoint, hai, hbi]
      using hab.2⟩

/-- The relocation creates the new contact `i-j`. -/
theorem phase1Relocated_new_contact {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    {i j : Fin n} (hji : j ≠ i)
    (hmax : ∀ k : Fin n, k ≠ i →
      phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j)) :
    (phase1RelocatedConfiguration X i j hmax).contactGraph.Adj i j := by
  refine ⟨hji.symm, ?_⟩
  simp [phase1RelocatedConfiguration, phase1RelocatedPoint, hji,
    dist_eq_norm, phase1Axis0_norm]

/-- The relocation increases the contact count by at least one. -/
theorem contactCount_add_one_le_phase1Relocated {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n))
    {i j : Fin n} (hji : j ≠ i)
    (hiso : IsContactIsolated X i)
    (hmax : ∀ k : Fin n, k ≠ i →
      phase1Coord0 (X.point k) ≤ phase1Coord0 (X.point j)) :
    X.contactCount + 1 ≤
      (phase1RelocatedConfiguration X i j hmax).contactCount := by
  classical
  let Y := phase1RelocatedConfiguration X i j hmax
  let e : Sym2 (Fin n) := s(i, j)
  have hle : X.contactGraph ≤ Y.contactGraph :=
    contactGraph_le_phase1Relocated X hiso hmax
  have hsubset : X.contactGraph.edgeFinset ⊆ Y.contactGraph.edgeFinset :=
    SimpleGraph.edgeFinset_mono hle
  have heY : e ∈ Y.contactGraph.edgeFinset := by
    simp [e, Y, phase1Relocated_new_contact X hji hmax]
  have heX : e ∉ X.contactGraph.edgeFinset := by
    simp [e, hiso j]
  have hinsert :
      insert e X.contactGraph.edgeFinset ⊆ Y.contactGraph.edgeFinset := by
    intro q hq
    simp only [Finset.mem_insert] at hq
    rcases hq with rfl | hq
    · exact heY
    · exact hsubset hq
  have hcard := Finset.card_le_card hinsert
  rw [Finset.card_insert_of_not_mem heX] at hcard
  simpa [UnitSeparatedConfiguration.contactCount, Y] using hcard

/-- A maximizing realization has no isolated contact vertex. -/
theorem no_isolated_of_contact_maximizer {n m : ℕ} (hn : 2 ≤ n)
    (hmaxN : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m) :
    ∀ i, ¬IsContactIsolated X i := by
  intro i hiso
  obtain ⟨j, hji, hcoord⟩ := exists_phase1Coord0_max_other hn X i
  let Y := phase1RelocatedConfiguration X i j hcoord
  have hgain : X.contactCount + 1 ≤ Y.contactCount :=
    contactCount_add_one_le_phase1Relocated X hji hiso hcoord
  have hupper : Y.contactCount ≤ m := hmaxN.2 Y
  rw [hX] at hgain
  omega

/-- Every vertex of a maximizing realization has contact degree at least one. -/
theorem contactDegree_pos_of_maximizer {n m : ℕ} (hn : 2 ≤ n)
    (hmaxN : IsThreeDimensionalContactNumber n m)
    {X : UnitSeparatedConfiguration (Fin n)}
    (hX : X.contactCount = m) :
    ∀ i, 1 ≤ X.contactDegree i := by
  intro i
  have hnotiso := no_isolated_of_contact_maximizer hn hmaxN hX i
  have hpos : 0 < X.contactDegree i := by
    by_contra hnot
    apply hnotiso
    intro k hadj
    have hmem : k ∈ X.contactGraph.neighborFinset i := by
      simpa using hadj
    have hcardpos : 0 < (X.contactGraph.neighborFinset i).card :=
      Finset.card_pos.mpr ⟨k, hmem⟩
    have : 0 < X.contactDegree i := by
      simpa [UnitSeparatedConfiguration.contactDegree] using hcardpos
    exact hnot this
  exact hpos

end

end Erdos1084
