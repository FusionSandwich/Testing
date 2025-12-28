"""
ALARA CSV helpers for cooling time matching.

Keeps the parsing logic for cooling time columns in one place so that
comparison/threshold plots can reuse it.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional

import pandas as pd

from alara_output_processing import SECONDS_CONV

_TIME_UNIT_ALIASES = {
    's': 's', 'sec': 's', 'secs': 's', 'second': 's', 'seconds': 's',
    'm': 'm', 'min': 'm', 'mins': 'm', 'minute': 'm', 'minutes': 'm',
    'h': 'h', 'hr': 'h', 'hrs': 'h', 'hour': 'h', 'hours': 'h',
    'd': 'd', 'day': 'd', 'days': 'd',
    'w': 'w', 'wk': 'w', 'wks': 'w', 'week': 'w', 'weeks': 'w',
    'y': 'y', 'yr': 'y', 'yrs': 'y', 'year': 'y', 'years': 'y',
    'c': 'c', 'century': 'c', 'centuries': 'c',
}


def parse_time_to_seconds(label: str) -> Optional[float]:
    """Parse cooling time labels like '300s', '2 h', '5.95 m', 'shutdown'."""
    if label is None:
        return None

    text = str(label).strip().lower()
    if not text:
        return None
    if text == 'shutdown':
        return 0.0

    text = re.sub(r'^(mean|sem|rel_unc)_', '', text)
    text = text.replace('_', '').replace(' ', '')

    match = re.match(r'^([+-]?[\d.]+(?:e[+-]?\d+)?)([a-z]+)?$', text)
    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2) or 's'
    unit_key = _TIME_UNIT_ALIASES.get(unit, unit)
    if unit_key not in SECONDS_CONV:
        return None

    return value * SECONDS_CONV[unit_key]


def format_seconds_label(seconds: float) -> str:
    """Format seconds into a compact ALARA-style label."""
    if seconds == 0:
        return 'shutdown'

    for unit in ('d', 'h', 'm', 's'):
        divisor = SECONDS_CONV[unit]
        if seconds >= divisor and seconds % divisor == 0:
            value = seconds / divisor
            return f"{value:g}{unit}"

    return f"{seconds:g}s"


def extract_mean_columns(alara_df: pd.DataFrame) -> List[str]:
    """Return mean columns from an ALARA averaged CSV (or all non-isotope columns)."""
    mean_cols = [c for c in alara_df.columns if c.startswith('mean_')]
    if mean_cols:
        return mean_cols
    return [c for c in alara_df.columns if c != 'isotope']


def find_closest_column(alara_df: pd.DataFrame, target_time: str) -> Optional[str]:
    """Find the closest ALARA column to the requested cooling time label."""
    target_seconds = parse_time_to_seconds(target_time)
    if target_seconds is None:
        return None

    best_col = None
    best_diff = None

    for col in extract_mean_columns(alara_df):
        col_seconds = parse_time_to_seconds(col)
        if col_seconds is None:
            continue
        diff = abs(col_seconds - target_seconds)
        if best_diff is None or diff < best_diff:
            best_diff = diff
            best_col = col

    return best_col


def build_cooling_map(alara_df: pd.DataFrame, exp_cooling_times: Iterable[str]) -> Dict[str, str]:
    """Map experimental cooling labels to the closest ALARA output column names."""
    cooling_map = {}
    for label in exp_cooling_times:
        col = find_closest_column(alara_df, label)
        if col:
            cooling_map[label] = col
    return cooling_map


class ALARADataLoader:
    """Lightweight loader for ALARA CSV outputs with cooling-time mapping."""

    def __init__(self, alara_df: pd.DataFrame):
        self.alara_df = alara_df

    @classmethod
    def from_csv(cls, csv_path: str) -> "ALARADataLoader":
        return cls(pd.read_csv(csv_path))

    def build_cooling_map(self, exp_cooling_times: Iterable[str]) -> Dict[str, str]:
        return build_cooling_map(self.alara_df, exp_cooling_times)
