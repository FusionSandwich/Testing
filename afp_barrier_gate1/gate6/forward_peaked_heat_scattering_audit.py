#!/usr/bin/env python3
"""Gate 6 benchmark for a positive forward-peaked scattering model.

The continuum scattering step is the spherical heat semigroup K_tau.  A degree
l spherical harmonic has moment exp(-tau*l*(l+1)), so the continuous-time
Boltzmann collision generator

    B_tau = (K_tau - I) / tau

has positive modal decay

    beta_l(tau) = (1 - exp(-tau*l*(l+1))) / tau.

As tau -> 0 this converges to the Fokker--Planck decay l(l+1).

For each discrete AFP matrix L_h, the benchmark constructs the positive Markov
step exp(tau L_h) and the corresponding discrete Boltzmann generator.  It then
separates:

* continuum Boltzmann-to-Fokker--Planck model error;
* angular discretization error for the discrete Boltzmann model;
* combined discrete Fokker--Planck error against the Boltzmann reference;
* positivity-limited explicit step counts for both generators;
* orientation dependence, mass conservation, and positivity.

No random sampling is used.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE / "angular_diffusion_transport_audit.py"
spec = importlib.util.spec_from_file_location("gate6_diffusion", BASE)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load Gate 6 angular-diffusion implementation")
g6 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g6
spec.loader.exec_module(g6)


@dataclass
class AuditRow:
    level: int
    family: str
    directions: int
    tau: float
    continuum_model_error_max: float
    discrete_boltzmann_error_max: float
    discrete_fp_to_boltzmann_error_max: float
    discrete_fp_to_fp_error_max: float
    boltzmann_orientation_spread: float
    fp_orientation_spread: float
    boltzmann_max_rate: float
    fp_max_rate: float
    boltzmann_dt_limit: float
    fp_dt_limit: float
    boltzmann_euler_steps: int
    fp_euler_steps: int
    transition_minimum: float
    transition_row_error: float
    detailed_balance_error: float
    boltzmann_mass_error: float
    boltzmann_minimum_solution: float


def heat_boltzmann_decay(tau: float, ell: int) -> float:
    lam = float(ell * (ell + 1))
    return -math.expm1(-tau * lam) / tau


def continuum_boltzmann_profiles(
    points: np.ndarray, axes: np.ndarray, time: float, tau: float
) -> np.ndarray:
    mu = points @ axes
    _, _, p2, p3, p4 = g6.legendre_values(mu)
    return (
        1.0
        + 0.35 * math.exp(-heat_boltzmann_decay(tau, 2) * time) * p2
        + 0.20 * math.exp(-heat_boltzmann_decay(tau, 3) * time) * p3
        + 0.10 * math.exp(-heat_boltzmann_decay(tau, 4) * time) * p4
    )


def continuum_fp_profiles(points: np.ndarray, axes: np.ndarray, time: float) -> np.ndarray:
    return g6.continuum_profiles(points, axes, time)


def spectral_data(operator):
    eigenvalues, eigenvectors = np.linalg.eigh(operator.symmetric_matrix)
    if float(np.max(eigenvalues)) > 5.0e-10:
        raise AssertionError(f"{operator.family}: positive AFP eigenvalue")
    return eigenvalues, eigenvectors


def evolve_with_modal_generator(
    operator, initial: np.ndarray, time: float,
    eigenvalues: np.ndarray, eigenvectors: np.ndarray,
    modal_generator: np.ndarray,
) -> np.ndarray:
    root_weight = np.sqrt(operator.weights)
    transformed = root_weight[:, None] * initial
    coefficients = eigenvectors.T @ transformed
    evolved = eigenvectors @ (np.exp(time * modal_generator)[:, None] * coefficients)
    return evolved / root_weight[:, None]


def physical_transition(operator, tau: float, eigenvalues, eigenvectors):
    p_symmetric = (
        eigenvectors * np.exp(tau * eigenvalues)[None, :]
    ) @ eigenvectors.T
    root_weight = np.sqrt(operator.weights)
    transition = (
        p_symmetric
        * root_weight[None, :]
        / root_weight[:, None]
    )
    transition[np.abs(transition) < 2.0e-15] = 0.0
    return transition


def audit_case(level: int, operator, tau: float, time: float, axes: np.ndarray) -> AuditRow:
    initial = g6.initial_profiles(operator.directions, axes)
    reference_boltzmann = continuum_boltzmann_profiles(
        operator.directions, axes, time, tau
    )
    reference_fp = continuum_fp_profiles(operator.directions, axes, time)

    continuum_model_errors = g6.weighted_relative_errors(
        operator.weights, reference_fp, reference_boltzmann
    )

    eigenvalues, eigenvectors = spectral_data(operator)
    boltzmann_modes = np.expm1(tau * eigenvalues) / tau
    discrete_boltzmann = evolve_with_modal_generator(
        operator, initial, time, eigenvalues, eigenvectors, boltzmann_modes
    )
    discrete_fp = evolve_with_modal_generator(
        operator, initial, time, eigenvalues, eigenvectors, eigenvalues
    )

    boltzmann_errors = g6.weighted_relative_errors(
        operator.weights, discrete_boltzmann, reference_boltzmann
    )
    fp_to_boltzmann_errors = g6.weighted_relative_errors(
        operator.weights, discrete_fp, reference_boltzmann
    )
    fp_to_fp_errors = g6.weighted_relative_errors(
        operator.weights, discrete_fp, reference_fp
    )

    transition = physical_transition(operator, tau, eigenvalues, eigenvectors)
    row_error = float(np.max(np.abs(np.sum(transition, axis=1) - 1.0)))
    transition_minimum = float(np.min(transition))
    detailed_balance = (
        operator.weights[:, None] * transition
        - operator.weights[None, :] * transition.T
    )
    detailed_balance_error = float(np.max(np.abs(detailed_balance)))

    generator = (transition - np.eye(len(operator.directions))) / tau
    boltzmann_rate = -np.diag(generator)
    offdiag = generator.copy()
    offdiag[np.diag_indices_from(offdiag)] = 0.0
    if float(np.min(offdiag)) < -2.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: negative Boltzmann off-diagonal"
        )
    boltzmann_max_rate = float(np.max(boltzmann_rate))
    fp_max_rate = float(np.max(operator.rate))
    boltzmann_dt = 1.0 / boltzmann_max_rate
    fp_dt = 1.0 / fp_max_rate
    boltzmann_steps = math.ceil(time / (0.9 * boltzmann_dt))
    fp_steps = math.ceil(time / (0.9 * fp_dt))

    initial_mass = g6.weighted_masses(operator.weights, initial)
    final_mass = g6.weighted_masses(operator.weights, discrete_boltzmann)
    mass_error = float(np.max(np.abs(final_mass - initial_mass)))
    minimum_solution = float(np.min(discrete_boltzmann))

    if transition_minimum < -2.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: transition minimum {transition_minimum}"
        )
    if row_error > 3.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: transition row error {row_error}"
        )
    if detailed_balance_error > 3.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: detailed balance error {detailed_balance_error}"
        )
    if mass_error > 3.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: mass error {mass_error}"
        )
    if minimum_solution < -2.0e-10:
        raise AssertionError(
            f"{operator.family}, tau={tau}: negative solution {minimum_solution}"
        )
    if not np.all(boltzmann_modes <= 5.0e-12):
        raise AssertionError("Boltzmann generator has a positive modal eigenvalue")
    # The finite-width generator is less negative than L_h: -beta >= -lambda.
    if np.min(boltzmann_modes - eigenvalues) < -5.0e-11:
        raise AssertionError("finite-width Boltzmann mode decayed faster than FP")

    return AuditRow(
        level=level,
        family=operator.family,
        directions=len(operator.directions),
        tau=tau,
        continuum_model_error_max=float(np.max(continuum_model_errors)),
        discrete_boltzmann_error_max=float(np.max(boltzmann_errors)),
        discrete_fp_to_boltzmann_error_max=float(np.max(fp_to_boltzmann_errors)),
        discrete_fp_to_fp_error_max=float(np.max(fp_to_fp_errors)),
        boltzmann_orientation_spread=float(np.max(boltzmann_errors) - np.min(boltzmann_errors)),
        fp_orientation_spread=float(np.max(fp_to_boltzmann_errors) - np.min(fp_to_boltzmann_errors)),
        boltzmann_max_rate=boltzmann_max_rate,
        fp_max_rate=fp_max_rate,
        boltzmann_dt_limit=boltzmann_dt,
        fp_dt_limit=fp_dt,
        boltzmann_euler_steps=boltzmann_steps,
        fp_euler_steps=fp_steps,
        transition_minimum=transition_minimum,
        transition_row_error=row_error,
        detailed_balance_error=detailed_balance_error,
        boltzmann_mass_error=mass_error,
        boltzmann_minimum_solution=minimum_solution,
    )


def regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    return float(np.sum((lx - np.mean(lx)) * (ly - np.mean(ly))) /
                 np.sum((lx - np.mean(lx)) ** 2))


def write_outputs(rows: Sequence[AuditRow], output_dir: Path, time: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "forward_peaked_heat_scattering_audit.csv"
    md_path = output_dir / "forward_peaked_heat_scattering_audit.md"
    fields = list(AuditRow.__dataclass_fields__)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Gate 6 forward-peaked heat-kernel scattering audit",
        "",
        f"Final time: `{time}`.",
        "",
        "| level | family | K | tau | continuum FP-model error | discrete Boltzmann error | discrete FP-to-Boltzmann error | Boltzmann steps | FP steps |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.tau:.6g} | "
            f"{row.continuum_model_error_max:.8e} | "
            f"{row.discrete_boltzmann_error_max:.8e} | "
            f"{row.discrete_fp_to_boltzmann_error_max:.8e} | "
            f"{row.boltzmann_euler_steps} | {row.fp_euler_steps} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--time", type=float, default=0.1)
    parser.add_argument(
        "--tau", type=float, nargs="+", default=[0.02, 0.005, 0.001, 0.0002]
    )
    parser.add_argument("--output-dir", type=Path, default=Path("gate6/generated"))
    args = parser.parse_args()
    if not 1 <= args.max_level <= 3:
        raise SystemExit("--max-level must be between 1 and 3")
    if args.time <= 0.0 or any(tau <= 0.0 for tau in args.tau):
        raise SystemExit("time and tau values must be positive")

    taus = sorted(args.tau, reverse=True)
    axes = g6.orientations()
    rows: list[AuditRow] = []
    for level in range(1, args.max_level + 1):
        operators = [
            g6.build_icosphere(level),
            g6.build_product(g6.nearest_product_n(10 * 4**level + 2)),
        ]
        for operator in operators:
            family_rows = []
            for tau in taus:
                row = audit_case(level, operator, tau, args.time, axes)
                family_rows.append(row)
                rows.append(row)
                print(
                    f"level={level} family={operator.family} K={row.directions} "
                    f"tau={tau:.6g} model={row.continuum_model_error_max:.3e} "
                    f"Boltz={row.discrete_boltzmann_error_max:.3e} "
                    f"FPcombined={row.discrete_fp_to_boltzmann_error_max:.3e} "
                    f"steps={row.boltzmann_euler_steps}/{row.fp_euler_steps}"
                )
            model_errors = [r.continuum_model_error_max for r in family_rows]
            increasing_errors = list(reversed(model_errors))
            if any(increasing_errors[k + 1] <= increasing_errors[k]
                   for k in range(len(increasing_errors) - 1)):
                raise AssertionError("continuum model error did not increase with tau")
            slope = regression_slope(taus[-3:], model_errors[-3:])
            if not 0.85 <= slope <= 1.15:
                raise AssertionError(f"unexpected small-tau model-error slope {slope}")

    finest_tau = min(taus)
    finest = [r for r in rows if r.level == args.max_level and r.tau == finest_tau]
    ico = next(r for r in finest if r.family.startswith("icosphere"))
    product = next(r for r in finest if r.family.startswith("product"))
    if ico.discrete_boltzmann_error_max >= product.discrete_boltzmann_error_max:
        raise AssertionError("finest quasi-uniform Boltzmann error was not lower")
    if product.fp_euler_steps / ico.fp_euler_steps < 20.0:
        raise AssertionError("FP explicit-step separation is unexpectedly small")
    if product.boltzmann_euler_steps / ico.boltzmann_euler_steps < 5.0:
        raise AssertionError("Boltzmann explicit-step separation is unexpectedly small")

    write_outputs(rows, args.output_dir, args.time)
    print("Gate 6 forward-peaked heat-scattering audit: PASS")


if __name__ == "__main__":
    main()
