import AFPBarrier.QuantitativeGlobalNearRigidity
import AFPBarrier.OneShellQuadraticRigidity
import AFPBarrier.QuadraticSphereResidual
import Mathlib.Tactic

/-!
# Covariance consequences and anisotropy boundary at `Q=1`

The exact quality equality fixes the radial covariance coefficient.  The
tangential second moment remains independent data; this module records its
finite entrywise decomposition and its exact equivalence with the dimension
three one-shell axial hypothesis from Prompt 2.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
variable [Fintype ι] [DecidableEq ι]

/-- Trace as a weighted sum of squared displacement norms is four when the
normal loss moment is two and `|Omega_j-Omega_i|^2=2 ell_ij`. -/
theorem covarianceTrace_eq_four_of_normLoss
    (a loss normDiffSq : ι → ι → ℝ) (i : ι)
    (hnorm : ∀ j ∈ offdiag i, normDiffSq i j = 2 * loss i j)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    (offdiag i).sum (fun j => a i j * normDiffSq i j) = 4 := by
  calc
    (offdiag i).sum (fun j => a i j * normDiffSq i j) =
        (offdiag i).sum (fun j => a i j * (2 * loss i j)) := by
          apply Finset.sum_congr rfl
          intro j hj
          rw [hnorm j hj]
    _ = 2 * (offdiag i).sum (fun j => a i j * loss i j) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = 4 := by rw [hmoment]; norm_num

/-- The covariance radial quadratic form is the spherical second loss moment
when the radial displacement is `-ell_ij`. -/
theorem radialCovariance_eq_sphericalEpsilon
    (a loss radialDiff : ι → ι → ℝ) (i : ι)
    (hradial : ∀ j ∈ offdiag i, radialDiff i j = -loss i j) :
    (offdiag i).sum (fun j => a i j * (radialDiff i j) ^ 2) =
      sphericalEpsilonAt a loss i := by
  unfold sphericalEpsilonAt
  apply Finset.sum_congr rfl
  intro j hj
  rw [hradial j hj]
  ring

/-- Rearrangement of `Q=r epsilon/4`: radial covariance is `4Q/r`. -/
theorem sphericalEpsilon_eq_four_mul_Q_div_rate
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i) :
    sphericalEpsilonAt a loss i =
      4 * sphericalQAt a loss i / jumpRate a i := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  unfold sphericalQAt
  field_simp [hrne]

/-- Normalized tangential second-moment entry. -/
def normalizedTangentSecondMoment
    (s : Finset ι) (pweight : ι → ℝ)
    (u : ι → κ → ℝ) (k l : κ) : ℝ :=
  s.sum (fun j => pweight j * u j k * u j l)

/-- Entry of the orthogonal projector onto the tangent space at `z`. -/
def tangentProjectorEntry
    [DecidableEq κ] (z : κ → ℝ) (k l : κ) : ℝ :=
  (if k = l then 1 else 0) - z k * z l

/-- A normalized affine tangent parametrization is centered whenever its
weighted spherical barycenter is the radial point `(1-ell)z`.  This is the
finite algebraic centering step used in the exact `Q=1` covariance split. -/
theorem normalizedTangent_centered_of_barycenter
    (s : Finset ι) (pweight : ι → ℝ)
    (Omega u : ι → κ → ℝ) (z : κ → ℝ)
    (ell sigma : ℝ)
    (hsum : s.sum pweight = 1)
    (hbarycenter : ∀ k,
      s.sum (fun j => pweight j * Omega j k) = (1 - ell) * z k)
    (hparametrization : ∀ j ∈ s, ∀ k,
      Omega j k = (1 - ell) * z k + sigma * u j k)
    (hsigma : sigma ≠ 0) :
    ∀ k, s.sum (fun j => pweight j * u j k) = 0 := by
  intro k
  have hexpand :
      s.sum (fun j => pweight j * Omega j k) =
        (1 - ell) * z k * s.sum pweight +
          sigma * s.sum (fun j => pweight j * u j k) := by
    calc
      s.sum (fun j => pweight j * Omega j k) =
          s.sum (fun j => pweight j *
            ((1 - ell) * z k + sigma * u j k)) := by
              apply Finset.sum_congr rfl
              intro j hj
              rw [hparametrization j hj k]
      _ = (1 - ell) * z k * s.sum pweight +
            sigma * s.sum (fun j => pweight j * u j k) := by
              simp only [mul_add, Finset.sum_add_distrib]
              apply congrArg₂ (fun x y : ℝ => x + y)
              · rw [← Finset.sum_mul]
                ring
              · rw [Finset.mul_sum]
                apply Finset.sum_congr rfl
                intro j hj
                ring
  rw [hbarycenter k, hsum] at hexpand
  have hzero :
      sigma * s.sum (fun j => pweight j * u j k) = 0 := by
    linarith
  exact (mul_eq_zero.mp hzero).resolve_left hsigma

/-- Unit tangent directions and normalized weights give `tr T=1`.  The trace
is written as an explicit finite diagonal sum so the statement is independent
of a matrix-wrapper choice. -/
theorem normalizedTangentSecondMoment_trace_one
    [Fintype κ]
    (s : Finset ι) (pweight : ι → ℝ) (u : ι → κ → ℝ)
    (hsum : s.sum pweight = 1)
    (hunit : ∀ j ∈ s, ∑ k, (u j k) ^ 2 = 1) :
    ∑ k, normalizedTangentSecondMoment s pweight u k k = 1 := by
  classical
  unfold normalizedTangentSecondMoment
  rw [Finset.sum_comm]
  calc
    ∑ j ∈ s, ∑ k, pweight j * u j k * u j k =
        ∑ j ∈ s, pweight j * ∑ k, (u j k) ^ 2 := by
          apply Finset.sum_congr rfl
          intro j hj
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro k hk
          ring
    _ = ∑ j ∈ s, pweight j := by
          apply Finset.sum_congr rfl
          intro j hj
          rw [hunit j hj]
          ring
    _ = 1 := hsum

/-- A centered weighted affine product has only its constant and second-moment
terms. -/
theorem weighted_centered_affine_product_sum
    (s : Finset ι) (p u v : ι → ℝ)
    (A B C D : ℝ)
    (hsum : s.sum p = 1)
    (hcenterU : s.sum (fun j => p j * u j) = 0)
    (hcenterV : s.sum (fun j => p j * v j) = 0) :
    s.sum (fun j => p j * ((A + B * u j) * (C + D * v j))) =
      A * C + B * D * s.sum (fun j => p j * u j * v j) := by
  calc
    s.sum (fun j => p j * ((A + B * u j) * (C + D * v j))) =
        s.sum (fun j =>
          p j * A * C +
            (A * D) * (p j * v j) +
            (B * C) * (p j * u j) +
            (B * D) * (p j * u j * v j)) := by
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = s.sum (fun j => p j * A * C) +
          s.sum (fun j => (A * D) * (p j * v j)) +
          s.sum (fun j => (B * C) * (p j * u j)) +
          s.sum (fun j => (B * D) * (p j * u j * v j)) := by
          simp only [Finset.sum_add_distrib]
    _ = (s.sum p) * A * C +
          (A * D) * s.sum (fun j => p j * v j) +
          (B * C) * s.sum (fun j => p j * u j) +
          (B * D) * s.sum (fun j => p j * u j * v j) := by
          simp only [Finset.sum_mul, Finset.mul_sum]
    _ = A * C + B * D * s.sum (fun j => p j * u j * v j) := by
          rw [hsum, hcenterU, hcenterV]
          ring

/-- Entrywise exact `Q=1` covariance decomposition.  The displacement is
`-ell*z + sigma*u`; centering removes the radial-tangential blocks. -/
theorem qOne_covarianceEntry_decomposition
    (s : Finset ι) (pweight : ι → ℝ) (u : ι → κ → ℝ)
    (z : κ → ℝ) (k l : κ)
    (rate ell sigma : ℝ)
    (hsum : s.sum pweight = 1)
    (hcenterK : s.sum (fun j => pweight j * u j k) = 0)
    (hcenterL : s.sum (fun j => pweight j * u j l) = 0)
    (hrateLoss : rate * ell = 2)
    (hsigma : sigma ^ 2 = ell * (2 - ell)) :
    rate * s.sum (fun j =>
      pweight j *
        ((-ell * z k + sigma * u j k) *
          (-ell * z l + sigma * u j l))) =
      2 * ell * z k * z l +
        2 * (2 - ell) *
          normalizedTangentSecondMoment s pweight u k l := by
  have hcentered := weighted_centered_affine_product_sum
    (s := s) (p := pweight) (u := fun j => u j k) (v := fun j => u j l)
    (A := -ell * z k) (B := sigma)
    (C := -ell * z l) (D := sigma)
    hsum hcenterK hcenterL
  have hsigmaMul : sigma * sigma = ell * (2 - ell) := by
    simpa only [pow_two] using hsigma
  rw [hcentered, hsigmaMul]
  unfold normalizedTangentSecondMoment
  calc
    rate *
        ((-ell * z k) * (-ell * z l) +
          ell * (2 - ell) *
            s.sum (fun j => pweight j * u j k * u j l)) =
        (rate * ell) * ell * z k * z l +
          (rate * ell) * (2 - ell) *
            s.sum (fun j => pweight j * u j k * u j l) := by ring
    _ = 2 * ell * z k * z l +
          2 * (2 - ell) *
            s.sum (fun j => pweight j * u j k * u j l) := by
          rw [hrateLoss]

/-- The actual jump covariance is the row rate times its normalized
displacement second moment. -/
theorem jumpCovariance_eq_rate_mul_normalized
    [Fintype κ] [DecidableEq κ]
    (a : ι → ι → ℝ) (Omega : ι → κ → ℝ) (i : ι) (k l : κ)
    (hrate : 0 < jumpRate a i) :
    jumpCovarianceMatrix a Omega i k l =
      jumpRate a i * (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          (Omega j k - Omega i k) * (Omega j l - Omega i l)) := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  unfold jumpCovarianceMatrix
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  field_simp [hrne]

/-- Actual covariance decomposition from normalized tangent data. -/
theorem qOne_jumpCovariance_decomposition
    [Fintype κ] [DecidableEq κ]
    (a : ι → ι → ℝ) (Omega : ι → κ → ℝ) (i : ι)
    (u : ι → κ → ℝ) (ell sigma : ℝ)
    (hrate : 0 < jumpRate a i)
    (hdisplacement : ∀ j ∈ offdiag i, ∀ k,
      Omega j k - Omega i k = -ell * Omega i k + sigma * u j k)
    (hcenter : ∀ k,
      (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) * u j k) = 0)
    (hrateLoss : jumpRate a i * ell = 2)
    (hsigma : sigma ^ 2 = ell * (2 - ell))
    (k l : κ) :
    jumpCovarianceMatrix a Omega i k l =
      2 * ell * Omega i k * Omega i l +
        2 * (2 - ell) *
          normalizedTangentSecondMoment (offdiag i)
            (fun j => a i j / jumpRate a i) u k l := by
  rw [jumpCovariance_eq_rate_mul_normalized a Omega i k l hrate]
  have hrewrite :
      (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          (Omega j k - Omega i k) * (Omega j l - Omega i l)) =
      (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          ((-ell * Omega i k + sigma * u j k) *
            (-ell * Omega i l + sigma * u j l))) := by
    apply Finset.sum_congr rfl
    intro j hj
    rw [hdisplacement j hj k, hdisplacement j hj l]
    ring
  rw [hrewrite]
  exact qOne_covarianceEntry_decomposition
    (s := offdiag i)
    (pweight := fun j => a i j / jumpRate a i)
    (u := u) (z := Omega i) (k := k) (l := l)
    (rate := jumpRate a i) (ell := ell) (sigma := sigma)
    (normalizedEdgeWeight_sum_one a i hrate)
    (hcenter k) (hcenter l) hrateLoss hsigma

/-- Exact axial covariance is equivalent to the normalized tangent moment
being one half of the tangent projector. -/
theorem qOne_covariance_axial_iff_tangentHalf
    [DecidableEq κ]
    (ell : ℝ) (hell : ell < 2)
    (z : κ → ℝ) (C T : κ → κ → ℝ)
    (hC : ∀ k l,
      C k l = 2 * ell * z k * z l + 2 * (2 - ell) * T k l) :
    (∀ k l,
      C k l = (2 - ell) * tangentProjectorEntry z k l +
        2 * ell * z k * z l) ↔
      (∀ k l, T k l = tangentProjectorEntry z k l / 2) := by
  constructor
  · intro haxial k l
    have hcoeff : 0 < 2 * (2 - ell) := by nlinarith
    have h := haxial k l
    rw [hC k l] at h
    have hfactor :
        2 * (2 - ell) *
          (T k l - tangentProjectorEntry z k l / 2) = 0 := by
      nlinarith
    have hzero : T k l - tangentProjectorEntry z k l / 2 = 0 :=
      (mul_eq_zero.mp hfactor).resolve_left (ne_of_gt hcoeff)
    exact sub_eq_zero.mp hzero
  · intro htangent k l
    rw [hC k l, htangent k l]
    ring

/-- Raw one-shell second moment equals the row rate times its normalized
version. -/
theorem oneShellSecondMoment_eq_rate_mul_normalized
    [Fintype κ] [DecidableEq κ]
    (J : Finset ι) (row : ι → ℝ) (u : ι → κ → ℝ)
    (rate : ℝ) (hrate : 0 < rate) (k l : κ) :
    oneShellSecondMoment J row u k l =
      rate * normalizedTangentSecondMoment J
        (fun j => row j / rate) u k l := by
  have hrne : rate ≠ 0 := ne_of_gt hrate
  unfold oneShellSecondMoment normalizedTangentSecondMoment
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  field_simp [hrne]

/-- In dimension three, the Prompt-2 full tangent-moment condition is exactly
`T=P/2`. -/
theorem normalizedTangentHalf_iff_d3_oneShellSecondMoment
    [Fintype κ] [DecidableEq κ]
    (J : Finset ι) (row : ι → ℝ) (u : ι → κ → ℝ)
    (z : κ → ℝ) (rate : ℝ) (hrate : 0 < rate) :
    (∀ k l,
      normalizedTangentSecondMoment J (fun j => row j / rate) u k l =
        tangentProjectorEntry z k l / 2) ↔
      (∀ k l,
        oneShellSecondMoment J row u k l =
          (rate / ((3 : ℝ) - 1)) * tangentProjectorEntry z k l) := by
  constructor
  · intro htangent k l
    rw [oneShellSecondMoment_eq_rate_mul_normalized
      J row u rate hrate k l, htangent k l]
    norm_num
    ring
  · intro hsecond k l
    have h := hsecond k l
    rw [oneShellSecondMoment_eq_rate_mul_normalized
      J row u rate hrate k l] at h
    norm_num at h
    have hrne : rate ≠ 0 := ne_of_gt hrate
    calc
      normalizedTangentSecondMoment J (fun j => row j / rate) u k l =
          (rate * normalizedTangentSecondMoment J
            (fun j => row j / rate) u k l) / rate := by
            field_simp [hrne]
      _ = ((rate / 2) * tangentProjectorEntry z k l) / rate := by
            rw [h]
      _ = tangentProjectorEntry z k l / 2 := by
            field_simp [hrne]

/-- Scalar algebra behind the degree-two residual tensor decomposition. -/
theorem qOne_residual_entry_algebra
    (ell zz diag T P C M : ℝ)
    (hP : P = diag - zz)
    (hC : C = 2 * ell * zz + 2 * (2 - ell) * T)
    (hM : M = C + 2 * zz - 2 * diag) :
    M = 3 * ell * (zz - diag / 3) +
      2 * (2 - ell) * (T - P / 2) := by
  rw [hM, hC, hP]
  ring

/-- If the unprojected covariance-plus-outer-product has trace six in three
dimensions, the Prompt-2 trace-free projection subtracts `2 I`. -/
theorem sphereResidualMatrix_entry_of_trace_six
    {I K : Type*}
    [Fintype I] [DecidableEq I]
    [Fintype K] [DecidableEq K]
    (a : I → I → ℝ) (Omega : I → K → ℝ) (i : I) (k l : K)
    (hcard : Fintype.card K = 3)
    (htrace :
      (jumpCovarianceMatrix a Omega i +
        (2 : ℝ) • Matrix.vecMulVec (Omega i) (Omega i)).trace = 6) :
    sphereResidualMatrix a Omega i k l =
      jumpCovarianceMatrix a Omega i k l +
        2 * Omega i k * Omega i l - (if k = l then 2 else 0) := by
  unfold sphereResidualMatrix traceFreeProjection
  simp only [Matrix.add_apply, Matrix.smul_apply, Matrix.vecMulVec_apply,
    smul_eq_mul]
  rw [htrace, hcard]
  by_cases hkl : k = l <;> simp [hkl]
  <;> ring

/-- The complete dimension-three residual entry formula.  Unlike
`sphereResidualMatrix_entry_of_trace_six`, this theorem derives the trace-six
normalization from `tr C=4`, `|z|^2=1`, and the exact `Q=1` covariance split;
the latter trace follows in turn from `tr T=1`. -/
theorem qOne_sphereResidual_entry_decomposition
    {I K : Type*}
    [Fintype I] [DecidableEq I]
    [Fintype K] [DecidableEq K]
    (a : I → I → ℝ) (Omega : I → K → ℝ) (i : I)
    (T : K → K → ℝ) (ell : ℝ)
    (hcard : Fintype.card K = 3)
    (hunit : ∑ k, (Omega i k) ^ 2 = 1)
    (htraceT : ∑ k, T k k = 1)
    (hC : ∀ k l,
      jumpCovarianceMatrix a Omega i k l =
        2 * ell * Omega i k * Omega i l + 2 * (2 - ell) * T k l)
    (k l : K) :
    sphereResidualMatrix a Omega i k l =
      3 * ell *
          (Omega i k * Omega i l - (if k = l then 1 else 0) / 3) +
        2 * (2 - ell) *
          (T k l - tangentProjectorEntry (Omega i) k l / 2) := by
  classical
  have htraceC : (jumpCovarianceMatrix a Omega i).trace = 4 := by
    unfold Matrix.trace
    simp only [Matrix.diag_apply]
    calc
      ∑ m, jumpCovarianceMatrix a Omega i m m =
          ∑ m, (2 * ell * Omega i m * Omega i m +
            2 * (2 - ell) * T m m) := by
              apply Finset.sum_congr rfl
              intro m hm
              rw [hC m m]
      _ = 2 * ell * ∑ m, (Omega i m) ^ 2 +
            2 * (2 - ell) * ∑ m, T m m := by
              rw [Finset.mul_sum, Finset.mul_sum]
              simp only [Finset.sum_add_distrib]
              apply congrArg₂ (fun x y : ℝ => x + y)
              · apply Finset.sum_congr rfl
                intro m hm
                ring
              · rfl
      _ = 4 := by rw [hunit, htraceT]; ring
  have htraceSix :
      (jumpCovarianceMatrix a Omega i +
        (2 : ℝ) • Matrix.vecMulVec (Omega i) (Omega i)).trace = 6 := by
    unfold Matrix.trace
    simp only [Matrix.diag_apply, Matrix.add_apply, Matrix.smul_apply,
      Matrix.vecMulVec_apply, smul_eq_mul]
    calc
      ∑ m, (jumpCovarianceMatrix a Omega i m m +
          2 * (Omega i m * Omega i m)) =
          (jumpCovarianceMatrix a Omega i).trace +
            2 * ∑ m, (Omega i m) ^ 2 := by
              rw [Finset.mul_sum]
              simp only [Matrix.trace, Matrix.diag_apply,
                Finset.sum_add_distrib]
              apply congrArg₂ (fun x y : ℝ => x + y) rfl
              apply Finset.sum_congr rfl
              intro m hm
              ring
      _ = 6 := by rw [htraceC, hunit]; norm_num
  have hentry := sphereResidualMatrix_entry_of_trace_six
    a Omega i k l hcard htraceSix
  have hresidual :
      sphereResidualMatrix a Omega i k l =
        jumpCovarianceMatrix a Omega i k l +
          2 * (Omega i k * Omega i l) -
            2 * (if k = l then 1 else 0) := by
    rw [hentry]
    by_cases hkl : k = l <;> simp [hkl] <;> ring
  have halgebra := qOne_residual_entry_algebra
    ell
    (Omega i k * Omega i l)
    (if k = l then 1 else 0)
    (T k l)
    (tangentProjectorEntry (Omega i) k l)
    (jumpCovarianceMatrix a Omega i k l)
    (sphereResidualMatrix a Omega i k l)
    (by simp [tangentProjectorEntry])
    (by simpa only [mul_assoc] using hC k l)
    hresidual
  exact halgebra

/-- At one weighted octahedral axis, equal tangent weights are equivalent to
equal conductances. -/
theorem weightedOctahedron_axis_axial_iff
    (g₁ g₂ : ℝ) (hsum : 0 < g₁ + g₂) :
    g₁ / (g₁ + g₂) = g₂ / (g₁ + g₂) ↔ g₁ = g₂ := by
  have hne : g₁ + g₂ ≠ 0 := ne_of_gt hsum
  constructor
  · intro h
    field_simp [hne] at h
    linarith
  · intro h
    rw [h]

/-- For the three weighted-octahedron coordinate axes, axial equality on all
axes is equivalent to equality of the three conductance parameters, assuming
the three pairwise sums are positive.
Each conjunct is exactly the two-direction tangent-weight comparison at the
remaining axis. -/
theorem weightedOctahedron_all_axes_axial_iff
    (g₁ g₂ g₃ : ℝ)
    (h₁₂ : 0 < g₁ + g₂)
    (h₁₃ : 0 < g₁ + g₃)
    (h₂₃ : 0 < g₂ + g₃) :
    (g₂ / (g₂ + g₃) = g₃ / (g₂ + g₃) ∧
      g₁ / (g₁ + g₃) = g₃ / (g₁ + g₃) ∧
      g₁ / (g₁ + g₂) = g₂ / (g₁ + g₂)) ↔
      g₁ = g₂ ∧ g₂ = g₃ := by
  rw [weightedOctahedron_axis_axial_iff g₂ g₃ h₂₃]
  rw [weightedOctahedron_axis_axial_iff g₁ g₃ h₁₃]
  rw [weightedOctahedron_axis_axial_iff g₁ g₂ h₁₂]
  constructor
  · rintro ⟨h₂₃', h₁₃', h₁₂'⟩
    exact ⟨h₁₂', h₂₃'⟩
  · rintro ⟨h₁₂', h₂₃'⟩
    exact ⟨h₂₃', h₁₂'.trans h₂₃', h₁₂'⟩

end AFPBarrier
