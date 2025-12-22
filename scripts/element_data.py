"""
Element data utilities for MCNP-ALARA workflow.

Provides Z <-> element symbol conversions.
Loads from ALARA elelib file to avoid hard-coding.

Author: MCNP-ALARA Workflow
"""

import re
from pathlib import Path
from typing import Optional, Dict

# Path to ALARA data directory
_DATA_DIR = Path(__file__).parent.parent / "data"
_ELELIB_PATH = _DATA_DIR / "elelib.std"


def _parse_elelib() -> Dict[str, int]:
    """Parse elelib.std to get element -> Z mapping."""
    element_z = {}
    
    if not _ELELIB_PATH.exists():
        # Fall back to parent data dir
        alt_path = Path(__file__).parent.parent.parent / "data" / "elelib.std"
        if alt_path.exists():
            path = alt_path
        else:
            return {}
    else:
        path = _ELELIB_PATH
    
    with open(path, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                # First column is element symbol
                elem = parts[0].lower()
                # Only process if it looks like an element (letters only)
                if elem.isalpha() and len(elem) <= 3:
                    try:
                        z = int(parts[2])
                        element_z[elem] = z
                    except (ValueError, IndexError):
                        pass
    
    return element_z


# Load element data at import time
ELEMENT_Z = _parse_elelib()
Z_TO_ELEMENT = {v: k for k, v in ELEMENT_Z.items()}


def element_to_z(element: str) -> Optional[int]:
    """
    Convert element symbol to atomic number (Z).
    
    Parameters
    ----------
    element : str
        Element symbol (case-insensitive), e.g., 'Fe', 'W', 'co'
    
    Returns
    -------
    int or None
        Atomic number, or None if not found
    """
    return ELEMENT_Z.get(element.lower().strip())


def z_to_element(z: int, capitalize: bool = False) -> Optional[str]:
    """
    Convert atomic number (Z) to element symbol.
    
    Parameters
    ----------
    z : int
        Atomic number
    capitalize : bool
        If True, capitalize first letter (e.g., 'Fe' instead of 'fe')
    
    Returns
    -------
    str or None
        Element symbol, or None if Z not found
    """
    el = Z_TO_ELEMENT.get(z)
    if el is None:
        return None
    return el.capitalize() if capitalize else el


def zaid_to_element_mass(zaid: int) -> tuple:
    """
    Parse MCNP ZAID to (element, mass_number, Z).
    
    ZAID format: ZZZAAA (Z * 1000 + A)
    
    Parameters
    ----------
    zaid : int
        MCNP ZAID number
    
    Returns
    -------
    tuple
        (element_symbol, mass_number, Z) or (None, None, None) if invalid
    """
    Z = zaid // 1000
    A = zaid % 1000
    el = z_to_element(Z)
    if el is None:
        return None, A, Z
    return el, A, Z


if __name__ == "__main__":
    print("Element Data Module")
    print(f"Loaded {len(ELEMENT_Z)} elements from elelib")
    print()
    
    # Test some conversions
    test_elements = ['Fe', 'W', 'Ta', 'Co', 'Cr', 'Mn']
    for el in test_elements:
        z = element_to_z(el)
        print(f"{el} -> Z={z}")
    
    print()
    test_z = [26, 74, 73, 27, 24, 25]
    for z in test_z:
        el = z_to_element(z, capitalize=True)
        print(f"Z={z} -> {el}")
    
    print()
    test_zaids = [26056, 74182, 73181, 27059]
    for zaid in test_zaids:
        el, A, Z = zaid_to_element_mass(zaid)
        print(f"ZAID {zaid} -> {el}-{A} (Z={Z})")
