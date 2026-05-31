"""
Mortality data processing functions.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Fixed municipality code mapping for alcaldía names
"""

import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from . import LOGS_DIR, MORTALITY_PROCESSED_DIR, ensure_directories
from .utils import (ALCALDIA_CODES, ALCALDIA_NAME_TO_CODE, CDMX_ENTIDAD_INT,
                    HARMONIZED_AGE_GROUPS, LUNG_CANCER_CODES, format_number,
                    get_mortality_file_path, safe_int, save_json)

logger = logging.getLogger(__name__)


def map_edad_to_age_group(edad):
    """Map DGIS edad code to harmonized age group."""
    if pd.isna(edad):
        return None

    try:
        edad_int = int(float(edad))
    except (ValueError, TypeError):
        return None

    if edad_int < 4000:
        return "0-4"

    if 4001 <= edad_int <= 4120:
        years = edad_int - 4000

        if years <= 4:
            return "0-4"
        elif years <= 14:
            return "5-14"
        elif years <= 17:
            return "15-17"
        elif years <= 24:
            return "18-24"
        elif years <= 59:
            return "25-59"
        else:
            return "60+"

    return None


def map_sexo_to_sex(sexo):
    """Map DGIS sexo code to sex string."""
    try:
        sexo_int = int(float(sexo))
    except (ValueError, TypeError):
        return None

    if sexo_int == 1:
        return "Male"
    elif sexo_int == 2:
        return "Female"
    else:
        return None


def process_mortality_data() -> pd.DataFrame | None:
    """Process all mortality files and create harmonized dataset."""
    logger.info("" + "=" * 70)
    logger.info("MORTALITY DATA PROCESSING")
    logger.info("=" * 70)

    ensure_directories()

    all_deaths = []
    years_processed = []
    total_lung_cancer = 0
    column_mapping_by_year = {}

    for year in range(2000, 2023):
        filepath = get_mortality_file_path(year)
        if not filepath.exists():
            logger.warning(f"⚠️ File not found for {year}")
            continue

        logger.info(f"Processing {year}...")

        try:
            df = pd.read_csv(filepath, low_memory=False)

            # Detect column names (case variations)
            ent_col = next((c for c in df.columns if c.upper() == "ENT_RESID"), None)
            mun_col = next((c for c in df.columns if c.upper() == "MUN_RESID"), None)
            causa_col = next((c for c in df.columns if c.upper() == "CAUSA_DEF"), None)
            sexo_col = next((c for c in df.columns if c.upper() == "SEXO"), None)
            edad_col = next((c for c in df.columns if c.upper() == "EDAD"), None)

            if not all([ent_col, mun_col, causa_col, sexo_col, edad_col]):
                missing = []
                if not ent_col:
                    missing.append("ENT_RESID")
                if not mun_col:
                    missing.append("MUN_RESID")
                if not causa_col:
                    missing.append("CAUSA_DEF")
                if not sexo_col:
                    missing.append("SEXO")
                if not edad_col:
                    missing.append("EDAD")
                logger.error(f"✗ Missing columns: {missing}")
                continue

            column_mapping_by_year[year] = {
                "ent": ent_col,
                "mun": mun_col,
                "causa": causa_col,
                "sexo": sexo_col,
                "edad": edad_col,
            }

            # Convert to numeric for filtering
            df[ent_col] = pd.to_numeric(df[ent_col], errors="coerce")
            df[mun_col] = pd.to_numeric(df[mun_col], errors="coerce")

            # Convert alcaldia code keys to integers for comparison
            alcaldia_codes_int = [int(k) for k in ALCALDIA_CODES.keys()]

            # Filter to CDMX alcaldías
            df_cdmx = df[
                (df[ent_col] == CDMX_ENTIDAD_INT)
                & (df[mun_col].isin(alcaldia_codes_int))
            ].copy()

            if len(df_cdmx) == 0:
                logger.warning(f"⚠️ No CDMX alcaldía deaths")
                continue

            # Filter to lung cancer deaths
            df_cdmx[causa_col] = df_cdmx[causa_col].astype(str)
            df_cdmx["is_lung_cancer"] = df_cdmx[causa_col].str.startswith(
                tuple(LUNG_CANCER_CODES)
            )
            df_lung = df_cdmx[df_cdmx["is_lung_cancer"]].copy()

            if len(df_lung) == 0:
                logger.warning(f"⚠️ No lung cancer deaths")
                continue

            # Map age and sex
            df_lung["age_group"] = df_lung[edad_col].apply(map_edad_to_age_group)
            df_lung["sex"] = df_lung[sexo_col].apply(map_sexo_to_sex)

            # Convert municipality code to zero-padded string for mapping
            df_lung["mun_str"] = df_lung[mun_col].astype(int).astype(str).str.zfill(3)
            df_lung["alcaldia"] = df_lung["mun_str"].map(ALCALDIA_CODES)
            df_lung["alcaldia_code"] = df_lung["mun_str"]

            # Drop rows with missing values
            df_valid = df_lung.dropna(subset=["age_group", "sex", "alcaldia"])

            if len(df_valid) == 0:
                logger.warning(f"⚠️ No valid lung cancer deaths after mapping")
                continue

            # Aggregate deaths by alcaldía, age group, and sex
            agg_deaths = (
                df_valid.groupby(["alcaldia", "alcaldia_code", "age_group", "sex"])
                .size()
                .reset_index(name="deaths")
            )
            agg_deaths["year"] = year

            all_deaths.append(agg_deaths)
            years_processed.append(year)
            total_lung_cancer += len(df_valid)

            logger.info(f"Lung cancer deaths: {len(df_valid):,}")

        except Exception as e:
            logger.error(f"✗ Error: {e}")
            continue

    if not all_deaths:
        logger.info("ERROR: No data processed")
        return None

    # Combine all years
    df_all = pd.concat(all_deaths, ignore_index=True)

    # Create full dataset with zeros for missing combinations
    alcaldias = list(ALCALDIA_CODES.values())
    years = range(min(years_processed), max(years_processed) + 1)

    full_index = pd.MultiIndex.from_product(
        [alcaldias, years, HARMONIZED_AGE_GROUPS, ["Female", "Male"]],
        names=["alcaldia", "year", "age_group", "sex"],
    )

    df_full = pd.DataFrame(index=full_index).reset_index()
    df_full["alcaldia_code"] = df_full["alcaldia"].map(ALCALDIA_NAME_TO_CODE)

    # Merge with aggregated deaths
    df_final = df_full.merge(
        df_all, on=["alcaldia", "alcaldia_code", "year", "age_group", "sex"], how="left"
    )
    df_final["deaths"] = df_final["deaths"].fillna(0).astype(int)
    df_final = df_final.sort_values(
        ["alcaldia", "year", "age_group", "sex"]
    ).reset_index(drop=True)

    logger.info(f"Dataset Summary:")
    logger.info(f"Total records: {len(df_final):,}")
    logger.info(f"Years covered: {df_final['year'].min()} - {df_final['year'].max()}")
    logger.info(f"Total lung cancer deaths: {df_final['deaths'].sum():,}")

    # Save long format
    output_path = MORTALITY_PROCESSED_DIR / "cdmx_lung_cancer_deaths_2000_2022.csv"
    df_final.to_csv(output_path, index=False)
    logger.info(f"✓ Saved to: {output_path}")

    # Save wide format
    df_wide = df_final.pivot_table(
        index=["alcaldia", "alcaldia_code", "year"],
        columns=["age_group", "sex"],
        values="deaths",
        fill_value=0,
    ).reset_index()
    output_path_wide = (
        MORTALITY_PROCESSED_DIR / "cdmx_lung_cancer_deaths_2000_2022_wide.csv"
    )
    df_wide.to_csv(output_path_wide, index=False)
    logger.info(f"✓ Saved wide format to: {output_path_wide}")

    # Save metadata
    metadata = {
        "title": "Lung Cancer Mortality Data for Mexico City",
        "date_created": datetime.now().isoformat(),
        "years_covered": f"{df_final['year'].min()}-{df_final['year'].max()}",
        "total_lung_cancer_deaths": int(df_final["deaths"].sum()),
        "icd10_codes": LUNG_CANCER_CODES,
        "age_groups": HARMONIZED_AGE_GROUPS,
        "column_mapping": column_mapping_by_year,
    }

    metadata_path = MORTALITY_PROCESSED_DIR / "cdmx_lung_cancer_metadata.json"
    save_json(metadata, metadata_path)
    logger.info(f"✓ Metadata saved to: {metadata_path}")

    return df_final


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("MORTALITY PROCESSING - STANDALONE EXECUTION")
    print("=" * 70)

    try:
        df = process_mortality_data()
        print("\n✓ Mortality processing completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error during mortality processing: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
