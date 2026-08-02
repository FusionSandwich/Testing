# AFP pure-math conjecture register

Every unresolved conjecture requires a precise hypothesis set, deterministic
falsification search, literature status, and kill criterion. Resolved and
rejected entries remain here as permanent regression controls.

## C-M1. Strict local spherical feasibility — resolved

**Status:** PROVED.

The corrected Prompt 1 package proves indexed convex-hull/relative-interior
feasibility, exact scaling and uniqueness, division-free antipodal handling,
quantitative margins, conditioning, and transported-span perturbation
stability. Repetitions, redundancies, and lower-dimensional spans are included.

## C-M1G. Local-to-global reversible compatibility — resolved negatively and conditionally

The unrestricted implication is REJECTED by exact centered sparse examples.
Complete-graph sufficiency, equivariant orbit averaging, centered-clique
submass decomposition, and the full shared-edge cone/Farkas test are PROVED
replacement mechanisms.

## C-M2A. Abstract global equality propagation — resolved

**Proved statement.** Under a positive common eigenvalue, positive row rates,
a symmetric active relation, a symmetric edge loss, the local equality formula

```text
loss(i,j)=lambda/rate(i)
```

on every active edge, and connectedness of the active relation, all row rates
are equal and all active-edge losses have one common value.

**Status:** PROVED / LEAN in `AFPBarrier/GlobalLossRigidity.lean` through:

```text
rate_eq_of_symmetric_active_loss,
rate_eq_of_active_reflTransGen,
connected_active_loss_rigidity.
```

This abstract propagation theorem is no longer a conjecture.

## C-M2B. Complete spherical `Q=1` specialization — Prompt 3 target

**Question.** Determine the exact spherical hypotheses under which the local
rate-defect equality condition supplies the abstract theorem's active-edge
formula, and audit all normalization and zero-edge cases.

**Status:** PROMPT 3 TARGET. Do not call it proved merely because the abstract
propagation theorem is formalized.

## C-M3. Restricted geodesic-triangulation classification — Prompt 3 target

**Candidate statement.** A connected nondegenerate geodesic triangulation of
`S^2` with positive conductances on every edge, exact coordinate eigenmap, and
`Q_i=1` at every vertex must be tetrahedral, octahedral, or icosahedral under a
fully stated convex-embedding/equal-loss hypothesis.

**Status:** CONJECTURE / PROMPT 3 TARGET.

**Known warning:** cube and dodecahedron embeddings defeat every unrestricted
Platonic-only claim.

**Kill criterion:** one valid non-Platonic triangulated counterexample under
the final hypotheses.

## C-M4. Quantitative near-rigidity — Prompt 3 target

**Candidate statement.** Under explicit lower active-weight, connectivity, and
rate-control hypotheses, small local equality defect forces global active-edge
loss concentration with an explicit graph-dependent bound.

**Status:** CONJECTURE / PROMPT 3 TARGET.

**Work needed:** propagate the local weighted-variance estimate while tracking
minimum conductance, graph diameter/overlap, and row-rate variation.

**Kill criterion:** a family with defect tending to zero but no controlled
loss concentration under the stated hypotheses.

## C-M5. Genuine sampled quadratic exactness — resolved after corrective audit

The covariance package proves

```text
R_X=(L+2d I)S_X,
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2d I),
dim E_sample=rank(S_X)-rank(R_X).
```

Positive axial covariance at every vertex gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension, and the five
Platonic examples are classified exactly.

The independent equivariant route is now correctly stated only under

```text
a_ij>=0 for every i!=j.
```

Together with transitivity, an equivariant unit-sphere coordinate eigenmap,
irreducibility of the real conjugation representation on `Sym_0(d)`, and one
positive distinct jump, this gives `E_form={0}`. Reversibility is not used.

**Permanent signed regression.** On the regular pentagon, distance-one rate

```text
(5+3sqrt(5))/10
```

and distance-two rate

```text
(5-3sqrt(5))/10
```

produce coordinate eigenvalue `-1`, full trace-free quadratic eigenvalue
`-4`, `E_form=Sym_0(2)`, and `dim E_sample=2`, while the real `C_5`
conjugation action is irreducible. Therefore the equivariant theorem without
global nonnegativity is REJECTED.

**Status:** PROVED AFTER CORRECTIVE AUDIT.

## C-M6. Centered spectral products — resolved locally, hierarchy rejected

For

```text
Gamma(f,g)=1/2 sum_j a_ij(f_j-f_i)(g_j-g_i),
Lf=-lambda f,
Lg=-nu g,
```

the exact shifted residual is

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

**Resolved conclusions:**

- uncentered resonance (`c=0`) forces zero carré du champ;
- on an irreducible positive chain with `lambda>0`, the uncentered resonant
  eigenfunction is zero;
- centered resonance may be nonzero;
- centered resonance gives semigroup variance
  `c(1-exp(-2lambda t))`, not Jensen equality.

**Permanent positive regression.** On the four-state Boolean square with rate
one coordinate flips and `f=x_1+x_2`,

```text
Lf=-2f,
f^2-2=2x_1x_2 != 0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

Thus universal centered-square impossibility is REJECTED.

The exact `S^2` table for `ell=1,...,6` has no additive resonance, while the
general higher-dimensional resonance equation remains Pell-type. After
sampling kernels, cross-degree aliases, equality sets, and component
identifiability are enforced, no `ell`-indexed sampled dimension tradeoff,
multiplicity obstruction, or new global consequence survives.

**Hierarchy status:** REJECTED FOR PROMPT 2 under that kill criterion. The
rejection does not rely on a centered-square impossibility theorem and does
not rule out future theorems under stronger association-scheme or design
hypotheses.

## Verification-policy correction — resolved

The dedicated Prompt 2 workflow now scans the aggregate pure-math Lean source
for both

```text
axiom
axioms
```

using an anchored declaration regex, includes deterministic singular/plural
fixtures, keeps `sorryAx` outside the nanoda allowed list, runs the focused
axiom audit, and asserts the literal checked-out head SHA.

## Rejected statements retained as regression warnings

- local positive rows plus centering imply arbitrary sparse shared-edge
  feasibility;
- unrestricted `Q=1` classification by `K in {4,6,12}`;
- algebraic form dimension equals genuine sampled exact dimension;
- equivariant irreducibility needs only one positive rate while other rates may
  be signed;
- every nonzero centered additive square is impossible;
- centered resonance is Jensen equality;
- a Pell arithmetic resonance alone produces a spectral-product hierarchy;
- blanket finite-graph Bakry–Émery curvature collapse;
- continuum `W_2` contraction from positivity alone; and
- general order independence of layered stopping maps.
