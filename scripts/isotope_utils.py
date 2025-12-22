"""
Isotope utilities for MCNP-ALARA workflow.

Provides functionality NOT already in alara_output_processing:
- Isotope name canonicalization (ALARA format: "fe-56")
- Activity unit conversions (Bq, Ci, etc.)
- Cross-section unit conversions
- Half-life database for common activation products
- Gamma emission data (uses paceENSDF when available via nuclear_data module)

For time unit conversions, use alara_output_processing.SECONDS_CONV and
alara_output_processing.convert_times() instead.

For nuclear data (half-lives, gamma energies, element mappings), this module 
now delegates to nuclear_data.py which uses paceENSDF when available.
"""

import re
import sys
import numpy as np
from pathlib import Path
from typing import Optional

# Add tools directory to path for alara_output_processing
tools_dir = Path(__file__).parent.parent / "tools"
if tools_dir.exists() and str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Import time conversion from alara_output_processing
from alara_output_processing import SECONDS_CONV, convert_times

# Import nuclear data functions (uses paceENSDF - no fallbacks)
from nuclear_data import (
    get_half_life as _nd_get_half_life,
    get_half_life_days as _nd_get_half_life_days,
    get_gamma_info as _nd_get_gamma_info,
    get_decay_constant as _nd_get_decay_constant,
    normalize_isotope as _nd_normalize_isotope,
    using_ensdf,
    get_data_source,
)

# ==============================================================================
# CONSTANTS
# ==============================================================================
LN2 = np.log(2)
AVOGADRO = 6.02214076e23

# HPGe detector energy range for gamma spectroscopy
GAMMA_ENERGY_MIN_KEV = 80.0    # Minimum detectable gamma energy
GAMMA_ENERGY_MAX_KEV = 4000.0  # Maximum typical gamma energy
GAMMA_INTENSITY_MIN = 0.01     # Minimum intensity (1%) to be detectable

# Unit conversion factors to Bq (not in alara_output_processing)
UNIT_TO_BQ = {
    'bq': 1.0,
    'kbq': 1e3,
    'mbq': 1e-3,  # milliBq
    'ci': 3.7e10,
    'mci': 3.7e7,
    'uci': 37000.0,
    'µci': 37000.0,
    'nci': 37.0,
}


# ==============================================================================
# ISOTOPE NAMING
# ==============================================================================
def canonical_iso(name: str) -> str:
    """
    Normalize isotope strings to lowercase element + mass (+ metastable suffix).
    
    Examples:
        'Ta-182' -> 'ta182'
        'Co 60'  -> 'co60'
        'In-115m' -> 'in115m'
        'Sc_46'  -> 'sc46'
    """
    if name is None:
        return ''
    s = str(name).strip().replace(' ', '').replace('_', '').replace('-', '')
    m = re.match(r'(?i)^([a-z]+)(\d+)(m?)$', s)
    if not m:
        return s.lower()
    elem, mass, meta = m.group(1, 2, 3)
    return f"{elem.lower()}{mass}{meta.lower()}"


def format_iso_pretty(iso: str) -> str:
    """
    Format isotope name for display (e.g., 'ta182' -> 'Ta-182').
    """
    if not iso:
        return iso
    # Try to parse element and mass
    m = re.match(r'(?i)^([a-z]+)(\d+)(m?)$', iso.replace('-', '').replace('_', ''))
    if m:
        elem, mass, meta = m.group(1, 2, 3)
        return f"{elem.capitalize()}-{mass}{meta.lower()}"
    return iso.capitalize()


# ==============================================================================
# HALF-LIFE UTILITIES
# ==============================================================================
def get_half_life_days(isotope: str) -> Optional[float]:
    """
    Get half-life in days for an isotope (case-insensitive).
    
    Uses paceENSDF via nuclear_data module for authoritative ENSDF data.
    
    Returns None if isotope not found in database.
    """
    return _nd_get_half_life_days(isotope)


def get_half_life_seconds(isotope: str) -> Optional[float]:
    """
    Get half-life in seconds for an isotope.
    
    Uses paceENSDF via nuclear_data module.
    """
    return _nd_get_half_life(isotope)


def half_life_to_lambda(half_life_seconds: float) -> float:
    """Convert half-life (seconds) to decay constant lambda (1/s)."""
    if half_life_seconds <= 0:
        return 0.0
    return LN2 / half_life_seconds


def parse_half_life_string(hl_string: str) -> Optional[float]:
    """
    Parse a half-life string like '12.7 h' or '27.7 d' to seconds.
    
    Uses SECONDS_CONV from alara_output_processing for unit mappings.
    Supports: s, m, h, d, w, y, c (seconds, minutes, hours, days, weeks, years, centuries)
    
    Returns None if parsing fails.
    """
    if not hl_string:
        return None
    parts = hl_string.strip().split()
    if len(parts) < 2:
        return None
    try:
        val = float(parts[0])
        unit = parts[1].lower().rstrip('.')
        # Map common aliases to SECONDS_CONV keys
        unit_map = {
            'sec': 's', 'second': 's', 'seconds': 's',
            'min': 'm', 'minute': 'm', 'minutes': 'm',
            'hr': 'h', 'hour': 'h', 'hours': 'h',
            'day': 'd', 'days': 'd',
            'wk': 'w', 'week': 'w', 'weeks': 'w',
            'yr': 'y', 'year': 'y', 'years': 'y',
        }
        unit_key = unit_map.get(unit, unit)
        mult = SECONDS_CONV.get(unit_key, None)
        if mult is None:
            return None
        return val * mult
    except (ValueError, IndexError):
        return None


# ==============================================================================
# GAMMA EMISSION UTILITIES (FOR HPGe DETECTABILITY)
# ==============================================================================
def has_gamma_emission(
    isotope: str, 
    min_intensity: float = GAMMA_INTENSITY_MIN,
    energy_min_keV: float = GAMMA_ENERGY_MIN_KEV,
    energy_max_keV: float = GAMMA_ENERGY_MAX_KEV
) -> bool:
    """
    Check if an isotope has detectable gamma emissions for HPGe spectroscopy.
    
    Queries paceENSDF database via nuclear_data module and filters for:
    - Gamma energies in the specified range (default 80-4000 keV)
    - Intensities above the minimum threshold (default 1%)
    
    Parameters:
        isotope: Isotope name (any format, will be canonicalized)
        min_intensity: Minimum gamma intensity (branching ratio) to consider
                       Default 0.01 (1%) - typical HPGe detection threshold
        energy_min_keV: Minimum gamma energy (default 80 keV)
        energy_max_keV: Maximum gamma energy (default 4000 keV)
    
    Returns:
        True if isotope has gamma emissions meeting all criteria
        False if no gamma data or no gammas in range above threshold
    """
    # Get gamma info from paceENSDF via nuclear_data
    info = _nd_get_gamma_info(isotope)
    if info is None:
        return False
    
    gammas = info.get('gammas', [])
    if not gammas:
        return False
    
    # Check if any gamma is in the detectable range with sufficient intensity
    for energy, intensity in gammas:
        if energy_min_keV <= energy <= energy_max_keV and intensity >= min_intensity:
            return True
    
    return False


def get_gamma_info(
    isotope: str,
    energy_min_keV: float = GAMMA_ENERGY_MIN_KEV,
    energy_max_keV: float = GAMMA_ENERGY_MAX_KEV
) -> Optional[dict]:
    """
    Get gamma emission information for an isotope from paceENSDF database.
    
    Filters gamma lines to the HPGe detectable energy range.
    
    Parameters:
        isotope: Isotope name (any format)
        energy_min_keV: Minimum gamma energy (default 80 keV)
        energy_max_keV: Maximum gamma energy (default 4000 keV)
    
    Returns:
        dict with gamma info if found, None otherwise.
        Keys:
        - 'gammas': List of (energy_keV, intensity) tuples in range
        - 'main_gamma_keV': Energy of highest intensity gamma in range
        - 'intensity': Intensity of the primary gamma
        - 'other_gammas': List of other gamma energies in range
    """
    nd_info = _nd_get_gamma_info(isotope)
    if nd_info is None:
        return None
    
    # Filter gammas to the detectable energy range
    all_gammas = nd_info.get('gammas', [])
    filtered_gammas = [
        (e, i) for e, i in all_gammas 
        if energy_min_keV <= e <= energy_max_keV
    ]
    
    if not filtered_gammas:
        return None
    
    # Find the primary (highest intensity) gamma in range
    primary = max(filtered_gammas, key=lambda x: x[1])
    
    return {
        'main_gamma_keV': primary[0],
        'intensity': primary[1],
        'gammas': filtered_gammas,
        'other_gammas': [g[0] for g in filtered_gammas if g[0] != primary[0]],
        '_from_ensdf': True,
    }


def filter_gamma_emitters(
    isotopes: list, 
    min_intensity: float = GAMMA_INTENSITY_MIN,
    energy_min_keV: float = GAMMA_ENERGY_MIN_KEV,
    energy_max_keV: float = GAMMA_ENERGY_MAX_KEV
) -> list:
    """
    Filter a list of isotopes to only those with detectable gamma emissions.
    
    Queries paceENSDF database and filters based on:
    - Energy range suitable for HPGe detection (default 80-4000 keV)
    - Intensity above minimum threshold (default 1%)
    
    Parameters:
        isotopes: List of isotope names or dicts with 'isotope' key
        min_intensity: Minimum gamma intensity threshold (default 0.01 = 1%)
        energy_min_keV: Minimum gamma energy (default 80 keV)
        energy_max_keV: Maximum gamma energy (default 4000 keV)
    
    Returns:
        Filtered list containing only gamma emitters with detectable peaks
    """
    result = []
    for item in isotopes:
        if isinstance(item, dict):
            iso = item.get('isotope', '')
        else:
            iso = str(item)
        
        if has_gamma_emission(iso, min_intensity, energy_min_keV, energy_max_keV):
            result.append(item)
    
    return result


# ==============================================================================
# UNIT CONVERSIONS
# ==============================================================================
def parse_activity_unit(unit_str: str) -> float:
    """
    Parse activity unit string and return conversion factor to Bq.
    
    Returns factor such that: activity_Bq = activity_raw * factor
    """
    if not unit_str:
        return UNIT_TO_BQ['uci']  # default: µCi
    
    u = unit_str.strip().lower()
    # Normalize micro symbol
    u = u.replace('\u00b5', 'u').replace('µ', 'u')
    # Remove /g or /kg etc
    u = re.sub(r'/[gk]?g?', '', u)
    u = u.replace('per', '').strip()
    
    # Extract just the unit part
    tokens = re.findall(r'[a-z]+', u)
    
    # Try exact match first (longer units first to avoid partial matches)
    for key in sorted(UNIT_TO_BQ.keys(), key=len, reverse=True):
        for token in tokens:
            if token == key:
                return UNIT_TO_BQ[key]
    
    # Fallback: substring match
    for key in sorted(UNIT_TO_BQ.keys(), key=len, reverse=True):
        if key in u:
            return UNIT_TO_BQ[key]
    
    # Default to µCi
    return UNIT_TO_BQ['uci']


def activity_bq_to_uci(activity_bq: float) -> float:
    """Convert activity from Bq to µCi."""
    return activity_bq / 37000.0


def activity_uci_to_bq(activity_uci: float) -> float:
    """Convert activity from µCi to Bq."""
    return activity_uci * 37000.0


def cross_section_to_cm2(xs: float, unit: str) -> float:
    """
    Convert cross-section to cm².
    
    Parameters:
        xs: Cross-section value
        unit: 'b' for barns, 'mb' for millibarns
    
    Returns:
        Cross-section in cm²
    """
    unit_lower = unit.lower().strip()
    if unit_lower in ('b', 'barn', 'barns'):
        return xs * 1e-24
    elif unit_lower in ('mb', 'millibarn', 'millibarns'):
        return xs * 1e-27
    else:
        # Assume barns
        return xs * 1e-24


# ==============================================================================
# ATOMIC CALCULATIONS
# ==============================================================================
def calculate_n_atoms(mass_g: float, atomic_mass: float) -> float:
    """
    Calculate number of atoms from mass and atomic mass.
    
    Parameters:
        mass_g: Mass in grams
        atomic_mass: Atomic mass in amu (approximately equal to mass number)
    
    Returns:
        Number of atoms
    """
    return (mass_g / atomic_mass) * AVOGADRO


def extract_mass_number(isotope: str) -> Optional[int]:
    """
    Extract mass number from isotope string.
    
    Examples:
        'ta182' -> 182
        'Co-60' -> 60
        'in115m' -> 115
    """
    m = re.search(r'(\d+)', isotope)
    if m:
        return int(m.group(1))
    return None


# ==============================================================================
# DISPLAY FORMATTING
# ==============================================================================
def get_half_life_info(isotope: str) -> tuple:
    """Get half-life info using paceENSDF via nuclear_data module.
    
    Returns:
        tuple: (half_life_days, decay_modes or None)
    """
    # Use paceENSDF via nuclear_data - no fallbacks
    hl_days = get_half_life_days(isotope)
    
    # Try to get decay modes from paceENSDF
    decay_modes = None
    decay_info = _nd_get_gamma_info(isotope)
    if decay_info and 'decay_modes' in decay_info:
        decay_modes = decay_info['decay_modes']
    
    return hl_days, decay_modes


def format_half_life(hl_days: float) -> str:
    """Format half-life for display."""
    if hl_days is None:
        return "?"
    elif hl_days < 1/24:  # < 1 hour
        return f"{hl_days * 24 * 60:.1f} min"
    elif hl_days < 1:  # < 1 day
        return f"{hl_days * 24:.1f} h"
    elif hl_days < 365:
        return f"{hl_days:.1f} d"
    else:
        return f"{hl_days / 365:.1f} y"


if __name__ == '__main__':
    # Quick tests
    print("Testing isotope_utils...")
    
    print(f"canonical_iso('Ta-182') = {canonical_iso('Ta-182')}")
    print(f"canonical_iso('Co 60') = {canonical_iso('Co 60')}")
    print(f"format_iso_pretty('ta182') = {format_iso_pretty('ta182')}")
    
    print(f"get_half_life_days('co60') = {get_half_life_days('co60')}")
    print(f"get_half_life_seconds('mn56') = {get_half_life_seconds('mn56')}")
    
    print(f"parse_activity_unit('µCi/g') = {parse_activity_unit('µCi/g')}")
    print(f"parse_activity_unit('Bq') = {parse_activity_unit('Bq')}")
    
    print(f"extract_mass_number('Ta-182') = {extract_mass_number('Ta-182')}")
    
    # Test gamma emission functions
    print("\n--- Gamma emission tests ---")
    print(f"has_gamma_emission('v-52') = {has_gamma_emission('v-52')}")  # True - 1434 keV
    print(f"has_gamma_emission('fe-55') = {has_gamma_emission('fe-55')}")  # False - EC only
    print(f"has_gamma_emission('ni-63') = {has_gamma_emission('ni-63')}")  # False - pure beta
    print(f"has_gamma_emission('co-60') = {has_gamma_emission('co-60')}")  # True - 1332 keV
    print(f"get_gamma_info('ta-182') = {get_gamma_info('ta-182')}")
    
    # Test filter_gamma_emitters
    test_isotopes = ['v-52', 'fe-55', 'ni-63', 'co-60', 'mn-54']
    filtered = filter_gamma_emitters(test_isotopes)
    print(f"filter_gamma_emitters({test_isotopes}) = {filtered}")
    
    print("\nAll tests passed!")
