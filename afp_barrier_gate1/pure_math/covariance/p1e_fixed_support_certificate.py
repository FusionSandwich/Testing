#!/usr/bin/env python3
"""Exact Fraction verifier for fixed-level AFP robustness certificates.

The committed certificate is a conformance fixture, not a production-level
radius certificate. A future explicit radius requires a production extension of this conformance schema.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re
import sys
from typing import Any

HEX64 = re.compile(r"[0-9a-f]{64}")


def F(value: Any) -> Fraction:
    if not isinstance(value, str):
        raise ValueError("all certified real values must be rational strings")
    return Fraction(value)


def verify(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if data.get("scientific_status") != "CONFORMANCE_FIXTURE_ONLY":
        errors.append("fixture must not be promoted to scientific evidence")
    if data.get("uniform_in_level") is not False:
        errors.append("the fixed-level certificate may not claim level-uniformity")
    if data.get("radius_kind") != "level-dependent-rational-lower-bound":
        errors.append("wrong radius kind")
    if not isinstance(data.get("level"), int) or data["level"] < 1:
        errors.append("level must be a positive integer")

    support = data.get("support", {})
    required_flags = (
        "ring_counts_fixed", "longitude_phases_fixed", "radial_masks_fixed",
        "horizontal_jumps_fixed", "pole_fixed", "equator_fixed",
        "north_south_reflection_fixed", "shared_edge_unknowns_unique",
    )
    for name in required_flags:
        if support.get(name) is not True:
            errors.append(f"support flag {name} is not true")
    if support.get("common_rotation_allowed") is not True:
        errors.append("common ambient rotation must remain permitted")
    if not isinstance(support.get("support_sha256"), str) or not HEX64.fullmatch(support["support_sha256"]):
        errors.append("support_sha256 must be a lower-case SHA-256")

    try:
        geometry = data["geometry"]
        rho = F(geometry["radius_over_h"])
        sep = F(geometry["base_separation_over_h_lower"])
        edge_min = F(geometry["base_edge_chord_over_h_lower"])
        edge_max = F(geometry["base_edge_chord_over_h_upper"])
        if min(rho, sep, edge_min, edge_max) <= 0:
            errors.append("geometry bounds must be positive")
        if rho > sep / 4:
            errors.append("radius does not preserve node separation")
        pert_min = edge_min - 2 * rho
        pert_max = edge_max + 2 * rho
        if pert_min <= 0:
            errors.append("radius does not preserve positive edge length")
        rate_required = 4 / (pert_min * pert_min)
        defect_required = Fraction(3, 2) * pert_max * pert_max
        if F(data["claimed_rate_constant"]) < rate_required:
            errors.append("claimed rate constant is too small")
        if F(data["claimed_defect_constant"]) < defect_required:
            errors.append("claimed defect constant is too small")
    except (KeyError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"invalid geometry: {exc}")
        rho = Fraction(0)

    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        errors.append("at least one Jacobian block is required")
    else:
        names: set[str] = set()
        for block in blocks:
            name = block.get("name")
            if not isinstance(name, str) or not name or name in names:
                errors.append("block names must be unique nonempty strings")
                continue
            names.add(name)
            try:
                if int(block["dimension"]) <= 0:
                    errors.append(f"{name}: dimension must be positive")
                det = F(block["determinant_abs_lower"])
                inv = F(block["inverse_norm_upper"])
                jac = F(block["jacobian_lipschitz_upper"])
                rhs = F(block["residual_lipschitz_upper"])
                margin = F(block["base_positive_margin"])
                if min(det, inv, margin) <= 0 or min(jac, rhs) < 0:
                    errors.append(f"{name}: invalid positivity or derivative bound")
                    continue
                q = inv * jac * rho
                if q >= 1:
                    errors.append(f"{name}: Neumann contraction factor is not below one")
                    continue
                displacement = inv * rhs * rho / (1 - q)
                if displacement >= margin:
                    errors.append(f"{name}: certified displacement exhausts positivity margin")
            except (KeyError, ValueError, ZeroDivisionError) as exc:
                errors.append(f"{name}: invalid block data: {exc}")
    return errors


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = verify(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: p1e_fixed_support_certificate.py CERTIFICATE.json")
    main(sys.argv[1])
