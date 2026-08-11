#!/usr/bin/env python3
"""Independent contract, mutation, and repository-scope audit for Outcome B.

The script consumes a declarative theorem contract and checks publication
surfaces. It does not import the construction generator and is not evidence
for the analytic unperturbed family or for any uniform perturbation estimate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "afp-fixed-level-local-persistence-v1"
THEOREM_ID = "P1E-LOCAL-PERSIST"

EXPECTED_FROZEN = {
    "pole",
    "equator",
    "ring_counts",
    "longitude_phases",
    "radial_masks",
    "horizontal_jump_integers",
    "undirected_support_graph",
    "north_south_reflection",
}
EXPECTED_MOTION = {
    "reflected_latitude_displacements",
    "one_common_ambient_rotation",
}
EXPECTED_HYPOTHESES = {
    "finite_level_construction",
    "strictly_positive_latitude_gaps",
    "strictly_positive_active_chord_losses",
    "every_local_system_nonsingular",
    "every_recovered_conductance_strictly_positive",
}
EXPECTED_MECHANISMS = {
    "guarded_open_parameter_domain",
    "continuity_of_local_system_entries",
    "continuity_of_determinants",
    "continuity_of_finite_recursive_solutions",
    "finite_positive_conductance_margin",
    "open_good_set_contains_unperturbed_point",
}
EXPECTED_CONCLUSIONS = {
    "unique_local_solvability",
    "strictly_positive_recovered_conductances",
    "shared_undirected_conductances",
    "positive_stationary_masses",
    "reversibility",
    "exact_H0_fidelity",
    "exact_H1_fidelity",
}
REQUIRED_EXCLUSIONS = {
    "uniform_radius_over_all_levels",
    "level_independent_lower_bound_for_delta_J",
    "delta_J_equal_to_constant_times_h_power",
    "perturbed_all_level_rate_constant",
    "perturbed_all_level_quadratic_defect_constant",
    "changed_ring_counts",
    "changed_longitude_phases",
    "changed_radial_masks",
    "changed_horizontal_jumps",
    "changed_support_graph",
    "independent_longitude_motion",
    "arbitrary_node_motion",
}


def as_set(value: Any, field: str, errors: list[str]) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        errors.append(f"{field} must be a list of strings")
        return set()
    if len(value) != len(set(value)):
        errors.append(f"{field} contains duplicate entries")
    return set(value)


def validate_contract(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["contract root must be an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("theorem_id") != THEOREM_ID:
        errors.append("theorem identifier mismatch")
    if data.get("outcome") != "B_EXACT_WEAKENING":
        errors.append("outcome must be exact weakening")
    if data.get("dimension") != 3:
        errors.append("dimension must remain d=3")
    if data.get("level_quantifier") != "for_each_fixed_level_J":
        errors.append("level quantifier must be fixed-level, not uniform")

    radius = data.get("radius")
    if not isinstance(radius, dict):
        errors.append("radius block missing")
    else:
        expected_radius = {
            "symbol": "delta_J",
            "existence": "existential",
            "positive": True,
            "level_dependent": True,
            "explicit": False,
            "uniform_in_J": False,
            "prescribed_h_power": None,
        }
        for key, expected in expected_radius.items():
            if radius.get(key) != expected:
                errors.append(f"radius.{key} must be {expected!r}")

    if as_set(data.get("frozen_data"), "frozen_data", errors) != EXPECTED_FROZEN:
        errors.append("frozen_data must exactly preserve the reflected support data")
    if as_set(data.get("permitted_motion"), "permitted_motion", errors) != EXPECTED_MOTION:
        errors.append("permitted_motion mismatch")
    if as_set(data.get("unperturbed_hypotheses"), "unperturbed_hypotheses", errors) != EXPECTED_HYPOTHESES:
        errors.append("unperturbed hypotheses mismatch")
    if as_set(data.get("proof_mechanism"), "proof_mechanism", errors) != EXPECTED_MECHANISMS:
        errors.append("proof mechanism must retain every continuity and guard step")
    if as_set(data.get("conclusions"), "conclusions", errors) != EXPECTED_CONCLUSIONS:
        errors.append("conclusion set mismatch")

    normalization = data.get("normalization")
    expected_normalization = {
        "mass_formula_factor": "1/2",
        "coordinate_eigenvalue": -2,
        "one_conductance_per_undirected_edge": True,
    }
    if normalization != expected_normalization:
        errors.append("normalization block mismatch")

    exclusions = as_set(data.get("not_claimed"), "not_claimed", errors)
    if not REQUIRED_EXCLUSIONS.issubset(exclusions):
        errors.append("not_claimed omits a required publication boundary")

    if data.get("ordinary_proof") != "docs/publication_program/P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md":
        errors.append("ordinary proof path mismatch")
    if data.get("rejected_claim_record") != "docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md":
        errors.append("rejected-claim path mismatch")
    if data.get("lean_scope") != "finite_stress_to_generator_algebra_only":
        errors.append("Lean scope is overstated")
    if data.get("computational_scope") != "contract_and_repository_regression_only":
        errors.append("computational scope is overstated")
    return errors


def solve_2x2(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
              b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ValueError("singular local system")
    return (
        (b[0] * a[1][1] - a[0][1] * b[1]) / det,
        (a[0][0] * b[1] - b[0] * a[1][0]) / det,
    )


def exact_fixture_regressions() -> None:
    """Small exact checks of verifier mechanics, never an all-level proof."""
    a0 = ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(2)))
    x0 = solve_2x2(a0, (Fraction(3), Fraction(3)))
    if x0 != (Fraction(1), Fraction(1)):
        raise AssertionError("unperturbed exact local solve")

    for t in (Fraction(-1, 2), Fraction(1, 2)):
        a = ((Fraction(2) + t, Fraction(1)),
             (Fraction(1), Fraction(2) - t))
        x = solve_2x2(a, (Fraction(3), Fraction(3)))
        if min(x) <= 0:
            raise AssertionError("positive finite fixture lost positivity")

    try:
        solve_2x2(((Fraction(1), Fraction(1)),
                   (Fraction(1), Fraction(1))),
                  (Fraction(2), Fraction(2)))
    except ValueError:
        pass
    else:
        raise AssertionError("singular-system mutation was accepted")

    negative = solve_2x2(a0, (Fraction(-3), Fraction(3)))
    if min(negative) >= 0:
        raise AssertionError("sign mutation did not expose negativity")

    conductances = (Fraction(2), Fraction(4))
    losses = (Fraction(1, 2), Fraction(3, 2))
    total_loss = sum(g * ell for g, ell in zip(conductances, losses))
    mu = Fraction(1, 2) * total_loss
    if total_loss != 2 * mu:
        raise AssertionError("mass normalization factor")
    wrong_mu = total_loss
    if total_loss == 2 * wrong_mu:
        raise AssertionError("missing one-half mutation was accepted")


def mutation_suite(contract: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Any]] = []

    def mutate(name: str, edit: Any) -> None:
        candidate = copy.deepcopy(contract)
        edit(candidate)
        mutations.append((name, candidate))

    mutate("sign_reversal", lambda x: x["normalization"].__setitem__("coordinate_eigenvalue", 2))
    mutate("missing_weight_factor", lambda x: x["normalization"].__setitem__("mass_formula_factor", "1"))
    mutate("altered_perturbation_power", lambda x: x["radius"].__setitem__("prescribed_h_power", 3))
    mutate("uniform_all_level_radius", lambda x: x["radius"].__setitem__("uniform_in_J", True))
    mutate("removed_denominator_guard", lambda x: x["proof_mechanism"].remove("guarded_open_parameter_domain"))
    mutate("singular_local_system", lambda x: x["unperturbed_hypotheses"].__setitem__(3, "an_unperturbed_local_system_is_singular"))
    mutate("changed_transition_gap", lambda x: x["unperturbed_hypotheses"].remove("strictly_positive_latitude_gaps"))
    mutate("changed_transition_row", lambda x: x["frozen_data"].remove("radial_masks"))
    mutate("missing_reflection", lambda x: x["frozen_data"].remove("north_south_reflection"))
    mutate("nonshared_edge_assignment", lambda x: x["normalization"].__setitem__("one_conductance_per_undirected_edge", False))
    mutate("changed_support_graph", lambda x: x["frozen_data"].remove("undirected_support_graph"))
    mutate("nonpositive_radius", lambda x: x["radius"].__setitem__("positive", False))

    accepted: list[str] = []
    for name, candidate in mutations:
        errors = validate_contract(candidate)
        if not errors:
            accepted.append(name)
        else:
            print(f"MUTATION_REJECTED {name}: {errors[0]}")
    return accepted


def read_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise AssertionError(f"required file missing: {relative}")
    return path.read_text(encoding="utf-8")


def require_markers(root: Path) -> None:
    requirements = {
        "docs/publication_program/P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md": (
            "PROVED ORDINARY THEOREM; EXISTENTIAL LEVEL-DEPENDENT RADIUS",
            "delta_J=\\frac12\\sup S_J",
            "No positive lower bound uniform in `J`",
            "exact constant and coordinate reproduction",
        ),
        "docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md": (
            "HISTORICAL / REJECTED CLAIM — NOT AN ACCEPTED THEOREM",
            "No part of the preceding paragraph is an accepted result",
            "fixed-level theorem",
        ),
        "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md": (
            "### Proposition 7.3 (fixed-level local persistence)",
            "existential and may depend on $J$",
            "P1E-LOCAL-PERSIST",
        ),
        "docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md": (
            "## 10. Fixed-level local persistence",
            "existential and level dependent",
            "P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md",
        ),
        "docs/publication_program/THEOREM_REGISTRY.md": (
            "| P1E-LOCAL-PERSIST | PROVED |",
            "existential level-dependent radius",
        ),
        "docs/publication_program/P1E_FLAGSHIP_THEOREM_AUDIT.md": (
            "## Final classification",
            "Proposition 7.3",
            "16",
        ),
        "docs/publication_program/P1E_PROP73_APPROACH_REGISTRY.md": (
            "OUTCOME B SELECTED",
            "literal expression DAG absent",
            "fixed-level continuity",
        ),
    }
    for relative, markers in requirements.items():
        text = read_text(root, relative)
        for marker in markers:
            if marker not in text:
                raise AssertionError(f"missing marker in {relative}: {marker!r}")


def scan_rejected_uniform_claim(root: Path) -> None:
    # Constructed in pieces so this verifier is not itself a false-positive.
    old_tokens = (
        "K" + "_*",
        "K" + "_\\*",
        "R" + "_rob",
        "C" + "_rob",
        "R" + "_{\\rm rob}",
        "C" + "_{\\rm rob}",
        "h^3/" + "K",
        "structured support-preserving " + "robustness",
        "structured " + "robustness with",
    )
    excluded = {
        "docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md",
        "afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py",
        "afp_barrier_gate1/pure_math/covariance/p1e_robustness_claim_inventory.py",
        "tools/apply_p1e_outcome_b.py",
    }
    suffixes = {".md", ".py", ".lean", ".json", ".yml", ".yaml", ".toml", ".txt", ".tex"}
    failures: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in suffixes:
            continue
        relative = path.relative_to(root).as_posix()
        if relative in excluded:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in old_tokens:
            if token in text:
                failures.append(f"{relative}: retained rejected token {token!r}")
    if failures:
        raise AssertionError("\n".join(failures))


def theorem_audit_coverage(root: Path) -> None:
    audit = read_text(root, "docs/publication_program/P1E_FLAGSHIP_THEOREM_AUDIT.md")
    result_ids = (
        "Proposition 2.1", "Theorem 3.1", "Proposition 3.2", "Theorem 4.1",
        "Theorem 5.1", "Theorem 5.2", "Theorem 5.3", "Proposition 5.4",
        "Corollary 5.5", "Corollary 5.6", "Theorem 6.1", "Corollary 6.2",
        "Corollary 6.3", "Theorem 7.1", "Theorem 7.2", "Proposition 7.3",
    )
    missing = [name for name in result_ids if f"| {name} |" not in audit]
    if missing:
        raise AssertionError(f"theorem audit missing rows: {missing}")
    if audit.count("| accepted") + audit.count("| proved") < 16:
        raise AssertionError("theorem audit lacks final classifications")


def report_hashes(root: Path) -> None:
    paths = (
        "docs/publication_program/P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md",
        "docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md",
        "docs/publication_program/P1E_FLAGSHIP_THEOREM_AUDIT.md",
        "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md",
        "docs/publication_program/THEOREM_REGISTRY.md",
    )
    for relative in paths:
        digest = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        print(f"SHA256 {digest}  {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_contract.json"),
    )
    parser.add_argument("--mutations-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    contract_path = args.contract
    if not contract_path.is_absolute():
        contract_path = root / contract_path
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    errors = validate_contract(contract)
    if errors:
        raise SystemExit("CONTRACT_REJECTED\n" + "\n".join(errors))
    print("CONTRACT_ACCEPTED fixed-level existential theorem")

    exact_fixture_regressions()
    print("EXACT_FIXTURE_REGRESSIONS PASS")

    accepted_mutations = mutation_suite(contract)
    if accepted_mutations:
        raise SystemExit(f"MUTATION_FAILURE accepted={accepted_mutations}")
    print("MUTATION_SUITE PASS: 12/12 rejected")

    if not args.mutations_only:
        require_markers(root)
        theorem_audit_coverage(root)
        scan_rejected_uniform_claim(root)
        report_hashes(root)
        print("REPOSITORY_SCOPE PASS")

    print("P1E fixed-level local-persistence audit: PASS")


if __name__ == "__main__":
    main()
