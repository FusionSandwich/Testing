import Mathlib

namespace ErdosGyarfas

/-- Arithmetic core of the doubled-lobe argument: if doubling either component
cannot reduce the vertex count, the two component orders are equal. -/
theorem doubled_lobes_force_equal_orders
    (c₁ c₂ n : Nat)
    (hsum : c₁ + c₂ + 1 = n)
    (h₁ : n ≤ 2 * c₁ + 1)
    (h₂ : n ≤ 2 * c₂ + 1) :
    c₁ = c₂ := by
  omega

/-- Lexicographic edge-minimality then forces equal lobe edge counts. -/
theorem doubled_lobes_force_equal_edges
    (e₁ e₂ m : Nat)
    (hsum : e₁ + e₂ = m)
    (h₁ : m ≤ 2 * e₁)
    (h₂ : m ≤ 2 * e₂) :
    e₁ = e₂ := by
  omega

end ErdosGyarfas
