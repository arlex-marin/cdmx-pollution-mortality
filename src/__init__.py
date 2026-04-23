"""
Source code modules for Project 1:
Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

This package contains modular functions for:
- data_validation: Validate census, mortality, and pollution datasets
- harmonization: Harmonize population data across censuses
- mortality_processing: Process lung cancer mortality data
- integration: Integrate and age-standardize datasets
- analysis: Statistical analysis and panel regression
- visualization: Create publication-quality figures
- geospatial: Create choropleth maps and geospatial visualizations
- utils: Utility functions for logging, file I/O, and data handling

Author: Arlex Marín
Date: April 2026
"""

__version__ = "1.0.0"
__author__ = "Arlex Marín"

import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
EXTERNAL_DATA_DIR = DATA_DIR / 'external'
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
LOGS_DIR = PROJECT_ROOT / 'logs'
DOCS_DIR = PROJECT_ROOT / 'docs'
TESTS_DIR = PROJECT_ROOT / 'tests'
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

# Specific data directories
CENSUS_RAW_DIR = RAW_DATA_DIR / 'census'
MORTALITY_RAW_DIR = RAW_DATA_DIR / 'mortality'
POLLUTION_RAW_DIR = RAW_DATA_DIR / 'pollution'
POPULATION_PROCESSED_DIR = PROCESSED_DATA_DIR / 'population'
MORTALITY_PROCESSED_DIR = PROCESSED_DATA_DIR / 'mortality'
INTEGRATED_PROCESSED_DIR = PROCESSED_DATA_DIR / 'integrated'
SHAPEFILE_DIR = EXTERNAL_DATA_DIR / 'shapefiles'
DICTIONARIES_DIR = EXTERNAL_DATA_DIR / 'dictionaries'

# Output subdirectories
FIGURES_DIR = OUTPUTS_DIR / 'figures'
TABLES_DIR = OUTPUTS_DIR / 'tables'
MODELS_DIR = OUTPUTS_DIR / 'models'


def ensure_directories():
    """Create all required directories if they don't exist."""
    directories = [
        LOGS_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        MODELS_DIR,
        POPULATION_PROCESSED_DIR,
        MORTALITY_PROCESSED_DIR,
        INTEGRATED_PROCESSED_DIR,
        SHAPEFILE_DIR,
        DICTIONARIES_DIR,
        TESTS_DIR,
        NOTEBOOKS_DIR,
    ]
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)

    return True


# Import all public functions for easier access
from .utils import (
    safe_int, normalize_string, format_number, format_percent, format_pvalue,
    read_csv_flexible, setup_logging, save_json, load_json, clamp_proportion,
    get_census_file_path, get_mortality_file_path, get_pollution_file_path,
    get_population_processed_path, get_mortality_processed_path,
    get_integrated_dataset_path, get_shapefile_path,
    ALCALDIA_CODES, ALCALDIA_NAME_TO_CODE, CDMX_ENTIDAD, CDMX_ENTIDAD_INT,
    HARMONIZED_AGE_GROUPS, WHO_WEIGHTS, LUNG_CANCER_CODES, POLLUTANTS,
    ALCALDIAS_WITH_POLLUTION, ALCALDIAS_WITHOUT_POLLUTION, CENSUS_YEARS,
    ANALYSIS_YEARS
)

from .data_validation import (
    validate_all_censuses, validate_mortality_data, validate_pollution_data,
    run_all_validations
)

from .harmonization import (
    harmonize_population
)

from .mortality_processing import (
    process_mortality_data
)

from .integration import (
    integrate_data, load_population_data, load_mortality_data,
    load_pollution_data, load_analysis_data, ANALYSIS_YEARS as INTEGRATION_ANALYSIS_YEARS
)

from .analysis import (
    descriptive_statistics, correlation_analysis, panel_regression,
    sex_specific_analysis, run_analysis, prepare_analysis_sample
)

from .visualization import (
    plot_temporal_trends, plot_correlation_scatter, plot_alcaldia_boxplot,
    plot_pm25_by_alcaldia, plot_regression_coefficients, plot_sex_specific_effects,
    plot_correlation_heatmap, create_all_visualizations, save_figure
)

# Try to import geospatial (may fail if geopandas not installed)
try:
    from .geospatial import (
        load_cdmx_shapefile, prepare_alcaldia_shapefile, create_choropleth_map,
        create_pollution_choropleth, create_bivariate_choropleth,
        create_all_geospatial_visualizations
    )
    GEOSPATIAL_AVAILABLE = True
except ImportError as e:
    GEOSPATIAL_AVAILABLE = False
    logger.warning(f"Geospatial module not available: {e}")


# Package metadata
__all__ = [
    # Version
    '__version__', '__author__',

    # Paths
    'PROJECT_ROOT', 'DATA_DIR', 'RAW_DATA_DIR', 'PROCESSED_DATA_DIR',
    'EXTERNAL_DATA_DIR', 'OUTPUTS_DIR', 'LOGS_DIR', 'DOCS_DIR',
    'CENSUS_RAW_DIR', 'MORTALITY_RAW_DIR', 'POLLUTION_RAW_DIR',
    'POPULATION_PROCESSED_DIR', 'MORTALITY_PROCESSED_DIR',
    'INTEGRATED_PROCESSED_DIR', 'SHAPEFILE_DIR', 'DICTIONARIES_DIR',
    'FIGURES_DIR', 'TABLES_DIR', 'MODELS_DIR',

    # Functions
    'ensure_directories',

    # Constants
    'ALCALDIA_CODES', 'ALCALDIA_NAME_TO_CODE', 'CDMX_ENTIDAD', 'CDMX_ENTIDAD_INT',
    'HARMONIZED_AGE_GROUPS', 'WHO_WEIGHTS', 'LUNG_CANCER_CODES', 'POLLUTANTS',
    'ALCALDIAS_WITH_POLLUTION', 'ALCALDIAS_WITHOUT_POLLUTION', 'CENSUS_YEARS',
    'ANALYSIS_YEARS', 'GEOSPATIAL_AVAILABLE',

    # Analysis functions
    'prepare_analysis_sample',
]
