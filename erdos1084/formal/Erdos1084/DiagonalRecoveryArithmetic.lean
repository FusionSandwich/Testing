import Mathlib

namespace Erdos1084

/-!
# Arithmetic bridge for diagonal coherent-twin recovery

For one fixed finite twin word, geometric constructions may produce constants
`A`, `B`, and `C` such that the total transition cost at macroscopic scale `T`
is bounded by

`A*T + B + C*angle*T²`.

This module proves the normalized estimate and the epsilon bookkeeping.  The
geometric construction of the constants and the terminal boundary mechanism
remain explicit hypotheses.
-/

/-- Normalize a line, point, and angular area contribution by `T²`. -/
theorem recoveryCost_surfaceDensity_bound
    {T A B C angle cost : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T + B + C * angle * T ^ 2) :
    cost / T ^ 2 ≤ A / T + B / T ^ 2 + C * angle := by
  have hT2 : 0 < T ^ 2 := sq_pos_of_pos hT
  apply (div_le_iff₀ hT2).2
  calc
    cost ≤ A * T + B + C * angle * T ^ 2 := hcost
    _ = (A / T + B / T ^ 2 + C * angle) * T ^ 2 := by
      field_simp [ne_of_gt hT]
      ring

/-- Three component estimates of size `ε/3` give total normalized cost at most `ε`. -/
theorem recoveryCost_surfaceDensity_le_epsilon
    {T A B C angle cost ε : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T + B + C * angle * T ^ 2)
    (hline : A / T ≤ ε / 3)
    (hpoint : B / T ^ 2 ≤ ε / 3)
    (hangle : C * angle ≤ ε / 3) :
    cost / T ^ 2 ≤ ε := by
  have hnormalized := recoveryCost_surfaceDensity_bound hT hcost
  linarith

/-- Strict component estimates give a strict total estimate. -/
theorem recoveryCost_surfaceDensity_lt_epsilon
    {T A B C angle cost ε : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T + B + C * angle * T ^ 2)
    (hline : A / T < ε / 3)
    (hpoint : B / T ^ 2 < ε / 3)
    (hangle : C * angle < ε / 3) :
    cost / T ^ 2 < ε := by
  have hnormalized := recoveryCost_surfaceDensity_bound hT hcost
  linarith

/--
A word-dependent finite line constant can always be made smaller than a target
surface tolerance once a sufficiently large scale is supplied.
-/
theorem lineTerm_small_of_scale
    {A T ε : ℝ}
    (hT : 0 < T)
    (hscale : 3 * A < ε * T) :
    A / T < ε / 3 := by
  have hthree : (0 : ℝ) < 3 := by norm_num
  have hεT : A * 3 < ε * T := by linarith
  have hdiv : A < ε * T / 3 := by
    exact (lt_div_iff₀ hthree).2 (by simpa [mul_comm] using hεT)
  exact (div_lt_iff₀ hT).2 <| by
    calc
      A < ε * T / 3 := hdiv
      _ = (ε / 3) * T := by ring

/-- A word-dependent finite point constant is negligible at sufficiently large `T²`. -/
theorem pointTerm_small_of_scale
    {B T ε : ℝ}
    (hT : 0 < T)
    (hscale : 3 * B < ε * T ^ 2) :
    B / T ^ 2 < ε / 3 := by
  have hT2 : 0 < T ^ 2 := sq_pos_of_pos hT
  have hthree : (0 : ℝ) < 3 := by norm_num
  have hdiv : B < ε * T ^ 2 / 3 := by
    exact (lt_div_iff₀ hthree).2 (by nlinarith)
  exact (div_lt_iff₀ hT2).2 <| by
    calc
      B < ε * T ^ 2 / 3 := hdiv
      _ = (ε / 3) * T ^ 2 := by ring

/-- Combine explicit scale and angular conditions into the diagonal epsilon estimate. -/
theorem diagonalRecovery_lt_epsilon
    {T A B C angle cost ε : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T + B + C * angle * T ^ 2)
    (hlineScale : 3 * A < ε * T)
    (hpointScale : 3 * B < ε * T ^ 2)
    (hangle : C * angle < ε / 3) :
    cost / T ^ 2 < ε := by
  apply recoveryCost_surfaceDensity_lt_epsilon hT hcost
  · exact lineTerm_small_of_scale hT hlineScale
  · exact pointTerm_small_of_scale hT hpointScale
  · exact hangle

end Erdos1084
