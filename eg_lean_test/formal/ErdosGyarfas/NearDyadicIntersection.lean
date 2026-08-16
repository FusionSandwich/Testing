import Mathlib

namespace ErdosGyarfas

/-- Arithmetic core of the equal near-dyadic theta rule.  If two cycles of
length `2^k+1` share a theta path of length `t`, and the complementary deficit
`2^k+1-t` equals `2^j`, then the third theta cycle has length `2^(j+1)`. -/
theorem equal_near_dyadic_forbidden_overlap
    (k j t : Nat) (hdeficit : t + 2 ^ j = 2 ^ k + 1) :
    2 * (2 ^ k + 1) - 2 * t = 2 ^ (j + 1) := by
  calc
    2 * (2 ^ k + 1) - 2 * t = 2 * 2 ^ j := by omega
    _ = 2 ^ (j + 1) := by simp [pow_succ, Nat.mul_comm]

/-- The previously isolated shared-edge rule is the case `t=1`, `j=k`. -/
theorem equal_near_dyadic_shared_edge_again (k : Nat) :
    2 * (2 ^ k + 1) - 2 = 2 ^ (k + 1) := by
  simpa using equal_near_dyadic_forbidden_overlap k k 1 (by omega)

end ErdosGyarfas
