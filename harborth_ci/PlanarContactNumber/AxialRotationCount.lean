import PlanarContactNumber.AxialNeighborCount
import PlanarContactNumber.AxialRotation

namespace PlanarContactNumber

/-- Rotation maps the intersection of the old centered ball with the six
neighbours of `p` onto the corresponding intersection for the rotated point. -/
theorem map_ball_inter_neighbors_rotate (s : ℕ) (p : Axial) :
    ((axialBall s).toFinset ∩ axialNeighborFinset p).map
        axialRotateEquiv.toEmbedding =
      (axialBall s).toFinset ∩ axialNeighborFinset (axialRotate p) := by
  classical
  ext q
  constructor
  · intro hq
    rcases Finset.mem_map.mp hq with ⟨a, ha, haq⟩
    have haq' : axialRotate a = q := by simpa [axialRotateEquiv] using haq
    subst q
    rcases Finset.mem_inter.mp ha with ⟨hballFin, hneigh⟩
    apply Finset.mem_inter.mpr
    constructor
    · have hball : a ∈ axialBall s := by simpa using hballFin
      have hrot : axialRotate a ∈ axialBall s :=
        (mem_axialBall_rotate_iff s a).2 hball
      simpa [axialRotateEquiv] using hrot
    · rw [mem_axialNeighborFinset_iff] at hneigh ⊢
      exact (axialAdjacent_rotate_iff a p).2 hneigh
  · intro hq
    rcases Finset.mem_inter.mp hq with ⟨hballFin, hneigh⟩
    let a : Axial := axialRotateInv q
    apply Finset.mem_map.mpr
    refine ⟨a, ?_, ?_⟩
    · apply Finset.mem_inter.mpr
      constructor
      · have hball : q ∈ axialBall s := by simpa using hballFin
        have hrot : axialRotate a ∈ axialBall s := by
          simpa [a] using hball
        have haBall : a ∈ axialBall s :=
          (mem_axialBall_rotate_iff s a).1 hrot
        simpa using haBall
      · rw [mem_axialNeighborFinset_iff] at hneigh ⊢
        have hrotAdj : AxialAdjacent (axialRotate a) (axialRotate p) := by
          simpa [a] using hneigh
        exact (axialAdjacent_rotate_iff a p).1 hrotAdj
    · simp [a, axialRotateEquiv]

/-- The six-site intersection cardinality is rotation-invariant. -/
theorem card_ball_inter_neighbors_rotate (s : ℕ) (p : Axial) :
    ((axialBall s).toFinset ∩ axialNeighborFinset (axialRotate p)).card =
      ((axialBall s).toFinset ∩ axialNeighborFinset p).card := by
  rw [← map_ball_inter_neighbors_rotate]
  simp

/-- The number of old centred-ball neighbours is rotation-invariant. -/
theorem newAxialNeighborCount_ball_rotate (s : ℕ) (p : Axial) :
    newAxialNeighborCount (axialBall s).get (axialRotate p) =
      newAxialNeighborCount (axialBall s).get p := by
  rw [newAxialNeighborCount_eq_inter_card _ (axialBall_nodup s),
    newAxialNeighborCount_eq_inter_card _ (axialBall_nodup s)]
  exact card_ball_inter_neighbors_rotate s p

end PlanarContactNumber
