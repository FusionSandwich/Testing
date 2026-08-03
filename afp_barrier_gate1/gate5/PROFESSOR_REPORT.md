# Gate 5 professor briefing: sharpness and optimality of monotone AFP rows

## Main result

For a positive angular jump row that preserves an eigenmode with eigenvalue
`-lambda`, let

```text
rate    = sum_j a_j
defect  = sum_j a_j ell_j^2
lambda  = sum_j a_j ell_j
ell_j   = f(i) - f(j)
```

at a normalized peak `f(i)=1`.

The project proves the exact identity

\[
\mathrm{rate}\,\mathrm{defect}-\lambda^2
=
\mathrm{rate}
\sum_j a_j\left(\ell_j-\frac{\lambda}{\mathrm{rate}}\right)^2.
\]

This identifies the excess over the universal lower bound as a weighted
variance of local angular losses.

## Consequences

1. **Equality:**

   \[
   \mathrm{rate}\,\mathrm{defect}=\lambda^2
   \]

   exactly when every strictly active edge has the same loss

   \[
   \ell_j=\lambda/\mathrm{rate}.
   \]

2. **Near equality:** if the gap is at most `eta`, then the weighted variance is
   at most `eta/rate`.  A minimum active edge rate gives a corresponding
   pointwise squared-deviation bound.

3. **Optimality:** on `S^2`, if the degree-two peak defect is bounded by
   `C h^2`, then

   \[
   \mathrm{rate}\ge 4/(C h^2).
   \]

   Gate 4 attains `rate = O(h^-2)`, so its order is optimal.

4. **Dual certificate:** the tangent inequality

   \[
   \ell^2\ge2m\ell-m^2
   \]

   solves the relaxed positive-rate row problem with fixed rate and first loss
   moment.  The optimal lower bound is `lambda^2/rate`, attained only by equal
   active losses.

## Grid comparison

For spherical degree-one modes define

\[
Q=\frac{\mathrm{rate}\,\mathrm{defect}}{4}.
\]

At about 10,000 directions:

```text
quasi-uniform icosphere maximum Q: 1.018962449
product-grid polar Q:              525.832476
ratio:                             516.047
```

The equal-angle product row has the exact formula

\[
\mathrm{rate}\,\mathrm{defect}-4
=
\frac{(\sin^2\theta-1)^2}{\sin^2\theta},
\]

so its polar inefficiency diverges as the latitude-ring radius collapses.

## Higher modes and rotation

A deterministic audit evaluates zonal harmonics of degrees 1–4 over 13 fixed
orientations.  At the finest matched grids, the quasi-uniform family has lower
Rayleigh eigenvalue error and substantially smaller orientation spread for
degrees 2–4.  The product family has a smaller residual for some sampled zonal
modes, showing that local peak efficiency, global residual error, and rotational
bias are separate design objectives.

## Verification

The theorem suite is written in Lean 4/Mathlib.  The workflow also runs complete
deterministic sharpness and low-mode audits, checks for proof placeholders or
user axioms, and archives the exact source state.

## Recommended next step

Gate 6 should compare the existing Radiant AFP operator, the equal-angle
reference operator, and the quasi-uniform operator on:

- exact spherical-harmonic decay;
- forward-peaked scattering;
- coupled charged-particle angular diffusion;
- one energy-loss or material-interface benchmark.

The key question is whether `Q`, low-mode eigenvalue error, and rotational bias
predict solver stiffness and transport-response error.
