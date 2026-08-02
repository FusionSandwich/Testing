import AFPBarrier.QuadraticSphereResidual
import Mathlib.Tactic

/-!
# Signed one-shell full-tangent-isotropy rigidity

The rowwise algebra is phrased for an explicit finite active-neighbour set.
No sign, symmetry, reversibility, connectivity, or transitivity hypothesis is
used.  Coincident or zero-rate jumps are omitted before these lemmas are
applied, exactly as in the theorem statement.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I K V : Type*} [Fintype K] [DecidableEq K]

/-- Euclidean coordinate pairing. -/
def oneShellFiniteDot (v w : K → ℝ) : ℝ := ∑ p, v p * w p

/-- Signed rate on the active one-shell row. -/
def oneShellRate (J : Finset I) (row : I → ℝ) : ℝ :=
  ∑ j ∈ J, row j

/-- Signed tangent first moment. -/
def oneShellFirstMoment
    (J : Finset I) (row : I → ℝ) (u : I → K → ℝ) (p : K) : ℝ :=
  ∑ j ∈ J, row j * u j p

/-- Signed tangent second moment. -/
def oneShellSecondMoment
    (J : Finset I) (row : I → ℝ) (u : I → K → ℝ)
    (p q : K) : ℝ :=
  ∑ j ∈ J, row j * u j p * u j q

/-- Covariance obtained from the one-shell increment decomposition
`Δ_j = -ell z + s u_j`. -/
def oneShellCovariance
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (ell s : ℝ) (p q : K) : ℝ :=
  ∑ j ∈ J, row j *
    ((-ell * z p + s * u j p) * (-ell * z q + s * u j q))

/-- Radial projection of the coordinate eigenmap equation forces
`r*ell=d-1`. -/
theorem oneShell_radial_rate
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (d ell s r : ℝ)
    (hr : r = oneShellRate J row)
    (hunit : oneShellFiniteDot z z = 1)
    (htangent : ∀ j ∈ J, oneShellFiniteDot z (u j) = 0)
    (heigen : ∀ p,
      ∑ j ∈ J, row j * (-ell * z p + s * u j p) =
        -(d - 1) * z p) :
    r * ell = d - 1 := by
  have hproject :
      (∑ p, z p *
        (∑ j ∈ J, row j * (-ell * z p + s * u j p))) =
        ∑ p, z p * (-(d - 1) * z p) := by
    apply Finset.sum_congr rfl
    intro p hp
    rw [heigen p]
  have hlhs :
      (∑ p, z p *
        (∑ j ∈ J, row j * (-ell * z p + s * u j p))) =
        -ell * r := by
    calc
      _ = ∑ p, ∑ j ∈ J,
          z p * (row j * (-ell * z p + s * u j p)) := by
            apply Finset.sum_congr rfl
            intro p hp
            rw [Finset.mul_sum]
      _ = ∑ j ∈ J, ∑ p,
          z p * (row j * (-ell * z p + s * u j p)) := by
            rw [Finset.sum_comm]
      _ = ∑ j ∈ J, row j * (-ell) := by
            apply Finset.sum_congr rfl
            intro j hj
            calc
              _ = row j * (-ell * (∑ p, z p * z p) +
                  s * (∑ p, z p * u j p)) := by
                    ring_nf
                    rw [Finset.sum_sub_distrib]
                    have h1 :
                        (∑ p, z p ^ 2 * row j * ell) =
                          row j * ell * ∑ p, z p * z p := by
                      rw [Finset.mul_sum]
                      apply Finset.sum_congr rfl
                      intro p hp
                      ring
                    have h2 :
                        (∑ p, z p * row j * s * u j p) =
                          row j * s * ∑ p, z p * u j p := by
                      rw [Finset.mul_sum]
                      apply Finset.sum_congr rfl
                      intro p hp
                      ring
                    rw [h1, h2]
                    ring
              _ = row j * (-ell) := by
                    rw [show ∑ p, z p * z p = 1 from hunit,
                      show ∑ p, z p * u j p = 0 from htangent j hj]
                    ring
      _ = -ell * r := by
            rw [hr]
            unfold oneShellRate
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro j hj
            ring
  have hrhs : (∑ p, z p * (-(d - 1) * z p)) = -(d - 1) := by
    calc
      _ = -(d - 1) * ∑ p, z p * z p := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro p hp
            ring
      _ = _ := by rw [show ∑ p, z p * z p = 1 from hunit]; ring
  rw [hlhs, hrhs] at hproject
  linarith

/-- After the radial equation is removed, the coordinate eigenmap equation
forces the signed tangent first moment to vanish. -/
theorem oneShell_tangent_balance
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (d ell s r : ℝ)
    (hr : r = oneShellRate J row)
    (hs : s ≠ 0)
    (hradial : r * ell = d - 1)
    (heigen : ∀ p,
      ∑ j ∈ J, row j * (-ell * z p + s * u j p) =
        -(d - 1) * z p) :
    ∀ p, oneShellFirstMoment J row u p = 0 := by
  intro p
  have hsplit :
      (∑ j ∈ J, row j * (-ell * z p + s * u j p)) =
        -ell * r * z p + s * oneShellFirstMoment J row u p := by
    unfold oneShellRate at hr
    unfold oneShellFirstMoment
    ring_nf
    rw [Finset.sum_add_distrib]
    have h1 :
        (∑ j ∈ J, -(row j * ell * z p)) =
          -ell * z p * (∑ j ∈ J, row j) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ring
    have h2 :
        (∑ j ∈ J, row j * s * u j p) =
          s * (∑ j ∈ J, row j * u j p) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ring
    rw [h1, h2, ← hr]
    ring
  have h := heigen p
  rw [hsplit] at h
  have hradial_z := congrArg (fun t : ℝ => t * z p) hradial
  have hz : s * oneShellFirstMoment J row u p = 0 := by
    ring_nf at h hradial_z ⊢
    linarith
  exact (mul_eq_zero.mp hz).resolve_left hs

/-- Direct expansion of the one-shell covariance into radial, mixed, and
tangent moments. -/
theorem oneShell_covariance_expansion
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (ell s : ℝ) (p q : K) :
    oneShellCovariance J row z u ell s p q =
      ell ^ 2 * oneShellRate J row * z p * z q -
        ell * s * z p * oneShellFirstMoment J row u q -
        ell * s * z q * oneShellFirstMoment J row u p +
        s ^ 2 * oneShellSecondMoment J row u p q := by
  unfold oneShellCovariance oneShellRate oneShellFirstMoment
    oneShellSecondMoment
  ring_nf
  simp_rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have h1 :
      (∑ j ∈ J, -(row j * ell * z p * s * u j q)) =
        -(ell * z p * s) * ∑ j ∈ J, row j * u j q := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  have h2 :
      (∑ j ∈ J, row j * ell * s * u j p * z q) =
        ell * s * z q * ∑ j ∈ J, row j * u j p := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  have h3 :
      (∑ j ∈ J, row j * ell ^ 2 * z p * z q) =
        ell ^ 2 * z p * z q * ∑ j ∈ J, row j := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  have h4 :
      (∑ j ∈ J, row j * s ^ 2 * u j p * u j q) =
        s ^ 2 * ∑ j ∈ J, row j * u j p * u j q := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  rw [h1, h2, h3, h4]
  ring

/-- Full signed tangent isotropy yields the required covariance formula. -/
theorem oneShell_covariance_decomposition
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (d ell s r : ℝ)
    (hd : d - 1 ≠ 0)
    (hradial : r * ell = d - 1)
    (hsquare : s ^ 2 = ell * (2 - ell))
    (hfirst : ∀ p, oneShellFirstMoment J row u p = 0)
    (hsecond : ∀ p q,
      oneShellSecondMoment J row u p q =
        (r / (d - 1)) *
          ((if p = q then 1 else 0) - z p * z q))
    (hr : r = oneShellRate J row)
    (p q : K) :
    oneShellCovariance J row z u ell s p q =
      (2 - ell) * ((if p = q then 1 else 0) - z p * z q) +
        (d - 1) * ell * z p * z q := by
  rw [oneShell_covariance_expansion]
  rw [← hr, hfirst q, hfirst p, hsecond p q]
  have htangentCoefficient : s ^ 2 * (r / (d - 1)) = 2 - ell := by
    calc
      _ = (ell * (2 - ell)) * (r / (d - 1)) := by rw [hsquare]
      _ = (2 - ell) * (r * ell) / (d - 1) := by ring
      _ = (2 - ell) * (d - 1) / (d - 1) := by rw [hradial]
      _ = 2 - ell := by field_simp [hd]
  have hradialCoefficient : ell ^ 2 * r = (d - 1) * ell := by
    calc
      _ = (r * ell) * ell := by ring
      _ = _ := by rw [hradial]
  have htangentTerm :
      s ^ 2 *
          ((r / (d - 1)) *
            ((if p = q then 1 else 0) - z p * z q)) =
        (2 - ell) * ((if p = q then 1 else 0) - z p * z q) := by
    rw [← mul_assoc, htangentCoefficient]
  rw [htangentTerm, hradialCoefficient]
  ring

/-- Bridge from the abstract one-shell covariance to the actual jump
covariance matrix. -/
theorem oneShell_actual_covariance_decomposition
    {I K : Type*} [Fintype K] [DecidableEq K]
    (J : Finset I) (row : I → ℝ) (z : K → ℝ)
    (u : I → K → ℝ) (C : Matrix K K ℝ)
    (d ell s r : ℝ)
    (hd : d - 1 ≠ 0)
    (hradial : r * ell = d - 1)
    (hsquare : s ^ 2 = ell * (2 - ell))
    (hfirst : ∀ p, oneShellFirstMoment J row u p = 0)
    (hsecond : ∀ p q,
      oneShellSecondMoment J row u p q =
        (r / (d - 1)) *
          ((if p = q then 1 else 0) - z p * z q))
    (hr : r = oneShellRate J row)
    (hactual : ∀ p q, C p q = oneShellCovariance J row z u ell s p q) :
    ∀ p q, C p q =
      (2 - ell) * ((if p = q then 1 else 0) - z p * z q) +
        (d - 1) * ell * z p * z q := by
  intro p q
  rw [hactual p q]
  exact oneShell_covariance_decomposition J row z u d ell s r hd
    hradial hsquare hfirst hsecond hr p q

/-- Frobenius pairing is additive in its right argument. -/
theorem oneShell_matrixFrobeniusPairing_add_right
    {K : Type*} [Fintype K]
    (A B C : Matrix K K ℝ) :
    matrixFrobeniusPairing A (B + C) =
      matrixFrobeniusPairing A B + matrixFrobeniusPairing A C := by
  unfold matrixFrobeniusPairing
  simp only [Matrix.add_apply]
  simp_rw [mul_add, Finset.sum_add_distrib]

/-- Frobenius pairing commutes with real scaling in its right argument. -/
theorem oneShell_matrixFrobeniusPairing_smul_right
    {K : Type*} [Fintype K]
    (A B : Matrix K K ℝ) (c : ℝ) :
    matrixFrobeniusPairing A (c • B) =
      c * matrixFrobeniusPairing A B := by
  unfold matrixFrobeniusPairing
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro p hp
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro q hq
  change A p q * (c * B p q) = c * (A p q * B p q)
  ring

/-- Pairing with the identity is the matrix trace. -/
theorem oneShell_matrixFrobeniusPairing_one
    {K : Type*} [Fintype K] [DecidableEq K]
    (A : Matrix K K ℝ) :
    matrixFrobeniusPairing A (1 : Matrix K K ℝ) = A.trace := by
  classical
  unfold matrixFrobeniusPairing Matrix.trace
  apply Finset.sum_congr rfl
  intro p hp
  simp [Matrix.one_apply]

/-- Pairing with `zzᵀ` is the sampled quadratic form. -/
theorem oneShell_matrixFrobeniusPairing_vecMulVec
    {K : Type*} [Fintype K]
    (A : Matrix K K ℝ) (z : K → ℝ) :
    matrixFrobeniusPairing A (Matrix.vecMulVec z z) =
      ∑ p, ∑ q, A p q * z p * z q := by
  unfold matrixFrobeniusPairing
  apply Finset.sum_congr rfl
  intro p hp
  apply Finset.sum_congr rfl
  intro q hq
  simp only [Matrix.vecMulVec_apply]
  ring

/-- The required trace-free residual bridge:
`⟨A,C+2zzᵀ⟩ = d ell ⟨A,zzᵀ⟩`. -/
theorem oneShell_traceFree_residual_pairing
    {K : Type*} [Fintype K] [DecidableEq K]
    (A C : Matrix K K ℝ) (z : K → ℝ) (d ell : ℝ)
    (htrace : A.trace = 0)
    (hC : ∀ p q, C p q =
      (2 - ell) * ((if p = q then 1 else 0) - z p * z q) +
        (d - 1) * ell * z p * z q) :
    matrixFrobeniusPairing A
        (C + (2 : ℝ) • Matrix.vecMulVec z z) =
      d * ell * (∑ p, ∑ q, A p q * z p * z q) := by
  classical
  have hmatrix :
      C + (2 : ℝ) • Matrix.vecMulVec z z =
        (2 - ell) • (1 : Matrix K K ℝ) +
          (d * ell) • Matrix.vecMulVec z z := by
    ext p q
    simp only [Matrix.add_apply]
    rw [hC p q]
    change
      (2 - ell) * ((if p = q then 1 else 0) - z p * z q) +
          (d - 1) * ell * z p * z q + 2 * (z p * z q) =
        (2 - ell) * (if p = q then 1 else 0) +
          (d * ell) * (z p * z q)
    ring
  rw [hmatrix, oneShell_matrixFrobeniusPairing_add_right,
    oneShell_matrixFrobeniusPairing_smul_right,
    oneShell_matrixFrobeniusPairing_smul_right,
    oneShell_matrixFrobeniusPairing_one,
    oneShell_matrixFrobeniusPairing_vecMulVec, htrace]
  ring

/-- Sphere-residual row equality obtained from the covariance decomposition,
not assumed as a separate hypothesis. -/
theorem oneShell_sphereResidual_row
    {I K : Type*}
    [Fintype I] [DecidableEq I] [Fintype K] [DecidableEq K]
    (a : I → I → ℝ) (x : I → K → ℝ) (ell : I → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (hcov : ∀ i p q, jumpCovarianceMatrix a x i p q =
      (2 - ell i) *
          ((if p = q then 1 else 0) - x i p * x i q) +
        ((Fintype.card K : ℝ) - 1) * ell i * x i p * x i q)
    (A : symmetricTraceFreeMatrices K) (i : I) :
    sphereResidualLinear a x A i =
      (Fintype.card K : ℝ) * ell i * sphereSamplingLinear x A i := by
  rw [sphereResidual_factorization a x hx A i]
  have htrace : (A.1 : Matrix K K ℝ).trace = 0 :=
    LinearMap.mem_ker.mp A.2.2
  unfold sphereResidualMatrix
  rw [matrixFrobeniusPairing_traceFreeProjection A.1 _ htrace]
  exact oneShell_traceFree_residual_pairing A.1
    (jumpCovarianceMatrix a x i) (x i) (Fintype.card K : ℝ) (ell i)
    htrace (hcov i)

section LinearConsequences

variable [AddCommGroup V] [Module ℝ V]

/-- Pointwise diagonal multiplication. -/
def diagonalMultiplier (scale : I → ℝ) : Module.End ℝ (I → ℝ) where
  toFun f i := scale i * f i
  map_add' f g := by ext i; simp; ring
  map_smul' c f := by ext i; simp; ring

/-- Pointwise row scaling is exactly the operator factorization `R = D S`. -/
theorem oneShell_residual_factorization
    (S R : V →ₗ[ℝ] (I → ℝ)) (scale : I → ℝ)
    (hrow : ∀ A i, R A i = scale i * S A i) :
    R = (diagonalMultiplier scale).comp S := by
  ext A i
  exact hrow A i

/-- If every diagonal factor is nonzero, exact forms are precisely sampling
aliases: `ker R = ker S`. -/
theorem oneShell_residualKernel_eq_samplingKernel
    (S R : V →ₗ[ℝ] (I → ℝ)) (scale : I → ℝ)
    (hscale : ∀ i, scale i ≠ 0)
    (hrow : ∀ A i, R A i = scale i * S A i) :
    LinearMap.ker R = LinearMap.ker S := by
  ext A
  constructor
  · intro hR
    apply LinearMap.mem_ker.mpr
    funext i
    have hz : R A i = 0 := by rw [LinearMap.mem_ker.mp hR]; rfl
    rw [hrow A i] at hz
    exact (mul_eq_zero.mp hz).resolve_left (hscale i)
  · intro hS
    apply LinearMap.mem_ker.mpr
    funext i
    change R A i = (0 : ℝ)
    have hSA : S A = 0 := LinearMap.mem_ker.mp hS
    have hSAi : S A i = (0 : ℝ) := congrFun hSA i
    rw [hrow A i, hSAi, mul_zero]

/-- Consequently `rank R = rank S`. -/
theorem oneShell_residualRank_eq_samplingRank
    [FiniteDimensional ℝ V]
    (S R : V →ₗ[ℝ] (I → ℝ)) (scale : I → ℝ)
    (hscale : ∀ i, scale i ≠ 0)
    (hrow : ∀ A i, R A i = scale i * S A i) :
    Module.finrank ℝ (LinearMap.range R) =
      Module.finrank ℝ (LinearMap.range S) := by
  have hker := oneShell_residualKernel_eq_samplingKernel S R scale hscale hrow
  have hRrank := LinearMap.finrank_range_add_finrank_ker R
  have hSrank := LinearMap.finrank_range_add_finrank_ker S
  rw [hker] at hRrank
  omega

/-- The genuinely sampled exact range is zero. -/
theorem oneShell_sampledExactRange_eq_bot
    (S R : V →ₗ[ℝ] (I → ℝ)) (scale : I → ℝ)
    (hscale : ∀ i, scale i ≠ 0)
    (hrow : ∀ A i, R A i = scale i * S A i) :
    LinearMap.range (S.domRestrict (LinearMap.ker R)) = ⊥ := by
  rw [eq_bot_iff]
  rintro f ⟨A, rfl⟩
  have hker := oneShell_residualKernel_eq_samplingKernel S R scale hscale hrow
  have hSA : S A.1 = 0 := by
    apply LinearMap.mem_ker.mp
    rw [← hker]
    exact A.2
  exact hSA.symm ▸ Submodule.zero_mem _

end LinearConsequences

/-! ## Sphere-specialized rigidity consequences -/

/-- The geometric row identity assembles into the requested operator
factorization `R_X = D S_X`, with `D_ii = d ell_i`. -/
theorem oneShell_sphereResidual_factorization
    {I K : Type*}
    [Fintype I] [DecidableEq I] [Fintype K] [DecidableEq K]
    (a : I → I → ℝ) (x : I → K → ℝ) (ell : I → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (hcov : ∀ i p q, jumpCovarianceMatrix a x i p q =
      (2 - ell i) *
          ((if p = q then 1 else 0) - x i p * x i q) +
        ((Fintype.card K : ℝ) - 1) * ell i * x i p * x i q) :
    sphereResidualLinear a x =
      (diagonalMultiplier
        (fun i => (Fintype.card K : ℝ) * ell i)).comp
        (sphereSamplingLinear x) := by
  apply oneShell_residual_factorization
  intro A i
  exact oneShell_sphereResidual_row a x ell hx hcov A i

/-- Nonzero shell losses make every diagonal factor nonzero. -/
theorem oneShell_sphereScale_ne_zero
    {I K : Type*} [Fintype K] [Nonempty K]
    (ell : I → ℝ) (hell : ∀ i, ell i ≠ 0) :
    ∀ i, (Fintype.card K : ℝ) * ell i ≠ 0 := by
  intro i
  apply mul_ne_zero
  · exact_mod_cast Fintype.card_ne_zero
  · exact hell i

/-- In the nondegenerate one-shell case, form exactness is exactly sampling
aliasing: `E_form = K_X`. -/
theorem oneShell_sphereResidualKernel_eq_samplingKernel
    {I K : Type*}
    [Fintype I] [DecidableEq I]
    [Fintype K] [DecidableEq K] [Nonempty K]
    (a : I → I → ℝ) (x : I → K → ℝ) (ell : I → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (hcov : ∀ i p q, jumpCovarianceMatrix a x i p q =
      (2 - ell i) *
          ((if p = q then 1 else 0) - x i p * x i q) +
        ((Fintype.card K : ℝ) - 1) * ell i * x i p * x i q)
    (hell : ∀ i, ell i ≠ 0) :
    LinearMap.ker (sphereResidualLinear a x) =
      LinearMap.ker (sphereSamplingLinear x) := by
  apply oneShell_residualKernel_eq_samplingKernel
    (sphereSamplingLinear x) (sphereResidualLinear a x)
    (fun i => (Fintype.card K : ℝ) * ell i)
    (oneShell_sphereScale_ne_zero ell hell)
  exact oneShell_sphereResidual_row a x ell hx hcov

/-- The one-shell factorization preserves sampling rank. -/
theorem oneShell_sphereResidualRank_eq_samplingRank
    {I K : Type*}
    [Fintype I] [DecidableEq I]
    [Fintype K] [DecidableEq K] [Nonempty K]
    (a : I → I → ℝ) (x : I → K → ℝ) (ell : I → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (hcov : ∀ i p q, jumpCovarianceMatrix a x i p q =
      (2 - ell i) *
          ((if p = q then 1 else 0) - x i p * x i q) +
        ((Fintype.card K : ℝ) - 1) * ell i * x i p * x i q)
    (hell : ∀ i, ell i ≠ 0) :
    Module.finrank ℝ (LinearMap.range (sphereResidualLinear a x)) =
      Module.finrank ℝ (LinearMap.range (sphereSamplingLinear x)) := by
  apply oneShell_residualRank_eq_samplingRank
    (sphereSamplingLinear x) (sphereResidualLinear a x)
    (fun i => (Fintype.card K : ℝ) * ell i)
    (oneShell_sphereScale_ne_zero ell hell)
  exact oneShell_sphereResidual_row a x ell hx hcov

/-- No genuinely nonzero sampled exact quadratic survives the nondegenerate
one-shell factorization: `E_sample = {0}`. -/
theorem oneShell_sphereSampledExactRange_eq_bot
    {I K : Type*}
    [Fintype I] [DecidableEq I]
    [Fintype K] [DecidableEq K] [Nonempty K]
    (a : I → I → ℝ) (x : I → K → ℝ) (ell : I → ℝ)
    (hx : ∀ p i,
      jumpGenerator a (fun j => x j p) i =
        -((Fintype.card K : ℝ) - 1) * x i p)
    (hcov : ∀ i p q, jumpCovarianceMatrix a x i p q =
      (2 - ell i) *
          ((if p = q then 1 else 0) - x i p * x i q) +
        ((Fintype.card K : ℝ) - 1) * ell i * x i p * x i q)
    (hell : ∀ i, ell i ≠ 0) :
    linearSampledExactRange (jumpGeneratorLinear a)
        (2 * (Fintype.card K : ℝ)) (sphereSamplingLinear x) = ⊥ := by
  simpa only [sphereResidualLinear] using
    oneShell_sampledExactRange_eq_bot
      (sphereSamplingLinear x) (sphereResidualLinear a x)
      (fun i => (Fintype.card K : ℝ) * ell i)
      (oneShell_sphereScale_ne_zero ell hell)
      (oneShell_sphereResidual_row a x ell hx hcov)

end AFPBarrier
