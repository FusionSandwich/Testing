# Gate 5: sharpness, equality, and angular-grid efficiency

**Status:** initial theorem and deterministic checkpoint under verification  
**Depends on:** closed Gates 1–4  
**Scope:** mathematical sharpness and spectral design; transport benchmarks remain Gate 6

## 1. Objective

Gate 4 proves that quasi-uniform positive spherical graphs achieve the natural
scales

\[
r_i=\Theta(h^{-2}),
\qquad
\varepsilon_i=\Theta(h^2).
\]

Gate 5 determines when the universal tradeoff

\[
\lambda^2\le r_i\varepsilon_i
\]

is sharp, measures the excess above the lower bound, and converts that excess
into a geometry diagnostic for angular quadratures.

The main quantity is the dimensionless efficiency factor

\[
Q_i=\frac{r_i\varepsilon_i}{\lambda^2}.
\]

For the spherical degree-one modes, `lambda=2`, so

\[
Q_i=\frac{r_i\varepsilon_i}{4}\ge1.
\]

A value close to one means the local angular losses are nearly uniform. Large
values identify a geometrically inefficient row whose stiffness is not buying a
corresponding reduction in second-mode defect.

---

## 2. Exact weighted-variance identity

At a normalized eigenmode peak, define

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

Direct expansion gives

\[
\boxed{
\varepsilon_i-2m\lambda+m^2r_i=V_i(m).
}
\]

If `m` is the weighted mean loss,

\[
m r_i=\lambda,
\]

then

\[
\boxed{
r_i\varepsilon_i-\lambda^2=r_iV_i(m).
}
\]

This is stronger than the Cauchy--Schwarz inequality: it gives the exact
nonnegative remainder.

Consequences:

1. `Q_i=1` exactly when the weighted loss variance vanishes.
2. With positive active rates, equality means every active edge has the same
   loss.
3. On the sphere, equal losses mean the active neighbours lie on one geodesic
   circle centred at the row vertex.
4. Near equality is a quantitative statement that the local edge-loss
   distribution is narrowly concentrated.

`AFPBarrier/LossVariance.lean` formalizes the centered identity and the exact
gap equation.

---

## 3. Exact product-grid inefficiency

For a square equal-angle ring, let

\[
s=\sin\theta.
\]

The existing Gate 3 formulas imply

\[
r=\frac{1}{2\sin^2h}
  +\frac{1}{2\sin^2h\,s^2},
\]

and

\[
\varepsilon=2\sin^2h+2s^2\sin^2h.
\]

Gate 5 proves the exact identity

\[
\boxed{
r\varepsilon-4=\frac{(s^2-1)^2}{s^2}.}
\]

Therefore

\[
\boxed{
Q=1+\frac{(s^2-1)^2}{4s^2}.
}
\]

The tradeoff is sharp at an equatorial ring, where `s^2=1`. Near a pole,
`s^2` is small and

\[
Q\sim\frac{1}{4s^2}.
\]

For the square grid polar ring, `s=sin(pi/(2N))`, so

\[
Q_{\rm polar}=\Theta(N^2).
\]

This identifies the Gate 3 polar stiffness as a growing weighted-loss variance,
not merely a large matrix coefficient.

---

## 4. Deterministic sharpness audit

`gate5/sharpness_audit.py` checks the exact variance identity at every vertex of
radially refined icosahedra and compares their efficiency with the node-matched
product-grid polar rows.

The reference deterministic results are:

| level | icosphere directions | maximum icosphere `Q` | product directions | product polar `Q` | ratio |
|---:|---:|---:|---:|---:|---:|
| 0 | 12 | 1.000000000 | 18 | 1.125000 | 1.125 |
| 1 | 42 | 1.013839845 | 50 | 3.141907 | 3.099 |
| 2 | 162 | 1.015065777 | 162 | 8.798398 | 8.668 |
| 3 | 642 | 1.017867875 | 648 | 33.413423 | 32.827 |
| 4 | 2,562 | 1.018735479 | 2,592 | 131.896095 | 129.470 |
| 5 | 10,242 | 1.018962449 | 10,368 | 525.832476 | 516.047 |

Thus the quasi-uniform implementation remains within about two percent of the
sharp local tradeoff through 10,242 directions, whereas the product-grid polar
inefficiency grows quadratically with refinement frequency.

These finite results are diagnostics. The exact variance identity and product
formula are the theorem-level results.

---

## 5. Remaining Gate 5 targets

### 5.1 Equality characterization

Formalize the equivalence

\[
r_i\varepsilon_i=\lambda^2
\iff
\ell_j=\lambda/r_i
\quad\text{for every strictly active edge}.
\]

### 5.2 Quantitative stability

Derive estimates converting

\[
Q_i-1
\]

into bounds on the weighted dispersion of edge losses. Possible forms include:

- weighted `L^2` variance;
- maximum loss deviation under a minimum active-rate assumption;
- concentration bounds for most of the local conductance mass.

### 5.3 Geometry-optimality theorem

Prove that any local monotone degree-one-exact family with

\[
\varepsilon_i\le C h^2
\]

must satisfy

\[
r_i\ge\frac{4}{C h^2}.
\]

Gate 4 attains this order, so `h^-2` is asymptotically optimal.

### 5.4 Design optimization

For a fixed node set and graph, solve the positive conductance problem under
one or more objectives:

- minimize maximum defect;
- minimize maximum rate at a prescribed defect;
- minimize maximum efficiency factor `Q`;
- minimize higher-mode spectral error;
- impose bounded graph degree or locality.

The primal and dual linear programs from Gate 2 provide feasibility and lower
bound certificates.

### 5.5 Higher spherical modes

Measure and bound the eigenvalue errors on degrees `2,3,...`. The central
question is whether minimizing the local degree-two variance also improves the
low-order spectrum globally, or whether a separate objective is required.

### 5.6 Rotational bias

Compare the variation of the response under rigid rotation of a fixed angular
profile. A quasi-uniform mesh should reduce the severe polar anisotropy of the
product grid, but this must be quantified independently of the peak defect.

---

## 6. Gate 5 completion criteria

Gate 5 is complete when:

1. the variance identity and equality characterization are Lean verified;
2. the product-grid sharpness formula is Lean verified;
3. an optimality theorem proves the `h^-2` rate order cannot be improved under
   `O(h^2)` defect;
4. deterministic sharpness audits pass on both product and quasi-uniform
   families;
5. at least one positive-conductance optimization problem is solved with a
   dual certificate;
6. higher-mode and rotational-bias comparisons are documented;
7. all exact source and generated records are archived by CI.

Gate 6 then tests whether these mathematical efficiency measures predict AFP
and BFP transport error and solver cost.
