# Gate 4: quasi-uniform positive angular graphs

**Status:** active mathematics gate  
**Starting point:** final verified Gate 3 source `74574c13e0f4d0a2e1e66742da3c7ade16a962a6`

## 1. Objective

Gate 3 proved that the equal-angle product family has

```text
maximum degree-two peak defect = Theta(N^-2)
maximum outgoing rate          = Theta(N^4).
```

Gate 4 seeks a local, conservative, reversible, monotone, degree-one-exact
spherical family for which

```text
maximum peak defect = Theta(h^2)
maximum rate        = Theta(h^-2).
```

The rate scale `h^-2` is the natural diffusion scale. Achieving it removes the
artificial polar stiffness caused by using the same azimuth count on every
latitude ring.

## 2. Generic local theorem

At a node `i`, let `f(i)=1` be a normalized degree-one zonal peak and define

```text
ell_ij = f(i) - f(j).
```

If the positive jump generator satisfies

```text
L f(i) = -lambda
```

then

```text
sum_j a_ij ell_ij = lambda.
```

If every active edge loss satisfies

```text
ell_min <= ell_ij <= ell_max,
```

then

```text
ell_min * r_i <= lambda <= ell_max * r_i,
ell_min * lambda <= epsilon_i <= ell_max * lambda.
```

Here `r_i` is the total outgoing rate and `epsilon_i` is the square or
second-harmonic peak defect.

For the unit sphere, `lambda=2` and

```text
ell_ij = 1 - Omega_i dot Omega_j.
```

Consequently, if all local geodesic edge lengths are comparable to `h`, then
`ell_ij = Theta(h^2)`, so

```text
r_i = Theta(h^-2),
epsilon_i = Theta(h^2).
```

The generic theorem is formalized in
`AFPBarrier/QuasiUniformLossBounds.lean`.

## 3. Candidate family

The first candidate is the radial refinement of the regular icosahedron. Each
planar midpoint is projected to the unit sphere and the resulting faces are
interpreted as geodesic spherical triangles.

On this triangulation Gate 4 uses the discrete spherical Laplacian of
Izmestiev and Lam:

```text
(Lu)_i = (1/d_i) sum_j c_ij (u_j-u_i),
```

with their spherical Delaunay edge conductances and vertex masses

```text
d_i = sum_j c_ij sin^2(lambda_ij/2).
```

Primary reference:

- I. Izmestiev and W. Y. Lam, *Discrete Laplacians — spherical and
  hyperbolic*, J. London Math. Soc. (2025),
  <https://doi.org/10.1112/jlms.70235>.

The existing geometric theorem supplies positive conductances on Delaunay
triangulations and exact `-2` modes associated with inscribed polyhedra. Gate 4
adds the AFP interpretation and the loss-window defect and stiffness theory.

## 4. Deterministic first results

`gate4/icosphere_spherical_laplacian_audit.py` checks every edge and vertex
through refinement level 5.

The levels contain

```text
12, 42, 162, 642, 2562, 10242 vertices.
```

The initial deterministic calculation gives:

| level | vertices | max/min edge | max coordinate residual | max defect | max rate |
|---:|---:|---:|---:|---:|---:|
| 0 | 12 | 1.0000 | 2.3e-16 | 1.1056 | 3.6180 |
| 1 | 42 | 1.1350 | 1.0e-15 | 0.3528 | 13.3914 |
| 2 | 162 | 1.1791 | 1.1e-14 | 0.09524 | 52.5463 |
| 3 | 642 | 1.1911 | 9.0e-14 | 0.02627 | 209.181 |
| 4 | 2562 | 1.1941 | 1.1e-12 | 0.006767 | 835.721 |
| 5 | 10242 | 1.1949 | 9.5e-12 | 0.001705 | 3341.884 |

The fitted slopes versus refinement frequency `2^level` are approximately

```text
maximum rate:   +1.992
maximum defect: -1.920
maximum edge:   -1.000.
```

These are deterministic evidence, not the all-order proof.

## 5. Current proof obligations

Gate 4 is not closed until all of the following are resolved.

1. The generic loss-window theorem builds in Lean with no placeholders or user
   axioms.
2. The deterministic icosphere audit passes from the exact committed source.
3. The radial icosahedral family is proved spherical Delaunay at every level,
   or a deterministic Delaunay-retriangulation rule is specified.
4. A uniform all-level edge-ratio bound is proved.
5. The Izmestiev–Lam matrix convention is transferred explicitly to the AFP
   forward and weighted-adjoint conventions.
6. Explicit constants are obtained for the `Theta(h^2)` defect and
   `Theta(h^-2)` rate statements.
7. The novelty language is limited to the transport consequences rather than
   claiming invention of the spherical Delaunay Laplacian.

## 6. Publication role

Gate 4 changes the paper from a negative theorem plus a polar-pathological
example into a complete geometric comparison:

1. exact degree two is impossible;
2. edge losses determine the unavoidable defect and rate;
3. a product grid has a quartic polar penalty;
4. a quasi-uniform positive graph restores the quadratic diffusion scale.

That is a materially stronger and more publishable result than Gates 1–3
alone.
