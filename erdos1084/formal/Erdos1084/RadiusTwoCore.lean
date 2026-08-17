import Mathlib

namespace Erdos1084

/--
The final cancellation in the radius-two proof. The variable `x` stands for
`n^(2/3)`, while `A` is the enlarged-union boundary area and `D = 6n-E`.
-/
theorem radiusTwo_surface_to_deficit
    {x A D : ℝ}
    (hLower : 4 * Real.pi * x ≤ A)
    (hUpper : A < (12 * Real.pi / 5) * D) :
    (5 / 3 : ℝ) * x < D := by
  have hchain : 4 * Real.pi * x < (12 * Real.pi / 5) * D :=
    lt_of_le_of_lt hLower hUpper
  have hpiineq :
      Real.pi * (4 * x) < Real.pi * ((12 / 5 : ℝ) * D) := by
    calc
      Real.pi * (4 * x) = 4 * Real.pi * x := by ring
      _ < (12 * Real.pi / 5) * D := hchain
      _ = Real.pi * ((12 / 5 : ℝ) * D) := by ring
  have hcancel : 4 * x < (12 / 5 : ℝ) * D :=
    (mul_lt_mul_left Real.pi_pos).mp hpiineq
  nlinarith

/-- Contact-number form of the final deficit inequality. -/
theorem radiusTwo_contact_upper
    {n E x : ℝ}
    (hDeficit : (5 / 3 : ℝ) * x < 6 * n - E) :
    E < 6 * n - (5 / 3 : ℝ) * x := by
  linarith

end Erdos1084
