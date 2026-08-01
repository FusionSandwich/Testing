# Prompt 2 stage report — sampled quadratic covariance and spectral products

## 1. Baseline and scope

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Prompt 1 closeout head used as the actual working baseline:
  `d3c64f73805392752696996c10d58cf26a6354f0`
- Original P0/M1 checkpoint named in Prompt 2:
  `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Isolated Prompt 2 branch: `agent/afp-quadratic-covariance-p2`
- Frozen transport archive:
  `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

The target branch had advanced through the completed Prompt 1 package, so this
stage starts from its verified closeout head rather than discarding those
changes. The Prompt 2 diff is limited to the pure-mathematics covariance
package, Lean finite algebra, exact symbolic regressions, proof-control
documents, and a dedicated workflow. It does not modify the immutable archive
or introduce transport, Radiant, HTS, multigroup, or spatial-solver work.

A literal multiagent-v2 runtime was not exposed in this execution environment.
It was not used and is not claimed. Independent approach families and
adversarial passes were maintained explicitly as described below.

## 2. Mathematical result

The paper-style proof is
`pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`.

### 2.1 Covariance and target residual

For a finite generator and coordinate eigenmap,

```text
L(Phi^T A Phi)(i)
  = -2 lambda Phi_i^T A Phi_i + tr(A^T C_i).
```

For a shifted target mode `Phi^T A Phi-c` with eigenvalue `-mu`, exactness is
equivalent to

```text
tr(A^T C_i)
  + (mu-2 lambda) Phi_i^T A Phi_i
  - mu c = 0
```

at every state. The proof is a coordinatewise finite product expansion and
requires neither positivity nor reversibility.

For the coordinate eigenmap on `S^(d-1)`, target degree two, and trace-free
symmetric forms, the zero-centered form space is

```text
E_form = span{P_0(C_i+2 Phi_i Phi_i^T)}^perp.
```

The shifted form condition is recorded separately; zero-centering is not
silently inferred from matrix trace-freeness on an arbitrary sample.

### 2.2 Sampling correction

The quadratic sampling map is

```text
S_X(A)_i = Phi_i^T A Phi_i,
K_X = ker S_X.
```

The genuine sampled exact space is

```text
E_sample = S_X(E_form),
```

not `E_form` itself. Therefore

```text
dim E_sample
  = dim E_form - dim(E_form intersect K_X).
```

For covariance-constraint matrix `R` and sampling matrix `S`,

```text
dim E_sample = rank([R;S]) - rank(R).
```

The exact audit includes a deliberately chosen matrix pair for which the
incorrect subtraction `dim E_form-dim K_X` returns zero while the true sampled
image dimension is one.

### 2.3 Sharp axial-covariance rigidity

If every local covariance has the radial/tangential form

```text
C_i = tau_i(I-Phi_i Phi_i^T)
      + beta_i Phi_i Phi_i^T
```

with `beta_i>0`, then

```text
M_i = d beta_i/(d-1)
      (Phi_i Phi_i^T-I/d).
```

Each covariance constraint is therefore a positive row scaling of the
corresponding quadratic sampling functional. It follows that

```text
E_form = K_X,
E_sample = {0}.
```

This is the principal sharp theorem. It improves on rank bookkeeping and is
meaningful for any finite positive eigenmap generator, independent of AFP
terminology. The local version forces an exact quadratic sample to vanish only
at vertices where axial isotropy holds; the global theorem needs the
hypothesis at every vertex.

### 2.4 Equality and independent rigidity mechanisms

A regular simplex in every dimension attains the theorem sharply. With rate
`(d-1)/(d+1)` on every complete-graph edge, its sampling rank is exactly `d`,
its form space has dimension

```text
d(d+1)/2 - 1 - d,
```

and that entire nonzero form space is sampling kernel.

A second theorem assumes a transitive equivariant eigenmap and irreducibility
of `Sym_0(d)` under conjugation. The exact-form kernel is then either zero or
the full module. Positivity and positive radial covariance exclude the full
alternative, so `E_form={0}`. This route is independent of axial row scaling.

### 2.5 Exact Platonic examples

For every shortest-edge Platonic generator, vertex-stabilizer symmetry makes
the covariance axially isotropic. If `alpha` is the adjacent inner product,

```text
C_i = (1+alpha)I + (1-3 alpha) Phi_i Phi_i^T,
M_i = 3(1-alpha)(Phi_i Phi_i^T-I/3).
```

Exact arithmetic over `Q(sqrt(5))` gives:

| Graph | rank span `M_i` | dim `E_form` | dim `K_X` | dim `E_sample` |
|---|---:|---:|---:|---:|
| tetrahedron | 3 | 2 | 2 | 0 |
| octahedron | 2 | 3 | 3 | 0 |
| cube | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 0 | 0 | 0 |

For the tetrahedron and cube, the diagonal trace-free forms are the sampling
kernel. For the octahedron, the off-diagonal forms are the sampling kernel.
The icosahedral and dodecahedral evaluation matrices have exact nonzero
five-by-five determinants

```text
32(11+5 sqrt(5))
```

and

```text
-192,
```

respectively. The exact audit also verifies zero first moments and

```text
sum_i Phi_i Phi_i^T = |I| I/3
```

for all five embeddings, so the shifted trace-free constant case is checked
without numerical design recognition.

### 2.6 Signed restoration

On the four cardinal points of `S^1`, rates one to both adjacent points and
rate `-1/2` to the antipode give a symmetric conservative matrix with

```text
Lx=-x,
Ly=-y,
L(x^2-y^2)=-4(x^2-y^2).
```

The two coordinate equations and the prescribed quadratic equation force the
rates `(1,-1/2,1)` in every row. Thus the sign violation is not merely one
unconstrained solution: on this fixed node/support problem every solution has
negative antipodal magnitude `1/2` per row, or total negative undirected mass
one.

### 2.7 Product obstruction and hierarchy decision

The carré-du-champ proof shows that additive exact product propagation forces
`Gamma(f,g)=0`. At aligned strict extrema positivity contradicts this. For a
square, zero carré du champ forces equality of the sampled function on every
positive active edge.

The semigroup proof independently uses

```text
P_t(f^2) >= (P_t f)^2.
```

Equality is characterized exactly by constancy on the support of the
transition measure, which for a finite continuous-time chain is the reachable
set. An irreducible positive chain and a positive eigenvalue therefore admit
no nonzero additive exact square.

The spherical-product audit distinguishes algebraic harmonic components from
sampled functions, accounts for even product parity, odd/even zonal antipodal
sets, non-singleton maxima, sampling kernels, and cross-degree aliases. The
additive-resonance equation is Pell-type and can possess sparse arithmetic
families. Those resonances do not identify a sampled component or produce a
dimension tradeoff. Every usable argument still reduces to the one-function
sampled-square obstruction.

The proposed general spectral-product hierarchy is therefore `REJECTED` for
Prompt 2 under its kill criterion. This is not a universal impossibility claim
under all future design or association-scheme hypotheses.

## 3. Approach registry

| Approach family | Outcome |
|---|---|
| Direct coordinate expansion | Adopted for the finite covariance identity |
| Abstract carré-du-champ expansion | Adopted independently for product obstruction and as a check on the coordinate proof |
| Form-space rank only | Blocked because it ignores the sampling kernel |
| Sampling-map restriction and stacked rank | Adopted for the exact genuine sampled dimension |
| Assume sampling injective | Rejected by tetrahedral, octahedral, and cubical kernels |
| Local covariance rank bound | Redirected; covariance matrix rank alone did not give a sharp global sampled conclusion |
| Axial stabilizer symmetry | Adopted; reduces every local covariance to radial/tangential scalars |
| Axial constraint-to-sampling row scaling | Adopted as the principal sharp theorem |
| Regular-simplex design family | Adopted as the all-dimensional equality construction |
| Transitive representation irreducibility | Adopted as an independent global rigidity theorem |
| Symmetry without exact module analysis | Blocked; no claim is accepted from numerical orbit intuition alone |
| Floating Platonic ranks | Replaced by exact symbolic algebra and determinant certificates |
| Association-scheme intersection numbers | Retained as a future generalization; not needed for the current theorem |
| Spherical-design averaging | Used only to rule out shifted nonzero constants in symmetric examples |
| Unconstrained signed linear solve | Rejected as insufficient |
| Fixed-support signed row equations | Adopted; proves the negative rate is forced |
| Strict-extremum carré-du-champ proof | Adopted as first product obstruction |
| Markov semigroup/Jensen equality | Adopted as conceptually independent second proof |
| Harmonic parity/Clebsch–Gordan bookkeeping | Adopted as an identifiability audit, not the main theorem |
| Bounded resonance enumeration | Retained as falsification only |
| Arithmetic resonance as a hierarchy | Rejected; resonance alone gives no sampled component or dimension theorem |
| Immediate full representation formalization in Lean | Deferred to avoid replacing a transparent finite proof by a large library project |
| Narrow finite Lean core | Adopted for covariance algebra, target residual, projection, restricted-map rank-nullity, and row-scaling consequences |

## 4. Adversarial audit

The final package was tested against the failure modes specified in Prompt 2:

- form-space dimension is never reported as sampled-space dimension;
- every rank formula contains the intersection or stacked matrix needed for
  the restricted sampling map;
- no theorem assumes sampling injectivity;
- algebraically nonzero forms in the Platonic kernels are exhibited exactly;
- local axial exactness is not promoted to global exactness without a
  vertexwise hypothesis;
- disconnected and directed generators are distinguished from irreducible
  positive chains in the product obstruction;
- the semigroup equality statement uses the exact reachable support;
- even zonal modes are not assigned a singleton maximizing set;
- odd zonal antipodes with opposite signs are treated separately from the
  square's equality set;
- algebraic harmonic components are not assumed nonzero after sampling;
- one sampled combination is not promoted to a complete irreducible
  component;
- the signed generator is checked for conservation, coordinate eigenmodes,
  quadratic eigenmode, symmetry, and sign pattern;
- the negative rate is obtained from exact local equations rather than an
  opaque solver output;
- Platonic `sqrt(5)` ranks use exact algebraic arithmetic;
- no equal-weight or reversibility assumption is hidden in the general
  covariance identity;
- axial rigidity states positivity and distinct-jump radial covariance
  explicitly; and
- CI/provenance data are kept outside the mathematical proof.

## 5. Exact verification files

- Ordinary theorem:
  `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`
- Corrected derivation summary:
  `pure_math/covariance/QUADRATIC_COVARIANCE_DERIVATION.md`
- Exact symbolic audit:
  `pure_math/covariance/quadratic_covariance_audit.py`
- Lean finite algebra:
  `AFPBarrier/QuadraticCovariance.lean`
- Theorem map:
  `docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md`

The symbolic audit is a deterministic falsification and regression tool. It is
not used as the proof of the general axial theorem.

## 6. Prior-art and publication boundary

The prior-art update covers Markov diffusion generators and products of
eigenspaces, finite weighted-Laplacian inverse problems, discrete eigenmaps,
spherical designs, harmonic-index designs, graphical designs, distance-regular
graphs, Q-polynomial association schemes, and quadratic harmonic sampling.

Standard inputs include covariance expansion, rank-nullity, carré du champ,
Jensen, Markov uniformization, harmonic parity/decomposition, and general
representation irreducibility. The publication contribution is not any one of
those inputs. It is the combined genuinely sampled covariance theorem, sharp
axial and equivariant rigidity, exact equality family, exact sampling-kernel
examples, and forced signed restoration.

## 7. Formalization boundary

Lean formalizes:

- the finite product identity;
- scalar and finite-sum compatibility of the jump generator;
- the coordinate covariance identity;
- the shifted target-eigenvalue equivalence;
- finite matrix trace and contraction;
- invariance of trace-free contraction under scalar-diagonal subtraction;
- the trace-free projection consequence;
- rank-nullity for the sampling map restricted to an exact-form subspace;
- equivalence of zero constraints and zero samples under nonzero row scaling;
  and
- the scalar coefficient forced by axial trace balance.

The semigroup/Jensen equality theorem and abstract real representation theory
remain precisely stated ordinary inputs. No `sorry`, `admit`, `sorryAx`, or
user-declared axioms are permitted.

## 8. Acceptance rule

Prompt 2 is accepted only after the exact implementation head passes:

1. the exact symbolic covariance and sampled-space regression;
2. source rejection of proof placeholders and user axioms;
3. the full Lean 4.30 / Mathlib 4.30 build;
4. the focused axiom audit; and
5. independent nanoda kernel checking of all selected Prompt 2 Lean
   declarations.

Concrete workflow, job, accepted-head, merge, and post-integration identifiers
are recorded in the pull request and final provenance record rather than
hard-coded before the gate completes.
