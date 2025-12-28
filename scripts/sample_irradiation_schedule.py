#!/usr/bin/env python3
"""
Sample-Specific Irradiation Schedule Calculator

This module parses experimental gamma spectroscopy files and calculates
the correct irradiation and cooling times for each RAFM3 sample.

Irradiation Schedule:
1. **Phase 1: 3-second irradiation**
   - Starts 6 minutes before the 300s gamma spec measurement time
   - Cooling measurements: 300s, 2hr, 24hr, 4d (relative to 3s irradiation end)

2. **Phase 2: 2-hour irradiation** 
   - Separate irradiation for long-term cooling
   - Cooling measurement: 15d (relative to 2hr irradiation end)

Sample Mapping:
- RAFM3-A → EUROFER97_2 (tally_85244)
- RAFM3-B → EUROFER97_3 (tally_85234)
- RAFM3-C → EUROFER97_4 (tally_85224)
- RAFM3-N → CNA (tally_85214)
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Sample to material mapping
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

# Cooling time labels in order
COOLING_LABELS_PHASE1 = ['300s', '2h', '24h', '4d']  # From 3s irradiation
COOLING_LABELS_PHASE2 = ['15d']  # From 2hr irradiation

# Phase 1: 3-second irradiation
PHASE1_IRRADIATION_SECONDS = 3
PHASE1_IRRADIATION_OFFSET_BEFORE_300S = 360  # 6 minutes = 360 seconds

# Phase 2: 2-hour irradiation  
PHASE2_IRRADIATION_SECONDS = 7200  # 2 hours

# Phase 2 irradiation START time: August 4, 2025 at 1:00 PM (13:00) (same for ALL samples)
# The 2hr irradiation ran from 1:00 PM to 3:00 PM on August 4, 2025
PHASE2_IRRADIATION_START = datetime(2025, 8, 4, 13, 0, 0)

# Aliases for backward compatibility and notebook use
SAMPLE_LETTERS = list(SAMPLE_TO_MATERIAL.keys())  # ['A', 'B', 'C', 'N']
SAMPLE_TO_MATERIAL_MAP = SAMPLE_TO_MATERIAL  # Alias
MATERIAL_TO_TALLY_MAP = MATERIAL_TO_TALLY  # Alias

# Irradiation timing aliases (for notebook import)
FIRST_IRR_DURATION = PHASE1_IRRADIATION_SECONDS  # 3 seconds
FIRST_IRR_OFFSET_BEFORE_300S = PHASE1_IRRADIATION_OFFSET_BEFORE_300S  # 360 seconds
SECOND_IRR_DURATION = PHASE2_IRRADIATION_SECONDS  # 7200 seconds (2 hours)
SECOND_IRR_START = PHASE2_IRRADIATION_START  # August 4, 2025 at 1:00 PM
SECOND_IRR_END = SECOND_IRR_START + timedelta(seconds=SECOND_IRR_DURATION)

# Cooling time file patterns
RAFM3_PATTERNS = {
    '300sEOI': '300s',
    '2hrEOI': '2h',
    '24hrEOI': '24h',
    '4dEOI': '4d',
}
RAFM4_PATTERNS = {
    '15dEOI': '15d',
}


def parse_date_from_file(filepath: Path) -> Optional[datetime]:
    """
    Parse the measurement date/time from a gamma spec file header.
    
    Expected format: "File: ... Date:  July 31, 2025 09:23:21"
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                match = re.search(r'Date:\s*(.+?)$', line, re.IGNORECASE)
                if match:
                    date_str = match.group(1).strip()
                    # Try multiple date formats
                    formats = [
                        '%B %d, %Y %H:%M:%S',  # July 31, 2025 09:23:21
                        '%b %d, %Y %H:%M:%S',  # Jul 31, 2025 09:23:21
                        '%Y-%m-%d %H:%M:%S',   # 2025-07-31 09:23:21
                    ]
                    for fmt in formats:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                    # Try dateutil parser as fallback
                    try:
                        from dateutil import parser as dtparser
                        return dtparser.parse(date_str)
                    except:
                        pass
    except Exception as e:
        print(f"Error parsing date from {filepath}: {e}")
    return None


# Alias for backward compatibility with notebook
def parse_date_from_gamma_file(filepath):
    """Alias for parse_date_from_file for backward compatibility."""
    return parse_date_from_file(Path(filepath))


def get_sample_measurement_times(exp_data_dir: Path) -> Dict[str, Dict[str, datetime]]:
    """
    Parse all experimental files and extract measurement times for each sample.
    
    Returns:
        Dict mapping sample letter to dict of cooling_label -> measurement_datetime
        e.g., {'A': {'300s': datetime(...), '2h': datetime(...), ...}, ...}
    """
    measurements = {}
    
    # Mapping from filename pattern to cooling label
    file_patterns = {
        '300sEOI': '300s',
        '2hrEOI': '2h',
        '24hrEOI': '24h',
        '4dEOI': '4d',
        '15dEOI': '15d',
    }
    
    for sample_letter in ['A', 'B', 'C', 'N']:
        measurements[sample_letter] = {}
        
        for pattern, label in file_patterns.items():
            filename = f"RAFM3-{sample_letter}_{pattern}.txt"
            filepath = exp_data_dir / filename
            
            if filepath.exists():
                meas_time = parse_date_from_file(filepath)
                if meas_time:
                    measurements[sample_letter][label] = meas_time
                else:
                    print(f"Warning: Could not parse date from {filename}")
            else:
                print(f"Warning: File not found: {filename}")
    
    return measurements


def calculate_sample_schedule(sample_letter: str, 
                              measurement_times: Dict[str, datetime]) -> Dict:
    """
    Calculate the complete irradiation schedule for a sample.
    
    Args:
        sample_letter: 'A', 'B', 'C', or 'N'
        measurement_times: Dict of cooling_label -> measurement_datetime
        
    Returns:
        Dict with:
        - 'sample': sample letter
        - 'material': ALARA material name
        - 'tally': tally name
        - 'phase1': {
            'irradiation_time': "3 s",
            'irradiation_start': datetime,
            'irradiation_end': datetime,
            'cooling_times': [{'label': str, 'seconds': float, 'alara_format': str}, ...]
          }
        - 'phase2': {
            'irradiation_time': "2 h",
            'irradiation_start': datetime (estimated),
            'irradiation_end': datetime (estimated),
            'cooling_times': [{'label': str, 'seconds': float, 'alara_format': str}, ...]
          }
    """
    material = SAMPLE_TO_MATERIAL.get(sample_letter, 'UNKNOWN')
    tally = MATERIAL_TO_TALLY.get(material, 'UNKNOWN')
    
    schedule = {
        'sample': sample_letter,
        'material': material,
        'tally': tally,
        'phase1': None,
        'phase2': None,
    }
    
    # Phase 1: 3-second irradiation
    # Irradiation ENDS 6 minutes before the 300s measurement (so cooling = exactly 6 min)
    if '300s' in measurement_times:
        meas_300s = measurement_times['300s']
        
        # 3s irradiation ends 6 minutes before 300s measurement
        irr_end = meas_300s - timedelta(seconds=PHASE1_IRRADIATION_OFFSET_BEFORE_300S)
        irr_start = irr_end - timedelta(seconds=PHASE1_IRRADIATION_SECONDS)
        
        phase1_cooling = []
        for label in COOLING_LABELS_PHASE1:
            if label in measurement_times:
                meas_time = measurement_times[label]
                cooling_seconds = (meas_time - irr_end).total_seconds()
                
                if cooling_seconds < 0:
                    print(f"Warning: Negative cooling time for {sample_letter} {label}: {cooling_seconds}s")
                    cooling_seconds = 0
                
                phase1_cooling.append({
                    'label': label,  # Category from filename (300s, 2h, 24h, 4d)
                    'category': label,  # Same as label - for clarity
                    'seconds': cooling_seconds,
                    'alara_format': format_seconds_to_alara(cooling_seconds),
                    'measurement_time': meas_time,
                })
        
        schedule['phase1'] = {
            'irradiation_time': "3 s",
            'irradiation_seconds': PHASE1_IRRADIATION_SECONDS,
            'irradiation_start': irr_start,
            'irradiation_end': irr_end,
            'cooling_times': phase1_cooling,
        }
    
    # Phase 2: 2-hour irradiation for 15d measurement
    # FIXED: All samples use the same irradiation start time: August 4, 2025 at 11:00 AM
    # Cooling time is calculated from irradiation END to each sample's 15d measurement
    if '15d' in measurement_times:
        meas_15d = measurement_times['15d']
        
        # Phase 2 irradiation start time is fixed for all samples
        irr_start_phase2 = PHASE2_IRRADIATION_START
        irr_end_phase2 = irr_start_phase2 + timedelta(seconds=PHASE2_IRRADIATION_SECONDS)
        
        # Calculate actual cooling time from irradiation end to 15d measurement
        actual_cooling_15d = (meas_15d - irr_end_phase2).total_seconds()
        
        if actual_cooling_15d < 0:
            print(f"Warning: Negative cooling time for {sample_letter} 15d: {actual_cooling_15d}s")
            print(f"  Irradiation end: {irr_end_phase2}")
            print(f"  Measurement: {meas_15d}")
            actual_cooling_15d = 0
        
        schedule['phase2'] = {
            'irradiation_time': "2 h",
            'irradiation_seconds': PHASE2_IRRADIATION_SECONDS,
            'irradiation_start': irr_start_phase2,
            'irradiation_end': irr_end_phase2,
            'cooling_times': [{
                'label': '15d',
                'seconds': actual_cooling_15d,
                'alara_format': format_seconds_to_alara(actual_cooling_15d),
                'measurement_time': meas_15d,
            }],
        }
    
    return schedule


def format_seconds_to_alara(seconds: float) -> str:
    """
    Format seconds into ALARA-compatible time string.
    Uses appropriate units (s, m, h, d, y) for readability.
    """
    if seconds < 0:
        return "0 s"
    
    # Use the most appropriate unit
    if seconds < 120:  # < 2 minutes
        return f"{seconds:.1f} s"
    elif seconds < 7200:  # < 2 hours
        minutes = seconds / 60
        return f"{minutes:.2f} m"
    elif seconds < 172800:  # < 2 days
        hours = seconds / 3600
        return f"{hours:.4f} h"
    elif seconds < 63072000:  # < 2 years
        days = seconds / 86400
        return f"{days:.4f} d"
    else:
        years = seconds / (365.25 * 86400)
        return f"{years:.4f} y"


def get_all_sample_schedules(exp_data_dir: Path) -> Dict[str, Dict]:
    """
    Get complete irradiation schedules for all samples.
    
    Returns:
        Dict mapping sample letter to schedule dict
    """
    measurement_times = get_sample_measurement_times(exp_data_dir)
    
    schedules = {}
    for sample_letter, meas_times in measurement_times.items():
        if meas_times:
            schedules[sample_letter] = calculate_sample_schedule(sample_letter, meas_times)
    
    return schedules


def print_schedule_summary(schedules: Dict[str, Dict]):
    """Print a human-readable summary of all sample schedules."""
    print("=" * 80)
    print("SAMPLE IRRADIATION SCHEDULES")
    print("=" * 80)
    
    for sample_letter, schedule in sorted(schedules.items()):
        print(f"\n{'='*40}")
        print(f"SAMPLE RAFM3-{sample_letter} → {schedule['material']} ({schedule['tally']})")
        print(f"{'='*40}")
        
        if schedule['phase1']:
            p1 = schedule['phase1']
            print(f"\nPhase 1: {p1['irradiation_time']} irradiation")
            print(f"  Start: {p1['irradiation_start']}")
            print(f"  End:   {p1['irradiation_end']}")
            print(f"  Cooling times:")
            for ct in p1['cooling_times']:
                print(f"    {ct['label']:6s} → {ct['alara_format']:>12s} ({ct['seconds']:.0f}s) @ {ct['measurement_time']}")
        
        if schedule['phase2']:
            p2 = schedule['phase2']
            print(f"\nPhase 2: {p2['irradiation_time']} irradiation")
            print(f"  Start: {p2['irradiation_start']}")
            print(f"  End:   {p2['irradiation_end']}")
            print(f"  Cooling times:")
            for ct in p2['cooling_times']:
                print(f"    {ct['label']:6s} → {ct['alara_format']:>12s} ({ct['seconds']:.0f}s) @ {ct['measurement_time']}")


def generate_alara_schedule_block(schedule: Dict, phase: int = 1) -> str:
    """
    Generate the ALARA schedule and cooling blocks for a specific phase.
    
    Args:
        schedule: Sample schedule dict
        phase: 1 for 3s irradiation, 2 for 2hr irradiation
        
    Returns:
        String containing ALARA schedule, pulsehistory, and cooling blocks
    """
    phase_key = f'phase{phase}'
    if phase_key not in schedule or schedule[phase_key] is None:
        return ""
    
    p = schedule[phase_key]
    irr_time = p['irradiation_time']
    
    lines = []
    lines.append(f"# Phase {phase}: {irr_time} irradiation")
    lines.append(f"# Irradiation start: {p['irradiation_start']}")
    lines.append(f"# Irradiation end: {p['irradiation_end']}")
    lines.append("")
    
    # Schedule block
    lines.append("schedule irradiation")
    lines.append(f"    {irr_time} flux_1 pulse_once 0 s")
    lines.append("end")
    lines.append("")
    
    # Pulse history
    lines.append("pulsehistory pulse_once")
    lines.append("    1 0 s")
    lines.append("end")
    lines.append("")
    
    # Cooling times
    lines.append("cooling")
    for ct in p['cooling_times']:
        lines.append(f"    {ct['alara_format']}  # {ct['label']} measurement")
    lines.append("end")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test the module
    exp_dir = Path(__file__).parent / "Experimental_Data" / "RAFM3"
    
    if exp_dir.exists():
        schedules = get_all_sample_schedules(exp_dir)
        print_schedule_summary(schedules)
        
        print("\n" + "=" * 80)
        print("ALARA SCHEDULE BLOCKS")
        print("=" * 80)
        
        for sample_letter, schedule in sorted(schedules.items()):
            print(f"\n# Sample RAFM3-{sample_letter}")
            print(generate_alara_schedule_block(schedule, phase=1))
            if schedule['phase2']:
                print("\n# --- Phase 2 would be a separate ALARA run ---")
                print(generate_alara_schedule_block(schedule, phase=2))
    else:
        print(f"Experimental data directory not found: {exp_dir}")
