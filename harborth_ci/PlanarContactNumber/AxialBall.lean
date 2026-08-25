import PlanarContactNumber.AxialShellNodup
import PlanarContactNumber.HarborthArithmetic

namespace PlanarContactNumber

/-- Hexagonal (axial) radius: the maximum of the three absolute axial
coordinates. -/
def axialHexRadius (p : Axial) : ℤ :=
  max |p.1| (max |p.2| |p.1 + p.2|)

private theorem axialHexRadius_eq_of_bounds {p : Axial} {R : ℤ}
    (hx : |p.1| ≤ R) (hy : |p.2| ≤ R) (hs : |p.1 + p.2| ≤ R)
    (hw : |p.1| = R ∨ |p.2| = R ∨ |p.1 + p.2| = R) :
    axialHexRadius p = R := by
  unfold axialHexRadius
  apply le_antisymm
  · exact max_le hx (max_le hy hs)
  · rcases hw with hw | hw | hw
    · rw [← hw]
      exact le_max_left _ _
    · rw [← hw]
      exact le_max_of_le_right (le_max_left _ _)
    · rw [← hw]
      exact le_max_of_le_right (le_max_right _ _)

private theorem block0_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock0 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock0At r i = p := by
    simpa [axialShellBlock0] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock0At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · right
    right
    rw [abs_of_nonneg] <;> omega

private theorem block1_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock1 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock1At r i = p := by
    simpa [axialShellBlock1] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock1At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · right
    left
    rw [abs_of_nonneg] <;> omega

private theorem block2_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock2 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock2At r i = p := by
    simpa [axialShellBlock2] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock2At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · left
    rw [abs_of_nonpos] <;> omega

private theorem block3_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock3 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock3At r i = p := by
    simpa [axialShellBlock3] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock3At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · right
    right
    rw [abs_of_nonpos] <;> omega

private theorem block4_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock4 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock4At r i = p := by
    simpa [axialShellBlock4] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock4At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · right
    left
    rw [abs_of_nonpos] <;> omega

private theorem block5_radius {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock5 r) : axialHexRadius p = (r : ℤ) := by
  obtain ⟨i, rfl⟩ : ∃ i : Fin r, axialShellBlock5At r i = p := by
    simpa [axialShellBlock5] using h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock5At]
  apply axialHexRadius_eq_of_bounds
  · rw [abs_of_nonneg] <;> omega
  · rw [abs_of_nonpos] <;> omega
  · rw [abs_of_nonneg] <;> omega
  · left
    rw [abs_of_nonneg] <;> omega

/-- Every point in the explicit radius-`r` shell has exact axial radius `r`. -/
theorem axialHexRadius_eq_of_mem_shell {r : ℕ} {p : Axial}
    (h : p ∈ axialShell r) : axialHexRadius p = (r : ℤ) := by
  simp only [axialShell, List.mem_append] at h
  rcases h with h | h | h | h | h | h
  · exact block0_radius h
  · exact block1_radius h
  · exact block2_radius h
  · exact block3_radius h
  · exact block4_radius h
  · exact block5_radius h

/-- Centered axial hexagons, listed by increasing shells. -/
def axialBall : ℕ → List Axial
  | 0 => [(0, 0)]
  | s + 1 => axialBall s ++ axialShell (s + 1)

@[simp] theorem axialBall_zero : axialBall 0 = [(0, 0)] := rfl

@[simp] theorem axialBall_succ (s : ℕ) :
    axialBall (s + 1) = axialBall s ++ axialShell (s + 1) := rfl

/-- Every point in the centered radius-`s` hexagon has radius at most `s`. -/
theorem axialHexRadius_le_of_mem_ball {s : ℕ} {p : Axial}
    (h : p ∈ axialBall s) : axialHexRadius p ≤ (s : ℤ) := by
  induction s with
  | zero =>
      simp only [axialBall_zero, List.mem_singleton] at h
      subst p
      norm_num [axialHexRadius]
  | succ s ih =>
      simp only [axialBall_succ, List.mem_append] at h
      rcases h with h | h
      · exact le_trans (ih h) (by omega)
      · rw [axialHexRadius_eq_of_mem_shell h]

/-- A new shell shares no point with the smaller centered hexagon. -/
theorem axialBall_disjoint_nextShell (s : ℕ) :
    Disjoint (axialBall s) (axialShell (s + 1)) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have hle := axialHexRadius_le_of_mem_ball hp
  have heq := axialHexRadius_eq_of_mem_shell hq
  omega

/-- The centered axial hexagon listing has no duplicate sites. -/
theorem axialBall_nodup (s : ℕ) : (axialBall s).Nodup := by
  induction s with
  | zero => simp
  | succ s ih =>
      exact ih.append (axialShell_nodup (s + 1)) (axialBall_disjoint_nextShell s)

/-- The centered axial hexagon has the centered-hexagonal cardinality. -/
theorem axialBall_length (s : ℕ) : (axialBall s).length = shellN s := by
  induction s with
  | zero => norm_num [axialBall, shellN]
  | succ s ih =>
      simp only [axialBall_succ, List.length_append, axialShell_length, ih]
      simp [shellN]
      ring

end PlanarContactNumber
