# Shared-edge reconciliation, exact examples, and novelty boundary

## A sparse constructive reconciliation mechanism

The complete graph is not the only positive construction. Let `R` be a finite
collection of permitted cliques. For every block `r`, assign nonnegative
submasses `m_i^r`, supported on that clique, such that

```text
W_r=sum_i m_i^r>0,
sum_i m_i^r Omega_i=0,
sum_r m_i^r=w_i.                                              (1)
```

Define, on permitted edges,

```text
gamma_ij=sum_{r:i,j in r} 2 m_i^r m_j^r/W_r.                 (2)
```

Each block is the dense centered construction for its submass. Therefore

```text
sum_j gamma_ij(Omega_j-Omega_i)
 =sum_r[-2m_i^r Omega_i]
 =-2w_i Omega_i.                                             (3)
```

This reconciles independently plausible rows into one shared-edge solution on
a graph that may be much sparser than complete. An edge is strictly positive
whenever at least one centered block assigns positive submass to both
endpoints. Antipodal pairs, centered tetrahedral blocks, and overlapping
centered design blocks are immediate instances.

## Exact tangent and antipodal examples

The executable rational checks are under `pure_math/examples/`.

- **Outside:** `{(1,0),(0,1)}` is separated from zero by `(1,1)`.
- **Relative boundary:** `{(1,0),(-1,0),(0,1)}` has dependence
  `(1/2,1/2,0)`; the functional `(0,1)` forces the third coefficient to zero.
- **Relative interior and unique dependence:**

  ```text
  u1=(1,0), u2=(-3/5,4/5), u3=(-3/5,-4/5),
  lambda=(3/8,5/16,5/16).
  ```

  With common angle `pi/3`, the exact rates are `(3/2,5/4,5/4)`.
- **Repeated and redundant:**
  `{e1,-e1,e2,-e2,e1}` has the positive dependence
  `(1/8,1/4,1/4,1/4,1/8)`. Splitting the total `e1` weight differently gives
  infinitely many positive dependences.
- **Lower-dimensional:** `{e1,-e1}` has positive relative margin one in its
  affine line, but no ambient two-dimensional interior.
- **Boundary crossing:** replace `-e1` by the rational unit points
  `(-99/101,+20/101)` and `(-99/101,-20/101)`. The plus case is outside. The
  minus case has the exact positive dependence
  `(99/220,101/220,1/11)`.
- **Antipodal-only:** two indexed antipodes with rates `(1/2,1/2)`.
- **Mixed strict:** tangent directions `{e1,-e1}` at angle `pi/2`, rates
  `(1/4,1/4)`, and one antipodal rate `3/4`.
- **Mixed boundary:** add candidate `e2` with zero rate; the antipode consumes
  the remaining normal budget, but all-edge strictness fails.
- **Mixed outside:** one non-antipodal direction has rate zero and one
  antipodal rate is one.

These examples provide exact primal dependences and exact separating
functionals rather than floating-point LP status.

## Centered, locally strict, globally incompatible cube

Let

```text
Omega_s=s/sqrt(3),  s in {+1,-1}^3,
```

and permit the twelve cube edges. At each vertex, the three neighbors have dot
product `1/3`, tangent directions balance, and normal loss `2/3`. The unique
local exact row has rate one on every incident edge; every row is locally
strictly feasible.

Assign mass two to the antipodal pair `+++` and `---`, and mass one to the
other six nodes. Equal masses within each antipodal pair give exact weighted
centering. Still, no shared solution exists. In the coordinate that an edge
flips, the row equation forces that edge conductance to equal the mass at its
endpoint. The edge from `+++` to `++-` would have to equal both two and one.

An exact Farkas certificate is

```text
y_{+++}=y_{++-}=e3,
y_i=0 otherwise.                                             (4)
```

Every cube-edge strain is zero, while

```text
b·y=-2/sqrt(3)<0.                                            (5)
```

Thus this is a centered local-versus-global obstruction with an exact dual
certificate, not merely a failure of weighted centering or a numerical solve.

## Globally strict symmetric cube and exact LP dual

On the same cube with unit masses, set `gamma_e=1` on every edge. This is a
strict exact shared-edge solution. For the total-conductance objective
`c_e=1`, the primal value is twelve. Let

```text
y_i=-(3/4)Omega_i.                                          (6)
```

Every cube edge has squared chord length `4/3`, hence

```text
sigma_e(y)=(3/4)||Omega_q-Omega_p||^2=1=c_e.
```

Also `b·y=12`. Thus the primal and dual certificates are exact and every edge
complementary-slackness equation is saturated.

## Prior-art and publication boundary

The finite convex-hull, relative-interior, Farkas, and LP-duality theorems are
standard infrastructure. Positive/minimal-stencil theory already treats local
sign-constrained consistency, geometric selection, sparsity, and M-matrix
properties. Spherical discrete-Laplacian theory also contains positive
Delaunay-weight constructions and exact low-degree spherical eigenfunctions.

The contribution here is therefore not a rowwise restatement that directions
must surround the origin. The additional package is the combined theory of:

1. exact spherical tangent/normal separation for the coordinate eigenmap;
2. the uniquely fixed angular normal scale and explicit rate formula;
3. antipodes classified without a fictitious tangent or division by zero;
4. a relative cone margin with coefficient, rate, conditioning, perturbation,
   and objective constants;
5. positive masses and one conductance per undirected edge;
6. the global edge-column cone, complete alternative, optimization duals, and
   geometric complementary slackness;
7. a centered example separating local strict rows from global reversibility;
   and
8. dense and sparse constructive reconciliation mechanisms.

Novelty claims must be restricted to this combined sphere-specific and global
package after specialist priority review. The underlying textbook theorems are
cited rather than claimed.
