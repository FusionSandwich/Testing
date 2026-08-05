# Hostile audit of the rational Cauchy and first-row guards

## Verdict

**ACCEPT.**  The rational Cauchy guard
really does prove the stated all-orders transition enclosure, uniformly on
the correlated phase box.  The separate first-row guard also proves finite
positivity.  The constants are very loose but valid.  No finite-level LP or
fitted convergence rate is used in either conclusion.

The transition right-hand-side explanation has been corrected: only the
force and loss-force rows contain the removable quotient \(1/(cr)\), while
the isotropy row is bounded directly.

**Final scoped verdict: ACCEPT for the normalized \(6\times6\) transition
guard and the separate first-polar-row positivity guard.**

The independent exact regression is

```bash
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_cauchy_hostile_audit.py
```

## 1. Analytic variables and denominator guards

Fix real \(\eta,c\) with \(|\eta|\le3\) and \(6/7\le c\le1\), and complexify
only

\[
 x=M^{-1},\qquad a=\tfrac14+\eta x,
 \qquad r={\pi x\over a},\qquad \alpha=\pi x=ar.
\]

On \(|x|\le10^{-4}\),

\[
 .249<|a|<.251,qquad |r|<1/700,qquad
 |16\alpha|<1/180,qquad |\cos\alpha|>9/10.
\]

Thus the only rational denominators in the cancellation-free program,
namely \(a,c,\cos\alpha\), do not vanish.  The functions
\(\operatorname{sinc}\) and \(\operatorname{cosc}\) are entire after filling
in their removable values.  There is no hidden division by \(s=\sin\theta\):
after row normalization every neighbor sine appears as a ratio to \(s\),
and those ratios have the cancellation-free forms

\[
 \cos(\lambda sr)+c\lambda r\operatorname{sinc}(\lambda sr)
\]

or the same expression with a minus sign.  The fine-row cosine ratio is

\[
 {c_f\over c}=\cos(gsr)-{s^2\over c}gr
                      \operatorname{sinc}(gsr).
\]

These remain analytic and bounded as \(c\uparrow1\).  Actual transition
rows have \(c<1\); the endpoint \(c=1\) is only the continuous closure of
the guard box.

## 2. Literal column comparison

Write a base sine, base cosine, and neighbor sine as

\[
 bs,\qquad c_0,qquad ns,
\]

put \(m_1=r^2M_1,m_2=r^4M_2\), and let the meridional gap be
\(z=\lambda sr\).  Direct substitution into all three literal row equations
gives exactly (4.8).  For an incoming edge the force and leading loss terms
change sign, the \(\lambda bM_1\) loss term changes sign, and the middle
isotropy term changes sign, exactly as stated in the candidate.

For a horizontal loss \(u=r^2U\), division by the rows in (4.2) gives

\[
 \left(-2b{c_0\over c}U,
       -2b^3{c_0\over c}U^2,
       2b^2[-2U+r^2(1+c_0^2)U^2]\right)^T.
\]

The independent symbolic audit checks both incoming and outgoing radial
columns and this horizontal column identically, not merely at \(x=0\).
Multiplication by \(\kappa=cr\), the fine incoming column factor \(1/2\),
and the six row multipliers therefore reproduces every column of \(A\).

## 3. Disk bounds for the transition matrix

On \(|z|\le1/180\),

\[
 |\operatorname{sinc}z|,|\operatorname{cosc}z|\le2.
\]

The cancellation-free mask identities imply

\[
 |m_1|\le3|\alpha|^2,qquad |m_2|\le17|\alpha|^4,
 \qquad |M_1|,|M_2|<1.
\]

All base sine ratios and base cosines are at most \(3\), and all neighbor
sine ratios are in fact at most \(3\); retaining the submitted bound \(7\)
gives radial-column bounds

\[
 |F|<3,\qquad |G|<45,qquad |I|<103.
\]

The largest horizontal argument is the coarse jump eight,
\(16\pi x=16ar\).  Hence

\[
 U={|1-\cos(16\pi x)|\over|r|^2}le(16|a|)^2<17.
\]

Together with \(|c_f/c|<7/2\), the three horizontal bounds are

\[
 400,qquad55\,000,qquad700.
\]

Since every row multiplier is below \(16\), this proves
\(|A_{ij}|<10^6\) on the boundary disk.

## 4. Every transition right-hand-side row

For force and loss-force, row normalization of a baseline radial column
introduces \(1/(cr)\).  On \(|x|=10^{-4}\),

\[
 {1\over|cr|}\le{.251\over(6/7)\,3\,10^{-4}}<1000.
\]

Each baseline is a sum of two radial columns with total coefficient below
\(3\), so

\[
 |b_F|<16\cdot3\cdot3\cdot1000,qquad
 |b_G|<16\cdot3\cdot45\cdot1000.
\]

The exact symbolic audit proves that each corresponding numerator vanishes
at \(x=0\), and prints its filled-in value (5.2).  Because the numerator is
analytic and has a zero there, the quotient has a removable singularity.

The isotropy row is instead divided by \(h^2\).  It has no \(1/(cr)\)
quotient, and directly

\[
 |b_I|<16\cdot3\cdot103.
\]

Thus every one of the six RHS entries is below \(10^7\) on the disk.  After
filling in the two removable quotients per endpoint, maximum modulus applies
to the whole vector.  Since the actual interval
\(0\le x\le2^{-80}\) lies inside half the disk radius, Cauchy's estimate and
integration from zero give

\[
 {|A-A_0|\over x}\le2\cdot10^{10},
 \qquad {|b-b_0|\over x}\le2\cdot10^{11}.
\]

These are stronger than (6.1).  The Neumann and solution bounds (6.3)--(6.4)
then follow exactly as printed.

## 5. First-row adjugate and Cauchy guard

At \(h=0\), every entry of the normalized polar matrix has absolute value
below \(3\).  Indeed, its radial column is \((1,1/2,1)^T\), while a horizontal
column with \(0<t<2/3\) is

\[
 (-2a_0t,-2a_0^3t^2,4a_0^2(t^2-t))^T.
\]

Every \(2\times2\) minor is therefore below \(18\), a sharper explicit
adjugate bound than the submitted \(512\).  With

\[
 |\det A_{\rm pol}(0)|\ge {704\over6075},
\]

this gives

\[
 \|A_{\rm pol}(0)^{-1}\|_\infty
 <{54\over704/6075}<500<20\,000.
\]

The formulas (8.5)--(8.6) directly give
\(\|z_{\rm pol}(0)\|_\infty<64\) on the entire \((u,v)\)-box.
On \(|h|\le10^{-2}\), the normalized matrix and RHS are entire combinations
of sinc, cosc, and cosine.  Their boundary bounds imply

\[
 |\partial_hA_{\rm pol}|\le22\,000,
 \qquad |\partial_hb_{\rm pol}|\le1\,600.
\]

Using the deliberately looser inverse bound \(20\,000\) and
\(h\le44/(7\,2^{80})\), the Neumann product is below \(10^{-12}\) and the
solution displacement is below \(10^{-6}\).  Since the limiting minimum is
strictly above \(1/20\), finite first-row positivity follows.

## 6. Exact correction recommended for the candidate

Replace the three sentences beginning “The force/loss RHS before division by
\(cr\)” in the Cauchy audit commentary by:

> The force and loss-force RHS rows are removable quotients by \(cr\); their
> boundary values are bounded using \(1/|cr|<1000\).  The isotropy RHS has no
> such quotient and is bounded directly by \(16\cdot3\cdot103\).  The exact
> symbolic limit proves removability of the force and loss-force quotients,
> so maximum modulus applies to all six filled-in RHS entries.

No theorem constant or construction formula needs to change.
