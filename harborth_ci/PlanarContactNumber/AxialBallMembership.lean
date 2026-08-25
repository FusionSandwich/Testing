import PlanarContactNumber.AxialBall

namespace PlanarContactNumber

private theorem exists_fin_with_cast_succ {r : ℕ} {k : ℤ}
    (hkpos : 1 ≤ k) (hkle : k ≤ (r : ℤ)) :
    ∃ i : Fin r, (i.1 : ℤ) + 1 = k := by
  have hk0 : 0 ≤ k := by omega
  have hkcast : ((k.toNat : ℕ) : ℤ) = k := Int.toNat_of_nonneg hk0
  have hkpos' : 1 ≤ k.toNat := by exact_mod_cast hkpos
  have hkle' : k.toNat ≤ r := by exact_mod_cast hkle
  refine ⟨⟨k.toNat - 1, by omega⟩, ?_⟩
  dsimp
  omega

private theorem mem_block0_of_sector {r : ℕ} {p : Axial}
    (hx : 0 ≤ p.1) (hy : 0 < p.2) (hs : p.1 + p.2 = (r : ℤ)) :
    p ∈ axialShellBlock0 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ (by omega : 1 ≤ p.2)
    (by omega : p.2 ≤ (r : ℤ))
  have hpoint : axialShellBlock0At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock0At] <;> omega
  simpa [axialShellBlock0] using
    (show ∃ i : Fin r, axialShellBlock0At r i = p from ⟨i, hpoint⟩)

private theorem mem_block1_of_sector {r : ℕ} {p : Axial}
    (hx : p.1 < 0) (hy : 0 < p.2) (hys : p.2 = (r : ℤ))
    (hs : 0 ≤ p.1 + p.2) :
    p ∈ axialShellBlock1 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ (by omega : 1 ≤ -p.1)
    (by omega : -p.1 ≤ (r : ℤ))
  have hpoint : axialShellBlock1At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock1At] <;> omega
  simpa [axialShellBlock1] using
    (show ∃ i : Fin r, axialShellBlock1At r i = p from ⟨i, hpoint⟩)

private theorem mem_block2_of_sector {r : ℕ} {p : Axial}
    (hx : p.1 = -(r : ℤ)) (hy0 : 0 ≤ p.2) (hyr : p.2 < (r : ℤ)) :
    p ∈ axialShellBlock2 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ
    (by omega : 1 ≤ (r : ℤ) - p.2)
    (by omega : (r : ℤ) - p.2 ≤ (r : ℤ))
  have hpoint : axialShellBlock2At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock2At] <;> omega
  simpa [axialShellBlock2] using
    (show ∃ i : Fin r, axialShellBlock2At r i = p from ⟨i, hpoint⟩)

private theorem mem_block3_of_sector {r : ℕ} {p : Axial}
    (hx : p.1 ≤ 0) (hy : p.2 < 0) (hs : p.1 + p.2 = -(r : ℤ)) :
    p ∈ axialShellBlock3 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ (by omega : 1 ≤ -p.2)
    (by omega : -p.2 ≤ (r : ℤ))
  have hpoint : axialShellBlock3At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock3At] <;> omega
  simpa [axialShellBlock3] using
    (show ∃ i : Fin r, axialShellBlock3At r i = p from ⟨i, hpoint⟩)

private theorem mem_block4_of_sector {r : ℕ} {p : Axial}
    (hx : 0 < p.1) (hxr : p.1 ≤ (r : ℤ)) (hy : p.2 = -(r : ℤ)) :
    p ∈ axialShellBlock4 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ (by omega : 1 ≤ p.1) hxr
  have hpoint : axialShellBlock4At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock4At] <;> omega
  simpa [axialShellBlock4] using
    (show ∃ i : Fin r, axialShellBlock4At r i = p from ⟨i, hpoint⟩)

private theorem mem_block5_of_sector {r : ℕ} {p : Axial}
    (hx : p.1 = (r : ℤ)) (hy : p.2 ≤ 0) (hyr : -(r : ℤ) < p.2) :
    p ∈ axialShellBlock5 r := by
  obtain ⟨i, hi⟩ := exists_fin_with_cast_succ
    (by omega : 1 ≤ (r : ℤ) + p.2)
    (by omega : (r : ℤ) + p.2 ≤ (r : ℤ))
  have hpoint : axialShellBlock5At r i = p := by
    apply Prod.ext <;> dsimp [axialShellBlock5At] <;> omega
  simpa [axialShellBlock5] using
    (show ∃ i : Fin r, axialShellBlock5At r i = p from ⟨i, hpoint⟩)

/-- Every integer point of positive exact hexagonal radius `r` occurs in the
explicit six-block shell listing. -/
theorem mem_axialShell_of_axialHexRadius_eq {r : ℕ} (hr : 0 < r) {p : Axial}
    (hR : axialHexRadius p = (r : ℤ)) : p ∈ axialShell r := by
  have hRpos : (0 : ℤ) < (r : ℤ) := by exact_mod_cast hr
  rcases p with ⟨x, y⟩
  change (x, y) ∈ axialShell r
  change axialHexRadius (x, y) = (r : ℤ) at hR
  by_cases hy0 : 0 ≤ y
  · by_cases hx0 : 0 ≤ x
    · by_cases hy : 0 < y
      · have hs0 : 0 ≤ x + y := by omega
        have hsR : x + y = (r : ℤ) := by
          unfold axialHexRadius at hR
          rw [abs_of_nonneg hx0, abs_of_nonneg hy0, abs_of_nonneg hs0] at hR
          simp only [max_eq_right (by omega : x ≤ x + y),
            max_eq_right (by omega : y ≤ x + y)] at hR
          exact hR
        have hmem0 := mem_block0_of_sector hx0 hy hsR
        simp [axialShell, hmem0]
      · have hyz : y = 0 := by omega
        have hxR : x = (r : ℤ) := by
          subst y
          simpa [axialHexRadius, abs_of_nonneg hx0] using hR
        have hxpos : 0 < x := by omega
        have hmem5 := mem_block5_of_sector hxR (by omega : (0 : ℤ) ≤ 0)
          (by omega : -(r : ℤ) < 0)
        simp [axialShell, hmem5]
    · have hx : x < 0 := by omega
      by_cases hs0 : 0 ≤ x + y
      · have hy : 0 < y := by omega
        have hyR : y = (r : ℤ) := by
          unfold axialHexRadius at hR
          rw [abs_of_nonpos (by omega : x ≤ 0), abs_of_nonneg hy0,
            abs_of_nonneg hs0] at hR
          simp only [max_eq_right (by omega : -x ≤ y),
            max_eq_left (by omega : x + y ≤ y)] at hR
          exact hR
        have hmem1 := mem_block1_of_sector hx hy hyR hs0
        simp [axialShell, hmem1]
      · have hs : x + y < 0 := by omega
        have hxR : x = -(r : ℤ) := by
          unfold axialHexRadius at hR
          rw [abs_of_nonpos (by omega : x ≤ 0), abs_of_nonneg hy0,
            abs_of_nonpos (by omega : x + y ≤ 0)] at hR
          have hinner : max y (-(x + y)) ≤ -x :=
            max_le (by omega) (by omega)
          rw [max_eq_left hinner] at hR
          omega
        have hyr : y < (r : ℤ) := by omega
        have hmem2 := mem_block2_of_sector hxR hy0 hyr
        simp [axialShell, hmem2]
  · have hy : y < 0 := by omega
    by_cases hx0 : x ≤ 0
    · have hs : x + y < 0 := by omega
      have hsR : x + y = -(r : ℤ) := by
        unfold axialHexRadius at hR
        rw [abs_of_nonpos hx0, abs_of_nonpos (by omega : y ≤ 0),
          abs_of_nonpos (by omega : x + y ≤ 0)] at hR
        simp only [max_eq_right (by omega : -x ≤ -(x + y)),
          max_eq_right (by omega : -y ≤ -(x + y))] at hR
        omega
      have hmem3 := mem_block3_of_sector hx0 hy hsR
      simp [axialShell, hmem3]
    · have hx : 0 < x := by omega
      by_cases hs0 : x + y ≤ 0
      · have hyR : y = -(r : ℤ) := by
          unfold axialHexRadius at hR
          rw [abs_of_nonneg (by omega : 0 ≤ x), abs_of_nonpos (by omega : y ≤ 0),
            abs_of_nonpos hs0] at hR
          simp only [max_eq_right (by omega : x ≤ -y),
            max_eq_left (by omega : -(x + y) ≤ -y)] at hR
          omega
        have hxr : x ≤ (r : ℤ) := by omega
        have hmem4 := mem_block4_of_sector hx hxr hyR
        simp [axialShell, hmem4]
      · have hs : 0 < x + y := by omega
        have hxR : x = (r : ℤ) := by
          unfold axialHexRadius at hR
          rw [abs_of_nonneg (by omega : 0 ≤ x), abs_of_nonpos (by omega : y ≤ 0),
            abs_of_nonneg (by omega : 0 ≤ x + y)] at hR
          have hinner : max (-y) (x + y) ≤ x :=
            max_le (by omega) (by omega)
          rw [max_eq_left hinner] at hR
          exact hR
        have hyr : -(r : ℤ) < y := by omega
        have hmem5 := mem_block5_of_sector hxR (by omega : y ≤ 0) hyr
        simp [axialShell, hmem5]

/-- Exact membership characterization of a positive axial shell. -/
theorem mem_axialShell_iff_axialHexRadius_eq {r : ℕ} (hr : 0 < r) {p : Axial} :
    p ∈ axialShell r ↔ axialHexRadius p = (r : ℤ) := by
  constructor
  · exact axialHexRadius_eq_of_mem_shell
  · exact mem_axialShell_of_axialHexRadius_eq hr

/-- The axial hexagonal radius is always nonnegative. -/
theorem axialHexRadius_nonneg (p : Axial) : 0 ≤ axialHexRadius p := by
  unfold axialHexRadius
  exact le_trans (abs_nonneg p.1) (le_max_left _ _)

/-- Exact membership characterization of the centered axial ball. -/
theorem mem_axialBall_iff_axialHexRadius_le {s : ℕ} {p : Axial} :
    p ∈ axialBall s ↔ axialHexRadius p ≤ (s : ℤ) := by
  induction s with
  | zero =>
      constructor
      · exact axialHexRadius_le_of_mem_ball
      · intro h
        have hR0 : axialHexRadius p = 0 := by
          exact le_antisymm h (axialHexRadius_nonneg p)
        have hxabs : |p.1| ≤ 0 := by
          unfold axialHexRadius at hR0
          have hx : |p.1| ≤ max |p.1| (max |p.2| |p.1 + p.2|) := le_max_left _ _
          omega
        have hyabs : |p.2| ≤ 0 := by
          unfold axialHexRadius at hR0
          have hy : |p.2| ≤ max |p.2| |p.1 + p.2| := le_max_left _ _
          have hy' : |p.2| ≤ max |p.1| (max |p.2| |p.1 + p.2|) :=
            le_trans hy (le_max_right _ _)
          omega
        have hx0 : p.1 = 0 := abs_eq_zero.mp (le_antisymm hxabs (abs_nonneg p.1))
        have hy0 : p.2 = 0 := abs_eq_zero.mp (le_antisymm hyabs (abs_nonneg p.2))
        have hp0 : p = (0, 0) := Prod.ext hx0 hy0
        subst p
        simp [axialBall]
  | succ s ih =>
      constructor
      · exact axialHexRadius_le_of_mem_ball
      · intro h
        by_cases hsmall : axialHexRadius p ≤ (s : ℤ)
        · simp only [axialBall_succ, List.mem_append]
          exact Or.inl (ih.mpr hsmall)
        · have heq : axialHexRadius p = ((s + 1 : ℕ) : ℤ) := by
            omega
          simp only [axialBall_succ, List.mem_append]
          exact Or.inr (mem_axialShell_of_axialHexRadius_eq (by omega) heq)

end PlanarContactNumber
