import AFPBarrier.JumpGenerator
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# Quadratic covariance and sampled exactness

This module formalizes the finite algebraic core of the sampled quadratic
exactness theorem.  It proves the product/covariance identity, the exact target
residual with a constant shift, the trace-free projection contraction, the
restricted sampling-map rank-nullity identity, and the row-scaled constraint
implication used by the axial-covariance rigidity theorem.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
variable [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

/-- Bilinear jump variation.  It equals `2 Γ(f,g)` under the convention in the
ordinary theorem document. -/
def jumpCrossVariation
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) : ℝ :=
  (offdiag i).sum (fun j =>
    a i j * (f j - f i) * (g j - g i))

/-- Exact finite product identity. -/
theorem jumpGenerator_product_identity
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => f j * g j) i
      = f i * jumpGenerator a g i
        + g i * jumpGenerator a f i
        + jumpCrossVariation a f g i := by
  classical
  unfold jumpGenerator jumpCrossVariation
  rw [Finset.mul_sum, Finset.mul_sum]
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- A jump generator commutes with multiplication by a scalar. -/
theorem jumpGenerator_const_mul
    (a : ι → ι → ℝ) (c : ℝ) (f : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => c * f j) i
      = c * jumpGenerator a f i := by
  classical
  unfold jumpGenerator
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- A jump generator commutes with a finite coordinate sum. -/
theorem jumpGenerator_fintype_sum
    (a : ι → ι → ℝ) (F : κ → ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => Finset.univ.sum (fun k => F k j)) i
      = Finset.univ.sum (fun k => jumpGenerator a (F k) i) := by
  classical
  unfold jumpGenerator
  calc
    (offdiag i).sum (fun j =>
        a i j *
          (Finset.univ.sum (fun k => F k j)
            - Finset.univ.sum (fun k => F k i)))
      = (offdiag i).sum (fun j =>
          Finset.univ.sum (fun k =>
            a i j * (F k j - F k i))) := by
              apply Finset.sum_congr rfl
              intro j hj
              rw [← Finset.sum_sub_distrib, Finset.mul_sum]
    _ = Finset.univ.sum (fun k =>
          (offdiag i).sum (fun j =>
            a i j * (F k j - F k i))) := by
              rw [Finset.sum_comm]

/-- Quadratic sample associated with a coordinate array and a coefficient
matrix.  Symmetry is not needed for the algebraic identity. -/
def finiteQuadraticSample
    (A : κ → κ → ℝ) (Φ : ι → κ → ℝ) (i : ι) : ℝ :=
  Finset.univ.sum (fun k =>
    Finset.univ.sum (fun l => A k l * Φ i k * Φ i l))

/-- One coordinate entry of the jump covariance tensor. -/
def jumpCovarianceEntry
    (a : ι → ι → ℝ) (Φ : ι → κ → ℝ)
    (i : ι) (k l : κ) : ℝ :=
  jumpCrossVariation a (fun j => Φ j k) (fun j => Φ j l) i

/-- Frobenius contraction of a coefficient matrix with the finite jump
covariance tensor. -/
def quadraticCovarianceContraction
    (A : κ → κ → ℝ) (a : ι → ι → ℝ)
    (Φ : ι → κ → ℝ) (i : ι) : ℝ :=
  Finset.univ.sum (fun k =>
    Finset.univ.sum (fun l => A k l * jumpCovarianceEntry a Φ i k l))

/-- Exact finite covariance identity for a coordinate eigenmap. -/
theorem jumpGenerator_quadratic_covariance_identity
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (Φ : ι → κ → ℝ) (i : ι) (lam : ℝ)
    (heigen : ∀ k,
      jumpGenerator a (fun j => Φ j k) i = -lam * Φ i k) :
    jumpGenerator a (finiteQuadraticSample A Φ) i
      = -2 * lam * finiteQuadraticSample A Φ i
        + quadraticCovarianceContraction A a Φ i := by
  classical
  calc
    jumpGenerator a (finiteQuadraticSample A Φ) i
      = Finset.univ.sum (fun k =>
          jumpGenerator a
            (fun j => Finset.univ.sum (fun l =>
              A k l * Φ j k * Φ j l)) i) := by
                unfold finiteQuadraticSample
                exact jumpGenerator_fintype_sum
                  (a := a)
                  (F := fun k j => Finset.univ.sum (fun l =>
                    A k l * Φ j k * Φ j l))
                  (i := i)
    _ = Finset.univ.sum (fun k =>
          Finset.univ.sum (fun l =>
            jumpGenerator a
              (fun j => A k l * (Φ j k * Φ j l)) i)) := by
                apply Finset.sum_congr rfl
                intro k hk
                simpa [mul_assoc] using
                  (jumpGenerator_fintype_sum
                    (a := a)
                    (F := fun l j => A k l * (Φ j k * Φ j l))
                    (i := i))
    _ = Finset.univ.sum (fun k =>
          Finset.univ.sum (fun l =>
            A k l * jumpGenerator a
              (fun j => Φ j k * Φ j l) i)) := by
                apply Finset.sum_congr rfl
                intro k hk
                apply Finset.sum_congr rfl
                intro l hl
                exact jumpGenerator_const_mul
                  (a := a) (c := A k l)
                  (f := fun j => Φ j k * Φ j l) (i := i)
    _ = Finset.univ.sum (fun k =>
          Finset.univ.sum (fun l =>
            A k l *
              (-2 * lam * (Φ i k * Φ i l)
                + jumpCovarianceEntry a Φ i k l))) := by
                apply Finset.sum_congr rfl
                intro k hk
                apply Finset.sum_congr rfl
                intro l hl
                rw [jumpGenerator_product_identity,
                  heigen k, heigen l]
                unfold jumpCovarianceEntry
                ring
    _ = -2 * lam * finiteQuadraticSample A Φ i
          + quadraticCovarianceContraction A a Φ i := by
                unfold finiteQuadraticSample quadraticCovarianceContraction
                simp_rw [mul_add]
                simp_rw [Finset.sum_add_distrib]
                rw [Finset.mul_sum]
                apply congrArg₂ (· + ·)
                · apply Finset.sum_congr rfl
                  intro k hk
                  rw [Finset.mul_sum]
                  apply Finset.sum_congr rfl
                  intro l hl
                  ring
                · rfl

/-- Exact necessary-and-sufficient residual equation for a shifted quadratic
target eigenmode. -/
theorem quadratic_target_eigen_iff
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (Φ : ι → κ → ℝ) (i : ι) (lam mu c : ℝ)
    (heigen : ∀ k,
      jumpGenerator a (fun j => Φ j k) i = -lam * Φ i k) :
    jumpGenerator a (fun j => finiteQuadraticSample A Φ j - c) i
        = -mu * (finiteQuadraticSample A Φ i - c)
      ↔ quadraticCovarianceContraction A a Φ i
          + (mu - 2 * lam) * finiteQuadraticSample A Φ i
          - mu * c = 0 := by
  rw [jumpGenerator_sub_const]
  rw [jumpGenerator_quadratic_covariance_identity
    (a := a) (A := A) (Φ := Φ) (i := i) (lam := lam) heigen]
  constructor <;> intro h <;> nlinarith

/-- Finite matrix trace. -/
def finiteMatrixTrace (A : κ → κ → ℝ) : ℝ :=
  Finset.univ.sum (fun k => A k k)

/-- Finite Frobenius contraction. -/
def finiteMatrixContraction
    (A T : κ → κ → ℝ) : ℝ :=
  Finset.univ.sum (fun k =>
    Finset.univ.sum (fun l => A k l * T k l))

/-- Subtract a scalar diagonal.  The trace-free projection is obtained by
choosing `c = trace(T) / card(κ)`. -/
def subtractScalarDiagonal
    (T : κ → κ → ℝ) (c : ℝ) (k l : κ) : ℝ :=
  T k l - if k = l then c else 0

/-- Contracting a trace-free matrix is unchanged by subtracting any scalar
diagonal from the other factor. -/
theorem finiteMatrixContraction_subtractScalarDiagonal
    (A T : κ → κ → ℝ) (c : ℝ)
    (htrace : finiteMatrixTrace A = 0) :
    finiteMatrixContraction A (subtractScalarDiagonal T c)
      = finiteMatrixContraction A T := by
  classical
  have hdiag :
      Finset.univ.sum (fun k =>
        Finset.univ.sum (fun l =>
          A k l * (if k = l then c else 0))) = 0 := by
    calc
      Finset.univ.sum (fun k =>
          Finset.univ.sum (fun l =>
            A k l * (if k = l then c else 0)))
        = Finset.univ.sum (fun k => A k k * c) := by
            apply Finset.sum_congr rfl
            intro k hk
            simp
      _ = c * Finset.univ.sum (fun k => A k k) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro k hk
            ring
      _ = 0 := by rw [← finiteMatrixTrace, htrace]; ring
  unfold finiteMatrixContraction subtractScalarDiagonal
  simp_rw [mul_sub]
  simp_rw [Finset.sum_sub_distrib]
  rw [hdiag]
  ring

/-- Coordinate definition of the trace-free projection. -/
noncomputable def finiteTracelessProjection
    (T : κ → κ → ℝ) : κ → κ → ℝ :=
  subtractScalarDiagonal T
    (finiteMatrixTrace T / (Fintype.card κ : ℝ))

/-- Trace-free projection does not change contraction against a trace-free
matrix. -/
theorem finiteMatrixContraction_tracelessProjection
    (A T : κ → κ → ℝ)
    (htrace : finiteMatrixTrace A = 0) :
    finiteMatrixContraction A (finiteTracelessProjection T)
      = finiteMatrixContraction A T := by
  unfold finiteTracelessProjection
  exact finiteMatrixContraction_subtractScalarDiagonal A T _ htrace

section SampledRestrictionDimension

variable {V W : Type*}
variable [AddCommGroup V] [Module ℝ V]
variable [AddCommGroup W] [Module ℝ W]
variable [FiniteDimensional ℝ V]

/-- Rank-nullity for the sampling map restricted to the exact-form subspace.
The range is the genuine sampled exact space and the kernel is the sampling
kernel inside that exact-form subspace. -/
theorem sampledRestriction_finrank
    (S : V →ₗ[ℝ] W) (E : Submodule ℝ V) :
    Module.finrank ℝ (LinearMap.range (S.domRestrict E))
      + Module.finrank ℝ (LinearMap.ker (S.domRestrict E))
      = Module.finrank ℝ E :=
  LinearMap.finrank_range_add_finrank_ker (S.domRestrict E)

end SampledRestrictionDimension

/-- If every form constraint is a nonzero row scaling of the corresponding
sampling functional, zero form residuals are equivalent to zero sampled
values.  This is the finite algebraic core of axial-covariance rigidity. -/
theorem zero_constraints_iff_zero_samples_of_row_scaling
    (constraint sample scale : ι → ℝ)
    (hscale : ∀ i, scale i ≠ 0)
    (hrow : ∀ i, constraint i = scale i * sample i) :
    (∀ i, constraint i = 0) ↔ (∀ i, sample i = 0) := by
  constructor
  · intro hconstraint i
    have hzero : scale i * sample i = 0 := by
      rw [← hrow i]
      exact hconstraint i
    exact (mul_eq_zero.mp hzero).resolve_left (hscale i)
  · intro hsample i
    rw [hrow i, hsample i, mul_zero]

/-- Scalar coefficient forced by the trace identity in an axially isotropic
covariance decomposition. -/
theorem axialCovariance_projectionCoefficient
    (d tau beta : ℝ)
    (hd : d - 1 ≠ 0)
    (htrace : (d - 1) * tau + beta = 2 * (d - 1)) :
    beta - tau + 2 = d * beta / (d - 1) := by
  field_simp [hd]
  nlinarith

end AFPBarrier
