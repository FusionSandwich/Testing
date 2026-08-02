# Prompt 2 stage report — sampled quadratic covariance and spectral products

## 1. Baseline and scope

- Repository: `FusionSandwich/Testing`
- Corrected Prompt 1 baseline:
  `923dc47dae4f83dbea9cd56aa904164c6378e52d`
- Corrected Prompt 1 branch:
  `agent/afp-pure-math-p1-local-global-corrected`
- Original checkpoint named in Prompt 2:
  `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Isolated Prompt 2 implementation branch:
  `agent/afp-quadratic-covariance-p2-corrected`
- Immutable transport archive:
  `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

Prompt 2 is developed from the corrected Prompt 1 theorem tree rather than
silently discarding the later local/global corrections. The diff is confined
to pure mathematics, exact symbolic regressions, claim-control documentation,
Lean finite algebra, and a dedicated workflow. It introduces no transport,
Radiant, HTS, multigroup, or spatial-solver work and does not modify the frozen
archive.

A literal multiagent-v2 runtime was not exposed in this execution environment.
It was not used and is not claimed. Independent covariance, sampling,
symmetry, signed-construction, product, harmonic, exact-symbolic, and Lean
routes were maintained explicitly and adversarially cross-checked.

## 2. Candidate-audit correction

An earlier Prompt 2 candidate on
`agent/afp-quadratic-covariance-p2` contained much of the required theorem
package and had a green dedicated workflow. It was not accepted unchanged for
two reasons:

1. it descended from the obsolete Prompt 1 head rather than corrected commit
   `923dc47...`; and
2. it treated the covariance-constraint and sampling maps as generic unrelated
   maps.

The second issue was mathematical rather than stylistic. In the spherical
quadratic problem,

```text
R_X = (L+2d I) S_X.
```

Therefore

```text
K_X = ker S_X subset ker R_X = E_form.
```

The generic restriction formula

```text
dim E_sample
  = dim E_form - dim(E_form intersect K_X)
```

remains correct, but the intersection is automatically `K_X` here. The sharp
specialized formulas are

```text
dim E_sample = dim E_form-dim K_X,
dim E_sample = rank(S_X)-rank(R_X),
rank([R;S]) = rank(S).
```

The corrected exact audit tests this factorization directly and no longer uses
an unrelated-map example as a negative test against the specialized formula.

## 3. Mathematical result

The paper-style proof is
`pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`.

### 3.1 Covariance and shifted residual

For a finite coordinate eigenmap,

```text
L(Phi^T A Phi)(i)
  = -2 lambda Phi_i^T A Phi_i + tr(A^T C_i).
```

For `q_{A,c}=Phi^T A Phi-c` with target eigenvalue `-mu`, exactness is
equivalent to

```text
tr(A^T C_i)
  + (mu-2 lambda) Phi_i^T A Phi_i
  - mu c = 0
```

at every state. No positivity or reversibility is required for this algebra.
The admissible shift is treated separately from trace-freeness because a
trace-free quadratic may have nonzero mean on a finite sample.

For the sphere coordinate eigenmap,

```text
lambda=d-1,
mu=2d,
A in Sym_0(d),
M_i=P_0(C_i+2 Phi_i Phi_i^T).
```

The zero-centered form space is

```text
E_form = span{M_i}^perp.
```

### 3.2 Genuine sampled exactness

The quadratic sampling map and residual map are

```text
S_X(A)_i = Phi_i^T A Phi_i,
R_X(A)_i = <A,M_i>_F.
```

The exact factorization gives

```text
R_X=(L+2dI)S_X,
K_X subset E_form,
E_sample=S_X(E_form)
        =im(S_X) intersect ker(L+2dI).
```

Thus every later dimension claim concerns sampled functions, not only
algebraic forms. The exact dimension formulas are

```text
dim E_sample
  = dim E_form-dim(E_form intersect K_X)
  = dim E_form-dim K_X
  = rank(S_X)-rank(R_X).
```

### 3.3 Sharp axial-covariance rigidity

If every local covariance has the radial/tangential form

```text
C_i=tau_i(I-Phi_i Phi_i^T)
    +beta_i Phi_i Phi_i^T,
beta_i>0,
```

then

```text
M_i=d beta_i/(d-1)
    (Phi_i Phi_i^T-I/d).
```

Every constraint row is therefore a positive scaling of the corresponding
sampling row. Consequently

```text
E_form=K_X,
E_sample={0}.
```

This is the principal sharp theorem. It improves on rank bookkeeping and is
meaningful for arbitrary finite positive eigenmap generators. The local
version forces vanishing only at vertices satisfying axial covariance; the
global conclusion requires the hypothesis at every state.

### 3.4 Equality and independent rigidity mechanisms

A regular simplex in every dimension attains the axial theorem. With complete
edge rate `(d-1)/(d+1)`, its sampling rank is exactly `d` and

```text
dim E_form=dim K_X=d(d+1)/2-1-d,
dim E_sample=0.
```

A second theorem assumes a transitive equivariant eigenmap and irreducibility
of `Sym_0(d)` under conjugation. The exact-form kernel is then zero or the full
module. Positive radial covariance excludes the full alternative, giving
`E_form={0}`. This route is independent of axial row scaling.

### 3.5 Exact Platonic examples

For a shortest-edge Platonic generator with adjacent inner product `alpha`,

```text
C_i=(1+alpha)I+(1-3alpha)Phi_i Phi_i^T,
M_i=3(1-alpha)(Phi_i Phi_i^T-I/3).
```

Exact rational and `Q(sqrt(5))` calculations give:

| Graph | rank `R_X` | rank `S_X` | dim `E_form` | dim `K_X` | dim `E_sample` |
|---|---:|---:|---:|---:|---:|
| tetrahedron | 3 | 3 | 2 | 2 | 0 |
| octahedron | 2 | 2 | 3 | 3 | 0 |
| cube | 3 | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 5 | 0 | 0 | 0 |

The tetrahedral and cubical kernels are diagonal trace-free forms; the
octahedral kernel is the off-diagonal subspace. The icosahedral and
dodecahedral evaluation determinants are exactly

```text
32(11+5 sqrt(5))
```

and

```text
-192.
```

The first three apparent algebraic exact spaces are entirely sampling kernel.
None of the five graphs has a nonzero sampled degree-two mode with eigenvalue
`-6`.

### 3.6 Signed restoration

On the four cardinal points of `S^1`, adjacent rates `1` and antipodal rates
`-1/2` give a symmetric conservative generator satisfying

```text
Lx=-x,
Ly=-y,
L(x^2-y^2)=-4(x^2-y^2).
```

At each row the coordinate and quadratic equations uniquely force
`(1,-1/2,1)`. The negative antipodal magnitude `1/2` is therefore sharp on
this fixed node/support problem; the total negative undirected mass is one.

### 3.7 Independent product obstructions

The carré-du-champ proof shows that additive exact product propagation forces
`Gamma(f,g)=0`; aligned strict extrema and a positive changing edge contradict
this. For a square, zero carré du champ makes the sampled function constant on
every positive active edge.

The independent semigroup proof uses

```text
P_t(f^2)>=(P_t f)^2.
```

If the square propagated at the additive eigenvalue, equality would hold.
Strict convexity characterizes equality as constancy on the transition
support, and uniformization identifies that support with the reachable set.
An irreducible positive chain and positive eigenvalue therefore admit no
nonzero additive exact sampled square.

### 3.8 Hierarchy decision

The bounded search handles even product parity, odd/even zonal antipodal
sets, non-singleton maxima, degree-specific sampling kernels, cross-degree
aliases, and the difference between one sampled combination and a complete
irreducible component.

The resonance equation

```text
k(k+d-2)=2l(l+d-2)
```

is Pell-type and can have infinite arithmetic families. Resonance alone does
not isolate a sampled component or eliminate other product terms. Whenever
additional assumptions do isolate the sampled square, the conclusion reduces
to the same one-function carré-du-champ/Jensen obstruction. No new
`l`-indexed dimension tradeoff or global consequence survives.

The general spectral-product hierarchy is therefore `REJECTED` for Prompt 2
under its kill criterion. This does not rule out future theorems under stronger
design or association-scheme hypotheses.

## 4. Approach registry

| Approach family | Outcome |
|---|---|
| Direct coordinate expansion | Adopted for the finite covariance identity |
| Abstract carré-du-champ expansion | Adopted independently for the product obstruction and as a check on the coordinate proof |
| Form-space rank only | Blocked because it ignores sampling aliases |
| Generic unrelated constraint/sampling maps | Rejected for the specialized problem after discovering `R_X=(L+2dI)S_X` |
| Residual-through-sampling factorization | Adopted as the central sampled-space correction |
| Assume sampling injective | Rejected by tetrahedral, octahedral, and cubical kernels |
| Local covariance matrix rank alone | Redirected; it did not give a sharp sampled conclusion |
| Axial stabilizer symmetry | Adopted to reduce covariance to radial/tangential scalars |
| Axial row scaling | Adopted as the principal sharp theorem |
| Regular-simplex family | Adopted as the all-dimensional equality construction |
| Transitive representation irreducibility | Adopted as an independent rigidity theorem |
| Symmetry without exact tensor/module analysis | Blocked |
| Floating Platonic ranks | Replaced by exact algebraic arithmetic and determinant witnesses |
| Association-scheme intersection numbers | Retained as a future extension, not assumed here |
| Spherical-design averaging | Used only for shifted-constant exclusion in symmetric examples |
| Unconstrained signed solve | Rejected as insufficient |
| Fixed-support signed row equations | Adopted; the negative rate is forced |
| Strict-extremum carré du champ | Adopted as first product obstruction |
| Markov semigroup/Jensen equality | Adopted as independent second proof |
| Harmonic parity/Fischer bookkeeping | Adopted as an identifiability audit, not as the main theorem |
| Bounded resonance enumeration | Retained as exact falsification only |
| Pell resonance as hierarchy | Rejected; arithmetic gives no sampled dimension theorem |
| Full abstract representation formalization in Lean | Deferred to avoid replacing a transparent ordinary proof with a large library project |
| Narrow finite Lean core | Adopted for covariance, factorization, projection, restricted rank-nullity, and axial consequences |

## 5. Adversarial audit

The package was checked against the required failure modes:

- nonzero matrices are not identified with nonzero sampled functions;
- form-space dimension is never reported as sampled-space dimension;
- the residual and sampling matrices are not treated as unrelated;
- every sampling alias is recognized as an exact zero function;
- no theorem assumes sampling injectivity;
- local axial exactness is not promoted globally without a vertexwise
  hypothesis;
- disconnected and directed generators are distinguished from irreducible
  chains in product arguments;
- semigroup equality uses the exact reachable support;
- even zonal modes are not assigned singleton maxima;
- odd antipodal signs are distinguished from the square's equality set;
- algebraic harmonic components are not assumed nonzero after sampling;
- one sampled combination is not promoted to a complete irreducible component;
- signed rates are checked for conservation, coordinate modes, quadratic mode,
  symmetry, and forced sign pattern;
- golden-ratio ranks use exact algebraic arithmetic;
- no equal-weight or reversibility hypothesis is hidden in the covariance
  identity;
- positivity and a distinct active jump are explicit in radial-covariance
  rigidity; and
- workflow counts and hashes remain provenance rather than mathematical
  evidence.

## 6. Files and formalization boundary

Primary files:

- theorem:
  `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`;
- derivation summary:
  `pure_math/covariance/QUADRATIC_COVARIANCE_DERIVATION.md`;
- exact symbolic audit:
  `pure_math/covariance/quadratic_covariance_audit.py`;
- Lean finite algebra:
  `AFPBarrier/QuadraticCovariance.lean`;
- theorem map:
  `docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md`.

Lean formalizes:

- finite product and covariance identities;
- shifted target equivalence;
- trace-free projection contraction;
- rank-nullity for sampling restricted to the exact-form subspace;
- sampling-kernel inclusion under residual factorization;
- equality of the sampled exact range with `range S intersect ker B`;
- row-scaled constraint/sample equivalence; and
- the axial trace coefficient.

The semigroup equality theorem, Markov uniformization, spherical harmonic
product decomposition, and real representation irreducibility remain clearly
identified standard external inputs. No `sorry`, `admit`, `sorryAx`, or
user-declared axioms are permitted.

## 7. Prior-art and publication boundary

The prior-art map covers finite Markov generators and product calculus,
positive stencils, discrete spherical eigenmaps, spherical designs, quadratic
harmonic sampling, distance-regular and Q-polynomial association schemes,
local covariance tensors, and signed Laplacian inverse problems.

Standard inputs include covariance expansion, finite rank-nullity, carré du
champ, Jensen, uniformization, harmonic parity/decomposition, and general
representation irreducibility. The candidate contribution is the combined
genuinely sampled covariance factorization, sharp axial/equivariant rigidity,
regular-simplex equality family, exact aliasing classifications, and forced
signed restoration.

## 8. Acceptance gate

Prompt 2 is accepted only after an exact implementation head passes:

1. exact symbolic covariance, factorization, Platonic, signed, and resonance
   regressions;
2. rejection of proof placeholders and user axioms;
3. full Lean 4.30 / Mathlib 4.30 build;
4. focused pure-math axiom audit; and
5. independent nanoda checking of all selected Prompt 2 declarations,
   including the new factorization theorems.

Workflow, job, accepted-head, PR, merge, and post-integration identifiers are
recorded after the gate completes rather than being used as mathematical
support.
