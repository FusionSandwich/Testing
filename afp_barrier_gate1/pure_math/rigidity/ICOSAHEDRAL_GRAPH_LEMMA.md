# The five-regular spherical-triangulation graph lemma

## Statement

Let `G` be a finite simple graph cellularly embedded in `S^2`. Assume:

1. every face is a triangle; and
2. every vertex has degree five.

Then `G` is isomorphic, as an embedded graph, to the icosahedral graph.

This note supplies the finite combinatorial step used by the Prompt 3
geodesic-triangulation classification. It does not use a graph-enumeration
program.

## 1. Counts

Write `V,E,F` for the numbers of vertices, edges, and faces. Degree and face
incidence give

```text
5V=2E,
3F=2E.
```

Euler's identity gives `V-E+F=2`. Eliminating `E,F` yields

```text
V=12,
E=30,
F=20.
```

## 2. There is no separating triangle

Suppose a triangular cycle `T` is not a face. It separates the sphere into two
triangulated disks with common boundary `T`. Consider one side and let `n` be
the number of its interior vertices.

Every interior vertex has all five incident edges on that side. For a
triangulated disk with triangular boundary, the disk-curvature identity is

```text
sum_interior (6-deg_D x) + sum_boundary (4-deg_D x) = 6.
```

The interior contribution is `n`. If `S` denotes the number of incidences
between boundary vertices and interior vertices on this side, then the three
boundary degrees sum to `6+S`, so the boundary contribution is `6-S`.
Therefore

```text
n+6-S=6,
S=n.
```

The interior degree sum is consequently

```text
5n=S+2E_int=n+2E_int,
```

and hence

```text
E_int=2n.
```

For `n<=2` this already exceeds the number of edges in a simple graph. For
`3<=n<=5`, planarity gives `E_int<=3n-6<2n`. Thus each side of a separating
triangle contains at least six interior vertices.

The two sides would therefore contain at least twelve interior vertices, in
addition to the three vertices of `T`, contradicting `V=12`. Every triangular
cycle is a face.

## 3. Expand the link of one vertex

Fix a vertex `x`. Its five neighbors occur cyclically in its link; write them

```text
a_0,a_1,a_2,a_3,a_4
```

with indices modulo five. The link edges `a_i a_(i+1)` are present.

There is no edge between nonconsecutive link vertices. Such an edge together
with `x` would form a triangular cycle that is not one of the five faces
incident to `x`, contradicting Section 2. Thus the graph induced by the link
is exactly a five-cycle.

For each link edge `a_i a_(i+1)`, let `b_i` be the third vertex of the face on
the side opposite `x`.

### 3.1 Each `b_i` lies outside the closed star of `x`

It is not `x`, because the two faces incident to an edge are distinct. If it
were another `a_j`, the triangle

```text
a_i a_(i+1) a_j
```

would require a nonconsecutive chord of the five-cycle, which Section 2 has
excluded.

### 3.2 The five vertices `b_i` are distinct

Adjacent values cannot agree. If `b_(i-1)=b_i=b`, then the cyclic link of
`a_i` consists of only the four vertices

```text
x, a_(i-1), b, a_(i+1),
```

because the four incident triangular faces around `a_i` are already fixed.
That contradicts `deg(a_i)=5`.

Suppose two nonadjacent values agree. On a five-cycle their indices have
cyclic distance two, say `b_i=b_(i+2)=b`. Then `b` is adjacent to both
`a_(i+1)` and `a_(i+2)`. Hence

```text
b a_(i+1) a_(i+2)
```

is a triangular cycle. Section 2 says it is a face. It is the unique face on
the side opposite `x` along `a_(i+1)a_(i+2)`, so `b=b_(i+1)`. This contradicts
the adjacent-distinct conclusion.

Thus `b_0,...,b_4` are five distinct vertices outside `x` and its link.
Exactly one vertex remains; call it `y`.

## 4. Force the second five-cycle and the opposite pole

The degree-five vertex `a_i` already has the five distinct neighbors

```text
x, a_(i-1), a_(i+1), b_(i-1), b_i.
```

Its link is a five-cycle. The two consecutive faces

```text
a_i a_(i+1) b_i,
a_i a_(i-1) b_(i-1)
```

force `b_(i-1)b_i` to be an edge. Hence the vertices `b_i` form a second
five-cycle.

Now `b_i` has the four distinct neighbors

```text
a_i, a_(i+1), b_(i-1), b_(i+1).
```

Its fifth neighbor cannot be any `a_j` or nonconsecutive `b_j`, because that
would create a nonfacial triangular cycle or a chord in one of the already
identified links. The only remaining vertex is `y`. Therefore `y` is adjacent
to every `b_i`.

The complete adjacency is now forced:

```text
x -- all a_i,
a_i -- a_(i-1), a_(i+1), b_(i-1), b_i,
b_i -- b_(i-1), b_(i+1), a_i, a_(i+1), y,
y -- all b_i.
```

This is the standard two-pole, two-pentagon presentation of the icosahedral
graph. The face cycles are also forced, so the embedded graph is the
icosahedral triangulation.

## 5. Role in Prompt 3

The graph lemma uses only:

- simplicity;
- a cellular spherical triangulation;
- degree five; and
- Euler/planarity.

The Prompt 3 theorem establishes all four hypotheses before invoking this
lemma. The subsequent geometric identification with the regular icosahedron
uses equal chord-triangle faces and convex Cauchy rigidity, which is a separate
step.
