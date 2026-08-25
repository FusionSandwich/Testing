import PlanarContactNumber.AxialShell

namespace PlanarContactNumber

private theorem mem_block0_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock0 r) :
    ∃ i : Fin r, axialShellBlock0At r i = p := by
  simpa [axialShellBlock0] using h

private theorem mem_block1_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock1 r) :
    ∃ i : Fin r, axialShellBlock1At r i = p := by
  simpa [axialShellBlock1] using h

private theorem mem_block2_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock2 r) :
    ∃ i : Fin r, axialShellBlock2At r i = p := by
  simpa [axialShellBlock2] using h

private theorem mem_block3_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock3 r) :
    ∃ i : Fin r, axialShellBlock3At r i = p := by
  simpa [axialShellBlock3] using h

private theorem mem_block4_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock4 r) :
    ∃ i : Fin r, axialShellBlock4At r i = p := by
  simpa [axialShellBlock4] using h

private theorem mem_block5_exists {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock5 r) :
    ∃ i : Fin r, axialShellBlock5At r i = p := by
  simpa [axialShellBlock5] using h

private theorem block0_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock0 r) :
    0 ≤ p.1 ∧ 0 < p.2 := by
  obtain ⟨i, rfl⟩ := mem_block0_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock0At]
  constructor <;> omega

private theorem block1_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock1 r) :
    p.1 < 0 ∧ 0 < p.2 ∧ p.2 = (r : ℤ) := by
  obtain ⟨i, rfl⟩ := mem_block1_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock1At]
  constructor
  · omega
  constructor <;> omega

private theorem block2_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock2 r) :
    p.1 < 0 ∧ 0 ≤ p.2 ∧ p.2 < (r : ℤ) := by
  obtain ⟨i, rfl⟩ := mem_block2_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock2At]
  constructor
  · omega
  constructor <;> omega

private theorem block3_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock3 r) :
    p.1 ≤ 0 ∧ p.2 < 0 := by
  obtain ⟨i, rfl⟩ := mem_block3_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock3At]
  constructor <;> omega

private theorem block4_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock4 r) :
    0 < p.1 ∧ p.2 < 0 ∧ p.2 = -(r : ℤ) := by
  obtain ⟨i, rfl⟩ := mem_block4_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock4At]
  constructor
  · omega
  constructor <;> omega

private theorem block5_sector {r : ℕ} {p : Axial}
    (h : p ∈ axialShellBlock5 r) :
    0 < p.1 ∧ p.2 ≤ 0 ∧ -(r : ℤ) < p.2 := by
  obtain ⟨i, rfl⟩ := mem_block5_exists h
  have hi : (i.1 : ℤ) < (r : ℤ) := by exact_mod_cast i.isLt
  dsimp [axialShellBlock5At]
  constructor
  · omega
  constructor <;> omega

private theorem block01_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock0 r) (axialShellBlock1 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h0 := block0_sector hp
  have h1 := block1_sector hq
  omega

private theorem block02_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock0 r) (axialShellBlock2 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h0 := block0_sector hp
  have h2 := block2_sector hq
  omega

private theorem block03_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock0 r) (axialShellBlock3 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h0 := block0_sector hp
  have h3 := block3_sector hq
  omega

private theorem block04_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock0 r) (axialShellBlock4 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h0 := block0_sector hp
  have h4 := block4_sector hq
  omega

private theorem block05_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock0 r) (axialShellBlock5 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h0 := block0_sector hp
  have h5 := block5_sector hq
  omega

private theorem block12_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock1 r) (axialShellBlock2 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h1 := block1_sector hp
  have h2 := block2_sector hq
  omega

private theorem block13_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock1 r) (axialShellBlock3 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h1 := block1_sector hp
  have h3 := block3_sector hq
  omega

private theorem block14_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock1 r) (axialShellBlock4 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h1 := block1_sector hp
  have h4 := block4_sector hq
  omega

private theorem block15_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock1 r) (axialShellBlock5 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h1 := block1_sector hp
  have h5 := block5_sector hq
  omega

private theorem block23_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock2 r) (axialShellBlock3 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h2 := block2_sector hp
  have h3 := block3_sector hq
  omega

private theorem block24_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock2 r) (axialShellBlock4 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h2 := block2_sector hp
  have h4 := block4_sector hq
  omega

private theorem block25_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock2 r) (axialShellBlock5 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h2 := block2_sector hp
  have h5 := block5_sector hq
  omega

private theorem block34_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock3 r) (axialShellBlock4 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h3 := block3_sector hp
  have h4 := block4_sector hq
  omega

private theorem block35_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock3 r) (axialShellBlock5 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h3 := block3_sector hp
  have h5 := block5_sector hq
  omega

private theorem block45_disjoint (r : ℕ) :
    List.Disjoint (axialShellBlock4 r) (axialShellBlock5 r) := by
  rw [List.disjoint_iff_ne]
  intro p hp q hq
  intro hpq
  subst q
  have h4 := block4_sector hp
  have h5 := block5_sector hq
  omega

private theorem disjoint_append_left_of_pair {α : Type*}
    {a b c : List α} (hac : List.Disjoint a c) (hbc : List.Disjoint b c) :
    List.Disjoint (a ++ b) c := by
  rw [List.disjoint_iff_ne] at hac hbc ⊢
  intro x hx y hy
  rcases List.mem_append.mp hx with hxa | hxb
  · exact hac x hxa y hy
  · exact hbc x hxb y hy

/-- The six axial side blocks form one injective cyclic listing of the shell. -/
theorem axialShell_nodup (r : ℕ) : (axialShell r).Nodup := by
  let b0 := axialShellBlock0 r
  let b1 := axialShellBlock1 r
  let b2 := axialShellBlock2 r
  let b3 := axialShellBlock3 r
  let b4 := axialShellBlock4 r
  let b5 := axialShellBlock5 r
  have n0 : b0.Nodup := axialShellBlock0_nodup r
  have n1 : b1.Nodup := axialShellBlock1_nodup r
  have n2 : b2.Nodup := axialShellBlock2_nodup r
  have n3 : b3.Nodup := axialShellBlock3_nodup r
  have n4 : b4.Nodup := axialShellBlock4_nodup r
  have n5 : b5.Nodup := axialShellBlock5_nodup r
  have d01 : List.Disjoint b0 b1 := block01_disjoint r
  have d02 : List.Disjoint b0 b2 := block02_disjoint r
  have d03 : List.Disjoint b0 b3 := block03_disjoint r
  have d04 : List.Disjoint b0 b4 := block04_disjoint r
  have d05 : List.Disjoint b0 b5 := block05_disjoint r
  have d12 : List.Disjoint b1 b2 := block12_disjoint r
  have d13 : List.Disjoint b1 b3 := block13_disjoint r
  have d14 : List.Disjoint b1 b4 := block14_disjoint r
  have d15 : List.Disjoint b1 b5 := block15_disjoint r
  have d23 : List.Disjoint b2 b3 := block23_disjoint r
  have d24 : List.Disjoint b2 b4 := block24_disjoint r
  have d25 : List.Disjoint b2 b5 := block25_disjoint r
  have d34 : List.Disjoint b3 b4 := block34_disjoint r
  have d35 : List.Disjoint b3 b5 := block35_disjoint r
  have d45 : List.Disjoint b4 b5 := block45_disjoint r
  have n01 : (b0 ++ b1).Nodup := n0.append n1 d01
  have d01_2 : List.Disjoint (b0 ++ b1) b2 :=
    disjoint_append_left_of_pair d02 d12
  have n012 : ((b0 ++ b1) ++ b2).Nodup := n01.append n2 d01_2
  have d01_3 : List.Disjoint (b0 ++ b1) b3 :=
    disjoint_append_left_of_pair d03 d13
  have d012_3 : List.Disjoint ((b0 ++ b1) ++ b2) b3 :=
    disjoint_append_left_of_pair d01_3 d23
  have n0123 : (((b0 ++ b1) ++ b2) ++ b3).Nodup := n012.append n3 d012_3
  have d01_4 : List.Disjoint (b0 ++ b1) b4 :=
    disjoint_append_left_of_pair d04 d14
  have d012_4 : List.Disjoint ((b0 ++ b1) ++ b2) b4 :=
    disjoint_append_left_of_pair d01_4 d24
  have d0123_4 : List.Disjoint (((b0 ++ b1) ++ b2) ++ b3) b4 :=
    disjoint_append_left_of_pair d012_4 d34
  have n01234 : ((((b0 ++ b1) ++ b2) ++ b3) ++ b4).Nodup :=
    n0123.append n4 d0123_4
  have d01_5 : List.Disjoint (b0 ++ b1) b5 :=
    disjoint_append_left_of_pair d05 d15
  have d012_5 : List.Disjoint ((b0 ++ b1) ++ b2) b5 :=
    disjoint_append_left_of_pair d01_5 d25
  have d0123_5 : List.Disjoint (((b0 ++ b1) ++ b2) ++ b3) b5 :=
    disjoint_append_left_of_pair d012_5 d35
  have d01234_5 : List.Disjoint ((((b0 ++ b1) ++ b2) ++ b3) ++ b4) b5 :=
    disjoint_append_left_of_pair d0123_5 d45
  have hall : (((((b0 ++ b1) ++ b2) ++ b3) ++ b4) ++ b5).Nodup :=
    n01234.append n5 d01234_5
  simpa [axialShell, b0, b1, b2, b3, b4, b5, List.append_assoc] using hall

end PlanarContactNumber
