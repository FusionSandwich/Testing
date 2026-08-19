import Mathlib

namespace Erdos1084

/-!
# Abstract closure of the normalized-deficit limit

This file formalizes the final logical step of the unrestricted Wulff program.  A matching
surface-order liminf theorem and recovery theorem imply convergence of the normalized minimum
energies.  The geometric Gamma-convergence and grain-boundary coercivity statements remain
explicit hypotheses.
-/

/-- Elementary epsilon definition of convergence for a real sequence. -/
def HasRealSequenceLimit (a : ℕ → ℝ) (c : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ n : ℕ, N ≤ n → |a n - c| < ε

/-- Eventual two-sided surface-order estimates around a candidate Wulff coefficient. -/
structure MatchingSurfaceBounds (a : ℕ → ℝ) (c : ℝ) : Prop where
  lower : ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ n : ℕ, N ≤ n → c - ε < a n
  upper : ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ n : ℕ, N ≤ n → a n < c + ε

/-- Matching liminf and recovery estimates force the full limit. -/
theorem hasRealSequenceLimit_of_matchingSurfaceBounds
    {a : ℕ → ℝ} {c : ℝ}
    (h : MatchingSurfaceBounds a c) :
    HasRealSequenceLimit a c := by
  intro ε hε
  obtain ⟨N₁, hN₁⟩ := h.lower ε hε
  obtain ⟨N₂, hN₂⟩ := h.upper ε hε
  refine ⟨max N₁ N₂, ?_⟩
  intro n hn
  have hn₁ : N₁ ≤ n := le_trans (le_max_left _ _) hn
  have hn₂ : N₂ ≤ n := le_trans (le_max_right _ _) hn
  have hl := hN₁ n hn₁
  have hu := hN₂ n hn₂
  rw [abs_lt]
  constructor <;> linarith

/--
Abstract unrestricted Wulff input.

`a n` is the normalized contact deficit.  The lower field represents crystallization,
Gamma-liminf, and interface coercivity.  The upper field represents an explicit FCC Wulff
recovery sequence plus interpolation to every sufficiently large particle number.
-/
structure UnrestrictedWulffInput (a : ℕ → ℝ) (cFcc : ℝ) : Prop where
  matching : MatchingSurfaceBounds a cFcc

/-- The unrestricted Wulff hypotheses identify the normalized-deficit limit. -/
theorem unrestricted_normalized_deficit_limit
    {a : ℕ → ℝ} {cFcc : ℝ}
    (h : UnrestrictedWulffInput a cFcc) :
    HasRealSequenceLimit a cFcc :=
  hasRealSequenceLimit_of_matchingSurfaceBounds h.matching

/-- A strict asymptotic phase gap transfers from coefficient cubes to coefficients. -/
theorem positive_cube_gap_implies_positive_coefficient_gap
    {c₁ c₂ : ℝ}
    (h₁ : 0 ≤ c₁) (h₂ : 0 ≤ c₂)
    (hCube : c₁ ^ 3 < c₂ ^ 3) :
    c₁ < c₂ := by
  by_contra hnot
  have hle : c₂ ≤ c₁ := le_of_not_gt hnot
  have hdiff : 0 ≤ c₁ - c₂ := sub_nonneg.mpr hle
  have hsum : 0 ≤ c₁ ^ 2 + c₁ * c₂ + c₂ ^ 2 := by positivity
  have hprod : 0 ≤ (c₁ - c₂) * (c₁ ^ 2 + c₁ * c₂ + c₂ ^ 2) :=
    mul_nonneg hdiff hsum
  have hCubeLe : c₂ ^ 3 ≤ c₁ ^ 3 := by nlinarith
  exact (not_lt_of_ge hCubeLe) hCube

end Erdos1084
