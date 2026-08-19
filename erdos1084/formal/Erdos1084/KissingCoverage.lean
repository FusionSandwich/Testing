import Mathlib
import Erdos1084.FiniteSpherePacking

namespace Erdos1084

/-!
# Spherical codes, kissing-number degree bounds, and degree-twelve coverage

This file separates the difficult external theorem "the three-dimensional kissing number is at
most twelve" from its elementary consequences for the Phase-I proof.
-/

noncomputable section

/-- A finite unit spherical code whose distinct points have inner product at most `1/2`. -/
structure PiThirdSphericalCode (ι : Type*) where
  point : ι → Point3
  norm_one : ∀ i, ‖point i‖ = 1
  separated : ∀ ⦃i j⦄, i ≠ j → ⟪point i, point j⟫_ℝ ≤ 1 / 2

/-- Abstract statement that the three-dimensional kissing number is at most twelve. -/
def KissingNumberThreeAtMostTwelve : Prop :=
  ∀ (ι : Type*) [Fintype ι],
    PiThirdSphericalCode ι → Fintype.card ι ≤ 12

namespace PiThirdSphericalCode

/-- Adjoin one further unit direction that is separated from every old code point. -/
def adjoin {ι : Type*} (C : PiThirdSphericalCode ι)
    (u : Point3) (hu : ‖u‖ = 1)
    (hsep : ∀ i, ⟪u, C.point i⟫_ℝ ≤ 1 / 2) :
    PiThirdSphericalCode (Option ι) where
  point
    | none => u
    | some i => C.point i
  norm_one
    | none => hu
    | some i => C.norm_one i
  separated := by
    intro a b hab
    cases a with
    | none =>
        cases b with
        | none => exact (hab rfl).elim
        | some j => exact hsep j
    | some i =>
        cases b with
        | none =>
            rw [real_inner_comm]
            exact hsep i
        | some j =>
            apply C.separated
            intro hij
            apply hab
            simpa [hij]

/-- A twelve-point code is covering at threshold `1/2` if the kissing bound is twelve. -/
theorem covers_of_card_eq_twelve
    {ι : Type*} [Fintype ι]
    (hk : KissingNumberThreeAtMostTwelve)
    (C : PiThirdSphericalCode ι)
    (hcard : Fintype.card ι = 12)
    (u : Point3) (hu : ‖u‖ = 1) :
    ∃ i, 1 / 2 ≤ ⟪u, C.point i⟫_ℝ := by
  classical
  by_contra hnot
  push_neg at hnot
  let C' := C.adjoin u hu (fun i => le_of_lt (hnot i))
  have hbound := hk (Option ι) C'
  simp [hcard] at hbound

end PiThirdSphericalCode

/-- Contact-neighbor labels of a point, represented by the neighbor finset subtype. -/
abbrev ContactNeighbor {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) :=
  {j : Fin n // j ∈ X.contactGraph.neighborFinset i}

/-- Unit direction from one point to a contact neighbor. -/
def contactNeighborDirection {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (j : ContactNeighbor X i) : Point3 :=
  X.point j.1 - X.point i

/-- Contact-neighbor directions have norm one. -/
theorem contactNeighborDirection_norm {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (j : ContactNeighbor X i) :
    ‖contactNeighborDirection X i j‖ = 1 := by
  have hadj : X.contactGraph.Adj i j.1 := by
    simpa using j.2
  rw [contactNeighborDirection, norm_sub_rev, ← dist_eq_norm]
  simpa [dist_comm] using hadj.2

/-- Distinct contact-neighbor directions have inner product at most `1/2`. -/
theorem contactNeighborDirection_inner_le_half {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    {j k : ContactNeighbor X i} (hjk : j ≠ k) :
    ⟪contactNeighborDirection X i j,
      contactNeighborDirection X i k⟫_ℝ ≤ 1 / 2 := by
  have hjkval : j.1 ≠ k.1 := by
    intro h
    apply hjk
    exact Subtype.ext h
  have hsep := X.separated hjkval
  have hnormj := contactNeighborDirection_norm X i j
  have hnormk := contactNeighborDirection_norm X i k
  have hdiff :
      contactNeighborDirection X i j -
          contactNeighborDirection X i k =
        X.point j.1 - X.point k.1 := by
    simp [contactNeighborDirection]
    abel
  have hdist :
      1 ≤ ‖contactNeighborDirection X i j -
          contactNeighborDirection X i k‖ := by
    rw [hdiff, ← dist_eq_norm]
    exact hsep
  have hsq := norm_sub_sq_real
    (contactNeighborDirection X i j)
    (contactNeighborDirection X i k)
  nlinarith [sq_nonneg
    ‖contactNeighborDirection X i j - contactNeighborDirection X i k‖]

/-- The contact-neighbor directions form a `π/3`-separated spherical code. -/
def contactNeighborCode {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) :
    PiThirdSphericalCode (ContactNeighbor X i) where
  point := contactNeighborDirection X i
  norm_one := contactNeighborDirection_norm X i
  separated := contactNeighborDirection_inner_le_half X i

/-- Kissing number twelve implies the contact-degree bound used by Phase I. -/
theorem contactDegree_le_twelve_of_kissing
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) :
    X.contactDegree i ≤ 12 := by
  classical
  have hbound := hk (ContactNeighbor X i) (contactNeighborCode X i)
  simpa [UnitSeparatedConfiguration.contactDegree, ContactNeighbor] using hbound

/-- Kissing number twelve supplies the global visible degree-bound interface. -/
theorem hasContactDegreeAtMostTwelve_of_kissing
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) :
    X.HasContactDegreeAtMostTwelve := by
  intro i
  exact contactDegree_le_twelve_of_kissing hk X i

/-- A degree-twelve contact environment covers every unit direction at threshold `1/2`. -/
theorem degree_twelve_contact_directions_cover
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (hdegree : X.contactDegree i = 12)
    (u : Point3) (hu : ‖u‖ = 1) :
    ∃ j : ContactNeighbor X i,
      1 / 2 ≤ ⟪u, contactNeighborDirection X i j⟫_ℝ := by
  classical
  apply PiThirdSphericalCode.covers_of_card_eq_twelve
    hk (contactNeighborCode X i)
  · simpa [UnitSeparatedConfiguration.contactDegree, ContactNeighbor] using hdegree
  · exact u
  · exact hu

end

end Erdos1084
