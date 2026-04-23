#!/usr/bin/env python3
"""
Master Analysis Script - Project 1
Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

This script orchestrates the complete analysis pipeline:

Phase 1: Data Validation
  - 1a: Validate census data (2000, 2005, 2010, 2020)
  - 1b: Validate mortality data (2000-2023)
  - 1c: Validate Zenodo Jub air pollution data (1986-2022)

Phase 2: Population Data Harmonization
  - Process census files to create harmonized population estimates
  - Output: cdmx_population_harmonized_2000_2022.csv

Phase 3: Mortality Data Processing
  - Process Zenodo mortality files to extract lung cancer deaths
  - Output: cdmx_lung_cancer_deaths_2000_2022.csv

Phase 4: Integration and Age Standardization
  - Merge population and mortality data
  - Calculate crude and age-standardized mortality rates
  - Merge with air pollution data
  - Output: cdmx_analysis_dataset_2004_2022.csv

Phase 5: Statistical Analysis and Visualization
  - Panel regression with cluster-robust standard errors
  - Create correlation plots and temporal trend visualizations
  - Output: figures/, tables/, models/

Phase 6: Geospatial Visualizations
  - Create choropleth maps of mortality rates
  - Create pollution distribution maps
  - Create bivariate PM2.5/mortality maps
  - Output: interactive HTML and static PNG maps

Author: Arlex Marín
Date: April 2026
Version: 3.3 - Fixed import conflicts and shapefile paths
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src import ensure_directories, LOGS_DIR
from src.utils import setup_logging


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"PHASE: {title}")
    print("=" * 80)


def print_step(step_name):
    """Print a step header."""
    print("\n" + "-" * 60)
    print(f"STEP: {step_name}")
    print("-" * 60)


def verify_output_files(expected_files):
    """Verify that expected output files were created."""
    print("\n" + "-" * 60)
    print("VERIFYING OUTPUT FILES")
    print("-" * 60)

    all_present = True
    file_sizes = {}

    for filepath in expected_files:
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"  ✓ {filepath.name} ({size_mb:.2f} MB)")
            file_sizes[str(filepath)] = size_mb
        else:
            print(f"  ✗ {filepath.name} not found")
            all_present = False

    return all_present, file_sizes


def verify_analysis_outputs():
    """Verify that Phase 5 analysis outputs were created."""
    print("\n" + "-" * 60)
    print("VERIFYING ANALYSIS OUTPUTS")
    print("-" * 60)

    from src import FIGURES_DIR, TABLES_DIR, MODELS_DIR

    output_summary = {
        'figures': [],
        'tables': [],
        'models': []
    }

    if FIGURES_DIR.exists():
        figures = list(FIGURES_DIR.glob('*.png'))
        output_summary['figures'] = [f.name for f in figures]
        print(f"\n  Figures ({len(figures)}):")
        for f in sorted(figures):
            print(f"    - {f.name}")

    if TABLES_DIR.exists():
        tables = list(TABLES_DIR.glob('*.csv'))
        output_summary['tables'] = [t.name for t in tables]
        print(f"\n  Tables ({len(tables)}):")
        for t in sorted(tables):
            print(f"    - {t.name}")

    if MODELS_DIR.exists():
        models = list(MODELS_DIR.glob('*.txt'))
        output_summary['models'] = [m.name for m in models]
        print(f"\n  Models ({len(models)}):")
        for m in sorted(models):
            print(f"    - {m.name}")

    return output_summary


def verify_geospatial_outputs():
    """Verify that Phase 6 geospatial outputs were created."""
    print("\n" + "-" * 60)
    print("VERIFYING GEOSPATIAL OUTPUTS")
    print("-" * 60)

    from src import FIGURES_DIR

    geospatial_files = {
        'html': list(FIGURES_DIR.glob('*.html')),
        'png': list(FIGURES_DIR.glob('choropleth_*.png')),
        'bivariate': list(FIGURES_DIR.glob('bivariate_*.png'))
    }

    print(f"\n  Interactive HTML maps ({len(geospatial_files['html'])}):")
    for f in sorted(geospatial_files['html']):
        print(f"    - {f.name}")

    print(f"\n  Static PNG maps ({len(geospatial_files['png'])}):")
    for f in sorted(geospatial_files['png']):
        print(f"    - {f.name}")

    print(f"\n  Bivariate maps ({len(geospatial_files['bivariate'])}):")
    for f in sorted(geospatial_files['bivariate']):
        print(f"    - {f.name}")

    return geospatial_files


def print_execution_summary(results):
    """Print execution summary."""
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)

    all_passed = all(results.values())

    if all_passed:
        print("\n✓ All phases completed successfully!")
    else:
        print("\n⚠️ Some phases failed. Check the log for details.")

    print("\nPhase Results:")
    for phase, status in results.items():
        icon = "✓" if status else "✗"
        print(f"  {icon} {phase}")

    return all_passed


# =============================================================================
# PHASE FUNCTIONS
# =============================================================================

def phase1_validation():
    """Phase 1: Run all data validations."""
    print_header("PHASE 1: DATA VALIDATION")

    try:
        from src.data_validation import run_all_validations
        results = run_all_validations()
        return True
    except Exception as e:
        print(f"\n  ✗ Error in validation phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase2_harmonization():
    """Phase 2: Harmonize population data."""
    print_header("PHASE 2: POPULATION DATA HARMONIZATION")

    try:
        from src.harmonization import harmonize_population
        from src import POPULATION_PROCESSED_DIR

        df_pop = harmonize_population()

        expected_files = [
            POPULATION_PROCESSED_DIR / 'cdmx_population_harmonized_2000_2022.csv',
            POPULATION_PROCESSED_DIR / 'cdmx_population_harmonized_2000_2022_wide.csv',
            POPULATION_PROCESSED_DIR / 'cdmx_population_metadata.json'
        ]
        verify_output_files(expected_files)

        return True
    except Exception as e:
        print(f"\n  ✗ Error in harmonization phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase3_mortality():
    """Phase 3: Process mortality data."""
    print_header("PHASE 3: MORTALITY DATA PROCESSING")

    try:
        from src.mortality_processing import process_mortality_data
        from src import MORTALITY_PROCESSED_DIR

        df_mort = process_mortality_data()

        expected_files = [
            MORTALITY_PROCESSED_DIR / 'cdmx_lung_cancer_deaths_2000_2022.csv',
            MORTALITY_PROCESSED_DIR / 'cdmx_lung_cancer_deaths_2000_2022_wide.csv',
            MORTALITY_PROCESSED_DIR / 'cdmx_lung_cancer_metadata.json'
        ]
        verify_output_files(expected_files)

        return True
    except Exception as e:
        print(f"\n  ✗ Error in mortality phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase4_integration():
    """Phase 4: Integrate and standardize data."""
    print_header("PHASE 4: INTEGRATION AND AGE STANDARDIZATION")

    try:
        from src.integration import integrate_data
        from src import INTEGRATED_PROCESSED_DIR

        df_final = integrate_data()

        expected_files = [
            INTEGRATED_PROCESSED_DIR / 'cdmx_population_mortality_merged_2000_2022.csv',
            INTEGRATED_PROCESSED_DIR / 'cdmx_mortality_rates_2000_2022.csv',
            INTEGRATED_PROCESSED_DIR / 'cdmx_analysis_dataset_2004_2022.csv',
            INTEGRATED_PROCESSED_DIR / 'cdmx_analysis_dataset_wide.csv',
            INTEGRATED_PROCESSED_DIR / 'integration_metadata.json'
        ]
        verify_output_files(expected_files)

        return True
    except Exception as e:
        print(f"\n  ✗ Error in integration phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase5_analysis():
    """Phase 5: Statistical analysis and visualization."""
    print_header("PHASE 5: STATISTICAL ANALYSIS AND VISUALIZATION")

    try:
        from src.analysis import run_analysis, prepare_analysis_sample, sex_specific_analysis
        from src.visualization import create_all_visualizations

        # Run statistical analysis
        df_pm25, models_dict = run_analysis()

        # Extract models for visualization
        models = {
            'pooled_ols': models_dict['pooled_ols'],
            'alcaldia_fe': models_dict['alcaldia_fe'],
            'twoway_fe': models_dict['twoway_fe']
        }

        # Run sex-specific analysis
        sex_models_dict, _ = sex_specific_analysis(df_pm25)

        # Create all visualizations
        create_all_visualizations(df_pm25, models, sex_models_dict)

        verify_analysis_outputs()

        return True
    except Exception as e:
        print(f"\n  ✗ Error in analysis phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase6_geospatial():
    """Phase 6: Geospatial visualizations."""
    print_header("PHASE 6: GEOSPATIAL VISUALIZATIONS")

    try:
        from src.integration import load_analysis_data
        from src.geospatial import create_all_geospatial_visualizations
        from src import ALCALDIAS_WITH_POLLUTION, ALCALDIAS_WITHOUT_POLLUTION, GEOSPATIAL_AVAILABLE

        if not GEOSPATIAL_AVAILABLE:
            print("\n  ✗ Geospatial module not available. Install geopandas.")
            return False

        print(f"\n  Alcaldías with pollution data: {len(ALCALDIAS_WITH_POLLUTION)}")
        print(f"  Alcaldías excluded (no monitoring): {', '.join(ALCALDIAS_WITHOUT_POLLUTION)}")

        # Load analysis data
        df, _ = load_analysis_data()

        # Create all geospatial visualizations
        figures = create_all_geospatial_visualizations(df)

        print(f"\n  ✓ Created {len(figures)} geospatial visualizations")

        verify_geospatial_outputs()

        return True
    except Exception as e:
        print(f"\n  ✗ Error in geospatial phase: {e}")
        import traceback
        traceback.print_exc()
        return False


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run the complete analysis pipeline for Project 1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.run_analysis              # Run all phases
  python -m src.run_analysis --phase 6    # Run only Phase 6 (geospatial)
  python -m src.run_analysis --from-phase 4  # Run from Phase 4 onward
  python -m src.run_analysis --skip-validation  # Skip validation phases
  python -m src.run_analysis --phases 2,3,4   # Run specific phases
  python -m src.run_analysis --list-phases    # List all phases
        """
    )
    parser.add_argument(
        '--phase', '-p',
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help='Run only a specific phase (1-6)'
    )
    parser.add_argument(
        '--phases', '-P',
        type=str,
        help='Run specific phases (comma-separated, e.g., "2,3,4")'
    )
    parser.add_argument(
        '--from-phase', '-f',
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help='Run from specified phase onward'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip validation phase (Phase 1)'
    )
    parser.add_argument(
        '--list-phases',
        action='store_true',
        help='List all phases and exit'
    )
    args = parser.parse_args()

    # List phases and exit
    if args.list_phases:
        print("\nAnalysis Pipeline Phases:")
        print("-" * 40)
        print("Phase 1: Data Validation (Census, Mortality, Pollution)")
        print("Phase 2: Population Data Harmonization")
        print("Phase 3: Mortality Data Processing")
        print("Phase 4: Integration and Age Standardization")
        print("Phase 5: Statistical Analysis and Visualization")
        print("Phase 6: Geospatial Visualizations")
        return 0

    # Setup
    ensure_directories()
    log_file = setup_logging()

    # Print header
    print("=" * 80)
    print("MASTER ANALYSIS SCRIPT")
    print("Project 1: Air Pollution and Cancer Mortality in CDMX")
    print("=" * 80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Log File: {log_file}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.phase:
        print(f"\nRunning only Phase {args.phase}")
    if args.phases:
        phases_list = [int(p.strip()) for p in args.phases.split(',')]
        print(f"\nRunning phases: {phases_list}")
    if args.from_phase:
        print(f"\nRunning from Phase {args.from_phase} onward")
    if args.skip_validation:
        print("\nSkipping validation phase (Phase 1)")

    results = {}

    # Determine which phases to run
    if args.phase:
        run_phases = {args.phase}
    elif args.phases:
        run_phases = set(int(p.strip()) for p in args.phases.split(','))
    elif args.from_phase:
        run_phases = set(range(args.from_phase, 7))
    else:
        run_phases = {1, 2, 3, 4, 5, 6}

    # Phase 1: Validation
    if 1 in run_phases and not args.skip_validation:
        results['1_validation'] = phase1_validation()
    elif 1 in run_phases:
        print_header("PHASE 1: DATA VALIDATION (SKIPPED)")
        results['1_validation'] = True
    elif not args.skip_validation and 1 not in run_phases:
        results['1_validation'] = True

    # Phase 2: Population Harmonization
    if 2 in run_phases:
        results['2_harmonization'] = phase2_harmonization()
    else:
        results['2_harmonization'] = True

    # Phase 3: Mortality Processing
    if 3 in run_phases:
        results['3_mortality'] = phase3_mortality()
    else:
        results['3_mortality'] = True

    # Phase 4: Integration
    if 4 in run_phases:
        results['4_integration'] = phase4_integration()
    else:
        results['4_integration'] = True

    # Phase 5: Analysis
    if 5 in run_phases:
        results['5_analysis'] = phase5_analysis()
    else:
        results['5_analysis'] = True

    # Phase 6: Geospatial
    if 6 in run_phases:
        results['6_geospatial'] = phase6_geospatial()
    else:
        results['6_geospatial'] = True

    # Print summary
    all_passed = print_execution_summary(results)

    # Show output file locations
    print("\n" + "-" * 60)
    print("OUTPUT FILES LOCATION")
    print("-" * 60)
    from src import (
        CENSUS_RAW_DIR, MORTALITY_RAW_DIR, POLLUTION_RAW_DIR,
        POPULATION_PROCESSED_DIR, MORTALITY_PROCESSED_DIR, INTEGRATED_PROCESSED_DIR,
        FIGURES_DIR, TABLES_DIR, MODELS_DIR, LOGS_DIR
    )

    print(f"\n  Raw data:")
    print(f"    Census:    {CENSUS_RAW_DIR}")
    print(f"    Mortality: {MORTALITY_RAW_DIR}")
    print(f"    Pollution: {POLLUTION_RAW_DIR}")
    print(f"\n  Processed data:")
    print(f"    Population: {POPULATION_PROCESSED_DIR}")
    print(f"    Mortality:  {MORTALITY_PROCESSED_DIR}")
    print(f"    Integrated: {INTEGRATED_PROCESSED_DIR}")
    print(f"\n  Outputs:")
    print(f"    Figures:    {FIGURES_DIR}")
    print(f"    Tables:     {TABLES_DIR}")
    print(f"    Models:     {MODELS_DIR}")
    print(f"\n  Logs:        {LOGS_DIR}")

    # Show next steps if successful
    if all_passed:
        print("\n" + "-" * 60)
        print("NEXT STEPS")
        print("-" * 60)
        print("\n  Analysis complete! Review the results:")
        print(f"    - Interactive maps: {FIGURES_DIR}/*.html")
        print(f"    - Static figures:   {FIGURES_DIR}/*.png")
        print(f"    - Tables:           {TABLES_DIR}/*.csv")
        print(f"    - Models:           {MODELS_DIR}/*.txt")

    # Log completion
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Script completed: {datetime.now().isoformat()}\n")
        f.write(f"Exit status: {'SUCCESS' if all_passed else 'PARTIAL/FAILURE'}\n")
        f.write("=" * 80 + "\n")

    print(f"\nLog file: {log_file}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
