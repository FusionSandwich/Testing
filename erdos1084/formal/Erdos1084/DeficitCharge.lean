import Mathlib

namespace Erdos1084

/-- The elementary affine inequality behind the missing-contact charge. -/
theorem local_affine_charge
    {H q δ : ℝ}
    (hH : 0 ≤ H)
    (hδ : 1 ≤ δ) :
    H + δ * q ≤ δ * (H + q) := by
  nlinarith

/-- Arithmetic form of the degree-sum conversion. -/
theorem degree_sum_arithmetic (n E : ℤ) :
    12 * n - 2 * E = 2 * (6 * n - E) := by
  ring

/-- Summing local exposed-area bounds preserves the common charge coefficient. -/
theorem sum_local_charges
    {ι : Type*} [Fintype ι]
    (exposure deficit : ι → ℝ)
    (Λ : ℝ)
    (hlocal : ∀ i, exposure i ≤ Λ * deficit i) :
    (∑ i, exposure i) ≤ Λ * ∑ i, deficit i := by
  calc
    (∑ i, exposure i) ≤ ∑ i, Λ * deficit i :=
      Finset.sum_le_sum fun i _ => hlocal i
    _ = Λ * ∑ i, deficit i := by
      rw [Finset.mul_sum]

/-- The strict surface lower bound and the global surface charge imply a deficit bound. -/
theorem surface_to_deficit
    {A Λ D : ℝ}
    (hΛ : 0 < Λ)
    (hSurface : A < 2 * Λ * D) :
    A / (2 * Λ) < D := by
  have hden : 0 < 2 * Λ := by positivity
  exact (div_lt_iff₀ hden).2 (by nlinarith)

/-- Abstract final algebraic step used by the manuscript. -/
theorem contact_upper_from_deficit
    {n E c x : ℝ}
    (hD : c * x < 6 * n - E) :
    E < 6 * n - c * x := by
  linarith

end Erdos1084
