# Manuscript-ready abstract

We study finite positive jump generators equipped with a prescribed Euclidean
eigenmap and ask when low-degree continuum structure survives after finite
sampling. For a unit-sphere coordinate eigenmap, nonnegative local exactness is
characterized by an indexed tangent convex hull; strict positivity is relative
interior membership, including repeated directions, redundant candidates,
lower-dimensional spans, and a separate division-free antipodal theory. With
positive masses and shared conductances, the global reversible problem becomes
an exact finitely generated cone problem with a full Farkas alternative,
complementary slackness, dense complete-graph sufficiency under weighted
centering, and explicit sparse local-to-global obstructions.

The central result concerns quadratic samples. If `Phi` is an eigenmap and
`C_i` is its local jump covariance, then the residual of a trace-free quadratic
form factors through the actual finite sampling map. In the spherical
degree-two specialization,

```text
R_X=(L+2dI)S_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

Thus algebraically nonzero exact forms, nonzero sampled functions, and genuine
sampled eigenmodes are distinct objects. Positive axial covariance forces the
form kernel to equal the sampling kernel, annihilating every genuine sampled
quadratic mode; an independent positive equivariant theorem gives complete
form rigidity under an irreducibility hypothesis. Regular simplices show
sharpness, while exact Platonic calculations exhibit large alias spaces and
signed examples identify the positivity boundary.

We also classify equality in the sharp spherical rate--defect inequality. At
one node, equality is equivalent to constant chord loss on the active row. On
a connected symmetric active support, this propagates one common row rate and
one common active loss. If the support is exactly an injective strict-convex
minor-geodesic triangulation of the sphere, the embedding is a regular
tetrahedron, octahedron, or icosahedron. Quantitative variants give explicit
edge-loss and row-rate estimates in terms of active-weight floors, graph paths,
and diameter, with exact counterfamilies showing that these hypotheses cannot
be removed.

Finally, we prove a sharp graph-class obstruction for the unreduced
latitude--longitude product graph. The three polar coordinate equations
uniquely force the polar rates, without an optimizer-symmetry assumption, and
give the exact minimax maximum rate

```text
1/[2 sin^2(pi/(2N))] + 1/[2 sin^4(pi/(2N))].
```

A uniform `N>=2` expansion has leading constant `8/pi^4` and an explicit
`O(N^-2)` remainder. A rate-capped, degree- and geometry-controlled extremal
problem has finite-order minimizers and asymptotic lower bound `4/R`. An exact
sliced linear program and its dual define the best a priori anisotropy lower
bound over the entire positive feasible cone, avoiding the false premise that
quality is determined by node geometry alone.

The main statements are independent of any discretization acronym. Selected
finite algebra is formalized in Lean, and deterministic rational or algebraic
computations are used only for independent falsification and reproducibility.

## Reconciliation addendum

The combined package also proves a restricted global rigidity theorem for
positive reversible spherical generators: sharp normalized loss variance on a
round minor-arc geodesic triangulation forces the regular tetrahedral,
octahedral, or icosahedral framework.  Near equality yields explicit path,
diameter, spectral-gap, effective-resistance, and edge-metric bounds, together
with a computable Gram/Heron-certified threshold for identifying the Platonic
type.  Exact scalar quality fixes only the radial covariance component; a
weighted-octahedral family shows tangential anisotropy can remain order one,
and the antipodal equality boundary is purely radial.  The finite plantri
census is used only as falsification evidence.
