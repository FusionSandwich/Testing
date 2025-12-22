"""
ALARA Comparison Analysis Module

Compares ALARA simulation results with experimental gamma spectroscopy measurements.
Produces comparison DataFrames for data analysis.

Based on code from MCNP_ALARA_Complete_Workflow_old.ipynb Cell 48, 58.

Key Design Principle:
- Uses dynamic column mapping via alara_data_loader (no hardcoded column names)
- Experimental data structure is kept constant - defined once at notebook start
- ALARA data is loaded dynamically and columns are matched by time parsing

NOTE: Plotting functions have been moved to the consolidated `plotting.py` module.
Import from there for visualization:
    from plotting import plot_comparison_scatter, plot_comparison_by_material
"""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import dynamic column mapping from alara_data_loader
from alara_data_loader import (
    build_cooling_map,
    extract_mean_columns,
    find_closest_column,
    parse_time_to_seconds,
    ALARADataLoader
)

# ============================================================
# Constants
# ============================================================

BQ_TO_UCI = 2.7027e-5  # 1 Bq = 2.7027e-5 µCi

# Half-life unit multipliers
HALF_LIFE_MULTIPLIER = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
    'w': 604800,
    'y': 365.25 * 86400,
}

N_A = 6.02214076e23  # Avogadro's number
U_TO_GRAM = 1.66053906660e-24  # atomic mass unit in grams


# ============================================================
# Helper Functions  
# ============================================================

def _dynamic_column_map(alara_df: pd.DataFrame, exp_cooling_times: List[str]) -> Dict[str, str]:
    """
    Build dynamic column mapping from experimental times to ALARA columns.
    Uses build_cooling_map from alara_data_loader.
    """
    return build_cooling_map(alara_df, exp_cooling_times)

def half_life_to_seconds(half_life_str: str) -> Optional[float]:
    """Convert half-life string like '5.271 y' to seconds."""
    try:
        parts = half_life_str.split()
        if len(parts) != 2:
            return None
        value = float(parts[0])
        unit = parts[1].lower()
        return value * HALF_LIFE_MULTIPLIER.get(unit, 1)
    except Exception:
        return None


def estimate_mass_g_per_cm3_from_activity_uCi(
    activity_uCi: float, 
    half_life_str: str, 
    isotope: str
) -> Optional[float]:
    """Approximate mass concentration from activity using A = λN.
    Assumes mass number ~ atomic mass (no periodictable dependency).
    """
    try:
        if activity_uCi is None or activity_uCi <= 0 or not half_life_str:
            return None
        hl_seconds = half_life_to_seconds(half_life_str)
        if not hl_seconds or hl_seconds <= 0:
            return None
        # Decay constant
        lam = np.log(2) / hl_seconds
        activity_Bq = activity_uCi * 3.7e4
        N_atoms = activity_Bq / lam
        mass_match = re.search(r"(\d+)$", isotope)
        mass_number = float(mass_match.group(1)) if mass_match else None
        if not mass_number:
            return None
        # mass (g) = N_atoms * atomic_mass_u * u_to_g
        return N_atoms * mass_number * U_TO_GRAM
    except Exception:
        return None


def canonical_iso(name: str) -> str:
    """Canonical isotope string preserving metastable states. Examples:
    'Ta-180m' -> 'ta-180m', 'ta180m' -> 'ta-180m', 'Ta_182' -> 'ta-182'
    """
    n = name.strip().lower().replace('_', '-')
    # insert dash before trailing digits if missing
    m = re.match(r"^([a-z]+)-?(\d+m?)$", n)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return n


# ============================================================
# Main Comparison Function
# ============================================================

def compare_alara_to_experiment(
    experimental_data: Dict[str, Dict[str, Dict[str, Any]]],
    alara_output_dir: Path,
    material_to_tally: Dict[str, str],
    verbose: bool = True
) -> pd.DataFrame:
    """
    Compare experimental gamma spectroscopy data with ALARA simulation results.
    
    Uses DYNAMIC column mapping - no hardcoded ALARA column names required.
    The function automatically finds the closest ALARA cooling time column
    for each experimental cooling time by parsing time values.
    
    Parameters
    ----------
    experimental_data : dict
        Nested dictionary: {material: {cooling_time: {isotope: {'activity': float, 'uncertainty': float, 'half_life': str}}}}
        This should be the SAME structure loaded at the start of the notebook.
    alara_output_dir : Path
        Directory containing ALARA output CSV files (e.g., tally_85214_Bq_per_cm3.csv)
    material_to_tally : dict
        Mapping from material name to ALARA tally folder name
        Example: {'CNA': 'tally_85214', 'EUROFER97_A': 'tally_85244', ...}
    verbose : bool
        Whether to print progress messages
        
    Returns
    -------
    pd.DataFrame
        Comparison DataFrame with columns:
        - Material, Isotope, Cooling Time
        - Exp Activity (uCi), Exp Uncertainty (uCi), Exp Half-life, Exp Mass (g/cm³)
        - ALARA Activity (uCi/cm³), ALARA Mass (g/cm³)
        - Status ('MATCHED' or 'MISSING')
    """
    alara_output_dir = Path(alara_output_dir)
    all_comparisons = []
    
    if verbose:
        print("=" * 80)
        print("COMPARISON: EXPERIMENTAL vs ALARA SIMULATION")
        print("=" * 80)
    
    for material, time_data in experimental_data.items():
        tally_folder = material_to_tally.get(material)
        if not tally_folder:
            continue
        
        if verbose:
            print(f"\n{'=' * 70}")
            print(f"MATERIAL: {material} ({tally_folder})")
            print(f"{'=' * 70}")
        
        # ALARA activity and mass files
        alara_activity_file = alara_output_dir / f"{tally_folder}_Bq_per_cm3.csv"
        alara_mass_file = alara_output_dir / f"{tally_folder}_g_per_cm3.csv"
        
        if not alara_activity_file.exists():
            if verbose:
                print(f"  ⚠ Missing ALARA activity file: {alara_activity_file}")
            continue
        
        alara_df = pd.read_csv(alara_activity_file)
        alara_isotopes = alara_df['isotope'].str.lower().tolist()
        if verbose:
            print(f"  ALARA isotopes: {alara_df['isotope'].tolist()}")
        
        alara_mass_df = None
        if alara_mass_file.exists():
            alara_mass_df = pd.read_csv(alara_mass_file)
        elif verbose:
            print(f"  ⚠ Missing ALARA mass file: {alara_mass_file}")
        
        # Build DYNAMIC column mapping for this material's ALARA data
        # This parses time values and finds closest matches
        exp_cooling_times = list(time_data.keys())
        cooling_map = _dynamic_column_map(alara_df, exp_cooling_times)
        
        if verbose:
            print(f"  Dynamic cooling map: {cooling_map}")
        
        for cooling_label, exp_nuclides in time_data.items():
            alara_col = cooling_map.get(cooling_label)
            if not alara_col:
                if verbose:
                    print(f"  ⚠ No matching ALARA column for '{cooling_label}'")
                continue
            
            if alara_col not in alara_df.columns:
                if verbose:
                    print(f"  ⚠ Column {alara_col} not found in ALARA output")
                    print(f"    Available columns: {list(alara_df.columns)}")
                continue
            
            if verbose:
                print(f"\n  Cooling Time: {cooling_label} → {alara_col}")
                print(f"  Experimental isotopes: {list(exp_nuclides.keys())}")
            
            # Try to match each experimental isotope
            matches = []
            for exp_iso, exp_data in exp_nuclides.items():
                exp_canon = canonical_iso(exp_iso)
                exp_uncertainty = exp_data.get('uncertainty')
                exp_half_life = exp_data.get('half_life')
                exp_mass_g_cm3 = estimate_mass_g_per_cm3_from_activity_uCi(
                    exp_data['activity'], exp_half_life, exp_iso
                )
                
                match_found = False
                for alara_iso in alara_isotopes:
                    alara_canon = canonical_iso(alara_iso)
                    # Require exact canonical equality (metastable states stay distinct)
                    if alara_canon == exp_canon:
                        alara_row = alara_df[alara_df['isotope'].str.lower() == alara_iso]
                        if not alara_row.empty:
                            alara_activity_Bq_cm3 = alara_row[alara_col].values[0]
                            alara_activity_uCi_cm3 = alara_activity_Bq_cm3 * BQ_TO_UCI
                            alara_mass_g_cm3 = None
                            if alara_mass_df is not None and alara_col in alara_mass_df.columns:
                                mass_row = alara_mass_df[alara_mass_df['isotope'].str.lower() == alara_iso]
                                if not mass_row.empty:
                                    alara_mass_g_cm3 = mass_row[alara_col].values[0]
                            matches.append({
                                'isotope': exp_iso,
                                'exp_activity_uCi': exp_data['activity'],
                                'exp_uncertainty': exp_uncertainty,
                                'exp_half_life': exp_half_life,
                                'exp_mass_g_cm3': exp_mass_g_cm3,
                                'alara_activity_Bq_cm3': alara_activity_Bq_cm3,
                                'alara_activity_uCi_cm3': alara_activity_uCi_cm3,
                                'alara_mass_g_cm3': alara_mass_g_cm3,
                                'material': material,
                                'cooling_time': cooling_label
                            })
                            match_found = True
                            break
                
                if not match_found:
                    matches.append({
                        'isotope': exp_iso,
                        'exp_activity_uCi': exp_data['activity'],
                        'exp_uncertainty': exp_uncertainty,
                        'exp_half_life': exp_half_life,
                        'exp_mass_g_cm3': exp_mass_g_cm3,
                        'alara_activity_Bq_cm3': None,
                        'alara_activity_uCi_cm3': None,
                        'alara_mass_g_cm3': None,
                        'material': material,
                        'cooling_time': cooling_label
                    })
            
            all_comparisons.extend(matches)
            
            # Print comparison (activities only, no ratios)
            match_count = sum(1 for m in matches if m['alara_activity_Bq_cm3'] is not None)
            if verbose:
                print(f"  Matched isotopes: {match_count}/{len(matches)}")
                
                if match_count > 0:
                    print(f"  {'Isotope':<10} {'Exp (µCi)':<15} {'ALARA (µCi/cm³)':<20}")
                    print(f"  {'-' * 50}")
                    for m in matches:
                        if m['alara_activity_Bq_cm3'] is not None:
                            print(f"  {m['isotope']:<10} {m['exp_activity_uCi']:<15.4g} {m['alara_activity_uCi_cm3']:<20.4g}")
                else:
                    print(f"  ⚠ No isotope matches - experimental isotopes not in ALARA output")
                    
                    # Show top ALARA isotopes by activity (non-zero only)
                    non_zero = alara_df[alara_df[alara_col] > 0]
                    if len(non_zero) > 0:
                        top_alara = non_zero.nlargest(min(5, len(non_zero)), alara_col)[['isotope', alara_col]]
                        print(f"    Top ALARA isotopes at {cooling_label}:")
                        for _, r in top_alara.iterrows():
                            print(f"      {r['isotope']}: {r[alara_col]:.4g} Bq/cm³")
                    else:
                        print(f"    ⚠ No non-zero ALARA activities at {cooling_label}")
    
    # Create summary DataFrame
    if all_comparisons:
        comparison_df = pd.DataFrame(all_comparisons)
        
        # Add standardized column names for plotting/reporting (including mass)
        comparison_df['Material'] = comparison_df['material']
        comparison_df['Isotope'] = comparison_df['isotope']
        comparison_df['Cooling Time'] = comparison_df['cooling_time']
        comparison_df['Exp Activity (uCi)'] = comparison_df['exp_activity_uCi']
        comparison_df['Exp Uncertainty (uCi)'] = comparison_df['exp_uncertainty']
        comparison_df['Exp Half-life'] = comparison_df['exp_half_life']
        comparison_df['Exp Mass (g/cm³)'] = comparison_df['exp_mass_g_cm3']
        comparison_df['ALARA Activity (uCi/cm³)'] = comparison_df['alara_activity_uCi_cm3']
        comparison_df['ALARA Mass (g/cm³)'] = comparison_df['alara_mass_g_cm3']
        comparison_df['Status'] = np.where(comparison_df['alara_activity_Bq_cm3'].notna(), 'MATCHED', 'MISSING')
        
        if verbose:
            matched = comparison_df[comparison_df['Status'] == 'MATCHED']
            unmatched = comparison_df[comparison_df['Status'] == 'MISSING']
            
            print(f"\n{'=' * 80}")
            print("COMPARISON SUMMARY")
            print(f"{'=' * 80}")
            print(f"\nTotal experimental measurements: {len(comparison_df)}")
            print(f"Matched with ALARA: {len(matched)}")
            print(f"Not found in ALARA: {len(unmatched)}")
            
            if not unmatched.empty:
                print(f"\nUnmatched isotopes (experimental only):")
                for iso in unmatched['isotope'].unique():
                    print(f"  - {iso}")
        
        return comparison_df
    else:
        if verbose:
            print("\n⚠ No comparison data generated. Check that experimental and ALARA files exist.")
        return pd.DataFrame()


def get_matched_isotopes(comparison_df: pd.DataFrame) -> pd.DataFrame:
    """Get only the matched isotopes from comparison DataFrame."""
    return comparison_df[comparison_df['Status'] == 'MATCHED'].copy()


def get_unmatched_isotopes(comparison_df: pd.DataFrame) -> pd.DataFrame:
    """Get only the unmatched (missing in ALARA) isotopes from comparison DataFrame."""
    return comparison_df[comparison_df['Status'] == 'MISSING'].copy()


def save_comparison_csv(comparison_df: pd.DataFrame, output_path: Path) -> None:
    """Save comparison DataFrame to CSV."""
    comparison_df.to_csv(output_path, index=False)
    print(f"Comparison saved to: {output_path}")


# ============================================================
# NOTE: Plotting functions moved to plotting.py for consolidation
# Import from there: from plotting import plot_comparison_scatter
# ============================================================


def summarize_comparison(comparison_df: pd.DataFrame) -> None:
    """Print a summary of the comparison analysis."""
    if comparison_df.empty:
        print("No comparison data to summarize!")
        return
    
    print("=" * 70)
    print("COMPARISON ANALYSIS SUMMARY")
    print("=" * 70)
    
    matched = comparison_df[comparison_df['Status'] == 'MATCHED']
    unmatched = comparison_df[comparison_df['Status'] == 'MISSING']
    
    print(f"\n1. MATCHING STATISTICS:")
    print(f"   Total experimental measurements: {len(comparison_df)}")
    print(f"   Matched with ALARA: {len(matched)}")
    print(f"   Not found in ALARA: {len(unmatched)}")
    print(f"   Match rate: {len(matched)/len(comparison_df)*100:.1f}%")
    
    print(f"\n2. BY MATERIAL:")
    for material in sorted(comparison_df['Material'].unique()):
        mat_df = comparison_df[comparison_df['Material'] == material]
        mat_matched = mat_df[mat_df['Status'] == 'MATCHED']
        print(f"   {material}: {len(mat_matched)}/{len(mat_df)} matched")
    
    print(f"\n3. BY COOLING TIME:")
    cooling_order = ['300s', '2h', '24h', '4d', '15d']
    for ct in cooling_order:
        ct_df = comparison_df[comparison_df['Cooling Time'] == ct]
        if ct_df.empty:
            continue
        ct_matched = ct_df[ct_df['Status'] == 'MATCHED']
        print(f"   {ct}: {len(ct_matched)}/{len(ct_df)} matched")
    
    if not unmatched.empty:
        print(f"\n4. UNMATCHED ISOTOPES (experimental only):")
        for iso in sorted(unmatched['isotope'].unique()):
            materials = unmatched[unmatched['isotope'] == iso]['Material'].unique()
            print(f"   - {iso} (in {', '.join(materials)})")


# ============================================================
# DEPRECATED: Plotting functions moved to plotting.py
# These wrappers exist for backwards compatibility only.
# ============================================================

def plot_comparison_scatter(*args, **kwargs):
    """DEPRECATED: Use plotting.plot_comparison_scatter() instead."""
    import warnings
    warnings.warn(
        "plot_comparison_scatter() has moved to plotting.py. "
        "Use: from plotting import plot_comparison_scatter",
        DeprecationWarning, stacklevel=2
    )
    from plotting import plot_comparison_scatter as _plot
    return _plot(*args, **kwargs)


def plot_comparison_by_material(*args, **kwargs):
    """DEPRECATED: Use plotting.plot_comparison_by_material() instead."""
    import warnings
    warnings.warn(
        "plot_comparison_by_material() has moved to plotting.py. "
        "Use: from plotting import plot_comparison_by_material",
        DeprecationWarning, stacklevel=2
    )
    from plotting import plot_comparison_by_material as _plot
    return _plot(*args, **kwargs)


if __name__ == '__main__':
    print("ALARA Comparison Module")
    print("=" * 50)
    print("This module provides functions for comparing ALARA simulation")
    print("results with experimental gamma spectroscopy measurements.")
    print()
    print("Main functions:")
    print("  - compare_alara_to_experiment(): Run full comparison")
    print("  - get_matched_isotopes(): Filter to matched isotopes")
    print("  - get_unmatched_isotopes(): Filter to unmatched isotopes")
    print()
    print("NOTE: Plotting functions moved to plotting.py:")
    print("  from plotting import plot_comparison_scatter, plot_comparison_by_material")
    print("  - plot_comparison_scatter(): Create 2x2 summary plot")
    print("  - plot_comparison_by_material(): Create per-material plots")
    print("  - summarize_comparison(): Print summary statistics")
