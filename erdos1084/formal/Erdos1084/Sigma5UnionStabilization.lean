import Mathlib

namespace Erdos1084

/-!
# Sigma-5 [001] two-lattice transition stabilization

This module checks the finite Bellman certificate for the coincidence-periodic transition model
whose candidate sites are the union of the two ideal FCC lattices. The geometric reconstruction
of the quotient graph is checked independently by exact arithmetic in `Q(sqrt 5)` in the
canonical Math repository.

The theorem is deliberately scoped to the two-lattice candidate class. Off-lattice transition
sites are not represented.
-/

def sigma5IntraEdges : Array (Nat × Nat) := #[
  (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
  (1, 2), (1, 3), (1, 4), (1, 7),
  (2, 3), (2, 4), (2, 8),
  (3, 4), (4, 9),
  (5, 6), (5, 7), (5, 8), (5, 9),
  (6, 7), (6, 8), (6, 9),
  (7, 8), (7, 9), (8, 9)
]

def sigma5AdjacentEdges : Array (Nat × Nat) := #[
  (0, 0), (0, 1), (0, 2), (0, 3),
  (1, 1), (1, 2), (1, 3), (1, 4),
  (2, 0), (2, 2), (2, 3), (2, 4),
  (3, 0), (3, 1), (3, 3), (3, 4),
  (4, 0), (4, 1), (4, 2), (4, 4),
  (5, 5), (5, 6), (5, 7), (5, 9),
  (6, 5), (6, 6), (6, 7), (6, 8),
  (7, 6), (7, 7), (7, 8), (7, 9),
  (8, 5), (8, 7), (8, 8), (8, 9),
  (9, 5), (9, 6), (9, 8), (9, 9)
]

def sigma5AdjacentConflicts : Array (Nat × Nat) := #[
  (5, 0), (5, 1), (5, 3), (6, 2),
  (7, 1), (7, 3), (7, 4),
  (8, 0), (8, 3), (8, 4),
  (9, 0), (9, 1), (9, 4)
]

def sigma5Bit (mask index : Nat) : Nat :=
  if mask.testBit index then 1 else 0

def sigma5StateSize (mask : Nat) : Nat :=
  ((List.range 10).map fun i => sigma5Bit mask i).sum

def sigma5IntraContacts (mask : Nat) : Nat :=
  sigma5IntraEdges.foldl
    (fun total edge => total + sigma5Bit mask edge.1 * sigma5Bit mask edge.2) 0

def sigma5AdjacentContacts (first second : Nat) : Nat :=
  sigma5AdjacentEdges.foldl
    (fun total edge => total + sigma5Bit first edge.1 * sigma5Bit second edge.2) 0

def sigma5Compatible (first second : Nat) : Bool :=
  sigma5AdjacentConflicts.all
    (fun edge => !(first.testBit edge.1 && second.testBit edge.2))

def sigma5TransitionCost (first second : Nat) : Nat :=
  6 * sigma5StateSize second -
    sigma5IntraContacts second -
    sigma5AdjacentContacts first second

/-- Lower bulk layer: all five lower-lattice sites and no upper-lattice sites. -/
def sigma5LowerBulk : Nat := 31

/-- Upper bulk layer: no lower-lattice sites and all five upper-lattice sites. -/
def sigma5UpperBulk : Nat := 992

/-- Mixed abrupt layer: all ten candidate sites. -/
def sigma5MixedLayer : Nat := 1023

/--
Compact form of the exact shortest-path/Bellman potential.

The exact Dijkstra reconstruction gives `transitionCost lowerBulk state` for every state except
`992` and `996`. Those two exceptional values are recorded explicitly.
-/
def sigma5PotentialValue (state : Nat) : Nat :=
  if state = sigma5UpperBulk then 16
  else if state = 996 then 19
  else sigma5TransitionCost sigma5LowerBulk state

def sigma5NonnegativeCheck : Bool :=
  (List.range 1024).all fun first =>
    (List.range 1024).all fun second =>
      if sigma5Compatible first second then
        decide
          (sigma5IntraContacts second + sigma5AdjacentContacts first second ≤
            6 * sigma5StateSize second)
      else true

def sigma5BellmanCheck : Bool :=
  (List.range 1024).all fun first =>
    (List.range 1024).all fun second =>
      if sigma5Compatible first second then
        decide
          (sigma5PotentialValue second ≤
            sigma5PotentialValue first + sigma5TransitionCost first second)
      else true

theorem sigma5_transition_cost_nonnegative : sigma5NonnegativeCheck = true := by
  native_decide

theorem sigma5_bellman_certificate : sigma5BellmanCheck = true := by
  native_decide

theorem sigma5_lower_bulk_potential :
    sigma5PotentialValue sigma5LowerBulk = 0 := by
  native_decide

theorem sigma5_upper_bulk_potential :
    sigma5PotentialValue sigma5UpperBulk = 16 := by
  native_decide

theorem sigma5_exceptional_state_potential :
    sigma5PotentialValue 996 = 19 := by
  native_decide

theorem sigma5_abrupt_witness :
    sigma5Compatible sigma5LowerBulk sigma5MixedLayer = true ∧
    sigma5Compatible sigma5MixedLayer sigma5UpperBulk = true ∧
    sigma5TransitionCost sigma5LowerBulk sigma5MixedLayer = 16 ∧
    sigma5TransitionCost sigma5MixedLayer sigma5UpperBulk = 0 := by
  native_decide

end Erdos1084
