"""
Flux Mesh Analysis Utilities
=============================

Functions for analyzing neutron flux measurements from MCNP mesh tallies,
comparing flux across voxels, materials, and experiments.

This module provides:
- `analyze_flux_spectrum`: Extract flux spectra from HDF5 mesh tallies
- `compare_materials_flux`: Compare total flux between materials/tallies
- `plot_flux_spectra`: Plot energy spectra with multi-voxel comparison
- `normalize_cooling_time`: Standardize cooling time labels
- `extract_time_from_label`: Convert time labels to days
- `get_top_isotopes_from_df`: Get top contributors from activity DataFrame
- `load_activity_data`: Load ALARA activity CSV files

Relationship with ALARA Tools:
- Uses alara_output_processing.py for parsing ALARA output when available
- Complements (does not duplicate) FileParser and DataLibrary classes
- Focuses on MESH TALLY analysis and flux calculations

Author: MCNP-ALARA Workflow
"""

import re
import sys
import glob
import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any, Union

import numpy as np
import pandas as pd

# Add tools directory to path for alara_output_processing imports
_tools_dir = Path(__file__).parent.parent / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

from alara_output_processing import SECONDS_CONV

# Optional imports
try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False
    print("Warning: h5py not available. HDF5 mesh tally functions disabled.")

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ==============================================================================
# TIME HANDLING UTILITIES
# ==============================================================================

# Time units for conversion to days (derived from SECONDS_CONV)
TIME_UNITS = {unit: secs / SECONDS_CONV['d'] for unit, secs in SECONDS_CONV.items()}


def extract_time_from_label(label: str) -> float:
    """
    Convert a cooling time label to days.
    
    Parameters
    ----------
    label : str
        Time label like "300s", "2h", "24h", "4d", "15d", "shutdown", "0s"
    
    Returns
    -------
    float
        Time in days. Returns 0.001 for shutdown/0s for log scale compatibility.
    
    Examples
    --------
    >>> extract_time_from_label("2h")
    0.08333...
    >>> extract_time_from_label("15d")
    15.0
    >>> extract_time_from_label("shutdown")
    0.001
    """
    label_lower = label.lower().strip()
    
    if 'shutdown' in label_lower or label_lower == '0s':
        return 0.001  # Small value for log scale
    
    # Match patterns like "300s", "2h", "24h", "4d", "15d", "1.5y"
    match = re.match(r'(\d+\.?\d*)\s*([smhdwy])', label_lower)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        return value * TIME_UNITS.get(unit, 1.0)
    
    return 0.001  # Default fallback


def normalize_cooling_time(time_label: str, exclude_shutdown: bool = True) -> Optional[str]:
    """
    Normalize cooling time labels to experimental measurement groups.
    
    Maps ALARA cooling times to the closest experimental measurement category:
    - 300s (5 min after first 3s irradiation)
    - 2h (after first 3s irradiation)
    - 24h (after first 3s irradiation)
    - 4d (after first 3s irradiation)
    - 15d (after second 2h irradiation)
    
    Parameters
    ----------
    time_label : str
        Original time label from ALARA output (e.g., "5m", "2.5h", "shutdown")
    exclude_shutdown : bool
        If True, return None for shutdown times (default: True)
    
    Returns
    -------
    str or None
        Normalized time label matching experimental groups, or None if shutdown
    
    Examples
    --------
    >>> normalize_cooling_time("1.00000e-03 s")
    None  # shutdown excluded
    >>> normalize_cooling_time("5m")
    '300s'
    >>> normalize_cooling_time("6m")
    '300s'
    >>> normalize_cooling_time("2.5h")
    '2h'
    >>> normalize_cooling_time("26h")
    '24h'
    >>> normalize_cooling_time("19d")
    '15d'
    """
    if not time_label or pd.isna(time_label):
        return None
    
    label = str(time_label).strip().lower()
    
    # Shutdown is not a real measurement time - exclude it
    if 'shutdown' in label:
        return None if exclude_shutdown else 'shutdown'
    
    # Experimental measurement groups in seconds
    # These are the actual measurement times after irradiation
    EXP_GROUPS = {
        '300s': 300,       # 5 min (first measurement after 3s irradiation)
        '2h': 7200,        # 2 hours
        '24h': 86400,      # 24 hours (1 day)
        '4d': 345600,      # 4 days
        '15d': 1296000,    # 15 days (after 2h irradiation)
    }
    
    # Parse the time label to get seconds
    match = re.match(r'([+-]?\d+\.?\d*(?:e[+-]?\d+)?)\s*([smhdwy])', label)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        
        # Convert to seconds
        seconds = value * {
            's': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31557600
        }.get(unit, 1)
        
        # Near-zero means shutdown - exclude
        if seconds < 1:
            return None if exclude_shutdown else 'shutdown'
        
        # Find the closest experimental group
        closest_group = None
        min_ratio = float('inf')
        
        for group_name, group_seconds in EXP_GROUPS.items():
            # Use log ratio to find closest match (works better across orders of magnitude)
            if seconds > 0 and group_seconds > 0:
                ratio = abs(np.log10(seconds / group_seconds))
                if ratio < min_ratio:
                    min_ratio = ratio
                    closest_group = group_name
        
        # Only accept if within a reasonable factor (e.g., 3x)
        if closest_group and min_ratio < np.log10(3):
            return closest_group
        
        # Fallback: format as readable time if no close match
        if seconds >= 86400:
            return f"{int(round(seconds / 86400))}d"
        elif seconds >= 3600:
            return f"{int(round(seconds / 3600))}h"
        elif seconds >= 60:
            return f"{int(round(seconds / 60))}m"
        else:
            return f"{int(seconds)}s"
    
    # Check if label already matches an experimental group
    for group in EXP_GROUPS.keys():
        if group in label:
            return group
    
    return time_label


# ==============================================================================
# HDF5 MESH TALLY ANALYSIS
# ==============================================================================

def analyze_flux_spectrum(h5_file: str, tally_num: int) -> Dict[str, Any]:
    """
    Analyze energy-dependent flux spectrum across voxels for a mesh tally.
    
    Parameters
    ----------
    h5_file : str
        Path to the HDF5 file containing mesh tally results
    tally_num : int
        Mesh tally number (e.g., 85214)
    
    Returns
    -------
    dict
        Dictionary containing:
        - n_groups: Number of energy groups
        - n_voxels: Number of spatial voxels
        - mean_spectrum: Average flux over all voxels (array of length n_groups)
        - energy_bins: Energy bin boundaries (array of length n_groups+1)
        - total_flux_per_voxel: Total flux for each voxel
        - flux_data: Full flux array (n_groups x n_voxels)
    
    Raises
    ------
    ImportError
        If h5py is not available
    FileNotFoundError
        If HDF5 file doesn't exist
    KeyError
        If tally not found in HDF5 file
    
    Examples
    --------
    >>> fa = analyze_flux_spectrum('runtpe.h5', 85214)
    >>> print(f"Energy groups: {fa['n_groups']}, Voxels: {fa['n_voxels']}")
    """
    if not HAS_H5PY:
        raise ImportError("h5py is required for HDF5 mesh tally analysis")
    
    with h5py.File(h5_file, 'r') as f:
        tally_key = f'mesh_tally_{tally_num}'
        if tally_key not in f['results']['mesh_tally']:
            raise KeyError(f"Tally {tally_key} not found in {h5_file}")
        
        mt = f['results']['mesh_tally'][tally_key]
        
        # Get flux values
        # Shape is (n_groups+1, 1, nx, ny, nz) where last group is total
        raw_flux = mt['mean'][:]
        
        # Separate energy groups and total
        flux_groups = raw_flux[:-1]  # Exclude total group
        total_flux_data = raw_flux[-1]  # The total group
        
        # Reshape to (n_groups, n_voxels)
        n_groups = flux_groups.shape[0]
        flux = flux_groups.reshape(n_groups, -1)
        n_voxels = flux.shape[1]
        
        # Flatten total flux to match voxels
        total_flux = total_flux_data.flatten()
        
        # Statistics across voxels
        mean_spectrum = flux.mean(axis=1)
        
        # Get energy bins
        try:
            energy_bins = mt['grid_energy'][:]
        except KeyError:
            # Fallback if grid_energy missing
            energy_bins = np.arange(n_groups + 1)
        
        return {
            'n_groups': n_groups,
            'n_voxels': n_voxels,
            'mean_spectrum': mean_spectrum,
            'energy_bins': energy_bins,
            'total_flux_per_voxel': total_flux,
            'flux_data': flux
        }


def compare_materials_flux(flux_analysis: Dict[int, Dict], 
                           material_names: Dict[str, str]) -> pd.DataFrame:
    """
    Compare total flux between different materials/tallies.
    
    Parameters
    ----------
    flux_analysis : dict
        Dictionary mapping tally numbers to analyze_flux_spectrum results
    material_names : dict
        Dictionary mapping tally keys (e.g., 'tally_85214') to material names
    
    Returns
    -------
    pd.DataFrame
        Comparison table with columns:
        - Tally, Material, Mean Flux, Min Flux, Max Flux, Spatial Std Dev, Spatial CV (%)
    """
    comparison = []
    
    for tally_num, flux_data in flux_analysis.items():
        material = material_names.get(f'tally_{tally_num}', 'unknown')
        total_flux_per_voxel = flux_data['total_flux_per_voxel']
        mean_total = total_flux_per_voxel.mean()
        std_total = total_flux_per_voxel.std()
        
        comparison.append({
            'Tally': tally_num,
            'Material': material,
            'Mean Flux (n/cm²/src)': mean_total,
            'Min Flux': total_flux_per_voxel.min(),
            'Max Flux': total_flux_per_voxel.max(),
            'Spatial Std Dev': std_total,
            'Spatial CV (%)': (std_total / mean_total * 100) if mean_total > 0 else 0,
        })
    
    return pd.DataFrame(comparison)


def plot_flux_spectra(flux_analysis: Dict[int, Dict],
                      material_names: Dict[str, str],
                      max_voxels_per_plot: int = 8,
                      figsize: Tuple[int, int] = (15, 10),
                      save_path: Optional[str] = None) -> None:
    """
    Plot flux spectra comparing different voxels within each material.
    
    Parameters
    ----------
    flux_analysis : dict
        Dictionary mapping tally numbers to analyze_flux_spectrum results
    material_names : dict
        Dictionary mapping tally keys to material names
    max_voxels_per_plot : int
        Maximum number of individual voxel spectra to plot
    figsize : tuple
        Figure size (width, height)
    save_path : str, optional
        Path to save the figure
    """
    if not HAS_MATPLOTLIB:
        print("matplotlib not available for plotting")
        return
    
    n_plots = min(len(flux_analysis), 6)
    n_rows = (n_plots + 2) // 3
    n_cols = min(3, n_plots)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_plots == 1:
        axes = np.array([[axes]])
    elif n_plots <= n_cols:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for plot_idx, (tally_num, flux_data) in enumerate(flux_analysis.items()):
        if plot_idx >= len(axes):
            break
        
        material = material_names.get(f'tally_{tally_num}', 'unknown')
        flux_per_voxel = flux_data['flux_data']
        energy_bins = flux_data['energy_bins']
        n_voxels = flux_data['n_voxels']
        
        # Energy bin centers (geometric mean) for proper VITAMIN-J structure
        e_centers = np.sqrt(energy_bins[:-1] * energy_bins[1:])
        
        ax = axes[plot_idx]
        
        # Plot a subset of voxels to avoid clutter
        n_plot = min(max_voxels_per_plot, n_voxels)
        voxel_indices = np.linspace(0, n_voxels - 1, n_plot, dtype=int)
        
        for v_idx in voxel_indices:
            flux = flux_per_voxel[:, v_idx]
            mask = flux > 0
            if mask.any():
                ax.loglog(e_centers[mask], flux[mask], 'o-', 
                         alpha=0.5, markersize=2, label=f'Voxel {v_idx + 1}')
        
        # Plot mean spectrum
        mean_spectrum = flux_per_voxel.mean(axis=1)
        mask = mean_spectrum > 0
        ax.loglog(e_centers[mask], mean_spectrum[mask], 'k-', linewidth=2, label='Mean')
        
        ax.set_xlabel('Energy (MeV)')
        ax.set_ylabel('Flux (n/cm²/src)')
        ax.set_title(f'{material} (Tally {tally_num})')
        ax.set_xlim(1e-11, 20)
        ax.legend(fontsize=7, ncol=2)
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(flux_analysis), len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('Neutron Flux Spectra by Voxel (VITAMIN-J 175-group)', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved flux spectra plot to: {save_path}")
    
    plt.show()


def print_flux_summary(flux_analysis: Dict[int, Dict], 
                       material_names: Dict[str, str]) -> None:
    """Print a formatted summary table of flux statistics by tally."""
    print("=" * 105)
    print("FLUX SUMMARY BY TALLY:")
    print("=" * 105)
    print(f"{'Tally':<10} {'Material':<15} {'Mean Flux':>15} {'Min Flux':>15} "
          f"{'Max Flux':>15} {'Rel. Std Dev':>15}")
    print("-" * 105)
    
    for tally_num, fa in flux_analysis.items():
        material = material_names.get(f'tally_{tally_num}', 'unknown')
        mean_total = fa['total_flux_per_voxel'].mean()
        min_total = fa['total_flux_per_voxel'].min()
        max_total = fa['total_flux_per_voxel'].max()
        rse = fa['total_flux_per_voxel'].std() / mean_total if mean_total > 0 else 0
        
        print(f" {tally_num:<10} {material:<15} {mean_total:>15.6e} "
              f"{min_total:>15.6e} {max_total:>15.6e} {rse:>15.6f}")


# ==============================================================================
# ACTIVITY DATA LOADING AND PROCESSING
# ==============================================================================

def load_activity_data(output_dir: str,
                       pattern: str = 'tally_*_Bq_per_cm3.csv',
                       material_names: Optional[Dict[str, str]] = None
                       ) -> Dict[str, Dict]:
    """
    Load ALARA activity CSV files from output directory.
    
    Parameters
    ----------
    output_dir : str
        Directory containing ALARA output CSV files
    pattern : str
        Glob pattern for activity files
    material_names : dict, optional
        Mapping of tally names to material names
    
    Returns
    -------
    dict
        Dictionary mapping tally names to {'material': str, 'data': DataFrame}
    """
    if material_names is None:
        material_names = {}
    
    activity_data = {}
    
    for csv_file in sorted(glob.glob(os.path.join(output_dir, pattern))):
        tally_name = os.path.basename(csv_file).replace('_Bq_per_cm3.csv', '')
        material = material_names.get(tally_name, 'unknown')
        df = pd.read_csv(csv_file)
        activity_data[tally_name] = {'material': material, 'data': df}
        
        print(f"Loaded {tally_name} ({material}): {len(df)} isotopes")
    
    return activity_data


def get_top_isotopes_from_df(df: pd.DataFrame, 
                              n: int = 10, 
                              column: Optional[str] = None) -> List[str]:
    """
    Get top N contributing isotopes from an activity DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'isotope' column and activity columns (mean_*)
    n : int
        Number of top isotopes to return
    column : str, optional
        Specific column to use. If None, uses first mean_* column.
    
    Returns
    -------
    list
        List of isotope names
    """
    if column is None:
        mean_cols = [c for c in df.columns if c.startswith('mean_')]
        if not mean_cols:
            return []
        column = mean_cols[0]
    
    return df.nlargest(n, column)['isotope'].tolist()


def load_decay_heat_data(output_dir: str,
                         pattern: str = 'tally_*_W_per_cm3.csv',
                         material_names: Optional[Dict[str, str]] = None
                         ) -> Dict[str, Dict]:
    """
    Load ALARA decay heat CSV files from output directory.
    
    Parameters
    ----------
    output_dir : str
        Directory containing ALARA output CSV files
    pattern : str
        Glob pattern for decay heat files
    material_names : dict, optional
        Mapping of tally names to material names
    
    Returns
    -------
    dict
        Dictionary mapping tally names to {'material': str, 'data': DataFrame}
    """
    if material_names is None:
        material_names = {}
    
    heat_data = {}
    
    for csv_file in sorted(glob.glob(os.path.join(output_dir, pattern))):
        tally_name = os.path.basename(csv_file).replace('_W_per_cm3.csv', '')
        material = material_names.get(tally_name, 'unknown')
        df = pd.read_csv(csv_file)
        heat_data[tally_name] = {'material': material, 'data': df}
        
        print(f"Loaded decay heat {tally_name} ({material}): {len(df)} contributors")
    
    return heat_data


def calculate_total_activity_by_material(activity_data: Dict[str, Dict],
                                         exclude_shutdown: bool = True
                                         ) -> pd.DataFrame:
    """
    Calculate total activity for each material at each cooling time.
    
    Parameters
    ----------
    activity_data : dict
        Activity data from load_activity_data()
    exclude_shutdown : bool
        Whether to exclude "0s" (shutdown) column
    
    Returns
    -------
    pd.DataFrame
        DataFrame with Material, Cooling Time, and Total Activity columns
    """
    total_activity = []
    
    for tally_name, data in activity_data.items():
        df = data['data']
        material = data['material']
        
        mean_cols = [c for c in df.columns if c.startswith('mean_')]
        if exclude_shutdown:
            mean_cols = [c for c in mean_cols if '0s' not in c]
        
        for col in mean_cols:
            time_label = col.replace('mean_', '')
            norm_time = normalize_cooling_time(time_label)
            total = df[col].sum()
            
            total_activity.append({
                'Material': material,
                'Cooling Time': norm_time,
                'Total Activity (Bq/cm³)': total,
                'Original Label': time_label
            })
    
    return pd.DataFrame(total_activity)


def calculate_total_decay_heat_by_material(heat_data: Dict[str, Dict],
                                           exclude_shutdown: bool = True
                                           ) -> pd.DataFrame:
    """
    Calculate total decay heat for each material at each cooling time.
    
    Parameters
    ----------
    heat_data : dict
        Decay heat data from load_decay_heat_data()
    exclude_shutdown : bool
        Whether to exclude "0s" (shutdown) column
    
    Returns
    -------
    pd.DataFrame
        DataFrame with Material, Cooling Time, and Total Decay Heat columns
    """
    total_heat = []
    
    for tally_name, data in heat_data.items():
        df = data['data']
        material = data['material']
        
        mean_cols = [c for c in df.columns if c.startswith('mean_')]
        if exclude_shutdown:
            mean_cols = [c for c in mean_cols if '0s' not in c]
        
        for col in mean_cols:
            time_label = col.replace('mean_', '')
            norm_time = normalize_cooling_time(time_label)
            total = df[col].sum()
            
            total_heat.append({
                'Material': material,
                'Cooling Time': norm_time,
                'Total Decay Heat (W/cm³)': total,
                'Original Label': time_label
            })
    
    return pd.DataFrame(total_heat)


# ==============================================================================
# CONVENIENCE FUNCTIONS FOR COMMON ANALYSES
# ==============================================================================

def analyze_all_mesh_tallies(h5_file: str,
                             tally_nums: List[int],
                             material_names: Dict[str, str],
                             verbose: bool = True) -> Dict[int, Dict]:
    """
    Analyze flux spectra from multiple mesh tallies.
    
    Parameters
    ----------
    h5_file : str
        Path to HDF5 file
    tally_nums : list
        List of tally numbers to analyze
    material_names : dict
        Mapping of tally keys to material names
    verbose : bool
        Whether to print progress
    
    Returns
    -------
    dict
        Dictionary mapping tally numbers to analysis results
    """
    flux_analysis = {}
    
    if verbose:
        print("=" * 80)
        print("ANALYZING FLUX SPECTRA FROM MESH TALLIES")
        print("=" * 80)
        print(f"Analyzing tallies: {tally_nums}\n")
    
    for tally_num in tally_nums:
        try:
            flux_analysis[tally_num] = analyze_flux_spectrum(h5_file, tally_num)
            fa = flux_analysis[tally_num]
            
            if verbose:
                material = material_names.get(f'tally_{tally_num}', 'unknown')
                print(f"✓ Tally {tally_num} ({material}):")
                print(f"    Energy groups: {fa['n_groups']}")
                print(f"    Voxels: {fa['n_voxels']}")
                print(f"    Mean total flux: {fa['mean_spectrum'].sum():.3e} n/cm²/s")
                print(f"    Flux range: {fa['total_flux_per_voxel'].min():.3e} - "
                      f"{fa['total_flux_per_voxel'].max():.3e}\n")
        except Exception as e:
            print(f"✗ Error analyzing tally {tally_num}: {e}")
    
    if verbose:
        print(f"✓ Successfully loaded {len(flux_analysis)} tallies\n")
    
    return flux_analysis


# ==============================================================================
# PARSING HALF-LIFE FROM STRINGS
# ==============================================================================

def parse_half_life_seconds(hl_str: str) -> Optional[float]:
    """
    Parse a half-life string to seconds.
    
    Parameters
    ----------
    hl_str : str
        Half-life string like "2.7d", "114.43d", "5.27y"
    
    Returns
    -------
    float or None
        Half-life in seconds, or None if parsing fails
    """
    if not hl_str or pd.isna(hl_str):
        return None
    
    hl_str = str(hl_str).strip().lower()
    
    # Match patterns like "114.43d", "2.7d", "5.27y"
    match = re.match(r'([+-]?\d+\.?\d*)\s*([smhdwy])', hl_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        
        multipliers = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800,
            'y': 31557600  # 365.25 days
        }
        
        return value * multipliers.get(unit, 1)
    
    return None


# ==============================================================================
# MAIN: EXAMPLE USAGE
# ==============================================================================

if __name__ == '__main__':
    print("Flux Mesh Analysis Utilities")
    print("=" * 50)
    print("\nAvailable functions:")
    print("  - analyze_flux_spectrum(h5_file, tally_num)")
    print("  - compare_materials_flux(flux_analysis, material_names)")
    print("  - plot_flux_spectra(flux_analysis, material_names)")
    print("  - print_flux_summary(flux_analysis, material_names)")
    print("  - load_activity_data(output_dir, pattern, material_names)")
    print("  - get_top_isotopes_from_df(df, n, column)")
    print("  - calculate_total_activity_by_material(activity_data)")
    print("  - analyze_all_mesh_tallies(h5_file, tally_nums, material_names)")
    print("  - normalize_cooling_time(time_label)")
    print("  - extract_time_from_label(label)")
    print("  - parse_half_life_seconds(hl_str)")
    print("\nExample usage:")
    print("""
    from flux_mesh_analysis import analyze_all_mesh_tallies, print_flux_summary
    
    material_names = {
        'tally_85214': 'CNA',
        'tally_85224': 'EUROFER97_C',
        'tally_85234': 'EUROFER97_B',
    }
    
    flux_analysis = analyze_all_mesh_tallies(
        h5_file='runtpe.h5',
        tally_nums=[85214, 85224, 85234],
        material_names=material_names
    )
    
    print_flux_summary(flux_analysis, material_names)
    """)
