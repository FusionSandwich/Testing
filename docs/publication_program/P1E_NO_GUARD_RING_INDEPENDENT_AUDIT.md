# Independent audit of the no-guard short-gap ring family

## Final verdict

**ACCEPTED FOR THE UNPERTURBED `d=3` CONSTRUCTION; THE FIXED-LEVEL ROBUSTNESS REPAIR IS PROVED ELSEWHERE; THE FORMER UNIFORM ROUTE IS REJECTED.**

The opening audit found five defects in an earlier submission.  Sections 4
and 5 repair the reachable integer-stencil margin and global transition
product estimate used by the unperturbed theorem. Sections 11 and 12 below record the final disposition: the unsupported
all-level compiler route is rejected, while the separate fixed-level theorem
uses the actual finite row systems and strict base margins. No literal emitted
program, verified operation count, complete denominator inventory, or uniform
recurrence certificate is claimed.

The integer schedule is well defined and closes exactly at the equator. The
reachable transition phase is smaller than the candidate's declared box, the
equal-gap recurrence is exact, and the proposed edge-length lower bound can
be proved with room to spare.

The first pass found:

1. an exact counterexample to the assertion that every ordinary band row has
   \(\phi_*/\delta\ge2\);
2. a logical gap in deriving the horizontal-conductance comparison from the
   loose box alone;
3. no all-orders certificate for the finite transition or first-ring
   matrices;
4. no proof of the transition recurrence estimate needed for the global
   conductance margin; and
5. a robustness scope broader than the row systems actually audited.

The first counterexample does not itself destroy positivity: at that row the
chosen jumps remain \(t_-=1,t_+=4\) and still bracket the target. It does mean
that the printed proof of the adaptive row had to be replaced by the wider
reachable-domain lemma proved in Section 4 and used in the final theorem.

## 1. Integer schedule and closure

Use

\[
 M_m=M_0 2^m,\quad S_0=M_J/8,\quad
 t_m^0=\frac{M_J}{4\pi}\arcsin(2^{m-J}),
\]

\[
 k_m=\operatorname{nint}(t_m^0-a_0-mg),\quad
 K=\operatorname{nint}(S_0-a_0-Jg),
\]

\[
 t_m=a_0+k_m+mg,\quad S=a_0+K+Jg,\quad h=\frac{\pi}{2S}.
\]

Nearest-integer rounding gives

\[
 |t_m-t_m^0|\le\frac12,\qquad |S-S_0|\le\frac12.
\]

The northern schedule starts at \(a_0h\), takes \(k_0\) ordinary gaps,
then alternates a short \(gh\) gap with \(k_{m+1}-k_m\) ordinary gaps, and
after the last short gap takes \(K-k_{J-1}\) ordinary gaps. The terminal
dimensionless latitude is exactly

\[
 a_0+k_{J-1}+(J-1)g+g+(K-k_{J-1})=S,
\]

so the last ring is at \(Sh=\pi/2\).

Since \(\arcsin(2x)-\arcsin x\ge x\),

\[
 t_{m+1}^0-t_m^0\ge\frac{M_m}{4\pi}>
 \frac{M_m}{13},
\]

and hence

\[
 k_{m+1}-k_m\ge\frac{M_m}{13}-g-1>0.
\]

Also \(k_0>0\), since \(t_0^0\ge M_0/(4\pi)\), and

\[
 S_0-t_{J-1}^0
 =M_J\left(\frac18-\frac1{24}\right)=\frac{M_J}{12},
\]

so \(K-k_{J-1}>0\). These inequalities are overwhelming for
\(M_0=2^{80}\).

## 2. Sharper reachable transition box

For

\[
 a(M,S,t)=\frac{2S}{M}\sin\left(\frac{\pi t}{2S}\right)
\]

one has

\[
 |\partial_ta|\le\frac{\pi}{M},\qquad
 |\partial_Sa|=\frac2M|\sin\theta-\theta\cos\theta|.
\]

Every transition has \(\theta\le\pi/6+2h\). Since
\(\sin\theta-\theta\cos\theta\) is increasing and its value at \(\pi/6\)
is less than \(1/20\), the tiny declared \(h\) permits the rational guard
\(1/19\). Thus

\[
 \boxed{\left|M_m(a_m-\tfrac14)\right|
 <\frac{\pi}{2}+\frac1{19}
 <\frac{11}{7}+\frac1{19}
 =\frac{216}{133}<2.}                              \tag{2.1}
\]

The fixed-\(g\) transition therefore need only be certified on

\[
 |M(a-\tfrac14)|\le2,\qquad 6/7\le c\le1.           \tag{2.2}
\]

The limiting formulas remain strictly positive on (2.2), with the old
\(1/500\) lower bound. This is only a limiting statement until the literal
finite matrix receives an outward remainder certificate.

## 3. Exact counterexample to the ordinary-row premise

The candidate claims every ordinary row after the first satisfies

\[
 \frac{\phi_*}{\delta}\ge2,\qquad
 \phi_*=\arccos(1-z_*),\quad
 z_*=\frac{1-\cos h}{\sin^2\theta},\quad
 \delta=\frac{2\pi}{M}.                              \tag{3.1}
\]

This is false at the last northern ordinary row of level \(J=1\).
Put \(M=M_1=2^{81}\). Since \(2<a_0+g<5/2\), rounding gives

\[
 S=S_0+e,\qquad e=g-\frac23>0.                       \tag{3.2}
\]

At the last ordinary row, \(\theta=\pi/2-h\), so

\[
 z_*=\frac{1-\cos h}{\cos^2h},\qquad
 h=\frac{\pi}{2S}<\frac{4\pi}{M}=2\delta.            \tag{3.3}
\]

Let \(H=4\pi/M\) and \(q=8e/M\), so \(h=H/(1+q)\). The bounds

\[
 1-\cos H\ge\frac{H^2}{2}-\frac{H^4}{24},\qquad
 z_*\le\frac{h^2}{2(1-h^2)}
\]

show \(z_*<1-\cos H\). After division by \(H^2\), the exact inequality is

\[
 \frac12-\frac{H^2}{24}
 -\frac{1}{2(1+q)^2\{1-H^2/(1+q)^2\}}>0.             \tag{3.4}
\]

The left side decreases with \(H^2\); substituting \(\pi<22/7\),
\(M=2^{81}\), and \(e=\sqrt{29/32}-2/3\) leaves a positive exact algebraic
number. Hence

\[
 z_*<1-\cos(2\delta),\qquad
 \boxed{\phi_*/\delta<2.}                            \tag{3.5}
\]

This exact counterexample is repairable. Here \(R=\phi_*/\delta\) differs
from \(2\) by only \(O(M^{-1})\), and the rule still chooses
\(t_-=1,t_+=4\). The schedule gives \(R>19/10\): indeed
\(\phi_*>h\). On the cap, \(a=\pi\sin\theta/(M_0h)\) is maximized at
the first transition; on each later constant-count band it is maximized at
the next transition; and on the last band it is maximized at the equator.
Equation (2.1) and \(|S-S_0|\le1/2\) therefore give, on every ordinary row,
\[
 a=\frac{\pi\sin\theta}{Mh}\le\frac14+\frac2M.
\]
Since \(M\ge2^{80}\) and \(h<1/100\),
\[
 a<\frac{251}{1000},\qquad
 \frac{\sin(h/2)}h>\frac{499}{1000}.
\]
Consequently
\[
 R\ge\frac{M\sin(h/2)}{\pi\sin\theta}
 =\frac{\sin(h/2)}{ah}>
 \frac{499}{251}>\frac{19}{10}.
\]
A correct proof should use this reachable bound, not the false lower bound
\(2\).

Also every ordinary row after the first has \(\theta\ge7h/3\). Since the
declared \(h<1/100\),

\[
 \sin\theta\ge\sin(7h/3)>\frac{23}{10}h,
\]

and therefore

\[
 z_*=\frac{1-\cos h}{\sin^2\theta}
 <\frac{h^2/2}{(23h/10)^2}<\frac1{10}.
\]

The Taylor lower bound

\[
 1-\cos(1/2)\ge\frac18-\frac1{384}>\frac1{10}
\]

then gives \(\phi_*<1/2\).

## 4. Adaptive horizontal brackets

For \(R=\phi_*/\delta\),

\[
 x(t)=\frac{1-\cos(t\delta)}{1-\cos\phi_*}
 =\frac{\sin^2(t\phi_*/(2R))}{\sin^2(\phi_*/2)}.
\]

When \(R\ge2\), the printed floor/ceiling choices give

\[
 \frac1{32}<x_-<\frac13,\qquad 2<x_+<10.
\]

The bounds persist on the reachable closure interval below \(R=2\), but
require a separate \(19/10<R<2\) case.

The loose rectangle alone does not imply that every horizontal conductance
is at least \(U_-/100\). At the formal corner
\(x_-\to1/3,x_+\to10\), the limiting upper-stencil ratio is below \(1/100\).
The actual integer rule is better: at its worst ceiling event,
\(R\downarrow2\) from above, \(t_-=1,t_+=5\), and

\[
 x_-\to\frac14,\quad x_+\to\frac{25}{4},\quad
 \frac{1-x_-}{x_+(x_+-x_-)}\to\frac1{50}.            \tag{4.1}
\]

Thus \(1/100\) is plausible for the reachable rule, but must be proved from
the floor/ceiling relation, not by substituting the loose box.

### Lemma 4.1 (reachable floor/ceiling margin)

On every ordinary row after the first,

\[
 \frac{19}{10}<R,\qquad 0<\phi_*<\frac12.
\]

Let

\[
 \lambda_-=\frac{t_-}{R},\qquad
 \lambda_+=\frac{t_+}{R}.
\]

For \(R\ge2\), the floor rule gives

\[
 \frac14\le\lambda_-\le\frac12.
\]

For \(19/10<R<2\), it gives \(t_-=1\), hence

\[
 \frac12<\lambda_-<\frac{10}{19}.
\]

The ceiling rule always gives

\[
 2\le\lambda_+<2+\frac1R<\frac{48}{19}.              \tag{4.2}
\]

Put \(t=\phi_*/2<1/4\). Since \(\sin x/x\) decreases on
\((0,\pi)\),

\[
 x_-=\frac{\sin^2(\lambda_-t)}{\sin^2t}
 \ge\lambda_-^2\ge\frac1{16}.                        \tag{4.3}
\]

Using \(\sin y\le y\) and
\(\sin t\ge t(1-t^2/6)>95t/96\) gives

\[
 x_-<
 \left(\frac{10}{19}\frac{96}{95}\right)^2
 <\frac13,                                           \tag{4.4}
\]

\[
 x_+<
 \left(\frac{48}{19}\frac{96}{95}\right)^2
 <7.                                                  \tag{4.5}
\]

Because \(\lambda_+\ge2\), \(\lambda_+t<12/19<\pi/2\), and sine is
increasing there,

\[
 x_+\ge\frac{\sin^2(2t)}{\sin^2t}
 =4\cos^2t>2.                                        \tag{4.6}
\]

These estimates prove the reachable brackets without the false premise
\(R\ge2\).

### Lemma 4.2 (actual horizontal-conductance margin)

Let

\[
 T=\frac{(1-\cos h)U_-}{s^2K}.
\]

The exact ordinary formulas give

\[
 T=\frac{1-\cos h}{\sin^2h}
 \left[
 2-\frac{(1+c^2)(1-\cos h)}{s^2}
 -\frac{c\sin h}{s}
 \right].                                            \tag{4.7}
\]

For ordinary rows, \(\theta\ge7h/3\). The tiny declared \(h\) gives

\[
 \tan(h/2)<\frac{11}{20}h,\qquad
 z=\tan(h/2)\cot\theta<\frac{33}{140}.
\]

The proof of \(0<\phi_*<1/2\) gives
\((1-\cos h)/s^2<1/10\), while

\[
 \frac{c\sin h}{s}=2z\cos^2(h/2)<\frac{33}{70}.
\]

Since

\[
 \frac{1-\cos h}{\sin^2h}
 =\frac{1}{2\cos^2(h/2)},
\]

one obtains the explicit box

\[
 \boxed{\frac35<T<\frac{101}{100}.}                  \tag{4.8}
\]

Now

\[
 \frac{H_-}{U_-}
 =\frac{x_+-1}{x_-(x_+-x_-)T},\qquad
 \frac{H_+}{U_-}
 =\frac{1-x_-}{x_+(x_+-x_-)T}.                       \tag{4.9}
\]

Using (4.3)--(4.6) and (4.8),

\[
 \frac{H_+}{U_-}>
 \frac{(2/3)}{7^2(101/100)}
 >\frac1{100},
\]

\[
 \frac{H_-}{U_-}>
 \frac{1}{(1/3)7(101/100)}
 >\frac1{100}.                                       \tag{4.10}
\]

For the upper bounds, each interpolation fraction is less than one,
\(x_->1/16\), \(x_+>2\), and \(T>3/5\), so

\[
 \boxed{\frac1{100}U_-<H_\pm<100U_-.}                \tag{4.11}
\]

This is the fixed fractional ordinary-row margin needed by the global
conductance argument.

## 5. Ordinary recurrence and global reconciliation

For equal meridional gaps, elimination gives exactly

\[
 \frac{U_+}{U_-}
 =\frac{(1-z)(1+2z)}{(1+z)(1-2z)},\qquad
 z=\tan(h/2)\cot\theta.                              \tag{5.1}
\]

Also

\[
 \frac{\sin(\theta+h/2)}{\sin(\theta-h/2)}
 =\frac{1+z}{1-z}.
\]

The logarithmic remainder is

\[
 E(z)=2\log(1-z)-2\log(1+z)
 +\log(1+2z)-\log(1-2z),                            \tag{5.2}
\]

and for \(0<z<2/5\),

\[
 0\le E(z)\le\frac{16z^3}{1-4z^2}.                  \tag{5.3}
\]

The sine quotient therefore telescopes. The cap total \(<12\) and band
total \(<1\) are safely obtainable, though the cap denominator \(>3/4\)
needs a sharper estimate such as \(\tan(h/2)<(11/20)h\), not merely
\(\tan(h/2)\le h\).

The remaining global step is

\[
 \frac{2U_{+,f}\sin(\theta-h/2)}
      {\sin(\theta+(g+1/2)h)}
 =1+\varepsilon_m,\qquad
 |\varepsilon_m|\le\frac{10^4}{M_m}.                \tag{5.4}
\]

This is consistent with the limiting transition solution, but no outward
derivation is printed. It follows cheaply once the transition certificate
gives \(|A_f|<7\). Indeed \(a>1/5\) implies

\[
 0<\kappa=\frac{\pi c}{Ma}<\frac{16}{M},\qquad
 |2U_{+,f}-1|=2\kappa|A_f|<\frac{224}{M}.
\]

With

\[
 \rho=\frac{\sin(\theta-h/2)}
 {\sin(\theta+(g+1/2)h)},
\]

monotonicity of sine on the northern construction gives \(0<\rho\le1\), and

\[
 1-\rho
 \le\frac{(g+1)h}{\sin\theta}
 =\frac{(g+1)\pi}{Ma}<\frac{32}{M}.
\]

Therefore

\[
 |\varepsilon_m|
 =|(2U_{+,f})\rho-1|
 <\frac{256}{M_m}<\frac{10^4}{M_m}.                 \tag{5.5}
\]

Thus (5.4) is not an independent theorem-strength gap; it is a missing
three-line consequence of the finite transition bound. The global
conductance margin remains conditional on that finite bound and on the
reachable adaptive comparison.

If (5.4), transition positivity, first-row positivity, and the reachable
adaptive comparison are certified, the huge margin

\[
 M_0^{-20}\le\gamma_e\le M_0^{20}
\]

is sufficient: ordinary remainders have summable logarithms, transition
errors sum geometrically, mask entries are \(>1/64\), and all other local
ratios are fixed.

## 6. First ring and equator

The removable first-ring solution is correct. With incoming pole conductance
one and \(a_0=4/3\), direct solution gives \(U_+=128/33\) and the two
horizontal formulas printed in the candidate. Their rational box gives
positive limiting coefficients but does not replace the finite-\(h\)
enclosure because the horizontal angles are \(O(1)\).

At the equator, reflection gives equal opposite radial tangent vectors.
Force and loss-force cancel, and the exact covariance equation is

\[
 H_{\rm eq}=\frac{U\sin^2h}{\sin^2(2\delta_J)}.
\]

Thus the equatorial formula is correct.

## 7. Active angular lower bound

The claimed lower bound \(h/8\) is compatible with every row class:

- ordinary radial edges have angle \(h\);
- pole edges have angle \(a_0h\);
- transition radial edges have angle at least \(gh\);
- adaptive edges use \(x_->1/32\) and
  \(1-\cos h>h^2/3\), giving chord \(>h/\sqrt{48}>h/8\);
- the fine transition jump-one chord obeys
  \[
  \frac{\operatorname{chord}}h
  \ge\frac{2a_m}{\pi}>\frac{2}{5\pi}>\frac18;
  \]
- the first-ring and equatorial horizontal jumps have larger margins.

Consequently

\[
 \ell_{\min}\ge\frac{h^2}{32\pi^2},\qquad
 r_{\max}\le64\pi^2h^{-2}
\]

once the conductance construction is complete.

## 8. Robustness scope after repair

The local systems use exact cyclic and reflection symmetry. Arbitrary
independent node perturbations remain outside their scope. Independent ring
rotations change aligned radial moments and can destroy the three-even-equation
reduction; changes of masks, phases, jumps, poles, equator or support likewise
require a different theorem.

The fixed-level repair permits unequal meridional gaps. For one fixed
production level, keep every discrete support choice and incidence fixed and
use all northern non-equatorial latitudes as a finite parameter vector. The
first-row, ordinary, transition and equatorial systems assemble into one finite
block-lower-triangular shared-conductance system. Its diagonal blocks are
nonsingular at the strictly positive unperturbed point, so analytic continuity
and the Neumann lemma provide a computable level-dependent radius. This avoids
the false claim that one normalized $O(h^2)$ derivative estimate works
uniformly over all latitudes and all refinement levels.

One common ambient rotation is exact. No lower bound on the latitude radius
uniform in the level is proved.

## 9. Current promotion boundary

The unperturbed construction has the required schedule, transition and polar
certificates, adaptive horizontal margins, shared recurrence, exact generator,
and sampled quotient proof. The separate robustness source adds the accurately
scoped fixed-level theorem. Promotion beyond that theorem would require new
evidence for at least one of the following:

1. a level-uniform inverse and positivity margin;
2. a literal all-level expression graph and independently checked derivative
   certificate;
3. a uniform shared-recurrence estimate under perturbation; or
4. a global right inverse covering arbitrary support or longitude motion.

No such stronger statement is active.

## 10. Reproduction

Run the exact regression:

    python afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py

It verifies the level-\(1\) counterexample, sharper phase constant, limiting
adaptive factor, recurrence identities, first-ring formula, and rate
arithmetic. It is not a replacement for the missing interval proofs.

## 11. Rejected all-level straight-line majorant

An earlier draft proposed bounding a cancellation-free straight-line program
by a doubly exponential constant derived from a nominal operation count. That
route is **rejected as uncertified**. The repository did not contain the
literal emitted expression graph, an automatically verified operation count,
a complete denominator-separation list, or independent interval checks for
all normalized first-row, ordinary, transition, equatorial, and recurrence
expressions. A recurrence for an abstract operation bound is not a certificate
for an unspecified program.

Accordingly, no enormous constant from that draft has theorem or value-registry
status. The determinant formulas, limiting transition cone, first-row
adjugate, and recurrence identities in the preceding sections remain useful
for the unperturbed theorem and for fixed-level nonsingularity. They do not
supply a uniform inverse or positivity margin across refinement levels.

## 12. Fixed-level support-preserving theorem

The strongest correct perturbation result is proved in
`P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md`. For every fixed production level of the declared `M_0=2^80` family,
keep the ring counts, longitude phases, radial masks, horizontal jumps, pole,
equator, reflection, and literal edge incidences fixed. The northern
non-equatorial latitudes are a finite parameter vector, and the exact shared
moment equations form a finite block-lower-triangular system. The diagonal
first-row, ordinary, transition, and equatorial blocks are nonsingular at the
strictly positive unperturbed point. Analytic dependence and the Neumann lemma
give a unique positive solution on a computable level-dependent neighborhood.

This fixed-level result preserves reversibility, connectivity, exact
`H_0 direct-sum H_1` fidelity, and the rowwise scalar quadratic residual. After
shrinking the neighborhood to preserve the active chord window, it gives
`r_max<=1024 h_J^-2` and `mathfrak D_2<=54 h_J^2`. One common ambient rotation
is permitted. No lower bound on the radius uniform in `J` is asserted.

The finite solver and certificate verifiers are regression and interface
checks. The committed certificate is explicitly a conformance fixture, not a
production radius. Independent longitude perturbations, arbitrary node
motion, support changes, and higher-dimensional claims remain excluded.
