import Mathlib

namespace ErdosGyarfas

/-- A positive even degree at most three must be two. This is the arithmetic
core of the fact that an Eulerian support with ambient maximum degree three
has no branching vertex. -/
theorem positive_even_le_three
    (d : Nat) (hpos : 0 < d) (heven : Even d) (hle : d ≤ 3) :
    d = 2 := by
  rcases heven with ⟨k, hk⟩
  omega

/-- A positive even degree which is not two is at least four. -/
theorem branching_even_degree_at_least_four
    (d : Nat) (hpos : 0 < d) (heven : Even d) (hne : d ≠ 2) :
    4 ≤ d := by
  rcases heven with ⟨k, hk⟩
  omega

/-- Branch lengths of the exact-`q` four-theta obstruction. -/
def exactQThetaBranches (q : Nat) : List Nat := [2, 3, 3, q - 8]

/-- The six simple-cycle lengths of the exact-`q` four-theta obstruction. -/
def exactQThetaCycleLengths (q : Nat) : List Nat :=
  [5, 5, 6, q - 6, q - 5, q - 5]

theorem exactQTheta_total_edges (q : Nat) (hq : 8 ≤ q) :
    (exactQThetaBranches q).sum = q := by
  simp [exactQThetaBranches]
  omega

/-- Every proper two-branch Eulerian subsupport has fewer than `q` edges. -/
theorem exactQTheta_pair_sums_lt_q (q : Nat) (hq : 16 ≤ q) :
    2 + 3 < q ∧
    3 + 3 < q ∧
    2 + (q - 8) < q ∧
    3 + (q - 8) < q := by
  omega

/-- The two large cycle lengths lie strictly between `q/2` and `q` once
`q ≥ 16`. For dyadic `q`, this is the arithmetic gap excluding powers of two. -/
theorem exactQTheta_large_cycle_bounds (q : Nat) (hq : 16 ≤ q) :
    q / 2 < q - 6 ∧ q - 6 < q ∧
    q / 2 < q - 5 ∧ q - 5 < q := by
  omega

/-- Executable bounded power-of-two predicate used only for finite certificate
checks; generic dyadic-gap reasoning is stated separately in the proof note. -/
def isPowerOfTwoThrough (maxExponent n : Nat) : Bool :=
  (List.range (maxExponent + 1)).any fun k => n == 2 ^ k

theorem exactQTheta_no_power_cycles_q16 :
    (exactQThetaCycleLengths 16).all
      (fun n => !(isPowerOfTwoThrough 16 n)) = true := by
  native_decide

theorem exactQTheta_no_power_cycles_q32 :
    (exactQThetaCycleLengths 32).all
      (fun n => !(isPowerOfTwoThrough 32 n)) = true := by
  native_decide

theorem exactQTheta_no_power_cycles_q64 :
    (exactQThetaCycleLengths 64).all
      (fun n => !(isPowerOfTwoThrough 64 n)) = true := by
  native_decide

theorem exactQTheta_no_power_cycles_q128 :
    (exactQThetaCycleLengths 128).all
      (fun n => !(isPowerOfTwoThrough 128 n)) = true := by
  native_decide

end ErdosGyarfas
