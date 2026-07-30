# Gate 4 closure: maximal spherical nets and optimal diffusion scaling

**Status:** theorem-level closure candidate; Lean and CI verification required on the exact final commit  
**Scope:** mathematics only; Radiant and transport benchmarks remain later gates

## 1. Result

For every angular scale

\[
0<h\le \frac{\pi}{4},
\]

there exists a finite monotone, conservative, weighted-reversible angular
Fokker--Planck graph on the unit sphere that preserves the complete degree-one
coordinate eigenspace exactly and satisfies, at every vertex,

\[
1\le h^2 r_i\le \pi^2,
\]

and

\[
\frac{4}{\pi^2}h^2\le \varepsilon_i\le 4h^2.
\]

Here `r_i` is the total outgoing jump rate and `epsilon_i` is the unavoidable
zonal degree-two peak defect.

Consequently,

\[
r_{\max}=\Theta(h^{-2}),
\qquad
\varepsilon_{\max}=\Theta(h^2).
\]

If `K_h` is the number of directions, then

\[
\frac{4}{h^2}\le K_h\le \frac{4\pi^2}{h^2},
\]

so equivalently

\[
r_{\max}=\Theta(K_h),
\qquad
\varepsilon_{\max}=\Theta(K_h^{-1}).
\]

This improves the equal-angle Gate 3 family from

\[
r_{\max}=\Theta(K^2)
\]

to the natural local-diffusion scale

\[
r_{\max}=\Theta(K)
\]

without changing the `Theta(K^-1)` degree-two peak-error order.

---

## 2. Maximal spherical nets

Choose a maximal `h`-separated set `X_h` on `S^2`: for distinct
`x,y in X_h`,

\[
d_{S^2}(x,y)\ge h,
\]

and no additional point can be added while preserving this property.

Such a set can be constructed greedily. The open spherical caps of radius
`h/2` centred at selected points are pairwise disjoint, so the process must
terminate after finitely many steps. Maximality implies the covering property

\[
\forall p\in S^2,\qquad
\min_{x\in X_h}d_{S^2}(p,x)\le h.
\]

Thus the separation radius is at least `h` and the covering radius is at most
`h`.

---

## 3. Delaunay edge-length window

Construct the spherical Voronoi decomposition of `X_h` and its dual spherical
Delaunay decomposition. If a Delaunay edge joins `x_i` and `x_j`, their Voronoi
cells meet at some point `p`. Hence

\[
d(p,x_i)=d(p,x_j)\le h.
\]

The triangle inequality gives

\[
d(x_i,x_j)\le 2h.
\]

Separation gives the opposite bound, so every active Delaunay edge has length

\[
\boxed{h\le \theta_{ij}\le 2h.}
\]

If a Delaunay cell is not triangular because of a cocircular degeneracy, it may
be triangulated by zero-weight diagonals. Removing those zero edges leaves the
same operator with strictly positive weights on every active edge.

Because `2h <= pi/2`, all active edges are shorter than a hemisphere and the
geodesic triangulation is non-antipodal.

---

## 4. Positive exact-degree-one spherical Laplacian

Izmestiev and Lam define a normalized spherical discrete Laplacian

\[
(Lu)_i
=\frac{1}{d_i}\sum_j c_{ij}(u_j-u_i).
\]

Their edge weights are nonnegative exactly for spherical Delaunay
triangulations. Their discrete deformation theorem supplies exact eigenvalue
`-2` functions. In particular, translations of an inscribed Euclidean
polyhedron are infinitesimal isometries, and their radial components are

\[
f_v(i)=v\cdot x_i.
\]

Therefore, for every `v in R^3`,

\[
Lf_v=-2f_v.
\]

References:

- I. Izmestiev and W. Y. Lam, *Discrete Laplacians -- spherical and
  hyperbolic*, Journal of the London Mathematical Society 112 (2025), e70235,
  DOI `10.1112/jlms.70235`.
- Preprint: `https://arxiv.org/abs/2408.04877`.

Set

\[
\kappa=\frac{4\pi}{\sum_i d_i},
\qquad
w_i=\kappa d_i,
\qquad
\gamma_{ij}=\kappa c_{ij}.
\]

Then

\[
\sum_iw_i=4\pi,
\qquad
w_iL_{ij}=\gamma_{ij}=w_jL_{ji},
\]

and the normalized operator is unchanged. This is exactly the shared-edge AFP
conductance convention formalized in Gate 2.

---

## 5. Explicit angular-loss constants

At the peak of the zonal degree-one mode based at `x_i`,

\[
f_i(j)=x_i\cdot x_j,
\qquad
f_i(i)=1,
\]

and an edge of geodesic length `theta` has loss

\[
\ell(\theta)=1-\cos\theta.
\]

For `h <= theta <= 2h` and `h <= pi/4`, monotonicity of cosine and Jordan's
inequality imply

\[
\frac{2}{\pi^2}h^2
\le 1-\cos\theta
\le 2h^2.
\]

The lower estimate follows from

\[
1-\cos h=2\sin^2(h/2)
\ge 2\left(\frac{h}{\pi}\right)^2,
\]

and the upper estimate from

\[
1-\cos(2h)=2\sin^2h\le 2h^2.
\]

`AFPBarrier/SphericalNetScaling.lean` formalizes these inequalities and their
jump-generator consequences.

---

## 6. Rate and defect bounds

The exact degree-one relation gives the first loss moment

\[
\sum_j a_{ij}\ell_{ij}=2.
\]

The exact peak-defect identity gives the second loss moment

\[
\varepsilon_i=\sum_j a_{ij}\ell_{ij}^2.
\]

With

\[
\ell_{\min}=\frac{2}{\pi^2}h^2,
\qquad
\ell_{\max}=2h^2,
\]

the Gate 4 loss-window theorem yields

\[
\frac{2}{\ell_{\max}}
\le r_i\le
\frac{2}{\ell_{\min}},
\]

hence

\[
\boxed{1\le h^2r_i\le \pi^2.}
\]

It also yields

\[
2\ell_{\min}\le\varepsilon_i\le2\ell_{\max},
\]

hence

\[
\boxed{
\frac{4}{\pi^2}h^2
\le\varepsilon_i\le4h^2.
}
\]

These are uniform all-order constants, not fitted slopes.

---

## 7. Direction-count bounds

A spherical cap of angular radius `rho` has area

\[
A(\rho)=2\pi(1-\cos\rho).
\]

The radius-`h/2` caps around `X_h` are disjoint, while the radius-`h` caps
cover the sphere. Therefore

\[
K_hA(h/2)\le4\pi
\le K_hA(h),
\]

or

\[
\frac{2}{1-\cos h}
\le K_h\le
\frac{2}{1-\cos(h/2)}.
\]

Using

\[
1-\cos h\le\frac{h^2}{2},
\qquad
1-\cos(h/2)\ge\frac{h^2}{2\pi^2},
\]

gives

\[
\boxed{
\frac{4}{h^2}\le K_h\le\frac{4\pi^2}{h^2}.
}
\]

Combining with the rate and defect bounds gives explicit direction-count
estimates

\[
\frac{K_h}{4\pi^2}
\le r_i\le
\frac{\pi^2}{4}K_h,
\]

and

\[
\frac{16}{\pi^2K_h}
\le\varepsilon_i\le
\frac{16\pi^2}{K_h}.
\]

Thus the maximal-net Delaunay family has linear stiffness and inverse-linear
peak defect in the number of angular directions.

---

## 8. Relation to the deterministic icosphere audit

The radially refined icosphere remains a useful explicit implementation and
benchmark. Through level 5, every tested edge was strictly Delaunay, the edge
ratio remained below `1.195`, the coordinate residual remained at roundoff,
and the observed rate and defect slopes matched the theorem.

The theorem above no longer depends on proving that the fixed radial
connectivity remains Delaunay for every level. A deterministic implementation
may:

1. generate a quasi-uniform point cloud, including the existing icosphere;
2. compute its spherical Delaunay decomposition;
3. assemble the Izmestiev--Lam weights;
4. remove zero-weight degeneracy edges;
5. normalize the vertex masses to total weight `4*pi`.

The maximal-net proof supplies a complete existence family; the icosphere
supplies a practical highly symmetric realization.

---

## 9. Gate 4 closure criteria

Gate 4 is closed when the following exact source state is green:

1. `QuasiUniformLossBounds.lean` builds;
2. `SphericalNetScaling.lean` builds;
3. all new public theorems pass the axiom audit;
4. the deterministic icosphere audit passes;
5. the node-matched Gate 3 comparison passes;
6. no proof placeholders or user axioms are present;
7. the exact source and generated records are archived by CI.

The next gate studies sharpness, equality, and optimization rather than
existence.
