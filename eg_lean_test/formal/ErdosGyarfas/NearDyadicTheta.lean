import Mathlib

namespace ErdosGyarfas

/-- Two cycles of length `2^k+1` sharing exactly one theta path edge have a
third-cycle length equal to the next power of two. This theorem records the
arithmetic core; graph-theoretic hypotheses are handled separately. -/
theorem equal_near_dyadic_shared_edge (k : Nat) :
    2 * (2 ^ k + 1) - 2 = 2 ^ (k + 1) := by
  calc
    2 * (2 ^ k + 1) - 2 = 2 * 2 ^ k := by omega
    _ = 2 ^ (k + 1) := by simp [pow_succ, Nat.mul_comm]

end ErdosGyarfas
