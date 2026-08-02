# Prompt 2 sampled quadratic covariance integration and closeout record

## 1. Original integration provenance

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Original P0/M1 checkpoint:
  `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Corrected Prompt 1 baseline:
  `923dc47dae4f83dbea9cd56aa904164c6378e52d`
- Prompt 2 theorem head before original reconciliation:
  `478055166fc874a519865506989586c3e02dc583`
- Prompt 2 merge into corrected Prompt 1 branch:
  PR `#17`, squash commit `f1cea9c13a3de28288470a53b67ad852aaa3635b`
- Prompt 1 plus Prompt 2 merge into the requested target:
  PR `#18`, squash commit `f9fb1e336a4569c2d7e2e440821976bd30a6c29f`
- Integration-record commit following that merge:
  `1835918fe9d0b941395e9f00f6ac5514129cefa0`

## 2. Corrected closeout provenance

At closeout start, the actual remote target head was

```text
1835918fe9d0b941395e9f00f6ac5514129cefa0.
```

The previously reported final target head

```text
694b913c99364bb0032a8ffbd7008b549b491af0
```

did not resolve as a remote commit. It is rejected as provenance and must not
be used as a Prompt 3 baseline.

The closeout branch was created without rewriting the target:

```text
agent/afp-pure-math-p2-closeout-corrected
```

from the actual target head `1835918...`.

The immutable archive remains

```text
archive/afp-gate6-spatial-multigroup-verified
515f1aae6c20bd85711c90b5c1c21b4905252d01.
```

## 3. Original sampled-space correction retained

The Prompt 2 covariance residual factors through sampling:

```text
R_X=(L+2dI)S_X.
```

Consequently

```text
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=dim E_form-dim K_X,
dim E_sample=rank(S_X)-rank(R_X),
rank([R_X;S_X])=rank(S_X).
```

This remains the central sampled-space theorem.

## 4. Closeout mathematical corrections

### 4.1 Equivariant positivity

The equivariant irreducibility theorem now requires

```text
a_ij>=0 for every i!=j.
```

With an equivariant unit-sphere coordinate eigenmap, transitivity,
irreducibility of the real conjugation representation on `Sym_0(d)`, and one
positive jump between distinct embedded points, this gives `E_form={0}`.
Reversibility is not required.

The signed regular pentagon is committed as the permanent exact counterexample
when global nonnegativity is removed:

```text
distance-one rate: (5+3sqrt(5))/10,
distance-two rate: (5-3sqrt(5))/10,
coordinate eigenvalue: -1,
trace-free quadratic eigenvalue: -4,
E_form=Sym_0(2),
dim E_sample=2,
real C_5 conjugation action irreducible.
```

### 4.2 Centered products

For eigenfunctions `Lf=-lambda f`, `Lg=-nu g`,

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

The Boolean square is the permanent positive centered-resonance regression.
Its semigroup variance is positive, so centered resonance is explicitly
separated from Jensen equality.

### 4.3 Low-degree hierarchy

The exact `S^2` table for `ell=1,...,6` is committed and has no additive
resonance. The generalized Pell analysis is retained. The general hierarchy is
rejected only because no sampled dimension tradeoff, multiplicity obstruction,
or new global consequence survived the kernel and alias audits.

## 5. Verification-policy correction

The dedicated Prompt 2 workflow now:

- asserts the literal expected head SHA and records the tree SHA;
- records the actual closeout start head/tree;
- verifies that the reported `694b913...` commit does not resolve;
- verifies the immutable archive SHA;
- runs existing and corrective exact audits;
- scans the aggregate Lean source for `sorry`, `admit`, and `sorryAx`;
- scans anchored declarations for both `axiom` and plural `axioms`;
- tests singular/plural regex fixtures and allowed nondeclaration text;
- performs the full Lean build and focused axiom audit;
- keeps `sorryAx` outside the nanoda permitted-axiom list;
- independently checks all selected Prompt 2 declarations with nanoda; and
- rejects out-of-scope closeout paths.

The repository-wide pure-math and spherical compatibility workflows also
assert literal head checkouts and use the aggregate singular/plural axiom
policy.

## 6. Scope preservation

The closeout diff is restricted to:

```text
.github/workflows/afp-quadratic-covariance.yml
.github/workflows/afp-pure-math.yml
.github/workflows/afp-spherical-feasibility.yml
afp_barrier_gate1/AFPBarrier.lean
afp_barrier_gate1/AFPBarrier/*.lean
afp_barrier_gate1/pure_math/**
afp_barrier_gate1/docs/**
```

No transport, Radiant, HTS, multigroup, evaluated-material, spatial-solver, or
production-solver path is permitted. The immutable archive is not merged,
rebased, or written.

## 7. Closeout integration fields

These fields are authoritative only after the closeout PR is merged and all
three workflows pass on the literal final target head:

```text
closeout_pr=19
closeout_implementation_head=TO_BE_RECORDED
closeout_merge_commit=TO_BE_RECORDED
final_target_head=TO_BE_RECORDED
final_target_tree=TO_BE_RECORDED
quadratic_workflow_run=TO_BE_RECORDED
quadratic_workflow_job=TO_BE_RECORDED
spherical_workflow_run=TO_BE_RECORDED
spherical_workflow_job=TO_BE_RECORDED
pure_math_workflow_run=TO_BE_RECORDED
pure_math_workflow_job=TO_BE_RECORDED
```

The final values are also copied into `PROMPT2_CLOSEOUT_AUDIT.md` and
`PROMPT3_READINESS_HANDOFF.md`.
