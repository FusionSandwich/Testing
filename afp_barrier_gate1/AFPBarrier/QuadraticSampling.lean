import AFPBarrier.QuadraticCovariance
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

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
  have hSA : S A = 0 := LinearMap.mem_ker.mp hA
  simp [linearSampledResidual, hSA]

/-- Consequently the residual rank cannot exceed the sampling rank. -/
theorem linearSampledResidual_finrank_le_sampling
    [FiniteDimensional ℝ V] [FiniteDimensional ℝ W]
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    Module.finrank ℝ (LinearMap.range (linearSampledResidual T mu S)) ≤
      Module.finrank ℝ (LinearMap.range S) := by
  have hs := LinearMap.finrank_range_add_finrank_ker S
  have hr := LinearMap.finrank_range_add_finrank_ker
    (linearSampledResidual T mu S)
  have hk := Submodule.finrank_mono
    (linear_samplingKernel_le_residualKernel T mu S)
  omega

/-- The subspace of genuinely sampled exact functions.  Its domain is the
residual kernel (exact algebraic forms), not the whole coefficient space. -/
def linearSampledExactRange
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) : Submodule ℝ W :=
  LinearMap.range
    (S.domRestrict (LinearMap.ker (linearSampledResidual T mu S)))

/-- The genuinely sampled exact space is the intersection of the sampling
range with the target kernel. -/
theorem linearSampledExactRange_eq_range_inf_targetKernel
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    linearSampledExactRange T mu S =
      LinearMap.range S ⊓ LinearMap.ker (T + mu • LinearMap.id) := by
  apply le_antisymm
  · rintro y ⟨x, rfl⟩
    refine ⟨LinearMap.mem_range_self S x.1, ?_⟩
    exact x.2
  · rintro y ⟨⟨x, rfl⟩, hy⟩
    refine ⟨⟨x, ?_⟩, rfl⟩
    exact hy

/-- Rank-nullity on exact forms, with the restricted kernel identified with
the original sampling kernel. -/
theorem linearSampledExactRange_finrank_add_samplingKernel
    [FiniteDimensional ℝ V]
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    Module.finrank ℝ (linearSampledExactRange T mu S) +
        Module.finrank ℝ (LinearMap.ker S) =
      Module.finrank ℝ
        (LinearMap.ker (linearSampledResidual T mu S)) := by
  let E : Submodule ℝ V := LinearMap.ker (linearSampledResidual T mu S)
  have hkernel : LinearMap.ker S ≤ E := by
    exact linear_samplingKernel_le_residualKernel T mu S
  have hrestricted :
      Module.finrank ℝ (LinearMap.ker (S.domRestrict E)) =
        Module.finrank ℝ (LinearMap.ker S) := by
    rw [LinearMap.ker_domRestrict]
    exact (Submodule.comapSubtypeEquivOfLe hkernel).finrank_eq
  have hrank := LinearMap.finrank_range_add_finrank_ker (S.domRestrict E)
  simpa [linearSampledExactRange, E, hrestricted] using hrank

/-- First requested dimension formula:
`dim E_sample = dim E_form - dim K_X`. -/
theorem linearSampledExactRange_finrank_eq_formExact_sub_samplingKernel
    [FiniteDimensional ℝ V]
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    Module.finrank ℝ (linearSampledExactRange T mu S) =
      Module.finrank ℝ
          (LinearMap.ker (linearSampledResidual T mu S)) -
        Module.finrank ℝ (LinearMap.ker S) := by
  have h := linearSampledExactRange_finrank_add_samplingKernel T mu S
  omega

/-- Second requested dimension formula:
`dim E_sample = rank S_X - rank R_X`. -/
theorem linearSampledExactRange_finrank_eq_samplingRank_sub_residualRank
    [FiniteDimensional ℝ V]
    (T : W →ₗ[ℝ] W) (mu : ℝ) (S : V →ₗ[ℝ] W) :
    Module.finrank ℝ (linearSampledExactRange T mu S) =
      Module.finrank ℝ (LinearMap.range S) -
        Module.finrank ℝ
          (LinearMap.range (linearSampledResidual T mu S)) := by
  have he := linearSampledExactRange_finrank_add_samplingKernel T mu S
  have hs := LinearMap.finrank_range_add_finrank_ker S
  have hr := LinearMap.finrank_range_add_finrank_ker
    (linearSampledResidual T mu S)
  omega

end Linear

end AFPBarrier
