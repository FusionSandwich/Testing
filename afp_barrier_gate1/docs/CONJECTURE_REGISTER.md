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

## C-M2B. Complete spherical `Q=1` specialization — resolved

**Status:** PROVED / LEAN finite core.

For the exact spherical generator, coordinate exactness gives

```text
sum_j a_ij ell_ij=2,
Q_i-1=sum_j p_ij(r_i ell_ij/2-1)^2.
```

Thus local `Q_i=1` fixes every active loss to `2/r_i`.  Shared positive
conductances make activity symmetric, spherical loss is symmetric, and a
shared active edge forces equal endpoint rates.  Connectedness propagates one
global rate and loss.  Loops, zero-rate rows, coincident active edges,
antipodal `ell=2`, repeated embeddings, and inactive permitted edges are
audited separately in `GLOBAL_Q_RIGIDITY_THEOREM.md` §§1–2.

## C-M3. Restricted geodesic-triangulation classification — resolved

**Status:** PROVED under the ten explicit hypotheses of Theorem P3-R.

An actual finite simple, injective, nondegenerate, convex-face, full-coverage
minor-arc geodesic triangulation with every edge active and `Q_i=1` is, up to
`O(3)`, the regular tetrahedral, octahedral, or icosahedral triangulation.
The proof establishes common spherical side and angle, the round `2pi` angle
sum, constant valence, Euler restriction, direct combinatorial uniqueness for
all three maps, exact side/loss/rate constants, and geometric uniqueness by
face propagation.

The source-pinned plantri census through 12 vertices is a hostile falsification
audit, not the proof.  Cube and dodecahedron remain permanent counterexamples
to every unrestricted formulation.

## C-M4. Quantitative near-rigidity — resolved

**Status:** PROVED with explicit constants.

Under `p_ij>=kappa>0`, `Q_i<=1+eta`, and
`delta=sqrt(eta/kappa)<1`, the theorem gives pointwise, adjacent, path,
diameter, incident-edge, global edge-loss, graph-center reference, and
minor-arclength bounds.  Detailed balance for
`pi_i proportional w_i r_i` gives

```text
E_P(log r)<=2eta/(1-delta)^2,
Var_pi(log r)<=2eta/((1-delta)^2 lambda_P),
|log r_i-log r_j|<=sqrt(2eta R_eff(i,j))/(1-delta).
```

For round geodesic triangulations, explicit side-domain, spherical-angle,
integer-valence, and equilateral-angle derivative constants identify the
Platonic type and bound the edge-length sup distance.  Section 6.5 supplies a
single conservative `eta_*=kappa delta_*^2` under displayed reference margins.
Long paths, small `kappa`, small spectral gap, and large resistance remain
necessity tests.

## C-M4C. `Q=1` covariance implication — resolved negatively and exactly

`Q=1` gives

```text
C_i=2(2-ell_i)T_i+2ell_i Omega_iOmega_i^T,
M_i=3ell_i(Omega_iOmega_i^T-I/3)
    +2(2-ell_i)(T_i-P_i/2).
```

Axial covariance holds iff `T_i=P_i/2`.  The positive reversible weighted
octahedral family has `Q=1` at every vertex but is axially isotropic at all
vertices iff `g_12=g_13=g_23`.  Its genuine sampled degree-two exact space is
`{0}` for all positive parameters.  Therefore `Q=1 =>` axial covariance is
permanently REJECTED.

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
