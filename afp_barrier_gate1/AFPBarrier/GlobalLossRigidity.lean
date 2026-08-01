import Mathlib.Tactic

/-!
# Global propagation of local equality

The local rate--defect equality theorem says that every strictly active edge at
a vertex has one common loss `lambda / rate(i)`.  In a reversible graph, an
active edge is active in both directions and its geometric loss is symmetric.
Consequently the two endpoint rates agree.  Connectivity propagates this to a
single global rate and a single active-edge loss.

This theorem is abstract and does not depend on AFP terminology.  It is a
supporting rigidity result; a publishable classification still requires extra
geometric hypotheses such as spherical triangulation.
-/

namespace AFPBarrier

variable {ι : Type*}

/-- One shared active edge forces its endpoint rates to agree. -/
theorem rate_eq_of_symmetric_active_loss
    (active : ι → ι → Prop)
    (loss : ι → ι → ℝ)
    (rate : ι → ℝ)
    (lam : ℝ)
    (hLam : 0 < lam)
    (hRate : ∀ i, 0 < rate i)
    (hActiveSymm : ∀ {i j}, active i j → active j i)
    (hLossSymm : ∀ i j, loss i j = loss j i)
    (hLocal : ∀ {i j}, active i j → loss i j = lam / rate i)
    {i j : ι}
    (hij : active i j) :
    rate i = rate j := by
  have hji : active j i := hActiveSymm hij
  have hi := hLocal hij
  have hj := hLocal hji
  have hquot : lam / rate i = lam / rate j := by
    calc
      lam / rate i = loss i j := hi.symm
      _ = loss j i := hLossSymm i j
      _ = lam / rate j := hj
  have hri : rate i ≠ 0 := ne_of_gt (hRate i)
  have hrj : rate j ≠ 0 := ne_of_gt (hRate j)
  field_simp [hri, hrj] at hquot
  nlinarith

/-- Equality of rates propagates along the reflexive transitive closure of the
active-edge relation. -/
theorem rate_eq_of_active_reflTransGen
    (active : ι → ι → Prop)
    (loss : ι → ι → ℝ)
    (rate : ι → ℝ)
    (lam : ℝ)
    (hLam : 0 < lam)
    (hRate : ∀ i, 0 < rate i)
    (hActiveSymm : ∀ {i j}, active i j → active j i)
    (hLossSymm : ∀ i j, loss i j = loss j i)
    (hLocal : ∀ {i j}, active i j → loss i j = lam / rate i)
    {i j : ι}
    (hpath : Relation.ReflTransGen active i j) :
    rate i = rate j := by
  induction hpath with
  | refl => rfl
  | tail hprefix hedge ih =>
      exact ih.trans <|
        rate_eq_of_symmetric_active_loss
          active loss rate lam hLam hRate hActiveSymm hLossSymm hLocal hedge

/-- On a connected active graph, all rates and all active-edge losses are
controlled by one chosen root rate. -/
theorem connected_active_loss_rigidity
    (active : ι → ι → Prop)
    (loss : ι → ι → ℝ)
    (rate : ι → ℝ)
    (lam : ℝ)
    (root : ι)
    (hLam : 0 < lam)
    (hRate : ∀ i, 0 < rate i)
    (hActiveSymm : ∀ {i j}, active i j → active j i)
    (hLossSymm : ∀ i j, loss i j = loss j i)
    (hLocal : ∀ {i j}, active i j → loss i j = lam / rate i)
    (hConnected : ∀ j, Relation.ReflTransGen active root j) :
    (∀ j, rate j = rate root) ∧
      (∀ {i j}, active i j → loss i j = lam / rate root) := by
  have hglobalRate : ∀ j, rate j = rate root := by
    intro j
    exact (rate_eq_of_active_reflTransGen
      active loss rate lam hLam hRate hActiveSymm hLossSymm hLocal
      (hConnected j)).symm
  constructor
  · exact hglobalRate
  · intro i j hij
    calc
      loss i j = lam / rate i := hLocal hij
      _ = lam / rate root := by rw [hglobalRate i]

end AFPBarrier
