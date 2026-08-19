import Mathlib

namespace Erdos1084

/-!
# Scalar geometry of tangent-neighbor hidden caps

These lemmas isolate the algebra behind the geometric statements

`|r u - 2 v| ≤ r  ↔  u·v ≥ 1/r`

for unit vectors, and the angular separation of two contact directions.  The norm/inner-product
identities themselves are standard Euclidean calculations; the potentially error-prone division
and factor-of-two steps are checked here.
-/

/-- The expanded squared-distance inequality is exactly the hidden-cap threshold. -/
theorem phase1_hidden_cap_scalar_iff {r z : ℝ} (hr : 0 < r) :
    r ^ 2 + 4 - 4 * r * z ≤ r ^ 2 ↔ 1 / r ≤ z := by
  have hdiv : 1 / r ≤ z ↔ 1 ≤ z * r := by
    simpa [one_div] using (div_le_iff₀ hr : (1 : ℝ) / r ≤ z ↔ 1 ≤ z * r)
  rw [hdiv]
  constructor <;> intro h <;> nlinarith

/-- Strict version of the hidden-cap threshold. -/
theorem phase1_hidden_cap_scalar_lt_iff {r z : ℝ} (hr : 0 < r) :
    r ^ 2 + 4 - 4 * r * z < r ^ 2 ↔ 1 / r < z := by
  have hdiv : 1 / r < z ↔ 1 < z * r := by
    simpa [one_div] using (div_lt_iff₀ hr : (1 : ℝ) / r < z ↔ 1 < z * r)
  rw [hdiv]
  constructor <;> intro h <;> nlinarith

/-- Unit-direction separation: squared chord distance at least one forces dot product at most `1/2`. -/
theorem phase1_contact_direction_dot_le_half {z : ℝ}
    (hsep : 1 ≤ 2 - 2 * z) :
    z ≤ 1 / 2 := by
  linarith

/-- Converse scalar identity used to translate a dot-product bound into chord separation. -/
theorem phase1_one_le_chord_sq_of_dot_le_half {z : ℝ}
    (hdot : z ≤ 1 / 2) :
    1 ≤ 2 - 2 * z := by
  linarith

end Erdos1084
