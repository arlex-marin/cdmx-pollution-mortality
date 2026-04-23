"""
Integration and age standardization functions.

This module integrates harmonized population data with processed mortality data
and calculates age-standardized mortality rates using WHO standard population weights.
It then merges the results with air pollution monitoring data to create the final
analytical dataset.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Added warning logging for unmapped alcaldías,
                         documented analysis year range rationale,
                         improved error handling and validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

from .utils import (
    safe_int, save_json, format_number, format_percent,
    ALCALDIA_CODES, ALCALDIA_NAME_TO_CODE, WHO_WEIGHTS, HARMONIZED_AGE_GROUPS,
    POLLUTANTS, ALCALDIAS_WITH_POLLUTION, ALCALDIAS_WITHOUT_POLLUTION,
    normalize_string, get_population_processed_path, get_mortality_processed_path,
    get_pollution_file_path, get_integrated_dataset_path
)
from . import INTEGRATED_PROCESSED_DIR, LOGS_DIR, ensure_directories

# =============================================================================
# ANALYSIS YEAR RANGE
# =============================================================================
# Analysis limited to 2004-2022 because:
# 1. 2023 mortality data is available but not yet fully validated
#    (the validation report shows some inconsistencies in 2023 coding)
# 2. Air pollution data from Zenodo (Jub et al.) ends in 2022
# 3. 2004 is the first year with complete pollution monitoring coverage
#    across all alcaldías with monitoring stations
# =============================================================================
ANALYSIS_YEARS = (2004, 2022)


# Track unmapped alcaldía names to avoid duplicate warnings
_UNMAPPED_ALCALDIA_CACHE = set()


def map_alcaldia_name(name):
    """
    Map pollution alcaldía name to standard name.

    This function handles common variations in alcaldía names found in the
    pollution dataset, including accent variations, abbreviations, and
    alternative spellings. It logs a warning if a name cannot be mapped.

    Parameters:
    -----------
    name : str or None
        Alcaldía name from pollution dataset

    Returns:
    --------
    str or None
        Standardized alcaldía name, or None if mapping fails

    Examples:
    ---------
    >>> map_alcaldia_name("Álvaro Obregón")
    'Alvaro Obregon'
    >>> map_alcaldia_name("benito juarez")
    'Benito Juarez'
    >>> map_alcaldia_name("Unknown Place")
    None  # With warning logged
    """
    if pd.isna(name):
        return None

    name_norm = normalize_string(name)

    # Direct match against standard names (fastest path)
    for std_name in ALCALDIA_CODES.values():
        if normalize_string(std_name) == name_norm:
            return std_name

    # Common variations mapping (curated from actual data)
    name_mappings = {
        # Accent variations
        'alvaro obregon': 'Alvaro Obregon',
        'alvaro obregón': 'Alvaro Obregon',
        'álvaro obregón': 'Alvaro Obregon',
        'benito juarez': 'Benito Juarez',
        'benito juárez': 'Benito Juarez',
        'coyoacan': 'Coyoacan',
        'coyoacán': 'Coyoacan',
        'cuauhtemoc': 'Cuauhtemoc',
        'cuauhtémoc': 'Cuauhtemoc',
        'tlahuac': 'Tlahuac',
        'tláhuac': 'Tlahuac',

        # Common abbreviations and variations
        'cuajimalpa': 'Cuajimalpa de Morelos',
        'cuajimalpa de morelos': 'Cuajimalpa de Morelos',
        'gustavo a madero': 'Gustavo A. Madero',
        'gustavo a. madero': 'Gustavo A. Madero',
        'gustavo madero': 'Gustavo A. Madero',
        'iztacalco': 'Iztacalco',
        'iztapalapa': 'Iztapalapa',
        'la magdalena contreras': 'La Magdalena Contreras',
        'magdalena contreras': 'La Magdalena Contreras',
        'miguel hidalgo': 'Miguel Hidalgo',
        'milpa alta': 'Milpa Alta',
        'tlalpan': 'Tlalpan',
        'venustiano carranza': 'Venustiano Carranza',
        'xochimilco': 'Xochimilco',
        'azcapotzalco': 'Azcapotzalco',

        # Historical names (pre-2016 delegaciones)
        'alvaro obregon (delegacion)': 'Alvaro Obregon',
        'benito juarez (delegacion)': 'Benito Juarez',
        'coyoacan (delegacion)': 'Coyoacan',
        'cuauhtemoc (delegacion)': 'Cuauhtemoc',
        'iztapalapa (delegacion)': 'Iztapalapa',
    }

    if name_norm in name_mappings:
        return name_mappings[name_norm]

    # Partial match (substring) as fallback
    # This handles cases like "Iztapalapa Centro" or "Tlalpan Sur"
    for std_name in ALCALDIA_CODES.values():
        std_norm = normalize_string(std_name)
        if std_norm in name_norm or name_norm in std_norm:
            return std_name

    # Could not map - log warning (only once per unique name)
    if name_norm not in _UNMAPPED_ALCALDIA_CACHE:
        _UNMAPPED_ALCALDIA_CACHE.add(name_norm)
        warnings.warn(
            f"Could not map alcaldía name: '{name}' (normalized: '{name_norm}'). "
            "This alcaldía will be excluded from the pollution merge.",
            UserWarning
        )
    return None


def load_population_data():
    """
    Load harmonized population data.

    Returns:
    --------
    pd.DataFrame
        Harmonized population data with columns:
        alcaldia, alcaldia_code, year, age_group, sex, population

    Raises:
    -------
    FileNotFoundError
        If population data file does not exist
    """
    filepath = get_population_processed_path()
    if not filepath.exists():
        raise FileNotFoundError(
            f"Population data not found: {filepath}\n"
            "Please run the harmonization phase first: python -m src.run_analysis --phase 2"
        )

    df = pd.read_csv(filepath)
    print(f"  Population: {len(df):,} records, {df['year'].min()}-{df['year'].max()}")
    return df


def load_mortality_data():
    """
    Load processed mortality data.

    Returns:
    --------
    pd.DataFrame
        Processed mortality data with columns:
        alcaldia, alcaldia_code, year, age_group, sex, deaths

    Raises:
    -------
    FileNotFoundError
        If mortality data file does not exist
    """
    filepath = get_mortality_processed_path()
    if not filepath.exists():
        raise FileNotFoundError(
            f"Mortality data not found: {filepath}\n"
            "Please run the mortality processing phase first: python -m src.run_analysis --phase 3"
        )

    df = pd.read_csv(filepath)
    total_deaths = df['deaths'].sum()
    print(f"  Mortality: {len(df):,} records, {total_deaths:,} total lung cancer deaths")
    return df


def load_pollution_data():
    """
    Load air pollution data from Zenodo.

    The pollution dataset contains annual average concentrations for
    PM2.5, PM10, O3, NO2, SO2, and CO by alcaldía from 1986-2022.

    Returns:
    --------
    pd.DataFrame
        Air pollution data with standardized alcaldía names

    Raises:
    -------
    FileNotFoundError
        If pollution data file does not exist
    """
    filepath = get_pollution_file_path()
    if not filepath.exists():
        raise FileNotFoundError(
            f"Pollution data not found: {filepath}\n"
            "Please ensure the Zenodo dataset is downloaded to data/raw/pollution/"
        )

    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower().str.strip()

    # Identify alcaldía column (may be named differently)
    alcaldia_col = None
    for col in df.columns:
        if 'alcald' in col or 'municip' in col or 'delegac' in col:
            alcaldia_col = col
            break

    if alcaldia_col:
        df['alcaldia'] = df[alcaldia_col].apply(map_alcaldia_name)
    else:
        warnings.warn("Could not identify alcaldía column in pollution data")
        df['alcaldia'] = None

    # Report mapping success
    mapped_count = df['alcaldia'].notna().sum()
    unique_mapped = df['alcaldia'].dropna().nunique()
    years_range = f"{df['year'].min()}-{df['year'].max()}" if 'year' in df.columns else 'unknown'

    print(f"  Pollution: {len(df):,} records, {years_range}")
    print(f"    Alcaldías mapped: {unique_mapped}/16 ({mapped_count} records)")

    # Check for missing alcaldías
    if unique_mapped < 16:
        mapped_set = set(df['alcaldia'].dropna().unique())
        missing = set(ALCALDIA_CODES.values()) - mapped_set
        print(f"    ⚠️ Alcaldías without pollution data: {sorted(missing)}")

    return df


def load_analysis_data():
    """
    Load the final analytical dataset.

    This is a convenience function for loading the integrated dataset
    that has already been created by `integrate_data()`.

    Returns:
    --------
    df : pd.DataFrame
        Complete analytical dataset
    df_pm25 : pd.DataFrame
        Dataset filtered to records with PM2.5 data

    Raises:
    -------
    FileNotFoundError
        If analysis data file does not exist
    """
    filepath = get_integrated_dataset_path()
    if not filepath.exists():
        raise FileNotFoundError(
            f"Analysis data not found: {filepath}\n"
            "Please run the integration phase first: python -m src.run_analysis --phase 4"
        )

    df = pd.read_csv(filepath)

    # Filter to records with PM2.5 data
    df_pm25 = df.dropna(subset=['pm25']).copy()

    # Add alcaldía code for fixed effects
    df['alcaldia_code'] = df['alcaldia'].map(ALCALDIA_NAME_TO_CODE).astype(int)
    df_pm25['alcaldia_code'] = df_pm25['alcaldia'].map(ALCALDIA_NAME_TO_CODE).astype(int)

    print(f"  Loaded analysis data: {len(df)} records")
    print(f"  Records with PM2.5: {len(df_pm25)}")

    return df, df_pm25


def merge_population_mortality(df_pop, df_mort):
    """
    Merge population and mortality data.

    This creates a complete person-years dataset with population counts
    and death counts for each alcaldía-year-age-sex combination.

    Parameters:
    -----------
    df_pop : pd.DataFrame
        Harmonized population data
    df_mort : pd.DataFrame
        Processed mortality data

    Returns:
    --------
    pd.DataFrame
        Merged dataset with population and death counts
    """
    merge_cols = ['alcaldia', 'year', 'age_group', 'sex']

    # Validate that all expected columns exist
    for col in merge_cols:
        if col not in df_pop.columns:
            raise ValueError(f"Population data missing column: {col}")
        if col not in df_mort.columns:
            raise ValueError(f"Mortality data missing column: {col}")

    df_merged = df_pop.merge(
        df_mort[merge_cols + ['deaths']],
        on=merge_cols,
        how='left'
    )

    # Fill missing deaths with 0 (no lung cancer deaths in that category)
    df_merged['deaths'] = df_merged['deaths'].fillna(0).astype(int)

    # Add alcaldía code for fixed effects
    df_merged['alcaldia_code'] = df_merged['alcaldia'].map(ALCALDIA_NAME_TO_CODE)

    # Validation checks
    total_pop = df_merged['population'].sum()
    total_deaths = df_merged['deaths'].sum()
    years_covered = f"{df_merged['year'].min()}-{df_merged['year'].max()}"

    print(f"  Merged: {len(df_merged):,} records, {years_covered}")
    print(f"    Total person-years: {format_number(total_pop)}")
    print(f"    Total lung cancer deaths: {format_number(total_deaths)}")

    return df_merged


def calculate_crude_rates(df):
    """
    Calculate crude mortality rates per 100,000 population.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with population and death counts

    Returns:
    --------
    pd.DataFrame
        Dataset with added 'crude_rate' column
    """
    df = df.copy()
    df['crude_rate'] = np.where(
        df['population'] > 0,
        (df['deaths'] / df['population']) * 100000,
        0
    )
    return df


def calculate_age_standardized_rates(df):
    """
    Calculate age-standardized mortality rates using WHO standard population.

    The WHO World Standard Population weights are used to enable valid
    comparisons across alcaldías with different age structures and over time.

    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age-specific population and death counts

    Returns:
    --------
    pd.DataFrame
        Dataset with age-standardized rates by alcaldía, year, and sex
    """
    print("\n  Calculating age-standardized rates...")

    df = df.copy()

    # Calculate age-specific rates (deaths per person)
    df['age_specific_rate'] = np.where(
        df['population'] > 0,
        df['deaths'] / df['population'],
        0
    )

    # Apply WHO standard weights
    df['who_weight'] = df['age_group'].map(WHO_WEIGHTS)

    # Check for missing weights
    missing_weights = df['who_weight'].isna().sum()
    if missing_weights > 0:
        warnings.warn(f"Missing WHO weights for {missing_weights} records")

    df['weighted_rate'] = df['age_specific_rate'] * df['who_weight']

    asr_list = []

    # Both sexes combined
    for (alcaldia, year), group in df.groupby(['alcaldia', 'year']):
        asr = group['weighted_rate'].sum() * 100000
        total_pop = group['population'].sum()
        total_deaths = group['deaths'].sum()
        crude_rate = (total_deaths / total_pop * 100000) if total_pop > 0 else 0

        asr_list.append({
            'alcaldia': alcaldia,
            'year': year,
            'sex': 'Both',
            'population': total_pop,
            'deaths': total_deaths,
            'crude_rate': crude_rate,
            'age_standardized_rate': asr
        })

    # Sex-specific
    for (alcaldia, year, sex), group in df.groupby(['alcaldia', 'year', 'sex']):
        asr = group['weighted_rate'].sum() * 100000
        total_pop = group['population'].sum()
        total_deaths = group['deaths'].sum()
        crude_rate = (total_deaths / total_pop * 100000) if total_pop > 0 else 0

        asr_list.append({
            'alcaldia': alcaldia,
            'year': year,
            'sex': sex,
            'population': total_pop,
            'deaths': total_deaths,
            'crude_rate': crude_rate,
            'age_standardized_rate': asr
        })

    df_asr = pd.DataFrame(asr_list)

    # Validation: check for negative or extreme rates
    if (df_asr['age_standardized_rate'] < 0).any():
        warnings.warn("Negative age-standardized rates detected")
        df_asr['age_standardized_rate'] = df_asr['age_standardized_rate'].clip(lower=0)

    print(f"    Standardized rates calculated for {len(df_asr)} alcaldía-year-sex combinations")

    return df_asr


def merge_with_pollution(df_asr, df_poll):
    """
    Merge standardized mortality rates with air pollution data.

    Parameters:
    -----------
    df_asr : pd.DataFrame
        Age-standardized mortality rates
    df_poll : pd.DataFrame
        Air pollution data with standardized alcaldía names

    Returns:
    --------
    pd.DataFrame
        Final analytical dataset with mortality rates and pollution data
    """
    print("\n  Merging with pollution data...")

    # Aggregate pollution data (in case of multiple measurements per year)
    poll_cols = ['alcaldia', 'year'] + [p for p in POLLUTANTS if p in df_poll.columns]
    poll_cols = [c for c in poll_cols if c in df_poll.columns]

    if 'year' not in df_poll.columns:
        raise ValueError("Pollution data missing 'year' column")

    df_poll_agg = df_poll[poll_cols].groupby(['alcaldia', 'year'], as_index=False).mean()

    # Merge
    df_final = df_asr.merge(df_poll_agg, on=['alcaldia', 'year'], how='left')

    # Filter to analysis years (2004-2022)
    df_final = df_final[
        (df_final['year'] >= ANALYSIS_YEARS[0]) &
        (df_final['year'] <= ANALYSIS_YEARS[1])
    ].copy()

    # Report merge results
    total_records = len(df_final)
    records_with_pollution = df_final['pm25'].notna().sum()
    alcaldias_with_data = df_final[df_final['pm25'].notna()]['alcaldia'].nunique()

    print(f"    Final dataset: {total_records} records")
    print(f"    Years: {df_final['year'].min()}-{df_final['year'].max()}")
    print(f"    Records with pollution data: {records_with_pollution}")
    print(f"    Alcaldías with pollution data: {alcaldias_with_data}/16")

    # Report excluded alcaldías
    alcaldias_in_final = set(df_final[df_final['pm25'].notna()]['alcaldia'].unique())
    excluded = set(ALCALDIA_CODES.values()) - alcaldias_in_final
    if excluded:
        print(f"    ⚠️ Excluded from analysis (no pollution data): {sorted(excluded)}")

    return df_final


def validate_integration_outputs(df_final):
    """
    Perform validation checks on the integrated dataset.

    Parameters:
    -----------
    df_final : pd.DataFrame
        Final analytical dataset

    Returns:
    --------
    dict
        Validation results
    """
    validation = {
        'total_records': len(df_final),
        'years_covered': f"{df_final['year'].min()}-{df_final['year'].max()}",
        'alcaldias_total': df_final['alcaldia'].nunique(),
        'alcaldias_with_pm25': df_final[df_final['pm25'].notna()]['alcaldia'].nunique(),
        'checks': {}
    }

    # Check for negative rates
    neg_crude = (df_final['crude_rate'] < 0).sum()
    neg_asr = (df_final['age_standardized_rate'] < 0).sum()
    validation['checks']['negative_crude_rates'] = neg_crude == 0
    validation['checks']['negative_asr'] = neg_asr == 0

    # Check for missing values in key columns
    validation['checks']['no_missing_alcaldia'] = df_final['alcaldia'].isna().sum() == 0
    validation['checks']['no_missing_year'] = df_final['year'].isna().sum() == 0
    validation['checks']['no_missing_population'] = df_final['population'].isna().sum() == 0

    # Check population consistency
    validation['checks']['population_positive'] = (df_final['population'] > 0).all()

    # Check pollution value ranges
    if 'pm25' in df_final.columns:
        pm25_valid = df_final['pm25'].dropna()
        if len(pm25_valid) > 0:
            validation['checks']['pm25_positive'] = (pm25_valid > 0).all()
            validation['checks']['pm25_max_reasonable'] = pm25_valid.max() < 100  # μg/m³

    # Report validation results
    all_passed = all(validation['checks'].values())
    if all_passed:
        print("\n  ✓ All validation checks passed")
    else:
        failed = [k for k, v in validation['checks'].items() if not v]
        warnings.warn(f"Validation checks failed: {failed}")

    return validation


def integrate_data():
    """
    Main integration pipeline.

    Executes the complete data integration workflow:
    1. Load harmonized population data
    2. Load processed mortality data
    3. Load air pollution data
    4. Merge population and mortality
    5. Calculate crude and age-standardized rates
    6. Merge with pollution data
    7. Save outputs in multiple formats
    8. Generate metadata

    Returns:
    --------
    pd.DataFrame
        Final analytical dataset
    """
    print("\n" + "=" * 70)
    print("DATA INTEGRATION AND AGE STANDARDIZATION")
    print("=" * 70)

    ensure_directories()

    # Phase 1: Load all data
    print("\nPhase 1: Loading data...")
    df_pop = load_population_data()
    df_mort = load_mortality_data()
    df_poll = load_pollution_data()

    # Phase 2: Merge population and mortality
    print("\nPhase 2: Merging population and mortality...")
    df_merged = merge_population_mortality(df_pop, df_mort)

    # Phase 3: Calculate rates
    print("\nPhase 3: Calculating mortality rates...")
    df_merged = calculate_crude_rates(df_merged)
    df_asr = calculate_age_standardized_rates(df_merged)

    # Phase 4: Integrate with pollution
    print("\nPhase 4: Integrating with pollution data...")
    df_final = merge_with_pollution(df_asr, df_poll)

    # Phase 5: Validation
    print("\nPhase 5: Validating outputs...")
    validation_results = validate_integration_outputs(df_final)

    # Phase 6: Save outputs
    print("\nPhase 6: Saving outputs...")

    # Save merged population-mortality dataset
    output_merged = INTEGRATED_PROCESSED_DIR / 'cdmx_population_mortality_merged_2000_2022.csv'
    df_merged.to_csv(output_merged, index=False)
    print(f"  ✓ Merged data: {output_merged.name} ({len(df_merged):,} records)")

    # Save mortality rates
    output_rates = INTEGRATED_PROCESSED_DIR / 'cdmx_mortality_rates_2000_2022.csv'
    df_asr.to_csv(output_rates, index=False)
    print(f"  ✓ Mortality rates: {output_rates.name} ({len(df_asr):,} records)")

    # Save final analytical dataset
    output_final = INTEGRATED_PROCESSED_DIR / 'cdmx_analysis_dataset_2004_2022.csv'
    df_final.to_csv(output_final, index=False)
    print(f"  ✓ Final dataset: {output_final.name} ({len(df_final):,} records)")

    # Save wide format for easier analysis
    df_wide = df_final.pivot_table(
        index=['alcaldia', 'year'],
        columns='sex',
        values=['population', 'deaths', 'crude_rate', 'age_standardized_rate'] + POLLUTANTS
    ).reset_index()
    df_wide.columns = ['_'.join(col).strip('_') for col in df_wide.columns.values]
    output_wide = INTEGRATED_PROCESSED_DIR / 'cdmx_analysis_dataset_wide.csv'
    df_wide.to_csv(output_wide, index=False)
    print(f"  ✓ Wide format: {output_wide.name}")

    # Phase 7: Generate metadata
    print("\nPhase 7: Generating metadata...")

    # Calculate summary statistics for metadata
    both_sex = df_final[df_final['sex'] == 'Both']
    pm25_records = both_sex.dropna(subset=['pm25'])

    metadata = {
        'title': 'Integrated Analysis Dataset for Mexico City',
        'description': 'Air pollution and lung cancer mortality data by alcaldía, 2004-2022',
        'date_created': datetime.now().isoformat(),
        'analysis_years': f"{df_final['year'].min()}-{df_final['year'].max()}",
        'total_records': len(df_final),
        'records_with_pm25': len(pm25_records),
        'alcaldias_included': ALCALDIAS_WITH_POLLUTION,
        'alcaldias_excluded': ALCALDIAS_WITHOUT_POLLUTION,
        'pollutants_available': [p for p in POLLUTANTS if p in df_final.columns],
        'age_groups': HARMONIZED_AGE_GROUPS,
        'who_weights': WHO_WEIGHTS,
        'validation_results': validation_results,
        'summary_statistics': {
            'mean_pm25_2020': float(pm25_records[pm25_records['year'] == 2020]['pm25'].mean()) if len(pm25_records[pm25_records['year'] == 2020]) > 0 else None,
            'mean_asr_2020': float(both_sex[both_sex['year'] == 2020]['age_standardized_rate'].mean()),
            'total_lung_cancer_deaths': int(df_final[df_final['sex'] == 'Both']['deaths'].sum()),
            'cdmx_population_2020': int(both_sex[both_sex['year'] == 2020]['population'].sum())
        },
        'unmapped_alcaldia_names': list(_UNMAPPED_ALCALDIA_CACHE) if _UNMAPPED_ALCALDIA_CACHE else []
    }

    metadata_path = INTEGRATED_PROCESSED_DIR / 'integration_metadata.json'
    save_json(metadata, metadata_path)
    print(f"  ✓ Metadata: {metadata_path.name}")

    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)
    print(f"\n  Final Dataset Summary:")
    print(f"    Analysis years: {df_final['year'].min()}-{df_final['year'].max()}")
    print(f"    Total records: {len(df_final):,}")
    print(f"    Alcaldías with pollution data: {len(ALCALDIAS_WITH_POLLUTION)}")
    print(f"    Alcaldías excluded: {len(ALCALDIAS_WITHOUT_POLLUTION)}")
    print(f"    Total lung cancer deaths (2004-2022): {int(df_final[df_final['sex']=='Both']['deaths'].sum()):,}")

    return df_final


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("DATA INTEGRATION - STANDALONE EXECUTION")
    print("=" * 70)

    try:
        df = integrate_data()
        print("\n✓ Integration completed successfully!")

        # Show sample of final dataset
        print("\nSample of final dataset:")
        print(df[df['sex'] == 'Both'].head(10).to_string(index=False))

        sys.exit(0)
    except FileNotFoundError as e:
        print(f"\n✗ File not found: {e}")
        print("\nPlease ensure all prerequisite data files exist.")
        print("Run the full pipeline: python -m src.run_analysis")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during integration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
