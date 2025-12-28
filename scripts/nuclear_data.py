"""
Nuclear Data Module - paceENSDF Interface
==========================================

Provides nuclear decay data (half-lives, gamma energies) from paceENSDF.
NO FALLBACK DATA - requires paceENSDF to be installed.

For isotopic data (atomic masses, abundances), use elelib_to_nuclib.py 
from the ALARA tools directory with PyNE (via Docker).

This module provides:
- `get_half_life(isotope)`: Get half-life in seconds
- `get_gamma_info(isotope)`: Get gamma energies and intensities
- `has_gamma_emission(isotope)`: Check if isotope has detectable gamma
- `normalize_isotope(label)`: Normalize isotope name to ALARA format

Author: MCNP-ALARA Workflow
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import numpy as np

# Add tools directory to path for alara_output_processing
_tools_dir = Path(__file__).parent.parent / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

from alara_output_processing import SECONDS_CONV

# ==============================================================================
# paceENSDF INTEGRATION
# ==============================================================================

try:
    import paceENSDF as pe
    HAS_PACE = True
except ImportError:
    HAS_PACE = False

# ==============================================================================
# CONSTANTS
# ==============================================================================
LN2 = np.log(2)
AVOGADRO = 6.02214076e23

# HPGe detector energy range for gamma spectroscopy
GAMMA_ENERGY_MIN_KEV = 80.0
GAMMA_ENERGY_MAX_KEV = 4000.0
GAMMA_INTENSITY_MIN = 0.01

# Unit conversion factors to Bq
UNIT_TO_BQ = {
    'bq': 1.0,
    'kbq': 1e3,
    'mbq': 1e-3,
    'ci': 3.7e10,
    'mci': 3.7e7,
    'uci': 37000.0,
    'µci': 37000.0,
    'nci': 37.0,
}


# ==============================================================================
# ISOTOPE NAME NORMALIZATION
# ==============================================================================

_ISO_PATTERNS = (
    re.compile(r"^(?P<el>[A-Za-z]{1,3})[-\s]?(?P<mass>\d{1,3})(?P<meta>m\d*|m)?$", re.IGNORECASE),
    re.compile(r"^(?P<mass>\d{1,3})(?P<meta>m\d*|m)?[-\s]?(?P<el>[A-Za-z]{1,3})$", re.IGNORECASE),
)


def normalize_isotope(label: str) -> str:
    """
    Normalize isotope label to ALARA-style format (lowercase, hyphenated).
    
    Examples:
        'W187' -> 'w-187'
        'Co-60' -> 'co-60'
        'Tb154m' -> 'tb-154m'
    """
    s = str(label).strip().replace("_", "").replace(" ", "")
    
    for pat in _ISO_PATTERNS:
        m = pat.match(s)
        if m:
            el = m.group("el").lower()
            mass = int(m.group("mass"))
            meta = (m.group("meta") or "").lower()
            return f"{el}-{mass}{meta}"
    
    return s.lower()


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
    """Format isotope name for display (e.g., 'ta182' -> 'Ta-182')."""
    if not iso:
        return iso
    m = re.match(r'(?i)^([a-z]+)(\d+)(m?)$', iso.replace('-', '').replace('_', ''))
    if m:
        elem, mass, meta = m.group(1, 2, 3)
        return f"{elem.capitalize()}-{mass}{meta.lower()}"
    return iso.capitalize()


def isotope_to_display(isotope: str) -> str:
    """Convert isotope to display format (e.g., 'w-187' -> 'W187')."""
    norm = normalize_isotope(isotope)
    m = re.match(r"([a-z]{1,3})-(\d+)(m\d*)?", norm)
    if m:
        el = m.group(1).capitalize()
        mass = m.group(2)
        meta = (m.group(3) or "").upper()
        return f"{el}{mass}{meta}"
    return isotope


def element_from_isotope(isotope: str) -> Optional[str]:
    """Extract element symbol from isotope label."""
    norm = normalize_isotope(isotope)
    m = re.match(r"([a-z]{1,3})-\d+", norm)
    return m.group(1).capitalize() if m else None


# ==============================================================================
# paceENSDF DATA EXTRACTION
# ==============================================================================

def _extract_ensdf_gammas(nucl: dict) -> List[Tuple[float, float]]:
    """
    Extract (energy_keV, intensity) pairs from paceENSDF nuclide data.
    
    paceENSDF structure:
        nucl['levelScheme'][*]['gammaDecay'][*] = {
            'gammaEnergy': float (keV),
            'gammaIntensity': float (percent, 0-100)
        }
    """
    gammas = []
    
    level_scheme = nucl.get('levelScheme', [])
    for level in level_scheme:
        gamma_decays = level.get('gammaDecay', [])
        for gd in gamma_decays:
            energy = gd.get('gammaEnergy')
            intensity = gd.get('gammaIntensity')
            
            if energy is not None and intensity is not None:
                try:
                    e = float(energy)
                    # Intensity is in percent (0-100), convert to fraction
                    ri = float(intensity) / 100.0
                    if 10.0 < e < 10000.0 and ri > 0.001:  # >0.1% threshold
                        gammas.append((e, ri))
                except (ValueError, TypeError):
                    pass
    
    return sorted(gammas, key=lambda x: -x[1])  # Sort by intensity descending


def _extract_ensdf_half_life(nucl: dict) -> Optional[float]:
    """
    Extract half-life in seconds from paceENSDF nuclide data.
    
    paceENSDF structure:
        nucl['parentDecay'][0]['halfLife'][0]['halfLifeConverted'] = float (seconds)
    """
    parent_decay = nucl.get('parentDecay', [])
    if not parent_decay:
        return None
    
    half_life_data = parent_decay[0].get('halfLife', [])
    if not half_life_data:
        return None
    
    # Get the converted half-life in seconds
    hl_entry = half_life_data[0]
    hl_seconds = hl_entry.get('halfLifeConverted')
    
    if hl_seconds is not None:
        try:
            return float(hl_seconds)
        except (ValueError, TypeError):
            pass
    
    return None


# Cache for ENSDF data
_ensdf_cache: Optional[dict] = None


def _load_ensdf_cache() -> dict:
    """
    Load and cache ENSDF data.
    
    For isotopes with multiple entries (ground state + metastable states),
    this merges gamma data and keeps the longest half-life (ground state).
    """
    global _ensdf_cache
    if _ensdf_cache is not None:
        return _ensdf_cache
    
    if not HAS_PACE:
        _ensdf_cache = {}
        return _ensdf_cache
    
    try:
        ensdf = pe.ENSDF()
        nuclides = ensdf.load_ensdf()
        
        _ensdf_cache = {}
        for nucl in nuclides:
            iso = nucl.get("parentID", "Unknown")
            iso_norm = normalize_isotope(str(iso))
            
            gammas = _extract_ensdf_gammas(nucl)
            half_life = _extract_ensdf_half_life(nucl)
            
            # Check if we already have an entry for this isotope
            if iso_norm in _ensdf_cache:
                existing = _ensdf_cache[iso_norm]
                
                # Merge gammas (add any new ones)
                existing_gammas = set((round(e, 1), round(i, 4)) for e, i in existing['gammas'])
                for g in gammas:
                    if (round(g[0], 1), round(g[1], 4)) not in existing_gammas:
                        existing['gammas'].append(g)
                
                # Keep the LONGER half-life (ground state is typically longer)
                if half_life is not None:
                    if existing['half_life_s'] is None or half_life > existing['half_life_s']:
                        existing['half_life_s'] = half_life
                
                # Re-sort gammas by intensity
                existing['gammas'] = sorted(existing['gammas'], key=lambda x: -x[1])
            else:
                _ensdf_cache[iso_norm] = {
                    'gammas': gammas,
                    'half_life_s': half_life,
                    'raw': nucl,
                }
    except Exception as e:
        print(f"Warning: Could not load paceENSDF data: {e}")
        _ensdf_cache = {}
    
    return _ensdf_cache


# ==============================================================================
# PUBLIC API
# ==============================================================================

def get_half_life(isotope: str) -> Optional[float]:
    """
    Get half-life in seconds for an isotope.
    
    Parameters
    ----------
    isotope : str
        Isotope label (e.g., 'Co-60', 'co60', 'Co60')
    
    Returns
    -------
    float or None
        Half-life in seconds, or None if not found
    
    Raises
    ------
    RuntimeError
        If paceENSDF is not available
    """
    if not HAS_PACE:
        raise RuntimeError(
            "paceENSDF is required but not installed. "
            "Install with: pip install paceENSDF"
        )
    
    norm = normalize_isotope(isotope)
    cache = _load_ensdf_cache()
    
    if norm in cache and cache[norm]['half_life_s'] is not None:
        return cache[norm]['half_life_s']
    
    return None


def get_half_life_days(isotope: str) -> Optional[float]:
    """Get half-life in days."""
    hl_s = get_half_life(isotope)
    if hl_s is None:
        return None
    return hl_s / SECONDS_CONV['d']


def get_gamma_info(isotope: str) -> Optional[Dict[str, Any]]:
    """
    Get gamma emission data for an isotope.
    
    Parameters
    ----------
    isotope : str
        Isotope label
    
    Returns
    -------
    dict or None
        Dict with keys:
        - 'gammas': List of (energy_keV, intensity) tuples
        - 'primary_keV': Energy of strongest gamma line
        - 'primary_intensity': Intensity of strongest line
    
    Raises
    ------
    RuntimeError
        If paceENSDF is not available
    """
    if not HAS_PACE:
        raise RuntimeError(
            "paceENSDF is required but not installed. "
            "Install with: pip install paceENSDF"
        )
    
    norm = normalize_isotope(isotope)
    cache = _load_ensdf_cache()
    
    if norm in cache and cache[norm]['gammas']:
        gammas = cache[norm]['gammas']
        primary = gammas[0]  # Already sorted by intensity
        return {
            'gammas': gammas,
            'primary_keV': primary[0],
            'primary_intensity': primary[1],
        }
    
    return None


def has_gamma_emission(
    isotope: str,
    min_intensity: float = GAMMA_INTENSITY_MIN,
    energy_min_keV: float = GAMMA_ENERGY_MIN_KEV,
    energy_max_keV: float = GAMMA_ENERGY_MAX_KEV
) -> bool:
    """
    Check if isotope has detectable gamma emission.
    
    Parameters
    ----------
    isotope : str
        Isotope label
    min_intensity : float
        Minimum intensity threshold (default 1%)
    energy_min_keV : float
        Minimum gamma energy (default 80 keV)
    energy_max_keV : float
        Maximum gamma energy (default 4000 keV)
    
    Returns
    -------
    bool
        True if isotope has gamma emission above threshold
    """
    try:
        info = get_gamma_info(isotope)
    except RuntimeError:
        return False
    
    if info is None:
        return False
    for energy, intensity in info['gammas']:
        if energy_min_keV <= energy <= energy_max_keV and intensity >= min_intensity:
            return True
    return False


def get_decay_constant(isotope: str) -> Optional[float]:
    """Get decay constant (lambda) in 1/s."""
    hl = get_half_life(isotope)
    if hl is None or hl <= 0:
        return None
    return LN2 / hl


def get_half_life_seconds(isotope: str) -> Optional[float]:
    """Alias for get_half_life (seconds)."""
    return get_half_life(isotope)


def half_life_to_lambda(half_life_seconds: float) -> float:
    """Convert half-life (seconds) to decay constant lambda (1/s)."""
    if half_life_seconds <= 0:
        return 0.0
    return LN2 / half_life_seconds


def parse_half_life_string(hl_string: str) -> Optional[float]:
    """
    Parse a half-life string like '12.7 h' or '27.7 d' to seconds.
    """
    if not hl_string:
        return None
    parts = hl_string.strip().split()
    if len(parts) < 2:
        return None
    try:
        val = float(parts[0])
        unit = parts[1].lower().rstrip('.')
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


def parse_activity_unit(unit_str: str) -> float:
    """
    Parse activity unit string and return conversion factor to Bq.
    """
    if not unit_str:
        return UNIT_TO_BQ['uci']

    u = unit_str.strip().lower()
    u = u.replace('\u00b5', 'u').replace('µ', 'u')
    u = re.sub(r'/[gk]?g?', '', u)
    u = u.replace('per', '').strip()

    tokens = re.findall(r'[a-z]+', u)

    for key in sorted(UNIT_TO_BQ.keys(), key=len, reverse=True):
        for token in tokens:
            if token == key:
                return UNIT_TO_BQ[key]

    for key in sorted(UNIT_TO_BQ.keys(), key=len, reverse=True):
        if key in u:
            return UNIT_TO_BQ[key]

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
    """
    unit_lower = unit.lower().strip()
    if unit_lower in ('b', 'barn', 'barns'):
        return xs * 1e-24
    if unit_lower in ('mb', 'millibarn', 'millibarns'):
        return xs * 1e-27
    return xs * 1e-24


def calculate_n_atoms(mass_g: float, atomic_mass: float) -> float:
    """
    Calculate number of atoms from mass and atomic mass.
    """
    return (mass_g / atomic_mass) * AVOGADRO


def extract_mass_number(isotope: str) -> Optional[int]:
    """
    Extract mass number from isotope string.
    """
    m = re.search(r'(\d+)', isotope)
    if m:
        return int(m.group(1))
    return None


def get_half_life_info(isotope: str) -> tuple:
    """Get half-life info using paceENSDF via nuclear_data module."""
    hl_days = get_half_life_days(isotope)
    decay_modes = None
    decay_info = get_gamma_info(isotope)
    if decay_info and 'decay_modes' in decay_info:
        decay_modes = decay_info['decay_modes']
    return hl_days, decay_modes


def format_half_life(hl_days: float) -> str:
    """Format half-life for display."""
    if hl_days is None:
        return "?"
    if hl_days < 1/24:
        return f"{hl_days * 24 * 60:.1f} min"
    if hl_days < 1:
        return f"{hl_days * 24:.1f} h"
    if hl_days < 365:
        return f"{hl_days:.1f} d"
    return f"{hl_days / 365:.1f} y"


def get_gamma_info_filtered(
    isotope: str,
    energy_min_keV: float = GAMMA_ENERGY_MIN_KEV,
    energy_max_keV: float = GAMMA_ENERGY_MAX_KEV
) -> Optional[dict]:
    """
    Get gamma emission information filtered to an energy range.
    """
    nd_info = get_gamma_info(isotope)
    if nd_info is None:
        return None

    all_gammas = nd_info.get('gammas', [])
    filtered_gammas = [
        (e, i) for e, i in all_gammas
        if energy_min_keV <= e <= energy_max_keV
    ]

    if not filtered_gammas:
        return None

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
    """
    result = []
    for item in isotopes:
        iso = item.get('isotope', '') if isinstance(item, dict) else str(item)
        if has_gamma_emission(iso, min_intensity, energy_min_keV, energy_max_keV):
            result.append(item)
    return result


# ==============================================================================
# CONVENIENCE: Check data source
# ==============================================================================

def using_ensdf() -> bool:
    """Return True if paceENSDF data is available."""
    return HAS_PACE


def get_data_source() -> str:
    """Return description of current data source."""
    if HAS_PACE:
        cache = _load_ensdf_cache()
        if cache:
            return f"paceENSDF (ENSDF database, {len(cache)} nuclides)"
        return "paceENSDF (loading...)"
    return "ERROR: paceENSDF not installed"


# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == "__main__":
    print(f"Nuclear Data Module")
    print(f"Data source: {get_data_source()}")
    print()
    
    if not HAS_PACE:
        print("ERROR: paceENSDF is not installed!")
        print("Install with: pip install paceENSDF")
        sys.exit(1)
    
    # Test some isotopes
    test_isotopes = ['Co-60', 'W187', 'ta-182', 'Mn-54', 'Fe59', 'Cr-51']
    
    print("Half-lives:")
    for iso in test_isotopes:
        hl = get_half_life_days(iso)
        print(f"  {iso}: {hl:.2f} days" if hl else f"  {iso}: Not found")
    
    print("\nGamma data:")
    for iso in test_isotopes:
        info = get_gamma_info(iso)
        if info:
            print(f"  {iso}: Primary = {info['primary_keV']:.1f} keV "
                  f"(I = {info['primary_intensity']:.3f})")
        else:
            print(f"  {iso}: No gamma data")
