"""
Data validation functions for census, mortality, and pollution datasets.

This module performs comprehensive validation of all raw data sources used in
the analysis. It checks data completeness, identifies potential issues, and
generates validation reports for quality assurance.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Fixed bare except clauses, improved encoding detection,
                         added comprehensive error handling, enhanced reporting
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

from .utils import (
    safe_int, read_csv_flexible, save_json, format_number, format_percent,
    ALCALDIA_CODES, CDMX_ENTIDAD, CDMX_ENTIDAD_INT, LUNG_CANCER_CODES,
    HARMONIZED_AGE_GROUPS, POLLUTANTS, normalize_string,
    get_census_file_path, get_mortality_file_path, get_pollution_file_path
)
from . import LOGS_DIR, CENSUS_RAW_DIR, MORTALITY_RAW_DIR, POLLUTION_RAW_DIR


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def read_census_with_encoding_detection(filepath, year):
    """
    Read census file with proper encoding detection.

    Attempts multiple common encodings and falls back to a flexible CSV reader
    if standard methods fail. Provides clear error messages when all attempts fail.

    Parameters:
    -----------
    filepath : Path
        Path to census file
    year : int
        Census year (for error messages)

    Returns:
    --------
    df : pd.DataFrame
        Loaded census data
    encoding : str
        Successfully used encoding

    Raises:
    -------
    ValueError
        If file cannot be read with any encoding
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    df = None
    successful_encoding = None

    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(filepath, encoding=encoding, engine='c', on_bad_lines='skip')
            successful_encoding = encoding
            break
        except UnicodeDecodeError:
            # Expected for wrong encoding - continue trying
            continue
        except Exception as e:
            # Unexpected error - log but continue trying other encodings
            warnings.warn(f"Unexpected error with encoding {encoding} for {year} census: {e}")
            continue

    if df is None:
        # Fall back to flexible reader for malformed CSV files
        try:
            df, successful_encoding = read_csv_flexible(filepath)
        except Exception as e:
            raise ValueError(
                f"Could not read census file {filepath} for year {year} with any encoding. "
                f"Last error: {e}"
            )

    if df is None or len(df) == 0:
        raise ValueError(f"Census file {filepath} appears to be empty")

    return df, successful_encoding


def validate_age_group_coverage(df_alcaldias, year):
    """
    Validate that age groups in census data can be properly harmonized.

    Parameters:
    -----------
    df_alcaldias : pd.DataFrame
        Filtered census data for CDMX alcaldías
    year : int
        Census year

    Returns:
    --------
    dict
        Validation results for age groups
    """
    age_cols_available = []
    age_cols_missing = []

    # Expected age columns by year
    expected_cols = {
        2000: ['POB0_4', 'POB6_14', 'POB15_17', 'POB15_24', 'POB18_', 'POB15_'],
        2005: ['P_0A4_FE', 'P_0A4_MA', 'P_6A14_F', 'P_6A14_M', 'P_5_AN',
               'P_15A24', 'P_15A59_F', 'P_15A59_M', 'P_F_60YMAS', 'P_M_60YMAS'],
        2010: ['P_0A2_F', 'P_3A5_F', 'P_0A2_M', 'P_3A5_M',
               'P_6A11_F', 'P_12A14_F', 'P_6A11_M', 'P_12A14_M',
               'P_15A17_F', 'P_15A17_M', 'P_18A24_F', 'P_18A24_M',
               'P_60YMAS_F', 'P_60YMAS_M', 'P_TOTAL', 'POBFEM', 'POBMAS'],
        2020: ['P_0A4_F', 'P_0A4_M', 'P_5A9_F', 'P_10A14_F', 'P_5A9_M', 'P_10A14_M',
               'P_15A19_F', 'P_15A19_M', 'P_20A24_F', 'P_20A24_M']
    }

    if year in expected_cols:
        for col in expected_cols[year]:
            if col in df_alcaldias.columns:
                age_cols_available.append(col)
            else:
                age_cols_missing.append(col)

    return {
        'available': age_cols_available,
        'missing': age_cols_missing,
        'coverage_pct': len(age_cols_available) / len(expected_cols.get(year, [])) * 100 if expected_cols.get(year) else 0
    }


# =============================================================================
# CENSUS VALIDATION FUNCTIONS
# =============================================================================

def validate_census_2000():
    """
    Validate 2000 census data.

    The 2000 census (XII Censo General de Población y Vivienda) provides
    limited age detail at the municipal level. This validation checks
    data completeness and reports any issues.

    Returns:
    --------
    dict
        Validation results for 2000 census
    """
    filepath = get_census_file_path(2000)

    if not filepath.exists():
        return {
            'year': 2000,
            'status': 'ERROR',
            'error': f'File not found: {filepath}'
        }

    try:
        df, encoding = read_census_with_encoding_detection(filepath, 2000)
        df.columns = [str(col).strip().upper() for col in df.columns]

        # Standardize geographic identifiers
        df['ENTIDAD'] = df['ENTIDAD'].astype(str).str.strip().str.zfill(2)
        df['MUN'] = df['MUN'].astype(str).str.strip().str.zfill(3)
        df['LOC'] = df['LOC'].astype(str).str.strip().str.zfill(4)

        # Filter to CDMX alcaldías
        df_alcaldias = df[
            (df['ENTIDAD'] == CDMX_ENTIDAD) &
            (df['LOC'] == '0000') &
            (df['MUN'].isin(ALCALDIA_CODES.keys()))
        ].copy()

        df_alcaldias['alcaldia'] = df_alcaldias['MUN'].map(ALCALDIA_CODES)

        # Calculate totals
        total_pop = sum(safe_int(row.get('P_TOTAL', 0)) for _, row in df_alcaldias.iterrows())
        total_male = sum(safe_int(row.get('PMASCUL', 0)) for _, row in df_alcaldias.iterrows())
        total_female = sum(safe_int(row.get('PFEMENI', 0)) for _, row in df_alcaldias.iterrows())

        # Validate age group coverage
        age_validation = validate_age_group_coverage(df_alcaldias, 2000)

        # Check for missing alcaldías
        found_alcaldias = set(df_alcaldias['alcaldia'].dropna().unique())
        missing_alcaldias = set(ALCALDIA_CODES.values()) - found_alcaldias

        return {
            'year': 2000,
            'status': 'OK',
            'file': filepath.name,
            'encoding': encoding,
            'total_rows': len(df),
            'alcaldias_found': len(df_alcaldias),
            'alcaldias_missing': list(missing_alcaldias) if missing_alcaldias else [],
            'totals': {
                'total': total_pop,
                'male': total_male,
                'female': total_female
            },
            'sex_ratio': total_male / total_female if total_female > 0 else None,
            'age_columns': age_validation,
            'notes': ['Limited age detail at municipal level']
        }

    except Exception as e:
        return {
            'year': 2000,
            'status': 'ERROR',
            'error': str(e)
        }


def validate_census_2005():
    """
    Validate 2005 Conteo data.

    The 2005 Conteo de Población y Vivienda provides more detailed age
    breakdowns than 2000 but still requires some estimation.

    Returns:
    --------
    dict
        Validation results for 2005 census
    """
    filepath = get_census_file_path(2005)

    if not filepath.exists():
        return {
            'year': 2005,
            'status': 'ERROR',
            'error': f'File not found: {filepath}'
        }

    try:
        df, encoding = read_census_with_encoding_detection(filepath, 2005)
        df.columns = [str(col).strip().upper() for col in df.columns]

        # Standardize geographic identifiers
        df['ENTIDAD'] = df['ENTIDAD'].astype(str).str.strip().str.zfill(2)
        df['MUN'] = df['MUN'].astype(str).str.strip().str.zfill(3)
        df['LOC'] = df['LOC'].astype(str).str.strip().str.zfill(4)

        # Filter to CDMX alcaldías
        df_alcaldias = df[
            (df['ENTIDAD'] == CDMX_ENTIDAD) &
            (df['LOC'] == '0000') &
            (df['MUN'].isin(ALCALDIA_CODES.keys()))
        ].copy()

        df_alcaldias['alcaldia'] = df_alcaldias['MUN'].map(ALCALDIA_CODES)

        # Calculate totals
        total_pop = sum(safe_int(row.get('P_TOTAL', 0)) for _, row in df_alcaldias.iterrows())
        total_male = sum(safe_int(row.get('P_MAS', 0)) for _, row in df_alcaldias.iterrows())
        total_female = sum(safe_int(row.get('P_FEM', 0)) for _, row in df_alcaldias.iterrows())

        # Validate age group coverage
        age_validation = validate_age_group_coverage(df_alcaldias, 2005)

        # Check for missing alcaldías
        found_alcaldias = set(df_alcaldias['alcaldia'].dropna().unique())
        missing_alcaldias = set(ALCALDIA_CODES.values()) - found_alcaldias

        return {
            'year': 2005,
            'status': 'OK',
            'file': filepath.name,
            'encoding': encoding,
            'total_rows': len(df),
            'alcaldias_found': len(df_alcaldias),
            'alcaldias_missing': list(missing_alcaldias) if missing_alcaldias else [],
            'totals': {
                'total': total_pop,
                'male': total_male,
                'female': total_female
            },
            'sex_ratio': total_male / total_female if total_female > 0 else None,
            'age_columns': age_validation,
            'notes': ['15-24 age group available, requires splitting into 15-17 and 18-24']
        }

    except Exception as e:
        return {
            'year': 2005,
            'status': 'ERROR',
            'error': str(e)
        }


def validate_census_2010():
    """
    Validate 2010 census data.

    The 2010 Censo de Población y Vivienda provides detailed quinquennial
    age groups, allowing accurate harmonization.

    Returns:
    --------
    dict
        Validation results for 2010 census
    """
    filepath = get_census_file_path(2010)

    if not filepath.exists():
        return {
            'year': 2010,
            'status': 'ERROR',
            'error': f'File not found: {filepath}'
        }

    try:
        df, encoding = read_census_with_encoding_detection(filepath, 2010)
        df.columns = [str(col).strip().upper() for col in df.columns]

        # Standardize geographic identifiers
        df['ENTIDAD'] = df['ENTIDAD'].astype(str).str.strip().str.zfill(2)
        df['MUN'] = df['MUN'].astype(str).str.strip().str.zfill(3)
        df['LOC'] = df['LOC'].astype(str).str.strip().str.zfill(4)

        # Filter to CDMX alcaldías
        df_alcaldias = df[
            (df['ENTIDAD'] == CDMX_ENTIDAD) &
            (df['LOC'] == '0000') &
            (df['MUN'].isin(ALCALDIA_CODES.keys()))
        ].copy()

        df_alcaldias['alcaldia'] = df_alcaldias['MUN'].map(ALCALDIA_CODES)

        # Calculate totals
        total_pop = sum(safe_int(row.get('P_TOTAL', 0)) for _, row in df_alcaldias.iterrows())
        total_male = sum(safe_int(row.get('POBMAS', 0)) for _, row in df_alcaldias.iterrows())
        total_female = sum(safe_int(row.get('POBFEM', 0)) for _, row in df_alcaldias.iterrows())

        # Validate age group coverage
        age_validation = validate_age_group_coverage(df_alcaldias, 2010)

        # Check for missing alcaldías
        found_alcaldias = set(df_alcaldias['alcaldia'].dropna().unique())
        missing_alcaldias = set(ALCALDIA_CODES.values()) - found_alcaldias

        # Validate 15-17 proportion (used for harmonization)
        total_15_24_f = sum(safe_int(row.get('P_15A17_F', 0)) + safe_int(row.get('P_18A24_F', 0))
                            for _, row in df_alcaldias.iterrows())
        total_15_17_f = sum(safe_int(row.get('P_15A17_F', 0)) for _, row in df_alcaldias.iterrows())
        prop_15_17 = total_15_17_f / total_15_24_f if total_15_24_f > 0 else None

        return {
            'year': 2010,
            'status': 'OK',
            'file': filepath.name,
            'encoding': encoding,
            'total_rows': len(df),
            'alcaldias_found': len(df_alcaldias),
            'alcaldias_missing': list(missing_alcaldias) if missing_alcaldias else [],
            'totals': {
                'total': total_pop,
                'male': total_male,
                'female': total_female
            },
            'sex_ratio': total_male / total_female if total_female > 0 else None,
            'age_columns': age_validation,
            'proportion_15_17_of_15_24': round(prop_15_17, 4) if prop_15_17 else None,
            'notes': ['Most detailed age breakdown available']
        }

    except Exception as e:
        return {
            'year': 2010,
            'status': 'ERROR',
            'error': str(e)
        }


def validate_census_2020():
    """
    Validate 2020 census data.

    The 2020 Censo de Población y Vivienda provides the most detailed
    age breakdown, requiring minimal estimation. Note that POBTOT is
    empty and totals must be calculated from age groups.

    Returns:
    --------
    dict
        Validation results for 2020 census
    """
    filepath = get_census_file_path(2020)

    if not filepath.exists():
        return {
            'year': 2020,
            'status': 'ERROR',
            'error': f'File not found: {filepath}'
        }

    try:
        df, encoding = read_census_with_encoding_detection(filepath, 2020)
        df.columns = [str(col).strip().upper() for col in df.columns]

        # Standardize geographic identifiers
        df['ENTIDAD'] = df['ENTIDAD'].astype(str).str.strip().str.zfill(2)
        df['MUN'] = df['MUN'].astype(str).str.strip().str.zfill(3)
        df['LOC'] = df['LOC'].astype(str).str.strip().str.zfill(4)

        # Filter to CDMX alcaldías
        df_alcaldias = df[
            (df['ENTIDAD'] == CDMX_ENTIDAD) &
            (df['LOC'] == '0000') &
            (df['MUN'].isin(ALCALDIA_CODES.keys()))
        ].copy()

        df_alcaldias['alcaldia'] = df_alcaldias['MUN'].map(ALCALDIA_CODES)

        # Calculate totals from age groups (POBTOT is empty in this file)
        age_groups = ['0A4', '5A9', '10A14', '15A19', '20A24', '25A29', '30A34',
                      '35A39', '40A44', '45A49', '50A54', '55A59', '60A64',
                      '65A69', '70A74', '75A79', '80A84', '85YMAS']

        total_male = 0
        total_female = 0

        for _, row in df_alcaldias.iterrows():
            total_male += sum(safe_int(row.get(f'P_{age}_M', 0)) for age in age_groups)
            total_female += sum(safe_int(row.get(f'P_{age}_F', 0)) for age in age_groups)

        total_pop = total_male + total_female

        # Validate age group coverage
        age_validation = validate_age_group_coverage(df_alcaldias, 2020)

        # Check for missing alcaldías
        found_alcaldias = set(df_alcaldias['alcaldia'].dropna().unique())
        missing_alcaldias = set(ALCALDIA_CODES.values()) - found_alcaldias

        return {
            'year': 2020,
            'status': 'OK',
            'file': filepath.name,
            'encoding': encoding,
            'total_rows': len(df),
            'alcaldias_found': len(df_alcaldias),
            'alcaldias_missing': list(missing_alcaldias) if missing_alcaldias else [],
            'totals': {
                'total': total_pop,
                'male': total_male,
                'female': total_female
            },
            'sex_ratio': total_male / total_female if total_female > 0 else None,
            'age_columns': age_validation,
            'notes': ['Total calculated from sum of age groups (POBTOT is empty)']
        }

    except Exception as e:
        return {
            'year': 2020,
            'status': 'ERROR',
            'error': str(e)
        }


def validate_all_censuses():
    """
    Run validation on all census files (2000, 2005, 2010, 2020).

    Returns:
    --------
    list
        List of validation result dictionaries
    """
    print("\n" + "=" * 80)
    print("CENSUS DATA VALIDATION")
    print("=" * 80)

    results = []

    validators = [
        validate_census_2000,
        validate_census_2005,
        validate_census_2010,
        validate_census_2020
    ]

    for validator in validators:
        try:
            result = validator()
            results.append(result)

            if result['status'] == 'OK':
                print(f"  ✓ {result['year']}: {format_number(result['totals']['total'])} total population")
                if result.get('alcaldias_missing'):
                    print(f"    ⚠️ Missing alcaldías: {result['alcaldias_missing']}")
                if result.get('notes'):
                    for note in result['notes']:
                        print(f"    ℹ️ {note}")
            else:
                print(f"  ✗ {result['year']}: {result.get('error', 'Unknown error')}")

        except Exception as e:
            results.append({
                'year': validator.__name__.replace('validate_census_', ''),
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"  ✗ Error validating census: {e}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = LOGS_DIR / f'census_validation_{timestamp}.json'
    save_json(results, output_path)
    print(f"\n  ✓ Results saved to: {output_path}")

    return results


# =============================================================================
# MORTALITY VALIDATION FUNCTIONS
# =============================================================================

def validate_mortality_data():
    """
    Validate mortality data across all available years (2000-2023).

    This function checks:
    - File availability for each year
    - Column name consistency across years
    - Lung cancer death counts by year
    - Geographic coverage of CDMX alcaldías

    Returns:
    --------
    list
        List of validation result dictionaries by year
    """
    print("\n" + "=" * 80)
    print("MORTALITY DATA VALIDATION")
    print("=" * 80)

    results = []
    total_lung_cancer = 0
    years_with_data = 0
    column_variations = {}

    for year in range(2000, 2024):
        filepath = get_mortality_file_path(year)

        if not filepath.exists():
            results.append({
                'year': year,
                'status': 'MISSING',
                'error': f'File not found: {filepath}'
            })
            print(f"  ⚠️ {year}: File not found")
            continue

        try:
            df = pd.read_csv(filepath, low_memory=False)

            # Detect column names (handle case variations across years)
            ent_col = next((c for c in df.columns if c.upper() == 'ENT_RESID'), None)
            mun_col = next((c for c in df.columns if c.upper() == 'MUN_RESID'), None)
            causa_col = next((c for c in df.columns if c.upper() == 'CAUSA_DEF'), None)
            sexo_col = next((c for c in df.columns if c.upper() == 'SEXO'), None)
            edad_col = next((c for c in df.columns if c.upper() == 'EDAD'), None)

            # Track column variations for metadata
            column_variations[year] = {
                'ent': ent_col, 'mun': mun_col, 'causa': causa_col,
                'sexo': sexo_col, 'edad': edad_col
            }

            if not all([ent_col, mun_col, causa_col, sexo_col, edad_col]):
                missing = []
                if not ent_col: missing.append('ENT_RESID')
                if not mun_col: missing.append('MUN_RESID')
                if not causa_col: missing.append('CAUSA_DEF')
                if not sexo_col: missing.append('SEXO')
                if not edad_col: missing.append('EDAD')

                results.append({
                    'year': year,
                    'status': 'ERROR',
                    'error': f'Missing columns: {missing}'
                })
                print(f"  ✗ {year}: Missing columns: {missing}")
                continue

            # Convert to numeric
            df[ent_col] = pd.to_numeric(df[ent_col], errors='coerce')
            df[mun_col] = pd.to_numeric(df[mun_col], errors='coerce')

            # Filter to CDMX alcaldías
            df_cdmx = df[
                (df[ent_col] == CDMX_ENTIDAD_INT) &
                (df[mun_col].isin([int(k) for k in ALCALDIA_CODES.keys()]))
            ].copy()

            # Filter to lung cancer deaths
            df_cdmx[causa_col] = df_cdmx[causa_col].astype(str)
            lung_cancer = df_cdmx[df_cdmx[causa_col].str.startswith(tuple(LUNG_CANCER_CODES))]

            # Count by alcaldía
            alcaldia_counts = lung_cancer[mun_col].value_counts().to_dict()

            results.append({
                'year': year,
                'status': 'OK',
                'total_deaths_cdmx': len(df_cdmx),
                'lung_cancer_deaths': len(lung_cancer),
                'alcaldias_with_deaths': len(alcaldia_counts),
                'alcaldia_breakdown': {str(k): v for k, v in alcaldia_counts.items()}
            })

            total_lung_cancer += len(lung_cancer)
            years_with_data += 1

            print(f"  ✓ {year}: {len(lung_cancer):,} lung cancer deaths "
                  f"({len(alcaldia_counts)} alcaldías)")

        except Exception as e:
            results.append({
                'year': year,
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"  ✗ {year}: Error - {e}")

    # Summary statistics
    print(f"\n  Summary:")
    print(f"    Years with data: {years_with_data}/24")
    print(f"    Total lung cancer deaths (2000-2023): {total_lung_cancer:,}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = LOGS_DIR / f'mortality_validation_{timestamp}.json'
    save_json({
        'summary': {
            'years_with_data': years_with_data,
            'total_lung_cancer_deaths': total_lung_cancer
        },
        'yearly_results': results,
        'column_variations': column_variations
    }, output_path)
    print(f"  ✓ Results saved to: {output_path}")

    return results


# =============================================================================
# POLLUTION VALIDATION FUNCTIONS
# =============================================================================

def validate_pollution_data():
    """
    Validate Zenodo air pollution data (Jub et al.).

    This function checks:
    - File availability and structure
    - Year range coverage
    - Alcaldía name mapping success
    - Pollutant availability and value ranges

    Returns:
    --------
    dict
        Validation results for pollution data
    """
    print("\n" + "=" * 80)
    print("POLLUTION DATA VALIDATION")
    print("=" * 80)

    filepath = get_pollution_file_path()

    if not filepath.exists():
        print(f"  ✗ File not found: {filepath}")
        return {
            'status': 'ERROR',
            'error': f'File not found: {filepath}'
        }

    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.lower().str.strip()

        # Find alcaldía column
        alcaldia_col = None
        for col in df.columns:
            if 'alcald' in col or 'municip' in col or 'delegac' in col:
                alcaldia_col = col
                break

        # Map alcaldía names
        if alcaldia_col:
            df['alcaldia_mapped'] = df[alcaldia_col].apply(
                lambda x: next((a for a in ALCALDIA_CODES.values()
                               if normalize_string(str(x)) == normalize_string(a)), None)
            )
            mapped_count = df['alcaldia_mapped'].notna().sum()
            unique_mapped = df['alcaldia_mapped'].dropna().nunique()

            # Identify unmapped names
            unmapped = df[df['alcaldia_mapped'].isna()][alcaldia_col].unique().tolist()
        else:
            mapped_count = 0
            unique_mapped = 0
            unmapped = []

        # Check pollutant availability
        pollutants_found = [p for p in POLLUTANTS if p in df.columns]
        pollutants_missing = [p for p in POLLUTANTS if p not in df.columns]

        # Check value ranges for each pollutant
        pollutant_stats = {}
        for pol in pollutants_found:
            valid_data = df[pol].dropna()
            if len(valid_data) > 0:
                pollutant_stats[pol] = {
                    'count': len(valid_data),
                    'min': float(valid_data.min()),
                    'max': float(valid_data.max()),
                    'mean': float(valid_data.mean()),
                    'negative_values': int((valid_data < 0).sum())
                }

        # Year range
        year_min = int(df['year'].min()) if 'year' in df.columns else None
        year_max = int(df['year'].max()) if 'year' in df.columns else None

        results = {
            'status': 'OK',
            'file': filepath.name,
            'total_records': len(df),
            'years': f"{year_min} - {year_max}" if year_min else 'N/A',
            'alcaldias_mapped': unique_mapped,
            'alcaldias_expected': 16,
            'mapping_success_rate': mapped_count / len(df) if len(df) > 0 else 0,
            'unmapped_names': unmapped[:10],  # Limit to first 10
            'pollutants_found': pollutants_found,
            'pollutants_missing': pollutants_missing,
            'pollutant_statistics': pollutant_stats
        }

        print(f"  Records: {results['total_records']}")
        print(f"  Years: {results['years']}")
        print(f"  Alcaldías mapped: {results['alcaldias_mapped']}/16 "
              f"({results['mapping_success_rate']*100:.1f}% success)")
        print(f"  Pollutants found: {results['pollutants_found']}")

        if unmapped:
            print(f"  ⚠️ Unmapped alcaldía names: {unmapped[:5]}...")

        for pol, stats in pollutant_stats.items():
            if stats['negative_values'] > 0:
                print(f"  ⚠️ {pol}: {stats['negative_values']} negative values detected")

    except Exception as e:
        results = {
            'status': 'ERROR',
            'error': str(e)
        }
        print(f"  ✗ Error: {e}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = LOGS_DIR / f'pollution_validation_{timestamp}.json'
    save_json(results, output_path)
    print(f"  ✓ Results saved to: {output_path}")

    return results


# =============================================================================
# MAIN VALIDATION PIPELINE
# =============================================================================

def run_all_validations():
    """
    Run all data validations and generate comprehensive report.

    Returns:
    --------
    dict
        Combined validation results for all data sources
    """
    print("=" * 80)
    print("DATA VALIDATION PIPELINE")
    print("Project 1: Air Pollution and Cancer Mortality in CDMX")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Ensure directories exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Run validations
    census_results = validate_all_censuses()
    mortality_results = validate_mortality_data()
    pollution_results = validate_pollution_data()

    # Compile summary
    census_ok = sum(1 for r in census_results if r.get('status') == 'OK')
    mortality_ok = sum(1 for r in mortality_results if r.get('status') == 'OK')

    summary = {
        'timestamp': datetime.now().isoformat(),
        'census': {
            'total': len(census_results),
            'passed': census_ok,
            'failed': len(census_results) - census_ok
        },
        'mortality': {
            'total': len(mortality_results),
            'passed': mortality_ok,
            'failed': len(mortality_results) - mortality_ok
        },
        'pollution': {
            'status': pollution_results.get('status', 'UNKNOWN')
        }
    }

    # Save summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = LOGS_DIR / f'validation_summary_{timestamp}.json'
    save_json({
        'summary': summary,
        'census_results': census_results,
        'mortality_results': mortality_results,
        'pollution_results': pollution_results
    }, summary_path)

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\n  Summary:")
    print(f"    Census files: {census_ok}/{len(census_results)} passed")
    print(f"    Mortality files: {mortality_ok}/{len(mortality_results)} passed")
    print(f"    Pollution file: {pollution_results.get('status', 'UNKNOWN')}")
    print(f"\n  Full report saved to: {summary_path}")

    return {
        'census': census_results,
        'mortality': mortality_results,
        'pollution': pollution_results,
        'summary': summary
    }


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("DATA VALIDATION - STANDALONE EXECUTION")
    print("=" * 70)

    try:
        results = run_all_validations()

        # Exit with appropriate code
        if results['summary']['census']['failed'] > 0:
            print("\n⚠️ Warning: Some census validations failed")
        if results['summary']['mortality']['failed'] > 0:
            print("\n⚠️ Warning: Some mortality validations failed")
        if results['summary']['pollution']['status'] != 'OK':
            print("\n⚠️ Warning: Pollution validation failed")

        print("\n✓ Validation completed!")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
