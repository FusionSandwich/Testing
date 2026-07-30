# Publication assessment and forward gate plan

**Assessment date:** 2026-07-30  
**Current mathematical baseline:** Gate 3 final commit `74574c13e0f4d0a2e1e66742da3c7ade16a962a6`

## 1. Is the Gate 1–3 package publishable now?

### Defensible answer

The existing package is potentially publishable as a short mathematical or
transport-methods note, but it is not yet the strongest paper that this project
can support.

The following pieces are substantive:

1. an AFP-specific no-go theorem showing that a finite conservative monotone
   jump discretization cannot preserve the complete degree-one and degree-two
   spherical-harmonic eigenspaces simultaneously;
2. the exact carré-du-champ expression for the unavoidable degree-two defect;
3. the sharp defect–stiffness inequality;
4. an explicit all-order equal-angle family that is positive, reversible, and
   exactly degree-one preserving;
5. a proved `Theta(N^-2)` defect and `Theta(N^4)` polar-rate barrier;
6. Lean and independent deterministic verification.

However, the general carré-du-champ mechanism is standard finite Markov-
generator mathematics. In addition, positive spherical Laplacians with exact
`-2` modes are now part of the discrete differential-geometry literature.
Formal verification improves reliability but is not, by itself, sufficient
novelty.

The current material is therefore best viewed as the first half of a stronger
paper rather than the final submission package.

## 2. Prior-art boundary that must be stated explicitly

### AFP literature

Bienvenue, Naceur, Carrier, and Hébert construct a flexible monotone
multidimensional AFP discretization preserving the null mode and degree-one
moments. Their paper motivates the quadrature-compatibility question but does
not, in the sources audited so far, state the complete degree-two no-go theorem
or the exact defect–stiffness theory.

- DOI: <https://doi.org/10.1080/00295639.2025.2462891>
- Open record: <https://publications.polymtl.ca/64454/>

### Discrete spherical Laplacians

Izmestiev and Lam construct a positive spherical Delaunay Laplacian and prove
exact `-2` eigenfunctions linked to discrete conformal geometry and inscribed
polyhedra. This is important prior art for the quasi-uniform continuation.

- DOI: <https://doi.org/10.1112/jlms.70235>
- Preprint: <https://arxiv.org/abs/2408.04877>

The transport contribution must therefore not be described as the invention of
positive spherical Laplacians. The candidate contribution is instead:

- the AFP interpretation;
- the degree-two impossibility and exact defect formula;
- sharp local loss-window bounds connecting angular geometry to stiffness;
- a comparison between polar product grids and quasi-uniform spherical graphs;
- transport consequences and implementation guidance.

### Quasi-uniform icosahedral grids

Almost-uniform icosahedral sphere refinements and their numerical value are
classical. Relevant examples include:

- Baumgardner and Frederickson, *Icosahedral Discretization of the Two-Sphere*,
  SIAM J. Numer. Anal., DOI: <https://doi.org/10.1137/0722066>;
- Bobenko and Springborn, *A discrete Laplace–Beltrami operator for simplicial
  surfaces*, <https://arxiv.org/abs/math/0503219>.

The novelty is not the mesh alone. It is the exact AFP moment structure and the
proved error–stiffness consequences.

## 3. Publication recommendation

### Minimum credible short paper

A short paper could be submitted after a specialist confirms that the explicit
AFP no-go statement is not already present. It would contain Gates 1–3 and be
positioned as a theorem note.

This route is publishable but leaves the obvious criticism that the only
explicit family has an artificial `Theta(N^4)` polar stiffness.

### Recommended full paper

The recommended paper should include Gates 1–5:

1. no-go theorem and defect identity;
2. exact loss-window rate/defect bounds;
3. the equal-angle family and polar barrier;
4. a quasi-uniform positive family with `Theta(h^-2)` rate and `Theta(h^2)`
   defect;
5. deterministic transport or angular-diffusion benchmarks comparing the two
   families and the existing AFP construction.

That produces a complete narrative:

> exact degree two is impossible; the unavoidable error is controlled by edge
> geometry; a product grid pays a quartic polar penalty; a quasi-uniform graph
> attains the geometrically optimal quadratic stiffness scale.

## 4. Forward gates

## Gate 4 — Quasi-uniform mathematical construction

**Goal:** construct and verify a positive, reversible, exactly degree-one AFP
operator with

```text
maximum defect = Theta(h^2)
maximum rate   = Theta(h^-2).
```

### Gate 4A: generic local theorem

For a normalized zonal mode, let

```text
ell_ij = 1 - Omega_i dot Omega_j.
```

If every active loss lies in `[ell_min, ell_max]`, prove

```text
ell_min * r_i <= 2 <= ell_max * r_i,
2 ell_min <= epsilon_i <= 2 ell_max.
```

This is formalized in `AFPBarrier/QuasiUniformLossBounds.lean` in generic
eigenvalue form.

### Gate 4B: deterministic candidate family

Use radially refined icosahedra with the positive spherical Delaunay Laplacian
of Izmestiev–Lam. Check every edge and vertex for:

- Delaunay positivity;
- positive vertex masses;
- all three coordinate eigenrelations;
- exact defect identity;
- generic loss-window bounds;
- quasi-uniform edge ratios;
- `h^2` defect and `h^-2` rate scaling.

The first implementation is
`gate4/icosphere_spherical_laplacian_audit.py`.

### Gate 4C: all-order family proof

Close the remaining non-computational steps:

1. prove that the selected radial icosahedral refinement is spherical Delaunay
   at every level, or specify a deterministic Delaunay-retriangulation rule;
2. prove uniform edge-length ratio bounds;
3. transfer the Izmestiev–Lam exact `-2` coordinate result into the AFP matrix
   convention;
4. combine those facts with the Lean loss-window theorem to obtain explicit
   all-order constants.

## Gate 5 — Optimality and comparison

**Goal:** show that `Theta(h^-2)` is not merely observed but geometrically
optimal for local monotone degree-one-exact schemes.

Targets:

1. derive lower rate bounds from the largest permitted edge loss;
2. characterize equality or near-equality cases;
3. compare the quasi-uniform construction against the defect-minimizing LP;
4. quantify sparsity, condition number, and spectral distortion beyond degree
   one.

## Gate 6 — Applied transport validation

**Goal:** demonstrate that the mathematical quantities predict actual BFP/AFP
behavior.

Benchmarks should include:

- pure angular diffusion with known spherical-harmonic decay;
- forward-peaked charged-particle scattering;
- a material-interface or energy-loss case relevant to Charles Bienvenue's
  work;
- comparisons with Radiant's current pseudoinverse coefficients.

Metrics:

- positivity;
- degree-one preservation;
- degree-two decay error;
- time-step or iterative stiffness;
- rotational bias;
- deposited-energy error;
- cost at equal accuracy.

## Gate 7 — Submission qualification

1. complete specialist priority review;
2. freeze theorem statements and terminology;
3. separate proved results from deterministic evidence;
4. package Lean, scripts, manifests, and CI artifacts;
5. prepare the journal manuscript and reproducibility appendix.

## 5. Current decision

Do not discard Gates 1–3. They are useful and likely form a publishable core.
The strongest publication path is to add the Gate 4 quasi-uniform theorem and
at least one Gate 6 transport benchmark before submission.
