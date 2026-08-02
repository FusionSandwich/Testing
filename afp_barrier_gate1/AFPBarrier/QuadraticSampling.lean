import AFPBarrier.QuadraticCovariance
import Mathlib.LinearAlgebra.FiniteDimensional.Basic

/-!
# Sampling kernels and exact sampled modes

These definitions deliberately distinguish an algebraic form from its sampled
function.  The residual factors through sampling, so every sampling alias is
vacuously form-exact.
-/

namespace AFPBarrier

variable {ι σ : Type*} [Fintype ι]

/-- The residual map `(T + mu I) o S`, written pointwise. -/
def sampledResidual
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (S : σ → (ι → ℝ)) (A : σ) (i : ι) : ℝ :=
  T (S A) i + mu * S A i

/-- An algebraic form is exact when its sampled residual vanishes. -/
def formExact
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (S : σ → (ι → ℝ)) (A : σ) : Prop :=
  ∀ i, sampledResidual T mu S A i = 0

/-- The pointwise sampling kernel. -/
def inSamplingKernel (S : σ → (ι → ℝ)) (A : σ) : Prop :=
  ∀ i, S A i = 0

/-- A function is genuinely sampled exact if it is the sample of an exact
algebraic form. -/
def sampledExact
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (S : σ → (ι → ℝ)) (f : ι → ℝ) : Prop :=
  ∃ A, formExact T mu S A ∧ S A = f

/-- Exact factorization of the residual through sampling. -/
theorem sampledResidual_factorization
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (S : σ → (ι → ℝ)) (A : σ) :
    sampledResidual T mu S A = fun i => T (S A) i + mu * S A i := rfl

/-- The sampling kernel is contained in the form-exact space. -/
theorem samplingKernel_subset_formExact
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (hT0 : T (fun _ => 0) = fun _ => 0)
    (S : σ → (ι → ℝ)) (A : σ)
    (hA : inSamplingKernel S A) :
    formExact T mu S A := by
  intro i
  have hfun : S A = fun _ => 0 := funext hA
  simp [sampledResidual, hfun, hT0]

/-- The genuinely sampled exact functions are precisely sampled functions in
the target eigenspace. -/
theorem sampledExact_iff_range_inter_targetKernel
    (T : (ι → ℝ) → (ι → ℝ)) (mu : ℝ)
    (S : σ → (ι → ℝ)) (f : ι → ℝ) :
    sampledExact T mu S f ↔
      (∃ A, S A = f) ∧ (∀ i, T f i + mu * f i = 0) := by
  constructor
  · rintro ⟨A, hA, rfl⟩
    exact ⟨⟨A, rfl⟩, hA⟩
  · rintro ⟨⟨A, hAf⟩, hf⟩
    refine ⟨A, ?_, hAf⟩
    intro i
    simpa [formExact, sampledResidual, hAf] using hf i

section Linear

variable {V W : Type*} [AddCommGroup V] [Module ℝ V]
  [AddCommGroup W] [Module ℝ W]

/-- Linear residual map `(T + mu I) o S`. -/
def linearSampledResidual
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) : V →ₗ[ℝ] W :=
  (T + mu • LinearMap.id).comp S

/-- Linear sampling aliases lie in the residual kernel. -/
theorem linear_samplingKernel_le_residualKernel
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    LinearMap.ker S ≤ LinearMap.ker (linearSampledResidual T mu S) := by
  intro A hA
  simp [linearSampledResidual, hA]

/-- Consequently the residual rank cannot exceed the sampling rank. -/
theorem linearSampledResidual_finrank_le_sampling
    [FiniteDimensional ℝ V] [FiniteDimensional ℝ W]
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    Module.finrank ℝ (LinearMap.range (linearSampledResidual T mu S)) ≤
      Module.finrank ℝ (LinearMap.range S) := by
  exact LinearMap.finrank_range_le_of_ker_le
    (linear_samplingKernel_le_residualKernel T mu S)

end Linear

end AFPBarrier
