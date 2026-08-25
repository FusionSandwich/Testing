import PlanarContactNumber.AxialAllInwardNeighbors

namespace PlanarContactNumber

/-- Consecutive points within the first shell block are adjacent. -/
theorem axialAdjacent_block0At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock0At r ⟨i + 1, hi⟩)
      (axialShellBlock0At r ⟨i, by omega⟩) := by
  unfold AxialAdjacent
  dsimp [axialShellBlock0At, axialNormSq]
  ring

/-- Consecutive points within the second shell block are adjacent. -/
theorem axialAdjacent_block1At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock1At r ⟨i + 1, hi⟩)
      (axialShellBlock1At r ⟨i, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock0At r ⟨i + 1, hi⟩)
    (axialShellBlock0At r ⟨i, by omega⟩)).2
      (axialAdjacent_block0At_succ r i hi)
  simpa using h

/-- Consecutive points within the third shell block are adjacent. -/
theorem axialAdjacent_block2At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock2At r ⟨i + 1, hi⟩)
      (axialShellBlock2At r ⟨i, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock1At r ⟨i + 1, hi⟩)
    (axialShellBlock1At r ⟨i, by omega⟩)).2
      (axialAdjacent_block1At_succ r i hi)
  simpa using h

/-- Consecutive points within the fourth shell block are adjacent. -/
theorem axialAdjacent_block3At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock3At r ⟨i + 1, hi⟩)
      (axialShellBlock3At r ⟨i, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock2At r ⟨i + 1, hi⟩)
    (axialShellBlock2At r ⟨i, by omega⟩)).2
      (axialAdjacent_block2At_succ r i hi)
  simpa using h

/-- Consecutive points within the fifth shell block are adjacent. -/
theorem axialAdjacent_block4At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock4At r ⟨i + 1, hi⟩)
      (axialShellBlock4At r ⟨i, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock3At r ⟨i + 1, hi⟩)
    (axialShellBlock3At r ⟨i, by omega⟩)).2
      (axialAdjacent_block3At_succ r i hi)
  simpa using h

/-- Consecutive points within the sixth shell block are adjacent. -/
theorem axialAdjacent_block5At_succ (r i : ℕ) (hi : i + 1 < r) :
    AxialAdjacent
      (axialShellBlock5At r ⟨i + 1, hi⟩)
      (axialShellBlock5At r ⟨i, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock4At r ⟨i + 1, hi⟩)
    (axialShellBlock4At r ⟨i, by omega⟩)).2
      (axialAdjacent_block4At_succ r i hi)
  simpa using h

/-- The first inter-block join is a contact. -/
theorem axialAdjacent_block0_last_block1_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock1At r ⟨0, hr⟩)
      (axialShellBlock0At r ⟨r - 1, by omega⟩) := by
  unfold AxialAdjacent
  dsimp [axialShellBlock0At, axialShellBlock1At, axialNormSq]
  ring

/-- The second inter-block join is a contact. -/
theorem axialAdjacent_block1_last_block2_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock2At r ⟨0, hr⟩)
      (axialShellBlock1At r ⟨r - 1, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock1At r ⟨0, hr⟩)
    (axialShellBlock0At r ⟨r - 1, by omega⟩)).2
      (axialAdjacent_block0_last_block1_first r hr)
  simpa using h

/-- The third inter-block join is a contact. -/
theorem axialAdjacent_block2_last_block3_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock3At r ⟨0, hr⟩)
      (axialShellBlock2At r ⟨r - 1, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock2At r ⟨0, hr⟩)
    (axialShellBlock1At r ⟨r - 1, by omega⟩)).2
      (axialAdjacent_block1_last_block2_first r hr)
  simpa using h

/-- The fourth inter-block join is a contact. -/
theorem axialAdjacent_block3_last_block4_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock4At r ⟨0, hr⟩)
      (axialShellBlock3At r ⟨r - 1, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock3At r ⟨0, hr⟩)
    (axialShellBlock2At r ⟨r - 1, by omega⟩)).2
      (axialAdjacent_block2_last_block3_first r hr)
  simpa using h

/-- The fifth inter-block join is a contact. -/
theorem axialAdjacent_block4_last_block5_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock5At r ⟨0, hr⟩)
      (axialShellBlock4At r ⟨r - 1, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock4At r ⟨0, hr⟩)
    (axialShellBlock3At r ⟨r - 1, by omega⟩)).2
      (axialAdjacent_block3_last_block4_first r hr)
  simpa using h

/-- The shell listing closes from the sixth block back to the first. -/
theorem axialAdjacent_block5_last_block0_first (r : ℕ) (hr : 0 < r) :
    AxialAdjacent
      (axialShellBlock0At r ⟨0, hr⟩)
      (axialShellBlock5At r ⟨r - 1, by omega⟩) := by
  have h := (axialAdjacent_rotate_iff
    (axialShellBlock5At r ⟨0, hr⟩)
    (axialShellBlock4At r ⟨r - 1, by omega⟩)).2
      (axialAdjacent_block4_last_block5_first r hr)
  simpa using h

end PlanarContactNumber
