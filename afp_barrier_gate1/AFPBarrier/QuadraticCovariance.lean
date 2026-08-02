import AFPBarrier.JumpGenerator
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# Quadratic covariance and sampled exactness

This module formalizes the finite algebraic core of the sampled quadratic
exactness theorem. It proves the product/covariance identity, arbitrary shifted
product residuals, centered and uncentered additive resonance, the exact
quadratic target residual, trace-free projection contraction, the
sampling/residual factorization consequences, restricted-map rank-nullity, and
the row-scaled constraint implication used by axial-covariance rigidity.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
variable [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

/-- Bilinear jump variation. It equals `2 Γ(f,g)` under the convention in the
ordinary theorem document. -/
def jumpCrossVariation
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) : ℝ :=
  (offdiag i).sum (fun j =>
    a i j * (f j - f i) * (g j - g i))

/-- The bilinear carré du champ with the conventional factor `1/2`. -/
noncomputable def jumpGamma
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) : ℝ :=
  (1 / 2 : ℝ) * jumpCrossVariation a f g i

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

/-- Product identity written using the conventional carré du champ. -/
theorem jumpGenerator_product_identity_gamma
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => f j * g j) i
      = f i * jumpGenerator a g i
        + g i * jumpGenerator a f i
        + 2 * jumpGamma a f g i := by
  rw [jumpGenerator_product_identity]
  unfold jumpGamma
  ring

/-- Exact arbitrary-target residual for a shifted product of two eigenfunctions. -/
theorem jumpGenerator_shifted_product_residual
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι)
    (lam nu mu c : ℝ)
    (hf : jumpGenerator a f i = -lam * f i)
    (hg : jumpGenerator a g i = -nu * g i) :
    jumpGenerator a (fun j => f j * g j - c) i
        + mu * (f i * g i - c)
      = 2 * jumpGamma a f g i
        + (mu - lam - nu) * (f i * g i)
        - mu * c := by
  rw [jumpGenerator_sub_const]
  rw [jumpGenerator_product_identity_gamma, hf, hg]
  ring

/-- Necessary and sufficient arbitrary-target equation for a shifted product. -/
theorem shifted_product_target_iff
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι)
    (lam nu mu c : ℝ)
    (hf : jumpGenerator a f i = -lam * f i)
    (hg : jumpGenerator a g i = -nu * g i) :
    jumpGenerator a (fun j => f j * g j - c) i
        = -mu * (f i * g i - c)
      ↔ 2 * jumpGamma a f g i
          + (mu - lam - nu) * (f i * g i)
          - mu * c = 0 := by
  have hres := jumpGenerator_shifted_product_residual
    (a := a) (f := f) (g := g) (i := i)
    (lam := lam) (nu := nu) (mu := mu) (c := c) hf hg
  constructor <;> intro h <;> nlinarith

/-- At additive resonance, a centered product is exact exactly when its
carré du champ is the corresponding constant. -/
theorem additive_product_resonance_iff
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι)
    (lam nu c : ℝ)
    (hf : jumpGenerator a f i = -lam * f i)
    (hg : jumpGenerator a g i = -nu * g i) :
    jumpGenerator a (fun j => f j * g j - c) i
        = -(lam + nu) * (f i * g i - c)
      ↔ 2 * jumpGamma a f g i = (lam + nu) * c := by
  have htarget := shifted_product_target_iff
    (a := a) (f := f) (g := g) (i := i)
    (lam := lam) (nu := nu) (mu := lam + nu) (c := c) hf hg
  constructor
  · intro h
    have hz := htarget.mp h
    nlinarith
  · intro h
    apply htarget.mpr
    nlinarith

/-- A centered square propagates at the doubled eigenvalue exactly when its
pointwise carré du champ is the constant `lam * c`. -/
theorem centered_square_resonance_iff
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam c : ℝ)
    (hf : jumpGenerator a f i = -lam * f i) :
    jumpGenerator a (fun j => (f j) ^ 2 - c) i
        = -2 * lam * ((f i) ^ 2 - c)
      ↔ jumpGamma a f f i = lam * c := by
  have hproduct := additive_product_resonance_iff
    (a := a) (f := f) (g := f) (i := i)
    (lam := lam) (nu := lam) (c := c) hf hf
  constructor
  · intro h
    have hmul :
        jumpGenerator a (fun j => f j * f j - c) i
          = -(lam + lam) * (f i * f i - c) := by
      simpa [pow_two, two_mul] using h
    have hgamma := hproduct.mp hmul
    nlinarith
  · intro h
    have hgamma :
        2 * jumpGamma a f f i = (lam + lam) * c := by
      nlinarith
    have hmul := hproduct.mpr hgamma
    simpa [pow_two, two_mul] using hmul

/-- The uncentered square is the `c=0` specialization of centered resonance. -/
theorem uncentered_square_resonance_iff_zero_gamma
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam : ℝ)
    (hf : jumpGenerator a f i = -lam * f i) :
    jumpGenerator a (fun j => (f j) ^ 2) i
        = -2 * lam * (f i) ^ 2
      ↔ jumpGamma a f f i = 0 := by
  simpa using centered_square_resonance_iff
    (a := a) (f := f) (i := i) (lam := lam) (c := 0) hf

/-- Self cross-variation is the project's square carré du champ. -/
theorem jumpCrossVariation_self_eq_carreDuChamp
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) :
    jumpCrossVariation a f f i = carreDuChamp a f i := by
  classical
  unfold jumpCrossVariation carreDuChamp
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- For nonnegative rates and a nonzero eigenvalue, an uncentered square at the
additive eigenvalue forces the sampled eigenfunction value to vanish at that
state. On an irreducible positive chain, applying this at every state gives the
usual zero-function obstruction. -/
theorem uncentered_square_resonance_forces_value_zero
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlam : lam ≠ 0)
    (hf : jumpGenerator a f i = -lam * f i)
    (hsquare :
      jumpGenerator a (fun j => (f j) ^ 2) i
        = -2 * lam * (f i) ^ 2) :
    f i = 0 := by
  have hgamma : jumpGamma a f f i = 0 :=
    (uncentered_square_resonance_iff_zero_gamma
      (a := a) (f := f) (i := i) (lam := lam) hf).mp hsquare
  have hcross : jumpCrossVariation a f f i = 0 := by
    unfold jumpGamma at hgamma
    nlinarith
  have hcarre : carreDuChamp a f i = 0 := by
    rw [← jumpCrossVariation_self_eq_carreDuChamp]
    exact hcross
  have hgenerator : jumpGenerator a f i = 0 :=
    zero_carreDuChamp_forces_generator_zero
      (a := a) (f := f) (i := i) ha hcarre
  rw [hf] at hgenerator
  have hproduct : lam * f i = 0 := by nlinarith
  exact (mul_eq_zero.mp hproduct).resolve_left hlam

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
matrix. Symmetry is not needed for the algebraic identity. -/
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

/-- Subtract a scalar diagonal. The trace-free projection is obtained by
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

section SamplingResidualFactorization

variable {V W Z : Type*}
variable [AddCommGroup V] [Module ℝ V]
variable [AddCommGroup W] [Module ℝ W]
variable [AddCommGroup Z] [Module ℝ Z]

/-- If the residual map factors through sampling, every sampling alias is an
exact form. This is the abstract inclusion `K_X ⊆ E_form`. -/
theorem samplingKernel_le_residualKernel
    (S : V →ₗ[ℝ] W) (B : W →ₗ[ℝ] Z) :
    LinearMap.ker S ≤ LinearMap.ker (B.comp S) := by
  intro x hx
  change B (S x) = 0
  rw [show S x = 0 from hx]
  exact map_zero B

/-- The sampled exact range is exactly the sampled range intersected with the
target eigenspace/kernel of the residual operator. -/
theorem sampledRange_exact_eq_range_inf_ker
    (S : V →ₗ[ℝ] W) (B : W →ₗ[ℝ] Z) :
    LinearMap.range
        (S.domRestrict (LinearMap.ker (B.comp S)))
      = LinearMap.range S ⊓ LinearMap.ker B := by
  apply le_antisymm
  · intro y hy
    rcases hy with ⟨x, hx⟩
    refine ⟨⟨x.1, hx⟩, ?_⟩
    have hxker := x.2
    change B (S x.1) = 0 at hxker
    change B y = 0
    rw [← hx]
    exact hxker
  · intro y hy
    rcases hy.1 with ⟨x, hx⟩
    refine ⟨⟨x, ?_⟩, hx⟩
    have hyker := hy.2
    change B y = 0 at hyker
    change B (S x) = 0
    rw [hx]
    exact hyker

end SamplingResidualFactorization

/-- If every form constraint is a nonzero row scaling of the corresponding
sampling functional, zero form residuals are equivalent to zero sampled
values. This is the finite algebraic core of axial-covariance rigidity. -/
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
