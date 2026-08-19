import Mathlib

namespace Erdos1084

/-!
# Abstract coverage consequence of a sharp finite-code bound

The degree-twelve step uses only the following logic: if every separated code has cardinality at
most twelve, then a separated twelve-point code is maximal, so every additional point fails the
separation condition with one of its members.  The large geometric theorem is the cardinality
bound; the maximality-to-coverage deduction is elementary and is checked here.
-/

/-- A sharp cardinality bound turns a saturated code into a covering code. -/
theorem coverage_of_sharp_code_bound
    {α : Type*} [DecidableEq α]
    (Far : α → α → Prop)
    (hSymm : Symmetric Far)
    (C : Finset α) (m : ℕ)
    (hpair : (C : Set α).Pairwise Far)
    (hcard : C.card = m)
    (hbound : ∀ D : Finset α, (D : Set α).Pairwise Far → D.card ≤ m)
    (x : α) (hx : x ∉ C) :
    ∃ c ∈ C, ¬Far x c := by
  by_contra hnone
  push_neg at hnone
  have hinsert : ((insert x C : Finset α) : Set α).Pairwise Far := by
    intro a ha b hb hab
    simp only [Finset.coe_insert, Set.mem_insert_iff] at ha hb
    rcases ha with rfl | haC
    · rcases hb with rfl | hbC
      · exact (hab rfl).elim
      · exact hnone b hbC
    · rcases hb with rfl | hbC
      · exact hSymm (hnone a haC)
      · exact hpair haC hbC hab
  have hlarge := hbound (insert x C) hinsert
  rw [Finset.card_insert_of_not_mem hx, hcard] at hlarge
  omega

/-- Version allowing the proposed point already to belong to the code. -/
theorem mem_or_not_far_of_sharp_code_bound
    {α : Type*} [DecidableEq α]
    (Far : α → α → Prop)
    (hSymm : Symmetric Far)
    (C : Finset α) (m : ℕ)
    (hpair : (C : Set α).Pairwise Far)
    (hcard : C.card = m)
    (hbound : ∀ D : Finset α, (D : Set α).Pairwise Far → D.card ≤ m)
    (x : α) :
    x ∈ C ∨ ∃ c ∈ C, ¬Far x c := by
  by_cases hx : x ∈ C
  · exact Or.inl hx
  · exact Or.inr
      (coverage_of_sharp_code_bound Far hSymm C m hpair hcard hbound x hx)

end Erdos1084
