#!/usr/bin/env python3
"""Independent integer cross-multiplication verifier for the conformance fixture."""

from __future__ import annotations

import json
from math import gcd
from pathlib import Path
import re
import sys

HEX64 = re.compile(r"[0-9a-f]{64}")


def rat(text: object) -> tuple[int, int]:
    if not isinstance(text, str):
        raise ValueError("rational value is not a string")
    if "/" in text:
        a, b = text.split("/", 1)
        n, d = int(a), int(b)
    else:
        n, d = int(text), 1
    if d == 0:
        raise ValueError("zero denominator")
    if d < 0:
        n, d = -n, -d
    g = gcd(abs(n), d)
    return n // g, d // g


def pos(x: tuple[int, int]) -> bool:
    return x[0] > 0


def nonneg(x: tuple[int, int]) -> bool:
    return x[0] >= 0


def lt(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] * b[1] < b[0] * a[1]


def le(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] * b[1] <= b[0] * a[1]


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return rat(f"{a[0]*b[1]+b[0]*a[1]}/{a[1]*b[1]}")


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return rat(f"{a[0]*b[1]-b[0]*a[1]}/{a[1]*b[1]}")


def mul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return rat(f"{a[0]*b[0]}/{a[1]*b[1]}")


def div(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    if b[0] == 0:
        raise ValueError("division by zero")
    return rat(f"{a[0]*b[1]}/{a[1]*b[0]}")


def verify(data: dict[str, object]) -> list[str]:
    e: list[str] = []
    if data.get("schema_version") != 1 or data.get("scientific_status") != "CONFORMANCE_FIXTURE_ONLY":
        e.append("status/schema mismatch")
    if data.get("uniform_in_level") is not False or data.get("radius_kind") != "level-dependent-rational-lower-bound":
        e.append("uniformity/radius mismatch")
    support = data.get("support")
    if not isinstance(support, dict):
        return e + ["support is not an object"]
    for key in (
        "ring_counts_fixed", "longitude_phases_fixed", "radial_masks_fixed",
        "horizontal_jumps_fixed", "pole_fixed", "equator_fixed",
        "north_south_reflection_fixed", "shared_edge_unknowns_unique",
        "common_rotation_allowed",
    ):
        if support.get(key) is not True:
            e.append(f"support:{key}")
    sha = support.get("support_sha256")
    if not isinstance(sha, str) or not HEX64.fullmatch(sha):
        e.append("support hash")
    try:
        g = data["geometry"]
        assert isinstance(g, dict)
        rho = rat(g["radius_over_h"])
        sep = rat(g["base_separation_over_h_lower"])
        emin = rat(g["base_edge_chord_over_h_lower"])
        emax = rat(g["base_edge_chord_over_h_upper"])
        if not all(pos(x) for x in (rho, sep, emin, emax)):
            e.append("nonpositive geometry")
        if not le(mul(rho, (4, 1)), sep):
            e.append("separation")
        pmin = sub(emin, mul((2, 1), rho))
        pmax = add(emax, mul((2, 1), rho))
        if not pos(pmin):
            e.append("edge collapse")
        rate_need = div((4, 1), mul(pmin, pmin))
        defect_need = mul((3, 2), mul(pmax, pmax))
        if not le(rate_need, rat(data["claimed_rate_constant"])):
            e.append("rate")
        if not le(defect_need, rat(data["claimed_defect_constant"])):
            e.append("defect")
    except (KeyError, ValueError, AssertionError, TypeError) as exc:
        e.append(f"geometry:{exc}")
        rho = (0, 1)
    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        e.append("blocks")
    else:
        seen: set[object] = set()
        for b in blocks:
            if not isinstance(b, dict):
                e.append("block type")
                continue
            name = b.get("name")
            if not isinstance(name, str) or name in seen:
                e.append("block name")
                continue
            seen.add(name)
            try:
                det = rat(b["determinant_abs_lower"])
                inv = rat(b["inverse_norm_upper"])
                jac = rat(b["jacobian_lipschitz_upper"])
                rhs = rat(b["residual_lipschitz_upper"])
                margin = rat(b["base_positive_margin"])
                if not pos(det) or not pos(inv) or not pos(margin) or not nonneg(jac) or not nonneg(rhs):
                    e.append(f"{name}:sign")
                    continue
                q = mul(mul(inv, jac), rho)
                if not lt(q, (1, 1)):
                    e.append(f"{name}:q")
                    continue
                disp = div(mul(mul(inv, rhs), rho), sub((1, 1), q))
                if not lt(disp, margin):
                    e.append(f"{name}:margin")
            except (KeyError, ValueError, TypeError) as exc:
                e.append(f"{name}:{exc}")
    return e


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = verify(data)
    if errors:
        print("FAIL", *errors, sep="\n")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: p1e_fixed_support_certificate_independent.py CERTIFICATE.json")
    main(sys.argv[1])
