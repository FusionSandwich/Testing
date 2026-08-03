# Prompt 2 stage report — corrective closeout

## 1. Provenance and bounded scope

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Actual remote target head at closeout start:
  `1835918fe9d0b941395e9f00f6ac5514129cefa0`
- Previously reported head:
  `694b913c99364bb0032a8ffbd7008b549b491af0`
- Reported head resolution: `NO COMMIT FOUND`
- Prompt 2 integration merge preceding the actual target head:
  `f9fb1e336a4569c2d7e2e440821976bd30a6c29f`
- Closeout branch:
  `agent/afp-pure-math-p2-closeout-corrected`
- Immutable transport archive:
  `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

The only intervening target change after `f9fb1e...` was the integration-record
commit `1835918...`. The closeout changes only pure-mathematics Lean source,
exact audits, claim-control documents, and the three pure-math workflows. It
does not begin Prompt 3 classification or near-rigidity and does not modify
transport, Radiant, HTS, multigroup, evaluated-material, spatial, or production
solver paths.

A literal multiagent-v2 runtime was unavailable. It was not used or claimed.
The independent audit routes are recorded in Section 8.

## 2. Defects found after the initial Prompt 2 integration

### 2.1 Equivariant positivity defect — PR #17

The earlier equivariant irreducibility statement required only one positive
jump between distinct embedded points. Its proof used

```text
beta_i=sum_j a_ij(1-Phi_i dot Phi_j)^2>0,
```

which is valid from one positive term only when every other off-diagonal rate
is nonnegative. Signed terms can cancel the positive square contribution.

The theorem is corrected to require

```text
a_ij>=0 for every i!=j.
```

Reversibility is not required. Conservation fixes only the diagonal matrix
entries. The positive distinct-jump assumption is used after global
nonnegativity to make one radial covariance strictly positive.

### 2.2 Centered-product omission

The earlier product discussion established the uncentered implication

```text
L(f^2)=-2lambda f^2 => Gamma(f)=0,
```

but did not give the arbitrary shift or centered resonance. It could therefore
be read as a universal centered-square obstruction, which is false.

The closeout adds the exact arbitrary-target residual and the Boolean
counterexample.

### 2.3 Low-degree hierarchy omission

The existing Pell search did not include the required hand-derived and
machine-checked `S^2` table for `ell=1,...,6`. The table is now part of the
theorem and exact closeout audit.

### 2.4 User-axiom verification defect — PR #18

The dedicated workflow scanned for singular `axiom` inside one Lean file but
missed Lean's valid plural declaration syntax `axioms`. The corrected workflow
scans the aggregate pure-math Lean source with an anchored
`(axiom|axioms)` declaration regex and contains deterministic singular/plural
fixtures.

## 3. Accepted covariance and sampled-space core

For a finite coordinate eigenmap,

```text
L(Phi^T A Phi)(i)
  =-2lambda Phi_i^T A Phi_i+tr(A^T C_i).
```

For `q_{A,c}=Phi^T A Phi-c` and target `-mu`, exactness is equivalent to

```text
tr(A^T C_i)
 +(mu-2lambda)Phi_i^T A Phi_i
 -mu c=0
```

at every state.

In the spherical degree-two specialization,

```text
lambda=d-1,
mu=2d,
M_i=P_0(C_i+2Phi_iPhi_i^T),
S_X(A)_i=Phi_i^T A Phi_i,
R_X(A)_i=<A,M_i>_F.
```

The exact structural relations are

```text
E_form=ker R_X=span{M_i}^perp,
R_X=(L+2dI)S_X,
K_X=ker S_X subset E_form,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

## 4. Corrected rigidity and exact signed boundary

### 4.1 Positive axial rigidity

If every local covariance is axially isotropic with positive radial variance,
then every residual row is a positive scaling of the corresponding sampling
row. Hence

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension. The closeout audit
checks the coordinate eigenvalue and explicit inverse sampling formula exactly
for dimensions 2 through 10.

### 4.2 Corrected positive equivariant rigidity

Let a finite group act transitively, let the unit-sphere eigenmap and rates be
equivariant, require

```text
L Phi=-(d-1)Phi,
a_ij>=0 for every i!=j,
```

and assume the real conjugation representation on `Sym_0(d)` is irreducible.
If at least one positive jump joins distinct embedded points, then

```text
E_form={0}.
```

The proof is valid without reversibility. Irreducibility makes the form kernel
zero or full. The full alternative forces zero radial covariance, while global
nonnegativity and one positive distinct jump force positive radial covariance.

### 4.3 Signed regular-pentagon counterexample

For the regular pentagon, set

```text
u=(5+3sqrt(5))/10>0
```

on distance-one neighbors and

```text
v=(5-3sqrt(5))/10<0
```

on distance-two neighbors. Exact `Q(sqrt(5))` calculation gives

```text
L1=0,
Lx=-x,
Ly=-y,
Lcos(2theta)=-4cos(2theta),
Lsin(2theta)=-4sin(2theta).
```

Thus

```text
E_form=Sym_0(2),
dim E_sample=2.
```

The `C_5` action on `Sym_0(2)` is rotation through `4pi/5`; its characteristic
discriminant `(sqrt(5)-5)/2` is negative, so the real representation is
irreducible. This is the exact counterexample when global positivity is
omitted.

## 5. Centered product and semigroup theory

Define

```text
Gamma(f,g)(i)
 =1/2 sum_j a_ij(f(j)-f(i))(g(j)-g(i)).
```

The completed theorem package proves

```text
L(fg)-fLg-gLf=2Gamma(f,g).
```

If `Lf=-lambda f` and `Lg=-nu g`, then

```text
L(fg-c)+mu(fg-c)
 =2Gamma(f,g)+(mu-lambda-nu)fg-mu c.
```

At additive resonance,

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2Gamma(f,g)=(lambda+nu)c.
```

For a square,

```text
L(f^2-c)=-2lambda(f^2-c)
iff
Gamma(f,f)=lambda c.
```

The uncentered `c=0` case forces zero carré du champ. On an irreducible
positive chain with `lambda>0`, this forces the eigenfunction to be zero. A
centered square may be nonzero.

### Boolean regression

On the four-state Boolean square with unit coordinate-flip rates and
`f=x_1+x_2`,

```text
Lf=-2f,
f^2-2=2x_1x_2!=0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

For `P_t=exp(tL)`, centered resonance gives

```text
P_t(f^2)-(P_t f)^2=c(1-exp(-2lambda t)).
```

The converse follows by differentiating the finite matrix exponential at
`t=0`. Jensen equality remains the separate condition that `f` is constant on
the positive transition support. The Boolean variance is

```text
2(1-exp(-4t))>0
```

for `t>0`; Jensen equality does not hold.

## 6. Spherical shift and hierarchy audit

On `S^(d-1)`:

```text
coordinate eigenvalue=d-1,
doubled coordinate eigenvalue=2(d-1),
degree-two eigenvalue=2d.
```

The covariance theorem therefore has shift `2` and is not additive square
resonance.

For `S^2`, the pointwise multiplication image of `Sym^2(H_ell)` contains the
even degrees `0,2,...,2ell`. The exact table for `ell=1,...,6` is:

| `ell` | degrees | eigenvalues | additive target | resonance |
|---:|---|---|---:|---|
| 1 | `0,2` | `0,6` | 4 | none |
| 2 | `0,2,4` | `0,6,20` | 12 | none |
| 3 | `0,2,4,6` | `0,6,20,42` | 24 | none |
| 4 | `0,2,4,6,8` | `0,6,20,42,72` | 40 | none |
| 5 | `0,2,4,6,8,10` | `0,6,20,42,72,110` | 60 | none |
| 6 | `0,2,4,6,8,10,12` | `0,6,20,42,72,110,156` | 84 | none |

Centering removes only degree zero. Odd/even antipodal equality sets and every
degree-specific sampling kernel/cross-degree alias still require explicit
audit.

The generalized resonance equation remains Pell-type. The bounded exact search
retains the higher-dimensional hits

```text
(4,4,6), (6,8,12), (8,12,18), (9,5,8).
```

No `ell`-indexed sampled dimension tradeoff, multiplicity obstruction, or new
global consequence survives the identifiability and alias checks. The general
hierarchy remains `REJECTED FOR PROMPT 2` for that reason, not because centered
squares are impossible.

## 7. Lean and exact verification boundary

`AFPBarrier/QuadraticCovariance.lean` now formalizes:

- bilinear `jumpGamma` and the product identity;
- the arbitrary shifted product residual and target equivalence;
- additive product resonance;
- centered and uncentered square resonance;
- the positive uncentered pointwise obstruction;
- the covariance identity and shifted quadratic target;
- trace-free projection contraction;
- restricted rank-nullity;
- sampling-kernel inclusion and sampled-range intersection; and
- axial row-scaling consequences.

The exact closeout audit verifies:

- existing covariance/factorization/Platonic tests;
- regular-simplex formulas;
- four-point signed restoration;
- signed pentagon counterexample and irreducibility certificate;
- centered product algebra;
- Boolean centered square;
- semigroup variance;
- `S^2` `ell=1,...,6` table;
- existing bounded/Pell assertions; and
- singular/plural axiom-regex fixtures.

## 8. Independent and adversarial audit routes

| Route | Exact question | Outcome |
|---|---|---|
| Equivariant proof audit | Does every use of radial positivity follow from stated hypotheses? | Global off-diagonal nonnegativity added; reversibility confirmed unused |
| Signed counterexample audit | Can negative rates cancel radial covariance under irreducible symmetry? | Yes; exact regular pentagon gives full quadratic exactness |
| Centered product derivation | What is the residual for arbitrary `mu,c`? | Exact residual and additive equivalence proved independently and in Lean |
| Boolean audit | Can a positive generator have nonzero centered doubled resonance? | Yes; exact four-state example with constant `Gamma=4` |
| Jensen adversary | Does centered resonance imply zero semigroup variance? | No; Boolean variance is strictly positive |
| Low-degree harmonic audit | Do `S^2` rows `ell=1,...,6` contain additive resonance? | No; exact integer table |
| Workflow policy audit | Are both `axiom` and `axioms` rejected without false positives? | Yes; anchored aggregate scan plus fixtures |
| Claim-status audit | Is abstract propagation still mislabeled conjectural? | Corrected to `PROVED / LEAN`; Prompt 3 specializations remain open |

## 9. Closeout status

The closeout is not certified by prose alone. Final closure requires all three
workflows on the literal merged target head, archive verification, review-thread
resolution, final commit/tree resolution, and completion of
`PROMPT2_CLOSEOUT_AUDIT.md` and `PROMPT3_READINESS_HANDOFF.md`.
