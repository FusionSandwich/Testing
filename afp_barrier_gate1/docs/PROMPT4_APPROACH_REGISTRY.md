# Prompt 4 approach and adversarial registry

## 1. Runtime boundary

A literal multiagent-v2 runtime is not exposed in this environment. It was not
used and is not claimed. The stage instead maintains independent ordinary
proof, exact-symbolic, formalization, duality, compactness, prior-art, and
adversarial routes. Agreement between routes is recorded only after the exact
equations and hypotheses agree.

Prompt 4 starts from:

```text
repository: FusionSandwich/Testing
target:     agent/afp-pure-math-p0-m1
baseline:   47ef59b0463ecd4bd7a18a3301f29b14f9777c20
development branch:
    agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis
```

The separate Prompt 3 integration-record branch and PR #23 are not modified.
The immutable transport archive remains
`515f1aae6c20bd85711c90b5c1c21b4905252d01`.

## 2. Mandatory approach families

| Route | Initial question | Outcome | Status |
|---|---|---|---|
| A. Mittag--Leffler asymptotics | Can the exact polar coefficients be given a uniform all-orders remainder? | Paired cotangent partial fractions give a positive tail and explicit `N>=2` bounds | ACCEPTED |
| B. Direct polar coordinate balance | Is the quartic rate an artifact of the chosen conductances? | The three local coordinate equations force all three polar rates uniquely | ACCEPTED / SHARP |
| C. Ring-symmetry averaging | Can an optimizer be symmetrized without increasing `r_max`? | Unneeded; Route B proves uniqueness before any averaging. No symmetry assumption is used | BLOCKED AS REDUNDANT |
| D. Cut/flow duality | Can a polar cut produce a quartic lower bound? | Gives weaker moment bounds than the exact local solve | BLOCKED AS NONSHARP |
| E. Rate-capped extremal compactness | Can the asymptotic quantity be made nondegenerate? | Separation, covering, degree, locality, mass, reversibility, and rate constraints give a compact finite-`K` class and `C*>=4/R` | ACCEPTED |
| F. Feasible-cone anisotropy | Can geometry constrain `Q` without pretending conductances are predetermined? | Projectivization plus mean-loss slicing gives a finite LP and exact dual certificate | ACCEPTED / SHARP |
| G. Delsarte/Gegenbauer | Is there a stronger global sampled-quadratic or valence certificate? | No new certificate survived sampling aliases; only standard LP reductions remained | BLOCKED |
| H. Bakry--Émery `Gamma_2` | Does the product algebra imply curvature rigidity? | The eigenfunction identity reduces to centered resonance on one function and gives no full `CD` theorem | KILLED |
| I. Compact homogeneous spaces | Does a second homogeneous space strengthen the central result? | Not without substantial new representation theory | DEFERRED |
| J. Discrete transport metric | Does positivity imply continuum Wasserstein contraction? | No; a Maas/Erbar metric and separate curvature proof are required | DEFERRED |
| K. Reduced-ring graph | Can varying ring populations use one-to-one nearest-ring couplings? | Biregular incidence gives `p M_i=q M_{i+1}`; perfect matching forces equal populations | ACCEPTED FOR THE STATED CLASS |
| L. Formalization | Which statements materially support the paper? | Polar uniqueness, coefficient algebra, rate barriers, two-loss anisotropy, and incidence counts are formalized | ACCEPTED / BOUNDED |

## 3. Independent derivations

### 3.1 Asymptotic route

The proof does not use a fitted slope. It starts from the differentiated
cotangent partial fraction, expands each paired pole with nonnegative
coefficients, and bounds the entire tail. The exact symbolic audit independently
checks:

```text
csc^2 tail coefficient < 1/80,
rate remainder transfer constant < 1/12,
quality remainder transfer constant < 1/3.
```

Lean checks the coefficient extraction and substitution into `N`.

### 3.2 Graph-class route

At a polar vertex, the transverse equation forces equality of the two
azimuthal rates. The axial equation fixes the inward rate. The remaining
horizontal equation fixes the common azimuthal rate. This route is independent
of reversibility, mass equality, global symmetry, and optimization.

The existing reversible construction supplies sharpness after the lower bound
is proved. It is not used to infer the lower bound.

### 3.3 Extremal route

The finite class is closed only after every potential degeneracy is controlled:

- separation and covering exclude collapse and holes;
- degree and edge locality exclude dense nonlocal support;
- mass bounds exclude vanishing or exploding row normalization;
- a linear rate cap excludes arbitrary stiffness;
- graph choice is a finite union; and
- zero conductances are handled by deleting the corresponding support edge.

The lower bound `4/R` comes from the universal rate--defect product and is
independent of compactness. The compactness proof independently gives
finite-`K` minimizers.

### 3.4 Anisotropy route

The normalized feasible polytope is formed before any objective is optimized.
At a fixed mean loss, the second moment is a linear program. Its dual variables
correspond exactly to:

```text
normalization,
mean loss,
tangent balance.
```

This yields a valid certificate for every feasible row. The two-opposite-
direction example and the polar product cone provide sharp equality cases.

## 4. Adversarial audit catalogue

### A1. Asymmetric polar conductances

The polar proof permits distinct left and right rates. The transverse coordinate
equation forces them equal. A theorem that begins by assuming equality fails
the audit.

### A2. Nonreversible local rows

The polar lower bound remains valid without reversibility. Reversibility is
used only to define the graph class and exhibit the attaining construction.

### A3. Unequal masses

Rates are `gamma_ij/w_i`. The local balance solves the rates directly and does
not assume equal masses.

### A4. Formal series without a remainder

A series produced by SymPy is regression evidence only. Acceptance requires
the positive partial-fraction tail and the explicit `N>=2` inequalities.

### A5. Collapsing extremal configurations

The extremal class includes a separation lower bound and mesh-ratio control.
Removing either allows geometrically degenerate sequences and is not accepted.

### A6. Dense or nonlocal graph escape

Degree and edge-locality bounds are part of the definition. An extremal theorem
without them is not the Prompt 4 quantity.

### A7. Conductance reweighting of `Q`

`Q` is not treated as geometry-only. The cone theorem takes the infimum over
all tangent-balanced projective weights through a sliced LP.

### A8. Sampling aliases in Delsarte routes

Any harmonic LP certificate must first survive finite sampling kernels and
cross-degree aliases. No candidate did.

### A9. Positive-curvature graph examples

The blanket statement that finite positive graphs cannot satisfy useful
Bakry--Émery curvature bounds remains false. The `Gamma_2` branch is not
promoted from a one-function calculation.

### A10. Perfect matching versus split/merge reduced rings

The reduced-ring theorem applies only to biregular, and in particular
one-to-one, adjacent-ring couplings. It does not claim impossibility for more
general split/merge graphs.

### A11. Fixed radial connectivity claimed Delaunay at all levels

No such claim is made. Delaunay positivity and exact low modes remain external
unless separately verified for the actual connectivity.

### A12. Workflow and branch interference

All Prompt 4 changes are confined to the new Prompt 4 branch and a dedicated
PR. The target, Prompt 3 development branch, Prompt 3 integration-record
branch, and archive are not rewritten or force-pushed.

## 5. Kill criteria applied

A route is stopped when it:

- assumes ring symmetry before proving it;
- produces only a formal series or finite fitted slope;
- defines an unconstrained extremal quantity;
- treats solved conductances as node geometry;
- reduces to a standard Delsarte, curvature, or transport framework without a
  new certificate;
- ignores sampling kernels;
- omits the active coupling class from a reduced-ring claim; or
- requires a broad formal-geometry library unrelated to accepted theorems.

## 6. Publication-boundary audit

The central paper theorem remains meaningful after removing all project names:
it concerns genuine sampled quadratic eigenspaces of finite positive generators
with prescribed eigenmaps. The Prompt 4 product-grid result is supporting
sharp-barrier theory, and the extremal and anisotropy theorems delimit the
numerical-analysis consequences.

The package is not presented as new merely because it is Lean-checked. Standard
partial fractions, Cauchy--Schwarz, LP duality, compactness, spherical design
theory, curvature frameworks, and convex rigidity remain prior inputs.
