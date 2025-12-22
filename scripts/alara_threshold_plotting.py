"""
ALARA Threshold Plotting Module

Plots ALARA-predicted isotopes above a given detection threshold,
with color-coding for measured vs unmeasured isotopes.

Based on code from MCNP_ALARA_Complete_Workflow_old.ipynb Cell 65.

Key Design Principle:
- Uses dynamic column mapping via alara_data_loader (no hardcoded column names)
- Experimental data structure is kept constant - defined once at notebook start
- Shows gamma emitter status for unmeasured isotopes to help explain gaps
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import dynamic column mapping from alara_data_loader
from alara_data_loader import (
    build_cooling_map,
    extract_mean_columns,
    find_closest_column,
    parse_time_to_seconds,
)

# Import gamma emission checking from isotope_utils
from isotope_utils import (
    has_gamma_emission, 
    get_gamma_info,
    GAMMA_ENERGY_MIN_KEV, 
    GAMMA_ENERGY_MAX_KEV,
)

# ============================================================
# Constants
# ============================================================

BQ_TO_UCI = 2.7027e-5  # 1 Bq = 2.7027e-5 µCi

# Color scheme - now with gamma emitter distinction for unmeasured isotopes
COLORS = {
    'Measured': '#2a9d8f',               # Teal - in experimental list
    'Not measured (γ)': '#e76f51',       # Coral - not measured but IS gamma emitter
    'Not measured (no γ)': '#adb5bd',    # Gray - not measured AND not gamma emitter
    'Total': '#264653'                   # Dark blue - total bar
}


# ============================================================
# Helper Functions
# ============================================================

def _get_dynamic_column(alara_df: pd.DataFrame, cooling_time: str) -> Optional[str]:
    """
    Get the ALARA column name for a given cooling time using dynamic matching.
    """
    cooling_map = build_cooling_map(alara_df, [cooling_time])
    return cooling_map.get(cooling_time)


# ============================================================
# Main Plotting Functions
# ============================================================

def plot_alara_predicted_threshold(
    alara_activity_file: Path,
    material: str,
    cooling_time: str,
    experimental_data: Optional[Dict[str, Dict[str, Any]]] = None,
    threshold_uCi: float = 1e-4,
    save_path: Optional[Path] = None,
    show_plot: bool = True,
    figsize: Tuple[int, int] = (12, 7)
) -> Optional[plt.Figure]:
    """
    Plot ALARA-predicted isotopes above threshold with experimental detection floor.
    
    Uses DYNAMIC column mapping - no hardcoded ALARA column names required.
    
    Parameters
    ----------
    alara_activity_file : Path
        Path to ALARA activity CSV file (e.g., tally_85214_Bq_per_cm3.csv)
    material : str
        Material name for title
    cooling_time : str
        Cooling time label (e.g., '300s', '2h', '24h', '4d', '15d')
    experimental_data : dict, optional
        Experimental data dict: {cooling_time: {isotope: {'activity': float, ...}}}
    threshold_uCi : float
        Activity threshold in µCi (default 1e-4)
    save_path : Path, optional
        If provided, save figure to this path
    show_plot : bool
        Whether to display the plot
    figsize : tuple
        Figure size
        
    Returns
    -------
    plt.Figure or None
    """
    # Load ALARA data
    alara_df = pd.read_csv(alara_activity_file)
    
    # Use dynamic column mapping
    alara_col = _get_dynamic_column(alara_df, cooling_time)
    if not alara_col:
        print(f"No matching ALARA column for cooling time: {cooling_time}")
        return None
    
    if alara_col not in alara_df.columns:
        print(f"Column {alara_col} not found in {alara_activity_file}")
        return None
    
    # Prepare data
    ct_df = alara_df[['isotope', alara_col]].copy()
    # Drop any existing total rows from ALARA output to avoid duplicate total bars
    ct_df = ct_df[ct_df['isotope'].str.lower() != 'total']
    ct_df['ALARA_uCi'] = ct_df[alara_col] * BQ_TO_UCI
    ct_df = ct_df[ct_df['ALARA_uCi'] > threshold_uCi]
    
    if ct_df.empty:
        print(f"No ALARA isotopes > threshold for {material} at {cooling_time}")
        return None
    
    # Get experimental isotope set and detection floor
    exp_nuclides = experimental_data.get(cooling_time, {}) if experimental_data else {}
    exp_iso_set = {iso.lower() for iso in exp_nuclides.keys()}
    detection_floor = None
    if exp_nuclides:
        detection_values = [v['activity'] for v in exp_nuclides.values() if v.get('activity', 0) > 0]
        if detection_values:
            detection_floor = min(detection_values)
    
    # Mark isotopes with status and gamma emission info
    def classify_isotope(iso):
        """
        Classify isotope into one of:
        - 'Measured': Present in experimental data
        - 'Not measured (γ)': Not measured but IS a gamma emitter in HPGe range
        - 'Not measured (no γ)': Not measured AND not a detectable gamma emitter
        """
        iso_clean = iso.lower().replace('_', '').replace('-', '')
        exp_clean = {s.replace('_', '').replace('-', '') for s in exp_iso_set}
        
        if iso_clean in exp_clean:
            return 'Measured'
        
        # Check if this is a gamma emitter in the HPGe detectable range
        if has_gamma_emission(iso, min_intensity=0.01, 
                              energy_min_keV=GAMMA_ENERGY_MIN_KEV, 
                              energy_max_keV=GAMMA_ENERGY_MAX_KEV):
            return 'Not measured (γ)'
        else:
            return 'Not measured (no γ)'
    
    ct_df['status'] = ct_df['isotope'].apply(classify_isotope)
    ct_df = ct_df.sort_values('ALARA_uCi', ascending=False)
    
    # Insert total as leftmost bar
    total_row = pd.DataFrame({
        'isotope': ['TOTAL'],
        'ALARA_uCi': [ct_df['ALARA_uCi'].sum()],
        'status': ['Total']
    })
    ct_df = pd.concat([total_row, ct_df], ignore_index=True)
    colors = ct_df['status'].map(COLORS).fillna('#264653')
    
    # Create figure - adjust size based on number of isotopes
    n_isotopes = len(ct_df)
    
    # Dynamically adjust figure width for many isotopes
    if n_isotopes > 30:
        fig_width = max(figsize[0], n_isotopes * 0.35)
    else:
        fig_width = figsize[0]
    
    fig, ax = plt.subplots(figsize=(fig_width, figsize[1]))
    x = np.arange(len(ct_df))
    ax.bar(x, ct_df['ALARA_uCi'], color=colors, edgecolor='black', linewidth=0.5)
    
    # Adaptive label handling for crowded x-axis
    if n_isotopes > 50:
        # For very many isotopes: smaller font, vertical labels
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=90, ha='center', fontsize=6)
    elif n_isotopes > 30:
        # For many isotopes: smaller font, steep angle
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=75, ha='right', fontsize=7)
    elif n_isotopes > 15:
        # Moderate number: 60 degree angle
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=60, ha='right', fontsize=8)
    else:
        # Few isotopes: standard 45 degree
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=45, ha='right', fontsize=10)
    
    ax.set_yscale('log')
    ax.set_title(f'ALARA predicted isotopes > {threshold_uCi} µCi — {material} — {cooling_time}', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel('ALARA Activity (µCi)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Isotope', fontsize=12, fontweight='bold')
    ax.grid(True, which='both', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    if detection_floor is not None and detection_floor > 0:
        ax.axhline(detection_floor, color='red', linestyle='--', linewidth=1.2, label='Lowest experimental activity')
    
    # Count isotopes by status for legend annotation
    n_measured = (ct_df['status'] == 'Measured').sum()
    n_gamma = (ct_df['status'] == 'Not measured (γ)').sum()
    n_no_gamma = (ct_df['status'] == 'Not measured (no γ)').sum()
    
    # Create legend with counts and gamma range info
    legend_handles = [
        mpatches.Patch(color=COLORS['Total'], label='Total (ALARA)'),
        mpatches.Patch(color=COLORS['Measured'], label=f'Measured experimentally ({n_measured})'),
        mpatches.Patch(color=COLORS['Not measured (γ)'], 
                       label=f'Not measured, γ emitter ({n_gamma})'),
        mpatches.Patch(color=COLORS['Not measured (no γ)'], 
                       label=f'Not measured, no γ ({n_no_gamma})'),
        mlines.Line2D([0], [0], color='red', linestyle='--', 
                      label='Lowest experimental activity')
    ]
    ax.legend(handles=legend_handles, fontsize=9, loc='upper right',
              title=f'γ range: {int(GAMMA_ENERGY_MIN_KEV)}-{int(GAMMA_ENERGY_MAX_KEV)} keV')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


def plot_all_materials_threshold(
    alara_output_dir: Path,
    experimental_data: Dict[str, Dict[str, Dict[str, Any]]],
    material_to_tally: Optional[Dict[str, str]] = None,
    threshold_uCi: float = 1e-4,
    cooling_times: Optional[List[str]] = None,
    save_dir: Optional[Path] = None,
    show_plots: bool = False,
    show_materials: Optional[List[str]] = None
) -> Dict[str, Dict[str, plt.Figure]]:
    """
    Plot threshold plots for all materials and cooling times.
    
    Parameters
    ----------
    alara_output_dir : Path
        Directory containing ALARA output CSV files
    experimental_data : dict
        Nested dict: {material: {cooling_time: {isotope: {'activity': float, ...}}}}
    material_to_tally : dict, optional
        Mapping from material name to tally folder
    threshold_uCi : float
        Activity threshold in µCi
    cooling_times : list, optional
        List of cooling times to plot (default: all)
    save_dir : Path, optional
        Directory to save plots
    show_plots : bool
        Whether to show all plots (default: False, only saves)
    show_materials : list, optional
        Materials to show plots for (others just save)
        
    Returns
    -------
    dict
        Nested dict of figures: {material: {cooling_time: figure}}
    """
    if material_to_tally is None:
        # Import here to avoid circular dependency
        try:
            from experimental_data_loader import MATERIAL_TO_TALLY
            material_to_tally = MATERIAL_TO_TALLY
        except ImportError:
            raise ValueError("material_to_tally must be provided when experimental_data_loader is not available")
    if cooling_times is None:
        cooling_times = ['300s', '2h', '24h', '4d', '15d']
    if show_materials is None:
        show_materials = []
    
    alara_output_dir = Path(alara_output_dir)
    figures = {}
    
    for material, tally_folder in material_to_tally.items():
        alara_activity_file = alara_output_dir / f"{tally_folder}_Bq_per_cm3.csv"
        if not alara_activity_file.exists():
            print(f"⚠ Missing ALARA activity file for {material}: {alara_activity_file}")
            continue
        
        safe_mat = str(material).replace(' ', '_')
        figures[material] = {}
        any_plotted = False
        
        # Get experimental data for this material
        mat_exp_data = experimental_data.get(material, {})
        
        for ct in cooling_times:
            save_path = None
            if save_dir:
                save_path = Path(save_dir) / f"alara_predicted_threshold_{safe_mat}_{ct}.png"
            
            should_show = show_plots or (material in show_materials)
            
            fig = plot_alara_predicted_threshold(
                alara_activity_file=alara_activity_file,
                material=material,
                cooling_time=ct,
                experimental_data=mat_exp_data,
                threshold_uCi=threshold_uCi,
                save_path=save_path,
                show_plot=should_show
            )
            
            if fig is not None:
                figures[material][ct] = fig
                any_plotted = True
        
        if not any_plotted:
            print(f"No ALARA isotopes above threshold for {material}.")
    
    return figures


# ============================================================
# Summary Functions
# ============================================================

def get_alara_isotopes_above_threshold(
    alara_activity_file: Path,
    cooling_time: str,
    threshold_uCi: float = 1e-4
) -> pd.DataFrame:
    """
    Get ALARA isotopes above threshold for a given cooling time.
    
    Uses DYNAMIC column mapping - no hardcoded ALARA column names required.
    
    Parameters
    ----------
    alara_activity_file : Path
        Path to ALARA activity CSV file
    cooling_time : str
        Cooling time label
    threshold_uCi : float
        Activity threshold in µCi
        
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: isotope, activity_Bq_cm3, activity_uCi
    """
    alara_df = pd.read_csv(alara_activity_file)
    
    # Use dynamic column mapping
    alara_col = _get_dynamic_column(alara_df, cooling_time)
    if not alara_col:
        return pd.DataFrame()
    
    if alara_col not in alara_df.columns:
        return pd.DataFrame()
    
    result = alara_df[['isotope', alara_col]].copy()
    result = result[result['isotope'].str.lower() != 'total']
    result['activity_uCi'] = result[alara_col] * BQ_TO_UCI
    result = result[result['activity_uCi'] > threshold_uCi]
    result = result.rename(columns={alara_col: 'activity_Bq_cm3'})
    result = result.sort_values('activity_uCi', ascending=False)
    
    return result
    
    return result


def count_alara_isotopes_by_material(
    alara_output_dir: Path,
    material_to_tally: Optional[Dict[str, str]] = None,
    threshold_uCi: float = 1e-4,
    cooling_times: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Count ALARA isotopes above threshold for all materials and cooling times.
    
    Parameters
    ----------
    alara_output_dir : Path
        Directory containing ALARA output CSV files
    material_to_tally : dict
        Mapping from material name to tally folder name
    threshold_uCi : float
        Activity threshold in µCi
    cooling_times : list, optional
        List of cooling times to check. If None, uses experimental standard times.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: material, cooling_time, isotope_count, total_activity_uCi
    """
    if cooling_times is None:
        cooling_times = ['300s', '2h', '24h', '4d', '15d']
    
    alara_output_dir = Path(alara_output_dir)
    results = []
    
    for material, tally_folder in material_to_tally.items():
        alara_activity_file = alara_output_dir / f"{tally_folder}_Bq_per_cm3.csv"
        if not alara_activity_file.exists():
            continue
        
        for ct in cooling_times:
            df = get_alara_isotopes_above_threshold(
                alara_activity_file, ct, threshold_uCi
            )
            results.append({
                'material': material,
                'cooling_time': ct,
                'isotope_count': len(df),
                'total_activity_uCi': df['activity_uCi'].sum() if not df.empty else 0
            })
    
    return pd.DataFrame(results)


if __name__ == '__main__':
    print("ALARA Threshold Plotting Module")
    print("=" * 50)
    print("This module provides functions for plotting ALARA-predicted")
    print("isotopes above a detection threshold.")
    print()
    print("Main functions:")
    print("  - plot_alara_predicted_threshold(): Plot single material/cooling time")
    print("  - plot_all_materials_threshold(): Plot all materials and cooling times")
    print("  - get_alara_isotopes_above_threshold(): Get isotopes above threshold")
    print("  - count_alara_isotopes_by_material(): Summary counts")
