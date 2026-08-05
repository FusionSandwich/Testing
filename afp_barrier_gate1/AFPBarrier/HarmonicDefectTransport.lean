import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Module
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Finite algebra for harmonic-defect transport estimates

This file checks the finite algebra used by the P2B error analysis.
It does not claim to formalize matrix exponentials, Bochner integration, trace
theorems, or well-posedness of a streaming--collision PDE.  Those analytic
inputs are explicit hypotheses in the manuscript.  The results below cover:

* a norm estimate for a finite contractive Duhamel sum;
* the resolvent residual identity for an explicitly supplied left inverse;
* exact six-way error telescoping and the associated norm bound;
* the finite transpose identity behind adjoint-weighted residuals;
* coercivity/Young inequalities used by the energy route; and
* geometric contraction bounds for preconditioned iteration.
-/

open scoped BigOperators

namespace AFPBarrier

/-! ## Contractive finite Duhamel sums -/

variable {K V : Type*}
  [Fintype K]
  [SeminormedAddCommGroup V]

/-- A finite Duhamel quadrature inherits the contraction bound term by term.
The continuous Duhamel estimate in the manuscript is the corresponding
Bochner-integral statement; it is not asserted by this theorem. -/
theorem finiteDuhamel_norm_le
    (term : K → V) (kernel : K → ℝ) (residual : ℝ)
    (hterm : ∀ k, ‖term k‖ ≤ kernel k * residual) :
    ‖∑ k, term k‖ ≤ (∑ k, kernel k) * residual := by
  calc
    ‖∑ k, term k‖ ≤ ∑ k, ‖term k‖ := norm_sum_le _ _
    _ ≤ ∑ k, kernel k * residual :=
      Finset.sum_le_sum (fun k _ => hterm k)
    _ = (∑ k, kernel k) * residual := by
      rw [Finset.sum_mul]

/-- The exponential transient kernel is nonnegative for positive target
eigenvalue and nonnegative time. -/
theorem transientKernel_nonneg
    (lambda t : ℝ) (hlambda : 0 < lambda) (ht : 0 ≤ t) :
    0 ≤ (1 - Real.exp (-lambda * t)) / lambda := by
  apply div_nonneg
  · exact sub_nonneg.mpr (Real.exp_le_one_iff.mpr (by nlinarith))
  · exact le_of_lt hlambda

/-! ## Resolvent residual identity -/

section Resolvent

variable [NormedSpace ℝ V]

/-- Algebraic resolvent identity.  `solve` is required only to be a left
inverse of `alpha I - L` at `u`; no spectral theorem is hidden here. -/
theorem resolvent_residual_identity
    (L solve : V →ₗ[ℝ] V) (alpha lambda : ℝ) (u : V)
    (hden : alpha + lambda ≠ 0)
    (hleft : solve (alpha • u - L u) = u) :
    solve u - (alpha + lambda)⁻¹ • u =
      (alpha + lambda)⁻¹ • solve (L u + lambda • u) := by
  have hdecomp :
      u = (alpha + lambda)⁻¹ •
        ((alpha • u - L u) + (L u + lambda • u)) := by
    calc
      u = (alpha + lambda)⁻¹ • ((alpha + lambda) • u) :=
        (inv_smul_smul₀ hden u).symm
      _ = (alpha + lambda)⁻¹ •
          ((alpha • u - L u) + (L u + lambda • u)) := by
        congr 1
        module
  have hsolve :
      solve u = (alpha + lambda)⁻¹ •
        (u + solve (L u + lambda • u)) := by
    calc
      solve u = solve ((alpha + lambda)⁻¹ •
          ((alpha • u - L u) + (L u + lambda • u))) :=
        congrArg solve hdecomp
      _ = (alpha + lambda)⁻¹ •
          (u + solve (L u + lambda • u)) := by
        rw [map_smul, map_add, hleft]
  rw [hsolve]
  module

/-- Solver-independent norm certificate obtained from the resolvent identity
and an explicitly supplied resolvent contraction bound. -/
theorem resolvent_residual_norm_le
    (L solve : V →ₗ[ℝ] V) (alpha lambda : ℝ) (u : V)
    (halpha : 0 < alpha) (hlambda : 0 ≤ lambda)
    (hleft : solve (alpha • u - L u) = u)
    (hcontract : ∀ v, ‖solve v‖ ≤ alpha⁻¹ * ‖v‖) :
    ‖solve u - (alpha + lambda)⁻¹ • u‖ ≤
      (alpha * (alpha + lambda))⁻¹ * ‖L u + lambda • u‖ := by
  have hden : alpha + lambda ≠ 0 := by positivity
  rw [resolvent_residual_identity L solve alpha lambda u hden hleft]
  rw [norm_smul, Real.norm_eq_abs, abs_inv,
    abs_of_pos (by positivity : 0 < alpha + lambda)]
  calc
    (alpha + lambda)⁻¹ * ‖solve (L u + lambda • u)‖ ≤
        (alpha + lambda)⁻¹ * (alpha⁻¹ * ‖L u + lambda • u‖) := by
      exact mul_le_mul_of_nonneg_left
        (hcontract (L u + lambda • u)) (by positivity)
    _ = (alpha * (alpha + lambda))⁻¹ * ‖L u + lambda • u‖ := by
      field_simp

end Resolvent

/-! ## Exact six-way decomposition -/

/-- The six named residual channels telescope exactly.  The names and order
match the P2B manuscript: physical model, angular generator, angular
sampling/quadrature, spatial discretization, energy grouping, and iteration. -/
theorem sixError_telescope
    (physical angular sampling spatial energy iteration reference : V) :
    iteration - reference =
      (physical - reference) +
      (angular - physical) +
      (sampling - angular) +
      (spatial - sampling) +
      (energy - spatial) +
      (iteration - energy) := by
  abel

/-- Triangle bound corresponding to `sixError_telescope`. -/
theorem sixError_norm_le
    (physical angular sampling spatial energy iteration reference : V) :
    ‖iteration - reference‖ ≤
      ‖physical - reference‖ +
      ‖angular - physical‖ +
      ‖sampling - angular‖ +
      ‖spatial - sampling‖ +
      ‖energy - spatial‖ +
      ‖iteration - energy‖ := by
  rw [sixError_telescope]
  calc
    ‖(physical - reference) + (angular - physical) +
        (sampling - angular) + (spatial - sampling) +
        (energy - spatial) + (iteration - energy)‖ ≤
      ‖(physical - reference) + (angular - physical) +
        (sampling - angular) + (spatial - sampling) +
        (energy - spatial)‖ + ‖iteration - energy‖ := norm_add_le _ _
    _ ≤
      (‖(physical - reference) + (angular - physical) +
        (sampling - angular) + (spatial - sampling)‖ +
        ‖energy - spatial‖) + ‖iteration - energy‖ := by
      gcongr
      exact norm_add_le _ _
    _ ≤
      ((‖(physical - reference) + (angular - physical) +
        (sampling - angular)‖ + ‖spatial - sampling‖) +
        ‖energy - spatial‖) + ‖iteration - energy‖ := by
      gcongr
      exact norm_add_le _ _
    _ ≤
      (((‖physical - reference‖ + ‖angular - physical‖) +
        ‖sampling - angular‖) + ‖spatial - sampling‖) +
        ‖energy - spatial‖ + ‖iteration - energy‖ := by
      gcongr
      calc
        ‖(physical - reference) + (angular - physical) +
            (sampling - angular)‖ ≤
            ‖(physical - reference) + (angular - physical)‖ +
              ‖sampling - angular‖ := norm_add_le _ _
        _ ≤ (‖physical - reference‖ + ‖angular - physical‖) +
              ‖sampling - angular‖ := by
          gcongr
          exact norm_add_le _ _
    _ =
      ‖physical - reference‖ + ‖angular - physical‖ +
      ‖sampling - angular‖ + ‖spatial - sampling‖ +
      ‖energy - spatial‖ + ‖iteration - energy‖ := by ring

/-! ## Finite adjoint-weighted residual identity -/

section Adjoint

variable {I : Type*} [Fintype I]

/-- Euclidean pairing on a finite ordinate/spatial/group state. -/
def finitePair (x y : I → ℝ) : ℝ :=
  ∑ i, x i * y i

/-- Finite matrix action. -/
def finiteOperatorApply (A : I → I → ℝ) (x : I → ℝ) (i : I) : ℝ :=
  ∑ j, A i j * x j

/-- Transpose action, written componentwise to keep conventions auditable. -/
def p2bFiniteTransposeApply (A : I → I → ℝ) (z : I → ℝ) (j : I) : ℝ :=
  ∑ i, A i j * z i

/-- Exact finite transpose identity. -/
theorem finitePair_transpose_apply
    (A : I → I → ℝ) (z x : I → ℝ) :
    finitePair (p2bFiniteTransposeApply A z) x =
      finitePair z (finiteOperatorApply A x) := by
  classical
  unfold finitePair p2bFiniteTransposeApply finiteOperatorApply
  calc
    (∑ j, (∑ i, A i j * z i) * x j) =
        ∑ j, ∑ i, (A i j * z i) * x j := by
      apply Finset.sum_congr rfl
      intro j hj
      rw [Finset.sum_mul]
    _ = ∑ i, ∑ j, z i * (A i j * x j) := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro i hi
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = ∑ i, z i * ∑ j, A i j * x j := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Finset.mul_sum]

/-- Exact response representation for an exact finite adjoint and exact
primal residual equation. -/
theorem adjointWeightedResidual_exact
    (A : I → I → ℝ) (z error residual response : I → ℝ)
    (hresidual : residual = finiteOperatorApply A error)
    (hadjoint : response = p2bFiniteTransposeApply A z) :
    finitePair response error = finitePair z residual := by
  rw [hadjoint, hresidual]
  exact finitePair_transpose_apply A z error

/-- Approximate-adjoint error representation.  The second term is the
computable adjoint-residual remainder that must be bounded, not discarded. -/
theorem adjointWeightedResidual_approx
    (A : I → I → ℝ) (z error residual response : I → ℝ)
    (hresidual : residual = finiteOperatorApply A error) :
    finitePair response error =
      finitePair z residual +
        finitePair (fun i => response i - p2bFiniteTransposeApply A z i) error := by
  rw [hresidual]
  rw [← finitePair_transpose_apply A z error]
  unfold finitePair
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  ring

end Adjoint

/-! ## Energy and coercivity inequalities -/

/-- Young absorption in the normalization used by the squared energy route. -/
theorem energyResidual_young
    (kappa error residual : ℝ) (hkappa : 0 < kappa) :
    2 * residual * error ≤
      kappa * error ^ 2 + residual ^ 2 / kappa := by
  have hsquare : 0 ≤ (kappa * error - residual) ^ 2 := sq_nonneg _
  rw [show kappa * error ^ 2 + residual ^ 2 / kappa =
      (kappa ^ 2 * error ^ 2 + residual ^ 2) / kappa by
        field_simp
        ]
  rw [le_div_iff₀ hkappa]
  nlinarith

/-- Coercivity turns a residual upper bound into a steady error estimate. -/
theorem coerciveResidual_bound
    (kappa error residual : ℝ)
    (hkappa : 0 < kappa)
    (hcoercive : kappa * error ≤ residual) :
    error ≤ residual / kappa := by
  exact (le_div_iff₀ hkappa).2 (by simpa [mul_comm] using hcoercive)

/-! ## Preconditioned contraction -/

/-- A preconditioned fixed-point iteration with contraction factor `eta`
has the standard geometric error bound. -/
theorem preconditionedIteration_geometric
    (error : ℕ → ℝ) (eta : ℝ)
    (heta : 0 ≤ eta)
    (hstep : ∀ n, error (n + 1) ≤ eta * error n) :
    ∀ n, error n ≤ eta ^ n * error 0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      calc
        error (n + 1) ≤ eta * error n := hstep n
        _ ≤ eta * (eta ^ n * error 0) :=
          mul_le_mul_of_nonneg_left ih heta
        _ = eta ^ (n + 1) * error 0 := by
          rw [pow_succ]
          ring

/-- Every finite preconditioned Neumann sum is bounded by the full geometric
series when the certified contraction factor lies in `[0,1)`. -/
theorem preconditionedGeometricSeries_le
    (eta : ℝ) (n : ℕ) (heta0 : 0 ≤ eta) (heta1 : eta < 1) :
    ∑ k ∈ Finset.range n, eta ^ k ≤ (1 - eta)⁻¹ := by
  calc
    ∑ k ∈ Finset.range n, eta ^ k ≤ ∑' k : ℕ, eta ^ k :=
      (summable_geometric_of_lt_one heta0 heta1).sum_le_tsum
        (Finset.range n) (fun k _ => pow_nonneg heta0 k)
    _ = (1 - eta)⁻¹ := tsum_geometric_of_lt_one heta0 heta1

end AFPBarrier
