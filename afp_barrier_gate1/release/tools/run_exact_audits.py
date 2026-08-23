#!/usr/bin/env python3
"""Run the P1A--P1E exact/symbolic and packaged certificate surface."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT = Path(__file__).resolve().parents[2]
AUDITS = [
    ("p1a_quadratic_fidelity_audit.py", "P1A exact quadratic-fidelity audit: PASS"),
    ("p1b_sharp_quadratic_defect_audit.py", "P1B sharp quadratic-defect audit: PASS"),
    ("p1c_equality_geometry_audit.py", "P1C exact equality-geometry audit: PASS"),
    ("p1d_quantitative_stability_audit.py", "P1D quantitative stability audit: PASS"),
    ("p1e_short_gap_symbolic_matrix_audit.py", "short-gap literal symbolic matrix-to-limit audit: PASS"),
    ("p1e_short_gap_cauchy_guard_audit.py", "short-gap rational Cauchy all-orders guard: PASS"),
    ("p1e_short_gap_cauchy_hostile_audit.py", "short-gap hostile Cauchy/first-row audit: ACCEPT"),
    ("p1e_short_gap_polar_guard_audit.py", "short-gap first-polar-row Cauchy guard: PASS"),
    ("p1e_short_gap_proof_audit.py", "short-gap exact algebra audit: PASS (remainder is certified by the Cauchy guard audit)"),
    ("p1e_no_guard_ring_independent_audit.py", "no-guard ring independent audit: exact regressions PASS"),
    ("p1e_short_gap_family_audit.py", "hostile transition and q/h-guard mutations: deterministic failure PASS"),
    ("p1e_short_gap_referee_audit.py", "short-gap hostile referee audit: rejected-mutation regressions PASS"),
    ("p1e_asymptotic_family_audit.py", "closed-form all-level polygon identities: PASS"),
]


def main() -> None:
    root = PROJECT / "pure_math" / "covariance"
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "0"
    for filename, marker in AUDITS:
        completed = subprocess.run(
            [sys.executable, str(root / filename)],
            cwd=PROJECT,
            env=environment,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(f"=== {filename} ===")
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
        if completed.returncode != 0 or marker not in completed.stdout.splitlines():
            raise SystemExit(f"AUDIT_FAILED {filename} exit={completed.returncode}")
    verifier = PROJECT / "release" / "certificates" / "theorem_7_2" / "verify_certificate.py"
    completed = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=PROJECT.parent,
        env=environment,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("=== theorem_7_2/verify_certificate.py ===")
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.returncode != 0 or "Theorem 7.2 exact-rational certificate: PASS" not in completed.stdout.splitlines():
        raise SystemExit(f"AUDIT_FAILED theorem_7_2 certificate exit={completed.returncode}")
    print(f"AFP_R6_EXACT_AUDITS_PASS count={len(AUDITS) + 1}")


if __name__ == "__main__":
    main()
