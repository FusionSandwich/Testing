import PlanarContactNumber.AxialInwardNeighbors
import PlanarContactNumber.AxialRotationCount

namespace PlanarContactNumber

/-- Exact number of inward neighbours for a point on the second shell side. -/
theorem newAxialNeighborCount_ball_block1 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock1At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  calc
    newAxialNeighborCount (axialBall s).get (axialShellBlock1At (s + 1) i) =
        newAxialNeighborCount (axialBall s).get
          (axialRotate (axialShellBlock0At (s + 1) i)) := by
            rw [axialRotate_block0At]
    _ = newAxialNeighborCount (axialBall s).get
          (axialShellBlock0At (s + 1) i) :=
        newAxialNeighborCount_ball_rotate s _
    _ = if i.1 = s then 1 else 2 :=
        newAxialNeighborCount_ball_block0 s i

/-- Exact number of inward neighbours for a point on the third shell side. -/
theorem newAxialNeighborCount_ball_block2 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock2At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  calc
    newAxialNeighborCount (axialBall s).get (axialShellBlock2At (s + 1) i) =
        newAxialNeighborCount (axialBall s).get
          (axialRotate (axialShellBlock1At (s + 1) i)) := by
            rw [axialRotate_block1At]
    _ = newAxialNeighborCount (axialBall s).get
          (axialShellBlock1At (s + 1) i) :=
        newAxialNeighborCount_ball_rotate s _
    _ = if i.1 = s then 1 else 2 :=
        newAxialNeighborCount_ball_block1 s i

/-- Exact number of inward neighbours for a point on the fourth shell side. -/
theorem newAxialNeighborCount_ball_block3 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock3At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  calc
    newAxialNeighborCount (axialBall s).get (axialShellBlock3At (s + 1) i) =
        newAxialNeighborCount (axialBall s).get
          (axialRotate (axialShellBlock2At (s + 1) i)) := by
            rw [axialRotate_block2At]
    _ = newAxialNeighborCount (axialBall s).get
          (axialShellBlock2At (s + 1) i) :=
        newAxialNeighborCount_ball_rotate s _
    _ = if i.1 = s then 1 else 2 :=
        newAxialNeighborCount_ball_block2 s i

/-- Exact number of inward neighbours for a point on the fifth shell side. -/
theorem newAxialNeighborCount_ball_block4 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock4At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  calc
    newAxialNeighborCount (axialBall s).get (axialShellBlock4At (s + 1) i) =
        newAxialNeighborCount (axialBall s).get
          (axialRotate (axialShellBlock3At (s + 1) i)) := by
            rw [axialRotate_block3At]
    _ = newAxialNeighborCount (axialBall s).get
          (axialShellBlock3At (s + 1) i) :=
        newAxialNeighborCount_ball_rotate s _
    _ = if i.1 = s then 1 else 2 :=
        newAxialNeighborCount_ball_block3 s i

/-- Exact number of inward neighbours for a point on the sixth shell side. -/
theorem newAxialNeighborCount_ball_block5 (s : ℕ) (i : Fin (s + 1)) :
    newAxialNeighborCount (axialBall s).get (axialShellBlock5At (s + 1) i) =
      if i.1 = s then 1 else 2 := by
  calc
    newAxialNeighborCount (axialBall s).get (axialShellBlock5At (s + 1) i) =
        newAxialNeighborCount (axialBall s).get
          (axialRotate (axialShellBlock4At (s + 1) i)) := by
            rw [axialRotate_block4At]
    _ = newAxialNeighborCount (axialBall s).get
          (axialShellBlock4At (s + 1) i) :=
        newAxialNeighborCount_ball_rotate s _
    _ = if i.1 = s then 1 else 2 :=
        newAxialNeighborCount_ball_block4 s i

end PlanarContactNumber
