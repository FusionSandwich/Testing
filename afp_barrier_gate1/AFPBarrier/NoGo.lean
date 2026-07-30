import AFPBarrier.JumpGenerator

/-!
# The second-harmonic no-go theorem

The theorem is stated algebraically for an arbitrary positive eigenvalue
`lam`. On `S^(d-1)`, the degree-one eigenvalue is `lam = d - 1`, and the
zonal degree-two harmonic forces the square value used below.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A finite nonnegative jump generator cannot simultaneously satisfy
`f(i)=1`, `L f(i)=-lam`, and `L(f^2)(i)=-2 lam` when `lam>0`. -/
theorem no_exact_linear_and_square_at_peak
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (lam : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlam : 0 < lam)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -lam)
    (hsquare : jumpGenerator a (fun j => (f j) ^ 2) i = -2 * lam) :
    False := by
  have hcarre : carreDuChamp a f i = 0 := by
    rw [← jumpGenerator_square_identity]
    rw [hsquare, hfi, hlinear]
    ring
  have hzero : jumpGenerator a f i = 0 :=
    zero_carreDuChamp_forces_generator_zero
      (a := a) (f := f) (i := i) ha hcarre
  linarith

/-- A shifted-quadratic formulation. The resonance condition
`mu * (1-c) = 2*lam` is exactly what holds for

`g(x)=p·x`, `c=1/d`, `lam=d-1`, and `mu=2d`

on the sphere `S^(d-1)`. -/
theorem no_exact_shifted_quadratic_at_peak
    (a : ι → ι → ℝ) (g : ι → ℝ) (i : ι)
    (lam mu c : ℝ)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hlam : 0 < lam)
    (hresonance : mu * (1 - c) = 2 * lam)
    (hgi : g i = 1)
    (hdegreeOne : jumpGenerator a g i = -lam)
    (hdegreeTwo :
      jumpGenerator a (fun j => (g j) ^ 2 - c) i
        = -mu * ((g i) ^ 2 - c)) :
    False := by
  have hshift :
      jumpGenerator a (fun j => (g j) ^ 2 - c) i
        = jumpGenerator a (fun j => (g j) ^ 2) i :=
    jumpGenerator_sub_const
      (a := a) (f := fun j => (g j) ^ 2) (c := c) (i := i)
  have hsquare :
      jumpGenerator a (fun j => (g j) ^ 2) i = -2 * lam := by
    calc
      jumpGenerator a (fun j => (g j) ^ 2) i
          = jumpGenerator a (fun j => (g j) ^ 2 - c) i := hshift.symm
      _ = -mu * ((g i) ^ 2 - c) := hdegreeTwo
      _ = -2 * lam := by rw [hgi]; nlinarith
  exact no_exact_linear_and_square_at_peak
    (a := a) (f := g) (i := i) (lam := lam)
    ha hlam hgi hdegreeOne hsquare

end AFPBarrier
