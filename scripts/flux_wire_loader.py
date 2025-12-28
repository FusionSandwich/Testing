"""
Flux wire data loader for MCNP-ALARA workflow.

This module parses EXPERIMENTAL flux wire gamma spectroscopy files (NOT ALARA output).
For parsing ALARA output files, use alara_output_processing.FileParser instead.

Provides:
- Parsing of flux wire measurement .txt files
- Activity and specific activity calculations
- Neutron flux calculation from activation measurements
- Wire metadata (cross-sections, masses)

Usage:
    from flux_wire_loader import load_flux_wires, WIRE_METADATA
    
    flux_wires_df = load_flux_wires(
        flux_wires_dir='flux_wires',
        sample_filter=r'-1($|_)',  # Only wires ending in -1
        default_irradiation_s=7200
    )
"""

import glob
import re
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from dateutil import parser as dtparser

# Import from isotope_utils
from isotope_utils import (
    canonical_iso, parse_activity_unit, get_half_life_seconds,
    half_life_to_lambda, calculate_n_atoms, extract_mass_number,
    LN2, AVOGADRO,
)
# Import time conversions from alara_output_processing (the authoritative source)
from alara_output_processing import SECONDS_CONV

# Map common time unit names to SECONDS_CONV keys
def _time_unit_to_seconds(unit: str) -> float:
    """Convert a time unit string to seconds multiplier."""
    unit = unit.lower().strip().rstrip('.')
    # Map common aliases to SECONDS_CONV keys
    aliases = {
        'sec': 's', 'second': 's', 'seconds': 's',
        'min': 'm', 'minute': 'm', 'minutes': 'm',
        'hr': 'h', 'hour': 'h', 'hours': 'h',
        'day': 'd', 'days': 'd',
        'wk': 'w', 'week': 'w', 'weeks': 'w',
        'yr': 'y', 'year': 'y', 'years': 'y',
    }
    key = aliases.get(unit, unit)
    return SECONDS_CONV.get(key, 1)

# ==============================================================================
# WIRE METADATA (cross-sections, masses)
# ==============================================================================
WIRE_METADATA = [
    # FAST / THRESHOLD (mb)
    {"sample": "Ti-RAFM-1", "iso": "ti46", "prod": "sc46", "mass_mg": 13.4986, "xs": 13.16, "unit": "mb", "e_start": 3.28, "e_end": 13.4},
    {"sample": "Ti-RAFM-2", "iso": "ti46", "prod": "sc46", "mass_mg": 14.0974, "xs": 13.16, "unit": "mb", "e_start": 3.28, "e_end": 13.4},
    {"sample": "Ti-RAFM-1", "iso": "ti47", "prod": "sc47", "mass_mg": 13.4986, "xs": 24.00, "unit": "mb", "e_start": 1.20, "e_end": 12.3},
    {"sample": "Ti-RAFM-2", "iso": "ti47", "prod": "sc47", "mass_mg": 14.0974, "xs": 24.00, "unit": "mb", "e_start": 1.20, "e_end": 12.3},
    {"sample": "Ti-RAFM-1", "iso": "ti48", "prod": "sc48", "mass_mg": 13.4986, "xs": 0.3998, "unit": "mb", "e_start": 5.19, "e_end": 17.4},
    {"sample": "Ti-RAFM-2", "iso": "ti48", "prod": "sc48", "mass_mg": 14.0974, "xs": 0.3998, "unit": "mb", "e_start": 5.19, "e_end": 17.4},
    {"sample": "Ni-RAFM-1", "iso": "ni58", "prod": "co58", "mass_mg": 41.6747, "xs": 113.2, "unit": "mb", "e_start": 1.34, "e_end": 13.0},
    {"sample": "Ni-RAFM-2", "iso": "ni58", "prod": "co58", "mass_mg": 44.3911, "xs": 113.2, "unit": "mb", "e_start": 1.34, "e_end": 13.0},
    {"sample": "In-Cd-RAFM-1", "iso": "in113", "prod": "in113m", "mass_mg": 17.3640, "xs": 70.0, "unit": "mb", "e_start": 0.674, "e_end": 11.3},
    {"sample": "In-Cd-RAFM-2", "iso": "in113", "prod": "in113m", "mass_mg": 15.4123, "xs": 70.0, "unit": "mb", "e_start": 0.674, "e_end": 11.3},
    {"sample": "In-Cd-RAFM-1", "iso": "in115", "prod": "in115m", "mass_mg": 17.3640, "xs": 183.1, "unit": "mb", "e_start": 0.674, "e_end": 11.6},
    {"sample": "In-Cd-RAFM-2", "iso": "in115", "prod": "in115m", "mass_mg": 15.4123, "xs": 183.1, "unit": "mb", "e_start": 0.674, "e_end": 11.6},
    # CAPTURE BARE (b)
    {"sample": "Sc-RAFM-1", "iso": "sc45", "prod": "sc46", "mass_mg": 0.9645, "xs": 27.14, "unit": "b", "e_start": 2.04e-9, "e_end": 5.25e-6},
    {"sample": "Sc-RAFM-2", "iso": "sc45", "prod": "sc46", "mass_mg": 0.7282, "xs": 27.14, "unit": "b", "e_start": 2.04e-9, "e_end": 5.25e-6},
    {"sample": "Co-RAFM-1", "iso": "co59", "prod": "co60", "mass_mg": 4.0661, "xs": 37.18, "unit": "b", "e_start": 2.23e-9, "e_end": 1.86e-4},
    {"sample": "Co-RAFM-2", "iso": "co59", "prod": "co60", "mass_mg": 2.9945, "xs": 37.18, "unit": "b", "e_start": 2.23e-9, "e_end": 1.86e-4},
    {"sample": "Cu-RAFM-1", "iso": "cu63", "prod": "cu64", "mass_mg": 1.3748, "xs": 4.50, "unit": "b", "e_start": 2.10e-9, "e_end": 2.77e-3},
    {"sample": "Cu-RAFM-2", "iso": "cu63", "prod": "cu64", "mass_mg": 1.2332, "xs": 4.50, "unit": "b", "e_start": 2.10e-9, "e_end": 2.77e-3},
    # CAPTURE CADMIUM-COVERED (b)
    {"sample": "Sc-Cd-RAFM-1", "iso": "sc45", "prod": "sc46", "mass_mg": 3.8285, "xs": 11.83, "unit": "b", "e_start": 2.36e-8, "e_end": 6.95e-2},
    {"sample": "Sc-Cd-RAFM-2", "iso": "sc45", "prod": "sc46", "mass_mg": 5.3237, "xs": 11.83, "unit": "b", "e_start": 2.36e-8, "e_end": 6.95e-2},
    {"sample": "Co-Cd-RAFM-1", "iso": "co59", "prod": "co60", "mass_mg": 3.6703, "xs": 74.0, "unit": "b", "e_start": 4.57e-8, "e_end": 3.81e-4},
    {"sample": "Co-Cd-RAFM-2", "iso": "co59", "prod": "co60", "mass_mg": 3.9085, "xs": 74.0, "unit": "b", "e_start": 4.57e-8, "e_end": 3.81e-4},
    {"sample": "Cu-Cd-RAFM-1", "iso": "cu63", "prod": "cu64", "mass_mg": 1.3748, "xs": 4.97, "unit": "b", "e_start": 2.57e-8, "e_end": 1.51},
    {"sample": "Cu-Cd-RAFM-2", "iso": "cu63", "prod": "cu64", "mass_mg": 1.2332, "xs": 4.97, "unit": "b", "e_start": 2.57e-8, "e_end": 1.51},
    {"sample": "Fe-Cd-RAFM-1", "iso": "fe58", "prod": "fe59", "mass_mg": 3.0209, "xs": 1.25, "unit": "b", "e_start": 3.05e-8, "e_end": 6.36e-1},
    {"sample": "Fe-Cd-RAFM-2", "iso": "fe58", "prod": "fe59", "mass_mg": 2.7912, "xs": 1.25, "unit": "b", "e_start": 3.05e-8, "e_end": 6.36e-1},
    {"sample": "In-Cd-RAFM-1", "iso": "in113", "prod": "in114m", "mass_mg": 17.3640, "xs": 325.2, "unit": "b", "e_start": 6.82e-7, "e_end": 7.79e-2},
    {"sample": "In-Cd-RAFM-2", "iso": "in113", "prod": "in114m", "mass_mg": 15.4123, "xs": 325.2, "unit": "b", "e_start": 6.82e-7, "e_end": 7.79e-2},
    {"sample": "In-Cd-RAFM-1", "iso": "in115", "prod": "in116m", "mass_mg": 17.3640, "xs": 2500.0, "unit": "b", "e_start": 4.97e-7, "e_end": 3.50e-5},
    {"sample": "In-Cd-RAFM-2", "iso": "in115", "prod": "in116m", "mass_mg": 15.4123, "xs": 2500.0, "unit": "b", "e_start": 4.97e-7, "e_end": 3.50e-5},
]


def get_metadata_df() -> pd.DataFrame:
    """Get wire metadata as a DataFrame with computed columns."""
    df = pd.DataFrame(WIRE_METADATA)
    df['iso_canon'] = df['iso'].apply(canonical_iso)
    df['prod_canon'] = df['prod'].apply(canonical_iso)
    df['mass_g'] = df['mass_mg'] / 1000.0
    df['sigma_cm2'] = np.where(
        df['unit'] == 'b',
        df['xs'] * 1e-24,
        df['xs'] * 1e-27
    )
    df['energy_mid_MeV'] = (df['e_start'] + df['e_end']) / 2.0
    df['category'] = np.where(df['unit'] == 'mb', 'Fast/Threshold', 'Capture')
    return df


# ==============================================================================
# FLUX CALCULATION HELPERS
# ==============================================================================

def parse_half_life_seconds(hl_str: str) -> Optional[float]:
    """Convert half-life string like '5.271 y' to seconds."""
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
    """
    if meta_df is None:
        meta_df = get_metadata_df()

    flux_records = []
    skipped = []

    for _, row in flux_wires_df.iterrows():
        sample = row['sample']
        prod_iso = canonical_iso(row['isotope'])

        base_sample = re.sub(r'_\d+cm$', '', sample)
        base_sample = re.sub(r'[a-z]$', '', base_sample)

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

        hl_seconds = parse_half_life_seconds(row.get('half_life'))
        if not hl_seconds or hl_seconds <= 0:
            skipped.append((sample, prod_iso, 'half-life parse failed'))
            continue

        lam = np.log(2) / hl_seconds

        mass_match = re.search(r"(\\d+)", mrow['iso_canon'])
        A_mass = float(mass_match.group(1)) if mass_match else None
        if not A_mass:
            skipped.append((sample, prod_iso, 'mass number missing'))
            continue

        N_atoms = (mass_g / A_mass) * AVOGADRO

        irr_sec = float(row.get('irradiation_seconds', default_irradiation_seconds))
        dec_sec = float(row.get('decay_seconds', default_decay_seconds))

        S = 1 - np.exp(-lam * irr_sec)
        D = np.exp(-lam * dec_sec)

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
        for s in skipped[:10]:
            print(f"  {s[0]} {s[1]} -> {s[2]}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")

    if not flux_records:
        print("No flux records computed. Check mapping, half-life strings, or decay time.")
        return pd.DataFrame()

    return pd.DataFrame(flux_records).dropna(subset=['phi', 'e_start', 'e_end'])


def load_mcnp_spectrum(
    spectrum_csv: str,
    energy_scale: str = 'MeV',
    flux_divisor: float = 15.0
) -> Optional[Dict[str, np.ndarray]]:
    """
    Load MCNP spectrum data from CSV file.
    """
    try:
        df = pd.read_csv(spectrum_csv)
        if 'energy' in df.columns and 'flux' in df.columns:
            energies = df['energy'].values
            flux = df['flux'].values
        else:
            energies = df.iloc[:, 0].values
            flux = df.iloc[:, 1].values

        if energy_scale.lower() == 'mev':
            energies = energies / 1e6 if energies.max() > 1e3 else energies

        flux = flux / flux_divisor if flux_divisor else flux

        e_low = energies[:-1]
        e_high = energies[1:]
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


def recompute_phi_in_dataframe(
    flux_wires_df: pd.DataFrame,
    meta_df: Optional[pd.DataFrame] = None,
    default_irradiation_seconds: float = 7203,
    default_decay_seconds: float = 0,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Recompute phi (neutron flux) values in-place in flux_wires_df.
    """
    if meta_df is None:
        meta_df = get_metadata_df()

    new_cols = ['phi', 'phi_unc', 'sigma_cm2', 'mass_used_g', 'A_mass',
                'N_atoms', 'lam', 'S', 'D', 'denom', 'irradiation_seconds_used']

    for col in new_cols:
        if col not in flux_wires_df.columns:
            flux_wires_df[col] = np.nan

    for idx, row in flux_wires_df.iterrows():
        sample = row['sample']
        prod_iso = canonical_iso(row['isotope'])
        base_sample = re.sub(r'_\d+cm$', '', sample)
        base_sample = re.sub(r'[a-z]$', '', base_sample)

        mrow = meta_df[(meta_df['sample'] == sample) & (meta_df['prod_canon'] == prod_iso)]
        if mrow.empty:
            mrow = meta_df[(meta_df['sample'] == base_sample) & (meta_df['prod_canon'] == prod_iso)]
        if mrow.empty:
            mrow = meta_df[meta_df['prod_canon'] == prod_iso]
        if mrow.empty:
            if verbose:
                print(f"Skipping {sample} {prod_iso}: no metadata")
            continue

        mrow = mrow.iloc[0]
        mass_g = mrow['mass_g'] if not pd.isna(mrow['mass_g']) else row.get('mass_g', 1.0)
        activity_Bq = row.get('activity_Bq', np.nan)
        unc_Bq = row.get('uncertainty_Bq', np.nan)
        hl_seconds = parse_half_life_seconds(row.get('half_life'))
        if not hl_seconds or hl_seconds <= 0:
            if verbose:
                print(f"Skipping {sample} {prod_iso}: half-life parse failed")
            continue

        lam = np.log(2) / hl_seconds
        mass_match = re.search(r"(\\d+)", mrow['iso_canon'])
        A_mass = float(mass_match.group(1)) if mass_match else None
        if not A_mass:
            if verbose:
                print(f"Skipping {sample} {prod_iso}: mass number missing")
            continue

        N_atoms = (mass_g / A_mass) * AVOGADRO
        irr_sec = float(row.get('irradiation_seconds', default_irradiation_seconds))
        dec_sec = float(row.get('decay_seconds', default_decay_seconds))
        S = 1 - np.exp(-lam * irr_sec)
        D = np.exp(-lam * dec_sec)
        denom = N_atoms * mrow['sigma_cm2'] * S * D
        phi = activity_Bq / denom if denom > 0 else np.nan

        phi_unc = np.nan
        if np.isfinite(phi) and activity_Bq > 0 and np.isfinite(unc_Bq):
            phi_unc = phi * (unc_Bq / activity_Bq)

        flux_wires_df.loc[idx, 'phi'] = phi
        flux_wires_df.loc[idx, 'phi_unc'] = phi_unc
        flux_wires_df.loc[idx, 'sigma_cm2'] = mrow['sigma_cm2']
        flux_wires_df.loc[idx, 'mass_used_g'] = mass_g
        flux_wires_df.loc[idx, 'A_mass'] = A_mass
        flux_wires_df.loc[idx, 'N_atoms'] = N_atoms
        flux_wires_df.loc[idx, 'lam'] = lam
        flux_wires_df.loc[idx, 'S'] = S
        flux_wires_df.loc[idx, 'D'] = D
        flux_wires_df.loc[idx, 'denom'] = denom
        flux_wires_df.loc[idx, 'irradiation_seconds_used'] = irr_sec

    return flux_wires_df

# ==============================================================================
# FILE PARSING
# ==============================================================================
# Regex for parsing activity lines
ACTIVITY_PATTERN = re.compile(
    r"^(?P<iso>[A-Za-z]+\d+m?)\s+(?P<hl_val>\d+\.?\d*)\s*(?P<hl_unit>[smhdywk]+)\s+\w+\s+Activity\s*=\s*(?P<act>[0-9.E+\-]+)\s*[±±]?\s*(?P<unc>[0-9.E+%\-]*)\s*(?P<unit>.*)$",
    re.IGNORECASE,
)

IRRADIATION_PATTERN = re.compile(
    r'irradiat\w* time\s*[:=]\s*([0-9.+-eE]+)\s*(s|sec|seconds|m|min|minutes|h|hr|hours)',
    re.IGNORECASE
)


def parse_measurement_datetime(lines: List[str]) -> Optional[datetime]:
    """
    Parse measurement datetime from file lines.
    
    Looks for 'Date:' header or any parseable datetime.
    """
    if dtparser is None:
        return None
    
    # 1) Look for 'Date:' header
    for line in lines:
        m = re.search(r"Date\s*[:=]\s*(.*)", line, re.IGNORECASE)
        if m:
            txt = m.group(1).strip()
            try:
                return dtparser.parse(txt, fuzzy=True)
            except Exception:
                continue
    
    # 2) Try parsing any line with digits
    for line in lines:
        txt = line.strip()
        if not txt or not re.search(r'\d', txt):
            continue
        try:
            return dtparser.parse(txt, fuzzy=True)
        except Exception:
            continue
    
    return None


def parse_irradiation_time(lines: List[str]) -> Optional[float]:
    """Parse irradiation time from file lines (returns seconds)."""
    for line in lines:
        m = IRRADIATION_PATTERN.search(line)
        if m:
            val = float(m.group(1))
            unit = m.group(2).lower()
            mult = _time_unit_to_seconds(unit)
            return val * mult
    return None


def calculate_flux(
    activity_bq: float,
    uncertainty_bq: float,
    sigma_cm2: float,
    mass_g: float,
    target_mass_number: int,
    half_life_seconds: float,
    irradiation_seconds: float,
    decay_seconds: float
) -> tuple:
    """
    Calculate neutron flux from measured activity.
    
    Returns (phi, phi_uncertainty) in n/cm²/s
    """
    if any(np.isnan([activity_bq, sigma_cm2, mass_g])):
        return np.nan, np.nan
    if mass_g <= 0 or half_life_seconds <= 0:
        return np.nan, np.nan
    
    lam = LN2 / half_life_seconds
    N_atoms = calculate_n_atoms(mass_g, target_mass_number)
    
    # Saturation and decay factors
    S = 1 - np.exp(-lam * irradiation_seconds)
    D = np.exp(-lam * decay_seconds)
    
    denom = N_atoms * sigma_cm2 * S * D
    if denom <= 0:
        return np.nan, np.nan
    
    phi = activity_bq / denom
    phi_unc = np.nan
    if not np.isnan(uncertainty_bq) and activity_bq > 0:
        phi_unc = phi * (uncertainty_bq / activity_bq)
    
    return phi, phi_unc


def load_flux_wires(
    flux_wires_dir: str = 'flux_wires',
    sample_filter: Optional[str] = r'-1($|_)',
    default_irradiation_s: float = 7200,
    default_decay_s: float = 357,
    output_csv: Optional[str] = None
) -> pd.DataFrame:
    """
    Load and parse flux wire measurement files.
    
    Parameters:
        flux_wires_dir: Directory containing .txt measurement files
        sample_filter: Regex pattern to filter sample names (None = no filter)
        default_irradiation_s: Default irradiation time if not found in file
        default_decay_s: Default decay time if not calculable
        output_csv: If provided, save results to this CSV file
    
    Returns:
        DataFrame with parsed flux wire data
    """
    flux_dir = Path(flux_wires_dir)
    if not flux_dir.exists():
        print(f"Warning: Flux wires directory not found: {flux_dir}")
        return pd.DataFrame()
    
    # Get metadata lookup
    meta_df = get_metadata_df()
    
    # Compile sample filter
    sample_filter_re = re.compile(sample_filter) if sample_filter else None
    
    records = []
    
    for filepath in sorted(glob.glob(str(flux_dir / '*.txt'))):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        lines = content.split('\n')
        sample_name = Path(filepath).stem
        
        # Apply sample filter
        if sample_filter_re and not sample_filter_re.search(sample_name):
            continue
        
        # Parse timing info
        irradiation_seconds = parse_irradiation_time(lines)
        if irradiation_seconds is None:
            irradiation_seconds = default_irradiation_s
        
        meas_dt = parse_measurement_datetime(lines)
        if meas_dt is None:
            try:
                stat = Path(filepath).stat()
                meas_dt = datetime.fromtimestamp(stat.st_mtime)
            except Exception:
                pass
        
        # Calculate decay time
        decay_seconds = default_decay_s
        if meas_dt:
            try:
                irr_end = meas_dt - timedelta(seconds=default_decay_s)
                decay_seconds = max((meas_dt - irr_end).total_seconds(), 0)
            except Exception:
                pass
        
        # Parse activity lines
        for line in lines:
            m = ACTIVITY_PATTERN.match(line.strip())
            if not m:
                continue
            
            iso_raw = m.group('iso')
            hl_val = float(m.group('hl_val'))
            hl_unit = m.group('hl_unit')
            half_life_str = f"{hl_val} {hl_unit}"
            activity_raw = float(m.group('act'))
            unc_str = m.group('unc') or ''
            unit = (m.group('unit') or '').strip()
            
            # Convert to Bq
            factor = parse_activity_unit(unit)
            activity_bq = activity_raw * factor
            
            # Parse uncertainty
            uncertainty_bq = np.nan
            try:
                if unc_str and '%' in unc_str:
                    unc_pct = float(unc_str.replace('%', ''))
                    uncertainty_bq = (unc_pct / 100.0) * activity_bq
                elif unc_str:
                    uncertainty_bq = float(unc_str) * factor
            except Exception:
                pass
            
            # Canonicalize isotope name
            canon = canonical_iso(iso_raw)
            
            # Lookup metadata
            base_sample = re.sub(r'_\d+cm$', '', sample_name)
            base_sample = re.sub(r'[a-z]$', '', base_sample)
            
            mrow = meta_df[(meta_df['sample'] == sample_name) & (meta_df['prod_canon'] == canon)]
            if mrow.empty:
                mrow = meta_df[(meta_df['sample'] == base_sample) & (meta_df['prod_canon'] == canon)]
            if mrow.empty:
                mrow = meta_df[meta_df['prod_canon'] == canon]
            
            mass_g = 1.0
            sigma_cm2 = np.nan
            target_iso = ''
            
            if not mrow.empty:
                row = mrow.iloc[0]
                mass_g = row['mass_g']
                sigma_cm2 = row['sigma_cm2']
                target_iso = row['iso_canon']
            
            # Calculate specific activity
            specific_activity_bq = activity_bq / mass_g if mass_g > 0 else np.nan
            specific_activity_uci = specific_activity_bq / 37000.0 if not np.isnan(specific_activity_bq) else np.nan
            specific_activity_uci_unc = (uncertainty_bq / mass_g / 37000.0) if (mass_g > 0 and not np.isnan(uncertainty_bq)) else np.nan
            
            # Calculate flux
            hl_seconds = hl_val * _time_unit_to_seconds(hl_unit)
            target_mass = extract_mass_number(target_iso) if target_iso else None
            
            phi, phi_unc = np.nan, np.nan
            if target_mass and not np.isnan(sigma_cm2):
                phi, phi_unc = calculate_flux(
                    activity_bq=activity_bq,
                    uncertainty_bq=uncertainty_bq,
                    sigma_cm2=sigma_cm2,
                    mass_g=mass_g,
                    target_mass_number=target_mass,
                    half_life_seconds=hl_seconds,
                    irradiation_seconds=irradiation_seconds,
                    decay_seconds=decay_seconds
                )
            
            records.append({
                'sample': sample_name,
                'isotope': canon,
                'half_life': half_life_str,
                'activity_raw': activity_raw,
                'unit': unit,
                'activity_Bq': activity_bq,
                'activity_uCi': activity_bq / 37000.0,
                'uncertainty_Bq': uncertainty_bq,
                'uncertainty_uCi': uncertainty_bq / 37000.0 if not np.isnan(uncertainty_bq) else np.nan,
                'mass_g': mass_g,
                'specific_activity_Bq_per_g': specific_activity_bq,
                'specific_activity_uCi_per_g': specific_activity_uci,
                'specific_activity_uCi_per_g_unc': specific_activity_uci_unc,
                'irradiation_seconds': irradiation_seconds,
                'decay_seconds': decay_seconds,
                'measurement_datetime': meas_dt,
                'phi': phi,
                'phi_unc': phi_unc
            })
    
    if not records:
        print("No flux wire activities parsed.")
        return pd.DataFrame()
    
    df = pd.DataFrame(records).sort_values(['sample', 'isotope'])
    
    if output_csv:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved flux wire activities to: {output_path}")
    
    print(f"Loaded {len(df)} flux-wire measurements across {df['sample'].nunique()} files")
    return df


if __name__ == '__main__':
    # Test loading
    print("Testing flux_wire_loader...")
    df = load_flux_wires()
    if not df.empty:
        print(df.head())
    else:
        print("No data loaded (flux_wires directory may not exist)")
