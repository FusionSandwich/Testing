import AFPBarrier.SharedEdgeEquilibrium
import AFPBarrier.ReversibleConductance
import Mathlib.Tactic

/-!
# Finite algebra for convex reversible-generator design

This module certifies the solver-independent finite identities used by the
convex design programs.  It deliberately stops short of formalizing analytic
conic strong duality.  The results here cover positivity and exactness under
convex mixing, affinity of sampled-shell residuals, the loss-weighted
conductance identity forced by degree-one reproduction, and soundness of a
rate-capped Farkas certificate.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I E K R S : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype E] [DecidableEq E]
  [Fintype K] [DecidableEq K]
  [Fintype R] [DecidableEq R]
  [Fintype S] [DecidableEq S]

/-! ## Positive reversible generator identities -/

/-- Conductance generators reproduce constants exactly, independently of the
conductance values. -/
theorem convexDesign_constant_exact
    (Gamma : I → I → ℝ) (w : I → ℝ) (c : ℝ) (i : I) :
    jumpGenerator (conductanceRate Gamma w) (fun _ => c) i = 0 := by
  exact jumpGenerator_const (conductanceRate Gamma w) c i

/-- Nonnegative shared conductances and positive masses give nonnegative
off-diagonal jump rates. -/
theorem convexDesign_rate_nonneg
    (Gamma : I → I → ℝ) (w : I → ℝ)
    (hGamma : ∀ i j, i ≠ j → 0 ≤ Gamma i j)
    (hw : ∀ i, 0 < w i)
    (i j : I) (hij : i ≠ j) :
    0 ≤ conductanceRate Gamma w i j := by
  exact conductanceRate_nonneg Gamma w hGamma hw i j hij

/-- Symmetric shared conductances give detailed balance with respect to the
quadrature masses. -/
theorem convexDesign_detailedBalance
    (Gamma : I → I → ℝ) (w : I → ℝ)
    (hGamma : ∀ i j, Gamma i j = Gamma j i)
    (hw : ∀ i, w i ≠ 0)
    (i j : I) :
    w i * conductanceRate Gamma w i j =
      w j * conductanceRate Gamma w j i := by
  exact conductanceRate_detailedBalance Gamma w hGamma hw i j

/-! ## Convex mixing of shared conductances -/

/-- Pointwise affine interpolation of two edge-conductance vectors. -/
def conductanceMix (theta : ℝ) (gamma0 gamma1 : E → ℝ) (e : E) : ℝ :=
  (1 - theta) * gamma0 e + theta * gamma1 e

/-- The nonnegative conductance cone is convex. -/
theorem conductanceMix_nonneg
    (theta : ℝ) (gamma0 gamma1 : E → ℝ)
    (htheta0 : 0 ≤ theta) (htheta1 : theta ≤ 1)
    (hgamma0 : ∀ e, 0 ≤ gamma0 e)
    (hgamma1 : ∀ e, 0 ≤ gamma1 e) :
    ∀ e, 0 ≤ conductanceMix theta gamma0 gamma1 e := by
  intro e
  exact add_nonneg
    (mul_nonneg (sub_nonneg.mpr htheta1) (hgamma0 e))
    (mul_nonneg htheta0 (hgamma1 e))

/-- The shared-edge equilibrium action is linear in the conductances. -/
theorem sharedEdgeApply_conductanceMix
    (Omega : I → K → ℝ) (left right : E → I)
    (theta : ℝ) (gamma0 gamma1 : E → ℝ) (i : I) (k : K) :
    sharedEdgeApply Omega left right
        (conductanceMix theta gamma0 gamma1) i k =
      (1 - theta) * sharedEdgeApply Omega left right gamma0 i k +
        theta * sharedEdgeApply Omega left right gamma1 i k := by
  classical
  unfold sharedEdgeApply conductanceMix
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro e he
  ring

/-- Two exact shared-edge solutions with the same target remain exact after
convex (indeed affine) interpolation. -/
theorem sharedEdge_exact_conductanceMix
    (Omega : I → K → ℝ) (left right : E → I)
    (b : I → K → ℝ)
    (theta : ℝ) (gamma0 gamma1 : E → ℝ)
    (hexact0 : ∀ i k, sharedEdgeApply Omega left right gamma0 i k = b i k)
    (hexact1 : ∀ i k, sharedEdgeApply Omega left right gamma1 i k = b i k) :
    ∀ i k,
      sharedEdgeApply Omega left right
        (conductanceMix theta gamma0 gamma1) i k = b i k := by
  intro i k
  rw [sharedEdgeApply_conductanceMix, hexact0 i k, hexact1 i k]
  ring

/-- A generic finite linear inequality is preserved by convex mixing.  This
is the algebra behind every fixed row-rate cap. -/
theorem finiteMatrixApply_conductanceMix_le
    (C : R → E → ℝ) (d : R → ℝ)
    (theta : ℝ) (gamma0 gamma1 : E → ℝ)
    (htheta0 : 0 ≤ theta) (htheta1 : theta ≤ 1)
    (hcap0 : ∀ r, finiteMatrixApply C gamma0 r ≤ d r)
    (hcap1 : ∀ r, finiteMatrixApply C gamma1 r ≤ d r) :
    ∀ r, finiteMatrixApply C (conductanceMix theta gamma0 gamma1) r ≤ d r := by
  intro r
  have hlinear :
      finiteMatrixApply C (conductanceMix theta gamma0 gamma1) r =
        (1 - theta) * finiteMatrixApply C gamma0 r +
          theta * finiteMatrixApply C gamma1 r := by
    classical
    unfold finiteMatrixApply conductanceMix
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro e he
    ring
  rw [hlinear]
  calc
    (1 - theta) * finiteMatrixApply C gamma0 r +
          theta * finiteMatrixApply C gamma1 r ≤
        (1 - theta) * d r + theta * d r :=
      add_le_add
        (mul_le_mul_of_nonneg_left (hcap0 r) (sub_nonneg.mpr htheta1))
        (mul_le_mul_of_nonneg_left (hcap1 r) htheta0)
    _ = d r := by ring

/-! ## Affine shell residuals -/

/-- A sampled-shell residual is an affine function of the conductances: a
fixed target term plus one column for each permitted edge. -/
def affineShellResidual
    (base : R → ℝ) (column : R → E → ℝ)
    (gamma : E → ℝ) (r : R) : ℝ :=
  base r + finiteMatrixApply column gamma r

/-- Exact affine interpolation formula for the residual. -/
theorem affineShellResidual_conductanceMix
    (base : R → ℝ) (column : R → E → ℝ)
    (theta : ℝ) (gamma0 gamma1 : E → ℝ) (r : R) :
    affineShellResidual base column
        (conductanceMix theta gamma0 gamma1) r =
      (1 - theta) * affineShellResidual base column gamma0 r +
        theta * affineShellResidual base column gamma1 r := by
  have hlinear :
      finiteMatrixApply column (conductanceMix theta gamma0 gamma1) r =
        (1 - theta) * finiteMatrixApply column gamma0 r +
          theta * finiteMatrixApply column gamma1 r := by
    classical
    unfold finiteMatrixApply conductanceMix
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro e he
    ring
  unfold affineShellResidual
  rw [hlinear]
  ring

/-! ## The degree-one radial identity fixes weighted total conductance -/

/-- At a node, each incident undirected edge contributes its conductance
times its spherical chord loss.  A loop is counted twice, consistently with
the two-endpoint incidence convention. -/
def incidentLossMass
    (left right : E → I) (gamma ell : E → ℝ) (i : I) : ℝ :=
  ∑ e, ((if i = left e then gamma e * ell e else 0) +
    (if i = right e then gamma e * ell e else 0))

/-- Double counting the endpoint incidences gives twice the undirected
loss-weighted total conductance. -/
theorem sum_incidentLossMass
    (left right : E → I) (gamma ell : E → ℝ) :
    ∑ i, incidentLossMass left right gamma ell i =
      2 * ∑ e, gamma e * ell e := by
  classical
  unfold incidentLossMass
  calc
    (∑ i, ∑ e, ((if i = left e then gamma e * ell e else 0) +
      (if i = right e then gamma e * ell e else 0))) =
        ∑ e, ∑ i, ((if i = left e then gamma e * ell e else 0) +
          (if i = right e then gamma e * ell e else 0)) := by
          rw [Finset.sum_comm]
    _ = ∑ e, 2 * (gamma e * ell e) := by
          apply Finset.sum_congr rfl
          intro e he
          simp [Finset.sum_add_distrib]
          ring
    _ = 2 * ∑ e, gamma e * ell e := by
          rw [Finset.mul_sum]

/-- If every radial degree-one equation has target `lambda * w_i`, then the
loss-weighted total conductance is exactly half the target mass. -/
theorem lossWeightedTotal_fixed_of_radialExact
    (left right : E → I) (gamma ell : E → ℝ)
    (w : I → ℝ) (lambda : ℝ)
    (hradial : ∀ i,
      incidentLossMass left right gamma ell i = lambda * w i) :
    ∑ e, gamma e * ell e =
      (lambda / 2) * ∑ i, w i := by
  have hsum :
      2 * ∑ e, gamma e * ell e =
        lambda * ∑ i, w i := by
    calc
      2 * ∑ e, gamma e * ell e =
          ∑ i, incidentLossMass left right gamma ell i :=
        (sum_incidentLossMass left right gamma ell).symm
      _ = ∑ i, lambda * w i := by
        apply Finset.sum_congr rfl
        intro i hi
        exact hradial i
      _ = lambda * ∑ i, w i := by rw [Finset.mul_sum]
  linarith

/-- On `S^2`, normalized quadrature mass and exact coordinate eigenvalue two
force `sum_e gamma_e (1 - omega_i dot omega_j) = 1`. -/
theorem S2_lossWeightedTotal_one
    (left right : E → I) (gamma ell : E → ℝ)
    (w : I → ℝ)
    (hradial : ∀ i, incidentLossMass left right gamma ell i = 2 * w i)
    (hmass : ∑ i, w i = 1) :
    ∑ e, gamma e * ell e = 1 := by
  rw [lossWeightedTotal_fixed_of_radialExact
    left right gamma ell w 2 hradial, hmass]
  norm_num

/-- If every permitted edge has one common nonzero loss, fixing the
loss-weighted objective also fixes the unweighted total conductance.  Thus an
unweighted `l1` objective is constant on a one-shell exact feasible set. -/
theorem totalConductance_fixed_of_constantLoss
    (gamma ell : E → ℝ) (ell0 target : ℝ)
    (hell : ∀ e, ell e = ell0)
    (hell0 : ell0 ≠ 0)
    (hfixed : ∑ e, gamma e * ell e = target) :
    ∑ e, gamma e = target / ell0 := by
  apply (eq_div_iff hell0).2
  calc
    (∑ e, gamma e) * ell0 = ∑ e, gamma e * ell0 := by
      rw [Finset.sum_mul]
    _ = ∑ e, gamma e * ell e := by
      apply Finset.sum_congr rfl
      intro e he
      rw [hell e]
    _ = target := hfixed

/-! ## Sound rate-capped Farkas certificates -/

/-- Weak duality for a nonnegative equality system with additional upper
inequalities.  In matrix notation the hypotheses are

`A x = b`, `C x ≤ d`, `x ≥ 0`, `z ≥ 0`, and
`Aᵀ y + Cᵀ z ≥ 0`.

They imply `b·y + d·z ≥ 0`. -/
theorem rateCapped_dualWork_nonneg
    (A : R → E → ℝ) (C : S → E → ℝ)
    (b y : R → ℝ) (d z : S → ℝ) (x : E → ℝ)
    (hx : ∀ e, 0 ≤ x e)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hCx : ∀ s, finiteMatrixApply C x s ≤ d s)
    (hz : ∀ s, 0 ≤ z s)
    (hdual : ∀ e,
      0 ≤ finiteTransposeApply A y e + finiteTransposeApply C z e) :
    0 ≤ finiteDot b y + finiteDot d z := by
  have hcone :
      0 ≤ finiteDot x (fun e =>
        finiteTransposeApply A y e + finiteTransposeApply C z e) := by
    unfold finiteDot
    apply Finset.sum_nonneg
    intro e he
    exact mul_nonneg (hx e) (hdual e)
  have hrewrite :
      finiteDot x (fun e =>
          finiteTransposeApply A y e + finiteTransposeApply C z e) =
        finiteDot b y + finiteDot (finiteMatrixApply C x) z := by
    calc
      finiteDot x (fun e =>
          finiteTransposeApply A y e + finiteTransposeApply C z e) =
          finiteDot x (finiteTransposeApply A y) +
            finiteDot x (finiteTransposeApply C z) := by
              unfold finiteDot
              rw [← Finset.sum_add_distrib]
              apply Finset.sum_congr rfl
              intro e he
              ring
      _ = finiteDot (finiteMatrixApply A x) y +
            finiteDot (finiteMatrixApply C x) z := by
              rw [finiteMatrix_bilinear_identity A x y,
                finiteMatrix_bilinear_identity C x z]
      _ = finiteDot b y + finiteDot (finiteMatrixApply C x) z := by
              congr 1
              unfold finiteDot
              apply Finset.sum_congr rfl
              intro r hr
              rw [hAx r]
  have hcapDot : finiteDot (finiteMatrixApply C x) z ≤ finiteDot d z := by
    unfold finiteDot
    apply Finset.sum_le_sum
    intro s hs
    exact mul_le_mul_of_nonneg_right (hCx s) (hz s)
  rw [hrewrite] at hcone
  linarith

/-- A strictly negative capped dual work value is a solver-independent
certificate that the positive, equality-constrained, rate-capped system is
infeasible. -/
theorem rateCapped_negative_dualWork_certifies_infeasible
    (A : R → E → ℝ) (C : S → E → ℝ)
    (b y : R → ℝ) (d z : S → ℝ)
    (hz : ∀ s, 0 ≤ z s)
    (hdual : ∀ e,
      0 ≤ finiteTransposeApply A y e + finiteTransposeApply C z e)
    (hwork : finiteDot b y + finiteDot d z < 0) :
    ¬ ∃ x : E → ℝ,
      (∀ e, 0 ≤ x e) ∧
      (∀ r, finiteMatrixApply A x r = b r) ∧
      (∀ s, finiteMatrixApply C x s ≤ d s) := by
  rintro ⟨x, hx, hAx, hCx⟩
  have hnonneg := rateCapped_dualWork_nonneg
    A C b y d z x hx hAx hCx hz hdual
  linarith

end AFPBarrier
