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
import csv
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

import numpy as np

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


def parse_json_results_all_voxels(json_file: str) -> Dict:
    """
    Parse ALARA results from JSON file, returning data for ALL voxels.
    
    Returns a dictionary with:
    {
        'voxels': {
            voxel_id: {
                'isotopes': {
                    isotope_name: {
                        'number_density': [...],
                        'specific_activity': [...],
                        'total_heat': [...]
                    }
                }
            }
        },
        'cooling_times': [...],
        'n_voxels': int
    }
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    results = {
        'voxels': {},
        'cooling_times': data.get('cooling_time_labels', []),
        'material': data.get('material', 'unknown'),
        'tally_number': data.get('tally_number', 0),
        'n_voxels': 0
    }
    
    # Handle voxel_results format
    voxel_results = data.get('voxel_results', {})
    
    for voxel_id, voxel_data in voxel_results.items():
        results['voxels'][voxel_id] = {
            'isotopes': voxel_data.get('isotopes', {})
        }
        results['n_voxels'] += 1
    
    return results


def parse_alara_multizone_output(output_file: str) -> Dict:
    """
    Parse ALARA multi-zone .out file to extract per-zone isotope data.
    
    Returns a dictionary with same structure as parse_json_results_all_voxels.
    """
    results = {
        'voxels': {},
        'cooling_times': [],
        'material': 'unknown',
        'n_voxels': 0
    }
    
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Find output type sections
    output_types = {
        'number_density': r'\*\*\* Number Density \[atoms/cm3\] \*\*\*',
        'specific_activity': r'\*\*\* Specific Activity \[Bq/cm3\] \*\*\*',
        'total_heat': r'\*\*\* Total Decay Heat \[W/cm3\] \*\*\*'
    }
    
    for output_type, pattern in output_types.items():
        # Find the section
        match = re.search(pattern, content)
        if not match:
            continue
            
        # Extract from this point to the next *** section or end
        start = match.end()
        next_section = re.search(r'\n\*\*\*', content[start:])
        if next_section:
            section_content = content[start:start + next_section.start()]
        else:
            section_content = content[start:]
        
        # Parse zones within this section
        zone_pattern = r'Zone #(\d+): (zone_\d+)'
        zone_matches = list(re.finditer(zone_pattern, section_content))
        
        for i, zone_match in enumerate(zone_matches):
            zone_num = zone_match.group(1)
            zone_name = zone_match.group(2)
            voxel_id = zone_name.replace('zone_', '')
            
            # Get content until next zone or end of section
            zone_start = zone_match.end()
            if i + 1 < len(zone_matches):
                zone_end = zone_matches[i + 1].start()
            else:
                zone_end = len(section_content)
            
            zone_content = section_content[zone_start:zone_end]
            
            # Initialize voxel if needed
            if voxel_id not in results['voxels']:
                results['voxels'][voxel_id] = {'isotopes': {}}
                results['n_voxels'] += 1
            
            # Find the data table in this zone
            # Look for the header line: "isotope  shutdown  ..."
            header_match = re.search(r'isotope\s+(shutdown.*?)(?:\n|$)', zone_content)
            if not header_match:
                continue
            
            # Extract cooling times from header (only once)
            # Header looks like: "shutdown         0 s         3 d         7 d        45 d         1 y"
            # or with decimals: "shutdown      5.95 m   25.5469 h    3.9491 d"
            # Need to combine value+unit pairs like "0 s" -> "0s", "5.95 m" -> "5.95m"
            if not results['cooling_times']:
                header_text = header_match.group(1)
                # Parse by fixed column widths or regex
                # Pattern: number (with optional decimal) followed by unit, or 'shutdown'
                # Match integers or decimals like: 0, 3, 45, 5.95, 25.5469
                parts = re.findall(r'(\d+\.?\d*)\s+([smhdy])|shutdown', header_text)
                cooling_times = ['shutdown']
                for match in parts:
                    if match[0]:  # number+unit pair
                        cooling_times.append(f"{match[0]}{match[1]}")
                results['cooling_times'] = cooling_times
            
            # Find the data lines (after the === separator)
            data_start = header_match.end()
            # Skip separator line
            sep_match = re.search(r'=+\n', zone_content[data_start:])
            if sep_match:
                data_start += sep_match.end()
            
            # Parse data lines until we hit an empty line or a non-data line
            lines = zone_content[data_start:].split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('=') or line.startswith('-'):
                    continue
                if line.startswith('Zone') or line.startswith('Constituent') or line.startswith('Total'):
                    break
                
                parts = line.split()
                if len(parts) < 2:
                    continue
                
                isotope = parts[0]
                try:
                    values = [float(v) for v in parts[1:]]
                except ValueError:
                    continue
                
                # Store in isotopes dict
                if isotope not in results['voxels'][voxel_id]['isotopes']:
                    results['voxels'][voxel_id]['isotopes'][isotope] = {}
                
                results['voxels'][voxel_id]['isotopes'][isotope][output_type] = values
    
    return results


def compute_voxel_averages_with_uncertainty(all_voxel_data: Dict) -> Dict:
    """
    Compute average values across all voxels with statistical uncertainty.
    
    For each isotope and each cooling time, computes:
    - mean: arithmetic mean across voxels
    - std: standard deviation across voxels  
    - sem: standard error of the mean (std / sqrt(n))
    - rel_unc: relative uncertainty (sem / mean)
    
    Args:
        all_voxel_data: Dict from parse_json_results_all_voxels
        
    Returns:
        Dict with averaged isotope data and uncertainties
    """
    cooling_times = all_voxel_data['cooling_times']
    n_times = len(cooling_times)
    n_voxels = all_voxel_data['n_voxels']
    
    if n_voxels == 0:
        return {}
    
    # Collect all isotope data across voxels
    # Structure: {isotope: {output_type: [[values_per_time] for each voxel]}}
    isotope_collections = defaultdict(lambda: defaultdict(list))
    
    for voxel_id, voxel_data in all_voxel_data['voxels'].items():
        for iso_name, iso_data in voxel_data.get('isotopes', {}).items():
            if isinstance(iso_data, dict):
                for output_type in ['number_density', 'specific_activity', 'total_heat']:
                    if output_type in iso_data:
                        values = iso_data[output_type]
                        isotope_collections[iso_name][output_type].append(values)
    
    # Compute statistics for each isotope
    averaged = {}
    
    for iso_name, output_types in isotope_collections.items():
        averaged[iso_name] = {}
        
        for output_type, voxel_values_list in output_types.items():
            # Convert to numpy array: shape (n_voxels, n_cooling_times)
            arr = np.array(voxel_values_list)
            
            # Compute statistics along voxel axis (axis=0)
            mean_vals = np.mean(arr, axis=0)
            std_vals = np.std(arr, axis=0, ddof=1)  # Sample std dev
            n = arr.shape[0]
            sem_vals = std_vals / np.sqrt(n)  # Standard error of mean
            
            # Relative uncertainty (handle division by zero)
            with np.errstate(divide='ignore', invalid='ignore'):
                rel_unc = np.where(mean_vals > 0, sem_vals / mean_vals, 0.0)
            
            averaged[iso_name][output_type] = {
                'mean': mean_vals.tolist(),
                'std': std_vals.tolist(),
                'sem': sem_vals.tolist(),
                'rel_unc': rel_unc.tolist(),
                'n_voxels': n
            }
    
    return averaged


def calculate_isotopic_mass_with_uncertainty(averaged_data: Dict) -> Dict:
    """
    Calculate isotopic mass [g/cm³] from number density [atoms/cm³].
    
    mass = number_density × atomic_mass / Avogadro
    
    Uncertainty propagates linearly since atomic mass has no uncertainty.
    """
    mass_data = {}
    
    for isotope, output_types in averaged_data.items():
        if 'number_density' not in output_types:
            continue
            
        nd_data = output_types['number_density']
        atomic_mass = get_atomic_mass(isotope)
        
        if atomic_mass <= 0:
            continue
        
        conversion = atomic_mass / AVOGADRO
        
        mass_data[isotope] = {
            'mean': [v * conversion for v in nd_data['mean']],
            'std': [v * conversion for v in nd_data['std']],
            'sem': [v * conversion for v in nd_data['sem']],
            'rel_unc': nd_data['rel_unc'],  # Relative uncertainty unchanged
            'n_voxels': nd_data['n_voxels']
        }
    
    return mass_data


def export_averaged_csv(averaged_data: Dict, output_type: str, cooling_times: List[str],
                        output_file: str, filter_zeros: bool = True):
    """
    Export averaged data to CSV with uncertainties.
    
    Format:
    isotope, mean_t0, unc_t0, mean_t1, unc_t1, ...
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Filter data
    if filter_zeros:
        filtered = {k: v for k, v in averaged_data.items() 
                   if output_type in v and any(abs(val) > 1e-30 for val in v[output_type]['mean'])}
    else:
        filtered = {k: v for k, v in averaged_data.items() if output_type in v}
    
    if not filtered:
        return 0
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header: isotope, mean_t0, sem_t0, rel_unc_t0, ...
        header = ['isotope']
        for ct in cooling_times:
            header.extend([f'mean_{ct}', f'sem_{ct}', f'rel_unc_{ct}'])
        writer.writerow(header)
        
        # Data rows
        for isotope in sorted(filtered.keys()):
            data = filtered[isotope][output_type]
            row = [isotope]
            for i in range(len(cooling_times)):
                row.extend([
                    data['mean'][i],
                    data['sem'][i],
                    data['rel_unc'][i]
                ])
            writer.writerow(row)
    
    return len(filtered)


def find_activation_products(averaged_data: Dict, products: List[str]) -> Dict:
    """
    Search for specific activation products in averaged data.
    """
    found = {}
    
    for product in products:
        if product in averaged_data:
            iso_data = averaged_data[product]
            if 'specific_activity' in iso_data:
                sa = iso_data['specific_activity']
                if any(abs(v) > 1e-30 for v in sa['mean']):
                    found[product] = sa
    
    return found


def print_activation_summary(found_products: Dict, cooling_times: List[str], expected: List[str]):
    """
    Print a summary of found activation products with uncertainties.
    """
    print("\n" + "=" * 80)
    print("ACTIVATION PRODUCTS VERIFICATION (Voxel-Averaged)")
    print("=" * 80)
    
    for product in expected:
        if product in found_products:
            data = found_products[product]
            print(f"\n{product.upper()}: FOUND (averaged over {data['n_voxels']} voxels)")
            print(f"  {'Cooling Time':>12s}  {'Activity (Bq/cm³)':>18s}  {'Uncertainty':>12s}  {'Rel.Unc.':>10s}")
            print(f"  {'-'*12}  {'-'*18}  {'-'*12}  {'-'*10}")
            for i, ct in enumerate(cooling_times):
                mean = data['mean'][i]
                sem = data['sem'][i]
                rel = data['rel_unc'][i]
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
        
        if os.path.exists(out_file):
            print(f"  Parsing ALARA output: {out_file}")
            all_voxel_data = parse_alara_multizone_output(out_file)
        elif os.path.exists(json_file):
            print(f"  Parsing JSON: {json_file}")
            all_voxel_data = parse_json_results_all_voxels(json_file)
        else:
            print(f"  Warning: No output file found (tried .out and .json)")
            continue
        
        n_voxels = all_voxel_data['n_voxels']
        cooling_times = all_voxel_data['cooling_times']
        
        print(f"  Found {n_voxels} voxels")
        print(f"  Cooling times: {cooling_times}")
        print(f"  Material: {all_voxel_data.get('material', 'unknown')}")
        
        # Compute averages with uncertainty
        print(f"\n  Computing voxel averages with uncertainty...")
        averaged = compute_voxel_averages_with_uncertainty(all_voxel_data)
        
        # Calculate isotopic mass
        mass_data = calculate_isotopic_mass_with_uncertainty(averaged)
        
        # Add mass data to averaged dict
        for iso, mass_vals in mass_data.items():
            if iso in averaged:
                averaged[iso]['isotopic_mass'] = mass_vals
        
        print(f"  Processed {len(averaged)} isotopes")
        
        # Export CSVs
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
            csv_file = os.path.join(args.output, f"{tally_name}_{units[ot]}.csv")
            n_isotopes = export_averaged_csv(averaged, ot, cooling_times, csv_file)
            if n_isotopes > 0:
                print(f"    Written: {csv_file} ({n_isotopes} isotopes)")
        
        # Verify activation products
        if args.verify:
            found = find_activation_products(averaged, expected_products)
            all_found_products[tally_name] = found
            print_activation_summary(found, cooling_times, expected_products)
    
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
