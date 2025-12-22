#!/usr/bin/env python3
"""
Schedule Optimizer for HPGe Gamma Spectroscopy of Neutron-Activated Samples

This module provides tools for planning irradiation + counting schedules
using ALARA-predicted nuclide activities and background models.

Key capabilities:
- Activity time dependence modeling
- Expected peak counts calculation
- Currie-style detection limits (Lc/Ld)
- Background continuum modeling
- Schedule optimization via grid search

Units convention:
- Time: seconds (internal), with helpers for hours/days
- Energy: keV
- Activity: Bq (decays/s)
- Cross-sections: cm²
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable, Union
from dataclasses import dataclass, field
import warnings

# Add tools directory to path for alara_output_processing imports
_tools_dir = Path(__file__).parent.parent / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

from alara_output_processing import SECONDS_CONV

# Import nuclear data functions (uses paceENSDF when available)
from nuclear_data import (
    get_half_life as nd_get_half_life,
    get_gamma_info as nd_get_gamma_info,
    get_data_source as nd_get_data_source,
)

# ==============================================================================
# CONSTANTS
# ==============================================================================
LN2 = np.log(2)
SECONDS_PER_HOUR = SECONDS_CONV['h']
SECONDS_PER_DAY = SECONDS_CONV['d']
SECONDS_PER_MINUTE = SECONDS_CONV['m']

# Default detection parameters (Currie, 95% confidence)
DEFAULT_ALPHA = 0.05  # Type I error (false positive)
DEFAULT_BETA = 0.05   # Type II error (false negative)
K_ALPHA_95 = 1.645    # z-score for alpha=0.05
K_BETA_95 = 1.645     # z-score for beta=0.05


# ==============================================================================
# TIME UNIT CONVERSIONS
# ==============================================================================
def seconds_to_hours(t_s: float) -> float:
    """Convert seconds to hours."""
    return t_s / SECONDS_PER_HOUR

def hours_to_seconds(t_h: float) -> float:
    """Convert hours to seconds."""
    return t_h * SECONDS_PER_HOUR

def seconds_to_days(t_s: float) -> float:
    """Convert seconds to days."""
    return t_s / SECONDS_PER_DAY

def days_to_seconds(t_d: float) -> float:
    """Convert days to seconds."""
    return t_d * SECONDS_PER_DAY

def parse_time_string(time_str: str) -> float:
    """
    Parse a time string like '2h', '30m', '1d', '300s' to seconds.
    
    Supported units: s, m, h, d (seconds, minutes, hours, days)
    """
    time_str = time_str.strip().lower()
    if time_str.endswith('d'):
        return float(time_str[:-1]) * SECONDS_PER_DAY
    elif time_str.endswith('h'):
        return float(time_str[:-1]) * SECONDS_PER_HOUR
    elif time_str.endswith('m'):
        return float(time_str[:-1]) * SECONDS_PER_MINUTE
    elif time_str.endswith('s'):
        return float(time_str[:-1])
    else:
        return float(time_str)  # Assume seconds


# ==============================================================================
# DECAY PHYSICS
# ==============================================================================
def half_life_to_lambda(T12: float, units: str = 's') -> float:
    """
    Convert half-life to decay constant lambda.
    
    Parameters:
        T12: Half-life value
        units: 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days), 'y' (years)
    
    Returns:
        Decay constant lambda in 1/seconds
    """
    unit_to_seconds = {
        's': 1.0,
        'm': 60.0,
        'h': 3600.0,
        'd': 86400.0,
        'y': 365.25 * 86400.0,
    }
    T12_s = T12 * unit_to_seconds.get(units.lower(), 1.0)
    if T12_s <= 0:
        return 0.0
    return LN2 / T12_s


def lambda_to_half_life(lam: float, units: str = 's') -> float:
    """
    Convert decay constant lambda to half-life.
    
    Parameters:
        lam: Decay constant in 1/seconds
        units: Output unit - 's', 'm', 'h', 'd', 'y'
    
    Returns:
        Half-life in specified units
    """
    if lam <= 0:
        return np.inf
    unit_to_seconds = {
        's': 1.0,
        'm': 60.0,
        'h': 3600.0,
        'd': 86400.0,
        'y': 365.25 * 86400.0,
    }
    T12_s = LN2 / lam
    return T12_s / unit_to_seconds.get(units.lower(), 1.0)


def activity_at_time(A0: float, lam: float, t: float) -> float:
    """
    Calculate activity at time t after reference time.
    
    A(t) = A0 * exp(-lambda * t)
    
    Parameters:
        A0: Activity at t=0 (Bq)
        lam: Decay constant (1/s)
        t: Time since reference (s)
    
    Returns:
        Activity at time t (Bq)
    """
    if lam <= 0 or t < 0:
        return A0
    return A0 * np.exp(-lam * t)


def integrate_activity(A0: float, lam: float, t_c: float) -> float:
    """
    Integrate activity over a counting interval [0, t_c].
    
    ∫_0^{t_c} A0*exp(-λt) dt = A0 * (1 - exp(-λ*t_c)) / λ
    
    Parameters:
        A0: Activity at start of count (Bq)
        lam: Decay constant (1/s)
        t_c: Counting live time (s)
    
    Returns:
        Integrated activity (Bq·s = decays)
    """
    if lam <= 0 or t_c <= 0:
        return A0 * t_c  # Stable isotope approximation
    
    # For numerical stability when λ*t_c is very small
    lam_tc = lam * t_c
    if lam_tc < 1e-6:
        # Taylor expansion: (1 - exp(-x))/x ≈ 1 - x/2 + x²/6
        return A0 * t_c * (1.0 - lam_tc / 2.0 + lam_tc**2 / 6.0)
    
    return A0 * (1.0 - np.exp(-lam_tc)) / lam


def activity_after_irradiation(
    production_rate: float,
    lam: float,
    t_irr: float,
    t_cool: float = 0.0
) -> float:
    """
    Calculate activity after irradiation and optional cooling.
    
    During irradiation: A_EOI = P * (1 - exp(-λ*t_irr)) / λ
    After cooling: A(t_cool) = A_EOI * exp(-λ*t_cool)
    
    Parameters:
        production_rate: Atom production rate (atoms/s) = N*σ*Φ
        lam: Decay constant (1/s)
        t_irr: Irradiation time (s)
        t_cool: Cooling time after EOI (s)
    
    Returns:
        Activity (Bq)
    """
    if lam <= 0:
        # Stable product - accumulates linearly
        return production_rate * t_irr
    
    # Saturation factor
    sat_factor = 1.0 - np.exp(-lam * t_irr)
    A_EOI = production_rate * sat_factor
    
    # Decay during cooling
    if t_cool > 0:
        return A_EOI * np.exp(-lam * t_cool)
    return A_EOI


# ==============================================================================
# PEAK COUNTS CALCULATION
# ==============================================================================
def peak_counts(
    A0_Bq: float,
    I_gamma: float,
    eff: float,
    lam: float,
    t_c: float
) -> float:
    """
    Calculate expected net peak counts for a gamma line during a count.
    
    C_peak = eff * I_gamma * ∫_0^{t_c} A0*exp(-λt) dt
           = eff * I_gamma * A0 * (1 - exp(-λ*t_c)) / λ
    
    Parameters:
        A0_Bq: Activity at count start (Bq)
        I_gamma: Gamma emission probability (photons/decay)
        eff: Full-energy peak efficiency (unitless, 0-1)
        lam: Decay constant (1/s)
        t_c: Counting live time (s)
    
    Returns:
        Expected peak counts
    """
    integrated_decays = integrate_activity(A0_Bq, lam, t_c)
    return eff * I_gamma * integrated_decays


# ==============================================================================
# DETECTOR RESPONSE MODELS
# ==============================================================================
def fwhm_model(E_keV: float, a: float = 0.5, b: float = 0.04) -> float:
    """
    FWHM energy resolution model for HPGe detector.
    
    FWHM(E) = sqrt(a² + b² * E)
    
    Parameters:
        E_keV: Gamma energy (keV)
        a: Electronic noise contribution (keV)
        b: Statistical broadening coefficient (keV^0.5)
    
    Returns:
        FWHM in keV
    """
    return np.sqrt(a**2 + (b**2) * E_keV)


def roi_width_keV(
    E_keV: float,
    fwhm_params: Tuple[float, float] = (0.5, 0.04),
    n_sigma: float = 3.0
) -> float:
    """
    Calculate ROI width based on detector resolution.
    
    ROI width = n_sigma * sigma = n_sigma * FWHM / 2.355
    
    Parameters:
        E_keV: Gamma energy (keV)
        fwhm_params: (a, b) parameters for FWHM model
        n_sigma: Number of sigma for ROI width (default 3)
    
    Returns:
        ROI width in keV
    """
    a, b = fwhm_params
    fwhm = fwhm_model(E_keV, a, b)
    sigma = fwhm / 2.355
    return n_sigma * sigma


def efficiency_polynomial(
    E_keV: float,
    coeffs: List[float],
    log_log: bool = True
) -> float:
    """
    Efficiency calibration using polynomial in log(E).
    
    If log_log:
        ln(eff) = Σ c_i * (ln(E))^i
    Else:
        eff = Σ c_i * E^i
    
    Parameters:
        E_keV: Gamma energy (keV)
        coeffs: Polynomial coefficients [c0, c1, c2, ...]
        log_log: If True, use log-log polynomial (typical for HPGe)
    
    Returns:
        Efficiency (unitless)
    """
    if log_log:
        ln_E = np.log(E_keV)
        ln_eff = sum(c * ln_E**i for i, c in enumerate(coeffs))
        return np.exp(ln_eff)
    else:
        return sum(c * E_keV**i for i, c in enumerate(coeffs))


def make_efficiency_function(
    coeffs: List[float],
    log_log: bool = True
) -> Callable[[float], float]:
    """
    Create an efficiency function from polynomial coefficients.
    
    Parameters:
        coeffs: Polynomial coefficients
        log_log: If True, use log-log polynomial
    
    Returns:
        Function eff(E_keV) -> efficiency
    """
    def eff_func(E_keV: float) -> float:
        return efficiency_polynomial(E_keV, coeffs, log_log)
    return eff_func


# ==============================================================================
# BACKGROUND MODELS
# ==============================================================================
@dataclass
class BackgroundModel:
    """
    Background model for HPGe spectra.
    
    Supports:
    - Constant environmental background template
    - Time-dependent Compton continuum from masking nuclides
    """
    # Environmental background rate (counts/s/keV) vs energy
    env_background: Optional[Callable[[float], float]] = None
    
    # Compton template for each masking nuclide: {nuclide: (E -> counts/s/keV)}
    compton_templates: Dict[str, Callable[[float], float]] = field(default_factory=dict)
    
    # Reference activities for Compton templates (Bq)
    compton_ref_activities: Dict[str, float] = field(default_factory=dict)
    
    def get_background_rate(
        self,
        E_keV: float,
        current_activities: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Get background rate at energy E (counts/s/keV).
        
        Parameters:
            E_keV: Energy (keV)
            current_activities: Current activities of masking nuclides (Bq)
        
        Returns:
            Background rate (counts/s/keV)
        """
        rate = 0.0
        
        # Environmental background
        if self.env_background is not None:
            rate += self.env_background(E_keV)
        
        # Scaled Compton from masking nuclides
        if current_activities is not None:
            for nuclide, template in self.compton_templates.items():
                if nuclide in current_activities and nuclide in self.compton_ref_activities:
                    ref_act = self.compton_ref_activities[nuclide]
                    if ref_act > 0:
                        scale = current_activities[nuclide] / ref_act
                        rate += scale * template(E_keV)
        
        return rate


def simple_continuum_model(E_keV: float, A: float = 1e-3, B: float = 2.0) -> float:
    """
    Simple power-law continuum model.
    
    b(E) = A * E^(-B)
    
    Parameters:
        E_keV: Energy (keV)
        A: Amplitude (counts/s/keV at 1 keV)
        B: Power law exponent
    
    Returns:
        Continuum rate (counts/s/keV)
    """
    return A * E_keV**(-B)


def exponential_continuum_model(
    E_keV: float,
    A: float = 0.1,
    E0: float = 500.0
) -> float:
    """
    Exponential continuum model.
    
    b(E) = A * exp(-E / E0)
    
    Parameters:
        E_keV: Energy (keV)
        A: Amplitude (counts/s/keV at E=0)
        E0: Characteristic energy (keV)
    
    Returns:
        Continuum rate (counts/s/keV)
    """
    return A * np.exp(-E_keV / E0)


def background_counts(
    E_keV: float,
    w_keV: float,
    t_c: float,
    background_model: BackgroundModel,
    current_activities: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate expected background counts in ROI.
    
    B = b_rate(E) * w_keV * t_c
    
    Parameters:
        E_keV: Peak energy (keV)
        w_keV: ROI width (keV)
        t_c: Counting time (s)
        background_model: BackgroundModel instance
        current_activities: Current activities of masking nuclides (Bq)
    
    Returns:
        Expected background counts in ROI
    """
    b_rate = background_model.get_background_rate(E_keV, current_activities)
    return b_rate * w_keV * t_c


# ==============================================================================
# DETECTION STATISTICS
# ==============================================================================
def z_score(N: float, B: float) -> float:
    """
    Simple detectability metric (Poisson-limited).
    
    Z = N / sqrt(N + B)
    
    Parameters:
        N: Expected net peak counts
        B: Expected background counts
    
    Returns:
        Z-score (dimensionless)
    """
    total = N + B
    if total <= 0:
        return 0.0
    return N / np.sqrt(total)


def currie_Lc_Ld(
    B: float,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA
) -> Tuple[float, float]:
    """
    Calculate Currie decision level (Lc) and detection limit (Ld).
    
    Lc = k_alpha * sqrt(B)
    Ld = k_alpha² + 2*Lc  (simplified approximation)
    
    More precisely, Ld solves: Ld = Lc + k_beta * sqrt(B + Ld)
    
    Parameters:
        B: Expected background counts
        alpha: Type I error rate (false positive)
        beta: Type II error rate (false negative)
    
    Returns:
        (Lc, Ld) - decision level and detection limit in counts
    """
    from scipy.stats import norm
    k_alpha = norm.ppf(1 - alpha)
    k_beta = norm.ppf(1 - beta)
    
    # Decision level
    Lc = k_alpha * np.sqrt(B)
    
    # Detection limit (iterative solution)
    # Ld = Lc + k_beta * sqrt(B + Ld)
    # Rearrange: Ld - k_beta*sqrt(B + Ld) = Lc
    # Use Newton-Raphson or closed-form approximation
    
    # Closed-form approximation (valid for B not too small):
    # Ld ≈ k_alpha² + 2*Lc when k_alpha = k_beta
    if abs(k_alpha - k_beta) < 0.01:
        Ld = k_alpha**2 + 2 * Lc
    else:
        # Iterative solution
        Ld = Lc + k_beta * np.sqrt(B)  # Initial guess
        for _ in range(20):
            Ld_new = Lc + k_beta * np.sqrt(B + Ld)
            if abs(Ld_new - Ld) < 1e-6:
                break
            Ld = Ld_new
    
    return Lc, Ld


def mda_from_Ld(
    Ld: float,
    eff: float,
    I_gamma: float,
    lam: float,
    t_c: float
) -> float:
    """
    Convert detection limit (counts) to MDA (Bq at count start).
    
    MDA = Ld * λ / (eff * I_gamma * (1 - exp(-λ*t_c)))
    
    Parameters:
        Ld: Detection limit (counts)
        eff: Full-energy peak efficiency
        I_gamma: Gamma emission probability
        lam: Decay constant (1/s)
        t_c: Counting time (s)
    
    Returns:
        Minimum Detectable Activity (Bq)
    """
    if eff <= 0 or I_gamma <= 0:
        return np.inf
    
    # Decay correction factor
    lam_tc = lam * t_c
    if lam_tc < 1e-6:
        decay_factor = t_c
    else:
        decay_factor = (1.0 - np.exp(-lam_tc)) / lam
    
    if decay_factor <= 0:
        return np.inf
    
    return Ld / (eff * I_gamma * decay_factor)


def relative_uncertainty(N: float, B: float) -> float:
    """
    Calculate relative uncertainty of net counts.
    
    sigma_N = sqrt(N + B)
    rel_unc = sigma_N / N
    
    Parameters:
        N: Expected net peak counts
        B: Expected background counts
    
    Returns:
        Relative uncertainty (dimensionless)
    """
    if N <= 0:
        return np.inf
    sigma = np.sqrt(N + B)
    return sigma / N


# ==============================================================================
# GAMMA LINE DATABASE
# ==============================================================================
@dataclass
class GammaLine:
    """A single gamma line for detection planning."""
    nuclide: str          # e.g., 'Co-60'
    energy_keV: float     # Gamma energy
    I_gamma: float        # Emission probability (0-1)
    half_life_s: float    # Half-life in seconds
    is_target: bool = True    # Target line (vs masking)
    weight: float = 1.0       # Weight in score function
    notes: str = ""
    
    @property
    def lam(self) -> float:
        """Decay constant (1/s)."""
        return half_life_to_lambda(self.half_life_s, 's')


def create_gamma_line_table(use_ensdf: bool = True) -> pd.DataFrame:
    """
    Create gamma line database for common activation products.
    
    Uses paceENSDF data when available (via nuclear_data module).
    Falls back to built-in values when paceENSDF is not installed.
    
    Parameters:
        use_ensdf: If True, try to use paceENSDF data first
    
    Returns DataFrame with columns:
        nuclide, energy_keV, I_gamma, half_life_s, half_life_str, is_target, weight
    """
    # Define isotopes of interest with their properties
    # (nuclide, default_energy, default_I, default_t12_s, type, weight, default_t12_str)
    isotope_defs = [
        # Short-lived (good for short irradiations)
        ('V-52', 1434.1, 0.999, 224.58, 'target', 1.0, '3.74 min'),
        ('Mn-56', 846.8, 0.989, 9284.0, 'target', 1.0, '2.58 h'),
        ('Mn-56', 1810.7, 0.272, 9284.0, 'target', 0.5, '2.58 h'),
        ('Al-28', 1778.9, 1.0, 134.5, 'target', 1.0, '2.24 min'),
        
        # Medium-lived
        ('W-187', 685.7, 0.273, 86220.0, 'target', 1.0, '23.9 h'),
        ('W-187', 479.5, 0.218, 86220.0, 'target', 0.8, '23.9 h'),
        ('Na-24', 1368.6, 1.0, 53820.0, 'target', 1.0, '14.95 h'),
        ('Na-24', 2754.0, 0.999, 53820.0, 'target', 0.8, '14.95 h'),
        ('Cu-64', 511.0, 0.352, 45720.0, 'target', 0.5, '12.7 h'),
        
        # Long-lived (need long irradiation)
        ('Cr-51', 320.1, 0.0991, 2393280.0, 'target', 1.0, '27.7 d'),
        ('Fe-59', 1099.2, 0.565, 3844800.0, 'target', 1.0, '44.5 d'),
        ('Fe-59', 1291.6, 0.432, 3844800.0, 'target', 0.8, '44.5 d'),
        ('Co-60', 1173.2, 0.9985, 166344000.0, 'target', 1.0, '5.27 y'),
        ('Co-60', 1332.5, 0.9998, 166344000.0, 'target', 0.9, '5.27 y'),
        ('Ta-182', 1121.3, 0.352, 9913536.0, 'target', 1.0, '114.7 d'),
        ('Ta-182', 1221.4, 0.270, 9913536.0, 'target', 0.8, '114.7 d'),
        ('Mn-54', 834.8, 0.9998, 26974080.0, 'target', 1.0, '312.2 d'),
        ('Zn-65', 1115.5, 0.502, 21075552.0, 'target', 0.8, '243.9 d'),
        
        # Potential masking nuclides (high activity, strong lines)
        ('Sc-46', 889.3, 0.9998, 7239456.0, 'masking', 0.0, '83.8 d'),
        ('Sc-46', 1120.5, 0.9999, 7239456.0, 'masking', 0.0, '83.8 d'),
    ]
    
    lines = []
    for (nuclide, def_E, def_I, def_t12, line_type, weight, def_t12_str) in isotope_defs:
        E_keV = def_E
        I_gamma = def_I
        t12_s = def_t12
        t12_str = def_t12_str
        
        # Try to get data from paceENSDF via nuclear_data
        if use_ensdf:
            nd_t12 = nd_get_half_life(nuclide)
            if nd_t12 is not None:
                t12_s = nd_t12
                # Generate human-readable half-life string
                if t12_s < 60:
                    t12_str = f"{t12_s:.2f} s"
                elif t12_s < 3600:
                    t12_str = f"{t12_s/60:.2f} min"
                elif t12_s < 86400:
                    t12_str = f"{t12_s/3600:.2f} h"
                elif t12_s < 31536000:
                    t12_str = f"{t12_s/86400:.2f} d"
                else:
                    t12_str = f"{t12_s/31536000:.2f} y"
            
            nd_gamma = nd_get_gamma_info(nuclide)
            if nd_gamma is not None:
                gammas = nd_gamma.get('gammas', [])
                # Try to find matching gamma line or use primary
                for g_E, g_I in gammas:
                    if abs(g_E - def_E) < 2.0:  # Within 2 keV
                        E_keV = g_E
                        I_gamma = g_I
                        break
        
        lines.append((nuclide, E_keV, I_gamma, t12_s, line_type, weight, t12_str))
    
    df = pd.DataFrame(lines, columns=[
        'nuclide', 'energy_keV', 'I_gamma', 'half_life_s', 'type', 'weight', 'half_life_str'
    ])
    df['is_target'] = df['type'] == 'target'
    df['lam'] = LN2 / df['half_life_s']
    
    return df


# ==============================================================================
# ACTIVITY INTERPOLATION FROM ALARA DATA
# ==============================================================================
class ActivityInterpolator:
    """
    Interpolate activity vs time from ALARA results.
    
    ALARA typically provides activity at discrete cooling times.
    This class enables interpolation to arbitrary times.
    """
    
    def __init__(
        self,
        times_s: np.ndarray,
        activities: Dict[str, np.ndarray]
    ):
        """
        Initialize interpolator.
        
        Parameters:
            times_s: Array of times after EOI (seconds)
            activities: Dict of {nuclide: activity_array} (Bq)
        """
        self.times_s = np.asarray(times_s)
        self.activities = activities
        self._decay_constants: Dict[str, float] = {}
    
    def set_decay_constant(self, nuclide: str, lam: float):
        """Set decay constant for a nuclide (for extrapolation)."""
        self._decay_constants[nuclide] = lam
    
    def get_activity(
        self,
        nuclide: str,
        t_s: float,
        extrapolate: bool = True
    ) -> float:
        """
        Get activity at time t.
        
        Parameters:
            nuclide: Nuclide name
            t_s: Time after EOI (seconds)
            extrapolate: If True, use decay extrapolation beyond data range
        
        Returns:
            Activity (Bq)
        """
        if nuclide not in self.activities:
            return 0.0
        
        act_array = self.activities[nuclide]
        
        # Interpolation
        if t_s <= self.times_s[0]:
            return act_array[0]
        elif t_s >= self.times_s[-1]:
            if extrapolate and nuclide in self._decay_constants:
                # Exponential decay extrapolation
                lam = self._decay_constants[nuclide]
                dt = t_s - self.times_s[-1]
                return act_array[-1] * np.exp(-lam * dt)
            else:
                return act_array[-1]
        else:
            return np.interp(t_s, self.times_s, act_array)
    
    def get_activities_dict(
        self,
        t_s: float,
        nuclides: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Get activities of multiple nuclides at time t.
        
        Parameters:
            t_s: Time after EOI (seconds)
            nuclides: List of nuclides (or all if None)
        
        Returns:
            Dict of {nuclide: activity_Bq}
        """
        if nuclides is None:
            nuclides = list(self.activities.keys())
        return {nuc: self.get_activity(nuc, t_s) for nuc in nuclides}


# ==============================================================================
# SCHEDULE SIMULATION
# ==============================================================================
@dataclass
class CountMetrics:
    """Metrics for a single gamma line count."""
    nuclide: str
    energy_keV: float
    activity_Bq: float      # Activity at count start
    expected_counts: float  # Net peak counts
    background_counts: float
    z_score: float
    Lc: float
    Ld: float
    mda_Bq: float
    rel_uncertainty: float
    detected: bool          # N > Ld
    quantifiable: bool      # rel_unc < threshold


@dataclass 
class Schedule:
    """
    Irradiation and counting schedule definition.
    
    Timeline:
    - Irradiation 1: t=0 to t=t_i1
    - Delay 1: t=t_i1 to t=t_i1+t_d1
    - Count 1: t=t_i1+t_d1 to t=t_i1+t_d1+t_c1
    - (optional) Irradiation 2, Delay 2, Count 2
    """
    # First cycle
    t_i1: float  # Irradiation time 1 (s)
    t_d1: float  # Delay before count 1 (s)
    t_c1: float  # Counting time 1 (s)
    
    # Second cycle (optional)
    t_i2: float = 0.0  # Irradiation time 2 (s)
    t_d2: float = 0.0  # Delay before count 2 (s)
    t_c2: float = 0.0  # Counting time 2 (s)
    
    # Time between cycles
    t_gap: float = 0.0  # Gap between end of count 1 and start of irrad 2
    
    @property
    def total_time(self) -> float:
        """Total schedule duration (s)."""
        cycle1 = self.t_i1 + self.t_d1 + self.t_c1
        if self.t_i2 > 0:
            cycle2 = self.t_gap + self.t_i2 + self.t_d2 + self.t_c2
            return cycle1 + cycle2
        return cycle1
    
    @property
    def count1_start(self) -> float:
        """Time of count 1 start after EOI-1 (s)."""
        return self.t_d1
    
    @property
    def count2_start_after_EOI2(self) -> float:
        """Time of count 2 start after EOI-2 (s)."""
        return self.t_d2
    
    def __str__(self) -> str:
        h = lambda s: f"{s/3600:.2f}h"
        s = f"Cycle1: irrad={h(self.t_i1)}, delay={h(self.t_d1)}, count={h(self.t_c1)}"
        if self.t_i2 > 0:
            s += f"\nCycle2: irrad={h(self.t_i2)}, delay={h(self.t_d2)}, count={h(self.t_c2)}"
        return s


def simulate_count_for_line(
    line: GammaLine,
    activity_at_count_start: float,
    t_c: float,
    eff_func: Callable[[float], float],
    background_model: BackgroundModel,
    fwhm_params: Tuple[float, float] = (0.5, 0.04),
    current_activities: Optional[Dict[str, float]] = None,
    quantification_threshold: float = 0.10
) -> CountMetrics:
    """
    Simulate counting for a single gamma line.
    
    Parameters:
        line: GammaLine object
        activity_at_count_start: Activity (Bq) at start of count
        t_c: Counting live time (s)
        eff_func: Efficiency function eff(E_keV)
        background_model: BackgroundModel instance
        fwhm_params: FWHM model parameters
        current_activities: Activities of masking nuclides for background
        quantification_threshold: Relative uncertainty threshold for quantification
    
    Returns:
        CountMetrics object
    """
    E = line.energy_keV
    eff = eff_func(E)
    w = roi_width_keV(E, fwhm_params)
    
    # Expected counts
    N = peak_counts(activity_at_count_start, line.I_gamma, eff, line.lam, t_c)
    B = background_counts(E, w, t_c, background_model, current_activities)
    
    # Detection metrics
    Z = z_score(N, B)
    Lc, Ld = currie_Lc_Ld(B)
    MDA = mda_from_Ld(Ld, eff, line.I_gamma, line.lam, t_c)
    rel_unc = relative_uncertainty(N, B)
    
    return CountMetrics(
        nuclide=line.nuclide,
        energy_keV=E,
        activity_Bq=activity_at_count_start,
        expected_counts=N,
        background_counts=B,
        z_score=Z,
        Lc=Lc,
        Ld=Ld,
        mda_Bq=MDA,
        rel_uncertainty=rel_unc,
        detected=(N > Ld),
        quantifiable=(rel_unc < quantification_threshold)
    )


def simulate_schedule(
    schedule: Schedule,
    gamma_lines: List[GammaLine],
    activity_interpolator: ActivityInterpolator,
    eff_func: Callable[[float], float],
    background_model: BackgroundModel,
    fwhm_params: Tuple[float, float] = (0.5, 0.04),
    masking_nuclides: Optional[List[str]] = None
) -> Dict[str, List[CountMetrics]]:
    """
    Simulate a full schedule for all gamma lines.
    
    Parameters:
        schedule: Schedule object
        gamma_lines: List of GammaLine objects
        activity_interpolator: ActivityInterpolator for ALARA data
        eff_func: Efficiency function
        background_model: BackgroundModel instance
        fwhm_params: FWHM model parameters
        masking_nuclides: List of masking nuclide names
    
    Returns:
        Dict with keys 'cycle1', 'cycle2' containing lists of CountMetrics
    """
    results = {'cycle1': [], 'cycle2': []}
    
    # Cycle 1
    t_count1_start = schedule.count1_start  # Time after EOI-1
    
    for line in gamma_lines:
        A0 = activity_interpolator.get_activity(line.nuclide, t_count1_start)
        
        # Get masking activities for background
        mask_acts = None
        if masking_nuclides:
            mask_acts = activity_interpolator.get_activities_dict(
                t_count1_start, masking_nuclides
            )
        
        metrics = simulate_count_for_line(
            line, A0, schedule.t_c1, eff_func, background_model,
            fwhm_params, mask_acts
        )
        results['cycle1'].append(metrics)
    
    # Cycle 2 (if present)
    if schedule.t_i2 > 0 and schedule.t_c2 > 0:
        t_count2_start = schedule.count2_start_after_EOI2
        
        for line in gamma_lines:
            A0 = activity_interpolator.get_activity(line.nuclide, t_count2_start)
            
            mask_acts = None
            if masking_nuclides:
                mask_acts = activity_interpolator.get_activities_dict(
                    t_count2_start, masking_nuclides
                )
            
            metrics = simulate_count_for_line(
                line, A0, schedule.t_c2, eff_func, background_model,
                fwhm_params, mask_acts
            )
            results['cycle2'].append(metrics)
    
    return results


# ==============================================================================
# SCORING FUNCTION
# ==============================================================================
def compute_schedule_score(
    metrics: Dict[str, List[CountMetrics]],
    gamma_lines: List[GammaLine],
    z_goal: float = 5.0,
    detection_weight: float = 1.0,
    quantification_weight: float = 0.5
) -> Tuple[float, Dict]:
    """
    Compute overall score for a schedule.
    
    Score = Σ (line_weight * min(Z/Z_goal, 1.0)) * detection_bonus * quant_bonus
    
    Parameters:
        metrics: Output from simulate_schedule
        gamma_lines: List of GammaLine objects
        z_goal: Target Z-score for full credit
        detection_weight: Bonus multiplier for detected lines
        quantification_weight: Bonus multiplier for quantifiable lines
    
    Returns:
        (total_score, breakdown_dict)
    """
    total_score = 0.0
    breakdown = {'per_line': [], 'n_detected': 0, 'n_quantifiable': 0}
    
    # Combine metrics from both cycles (take best for each line)
    line_best = {}
    for cycle, cycle_metrics in metrics.items():
        for m in cycle_metrics:
            key = (m.nuclide, m.energy_keV)
            if key not in line_best or m.z_score > line_best[key].z_score:
                line_best[key] = m
    
    # Score each target line
    for line in gamma_lines:
        if not line.is_target:
            continue
        
        key = (line.nuclide, line.energy_keV)
        if key not in line_best:
            continue
        
        m = line_best[key]
        
        # Base score from Z-score
        z_factor = min(m.z_score / z_goal, 1.0) if z_goal > 0 else 0.0
        
        # Bonuses
        det_bonus = 1.0 + detection_weight if m.detected else 1.0
        quant_bonus = 1.0 + quantification_weight if m.quantifiable else 1.0
        
        line_score = line.weight * z_factor * det_bonus * quant_bonus
        total_score += line_score
        
        breakdown['per_line'].append({
            'nuclide': line.nuclide,
            'energy_keV': line.energy_keV,
            'z_score': m.z_score,
            'detected': m.detected,
            'quantifiable': m.quantifiable,
            'line_score': line_score
        })
        
        if m.detected:
            breakdown['n_detected'] += 1
        if m.quantifiable:
            breakdown['n_quantifiable'] += 1
    
    n_targets = sum(1 for line in gamma_lines if line.is_target)
    breakdown['n_targets'] = n_targets
    breakdown['total_score'] = total_score
    
    return total_score, breakdown


# ==============================================================================
# GRID SEARCH OPTIMIZATION
# ==============================================================================
@dataclass
class ScheduleResult:
    """Result from schedule optimization."""
    schedule: Schedule
    score: float
    breakdown: Dict
    metrics: Dict[str, List[CountMetrics]]
    rank: int = 0


def grid_search_schedules(
    t_i1_list: List[float],
    t_d1_list: List[float],
    t_c1_list: List[float],
    gamma_lines: List[GammaLine],
    activity_interpolator: ActivityInterpolator,
    eff_func: Callable[[float], float],
    background_model: BackgroundModel,
    t_i2_list: Optional[List[float]] = None,
    t_d2_list: Optional[List[float]] = None,
    t_c2_list: Optional[List[float]] = None,
    max_total_time: Optional[float] = None,
    fwhm_params: Tuple[float, float] = (0.5, 0.04),
    masking_nuclides: Optional[List[str]] = None,
    z_goal: float = 5.0,
    top_n: int = 10,
    verbose: bool = True
) -> List[ScheduleResult]:
    """
    Grid search over schedule parameters.
    
    Parameters:
        t_i1_list: List of irradiation times for cycle 1 (s)
        t_d1_list: List of delay times for cycle 1 (s)
        t_c1_list: List of counting times for cycle 1 (s)
        gamma_lines: List of GammaLine objects
        activity_interpolator: ActivityInterpolator instance
        eff_func: Efficiency function
        background_model: BackgroundModel instance
        t_i2_list: Optional list of irradiation times for cycle 2
        t_d2_list: Optional list of delay times for cycle 2
        t_c2_list: Optional list of counting times for cycle 2
        max_total_time: Maximum total schedule time (s)
        fwhm_params: FWHM model parameters
        masking_nuclides: List of masking nuclide names
        z_goal: Target Z-score
        top_n: Number of top schedules to return
        verbose: Print progress
    
    Returns:
        List of top ScheduleResult objects, sorted by score (descending)
    """
    results = []
    
    # Single cycle if no cycle 2 parameters
    if t_i2_list is None:
        t_i2_list = [0.0]
    if t_d2_list is None:
        t_d2_list = [0.0]
    if t_c2_list is None:
        t_c2_list = [0.0]
    
    total_combinations = (
        len(t_i1_list) * len(t_d1_list) * len(t_c1_list) *
        len(t_i2_list) * len(t_d2_list) * len(t_c2_list)
    )
    
    if verbose:
        print(f"Grid search: {total_combinations} combinations")
    
    count = 0
    for t_i1 in t_i1_list:
        for t_d1 in t_d1_list:
            for t_c1 in t_c1_list:
                for t_i2 in t_i2_list:
                    for t_d2 in t_d2_list:
                        for t_c2 in t_c2_list:
                            count += 1
                            
                            schedule = Schedule(
                                t_i1=t_i1, t_d1=t_d1, t_c1=t_c1,
                                t_i2=t_i2, t_d2=t_d2, t_c2=t_c2
                            )
                            
                            # Check time constraint
                            if max_total_time and schedule.total_time > max_total_time:
                                continue
                            
                            # Simulate
                            metrics = simulate_schedule(
                                schedule, gamma_lines, activity_interpolator,
                                eff_func, background_model, fwhm_params,
                                masking_nuclides
                            )
                            
                            # Score
                            score, breakdown = compute_schedule_score(
                                metrics, gamma_lines, z_goal
                            )
                            
                            results.append(ScheduleResult(
                                schedule=schedule,
                                score=score,
                                breakdown=breakdown,
                                metrics=metrics
                            ))
    
    # Sort by score (descending)
    results.sort(key=lambda x: x.score, reverse=True)
    
    # Assign ranks
    for i, r in enumerate(results):
        r.rank = i + 1
    
    if verbose:
        print(f"Evaluated {len(results)} valid schedules")
    
    return results[:top_n]


# ==============================================================================
# RESULTS DISPLAY
# ==============================================================================
def format_schedule_results(
    results: List[ScheduleResult],
    time_unit: str = 'h'
) -> pd.DataFrame:
    """
    Format schedule results as a DataFrame.
    
    Parameters:
        results: List of ScheduleResult objects
        time_unit: 'h' for hours, 'd' for days, 's' for seconds
    
    Returns:
        DataFrame with schedule parameters and scores
    """
    if time_unit == 'h':
        factor = 1/3600
        suffix = 'h'
    elif time_unit == 'd':
        factor = 1/86400
        suffix = 'd'
    else:
        factor = 1
        suffix = 's'
    
    rows = []
    for r in results:
        s = r.schedule
        row = {
            'rank': r.rank,
            f't_i1 ({suffix})': s.t_i1 * factor,
            f't_d1 ({suffix})': s.t_d1 * factor,
            f't_c1 ({suffix})': s.t_c1 * factor,
            f't_i2 ({suffix})': s.t_i2 * factor,
            f't_d2 ({suffix})': s.t_d2 * factor,
            f't_c2 ({suffix})': s.t_c2 * factor,
            f'total ({suffix})': s.total_time * factor,
            'score': r.score,
            'detected': r.breakdown['n_detected'],
            'quantifiable': r.breakdown['n_quantifiable'],
            'n_targets': r.breakdown['n_targets']
        }
        rows.append(row)
    
    return pd.DataFrame(rows)


def print_detailed_metrics(
    result: ScheduleResult,
    cycle: str = 'cycle1'
) -> None:
    """Print detailed metrics for a schedule result."""
    print(f"\n{'='*70}")
    print(f"SCHEDULE RANK #{result.rank} (Score: {result.score:.2f})")
    print(f"{'='*70}")
    print(result.schedule)
    print(f"\n{cycle.upper()} Metrics:")
    print(f"{'Nuclide':<12} {'E (keV)':<10} {'Activity':<12} {'Counts':<10} "
          f"{'Bkg':<10} {'Z':<8} {'MDA':<12} {'Det':<5} {'Quant':<5}")
    print("-" * 90)
    
    for m in result.metrics.get(cycle, []):
        det_str = "✓" if m.detected else "✗"
        quant_str = "✓" if m.quantifiable else "✗"
        print(f"{m.nuclide:<12} {m.energy_keV:<10.1f} {m.activity_Bq:<12.2e} "
              f"{m.expected_counts:<10.1f} {m.background_counts:<10.1f} "
              f"{m.z_score:<8.2f} {m.mda_Bq:<12.2e} {det_str:<5} {quant_str:<5}")


# ==============================================================================
# SYNTHETIC EXAMPLE DATA
# ==============================================================================
def create_synthetic_alara_data(
    nuclides: List[str],
    half_lives: Dict[str, float],
    eoi_activities: Dict[str, float],
    times_after_eoi: np.ndarray
) -> ActivityInterpolator:
    """
    Create synthetic ALARA-like data for testing.
    
    Parameters:
        nuclides: List of nuclide names
        half_lives: Dict of {nuclide: half_life_s}
        eoi_activities: Dict of {nuclide: activity_Bq_at_EOI}
        times_after_eoi: Array of times (s)
    
    Returns:
        ActivityInterpolator instance
    """
    activities = {}
    for nuc in nuclides:
        A0 = eoi_activities.get(nuc, 0.0)
        T12 = half_lives.get(nuc, 1e20)
        lam = LN2 / T12 if T12 > 0 else 0.0
        activities[nuc] = A0 * np.exp(-lam * times_after_eoi)
    
    interp = ActivityInterpolator(times_after_eoi, activities)
    
    # Set decay constants for extrapolation
    for nuc, T12 in half_lives.items():
        if T12 > 0:
            interp.set_decay_constant(nuc, LN2 / T12)
    
    return interp


def run_example():
    """Run a complete example demonstration."""
    print("=" * 70)
    print("SCHEDULE OPTIMIZER - EXAMPLE DEMONSTRATION")
    print("=" * 70)
    
    # 1. Create gamma line database
    print("\n1. Creating gamma line database...")
    line_data = [
        GammaLine('V-52', 1434.1, 0.999, 224.58, True, 1.0),
        GammaLine('Mn-56', 846.8, 0.989, 9284.0, True, 1.0),
        GammaLine('W-187', 685.7, 0.273, 86220.0, True, 1.0),
        GammaLine('Cr-51', 320.1, 0.0991, 2393280.0, True, 1.0),
        GammaLine('Ta-182', 1121.3, 0.352, 9913536.0, True, 0.8),
        GammaLine('Fe-59', 1099.2, 0.565, 3844800.0, True, 0.7),
    ]
    print(f"   Loaded {len(line_data)} gamma lines")
    
    # 2. Create synthetic ALARA data
    print("\n2. Creating synthetic ALARA activity data...")
    nuclides = [l.nuclide for l in line_data]
    half_lives = {l.nuclide: l.half_life_s for l in line_data}
    
    # Typical EOI activities (Bq) for ~1g sample, 1e13 n/cm²/s flux
    eoi_activities = {
        'V-52': 1e8,    # Short-lived, high activity
        'Mn-56': 5e6,
        'W-187': 3e5,
        'Cr-51': 2e4,
        'Ta-182': 1e4,
        'Fe-59': 5e3,
    }
    
    times = np.linspace(0, 30*86400, 1000)  # 0 to 30 days
    interp = create_synthetic_alara_data(nuclides, half_lives, eoi_activities, times)
    print(f"   Created interpolator for {len(nuclides)} nuclides, 0-30 days")
    
    # 3. Create efficiency function (typical HPGe)
    print("\n3. Creating efficiency calibration...")
    # Log-log polynomial: ln(eff) = c0 + c1*ln(E) + c2*ln(E)² + ...
    eff_coeffs = [-3.0, -0.8, 0.05]  # Example coefficients
    eff_func = make_efficiency_function(eff_coeffs, log_log=True)
    print(f"   eff(100 keV) = {eff_func(100):.4f}")
    print(f"   eff(500 keV) = {eff_func(500):.4f}")
    print(f"   eff(1000 keV) = {eff_func(1000):.4f}")
    
    # 4. Create background model
    print("\n4. Creating background model...")
    env_bkg = lambda E: 0.001 * np.exp(-E/800)  # counts/s/keV
    bg_model = BackgroundModel(env_background=env_bkg)
    print(f"   Background @ 500 keV: {env_bkg(500):.4f} counts/s/keV")
    
    # 5. Grid search
    print("\n5. Running grid search optimization...")
    
    # Define search grid (in seconds)
    t_i1_list = [hours_to_seconds(t) for t in [0.5, 1, 2, 4]]
    t_d1_list = [hours_to_seconds(t) for t in [0.1, 0.5, 1, 2, 4]]
    t_c1_list = [hours_to_seconds(t) for t in [0.5, 1, 2, 4]]
    
    results = grid_search_schedules(
        t_i1_list=t_i1_list,
        t_d1_list=t_d1_list,
        t_c1_list=t_c1_list,
        gamma_lines=line_data,
        activity_interpolator=interp,
        eff_func=eff_func,
        background_model=bg_model,
        max_total_time=hours_to_seconds(12),  # 12 hour max
        z_goal=5.0,
        top_n=5,
        verbose=True
    )
    
    # 6. Display results
    print("\n6. Top 5 Schedules:")
    print("-" * 70)
    df = format_schedule_results(results, time_unit='h')
    print(df.to_string(index=False))
    
    # 7. Detailed view of best schedule
    if results:
        print_detailed_metrics(results[0], 'cycle1')
    
    return results


if __name__ == '__main__':
    run_example()
