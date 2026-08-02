# Prompt 2 sampled quadratic covariance integration and closeout record

## 1. Original integration

```text
repository=FusionSandwich/Testing
target_branch=agent/afp-pure-math-p0-m1
original_checkpoint=4efef67a20cdb8b2437cad093ccc16bcd0f17796
corrected_prompt1_baseline=923dc47dae4f83dbea9cd56aa904164c6378e52d
prompt2_pr17_merge=f1cea9c13a3de28288470a53b67ad852aaa3635b
prompt1_prompt2_pr18_merge=f9fb1e336a4569c2d7e2e440821976bd30a6c29f
integration_record_commit=1835918fe9d0b941395e9f00f6ac5514129cefa0
```

## 2. Provenance correction

At corrective closeout start, the actual target was

```text
head=1835918fe9d0b941395e9f00f6ac5514129cefa0
tree=2f6678b1589e2561f6fc2cb44785f3c4989424b1.
```

The previously reported
`694b913c99364bb0032a8ffbd7008b549b491af0` did not resolve remotely and is
not an accepted baseline.

The immutable archive remained

```text
archive/afp-gate6-spatial-multigroup-verified
515f1aae6c20bd85711c90b5c1c21b4905252d01.
```

## 3. Corrective implementation and integration

```text
closeout_branch=agent/afp-pure-math-p2-closeout-corrected
closeout_pr=19
implementation_head=afb31139cacdf1bf252e86e890c4792a03df4796
implementation_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
closeout_merge_commit=dbe5d5db315d4e99b75c775c269827ac906b4fad
closeout_merge_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
```

The implementation was confined to the pure-math Lean package, exact
regressions, claim/provenance documents, and the three pure-math workflows. The
closeout-scope workflow rejected any path outside that allow-list.

## 4. Accepted mathematical corrections

### 4.1 Sampling theorem retained

```text
R_X=(L+2dI)S_X,
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

### 4.2 Equivariant theorem corrected

The irreducible equivariant theorem now requires every off-diagonal rate to be
nonnegative. Conservation fixes the diagonal; reversibility is not used. With
an equivariant unit-sphere coordinate eigenmap, irreducible real conjugation on
`Sym_0(d)`, and one positive distinct jump, `E_form={0}`.

The exact signed regular pentagon is the permanent counterexample when global
nonnegativity is omitted:

```text
u=(5+3sqrt(5))/10>0,
v=(5-3sqrt(5))/10<0,
L(x,y)=-(x,y),
L(cos2theta,sin2theta)=-4(cos2theta,sin2theta),
E_form=Sym_0(2),
dim E_sample=2,
real C_5 conjugation irreducible.
```

### 4.3 Centered products completed

For `Lf=-lambda f` and `Lg=-nu g`,

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

The Boolean four-state chain is the permanent positive centered-resonance
example. Its positive semigroup variance separates centered resonance from
Jensen equality.

### 4.4 Product hierarchy bounded correctly

The exact `S^2` `ell=1,...,6` table has no additive resonance. Generalized
higher-dimensional Pell resonances remain, but no sampled dimension tradeoff,
multiplicity obstruction, or new global consequence survived kernel and alias
audits. The hierarchy is rejected for Prompt 2 on that basis only.

### 4.5 Global rigidity claim state corrected

The abstract connected symmetric active-graph propagation theorem in
`GlobalLossRigidity.lean` is `PROVED / LEAN`. Complete spherical `Q=1`
specialization, restricted geodesic-triangulation classification, and
quantitative near-rigidity remain Prompt 3 targets.

## 5. Verification correction

All three workflows now:

- assert the literal checked-out head;
- reject aggregate `sorry`, `admit`, and `sorryAx`;
- reject anchored declarations using singular `axiom` or plural `axioms`;
- retain `sorryAx` outside nanoda's allowed-axiom list; and
- verify the immutable archive.

The dedicated Prompt 2 workflow additionally tests singular/plural declaration
fixtures and an allowed `#print axioms` fixture, runs both exact covariance
audits, performs the full Lean build and focused axiom audit, independently
checks the expanded Prompt 2 declaration set, and rejects out-of-scope paths.

## 6. Accepted implementation-head workflows

```text
AFP quadratic covariance
run=30734370610
job=91460293629
result=SUCCESS

AFP spherical feasibility
run=30734370649
job=91460293565
result=SUCCESS

AFP Pure Mathematics
run=30734370607
job=91460293589
result=SUCCESS
```

All three validated the literal implementation head
`afb31139cacdf1bf252e86e890c4792a03df4796` and tree
`2414b6048e3c0d090152b7873b8ee52b5e40ea3c`.

The repository-wide post-merge run also passed on
`dbe5d5db315d4e99b75c775c269827ac906b4fad`:

```text
run=30734539844
job=91460829310
result=SUCCESS.
```

## 7. Final metadata fast-forward

A documentation-only PR #20 records this closeout and Prompt 3 handoff. After
all three workflows pass its literal head, the target reference is advanced to
that exact commit with a non-forced fast-forward. This makes the validated PR
head the actual final target SHA rather than creating a synthetic merge SHA.

Because a Git commit cannot embed its own SHA/tree hash without a
self-referential hash fixed point, the exact final metadata head/tree and its
three workflow run/job identifiers are recorded in the immutable PR #20 and
PR #19 discussions and repeated in the final return. The accepted mathematical
baseline remains the merge commit/tree above.
