"""
Flux wire plotting and analysis functions for MCNP-ALARA workflow.

This module provides visualization functions for flux wire measurements,
including comparison with MCNP spectrum data.

Depends on:
    - flux_wire_loader: For loading and calculating flux wire data
    - isotope_utils: For isotope name utilities

Usage:
    from flux_wire_plotting import (
        compute_flux_from_measurements,
        plot_flux_wire_measurements,
        plot_flux_vs_spectrum,
        plot_flux_energy_ranges,
        load_mcnp_spectrum
    )
    
    # Compute flux values
    flux_df = compute_flux_from_measurements(flux_wires_df, meta_df)
    
    # Generate plots
    fig = plot_flux_wire_measurements(flux_df, output_dir='alara_output')
    fig = plot_flux_vs_spectrum(flux_df, spectrum_csv='spectrum_vit_j.csv')
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

from isotope_utils import canonical_iso, LN2, AVOGADRO
from flux_wire_loader import get_metadata_df, WIRE_METADATA


# ==============================================================================
# FLUX CALCULATION FROM MEASUREMENTS
# ==============================================================================

def parse_half_life_seconds(hl_str: str) -> Optional[float]:
    """
    Convert half-life string like '5.271 y' or '83.6 d' to seconds.
    
    Parameters:
        hl_str: Half-life string with value and unit (e.g., '12.701 h')
    
    Returns:
        Half-life in seconds, or None if parsing fails
    """
    if not hl_str:
        return None
    try:
        parts = hl_str.split()
        if len(parts) != 2:
            return None
        val, unit = parts
        val = float(val)
        unit = unit.lower()
        mult = {
            's': 1, 'sec': 1,
            'm': 60, 'min': 60,
            'h': 3600, 'hr': 3600,
            'd': 86400, 'day': 86400,
            'w': 604800, 'wk': 604800,
            'y': 365.25 * 86400, 'yr': 365.25 * 86400,
        }.get(unit)
        return val * mult if mult else None
    except Exception:
        return None


def compute_flux_from_measurements(
    flux_wires_df: pd.DataFrame,
    meta_df: Optional[pd.DataFrame] = None,
    default_irradiation_seconds: float = 7203,
    default_decay_seconds: float = 0
) -> pd.DataFrame:
    """
    Compute neutron flux from flux wire activity measurements.
    
    Parameters:
        flux_wires_df: DataFrame with flux wire measurements (from flux_wire_loader)
        meta_df: Wire metadata DataFrame (will be created if not provided)
        default_irradiation_seconds: Default irradiation time if not in data
        default_decay_seconds: Default decay time if not in data
    
    Returns:
        DataFrame with computed flux values for plotting
    """
    if meta_df is None:
        meta_df = get_metadata_df()
    
    flux_records = []
    skipped = []
    
    for _, row in flux_wires_df.iterrows():
        sample = row['sample']
        prod_iso = canonical_iso(row['isotope'])
        
        # Extract base sample name (remove suffixes like _25cm, trailing letters)
        base_sample = re.sub(r'_\d+cm$', '', sample)
        base_sample = re.sub(r'[a-z]$', '', base_sample)
        
        # Try to find matching metadata (exact match first, then base, then isotope-only)
        mrow = meta_df[(meta_df['sample'] == sample) & (meta_df['prod_canon'] == prod_iso)]
        if mrow.empty:
            mrow = meta_df[(meta_df['sample'] == base_sample) & (meta_df['prod_canon'] == prod_iso)]
        if mrow.empty:
            mrow = meta_df[meta_df['prod_canon'] == prod_iso]
        if mrow.empty:
            skipped.append((sample, prod_iso, 'no metadata'))
            continue
        
        mrow = mrow.iloc[0]
        mass_g = mrow['mass_g'] if not pd.isna(mrow['mass_g']) else row.get('mass_g', 1.0)
        activity_Bq = row.get('activity_Bq', np.nan)
        unc_Bq = row.get('uncertainty_Bq', np.nan)
        
        # Parse half-life
        hl_seconds = parse_half_life_seconds(row.get('half_life'))
        if not hl_seconds or hl_seconds <= 0:
            skipped.append((sample, prod_iso, 'half-life parse failed'))
            continue
        
        lam = np.log(2) / hl_seconds
        
        # Get target atomic weight from target isotope
        mass_match = re.search(r"(\d+)", mrow['iso_canon'])
        A_mass = float(mass_match.group(1)) if mass_match else None
        if not A_mass:
            skipped.append((sample, prod_iso, 'mass number missing'))
            continue
        
        # Calculate N_atoms
        N_atoms = (mass_g / A_mass) * AVOGADRO
        
        # Get irradiation and decay times
        irr_sec = float(row.get('irradiation_seconds', default_irradiation_seconds))
        dec_sec = float(row.get('decay_seconds', default_decay_seconds))
        
        # Saturation and decay factors
        S = 1 - np.exp(-lam * irr_sec)
        D = np.exp(-lam * dec_sec)
        
        # Calculate flux
        denom = N_atoms * mrow['sigma_cm2'] * S * D
        phi = activity_Bq / denom if denom > 0 else np.nan
        
        phi_unc = np.nan
        if np.isfinite(phi) and activity_Bq > 0 and np.isfinite(unc_Bq):
            phi_unc = phi * (unc_Bq / activity_Bq)
        
        flux_records.append({
            'sample': sample,
            'product': prod_iso,
            'phi': phi,
            'phi_unc': phi_unc,
            'activity_Bq': activity_Bq,
            'uncertainty_Bq': unc_Bq,
            'N_atoms': N_atoms,
            'sigma_cm2': mrow['sigma_cm2'],
            'S': S,
            'D': D,
            'denom': denom,
            'energy_MeV': mrow['energy_mid_MeV'],
            'e_start': mrow['e_start'],
            'e_end': mrow['e_end'],
            'category': mrow['category']
        })
    
    if skipped:
        print("Skipped entries:")
        for s in skipped[:10]:  # Limit output
            print(f"  {s[0]} {s[1]} -> {s[2]}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")
    
    if not flux_records:
        print("No flux records computed. Check mapping, half-life strings, or decay time.")
        return pd.DataFrame()
    
    return pd.DataFrame(flux_records).dropna(subset=['phi', 'e_start', 'e_end'])


# ==============================================================================
# SPECTRUM LOADING
# ==============================================================================

def load_mcnp_spectrum(
    spectrum_csv: str,
    energy_scale: str = 'MeV',
    flux_divisor: float = 15.0
) -> Optional[Dict[str, np.ndarray]]:
    """
    Load MCNP spectrum data from CSV file.
    
    Parameters:
        spectrum_csv: Path to CSV file with spectrum data
        energy_scale: Output energy scale ('MeV' or 'eV')
        flux_divisor: Divisor to scale flux per lethargy (normalization factor)
    
    Returns:
        Dictionary with 'edges', 'e_low', 'e_high', 'flux' arrays, or None if load fails
    """
    spectrum_path = Path(spectrum_csv)
    if not spectrum_path.exists():
        print(f"Spectrum CSV not found at: {spectrum_path}")
        return None
    
    try:
        spectrum_df = pd.read_csv(spectrum_path)
        
        # Convert energies
        if 'E_low[eV]' in spectrum_df.columns:
            e_low = spectrum_df['E_low[eV]'].values
            e_high = spectrum_df['E_high[eV]'].values
        elif 'E_low_MeV' in spectrum_df.columns:
            e_low = spectrum_df['E_low_MeV'].values * 1e6
            e_high = spectrum_df['E_high_MeV'].values * 1e6
        else:
            print("Unrecognized spectrum CSV format")
            return None
        
        if energy_scale == 'MeV':
            e_low = e_low / 1e6
            e_high = e_high / 1e6
        
        # Get flux per lethargy
        if 'flux_per_lethargy [n·cm⁻²·s⁻¹]' in spectrum_df.columns:
            flux = spectrum_df['flux_per_lethargy [n·cm⁻²·s⁻¹]'].values / flux_divisor
        elif 'flux_per_lethargy' in spectrum_df.columns:
            flux = spectrum_df['flux_per_lethargy'].values / flux_divisor
        else:
            print("Flux column not found in spectrum CSV")
            return None
        
        # Create bin edges for step plot
        edges = np.concatenate([e_low[:1], e_high])
        
        return {
            'e_low': e_low,
            'e_high': e_high,
            'edges': edges,
            'flux': flux
        }
    
    except Exception as e:
        print(f"Could not load spectrum CSV: {e}")
        return None


# ==============================================================================
# PLOTTING FUNCTIONS
# ==============================================================================

def plot_flux_wire_measurements(
    flux_df: pd.DataFrame,
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Measurements (Individual Samples)',
    show_errorbar: bool = True
) -> plt.Figure:
    """
    Plot flux wire measurements showing energy ranges for each sample.
    
    Parameters:
        flux_df: DataFrame from compute_flux_from_measurements()
        output_dir: Directory to save plot (None = don't save)
        figsize: Figure size in inches
        title: Plot title
        show_errorbar: Whether to show error bars
    
    Returns:
        Matplotlib Figure object
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
            # Horizontal line for energy range
            ax.hlines(y=r['phi'], xmin=r['e_start'], xmax=r['e_end'], 
                     color=color, linewidth=6, alpha=0.9)
            # Point at midpoint
            ax.scatter(r['energy_MeV'], r['phi'], s=40, color=color, 
                      edgecolor='k', zorder=3)
            # Error bar
            if show_errorbar and np.isfinite(r.get('phi_unc', np.nan)) and r['phi_unc'] > 0:
                ax.errorbar(r['energy_MeV'], r['phi'], yerr=r['phi_unc'], 
                           fmt='none', ecolor=color, elinewidth=1.2, capsize=3)
        
        # Legend label (remove _XXcm suffix)
        legend_label = re.sub(r'_\d+cm$', '', sample)
        handles[sample] = plt.Line2D([0], [0], color=color, lw=6, label=legend_label)
    
    ax.legend(handles=handles.values(), bbox_to_anchor=(1.02, 1.0), 
              loc='upper left', fontsize=7)
    ax.set_xlabel('Neutron Energy Range (MeV)')
    ax.set_ylabel('Estimated Flux (n/cm²/s)')
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_energy_vs_flux.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")
    
    return fig


def plot_flux_vs_spectrum(
    flux_df: pd.DataFrame,
    spectrum_csv: str,
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Measurements vs MCNP Spectrum',
    show_errorbar: bool = True,
    flux_divisor: float = 15.0
) -> Optional[plt.Figure]:
    """
    Plot flux wire measurements overlaid on MCNP spectrum.
    
    Parameters:
        flux_df: DataFrame from compute_flux_from_measurements()
        spectrum_csv: Path to MCNP spectrum CSV file
        output_dir: Directory to save plot (None = don't save)
        figsize: Figure size in inches
        title: Plot title
        show_errorbar: Whether to show error bars
        flux_divisor: Divisor for spectrum flux normalization
    
    Returns:
        Matplotlib Figure object, or None if spectrum load fails
    """
    if flux_df.empty:
        print("Flux DataFrame is empty, cannot plot.")
        return None
    
    spectrum = load_mcnp_spectrum(spectrum_csv, flux_divisor=flux_divisor)
    if spectrum is None:
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot spectrum as step
    ax.step(spectrum['edges'], 
            np.concatenate([spectrum['flux'], spectrum['flux'][-1:]]), 
            where='post', color='gray', linewidth=2.2, alpha=0.7, 
            label='MCNP Spectrum (VIT-J)')
    
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
    
    # Build legend
    legend_elements = [plt.Line2D([0], [0], color='gray', lw=2.2, 
                                  label='MCNP Spectrum (VIT-J)')] + list(handles.values())
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1.0), 
              loc='upper left', fontsize=7)
    
    ax.set_xlabel('Neutron Energy (MeV)')
    ax.set_ylabel('Flux (n/cm²/s)')
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_vs_spectrum.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")
    
    return fig


def plot_flux_energy_ranges(
    flux_df: pd.DataFrame,
    spectrum_csv: str,
    output_dir: Optional[str] = None,
    figsize: Tuple[float, float] = (12, 7),
    title: str = 'Flux Wire Energy Ranges vs MCNP Spectrum',
    show_errorbar: bool = True,
    flux_divisor: float = 15.0
) -> Optional[plt.Figure]:
    """
    Plot flux wire energy ranges (as horizontal lines) over MCNP spectrum.
    
    Parameters:
        flux_df: DataFrame from compute_flux_from_measurements()
        spectrum_csv: Path to MCNP spectrum CSV file
        output_dir: Directory to save plot (None = don't save)
        figsize: Figure size in inches
        title: Plot title
        show_errorbar: Whether to show error bars
        flux_divisor: Divisor for spectrum flux normalization
    
    Returns:
        Matplotlib Figure object, or None if spectrum load fails
    """
    if flux_df.empty:
        print("Flux DataFrame is empty, cannot plot.")
        return None
    
    spectrum = load_mcnp_spectrum(spectrum_csv, flux_divisor=flux_divisor)
    if spectrum is None:
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot spectrum
    ax.step(spectrum['edges'], 
            np.concatenate([spectrum['flux'], spectrum['flux'][-1:]]), 
            where='post', color='gray', linewidth=2.2, alpha=0.7, 
            label='MCNP Spectrum (VIT-J)')
    
    # Plot flux wire ranges
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
                                  label='MCNP Spectrum (VIT-J)')] + list(handles.values())
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1.0), 
              loc='upper left', fontsize=7)
    
    ax.set_xlabel('Neutron Energy (MeV)')
    ax.set_ylabel('Flux (n/cm²/s)')
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        out_path = os.path.join(output_dir, 'flux_wire_vs_spectrum_ranges.png')
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {out_path}")
    
    return fig


def recompute_phi_in_dataframe(
    flux_wires_df: pd.DataFrame,
    meta_df: Optional[pd.DataFrame] = None,
    default_irradiation_seconds: float = 7203,
    default_decay_seconds: float = 0,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Recompute phi (neutron flux) values in-place in flux_wires_df.
    
    This updates the flux_wires_df with computed phi and phi_unc columns
    along with intermediate calculation values for debugging.
    
    Parameters:
        flux_wires_df: DataFrame with flux wire measurements
        meta_df: Wire metadata DataFrame (will be created if not provided)
        default_irradiation_seconds: Default irradiation time
        default_decay_seconds: Default decay time
        verbose: Whether to print diagnostic information
    
    Returns:
        Updated DataFrame with phi and calculation columns added
    """
    if meta_df is None:
        meta_df = get_metadata_df()
    
    # Columns to add
    new_cols = ['phi', 'phi_unc', 'sigma_cm2', 'mass_used_g', 'A_mass', 
                'N_atoms', 'lam', 'S', 'D', 'denom', 'irradiation_seconds_used']
    
    for col in new_cols:
        if col not in flux_wires_df.columns:
            flux_wires_df[col] = np.nan
    
    for idx, row in flux_wires_df.iterrows():
        sample = row['sample']
        prod_iso = row['isotope']
        activity_Bq = row.get('activity_Bq', np.nan)
        unc_Bq = row.get('uncertainty_Bq', np.nan)
        
        irr_sec = int(row.get('irradiation_seconds', default_irradiation_seconds))
        if irr_sec == 7203:
            irr_sec = int(default_irradiation_seconds)
        
        # Find matching metadata
        mrow = meta_df[(meta_df['sample'] == sample) & (meta_df['prod_canon'] == prod_iso)]
        if mrow.empty:
            mrow = meta_df[meta_df['prod_canon'] == prod_iso]
        
        if mrow.empty:
            if verbose:
                print(f"No metadata for sample={sample}, isotope={prod_iso}")
            continue
        
        mrow = mrow.iloc[0]
        sigma_cm2 = mrow['sigma_cm2']
        mass_used = mrow['mass_g'] if not pd.isna(mrow.get('mass_g')) else row.get('mass_g', np.nan)
        
        # Parse mass number
        mass_match = re.search(r"(\d+)", mrow['prod_canon'])
        A_mass = float(mass_match.group(1)) if mass_match else np.nan
        
        # Parse half-life
        hl_seconds = parse_half_life_seconds(row.get('half_life', ''))
        if not hl_seconds or hl_seconds <= 0:
            continue
        
        lam = np.log(2) / hl_seconds
        dec_sec = int(row.get('decay_seconds', default_decay_seconds))
        
        # Calculate factors
        S = 1 - np.exp(-lam * float(irr_sec)) if not np.isnan(lam) else np.nan
        D = np.exp(-lam * float(dec_sec)) if not np.isnan(lam) else np.nan
        
        # N_atoms
        if not np.isnan(mass_used) and not np.isnan(A_mass) and A_mass > 0:
            N_atoms = (mass_used / A_mass) * AVOGADRO
        else:
            N_atoms = np.nan
        
        denom = N_atoms * sigma_cm2 * S * D if not any(np.isnan([N_atoms, sigma_cm2, S, D])) else np.nan
        phi = activity_Bq / denom if denom and denom > 0 else np.nan
        phi_unc = phi * (unc_Bq / activity_Bq) if (not np.isnan(phi) and not np.isnan(unc_Bq) and activity_Bq > 0) else np.nan
        
        # Update DataFrame
        flux_wires_df.loc[idx, 'phi'] = phi
        flux_wires_df.loc[idx, 'phi_unc'] = phi_unc
        flux_wires_df.loc[idx, 'sigma_cm2'] = sigma_cm2
        flux_wires_df.loc[idx, 'mass_used_g'] = mass_used
        flux_wires_df.loc[idx, 'A_mass'] = A_mass
        flux_wires_df.loc[idx, 'N_atoms'] = N_atoms
        flux_wires_df.loc[idx, 'lam'] = lam
        flux_wires_df.loc[idx, 'S'] = S
        flux_wires_df.loc[idx, 'D'] = D
        flux_wires_df.loc[idx, 'denom'] = denom
        flux_wires_df.loc[idx, 'irradiation_seconds_used'] = irr_sec
    
    return flux_wires_df


def display_flux_debug_table(
    flux_wires_df: pd.DataFrame,
    threshold: float = 1e14
) -> pd.DataFrame:
    """
    Display debug table of computed flux values and flag suspicious entries.
    
    Parameters:
        flux_wires_df: DataFrame with computed phi values
        threshold: Flag entries with phi above this value
    
    Returns:
        DataFrame of flagged entries (if any)
    """
    debug_cols = ['sample', 'isotope', 'activity_Bq', 'uncertainty_Bq', 
                  'mass_used_g', 'A_mass', 'N_atoms', 'sigma_cm2', 
                  'S', 'D', 'denom', 'phi', 'phi_unc', 'irradiation_seconds_used']
    
    available_cols = [c for c in debug_cols if c in flux_wires_df.columns]
    
    print("\nFlux wire computed values (sorted by phi):")
    display_df = flux_wires_df[available_cols].sort_values('phi', ascending=False)
    
    # Check for flagged entries
    if 'phi' in flux_wires_df.columns:
        flagged = flux_wires_df[flux_wires_df['phi'] > threshold][available_cols]
        if not flagged.empty:
            print(f"\n⚠️ Flagged {len(flagged)} rows with phi > {threshold:e} n/cm²/s")
            return flagged
    
    return pd.DataFrame()


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def create_all_flux_plots(
    flux_wires_df: pd.DataFrame,
    spectrum_csv: str,
    output_dir: str,
    meta_df: Optional[pd.DataFrame] = None,
    show_plots: bool = True
) -> Dict[str, plt.Figure]:
    """
    Create all flux wire plots in one call.
    
    Parameters:
        flux_wires_df: DataFrame with flux wire measurements
        spectrum_csv: Path to MCNP spectrum CSV
        output_dir: Directory to save plots
        meta_df: Wire metadata DataFrame (optional)
        show_plots: Whether to display plots
    
    Returns:
        Dictionary of figure names to Figure objects
    """
    # Compute flux values
    flux_df = compute_flux_from_measurements(flux_wires_df, meta_df)
    
    if flux_df.empty:
        print("No flux data to plot")
        return {}
    
    figures = {}
    
    # Plot 1: Individual measurements
    fig1 = plot_flux_wire_measurements(flux_df, output_dir=output_dir)
    if fig1:
        figures['measurements'] = fig1
        if show_plots:
            plt.show()
    
    # Plot 2: Measurements vs spectrum (points)
    fig2 = plot_flux_vs_spectrum(flux_df, spectrum_csv, output_dir=output_dir)
    if fig2:
        figures['vs_spectrum'] = fig2
        if show_plots:
            plt.show()
    
    # Plot 3: Energy ranges vs spectrum
    fig3 = plot_flux_energy_ranges(flux_df, spectrum_csv, output_dir=output_dir)
    if fig3:
        figures['energy_ranges'] = fig3
        if show_plots:
            plt.show()
    
    return figures


if __name__ == '__main__':
    print("flux_wire_plotting module - use from notebook or import functions")
    print("\nAvailable functions:")
    print("  - compute_flux_from_measurements(flux_wires_df, meta_df)")
    print("  - plot_flux_wire_measurements(flux_df, output_dir)")
    print("  - plot_flux_vs_spectrum(flux_df, spectrum_csv, output_dir)")
    print("  - plot_flux_energy_ranges(flux_df, spectrum_csv, output_dir)")
    print("  - create_all_flux_plots(flux_wires_df, spectrum_csv, output_dir)")
