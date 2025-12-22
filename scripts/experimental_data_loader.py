"""
Experimental data loader for MCNP-ALARA workflow.

This module parses EXPERIMENTAL gamma spectroscopy files (NOT ALARA output).
For parsing ALARA output files, use alara_output_processing.FileParser instead.

The key difference:
- alara_output_processing: Parses ALARA simulation output tables
- experimental_data_loader: Parses experimental gamma spec measurements (RAFM3, etc.)

These are complementary - you use experimental_data_loader to get measured values,
then compare against ALARA predictions using alara_output_processing.

Usage:
    from experimental_data_loader import (
        load_experimental_data,
        parse_experimental_file,
        SAMPLE_TO_MATERIAL,
        COOLING_TIME_MAP
    )
    
    experimental_data = load_experimental_data('Experimental_Data/RAFM3')
"""

import re
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import from isotope_utils (which uses alara_output_processing where possible)
from isotope_utils import canonical_iso, format_iso_pretty, parse_activity_unit

# ==============================================================================
# SAMPLE MAPPINGS
# ==============================================================================
SAMPLE_TO_MATERIAL = {
    'N': 'CNA',           # tally_85214
    'A': 'EUROFER97_A',   # tally_85244
    'B': 'EUROFER97_B',   # tally_85234
    'C': 'EUROFER97_C',   # tally_85224
}

MATERIAL_TO_TALLY = {
    'CNA': 'tally_85214',
    'EUROFER97_A': 'tally_85244',
    'EUROFER97_B': 'tally_85234',
    'EUROFER97_C': 'tally_85224',
}

COOLING_TIME_MAP = {
    '300sEOI': '300s',
    '2hrEOI': '2h',
    '24hrEOI': '24h',
    '4dEOI': '4d',
    '15dEOI': '15d',
}

# ==============================================================================
# FILE PARSING
# ==============================================================================
# Pattern for parsing activity lines:
# "W187       23.900 h   B   Activity = 0.519 ± 1.63E-02 uCi"
ACTIVITY_PATTERN = re.compile(
    r'^(\w+\d+m?)\s+(\d+\.?\d*)\s*([smhdywk]+)\s+\w+\s+Activity\s*=\s*([0-9.E+-]+)\s*[±�]\s*([0-9.E+%-]+)\s*(\w+)',
    re.IGNORECASE
)


def parse_experimental_file(filepath: str) -> Dict[str, Dict[str, Any]]:
    """
    Parse a gamma spectroscopy file to extract nuclide activities.
    
    Parameters:
        filepath: Path to the experimental data file
    
    Returns:
        Dict mapping isotope names to activity data:
        {
            'w-187': {
                'activity': 0.519,
                'uncertainty': 0.0163,
                'unit': 'uCi',
                'half_life': '23.9 h',
                'rel_unc': 0.0314
            },
            ...
        }
    """
    nuclides = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        return nuclides
    
    for line in content.split('\n'):
        match = ACTIVITY_PATTERN.match(line.strip())
        if not match:
            continue
        
        isotope_raw = match.group(1)
        half_life_val = match.group(2)
        half_life_unit = match.group(3)
        activity = float(match.group(4))
        unc_str = match.group(5)
        unit = match.group(6)
        
        # Parse uncertainty (may be percentage)
        try:
            if '%' in unc_str:
                unc_pct = float(unc_str.replace('%', ''))
                uncertainty = (unc_pct / 100.0) * activity
            else:
                uncertainty = float(unc_str)
        except ValueError:
            uncertainty = 0.0
        
        # Convert isotope name to canonical format (e.g., W187 -> w-187)
        iso_match = re.match(r'([A-Za-z]+)(\d+)(m?)', isotope_raw, re.IGNORECASE)
        if iso_match:
            element = iso_match.group(1).lower()
            mass_num = iso_match.group(2)
            meta = iso_match.group(3).lower() if iso_match.group(3) else ''
            isotope = f"{element}-{mass_num}{meta}"
            
            nuclides[isotope] = {
                'activity': activity,
                'uncertainty': uncertainty,
                'unit': unit,
                'half_life': f"{half_life_val} {half_life_unit}",
                'rel_unc': uncertainty / activity if activity > 0 else 0
            }
    
    return nuclides


def load_experimental_data(
    exp_data_dir: str = 'Experimental_Data/RAFM3',
    sample_letters: Optional[List[str]] = None,
    verbose: bool = True
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Load all experimental data from a directory.
    
    Parameters:
        exp_data_dir: Directory containing experimental data files
        sample_letters: List of samples to load (default: ['A', 'B', 'C', 'N'])
        verbose: Whether to print loading progress
    
    Returns:
        Nested dict structure:
        {
            'EUROFER97_A': {
                '300s': {'w-187': {...}, 'ta-182': {...}, ...},
                '2h': {...},
                ...
            },
            'CNA': {...},
            ...
        }
    """
    exp_dir = Path(exp_data_dir)
    
    # Determine prefix from directory name (e.g. RAFM3, RAFM4)
    # Default to RAFM3 if not found or if directory name doesn't start with RAFM
    prefix = exp_dir.name if exp_dir.name.startswith('RAFM') else 'RAFM3'
    
    if sample_letters is None:
        sample_letters = ['A', 'B', 'C', 'N']
    
    experimental_data = {}
    
    if verbose:
        print("=" * 80)
        print(f"LOADING EXPERIMENTAL DATA FROM {prefix}")
        print("=" * 80)
    
    for sample_letter in sample_letters:
        if sample_letter not in SAMPLE_TO_MATERIAL:
            if verbose:
                print(f"Warning: Unknown sample letter '{sample_letter}'")
            continue
        
        material = SAMPLE_TO_MATERIAL[sample_letter]
        experimental_data[material] = {}
        
        if verbose:
            print(f"\nSample {prefix}-{sample_letter} → {material}:")
        
        for cooling_key, alara_label in COOLING_TIME_MAP.items():
            filename = f"{prefix}-{sample_letter}_{cooling_key}.txt"
            filepath = exp_dir / filename
            
            if filepath.exists():
                nuclides = parse_experimental_file(str(filepath))
                experimental_data[material][alara_label] = nuclides
                
                if verbose:
                    print(f"  {cooling_key}: {len(nuclides)} nuclides detected")
                    for iso, data in nuclides.items():
                        print(f"    {iso}: {data['activity']:.3e} ± {data['uncertainty']:.2e} {data['unit']} (t½={data['half_life']})")
            else:
                if verbose:
                    # Only print if we expect this file to exist (reduce noise)
                    # For RAFM4, we only expect 15dEOI
                    if prefix == 'RAFM4' and cooling_key != '15dEOI':
                        continue
                    if prefix == 'RAFM3' and cooling_key == '15dEOI':
                        continue
                        
                    print(f"  {cooling_key}: File not found")
    
    # Summary
    if verbose:
        print("\n" + "=" * 80)
        print("EXPERIMENTAL ISOTOPES SUMMARY")
        print("=" * 80)
        all_isotopes = get_all_isotopes(experimental_data)
        print(f"Unique isotopes detected: {sorted(all_isotopes)}")
    
    return experimental_data


def get_all_isotopes(experimental_data: Dict) -> set:
    """Get set of all unique isotopes across all materials and times."""
    isotopes = set()
    for mat_data in experimental_data.values():
        for time_data in mat_data.values():
            isotopes.update(time_data.keys())
    return isotopes


def experimental_to_dataframe(experimental_data: Dict) -> pd.DataFrame:
    """
    Convert experimental data dict to a flat DataFrame.
    
    Returns DataFrame with columns:
        material, cooling_time, isotope, activity, uncertainty, unit, half_life, rel_unc
    """
    records = []
    
    for material, time_data in experimental_data.items():
        for cooling_time, nuclides in time_data.items():
            for isotope, data in nuclides.items():
                records.append({
                    'material': material,
                    'cooling_time': cooling_time,
                    'isotope': isotope,
                    'activity': data['activity'],
                    'uncertainty': data['uncertainty'],
                    'unit': data['unit'],
                    'half_life': data['half_life'],
                    'rel_unc': data['rel_unc']
                })
    
    return pd.DataFrame(records)


def get_top_isotopes(
    experimental_data: Dict,
    material: Optional[str] = None,
    top_n: int = 3
) -> Dict[str, List[tuple]]:
    """
    Get top N isotopes by total activity for each material.
    
    Parameters:
        experimental_data: Loaded experimental data
        material: Specific material to analyze (None = all materials)
        top_n: Number of top isotopes to return
    
    Returns:
        Dict mapping material to list of (isotope, total_activity_bq) tuples
    """
    results = {}
    
    materials = [material] if material else experimental_data.keys()
    
    for mat in materials:
        if mat not in experimental_data:
            continue
        
        # Sum activities across all cooling times
        isotope_totals = {}
        
        for time_data in experimental_data[mat].values():
            for iso, data in time_data.items():
                # Convert to Bq for consistent comparison
                factor = parse_activity_unit(data.get('unit', 'uCi'))
                act_bq = data['activity'] * factor
                
                if iso not in isotope_totals:
                    isotope_totals[iso] = 0
                isotope_totals[iso] += act_bq
        
        # Sort and get top N
        sorted_isos = sorted(isotope_totals.items(), key=lambda x: x[1], reverse=True)
        results[mat] = sorted_isos[:top_n]
    
    return results


def activity_to_bq(activity: float, unit: str) -> float:
    """Convert activity to Bq using unit string."""
    factor = parse_activity_unit(unit)
    return activity * factor


if __name__ == '__main__':
    # Test loading
    print("Testing experimental_data_loader...")
    
    exp_data = load_experimental_data(verbose=True)
    
    if exp_data:
        print("\n\nConverting to DataFrame...")
        df = experimental_to_dataframe(exp_data)
        print(df.head(10))
        
        print("\n\nTop isotopes by material:")
        top = get_top_isotopes(exp_data, top_n=3)
        for mat, isos in top.items():
            print(f"\n{mat}:")
            for iso, act in isos:
                print(f"  {iso}: {act:.2e} Bq")
    else:
        print("No data loaded (check if Experimental_Data/RAFM3 exists)")
