"""
Data loaders for MCNP-ALARA workflow.

Includes:
- Experimental gamma spectroscopy loader (RAFM3/RAFM4)
- Flux wire loader + metadata + spectrum helpers
"""

import glob
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

import numpy as np
import pandas as pd
from dateutil import parser as dtparser

from nuclear_data import (
    canonical_iso,
    format_iso_pretty,
    parse_activity_unit,
    LN2,
    AVOGADRO,
    calculate_n_atoms,
    extract_mass_number,
)
from alara_output_processing import SECONDS_CONV

# ==============================================================================#
# EXPERIMENTAL DATA LOADER
# ==============================================================================#

SAMPLE_TO_MATERIAL = {
    'N': 'CNA',           # tally_85214
    'A': 'EUROFER97_A',   # tally_85244
    'B': 'EUROFER97_B',   # tally_85234
    'C': 'EUROFER97_C',   # tally_85224
}

MATERIAL_TO_TALLY = {
    'CNA': 'tally_85214',
    'EUROFER97_A': 'tally_85244',
    'EUROFER97_B': 'tally_85234',
    'EUROFER97_C': 'tally_85224',
}

COOLING_TIME_MAP = {
    '300sEOI': '300s',
    '2hrEOI': '2h',
    '24hrEOI': '24h',
    '4dEOI': '4d',
    '15dEOI': '15d',
}

ACTIVITY_PATTERN = re.compile(
    r'^(\w+\d+m?)\s+(\d+\.?\d*)\s*([smhdywk]+)\s+\w+\s+Activity\s*=\s*([0-9.E+-]+)\s*[±�]\s*([0-9.E+%-]+)\s*(\w+)',
    re.IGNORECASE
)


def parse_experimental_file(filepath: str) -> Dict[str, Dict[str, Any]]:
    """Parse a gamma spectroscopy file to extract nuclide activities."""
    nuclides = {}

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        return nuclides

    for line in content.split('\n'):
        match = ACTIVITY_PATTERN.match(line.strip())
        if not match:
            continue

        isotope_raw = match.group(1)
        half_life_val = match.group(2)
        half_life_unit = match.group(3)
        activity = float(match.group(4))
        unc_str = match.group(5)
        unit = match.group(6)

        try:
            if '%' in unc_str:
                unc_pct = float(unc_str.replace('%', ''))
                uncertainty = (unc_pct / 100.0) * activity
            else:
                uncertainty = float(unc_str)
        except ValueError:
            uncertainty = 0.0

        iso_match = re.match(r'([A-Za-z]+)(\d+)(m?)', isotope_raw, re.IGNORECASE)
        if iso_match:
            element = iso_match.group(1).lower()
            mass_num = iso_match.group(2)
            meta = iso_match.group(3).lower() if iso_match.group(3) else ''
            isotope = f"{element}-{mass_num}{meta}"

            nuclides[isotope] = {
                'activity': activity,
                'uncertainty': uncertainty,
                'unit': unit,
                'half_life': f"{half_life_val} {half_life_unit}",
                'rel_unc': uncertainty / activity if activity > 0 else 0
            }

    return nuclides


def load_experimental_data(
    exp_data_dir: str = 'Experimental_Data/RAFM3',
    sample_letters: Optional[List[str]] = None,
    verbose: bool = True
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Load all experimental data from a directory."""
    exp_dir = Path(exp_data_dir)
    prefix = exp_dir.name if exp_dir.name.startswith('RAFM') else 'RAFM3'

    if sample_letters is None:
        sample_letters = ['A', 'B', 'C', 'N']

    experimental_data: Dict[str, Dict[str, Dict[str, Any]]] = {}

    if verbose:
        print("=" * 80)
        print(f"LOADING EXPERIMENTAL DATA FROM {prefix}")
        print("=" * 80)

    for sample_letter in sample_letters:
        if sample_letter not in SAMPLE_TO_MATERIAL:
            if verbose:
                print(f"Warning: Unknown sample letter '{sample_letter}'")
            continue

        material = SAMPLE_TO_MATERIAL[sample_letter]
        experimental_data[material] = {}

        if verbose:
            print(f"\nSample {prefix}-{sample_letter} → {material}:")

        for cooling_key, alara_label in COOLING_TIME_MAP.items():
            filename = f"{prefix}-{sample_letter}_{cooling_key}.txt"
            filepath = exp_dir / filename

            if filepath.exists():
                nuclides = parse_experimental_file(str(filepath))
                experimental_data[material][alara_label] = nuclides

                if verbose:
                    print(f"  {cooling_key}: {len(nuclides)} nuclides detected")
                    for iso, data in nuclides.items():
                        print(
                            f"    {iso}: {data['activity']:.3e} ± {data['uncertainty']:.2e} "
                            f"{data['unit']} (t½={data['half_life']})"
                        )
            else:
                if verbose:
                    if prefix == 'RAFM4' and cooling_key != '15dEOI':
                        continue
                    if prefix == 'RAFM3' and cooling_key == '15dEOI':
                        continue
                    print(f"  {cooling_key}: File not found")

    if verbose:
        print("\n" + "=" * 80)
        print("EXPERIMENTAL ISOTOPES SUMMARY")
        print("=" * 80)
        all_isotopes = get_all_isotopes(experimental_data)
        print(f"Unique isotopes detected: {sorted(all_isotopes)}")

    return experimental_data


def get_all_isotopes(experimental_data: Dict) -> set:
    isotopes = set()
    for mat_data in experimental_data.values():
        for time_data in mat_data.values():
            isotopes.update(time_data.keys())
    return isotopes


def experimental_to_dataframe(experimental_data: Dict) -> pd.DataFrame:
    records = []

    for material, time_data in experimental_data.items():
        for cooling_time, nuclides in time_data.items():
            for isotope, data in nuclides.items():
                records.append({
                    'material': material,
                    'cooling_time': cooling_time,
                    'isotope': isotope,
                    'activity': data['activity'],
                    'uncertainty': data['uncertainty'],
                    'unit': data['unit'],
                    'half_life': data['half_life'],
                    'rel_unc': data['rel_unc']
                })

    return pd.DataFrame(records)


def get_top_isotopes(
    experimental_data: Dict,
    material: Optional[str] = None,
    top_n: int = 3
) -> Dict[str, List[tuple]]:
    results = {}
    materials = [material] if material else experimental_data.keys()

    for mat in materials:
        if mat not in experimental_data:
            continue

        isotope_totals = {}

        for time_data in experimental_data[mat].values():
            for iso, data in time_data.items():
                factor = parse_activity_unit(data.get('unit', 'uCi'))
                act_bq = data['activity'] * factor

                if iso not in isotope_totals:
                    isotope_totals[iso] = 0
                isotope_totals[iso] += act_bq

        sorted_isos = sorted(isotope_totals.items(), key=lambda x: x[1], reverse=True)
        results[mat] = sorted_isos[:top_n]

    return results


def activity_to_bq(activity: float, unit: str) -> float:
    factor = parse_activity_unit(unit)
    return activity * factor


# ==============================================================================#
# FLUX WIRE LOADER
# ==============================================================================#

WIRE_METADATA = [
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
    {"sample": "Sc-RAFM-1", "iso": "sc45", "prod": "sc46", "mass_mg": 0.9645, "xs": 27.14, "unit": "b", "e_start": 2.04e-9, "e_end": 5.25e-6},
    {"sample": "Sc-RAFM-2", "iso": "sc45", "prod": "sc46", "mass_mg": 0.7282, "xs": 27.14, "unit": "b", "e_start": 2.04e-9, "e_end": 5.25e-6},
    {"sample": "Co-RAFM-1", "iso": "co59", "prod": "co60", "mass_mg": 4.0661, "xs": 37.18, "unit": "b", "e_start": 2.23e-9, "e_end": 1.86e-4},
    {"sample": "Co-RAFM-2", "iso": "co59", "prod": "co60", "mass_mg": 2.9945, "xs": 37.18, "unit": "b", "e_start": 2.23e-9, "e_end": 1.86e-4},
    {"sample": "Cu-RAFM-1", "iso": "cu63", "prod": "cu64", "mass_mg": 1.3748, "xs": 4.50, "unit": "b", "e_start": 2.10e-9, "e_end": 2.77e-3},
    {"sample": "Cu-RAFM-2", "iso": "cu63", "prod": "cu64", "mass_mg": 1.2332, "xs": 4.50, "unit": "b", "e_start": 2.10e-9, "e_end": 2.77e-3},
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


def _time_unit_to_seconds(unit: str) -> float:
    unit = unit.lower().strip().rstrip('.')
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


def get_metadata_df() -> pd.DataFrame:
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


ACTIVITY_PATTERN_WIRE = re.compile(
    r"^(?P<iso>[A-Za-z]+\d+m?)\s+(?P<hl_val>\d+\.?\d*)\s*(?P<hl_unit>[smhdywk]+)\s+\w+\s+Activity\s*=\s*(?P<act>[0-9.E+\-]+)\s*[±±]?\s*(?P<unc>[0-9.E+%\-]*)\s*(?P<unit>.*)$",
    re.IGNORECASE,
)

IRRADIATION_PATTERN = re.compile(
    r'irradiat\w* time\s*[:=]\s*([0-9.+-eE]+)\s*(s|sec|seconds|m|min|minutes|h|hr|hours)',
    re.IGNORECASE
)


def parse_measurement_datetime(lines: List[str]) -> Optional[datetime]:
    if dtparser is None:
        return None

    for line in lines:
        m = re.search(r"Date\s*[:=]\s*(.*)", line, re.IGNORECASE)
        if m:
            txt = m.group(1).strip()
            try:
                return dtparser.parse(txt, fuzzy=True)
            except Exception:
                continue

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
    if any(np.isnan([activity_bq, sigma_cm2, mass_g])):
        return np.nan, np.nan
    if mass_g <= 0 or half_life_seconds <= 0:
        return np.nan, np.nan

    lam = LN2 / half_life_seconds
    N_atoms = calculate_n_atoms(mass_g, target_mass_number)

    S = 1 - np.exp(-lam * irradiation_seconds)
    D = np.exp(-lam * decay_seconds)

    denom = N_atoms * sigma_cm2 * S * D

    phi = activity_bq / denom if denom > 0 else np.nan

    phi_unc = np.nan
    if np.isfinite(phi) and activity_bq > 0:
        phi_unc = phi * (uncertainty_bq / activity_bq)

    return phi, phi_unc


def load_flux_wires(
    flux_wires_dir: str = 'flux_wires',
    sample_filter: Optional[str] = None,
    default_irradiation_s: float = 7200,
    default_decay_s: float = 0,
    output_csv: Optional[str] = None
) -> pd.DataFrame:
    flux_dir = Path(flux_wires_dir)
    if not flux_dir.exists():
        print(f"Warning: Flux wires directory not found: {flux_dir}")
        return pd.DataFrame()

    meta_df = get_metadata_df()
    records = []

    for filepath in sorted(glob.glob(str(flux_dir / '*.txt'))):
        sample_name = Path(filepath).stem

        if sample_filter and not re.search(sample_filter, sample_name):
            continue

        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        meas_dt = parse_measurement_datetime(lines)
        irradiation_seconds = parse_irradiation_time(lines) or default_irradiation_s
        decay_seconds = default_decay_s

        for line in lines:
            m = ACTIVITY_PATTERN_WIRE.match(line.strip())
            if not m:
                continue

            iso_raw = m.group('iso')
            hl_val = float(m.group('hl_val'))
            hl_unit = m.group('hl_unit')
            activity_raw = float(m.group('act'))
            unc_str = m.group('unc')
            unit = m.group('unit')

            activity_bq = activity_raw * parse_activity_unit(unit)
            uncertainty_bq = 0.0

            try:
                if '%' in unc_str:
                    unc_pct = float(unc_str.replace('%', ''))
                    uncertainty_bq = (unc_pct / 100.0) * activity_bq
                elif unc_str:
                    uncertainty_bq = float(unc_str) * parse_activity_unit(unit)
            except Exception:
                pass

            canon = canonical_iso(iso_raw)

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

            specific_activity_bq = activity_bq / mass_g if mass_g > 0 else np.nan
            specific_activity_uci = specific_activity_bq / 37000.0 if not np.isnan(specific_activity_bq) else np.nan
            specific_activity_uci_unc = (uncertainty_bq / mass_g / 37000.0) if (mass_g > 0 and not np.isnan(uncertainty_bq)) else np.nan

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
                'half_life': f"{hl_val} {hl_unit}",
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
        print(f"Saved flux wire activity summary to: {output_path}")

    return df


def compute_flux_from_measurements(
    flux_wires_df: pd.DataFrame,
    meta_df: Optional[pd.DataFrame] = None,
    default_irradiation_seconds: float = 7203,
    default_decay_seconds: float = 0
) -> pd.DataFrame:
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

        mass_match = re.search(r"(\d+)", mrow['iso_canon'])
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


def parse_half_life_seconds(hl_str: str) -> Optional[float]:
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


def load_mcnp_spectrum(
    spectrum_csv: str,
    energy_scale: str = 'MeV',
    flux_divisor: float = 15.0
) -> Optional[Dict[str, np.ndarray]]:
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
        mass_match = re.search(r"(\d+)", mrow['iso_canon'])
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
