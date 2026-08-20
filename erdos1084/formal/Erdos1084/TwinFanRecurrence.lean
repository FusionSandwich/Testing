import Mathlib

namespace Erdos1084

/-!
# Constant-angle recurrence for a coherent-twin edge fan

In a transverse plane, successive coherent face lines satisfy
`α_{k+1} = 2 α_k - α_{k-1}`.  This module proves that their angle increments
are constant and that finite closure forces an integer relation between the
sector angle and `π`.  The external number-theoretic input is that the FCC twin
angle with cosine `±1/3` is not a rational multiple of `π`.
-/

/-- A zero second difference makes every first difference equal to the initial one. -/
theorem fanAngle_difference_constant
    (α : ℕ → ℝ)
    (hrec : ∀ k : ℕ,
      α (k + 2) - α (k + 1) = α (k + 1) - α k) :
    ∀ k : ℕ, α (k + 1) - α k = α 1 - α 0 := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
      calc
        α (k + 1 + 1) - α (k + 1)
            = α (k + 2) - α (k + 1) := by congr 2 <;> omega
        _ = α (k + 1) - α k := hrec k
        _ = α 1 - α 0 := ih

/-- Exact arithmetic-progression formula for the face-line angles. -/
theorem fanAngle_eq_initial_add
    (α : ℕ → ℝ)
    (hrec : ∀ k : ℕ,
      α (k + 2) - α (k + 1) = α (k + 1) - α k) :
    ∀ k : ℕ,
      α k = α 0 + (k : ℝ) * (α 1 - α 0) := by
  have hdiff := fanAngle_difference_constant α hrec
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
      have hk := hdiff k
      calc
        α (k + 1) = α k + (α (k + 1) - α k) := by ring
        _ = α k + (α 1 - α 0) := by rw [hk]
        _ = α 0 + ((k + 1 : ℕ) : ℝ) * (α 1 - α 0) := by
          rw [ih]
          push_cast
          ring

/-- Finite return of the same unoriented line forces an integer `π` relation. -/
theorem finiteFanClosure_implies_angle_relation
    (α : ℕ → ℝ)
    (hrec : ∀ k : ℕ,
      α (k + 2) - α (k + 1) = α (k + 1) - α k)
    (m : ℕ) (q : ℤ)
    (hclosure : α m = α 0 + (q : ℝ) * Real.pi) :
    (m : ℝ) * (α 1 - α 0) = (q : ℝ) * Real.pi := by
  have hm := fanAngle_eq_initial_add α hrec m
  linarith

/--
If the initial sector angle has no nonzero integer relation with `π`, a finite
nontrivial fan cannot return to its initial line.
-/
theorem no_finiteFanClosure_of_no_angle_relation
    (α : ℕ → ℝ)
    (hrec : ∀ k : ℕ,
      α (k + 2) - α (k + 1) = α (k + 1) - α k)
    (hirr : ∀ (m : ℕ) (q : ℤ), 0 < m →
      (m : ℝ) * (α 1 - α 0) ≠ (q : ℝ) * Real.pi) :
    ∀ (m : ℕ) (q : ℤ), 0 < m →
      α m ≠ α 0 + (q : ℝ) * Real.pi := by
  intro m q hm hclosure
  exact hirr m q hm
    (finiteFanClosure_implies_angle_relation α hrec m q hclosure)

end Erdos1084
