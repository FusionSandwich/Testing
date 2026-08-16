from __future__ import annotations

import copy
import json
import math
from pathlib import Path
import sys

import numpy as np

COV = Path(__file__).resolve().parents[1] / "covariance"
sys.path.insert(0, str(COV))

from p1e_fixed_support_certificate import verify as verify_fraction  # noqa: E402
from p1e_fixed_support_certificate_independent import verify as verify_integer  # noqa: E402
from p1e_fixed_support_robustness import exactness_report, expand_fixed_support, solve_fixed_support  # noqa: E402
from p1e_short_gap_family_audit import build_orbits  # noqa: E402


def fixture() -> dict[str, object]:
    return json.loads((COV / "p1e_fixed_support_certificate_fixture.json").read_text(encoding="utf-8"))


def test_two_independent_certificate_verifiers_accept_fixture() -> None:
    data = fixture()
    assert verify_fraction(data) == []
    assert verify_integer(data) == []


def test_certificate_rejects_uniformity_and_margin_mutations() -> None:
    for mutate in ("uniform", "det", "margin", "support", "rate", "defect"):
        data = copy.deepcopy(fixture())
        if mutate == "uniform":
            data["uniform_in_level"] = True
        elif mutate == "det":
            data["blocks"][0]["determinant_abs_lower"] = "0"  # type: ignore[index]
        elif mutate == "margin":
            data["blocks"][1]["base_positive_margin"] = "0"  # type: ignore[index]
        elif mutate == "support":
            data["support"]["radial_masks_fixed"] = False  # type: ignore[index]
        elif mutate == "rate":
            data["claimed_rate_constant"] = "100"
        else:
            data["claimed_defect_constant"] = "10"
        assert verify_fraction(data)
        assert verify_integer(data)


def test_fixed_support_resolve_preserves_exact_equations_for_small_perturbation() -> None:
    base = build_orbits(32, 2)
    delta = [base.h * 1e-7 * math.sin(k + 1) for k in range(len(base.rings))]
    delta[-1] = 0.0
    graph = expand_fixed_support(solve_fixed_support(base, delta))
    report = exactness_report(graph)
    assert report["h1"] < 5e-10
    assert report["loss_force"] < 2e-7
    assert report["isotropy"] < 2e-7
    assert report["rate_h2"] < 1024
    assert report["defect_over_h2"] < 54


def test_fixed_support_resolve_rejects_collapsed_gap() -> None:
    base = build_orbits(32, 1)
    delta = [0.0] * len(base.rings)
    delta[1] = -(base.rings[1].t - base.rings[0].t) * base.h
    try:
        solve_fixed_support(base, delta)
    except (ValueError, np.linalg.LinAlgError):
        return
    raise AssertionError("collapsed gap was accepted")
