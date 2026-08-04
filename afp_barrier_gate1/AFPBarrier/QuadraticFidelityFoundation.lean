import AFPBarrier.QuadraticSphereResidual
import AFPBarrier.LossVariance
import Mathlib.Tactic

/-!
# Sampling-quotient Gram algebra and the quadratic two-defect split

This module isolates the finite algebra used by the degree-two fidelity
frontier.  It uses the weighted sample pairing and the Frobenius pairing
explicitly, so that transposes with respect to the unweighted counting
measure cannot be substituted accidentally.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I K : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype K] [DecidableEq K]

/-- Squared Frobenius norm, kept entrywise to avoid hidden normalization. -/
def matrixFrobeniusNormSq (A : Matrix K K ℝ) : ℝ :=
  matrixFrobeniusPairing A A

/-- Weighted pairing on sampled functions. -/
def weightedSamplePairing
    (w f g : I → ℝ) : ℝ :=
  ∑ i, w i * f i * g i

/-- Analysis by a finite family of Frobenius rows. -/
def frobeniusRowAnalysis
    (rows : I → Matrix K K ℝ) (A : Matrix K K ℝ) : I → ℝ :=
  fun i => matrixFrobeniusPairing A (rows i)

/-- The weighted synthesis operator associated with Frobenius rows. -/
def weightedFrobeniusRowSynthesis
    (w : I → ℝ) (rows : I → Matrix K K ℝ) (f : I → ℝ) :
    Matrix K K ℝ :=
  fun p q => ∑ i, w i * f i * rows i p q

/-- The row Gram operator is weighted synthesis after row analysis. -/
def weightedFrobeniusRowGram
    (w : I → ℝ) (rows : I → Matrix K K ℝ) (A : Matrix K K ℝ) :
    Matrix K K ℝ :=
  weightedFrobeniusRowSynthesis w rows (frobeniusRowAnalysis rows A)

/-- The explicit weighted adjoint identity for a finite Frobenius row map. -/
theorem weightedFrobeniusRowSynthesis_adjoint
    (w : I → ℝ) (rows : I → Matrix K K ℝ)
    (A : Matrix K K ℝ) (f : I → ℝ) :
    matrixFrobeniusPairing A (weightedFrobeniusRowSynthesis w rows f) =
      weightedSamplePairing w (frobeniusRowAnalysis rows A) f := by
  classical
  change
    (∑ p, ∑ q, A p q * (∑ i, w i * f i * rows i p q)) =
      ∑ i, w i * (∑ p, ∑ q, A p q * rows i p q) * f i
  calc
    (∑ p, ∑ q, A p q * (∑ i, w i * f i * rows i p q)) =
        ∑ p, ∑ q, ∑ i, A p q * (w i * f i * rows i p q) := by
          apply Finset.sum_congr rfl
          intro p hp
          apply Finset.sum_congr rfl
          intro q hq
          rw [Finset.mul_sum]
    _ =
        ∑ p, ∑ i, ∑ q, A p q * (w i * f i * rows i p q) := by
          apply Finset.sum_congr rfl
          intro p hp
          rw [Finset.sum_comm]
    _ = ∑ i, ∑ p, ∑ q, A p q * (w i * f i * rows i p q) := by
          rw [Finset.sum_comm]
    _ = ∑ i, w i * (∑ p, ∑ q, A p q * rows i p q) * f i := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [Finset.mul_sum, Finset.sum_mul]
          apply Finset.sum_congr rfl
          intro p hp
          rw [Finset.mul_sum, Finset.sum_mul]
          apply Finset.sum_congr rfl
          intro q hq
          ring

/-- Exact weighted Gram bilinear formula. -/
theorem weightedFrobeniusRowGram_pairing
    (w : I → ℝ) (rows : I → Matrix K K ℝ)
    (A H : Matrix K K ℝ) :
    matrixFrobeniusPairing H (weightedFrobeniusRowGram w rows A) =
      ∑ i, w i * matrixFrobeniusPairing H (rows i) *
        matrixFrobeniusPairing A (rows i) := by
  unfold weightedFrobeniusRowGram
  rw [weightedFrobeniusRowSynthesis_adjoint]
  rfl

/-- Exact weighted Gram quadratic formula. -/
theorem weightedFrobeniusRowGram_quadratic
    (w : I → ℝ) (rows : I → Matrix K K ℝ)
    (A : Matrix K K ℝ) :
    matrixFrobeniusPairing A (weightedFrobeniusRowGram w rows A) =
      ∑ i, w i * (matrixFrobeniusPairing A (rows i)) ^ 2 := by
  rw [weightedFrobeniusRowGram_pairing]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- The trace-free sampling row `Z_i`; its explicit coordinate form is the
trace-free projection of `x_i x_i^T`. -/
noncomputable def sphereSamplingRowMatrix
    (x : I → K → ℝ) (i : I) : Matrix K K ℝ :=
  traceFreeProjection (Matrix.vecMulVec (x i) (x i))

/-- Quadratic sampling is Frobenius analysis by the trace-free rows `Z_i`. -/
theorem sphereSamplingLinear_eq_frobeniusRowAnalysis
    (x : I → K → ℝ) (A : symmetricTraceFreeMatrices K) (i : I) :
    sphereSamplingLinear x A i =
      matrixFrobeniusPairing A.1 (sphereSamplingRowMatrix x i) := by
  classical
  have htrace : (A.1 : Matrix K K ℝ).trace = 0 :=
    LinearMap.mem_ker.mp A.2.2
  change sampledQuadratic A.1 x i =
    matrixFrobeniusPairing A.1
      (traceFreeProjection (Matrix.vecMulVec (x i) (x i)))
  rw [matrixFrobeniusPairing_traceFreeProjection A.1 _ htrace]
  unfold sampledQuadratic matrixFrobeniusPairing
  simp only [Matrix.vecMulVec_apply]
  apply Finset.sum_congr rfl
  intro p hp
  apply Finset.sum_congr rfl
  intro q hq
  ring

/-- Weighted `S_2^* S_2` as a concrete Frobenius row Gram matrix. -/
noncomputable def sphereSamplingWeightedGram
    (w : I → ℝ) (x : I → K → ℝ)
    (A : symmetricTraceFreeMatrices K) : Matrix K K ℝ :=
  weightedFrobeniusRowGram w (sphereSamplingRowMatrix x) A.1

/-- Bilinear weighted Gram formula for quadratic sampling. -/
theorem sphereSamplingWeightedGram_pairing
    (w : I → ℝ) (x : I → K → ℝ)
    (A H : symmetricTraceFreeMatrices K) :
    matrixFrobeniusPairing H.1 (sphereSamplingWeightedGram w x A) =
      ∑ i, w i * sphereSamplingLinear x H i *
        sphereSamplingLinear x A i := by
  unfold sphereSamplingWeightedGram
  rw [weightedFrobeniusRowGram_pairing]
  apply Finset.sum_congr rfl
  intro i hi
  rw [sphereSamplingLinear_eq_frobeniusRowAnalysis,
    sphereSamplingLinear_eq_frobeniusRowAnalysis]

/-- Quadratic weighted Gram formula for `S_2^* S_2`. -/
theorem sphereSamplingWeightedGram_quadratic
    (w : I → ℝ) (x : I → K → ℝ)
    (A : symmetricTraceFreeMatrices K) :
    matrixFrobeniusPairing A.1 (sphereSamplingWeightedGram w x A) =
      ∑ i, w i * (sphereSamplingLinear x A i) ^ 2 := by
  rw [sphereSamplingWeightedGram_pairing]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- Weighted `R_2^* R_2` as a concrete residual-row Gram matrix. -/
noncomputable def sphereResidualWeightedGram
    (w : I → ℝ) (a : I → I → ℝ) (x : I → K → ℝ)
    (A : symmetricTraceFreeMatrices K) : Matrix K K ℝ :=
  weightedFrobeniusRowGram w (sphereResidualMatrix a x) A.1

/-- Bilinear weighted Gram formula for the degree-two residual. -/
theorem sphereResidualWeightedGram_pairing
    (w : I → ℝ) (a : I → I → ℝ) (x : I → K → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (A H : symmetricTraceFreeMatrices K) :
    matrixFrobeniusPairing H.1 (sphereResidualWeightedGram w a x A) =
      ∑ i, w i * sphereResidualLinear a x H i *
        sphereResidualLinear a x A i := by
  unfold sphereResidualWeightedGram
  rw [weightedFrobeniusRowGram_pairing]
  apply Finset.sum_congr rfl
  intro i hi
  rw [sphereResidual_factorization a x hx H i,
    sphereResidual_factorization a x hx A i]

/-- Quadratic weighted Gram formula for `R_2^* R_2`. -/
theorem sphereResidualWeightedGram_quadratic
    (w : I → ℝ) (a : I → I → ℝ) (x : I → K → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (A : symmetricTraceFreeMatrices K) :
    matrixFrobeniusPairing A.1 (sphereResidualWeightedGram w a x A) =
      ∑ i, w i * (sphereResidualLinear a x A i) ^ 2 := by
  rw [sphereResidualWeightedGram_pairing w a x hx A A]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- Subtract the Frobenius projection coefficient along a distinguished row. -/
def frobeniusRowRemainder
    (M Z : Matrix K K ℝ) (c : ℝ) : Matrix K K ℝ :=
  M - c • Z

/-- Pairing of the row remainder with the distinguished direction. -/
theorem frobeniusRowRemainder_pairing
    (M Z : Matrix K K ℝ) (c : ℝ) :
    matrixFrobeniusPairing (frobeniusRowRemainder M Z c) Z =
      matrixFrobeniusPairing M Z - c * matrixFrobeniusPairing Z Z := by
  classical
  unfold frobeniusRowRemainder matrixFrobeniusPairing
  simp only [Matrix.sub_apply, Pi.smul_apply, smul_eq_mul]
  simp_rw [sub_mul, Finset.sum_sub_distrib]
  apply congrArg₂ (fun u v : ℝ => u - v)
  · rfl
  · rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro q hq
    change (c * Z p q) * Z p q = Z p q ^ 2 * c
    ring

/-- Squared norm of a row remainder. -/
theorem matrixFrobeniusNormSq_rowRemainder
    (M Z : Matrix K K ℝ) (c : ℝ) :
    matrixFrobeniusNormSq (frobeniusRowRemainder M Z c) =
      matrixFrobeniusNormSq M -
        2 * c * matrixFrobeniusPairing M Z +
        c ^ 2 * matrixFrobeniusNormSq Z := by
  classical
  change
    (∑ p, ∑ q, (M p q - c * Z p q) * (M p q - c * Z p q)) =
      (∑ p, ∑ q, M p q * M p q) -
        2 * c * (∑ p, ∑ q, M p q * Z p q) +
        c ^ 2 * (∑ p, ∑ q, Z p q * Z p q)
  calc
    (∑ p, ∑ q, (M p q - c * Z p q) * (M p q - c * Z p q)) =
        ∑ p, ∑ q,
          (M p q * M p q - 2 * c * (M p q * Z p q) +
            c ^ 2 * (Z p q * Z p q)) := by
              apply Finset.sum_congr rfl
              intro p hp
              apply Finset.sum_congr rfl
              intro q hq
              ring
    _ = (∑ p, ∑ q, M p q * M p q) -
          2 * c * (∑ p, ∑ q, M p q * Z p q) +
          c ^ 2 * (∑ p, ∑ q, Z p q * Z p q) := by
            simp_rw [Finset.sum_add_distrib, Finset.sum_sub_distrib,
              Finset.mul_sum]

/-- The exact degree-two defect remainder
`B = M - d/(d-1) epsilon Z`. -/
noncomputable def quadraticTwoDefectRemainder
    (d epsilon : ℝ) (M Z : Matrix K K ℝ) : Matrix K K ℝ :=
  frobeniusRowRemainder M Z (d / (d - 1) * epsilon)

/-- Orthogonality of the two degree-two defect components. -/
theorem quadraticTwoDefectRemainder_orthogonal
    (d epsilon : ℝ) (M Z : Matrix K K ℝ)
    (hd0 : d ≠ 0) (hd1 : d ≠ 1)
    (hMZ : matrixFrobeniusPairing M Z = epsilon)
    (hZZ : matrixFrobeniusPairing Z Z = (d - 1) / d) :
    matrixFrobeniusPairing
        (quadraticTwoDefectRemainder d epsilon M Z) Z = 0 := by
  unfold quadraticTwoDefectRemainder
  rw [frobeniusRowRemainder_pairing, hMZ, hZZ]
  field_simp [hd0, sub_ne_zero.mpr hd1]
  ring

/-- Exact Pythagorean split
`||M||_F^2 = d/(d-1) epsilon^2 + ||B||_F^2`. -/
theorem quadraticTwoDefect_pythagorean
    (d epsilon : ℝ) (M Z : Matrix K K ℝ)
    (hd0 : d ≠ 0) (hd1 : d ≠ 1)
    (hMZ : matrixFrobeniusPairing M Z = epsilon)
    (hZZ : matrixFrobeniusNormSq Z = (d - 1) / d) :
    matrixFrobeniusNormSq M =
      d / (d - 1) * epsilon ^ 2 +
        matrixFrobeniusNormSq
          (quadraticTwoDefectRemainder d epsilon M Z) := by
  unfold quadraticTwoDefectRemainder
  rw [matrixFrobeniusNormSq_rowRemainder, hMZ, hZZ]
  field_simp [hd0, sub_ne_zero.mpr hd1]
  ring

/-- Generic finite weighted-variance identity.  In the spherical application
take `ell i j = 1 - Omega_i · Omega_j` and `lam = d-1`. -/
theorem exactLossSecondMoment_decomposition
    (a ell : I → I → ℝ) (i : I) (lam : ℝ)
    (hrate : jumpRate a i ≠ 0)
    (hmoment : (offdiag i).sum (fun j => a i j * ell i j) = lam) :
    (offdiag i).sum (fun j => a i j * (ell i j) ^ 2) =
      lam ^ 2 / jumpRate a i +
        (offdiag i).sum (fun j =>
          a i j * (ell i j - lam / jumpRate a i) ^ 2) := by
  classical
  have hexpand :
      (offdiag i).sum (fun j =>
          a i j * (ell i j - lam / jumpRate a i) ^ 2) =
        (offdiag i).sum (fun j => a i j * (ell i j) ^ 2) -
          2 * (lam / jumpRate a i) *
            (offdiag i).sum (fun j => a i j * ell i j) +
          (lam / jumpRate a i) ^ 2 * jumpRate a i := by
    calc
      (offdiag i).sum (fun j =>
          a i j * (ell i j - lam / jumpRate a i) ^ 2) =
          (offdiag i).sum (fun j =>
            a i j * (ell i j) ^ 2 -
              2 * (lam / jumpRate a i) * (a i j * ell i j) +
              (lam / jumpRate a i) ^ 2 * a i j) := by
                apply Finset.sum_congr rfl
                intro j hj
                ring
      _ = (offdiag i).sum (fun j => a i j * (ell i j) ^ 2) -
            2 * (lam / jumpRate a i) *
              (offdiag i).sum (fun j => a i j * ell i j) +
            (lam / jumpRate a i) ^ 2 * jumpRate a i := by
              unfold jumpRate
              simp_rw [Finset.sum_add_distrib, Finset.sum_sub_distrib,
                Finset.mul_sum]
  rw [hexpand, hmoment]
  field_simp [hrate]
  ring

end AFPBarrier
