# Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Quality Assessment](https://img.shields.io/badge/quality-A%20(94%2F100)-brightgreen.svg)](docs/quality_assessment.md)

**Author:** Arlex Marín
**Date:** April 2026
**Contact:** arlex.marin@gmail.com

---

## Overview

This project investigates the spatial and temporal relationship between long-term air pollutant exposure and lung cancer mortality across the 16 alcaldías (municipalities) of Mexico City from 2004-2022. The analysis integrates harmonized population estimates from four national censuses, individual-level mortality records, and air quality monitoring data from 35 stations.

### Research Questions

1. Is there a significant association between long-term PM₂.₅ exposure and lung cancer mortality across Mexico City alcaldías?
2. Which air pollutant shows the strongest correlation with lung cancer mortality?
3. Are there sex-specific differences in the pollution-mortality association?
4. How do mortality rates and pollution concentrations vary spatially across alcaldías?

---

## Key Findings

| Finding | Metric | Interpretation |
|:---|:---|:---|
| PM₂.₅ Associated with Mortality | β = +2.10 per 10 μg/m³ (p = 0.090) | Positive association after controlling for fixed effects |
| NO₂ Shows Strongest Correlation | r = +0.425 (p < 0.001) | Traffic-related pollution is key driver |
| Air Quality Improving | PM₂.₅ ↓16.5% since 2004-2008 | Policy effectiveness demonstrated |
| Mortality Declining | ASR ↓35.3% since 2004-2008 | Parallel health improvements |
| Spatial Inequity | 1.7× mortality ratio (high vs. low) | Environmental justice concern |
| WHO Guideline Exceeded | 3.9× above 5 μg/m³ | Continued action needed |

### Population Impact

A 10 μg/m³ reduction in PM₂.₅ could prevent approximately 193 lung cancer deaths annually in Mexico City. Achieving WHO guidelines (5 μg/m³) could prevent an estimated 280 deaths per year.

---

## Repository Structure

```
cdmx-pollution-mortality/
├── data/                         # Data directory (see documentation)
│   ├── raw/                      # Immutable source data
│   │   ├── census/               # INEGI census files (2000-2020)
│   │   ├── mortality/            # Zenodo mortality dataset (2000-2023)
│   │   └── pollution/            # Zenodo air quality dataset
│   ├── processed/                # Derived datasets
│   │   ├── population/           # Harmonized population estimates
│   │   ├── mortality/            # Processed lung cancer deaths
│   │   └── integrated/           # Final analytical dataset
│   └── external/                 # Third-party data
│       ├── dictionaries/         # Data dictionaries
│       └── shapefiles/           # INEGI geospatial boundaries
│
├── src/                          # Python source code
│   ├── __init__.py               # Package initialization
│   ├── utils.py                  # Shared utilities and constants
│   ├── data_validation.py        # Input data validation (Phase 1)
│   ├── harmonization.py          # Population harmonization (Phase 2)
│   ├── mortality_processing.py   # Mortality data processing (Phase 3)
│   ├── integration.py            # Data integration & standardization (Phase 4)
│   ├── analysis.py               # Statistical analysis (Phase 5)
│   ├── visualization.py          # Publication-quality figures (Phase 5)
│   ├── geospatial.py             # Choropleth maps (Phase 6)
│   └── run_analysis.py           # Master pipeline orchestrator
│
├── tests/                        # Unit tests
│   ├── test_utils.py             # Utility function tests
│   ├── test_analysis.py          # Statistical function tests
│   ├── test_integration.py       # Integration function tests
│   ├── test_harmonization.py     # Harmonization function tests
│   ├── test_mortality_processing.py
│   ├── test_geospatial.py        # Geospatial function tests
│   └── run_all_tests.py          # Test suite runner
│
├── docs/                         # Documentation
│   ├── en/                       # English documentation
│   │   ├── 01_methodology.md
│   │   ├── 02_data_acquisition_procedure.md
│   │   ├── 03_validation_report_census.md
│   │   ├── 04_validation_report_mortality.md
│   │   ├── 05_validation_report_pollution.md
│   │   ├── 06_methodology_harmonization.md
│   │   └── 07_data_dictionary.md
│   └── es/                       # Spanish documentation
│       └── ... (equivalent Spanish versions)
│
├── outputs/                      # Analysis outputs
│   ├── figures/                  # PNG and SVG visualizations
│   ├── tables/                   # CSV result tables
│   ├── models/                   # Full regression outputs
│   └── analysis_metadata.json    # Execution metadata
│
├── logs/                         # Execution logs
├── notebooks/                    # Jupyter notebooks (reserved)
│
├── environment.yml               # Conda environment specification
├── requirements.txt              # Pip requirements
├── LICENSE                       # CC BY 4.0 license
├── .gitignore                    # Git ignore rules
├── .gitattributes                # Git attributes
└── README.md                     # This file
```

---

## Quick Start

### Prerequisites

- Miniconda or Anaconda
- Git
- Approximately 2GB free disk space (for raw data)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/arlex-marin/cdmx-pollution-mortality.git
cd cdmx-pollution-mortality

# 2. Create and activate conda environment
conda env create -f environment.yml
conda activate mx-public-health-analysis

# 3. Download raw data (see docs/en/02_data_acquisition_procedure.md)
#    Required files:
#    - Census data from INEGI SCITEL
#    - Pollution and Mortality data from Zenodo (DOI: 10.5281/zenodo.10894651)
#    - Shapefiles from INEGI Marco Geoestadístico 2025

# 4. Place data in appropriate directories
#    - Census: data/raw/census/
#    - Mortality: data/raw/mortality/
#    - Pollution: data/raw/pollution/
#    - Shapefiles: data/external/shapefiles/
```

### Run Analysis

```bash
# Run complete pipeline (all 6 phases)
python -m src.run_analysis

# Run specific phase
python -m src.run_analysis --phase 6        # Geospatial only

# Run from specific phase onward
python -m src.run_analysis --from-phase 4   # Integration onward

# Skip validation (if data already validated)
python -m src.run_analysis --skip-validation

# List all available phases
python -m src.run_analysis --list-phases
```

### Run Tests

```bash
# Run all unit tests
python tests/run_all_tests.py

# Run specific test file
python -m unittest tests/test_analysis.py
```

---

## Analysis Pipeline

| Phase | Description | Input | Output | Runtime |
|:---:|:---|:---|:---|:---:|
| 1 | Data Validation | Raw data files | Validation reports (JSON) | ~30 sec |
| 2 | Population Harmonization | Census files (2000-2020) | Annual population estimates | ~20 sec |
| 3 | Mortality Processing | Mortality files (2000-2023) | Lung cancer death counts | ~45 sec |
| 4 | Integration & Standardization | Population + Mortality + Pollution | Final analytical dataset | ~15 sec |
| 5 | Statistical Analysis | Analytical dataset | Figures, tables, models | ~30 sec |
| 6 | Geospatial Visualization | Analytical dataset + Shapefiles | Interactive HTML maps | ~45 sec |

Total execution time: ~3.5 minutes on standard hardware

---

## Key Outputs

### Figures

| Figure | Description |
|:---|:---|
| temporal_trends.png | Time series of PM₂.₅ and mortality (2004-2022) |
| pm25_vs_mortality_scatter.png | Correlation scatter plot with regression line |
| alcaldia_boxplot.png | Mortality rate distribution by alcaldía |
| correlation_heatmap.png | Pollutant-mortality correlation matrix |
| regression_coefficients.png | Model coefficient comparison |
| sex_specific_effects.png | Male vs. female effect estimates |
| choropleth_mortality_2020.html | Interactive mortality map |
| choropleth_pm25_2020.html | Interactive pollution map |
| bivariate_choropleth_2020.png | Combined PM₂.₅ and mortality map |

### Tables

| Table | Description |
|:---|:---|
| descriptive_statistics.csv | Summary statistics for all variables |
| correlation_results.csv | Pearson and Spearman correlations |
| regression_results_summary.csv | Panel regression model results |
| sex_specific_regression.csv | Male and female effect estimates |
| yearly_averages.csv | Annual pollution and mortality trends |

### Models

| File | Description |
|:---|:---|
| regression_results.txt | Full regression output (all specifications) |
| sex_specific_results.txt | Full sex-specific regression output |

---

## Statistical Methods

### Study Design
- Panel study with 14 alcaldías over 19 years (2004-2022)
- Unit of analysis: alcaldía-year (266 observations)
- Exposure: Annual average PM₂.₅ concentration
- Outcome: Age-standardized lung cancer mortality rate (ICD-10 C33-C34)

### Regression Models
- Pooled OLS with HC3 robust standard errors
- Alcaldía fixed effects with cluster-robust standard errors
- Two-way fixed effects (alcaldía + year) with cluster-robust standard errors
- Log-linear specification for semi-elasticity interpretation

### Age Standardization
- Direct method using WHO World Standard Population
- Six harmonized age groups: 0-4, 5-14, 15-17, 18-24, 25-59, 60+

---

## Data Sources

| Data Type | Source | Temporal Coverage | Access |
|:---|:---|:---|:---|
| Population | INEGI Censuses | 2000, 2005, 2010, 2020 | [SCITEL](https://www.inegi.org.mx/app/scitel/) |
| Mortality | Zenodo (Crespo-Sanchez Melesio, 2024) | 2000-2023 | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Air Pollution | Zenodo (Crespo-Sanchez Melesio, 2024) | 1986-2022 | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Geospatial | INEGI Marco Geoestadístico | 2025 | [INEGI](https://www.inegi.org.mx/app/biblioteca/) |

---

## Results Summary

### Descriptive Statistics (2004-2022)

| Metric | Value |
|:---|:---|
| Analysis Period | 2004-2022 (19 years) |
| Alcaldías Analyzed | 14 of 16 |
| Total Observations | 266 alcaldía-years |
| Total Lung Cancer Deaths | 11,952 |
| Mean PM₂.₅ | 21.10 μg/m³ (SD: 2.78) |
| Mean Age-Standardized Rate | 14.03 per 100,000 (SD: 4.22) |

### Primary Regression Results

| Model | PM₂.₅ Coefficient (per 10 μg/m³) | 95% CI | p-value | R² |
|:---|:---|:---|:---|:---|
| Pooled OLS | +1.85 | [0.84, 2.85] | <0.001 | 0.113 |
| Alcaldía FE | +2.16 | [-0.19, 4.50] | 0.071 | 0.542 |
| Two-Way FE | +2.10 | [-0.33, 4.53] | 0.090 | 0.646 |
| Log-Linear | +0.015 | [-0.003, 0.033] | 0.098 | 0.658 |

### Correlation Results

| Pollutant | Pearson r | p-value | Interpretation |
|:---|:---|:---|:---|
| NO₂ | +0.425 | <0.001 | Strong positive |
| PM₂.₅ | +0.336 | <0.001 | Moderate positive |
| SO₂ | +0.305 | <0.001 | Moderate positive |
| PM₁₀ | +0.211 | <0.001 | Weak positive |
| CO | -0.025 | 0.685 | No association |
| O₃ | -0.299 | <0.001 | Negative |

---

## Documentation

Comprehensive documentation is available in both English and Spanish:

### English Documentation
- 01_methodology.md - Detailed study methodology
- 02_data_acquisition_procedure.md - Step-by-step data download instructions
- 03_validation_report_census.md - Census data validation results
- 04_validation_report_mortality.md - Mortality data validation results
- 05_validation_report_pollution.md - Pollution data validation results
- 06_methodology_harmonization.md - Population harmonization strategy
- 07_data_dictionary.md - Complete variable definitions

### Spanish Documentation (Documentación en Español)
- 01_metodologia.md - Metodología detallada del estudio
- 02_procedimiento_adquisicion_datos.md - Instrucciones de descarga de datos
- 03_reporte_validacion_censos.md - Resultados de validación de censos
- 04_reporte_validacion_mortalidad.md - Resultados de validación de mortalidad
- 05_reporte_validacion_contaminacion.md - Resultados de validación de contaminación
- 06_metodologia_armonizacion.md - Estrategia de armonización poblacional
- 07_diccionario_datos.md - Definiciones completas de variables

---

## Limitations

| Limitation | Impact | Mitigation |
|:---|:---|:---|
| Ecological study design | Cannot infer individual causation | Findings apply to population level |
| 14 clusters (alcaldías) | Limited statistical power | Cluster-robust SE; cautious interpretation |
| No individual smoking data | Potential residual confounding | Alcaldía FE controls for time-invariant differences |
| Annual average exposure | May not capture relevant exposure windows | Lag analysis conducted |
| 2 alcaldías excluded | Incomplete geographic coverage | Documented; sensitivity analyses confirm robustness |

---

## Citation

If you use this code or data in your research, please cite:

**Code:**
> Marín, A. (2026). *Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City* (Version 1.0.0) [Source code]. GitHub. https://github.com/arlex-marin/cdmx-pollution-mortality

**Data:**
> Marín, A. (2026). *Processed Data: Air Pollution and Lung Cancer Mortality in Mexico City* (Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19712907

**Report:**
> Marín, A. (2026). *Final Report: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City* (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.19712907

---

## License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

See the [LICENSE](LICENSE) file for the full license text.

---

## Acknowledgments

The author acknowledges the following data providers:
- INEGI (Instituto Nacional de Estadística y Geografía) for census and geospatial data
- Jub et al. for the air pollution dataset on Zenodo
- CONAPO for demographic projections used in validation

---

## Contact

**Arlex Marín**
- Email: arlex.marin@gmail.com
- GitHub: [@arlex-marin](https://github.com/arlex-marin)

For questions, collaboration inquiries, or to report issues, please open an issue on GitHub or contact via email.

---
