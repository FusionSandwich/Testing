import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Tactic.Module

/-!
# Finite algebra for fixed-point-preserving AFP acceleration

This file checks only the stable linear algebra used by P2D.  It does not
formalize GMRES convergence, transport traces, field-of-values estimates, or
physical Boltzmann-to-Fokker--Planck approximation hypotheses.
-/

namespace AFPBarrier

variable {V W : Type*} [AddCommGroup V] [AddCommGroup W]
  [Module ℝ V] [Module ℝ W]

/-- A residual correction using any linear low-order inverse leaves an exact
high-order solution fixed. -/
theorem residualCorrection_fixedPoint
    (A B : V →ₗ[ℝ] V) (b x : V) (omega : ℝ)
    (hfixed : A x = b) :
    x + omega • B (b - A x) = x := by
  rw [hfixed, sub_self, map_zero, smul_zero, add_zero]

/-- Exact error-propagation identity for residual correction. -/
theorem residualCorrection_error
    (A B : V →ₗ[ℝ] V) (b x xstar : V) (omega : ℝ)
    (hfixed : A xstar = b) :
    (x + omega • B (b - A x)) - xstar =
      (x - xstar) - omega • B (A (x - xstar)) := by
  subst b
  simp only [map_sub]
  module

/-- If every low-order correction lies in the kernel of a declared balance
functional, every intermediate iterate preserves that balance exactly. -/
theorem residualCorrection_preservesConstraint
    (A B : V →ₗ[ℝ] V) (Q : V →ₗ[ℝ] W)
    (b x : V) (omega : ℝ)
    (hQB : ∀ v, Q (B v) = 0) :
    Q (x + omega • B (b - A x)) = Q x := by
  rw [map_add, map_smul, hQB, smul_zero, add_zero]

/-- In a common scalar shell, the correction factor is exactly
`1 - omega * aH / aL`. -/
theorem scalarShell_errorFactor
    (aH aL omega e : ℝ) (haL : aL ≠ 0) :
    e - omega * (aH * e / aL) = (1 - omega * aH / aL) * e := by
  field_simp

end AFPBarrier
