"""
Decay physics and SNR optimization for MCNP-ALARA workflow.

This module provides NEW functionality not in alara_output_processing:
- Decay correction calculations (A_meas -> A_EOI -> A_sat)
- Flux calculation from saturation activity
- Signal-to-Noise Ratio (SNR) optimization for isotope detection
- Weighted average activity calculation
- **Bateman equation modeling for multi-stage irradiation histories**

For ALARA output parsing and time conversions, use alara_output_processing instead.

NOTE: Plotting functions (plot_snr_heatmap, plot_snr_lines, etc.) have been
consolidated in plotting.py for consistent styling. For new code, import from:
    from plotting import plot_snr_heatmap, plot_snr_lines
The versions here are kept for backwards compatibility.

Usage:
    from decay_physics import (
        decay_correct_to_eoi,
        calculate_saturation_activity,
        activity_to_asat,           # convenience: A_meas -> A_sat directly
        full_decay_chain,           # returns dict with EOI and sat activities
        calculate_flux_from_asat,
        calculate_snr_grid,
        weighted_average_activity,
        bateman_activity,
        multi_irradiation_activity
    )
    
    # For plotting, use:
    from plotting import plot_snr_heatmap, plot_snr_lines
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Union

# Import from nuclear_data (which uses paceENSDF where possible)
from nuclear_data import (
    LN2, AVOGADRO,
    get_half_life_days, get_half_life_seconds,
    half_life_to_lambda, canonical_iso, format_iso_pretty
)


# ==============================================================================
# BATEMAN EQUATION FOR IRRADIATION + DECAY
# ==============================================================================
def bateman_activity(
    t: Union[float, np.ndarray],
    half_life_s: float,
    production_rate: float = 1.0,
    t_irradiation: float = 0.0,
    A0: float = 0.0
) -> Union[float, np.ndarray]:
    """
    Calculate activity using Bateman equation for irradiation followed by decay.
    
    During irradiation (t <= t_irradiation):
        A(t) = A0*exp(-λt) + P/λ * (1 - exp(-λt))
        
    During decay (t > t_irradiation):
        A(t) = A(t_irradiation) * exp(-λ*(t - t_irradiation))
    
    Parameters:
        t: Time since start of irradiation (seconds) - can be array
        half_life_s: Half-life of isotope (seconds)
        production_rate: Production rate P = σ*φ*N (atoms/s), normalized to 1 for relative curves
        t_irradiation: Duration of irradiation (seconds)
        A0: Initial activity at t=0 (default 0)
    
    Returns:
        Activity at time t (or array of activities)
    """
    if half_life_s <= 0:
        return np.nan if isinstance(t, float) else np.full_like(t, np.nan)
    
    lam = LN2 / half_life_s
    t = np.asarray(t)
    scalar_input = t.ndim == 0
    t = np.atleast_1d(t)
    
    result = np.zeros_like(t, dtype=float)
    
    # Phase 1: During irradiation (buildup + decay)
    irr_mask = t <= t_irradiation
    if np.any(irr_mask):
        t_irr = t[irr_mask]
        exp_decay = np.exp(-lam * t_irr)
        result[irr_mask] = A0 * exp_decay + (production_rate / lam) * (1 - exp_decay)
    
    # Phase 2: After irradiation (pure decay)
    decay_mask = t > t_irradiation
    if np.any(decay_mask):
        # Activity at end of irradiation
        if t_irradiation > 0:
            exp_irr = np.exp(-lam * t_irradiation)
            A_eoi = A0 * exp_irr + (production_rate / lam) * (1 - exp_irr)
        else:
            A_eoi = A0
        # Decay after EOI
        t_decay = t[decay_mask] - t_irradiation
        result[decay_mask] = A_eoi * np.exp(-lam * t_decay)
    
    return result.item() if scalar_input else result


def multi_irradiation_activity(
    t: Union[float, np.ndarray],
    half_life_s: float,
    irradiation_schedule: List[Tuple[float, float, float]],
    production_rate: float = 1.0
) -> Union[float, np.ndarray]:
    """
    Calculate activity for complex irradiation schedules (multiple irradiations).
    
    This models:
    1. First irradiation (e.g., 3 seconds)
    2. Cooling period (decay only)
    3. Second irradiation (e.g., 2 hours)
    4. Further cooling/measurement times
    
    Parameters:
        t: Time since start of first irradiation (seconds) - can be array
        half_life_s: Half-life of isotope (seconds)
        irradiation_schedule: List of (start_time, end_time, relative_flux) tuples
            e.g., [(0, 3, 1.0), (3600, 3600+7200, 1.0)] for 3s irrad, 1hr cool, 2hr irrad
        production_rate: Base production rate P = σ*φ*N (atoms/s)
    
    Returns:
        Activity at time t
    """
    if half_life_s <= 0:
        return np.nan if isinstance(t, float) else np.full_like(t, np.nan)
    
    lam = LN2 / half_life_s
    t = np.asarray(t)
    scalar_input = t.ndim == 0
    t = np.atleast_1d(t)
    
    result = np.zeros_like(t, dtype=float)
    
    for i, t_val in enumerate(t):
        A_current = 0.0
        t_prev = 0.0
        
        for (t_start, t_end, rel_flux) in irradiation_schedule:
            P = production_rate * rel_flux
            
            if t_val <= t_start:
                # Before this irradiation - just decay from previous state
                dt = t_val - t_prev
                A_current = A_current * np.exp(-lam * dt)
                break
            
            elif t_val <= t_end:
                # During this irradiation
                # First decay to start of irradiation
                if t_start > t_prev:
                    dt_decay = t_start - t_prev
                    A_current = A_current * np.exp(-lam * dt_decay)
                
                # Then buildup during irradiation
                t_irr = t_val - t_start
                exp_decay = np.exp(-lam * t_irr)
                A_current = A_current * exp_decay + (P / lam) * (1 - exp_decay)
                break
            
            else:
                # After this irradiation
                # Decay to start of irradiation
                if t_start > t_prev:
                    dt_decay = t_start - t_prev
                    A_current = A_current * np.exp(-lam * dt_decay)
                
                # Full irradiation
                t_irr = t_end - t_start
                exp_decay = np.exp(-lam * t_irr)
                A_current = A_current * exp_decay + (P / lam) * (1 - exp_decay)
                
                t_prev = t_end
        
        else:
            # After all irradiations - pure decay
            if t_val > t_prev:
                dt = t_val - t_prev
                A_current = A_current * np.exp(-lam * dt)
        
        result[i] = A_current
    
    return result.item() if scalar_input else result

# ==============================================================================
# DECAY CORRECTIONS
# ==============================================================================
def decay_correct_to_eoi(
    activity_measured: float,
    decay_time_s: float,
    half_life_s: float
) -> float:
    """
    Correct measured activity back to End-Of-Irradiation (EOI).
    
    A_EOI = A_meas / exp(-λ * t_d)
    
    Parameters:
        activity_measured: Activity at time of measurement
        decay_time_s: Time between EOI and measurement (seconds)
        half_life_s: Half-life of isotope (seconds)
    
    Returns:
        Activity at end of irradiation
    """
    if half_life_s <= 0:
        return np.nan
    lam = LN2 / half_life_s
    decay_factor = np.exp(-lam * decay_time_s)
    if decay_factor <= 0:
        return np.nan
    return activity_measured / decay_factor


def calculate_saturation_activity(
    activity_eoi: float,
    irradiation_time_s: float,
    half_life_s: float
) -> float:
    """
    Calculate saturation activity from EOI activity.
    
    A_sat = A_EOI / (1 - exp(-λ * t_i))
    
    Saturation activity is what you'd get with infinite irradiation time.
    
    Parameters:
        activity_eoi: Activity at end of irradiation
        irradiation_time_s: Total irradiation time (seconds)
        half_life_s: Half-life of isotope (seconds)
    
    Returns:
        Saturation activity
    """
    if half_life_s <= 0:
        return np.nan
    lam = LN2 / half_life_s
    saturation_factor = 1 - np.exp(-lam * irradiation_time_s)
    if saturation_factor <= 0:
        return np.nan
    return activity_eoi / saturation_factor


def full_decay_chain(
    activity_measured: float,
    decay_time_s: float,
    irradiation_time_s: float,
    half_life_s: float,
    uncertainty: Optional[float] = None
) -> Dict[str, float]:
    """
    Full decay chain calculation: A_meas -> A_EOI -> A_sat
    
    Returns dict with:
        - activity_eoi: Activity at end of irradiation
        - activity_sat: Saturation activity
        - uncertainty_eoi: Propagated uncertainty at EOI (if provided)
        - uncertainty_sat: Propagated uncertainty at saturation (if provided)
    """
    a_eoi = decay_correct_to_eoi(activity_measured, decay_time_s, half_life_s)
    a_sat = calculate_saturation_activity(a_eoi, irradiation_time_s, half_life_s)
    
    result = {
        'activity_eoi': a_eoi,
        'activity_sat': a_sat,
    }
    
    if uncertainty is not None and not np.isnan(uncertainty):
        # Propagate uncertainty (relative uncertainty is preserved)
        rel_unc = uncertainty / activity_measured if activity_measured > 0 else np.nan
        result['uncertainty_eoi'] = a_eoi * rel_unc
        result['uncertainty_sat'] = a_sat * rel_unc
    else:
        result['uncertainty_eoi'] = np.nan
        result['uncertainty_sat'] = np.nan
    
    return result


# ==============================================================================
# CONVENIENCE FUNCTION: MEASURED ACTIVITY → SATURATION ACTIVITY
# ==============================================================================
def activity_to_asat(
    activity_measured: float,
    half_life_s: float,
    t_irradiation_s: float,
    t_cooling_s: float
) -> float:
    """
    Convert measured activity directly to saturation activity.
    
    This is a convenience wrapper combining decay_correct_to_eoi and
    calculate_saturation_activity.
    
    A_measured = A_sat * (1 - e^(-λ*t_irr)) * e^(-λ*t_cool)
    A_sat = A_measured / [(1 - e^(-λ*t_irr)) * e^(-λ*t_cool)]
    
    Parameters:
        activity_measured: Activity at time of measurement (Bq or any unit)
        half_life_s: Half-life in seconds
        t_irradiation_s: Irradiation time in seconds
        t_cooling_s: Cooling time (time from EOI to measurement) in seconds
    
    Returns:
        Saturation activity (same units as input)
    """
    if half_life_s <= 0 or activity_measured <= 0:
        return 0.0
    
    # Use the existing chain
    a_eoi = decay_correct_to_eoi(activity_measured, t_cooling_s, half_life_s)
    if np.isnan(a_eoi):
        return 0.0
    a_sat = calculate_saturation_activity(a_eoi, t_irradiation_s, half_life_s)
    if np.isnan(a_sat):
        return 0.0
    return a_sat


# ==============================================================================
# UNIT CONVERSIONS
# ==============================================================================
def activity_uci_to_bq(activity_uci: float) -> float:
    """Convert microcuries to Becquerels. 1 µCi = 37,000 Bq."""
    return activity_uci * 37000.0


def activity_bq_to_uci(activity_bq: float) -> float:
    """Convert Becquerels to microcuries. 1 Bq = 1/37000 µCi."""
    return activity_bq / 37000.0


# ==============================================================================
# FLUX CALCULATION
# ==============================================================================
def calculate_flux_from_asat(
    a_sat_bq: float,
    decay_constant: float,
    cross_section_cm2: float,
    n_atoms: float,
    uncertainty_bq: Optional[float] = None
) -> Tuple[float, Optional[float]]:
    """
    Calculate neutron flux from saturation activity.
    
    φ = (A_sat × λ) / (σ × N)
    
    This uses the relationship: A_sat = φ × σ × N / λ
    
    Parameters:
        a_sat_bq: Saturation activity (Bq = decays/s)
        decay_constant: Lambda = ln(2)/T_half (1/s)
        cross_section_cm2: Cross-section in cm²
        n_atoms: Number of target atoms
        uncertainty_bq: Optional uncertainty in A_sat (Bq)
    
    Returns:
        Tuple of (flux, uncertainty) where flux is in n/cm²/s
    """
    denom = cross_section_cm2 * n_atoms
    if denom <= 0:
        return np.nan, np.nan
    
    numerator = a_sat_bq * decay_constant
    phi = numerator / denom
    
    if uncertainty_bq is not None:
        phi_unc = (uncertainty_bq * decay_constant) / denom
        return phi, phi_unc
    
    return phi, None


def calculate_flux_direct(
    activity_measured: float,
    decay_time_s: float,
    irradiation_time_s: float,
    half_life_s: float,
    cross_section_cm2: float,
    mass_g: float,
    atomic_mass: float
) -> float:
    """
    Calculate flux directly from measured activity using full correction chain.
    
    φ = A_meas / [σ × N × (1 - e^(-λ*ti)) × e^(-λ*td)]
    
    Parameters:
        activity_measured: Measured activity (Bq)
        decay_time_s: Decay time since EOI (seconds)
        irradiation_time_s: Irradiation duration (seconds)
        half_life_s: Half-life (seconds)
        cross_section_cm2: Cross-section (cm²)
        mass_g: Target mass (grams)
        atomic_mass: Atomic mass of target (amu ≈ mass number)
    
    Returns:
        Neutron flux (n/cm²/s)
    """
    if half_life_s <= 0 or mass_g <= 0 or cross_section_cm2 <= 0:
        return np.nan
    
    lam = LN2 / half_life_s
    n_atoms = (mass_g / atomic_mass) * AVOGADRO
    
    S = 1 - np.exp(-lam * irradiation_time_s)  # Saturation factor
    D = np.exp(-lam * decay_time_s)            # Decay factor
    
    denom = cross_section_cm2 * n_atoms * S * D
    if denom <= 0:
        return np.nan
    
    return activity_measured / denom


# ==============================================================================
# WEIGHTED AVERAGING
# ==============================================================================
def weighted_average_activity(
    activities: List[float],
    uncertainties: List[float]
) -> Tuple[float, float]:
    """
    Compute weighted average activity from multiple measurements.
    
    Weights are 1/σ² (inverse variance weighting).
    
    A_final = Σ(Aᵢ/σᵢ²) / Σ(1/σᵢ²)
    σ_final = 1 / √(Σ(1/σᵢ²))
    
    Parameters:
        activities: List of activity measurements
        uncertainties: List of corresponding uncertainties
    
    Returns:
        (weighted_average, combined_uncertainty)
    """
    activities = np.array(activities)
    uncertainties = np.array(uncertainties)
    
    # Filter out invalid values
    valid = (uncertainties > 0) & np.isfinite(activities) & np.isfinite(uncertainties)
    if not np.any(valid):
        return np.nan, np.nan
    
    a = activities[valid]
    u = uncertainties[valid]
    
    weights = 1.0 / (u ** 2)
    w_sum = np.sum(weights)
    
    if w_sum <= 0:
        return np.nan, np.nan
    
    weighted_avg = np.sum(a * weights) / w_sum
    combined_unc = 1.0 / np.sqrt(w_sum)
    
    return weighted_avg, combined_unc


# ==============================================================================
# SNR OPTIMIZATION
# ==============================================================================
def calculate_snr_grid(
    target_half_life_s: float,
    target_asat: float,
    mask_half_life_s: float,
    mask_asat: float,
    ti_range: np.ndarray,
    td_range: np.ndarray
) -> np.ndarray:
    """
    Calculate Signal-to-Noise Ratio grid for detecting a target isotope
    against a masking (dominant) isotope.
    
    SNR(ti, td) = [A_sat_target × (1 - e^(-λ_target×ti)) × e^(-λ_target×td)] /
                  [A_sat_mask × (1 - e^(-λ_mask×ti)) × e^(-λ_mask×td)]
    
    Parameters:
        target_half_life_s: Half-life of target isotope (seconds)
        target_asat: Saturation activity of target (arbitrary units)
        mask_half_life_s: Half-life of masking isotope (seconds)
        mask_asat: Saturation activity of masking isotope
        ti_range: Array of irradiation times (seconds)
        td_range: Array of cooling times (seconds)
    
    Returns:
        2D grid of SNR values (shape: len(td_range) x len(ti_range))
    """
    lam_target = LN2 / target_half_life_s
    lam_mask = LN2 / mask_half_life_s
    
    TI, TD = np.meshgrid(ti_range, td_range)
    
    # Target activity at measurement
    A_target = target_asat * (1 - np.exp(-lam_target * TI)) * np.exp(-lam_target * TD)
    
    # Masking activity at measurement
    A_mask = mask_asat * (1 - np.exp(-lam_mask * TI)) * np.exp(-lam_mask * TD)
    
    # Avoid division by zero
    A_mask = np.maximum(A_mask, 1e-30)
    
    return A_target / A_mask


def find_optimal_detection_window(
    target_half_life_s: float,
    target_asat: float,
    mask_half_life_s: float,
    mask_asat: float,
    ti_max_hours: float = 24,
    td_max_days: float = 60,
    n_points: int = 100
) -> Dict[str, float]:
    """
    Find optimal irradiation and cooling times for detecting target vs mask.
    
    Returns dict with:
        - optimal_ti_hours: Optimal irradiation time (hours)
        - optimal_td_days: Optimal cooling time (days)
        - max_snr: Maximum SNR value
        - strategy: Text description of detection strategy
    """
    ti_range = np.linspace(0.1 * 3600, ti_max_hours * 3600, n_points)
    td_range = np.linspace(0.01 * 24 * 3600, td_max_days * 24 * 3600, n_points)
    
    snr_grid = calculate_snr_grid(
        target_half_life_s, target_asat,
        mask_half_life_s, mask_asat,
        ti_range, td_range
    )
    
    max_idx = np.unravel_index(np.nanargmax(snr_grid), snr_grid.shape)
    opt_ti_hours = ti_range[max_idx[1]] / 3600
    opt_td_days = td_range[max_idx[0]] / (24 * 3600)
    max_snr = snr_grid[max_idx]
    
    # Determine strategy
    target_hl_days = target_half_life_s / 86400
    mask_hl_days = mask_half_life_s / 86400
    
    if target_hl_days > mask_hl_days:
        strategy = f"Wait for mask (T½={mask_hl_days:.1f}d) to decay while target persists"
    else:
        strategy = f"Count quickly before target (T½={target_hl_days:.2f}d) decays"
    
    return {
        'optimal_ti_hours': opt_ti_hours,
        'optimal_td_days': opt_td_days,
        'max_snr': max_snr,
        'strategy': strategy
    }


def plot_snr_heatmap(
    ti_range: np.ndarray,
    td_range: np.ndarray,
    snr_grid: np.ndarray,
    target_name: str = "Target",
    mask_name: str = "Mask",
    ti_unit: str = "hours",
    td_unit: str = "days",
    save_path: Optional[str] = None,
    show: bool = True
) -> Optional[plt.Figure]:
    """
    Plot 2D heatmap of SNR as a function of irradiation and cooling time.
    
    Parameters:
        ti_range: Irradiation time array (seconds)
        td_range: Cooling time array (seconds)
        snr_grid: 2D SNR values
        target_name: Name of target isotope for labels
        mask_name: Name of masking isotope for labels
        ti_unit: Display unit for irradiation time
        td_unit: Display unit for cooling time
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    
    Returns:
        matplotlib Figure object (or None if no valid data)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Convert units for display
    ti_display = ti_range / 3600 if ti_unit == "hours" else ti_range
    td_display = td_range / (24 * 3600) if td_unit == "days" else td_range
    
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
    
    plt.colorbar(im, ax=ax, label=f'SNR ({target_name} / {mask_name})')
    
    # Find and mark optimal point
    max_idx = np.unravel_index(np.nanargmax(snr_grid), snr_grid.shape)
    opt_td = td_display[max_idx[0]]
    opt_ti = ti_display[max_idx[1]]
    opt_snr = snr_grid[max_idx]
    
    ax.scatter([opt_ti], [opt_td], color='red', s=200, marker='*',
               edgecolor='white', linewidth=2, zorder=5,
               label=f'Optimal: ti={opt_ti:.1f}{ti_unit[0]}, td={opt_td:.1f}{td_unit[0]}\nSNR={opt_snr:.2e}')
    
    ax.set_xlabel(f'Irradiation Time ({ti_unit})', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'Cooling Time ({td_unit})', fontsize=12, fontweight='bold')
    ax.set_title(f'Detection Window: {target_name} vs {mask_name}', fontsize=14, fontweight='bold')
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
    Plot SNR as line plots (easier to read than heatmaps).
    
    Shows SNR vs cooling time for each target isotope, at a fixed irradiation time.
    This makes it much clearer when detection becomes favorable.
    
    Parameters:
        isotope_data: List of dicts with 'isotope', 'activity', 'half_life_s' keys
        mask_iso: Name of dominant/masking isotope
        mask_hl_s: Half-life of mask isotope (seconds)
        irradiation_time_h: Fixed irradiation time (hours)
        td_max_days: Maximum cooling time to plot (days)
        output_dir: Directory for saving plots
        show: Whether to display the plot
    
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ti_s = irradiation_time_h * 3600
    td_range = np.logspace(-2, np.log10(td_max_days), 200)  # Days
    td_range_s = td_range * 86400  # Convert to seconds
    
    mask_pretty = format_iso_pretty(mask_iso)
    lam_mask = LN2 / mask_hl_s
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(isotope_data)))
    
    # Get mask activity (from isotope_data or estimate)
    mask_act = 1.0
    for d in isotope_data:
        if canonical_iso(d['isotope']) == canonical_iso(mask_iso):
            mask_act = d.get('activity', 1.0)
            break
    
    # Calculate mask activity over time
    S_mask = 1 - np.exp(-lam_mask * ti_s)  # Saturation factor
    A_mask_t = mask_act * S_mask * np.exp(-lam_mask * td_range_s)
    
    for i, data in enumerate(isotope_data):
        iso = data['isotope']
        if canonical_iso(iso) == canonical_iso(mask_iso):
            continue  # Skip plotting mask vs itself
        
        target_act = data.get('activity', 1.0)
        target_hl_s = data.get('half_life_s', get_half_life_seconds(iso))
        
        if target_hl_s is None or target_hl_s <= 0:
            continue
        
        lam_target = LN2 / target_hl_s
        S_target = 1 - np.exp(-lam_target * ti_s)
        
        # Target activity at each cooling time
        A_target_t = target_act * S_target * np.exp(-lam_target * td_range_s)
        
        # SNR = target / mask
        snr = A_target_t / np.maximum(A_mask_t, 1e-30)
        
        target_pretty = format_iso_pretty(iso)
        hl_days = target_hl_s / 86400
        hl_label = f"{hl_days:.1f}d" if hl_days >= 1 else f"{hl_days*24:.1f}h"
        
        # Plot on left axis (log scale)
        ax1.loglog(td_range, snr, linewidth=2, color=colors[i],
                  label=f"{target_pretty} (T½={hl_label})")
        
        # Plot activities on right axis
        ax2.semilogy(td_range, A_target_t, '--', linewidth=1.5, color=colors[i],
                    label=f"{target_pretty}")
    
    # Plot mask activity
    ax2.semilogy(td_range, A_mask_t, 'k-', linewidth=2.5,
                label=f"{mask_pretty} (mask)")
    
    # Left plot: SNR
    ax1.axhline(y=1, color='red', linestyle=':', linewidth=1.5, alpha=0.7, label='SNR = 1')
    ax1.set_xlabel('Cooling Time (days)', fontsize=11)
    ax1.set_ylabel(f'SNR (Target / {mask_pretty})', fontsize=11)
    ax1.set_title(f'SNR vs Cooling Time\n(ti = {irradiation_time_h:.1f} hours)', 
                 fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_xlim(td_range[0], td_range[-1])
    
    # Right plot: Activities
    ax2.set_xlabel('Cooling Time (days)', fontsize=11)
    ax2.set_ylabel('Activity (relative)', fontsize=11)
    ax2.set_title('Activity Decay Curves', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_xlim(0, td_max_days)
    
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


def plot_irradiation_decay_curves(
    isotopes: List[str],
    irradiation_schedule: List[Tuple[float, float, float]],
    total_time_days: float = 30.0,
    title: str = "Irradiation and Decay History",
    save_path: Optional[str] = None,
    show: bool = True,
    log_x: bool = False,
    show_asat: bool = True,
    saturation_activities: Optional[Dict[str, float]] = None,
    experimental_points: Optional[Dict[str, List[Tuple[float, float]]]] = None
) -> Optional[plt.Figure]:
    """
    Plot proper Bateman decay curves showing irradiation buildup and decay.
    
    Parameters:
        isotopes: List of isotope names to plot
        irradiation_schedule: List of (start_s, end_s, relative_flux) tuples
        total_time_days: Total time to plot (days)
        title: Plot title
        save_path: Where to save the figure
        show: Whether to display
        log_x: Use log scale for x-axis
        show_asat: Show A_sat as dotted horizontal lines
        saturation_activities: Dict mapping isotope to A_sat value (if None, uses theoretical)
        experimental_points: Dict mapping isotope to list of (time_s, activity) tuples
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate total irradiation time for schedule info
    total_irr_s = sum(end - start for start, end, _ in irradiation_schedule)
    
    # Time array from 0 to total_time
    t_max_s = total_time_days * 86400
    
    # For log scale, use log-spaced points; for linear use linear spacing
    if log_x:
        # Start from a small positive time for log scale
        t_min = 1.0  # 1 second
        t_array = np.logspace(np.log10(t_min), np.log10(t_max_s), 800)
        # Add key points near irradiations
        for (t_start, t_end, _) in irradiation_schedule:
            t_array = np.concatenate([t_array, 
                np.linspace(max(t_start, 0.1), t_end + 60, 50)])
        t_array = np.unique(np.sort(t_array))
    else:
        # Use more points near irradiations
        t_array = np.concatenate([
            np.linspace(0.1, irradiation_schedule[-1][1] + 3600, 500),
            np.linspace(irradiation_schedule[-1][1] + 3600, t_max_s, 500)
        ])
        t_array = np.unique(np.sort(t_array))
    
    t_days = t_array / 86400
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(isotopes)))
    
    valid_isotopes = []
    for i, iso in enumerate(isotopes):
        hl_s = get_half_life_seconds(iso)
        if hl_s is None or hl_s <= 0:
            continue
        
        # Calculate activity over time (normalized by production rate P)
        A_t = multi_irradiation_activity(t_array, hl_s, irradiation_schedule, production_rate=1.0)
        
        # Calculate saturation activity A_sat = P/λ (theoretical max)
        lam = LN2 / hl_s
        A_sat_theoretical = 1.0 / lam  # For P=1, A_sat = 1/λ
        
        # Use provided A_sat if available, otherwise theoretical
        if saturation_activities and iso in saturation_activities:
            A_sat = saturation_activities[iso]
            # Scale A_t to match provided A_sat
            A_t = A_t * lam  # This gives activity in units where A_sat = provided value
            A_t = A_t * A_sat
        else:
            A_sat = A_sat_theoretical
            # Keep A_t in raw units (P/λ normalized)
        
        hl_days = hl_s / 86400
        hl_label = f"{hl_days:.1f}d" if hl_days >= 1 else f"{hl_days*24:.1f}h" if hl_days*24 >= 1 else f"{hl_days*24*60:.1f}m"
        
        if log_x:
            ax.loglog(t_days, A_t, linewidth=2, color=colors[i],
                     label=f"{format_iso_pretty(iso)} (T½={hl_label})")
        else:
            ax.semilogy(t_days, A_t, linewidth=2, color=colors[i],
                       label=f"{format_iso_pretty(iso)} (T½={hl_label})")
        
        # Add A_sat line if requested
        if show_asat:
            ax.axhline(y=A_sat, color=colors[i], linestyle=':', alpha=0.5, linewidth=1.5)
            # Label A_sat
            ax.text(t_days[-1] * 0.95 if not log_x else t_days[-1] * 0.7, 
                   A_sat * 1.1, f"A_sat", color=colors[i], fontsize=7, alpha=0.7)
        
        # Add experimental points if provided
        if experimental_points and iso in experimental_points:
            exp_pts = experimental_points[iso]
            t_exp = [p[0] / 86400 for p in exp_pts]  # Convert to days
            A_exp = [p[1] for p in exp_pts]
            ax.scatter(t_exp, A_exp, s=100, marker='o', color=colors[i], 
                      edgecolor='black', linewidth=1.5, zorder=5)
        
        valid_isotopes.append(iso)
    
    # Mark irradiation periods
    for j, (t_start, t_end, _) in enumerate(irradiation_schedule):
        ax.axvspan(t_start/86400, t_end/86400, alpha=0.2, color='yellow',
                  label='Irradiation' if j == 0 else None)
        ax.axvline(x=t_end/86400, color='orange', linestyle='--', alpha=0.5, linewidth=1)
    
    ax.set_xlabel('Time since first irradiation (days)', fontsize=11)
    ax.set_ylabel('Activity (normalized or Bq)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3, which='both')
    
    if log_x:
        ax.set_xlim(1e-5, total_time_days)  # Start from ~1 second in days
    else:
        ax.set_xlim(0, total_time_days)
    
    # Add schedule info
    schedule_str = "Irradiation schedule:\n"
    for j, (t_start, t_end, flux) in enumerate(irradiation_schedule):
        duration = t_end - t_start
        if duration < 60:
            dur_str = f"{duration:.0f}s"
        elif duration < 3600:
            dur_str = f"{duration/60:.0f}min"
        else:
            dur_str = f"{duration/3600:.1f}hr"
        schedule_str += f"  {j+1}. t={t_start/3600:.2f}h, dur={dur_str}\n"
    
    ax.text(0.02, 0.02, schedule_str.strip(), transform=ax.transAxes, fontsize=8,
           verticalalignment='bottom', fontfamily='monospace',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
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


def analyze_top_isotopes_snr(
    isotope_activities: Dict[str, float],
    top_n: int = 3,
    output_dir: Optional[str] = None,
    show_plots: bool = True
) -> List[Dict]:
    """
    Analyze SNR optimization for top N isotopes from experimental data.
    
    Parameters:
        isotope_activities: Dict mapping isotope names to activities (Bq)
        top_n: Number of top isotopes to analyze
        output_dir: Directory for saving plots
        show_plots: Whether to display plots
    
    Returns:
        List of analysis results for each isotope pair
    """
    # Sort by activity
    sorted_isos = sorted(isotope_activities.items(), key=lambda x: x[1], reverse=True)
    top_isos = sorted_isos[:top_n]
    
    if len(top_isos) < 2:
        print(f"Need at least 2 isotopes for SNR analysis, got {len(top_isos)}")
        return []
    
    # Dominant isotope is the mask
    mask_iso, mask_act = top_isos[0]
    mask_hl_days = get_half_life_days(mask_iso)
    
    if mask_hl_days is None:
        print(f"Unknown half-life for dominant isotope {mask_iso}")
        return []
    
    mask_hl_s = mask_hl_days * 86400
    
    results = []
    
    for target_iso, target_act in top_isos[1:]:
        target_hl_days = get_half_life_days(target_iso)
        if target_hl_days is None:
            print(f"Unknown half-life for {target_iso}, skipping")
            continue
        
        target_hl_s = target_hl_days * 86400
        
        # Determine time ranges
        max_ti_hours = max(24, min(target_hl_days * 24, 168))
        max_td_days = max(7, min(max(mask_hl_days, target_hl_days) * 3, 180))
        
        ti_range = np.linspace(0.1 * 3600, max_ti_hours * 3600, 100)
        td_range = np.linspace(0.01 * 86400, max_td_days * 86400, 100)
        
        snr_grid = calculate_snr_grid(
            target_hl_s, target_act,
            mask_hl_s, mask_act,
            ti_range, td_range
        )
        
        optimal = find_optimal_detection_window(
            target_hl_s, target_act,
            mask_hl_s, mask_act,
            ti_max_hours=max_ti_hours,
            td_max_days=max_td_days
        )
        
        result = {
            'target': target_iso,
            'mask': mask_iso,
            'target_activity': target_act,
            'mask_activity': mask_act,
            'target_half_life_days': target_hl_days,
            'mask_half_life_days': mask_hl_days,
            **optimal
        }
        results.append(result)
        
        # Generate plot
        if output_dir:
            save_path = Path(output_dir) / f"snr_{target_iso.replace('-','')}_vs_{mask_iso.replace('-','')}.png"
        else:
            save_path = None
        
        target_name = format_iso_pretty(target_iso)
        mask_name = format_iso_pretty(mask_iso)
        
        plot_snr_heatmap(
            ti_range, td_range, snr_grid,
            target_name=target_name,
            mask_name=mask_name,
            save_path=str(save_path) if save_path else None,
            show=show_plots
        )
    
    return results


if __name__ == '__main__':
    # Quick tests
    print("Testing decay_physics...")
    
    # Test decay correction
    a_meas = 1000  # Bq
    t_decay = 86400  # 1 day
    t_irr = 7200    # 2 hours
    hl = 27.7 * 86400  # Cr-51 half-life in seconds
    
    a_eoi = decay_correct_to_eoi(a_meas, t_decay, hl)
    a_sat = calculate_saturation_activity(a_eoi, t_irr, hl)
    print(f"A_meas = {a_meas} Bq")
    print(f"A_EOI = {a_eoi:.2f} Bq")
    print(f"A_sat = {a_sat:.2f} Bq")
    
    # Test weighted average
    activities = [100, 105, 98]
    uncertainties = [5, 8, 4]
    avg, unc = weighted_average_activity(activities, uncertainties)
    print(f"Weighted average: {avg:.2f} ± {unc:.2f}")
    
    # Test SNR optimization
    result = find_optimal_detection_window(
        target_half_life_s=1925.2 * 86400,  # Co-60
        target_asat=100,
        mask_half_life_s=27.7 * 86400,  # Cr-51
        mask_asat=10000
    )
    print(f"Optimal detection: ti={result['optimal_ti_hours']:.1f}h, td={result['optimal_td_days']:.1f}d")
    print(f"Strategy: {result['strategy']}")
    
    print("All tests passed!")
