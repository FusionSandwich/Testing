#!/usr/bin/env python3
"""Verify a finite weighted exact-contact circle arrangement.

The input is JSON with rational circle centers, squared radii, integer weights,
optional open conflict disks, one rational witness translation, and a claimed
maximum contact weight.

The solver-free verifier proves the global maximum over the full plane by
checking the total weight of each coincident-circle class and every pairwise
intersection point of distinct circles.  A weighted circle count is constant on
open arcs between intersections, so those candidates are exhaustive.

Pairwise intersections are represented exactly in `Q(sqrt(d))`; no floating-
point pass/fail decision is used.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
from typing import Any


def parse_q(value: Any) -> Q:
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str):
        return Q(value)
    raise TypeError(f"expected integer or rational string, got {value!r}")


def rational_sqrt(value: Q) -> Q | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return Q(numerator, denominator)
    return None


@dataclass(frozen=True)
class Quad:
    a: Q
    b: Q = Q(0)
    d: Q = Q(0)

    @staticmethod
    def rational(value: Q) -> "Quad":
        return Quad(value, Q(0), Q(0))

    @staticmethod
    def from_sqrt(coefficient: Q, radicand: Q, rational: Q = Q(0)) -> "Quad":
        if coefficient == 0 or radicand == 0:
            return Quad.rational(rational)
        root = rational_sqrt(radicand)
        if root is not None:
            return Quad.rational(rational + coefficient * root)
        return Quad(rational, coefficient, radicand)

    def _coerce(self, other: "Quad | Q | int") -> "Quad":
        if isinstance(other, Quad):
            return other
        return Quad.rational(Q(other))

    def _common(self, other: "Quad") -> tuple[Q, Q, Q, Q, Q]:
        if self.b == 0:
            return self.a, Q(0), other.a, other.b, other.d
        if other.b == 0:
            return self.a, self.b, other.a, Q(0), self.d
        if self.d != other.d:
            raise ValueError(f"incompatible quadratic fields sqrt({self.d}) and sqrt({other.d})")
        return self.a, self.b, other.a, other.b, self.d

    def __add__(self, other: "Quad | Q | int") -> "Quad":
        other_q = self._coerce(other)
        a1, b1, a2, b2, d = self._common(other_q)
        return Quad.from_sqrt(b1 + b2, d, a1 + a2)

    __radd__ = __add__

    def __neg__(self) -> "Quad":
        return Quad.from_sqrt(-self.b, self.d, -self.a)

    def __sub__(self, other: "Quad | Q | int") -> "Quad":
        return self + (-self._coerce(other))

    def __rsub__(self, other: "Quad | Q | int") -> "Quad":
        return self._coerce(other) - self

    def __mul__(self, other: "Quad | Q | int") -> "Quad":
        other_q = self._coerce(other)
        a1, b1, a2, b2, d = self._common(other_q)
        return Quad.from_sqrt(a1 * b2 + b1 * a2, d, a1 * a2 + b1 * b2 * d)

    __rmul__ = __mul__

    def square(self) -> "Quad":
        return self * self

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def as_text(self) -> str:
        if self.b == 0:
            return str(self.a)
        sign = "+" if self.b >= 0 else "-"
        return f"{self.a} {sign} {abs(self.b)}*sqrt({self.d})"


@dataclass(frozen=True)
class Point:
    x: Quad
    y: Quad

    @staticmethod
    def rational(x: Q, y: Q) -> "Point":
        return Point(Quad.rational(x), Quad.rational(y))

    def key(self) -> tuple[Q, Q, Q, Q, Q, Q]:
        return (self.x.a, self.x.b, self.x.d, self.y.a, self.y.b, self.y.d)

    def as_text(self) -> str:
        return f"({self.x.as_text()}, {self.y.as_text()})"


@dataclass(frozen=True)
class Circle:
    identifier: str
    cx: Q
    cy: Q
    r2: Q
    weight: int

    def geometry_key(self) -> tuple[Q, Q, Q]:
        return self.cx, self.cy, self.r2

    def contains(self, point: Point) -> bool:
        value = (point.x - self.cx).square() + (point.y - self.cy).square() - self.r2
        return value.is_zero()


@dataclass(frozen=True)
class Disk:
    identifier: str
    cx: Q
    cy: Q
    r2: Q

    def contains_open_rational(self, x: Q, y: Q) -> bool:
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 < self.r2


def merge_circles(circles: list[Circle]) -> list[Circle]:
    groups: dict[tuple[Q, Q, Q], list[Circle]] = {}
    for circle in circles:
        groups.setdefault(circle.geometry_key(), []).append(circle)

    merged: list[Circle] = []
    for index, (geometry, group) in enumerate(sorted(groups.items(), key=lambda item: item[0])):
        cx, cy, r2 = geometry
        identifiers = ",".join(circle.identifier for circle in group)
        merged.append(Circle(identifiers or f"class-{index}", cx, cy, r2, sum(c.weight for c in group)))
    return merged


def intersections(first: Circle, second: Circle) -> list[Point]:
    dx = second.cx - first.cx
    dy = second.cy - first.cy
    distance2 = dx * dx + dy * dy

    if distance2 == 0:
        if first.r2 == second.r2:
            raise ValueError("coincident circles must be merged before intersection enumeration")
        return []

    u = (first.r2 - second.r2 + distance2) / (2 * distance2)
    px = first.cx + u * dx
    py = first.cy + u * dy
    height2 = first.r2 - u * u * distance2

    if height2 < 0:
        return []
    if height2 == 0:
        return [Point.rational(px, py)]

    radicand = height2 / distance2
    x_offset = Quad.from_sqrt(-dy, radicand)
    y_offset = Quad.from_sqrt(dx, radicand)
    return [
        Point(Quad.rational(px) + x_offset, Quad.rational(py) + y_offset),
        Point(Quad.rational(px) - x_offset, Quad.rational(py) - y_offset),
    ]


def contact_weight(circles: list[Circle], point: Point) -> int:
    return sum(circle.weight for circle in circles if circle.contains(point))


def global_arrangement_maximum(circles: list[Circle]) -> tuple[int, list[str]]:
    merged = merge_circles(circles)
    if not merged:
        return 0, ["empty arrangement"]

    maximum = max(circle.weight for circle in merged)
    witnesses = [f"open arc of {circle.identifier}" for circle in merged if circle.weight == maximum]

    points: dict[tuple[Q, Q, Q, Q, Q, Q], Point] = {}
    for first_index, first in enumerate(merged):
        for second in merged[first_index + 1 :]:
            for point in intersections(first, second):
                points[point.key()] = point

    for point in points.values():
        weight = contact_weight(merged, point)
        if weight > maximum:
            maximum = weight
            witnesses = [point.as_text()]
        elif weight == maximum:
            witnesses.append(point.as_text())

    return maximum, sorted(set(witnesses))


def load_input(path: Path) -> tuple[list[Circle], list[Disk], Q, Q, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    circles = [
        Circle(
            str(entry.get("id", f"circle-{index}")),
            parse_q(entry["center"][0]),
            parse_q(entry["center"][1]),
            parse_q(entry["radius_sq"]),
            int(entry.get("weight", 1)),
        )
        for index, entry in enumerate(data.get("circles", []))
    ]
    disks = [
        Disk(
            str(entry.get("id", f"disk-{index}")),
            parse_q(entry["center"][0]),
            parse_q(entry["center"][1]),
            parse_q(entry["radius_sq"]),
        )
        for index, entry in enumerate(data.get("conflict_disks", []))
    ]
    witness_x = parse_q(data["witness"][0])
    witness_y = parse_q(data["witness"][1])
    claimed = int(data["claimed_maximum"])
    return circles, disks, witness_x, witness_y, claimed


def verify(path: Path) -> None:
    circles, disks, witness_x, witness_y, claimed = load_input(path)
    if any(circle.r2 < 0 or circle.weight < 0 for circle in circles):
        raise AssertionError("circle squared radii and weights must be nonnegative")
    if any(disk.r2 < 0 for disk in disks):
        raise AssertionError("conflict-disk squared radii must be nonnegative")

    witness = Point.rational(witness_x, witness_y)
    active = [circle.identifier for circle in circles if circle.contains(witness)]
    witness_weight = sum(circle.weight for circle in circles if circle.contains(witness))
    conflicts = [disk.identifier for disk in disks if disk.contains_open_rational(witness_x, witness_y)]
    if conflicts:
        raise AssertionError(f"witness lies in open conflict disks: {conflicts}")

    maximum, maximum_witnesses = global_arrangement_maximum(circles)
    if maximum != claimed:
        raise AssertionError(f"claimed maximum {claimed}, exact arrangement maximum {maximum}")
    if witness_weight != claimed:
        raise AssertionError(f"witness weight {witness_weight}, claimed maximum {claimed}")

    print("FINITE CONTACT CIRCLE ARRANGEMENT: PASS")
    print(f"  input: {path}")
    print(f"  raw circles: {len(circles)}")
    print(f"  coincident-circle classes: {len(merge_circles(circles))}")
    print(f"  open conflict disks: {len(disks)}")
    print(f"  exact global maximum weight: {maximum}")
    print(f"  supplied admissible witness: ({witness_x},{witness_y})")
    print(f"  active witness circles: {','.join(active) if active else 'none'}")
    print(f"  exact maximum candidate locations: {len(maximum_witnesses)}")
    for text in maximum_witnesses[:8]:
        print(f"    {text}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    verify(args.input)


if __name__ == "__main__":
    main()
