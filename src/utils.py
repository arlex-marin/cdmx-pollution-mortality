"""
Utility functions for file I/O, logging, and data handling.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Fixed logging directory creation, added np.bool_ JSON serialization
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import unicodedata
import warnings
from pathlib import Path

def get_project_root() -> Path:
    """Return project root directory (parent of src/)."""
    return Path(__file__).parent.parent

PROJECT_ROOT = get_project_root()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

def safe_int(value):
    """Safely convert value to integer, handling strings and special characters."""
    if pd.isna(value):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        value = value.strip()
        if value in ['*', '', 'N/D', 'NA', 'N.D.']:
            return 0
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return 0
    return 0


def normalize_string(s):
    """Normalize string by removing accents and converting to lowercase."""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    return s.lower()


def format_number(n):
    """Format number with commas."""
    return f"{n:,.0f}"


def format_percent(value, total):
    """Format percentage."""
    if total > 0:
        return f"{value/total*100:.2f}%"
    return "0.00%"


def format_pvalue(p):
    """Format p-value with significance stars."""
    if p < 0.001:
        return "p < 0.001 ***"
    elif p < 0.01:
        return f"p = {p:.3f} **"
    elif p < 0.05:
        return f"p = {p:.3f} *"
    else:
        return f"p = {p:.3f}"


def clamp_proportion(value, min_val=0.0, max_val=1.0, default=0.52):
    """Clamp a proportion value to valid range."""
    if pd.isna(value):
        return default
    return max(min_val, min(max_val, value))


def read_csv_flexible(filepath, encodings_to_try=None):
    """Read CSV with flexible handling of inconsistent column counts."""
    if encodings_to_try is None:
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                lines = f.readlines()

            parsed_lines = []
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if i == 0:
                    header = [p.strip().strip('"') for p in parts]
                    expected_cols = len(header)
                    parsed_lines.append(header)
                else:
                    if len(parts) > expected_cols:
                        parts = parts[:expected_cols]
                    elif len(parts) < expected_cols:
                        parts.extend([''] * (expected_cols - len(parts)))
                    cleaned_parts = [p.strip().strip('"') for p in parts]
                    parsed_lines.append(cleaned_parts)

            if parsed_lines:
                header = parsed_lines[0]
                data = parsed_lines[1:]
                df = pd.DataFrame(data, columns=header)
                return df, encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            warnings.warn(f"Error reading with encoding {encoding}: {e}")
            continue

    raise ValueError(f"Could not read {filepath} with any encoding")


def setup_logging(prefix="analysis"):
    """
    Setup logging to capture both stdout and stderr.

    Creates the logs directory if it doesn't exist.
    """
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOGS_DIR / f'{prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Log started: {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

    return log_file


def save_json(data, filepath):
    """Save data as JSON with proper encoding."""
    def convert_to_serializable(obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {str(k): convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(i) for i in obj]
        return obj

    data_serializable = convert_to_serializable(data)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_serializable, f, indent=2, ensure_ascii=False)


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_census_file_path(year):
    """Get the path to a census file for a given year."""
    from . import CENSUS_RAW_DIR

    file_map = {
        2000: 'RESLOC2000_09_CDMX.csv',
        2005: 'RESLOC2005_09_CDMX.csv',
        2010: 'RESLOC2010_09_CDMX.csv',
        2020: 'ITER2020_09_CDMX.csv'
    }
    return CENSUS_RAW_DIR / file_map[year]


def get_mortality_file_path(year):
    """Get the path to a mortality file for a given year."""
    from . import MORTALITY_RAW_DIR
    return MORTALITY_RAW_DIR / f'{year}.csv'


def get_pollution_file_path():
    """Get the path to the pollution data file."""
    from . import POLLUTION_RAW_DIR
    return POLLUTION_RAW_DIR / 'Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv'


def get_population_processed_path():
    """Get the path to the harmonized population file."""
    from . import POPULATION_PROCESSED_DIR
    return POPULATION_PROCESSED_DIR / 'cdmx_population_harmonized_2000_2022.csv'


def get_mortality_processed_path():
    """Get the path to the processed mortality file."""
    from . import MORTALITY_PROCESSED_DIR
    return MORTALITY_PROCESSED_DIR / 'cdmx_lung_cancer_deaths_2000_2022.csv'


def get_integrated_dataset_path():
    """Get the path to the final analytical dataset."""
    from . import INTEGRATED_PROCESSED_DIR
    return INTEGRATED_PROCESSED_DIR / 'cdmx_analysis_dataset_2004_2022.csv'


def get_shapefile_path():
    """
    Get the path to the CDMX shapefile using recursive search.

    Returns:
    --------
    Path
        Path to 09mun.shp

    Raises:
    -------
    FileNotFoundError
        If shapefile cannot be found
    """
    from . import SHAPEFILE_DIR

    matches = list(SHAPEFILE_DIR.rglob('09mun.shp'))
    if matches:
        return matches[0]

    raise FileNotFoundError(
        f"Municipal shapefile '09mun.shp' not found in {SHAPEFILE_DIR}.\n"
        "Please ensure the INEGI shapefile is properly extracted."
    )


# Alcaldía codes for CDMX
ALCALDIA_CODES = {
    '002': 'Azcapotzalco',
    '003': 'Coyoacan',
    '004': 'Cuajimalpa de Morelos',
    '005': 'Gustavo A. Madero',
    '006': 'Iztacalco',
    '007': 'Iztapalapa',
    '008': 'La Magdalena Contreras',
    '009': 'Milpa Alta',
    '010': 'Alvaro Obregon',
    '011': 'Tlahuac',
    '012': 'Tlalpan',
    '013': 'Xochimilco',
    '014': 'Benito Juarez',
    '015': 'Cuauhtemoc',
    '016': 'Miguel Hidalgo',
    '017': 'Venustiano Carranza'
}

# Reverse mapping
ALCALDIA_NAME_TO_CODE = {v: k for k, v in ALCALDIA_CODES.items()}

# CDMX Entity Code
CDMX_ENTIDAD = '09'
CDMX_ENTIDAD_INT = 9

# Harmonized age groups
HARMONIZED_AGE_GROUPS = ['0-4', '5-14', '15-17', '18-24', '25-59', '60+']

# WHO Standard Population Weights
WHO_WEIGHTS = {
    '0-4': 0.0886,
    '5-14': 0.1729,
    '15-17': 0.0254,
    '18-24': 0.0702,
    '25-59': 0.5167,
    '60+': 0.1262
}

# ICD-10 codes for lung cancer
LUNG_CANCER_CODES = ['C33', 'C34']

# Pollutants available for analysis
POLLUTANTS = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']

# Alcaldías with pollution data (from validation)
ALCALDIAS_WITH_POLLUTION = [
    'Azcapotzalco', 'Benito Juarez', 'Coyoacan', 'Cuajimalpa de Morelos',
    'Cuauhtemoc', 'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa',
    'Miguel Hidalgo', 'Milpa Alta', 'Tlalpan', 'Venustiano Carranza',
    'Xochimilco', 'Alvaro Obregon'
]

# Alcaldías without pollution data
ALCALDIAS_WITHOUT_POLLUTION = ['La Magdalena Contreras', 'Tlahuac']

# Census years
CENSUS_YEARS = [2000, 2005, 2010, 2020]

# Analysis years (matching pollution data availability)
# Analysis limited to 2004-2022 because:
# - 2023 mortality data not yet fully validated
# - Pollution data from Zenodo ends in 2022
ANALYSIS_YEARS = (2004, 2022)
