import AFPBarrier.SphericalQEqualityRigidity
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# Quantitative global near-rigidity

The local normalized variance gives pointwise edge-scale control.  This module
formalizes the adjacent algebra and its explicit multiplication and logarithmic
accumulation along a finite active path.
-/

namespace AFPBarrier

/-- Multiplicative distortion associated with a local relative error. -/
noncomputable def qDelta (delta : ℝ) : ℝ :=
  (1 + delta) / (1 - delta)

/-- Logarithmic one-edge distortion. -/
noncomputable def sDelta (delta : ℝ) : ℝ :=
  Real.log (qDelta delta)

/-- One-sided logarithmic normalized-scale distortion. -/
noncomputable def hDelta (delta : ℝ) : ℝ :=
  -Real.log (1 - delta)

/-- A squared deviation bound gives the corresponding absolute bound. -/
theorem abs_sub_one_le_of_sq_le_delta_sq
    (x delta : ℝ)
    (hdelta : 0 ≤ delta)
    (hsq : (x - 1) ^ 2 ≤ delta ^ 2) :
    |x - 1| ≤ delta := by
  rw [abs_le]
  constructor <;>
    nlinarith [sq_nonneg (x - 1 - delta), sq_nonneg (x - 1 + delta)]

/-- One weighted variance term and a lower probability bound imply the
pointwise `delta` estimate. -/
theorem pointwise_delta_bound
    (p x kappa eta delta : ℝ)
    (hkappa : 0 < kappa)
    (hp : kappa ≤ p)
    (hterm : p * (x - 1) ^ 2 ≤ eta)
    (heta : eta = kappa * delta ^ 2)
    (hdelta : 0 ≤ delta) :
    |x - 1| ≤ delta := by
  have hweight :
      kappa * (x - 1) ^ 2 ≤ p * (x - 1) ^ 2 :=
    mul_le_mul_of_nonneg_right hp (sq_nonneg _)
  have hscaled : kappa * (x - 1) ^ 2 ≤ kappa * delta ^ 2 := by
    calc
      kappa * (x - 1) ^ 2 ≤ p * (x - 1) ^ 2 := hweight
      _ ≤ eta := hterm
      _ = kappa * delta ^ 2 := heta
  have hsq : (x - 1) ^ 2 ≤ delta ^ 2 :=
    (mul_le_mul_iff_right₀ hkappa).mp hscaled
  exact abs_sub_one_le_of_sq_le_delta_sq x delta hdelta hsq

/-- The exact normalized `Q-1` identity gives the pointwise active-edge
estimate under a normalized-weight floor. -/
theorem sphericalQ_pointwise_delta_bound
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (a loss : ι → ι → ℝ) (i j : ι)
    (kappa eta delta : ℝ)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hji : j ≠ i)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun k => a i k * loss i k) = 2)
    (hkappa : 0 < kappa)
    (hp : kappa ≤ a i j / jumpRate a i)
    (hQupper : sphericalQAt a loss i ≤ 1 + eta)
    (heta : eta = kappa * delta ^ 2)
    (hdelta : 0 ≤ delta) :
    |jumpRate a i * loss i j / 2 - 1| ≤ delta := by
  have hid := sphericalQ_sub_one_eq_normalizedLossVariance
    (a := a) (loss := loss) (i := i) hrate hmoment
  have hsumle :
      (offdiag i).sum (fun k =>
        (a i k / jumpRate a i) *
          (jumpRate a i * loss i k / 2 - 1) ^ 2) ≤ eta := by
    rw [← hid]
    linarith
  have hjmem : j ∈ offdiag i :=
    Finset.mem_erase.mpr ⟨hji, Finset.mem_univ j⟩
  have hsingle :
      (a i j / jumpRate a i) *
          (jumpRate a i * loss i j / 2 - 1) ^ 2 ≤
        (offdiag i).sum (fun k =>
          (a i k / jumpRate a i) *
            (jumpRate a i * loss i k / 2 - 1) ^ 2) := by
    refine Finset.single_le_sum
      (s := offdiag i)
      (f := fun k =>
        (a i k / jumpRate a i) *
          (jumpRate a i * loss i k / 2 - 1) ^ 2) ?_ hjmem
    intro k hk
    have hki : k ≠ i := (Finset.mem_erase.mp hk).1
    exact mul_nonneg
      (div_nonneg (ha k hki) (le_of_lt hrate)) (sq_nonneg _)
  exact pointwise_delta_bound
    (a i j / jumpRate a i)
    (jumpRate a i * loss i j / 2)
    kappa eta delta hkappa hp (hsingle.trans hsumle) heta hdelta

/-- Absolute pointwise control is equivalent to the normalized scale
interval. -/
theorem normalized_scale_interval_of_abs
    (x delta : ℝ)
    (habs : |x - 1| ≤ delta) :
    1 - delta ≤ x ∧ x ≤ 1 + delta := by
  have h := abs_le.mp habs
  constructor <;> linarith

/-- The distortion factor is at least one on `0 <= delta < 1`. -/
theorem one_le_qDelta
    (delta : ℝ) (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1) :
    1 ≤ qDelta delta := by
  have hminus : 0 < 1 - delta := by linarith
  unfold qDelta
  apply (le_div_iff₀ hminus).2
  nlinarith

/-- Two normalized scales in the pointwise `delta` interval differ by at most
the multiplicative factor `qDelta delta`. -/
theorem normalized_scale_qDelta_cross_bounds
    (x₁ x₂ delta : ℝ)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hx₁Lo : 1 - delta ≤ x₁)
    (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂)
    (hx₂Hi : x₂ ≤ 1 + delta) :
    x₂ ≤ qDelta delta * x₁ ∧
      x₁ ≤ qDelta delta * x₂ := by
  have hminus : 0 < 1 - delta := by linarith
  have hminus_ne : 1 - delta ≠ 0 := ne_of_gt hminus
  have hplus : 0 ≤ 1 + delta := by linarith
  have hcross₁ : (1 - delta) * x₂ ≤ (1 + delta) * x₁ := by
    calc
      (1 - delta) * x₂ ≤ (1 - delta) * (1 + delta) :=
        mul_le_mul_of_nonneg_left hx₂Hi (le_of_lt hminus)
      _ = (1 + delta) * (1 - delta) := by ring
      _ ≤ (1 + delta) * x₁ :=
        mul_le_mul_of_nonneg_left hx₁Lo hplus
  have hcross₂ : (1 - delta) * x₁ ≤ (1 + delta) * x₂ := by
    calc
      (1 - delta) * x₁ ≤ (1 - delta) * (1 + delta) :=
        mul_le_mul_of_nonneg_left hx₁Hi (le_of_lt hminus)
      _ = (1 + delta) * (1 - delta) := by ring
      _ ≤ (1 + delta) * x₂ :=
        mul_le_mul_of_nonneg_left hx₂Lo hplus
  constructor
  · calc
      x₂ ≤ ((1 + delta) * x₁) / (1 - delta) :=
        (le_div_iff₀ hminus).2 (by simpa [mul_comm] using hcross₁)
      _ = qDelta delta * x₁ := by
        unfold qDelta
        field_simp [hminus_ne]
  · calc
      x₁ ≤ ((1 + delta) * x₂) / (1 - delta) :=
        (le_div_iff₀ hminus).2 (by simpa [mul_comm] using hcross₂)
      _ = qDelta delta * x₂ := by
        unfold qDelta
        field_simp [hminus_ne]

/-- Shared-edge balance plus local normalized-scale bounds gives
cross-multiplied adjacent rate bounds. -/
theorem adjacent_rate_cross_bounds
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 ≤ r_i) (hrj : 0 ≤ r_j)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    (1 - delta) * r_j ≤ (1 + delta) * r_i ∧
      (1 - delta) * r_i ≤ (1 + delta) * r_j := by
  constructor
  · calc
      (1 - delta) * r_j ≤ x_ij * r_j :=
        mul_le_mul_of_nonneg_right hijLo hrj
      _ = x_ji * r_i := by simpa [mul_comm] using hbalance
      _ ≤ (1 + delta) * r_i :=
        mul_le_mul_of_nonneg_right hjiHi hri
  · calc
      (1 - delta) * r_i ≤ x_ji * r_i :=
        mul_le_mul_of_nonneg_right hjiLo hri
      _ = x_ij * r_j := by simpa [mul_comm] using hbalance.symm
      _ ≤ (1 + delta) * r_j :=
        mul_le_mul_of_nonneg_right hijHi hrj

/-- Division form of the adjacent rate-ratio estimate. -/
theorem adjacent_rate_ratio_bounds
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    (1 - delta) / (1 + delta) ≤ r_i / r_j ∧
      r_i / r_j ≤ (1 + delta) / (1 - delta) := by
  have hcross := adjacent_rate_cross_bounds
    r_i r_j x_ij x_ji delta (le_of_lt hri) (le_of_lt hrj)
    hijLo hijHi hjiLo hjiHi hbalance
  have hplus : 0 < 1 + delta := by linarith
  have hminus : 0 < 1 - delta := by linarith
  constructor
  · apply (div_le_div_iff₀ hplus hrj).2
    simpa [mul_comm] using hcross.1
  · apply (div_le_div_iff₀ hrj hminus).2
    simpa [mul_comm] using hcross.2

/-- Exact adjacent relative-error consequence of the rate-ratio interval. -/
theorem adjacent_rate_relative_error_bound
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    |r_i / r_j - 1| ≤ 2 * delta / (1 - delta) := by
  have hratio := adjacent_rate_ratio_bounds
    r_i r_j x_ij x_ji delta hri hrj hdelta0 hdelta1
    hijLo hijHi hjiLo hjiHi hbalance
  have hplus : 0 < 1 + delta := by linarith
  have hminus : 0 < 1 - delta := by linarith
  have hplus_ne : 1 + delta ≠ 0 := ne_of_gt hplus
  have hminus_ne : 1 - delta ≠ 0 := ne_of_gt hminus
  have hfractions :
      2 * delta / (1 + delta) ≤ 2 * delta / (1 - delta) := by
    apply (div_le_div_iff₀ hplus hminus).2
    nlinarith
  rw [abs_le]
  constructor
  · calc
      -(2 * delta / (1 - delta)) ≤ -(2 * delta / (1 + delta)) :=
        neg_le_neg hfractions
      _ = (1 - delta) / (1 + delta) - 1 := by
        field_simp [hplus_ne]
        ring
      _ ≤ r_i / r_j - 1 := sub_le_sub_right hratio.1 1
  · calc
      r_i / r_j - 1 ≤ (1 + delta) / (1 - delta) - 1 :=
        sub_le_sub_right hratio.2 1
      _ = 2 * delta / (1 - delta) := by
        field_simp [hminus_ne]
        ring

/-- Adjacent bounds in the `q_delta` form used by path multiplication. -/
theorem adjacent_rate_qDelta_cross_bounds
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    r_j ≤ qDelta delta * r_i ∧
      r_i ≤ qDelta delta * r_j := by
  have hcross := adjacent_rate_cross_bounds
    r_i r_j x_ij x_ji delta (le_of_lt hri) (le_of_lt hrj)
    hijLo hijHi hjiLo hjiHi hbalance
  have hminus : 0 < 1 - delta := by linarith
  have hminus_ne : 1 - delta ≠ 0 := ne_of_gt hminus
  constructor
  · calc
      r_j ≤ ((1 + delta) * r_i) / (1 - delta) := by
        apply (le_div_iff₀ hminus).2
        simpa [mul_comm] using hcross.1
      _ = qDelta delta * r_i := by
        unfold qDelta
        field_simp [hminus_ne]
  · calc
      r_i ≤ ((1 + delta) * r_j) / (1 - delta) := by
        apply (le_div_iff₀ hminus).2
        simpa [mul_comm] using hcross.2
      _ = qDelta delta * r_j := by
        unfold qDelta
        field_simp [hminus_ne]

/-- Correct incident-edge cross bounds.  The restriction
`0 <= delta < 1` is essential: without it the interval may contain negative
normalized scales and the cross multiplication is false. -/
theorem incident_loss_cross_bounds
    (ell₁ ell₂ x₁ x₂ rate delta : ℝ)
    (hrate : 0 < rate)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hbalance₁ : rate * ell₁ = 2 * x₁)
    (hbalance₂ : rate * ell₂ = 2 * x₂)
    (hx₁Lo : 1 - delta ≤ x₁)
    (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂)
    (hx₂Hi : x₂ ≤ 1 + delta) :
    (1 - delta) * ell₂ ≤ (1 + delta) * ell₁ ∧
      (1 - delta) * ell₁ ≤ (1 + delta) * ell₂ := by
  have hminus : 0 ≤ 1 - delta := by linarith
  have hplus : 0 ≤ 1 + delta := by linarith
  have hcross₁ : (1 - delta) * x₂ ≤ (1 + delta) * x₁ := by
    calc
      (1 - delta) * x₂ ≤ (1 - delta) * (1 + delta) :=
        mul_le_mul_of_nonneg_left hx₂Hi hminus
      _ = (1 + delta) * (1 - delta) := by ring
      _ ≤ (1 + delta) * x₁ :=
        mul_le_mul_of_nonneg_left hx₁Lo hplus
  have hcross₂ : (1 - delta) * x₁ ≤ (1 + delta) * x₂ := by
    calc
      (1 - delta) * x₁ ≤ (1 - delta) * (1 + delta) :=
        mul_le_mul_of_nonneg_left hx₁Hi hminus
      _ = (1 + delta) * (1 - delta) := by ring
      _ ≤ (1 + delta) * x₂ :=
        mul_le_mul_of_nonneg_left hx₂Lo hplus
  constructor
  · apply (mul_le_mul_iff_right₀ hrate).mp
    calc
      rate * ((1 - delta) * ell₂) = 2 * ((1 - delta) * x₂) := by
        linear_combination (1 - delta) * hbalance₂
      _ ≤ 2 * ((1 + delta) * x₁) :=
        mul_le_mul_of_nonneg_left hcross₁ (by norm_num)
      _ = rate * ((1 + delta) * ell₁) := by
        linear_combination -(1 + delta) * hbalance₁
  · apply (mul_le_mul_iff_right₀ hrate).mp
    calc
      rate * ((1 - delta) * ell₁) = 2 * ((1 - delta) * x₁) := by
        linear_combination (1 - delta) * hbalance₁
      _ ≤ 2 * ((1 + delta) * x₂) :=
        mul_le_mul_of_nonneg_left hcross₂ (by norm_num)
      _ = rate * ((1 + delta) * ell₂) := by
        linear_combination -(1 + delta) * hbalance₂

/-- Division form of the incident-edge loss estimate.  Positivity of both
losses follows from the positive rate and the normalized-scale interval. -/
theorem incident_loss_ratio_bounds
    (ell₁ ell₂ x₁ x₂ rate delta : ℝ)
    (hrate : 0 < rate)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hbalance₁ : rate * ell₁ = 2 * x₁)
    (hbalance₂ : rate * ell₂ = 2 * x₂)
    (hx₁Lo : 1 - delta ≤ x₁)
    (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂)
    (hx₂Hi : x₂ ≤ 1 + delta) :
    1 / qDelta delta ≤ ell₁ / ell₂ ∧
      ell₁ / ell₂ ≤ qDelta delta := by
  have hminus : 0 < 1 - delta := by linarith
  have hplus : 0 < 1 + delta := by linarith
  have hx₁pos : 0 < x₁ := hminus.trans_le hx₁Lo
  have hx₂pos : 0 < x₂ := hminus.trans_le hx₂Lo
  have hell₁pos : 0 < ell₁ := by
    apply pos_of_mul_pos_right (b := ell₁) _ (le_of_lt hrate)
    rw [hbalance₁]
    exact mul_pos (by norm_num) hx₁pos
  have hell₂pos : 0 < ell₂ := by
    apply pos_of_mul_pos_right (b := ell₂) _ (le_of_lt hrate)
    rw [hbalance₂]
    exact mul_pos (by norm_num) hx₂pos
  have hcross := incident_loss_cross_bounds
    ell₁ ell₂ x₁ x₂ rate delta hrate hdelta0 hdelta1
    hbalance₁ hbalance₂ hx₁Lo hx₁Hi hx₂Lo hx₂Hi
  have hqinv :
      1 / qDelta delta = (1 - delta) / (1 + delta) := by
    unfold qDelta
    field_simp [ne_of_gt hminus, ne_of_gt hplus]
  constructor
  · rw [hqinv]
    apply (div_le_div_iff₀ hplus hell₂pos).2
    simpa [mul_comm] using hcross.1
  · unfold qDelta
    apply (div_le_div_iff₀ hell₂pos hminus).2
    simpa [mul_comm] using hcross.2

/-! ## Finite path multiplication -/

/-- A path with its number of active edges in the type. -/
inductive ActivePath {ι : Type*} (active : ι → ι → Prop) :
    ℕ → ι → ι → Prop
  | refl (i : ι) : ActivePath active 0 i i
  | tail {n : ℕ} {i j k : ι} :
      ActivePath active n i j → active j k →
        ActivePath active (n + 1) i k

/-- Pairwise connectedness by an active path of at most `D` edges. -/
def ActiveDiameterAtMost {ι : Type*}
    (active : ι → ι → Prop) (D : ℕ) : Prop :=
  ∀ i j, ∃ n, n ≤ D ∧ ActivePath active n i j

/-- Multiplicative endpoint bounds accumulate as the path-length power. -/
theorem path_rate_cross_bounds
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (q : ℝ)
    (hq : 1 ≤ q)
    (hEdge : ∀ {i j}, active i j →
      rate j ≤ q * rate i ∧ rate i ≤ q * rate j)
    {n : ℕ} {i j : ι}
    (hpath : ActivePath active n i j) :
    rate j ≤ q ^ n * rate i ∧
      rate i ≤ q ^ n * rate j := by
  induction hpath with
  | refl i => simp
  | @tail n i j k hprefix hedge ih =>
      have hq0 : 0 ≤ q := le_trans (by norm_num) hq
      have hqpow0 : 0 ≤ q ^ n := pow_nonneg hq0 n
      have hedgeBounds := hEdge hedge
      constructor
      · calc
          rate k ≤ q * rate j := hedgeBounds.1
          _ ≤ q * (q ^ n * rate i) :=
            mul_le_mul_of_nonneg_left ih.1 hq0
          _ = q ^ (n + 1) * rate i := by
            rw [pow_succ]
            ring
      · calc
          rate i ≤ q ^ n * rate j := ih.2
          _ ≤ q ^ n * (q * rate k) :=
            mul_le_mul_of_nonneg_left hedgeBounds.2 hqpow0
          _ = q ^ (n + 1) * rate k := by
            rw [pow_succ]
            ring

/-- Division form of the finite path bounds. -/
theorem path_rate_ratio_bounds
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (q : ℝ)
    (hrate : ∀ v, 0 < rate v)
    (hq : 1 ≤ q)
    (hEdge : ∀ {i j}, active i j →
      rate j ≤ q * rate i ∧ rate i ≤ q * rate j)
    {n : ℕ} {i j : ι}
    (hpath : ActivePath active n i j) :
    1 / q ^ n ≤ rate i / rate j ∧
      rate i / rate j ≤ q ^ n := by
  have hcross := path_rate_cross_bounds active rate q hq hEdge hpath
  have hqpos : 0 < q := lt_of_lt_of_le (by norm_num) hq
  have hqpowpos : 0 < q ^ n := pow_pos hqpos n
  constructor
  · apply (div_le_div_iff₀ hqpowpos (hrate j)).2
    simpa [mul_comm] using hcross.1
  · apply (div_le_iff₀ (hrate j)).2
    simpa [mul_comm] using hcross.2

/-- Loss ratios for two edges based at the endpoints of an active path.
The local normalized-scale comparison costs one extra factor of `qDelta` in
addition to the `n` rate factors accumulated along the path. -/
theorem path_loss_ratio_bounds
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (delta : ℝ)
    (hrate : ∀ v, 0 < rate v)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hEdge : ∀ {i j}, active i j →
      rate j ≤ qDelta delta * rate i ∧
        rate i ≤ qDelta delta * rate j)
    {n : ℕ} {i j : ι}
    (hpath : ActivePath active n i j)
    (ell₁ ell₂ x₁ x₂ : ℝ)
    (hbalance₁ : rate i * ell₁ = 2 * x₁)
    (hbalance₂ : rate j * ell₂ = 2 * x₂)
    (hx₁Lo : 1 - delta ≤ x₁)
    (hx₁Hi : x₁ ≤ 1 + delta)
    (hx₂Lo : 1 - delta ≤ x₂)
    (hx₂Hi : x₂ ≤ 1 + delta) :
    1 / (qDelta delta) ^ (n + 1) ≤ ell₁ / ell₂ ∧
      ell₁ / ell₂ ≤ (qDelta delta) ^ (n + 1) := by
  let q := qDelta delta
  have hq : 1 ≤ q := one_le_qDelta delta hdelta0 hdelta1
  have hq0 : 0 ≤ q := le_trans (by norm_num) hq
  have hqpos : 0 < q := lt_of_lt_of_le (by norm_num) hq
  have hminus : 0 < 1 - delta := by linarith
  have hx₁pos : 0 < x₁ := hminus.trans_le hx₁Lo
  have hx₂pos : 0 < x₂ := hminus.trans_le hx₂Lo
  have hell₁pos : 0 < ell₁ := by
    apply pos_of_mul_pos_right (b := ell₁) _ (le_of_lt (hrate i))
    rw [hbalance₁]
    exact mul_pos (by norm_num) hx₁pos
  have hell₂pos : 0 < ell₂ := by
    apply pos_of_mul_pos_right (b := ell₂) _ (le_of_lt (hrate j))
    rw [hbalance₂]
    exact mul_pos (by norm_num) hx₂pos
  have hscale := normalized_scale_qDelta_cross_bounds
    x₁ x₂ delta hdelta0 hdelta1 hx₁Lo hx₁Hi hx₂Lo hx₂Hi
  have hratePath := path_rate_cross_bounds active rate q hq hEdge hpath
  have hforward : ell₁ ≤ q ^ (n + 1) * ell₂ := by
    apply (mul_le_mul_iff_right₀ (hrate i)).mp
    calc
      rate i * ell₁ = 2 * x₁ := hbalance₁
      _ ≤ 2 * (q * x₂) :=
        mul_le_mul_of_nonneg_left hscale.2 (by norm_num)
      _ = q * (rate j * ell₂) := by rw [hbalance₂]; ring
      _ ≤ q * ((q ^ n * rate i) * ell₂) := by
        apply mul_le_mul_of_nonneg_left _ hq0
        exact mul_le_mul_of_nonneg_right hratePath.1 (le_of_lt hell₂pos)
      _ = rate i * (q ^ (n + 1) * ell₂) := by
        rw [pow_succ]
        ring
  have hbackward : ell₂ ≤ q ^ (n + 1) * ell₁ := by
    apply (mul_le_mul_iff_right₀ (hrate j)).mp
    calc
      rate j * ell₂ = 2 * x₂ := hbalance₂
      _ ≤ 2 * (q * x₁) :=
        mul_le_mul_of_nonneg_left hscale.1 (by norm_num)
      _ = q * (rate i * ell₁) := by rw [hbalance₁]; ring
      _ ≤ q * ((q ^ n * rate j) * ell₁) := by
        apply mul_le_mul_of_nonneg_left _ hq0
        exact mul_le_mul_of_nonneg_right hratePath.2 (le_of_lt hell₁pos)
      _ = rate j * (q ^ (n + 1) * ell₁) := by
        rw [pow_succ]
        ring
  have hqpowpos : 0 < q ^ (n + 1) := pow_pos hqpos (n + 1)
  constructor
  · apply (div_le_div_iff₀ hqpowpos hell₂pos).2
    simpa [mul_comm] using hbackward
  · apply (div_le_iff₀ hell₂pos).2
    exact hforward

/-- One-edge multiplicative cross bounds imply an additive logarithmic
bound. -/
theorem abs_log_rate_sub_le_of_cross_bounds
    (r_i r_j q : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hq : 1 ≤ q)
    (hij : r_i ≤ q * r_j)
    (hji : r_j ≤ q * r_i) :
    |Real.log r_i - Real.log r_j| ≤ Real.log q := by
  have hqpos : 0 < q := lt_of_lt_of_le (by norm_num) hq
  have hlogij : Real.log r_i ≤ Real.log (q * r_j) :=
    Real.strictMonoOn_log.monotoneOn hri (mul_pos hqpos hrj) hij
  have hlogji : Real.log r_j ≤ Real.log (q * r_i) :=
    Real.strictMonoOn_log.monotoneOn hrj (mul_pos hqpos hri) hji
  rw [Real.log_mul (ne_of_gt hqpos) (ne_of_gt hrj)] at hlogij
  rw [Real.log_mul (ne_of_gt hqpos) (ne_of_gt hri)] at hlogji
  rw [abs_le]
  constructor <;> linarith

/-- Adjacent logarithmic rate control in the normalized `delta` notation. -/
theorem adjacent_log_rate_bound
    (r_i r_j x_ij x_ji delta : ℝ)
    (hri : 0 < r_i) (hrj : 0 < r_j)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hijLo : 1 - delta ≤ x_ij)
    (hijHi : x_ij ≤ 1 + delta)
    (hjiLo : 1 - delta ≤ x_ji)
    (hjiHi : x_ji ≤ 1 + delta)
    (hbalance : r_j * x_ij = r_i * x_ji) :
    |Real.log r_i - Real.log r_j| ≤ sDelta delta := by
  have hcross := adjacent_rate_qDelta_cross_bounds
    r_i r_j x_ij x_ji delta hri hrj hdelta0 hdelta1
    hijLo hijHi hjiLo hjiHi hbalance
  have hq := one_le_qDelta delta hdelta0 hdelta1
  simpa [sDelta] using abs_log_rate_sub_le_of_cross_bounds
    r_i r_j (qDelta delta) hri hrj hq hcross.2 hcross.1

/-- Additive logarithmic edge bounds accumulate linearly along a path. -/
theorem path_log_rate_bound
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (s : ℝ)
    (hs : 0 ≤ s)
    (hEdgeLog : ∀ {i j}, active i j →
      |Real.log (rate i) - Real.log (rate j)| ≤ s)
    {n : ℕ} {i j : ι}
    (hpath : ActivePath active n i j) :
    |Real.log (rate i) - Real.log (rate j)| ≤ (n : ℝ) * s := by
  induction hpath with
  | refl i => simp
  | @tail n i j k hprefix hedge ih =>
      calc
        |Real.log (rate i) - Real.log (rate k)| =
            |(Real.log (rate i) - Real.log (rate j)) +
              (Real.log (rate j) - Real.log (rate k))| := by
                congr 1
                ring
        _ ≤ |Real.log (rate i) - Real.log (rate j)| +
              |Real.log (rate j) - Real.log (rate k)| := abs_add_le _ _
        _ ≤ (n : ℝ) * s + s := add_le_add ih (hEdgeLog hedge)
        _ = ((n + 1 : ℕ) : ℝ) * s := by
              norm_num
              ring

/-- A normalized scale in `[1-delta,1+delta]` has logarithm bounded by
`hDelta delta`.  The lower endpoint controls both logarithmic tails. -/
theorem abs_log_normalized_scale_le_hDelta
    (x delta : ℝ)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hxLo : 1 - delta ≤ x)
    (hxHi : x ≤ 1 + delta) :
    |Real.log x| ≤ hDelta delta := by
  have hminus : 0 < 1 - delta := by linarith
  have hplus : 0 < 1 + delta := by linarith
  have hxpos : 0 < x := hminus.trans_le hxLo
  have hlogLo : Real.log (1 - delta) ≤ Real.log x :=
    Real.strictMonoOn_log.monotoneOn hminus hxpos hxLo
  have hlogHi : Real.log x ≤ Real.log (1 + delta) :=
    Real.strictMonoOn_log.monotoneOn hxpos hplus hxHi
  have hproductPos : 0 < (1 + delta) * (1 - delta) :=
    mul_pos hplus hminus
  have hproductLe : (1 + delta) * (1 - delta) ≤ 1 := by
    nlinarith [sq_nonneg delta]
  have hlogProduct :
      Real.log ((1 + delta) * (1 - delta)) ≤ Real.log 1 :=
    Real.strictMonoOn_log.monotoneOn hproductPos (by norm_num) hproductLe
  rw [Real.log_mul (ne_of_gt hplus) (ne_of_gt hminus), Real.log_one] at hlogProduct
  have hlogPlus : Real.log (1 + delta) ≤ -Real.log (1 - delta) := by
    linarith
  unfold hDelta
  rw [abs_le]
  constructor
  · simpa using hlogLo
  · exact hlogHi.trans hlogPlus

/-- Reference-loss logarithmic bound along a path of at most `R` active
edges.  Taking `o` to be a graph center and `R` its radius gives the
graph-center estimate without depending on a particular graph-distance API. -/
theorem reference_loss_log_bound
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (delta : ℝ)
    (hrate : ∀ v, 0 < rate v)
    (hdelta0 : 0 ≤ delta) (hdelta1 : delta < 1)
    (hEdgeLog : ∀ {i j}, active i j →
      |Real.log (rate i) - Real.log (rate j)| ≤ sDelta delta)
    {n R : ℕ} {o i : ι}
    (hpath : ActivePath active n o i)
    (hn : n ≤ R)
    (ell x : ℝ)
    (hbalance : rate i * ell = 2 * x)
    (hxLo : 1 - delta ≤ x)
    (hxHi : x ≤ 1 + delta) :
    |Real.log (ell / (2 / rate o))| ≤
      hDelta delta + (R : ℝ) * sDelta delta := by
  have hxpos : 0 < x := by linarith
  have hs : 0 ≤ sDelta delta := by
    unfold sDelta
    exact Real.log_nonneg (one_le_qDelta delta hdelta0 hdelta1)
  have hrateLog :
      |Real.log (rate o) - Real.log (rate i)| ≤ (n : ℝ) * sDelta delta :=
    path_log_rate_bound active rate (sDelta delta) hs hEdgeLog hpath
  have hrateLogR :
      |Real.log (rate o) - Real.log (rate i)| ≤ (R : ℝ) * sDelta delta := by
    exact hrateLog.trans (mul_le_mul_of_nonneg_right (by exact_mod_cast hn) hs)
  have hell : ell = 2 * x / rate i := by
    apply (eq_div_iff (ne_of_gt (hrate i))).2
    simpa [mul_comm] using hbalance
  have hratio : ell / (2 / rate o) = x * (rate o / rate i) := by
    rw [hell]
    field_simp [ne_of_gt (hrate o), ne_of_gt (hrate i)]
  calc
    |Real.log (ell / (2 / rate o))| =
        |Real.log x + (Real.log (rate o) - Real.log (rate i))| := by
          rw [hratio, Real.log_mul (ne_of_gt hxpos)
            (ne_of_gt (div_pos (hrate o) (hrate i)))]
          rw [Real.log_div (ne_of_gt (hrate o)) (ne_of_gt (hrate i))]
    _ ≤ |Real.log x| +
          |Real.log (rate o) - Real.log (rate i)| := abs_add_le _ _
    _ ≤ hDelta delta + (R : ℝ) * sDelta delta :=
      add_le_add
        (abs_log_normalized_scale_le_hDelta
          x delta hdelta0 hdelta1 hxLo hxHi)
        hrateLogR

/-- Logarithmic diameter consequence, stated through an explicit bounded-path
witness rather than a version-sensitive graph-distance API. -/
theorem diameter_log_rate_bound
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (s : ℝ) (D : ℕ)
    (hs : 0 ≤ s)
    (hEdgeLog : ∀ {i j}, active i j →
      |Real.log (rate i) - Real.log (rate j)| ≤ s)
    (hdiam : ActiveDiameterAtMost active D) :
    ∀ i j,
      |Real.log (rate i) - Real.log (rate j)| ≤ (D : ℝ) * s := by
  intro i j
  rcases hdiam i j with ⟨n, hn, hpath⟩
  calc
    |Real.log (rate i) - Real.log (rate j)| ≤ (n : ℝ) * s :=
      path_log_rate_bound active rate s hs hEdgeLog hpath
    _ ≤ (D : ℝ) * s := by
      apply mul_le_mul_of_nonneg_right _ hs
      exact_mod_cast hn

/-- Powers of a base at least one are monotone in the natural exponent. -/
theorem pow_le_pow_of_one_le_of_nat_le
    (q : ℝ) (hq : 1 ≤ q) {m n : ℕ} (hmn : m ≤ n) :
    q ^ m ≤ q ^ n := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hmn
  rw [pow_add]
  have hq0 : 0 ≤ q := le_trans (by norm_num) hq
  have hleft : 0 ≤ q ^ m := pow_nonneg hq0 m
  have hright : 1 ≤ q ^ k := one_le_pow₀ hq
  simpa using mul_le_mul_of_nonneg_left hright hleft

/-- Multiplicative diameter consequence. -/
theorem diameter_rate_ratio_bounds
    {ι : Type*} (active : ι → ι → Prop)
    (rate : ι → ℝ) (q : ℝ) (D : ℕ)
    (hrate : ∀ v, 0 < rate v)
    (hq : 1 ≤ q)
    (hEdge : ∀ {i j}, active i j →
      rate j ≤ q * rate i ∧ rate i ≤ q * rate j)
    (hdiam : ActiveDiameterAtMost active D) :
    ∀ i j,
      1 / q ^ D ≤ rate i / rate j ∧
        rate i / rate j ≤ q ^ D := by
  intro i j
  rcases hdiam i j with ⟨n, hn, hpath⟩
  have hcross := path_rate_cross_bounds active rate q hq hEdge hpath
  have hpow := pow_le_pow_of_one_le_of_nat_le q hq hn
  have hcross₁ : rate j ≤ q ^ D * rate i := by
    calc
      rate j ≤ q ^ n * rate i := hcross.1
      _ ≤ q ^ D * rate i :=
        mul_le_mul_of_nonneg_right hpow (le_of_lt (hrate i))
  have hcross₂ : rate i ≤ q ^ D * rate j := by
    calc
      rate i ≤ q ^ n * rate j := hcross.2
      _ ≤ q ^ D * rate j :=
        mul_le_mul_of_nonneg_right hpow (le_of_lt (hrate j))
  have hqpos : 0 < q := lt_of_lt_of_le (by norm_num) hq
  have hqpowpos : 0 < q ^ D := pow_pos hqpos D
  constructor
  · apply (div_le_div_iff₀ hqpowpos (hrate j)).2
    simpa [mul_comm] using hcross₁
  · apply (div_le_iff₀ (hrate j)).2
    simpa [mul_comm] using hcross₂

/-- Algebraic radial near-equality estimate used by the covariance transfer. -/
theorem radial_covariance_error_bounds
    (Q rate eta : ℝ)
    (hrate : 0 < rate)
    (hQlower : 1 ≤ Q)
    (hQupper : Q ≤ 1 + eta) :
    0 ≤ 4 * Q / rate - 4 / rate ∧
      4 * Q / rate - 4 / rate ≤ 4 * eta / rate := by
  have hrne : rate ≠ 0 := ne_of_gt hrate
  have hrearrange :
      4 * Q / rate - 4 / rate = (4 * Q - 4) / rate := by
    field_simp [hrne]
  rw [hrearrange]
  constructor
  · exact div_nonneg (by nlinarith) (le_of_lt hrate)
  · apply (div_le_div_iff₀ hrate hrate).2
    nlinarith

end AFPBarrier
