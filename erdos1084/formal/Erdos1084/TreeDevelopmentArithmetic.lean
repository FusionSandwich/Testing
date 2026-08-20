import Mathlib

namespace Erdos1084

/-!
# Finite path development bookkeeping for coherent grain trees

A rooted tree gives every grain one unique finite edge path from the root.  The
geometric coherent-continuation maps label those edges by group elements.  This
module formalizes the path-product development and the exact child recursion.
Existence and uniqueness of the root paths in a geometric grain tree remain the
standard graph-theoretic input.
-/

section PathDevelopment

variable {V G : Type*} [Group G]

/-- Product of transition labels along one root path. -/
def transitionWordProduct (word : List G) : G := word.prod

/-- Development potential attached to a chosen root path for every vertex. -/
def pathDevelopment (rootPath : V → List G) (v : V) : G :=
  transitionWordProduct (rootPath v)

/-- An empty root path develops to the identity. -/
theorem pathDevelopment_root
    (rootPath : V → List G) {root : V}
    (hroot : rootPath root = []) :
    pathDevelopment rootPath root = 1 := by
  simp [pathDevelopment, transitionWordProduct, hroot]

/-- Extending the parent path by one transition multiplies the development by that label. -/
theorem pathDevelopment_child
    (rootPath : V → List G)
    {parent child : V} {transition : G}
    (hpath : rootPath child = rootPath parent ++ [transition]) :
    pathDevelopment rootPath child =
      pathDevelopment rootPath parent * transition := by
  simp [pathDevelopment, transitionWordProduct, hpath]

/-- Two vertices with the same root word receive the same development. -/
theorem pathDevelopment_eq_of_path_eq
    (rootPath : V → List G) {u v : V}
    (hpath : rootPath u = rootPath v) :
    pathDevelopment rootPath u = pathDevelopment rootPath v := by
  simp [pathDevelopment, hpath]

/--
A closed path whose transition word has product one is compatible with the
existing development.
-/
theorem pathDevelopment_cycle_closes
    (rootPath : V → List G) {v : V} (cycle : List G)
    (hcycle : cycle.prod = 1) :
    transitionWordProduct (rootPath v ++ cycle) =
      pathDevelopment rootPath v := by
  simp [transitionWordProduct, pathDevelopment, hcycle]

/--
If appending a cycle leaves the development unchanged, the cycle product is the
identity. This is the algebraic holonomy condition.
-/
theorem pathDevelopment_cycle_identity
    (rootPath : V → List G) {v : V} (cycle : List G)
    (hclose : transitionWordProduct (rootPath v ++ cycle) =
      pathDevelopment rootPath v) :
    cycle.prod = 1 := by
  have hmul : (rootPath v).prod * cycle.prod = (rootPath v).prod := by
    simpa [transitionWordProduct, pathDevelopment] using hclose
  exact mul_left_cancel hmul

/-- Reversing a transition is represented by the inverse group element. -/
theorem pathDevelopment_backtrack
    (rootPath : V → List G) {v : V} (transition : G) :
    transitionWordProduct
      (rootPath v ++ [transition, transition⁻¹]) =
      pathDevelopment rootPath v := by
  simp [transitionWordProduct, pathDevelopment]

end PathDevelopment

end Erdos1084
