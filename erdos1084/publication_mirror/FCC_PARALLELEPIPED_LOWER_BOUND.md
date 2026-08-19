# FCC parallelepiped lower construction

Math source provenance:

```text
FusionSandwich/Math
branch: agent/erdos-1084-target-a-publication-20260819
source head: f805b022bf947a28d7dfedc40e638d1849534eb3
```

Let

\[
u_1=(0,1,1)/\sqrt2,
\quad
u_2=(1,0,1)/\sqrt2,
\quad
u_3=(1,1,0)/\sqrt2.
\]

For positive integers `a,b,c`, the FCC parallelepiped

\[
X_{a,b,c}
=\{iu_1+ju_2+ku_3:0\le i<a,0\le j<b,0\le k<c\}
\]

has `abc` points and exactly

\[
E(a,b,c)=6abc-3ab-3ac-3bc+a+b+c
\]

unit-distance pairs. The six positively oriented contact directions are

\[
u_1,u_2,u_3,u_1-u_2,u_1-u_3,u_2-u_3.
\]

For `a=b=c=m`,

\[
f_3(m^3)\ge6m^3-9m^2+3m.
\]

For arbitrary positive `n`, let `m=floor(n^(1/3))` and append `t=n-m^3` FCC points along the continuing `u_1` contact chain. Every appended point contributes at least one new contact and `t<3m^2+3m+1`, giving

\[
f_3(n)>6n-24n^{2/3}-12n^{1/3}-5.
\]

This proves the secondary order `n^(2/3)` from below. It does not determine the exact normalized-deficit constant.