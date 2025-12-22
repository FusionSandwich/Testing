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


def has_gamma_emission(isotope: str, min_intensity: float = 0.01) -> bool:
    """
    Check if isotope has detectable gamma emission.
    
    Parameters
    ----------
    isotope : str
        Isotope label
    min_intensity : float
        Minimum intensity threshold (default 1%)
    
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
    return any(g[1] >= min_intensity for g in info['gammas'])


def get_decay_constant(isotope: str) -> Optional[float]:
    """Get decay constant (lambda) in 1/s."""
    hl = get_half_life(isotope)
    if hl is None or hl <= 0:
        return None
    return LN2 / hl


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
