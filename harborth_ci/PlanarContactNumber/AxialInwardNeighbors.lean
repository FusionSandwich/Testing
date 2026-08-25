import PlanarContactNumber.AxialNeighborCount
import PlanarContactNumber.AxialRadiusBounds

namespace PlanarContactNumber

private theorem neighbor_cases (p q : Axial) (h : q ∈ axialNeighborFinset p) :
    q = (p.1 + 1, p.2) ∨ q = (p.1, p.2 + 1) ∨
    q = (p.1 - 1, p.2 + 1) ∨ q = (p.1 - 1, p.2) ∨
    q = (p.1, p.2 - 1) ∨ q = (p.1 + 1, p.2 - 1) := by
  simpa [axialNeighborFinset] using h

/-- For a non-corner point of the first side of shell `s+1`, the old centered
ball contains exactly the two inward neighbours. -/
theorem ball_inter_neighbors_block0_of_lt (s : ℕ) (i : Fin (s + 1))
    (hi : i.1 < s) :
    (axialBall s).toFinset ∩ axialNeighborFinset (axialShellBlock0At (s + 1) i) =
      {(axialShellBlock0At (s + 1) i).1 - 1,
          (axialShellBlock0At (s + 1) i).2,
        (axialShellBlock0At (s + 1) i).1,
          (axialShellBlock0At (s + 1) i).2 - 1} := by
  classical
  have hiZ : (i.1 : ℤ) < (s : ℤ) := by exact_mod_cast hi
  ext q
  constructor
  · intro hq
    rcases Finset.mem_inter.mp hq with ⟨hballFin, hneigh⟩
    have hballList : q ∈ axialBall s := by simpa using hballFin
    have hb := mem_axialBall_iff_bounds.mp hballList
    rcases neighbor_cases _ _ hneigh with h | h | h | h | h | h
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      simp
    · subst q
      simp
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
  · intro hq
    simp only [Finset.mem_insert, Finset.mem_singleton] at hq
    rcases hq with hq | hq
    · subst q
      apply Finset.mem_inter.mpr
      constructor
      · have hmem :
            ((axialShellBlock0At (s + 1) i).1 - 1,
              (axialShellBlock0At (s + 1) i).2) ∈ axialBall s := by
          apply mem_axialBall_iff_bounds.mpr
          dsimp [axialShellBlock0At]
          omega
        simpa using hmem
      · simp [axialNeighborFinset]
    · subst q
      apply Finset.mem_inter.mpr
      constructor
      · have hmem :
            ((axialShellBlock0At (s + 1) i).1,
              (axialShellBlock0At (s + 1) i).2 - 1) ∈ axialBall s := by
          apply mem_axialBall_iff_bounds.mpr
          dsimp [axialShellBlock0At]
          omega
        simpa using hmem
      · simp [axialNeighborFinset]

/-- At the terminal corner of the first side of shell `s+1`, only one inward
neighbour lies in the old centered ball. -/
theorem ball_inter_neighbors_block0_of_eq (s : ℕ) (i : Fin (s + 1))
    (hi : i.1 = s) :
    (axialBall s).toFinset ∩ axialNeighborFinset (axialShellBlock0At (s + 1) i) =
      {((axialShellBlock0At (s + 1) i).1,
          (axialShellBlock0At (s + 1) i).2 - 1)} := by
  classical
  have hiZ : (i.1 : ℤ) = (s : ℤ) := by exact_mod_cast hi
  ext q
  constructor
  · intro hq
    rcases Finset.mem_inter.mp hq with ⟨hballFin, hneigh⟩
    have hballList : q ∈ axialBall s := by simpa using hballFin
    have hb := mem_axialBall_iff_bounds.mp hballList
    rcases neighbor_cases _ _ hneigh with h | h | h | h | h | h
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
    · subst q
      simp
    · subst q
      dsimp [axialShellBlock0At] at hb
      omega
  · intro hq
    simp only [Finset.mem_singleton] at hq
    subst q
    apply Finset.mem_inter.mpr
    constructor
    · have hmem :
          ((axialShellBlock0At (s + 1) i).1,
            (axialShellBlock0At (s + 1) i).2 - 1) ∈ axialBall s := by
        apply mem_axialBall_iff_bounds.mpr
        dsimp [axialShellBlock0At]
        omega
      simpa using hmem
    · simp [axialNeighborFinset]

/-- Exact number of inward neighbours for a point on the first shell side. -/
theorem newAxialNeighborCount_ball_block0 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock0At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  rw [newAxialNeighborCount_eq_inter_card _ (axialBall_nodup s)]
  split_ifs with hi
  · rw [ball_inter_neighbors_block0_of_eq s i hi]
    simp
  · have hlt : i.1 < s := by omega
    rw [ball_inter_neighbors_block0_of_lt s i hlt]
    simp [Prod.ext_iff]
    omega

end PlanarContactNumber
