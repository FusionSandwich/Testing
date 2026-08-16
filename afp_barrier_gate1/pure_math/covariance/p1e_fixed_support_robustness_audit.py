#!/usr/bin/env python3
"""Adversarial audit for the fixed-level replacement of Proposition 7.3."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import numpy as np

from p1e_fixed_support_certificate import verify as verify_fraction
from p1e_fixed_support_certificate_independent import verify as verify_integer
from p1e_fixed_support_robustness import (
    exactness_report,
    expand_fixed_support,
    rotate_graph,
    solve_fixed_support,
)
from p1e_short_gap_family_audit import build_orbits

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "p1e_fixed_support_certificate_fixture.json"


def assert_rejected(data: dict[str, object], label: str) -> None:
    fraction_errors = verify_fraction(data)
    integer_errors = verify_integer(data)
    if fraction_errors and integer_errors:
        return
    raise AssertionError(
        f"hostile certificate mutation survived one verifier: {label}; "
        f"fraction={fraction_errors}, integer={integer_errors}"
    )


def certificate_audit() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert verify_fraction(data) == []
    assert verify_integer(data) == []

    mutations: list[tuple[str, tuple[str, ...], object]] = [
        ("uniform-level", ("uniform_in_level",), True),
        ("mask-change", ("support", "radial_masks_fixed"), False),
        ("phase-change", ("support", "longitude_phases_fixed"), False),
        ("shared-edge-duplication", ("support", "shared_edge_unknowns_unique"), False),
        ("pole-motion", ("support", "pole_fixed"), False),
        ("equator-motion", ("support", "equator_fixed"), False),
        ("reflection-loss", ("support", "north_south_reflection_fixed"), False),
        ("determinant-collapse", ("blocks", "0", "determinant_abs_lower"), "0"),
        ("near-zero-conductance", ("blocks", "1", "base_positive_margin"), "0"),
        ("inverse-blowup", ("blocks", "2", "inverse_norm_upper"), "1000"),
        ("gap-collapse", ("geometry", "radius_over_h"), "1/8"),
        ("rate-underclaim", ("claimed_rate_constant",), "100"),
        ("defect-underclaim", ("claimed_defect_constant",), "10"),
    ]
    for label, path, value in mutations:
        bad = copy.deepcopy(data)
        cursor: object = bad
        for key in path[:-1]:
            if isinstance(cursor, list):
                cursor = cursor[int(key)]
            else:
                assert isinstance(cursor, dict)
                cursor = cursor[key]
        assert isinstance(cursor, dict)
        cursor[path[-1]] = value
        assert_rejected(bad, label)


def finite_solver_audit() -> None:
    for M0, J in ((32, 1), (32, 3), (64, 2)):
        base = build_orbits(M0, J)
        n = len(base.rings)
        delta = [base.h * 2e-7 * math.sin(1.7 * (k + 1)) for k in range(n)]
        delta[-1] = 0.0
        solution = solve_fixed_support(base, delta)
        graph = expand_fixed_support(solution)
        report = exactness_report(graph)
        assert report["h1"] < 5e-10
        assert report["loss_force"] < 2e-7
        assert report["isotropy"] < 2e-7
        assert report["edge_min_over_h"] > 1 / 16
        assert report["edge_max_over_h"] < 6
        assert report["rate_h2"] < 1024
        assert report["defect_over_h2"] < 54

        angle = 0.371
        Q = np.array([
            [math.cos(angle), -math.sin(angle), 0.0],
            [math.sin(angle), math.cos(angle), 0.0],
            [0.0, 0.0, 1.0],
        ])
        rotated = exactness_report(rotate_graph(graph, Q))
        for key in ("h1", "loss_force", "isotropy", "rate_h2", "defect_over_h2"):
            assert abs(rotated[key] - report[key]) < 5e-10

        collapsed = [0.0] * n
        collapsed[1] = -(base.rings[1].t - base.rings[0].t) * base.h
        try:
            solve_fixed_support(base, collapsed)
        except (ValueError, np.linalg.LinAlgError):
            pass
        else:
            raise AssertionError("collapsed meridional gap was accepted")


def prose_firewall() -> None:
    root = HERE.parents[2]
    theorem = (root / "docs/publication_program/P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md").read_text(encoding="utf-8")
    registry = (root / "docs/publication_program/THEOREM_REGISTRY.md").read_text(encoding="utf-8")
    manuscript = (root / "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md").read_text(encoding="utf-8")
    assert "level-dependent" in theorem
    assert "merely existential" in theorem
    assert "P1E-ROBUST-FIXED | PROVED" in registry
    assert "P1E-ROBUST-UNIFORM | REJECTED" in registry
    assert "Proposition 7.3 (fixed-level support-preserving robustness)" in manuscript
    for text in (theorem, registry, manuscript):
        assert "2^{28\\cdot2^{10^6}}" not in text
        assert "uniform perturbation radius is proved" not in text
    assert "no sampling-frame lower bound" in theorem


def main() -> None:
    certificate_audit()
    finite_solver_audit()
    prose_firewall()
    print("fixed-level support-preserving robustness audit: PASS")


if __name__ == "__main__":
    main()
