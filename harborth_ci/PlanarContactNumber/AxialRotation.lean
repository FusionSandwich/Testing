import PlanarContactNumber.AxialRadiusBounds
import PlanarContactNumber.AxialShell

namespace PlanarContactNumber

/-- Sixty-degree rotation in axial coordinates. -/
def axialRotate (p : Axial) : Axial :=
  (-p.2, p.1 + p.2)

/-- Inverse sixty-degree axial rotation. -/
def axialRotateInv (p : Axial) : Axial :=
  (p.1 + p.2, -p.1)

@[simp] theorem axialRotateInv_rotate (p : Axial) :
    axialRotateInv (axialRotate p) = p := by
  apply Prod.ext <;> simp [axialRotate, axialRotateInv] <;> ring

@[simp] theorem axialRotate_rotateInv (p : Axial) :
    axialRotate (axialRotateInv p) = p := by
  apply Prod.ext <;> simp [axialRotate, axialRotateInv] <;> ring

/-- The axial rotation as an equivalence of lattice sites. -/
def axialRotateEquiv : Axial ≃ Axial where
  toFun := axialRotate
  invFun := axialRotateInv
  left_inv := axialRotateInv_rotate
  right_inv := axialRotate_rotateInv

/-- Axial radius is invariant under the sixty-degree rotation. -/
theorem axialHexRadius_rotate (p : Axial) :
    axialHexRadius (axialRotate p) = axialHexRadius p := by
  unfold axialHexRadius axialRotate
  dsimp
  rw [abs_neg]
  have hsum : -p.2 + (p.1 + p.2) = p.1 := by ring
  rw [hsum]
  ac_rfl

/-- The triangular quadratic form of a difference is rotation-invariant. -/
theorem axialNormSq_rotate_sub (p q : Axial) :
    axialNormSq ((axialRotate p).1 - (axialRotate q).1,
      (axialRotate p).2 - (axialRotate q).2) =
      axialNormSq (p.1 - q.1, p.2 - q.2) := by
  rcases p with ⟨px, py⟩
  rcases q with ⟨qx, qy⟩
  simp [axialRotate, axialNormSq]
  ring

/-- Axial adjacency is rotation-invariant. -/
theorem axialAdjacent_rotate_iff (p q : Axial) :
    AxialAdjacent (axialRotate p) (axialRotate q) ↔ AxialAdjacent p q := by
  unfold AxialAdjacent
  rw [axialNormSq_rotate_sub]

/-- Centered axial-ball membership is rotation-invariant. -/
theorem mem_axialBall_rotate_iff (s : ℕ) (p : Axial) :
    axialRotate p ∈ axialBall s ↔ p ∈ axialBall s := by
  rw [mem_axialBall_iff_axialHexRadius_le,
    mem_axialBall_iff_axialHexRadius_le, axialHexRadius_rotate]

@[simp] theorem axialRotate_block0At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock0At r i) = axialShellBlock1At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock0At, axialShellBlock1At] <;> ring

@[simp] theorem axialRotate_block1At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock1At r i) = axialShellBlock2At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock1At, axialShellBlock2At] <;> ring

@[simp] theorem axialRotate_block2At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock2At r i) = axialShellBlock3At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock2At, axialShellBlock3At] <;> ring

@[simp] theorem axialRotate_block3At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock3At r i) = axialShellBlock4At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock3At, axialShellBlock4At] <;> ring

@[simp] theorem axialRotate_block4At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock4At r i) = axialShellBlock5At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock4At, axialShellBlock5At] <;> ring

@[simp] theorem axialRotate_block5At (r : ℕ) (i : Fin r) :
    axialRotate (axialShellBlock5At r i) = axialShellBlock0At r i := by
  apply Prod.ext <;> simp [axialRotate, axialShellBlock5At, axialShellBlock0At] <;> ring

end PlanarContactNumber
