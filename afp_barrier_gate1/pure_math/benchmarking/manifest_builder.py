"""Create the development P2E benchmark manifest without executing held-out data.

The case definitions are deterministic and are frozen before the held-out
workflow is enabled.  Training and validation may be executed from a manifest
with ``DEVELOPMENT_TRAINING_VALIDATION`` status.  The held-out harness accepts
only a committed copy whose status is ``IMMUTABLE_PREREGISTERED``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping


def _canonical(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(payload: object) -> str:
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _unit(angle_degrees: float) -> list[float]:
    angle = math.radians(angle_degrees)
    return [math.sin(angle), 0.0, math.cos(angle)]


def _electron_parameters(
    *,
    source_kind: str,
    slab_cm: float,
    spatial_cells: int,
    energy_groups: int,
    concentration: float = 60.0,
) -> dict[str, Any]:
    return {
        "source_kind": source_kind,
        "slab_cm": float(slab_cm),
        "spatial_cells": int(spatial_cells),
        "energy_groups": int(energy_groups),
        "top_energy_mev": 10.0,
        "cutoff_mev": 0.001,
        "source_start_cm": 2.0,
        "source_end_cm": 3.0,
        "normal": [1.0, 0.0, 0.0],
        "axis": [1.0, 0.0, 0.0],
        "concentration": float(concentration),
        "surrogate_coefficients": {
            "transfer_fraction": 0.36,
            "absorption_base": 0.018,
            "absorption_scale": 0.022,
            "absorption_shift": 0.03,
            "absorption_exponent": 0.14,
            "diffusion_base": 0.055,
            "diffusion_scale": 0.11,
            "diffusion_shift": 0.12,
        },
        "reference_n_mu": 6,
        "reference_n_phi": 12,
        "reference_lmax": 8,
        "reference_lmax_low": 6,
        "physical_model_uncertainty": 0.05,
        "physical_rotation_samples": 0,
        "rtol": 3e-8,
        "max_iterations": 700,
        "source_provenance": {
            "publication": "Bienvenue et al., Nuclear Science and Engineering (2025)",
            "doi": "10.1080/00295639.2025.2462891",
            "geometry_match": "5-cm water slab, 40 voxels, 40 logarithmic groups, 10 MeV to 1 keV; isotropic 2-3 cm or normal boundary beam",
            "cross_section_scope": "preregistered analytic surrogate; not the authors' Radiant cross-section tables",
        },
    }


def _proton_parameters(*, validation: bool) -> dict[str, Any]:
    scale = 0.55 if validation else 1.0
    return {
        "axis": _unit(22.0 if not validation else 12.0),
        "normal": [0.0, 0.0, 1.0],
        "concentration": 85.0 if not validation else 55.0,
        "energy_mev": 1.0,
        "reference_n_mu": 6,
        "reference_n_phi": 12,
        "reference_lmax": 8,
        "reference_lmax_low": 6,
        "physical_rotation_samples": 3 if not validation else 2,
        "coefficient_scale_low": 0.92,
        "coefficient_scale_high": 1.08,
        "layers": [
            {"material": "Al", "thickness_cm": 0.010 * scale, "cells": 2, "absorption": 2.0, "angular_diffusion": 10.0, "stopping_mev_per_cm": 4.358},
            {"material": "water", "thickness_cm": 0.050 * scale, "cells": 3, "absorption": 0.35, "angular_diffusion": 2.0, "stopping_mev_per_cm": 1.981},
            {"material": "Cu", "thickness_cm": 0.005 * scale, "cells": 2, "absorption": 3.5, "angular_diffusion": 18.0, "stopping_mev_per_cm": 12.57},
            {"material": "water", "thickness_cm": 0.025 * scale, "cells": 2, "absorption": 0.6, "angular_diffusion": 4.0, "stopping_mev_per_cm": 1.981},
        ],
        "coefficient_scope": "fixed layered proton BFP surrogate; stopping coefficients use PDG minimum-ionization values as deterministic scales, not a full PSTAR transport model",
        "material_source": "PDG Atomic and Nuclear Properties; NIST PSTAR is the recommended production replacement",
    }


def _hts_parameters(*, angle_degrees: float, validation: bool) -> dict[str, Any]:
    return {
        "axis": _unit(angle_degrees),
        "normal": [0.0, 0.0, 1.0],
        "concentration": 95.0 if not validation else 55.0,
        "energy_mev": 10.0,
        "reference_n_mu": 6,
        "reference_n_phi": 12,
        "reference_lmax": 8,
        "reference_lmax_low": 6,
        "physical_rotation_samples": 3 if not validation else 2,
        "coefficient_scale_low": 0.88,
        "coefficient_scale_high": 1.12,
        "layers": [
            {"material": "Cu_top", "thickness_cm": 0.0020, "cells": 2, "absorption": 120.0, "angular_diffusion": 90.0, "stopping_mev_per_cm": 12.57},
            {"material": "Ag_top", "thickness_cm": 0.0001, "cells": 1, "absorption": 180.0, "angular_diffusion": 130.0, "stopping_mev_per_cm": 15.0},
            {"material": "REBCO", "thickness_cm": 0.0001, "cells": 2, "absorption": 240.0, "angular_diffusion": 175.0, "stopping_mev_per_cm": 8.0},
            {"material": "buffer", "thickness_cm": 0.00002, "cells": 1, "absorption": 210.0, "angular_diffusion": 150.0, "stopping_mev_per_cm": 7.0},
            {"material": "Hastelloy_substrate", "thickness_cm": 0.0050, "cells": 4, "absorption": 95.0, "angular_diffusion": 65.0, "stopping_mev_per_cm": 10.0},
            {"material": "Ag_bottom", "thickness_cm": 0.0001, "cells": 1, "absorption": 180.0, "angular_diffusion": 130.0, "stopping_mev_per_cm": 15.0},
            {"material": "Cu_bottom", "thickness_cm": 0.0020, "cells": 2, "absorption": 120.0, "angular_diffusion": 90.0, "stopping_mev_per_cm": 12.57},
        ],
        "stack_provenance": {
            "Cu_total_um": 40.0,
            "Ag_each_um": 1.0,
            "REBCO_um": 1.0,
            "buffer_um": 0.2,
            "substrate_um": 50.0,
            "scope": "representative commercial coated-conductor thicknesses; deterministic BFP coefficients are benchmark surrogates, not P2F engineering validation",
        },
    }


def _case(case_id: str, category: str, partition: str, kind: str, parameters: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": case_id,
        "category": category,
        "partition": partition,
        "kind": kind,
        "parameters": dict(parameters),
    }


def build_manifest(registry: Mapping[str, Any], *, status: str) -> dict[str, Any]:
    if registry.get("schema") != "afp-p2e-frozen-operator-registry-v1":
        raise ValueError("unexpected operator registry schema")
    if status not in {"DEVELOPMENT_TRAINING_VALIDATION", "IMMUTABLE_PREREGISTERED"}:
        raise ValueError("invalid manifest status")

    cases: list[dict[str, Any]] = [
        _case("train_mode_l2_m0", "exact_Ylm_decay", "training", "mode_decay", {"degree": 2, "column": 0, "depth": 0.12, "diffusion": 1.0}),
        _case("train_random_l4", "random_band_limited", "training", "bandlimited", {"seed": 104729, "maximum_degree": 4, "depth": 0.075}),
        _case("train_narrow_beam", "narrow_beam", "training", "narrow_beam", {"axis": [0.0, 0.0, 1.0], "concentration": 18.0, "depth": 0.055, "cone_cosine": 0.82, "reference_n_mu": 6, "reference_n_phi": 12, "reference_lmax": 8, "reference_lmax_low": 6, "physical_rotation_samples": 2}),
        _case("validation_mode_l3_m2", "exact_Ylm_decay", "validation", "mode_decay", {"degree": 3, "column": 2, "depth": 0.09, "diffusion": 1.0}),
        _case("validation_random_l5", "random_band_limited", "validation", "bandlimited", {"seed": 130363, "maximum_degree": 5, "depth": 0.06}),
        _case("validation_narrow_beam", "narrow_beam", "validation", "narrow_beam", {"axis": [0.2672612419124244, 0.5345224838248488, 0.8017837257372732], "concentration": 32.0, "depth": 0.045, "cone_cosine": 0.88, "reference_n_mu": 6, "reference_n_phi": 12, "reference_lmax": 8, "reference_lmax_low": 6, "physical_rotation_samples": 2}),
        _case("validation_electron_reduced", "published_electron_depth_dose", "validation", "electron_published", _electron_parameters(source_kind="normal_beam", slab_cm=2.5, spatial_cells=20, energy_groups=20, concentration=45.0)),
        _case("validation_neutron_bfp", "justified_neutron_BFP", "validation", "neutron_bfp", {"seed": 15485863, "maximum_degree": 5, "epsilon": 0.04, "collision_depth": 1.0}),
        _case("validation_proton_layered", "proton_multiple_scattering", "validation", "proton_layered", _proton_parameters(validation=True)),
        _case("validation_hts_normal", "HTS_oblique_stack", "validation", "hts_oblique", _hts_parameters(angle_degrees=20.0, validation=True)),
        _case("heldout_mode_l2_m3", "exact_Ylm_decay", "heldout", "mode_decay", {"degree": 2, "column": 3, "depth": 0.16, "diffusion": 0.85}),
        _case("heldout_mode_l3_m5", "exact_Ylm_decay", "heldout", "mode_decay", {"degree": 3, "column": 5, "depth": 0.11, "diffusion": 1.15}),
        _case("heldout_mode_l4_m1", "exact_Ylm_decay", "heldout", "mode_decay", {"degree": 4, "column": 1, "depth": 0.065, "diffusion": 0.9}),
        _case("heldout_mode_l6_m7", "exact_Ylm_decay", "heldout", "mode_decay", {"degree": 6, "column": 7, "depth": 0.035, "diffusion": 0.7}),
        _case("heldout_random_l5_a", "random_band_limited", "heldout", "bandlimited", {"seed": 32452843, "maximum_degree": 5, "depth": 0.055}),
        _case("heldout_random_l6_b", "random_band_limited", "heldout", "bandlimited", {"seed": 49979687, "maximum_degree": 6, "depth": 0.035}),
        _case("heldout_narrow_beam", "narrow_beam", "heldout", "narrow_beam", {"axis": [0.8017837257372732, -0.5345224838248488, 0.2672612419124244], "concentration": 60.0, "depth": 0.04, "cone_cosine": 0.92, "reference_n_mu": 7, "reference_n_phi": 16, "reference_lmax": 10, "reference_lmax_low": 8, "physical_rotation_samples": 4}),
        _case("heldout_electron_normal_beam", "published_electron_depth_dose", "heldout", "electron_published", _electron_parameters(source_kind="normal_beam", slab_cm=5.0, spatial_cells=40, energy_groups=40, concentration=60.0)),
        _case("heldout_electron_isotropic_2_3cm", "published_electron_depth_dose", "heldout", "electron_published", _electron_parameters(source_kind="isotropic_internal", slab_cm=5.0, spatial_cells=40, energy_groups=40, concentration=60.0)),
        _case("heldout_neutron_bfp", "justified_neutron_BFP", "heldout", "neutron_bfp", {"seed": 67867967, "maximum_degree": 6, "epsilon": 0.02, "collision_depth": 1.4}),
        _case("heldout_proton_layered", "proton_multiple_scattering", "heldout", "proton_layered", _proton_parameters(validation=False)),
        _case("heldout_hts_oblique_67deg", "HTS_oblique_stack", "heldout", "hts_oblique", _hts_parameters(angle_degrees=67.0, validation=False)),
    ]

    manifest: dict[str, Any] = {
        "schema": "afp-p2e-benchmark-manifest-v1",
        "status": status,
        "literal_parent_sha": "b34c29b1b04f5293eaa4007b39d189efa03c51f5",
        "operator_registry_sha256": registry["registry_sha256"],
        "frozen_software": {
            "python": "3.12",
            "clarabel": "0.11.1",
            "cvxpy": "1.7.3",
            "numpy": "2.3.2",
            "osqp": "1.0.4",
            "pytest": "8.4.2",
            "scipy": "1.18.0",
            "scs": "3.2.9",
            "sympy": "1.14.0",
        },
        "comparison_firewall": {
            "operator_quality": "identical product_4x8 nodes and masses for all fixed-node production and ablation methods",
            "different_quadrature": "reported only in separate co-design tables",
            "reference": "analytic harmonic solution or independent finer product quadrature with weighted spherical-harmonic angular operator",
        },
        "fixed_node_method_order": [
            "monotone_afp_baseline",
            "harmonic_fidelity",
            "remove_h2_objective",
            "remove_rate_cap",
            "remove_rotation_penalty",
            "alter_graph_locality",
            "signed_higher_accuracy",
        ],
        "partitions": {
            "training": [case["id"] for case in cases if case["partition"] == "training"],
            "validation": [case["id"] for case in cases if case["partition"] == "validation"],
            "heldout": [case["id"] for case in cases if case["partition"] == "heldout"],
        },
        "cases": cases,
        "timing": {
            "repeats": 1,
            "measurement": "median wall/process time and Python/process peak memory in one pinned GitHub Actions runner",
            "equal_wall_protocol": "paired fixed-node runs at a common max-of-pair budget; scaling across direction counts is confined to co-design",
        },
        "accelerator_ablation": {
            "diagonal": 1.0,
            "streaming": 0.2,
            "beta": 0.95,
            "source_concentration": 8.0,
            "rtol": 1e-10,
            "timing_repeats": 3,
            "scope": "use harmonic_fidelity only as a preconditioner while retaining the baseline production matrix; computational P2E ablation, not P2D completion",
        },
        "co_design_case_ids": [
            "validation_narrow_beam",
            "validation_hts_normal",
            "heldout_narrow_beam",
            "heldout_hts_oblique_67deg",
        ],
        "success_criteria": {
            "invariant_gates": {
                "positive_method_conservation_inf": 5e-8,
                "positive_method_h0_inf": 5e-8,
                "positive_method_h1_inf": 5e-7,
                "positive_method_minimum_offdiagonal": -3e-10,
                "harmonic_fidelity_all_case_minimum_flux": -3e-8,
            },
            "predeclared_primary_value_gate": {
                "geometric_mean_response_error_ratio_to_baseline_max": 0.95,
                "fraction_of_heldout_cases_with_lower_response_error_min": 0.60,
                "worst_response_error_ratio_to_baseline_max": 1.35,
                "exact_mode_geometric_mean_state_error_ratio_max": 0.85,
                "note": "thresholds may be tightened, but not relaxed, in the immutable preregistration after validation-only execution",
            },
            "reference_gate": {
                "reference_uncertainty_reported_separately": True,
                "physical_model_uncertainty_reported_separately": True,
            },
        },
        "ablation_inventory": [
            "remove_h2_objective",
            "remove_rate_cap",
            "remove_rotation_penalty",
            "alter_graph_locality",
            "alter_quadrature_separate_co_design",
            "signed_higher_accuracy",
            "accelerator_only_unchanged_production_operator",
        ],
        "claim_boundary": {
            "P2E": "computational evidence for the frozen reduced BFP benchmark hierarchy",
            "not_claimed": [
                "completion of the absent P2D theorem package",
                "reproduction of proprietary or unavailable electron cross-section tables",
                "replacement of full Boltzmann or nuclear-reaction physics",
                "P2F engineering validation or prediction of superconducting degradation",
            ],
        },
    }
    digest_payload = dict(manifest)
    manifest["manifest_sha256"] = _sha256(digest_payload)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--status",
        choices=("DEVELOPMENT_TRAINING_VALIDATION", "IMMUTABLE_PREREGISTERED"),
        default="DEVELOPMENT_TRAINING_VALIDATION",
    )
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    payload = build_manifest(registry, status=args.status)
    rendered = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("P2E_MANIFEST_BUILD_PASS")


if __name__ == "__main__":
    main()
