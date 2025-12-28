"""
Consolidated Plotting Module for MCNP-ALARA Workflow.

This module centralizes ALL plotting functions and style definitions for the
neutron activation analysis workflow. Import plotting functions from here,
not from individual analysis scripts.

Design Philosophy:
- Single source of truth for colors, labels, and styles
- Analysis scripts (alara_comparison.py, decay_physics.py, etc.) handle data processing
- This module handles ALL visualization

Usage:
    from plotting import (
        # Style constants
        MATERIAL_COLORS, COOLING_COLORS, SOURCE_COLORS,
        apply_standard_style,
        
        # Comparison plots
        plot_comparison_scatter, plot_comparison_by_material,
        
        # SNR/Detection plots
        plot_snr_heatmap, plot_snr_lines, plot_threshold_comparison,
        
        # Decay/Activity plots
        plot_irradiation_decay_curves, plot_experimental_activity_pies,
        
        # Flux plots
        plot_flux_wire_measurements, plot_flux_vs_spectrum, plot_flux_energy_ranges,
    )

Author: MCNP-ALARA Workflow Team
Created: December 2024
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.colors import LogNorm
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

from alara_data_loader import build_cooling_map
from data_loaders import compute_flux_from_measurements, load_mcnp_spectrum

# ==============================================================================
# STYLE CONSTANTS - Single Source of Truth
# ==============================================================================

# Material colors - distinct for each material
MATERIAL_COLORS = {
    'CNA': '#1f77b4',           # Blue
    'EUROFER97_2': '#ff7f0e',   # Orange  
    'EUROFER97_3': '#2ca02c',   # Green
    'EUROFER97_4': '#d62728',   # Red
    'EUROFER97': '#9467bd',     # Purple (generic)
}

# Source type colors - Experimental vs ALARA
SOURCE_COLORS = {
    'experimental': '#2a9d8f',  # Teal
    'alara': '#e76f51',         # Coral
    'total': '#264653',         # Dark slate
}

# Cooling time colors - distinct per cooling time for bar charts
COOLING_COLORS = {
    '300s': '#440154',   # Dark purple
    '2h': '#31688e',     # Blue
    '24h': '#35b779',    # Green  
    '4d': '#fde725',     # Yellow
    '15d': '#f89540',    # Orange
}

# Irradiation type colors
IRRADIATION_COLORS = {
    '3s_rabbit': '#28a745',   # Green - 3s rabbit irradiation
    '2hr_long': '#dc3545',    # Red - 2hr irradiation
}

# Marker styles by cooling time
MARKERS = {
    '300s': 'o',
    '2h': 's', 
    '24h': '^',
    '4d': 'D',
    '15d': 'v',
}

# Status colors for threshold plots
STATUS_COLORS = {
    'Total': '#264653',             # Dark slate
    'Measured': '#2a9d8f',          # Teal - experimentally measured
    'Not measured (γ)': '#e76f51',  # Coral - has gamma, not detected  
    'Not measured (no γ)': '#bfbfbf',  # Gray - no detectable gamma
    'Not measured': '#e76f51',      # Coral - legacy
}

# Standard labels - ALWAYS use these (never "Exp")
LABELS = {
    'experimental': 'Experimental',
    'alara': 'ALARA',
    'detection_floor': 'Experimental Detection Floor',
}

# Unit conversions
BQ_TO_UCI = 2.7027e-5  # Bq to µCi

# HPGe detector energy range (keV) for gamma detection
GAMMA_ENERGY_MIN_KEV = 50.0
GAMMA_ENERGY_MAX_KEV = 3000.0


# ==============================================================================
# STYLE APPLICATION
# ==============================================================================

def apply_standard_style():
    """
    Apply standard matplotlib style settings for consistency across all plots.
    Call this at the start of analysis notebooks.
    """
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'legend.fontsize': 9,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.dpi': 150,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.axisbelow': True,
    })


def get_material_color(material: str) -> str:
    """Get color for a material, with fallback to gray."""
    return MATERIAL_COLORS.get(material, '#7f7f7f')


def get_cooling_color(cooling_time: str) -> str:
    """Get color for a cooling time, with fallback to gray."""
    return COOLING_COLORS.get(cooling_time, '#7f7f7f')


# ==============================================================================
# HELPER FUNCTIONS (imported from other modules)
# ==============================================================================

def _safe_import_decay_physics():
    """Safely import decay_physics module."""
    try:
        from decay_physics import (
            LN2, get_half_life_seconds, format_iso_pretty, canonical_iso,
            calculate_snr_grid, multi_irradiation_activity
        )
        return {
            'LN2': LN2,
            'get_half_life_seconds': get_half_life_seconds,
            'format_iso_pretty': format_iso_pretty,
            'canonical_iso': canonical_iso,
            'calculate_snr_grid': calculate_snr_grid,
            'multi_irradiation_activity': multi_irradiation_activity,
        }
    except ImportError:
        return None


def _safe_import_nuclear_data():
    """Safely import nuclear_data module."""
    try:
        from nuclear_data import (
            canonical_iso, format_iso_pretty, has_gamma_emission, LN2, AVOGADRO,
            GAMMA_ENERGY_MIN_KEV, GAMMA_ENERGY_MAX_KEV
        )
        return {
            'canonical_iso': canonical_iso,
            'format_iso_pretty': format_iso_pretty,
            'has_gamma_emission': has_gamma_emission,
            'LN2': LN2,
            'AVOGADRO': AVOGADRO,
            'GAMMA_ENERGY_MIN_KEV': GAMMA_ENERGY_MIN_KEV,
            'GAMMA_ENERGY_MAX_KEV': GAMMA_ENERGY_MAX_KEV,
        }
    except ImportError:
        return None


# ==============================================================================
# COMPARISON PLOTS
# ==============================================================================

def plot_comparison_scatter(
    matched_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    figsize: Tuple[int, int] = (15, 10),
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Create 2x2 comparison plots for matched ALARA vs Experimental isotopes.
    
    Plots:
    1. Scatter of activities by cooling time (log-log)
    2. Total activity by cooling time and material (bar chart)
    3. Mass concentration scatter (where available)
    4. Matched isotope counts by cooling time
    
    Parameters
    ----------
    matched_df : pd.DataFrame
        DataFrame containing only matched isotopes with columns:
        'Material', 'Cooling Time', 'Isotope', 'Exp Activity (uCi)', 
        'ALARA Activity (uCi/cm³)', optionally 'Exp Mass', 'ALARA Mass'
    save_path : Path, optional
        If provided, save figure to this path
    figsize : tuple
        Figure size
    show : bool
        Whether to display the plot
        
    Returns
    -------
    plt.Figure or None
    """
    if matched_df.empty:
        print("No matched isotopes to plot!")
        return None
    
    cooling_order = ['300s', '2h', '24h', '4d', '15d']
    materials = sorted(matched_df['Material'].dropna().unique())
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Plot 1: Scatter of activities by cooling time (log-log)
    ax1 = axes[0, 0]
    for ct in cooling_order:
        ct_data = matched_df[matched_df['Cooling Time'] == ct]
        if ct_data.empty:
            continue
        ax1.scatter(
            ct_data['Exp Activity (uCi)'], 
            ct_data['ALARA Activity (uCi/cm³)'],
            label=f'{ct} (n={len(ct_data)})', 
            alpha=0.7,
            marker=MARKERS.get(ct, 'o'),
            color=COOLING_COLORS.get(ct, '#7f7f7f')
        )
    
    # Add 1:1 line
    all_exp = matched_df['Exp Activity (uCi)'].dropna()
    all_alara = matched_df['ALARA Activity (uCi/cm³)'].dropna()
    if not all_exp.empty and not all_alara.empty:
        min_val = min(all_exp.min(), all_alara.min())
        max_val = max(all_exp.max(), all_alara.max())
        ax1.loglog([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label='1:1 line')
    
    ax1.set_xlabel(f'{LABELS["experimental"]} Activity (µCi)')
    ax1.set_ylabel(f'{LABELS["alara"]} Activity (µCi/cm³)')
    ax1.set_title(f'{LABELS["alara"]} vs {LABELS["experimental"]} Activity')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Plot 2: Total activity by cooling time and material
    ax2 = axes[0, 1]
    agg_act = matched_df.groupby(['Material', 'Cooling Time']).agg(
        Exp_Total=('Exp Activity (uCi)', 'sum'),
        ALARA_Total=('ALARA Activity (uCi/cm³)', 'sum')
    ).reset_index()
    
    x = np.arange(len(cooling_order))
    n_mats = max(len(materials), 1)
    barw = 0.8 / n_mats
    
    for i, mat in enumerate(materials):
        mat_data = agg_act[agg_act['Material'] == mat].set_index('Cooling Time').reindex(cooling_order).fillna(0)
        mat_color = get_material_color(mat)
        offset = (i - n_mats/2 + 0.5) * barw
        
        # Experimental: solid
        ax2.bar(x + offset - barw*0.2, mat_data['Exp_Total'], width=barw*0.4, 
                label=f'{mat} {LABELS["experimental"]}', color=mat_color, edgecolor='black')
        # ALARA: hatched
        ax2.bar(x + offset + barw*0.2, mat_data['ALARA_Total'], width=barw*0.4, 
                label=f'{mat} {LABELS["alara"]}', color=mat_color, alpha=0.5, 
                edgecolor='black', hatch='///')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(cooling_order)
    ax2.set_yscale('log')
    ax2.set_ylabel('Total Activity (log scale)')
    ax2.set_title('Total Activity by Cooling Time and Material')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=7, ncol=2)
    
    # Plot 3: Mass concentration scatter (where available)
    ax3 = axes[1, 0]
    if 'Exp Mass (g/cm³)' in matched_df.columns and 'ALARA Mass (g/cm³)' in matched_df.columns:
        mass_data = matched_df.dropna(subset=['Exp Mass (g/cm³)', 'ALARA Mass (g/cm³)'])
        if not mass_data.empty:
            for mat in materials:
                mat_mass = mass_data[mass_data['Material'] == mat]
                if mat_mass.empty:
                    continue
                ax3.scatter(mat_mass['Exp Mass (g/cm³)'], mat_mass['ALARA Mass (g/cm³)'],
                            label=mat, alpha=0.7, color=get_material_color(mat))
            min_m = mass_data[['Exp Mass (g/cm³)', 'ALARA Mass (g/cm³)']].min().min()
            max_m = mass_data[['Exp Mass (g/cm³)', 'ALARA Mass (g/cm³)']].max().max()
            ax3.loglog([min_m, max_m], [min_m, max_m], 'k--', alpha=0.5, label='1:1 line')
            ax3.set_xlabel(f'{LABELS["experimental"]} Mass (g/cm³)')
            ax3.set_ylabel(f'{LABELS["alara"]} Mass (g/cm³)')
            ax3.set_title('Mass Concentration Comparison')
            ax3.legend(fontsize=8)
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'No mass data available', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_xticks([])
            ax3.set_yticks([])
    else:
        ax3.text(0.5, 0.5, 'No mass data available', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_xticks([])
        ax3.set_yticks([])
    
    # Plot 4: Counts of matched isotopes per cooling time and material
    ax4 = axes[1, 1]
    count_data = matched_df.groupby(['Material', 'Cooling Time']).size().unstack(fill_value=0)
    count_data = count_data.reindex(columns=cooling_order, fill_value=0)
    
    # Use material colors
    bar_colors = [get_material_color(m) for m in count_data.index]
    count_data.T.plot(kind='bar', ax=ax4, color=bar_colors)
    ax4.set_ylabel('Matched Isotope Count')
    ax4.set_title('Matched Isotopes by Cooling Time')
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=8)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


def plot_comparison_by_material(
    matched_df: pd.DataFrame,
    save_dir: Optional[Path] = None,
    figsize: Tuple[int, int] = (14, 8),
    show: bool = True
) -> Dict[str, plt.Figure]:
    """
    Create detailed bar charts comparing Experimental vs ALARA for each material.
    
    Uses distinct colors per cooling time with solid bars for Experimental
    and hatched bars for ALARA.
    
    Parameters
    ----------
    matched_df : pd.DataFrame
        DataFrame containing matched isotopes
    save_dir : Path, optional
        If provided, save figures to this directory
    figsize : tuple
        Figure size for each plot
    show : bool
        Whether to display plots
        
    Returns
    -------
    dict
        Dictionary of figures keyed by material name
    """
    if matched_df.empty:
        print("No matched isotopes to plot!")
        return {}
    
    cooling_order = ['300s', '2h', '24h', '4d', '15d']
    materials = sorted(matched_df['Material'].dropna().unique())
    figures = {}
    
    for material in materials:
        mat_df = matched_df[matched_df['Material'] == material]
        if mat_df.empty:
            continue
        
        # Create pivot table for activities
        pivot_exp = mat_df.pivot_table(
            index='Isotope', 
            columns='Cooling Time', 
            values='Exp Activity (uCi)',
            aggfunc='first'
        ).reindex(columns=[c for c in cooling_order if c in mat_df['Cooling Time'].unique()])
        
        pivot_alara = mat_df.pivot_table(
            index='Isotope', 
            columns='Cooling Time', 
            values='ALARA Activity (uCi/cm³)',
            aggfunc='first'
        ).reindex(columns=[c for c in cooling_order if c in mat_df['Cooling Time'].unique()])
        
        if pivot_exp.empty:
            continue
        
        # Create figure with grouped bar chart
        fig, ax = plt.subplots(figsize=figsize)
        
        isotopes = pivot_exp.index.tolist()
        cooling_times = pivot_exp.columns.tolist()
        n_isotopes = len(isotopes)
        n_times = len(cooling_times)
        
        # Create grouped bars - Experimental solid, ALARA hatched
        x = np.arange(n_isotopes)
        total_width = 0.8
        bar_width = total_width / (n_times * 2)
        
        for i, ct in enumerate(cooling_times):
            offset = (i - n_times/2 + 0.5) * bar_width * 2
            base_color = COOLING_COLORS.get(ct, '#7f7f7f')
            
            exp_vals = pivot_exp[ct].fillna(0).values
            alara_vals = pivot_alara[ct].fillna(0).values if ct in pivot_alara.columns else np.zeros(n_isotopes)
            
            # Experimental: solid fill
            ax.bar(x + offset - bar_width/2, exp_vals, width=bar_width, 
                   label=f'{ct} {LABELS["experimental"]}', color=base_color, 
                   edgecolor='black', linewidth=0.8)
            # ALARA: hatched fill with lighter color
            ax.bar(x + offset + bar_width/2, alara_vals, width=bar_width, 
                   label=f'{ct} {LABELS["alara"]}', color=base_color, alpha=0.5,
                   edgecolor='black', linewidth=0.8, hatch='///')
        
        ax.set_xticks(x)
        ax.set_xticklabels(isotopes, rotation=45, ha='right', fontsize=11)
        ax.set_yscale('log')
        ax.set_ylabel('Activity (µCi)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Isotope', fontsize=12, fontweight='bold')
        ax.set_title(f'{LABELS["experimental"]} vs {LABELS["alara"]} Activity - {material}', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9, ncol=2, 
                  title='Cooling Time', title_fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_dir:
            save_path = Path(save_dir) / f"comparison_{material.replace(' ', '_')}.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Figure saved to: {save_path}")
        
        figures[material] = fig
        
        if show:
            plt.show()
        else:
            plt.close(fig)
    
    return figures


# ==============================================================================
# SNR / DETECTION HEATMAPS
# ==============================================================================

def plot_snr_heatmap(
    ti_range: np.ndarray,
    td_range: np.ndarray,
    snr_grid: np.ndarray,
    target_name: str = "Target",
    mask_name: str = "Mask",
    ti_unit: str = "hours",
    td_unit: str = "days",
    save_path: Optional[str] = None,
    show: bool = True,
    title_suffix: str = ""
) -> Optional[plt.Figure]:
    """
    Plot 2D heatmap of SNR as a function of irradiation and cooling time.
    
    Parameters
    ----------
    ti_range : np.ndarray
        Irradiation time array (seconds)
    td_range : np.ndarray
        Cooling time array (seconds)
    snr_grid : np.ndarray
        2D SNR values [td_index, ti_index]
    target_name : str
        Name of target isotope for labels
    mask_name : str
        Name of masking isotope for labels
    ti_unit : str
        Display unit for irradiation time ('hours' or 'seconds')
    td_unit : str
        Display unit for cooling time ('days' or 'seconds')
    save_path : str, optional
        If provided, save figure to this path
    show : bool
        Whether to display the plot
    title_suffix : str
        Additional text for title (e.g., cooling time)
    
    Returns
    -------
    plt.Figure or None
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Convert units for display
    ti_display = ti_range / 3600 if ti_unit == "hours" else ti_range
    td_display = td_range / 86400 if td_unit == "days" else td_range
    
    # Check for valid data
    valid_snr = snr_grid[np.isfinite(snr_grid) & (snr_grid > 0)]
    if len(valid_snr) == 0:
        print(f"Warning: No valid SNR values for {target_name} vs {mask_name}")
        plt.close(fig)
        return None
    
    vmin, vmax = np.nanmin(valid_snr), np.nanmax(valid_snr)
    if vmax / max(vmin, 1e-30) > 100:
        norm = LogNorm(vmin=max(vmin, 1e-10), vmax=vmax)
    else:
        norm = None
    
    im = ax.pcolormesh(ti_display, td_display, snr_grid, shading='auto',
                       cmap='viridis', norm=norm)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(f'SNR ({target_name} / {mask_name})', fontsize=11)
    
    # Find and mark optimal point
    max_idx = np.unravel_index(np.nanargmax(snr_grid), snr_grid.shape)
    opt_td = td_display[max_idx[0]]
    opt_ti = ti_display[max_idx[1]]
    opt_snr = snr_grid[max_idx]
    
    ax.scatter([opt_ti], [opt_td], color='red', s=200, marker='*',
               edgecolor='white', linewidth=2, zorder=5,
               label=f'Optimal: ti={opt_ti:.1f}{ti_unit[0]}, td={opt_td:.1f}{td_unit[0]}\nSNR={opt_snr:.2e}')
    
    # SNR = 10 contour
    try:
        cs = ax.contour(ti_display, td_display, snr_grid, levels=[10], 
                       colors='red', linewidths=2, linestyles='--')
        ax.clabel(cs, fmt='SNR=10', fontsize=9)
    except:
        pass
    
    ax.set_xlabel(f'Irradiation Time ({ti_unit})', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'Cooling Time ({td_unit})', fontsize=12, fontweight='bold')
    
    title = f'Detection Window: {target_name} vs {mask_name}'
    if title_suffix:
        title = f'{title}\n{title_suffix}'
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


def plot_snr_lines(
    isotope_data: List[Dict],
    mask_iso: str,
    mask_hl_s: float,
    irradiation_time_h: float = 2.0,
    td_max_days: float = 30.0,
    output_dir: Optional[str] = None,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Plot SNR as line plots showing SNR vs cooling time for each target isotope.
    
    Parameters
    ----------
    isotope_data : list
        List of dicts with 'isotope', 'activity', 'half_life_s' keys
    mask_iso : str
        Name of dominant/masking isotope
    mask_hl_s : float
        Half-life of mask isotope (seconds)
    irradiation_time_h : float
        Fixed irradiation time (hours)
    td_max_days : float
        Maximum cooling time to plot (days)
    output_dir : str, optional
        Directory for saving plots
    show : bool
        Whether to display the plot
    
    Returns
    -------
    plt.Figure or None
    """
    utils = _safe_import_nuclear_data()
    decay = _safe_import_decay_physics()
    
    if not utils or not decay:
        print("Required modules (nuclear_data, decay_physics) not available")
        return None
    
    format_iso_pretty = utils['format_iso_pretty']
    canonical_iso = utils['canonical_iso']
    LN2 = utils['LN2']
    get_half_life_seconds = decay['get_half_life_seconds']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ti_s = irradiation_time_h * 3600
    td_range = np.logspace(-2, np.log10(td_max_days), 200)  # Days
    td_range_s = td_range * 86400  # Convert to seconds
    
    mask_pretty = format_iso_pretty(mask_iso)
    lam_mask = LN2 / mask_hl_s
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(isotope_data)))
    
    # Get mask activity
    mask_act = 1.0
    for d in isotope_data:
        if canonical_iso(d['isotope']) == canonical_iso(mask_iso):
            mask_act = d.get('activity', 1.0)
            break
    
    # Calculate mask activity over time
    S_mask = 1 - np.exp(-lam_mask * ti_s)
    A_mask_t = mask_act * S_mask * np.exp(-lam_mask * td_range_s)
    
    for i, data in enumerate(isotope_data):
        iso = data['isotope']
        if canonical_iso(iso) == canonical_iso(mask_iso):
            continue
        
        target_act = data.get('activity', 1.0)
        target_hl_s = data.get('half_life_s', get_half_life_seconds(iso))
        
        if target_hl_s is None or target_hl_s <= 0:
            continue
        
        lam_target = LN2 / target_hl_s
        S_target = 1 - np.exp(-lam_target * ti_s)
        A_target_t = target_act * S_target * np.exp(-lam_target * td_range_s)
        snr = A_target_t / np.maximum(A_mask_t, 1e-30)
        
        target_pretty = format_iso_pretty(iso)
        hl_days = target_hl_s / 86400
        hl_label = f"{hl_days:.1f}d" if hl_days >= 1 else f"{hl_days*24:.1f}h"
        
        ax1.loglog(td_range, snr, linewidth=2, color=colors[i],
                  label=f"{target_pretty} (T½={hl_label})")
        ax2.semilogy(td_range, A_target_t, '--', linewidth=1.5, color=colors[i],
                    label=f"{target_pretty}")
    
    # Plot mask activity
    ax2.semilogy(td_range, A_mask_t, 'k-', linewidth=2.5, label=f"{mask_pretty} (mask)")
    
    # Left plot: SNR
    ax1.axhline(y=1, color='red', linestyle=':', linewidth=1.5, alpha=0.7, label='SNR = 1')
    ax1.set_xlabel('Cooling Time (days)', fontsize=11)
    ax1.set_ylabel(f'SNR (Target / {mask_pretty})', fontsize=11)
    ax1.set_title(f'SNR vs Cooling Time\n(ti = {irradiation_time_h:.1f} hours)', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3, which='both')
    
    # Right plot: Activities
    ax2.set_xlabel('Cooling Time (days)', fontsize=11)
    ax2.set_ylabel('Activity (relative)', fontsize=11)
    ax2.set_title('Activity Decay Curves', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    if output_dir:
        save_path = Path(output_dir) / f"snr_lines_{mask_iso.replace('-','')}.png"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


# ==============================================================================
# THRESHOLD COMPARISON PLOTS
# ==============================================================================

def plot_threshold_comparison(
    alara_df: pd.DataFrame,
    material_name: str,
    experimental_data: Dict[str, Dict],
    threshold_uCi: float = 1e-4,
    cooling_map: Optional[Dict[str, str]] = None,
    save_dir: Optional[Path] = None,
    show: bool = True,
    title_suffix: str = ""
) -> Optional[plt.Figure]:
    """
    Plot ALARA predicted isotopes above threshold vs Experimental Detection Floor.
    
    Multi-panel figure showing each cooling time that exists in the data.
    
    Parameters
    ----------
    alara_df : pd.DataFrame
        ALARA DataFrame with 'isotope' column and activity columns
    material_name : str
        Material name for title
    experimental_data : dict
        {cooling_time: {isotope: {'activity': float, ...}}}
    threshold_uCi : float
        Activity threshold in µCi
    cooling_map : dict, optional
        Mapping from cooling time labels to ALARA column names
    save_dir : Path, optional
        Directory to save figure
    show : bool
        Whether to display
    title_suffix : str
        Additional title text
    
    Returns
    -------
    plt.Figure or None
    """
    utils = _safe_import_nuclear_data()
    if not utils:
        print("nuclear_data not available")
        return None
    
    canonical_iso = utils['canonical_iso']
    
    cooling_order = ["300s", "2h", "24h", "4d", "15d"]
    
    # Build default cooling map if not provided
    if cooling_map is None:
        cooling_map = build_cooling_map(alara_df, cooling_order)
    
    valid_cols = [c for c in cooling_order if cooling_map.get(c) in alara_df.columns]
    if not valid_cols:
        print(f"No valid cooling columns found for {material_name}")
        return None
    
    fig, axes = plt.subplots(1, len(valid_cols), figsize=(4 * len(valid_cols), 6), squeeze=False)
    axes = axes.flatten()
    
    for idx, ct in enumerate(valid_cols):
        ax = axes[idx]
        col = cooling_map[ct]
        
        ct_df = alara_df[["isotope", col]].copy()
        ct_df = ct_df[ct_df["isotope"].str.lower() != "total"]
        ct_df["ALARA_uCi"] = ct_df[col] * BQ_TO_UCI
        ct_df = ct_df[ct_df["ALARA_uCi"] > threshold_uCi]
        
        exp_nuclides = experimental_data.get(ct, {})
        exp_iso_set = {canonical_iso(k) for k in exp_nuclides.keys()}
        
        detection_floor = None
        if exp_nuclides:
            vals = [v["activity"] for v in exp_nuclides.values() if v.get("activity", 0) > 0]
            if vals:
                detection_floor = min(vals)
        
        if ct_df.empty:
            ax.text(0.5, 0.5, "No ALARA > threshold", ha="center", va="center")
            ax.axis("off")
            continue
        
        ct_df["status"] = ct_df["isotope"].apply(
            lambda x: "Measured" if canonical_iso(x) in exp_iso_set else "Not measured"
        )
        ct_df = ct_df.sort_values("ALARA_uCi", ascending=False)
        
        # Insert TOTAL bar at the beginning
        total_row = pd.DataFrame({
            "isotope": ["TOTAL"], 
            "ALARA_uCi": [ct_df["ALARA_uCi"].sum()], 
            "status": ["Total"]
        })
        ct_df = pd.concat([total_row, ct_df], ignore_index=True)
        
        colors = ct_df["status"].map(STATUS_COLORS).fillna('#264653')
        
        x = np.arange(len(ct_df))
        ax.bar(x, ct_df["ALARA_uCi"], color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df["isotope"], rotation=45, ha="right", fontsize=9)
        ax.set_yscale("log")
        ax.set_title(f"{ct}")
        ax.set_ylabel("Activity (µCi)")
        ax.grid(True, alpha=0.3, axis='y')
        
        if detection_floor:
            ax.axhline(detection_floor, color="red", linestyle="--", linewidth=1.5)
    
    # Legend
    handles = [
        mpatches.Patch(color=STATUS_COLORS['Total'], label='Total (ALARA)'),
        mpatches.Patch(color=STATUS_COLORS['Measured'], label='Measured Experimentally'),
        mpatches.Patch(color=STATUS_COLORS['Not measured'], label='Not Measured'),
        mlines.Line2D([], [], color="red", linestyle="--", label=LABELS['detection_floor']),
    ]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.02), ncol=4, fontsize=10)
    
    plt.suptitle(
        f"ALARA Predicted Isotopes > {threshold_uCi} µCi — {material_name} {title_suffix}",
        fontsize=14, y=1.08
    )
    plt.tight_layout()
    
    if save_dir:
        safe_name = material_name.replace(" ", "_").replace("-", "")
        safe_suffix = title_suffix.replace(" ", "_").replace("-", "").replace("(", "").replace(")", "")
        filename = f"alara_threshold_pred_{safe_name}_{safe_suffix}.png"
        save_path = Path(save_dir) / filename
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


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
    Plot ALARA-predicted isotopes above threshold with gamma-emitter status.
    """
    utils = _safe_import_nuclear_data()
    if not utils:
        print("nuclear_data not available")
        return None

    has_gamma_emission = utils['has_gamma_emission']
    gamma_min = utils['GAMMA_ENERGY_MIN_KEV']
    gamma_max = utils['GAMMA_ENERGY_MAX_KEV']

    colors = {
        'Measured': '#2a9d8f',
        'Not measured (γ)': '#e76f51',
        'Not measured (no γ)': '#adb5bd',
        'Total': '#264653'
    }

    alara_df = pd.read_csv(alara_activity_file)
    alara_col = build_cooling_map(alara_df, [cooling_time]).get(cooling_time)
    if not alara_col or alara_col not in alara_df.columns:
        print(f"No matching ALARA column for cooling time: {cooling_time}")
        return None

    ct_df = alara_df[['isotope', alara_col]].copy()
    ct_df = ct_df[ct_df['isotope'].str.lower() != 'total']
    ct_df['ALARA_uCi'] = ct_df[alara_col] * BQ_TO_UCI
    ct_df = ct_df[ct_df['ALARA_uCi'] > threshold_uCi]

    if ct_df.empty:
        print(f"No ALARA isotopes > threshold for {material} at {cooling_time}")
        return None

    exp_nuclides = experimental_data.get(cooling_time, {}) if experimental_data else {}
    exp_iso_set = {iso.lower() for iso in exp_nuclides.keys()}
    detection_floor = None
    if exp_nuclides:
        detection_values = [v['activity'] for v in exp_nuclides.values() if v.get('activity', 0) > 0]
        if detection_values:
            detection_floor = min(detection_values)

    def classify_isotope(iso):
        iso_clean = iso.lower().replace('_', '').replace('-', '')
        exp_clean = {s.replace('_', '').replace('-', '') for s in exp_iso_set}
        if iso_clean in exp_clean:
            return 'Measured'
        if has_gamma_emission(iso, min_intensity=0.01,
                              energy_min_keV=gamma_min,
                              energy_max_keV=gamma_max):
            return 'Not measured (γ)'
        return 'Not measured (no γ)'

    ct_df['status'] = ct_df['isotope'].apply(classify_isotope)
    ct_df = ct_df.sort_values('ALARA_uCi', ascending=False)

    total_row = pd.DataFrame({
        'isotope': ['TOTAL'],
        'ALARA_uCi': [ct_df['ALARA_uCi'].sum()],
        'status': ['Total']
    })
    ct_df = pd.concat([total_row, ct_df], ignore_index=True)
    bar_colors = ct_df['status'].map(colors).fillna('#264653')

    n_isotopes = len(ct_df)
    fig_width = max(figsize[0], n_isotopes * 0.35) if n_isotopes > 30 else figsize[0]
    fig, ax = plt.subplots(figsize=(fig_width, figsize[1]))
    x = np.arange(len(ct_df))
    ax.bar(x, ct_df['ALARA_uCi'], color=bar_colors, edgecolor='black', linewidth=0.5)

    if n_isotopes > 50:
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=90, ha='center', fontsize=6)
    elif n_isotopes > 30:
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=75, ha='right', fontsize=7)
    elif n_isotopes > 15:
        ax.set_xticks(x)
        ax.set_xticklabels(ct_df['isotope'], rotation=60, ha='right', fontsize=8)
    else:
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
        ax.axhline(detection_floor, color='red', linestyle='--', linewidth=1.2,
                   label='Lowest experimental activity')

    n_measured = (ct_df['status'] == 'Measured').sum()
    n_gamma = (ct_df['status'] == 'Not measured (γ)').sum()
    n_no_gamma = (ct_df['status'] == 'Not measured (no γ)').sum()

    legend_handles = [
        mpatches.Patch(color=colors['Total'], label='Total (ALARA)'),
        mpatches.Patch(color=colors['Measured'], label=f'Measured experimentally ({n_measured})'),
        mpatches.Patch(color=colors['Not measured (γ)'], label=f'Not measured, γ emitter ({n_gamma})'),
        mpatches.Patch(color=colors['Not measured (no γ)'], label=f'Not measured, no γ ({n_no_gamma})'),
        mlines.Line2D([0], [0], color='red', linestyle='--',
                      label='Lowest experimental activity')
    ]
    ax.legend(handles=legend_handles, fontsize=9, loc='upper right',
              title=f'γ range: {int(gamma_min)}-{int(gamma_max)} keV')

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
    """
    if material_to_tally is None:
        try:
            from data_loaders import MATERIAL_TO_TALLY
            material_to_tally = MATERIAL_TO_TALLY
        except ImportError:
            raise ValueError("material_to_tally must be provided when data_loaders is not available")
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


def get_alara_isotopes_above_threshold(
    alara_activity_file: Path,
    cooling_time: str,
    threshold_uCi: float = 1e-4
) -> pd.DataFrame:
    """
    Get ALARA isotopes above threshold for a given cooling time.
    """
    alara_df = pd.read_csv(alara_activity_file)
    alara_col = build_cooling_map(alara_df, [cooling_time]).get(cooling_time)
    if not alara_col or alara_col not in alara_df.columns:
        return pd.DataFrame()

    result = alara_df[['isotope', alara_col]].copy()
    result = result[result['isotope'].str.lower() != 'total']
    result['activity_uCi'] = result[alara_col] * BQ_TO_UCI
    result = result[result['activity_uCi'] > threshold_uCi]
    result = result.rename(columns={alara_col: 'activity_Bq_cm3'})
    result = result.sort_values('activity_uCi', ascending=False)
    return result


def count_alara_isotopes_by_material(
    alara_output_dir: Path,
    material_to_tally: Optional[Dict[str, str]] = None,
    threshold_uCi: float = 1e-4,
    cooling_times: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Count ALARA isotopes above threshold for all materials and cooling times.
    """
    if material_to_tally is None:
        try:
            from data_loaders import MATERIAL_TO_TALLY
            material_to_tally = MATERIAL_TO_TALLY
        except ImportError:
            raise ValueError("material_to_tally must be provided when data_loaders is not available")
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


def plot_vit_j_comparison(
    alara_df: pd.DataFrame,
    material_name: str,
    experimental_data: Dict[str, Dict],
    cooling_map: Optional[Dict[str, str]] = None,
    save_dir: Optional[Path] = None,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Side-by-side bar chart comparison for VIT-J test.
    Only includes isotopes measured experimentally.
    
    Parameters
    ----------
    alara_df : pd.DataFrame
        ALARA DataFrame with 'isotope' column and activity columns
    material_name : str
        Material name for title
    experimental_data : dict
        {cooling_time: {isotope: {'activity': float, ...}}}
    cooling_map : dict, optional
        Mapping from cooling time labels to ALARA column names
    save_dir : Path, optional
        Directory to save figure
    show : bool
        Whether to display
    
    Returns
    -------
    plt.Figure or None
    """
    utils = _safe_import_nuclear_data()
    if not utils:
        print("nuclear_data not available")
        return None
    
    canonical_iso = utils['canonical_iso']
    
    cooling_order = ["300s", "2h", "24h", "4d", "15d"]
    
    # Build default cooling map if not provided
    if cooling_map is None:
        cooling_map = build_cooling_map(alara_df, cooling_order)
    
    valid_cols = [c for c in cooling_order if cooling_map.get(c) in alara_df.columns]
    if not valid_cols:
        return None
    
    fig, axes = plt.subplots(1, len(valid_cols), figsize=(5 * len(valid_cols), 6), squeeze=False)
    axes = axes.flatten()
    
    for idx, ct in enumerate(valid_cols):
        ax = axes[idx]
        col = cooling_map[ct]
        
        exp_nuclides = experimental_data.get(ct, {})
        if not exp_nuclides:
            ax.text(0.5, 0.5, "No Exp Data", ha="center", va="center")
            ax.axis("off")
            continue
        
        rows = []
        for iso, props in exp_nuclides.items():
            canon = canonical_iso(iso)
            alara_row = alara_df[alara_df["isotope"].apply(canonical_iso) == canon]
            alara_val_bq = alara_row[col].values[0] if not alara_row.empty else 0.0
            alara_uCi = alara_val_bq * BQ_TO_UCI
            
            rows.append({
                "isotope": iso,
                "ALARA": alara_uCi,
                LABELS["experimental"]: props.get("activity", 0.0)
            })
        
        comp_df = pd.DataFrame(rows)
        if comp_df.empty:
            ax.text(0.5, 0.5, "No matched isotopes", ha="center", va="center")
            ax.axis("off")
            continue
        
        comp_df = comp_df.sort_values(LABELS["experimental"], ascending=False)
        
        x = np.arange(len(comp_df))
        width = 0.35
        
        ax.bar(x - width/2, comp_df["ALARA"], width, 
               label=LABELS["alara"], color=SOURCE_COLORS['alara'])
        ax.bar(x + width/2, comp_df[LABELS["experimental"]], width, 
               label=LABELS["experimental"], color=SOURCE_COLORS['experimental'])
        
        ax.set_xticks(x)
        ax.set_xticklabels(comp_df["isotope"], rotation=45, ha="right")
        ax.set_yscale("log")
        ax.set_title(f"{ct}")
        ax.set_ylabel("Activity (µCi)")
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", alpha=0.3)
    
    plt.suptitle(f"VIT-J Test: {LABELS['alara']} vs {LABELS['experimental']} — {material_name}",
                 fontsize=14, y=1.05)
    plt.tight_layout()
    
    if save_dir:
        safe_name = material_name.replace(" ", "_").replace("-", "")
        filename = f"vit_j_comparison_{safe_name}.png"
        save_path = Path(save_dir) / filename
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


# ==============================================================================
# FLUX WIRE PLOTS
# ==============================================================================

def plot_flux_wire_measurements(
    flux_df: pd.DataFrame,
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Measurements (Individual Samples)',
    show_errorbar: bool = True,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Plot flux wire measurements showing energy ranges for each sample.
    
    Parameters
    ----------
    flux_df : pd.DataFrame
        DataFrame with 'sample', 'phi', 'phi_unc', 'e_start', 'e_end', 'energy_MeV'
    output_dir : str, optional
        Directory to save plot
    figsize : tuple
        Figure size in inches
    title : str
        Plot title
    show_errorbar : bool
        Whether to show error bars
    show : bool
        Whether to display
    
    Returns
    -------
    plt.Figure or None
    """
    if flux_df.empty:
        print("Flux DataFrame is empty, cannot plot.")
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    samples = sorted(flux_df['sample'].unique())
    cmap = plt.cm.get_cmap('tab20', max(20, len(samples)))
    handles = {}
    
    for idx, sample in enumerate(samples):
        sub = flux_df[flux_df['sample'] == sample]
        color = cmap(idx % 20)
        
        for _, r in sub.iterrows():
            ax.hlines(y=r['phi'], xmin=r['e_start'], xmax=r['e_end'], 
                     color=color, linewidth=6, alpha=0.9)
            ax.scatter(r['energy_MeV'], r['phi'], s=40, color=color, 
                      edgecolor='k', zorder=3)
            if show_errorbar and np.isfinite(r.get('phi_unc', np.nan)) and r['phi_unc'] > 0:
                ax.errorbar(r['energy_MeV'], r['phi'], yerr=r['phi_unc'], 
                           fmt='none', ecolor=color, elinewidth=1.2, capsize=3)
        
        legend_label = re.sub(r'_\d+cm$', '', sample)
        handles[sample] = plt.Line2D([0], [0], color=color, lw=6, label=legend_label)
    
    ax.legend(handles=handles.values(), bbox_to_anchor=(1.02, 1.0), loc='upper left', fontsize=7)
    ax.set_xlabel('Neutron Energy Range (MeV)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Estimated Flux (n/cm²/s)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_energy_vs_flux.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


def plot_flux_vs_spectrum(
    flux_df: pd.DataFrame,
    spectrum_edges: np.ndarray,
    spectrum_flux: np.ndarray,
    spectrum_label: str = 'MCNP Spectrum',
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Measurements vs MCNP Spectrum',
    show_errorbar: bool = True,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Plot flux wire measurements overlaid on MCNP spectrum.
    
    Parameters
    ----------
    flux_df : pd.DataFrame
        DataFrame with flux wire measurements
    spectrum_edges : np.ndarray
        Energy bin edges for spectrum (MeV)
    spectrum_flux : np.ndarray
        Flux values for each bin
    spectrum_label : str
        Label for spectrum in legend
    output_dir : str, optional
        Directory to save plot
    figsize : tuple
        Figure size
    title : str
        Plot title
    show_errorbar : bool
        Whether to show error bars
    show : bool
        Whether to display
    
    Returns
    -------
    plt.Figure or None
    """
    if flux_df.empty:
        print("Flux DataFrame is empty, cannot plot.")
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot spectrum as step
    ax.step(spectrum_edges, np.concatenate([spectrum_flux, spectrum_flux[-1:]]), 
            where='post', color='gray', linewidth=2.2, alpha=0.7, label=spectrum_label)
    
    # Plot flux wire measurements
    samples = sorted(flux_df['sample'].unique())
    cmap = plt.cm.get_cmap('tab20', max(20, len(samples)))
    handles = {}
    
    for idx, sample in enumerate(samples):
        sub = flux_df[flux_df['sample'] == sample]
        color = cmap(idx % 20)
        
        for _, r in sub.iterrows():
            ax.scatter(r['energy_MeV'], r['phi'], s=80, color=color, 
                      edgecolor='k', linewidth=1.5, zorder=5, alpha=0.8)
            if show_errorbar and np.isfinite(r.get('phi_unc', np.nan)) and r['phi_unc'] > 0:
                ax.errorbar(r['energy_MeV'], r['phi'], yerr=r['phi_unc'], 
                           fmt='none', ecolor=color, elinewidth=1.5, capsize=4, zorder=4)
        
        legend_label = re.sub(r'_\d+cm$', '', sample)
        handles[sample] = plt.Line2D([0], [0], marker='o', color='w', 
                                     markerfacecolor=color, markersize=8, 
                                     markeredgecolor='k', label=legend_label)
    
    legend_elements = [plt.Line2D([0], [0], color='gray', lw=2.2, label=spectrum_label)] + list(handles.values())
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1.0), loc='upper left', fontsize=7)
    
    ax.set_xlabel('Neutron Energy (MeV)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Flux (n/cm²/s)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_vs_spectrum.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


def plot_flux_energy_ranges(
    flux_df: pd.DataFrame,
    spectrum_edges: np.ndarray,
    spectrum_flux: np.ndarray,
    spectrum_label: str = 'MCNP Spectrum',
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Energy Ranges vs MCNP Spectrum',
    show_errorbar: bool = True,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Plot flux wire energy ranges (as horizontal lines) over MCNP spectrum.
    """
    if flux_df.empty:
        print("Flux DataFrame is empty, cannot plot.")
        return None

    fig, ax = plt.subplots(figsize=figsize)
    ax.step(spectrum_edges,
            np.concatenate([spectrum_flux, spectrum_flux[-1:]]),
            where='post', color='gray', linewidth=2.2, alpha=0.7,
            label=spectrum_label)

    samples = sorted(flux_df['sample'].unique())
    cmap = plt.cm.get_cmap('tab20', max(20, len(samples)))
    handles = {}

    for idx, sample in enumerate(samples):
        sub = flux_df[flux_df['sample'] == sample]
        color = cmap(idx % 20)

        for _, r in sub.iterrows():
            ax.hlines(y=r['phi'], xmin=r['e_start'], xmax=r['e_end'],
                      color=color, linewidth=4, alpha=0.9)
            if show_errorbar and np.isfinite(r.get('phi_unc', np.nan)) and r['phi_unc'] > 0:
                ax.errorbar(r['energy_MeV'], r['phi'], yerr=r['phi_unc'],
                            fmt='none', ecolor=color, elinewidth=1.5, capsize=4, zorder=4)

        legend_label = re.sub(r'_\d+cm$', '', sample)
        handles[sample] = plt.Line2D([0], [0], color=color, lw=4, label=legend_label)

    legend_elements = [plt.Line2D([0], [0], color='gray', lw=2.2,
                                  label=spectrum_label)] + list(handles.values())
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1.0),
              loc='upper left', fontsize=7)

    ax.set_xlabel('Neutron Energy (MeV)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Flux (n/cm²/s)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()

    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_vs_spectrum_ranges.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def create_all_flux_plots(
    flux_wires_df: pd.DataFrame,
    spectrum_csv: str,
    output_dir: str,
    meta_df: Optional[pd.DataFrame] = None,
    show_plots: bool = True
) -> Dict[str, plt.Figure]:
    """
    Create all flux wire plots in one call.
    """
    flux_df = compute_flux_from_measurements(flux_wires_df, meta_df)
    if flux_df.empty:
        print("No flux data to plot")
        return {}

    spectrum = load_mcnp_spectrum(spectrum_csv)
    if spectrum is None:
        return {}

    figures = {}

    fig1 = plot_flux_wire_measurements(flux_df, output_dir=output_dir, show=show_plots)
    if fig1:
        figures['measurements'] = fig1

    fig2 = plot_flux_vs_spectrum(
        flux_df,
        spectrum_edges=spectrum['edges'],
        spectrum_flux=spectrum['flux'],
        output_dir=output_dir,
        show=show_plots
    )
    if fig2:
        figures['vs_spectrum'] = fig2

    fig3 = plot_flux_energy_ranges(
        flux_df,
        spectrum_edges=spectrum['edges'],
        spectrum_flux=spectrum['flux'],
        output_dir=output_dir,
        show=show_plots
    )
    if fig3:
        figures['energy_ranges'] = fig3

    return figures


# ==============================================================================
# DECAY CURVE PLOTS  
# ==============================================================================

def plot_decay_curves(
    isotopes: List[str],
    half_lives_s: Dict[str, float],
    initial_activities: Optional[Dict[str, float]] = None,
    t_max_days: float = 30.0,
    title: str = "Radioactive Decay Curves",
    save_path: Optional[str] = None,
    show: bool = True,
    log_y: bool = True
) -> Optional[plt.Figure]:
    """
    Plot decay curves for multiple isotopes.
    
    Parameters
    ----------
    isotopes : list
        List of isotope names
    half_lives_s : dict
        {isotope: half_life_seconds}
    initial_activities : dict, optional
        {isotope: initial_activity} - if None, normalized to 1
    t_max_days : float
        Maximum time to plot (days)
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display
    log_y : bool
        Use log scale for y-axis
    
    Returns
    -------
    plt.Figure or None
    """
    utils = _safe_import_nuclear_data()
    if not utils:
        LN2 = 0.693147
        format_iso_pretty = lambda x: x
    else:
        LN2 = utils['LN2']
        format_iso_pretty = utils['format_iso_pretty']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    t_array = np.linspace(0, t_max_days * 86400, 500)
    t_days = t_array / 86400
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(isotopes)))
    
    for i, iso in enumerate(isotopes):
        hl_s = half_lives_s.get(iso)
        if hl_s is None or hl_s <= 0:
            continue
        
        A0 = 1.0 if initial_activities is None else initial_activities.get(iso, 1.0)
        lam = LN2 / hl_s
        A_t = A0 * np.exp(-lam * t_array)
        
        hl_days = hl_s / 86400
        hl_label = f"{hl_days:.1f}d" if hl_days >= 1 else f"{hl_days*24:.1f}h"
        
        if log_y:
            ax.semilogy(t_days, A_t, linewidth=2, color=colors[i],
                       label=f"{format_iso_pretty(iso)} (T½={hl_label})")
        else:
            ax.plot(t_days, A_t, linewidth=2, color=colors[i],
                   label=f"{format_iso_pretty(iso)} (T½={hl_label})")
    
    ax.set_xlabel('Time (days)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Activity (relative to initial)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, t_max_days)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return fig


# ==============================================================================
# MODULE INFO
# ==============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("CONSOLIDATED PLOTTING MODULE FOR MCNP-ALARA WORKFLOW")
    print("=" * 70)
    print()
    print("This module centralizes ALL plotting functions for consistent styling.")
    print()
    print("STYLE CONSTANTS:")
    print("  - MATERIAL_COLORS: Colors for each material")
    print("  - COOLING_COLORS: Colors for each cooling time")
    print("  - SOURCE_COLORS: 'experimental' (teal) vs 'alara' (coral)")
    print("  - LABELS: Standard labels (always 'Experimental', never 'Exp')")
    print()
    print("PLOTTING FUNCTIONS:")
    print("  Comparison:")
    print("    - plot_comparison_scatter()")
    print("    - plot_comparison_by_material()")
    print()
    print("  SNR/Detection:")
    print("    - plot_snr_heatmap()")
    print("    - plot_snr_lines()")
    print("    - plot_threshold_comparison()")
    print("    - plot_vit_j_comparison()")
    print()
    print("  Flux:")
    print("    - plot_flux_wire_measurements()")
    print("    - plot_flux_vs_spectrum()")
    print()
    print("  Decay:")
    print("    - plot_decay_curves()")
    print()
    print("USAGE:")
    print("  from plotting import plot_comparison_by_material, COOLING_COLORS")
    print("  apply_standard_style()  # Call once at notebook start")
