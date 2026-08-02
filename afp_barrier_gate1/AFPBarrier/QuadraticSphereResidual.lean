import AFPBarrier.QuadraticSampling
import Mathlib.LinearAlgebra.Matrix.Symmetric
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# Unit-sphere quadratic residual

This is a deliberately coordinate-indexed formalization. It defines the
symmetric trace-free coefficient space, the sampling and residual maps, and
the projected covariance matrices without introducing a tensor library.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I K : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype K] [DecidableEq K]

/-- Symmetric finite real matrices as a linear subspace. -/
def symmetricMatrices (K : Type*) [Fintype K] :
    Submodule ℝ (Matrix K K ℝ) where
  carrier := {A | A.IsSymm}
  zero_mem' := Matrix.isSymm_zero
  add_mem' hA hB := hA.add hB
  smul_mem' c A hA := hA.smul c

/-- The coefficient space `Sym₀(K)`. -/
def symmetricTraceFreeMatrices (K : Type*) [Fintype K] :
    Submodule ℝ (Matrix K K ℝ) :=
  symmetricMatrices K ⊓
    LinearMap.ker (Matrix.traceLinearMap K ℝ ℝ)

/-- Entrywise Frobenius contraction. -/
def matrixFrobeniusPairing (A B : Matrix K K ℝ) : ℝ :=
  ∑ p, ∑ q, A p q * B p q

/-- Frobenius contraction agrees with the trace-product convention when the
right matrix is symmetric. -/
theorem matrixFrobeniusPairing_eq_trace_mul_of_isSymm_right
    (A B : Matrix K K ℝ) (hB : B.IsSymm) :
    matrixFrobeniusPairing A B = (A * B).trace := by
  unfold matrixFrobeniusPairing Matrix.trace
  simp only [Matrix.diag_apply, Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro p hp
  apply Finset.sum_congr rfl
  intro q hq
  rw [hB.apply]

/-- Coordinate jump covariance `C_i`. -/
def jumpCovarianceMatrix
    (a : I → I → ℝ) (x : I → K → ℝ) (i : I) : Matrix K K ℝ :=
  fun p q => (offdiag i).sum fun j =>
    a i j * (x j p - x i p) * (x j q - x i q)

/-- Coordinate trace-free projection `P₀`. -/
noncomputable def traceFreeProjection (B : Matrix K K ℝ) : Matrix K K ℝ :=
  fun p q => B p q -
    if p = q then B.trace / (Fintype.card K : ℝ) else 0

/-- The projected sphere residual matrix
`M_i = P₀(C_i + 2 x_i x_iᵀ)`. -/
noncomputable def sphereResidualMatrix
    (a : I → I → ℝ) (x : I → K → ℝ) (i : I) : Matrix K K ℝ :=
  traceFreeProjection
    (jumpCovarianceMatrix a x i +
      (2 : ℝ) • Matrix.vecMulVec (x i) (x i))

/-- Projection is invisible when paired against a trace-free coefficient
matrix. -/
theorem matrixFrobeniusPairing_traceFreeProjection
    (A B : Matrix K K ℝ) (htrace : A.trace = 0) :
    matrixFrobeniusPairing A (traceFreeProjection B) =
      matrixFrobeniusPairing A B := by
  classical
  have hdiag :
      ∑ p, ∑ q,
          A p q *
            (if p = q then B.trace / (Fintype.card K : ℝ) else 0) = 0 := by
    calc
      ∑ p, ∑ q,
          A p q *
            (if p = q then B.trace / (Fintype.card K : ℝ) else 0) =
          ∑ p, A p p * (B.trace / (Fintype.card K : ℝ)) := by
            apply Finset.sum_congr rfl
            intro p hp
            simp
      _ = (B.trace / (Fintype.card K : ℝ)) * ∑ p, A p p := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro p hp
            ring
      _ = (B.trace / (Fintype.card K : ℝ)) * A.trace := rfl
      _ = 0 := by rw [htrace, mul_zero]
  unfold matrixFrobeniusPairing traceFreeProjection
  simp_rw [mul_sub, Finset.sum_sub_distrib]
  rw [hdiag]
  ring

/-- `M_i` is trace-free when the coordinate space is nonempty. -/
theorem trace_sphereResidualMatrix_eq_zero
    [Nonempty K]
    (a : I → I → ℝ) (x : I → K → ℝ) (i : I) :
    (sphereResidualMatrix a x i).trace = 0 := by
  classical
  unfold sphereResidualMatrix traceFreeProjection
  simp only [Matrix.trace, Matrix.diag_apply]
  change ∑ p,
      ((jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i)) p p -
        (jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i)).trace /
            (Fintype.card K : ℝ)) = 0
  rw [Finset.sum_sub_distrib]
  have hcard : (Fintype.card K : ℝ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  change (jumpCovarianceMatrix a x i +
        (2 : ℝ) • Matrix.vecMulVec (x i) (x i)).trace -
      (Fintype.card K : ℝ) *
        ((jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i)).trace /
            (Fintype.card K : ℝ)) = 0
  field_simp
  ring

/-- `M_i` is symmetric. -/
theorem sphereResidualMatrix_isSymm
    (a : I → I → ℝ) (x : I → K → ℝ) (i : I) :
    (sphereResidualMatrix a x i).IsSymm := by
  rw [Matrix.IsSymm.ext_iff]
  intro p q
  simp only [sphereResidualMatrix, traceFreeProjection,
    jumpCovarianceMatrix, Matrix.add_apply, Pi.smul_apply,
    Matrix.vecMulVec_apply, smul_eq_mul]
  by_cases hpq : p = q
  · subst q
    rfl
  · have hqp : q ≠ p := Ne.symm hpq
    simp only [hpq, hqp, if_false, sub_zero]
    change
      (offdiag i).sum (fun j =>
          a i j * (x j q - x i q) * (x j p - x i p)) +
          2 * (x i q * x i p) =
        (offdiag i).sum (fun j =>
          a i j * (x j p - x i p) * (x j q - x i q)) +
          2 * (x i p * x i q)
    apply congrArg₂ (fun u v : ℝ => u + v)
    · apply Finset.sum_congr rfl
      intro j hj
      ring
    · ring

/-- The unprojected covariance-plus-outer-product matrix is symmetric. -/
theorem sphereCovarianceAddOuter_isSymm
    (a : I → I → ℝ) (x : I → K → ℝ) (i : I) :
    (jumpCovarianceMatrix a x i +
      (2 : ℝ) • Matrix.vecMulVec (x i) (x i)).IsSymm := by
  have hcov : (jumpCovarianceMatrix a x i).IsSymm := by
    rw [Matrix.IsSymm.ext_iff]
    intro p q
    unfold jumpCovarianceMatrix
    apply Finset.sum_congr rfl
    intro j hj
    ring
  have houter : (Matrix.vecMulVec (x i) (x i)).IsSymm := by
    rw [Matrix.IsSymm.ext_iff]
    intro p q
    simp only [Matrix.vecMulVec_apply]
    ring
  exact hcov.add (houter.smul 2)

/-- The jump generator as a linear endomorphism of sampled functions. -/
def jumpGeneratorLinear (a : I → I → ℝ) : Module.End ℝ (I → ℝ) where
  toFun f := jumpGenerator a f
  map_add' f g := by
    funext i
    classical
    unfold jumpGenerator
    change (offdiag i).sum (fun j =>
        a i j * ((f j + g j) - (f i + g i))) =
      (offdiag i).sum (fun j => a i j * (f j - f i)) +
        (offdiag i).sum (fun j => a i j * (g j - g i))
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  map_smul' c f := by
    funext i
    classical
    unfold jumpGenerator
    change (offdiag i).sum (fun j =>
        a i j * (c * f j - c * f i)) =
      c * (offdiag i).sum (fun j => a i j * (f j - f i))
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring

/-- Quadratic sampling as a linear map on all coefficient matrices. -/
def quadraticSamplingLinear (x : I → K → ℝ) :
    Matrix K K ℝ →ₗ[ℝ] (I → ℝ) where
  toFun A := sampledQuadratic A x
  map_add' A B := by
    funext i
    classical
    unfold sampledQuadratic finiteQuadraticSample
    change (∑ p, ∑ q, (A p q + B p q) * x i p * x i q) =
      (∑ p, ∑ q, A p q * x i p * x i q) +
        ∑ p, ∑ q, B p q * x i p * x i q
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro p hp
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro q hq
    ring
  map_smul' c A := by
    funext i
    classical
    unfold sampledQuadratic finiteQuadraticSample
    change (∑ p, ∑ q, (c * A p q) * x i p * x i q) =
      c * ∑ p, ∑ q, A p q * x i p * x i q
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro q hq
    ring

/-- Quadratic sampling restricted to `Sym₀(K)`. -/
def sphereSamplingLinear (x : I → K → ℝ) :
    symmetricTraceFreeMatrices K →ₗ[ℝ] (I → ℝ) :=
  (quadraticSamplingLinear x).domRestrict (symmetricTraceFreeMatrices K)

/-- The target degree-two residual `(L + 2 d I) S_X`. -/
def sphereResidualLinear
    (a : I → I → ℝ) (x : I → K → ℝ) :
    symmetricTraceFreeMatrices K →ₗ[ℝ] (I → ℝ) :=
  linearSampledResidual (jumpGeneratorLinear a)
    (2 * (Fintype.card K : ℝ)) (sphereSamplingLinear x)

/-- Pairing with `C_i + 2 x_i x_iᵀ` expands to the covariance term plus
twice the quadratic sample. -/
theorem matrixFrobeniusPairing_covariance_add_outer
    (a : I → I → ℝ) (x : I → K → ℝ)
    (A : Matrix K K ℝ) (i : I) :
    matrixFrobeniusPairing A
        (jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i)) =
      quadraticCovariancePairing a A x i +
        2 * sampledQuadratic A x i := by
  classical
  unfold matrixFrobeniusPairing jumpCovarianceMatrix
    quadraticCovariancePairing sampledQuadratic finiteQuadraticSample
  simp only [Matrix.add_apply]
  simp_rw [mul_add, Finset.sum_add_distrib]
  apply congrArg₂ (fun u v : ℝ => u + v)
  · rfl
  · change
      (∑ p, ∑ q, A p q * (2 * (x i p * x i q))) =
        2 * ∑ p, ∑ q, A p q * x i p * x i q
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro q hq
    ring

/-- Explicit unit-sphere residual factorization
`R_X(A)_i = ⟨A,M_i⟩_F = tr(A(C_i+2x_ix_iᵀ))`.

Only the coordinate eigenmap equation and trace-freeness are used by this
algebraic identity; symmetry and unit length are carried by the domain and the
geometric interpretation. -/
theorem sphereResidual_factorization
    (a : I → I → ℝ) (x : I → K → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (A : symmetricTraceFreeMatrices K) (i : I) :
    sphereResidualLinear a x A i =
      matrixFrobeniusPairing A.1 (sphereResidualMatrix a x i) := by
  have htrace : (A.1 : Matrix K K ℝ).trace = 0 := by
    exact LinearMap.mem_ker.mp A.2.2
  unfold sphereResidualMatrix
  rw [matrixFrobeniusPairing_traceFreeProjection A.1 _ htrace]
  rw [matrixFrobeniusPairing_covariance_add_outer]
  unfold sphereResidualLinear linearSampledResidual sphereSamplingLinear
    quadraticSamplingLinear jumpGeneratorLinear
  change jumpGenerator a (sampledQuadratic A.1 x) i +
      (2 * (Fintype.card K : ℝ)) * sampledQuadratic A.1 x i = _
  rw [jumpGenerator_sampledQuadratic a A.1 x
    ((Fintype.card K : ℝ) - 1) hx i]
  ring

/-- For trace-free coefficients, pairing with the projected residual matrix
is exactly the conventional trace product against the unprojected matrix. -/
theorem matrixFrobeniusPairing_sphereResidualMatrix_eq_trace
    (a : I → I → ℝ) (x : I → K → ℝ)
    (A : symmetricTraceFreeMatrices K) (i : I) :
    matrixFrobeniusPairing A.1 (sphereResidualMatrix a x i) =
      (A.1 *
        (jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i))).trace := by
  have htrace : (A.1 : Matrix K K ℝ).trace = 0 :=
    LinearMap.mem_ker.mp A.2.2
  unfold sphereResidualMatrix
  rw [matrixFrobeniusPairing_traceFreeProjection A.1 _ htrace]
  exact matrixFrobeniusPairing_eq_trace_mul_of_isSymm_right A.1 _
    (sphereCovarianceAddOuter_isSymm a x i)

/-- Complete unit-sphere display identity
`R_X(A)_i = ⟨A,M_i⟩_F = tr(A(C_i+2x_ix_iᵀ))`. -/
theorem sphereResidual_factorization_trace
    (a : I → I → ℝ) (x : I → K → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (A : symmetricTraceFreeMatrices K) (i : I) :
    sphereResidualLinear a x A i =
      (A.1 *
        (jumpCovarianceMatrix a x i +
          (2 : ℝ) • Matrix.vecMulVec (x i) (x i))).trace := by
  rw [sphereResidual_factorization a x hx A i]
  exact matrixFrobeniusPairing_sphereResidualMatrix_eq_trace a x A i

/-- The explicit pairing-orthogonal form space. This is the coordinate
meaning of `span {M_i}^⊥`. -/
def sphereResidualOrthogonal
    (a : I → I → ℝ) (x : I → K → ℝ) :
    Submodule ℝ (symmetricTraceFreeMatrices K) where
  carrier := {A | ∀ i, matrixFrobeniusPairing A.1 (sphereResidualMatrix a x i) = 0}
  zero_mem' := by
    intro i
    unfold matrixFrobeniusPairing
    simp
  add_mem' := by
    intro A B hA hB i
    specialize hA i
    specialize hB i
    unfold matrixFrobeniusPairing at *
    change (∑ p, ∑ q,
        (A.1 p q + B.1 p q) * sphereResidualMatrix a x i p q) = 0
    simp_rw [add_mul, Finset.sum_add_distrib]
    linarith
  smul_mem' := by
    intro c A hA i
    specialize hA i
    unfold matrixFrobeniusPairing at *
    change (∑ p, ∑ q,
        (c * A.1 p q) * sphereResidualMatrix a x i p q) = 0
    calc
      ∑ p, ∑ q,
          (c * A.1 p q) * sphereResidualMatrix a x i p q =
          c * ∑ p, ∑ q,
            A.1 p q * sphereResidualMatrix a x i p q := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro p hp
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro q hq
              ring
      _ = 0 := by rw [hA, mul_zero]

/-- Exact forms are precisely the pairing-orthogonal complement of all
residual matrices. -/
theorem sphereFormExact_eq_residualOrthogonal
    (a : I → I → ℝ) (x : I → K → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p) :
    LinearMap.ker (sphereResidualLinear a x) =
      sphereResidualOrthogonal a x := by
  ext A
  constructor
  · intro hA i
    have hzero : sphereResidualLinear a x A i = 0 := by
      rw [LinearMap.mem_ker.mp hA]
      rfl
    rw [sphereResidual_factorization a x hx A i] at hzero
    exact hzero
  · intro hA
    apply LinearMap.mem_ker.mpr
    funext i
    rw [sphereResidual_factorization a x hx A i]
    exact hA i

/-- Sphere-specialized sampling aliases are exact forms. -/
theorem sphereSamplingKernel_le_formExact
    (a : I → I → ℝ) (x : I → K → ℝ) :
    LinearMap.ker (sphereSamplingLinear x) ≤
      LinearMap.ker (sphereResidualLinear a x) :=
  linear_samplingKernel_le_residualKernel
    (jumpGeneratorLinear a) (2 * (Fintype.card K : ℝ))
    (sphereSamplingLinear x)

/-- Sphere-specialized range/eigenspace characterization. -/
theorem sphereSampledExact_eq_range_inf_targetKernel
    (a : I → I → ℝ) (x : I → K → ℝ) :
    linearSampledExactRange (jumpGeneratorLinear a)
        (2 * (Fintype.card K : ℝ)) (sphereSamplingLinear x) =
      LinearMap.range (sphereSamplingLinear x) ⊓
        LinearMap.ker
          (jumpGeneratorLinear a +
            (2 * (Fintype.card K : ℝ)) • LinearMap.id) :=
  linearSampledExactRange_eq_range_inf_targetKernel
    (jumpGeneratorLinear a) (2 * (Fintype.card K : ℝ))
    (sphereSamplingLinear x)

/-- Sphere-specialized dimension formula in form/kernel language. -/
theorem sphereSampledExact_finrank_eq_form_sub_alias
    (a : I → I → ℝ) (x : I → K → ℝ) :
    Module.finrank ℝ
        (linearSampledExactRange (jumpGeneratorLinear a)
          (2 * (Fintype.card K : ℝ)) (sphereSamplingLinear x)) =
      Module.finrank ℝ (LinearMap.ker (sphereResidualLinear a x)) -
        Module.finrank ℝ (LinearMap.ker (sphereSamplingLinear x)) :=
  linearSampledExactRange_finrank_eq_formExact_sub_samplingKernel
    (jumpGeneratorLinear a) (2 * (Fintype.card K : ℝ))
    (sphereSamplingLinear x)

/-- Sphere-specialized rank-difference dimension formula. -/
theorem sphereSampledExact_finrank_eq_samplingRank_sub_residualRank
    (a : I → I → ℝ) (x : I → K → ℝ) :
    Module.finrank ℝ
        (linearSampledExactRange (jumpGeneratorLinear a)
          (2 * (Fintype.card K : ℝ)) (sphereSamplingLinear x)) =
      Module.finrank ℝ (LinearMap.range (sphereSamplingLinear x)) -
        Module.finrank ℝ (LinearMap.range (sphereResidualLinear a x)) :=
  linearSampledExactRange_finrank_eq_samplingRank_sub_residualRank
    (jumpGeneratorLinear a) (2 * (Fintype.card K : ℝ))
    (sphereSamplingLinear x)

end AFPBarrier
