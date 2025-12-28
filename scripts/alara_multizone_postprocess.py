#!/usr/bin/env python3
"""
ALARA Multi-Zone Post-Processing Script

This script parses ALARA multi-zone output files (JSON) and produces:
1. CSV files with AVERAGED values across all voxels (with uncertainties)
2. Verification that expected activation products are present

The script averages isotopic values across all voxels and computes 
statistical uncertainties (standard deviation of the mean).

Usage:
    python alara_multizone_postprocess.py --input <alara_output_dir> --output <csv_output_dir>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from alara_output_processing import ALARADFrame, FileParser
from alara_data_loader import format_seconds_label, parse_time_to_seconds

# Use periodictable library for accurate atomic masses
try:
    import periodictable
    HAS_PERIODICTABLE = True
except ImportError:
    HAS_PERIODICTABLE = False
    print("Warning: periodictable not installed. Install with: pip install periodictable")

# Avogadro's number
AVOGADRO = 6.02214076e23


def parse_isotope_name(name: str) -> Tuple[str, int, str]:
    """
    Parse isotope name like 'fe-55' or 'ta-180m' into (element, mass_number, metastable_state).
    """
    # Match patterns like 'fe-55', 'ta-180', 'ta-180m', 'c-12m'
    match = re.match(r'([a-z]+)-(\d+)([a-z]?)$', name.lower())
    if match:
        element = match.group(1)
        mass_num = int(match.group(2))
        meta = match.group(3)
        return element, mass_num, meta
    return name.lower(), 0, ''


def get_atomic_mass(isotope_name: str) -> float:
    """
    Get atomic mass for an isotope using periodictable library.
    Uses mass number if available (more accurate for specific isotopes).
    
    Args:
        isotope_name: Isotope name like 'fe-55' or 'ta-180m'
        
    Returns:
        Atomic mass in amu. Returns mass number for specific isotopes,
        or element average mass if no mass number specified.
    """
    element, mass_num, _ = parse_isotope_name(isotope_name)
    
    # For specific isotopes, use mass number (good approximation)
    if mass_num > 0:
        return float(mass_num)
    
    # For elements without mass number, use periodictable
    if HAS_PERIODICTABLE:
        try:
            elem = getattr(periodictable, element.capitalize(), None)
            if elem is None:
                # Try full element name lookup
                for e in periodictable.elements:
                    if e.symbol.lower() == element.lower():
                        return e.mass
            else:
                return elem.mass
        except Exception:
            pass
    
    # Fallback: return 0 if we can't determine mass
    return 0.0


def get_element_info(element_symbol: str) -> dict:
    """
    Get element information from periodictable library.
    
    Returns dict with 'symbol', 'name', 'mass', 'number'
    """
    if not HAS_PERIODICTABLE:
        return {'symbol': element_symbol, 'name': '', 'mass': 0.0, 'number': 0}
    
    try:
        elem = getattr(periodictable, element_symbol.capitalize(), None)
        if elem:
            return {
                'symbol': elem.symbol,
                'name': elem.name,
                'mass': elem.mass,
                'number': elem.number
            }
    except Exception:
        pass
    
    return {'symbol': element_symbol, 'name': '', 'mass': 0.0, 'number': 0}




def load_alara_zone_data(output_file: str, time_unit: str = 's') -> pd.DataFrame:
    """
    Parse ALARA multi-zone output using the ALARA helper parser.

    Returns a DataFrame filtered to zone blocks only.
    """
    parser = FileParser(output_file, run_lbl=Path(output_file).stem, time_unit=time_unit)
    adf = parser.extract_tables()
    zone_block = ALARADFrame.BLOCK_ENUM['Zone']
    return adf[adf['block'] == zone_block].copy()


def compute_variable_stats(adf: pd.DataFrame, variable_name: str) -> pd.DataFrame:
    """
    Compute voxel mean/std/sem/rel_unc for a single ALARA variable.
    """
    variable_code = ALARADFrame.VARIABLE_ENUM[variable_name]
    subset = adf[adf['variable'] == variable_code]
    if subset.empty:
        return pd.DataFrame()

    grouped = subset.groupby(['nuclide', 'time'])['value']
    stats = grouped.agg(['mean', 'std', 'count']).reset_index()
    stats['sem'] = stats['std'] / np.sqrt(stats['count'])
    with np.errstate(divide='ignore', invalid='ignore'):
        stats['rel_unc'] = np.where(stats['mean'] > 0, stats['sem'] / stats['mean'], 0.0)
    return stats


def build_time_labels(times: List[float]) -> Dict[float, str]:
    """
    Map numeric cooling times to display labels.
    """
    return {t: format_seconds_label(t) for t in times}


def stats_to_csv_table(stats_df: pd.DataFrame, time_labels: Dict[float, str]) -> pd.DataFrame:
    """
    Expand stats into wide CSV format with mean/sem/rel_unc columns.
    """
    if stats_df.empty:
        return pd.DataFrame()

    isotopes = sorted(stats_df['nuclide'].unique())
    output = pd.DataFrame({'isotope': isotopes})

    for time in sorted(time_labels.keys()):
        label = time_labels[time]
        time_slice = stats_df[stats_df['time'] == time].set_index('nuclide')
        output[f'mean_{label}'] = output['isotope'].map(time_slice['mean']).fillna(0.0)
        output[f'sem_{label}'] = output['isotope'].map(time_slice['sem']).fillna(0.0)
        output[f'rel_unc_{label}'] = output['isotope'].map(time_slice['rel_unc']).fillna(0.0)

    return output


def load_json_stats(json_file: str) -> Tuple[Dict[str, pd.DataFrame], Dict[float, str], int]:
    """
    Load ALARA JSON voxel results into stats tables per output type.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    cooling_labels = data.get('cooling_time_labels', [])
    times = [parse_time_to_seconds(label) for label in cooling_labels]
    time_labels = build_time_labels(times)

    voxel_results = data.get('voxel_results', {})
    n_voxels = len(voxel_results)

    output_types = ['number_density', 'specific_activity', 'total_heat']
    rows_by_type = {ot: [] for ot in output_types}

    for voxel_data in voxel_results.values():
        for iso_name, iso_data in voxel_data.get('isotopes', {}).items():
            for output_type in output_types:
                values = iso_data.get(output_type)
                if values is None:
                    continue
                for time, value in zip(times, values):
                    rows_by_type[output_type].append({
                        'nuclide': iso_name,
                        'time': time,
                        'value': value
                    })

    stats_by_type = {}
    for output_type, rows in rows_by_type.items():
        if rows:
            stats_by_type[output_type] = aggregate_stats(pd.DataFrame(rows))
        else:
            stats_by_type[output_type] = pd.DataFrame()

    return stats_by_type, time_labels, n_voxels


def aggregate_stats(values_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate voxel values into mean/std/sem/rel_unc per isotope/time.
    """
    if values_df.empty:
        return pd.DataFrame()

    grouped = values_df.groupby(['nuclide', 'time'])['value']
    stats = grouped.agg(['mean', 'std', 'count']).reset_index()
    stats['sem'] = stats['std'] / np.sqrt(stats['count'])
    with np.errstate(divide='ignore', invalid='ignore'):
        stats['rel_unc'] = np.where(stats['mean'] > 0, stats['sem'] / stats['mean'], 0.0)
    return stats


def calculate_mass_stats(number_density_stats: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate isotopic mass [g/cm³] from number density stats [atoms/cm³].
    """
    if number_density_stats.empty:
        return pd.DataFrame()

    mass_stats = number_density_stats.copy()
    mass_stats['atomic_mass'] = mass_stats['nuclide'].map(get_atomic_mass)
    mass_stats = mass_stats[mass_stats['atomic_mass'] > 0]
    conversion = mass_stats['atomic_mass'] / AVOGADRO
    mass_stats['mean'] = mass_stats['mean'] * conversion
    mass_stats['std'] = mass_stats['std'] * conversion
    mass_stats['sem'] = mass_stats['sem'] * conversion
    return mass_stats


def filter_zero_rows(table: pd.DataFrame) -> pd.DataFrame:
    """
    Drop isotopes with no meaningful mean values.
    """
    mean_cols = [c for c in table.columns if c.startswith('mean_')]
    if not mean_cols:
        return table
    return table[table[mean_cols].abs().max(axis=1) > 1e-30]


def find_activation_products(stats_df: pd.DataFrame, products: List[str]) -> Dict[str, Dict]:
    """
    Search for specific activation products in stats data.
    """
    found = {}
    if stats_df.empty:
        return found

    for product in products:
        iso_stats = stats_df[stats_df['nuclide'] == product]
        if iso_stats.empty:
            continue
        if (iso_stats['mean'].abs() > 1e-30).any():
            found[product] = iso_stats
    return found


def print_activation_summary(found_products: Dict[str, pd.DataFrame],
                             time_labels: Dict[float, str],
                             expected: List[str]):
    """
    Print a summary of found activation products with uncertainties.
    """
    print("\n" + "=" * 80)
    print("ACTIVATION PRODUCTS VERIFICATION (Voxel-Averaged)")
    print("=" * 80)

    times = sorted(time_labels.keys())

    for product in expected:
        if product in found_products:
            data = found_products[product].set_index('time')
            n_voxels = int(found_products[product]['count'].max())
            print(f"\n{product.upper()}: FOUND (averaged over {n_voxels} voxels)")
            print(f"  {'Cooling Time':>12s}  {'Activity (Bq/cm³)':>18s}  {'Uncertainty':>12s}  {'Rel.Unc.':>10s}")
            print(f"  {'-'*12}  {'-'*18}  {'-'*12}  {'-'*10}")
            for time in times:
                ct = time_labels[time]
                if time not in data.index:
                    continue
                mean = data.loc[time, 'mean']
                sem = data.loc[time, 'sem']
                rel = data.loc[time, 'rel_unc']
                if mean > 1e-30:
                    print(f"  {ct:>12s}  {mean:>18.4e}  {sem:>12.4e}  {rel*100:>9.2f}%")
        else:
            print(f"\n{product.upper()}: NOT FOUND")


def main():
    parser = argparse.ArgumentParser(
        description='ALARA Multi-Zone Post-Processing with Voxel Averaging'
    )
    
    parser.add_argument('--input', required=True, 
                        help='ALARA output directory (containing tally_* subdirectories)')
    parser.add_argument('--output', default=None,
                        help='Output directory for CSV files (default: <input>/csv_averaged)')
    parser.add_argument('--tally', default=None,
                        help='Specific tally number to process (default: all)')
    parser.add_argument('--verify', action='store_true',
                        help='Check for expected activation products')
    
    args = parser.parse_args()
    
    if args.output is None:
        args.output = os.path.join(args.input, 'csv_averaged')
    
    # Check periodictable
    if HAS_PERIODICTABLE:
        print(f"Using periodictable library for atomic masses (Fe mass: {periodictable.Fe.mass:.4f} amu)")
    else:
        print("WARNING: periodictable not available, using mass numbers for isotopes")
    
    # Expected activation products for steel/EUROFER materials
    expected_products = [
        'co-60', 'co-58', 'mn-54', 'mn-56', 'fe-55', 'fe-59',
        'cr-51', 'ni-63', 'ta-182', 'ta-180', 'w-187', 'w-185'
    ]
    
    # Find all tally directories
    tally_dirs = []
    for entry in os.listdir(args.input):
        if entry.startswith('tally_'):
            tally_path = os.path.join(args.input, entry)
            if os.path.isdir(tally_path):
                if args.tally is None or args.tally in entry:
                    tally_dirs.append((entry, tally_path))
    
    if not tally_dirs:
        print(f"No tally directories found in {args.input}")
        return 1
    
    print(f"Found {len(tally_dirs)} tally directories")
    
    all_found_products = {}
    
    for tally_name, tally_path in sorted(tally_dirs):
        print(f"\n{'='*60}")
        print(f"Processing {tally_name}")
        print(f"{'='*60}")
        
        # Prefer .out file (has per-zone data) over JSON
        out_file = os.path.join(tally_path, f"{tally_name}_multizone.out")
        json_file = os.path.join(tally_path, f"{tally_name}_results.json")
        
        stats_by_type = {}
        time_labels = {}
        n_voxels = 0

        if os.path.exists(out_file):
            print(f"  Parsing ALARA output: {out_file}")
            adf_zone = load_alara_zone_data(out_file, time_unit='s')
            if adf_zone.empty:
                print("  Warning: No zone data found in output file")
                continue

            n_voxels = adf_zone['block_name'].nunique()
            variable_map = {
                'specific_activity': 'Specific Activity',
                'number_density': 'Number Density',
                'total_heat': 'Total Decay Heat'
            }

            for output_type, variable_name in variable_map.items():
                stats = compute_variable_stats(adf_zone, variable_name)
                stats_by_type[output_type] = stats
                if not time_labels and not stats.empty:
                    time_labels = build_time_labels(sorted(stats['time'].unique()))
        elif os.path.exists(json_file):
            print(f"  Parsing JSON: {json_file}")
            stats_by_type, time_labels, n_voxels = load_json_stats(json_file)
        else:
            print(f"  Warning: No output file found (tried .out and .json)")
            continue

        if not time_labels:
            print("  Warning: No cooling times found")
            continue

        cooling_times = [time_labels[t] for t in sorted(time_labels.keys())]

        print(f"  Found {n_voxels} voxels")
        print(f"  Cooling times: {cooling_times}")

        print(f"\n  Computing voxel averages with uncertainty...")
        stats_by_type['isotopic_mass'] = calculate_mass_stats(
            stats_by_type.get('number_density', pd.DataFrame())
        )

        total_isotopes = 0
        for stats_df in stats_by_type.values():
            if not stats_df.empty:
                total_isotopes = max(total_isotopes, stats_df['nuclide'].nunique())
        print(f"  Processed {total_isotopes} isotopes")

        os.makedirs(args.output, exist_ok=True)

        output_types = ['specific_activity', 'number_density', 'total_heat', 'isotopic_mass']
        units = {
            'specific_activity': 'Bq_per_cm3',
            'number_density': 'atoms_per_cm3',
            'total_heat': 'W_per_cm3',
            'isotopic_mass': 'g_per_cm3'
        }

        print(f"\n  Exporting averaged CSV files...")
        for ot in output_types:
            stats_df = stats_by_type.get(ot, pd.DataFrame())
            if stats_df.empty:
                continue
            csv_file = os.path.join(args.output, f"{tally_name}_{units[ot]}.csv")
            table = stats_to_csv_table(stats_df, time_labels)
            table = filter_zero_rows(table)
            if table.empty:
                continue
            table.to_csv(csv_file, index=False)
            print(f"    Written: {csv_file} ({len(table)} isotopes)")

        if args.verify:
            found = find_activation_products(
                stats_by_type.get('specific_activity', pd.DataFrame()),
                expected_products
            )
            all_found_products[tally_name] = found
            print_activation_summary(found, time_labels, expected_products)
    
    # Final summary
    if args.verify and all_found_products:
        print("\n" + "=" * 80)
        print("OVERALL ACTIVATION PRODUCT SUMMARY")
        print("=" * 80)
        
        for product in expected_products:
            tallies_with_product = [t for t, found in all_found_products.items() if product in found]
            
            if tallies_with_product:
                print(f"  {product:>10s}: FOUND in {len(tallies_with_product)} tallies ✓")
            else:
                print(f"  {product:>10s}: NOT FOUND")
    
    print(f"\nAveraged CSV files written to: {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
