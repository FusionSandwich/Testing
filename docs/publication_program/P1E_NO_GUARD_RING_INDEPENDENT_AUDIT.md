# Independent audit of the no-guard short-gap ring family

## Final verdict

**ACCEPTED AS AN INDEPENDENT AUDIT OF THE COMPLETE \(d=3\) THEOREM.**

The opening audit found five defects in an earlier submission.  Sections 4,
5, 11, and 12 below supply the reachable integer-stencil margin, the global
transition product estimate, an analytic all-orders closure, and the
support-preserving robustness theorem.  The final construction source uses
the sharper rational Cauchy certificates in
`P1E_SHORT_GAP_S2_CONSTRUCTION.md` with \(M_0=2^{80}\); those certificates
replace the deliberately gigantic fallback constant in Section 11.  The
earlier failures are retained here as hostile regressions, not as current
blockers.

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

## 8. Robustness scope

The local systems use exact cyclic and reflection symmetry. Arbitrary
independent node perturbations are outside their scope.

Even “structured ring perturbations” is presently too broad. Independent
\(O(h^3)\) changes of ring latitudes make ordinary gaps unequal, so (5.1)
no longer applies. Independent rotations of rings change aligned radial
moments and can destroy the three-even-equation reduction. No matrices or
global recurrence are given for either perturbation.

The printed \(O(h^2)\) scaled-change claim is also false uniformly across
latitudes. At a transition with \(\theta\) bounded away from zero, changing
one ring latitude by \(O(h^3)\) changes a radial
\(\ell\tau=O(h^3)\) column by \(O(h^5)\). The loss-force normalization is
\(1/(h^4\cot\theta)=O(h^{-4})\), so the normalized change is \(O(h)\), not
\(O(h^2)\). This still tends to zero and may preserve a fixed positivity
margin, but it needs the correct bound.

Currently justified are ambient rotations and small parameter changes which
preserve every orbit, the literal support, equal ordinary gaps, and the
transition block form, provided the missing interval certificates are
uniform on that box. Any broader result needs unequal-gap row matrices and
their shared recurrence or a global right inverse for the full six-moment
edge system.

## 9. Historical promotion boundary

At this stage of the audit the route still required:

1. a literal outward certificate for the finite transition system on (2.2);
2. a literal outward certificate for the finite first-ring system;
3. a corrected adaptive proof including \(19/10<R<2\);
4. a floor/ceiling horizontal-conductance margin proof;
5. inclusion of the transition recurrence estimate (5.5);
6. a generator instantiating each undirected edge once and checking every
   row class; and
7. an accurately scoped perturbation theorem.

The exact schedule, ordinary recurrence, equator row, quotient
factorization, rate implication, and limiting transition cone can be
retained. They do not alone complete the all-level family.

## 10. Reproduction

Run the exact regression:

    python afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py

It verifies the level-\(1\) counterexample, sharper phase constant, limiting
adaptive factor, recurrence identities, first-ring formula, and rate
arithmetic. It is not a replacement for the missing interval proofs.

## 11. An explicit analytic all-orders closure

The remaining finite transition and first-row margins can be closed without
fitted slopes or a finite list of levels. The price is replacing \(2^{80}\)
by one much larger, but completely explicit, fixed dyadic.

### Lemma 11.1 (straight-line \(C^1\) compiler)

Suppose a cancellation-free straight-line program has at most \(L\)
arithmetic nodes. Its leaves and analytic atoms have value and
\(\varepsilon\)-derivative bounds at most \(2^{16}\), and every reciprocal
denominator is at least \(2^{-6}\). Let \(W_k\) bound both values and
derivatives after node \(k\). For addition, multiplication, and reciprocal,
respectively,

\[
 W_{k+1}\le2W_k,\qquad
 W_{k+1}\le2W_k^2,\qquad
 W_{k+1}\le2^{12}W_k.
\]

Since \(W_k\ge1\), all three are bounded by

\[
 W_{k+1}\le2^{12}W_k^2.
\]

Writing \(W_k\le2^{e_k}\), \(e_0=16\), gives

\[
 e_{k+1}=12+2e_k,\qquad
 e_L=28\cdot2^L-12.                                  \tag{11.1}
\]

Thus every output has

\[
 |\partial_\varepsilon F|\le
 K_L:=2^{28\cdot2^L}.                                \tag{11.2}
\]

This is a literal induction, not an appeal to compactness.

### Transition application

Use

\[
 \varepsilon=M^{-1},\qquad
 a=\frac14+\eta\varepsilon,\quad |\eta|\le2,\qquad
 r=\frac{\pi\varepsilon}{a},\qquad \kappa=cr.
\]

Rewrite every occurrence of sine and cosine using \(\operatorname{sinc}\)
and \(\operatorname{cosc}\), factor the powers of \(s=\sqrt{1-c^2}\) and
\(r\) cancelled by the row normalization, and use the cancellation-free
mask moments. The only reciprocal guards are consequences of

\[
 a>\frac15,\qquad c\ge\frac67,\qquad
 c_\alpha>\frac9{10},\qquad g>\frac9{10};
\]

they are all stronger than \(2^{-6}\). On arguments of absolute value at
most \(1/2\), sinc, cosc, and their first derivatives satisfy the leaf bound
\(2^{16}\).

The right-hand sides contain differences whose separately normalized
summands would have artificial \(r^{-1}\) or \(r^{-k}\) poles. They must be
combined before division. Introduce the finite atom list

\[
 \frac{f(\lambda r)-
 \sum_{j<k}f^{(j)}(0)(\lambda r)^j/j!}{r^k},
 \qquad 1\le k\le4,                                  \tag{11.2a}
\]

for \(f=\sin,\cos,\operatorname{sinc},\operatorname{cosc}\) and the finitely
many constants \(\lambda\) in the two transition rows. Taylor's formula
defines these atoms at \(r=0\), and on \(|\lambda r|\le1/2\) bounds their
values and first \(r\)-derivatives by \(2^{16}\). Thus no reciprocal by
\(r\), \(s\), or \(1-c\) occurs in the cancellation-free DAG. Checking that
every numerator has the stated zero order is a finite polynomial identity
obtained from the row formulas and is part of the DAG emitter, not a
numerical limit.

The six-by-six system, including all 42 matrix/right-hand-side entries,
uses far fewer than

\[
 L=10^6
\]

nodes when written without expansion. This bound can be checked simply by
assigning one node to every displayed arithmetic operation; it is
intentionally six orders of magnitude looser than the literal formula.
The fundamental theorem of calculus and (11.2) then give

\[
 \|A-A_0\|_{\max},\ \|b-b_0\|_\infty
 \le\frac{K_L}{M}.                                   \tag{11.3}
\]

The limiting data satisfy

\[
 \|A_0^{-1}\|_\infty<3,\qquad
 \|A_0^{-1}b_0\|_\infty<7,\qquad
 \min(A_0^{-1}b_0)>\frac1{500}.
\]

If \(M>2^{20}K_L\), the Neumann lemma gives

\[
 \|A^{-1}b-A_0^{-1}b_0\|_\infty<\frac1{1000},
\]

so every finite transition coefficient is positive.

### First-row application

After dividing its three equations by \(h,h^3,h^2\), the limiting first-row
matrix is

\[
 A_P=
 \begin{pmatrix}
 1&-2au&-2av\\
 1/2&-2a^3u^2&-2a^3v^2\\
 1&-4a^2u(1-u)&-4a^2v(1-v)
 \end{pmatrix},
\]

and

\[
 \det A_P=4a^3uv(a-1)(2a+1)(u-v).                   \tag{11.4}
\]

For \(a=4/3\), \(1/20<u<1/10\), and \(1/2<v<2/3\),

\[
 |\det A_P|>\frac{704}{6075}>\frac19.                \tag{11.5}
\]

Every adjugate entry is less than \(512\) in absolute value, so

\[
 \|A_P^{-1}\|_\infty<2^{14}.                         \tag{11.6}
\]

The limiting solution has norm less than \(64\) and minimum greater than
\(1/20\). The cancellation-free normalized finite matrix has the same atom
and denominator guards as above and fewer than \(10^6\) nodes. Therefore
the same \(K_L\) bounds its change, and \(M_0>2^{40}K_L\) preserves a
positive margin.

### One explicit choice

Take

\[
 L=10^6,\qquad
 N=28\cdot2^{10^6}+100,\qquad
 \boxed{M_0=2^N.}                                    \tag{11.7}
\]

Then \(M_0>2^{100}K_L\), so both the transition and first-row Neumann
arguments close. All schedule, degree, separation, rate, and defect
arguments use only that \(M_0\) is a fixed dyadic above their stated lower
thresholds, and remain valid after this replacement.

To turn Lemma 11.1 into a machine audit, the generator should emit the
cancellation-free expression DAG and count its nodes while checking the
listed reciprocal guards. The mathematical proof is the induction
(11.1), not the numerical evaluation of any refinement level.

## 12. A rigorously support-preserving perturbation theorem

The analytic closure also supplies a nontrivial robustness statement, but
only within the symmetry class actually used by the construction.

For one level, perturb each northern ring latitude by

\[
 |\theta_k'-\theta_k|\le h^3,
\]

fix the pole and equator, and reflect the perturbation into the southern
hemisphere. Keep every ring count, longitude phase, radial mask, and
horizontal jump integer unchanged. Allow one common ambient rotation of the
whole configuration. For the dyadic (11.7), all perturbed meridional gaps
remain positive and in \([g h/2,2h]\).

At an ordinary row, prescribe the incoming shared radial conductance and
solve the full three even equations for the outgoing radial conductance and
the two horizontal conductances. At the unperturbed row this matrix is
invertible: its explicit solution has

\[
 U_+>0,\qquad U_-/100<H_\pm<100U_-,
\]

and the determinant factors consist only of the positive radial factor,
\(x_+-x_->0\), and the positive factor \(T\) in (4.8). The same
cancellation-free \(C^1\) compiler bounds the inverse uniformly.

Indeed, before harmless row normalizations, with
\(A_h=\sin h\), \(\ell=1-\cos h\), and horizontal losses \(u,v\), the
determinant of the three columns \((U_+,H_u,H_v)\) is exactly

\[
 4A_hcs^3uv(u-v)
 \left\{2s^2-(1+c^2)\ell-A_hcs\right\}.              \tag{12.1}
\]

The last brace equals the positive bracket in (4.7) times \(s^2\), and
\(u-v\ne0\) by (4.3)--(4.6).

An \(O(h^3)\) latitude displacement changes an ordinary force column by
\(O(h^3)\), a loss-force column by \(O(h^5)\), and a covariance column by
\(O(h^4)\). After the natural ordinary-row normalizations
\(h,h^3,h^2\), every normalized change is \(O(K_Lh^2)\). Thus all ordinary
coefficients retain half their positive margins. Summed over \(O(h^{-1})\)
ordinary rows, their logarithmic recurrence perturbation is
\(O(K_Lh)\).

At a transition the loss-force baseline has one additional cancellation, so
the normalized perturbation is only bounded by \(O(K_Lh)\), as noted in
Section 8. There are \(J\) transitions and

\[
 Jh\le\frac{7J}{M_0 2^J}\le\frac7{M_0}.
\]

Hence their total logarithmic perturbation is \(O(K_L/M_0)\). The first row
is handled by (11.4)--(11.6), and the equator remains exact by reflection
with its positive horizontal coefficient re-solved explicitly.

Because (11.7) gives \(K_L/M_0<2^{-100}\), all local coefficients stay
positive and the global conductance product changes by less than a fixed
factor two. The perturbed family therefore remains positive, reversible,
exact on \(H_0,H_1\), and satisfies the same \(O(h^2)\) quotient bound with
slightly enlarged edge-window constants.

This theorem does not cover independent longitude perturbations or arbitrary
node motion. Those destroy the reflection reduction and still require a
global six-moment right inverse.
