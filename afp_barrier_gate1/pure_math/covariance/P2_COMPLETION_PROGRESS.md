# Prompt 2 completion record

## Immutable baseline and branch

```text
repository=FusionSandwich/Testing
accepted_prompt1_commit=923dc47dae4f83dbea9cd56aa904164c6378e52d
accepted_prompt1_tree=906449c151fd97756a10fb83e7106a2e6ba39b0f
saved_prompt2_wip_commit=9cfacd0cb55b8f12f802beae86a4708f96ed7aa3
saved_prompt2_wip_tree=efeedbc492764a3ddc844ae7427961f84cbf4a6b
saved_prompt2_wip_parent=923dc47dae4f83dbea9cd56aa904164c6378e52d
completion_branch=agent/afp-pure-math-p2-quadratic-covariance-completion
immutable_transport_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

The commit and tree identifiers above were independently checked with Git.
Prompt 1 is identified by its immutable accepted commit and tree; the present
tip of any mutable Prompt-1 branch is not substituted for that checkpoint.
The completion delta is always audited against the literal Prompt-2 WIP commit
`9cfacd0cb55b8f12f802beae86a4708f96ed7aa3`.

## Correction accepted during completion

The unrestricted implication from pairwise-distinct harmonic degrees is
false. The exact rejected witness is

```text
d=1
I={*}
Phi(*)=+1 in S^0
L=0
D={0,1}
V_0=V_1=R^I
rank(V_0)+rank(V_1)=2>|I|=1
lambda_0=lambda_1=0
```

Accordingly, the completed theorem groups sampled spaces by equal target
eigenvalue. When one common operator has the prescribed scalar action on every
class, distinct target-class sums are internal and their dimensions obey the
rank bound. For spherical harmonics, distinct degrees give distinct
targets only when `d>=2`, because

\[
 \ell\longmapsto \ell(\ell+d-2)
\]

is then strictly increasing. In `d=1`, degrees are grouped by equal
`ell(ell-1)` target before any direct-sum or rank count.

The converse is constants-safe: `span{1}` is included exactly once in the
zero-target class. In the weighted-reversible version, constants must be
weighted-orthogonal to every nonzero-target class, in addition to the mutual
orthogonality of distinct nonconstant classes.

## Closure of the saved-checkpoint gaps

The initial WIP audit identified ten completion gaps. The candidate closes
them as follows.

| initial gap | completion evidence | state |
|---|---|---|
| weighted-reversible centering | ordinary proof plus `QuadraticCovariance.lean`, including zero-target center independence | closed |
| sphere residual and genuine sampled dimension | `QuadraticSphereResidual.lean` and the linear range/rank theorems in `QuadraticSampling.lean` | closed |
| signed one-shell factorization | ordinary proof and `OneShellQuadraticRigidity.lean` | closed |
| finite spectral direct-sum/rank theorem | corrected target-eigenvalue-class proof and `SpectralSamplingObstruction.lean` | closed |
| missing exact \(D_3\) counterexample | `exact_d3_invariance_counterexample.py` | closed |
| incomplete prism certificate | exact unit-shell, positivity, conservativity, reversibility, connectivity, transitivity, action, rank, minor, and anisotropy checks | closed |
| incomplete signed-cube certificate | exact ranks, aliases, 48 actions, orbit equations, invariant averaging, lower bound, optimizer, and KKT identities | closed |
| incomplete ordinary proofs | covariance theorem, derivation companion, and spectral-product analysis now state complete arguments and exact hypothesis boundaries | closed |
| unsynchronized claim control | theorem and approach registries, claim matrix, conjecture register, prior-art map, theorem-to-file map, and README synchronized | closed |
| no dedicated completion workflow | `.github/workflows/afp-prompt2-completion.yml` | closed |

The two easily hidden hypotheses are explicit throughout the synchronized
documents:

- the positive residual/rank obstruction needs a nonempty finite state set,
  `d>1`, nonnegative rates, unit nodes, and
  `L Phi = -(d-1) Phi`; and
- the signed one-shell theorem needs `d>1`, unit nodes with the same eigenmap
  equation, a nonempty noncoincident shell with `0<ell_i<2`, and the full
  signed tangent-moment identity.

## Completed theorem package

The ordinary proofs establish, under their stated hypotheses:

- the quadratic covariance identity and arbitrary target, including
  `mu=0`;
- weighted centering for a nonzero reversible target and the independence of
  the center at zero target;
- the sphere residual factorization, sampling quotient, and
  `rank(S)-rank(R)` genuine-dimension formula;
- the positive residual/Frobenius obstruction;
- signed one-shell full-tangent-isotropy rigidity `R_X=D S_X` under the
  nonempty-shell and `0<ell_i<2` hypotheses;
- the positive hexagonal-prism sharpness result;
- the multiplicity-free kernel formulas and quotient rank gap under invariant
  generator rates, and the corrected invariance theorem;
- the five-Platonic degree-two classification;
- signed-cube restoration with sharp undirected negative mass two;
- product resonance and the finite semigroup variance identity;
- the corrected common-operator target-eigenvalue-class sampling theorem and
  constants-safe converse; and
- the project-specific parity transfer and recurrence for the spherical Pell
  hierarchy.

The following inputs remain labeled EXTERNAL rather than being presented as
new project proofs: finite rank-nullity, real Maschke semisimplicity, the
self-adjoint spectral theorem, convex subgradient/KKT theory, finite
Markov-kernel Jensen equality and uniformization, the real spherical-harmonic
Clebsch--Gordan decomposition, and completeness of positive negative-Pell
solutions.

The unrestricted distinct-degree theorem in all dimensions, scalarity without
invariance, a universal positivity-only spectral hierarchy, and the blanket
positive-square obstruction are labeled REJECTED. Exact finite rank tables,
minors, polynomial aliases, group actions, and optimizer identities are
labeled COMPUTATIONAL unless an ordinary proof separately establishes the
general claim.

## Exact and formal support

The deterministic exact certificate set is:

```text
pure_math/covariance/exact_quadratic_covariance_audit.py
pure_math/covariance/exact_signed_restoration_audit.py
pure_math/covariance/exact_d3_invariance_counterexample.py
pure_math/spectral_products/exact_spectral_product_audit.py
```

The new or extended formal support is:

```text
AFPBarrier/QuadraticCovariance.lean
AFPBarrier/QuadraticSampling.lean
AFPBarrier/QuadraticSphereResidual.lean
AFPBarrier/OneShellQuadraticRigidity.lean
AFPBarrier/SpectralSamplingObstruction.lean
```

These Lean modules certify the finite algebraic core. Standard representation
theory, Markov Jensen theory, continuous spherical-harmonic decomposition, and
Pell completeness remain outside the formal kernel and retain their EXTERNAL
labels.

## Verification gate

The pinned candidate environment is Python 3.12, NumPy 2.3.2, SymPy 1.14.0,
and Lean/Mathlib 4.30.0. The dedicated workflow performs two independent jobs:

1. scope and whitespace audit against the exact WIP baseline, Python bytecode
   compilation, retained Prompt-1 regressions, and all exact Prompt-2
   certificates; and
2. the pinned Lean build, focused axiom audit, and source scan rejecting
   `sorry`, `admit`, `sorryAx`, and user-declared axioms.

Both jobs reject a dirty checkout after verification and upload logs, toolchain
records, hashes, and an exact source archive. A final commit identifier,
workflow run identifier, and green status belong in the immutable CI records;
they are not guessed in this source document before the integrated candidate
is committed and the remote workflow completes.

## Scope guard

This completion changes only the Prompt-2 pure-mathematics package, its Lean
algebraic support, exact certificates, claim-control documentation, and its
dedicated workflow. It does not redo Prompt 1, begin Prompt 3 triangulation or
near-rigidity, or alter transport, Radiant, HTS, multigroup, spatial-solver, or
evaluated-material work. The transport archive remains immutable.
