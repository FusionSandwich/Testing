#!/usr/bin/env python3
"""
MCNP to ALARA Workflow Script - Version 3

This script:
1. Parses FMESH definitions from MCNP input and gets the material name from comment before each FMESH
2. Searches for "C name: MATERIAL_NAME" to find the material definition section
3. Gets density from the first "C density = X.XX" after that material name line
4. Gets isotopic composition from the material card (mXXXXX) that follows
5. Extracts mesh tally flux data from HDF5 file
6. Generates ALARA input files for each mesh tally with comprehensive output options
7. Runs ALARA and parses results for each voxel
8. Calculates averages across all voxels

Hardcoded Parameters:
- Phase 1: 3 second irradiation, cooling times: 5.00m, 2h, 26h, 4d
- Phase 2: 2 hour irradiation, cooling times: 15d, 30d, 1y, 5y, 10y, 20y, 50y, 100y
- Default library: FENDL-3 DSV (December 2024 - complete with all reactions)

Output quantities for each voxel:
- Nuclide inventories (atoms, grams) vs. time
- Nuclide-specific activities (Bq, Bq/g) vs. time
- Total activity of the sample (Bq, Bq/g) vs. time
- Decay heat / total power (W, W/g) vs. time
- Photon (gamma) source spectrum vs. time
- Transmutation products and changes in isotopic composition
- Dominant contributor analysis

Usage:
    python mcnp_to_alara.py --mcnp <mcnp_input.i> --h5 <runtpk.h5> --output <output_dir> [--library fendl2] [--phase 1|2]
    
    # Phase 1 (3s irradiation for experimental comparison):
    python mcnp_to_alara.py --mcnp whale.i --h5 runtpe.h5 --output alara_phase1 --run-alara --phase 1
    
    # Phase 2 (2h irradiation for long-term predictions):
    python mcnp_to_alara.py --mcnp whale.i --h5 runtpe.h5 --output alara_phase2 --run-alara --phase 2
"""

import argparse
import os
import re
import sys
import json
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np

# Add tools directory to path for alara_output_processing
# In the rafm_irradiation_ldrd repo, tools is at ALARA_ROOT/tools (two levels up)
_script_dir = Path(__file__).parent
_project_root = _script_dir.parent  # rafm_irradiation_ldrd
_alara_root = _project_root.parent  # ALARA
_tools_dir = _alara_root / "tools"
if _tools_dir.exists() and str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))
# Also add scripts directory for our support modules
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

# Import from ALARA tools modules
from alara_output_processing import SECONDS_CONV, convert_times, FileParser, ALARADFrame, DataLibrary

# Import isotope utilities (half-life, gamma info, formatting)
from isotope_utils import (
    canonical_iso, format_iso_pretty,
    get_half_life_days, get_half_life_seconds,
    has_gamma_emission, get_gamma_info,
)

# Import element data (Z <-> element conversions from elelib)
from element_data import ELEMENT_Z, Z_TO_ELEMENT, element_to_z, z_to_element

try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False
    print("Warning: h5py not available. HDF5 reading will be disabled.")

# Try to import sample schedule module for sample-specific cooling times
try:
    from sample_irradiation_schedule import (
        get_all_sample_schedules, 
        SAMPLE_TO_MATERIAL,
        MATERIAL_TO_TALLY
    )
    HAS_SAMPLE_SCHEDULE = True
except ImportError:
    HAS_SAMPLE_SCHEDULE = False
    # Define fallback mappings if module not available
    SAMPLE_TO_MATERIAL = {
        'A': 'EUROFER97_2',
        'B': 'EUROFER97_3', 
        'C': 'EUROFER97_4',
        'N': 'CNA',
    }
    MATERIAL_TO_TALLY = {
        'EUROFER97_2': 'tally_85244',
        'EUROFER97_3': 'tally_85234',
        'EUROFER97_4': 'tally_85224',
        'CNA': 'tally_85214',
        'SS420': 'tally_85114',
    }


# ============================================================================
# HARDCODED IRRADIATION AND COOLING PARAMETERS
# ============================================================================
# Experiment schedule:
# Phase 1: 3 second irradiation, then cooling measurements at 300s, 2hr, 24hr, 4d
# Phase 2: 2 hour irradiation, then cooling for 15d measurement
# 
# IMPORTANT: Each sample has DIFFERENT actual cooling times based on when
# gamma spec measurements were taken. Use sample_irradiation_schedule.py
# to calculate the exact times for each sample.
#
# For generic runs without sample-specific timing, we use approximate values:
IRRADIATION_SCHEDULE = [
    {"irradiation": "3 s", "cooling_times": ["5.00 m", "2 h", "26 h", "4 d"]},  # Phase 1
    {"irradiation": "2 h", "cooling_times": ["15 d"]},  # Phase 2
]

# For backward compatibility, keep a simple version
# Phase 1 uses 3s irradiation for short-term activation measurements
IRRADIATION_TIME = "3 s"  # 3-second irradiation (Phase 1)

# Flux normalization factor
# MCNP outputs flux per source particle. For absolute activation, multiply by source strength.
# Based on experimental calibration, the absolute flux is:
#   φ_abs = φ_MC × 7.6×10^16
# This accounts for the actual neutron source strength in the experiment.
FLUX_NORMALIZATION = 7.6e16  # n/s from experimental calibration

# Cooling times for Phase 1 (after 3s irradiation) - approximate values
# For sample-specific times, use sample_irradiation_schedule.py
COOLING_TIMES_PHASE1 = [
    "5.00 m",   # ~357s post-irradiation (experimental: 300sEOI)
    "2 h",      # ~2 hours post-irradiation (experimental: 2hrEOI)  
    "26 h",     # ~26 hours post-irradiation (experimental: 24hrEOI)
    "4 d",      # ~4 days post-irradiation (experimental: 4dEOI)
]

# Cooling times for Phase 2 (after 2h irradiation) - long-term predictions
COOLING_TIMES_PHASE2 = [
    "15 d",     # 15 days
    "30 d",     # 30 days  
]

# Combined for single-phase runs (use Phase 1 for experimental comparison)
COOLING_TIMES = COOLING_TIMES_PHASE1

# Labels for output (Phase 1)
COOLING_TIME_LABELS = [
    "300s",
    "2hr",
    "24hr", 
    "4d",
    "15d",
]

# ============================================================================
# LIBRARY PATHS AND GROUP STRUCTURES
# ============================================================================
# 
# NOTE ON LIBRARIES:
# - FENDL-2.0: Complete activation library with all (n,γ) capture reactions
#              This is the RECOMMENDED library for activation calculations
# - FENDL-3.x: The converted versions are MISSING (n,γ) capture reactions!
#              These should NOT be used for activation analysis until fixed
#
LIBRARY_PATHS = {
    'fendl2': {
        'data_library': '/groupspace/cnerg/opt/FENDL2.0-A/fendl2.0bin',
        'description': 'FENDL-2.0 activation library (COMPLETE - all reactions including n,gamma)',
        'gamma_lib': '/groupspace/cnerg/opt/FENDL2.0-A/fendl2.0bin',
        'gamma_lib_file': '/groupspace/cnerg/opt/FENDL2.0-A/fendl2.0bin',  # Gamma spectrum library (ALARA adds .gam)
        'n_groups': 175,  # VITAMIN-J 175-group structure
    },
    'fendl3_new': {
        'data_library': '/filespace/s/smandych/CAE/projects/ALARA/MCNP_ALARA_Workflow/data/cumulative_gendf_data.dsv',
        'description': 'FENDL-3 DSV library (December 2024 - COMPLETE with all reactions)',
        'gamma_lib': '/filespace/s/smandych/CAE/projects/ALARA/MCNP_ALARA_Workflow/data/cumulative_gendf_data.dsv',
        'n_groups': 175,  # VITAMIN-J 175-group structure
    },
}

# Default library - use new FENDL-3 DSV library from December 2024
DEFAULT_LIBRARY = 'fendl3_new'

# Element library path
ELEMENT_LIB = '/filespace/s/smandych/CAE/projects/ALARA/data/elelib.std'

# ALARA executable path
ALARA_EXECUTABLE = '/filespace/s/smandych/CAE/projects/ALARA/bin/alara'


# ============================================================================
# TIME CONVERSION UTILITIES
# Uses SECONDS_CONV from alara_output_processing
# ============================================================================

def parse_time_to_seconds(time_str):
    """
    Convert ALARA time string (e.g., '3 s', '4 d', '2.5 h') to seconds.
    
    Uses SECONDS_CONV from alara_output_processing for core unit mappings.
    """
    parts = time_str.strip().split()
    if len(parts) != 2:
        return 0
    
    value = float(parts[0])
    unit = parts[1].lower()
    
    # Extended mappings based on SECONDS_CONV from alara_output_processing
    # Core units: s, m, h, d, w, y, c
    conversions = dict(SECONDS_CONV)
    # Add common aliases
    conversions.update({
        'sec': SECONDS_CONV['s'], 'second': SECONDS_CONV['s'], 'seconds': SECONDS_CONV['s'],
        'min': SECONDS_CONV['m'], 'minute': SECONDS_CONV['m'], 'minutes': SECONDS_CONV['m'],
        'hr': SECONDS_CONV['h'], 'hour': SECONDS_CONV['h'], 'hours': SECONDS_CONV['h'],
        'day': SECONDS_CONV['d'], 'days': SECONDS_CONV['d'],
        'yr': SECONDS_CONV['y'], 'year': SECONDS_CONV['y'], 'years': SECONDS_CONV['y'],
    })
    
    return value * conversions.get(unit, 1)


def seconds_to_alara_time(seconds):
    """
    Convert seconds to appropriate ALARA time string.
    
    Uses SECONDS_CONV from alara_output_processing for unit thresholds.
    """
    if seconds < SECONDS_CONV['m']:
        return f"{seconds} s"
    elif seconds < SECONDS_CONV['h']:
        return f"{seconds / SECONDS_CONV['m']:.4f} m"
    elif seconds < SECONDS_CONV['d']:
        return f"{seconds / SECONDS_CONV['h']:.4f} h"
    elif seconds < SECONDS_CONV['y']:
        return f"{seconds / SECONDS_CONV['d']:.4f} d"
    else:
        return f"{seconds / SECONDS_CONV['y']:.4f} y"


def check_material_library_coverage(material_data, library):
    """
    Check which elements in the material are covered by the library.
    Returns list of covered and uncovered elements.
    """
    lib_info = LIBRARY_PATHS.get(library, LIBRARY_PATHS[DEFAULT_LIBRARY])
    max_z = lib_info.get('max_z', 100)  # Default to all elements if not specified
    
    covered = []
    uncovered = []
    
    for Z, A, frac in material_data['isotopes']:
        element = Z_TO_ELEMENT.get(Z, f'Z{Z}')
        if Z <= max_z:
            if element not in covered:
                covered.append(element)
        else:
            if element not in uncovered:
                uncovered.append(element)
    
    return covered, uncovered


# ============================================================================
# MCNP PARSING FUNCTIONS
# ============================================================================

def parse_mcnp_fmesh_with_materials(mcnp_file):
    """
    Parse MCNP input file to extract FMESH definitions and their associated material names.
    
    Also extracts mesh coordinates (IMESH, JMESH, KMESH) to calculate actual voxel volumes.
    """
    fmesh_data = {}
    
    with open(mcnp_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for FMESH card
        fmesh_match = re.match(r'FMESH(\d+):N', line, re.IGNORECASE)
        if fmesh_match:
            tally_num = int(fmesh_match.group(1))
            
            # Look at the previous non-empty line for material comment
            material_name = None
            j = i - 1
            while j >= 0:
                prev_line = lines[j].strip()
                if prev_line:
                    mat_match = re.match(r'^C\s+(\S+)\s*$', prev_line, re.IGNORECASE)
                    if mat_match:
                        potential_name = mat_match.group(1)
                        if not any(kw in potential_name.lower() for kw in ['whale', 'bottle', 'mesh', 'tallies', 'specification', 'source']):
                            material_name = potential_name
                    break
                j -= 1
            
            # Parse FMESH parameters (collect continuation lines)
            fmesh_lines = [line]
            k = i + 1
            while k < len(lines):
                next_line = lines[k].strip()
                if next_line.startswith(' ') or (next_line and not next_line.startswith('C') and not re.match(r'^[A-Za-z]', next_line)):
                    fmesh_lines.append(next_line)
                    k += 1
                elif next_line.upper().startswith('IMESH') or next_line.upper().startswith('JMESH') or \
                     next_line.upper().startswith('KMESH') or next_line.upper().startswith('EMESH') or \
                     next_line.upper().startswith('IINTS') or next_line.upper().startswith('JINTS') or \
                     next_line.upper().startswith('KINTS') or next_line.upper().startswith('OUT'):
                    fmesh_lines.append(next_line)
                    k += 1
                else:
                    break
            
            # Parse mesh dimensions
            full_fmesh = ' '.join(fmesh_lines)
            
            # Parse EMESH for energy groups
            emesh_match = re.search(r'EMESH\s*=?\s*([\d\s.eE+\-]+)', full_fmesh, re.IGNORECASE)
            energy_groups = []
            if emesh_match:
                emesh_str = emesh_match.group(1)
                energy_groups = [float(x) for x in emesh_str.split()]
            
            # Parse mesh dimensions (IINTS, JINTS, KINTS)
            iints_match = re.search(r'IINTS\s*=?\s*([\d\s]+)', full_fmesh, re.IGNORECASE)
            jints_match = re.search(r'JINTS\s*=?\s*([\d\s]+)', full_fmesh, re.IGNORECASE)
            kints_match = re.search(r'KINTS\s*=?\s*([\d\s]+)', full_fmesh, re.IGNORECASE)
            
            n_i = sum([int(x) for x in iints_match.group(1).split()]) if iints_match else 1
            n_j = sum([int(x) for x in jints_match.group(1).split()]) if jints_match else 1
            n_k = sum([int(x) for x in kints_match.group(1).split()]) if kints_match else 1
            
            # ================================================================
            # EXTRACT MESH COORDINATES (IMESH, JMESH, KMESH) FOR VOLUME CALCULATION
            # ================================================================
            # Parse origin (ORIGIN=x y z or ORIGIN x y z)
            origin = [0.0, 0.0, 0.0]
            origin_match = re.search(r'ORIGIN\s*=?\s*([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)', full_fmesh, re.IGNORECASE)
            if origin_match:
                origin = [float(origin_match.group(1)), float(origin_match.group(2)), float(origin_match.group(3))]
            
            # Parse IMESH coordinates (upper bounds of mesh intervals)
            imesh_match = re.search(r'IMESH\s*=?\s*([-\d.eE+\s]+?)(?=JMESH|KMESH|EMESH|IINTS|JINTS|KINTS|OUT|$)', full_fmesh, re.IGNORECASE)
            imesh_coords = [origin[0]]  # Start with origin
            if imesh_match:
                imesh_str = imesh_match.group(1).strip()
                imesh_vals = [float(x) for x in imesh_str.split() if x]
                imesh_coords.extend(imesh_vals)
            
            # Parse JMESH coordinates
            jmesh_match = re.search(r'JMESH\s*=?\s*([-\d.eE+\s]+?)(?=IMESH|KMESH|EMESH|IINTS|JINTS|KINTS|OUT|$)', full_fmesh, re.IGNORECASE)
            jmesh_coords = [origin[1]]
            if jmesh_match:
                jmesh_str = jmesh_match.group(1).strip()
                jmesh_vals = [float(x) for x in jmesh_str.split() if x]
                jmesh_coords.extend(jmesh_vals)
            
            # Parse KMESH coordinates
            kmesh_match = re.search(r'KMESH\s*=?\s*([-\d.eE+\s]+?)(?=IMESH|JMESH|EMESH|IINTS|JINTS|KINTS|OUT|$)', full_fmesh, re.IGNORECASE)
            kmesh_coords = [origin[2]]
            if kmesh_match:
                kmesh_str = kmesh_match.group(1).strip()
                kmesh_vals = [float(x) for x in kmesh_str.split() if x]
                kmesh_coords.extend(kmesh_vals)
            
            # Calculate voxel volumes from mesh coordinates
            # Each voxel is bounded by consecutive mesh coordinates
            voxel_volumes = []
            for ii in range(n_i):
                for jj in range(n_j):
                    for kk in range(n_k):
                        # Get voxel dimensions
                        dx = imesh_coords[ii+1] - imesh_coords[ii] if ii+1 < len(imesh_coords) else 1.0
                        dy = jmesh_coords[jj+1] - jmesh_coords[jj] if jj+1 < len(jmesh_coords) else 1.0
                        dz = kmesh_coords[kk+1] - kmesh_coords[kk] if kk+1 < len(kmesh_coords) else 1.0
                        vol = abs(dx * dy * dz)
                        voxel_volumes.append(vol)
            
            fmesh_data[tally_num] = {
                'material_name': material_name,
                'energy_groups': energy_groups,
                'n_groups': len(energy_groups),
                'mesh_dims': (n_i, n_j, n_k),
                'n_voxels': n_i * n_j * n_k,
                'origin': origin,
                'imesh': imesh_coords,
                'jmesh': jmesh_coords,
                'kmesh': kmesh_coords,
                'voxel_volumes': voxel_volumes,
            }
            
            total_volume = sum(voxel_volumes) if voxel_volumes else n_i * n_j * n_k
            print(f"  Found FMESH{tally_num}: material={material_name}, groups={len(energy_groups)}, voxels={n_i}x{n_j}x{n_k}={n_i*n_j*n_k}")
            print(f"    Mesh origin: ({origin[0]}, {origin[1]}, {origin[2]})")
            print(f"    Total mesh volume: {total_volume:.4f} cm³")
        
        i += 1
    
    return fmesh_data


def parse_mcnp_materials(mcnp_file, required_materials=None):
    """
    Parse MCNP input file to extract material definitions.
    
    Args:
        mcnp_file: Path to MCNP input file
        required_materials: Optional set of material names to look for.
                           If None, all materials are parsed.
    """
    materials = {}
    
    with open(mcnp_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        name_match = re.match(r'^C\s+name:\s*(.+)$', line, re.IGNORECASE)
        if name_match:
            material_name = name_match.group(1).strip()
            
            # Skip if not in required materials (if specified)
            if required_materials is not None and material_name not in required_materials:
                i += 1
                continue
            
            density = None
            mat_number = None
            isotopes = []
            
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                
                density_match = re.match(r'^C\s+density\s*=\s*([\d.eE+\-]+)', next_line, re.IGNORECASE)
                if density_match:
                    density = float(density_match.group(1))
                    j += 1
                    continue
                
                mat_match = re.match(r'^m(\d+)\s*$', next_line, re.IGNORECASE)
                if mat_match:
                    mat_number = mat_match.group(1)
                    j += 1
                    
                    while j < len(lines):
                        iso_line = lines[j].strip()
                        
                        # Match isotope lines: ZAID.XXc fraction (fraction can be negative for mass fractions)
                        iso_match = re.match(r'(\d+)\.(\d+c)\s+([-]?[\d.eE+\-]+)', iso_line)
                        if iso_match:
                            zaid = int(iso_match.group(1))
                            fraction = float(iso_match.group(3))
                            
                            Z = zaid // 1000
                            A = zaid % 1000
                            
                            isotopes.append((Z, A, abs(fraction)))  # Use absolute value
                            j += 1
                        elif iso_line.startswith('C name:') or re.match(r'^m\d+', iso_line, re.IGNORECASE):
                            # Hit next material definition
                            break
                        elif iso_line == '' or iso_line.startswith('C'):
                            # Skip empty lines and comments within material
                            j += 1
                        else:
                            j += 1
                    break
                
                if next_line.startswith('C name:') or (next_line and not next_line.startswith('C') and not next_line.startswith(' ')):
                    break
                
                j += 1
            
            if density is not None and isotopes:
                materials[material_name] = {
                    'density': density,
                    'mat_number': mat_number,
                    'isotopes': isotopes
                }
        
        i += 1
    
    return materials


# ============================================================================
# HDF5 EXTRACTION
# ============================================================================

def extract_mesh_tally_from_h5(h5_file, tally_number):
    """
    Extract mesh tally data from HDF5 file.
    """
    if not HAS_H5PY:
        return None
    
    tally_path = f'/results/mesh_tally/mesh_tally_{tally_number}'
    
    with h5py.File(h5_file, 'r') as f:
        if tally_path not in f:
            print(f"  Warning: Tally {tally_number} not found in HDF5 file")
            return None
        
        tally_group = f[tally_path]
        
        mean = tally_group['mean'][:]
        
        energy_bins = None
        if 'grid_energy' in tally_group:
            energy_bins = tally_group['grid_energy'][:]
        
        return {
            'mean': mean,
            'energy_bins': energy_bins,
            'shape': mean.shape
        }


# ============================================================================
# ALARA FILE GENERATION
# ============================================================================

def generate_alara_flux_file_per_voxel(tally_data, output_dir, tally_num, n_groups, library_groups=175):
    """
    Generate individual ALARA flux files for each voxel.
    
    HDF5 mesh tally structure (for 175 VITAMIN-J groups):
    - mean shape: (177, 1, n_i, n_j, n_k)
    - Index 0: unused (always 0)
    - Indices 1-175: flux for energy groups 1-175
    - Index 176: total flux (sum of all groups)
    
    ALARA expects flux in order from highest to lowest energy.
    
    Args:
        tally_data: Dict with 'mean' array and optional 'energy_bins'
        output_dir: Directory to write flux files
        tally_num: Tally number for naming
        n_groups: Number of energy groups from MCNP EMESH (should be 175)
        library_groups: Number of groups expected by ALARA library (default 175 for FENDL2)
    
    Returns:
        list: List of (voxel_id, flux_file_path, voxel_coords) tuples
    """
    mean = tally_data['mean']
    shape = mean.shape
    
    if len(shape) == 5:
        n_energy, n_time, n_i, n_j, n_k = shape
    elif len(shape) == 4:
        n_energy, n_i, n_j, n_k = shape
        n_time = 1
    else:
        print(f"  Warning: Unexpected data shape {shape}")
        return []
    
    # HDF5 has n_energy entries: index 0 unused, indices 1 to (n_energy-2) are groups, 
    # index (n_energy-1) is total
    # So actual number of groups = n_energy - 2
    actual_groups = n_energy - 2
    
    print(f"  HDF5 data: {n_energy} entries -> {actual_groups} energy groups + total")
    
    if actual_groups != library_groups:
        print(f"  WARNING: MCNP has {actual_groups} energy groups, library expects {library_groups}")
        if actual_groups < library_groups:
            print(f"           Padding with {library_groups - actual_groups} zero-flux high-energy groups")
        else:
            print(f"           Using only first {library_groups} groups")
    
    voxel_files = []
    voxel_id = 0
    
    for i in range(n_i):
        for j in range(n_j):
            for k in range(n_k):
                flux_file = os.path.join(output_dir, f"tally_{tally_num}_voxel_{voxel_id:04d}.flx")
                
                # Get flux for this voxel
                # Indices 1 to (actual_groups) contain the group fluxes
                # Index 0 is unused, index (actual_groups+1) is total
                if len(shape) == 5:
                    flux_raw = mean[1:actual_groups+1, 0, i, j, k][::-1]  # Reverse: high E first
                else:
                    flux_raw = mean[1:actual_groups+1, i, j, k][::-1]
                
                # Pad or truncate to match library group structure
                if actual_groups < library_groups:
                    # Pad with zeros so high-energy groups come first (ALARA expects high->low)
                    flux = np.zeros(library_groups)
                    # flux_raw is already reversed to high->low; place it at the start
                    flux[:actual_groups] = flux_raw
                elif actual_groups > library_groups:
                    # Truncate to library_groups (keep high energy groups)
                    flux = flux_raw[:library_groups]
                else:
                    flux = flux_raw
                
                with open(flux_file, 'w') as f:
                    flux_str = ' '.join([f'{v:.6e}' for v in flux])
                    f.write(f'{flux_str}\n')
                
                voxel_files.append((voxel_id, flux_file, (i, j, k)))
                voxel_id += 1
    
    print(f"  Written {voxel_id} voxel flux files ({library_groups} groups each)")
    return voxel_files


def generate_alara_matlib(material_name, material_data, matlib_file):
    """
    Generate ALARA material library file.
    
    ALARA matlib format uses element symbols (e.g., fe, cr) with mass percentages.
    ALARA looks up natural isotopic abundances from the element library.
    
    Note: MCNP provides explicit isotopic composition (e.g., fe-56: 91.7%), but
    ALARA requires element symbols and uses natural abundances. The MCNP isotopes
    are aggregated by element.
    
    Format:
        MATNAME  density  n_elements
                                  element  mass_percent  Z
    """
    density = material_data['density']
    isotopes = material_data['isotopes']
    
    # Aggregate isotopes by element (ALARA uses elements, not isotopes)
    element_weights = {}
    isotope_details = {}  # For informational output
    
    for Z, A, frac in isotopes:
        element = Z_TO_ELEMENT.get(Z, f'z{Z}')
        if element not in element_weights:
            element_weights[element] = {'Z': Z, 'weight': 0.0}
            isotope_details[element] = []
        element_weights[element]['weight'] += abs(frac)
        isotope_details[element].append((A, abs(frac)))
    
    # Normalize to 100%
    total_weight = sum(data['weight'] for data in element_weights.values())
    for elem in element_weights:
        element_weights[elem]['weight'] = (element_weights[elem]['weight'] / total_weight) * 100.0
    
    # Also normalize isotope details for comments
    for elem in isotope_details:
        total_elem = sum(frac for _, frac in isotope_details[elem])
        isotope_details[elem] = [(A, (frac/total_elem)*100.0) for A, frac in isotope_details[elem]]
    
    with open(matlib_file, 'w') as f:
        mat_name = material_name.upper().replace(' ', '_')
        
        # Header comments with isotopic detail from MCNP
        f.write(f"# Material: {material_name}\n")
        f.write(f"# Source: MCNP isotopic composition\n")
        f.write(f"# Note: ALARA uses natural abundances from element library\n")
        f.write(f"# MCNP isotopic breakdown (for reference):\n")
        for elem, isos in sorted(isotope_details.items(), key=lambda x: element_weights[x[0]]['Z']):
            iso_str = ", ".join([f"{elem}-{A}: {pct:.2f}%" for A, pct in sorted(isos)])
            f.write(f"#   {elem}: {iso_str}\n")
        f.write("#\n")
        
        # Actual ALARA format: element symbols
        f.write(f"{mat_name:<8} {density:.5e}  {len(element_weights):2d}\n")
        
        for elem, data in sorted(element_weights.items(), key=lambda x: x[1]['Z']):
            weight_pct = data['weight']
            Z = data['Z']
            f.write(f"                              {elem:<2} {weight_pct:.5e} {Z:3d}\n")
    
    return mat_name


def generate_custom_elelib(material_data, elelib_file, base_elelib=None):
    """
    Generate a custom element library with MCNP isotopic ratios.
    
    ALARA element library format:
        element  atomic_mass  Z  density  n_isotopes
                                                    mass_number  abundance_percent
                                                    mass_number  abundance_percent
                                                    ...
    
    This function creates element entries with the exact isotopic ratios from MCNP,
    allowing ALARA to use the actual composition instead of natural abundances.
    
    Args:
        material_data: Dict with 'isotopes' list of (Z, A, frac) tuples
        elelib_file: Output file path for custom element library
        base_elelib: Optional path to base element library to copy unmodified elements from
    """
    isotopes = material_data['isotopes']
    
    # Group isotopes by element
    elements = {}
    for Z, A, frac in isotopes:
        element = Z_TO_ELEMENT.get(Z, f'z{Z}')
        if element not in elements:
            elements[element] = {'Z': Z, 'isotopes': [], 'total_frac': 0.0}
        elements[element]['isotopes'].append((A, abs(frac)))
        elements[element]['total_frac'] += abs(frac)
    
    # Calculate average atomic mass and normalize abundances for each element
    for elem, data in elements.items():
        # Normalize to 100% and calculate weighted average atomic mass
        total = data['total_frac']
        data['abundances'] = [(A, (frac/total)*100.0) for A, frac in data['isotopes']]
        # Weighted average atomic mass
        data['avg_mass'] = sum(A * (frac/total) for A, frac in data['isotopes'])
    
    # Standard element densities (g/cm³) - used as placeholder
    ELEMENT_DENSITIES = {
        'h': 0.0899e-3, 'he': 0.1787e-3, 'li': 0.53, 'be': 1.85, 'b': 2.34, 'c': 2.62,
        'n': 1.251e-3, 'o': 1.429e-3, 'f': 1.696e-3, 'ne': 0.901e-3, 'na': 0.97, 'mg': 1.74,
        'al': 2.70, 'si': 2.33, 'p': 1.82, 's': 2.07, 'cl': 3.17e-3, 'ar': 1.784e-3,
        'k': 0.86, 'ca': 1.55, 'sc': 3.00, 'ti': 4.50, 'v': 5.80, 'cr': 7.19,
        'mn': 7.43, 'fe': 7.86, 'co': 8.90, 'ni': 8.90, 'cu': 8.96, 'zn': 7.14,
        'ga': 5.91, 'ge': 5.32, 'as': 5.72, 'se': 4.80, 'br': 3.12, 'kr': 3.74e-3,
        'rb': 1.53, 'sr': 2.60, 'y': 4.50, 'zr': 6.49, 'nb': 8.55, 'mo': 10.2,
        'ru': 12.2, 'rh': 12.4, 'pd': 12.0, 'ag': 10.5, 'cd': 8.65, 'in': 7.31,
        'sn': 7.30, 'sb': 6.68, 'te': 6.24, 'i': 4.92, 'xe': 5.89e-3, 'cs': 1.87,
        'ba': 3.50, 'la': 6.70, 'ce': 6.78, 'pr': 6.77, 'nd': 7.00, 'sm': 7.54,
        'eu': 5.26, 'gd': 7.89, 'tb': 8.27, 'dy': 8.54, 'ho': 8.80, 'er': 9.05,
        'tm': 9.33, 'yb': 6.98, 'lu': 9.84, 'hf': 13.1, 'ta': 16.6, 'w': 19.3,
        're': 21.0, 'os': 22.4, 'ir': 22.5, 'pt': 21.4, 'au': 19.3, 'hg': 13.53,
        'tl': 11.85, 'pb': 11.4, 'bi': 9.80, 'th': 11.7, 'u': 18.9
    }
    
    with open(elelib_file, 'w') as f:
        f.write("# Custom element library with MCNP isotopic ratios\n")
        f.write("# Generated automatically - DO NOT use natural abundance assumptions\n")
        f.write("#\n")
        f.write("# Format: element  atomic_mass  Z  density  n_isotopes\n")
        f.write("#                                                 mass_number  abundance_%\n")
        f.write("#\n")
        
        for elem in sorted(elements.keys(), key=lambda x: elements[x]['Z']):
            data = elements[elem]
            Z = data['Z']
            avg_mass = data['avg_mass']
            density = ELEMENT_DENSITIES.get(elem, 1.0)
            n_isos = len(data['abundances'])
            
            # Element header line
            f.write(f"{elem:<8}{avg_mass:.6E}  {Z:2d}      {density:.3E}   {n_isos}\n")
            
            # Isotope lines (sorted by mass number)
            for A, abundance in sorted(data['abundances']):
                f.write(f"                                                {A:3d}      {abundance:.4E}\n")
    
    print(f"  Written custom element library: {elelib_file}")
    print(f"    - {len(elements)} elements with MCNP isotopic ratios")
    return elelib_file


def generate_combined_flux_file(tally_data, output_file, n_groups, library_groups=175, 
                                flux_norm=None):
    """
    Generate a single combined flux file for all voxels.
    
    ALARA expects flux values for all zones/intervals concatenated in a single file.
    Each zone gets one set of N energy group values, in high-to-low energy order.
    The flux file should NOT contain comments (ALARA reads flux values only).
    
    Args:
        tally_data: Dict with 'mean' array from HDF5
        output_file: Path for the combined flux file
        n_groups: Number of energy groups from MCNP
        library_groups: Number of groups expected by the library (default 175)
        flux_norm: Normalization factor (source strength in n/s). If None, uses FLUX_NORMALIZATION.
    
    Returns:
        List of voxel info tuples: [(voxel_id, (i, j, k)), ...]
    """
    if flux_norm is None:
        flux_norm = FLUX_NORMALIZATION
    
    mean = tally_data['mean']
    shape = mean.shape
    
    # Determine mesh dimensions based on array shape
    if len(shape) == 5:
        n_energy, n_t, n_i, n_j, n_k = shape
        n_time = n_t
    elif len(shape) == 4:
        n_energy, n_i, n_j, n_k = shape
        n_time = 1
    else:
        print(f"  Warning: Unexpected data shape {shape}")
        return []
    
    # HDF5 has n_energy entries: index 0 unused, indices 1 to (n_energy-2) are groups, 
    # index (n_energy-1) is total
    actual_groups = n_energy - 2
    
    voxel_info = []
    voxel_id = 0
    
    with open(output_file, 'w') as f:
        # NOTE: ALARA flux files should NOT contain comments!
        # Just write the flux values, one set per zone
        
        for i in range(n_i):
            for j in range(n_j):
                for k in range(n_k):
                    # Get flux for this voxel
                    # Indices 1 to (actual_groups) contain the group fluxes
                    if len(shape) == 5:
                        flux_raw = mean[1:actual_groups+1, 0, i, j, k][::-1]  # Reverse: high E first
                    else:
                        flux_raw = mean[1:actual_groups+1, i, j, k][::-1]
                    
                    # Apply flux normalization (MCNP values are per source particle)
                    flux_raw = flux_raw * flux_norm
                    
                    # Pad or truncate to match library group structure
                    if actual_groups < library_groups:
                        # Pad with zeros - high-energy groups come first (ALARA expects high->low)
                        flux = np.zeros(library_groups)
                        flux[:actual_groups] = flux_raw
                    elif actual_groups > library_groups:
                        # Truncate to library_groups (keep high energy groups)
                        flux = flux_raw[:library_groups]
                    else:
                        flux = flux_raw
                    
                    # Write flux values for this voxel
                    # Use standard ALARA format: 6 values per line
                    for g in range(0, library_groups, 6):
                        line_values = flux[g:min(g+6, library_groups)]
                        line_str = ' '.join([f'{v:.5E}' for v in line_values])
                        f.write(f' {line_str}\n')
                    
                    voxel_info.append((voxel_id, (i, j, k)))
                    voxel_id += 1
    
    print(f"  Written combined flux file with {voxel_id} voxels ({library_groups} groups each)")
    print(f"  Flux normalization applied: {flux_norm:.3e} n/s")
    return voxel_info


def generate_flux_file_from_csv(csv_file, output_file, library_groups=175):
    """
    Generate ALARA flux file from a spectrum CSV file.
    
    The CSV file should have columns: E_low[eV], E_high[eV], flux_bin [n·s⁻¹], ...
    The flux_bin column contains the total flux in each energy bin (already absolute, not per source particle).
    
    This creates a single-zone flux file with the spectrum from the CSV.
    ALARA expects flux in high-to-low energy order.
    
    Args:
        csv_file: Path to the spectrum CSV file
        output_file: Path for the ALARA flux file  
        library_groups: Number of groups expected by the library (default 175)
        
    Returns:
        List with single voxel info: [(0, (0, 0, 0))]
    """
    import pandas as pd
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Expected column for flux - try different possible names
    flux_col = None
    for col in ['flux_bin [n·s⁻¹]', 'flux_bin', 'flux', 'Flux']:
        if col in df.columns:
            flux_col = col
            break
    
    if flux_col is None:
        # Try to find a column that looks like flux
        for col in df.columns:
            if 'flux' in col.lower() and 'err' not in col.lower() and 'per' not in col.lower():
                flux_col = col
                break
    
    if flux_col is None:
        raise ValueError(f"Could not find flux column in CSV. Available columns: {list(df.columns)}")
    
    print(f"  Using flux column: '{flux_col}'")
    
    # Get flux values (CSV is typically low-to-high energy, ALARA needs high-to-low)
    flux_raw = df[flux_col].values
    n_groups_csv = len(flux_raw)
    
    print(f"  CSV energy groups: {n_groups_csv}")
    print(f"  Total flux: {flux_raw.sum():.3e} n/s")
    print(f"  NOTE: Using CSV spectrum creates SINGLE-ZONE geometry (1 voxel with averaged flux)")
    print(f"        For multi-zone analysis, use --h5 to extract per-voxel flux from mesh tally")
    
    # Reverse to high-to-low energy order (ALARA convention)
    flux_high_to_low = flux_raw[::-1]
    
    # Pad or truncate to match library group structure
    if n_groups_csv < library_groups:
        # Pad with zeros at the end (low energy side)
        flux = np.zeros(library_groups)
        flux[:n_groups_csv] = flux_high_to_low
        print(f"  Padded from {n_groups_csv} to {library_groups} groups (zeros at low energy)")
    elif n_groups_csv > library_groups:
        # Truncate to library_groups (keep high energy groups)
        flux = flux_high_to_low[:library_groups]
        print(f"  Truncated from {n_groups_csv} to {library_groups} groups")
    else:
        flux = flux_high_to_low
        print(f"  Groups match library ({library_groups})")
    
    # Write flux file
    with open(output_file, 'w') as f:
        # Write flux values for single zone
        # Use standard ALARA format: 6 values per line
        for g in range(0, library_groups, 6):
            line_values = flux[g:min(g+6, library_groups)]
            line_str = ' '.join([f'{v:.5E}' for v in line_values])
            f.write(f' {line_str}\n')
    
    print(f"  Written flux file: {output_file}")
    print(f"  Single zone with {library_groups} energy groups")
    
    # Return single voxel info (single zone geometry)
    return [(0, (0, 0, 0))]


def generate_combined_flux_file_from_csv(csv_file, output_file, library_groups, tally_data, n_groups_h5):
    """
    Generate multi-zone ALARA flux file using CSV spectrum for ALL voxels.
    
    This applies the same spectrum from the CSV to all voxels extracted from HDF5 mesh tally,
    allowing multi-zone geometry with a uniform (averaged/representative) spectrum.
    
    Args:
        csv_file: Path to the spectrum CSV file
        output_file: Path for the ALARA flux file
        library_groups: Number of groups expected by the library (default 175)
        tally_data: Mesh tally data extracted from HDF5 (contains voxel geometry)
        n_groups_h5: Number of energy groups in HDF5 mesh tally
        
    Returns:
        List of (voxel_id, (i, j, k)) tuples for each voxel
    """
    import pandas as pd
    
    # Read the CSV spectrum
    df = pd.read_csv(csv_file)
    
    # Find flux column
    flux_col = None
    for col in ['flux_bin [n·s⁻¹]', 'flux_bin', 'flux', 'Flux']:
        if col in df.columns:
            flux_col = col
            break
    
    if flux_col is None:
        for col in df.columns:
            if 'flux' in col.lower() and 'err' not in col.lower() and 'per' not in col.lower():
                flux_col = col
                break
    
    if flux_col is None:
        raise ValueError(f"Could not find flux column in CSV. Available columns: {list(df.columns)}")
    
    print(f"  Using flux column from CSV: '{flux_col}'")
    
    # Get flux values and reverse to high-to-low energy order
    flux_raw = df[flux_col].values
    n_groups_csv = len(flux_raw)
    flux_high_to_low = flux_raw[::-1]
    
    print(f"  CSV energy groups: {n_groups_csv}")
    print(f"  Total flux from CSV: {flux_raw.sum():.3e} n/s")
    
    # Pad or truncate to match library group structure
    if n_groups_csv < library_groups:
        flux = np.zeros(library_groups)
        flux[:n_groups_csv] = flux_high_to_low
        print(f"  Padded from {n_groups_csv} to {library_groups} groups (zeros at low energy)")
    elif n_groups_csv > library_groups:
        flux = flux_high_to_low[:library_groups]
        print(f"  Truncated from {n_groups_csv} to {library_groups} groups")
    else:
        flux = flux_high_to_low
    
    # Extract voxel geometry from HDF5
    mesh_shape = tally_data['shape']
    
    # Handle both 4D and 5D shapes
    if len(mesh_shape) == 5:
        ng, n_t, ni, nj, nk = mesh_shape
    elif len(mesh_shape) == 4:
        ng, ni, nj, nk = mesh_shape
    else:
        raise ValueError(f"Unexpected HDF5 shape: {mesh_shape}")
    
    n_voxels = ni * nj * nk
    
    print(f"  Applying CSV spectrum to {n_voxels} voxels from HDF5 ({ni}×{nj}×{nk})")
    
    # Create voxel info list
    voxel_info = []
    voxel_id = 0
    for i in range(ni):
        for j in range(nj):
            for k in range(nk):
                voxel_info.append((voxel_id, (i, j, k)))
                voxel_id += 1
    
    # Write flux file with same spectrum for all voxels
    # NOTE: ALARA flux files should NOT contain comments!
    with open(output_file, 'w') as f:
        for vid, (i, j, k) in voxel_info:
            # Write flux values (6 per line) - NO comments
            for g in range(0, library_groups, 6):
                line_values = flux[g:min(g+6, library_groups)]
                line_str = ' '.join([f'{v:.5E}' for v in line_values])
                f.write(f' {line_str}\n')
    
    print(f"  Written flux file: {output_file}")
    print(f"  {n_voxels} zones, each with {library_groups} energy groups from CSV")
    
    return voxel_info


def generate_multizone_alara_input(material_name, material_data, voxel_info, 
                                    combined_flux_file, output_file, n_groups, 
                                    library='fendl2', mesh_dims=None,
                                    voxel_volumes=None, elelib_file=None,
                                    matlib_file=None, schedules=None):
    """
    Generate a single ALARA input file with all voxels as separate zones.
    
    Supports DUAL-PHASE irradiation schedules (3s + 2h) in a single run.
    Uses material_lib and element_lib for proper ALARA material definition.
    
    Args:
        material_name: Name of the material
        material_data: Dict with 'density', 'isotopes'
        voxel_info: List of (voxel_id, (i, j, k)) tuples
        combined_flux_file: Path to combined flux file
        output_file: Path for ALARA input file
        n_groups: Number of energy groups
        library: Library name ('fendl2' or 'fendl3_new')
        mesh_dims: Optional (ni, nj, nk) mesh dimensions 
        voxel_volumes: Optional list of volumes for each voxel (cm³)
        elelib_file: Path to custom element library with MCNP isotopic ratios (REQUIRED)
        schedules: List of schedule dicts with keys 'irradiation_time' and 'cooling_times'.
                   Example: [{'irradiation_time': '3 s', 'cooling_times': ['6.00 m', '2 h']},
                             {'irradiation_time': '2 h', 'cooling_times': ['15 d']}]
    """
    # Default to single-phase global schedule if not provided
    if schedules is None:
        schedules = [{'irradiation_time': IRRADIATION_TIME, 'cooling_times': COOLING_TIMES}]
    
    density = material_data['density']
    mat_name = material_name.upper().replace(' ', '_')
    zone_base = material_name.lower().replace(' ', '_')
    
    # Get library paths
    lib_info = LIBRARY_PATHS.get(library, LIBRARY_PATHS[DEFAULT_LIBRARY])
    
    n_voxels = len(voxel_info)
    
    # Calculate default volume if not provided (assume 1 cm³ each)
    if voxel_volumes is None:
        voxel_volumes = [1.0] * n_voxels
    
    # Build cooling times list for dual-phase schedule
    # Phase 1 cooling times are relative to end of Phase 1
    # Phase 2 cooling times need to be offset by: (delay to Phase 2 start + Phase 2 irr duration + Phase 2 cooling)
    all_cooling_times = []
    
    if len(schedules) == 1:
        # Single phase - use cooling times as-is
        all_cooling_times = schedules[0].get('cooling_times', [])
    else:
        # Multi-phase: combine Phase 1 times + offset Phase 2 times
        phase1 = schedules[0]
        phase2 = schedules[1] if len(schedules) > 1 else None
        
        # Add Phase 1 cooling times
        phase1_times = phase1.get('cooling_times', [])
        all_cooling_times.extend(phase1_times)
        
        # Calculate Phase 2 offset times
        if phase2 and phase1_times:
            # Phase 2 starts after last Phase 1 measurement
            delay_seconds = parse_time_to_seconds(phase1_times[-1])
            # Add Phase 2 irradiation duration
            phase2_irr = phase2.get('irradiation_time', '2 h')
            delay_seconds += parse_time_to_seconds(phase2_irr)
            
            # Add Phase 2 cooling times with offset
            for ct in phase2.get('cooling_times', []):
                ct_seconds = parse_time_to_seconds(ct)
                total_seconds = delay_seconds + ct_seconds
                offset_time = seconds_to_alara_time(total_seconds)
                all_cooling_times.append(offset_time)
    
    with open(output_file, 'w') as f:
        f.write(f"# ALARA Multi-Zone Activation Analysis\n")
        f.write(f"# Material: {material_name}\n")
        f.write(f"# Total voxels/zones: {n_voxels}\n")
        if len(schedules) == 1:
            f.write(f"# Irradiation: {schedules[0].get('irradiation_time', 'N/A')}\n")
            f.write(f"# Cooling times: {', '.join(schedules[0].get('cooling_times', []))}\n")
        else:
            f.write(f"# Dual-phase irradiation schedule:\n")
            f.write(f"#   Phase 1: {schedules[0].get('irradiation_time', 'N/A')} → cool → measure\n")
            f.write(f"#   Phase 2: {schedules[1].get('irradiation_time', 'N/A')} → cool → measure\n")
        f.write(f"# Library: {lib_info['description']}\n")
        f.write(f"# Generated automatically from MCNP mesh tally data\n\n")
        
        # Geometry
        f.write("geometry rectangular\n\n")
        
        # Use volumes block - define each voxel as a separate zone
        f.write("# Zone volumes (one entry per voxel)\n")
        f.write("volumes\n")
        for voxel_id, coords in voxel_info:
            zone_name = f"zone_{voxel_id:04d}"
            volume = voxel_volumes[voxel_id] if voxel_id < len(voxel_volumes) else 1.0
            f.write(f"    {volume:.6e}  {zone_name}\n")
        f.write("end\n\n")
        
        # Material loading - all zones use the same mixture
        f.write("# Material loading (all zones use same material)\n")
        f.write("mat_loading\n")
        for voxel_id, coords in voxel_info:
            zone_name = f"zone_{voxel_id:04d}"
            f.write(f"    {zone_name}  mix_{zone_base}\n")
        f.write("end\n\n")
        
        # Libraries - use BOTH material_lib and element_lib
        if matlib_file:
            f.write(f"material_lib {os.path.basename(matlib_file)}\n")
        if elelib_file:
            f.write(f"element_lib {os.path.basename(elelib_file)}\n")
            f.write("# NOTE: Using custom element library with MCNP isotopic ratios\n\n")
        else:
            f.write(f"element_lib {ELEMENT_LIB}\n")
            f.write("# NOTE: Using standard element library (natural abundances)\n\n")
        
        # Mixture (single mixture for all zones)
        # Use elemental composition directly from element library
        f.write(f"mixture mix_{zone_base}\n")
        f.write(f"    material {mat_name} 1.0 {density}\n")
        f.write("end\n\n")
        
        # Flux - single flux definition referencing combined file
        f.write(f"flux flux_1 {os.path.basename(combined_flux_file)} 1.0 0 default\n\n")
        
        # ================================================================
        # DUAL-PHASE IRRADIATION SCHEDULE WITH COOLING BETWEEN PHASES
        # ================================================================
        # Phase 1: Short irradiation (3s) → cooling measurements
        # Phase 2: Long irradiation (2h) starts AFTER Phase 1 cooling completes → cooling measurements
        #
        # In ALARA, use a multi-pulse schedule where Phase 2 starts after Phase 1's last measurement
        
        if len(schedules) == 1:
            # Single phase schedule
            sched = schedules[0]
            irr_time = sched.get('irradiation_time', IRRADIATION_TIME)
            
            f.write("# Irradiation schedule (single phase)\n")
            f.write("schedule irradiation\n")
            f.write(f"    {irr_time} flux_1 pulse_once 0 s\n")
            f.write("end\n\n")
            
            f.write("pulsehistory pulse_once\n")
            f.write("    1 0 s\n")
            f.write("end\n\n")
        else:
            # Multi-phase schedule: irradiate → cool → irradiate again → cool
            # Get Phase 1 and Phase 2 info
            phase1 = schedules[0]
            phase2 = schedules[1] if len(schedules) > 1 else None
            
            phase1_irr = phase1.get('irradiation_time', '3 s')
            phase1_times = phase1.get('cooling_times', [])
            
            # Phase 2 starts after last Phase 1 measurement
            # Use last Phase 1 cooling time as the delay before Phase 2
            if phase1_times:
                delay_to_phase2 = phase1_times[-1]  # e.g., "4 d"
            else:
                delay_to_phase2 = "0 s"
            
            f.write("# Dual-phase irradiation schedule\n")
            f.write("# Phase 1: Short irradiation for short-term measurements\n")
            f.write("# Phase 2: Long irradiation starting after Phase 1 cooling completes\n")
            f.write("schedule irradiation\n")
            f.write(f"    {phase1_irr} flux_1 pulse_phase1 0 s\n")
            
            if phase2:
                phase2_irr = phase2.get('irradiation_time', '2 h')
                f.write(f"    {phase2_irr} flux_1 pulse_phase2 {delay_to_phase2}\n")
            
            f.write("end\n\n")
            
            # Separate pulse histories for each phase
            f.write("pulsehistory pulse_phase1\n")
            f.write("    1 0 s\n")
            f.write("end\n\n")
            
            if phase2:
                f.write("pulsehistory pulse_phase2\n")
                f.write("    1 0 s\n")
                f.write("end\n\n")
        
        # Cooling times - from Phase 1 only
        f.write("# Cooling times\n")
        if len(schedules) == 1:
            f.write("# Measurement times after Phase 1 irradiation\n")
        else:
            f.write("# Phase 1 measurements, then Phase 2 measurements (offset by delay + Phase 2 irr)\n")
        f.write("cooling\n")
        for ct in all_cooling_times:
            f.write(f"    {ct}\n")
        f.write("end\n\n")
        
        # Data library
        f.write(f"data_library alaralib {lib_info['data_library']}\n\n")
        
        # Dump file
        dump_file = os.path.basename(output_file).replace('.inp', '.dump')
        f.write(f"dump_file {dump_file}\n\n")
        
        # ================================================================
        # COMPREHENSIVE OUTPUT OPTIONS
        # ================================================================
        f.write("# ============================================================\n")
        f.write("# COMPREHENSIVE OUTPUT OPTIONS\n")
        f.write("# All isotopes, all cooling times, full breakdown per zone\n")
        f.write("# ============================================================\n\n")
        
        # Zone-based output with constituent breakdown
        f.write("output zone\n")
        f.write("    units Bq cm3\n")
        f.write("    # Show breakdown by constituent (parent nuclide)\n")
        f.write("    constituent\n")
        f.write("    # Isotopic concentration [atoms/cm³]\n")
        f.write("    number_density\n")
        f.write("    # Activity [Bq/cm³]\n")
        f.write("    specific_activity\n")
        f.write("    # Decay heat breakdown [W/cm³]\n")
        f.write("    total_heat\n")
        f.write("    alpha_heat\n")
        f.write("    beta_heat\n")
        f.write("    gamma_heat\n")
        
        # Photon source
        if lib_info.get('gamma_lib'):
            photon_output = os.path.basename(output_file).replace('.inp', '.photonSrc')
            # Use dedicated gamma library file if available, otherwise use main library
            gamma_file = lib_info.get('gamma_lib_file', lib_info['gamma_lib'])
            f.write("    # Photon source spectrum [gammas/s/cm³]\n")
            f.write(f"    photon_source {gamma_file} {photon_output} 5 1e4 1e5 1e6 5e6 1e7\n")
        
        f.write("end\n\n")
        
        # Truncation and impurity settings
        f.write("# Truncation settings (1e-12 keeps essentially ALL isotopes)\n")
        f.write("truncation 1e-12\n\n")
        f.write("# Impurity threshold (relative, absolute)\n")
        f.write("impurity 1e-8 1e-10\n\n")
    
    print(f"  Written multi-zone ALARA input: {output_file}")
    print(f"    - {n_voxels} zones defined")
    return True


def generate_alara_input_comprehensive(material_name, material_data, flux_file, output_file,
                                        n_groups, matlib_file, library='fendl2', voxel_id=None):
    """
    Generate comprehensive ALARA input file with all output options.
    (Single-voxel version - kept for compatibility)
    
    Outputs requested:
    - Nuclide inventories (atoms, grams) vs. time
    - Nuclide-specific activities (Bq, Bq/g) vs. time  
    - Total activity of the sample (Bq, Bq/g) vs. time
    - Decay heat / total power (W, W/g) vs. time
    - Photon (gamma) source spectrum vs. time
    - Transmutation products and changes in isotopic composition
    - Dominant contributor analysis
    """
    density = material_data['density']
    
    mat_name = material_name.upper().replace(' ', '_')
    zone_name = material_name.lower().replace(' ', '_')
    
    # Get library paths
    lib_info = LIBRARY_PATHS.get(library, LIBRARY_PATHS[DEFAULT_LIBRARY])
    
    with open(output_file, 'w') as f:
        f.write(f"# ALARA Comprehensive Activation Analysis\n")
        f.write(f"# Material: {material_name}\n")
        if voxel_id is not None:
            f.write(f"# Voxel ID: {voxel_id}\n")
        f.write(f"# Irradiation: {IRRADIATION_TIME}\n")
        f.write(f"# Library: {lib_info['description']}\n")
        f.write(f"# Generated automatically from MCNP mesh tally data\n\n")
        
        # Geometry
        f.write("geometry rectangular\n\n")
        
        # Dimension - single zone for each voxel
        f.write("dimension x\n")
        f.write("    0.0\n")
        f.write("    1    1.0\n")
        f.write("end\n\n")
        
        # Material loading
        f.write("mat_loading\n")
        f.write(f"    zone_1 mix_{zone_name}\n")
        f.write("end\n\n")
        
        # Libraries
        f.write(f"material_lib {matlib_file}\n")
        f.write(f"element_lib {ELEMENT_LIB}\n\n")
        
        # Mixture
        f.write(f"mixture mix_{zone_name}\n")
        f.write(f"    material {mat_name} 1.0 {density}\n")
        f.write("end\n\n")
        
        # Flux
        f.write(f"flux flux_1 {flux_file} 1.0 0 default\n\n")
        
        # Schedule - hardcoded 2 hour irradiation
        f.write("schedule irradiation\n")
        f.write(f"    {IRRADIATION_TIME} flux_1 pulse_once 0 s\n")
        f.write("end\n\n")
        
        # Pulse history
        f.write("pulsehistory pulse_once\n")
        f.write("    1 0 s\n")
        f.write("end\n\n")
        
        # Cooling times - hardcoded
        f.write("cooling\n")
        for ct in COOLING_TIMES:
            f.write(f"    {ct}\n")
        f.write("end\n\n")
        
        # Data library
        f.write(f"data_library alaralib {lib_info['data_library']}\n\n")
        
        # Dump file for restart capability (use basename to keep in same directory)
        dump_file = os.path.basename(output_file).replace('.inp', '.dump')
        f.write(f"dump_file {dump_file}\n\n")
        
        # ================================================================
        # COMPREHENSIVE OUTPUT OPTIONS
        # ================================================================
        # 
        # ALARA output types available:
        #   number_density   - isotopic concentration [atoms/cm³ or atoms/kg]
        #   specific_activity - activity [Bq/cm³ or Ci/cm³]
        #   total_heat       - total decay heat [W/cm³]
        #   alpha_heat       - alpha particle decay heat [W/cm³]
        #   beta_heat        - beta particle decay heat [W/cm³]
        #   gamma_heat       - gamma ray decay heat [W/cm³]
        #   photon_source    - gamma source spectrum [gammas/s/cm³]
        #   constituent      - breakdown by parent nuclide
        #
        # Units options:
        #   units <activity> <norm>
        #   activity: Bq or Ci
        #   norm: cm3, m3, g, kg, or vol_int (volume integrated)
        #
        # NOTE: ALARA does not have a direct "mass" output.
        # To get isotopic mass, multiply number_density by atomic mass / Avogadro's number:
        #   mass [g/cm³] = number_density [atoms/cm³] × A [g/mol] / (6.022e23 [atoms/mol])
        #
        # ================================================================
        
        f.write("# ============================================================\n")
        f.write("# COMPREHENSIVE OUTPUT OPTIONS\n")
        f.write("# All isotopes, all cooling times, full breakdown\n")
        f.write("# ============================================================\n\n")
        
        # Zone-based output with constituent breakdown (per-zone results)
        # This gives results for ALL isotopes at ALL cooling times
        f.write("output zone\n")
        f.write("    units Bq cm3\n")
        f.write("    # Show breakdown by constituent (parent nuclide)\n")
        f.write("    constituent\n")
        f.write("    # Isotopic concentration [atoms/cm³]\n")
        f.write("    number_density\n")
        f.write("    # Activity [Bq/cm³]\n")
        f.write("    specific_activity\n")
        f.write("    # Decay heat breakdown [W/cm³]\n")
        f.write("    total_heat\n")
        f.write("    alpha_heat\n")
        f.write("    beta_heat\n")
        f.write("    gamma_heat\n")
        
        # Photon source - requires gamma library and energy group boundaries
        if lib_info.get('gamma_lib'):
            photon_output = os.path.basename(output_file).replace('.inp', '.photonSrc')
            # Use dedicated gamma library file if available, otherwise use main library
            gamma_file = lib_info.get('gamma_lib_file', lib_info['gamma_lib'])
            # 5 gamma energy groups (same format as sample5)
            # Groups span: 10keV to 10MeV
            f.write("    # Photon source spectrum [gammas/s/cm³]\n")
            f.write(f"    photon_source {gamma_file} {photon_output} 5 1e4 1e5 1e6 5e6 1e7\n")
        
        f.write("end\n\n")
        
        # Truncation for numerical stability (lower = more isotopes tracked)
        f.write("# Truncation settings (1e-12 keeps essentially ALL isotopes)\n")
        f.write("truncation 1e-12\n\n")
        
        # Impurity settings (relative threshold, absolute threshold)
        f.write("# Impurity threshold (relative, absolute)\n")
        f.write("impurity 1e-8 1e-10\n\n")
    
    return True


# ============================================================================
# ALARA EXECUTION AND OUTPUT PARSING
# ============================================================================

def run_alara(input_file, output_dir):
    """
    Run ALARA on an input file and capture output.
    """
    output_file = os.path.join(output_dir, input_file.replace('.inp', '.out'))
    
    try:
        result = subprocess.run(
            [ALARA_EXECUTABLE, input_file],
            capture_output=True,
            text=True,
            cwd=output_dir,
            timeout=300  # 5 minute timeout
        )
        
        # Save output
        with open(output_file, 'w') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\n=== STDERR ===\n")
                f.write(result.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        print(f"    Warning: ALARA timed out for {input_file}")
        return False, "", "Timeout"
    except Exception as e:
        print(f"    Error running ALARA: {e}")
        return False, "", str(e)


def parse_alara_output(output_text):
    """
    Parse ALARA output text to extract results for multiple zones.
    
    Returns:
        dict: Dictionary mapping voxel_id (int) to results dict
    """
    all_results = {}
    current_voxel_id = None
    current_results = None
    
    current_quantity = None
    
    lines = output_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect Zone header
        # Zone #1: zone_0000
        zone_match = re.match(r'Zone #(\d+):\s*zone_(\d+)', line)
        if zone_match:
            # Save previous results if any
            if current_voxel_id is not None and current_results:
                all_results[current_voxel_id] = current_results
            
            # Start new zone
            current_voxel_id = int(zone_match.group(2))
            current_results = {
                'specific_activity': {},  # Bq/cm³
                'total_heat': {},         # W/cm³
                'number_density': {},     # atoms/cm³
                'photon_source': {},      # photons/s/cm³
                'isotopes': {},           # Per-isotope breakdown
                'total_specific_activity': [],
                'total_total_heat': [],
            }
            current_quantity = None
        
        # Detect section headers within a zone
        if 'Specific Activity' in line and 'Bq' in line:
            current_quantity = 'specific_activity'
        elif 'Total Decay Heat' in line or 'total_heat' in line.lower():
            current_quantity = 'total_heat'
        elif 'Number Density' in line:
            current_quantity = 'number_density'
        elif 'Photon Source' in line:
            current_quantity = 'photon_source'
        
        # Parse data lines (isotope data)
        if current_results and current_quantity and line and not line.startswith('=') and not line.startswith('isotope') and not line.startswith('Zone'):
            parts = line.split()
            if len(parts) >= 2:
                try:
                    isotope = parts[0]
                    # Check if first value is numeric (isotope data line)
                    values = []
                    for p in parts[1:]:
                        try:
                            values.append(float(p))
                        except ValueError:
                            break
                    
                    if values:
                        if isotope == 'total':
                            # Store total for the current quantity
                            if current_quantity == 'specific_activity':
                                current_results['total_specific_activity'] = values
                            elif current_quantity == 'total_heat':
                                current_results['total_total_heat'] = values
                            
                            # Also store in generic total_quantity
                            current_results[f'total_{current_quantity}'] = values
                        elif isotope != 'zone' and not isotope.startswith('Zone'):
                            if isotope not in current_results['isotopes']:
                                current_results['isotopes'][isotope] = {}
                            current_results['isotopes'][isotope][current_quantity] = values
                
                except (ValueError, IndexError):
                    pass
        
        i += 1
    
    # Save last zone
    if current_voxel_id is not None and current_results:
        all_results[current_voxel_id] = current_results
        
    return all_results


def calculate_averages(all_voxel_results):
    """
    Calculate average values across all voxels for each quantity and cooling time.
    
    Returns:
        dict: Averaged results
    """
    if not all_voxel_results:
        return {}
    
    averages = {
        'n_voxels': len(all_voxel_results),
        'specific_activity': {'mean': [], 'std': [], 'min': [], 'max': []},
        'total_heat': {'mean': [], 'std': [], 'min': [], 'max': []},
        'number_density': {'mean': [], 'std': [], 'min': [], 'max': []},
    }
    
    # Collect values for each cooling time
    for quantity in ['total_specific_activity', 'total_total_heat']:
        all_values = []
        for voxel_results in all_voxel_results.values():
            if quantity in voxel_results:
                all_values.append(voxel_results[quantity])
        
        if all_values:
            all_values = np.array(all_values)
            key = quantity.replace('total_', '', 1)
            
            averages[key]['mean'] = np.mean(all_values, axis=0).tolist()
            averages[key]['std'] = np.std(all_values, axis=0).tolist()
            averages[key]['min'] = np.min(all_values, axis=0).tolist()
            averages[key]['max'] = np.max(all_values, axis=0).tolist()
    
    return averages


def identify_dominant_contributors(isotope_data, top_n=10):
    """
    Identify the dominant contributing isotopes at each cooling time.
    """
    contributors = {}
    
    for quantity in ['specific_activity', 'total_heat']:
        contributors[quantity] = []
        
        # Get number of cooling times from first isotope
        n_times = 0
        for isotope, data in isotope_data.items():
            if quantity in data:
                n_times = len(data[quantity])
                break
        
        for t_idx in range(n_times):
            time_contributors = []
            for isotope, data in isotope_data.items():
                if quantity in data and len(data[quantity]) > t_idx:
                    value = data[quantity][t_idx]
                    time_contributors.append((isotope, value))
            
            # Sort by value descending
            time_contributors.sort(key=lambda x: abs(x[1]), reverse=True)
            contributors[quantity].append(time_contributors[:top_n])
    
    return contributors


# ============================================================================
# RESULTS SUMMARY
# ============================================================================

def generate_summary_report(tally_num, material_name, all_voxel_results, averages, output_dir):
    """
    Generate a comprehensive summary report for a mesh tally.
    """
    report_file = os.path.join(output_dir, f"tally_{tally_num}_summary.txt")
    json_file = os.path.join(output_dir, f"tally_{tally_num}_results.json")
    
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write(f"ALARA ACTIVATION ANALYSIS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Mesh Tally: {tally_num}\n")
        f.write(f"Material: {material_name}\n")
        f.write(f"Irradiation Time: {IRRADIATION_TIME}\n")
        f.write(f"Number of Voxels: {averages.get('n_voxels', 0)}\n\n")
        
        f.write("Cooling Times:\n")
        for label, time in zip(COOLING_TIME_LABELS, COOLING_TIMES):
            f.write(f"  {label}: {time}\n")
        f.write("\n")
        
        f.write("-" * 80 + "\n")
        f.write("AVERAGE VALUES ACROSS ALL VOXELS\n")
        f.write("-" * 80 + "\n\n")
        
        # Specific Activity
        if averages.get('specific_activity', {}).get('mean'):
            f.write("Specific Activity [Bq/cm³]:\n")
            f.write(f"  {'Time':<12} {'Mean':<15} {'Std Dev':<15} {'Min':<15} {'Max':<15}\n")
            for i, label in enumerate(COOLING_TIME_LABELS):
                if i < len(averages['specific_activity']['mean']):
                    mean = averages['specific_activity']['mean'][i]
                    std = averages['specific_activity']['std'][i]
                    min_val = averages['specific_activity']['min'][i]
                    max_val = averages['specific_activity']['max'][i]
                    f.write(f"  {label:<12} {mean:<15.6e} {std:<15.6e} {min_val:<15.6e} {max_val:<15.6e}\n")
            f.write("\n")
        
        # Decay Heat
        if averages.get('total_heat', {}).get('mean'):
            f.write("Decay Heat [W/cm³]:\n")
            f.write(f"  {'Time':<12} {'Mean':<15} {'Std Dev':<15} {'Min':<15} {'Max':<15}\n")
            for i, label in enumerate(COOLING_TIME_LABELS):
                if i < len(averages['total_heat']['mean']):
                    mean = averages['total_heat']['mean'][i]
                    std = averages['total_heat']['std'][i]
                    min_val = averages['total_heat']['min'][i]
                    max_val = averages['total_heat']['max'][i]
                    f.write(f"  {label:<12} {mean:<15.6e} {std:<15.6e} {min_val:<15.6e} {max_val:<15.6e}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("PER-VOXEL RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for voxel_id, results in sorted(all_voxel_results.items()):
            f.write(f"Voxel {voxel_id}:\n")
            if 'total_specific_activity' in results:
                f.write(f"  Activity [Bq/cm³]: {results['total_specific_activity']}\n")
            if 'total_total_heat' in results:
                f.write(f"  Decay Heat [W/cm³]: {results['total_total_heat']}\n")
            f.write("\n")
    
    # Save JSON for programmatic access
    json_data = {
        'tally_number': tally_num,
        'material': material_name,
        'irradiation_time': IRRADIATION_TIME,
        'cooling_times': COOLING_TIMES,
        'cooling_time_labels': COOLING_TIME_LABELS,
        'averages': averages,
        'voxel_results': {str(k): v for k, v in all_voxel_results.items()},
    }
    
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2, default=str)
    
    print(f"  Written summary report: {report_file}")
    print(f"  Written JSON results: {json_file}")
    
    return report_file, json_file


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='MCNP to ALARA Comprehensive Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Irradiation Phases:
  Phase 1: 3 second irradiation (experimental short-term measurements)
           Cooling times: 5.00m (300s), 2h, 26h (24h), 4d
           
  Phase 2: 2 hour irradiation (long-term predictions)
           Cooling times: 15d, 30d, 1y, 5y, 10y, 20y, 50y, 100y

Available Libraries:
  fendl2      - FENDL-2.0 activation library (COMPLETE with all reactions)
  fendl3_new  - FENDL-3 DSV library (December 2024 - COMPLETE with all reactions)

Output Quantities:
  - Nuclide inventories (atoms/cm³)
  - Specific activities (Bq/cm³)
  - Decay heat (W/cm³)
  - Photon source spectra
  - Per-voxel and averaged results
  - Dominant contributor analysis
        """
    )
    
    parser.add_argument('--mcnp', required=True, help='MCNP input file')
    parser.add_argument('--h5', default=None, help='HDF5 file with mesh tally results (optional if using --spectrum-csv)')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--spectrum-csv', type=str, default=None,
                        help='Spectrum CSV file with flux data. When provided, uses this flux for all materials instead of extracting from HDF5. Format: E_low[eV], E_high[eV], flux_bin [n·s⁻¹], ...')
    parser.add_argument('--library', default=DEFAULT_LIBRARY, 
                        choices=['fendl2', 'fendl3_new'],
                        help=f'Activation library (default: {DEFAULT_LIBRARY})')
    parser.add_argument('--run-alara', action='store_true',
                        help='Run ALARA after generating input files')
    parser.add_argument('--max-voxels', type=int, default=None,
                        help='Maximum number of voxels to process (for testing)')
    parser.add_argument('--flux-norm', type=float, default=FLUX_NORMALIZATION,
                        help=f'Flux normalization factor (n/s). For kcode at 1 MW, use ~3.1e16. (default: {FLUX_NORMALIZATION:.2e})')
    parser.add_argument('--use-natural-abundances', action='store_true',
                        help='Use natural isotopic abundances instead of MCNP isotopic ratios (default: use MCNP)')
    parser.add_argument('--exp-data-dir', type=str, default=None,
                        help='Experimental data directory for sample-specific cooling times. If provided, cooling times will be calculated from gamma spec measurement timestamps.')
    
    args = parser.parse_args()
    
    # Now always generating DUAL-PHASE schedules (3s + 2h irradiations)
    # No need for --phase argument anymore
    
    # Load sample-specific schedules if experimental data directory provided
    sample_schedules = None
    material_to_schedule = {}
    if args.exp_data_dir:
        if HAS_SAMPLE_SCHEDULE:
            exp_path = Path(args.exp_data_dir)
            if exp_path.exists():
                sample_schedules = get_all_sample_schedules(exp_path)
                # Create mapping from material name to schedule
                for sample_letter, schedule in sample_schedules.items():
                    material = SAMPLE_TO_MATERIAL.get(sample_letter)
                    if material:
                        material_to_schedule[material] = schedule
                print(f"Loaded sample-specific schedules for {len(sample_schedules)} samples")
                print(f"  Materials with custom cooling times: {', '.join(sorted(material_to_schedule.keys()))}")
            else:
                print(f"Warning: Experimental data directory not found: {exp_path}")
        else:
            print("Warning: sample_irradiation_schedule module not available, using global cooling times")
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("=" * 80)
    print("MCNP to ALARA Comprehensive Workflow - Version 4")
    print("=" * 80)
    print("\nDUAL-PHASE IRRADIATION MODE:")
    print("  Phase 1: 3s irradiation -> short-term measurements (300s, 2h, 24h, 4d)")
    print("  Phase 2: 2h irradiation -> long-term predictions (15d)")
    print("\nNOTE: Using ONLY custom element library (no materials.matlib)")
    print("      Mesh geometry extracted from MCNP model for accurate volumes")
    
    # Show flux source
    if args.spectrum_csv:
        print(f"\nFlux Source: Spectrum CSV file")
        print(f"  File: {args.spectrum_csv}")
        print(f"  NOTE: Same flux will be used for ALL materials (single-zone)")
    else:
        print(f"\nFlux Source: HDF5 mesh tally data")
        print(f"  File: {args.h5}")
        print(f"  Flux Normalization: {args.flux_norm:.3e} n/s")
    
    if material_to_schedule:
        print(f"\n  NOTE: Sample-specific cooling times will be used for materials:")
        for mat, sched in sorted(material_to_schedule.items()):
            # Show both phase 1 and phase 2 cooling times
            for phase_num in [1, 2]:
                phase_key = f'phase{phase_num}'
                if sched.get(phase_key) and sched[phase_key].get('cooling_times'):
                    ct_list = [ct['alara_format'] for ct in sched[phase_key]['cooling_times']]
                    print(f"    {mat} (Phase {phase_num}): {', '.join(ct_list)}")
    
    lib_info = LIBRARY_PATHS[args.library]
    print(f"\nLibrary: {lib_info['description']}")
    if lib_info.get('warning'):
        print(f"\n*** LIBRARY WARNING ***")
        print(f"*** {lib_info['warning']} ***\n")
    
    if args.use_natural_abundances:
        print("Isotopic Composition: Natural abundances (standard element library)")
    else:
        print("Isotopic Composition: MCNP (custom element library)")
    
    print(f"Output Directory: {args.output}")
    
    # Step 1: Parse FMESH definitions
    print("\n" + "-" * 60)
    print("[Step 1] Parsing FMESH definitions from MCNP input...")
    print("-" * 60)
    fmesh_data = parse_mcnp_fmesh_with_materials(args.mcnp)
    print(f"\nFound {len(fmesh_data)} mesh tallies")
    
    # Step 2: Parse material definitions
    print("\n" + "-" * 60)
    print("[Step 2] Parsing material definitions from MCNP input...")
    print("-" * 60)
    
    # Get unique material names from mesh tallies
    required_materials = set()
    for fmesh_info in fmesh_data.values():
        if fmesh_info['material_name']:
            required_materials.add(fmesh_info['material_name'])
    
    print(f"  Required materials from mesh tallies: {', '.join(sorted(required_materials))}")
    
    # Only parse the materials we need (much faster for large MCNP files)
    materials = parse_mcnp_materials(args.mcnp, required_materials)
    
    # Report what was found
    for mat_name in sorted(required_materials):
        if mat_name in materials:
            mat_data = materials[mat_name]
            print(f"  Found '{mat_name}': density={mat_data['density']}, isotopes={len(mat_data['isotopes'])}")
        else:
            print(f"  WARNING: Material '{mat_name}' not found in MCNP file!")
    
    print(f"\nFound {len(materials)} activation materials")
    
    # Step 3: Process each mesh tally
    print("\n" + "-" * 60)
    print("[Step 3] Processing mesh tallies...")
    print("-" * 60)
    
    for tally_num, fmesh_info in fmesh_data.items():
        material_name = fmesh_info['material_name']
        n_groups = fmesh_info['n_groups']
        n_voxels = fmesh_info['n_voxels']
        
        print(f"\n{'='*60}")
        print(f"Processing Tally {tally_num}")
        print(f"{'='*60}")
        print(f"  Material: {material_name}")
        print(f"  Energy groups: {n_groups}")
        print(f"  Mesh dimensions: {fmesh_info['mesh_dims']}")
        print(f"  Total voxels: {n_voxels}")
        
        if material_name is None:
            print(f"  Warning: No material name found, skipping")
            continue
        
        if material_name not in materials:
            print(f"  Warning: Material '{material_name}' not found, skipping")
            continue
        
        material_data = materials[material_name]
        print(f"  Density: {material_data['density']} g/cm³")
        print(f"  Isotopes: {len(material_data['isotopes'])}")
        
        # Check library coverage for this material
        covered, uncovered = check_material_library_coverage(material_data, args.library)
        print(f"  Elements in library ({len(covered)}): {', '.join(sorted(covered))}")
        if uncovered:
            print(f"  *** WARNING: Elements NOT in library ({len(uncovered)}): {', '.join(sorted(uncovered))} ***")
            print(f"  *** These elements will NOT be activated! Use a complete library for production runs. ***")
        
        # Create tally-specific output directory
        tally_output_dir = os.path.join(args.output, f"tally_{tally_num}")
        os.makedirs(tally_output_dir, exist_ok=True)
        
        # NOTE: We no longer generate materials.matlib - using only custom element library
        # The element library contains the full isotopic composition from MCNP
        
        # Get library group structure
        lib_info = LIBRARY_PATHS.get(args.library, LIBRARY_PATHS[DEFAULT_LIBRARY])
        library_groups = lib_info.get('n_groups', 175)
        
        # ================================================================
        # FLUX SOURCE: CSV spectrum, HDF5 per-voxel, or CSV applied to HDF5 voxels
        # ================================================================
        combined_flux_file = os.path.join(tally_output_dir, f"tally_{tally_num}_combined.flx")
        
        # Check what flux sources are available
        has_csv = args.spectrum_csv is not None
        has_h5 = args.h5 is not None
        
        if not has_csv and not has_h5:
            print(f"  Error: Either --h5 or --spectrum-csv must be provided")
            continue
        
        # Determine mode
        if has_h5:
            # Extract mesh tally data for voxel geometry
            tally_data = extract_mesh_tally_from_h5(args.h5, tally_num)
            if tally_data is None:
                print(f"  Warning: Could not extract tally data from HDF5, skipping")
                continue
            
            print(f"  HDF5 data shape: {tally_data['shape']}")
            print(f"\n  Using multi-zone geometry (all voxels in single ALARA run)...")
            
            if has_csv:
                # Mode 1: Apply CSV spectrum to all HDF5 voxels
                print(f"  Flux source: CSV spectrum applied to ALL voxels from HDF5 geometry")
                print(f"  CSV file: {args.spectrum_csv}")
                voxel_info = generate_combined_flux_file_from_csv(
                    args.spectrum_csv, combined_flux_file, library_groups,
                    tally_data, n_groups
                )
            else:
                # Mode 2: Use per-voxel flux from HDF5
                print(f"  Flux source: Per-voxel flux from HDF5 mesh tally")
                voxel_info = generate_combined_flux_file(
                    tally_data, combined_flux_file, n_groups, library_groups,
                    flux_norm=args.flux_norm
                )
            
            if args.max_voxels:
                voxel_info = voxel_info[:args.max_voxels]
                print(f"  Limited to {args.max_voxels} voxels for testing")
                # Regenerate flux file with limited voxels
                with open(combined_flux_file, 'r') as f:
                    lines = f.readlines()
                # Keep header and first max_voxels worth of data
                # Each voxel has 2 lines (comment + data)
                with open(combined_flux_file, 'w') as f:
                    f.writelines(lines[:4])  # Header lines
                    for i in range(args.max_voxels):
                        f.writelines(lines[4 + i*2:4 + (i+1)*2])
        else:
            # Mode 3: CSV only - single voxel
            print(f"\n  Using single-zone geometry (CSV spectrum only, no HDF5)")
            print(f"  CSV file: {args.spectrum_csv}")
            voxel_info = generate_flux_file_from_csv(
                args.spectrum_csv, combined_flux_file, library_groups
            )
        
        # Generate custom element library with MCNP isotopic ratios (default behavior)
        # Unless --use-natural-abundances is specified
        elelib_file = None
        if not args.use_natural_abundances:
            elelib_file = os.path.join(tally_output_dir, f"custom_elelib.txt")
            generate_custom_elelib(material_data, elelib_file)
        
        # Generate material library file (required by ALARA)
        matlib_file = os.path.join(tally_output_dir, "materials.matlib")
        mat_name = generate_alara_matlib(material_name, material_data, matlib_file)
        print(f"  Written material library: {matlib_file}")
        
        # ================================================================
        # BUILD DUAL-PHASE SCHEDULE (3s + 2h irradiations)
        # ================================================================
        # Always include BOTH irradiation phases for complete analysis
        schedules = []
        
        if material_name in material_to_schedule:
            # Use sample-specific schedules with exact cooling times
            schedule = material_to_schedule[material_name]
            
            # Phase 1: 3s irradiation
            if schedule.get('phase1'):
                p1 = schedule['phase1']
                schedules.append({
                    'irradiation_time': p1['irradiation_time'],
                    'cooling_times': [ct['alara_format'] for ct in p1['cooling_times']]
                })
                print(f"  Phase 1 (sample-specific):")
                print(f"    Irradiation: {p1['irradiation_time']}")
                print(f"    Cooling times: {', '.join([ct['alara_format'] for ct in p1['cooling_times']])}")
            
            # Phase 2: 2h irradiation
            if schedule.get('phase2'):
                p2 = schedule['phase2']
                schedules.append({
                    'irradiation_time': p2['irradiation_time'],
                    'cooling_times': [ct['alara_format'] for ct in p2['cooling_times']]
                })
                print(f"  Phase 2 (sample-specific):")
                print(f"    Irradiation: {p2['irradiation_time']}")
                print(f"    Cooling times: {', '.join([ct['alara_format'] for ct in p2['cooling_times']])}")
        else:
            # Use default global schedules for both phases
            schedules = [
                {'irradiation_time': '3 s', 'cooling_times': COOLING_TIMES_PHASE1},
                {'irradiation_time': '2 h', 'cooling_times': COOLING_TIMES_PHASE2}
            ]
            print(f"  Using default dual-phase schedules:")
            print(f"    Phase 1: 3s irradiation, cooling: {', '.join(COOLING_TIMES_PHASE1)}")
            print(f"    Phase 2: 2h irradiation, cooling: {', '.join(COOLING_TIMES_PHASE2)}")
        
        # Get voxel volumes from FMESH parsing (actual mesh geometry)
        voxel_volumes = fmesh_info.get('voxel_volumes', None)
        if voxel_volumes:
            print(f"  Using actual voxel volumes from MCNP mesh ({len(voxel_volumes)} voxels)")
            print(f"    Total mesh volume: {sum(voxel_volumes):.4f} cm³")
        
        # Generate multi-zone ALARA input file
        multizone_input = os.path.join(tally_output_dir, f"tally_{tally_num}_multizone.inp")
        generate_multizone_alara_input(
            material_name,
            material_data,
            voxel_info,
            combined_flux_file,
            multizone_input,
            library_groups,
            library=args.library,
            mesh_dims=fmesh_info['mesh_dims'],
            voxel_volumes=voxel_volumes,
            elelib_file=elelib_file,
            matlib_file=matlib_file,
            schedules=schedules
        )
        
        # Run ALARA if requested
        if args.run_alara:
            print(f"\n  Running ALARA with multi-zone geometry ({len(voxel_info)} zones)...")
            
            success, stdout, stderr = run_alara(
                os.path.basename(multizone_input), 
                tally_output_dir
            )
            
            if success:
                print(f"  ALARA completed successfully!")
                output_file = multizone_input.replace('.inp', '.out')
                print(f"  Output written to: {output_file}")
                
                # Parse the multi-zone output
                all_voxel_results = parse_alara_output(stdout)
                
                # Calculate averages
                averages = calculate_averages(all_voxel_results)
                
                # Generate summary report for the multi-zone run
                generate_summary_report(
                    tally_num, material_name, all_voxel_results, averages, tally_output_dir
                )
            else:
                print(f"  ALARA FAILED: {stderr[:200] if stderr else 'Unknown error'}")
        else:
            print(f"\n  Note: Use --run-alara to execute ALARA and get results")
    
    # Final summary
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    print(f"\nOutput files in: {args.output}")
    print("\nGenerated files per tally:")
    print("  - custom_elelib.txt              : Custom element library (MCNP isotopic ratios)")
    print("  - tally_XXXXX_combined.flx       : Combined flux file (all voxels)")
    print("  - tally_XXXXX_multizone.inp      : Multi-zone ALARA input (DUAL-PHASE schedule)")
    if args.run_alara:
        print("  - tally_XXXXX_multizone.out      : ALARA output (all zones)")
        print("  - tally_XXXXX_summary.txt        : Summary report")
        print("  - tally_XXXXX_results.json       : JSON results")
    print("\nNOTE: materials.matlib no longer generated - using only custom element library")
    print("\nTo run ALARA manually:")
    print(f"  cd {args.output}/tally_XXXXX")
    print(f"  {ALARA_EXECUTABLE} tally_XXXXX_multizone.inp")


if __name__ == '__main__':
    main()
