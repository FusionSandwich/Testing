import Erdos1084.Phase1KissingCoverage

open Erdos1084

example {α : Type*} [DecidableEq α]
    (Far : α → α → Prop) (hSymm : Symmetric Far)
    (C : Finset α) (m : ℕ)
    (hpair : (C : Set α).Pairwise Far)
    (hcard : C.card = m)
    (hbound : ∀ D : Finset α, (D : Set α).Pairwise Far → D.card ≤ m)
    (x : α) (hx : x ∉ C) :
    ∃ c ∈ C, ¬Far x c :=
  coverage_of_sharp_code_bound Far hSymm C m hpair hcard hbound x hx
