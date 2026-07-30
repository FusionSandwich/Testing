# Gate 3: an all-orders positive product-grid theorem and a polar stiffness barrier

**Status:** implementation draft for Lean and deterministic verification  
**Scope:** mathematics only; integration with `Radiant.jl` is deliberately deferred

## 1. Gate decision

Gate 3 establishes a complete all-orders theorem for a cell-centred equal-angle
latitude--longitude quadrature on the unit sphere. The construction is:

- local: every node has at most four neighbours;
- reversible with respect to the quadrature weights;
- monotone: every off-diagonal conductance is positive;
- conservative;
- exactly preserves all three degree-one spherical harmonics with eigenvalue
  `-2`;
- accompanied by exact formulas for the unavoidable degree-two peak defect and
  the total jump rate.

The same calculation also exposes a structural limitation of unreduced product
grids: when the polar and azimuthal resolutions are comparable, the largest
jump rate grows as `Theta(N^4)`, even though the degree-two defect decays as
`Theta(N^-2)`.

This is a deterministic mathematical reference family. It is not yet a claim
about every Gauss--Legendre--Chebyshev order used by Radiant. A direct all-order
proof for that family requires uniform inequalities between Gauss--Legendre
nodes, weights, and cumulative first moments. Recent mathematical analyses
still describe several of the needed uniform relations as conjectural or as
supported by strong asymptotic evidence:

- O. López Pouso and J. Segura, *Analysis of difference schemes for the
  Fokker--Planck angular diffusion operator*, Computers & Mathematics with
  Applications 181 (2025), 84--110, DOI:
  <https://doi.org/10.1016/j.camwa.2025.01.005>.
- O. López Pouso and J. Segura, *Uniform relations between the
  Gauss--Legendre nodes and weights*, Journal of Inequalities and Applications
  2025:40, DOI: <https://doi.org/10.1186/s13660-025-03283-w>.

The equal-angle theorem avoids building Gate 3 on an unproved
Gauss--Legendre inequality. It also gives a benchmark against which a future
GLC theorem or optimization can be tested.

---

## 2. Grid and quadrature

Choose integers

\[
N\ge 2,\qquad M\ge 3,
\]

and define

\[
\delta=\frac{\pi}{N},\qquad
\alpha=\frac{2\pi}{M}.
\]

The latitude and azimuth nodes are

\[
\theta_i=\left(i+\frac12\right)\delta,
\quad i=0,\ldots,N-1,
\]

\[
\phi_j=j\alpha,
\quad j=0,\ldots,M-1.
\]

The corresponding unit vector is

\[
\Omega_{ij}
=
\left(
\cos\theta_i,
\sin\theta_i\cos\phi_j,
\sin\theta_i\sin\phi_j
\right).
\]

Use the exact area of the spherical cell centred at `Omega_ij` as its weight:

\[
q_i
=
\int_{\phi_j-\alpha/2}^{\phi_j+\alpha/2}
\int_{\theta_i-\delta/2}^{\theta_i+\delta/2}
\sin\theta\,d\theta\,d\phi
=
2\alpha\sin\theta_i\sin\frac{\delta}{2}.
\]

Consequently,

\[
q_i>0,
\qquad
\sum_{i,j}q_i=4\pi.
\]

By the reflection and cyclic symmetries,

\[
\sum_{i,j}q_i\Omega_{ij}=0.
\]

---

## 3. Explicit positive conductances

For the meridional edge joining rings `i` and `i+1`, define

\[
B_{i+1/2}
=
\frac{\alpha\sin((i+1)\delta)}{\sin\delta},
\qquad i=0,\ldots,N-2.
\]

Set the boundary values

\[
B_{-1/2}=B_{N-1/2}=0.
\]

For each of the two azimuthal edges incident to a node on ring `i`, define

\[
C_i
=
\frac{
\alpha\sin(\delta/2)
}{
(1-\cos\alpha)\sin\theta_i
}.
\]

All conductances attached to actual edges are strictly positive because

\[
0<\delta<\pi,
\qquad
0<\theta_i<\pi,
\qquad
0<\alpha<2\pi.
\]

The discrete operator is

\[
\begin{aligned}
(Lf)_{ij}=\frac{1}{q_i}\big[&
B_{i+1/2}(f_{i+1,j}-f_{ij})
+B_{i-1/2}(f_{i-1,j}-f_{ij})\\
&+C_i(f_{i,j+1}-f_{ij})
+C_i(f_{i,j-1}-f_{ij})
\big],
\end{aligned}
\]

where azimuthal indices are periodic and absent meridional boundary terms are
omitted.

Because every edge uses one shared conductance, the operator satisfies detailed
balance:

\[
q_i L_{(i,j),(k,l)}
=
q_k L_{(k,l),(i,j)}.
\]

It is therefore self-adjoint in the weighted inner product and conserves every
weighted integral of the form `sum q_i f_ij`.

---

## 4. Exact degree-one eigenmodes

### 4.1 Axial coordinate

Let

\[
x_{ij}=\cos\theta_i.
\]

The azimuthal part vanishes. The identities

\[
\cos(\theta_i+\delta)-\cos\theta_i
=-2\sin\left(\theta_i+\frac\delta2\right)
  \sin\frac\delta2,
\]

\[
\cos(\theta_i-\delta)-\cos\theta_i
=2\sin\left(\theta_i-\frac\delta2\right)
 \sin\frac\delta2
\]

give

\[
\begin{aligned}
&B_{i+1/2}(x_{i+1,j}-x_{ij})
+B_{i-1/2}(x_{i-1,j}-x_{ij})\\
&=-2q_i\cos\theta_i.
\end{aligned}
\]

Hence

\[
Lx=-2x.
\]

The same formula remains valid on the first and last rings because the missing
boundary conductance is zero.

### 4.2 Transverse coordinates

Set

\[
s_i=\sin\theta_i.
\]

A direct trigonometric reduction gives the meridional identity

\[
B_{i+1/2}(s_{i+1}-s_i)
+B_{i-1/2}(s_{i-1}-s_i)
=
2\alpha\sin\frac\delta2\cos(2\theta_i).
\]

For

\[
y_{ij}=s_i\cos\phi_j,
\]

the two azimuthal neighbours satisfy

\[
y_{i,j+1}+y_{i,j-1}-2y_{ij}
=
2(\cos\alpha-1)y_{ij}.
\]

The azimuthal numerator is therefore

\[
-2\alpha\sin\frac\delta2\cos\phi_j.
\]

Adding the meridional and azimuthal contributions yields

\[
2\alpha\sin\frac\delta2
(\cos 2\theta_i-1)\cos\phi_j
=-2q_i y_{ij}.
\]

Thus

\[
Ly=-2y.
\]

Replacing cosine by sine gives, identically,

\[
Lz=-2z.
\]

Therefore the complete degree-one spherical-harmonic eigenspace is preserved
exactly at every `N` and `M`.

---

## 5. Exact degree-two peak defect

Fix a node and define the sampled zonal degree-one function

\[
g_{ij}(k,l)=\Omega_{ij}\cdot\Omega_{kl}.
\]

At its peak,

\[
g_{ij}(i,j)=1,
\qquad
Lg_{ij}(i,j)=-2.
\]

The Gate 1 carré-du-champ theorem gives the degree-two defect

\[
\varepsilon_i
=
\sum_{(k,l)\sim(i,j)}
 a_{(i,j),(k,l)}
 \left(1-\Omega_{ij}\cdot\Omega_{kl}\right)^2.
\]

For either meridional neighbour,

\[
1-\Omega_{ij}\cdot\Omega_{i\pm1,j}
=1-\cos\delta.
\]

For either azimuthal neighbour,

\[
1-\Omega_{ij}\cdot\Omega_{i,j\pm1}
=
\sin^2\theta_i(1-\cos\alpha).
\]

The conductance identities

\[
\frac{B_{i-1/2}+B_{i+1/2}}{q_i}
=
\frac{1}{1-\cos\delta},
\]

\[
\frac{C_i}{q_i}
=
\frac{1}{2(1-\cos\alpha)\sin^2\theta_i}
\]

then give the exact formula

\[
\boxed{
\varepsilon_i
=
(1-\cos\delta)
+
\sin^2\theta_i(1-\cos\alpha).
}
\]

This quantity is strictly positive at every finite resolution, in agreement
with the no-go theorem.

For the square product family `M=2N`, so that `alpha=delta`,

\[
1-\cos\delta
\le
\max_i\varepsilon_i
\le
2(1-\cos\delta).
\]

Consequently,

\[
\max_i\varepsilon_i=\Theta(N^{-2}).
\]

---

## 6. Exact jump rate and polar stiffness

The total outgoing rate at ring `i` is

\[
\boxed{
r_i
=
\frac{1}{1-\cos\delta}
+
\frac{1}{(1-\cos\alpha)\sin^2\theta_i}.
}
\]

For `M=2N`, the maximum occurs on the first and last rings, where

\[
\theta_0=\frac\delta2,
\qquad
1-\cos\delta=2\sin^2\frac\delta2.
\]

Hence

\[
\boxed{
r_{\max}
=
\frac{1}{2\sin^2(\delta/2)}
+
\frac{1}{2\sin^4(\delta/2)}.
}
\]

With `delta=pi/N`,

\[
r_{\max}
\sim
\frac{8}{\pi^4}N^4
+
\frac{2}{\pi^2}N^2.
\]

Thus the all-orders local positive construction has

\[
\boxed{
\varepsilon_{\max}=\Theta(N^{-2}),
\qquad
r_{\max}=\Theta(N^4).
}
\]

The quartic stiffness is caused by combining a fixed number of azimuthal nodes
on every ring with rings whose radius is only `Theta(N^-1)` near the poles.
It is a geometric product-grid effect, not a failure of the degree-one balance.

---

## 7. Verification strategy

### Lean

`AFPBarrier/EqualAngleProduct.lean` verifies:

1. the four-neighbour local action and its balance-to-eigenvalue implication;
2. positivity of the algebraic weight and conductance formulas;
3. the exact meridional and azimuthal rate identities;
4. the closed-form degree-two defect;
5. the closed-form total rate;
6. the square-grid polar rate and defect formulas.

The Lean layer intentionally separates the algebraic theorem from the
trigonometric mesh derivation. The latter is independently checked by the
fully deterministic audit below.

### Deterministic coded audit

`gate3/equal_angle_product_audit.py` uses only the Python standard library and
contains no random sampling. For

\[
N=2,3,4,5,8,16,32,64,128,
\qquad M=2N,
\]

it checks every node for:

- positive weights and edge conductances;
- total area `4*pi` and weighted centering;
- `Lx=-2x`, `Ly=-2y`, and `Lz=-2z`;
- the exact peak-defect formula;
- the exact jump-rate formula;
- the exact polar maximum-rate formula.

It also fits the deterministic log--log slopes over
`N=8,16,32,64,128`. The reference run gives

\[
\text{defect slope}=-1.98969363,
\qquad
\text{rate slope}=3.97970684.
\]

These numerical slopes are evidence for the already-derived exact asymptotic
formulas; they are not used as substitutes for the proof.

---

## 8. Gate 3 conclusion

Gate 3 is complete when:

1. the Lean package builds without proof placeholders or user axioms;
2. the deterministic audit passes all listed orders;
3. the exact source snapshot and audit outputs are archived by CI;
4. the claim wording remains limited to the equal-angle reference family.

The next mathematical target is a **reduced-ring or quasi-uniform spherical
family** that retains positivity and degree-one exactness while improving the
worst-case stiffness from `Theta(N^4)` to `Theta(N^2)`. A separate route is to
prove the missing all-order Gauss--Legendre inequalities needed to place the
GLC family under a theorem of the same type.
