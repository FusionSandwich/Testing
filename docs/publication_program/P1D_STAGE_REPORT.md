# P1D stage report — quantitative stability at the sharp frontier

## Frozen input and additive work line

P1D starts from the exact accepted P1C archive:

```text
P1C archive:
    archive/afp-publication-p1c-equality-geometry-verified

P1C commit:
    9ae0c8f16e8cd97cd84ef89b25064512a04b308a

P1C tree:
    289113bb760fbe079f5d581c10f1cefea8a72931

P1D branch:
    agent/afp-publication-p1d-quantitative-stability-9ae0c8f1

P1D archive after exact-head verification:
    archive/afp-publication-p1d-quantitative-stability-verified
```

P1D is a normal non-merging descendant. P1C/P1B/P1A and every accepted
historical archive remain read-only. Literal candidate commit/tree, workflow
run, artifact identifiers and digests, and archive equality are recorded only
after exact-head CI; a commit cannot contain its own identifier.

## Universal master theorem

Let `n=d-1`,

```text
a_0=n^2/r_max,
eta=2 delta+delta^2,
s_i=r_max/r_i-1,
v_i=V_i/a_0,
q_i=x_i-1=s_i+v_i.
```

From the P1B two-defect inequality and
`D_2 r_max<=d(d-1)(1+delta)`, P1D proves

```text
sum_i w_i (2 q_i+q_i^2)
  + n/(d a_0^2) sum_i w_i ||B_i||_F^2
<= eta.
```

Consequently,

```text
sum w_i (x_i-1)^2 <= eta,
sum w_i (r_max/r_i-1)^2 <= eta,
sum w_i ||B_i||_F^2 <= d(d-1)^3 eta/r_max^2,
sum w_i V_i <= a_0 delta,
sum w_i V_i^2 <= a_0^2 eta.
```

No connectedness, sampling injectivity, equal mass, regular degree, or
transitivity enters these statements.

## Weighted, edgewise, and graph consequences

With the tensor-corrected allowance

```text
H=eta-n E_B/(d a_0^2),
```

the exact pointwise scalar envelope is

```text
q_i <= sqrt(1+H/w_i)-1.
```

The weighted mass of vertices with `q_i`, `s_i`, or `v_i` at least `rho` is
at most `min(1,H/[rho(2+rho)])`. A vertex-count or uniform pointwise theorem
uses `w_min` explicitly.

Normalizing directed conductance by
`nu_ij=gamma_ij/sum_k w_k r_k` gives a symmetric probability measure. P1D
proves an exact shell-loss identity and

```text
E_nu[(ell_ij/ell_0-1)^2] <= sqrt(1+H) H/2.
```

If every active `p_ij=a_ij/r_i` is at least `kappa`, local variance becomes
an edgewise estimate with the exact `kappa^(-1/2)` dependence. Multiplicative
path bounds show literal products; additive propagation shows `sqrt(L)`;
effective-resistance and Poincare alternatives display resistance,
`lambda_P`, `w_min`, and any canonical-path congestion rather than hiding
them.

## Local covariance and sampled-shell conclusions

P1C's orthogonal block identity

```text
||B_i||_F^2=2||h_i||^2+||A_i||_F^2
```

gives explicit mixed radial--tangent covariance and tangent anisotropy
bounds. The covariance rows satisfy

```text
sum_i w_i ||C_i-C_i^*||_F^2
 = sum_i w_i ||M_i-c_0 Z_i||_F^2
 <= K_0,

K_0=d(d-1)^3 eta/r_max^2.
```

Hence Hoffman--Wielandt controls the local shell spectrum. On the genuinely
sampled quotient, with lower sampling-frame constant `alpha_X`,

```text
||U-c_0 iota|| <= sqrt(K_0/alpha_X).
```

This controls both compressed shell splitting and leakage from `im S_2`;
range invariance is not assumed. Tetrahedral/octahedral/cubical aliases and
an exact near-singular sampling family show why the quotient is necessary
and why the underlying Hilbert--Schmidt-to-quotient transfer has the sharp
factor `alpha_X^(-1/2)`.

## Strong local geometric stability

Two constructive results are separated.

1. If the raw tangent covariance satisfies `T_i/r_i >= lambda P_i`, polar
   whitening constructs an exact centered weighted tight frame. Its weighted
   Procrustes displacement is bounded by

   ```text
   (||B_i||_F^2+V_i^2/(d-1)) /
   [r_i^2 (sqrt(lambda)+sqrt(theta_i))^2].
   ```

2. To retain unit tangent directions and positive probabilities, P1D assumes
   an explicit shell floor `s_-`, edge-probability floor `kappa`, and minimum
   singular value `mu` for the centered first/second-moment feature operator.
   The theorem gives the minimum-norm weight correction, its positivity
   radius, and a labeled spherical-neighbor metric modulo rotations fixing
   the center.

No global embedding-stability theorem is imported. A zero-loss bridge shows
that connectedness alone leaves arbitrary relative tangent rotations.

## Necessity and exact audit

The ordinary theorem gives analytic constructions showing the need for:

- `w_min`: a cube/tetrahedron equality mixture concentrates fixed rate defect
  on vanishing mass;
- `kappa`: a compass generator puts order-one defect on a probability-`kappa`
  antipodal edge;
- diameter/gap/resistance: exact cyclic ramps certify the standalone
  local-edge propagation dependence, while `N`-cycles certify the gap
  dependence; the ramp is not claimed to have global frontier slack tending
  to zero;
- tangent lower-frame and shell margins: a rank-one tangent figure has
  `B_i->0` but stays away from every unit tight frame;
- sampling quotient/gap: exact aliases and a family attaining the
  `alpha_X^(-1/2)` transfer;
- overlap: zero-loss bridges preserve arbitrary relative rotations.

The deterministic audit has 30 fixtures and combines exact SymPy algebra
with outward-rounded interval arithmetic. It never uses floating-point rank
thresholds and does not replace the all-orders proof.

## Formal core and acceptance contract

`AFPBarrier/QuadraticFidelityStability.lean` formalizes the normalized slack
identity, scalar square and linear extraction, nonnegative component bounds,
pointwise and `w_min` bounds, sharp bad-vertex mass, tensor constants, and
scaled variance. The aggregate import and focused axiom audit include it;
placeholders, project axioms, and project constants are forbidden.

The dedicated exact-head workflow must pass on the literal P1D branch and,
after create-only freezing, on the immutable P1D archive. It runs:

```text
P1D exact/interval audit and retained P1C/P1B/P1A audits;
every retained Prompt-1-through-Prompt-4 exact regression;
source-pinned Plantri enumeration of 9,150 maps;
full Lean 4.30 build and focused P1D/axiom compilation;
placeholder, axiom, constant, generated-artifact, scope and diff checks;
exact P1C ancestry/tree and all immutable-ref checks;
source/evidence artifact hashing and final-state revalidation.
```

No run, job, artifact, digest, or success claim is recorded before the
literal exact-head workflow supplies it.
