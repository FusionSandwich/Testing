import Mathlib

namespace ErdosGyarfas

/-- Once bridges exclude one attachment and minimality excludes three or more,
a cutvertex component has exactly two attachment edges. -/
theorem attachment_count_eq_two
    (t : Nat) (hbridge : 2 ≤ t) (hproper : ¬ 3 ≤ t) :
    t = 2 := by
  omega

/-- Once a cutvertex has at least two components and minimality excludes three
or more, it has exactly two components. -/
theorem cut_component_count_eq_two
    (r : Nat) (hcut : 2 ≤ r) (hproper : ¬ 3 ≤ r) :
    r = 2 := by
  omega

/-- Two attachment edges from each of two components give root degree four. -/
theorem two_lobes_root_degree_four
    (t₁ t₂ : Nat) (h₁ : t₁ = 2) (h₂ : t₂ = 2) :
    t₁ + t₂ = 4 := by
  omega

/-- The doubled rooted lobe has the same order precisely in the equality case. -/
theorem doubled_lobe_order
    (c n : Nat) (h : n = 2 * c + 1) :
    2 * c + 1 = n := by
  omega

end ErdosGyarfas
