from fractions import Fraction as Q
from typing import Sequence, Tuple

Vec2 = Tuple[Q, Q]


def weighted_sum(weights: Sequence[Q], vectors: Sequence[Vec2]) -> Vec2:
    return (
        sum((w * u[0] for w, u in zip(weights, vectors, strict=True)), Q(0)),
        sum((w * u[1] for w, u in zip(weights, vectors, strict=True)), Q(0)),
    )


def run() -> None:
    e1: Vec2 = (Q(1), Q(0))
    e2: Vec2 = (Q(0), Q(1))

    # Outside, boundary, and full relative-interior tangent hulls.
    outside = [e1, e2]
    assert all(u[0] + u[1] > 0 for u in outside)
    boundary = [e1, (Q(-1), Q(0)), e2]
    assert weighted_sum([Q(1, 2), Q(1, 2), Q(0)], boundary) == (Q(0), Q(0))
    interior = [e1, (Q(-3, 5), Q(4, 5)), (Q(-3, 5), Q(-4, 5))]
    lam = [Q(3, 8), Q(5, 16), Q(5, 16)]
    assert all(x > 0 for x in lam) and sum(lam, Q(0)) == 1
    assert weighted_sum(lam, interior) == (Q(0), Q(0))
    rates = [4 * x for x in lam]
    assert sum((a * Q(1, 2) for a in rates), Q(0)) == 2

    # Repeated/redundant indexed directions and nonuniqueness.
    repeated = [e1, (Q(-1), Q(0)), e2, (Q(0), Q(-1)), e1]
    for split in (Q(1, 16), Q(1, 8), Q(3, 16)):
        weights = [split, Q(1, 4), Q(1, 4), Q(1, 4), Q(1, 4) - split]
        assert all(x > 0 for x in weights)
        assert weighted_sum(weights, repeated) == (Q(0), Q(0))

    # Rational perturbations on opposite sides of a boundary configuration.
    up: Vec2 = (Q(-99, 101), Q(20, 101))
    down: Vec2 = (Q(-99, 101), Q(-20, 101))
    assert up[0] ** 2 + up[1] ** 2 == 1
    assert down[0] ** 2 + down[1] ** 2 == 1 and up[1] > 0
    crossed = [Q(99, 220), Q(101, 220), Q(1, 11)]
    assert weighted_sum(crossed, [e1, down, e2]) == (Q(0), Q(0))

    # Antipodal-only, mixed strict, mixed boundary, and mixed outside budgets.
    assert 2 * sum([Q(1, 2), Q(1, 2)], Q(0)) == 2
    assert sum([Q(1, 4), Q(1, 4)], Q(0)) + 2 * Q(3, 4) == 2
    assert sum([Q(1, 4), Q(1, 4), Q(0)], Q(0)) + 2 * Q(3, 4) == 2
    assert 2 * Q(1) == 2
