import AFPBarrier.LossVarianceSharpness
import AFPBarrier.GlobalLossRigidity
import Mathlib.Tactic

/-!
# Spherical Q=1 rigidity and quantitative edge-loss stability

This module transfers the sharp local loss-variance equality into the abstract
connected active-edge propagation theorem.  It also records the finite algebra
used by the restricted spherical-triangulation classification and the
quantitative near-rigidity estimates.

The geometric triangulation and convex-polyhedron classification is proved in
the accompanying ordinary mathematics document.  No graph-classification or
differential-geometric fact is introduced as a Lean axiom.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A strictly active off-diagonal jump. -/
def activeOffdiag (a : ι → ι → ℝ) (i j : ι) : Prop :=
  j ≠ i ∧ 0 < a i j

/-- Spherical zonal chord loss `1 - Omega_i dot Omega_j`. -/
def zonalLoss (zonal : ι → ι → ℝ) (i j : ι) : ℝ :=
  1 - zonal i j

/-- The sharp `S²` quality equality at one node. -/
def sphericalQOneAt
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i : ι) : Prop :=
  jumpRate a i * peakDefect a (zonal i) i 2 = 4

/-- A normalized peak with a nonzero exact eigenvalue has strictly positive
outgoing rate under nonnegative off-diagonal jumps. -/
theorem jumpRate_pos_of_nonzero_eigenvalue_at_peak
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlam : lam ≠ 0)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam) :
    0 < jumpRate a i := by
  have hrate0 : 0 ≤ jumpRate a i := jumpRate_nonneg a i ha
  have hbound : lam ^ 2 ≤ jumpRate a i * peakDefect a f i lam :=
    eigenvalue_sq_le_rate_mul_peakDefect a f i lam ha hfi hlinear
  by_contra hnot
  have hrate_le : jumpRate a i ≤ 0 := le_of_not_gt hnot
  have hrate_zero : jumpRate a i = 0 := le_antisymm hrate_le hrate0
  rw [hrate_zero] at hbound
  have hlam_sq : 0 < lam ^ 2 := sq_pos_of_ne_zero hlam
  nlinarith

/-- Exact `Q=1` at an `S²` coordinate peak forces every strictly active edge
loss to equal `2 / rowRate`. -/
theorem sphericalQOne_active_loss
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i j : ι)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hdiag : zonal i i = 1)
    (hlinear : jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hq : sphericalQOneAt a zonal i)
    (hactive : activeOffdiag a i j) :
    zonalLoss zonal i j = 2 / jumpRate a i := by
  have hquality :
      jumpRate a i * peakDefect a (zonal i) i 2 = (2 : ℝ) ^ 2 := by
    simpa [sphericalQOneAt] using hq
  have hall :=
    (rate_mul_peakDefect_eq_eigenvalue_sq_iff_active_losses_eq_mean
      a (zonal i) i 2 ha hdiag hlinear
      (jumpRate_pos_of_nonzero_eigenvalue_at_peak
        a (zonal i) i 2 ha (by norm_num) hdiag hlinear)).mp hquality
  have hedge := hall j hactive.1 hactive.2
  simpa [zonalLoss, hdiag] using hedge

/-- Every active edge in an exact `Q=1` row has strictly positive loss. -/
theorem sphericalQOne_active_loss_pos
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i j : ι)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hdiag : zonal i i = 1)
    (hlinear : jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hq : sphericalQOneAt a zonal i)
    (hactive : activeOffdiag a i j) :
    0 < zonalLoss zonal i j := by
  rw [sphericalQOne_active_loss a zonal i j ha hdiag hlinear hq hactive]
  have hrate := jumpRate_pos_of_nonzero_eigenvalue_at_peak
    a (zonal i) i 2 ha (by norm_num) hdiag hlinear
  positivity

/-- An active edge whose endpoints have the same embedded sample is
incompatible with exact positive `Q=1`. -/
theorem sphericalQOne_active_zero_loss_impossible
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i j : ι)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hdiag : zonal i i = 1)
    (hlinear : jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hq : sphericalQOneAt a zonal i)
    (hactive : activeOffdiag a i j)
    (hsame : zonal i j = 1) :
    False := by
  have hpos := sphericalQOne_active_loss_pos
    a zonal i j ha hdiag hlinear hq hactive
  simp [zonalLoss, hsame] at hpos

/-- A symmetric connected active support transfers exact local `S²` quality
into one common row rate and one common spherical edge loss. -/
theorem connected_sphericalQOne_rigidity
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (root : ι)
    (ha : ∀ i j, j ≠ i → 0 ≤ a i j)
    (hdiag : ∀ i, zonal i i = 1)
    (hlinear : ∀ i, jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hq : ∀ i, sphericalQOneAt a zonal i)
    (hActiveSymm : ∀ {i j}, activeOffdiag a i j → activeOffdiag a j i)
    (hZonalSymm : ∀ i j, zonal i j = zonal j i)
    (hConnected : ∀ j, Relation.ReflTransGen (activeOffdiag a) root j) :
    (∀ j, jumpRate a j = jumpRate a root) ∧
      (∀ {i j}, activeOffdiag a i j →
        zonalLoss zonal i j = 2 / jumpRate a root) := by
  have hRate : ∀ i, 0 < jumpRate a i := by
    intro i
    exact jumpRate_pos_of_nonzero_eigenvalue_at_peak
      a (zonal i) i 2 (ha i) (by norm_num) (hdiag i) (hlinear i)
  have hLossSymm : ∀ i j, zonalLoss zonal i j = zonalLoss zonal j i := by
    intro i j
    simp [zonalLoss, hZonalSymm i j]
  have hLocal : ∀ {i j}, activeOffdiag a i j →
      zonalLoss zonal i j = 2 / jumpRate a i := by
    intro i j hij
    exact sphericalQOne_active_loss
      a zonal i j (ha i) (hdiag i) (hlinear i) (hq i) hij
  exact connected_active_loss_rigidity
    (activeOffdiag a) (zonalLoss zonal) (jumpRate a) 2 root
    (by norm_num) hRate hActiveSymm hLossSymm hLocal hConnected

/-- An active antipodal edge has loss two and therefore forces its endpoint row
rate to equal one in an exact `Q=1` row. -/
theorem sphericalQOne_active_antipode_forces_rate_one
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i j : ι)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hdiag : zonal i i = 1)
    (hlinear : jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hq : sphericalQOneAt a zonal i)
    (hactive : activeOffdiag a i j)
    (hantipodal : zonal i j = -1) :
    jumpRate a i = 1 := by
  have hloss := sphericalQOne_active_loss
    a zonal i j ha hdiag hlinear hq hactive
  have hrate := jumpRate_pos_of_nonzero_eigenvalue_at_peak
    a (zonal i) i 2 ha (by norm_num) hdiag hlinear
  simp [zonalLoss, hantipodal] at hloss
  field_simp [ne_of_gt hrate] at hloss
  nlinarith

/-- Scalar form of the equilateral spherical-triangle angle identity:
`c = c² + (1-c²) cos(alpha)` implies `cos(alpha)=c/(1+c)`. -/
theorem equilateral_tangent_cosine
    (c cosAlpha : ℝ)
    (hcNeg : c ≠ -1)
    (hcOne : c ≠ 1)
    (hlaw : c = c ^ 2 + (1 - c ^ 2) * cosAlpha) :
    cosAlpha = c / (1 + c) := by
  have hden : 1 + c ≠ 0 := by
    intro hzero
    apply hcNeg
    linarith
  have hleft : 1 - c ≠ 0 := by
    exact sub_ne_zero.mpr (Ne.symm hcOne)
  have hfactor : (1 - c) * ((1 + c) * cosAlpha - c) = 0 := by
    calc
      (1 - c) * ((1 + c) * cosAlpha - c)
          = c ^ 2 + (1 - c ^ 2) * cosAlpha - c := by ring
      _ = 0 := by linarith
  have hinner : (1 + c) * cosAlpha - c = 0 :=
    (mul_eq_zero.mp hfactor).resolve_left hleft
  apply (eq_div_iff hden).2
  linarith

/-- Euler plus the edge/face incidence equations for a regular spherical
triangulation. -/
theorem regular_triangulation_euler_identity
    (q V E F : ℝ)
    (hDegree : q * V = 2 * E)
    (hFaces : 3 * F = 2 * E)
    (hEuler : V - E + F = 2) :
    (6 - q) * V = 12 := by
  nlinarith

/-- The degree-three regular triangulation has tetrahedral counts. -/
theorem degree_three_triangulation_counts
    (V E F : ℝ)
    (hDegree : 3 * V = 2 * E)
    (hFaces : 3 * F = 2 * E)
    (hEuler : V - E + F = 2) :
    V = 4 ∧ E = 6 ∧ F = 4 := by
  constructor
  · nlinarith
  · constructor <;> nlinarith

/-- The degree-four regular triangulation has octahedral counts. -/
theorem degree_four_triangulation_counts
    (V E F : ℝ)
    (hDegree : 4 * V = 2 * E)
    (hFaces : 3 * F = 2 * E)
    (hEuler : V - E + F = 2) :
    V = 6 ∧ E = 12 ∧ F = 8 := by
  constructor
  · nlinarith
  · constructor <;> nlinarith

/-- The degree-five regular triangulation has icosahedral counts. -/
theorem degree_five_triangulation_counts
    (V E F : ℝ)
    (hDegree : 5 * V = 2 * E)
    (hFaces : 3 * F = 2 * E)
    (hEuler : V - E + F = 2) :
    V = 12 ∧ E = 30 ∧ F = 20 := by
  constructor
  · nlinarith
  · constructor <;> nlinarith

/-- The exact `S²` gap controls each active loss deviation from the local mean
loss `2 / rowRate`. -/
theorem spherical_active_loss_deviation_sq_le_gap_div_rate
    (a : ι → ι → ℝ) (zonal : ι → ι → ℝ) (i j : ι)
    (eta amin : ℝ)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hji : j ≠ i)
    (hamin : amin ≤ a i j)
    (hdiag : zonal i i = 1)
    (hlinear : jumpGenerator a (zonal i) i = -(2 : ℝ))
    (hrate : 0 < jumpRate a i)
    (hgap : jumpRate a i * peakDefect a (zonal i) i 2 - 4 ≤ eta) :
    amin * (zonalLoss zonal i j - 2 / jumpRate a i) ^ 2
      ≤ eta / jumpRate a i := by
  have hm : (2 / jumpRate a i) * jumpRate a i = (2 : ℝ) := by
    field_simp [ne_of_gt hrate]
  have h := minActiveRate_mul_loss_deviation_sq_le_gap_div_rate
    a (zonal i) i j 2 (2 / jumpRate a i) eta amin
    ha hji hamin hdiag hlinear hrate hm hgap
  simpa [zonalLoss, hdiag] using h

/-- Two local mean losses that are both within `Delta` of one shared symmetric
edge loss differ by at most `2 Delta`. -/
theorem shared_edge_centers_close
    (ell mi mj Delta : ℝ)
    (hi : |ell - mi| ≤ Delta)
    (hj : |ell - mj| ≤ Delta) :
    |mi - mj| ≤ 2 * Delta := by
  rw [abs_le] at hi hj ⊢
  constructor <;> linarith

/-- Multiplicative overlap on one shared edge gives the cross-multiplied center
bounds used in path propagation. -/
theorem shared_relative_center_cross_bounds
    (ell mi mj delta : ℝ)
    (hiLower : (1 - delta) * mi ≤ ell)
    (hiUpper : ell ≤ (1 + delta) * mi)
    (hjLower : (1 - delta) * mj ≤ ell)
    (hjUpper : ell ≤ (1 + delta) * mj) :
    (1 - delta) * mj ≤ (1 + delta) * mi ∧
      (1 - delta) * mi ≤ (1 + delta) * mj := by
  exact ⟨hjLower.trans hiUpper, hiLower.trans hjUpper⟩

end AFPBarrier
