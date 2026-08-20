#!/usr/bin/env python3
"""Exact verifier for a finite fractional-development selector certificate."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


def parse_q(value: Any) -> Q:
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str):
        return Q(value)
    raise TypeError(f"expected an integer or rational string, got {value!r}")


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Development:
    identifier: str
    jump: tuple[Q, ...]


@dataclass(frozen=True)
class Problem:
    interfaces: tuple[str, ...]
    developments: tuple[Development, ...]
    physical: tuple[Q, ...]
    certificate: dict[str, Any]


def require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {label}: {values}")


def load_problem(path: Path) -> Problem:
    raw = json.loads(path.read_text(encoding="utf-8"))
    interfaces = tuple(str(value) for value in raw["interfaces"])
    if not interfaces:
        raise AssertionError("the interface set must be nonempty")
    require_unique(list(interfaces), "interface identifiers")

    physical_map = raw["physical"]
    physical = tuple(parse_q(physical_map[name]) for name in interfaces)
    if any(value < 0 for value in physical):
        raise AssertionError("physical interface capacities must be nonnegative")

    developments: list[Development] = []
    development_ids: list[str] = []
    for index, entry in enumerate(raw["developments"]):
        identifier = str(entry.get("id", f"development-{index}"))
        development_ids.append(identifier)
        jump_map = entry["jump"]
        vector = tuple(parse_q(jump_map.get(name, 0)) for name in interfaces)
        if any(value < 0 for value in vector):
            raise AssertionError(f"development {identifier}: jump entries must be nonnegative")
        developments.append(Development(identifier, vector))

    if not developments:
        raise AssertionError("the development family must be nonempty")
    require_unique(development_ids, "development identifiers")
    return Problem(interfaces, tuple(developments), physical, dict(raw["certificate"]))


def dot(first: tuple[Q, ...], second: tuple[Q, ...]) -> Q:
    if len(first) != len(second):
        raise AssertionError("dot-product dimension mismatch")
    return sum((a * b for a, b in zip(first, second)), Q(0))


def verify_primal(problem: Problem) -> list[str]:
    weights_raw = problem.certificate.get("weights", {})
    known = {development.identifier for development in problem.developments}
    unknown = set(weights_raw) - known
    if unknown:
        raise AssertionError(f"primal certificate names unknown developments: {sorted(unknown)}")
    weights = tuple(parse_q(weights_raw.get(development.identifier, 0))
                    for development in problem.developments)
    if any(weight < 0 for weight in weights):
        raise AssertionError("primal weights must be nonnegative")
    total_weight = sum(weights, Q(0))
    if total_weight != 1:
        raise AssertionError(f"primal weights sum to {qtext(total_weight)}, not 1")

    expected = tuple(
        sum(
            weights[d] * problem.developments[d].jump[e]
            for d in range(len(problem.developments))
        )
        for e in range(len(problem.interfaces))
    )
    violations = [
        (problem.interfaces[e], expected[e], problem.physical[e])
        for e in range(len(problem.interfaces))
        if expected[e] > problem.physical[e]
    ]
    if violations:
        details = ", ".join(
            f"{name}: expected {qtext(value)} > physical {qtext(capacity)}"
            for name, value, capacity in violations
        )
        raise AssertionError(f"primal capacity violations: {details}")

    lines = [
        "FRACTIONAL DEVELOPMENT LP CERTIFICATE: PASS",
        "  certificate type: primal",
        f"  interfaces: {len(problem.interfaces)}",
        f"  developments: {len(problem.developments)}",
        "  total development weight: 1",
    ]
    for e, name in enumerate(problem.interfaces):
        lines.append(
            f"  {name}: expected {qtext(expected[e])}, physical {qtext(problem.physical[e])}, "
            f"slack {qtext(problem.physical[e] - expected[e])}"
        )
    positive = [
        f"{problem.developments[d].identifier}={qtext(weight)}"
        for d, weight in enumerate(weights) if weight != 0
    ]
    lines.append("  positive weights: " + ", ".join(positive))
    return lines


def verify_dual(problem: Problem) -> list[str]:
    prices_raw = problem.certificate.get("prices", {})
    unknown = set(prices_raw) - set(problem.interfaces)
    if unknown:
        raise AssertionError(f"dual certificate names unknown interfaces: {sorted(unknown)}")
    prices = tuple(parse_q(prices_raw.get(name, 0)) for name in problem.interfaces)
    if any(price < 0 for price in prices):
        raise AssertionError("dual prices must be nonnegative")
    if not any(price > 0 for price in prices):
        raise AssertionError("dual price vector must be nonzero")

    development_costs = tuple(dot(prices, development.jump)
                              for development in problem.developments)
    minimum = min(development_costs)
    physical_budget = dot(prices, problem.physical)
    if not physical_budget < minimum:
        raise AssertionError(
            f"dual separation failed: physical {qtext(physical_budget)} is not below "
            f"minimum cut {qtext(minimum)}"
        )
    minimizers = [
        problem.developments[d].identifier
        for d, value in enumerate(development_costs) if value == minimum
    ]
    lines = [
        "FRACTIONAL DEVELOPMENT LP CERTIFICATE: PASS",
        "  certificate type: dual",
        f"  interfaces: {len(problem.interfaces)}",
        f"  developments: {len(problem.developments)}",
        f"  priced physical budget: {qtext(physical_budget)}",
        f"  minimum priced development cut: {qtext(minimum)}",
        f"  strict dual gap: {qtext(minimum - physical_budget)}",
        "  minimizing developments: " + ", ".join(minimizers),
    ]
    positive = [
        f"{problem.interfaces[e]}={qtext(price)}"
        for e, price in enumerate(prices) if price != 0
    ]
    lines.append("  positive prices: " + ", ".join(positive))
    return lines


def verify(path: Path) -> list[str]:
    problem = load_problem(path)
    certificate_type = str(problem.certificate["type"])
    if certificate_type == "primal":
        return verify_primal(problem)
    if certificate_type == "dual":
        return verify_dual(problem)
    raise AssertionError(f"unknown certificate type {certificate_type!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    arguments = parser.parse_args()
    for line in verify(arguments.input):
        print(line)


if __name__ == "__main__":
    main()
