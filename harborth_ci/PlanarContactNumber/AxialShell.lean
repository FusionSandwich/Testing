import PlanarContactNumber.LatticeRealization

namespace PlanarContactNumber

/-- The first side of the axial shell of radius `r`, starting immediately after
one corner and ending at the next corner. -/
def axialShellBlock0At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (R - k, k)

/-- The second side of the axial shell of radius `r`. -/
def axialShellBlock1At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (-k, R)

/-- The third side of the axial shell of radius `r`. -/
def axialShellBlock2At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (-R, R - k)

/-- The fourth side of the axial shell of radius `r`. -/
def axialShellBlock3At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (-R + k, -k)

/-- The fifth side of the axial shell of radius `r`. -/
def axialShellBlock4At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (k, -R)

/-- The sixth side of the axial shell of radius `r`. -/
def axialShellBlock5At (r : ℕ) (i : Fin r) : Axial :=
  let R : ℤ := r
  let k : ℤ := (i.1 : ℤ) + 1
  (R, -R + k)

/-- Each shell block is listed in its cyclic order. -/
def axialShellBlock0 (r : ℕ) : List Axial := List.ofFn (axialShellBlock0At r)
def axialShellBlock1 (r : ℕ) : List Axial := List.ofFn (axialShellBlock1At r)
def axialShellBlock2 (r : ℕ) : List Axial := List.ofFn (axialShellBlock2At r)
def axialShellBlock3 (r : ℕ) : List Axial := List.ofFn (axialShellBlock3At r)
def axialShellBlock4 (r : ℕ) : List Axial := List.ofFn (axialShellBlock4At r)
def axialShellBlock5 (r : ℕ) : List Axial := List.ofFn (axialShellBlock5At r)

/-- The complete radius-`r` shell, in cyclic order, beginning immediately
after the corner `(r,0)`. -/
def axialShell (r : ℕ) : List Axial :=
  axialShellBlock0 r ++ axialShellBlock1 r ++ axialShellBlock2 r ++
    axialShellBlock3 r ++ axialShellBlock4 r ++ axialShellBlock5 r

@[simp] theorem axialShellBlock0_length (r : ℕ) : (axialShellBlock0 r).length = r := by
  simp [axialShellBlock0]
@[simp] theorem axialShellBlock1_length (r : ℕ) : (axialShellBlock1 r).length = r := by
  simp [axialShellBlock1]
@[simp] theorem axialShellBlock2_length (r : ℕ) : (axialShellBlock2 r).length = r := by
  simp [axialShellBlock2]
@[simp] theorem axialShellBlock3_length (r : ℕ) : (axialShellBlock3 r).length = r := by
  simp [axialShellBlock3]
@[simp] theorem axialShellBlock4_length (r : ℕ) : (axialShellBlock4 r).length = r := by
  simp [axialShellBlock4]
@[simp] theorem axialShellBlock5_length (r : ℕ) : (axialShellBlock5 r).length = r := by
  simp [axialShellBlock5]

@[simp] theorem axialShell_length (r : ℕ) : (axialShell r).length = 6 * r := by
  simp [axialShell]
  omega

@[simp] theorem axialShell_zero : axialShell 0 = [] := by
  simp [axialShell, axialShellBlock0, axialShellBlock1, axialShellBlock2,
    axialShellBlock3, axialShellBlock4, axialShellBlock5]

private theorem axialShellBlock0At_injective (r : ℕ) :
    Function.Injective (axialShellBlock0At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.snd h
  dsimp [axialShellBlock0At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

private theorem axialShellBlock1At_injective (r : ℕ) :
    Function.Injective (axialShellBlock1At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.fst h
  dsimp [axialShellBlock1At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

private theorem axialShellBlock2At_injective (r : ℕ) :
    Function.Injective (axialShellBlock2At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.snd h
  dsimp [axialShellBlock2At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

private theorem axialShellBlock3At_injective (r : ℕ) :
    Function.Injective (axialShellBlock3At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.snd h
  dsimp [axialShellBlock3At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

private theorem axialShellBlock4At_injective (r : ℕ) :
    Function.Injective (axialShellBlock4At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.fst h
  dsimp [axialShellBlock4At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

private theorem axialShellBlock5At_injective (r : ℕ) :
    Function.Injective (axialShellBlock5At r) := by
  intro i j h
  apply Fin.ext
  have hk := congrArg Prod.snd h
  dsimp [axialShellBlock5At] at hk
  exact_mod_cast (by omega : i.1 = j.1)

/-- No side of a shell repeats a lattice site. -/
theorem axialShellBlock0_nodup (r : ℕ) : (axialShellBlock0 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock0At_injective r)
theorem axialShellBlock1_nodup (r : ℕ) : (axialShellBlock1 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock1At_injective r)
theorem axialShellBlock2_nodup (r : ℕ) : (axialShellBlock2 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock2At_injective r)
theorem axialShellBlock3_nodup (r : ℕ) : (axialShellBlock3 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock3At_injective r)
theorem axialShellBlock4_nodup (r : ℕ) : (axialShellBlock4 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock4At_injective r)
theorem axialShellBlock5_nodup (r : ℕ) : (axialShellBlock5 r).Nodup := by
  exact List.nodup_ofFn.mpr (axialShellBlock5At_injective r)

end PlanarContactNumber
