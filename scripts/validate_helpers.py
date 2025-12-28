#!/usr/bin/env python3
"""
Quick validation for helper scripts in /scripts.

This script runs the experimental and flux-wire loaders on the current
repository data to ensure the helpers still perform their core jobs.
"""

import argparse
from pathlib import Path

import pandas as pd

from experimental_data_loader import load_experimental_data
from flux_wire_loader import load_flux_wires, get_metadata_df


def summarize_experimental(exp_dir: Path) -> None:
    print("\n" + "=" * 80)
    print(f"EXPERIMENTAL DATA SUMMARY: {exp_dir}")
    print("=" * 80)
    exp_data = load_experimental_data(exp_data_dir=str(exp_dir), verbose=False)
    total = sum(len(times) for mat in exp_data.values() for times in mat.values())
    print(f"Materials: {len(exp_data)}")
    print(f"Total measurements: {total}")
    for material in sorted(exp_data.keys()):
        cooling_times = sorted(exp_data[material].keys())
        counts = {ct: len(exp_data[material][ct]) for ct in cooling_times}
        print(f"  {material}: {counts}")


def summarize_flux(flux_dir: Path, output_csv: Path) -> None:
    print("\n" + "=" * 80)
    print(f"FLUX WIRE SUMMARY: {flux_dir}")
    print("=" * 80)
    flux_df = load_flux_wires(
        flux_wires_dir=str(flux_dir),
        sample_filter=r'-1($|_)',
        default_irradiation_s=7200,
        output_csv=str(output_csv)
    )
    if flux_df.empty:
        print("No flux wire entries found.")
        return

    meta_df = get_metadata_df()
    print(f"Loaded flux wire rows: {len(flux_df)}")
    print(f"Metadata rows: {len(meta_df)}")
    print(f"Flux wire columns: {sorted(flux_df.columns.tolist())}")

    summary = flux_df.groupby('sample')['isotope'].nunique().reset_index()
    summary = summary.rename(columns={'isotope': 'unique_isotopes'})
    print("\nUnique isotopes per sample:")
    print(summary.to_string(index=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate helper script outputs")
    parser.add_argument(
        '--experimental-dir',
        default='irradiation_QG_processed',
        help='Directory containing RAFM3/RAFM4 experimental data'
    )
    parser.add_argument(
        '--flux-dir',
        default='irradiation_QG_processed/flux_wires',
        help='Directory containing flux wire measurement files'
    )
    parser.add_argument(
        '--output-csv',
        default='alara_output/flux_wires_activity.csv',
        help='Output CSV for flux wire loader'
    )
    args = parser.parse_args()

    experimental_root = Path(args.experimental_dir)
    flux_dir = Path(args.flux_dir)
    output_csv = Path(args.output_csv)

    if not experimental_root.exists():
        print(f"Experimental data directory not found: {experimental_root}")
        return 0

    for subdir in ['RAFM3', 'RAFM4']:
        exp_dir = experimental_root / subdir
        if exp_dir.exists():
            summarize_experimental(exp_dir)
        else:
            print(f"Missing experimental directory: {exp_dir}")

    if flux_dir.exists():
        summarize_flux(flux_dir, output_csv)
    else:
        print(f"Flux wire directory not found: {flux_dir}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
