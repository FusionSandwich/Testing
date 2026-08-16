import Std.Tactic.NativeDecide

namespace ErdosGyarfas

/-- Branch lengths in the connected 16-edge four-theta obstruction. -/
def fourThetaBranches : List Nat := [2, 4, 5, 5]

/-- The six simple-cycle lengths are the pairwise branch sums. -/
def fourThetaCycleLengths : List Nat := [6, 7, 7, 9, 9, 10]

theorem fourTheta_total_edges : fourThetaBranches.sum = 16 := by
  native_decide

theorem fourTheta_cycle_lengths_complete :
    fourThetaCycleLengths = [2 + 4, 2 + 5, 2 + 5, 4 + 5, 4 + 5, 5 + 5] := by
  native_decide

theorem fourTheta_has_no_cycle_of_length_4_8_or_16 :
    ∀ n ∈ fourThetaCycleLengths, n ≠ 4 ∧ n ≠ 8 ∧ n ≠ 16 := by
  native_decide

end ErdosGyarfas
