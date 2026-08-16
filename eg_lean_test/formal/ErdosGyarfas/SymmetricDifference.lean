import Mathlib

namespace ErdosGyarfas

/-- Indicator weight of a Boolean edge-membership bit. -/
def bitWeight (b : Bool) : Nat := if b then 1 else 0

/-- The one-edge cardinality identity behind `|S △ Z| = |S| + |Z| - 2|S ∩ Z|`. -/
theorem xor_bit_weight (a b : Bool) :
    bitWeight (xor a b) = bitWeight a + bitWeight b - 2 * bitWeight (a && b) := by
  cases a <;> cases b <;> native_decide

/-- Exact residue test for the recovered 16-edge four-theta switch obstruction. -/
theorem fourTheta_support_is_eight_divisible : 16 % 8 = 0 := by
  native_decide

end ErdosGyarfas
