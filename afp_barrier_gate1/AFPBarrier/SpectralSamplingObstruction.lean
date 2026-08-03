import Mathlib.Algebra.DirectSum.Module
import Mathlib.LinearAlgebra.DFinsupp
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# Finite spectral sampling obstruction

This module isolates the finite-dimensional statement used by the sampled
harmonic hierarchy.  The essential hypothesis is injectivity of the *target
eigenvalue* map.  Distinct degrees alone are insufficient in dimension one.
-/

open scoped BigOperators DirectSum

namespace AFPBarrier

variable {J W : Type*}
  [Fintype J] [DecidableEq J]
  [AddCommGroup W] [Module ℝ W]

/-- Subspaces on which one operator acts at pairwise distinct scalars form an
independent family.  `iSupIndep` is the precise internal-direct-sum assertion
inside their span; it does not incorrectly require that the spaces span `W`. -/
theorem spectralSampledSpaces_iSupIndep
    (L : Module.End ℝ W) (mu : J → ℝ) (V : J → Submodule ℝ W)
    (hmu : Function.Injective mu)
    (hV : ∀ j, V j ≤ L.eigenspace (mu j)) :
    iSupIndep V := by
  exact (L.eigenspaces_iSupIndep.comp hmu).mono hV

/-- In particular, different sampled target spaces have zero intersection. -/
theorem spectralSampledSpaces_pairwise_disjoint
    (L : Module.End ℝ W) (mu : J → ℝ) (V : J → Submodule ℝ W)
    (hmu : Function.Injective mu)
    (hV : ∀ j, V j ≤ L.eigenspace (mu j)) :
    Pairwise fun i j => Disjoint (V i) (V j) :=
  (spectralSampledSpaces_iSupIndep L mu V hmu hV).pairwiseDisjoint

/-- The sum of the sampled ranks cannot exceed the ambient dimension. -/
theorem spectralSampledSpaces_finrank_sum_le
    [FiniteDimensional ℝ W]
    (L : Module.End ℝ W) (mu : J → ℝ) (V : J → Submodule ℝ W)
    (hmu : Function.Injective mu)
    (hV : ∀ j, V j ≤ L.eigenspace (mu j)) :
    ∑ j, Module.finrank ℝ (V j) ≤ Module.finrank ℝ W := by
  let total : (⨁ j, V j) →ₗ[ℝ] W :=
    DFinsupp.lsum ℕ fun j => (V j).subtype
  have hind := spectralSampledSpaces_iSupIndep L mu V hmu hV
  have hinjective : Function.Injective total := by
    dsimp only [total]
    exact hind.dfinsupp_lsum_injective
  have hfinrank := LinearMap.finrank_le_finrank_of_injective hinjective
  simpa only [Module.finrank_directSum] using hfinrank

/-- Rank bound for sampled functions on a finite state space. -/
theorem spectralSampledFunctions_finrank_sum_le
    {I : Type*} [Fintype I]
    (L : Module.End ℝ (I → ℝ))
    (mu : J → ℝ) (V : J → Submodule ℝ (I → ℝ))
    (hmu : Function.Injective mu)
    (hV : ∀ j, V j ≤ L.eigenspace (mu j)) :
    ∑ j, Module.finrank ℝ (V j) ≤ Fintype.card I := by
  simpa only [Module.finrank_pi] using
    spectralSampledSpaces_finrank_sum_le L mu V hmu hV

/-- The continuous spherical target eigenvalue in coordinate dimension `d`. -/
def sphericalEigenvalue (d ell : ℕ) : ℝ :=
  (ell : ℝ) * ((ell : ℝ) + (d : ℝ) - 2)

/-- For `d ≥ 2`, different harmonic degrees have different continuous
spherical eigenvalues. -/
theorem sphericalEigenvalue_injective
    {d : ℕ} (hd : 2 ≤ d) :
    Function.Injective (sphericalEigenvalue d) := by
  intro ell m hvalue
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlm | hml
  · have hell_nonneg : 0 ≤ (ell : ℝ) := Nat.cast_nonneg ell
    have hm_nonneg : 0 ≤ (m : ℝ) := Nat.cast_nonneg m
    have hd_real : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd
    have hlm_real : (ell : ℝ) < (m : ℝ) := by exact_mod_cast hlm
    have hm_one : (1 : ℝ) ≤ (m : ℝ) := by
      exact_mod_cast (Nat.succ_le_iff.mpr (Nat.zero_lt_of_lt hlm))
    have hfactor :
        0 < ((m : ℝ) - (ell : ℝ)) *
          ((m : ℝ) + (ell : ℝ) + (d : ℝ) - 2) := by
      apply mul_pos (sub_pos.mpr hlm_real)
      nlinarith
    dsimp only [sphericalEigenvalue] at hvalue
    nlinarith
  · have hell_nonneg : 0 ≤ (ell : ℝ) := Nat.cast_nonneg ell
    have hm_nonneg : 0 ≤ (m : ℝ) := Nat.cast_nonneg m
    have hd_real : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd
    have hml_real : (m : ℝ) < (ell : ℝ) := by exact_mod_cast hml
    have hell_one : (1 : ℝ) ≤ (ell : ℝ) := by
      exact_mod_cast (Nat.succ_le_iff.mpr (Nat.zero_lt_of_lt hml))
    have hfactor :
        0 < ((ell : ℝ) - (m : ℝ)) *
          ((ell : ℝ) + (m : ℝ) + (d : ℝ) - 2) := by
      apply mul_pos (sub_pos.mpr hml_real)
      nlinarith
    dsimp only [sphericalEigenvalue] at hvalue
    nlinarith

/-- Harmonic-degree specialization of the direct-sum theorem.  The explicit
`d ≥ 2` assumption excludes the dimension-one collision. -/
theorem harmonicSampledSpaces_iSupIndep
    {d : ℕ} (hd : 2 ≤ d)
    (degree : J → ℕ) (hdegree : Function.Injective degree)
    (L : Module.End ℝ W) (V : J → Submodule ℝ W)
    (hV : ∀ j,
      V j ≤ L.eigenspace (-(sphericalEigenvalue d (degree j)))) :
    iSupIndep V := by
  apply spectralSampledSpaces_iSupIndep L
    (fun j => -(sphericalEigenvalue d (degree j))) V
  · intro j k h
    apply hdegree
    apply sphericalEigenvalue_injective hd
    exact neg_injective h
  · exact hV

/-- The literal dimension-one degree formulation is rejected: degrees zero
and one have the same target scalar. -/
theorem sphericalEigenvalue_dimension_one_collision :
    sphericalEigenvalue 1 0 = sphericalEigenvalue 1 1 := by
  norm_num [sphericalEigenvalue]

theorem sphericalEigenvalue_dimension_one_not_injective :
    ¬ Function.Injective (sphericalEigenvalue 1) := by
  intro h
  have := h sphericalEigenvalue_dimension_one_collision
  norm_num at this

/-! ## Converse signed construction -/

/-- Conjugate coordinatewise scalar multiplication on an internal direct sum
back to the ambient space.  Matrix off-diagonal entries of this endomorphism
give signed jump rates whenever constants are assigned scalar zero. -/
noncomputable def internalScalarOperator
    (V : J → Submodule ℝ W) (mu : J → ℝ)
    (hinternal : DirectSum.IsInternal V) : Module.End ℝ W :=
  let e : (⨁ j, V j) ≃ₗ[ℝ] W :=
    LinearEquiv.ofBijective (DirectSum.coeLinearMap V) hinternal
  e.toLinearMap.comp
    ((DFinsupp.mapRange.linearMap fun j =>
      mu j • (LinearMap.id : V j →ₗ[ℝ] V j)).comp e.symm.toLinearMap)

/-- The constructed operator has the prescribed scalar action on each
summand. -/
theorem internalScalarOperator_apply_of_mem
    (V : J → Submodule ℝ W) (mu : J → ℝ)
    (hinternal : DirectSum.IsInternal V)
    (j : J) (x : W) (hx : x ∈ V j) :
    internalScalarOperator V mu hinternal x = mu j • x := by
  let e : (⨁ j, V j) ≃ₗ[ℝ] W :=
    LinearEquiv.ofBijective (DirectSum.coeLinearMap V) hinternal
  have he : e.symm x = DirectSum.of (fun j => V j) j ⟨x, hx⟩ := by
    apply DFinsupp.ext
    intro k
    apply Subtype.ext
    by_cases hkj : k = j
    · subst k
      rw [show e.symm x j = ⟨x, hx⟩ by
        simpa only [e] using
          hinternal.ofBijective_coeLinearMap_of_mem hx]
      simp
    · have hjk : j ≠ k := Ne.symm hkj
      rw [show e.symm x k = 0 by
        simpa only [e] using
          hinternal.ofBijective_coeLinearMap_of_mem_ne hjk hx]
      simp [DirectSum.of_apply, hjk]
  change (DirectSum.coeLinearMap V)
      ((DFinsupp.mapRange.linearMap fun j =>
        mu j • (LinearMap.id : V j →ₗ[ℝ] V j)) (e.symm x)) = _
  rw [he]
  rw [DFinsupp.mapRange.linearMap_apply]
  change (DirectSum.coeLinearMap V)
      (DFinsupp.mapRange
        (fun i x => (mu i • (LinearMap.id : V i →ₗ[ℝ] V i)) x)
        (fun i => (mu i • (LinearMap.id : V i →ₗ[ℝ] V i)).map_zero)
        (DFinsupp.single j ⟨x, hx⟩)) = _
  rw [DFinsupp.mapRange_single]
  change (DirectSum.coeLinearMap V)
      (DirectSum.of (fun i => V i) j
        ((mu j • (LinearMap.id : V j →ₗ[ℝ] V j)) ⟨x, hx⟩)) = _
  rw [DirectSum.coeLinearMap_of]
  simp

/-- A distinguished zero-scalar summand is annihilated. -/
theorem internalScalarOperator_eq_zero_of_mem_zeroSummand
    (V : J → Submodule ℝ W) (mu : J → ℝ)
    (hinternal : DirectSum.IsInternal V)
    (j0 : J) (hmu0 : mu j0 = 0) (x : W) (hx : x ∈ V j0) :
    internalScalarOperator V mu hinternal x = 0 := by
  rw [internalScalarOperator_apply_of_mem V mu hinternal j0 x hx, hmu0,
    zero_smul]

/-- Constants are conserved when they are explicitly included in the
zero-scalar summand.  This prevents the converse construction from silently
forgetting degree zero. -/
theorem internalScalarOperator_constants_eq_zero
    {I : Type*}
    (V : J → Submodule ℝ (I → ℝ)) (mu : J → ℝ)
    (hinternal : DirectSum.IsInternal V)
    (j0 : J) (hmu0 : mu j0 = 0)
    (hconstants : ∀ c : ℝ, (fun _ : I => c) ∈ V j0)
    (c : ℝ) :
    internalScalarOperator V mu hinternal (fun _ : I => c) = 0 := by
  exact internalScalarOperator_eq_zero_of_mem_zeroSummand
    V mu hinternal j0 hmu0 _ (hconstants c)

end AFPBarrier
