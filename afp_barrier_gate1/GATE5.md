# Gate 5: sharpness, optimality, and angular-grid efficiency

**Status:** CLOSED AND VERIFIED  
**Depends on:** closed Gates 1–4  
**Scope:** mathematical sharpness, positive-row optimization, low-mode spectrum, and rotational bias

**Final verification:** branch `0e1c4cc19f8d033f6994b27900ea7c7c3012a420`, workflow run `30566683599`, artifact `8769176963`, SHA-256 `a02ffb65b4c8d98a68c504c4a56c330164fd28a1ebc6d91c5fcf4619b2c607ce`.

---

## 1. Gate result

Gate 5 characterizes equality and near-equality in the universal AFP
peak-defect/stiffness inequality

\[
\lambda^2\le r_i\varepsilon_i.
\]

It proves that the exact excess above the lower bound is a weighted variance of
local angular losses.  This supplies:

1. a complete equality characterization;
2. quantitative near-equality stability;
3. a dual certificate solving the relaxed positive-rate row optimization;
4. a proof that the `h^-2` rate scale from Gate 4 is asymptotically optimal;
5. an exact product-grid inefficiency formula;
6. deterministic degree-2 through degree-4 spectral and rotational-bias data.

For spherical degree-one modes, define

\[
Q_i=\frac{r_i\varepsilon_i}{4}.
\]

Then `Q_i >= 1`, and `Q_i-1` is an exact local geometry inefficiency measure.

---

## 2. Exact weighted-variance identity

At a normalized eigenmode peak, write

\[
\ell_j=f(i)-f(j),
\qquad
r_i=\sum_j a_{ij},
\qquad
\sum_j a_{ij}\ell_j=\lambda,
\]

and

\[
\varepsilon_i=\sum_j a_{ij}\ell_j^2.
\]

For any center `m`, define

\[
V_i(m)=\sum_j a_{ij}(\ell_j-m)^2.
\]

`LossVariance.lean` proves

\[
\boxed{
\varepsilon_i-2m\lambda+m^2r_i=V_i(m).
}
\]

If `m` is the weighted mean loss,

\[
mr_i=\lambda,
\]

then

\[
\boxed{
r_i\varepsilon_i-\lambda^2=r_iV_i(m).
}
\]

Thus the Cauchy--Schwarz remainder is known exactly.

---

## 3. Equality characterization

Assume the total rate is positive and all off-diagonal rates are nonnegative.
`LossVarianceSharpness.lean` proves

\[
\boxed{
r_i\varepsilon_i=\lambda^2
\iff
\ell_j=\frac{\lambda}{r_i}
\quad\text{for every edge with }a_{ij}>0.
}
\]

Therefore equality holds precisely when every strictly active neighbour lies on
one loss level.  On the sphere, for a zonal degree-one mode, this means all
active neighbours lie on one geodesic circle centered at the row vertex.

Zero-rate edges do not affect the characterization.

---

## 4. Quantitative near-equality stability

Let

\[
G_i=r_i\varepsilon_i-\lambda^2.
\]

If `G_i <= eta`, then Lean proves

\[
\boxed{
V_i\!\left(\frac{\lambda}{r_i}\right)
\le \frac{\eta}{r_i}.
}
\]

For a particular active edge whose rate is at least `a_min`, it also proves

\[
\boxed{
a_{\min}
\left(\ell_j-\frac{\lambda}{r_i}\right)^2
\le \frac{\eta}{r_i}.
}
\]

This turns a small value of `Q_i-1` into a quantitative statement that the
active loss distribution is concentrated around its weighted mean.

For the spherical degree-one case,

\[
G_i=4(Q_i-1).
\]

---

## 5. Positive-row optimization and dual certificate

Consider the relaxed positive-rate row problem

\[
\begin{aligned}
\text{minimize}\quad & \sum_j a_j\ell_j^2,\\
\text{subject to}\quad
& a_j\ge0,\\
& \sum_j a_j=r,\\
& \sum_j a_j\ell_j=\lambda.
\end{aligned}
\]

For any `m`, the tangent inequality

\[
\ell^2\ge 2m\ell-m^2
\]

provides the dual lower bound

\[
\boxed{
\varepsilon\ge 2m\lambda-m^2r.
}
\]

Lean verifies this certificate directly from the variance identity.  Choosing

\[
m=\frac{\lambda}{r}
\]

gives

\[
\boxed{
\varepsilon\ge\frac{\lambda^2}{r}.
}
\]

The equality theorem shows that this lower bound is attained exactly when every
strictly active loss is `lambda/r`.  Hence the relaxed fixed-rate/fixed-moment
positive-row optimization is solved, with matching primal equality conditions
and an explicit dual certificate.

This is not yet the full graph-coupled conductance optimization.  It is the
sharp local lower bound against which graph-constrained Gate 6 constructions
should be compared.

---

## 6. Asymptotic optimality of Gate 4

For the spherical degree-one eigenvalue `lambda=2`, suppose

\[
\varepsilon_i\le C h^2.
\]

Lean proves

\[
\boxed{
r_i\ge\frac{4}{C h^2}.}
\]

Therefore no monotone degree-one-exact family with `O(h^2)` peak defect can have
rate `o(h^-2)`.

Gate 4 constructs a positive quasi-uniform family with

\[
r_i=O(h^{-2}),
\]

so its rate order is asymptotically optimal.

---

## 7. Exact product-grid inefficiency

For a square equal-angle ring, let

\[
s=\sin\theta.
\]

Lean proves

\[
\boxed{
r\varepsilon-4=\frac{(s^2-1)^2}{s^2}.}
\]

Thus

\[
\boxed{
Q=1+\frac{(s^2-1)^2}{4s^2}.}
\]

The equatorial row is sharp.  Near a pole, `s` becomes small and the weighted
loss variance diverges.  For the square-grid polar ring,

\[
Q_{\mathrm{polar}}=\Theta(N^2).
\]

This identifies the Gate 3 polar stiffness as a geometric variance penalty,
not merely a large matrix coefficient.

---

## 8. Deterministic sharpness audit

`gate5/sharpness_audit.py` checks the exact variance identity at every icosphere
vertex through level 5 and on node-matched product-grid polar rows.

| Level | Icosphere directions | Maximum icosphere `Q` | Product directions | Product polar `Q` | Ratio |
|---:|---:|---:|---:|---:|---:|
| 0 | 12 | 1.000000000 | 18 | 1.125000 | 1.125 |
| 1 | 42 | 1.013839845 | 50 | 3.141907 | 3.099 |
| 2 | 162 | 1.015065777 | 162 | 8.798398 | 8.668 |
| 3 | 642 | 1.017867875 | 648 | 33.413423 | 32.827 |
| 4 | 2,562 | 1.018735479 | 2,592 | 131.896095 | 129.470 |
| 5 | 10,242 | 1.018962449 | 10,368 | 525.832476 | 516.047 |

At approximately 10,000 directions, the quasi-uniform implementation remains
within about `1.9%` of the exact local lower bound, while the product polar row
is more than `500` times less efficient in `Q`.

---

## 9. Higher spherical modes and rotational bias

`gate5/spectral_bias_audit.py` evaluates deterministic zonal harmonics

\[
P_\ell(u\cdot\Omega),
\qquad \ell=1,2,3,4,
\]

for 13 fixed orientations `u`.  It reports weighted Rayleigh eigenvalue errors,
orientation-to-orientation spread, and residuals against the exact eigenvalue
`-ell(ell+1)`.

At the finest node-matched comparison:

| Family | Directions | Degree | Maximum relative eigenvalue error | Rotational spread | Maximum relative residual |
|---|---:|---:|---:|---:|---:|
| Icosphere | 10,242 | 2 | 3.560987e-4 | 2.072416e-14 | 2.221897e-3 |
| Product | 10,368 | 2 | 6.345504e-4 | 3.347017e-4 | 8.163879e-4 |
| Icosphere | 10,242 | 3 | 9.503630e-4 | 1.263448e-4 | 3.071265e-3 |
| Product | 10,368 | 3 | 1.585804e-3 | 7.805824e-4 | 1.614418e-3 |
| Icosphere | 10,242 | 4 | 1.619838e-3 | 3.831504e-5 | 3.546352e-3 |
| Product | 10,368 | 4 | 2.853054e-3 | 1.281538e-3 | 2.886957e-3 |

The quasi-uniform icosphere has lower Rayleigh eigenvalue error and dramatically
smaller orientation spread for these tests.  The product operator has a smaller
zonal residual in some fine-grid cases, so the conclusion is not that one
operator dominates every spectral metric.  The main result is that peak defect,
low-mode eigenvalue error, residual error, and rotational bias are distinct
design objectives.

Degree one is preserved to floating-point roundoff in both families and is used
as a regression check.

---

## 10. Formal verification

The final workflow passed:

- deterministic sharpness and weighted-variance audit;
- deterministic degree-1 through degree-4 spectral and rotational-bias audit;
- Lean/Mathlib `v4.30.0` kernel build with 3,085 jobs;
- main and Gate-5-specific axiom audits with 150 explicit theorem entries;
- proof-placeholder and user-axiom scan;
- exact source and generated-record packaging.

No `sorry`, `admit`, `sorryAx`, or user-declared axiom is present.

---

## 11. Completion criteria

Gate 5 is complete because:

- [x] the variance identity is Lean verified;
- [x] the equality characterization is Lean verified;
- [x] quantitative near-equality stability is Lean verified;
- [x] the product-grid sharpness formula is Lean verified;
- [x] `h^-2` rate optimality under `O(h^2)` defect is Lean verified;
- [x] the relaxed positive-rate optimization is solved with a dual certificate;
- [x] deterministic sharpness audits pass on both families;
- [x] higher-mode errors are documented;
- [x] rotational bias is documented;
- [x] exact source and generated records are archived by CI.

Gate 6 should now test whether `Q`, higher-mode spectral errors, and rotational
bias predict AFP/BFP transport accuracy, solver stiffness, and runtime.
