import Mathlib
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.RadiusTwoAssembly

namespace Erdos1084

/-!
# Radius-two geometric bridge lemmas

This file isolates the exact interfaces between the external geometric theorems and the
algebraic/finite-sum spine already formalized in the project.

No external theorem is introduced as an axiom.  Instead, each bridge accepts the published
geometric statement as an explicit hypothesis and proves the normalization and algebraic
consequence used by the radius-two contact-number argument.
-/

noncomputable section

/-- Three-dimensional Euclidean space in the normalization used by the packing proof. -/
abbrev RadiusTwoE3 := EuclideanSpace ℝ (Fin 3)

/--
A finite-code formulation of the upper kissing-number bound `τ₃ ≤ 12`.

Unit vectors represent centers of unit balls tangent to a central unit ball after division by two.
Chord separation at least one is equivalent to nonoverlap of the tangent unit balls.
-/
def KissingNumberAtMostTwelve : Prop :=
  ∀ s : Finset RadiusTwoE3,
    (∀ u ∈ s, ‖u‖ = 1) →
    (∀ u ∈ s, ∀ v ∈ s, u ≠ v → 1 ≤ ‖u - v‖) →
    s.card ≤ 12

/-- Reversing a difference does not change its norm. -/
theorem radiusTwo_norm_sub_comm (u v : RadiusTwoE3) :
    ‖u - v‖ = ‖v - u‖ := by
  have h : u - v = -(v - u) := by
    abel
  rw [h, norm_neg]

/--
The kissing-number theorem implies that twelve contact directions cover the unit sphere by
closed chordal caps of radius one.  These are exactly the angular-radius-`π/3` caps appearing
on a physical enlarged sphere of radius two.
-/
theorem kissing_twelve_closed_cap_cover
    (hk : KissingNumberAtMostTwelve)
    (s : Finset RadiusTwoE3)
    (hcard : s.card = 12)
    (hunit : ∀ u ∈ s, ‖u‖ = 1)
    (hsep : ∀ u ∈ s, ∀ v ∈ s, u ≠ v → 1 ≤ ‖u - v‖)
    {w : RadiusTwoE3}
    (hw : ‖w‖ = 1) :
    ∃ u ∈ s, ‖w - u‖ ≤ 1 := by
  classical
  by_contra hcover
  have hfar : ∀ u ∈ s, 1 < ‖w - u‖ := by
    intro u hu
    have hnle : ¬ ‖w - u‖ ≤ 1 := by
      intro hle
      exact hcover ⟨u, hu, hle⟩
    exact lt_of_not_ge hnle
  have hwnot : w ∉ s := by
    intro hws
    have hbad := hfar w hws
    norm_num at hbad
  let t : Finset RadiusTwoE3 := insert w s
  have htunit : ∀ u ∈ t, ‖u‖ = 1 := by
    intro u hu
    rw [Finset.mem_insert] at hu
    rcases hu with rfl | hu
    · exact hw
    · exact hunit u hu
  have htsep : ∀ u ∈ t, ∀ v ∈ t, u ≠ v → 1 ≤ ‖u - v‖ := by
    intro u hu v hv huv
    rw [Finset.mem_insert] at hu hv
    rcases hu with rfl | hu <;> rcases hv with rfl | hv
    · exact (huv rfl).elim
    · exact le_of_lt (hfar v hv)
    · have h := le_of_lt (hfar u hu)
      rw [radiusTwo_norm_sub_comm]
      exact h
    · exact hsep u hu v hv huv
  have htcard : t.card = 13 := by
    simp [t, hwnot, hcard]
  have hbound := hk t htunit htsep
  omega

/--
Radius-two cap normalization in chordal form: a point `2v` on the enlarged central sphere lies
in the radius-two ball centered at `2u` exactly when the unit directions have chord distance at
most one.
-/
theorem radiusTwo_covering_ball_iff
    (u v : RadiusTwoE3) :
    ‖(2 : ℝ) • v - (2 : ℝ) • u‖ ≤ 2 ↔ ‖v - u‖ ≤ 1 := by
  rw [← smul_sub, norm_smul]
  norm_num

/--
Algebraic adapter from the three-dimensional Euclidean isoperimetric inequality to the surface
lower bound used by the radius-two proof.

`V` and `A` denote volume and boundary area.  The variable `x` is an abstract nonnegative
representative of `n^(2/3)`, encoded by `x^3 = n^2` so no real-power API is needed here.
-/
theorem euclidean_isoperimetric_to_radiusTwo_lower
    {n x V A : ℝ}
    (hn : 0 ≤ n)
    (hx : 0 ≤ x)
    (hroot : x ^ 3 = n ^ 2)
    (hV : (4 * Real.pi / 3) * n ≤ V)
    (hVnonneg : 0 ≤ V)
    (hAnonneg : 0 ≤ A)
    (hIso : 36 * Real.pi * V ^ 2 ≤ A ^ 3) :
    4 * Real.pi * x ≤ A := by
  let b : ℝ := (4 * Real.pi / 3) * n
  have hb : 0 ≤ b := by
    dsimp [b]
    positivity
  have htargetNonneg : 0 ≤ 4 * Real.pi * x := by
    positivity
  have hV2 : b ^ 2 ≤ V ^ 2 := by
    have hprod : 0 ≤ (V - b) * (V + b) :=
      mul_nonneg (sub_nonneg.mpr hV) (add_nonneg hVnonneg hb)
    nlinarith
  have hcubeA : 64 * Real.pi ^ 3 * n ^ 2 ≤ A ^ 3 := by
    calc
      64 * Real.pi ^ 3 * n ^ 2 = 36 * Real.pi * b ^ 2 := by
        dsimp [b]
        ring
      _ ≤ 36 * Real.pi * V ^ 2 :=
        mul_le_mul_of_nonneg_left hV2 (by positivity)
      _ ≤ A ^ 3 := hIso
  have htargetCube : (4 * Real.pi * x) ^ 3 ≤ A ^ 3 := by
    calc
      (4 * Real.pi * x) ^ 3 = 64 * Real.pi ^ 3 * x ^ 3 := by ring
      _ = 64 * Real.pi ^ 3 * n ^ 2 := by rw [hroot]
      _ ≤ A ^ 3 := hcubeA
  by_contra hnot
  have hlt : A < 4 * Real.pi * x := lt_of_not_ge hnot
  have htpos : 0 < 4 * Real.pi * x := lt_of_le_of_lt hAnonneg hlt
  have hsum :
      0 < (4 * Real.pi * x) ^ 2 + (4 * Real.pi * x) * A + A ^ 2 := by
    have hsquare : 0 < (4 * Real.pi * x) ^ 2 := sq_pos_of_pos htpos
    have hmiddle : 0 ≤ (4 * Real.pi * x) * A :=
      mul_nonneg htargetNonneg hAnonneg
    have hA2 : 0 ≤ A ^ 2 := sq_nonneg A
    nlinarith
  have hprod :
      0 < ((4 * Real.pi * x) - A) *
        ((4 * Real.pi * x) ^ 2 + (4 * Real.pi * x) * A + A ^ 2) :=
    mul_pos (sub_pos.mpr hlt) hsum
  have hcubes : A ^ 3 < (4 * Real.pi * x) ^ 3 := by
    nlinarith
  exact (not_lt_of_ge htargetCube) hcubes

/--
Algebraic adapter from a spherical-neighborhood covered-area lower bound to the strict affine
local exposed-area charge.

The geometric input is exactly the conclusion supplied by spherical neighborhood
isoperimetry after the cap-neighborhood identification.  The factor four converts direction
area on the unit sphere to physical area on a sphere of radius two.
-/
theorem spherical_neighborhood_to_local_charge
    {d q H covered exposure : ℝ}
    (hCovered : 2 * Real.pi * (1 - q) ≤ covered)
    (hExposure : exposure ≤ 4 * (4 * Real.pi - covered))
    (hH : H = 1 + q)
    (hEnvelope : H < (3 / 20 : ℝ) * (12 - d)) :
    exposure < (6 * Real.pi / 5) * (12 - d) := by
  have hToH : exposure ≤ 8 * Real.pi * H := by
    rw [hH]
    nlinarith [Real.pi_pos]
  have hStrict :
      8 * Real.pi * H < (6 * Real.pi / 5) * (12 - d) := by
    have hmul := mul_lt_mul_of_pos_left hEnvelope (show 0 < 8 * Real.pi by positivity)
    nlinarith
  exact lt_of_le_of_lt hToH hStrict

end

end Erdos1084
