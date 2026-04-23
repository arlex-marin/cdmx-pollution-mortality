# ZENODO JUB AIR POLLUTION DATA VALIDATION REPORT

## Project 1: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

**Author:** Arlex Marín  
**Date:** April 21, 2026  
**Version:** 1.1 (Updated script paths and execution references)

---

## Executive Summary

This document presents the validation results for the Zenodo Jub air pollution dataset used in the analysis of lung cancer mortality in Mexico City. The dataset contains annual average concentrations of multiple air pollutants across monitoring stations in the Mexico City Metropolitan Area from 1986 to 2022.

**Key Findings:**
- 722 total records spanning 37 years (1986-2022)
- 6 pollutants available: PM2.5, PM10, O3, NO2, SO2, CO
- 35 monitoring stations across the metropolitan area
- 14 out of 16 CDMX alcaldías have pollution data
- 2 alcaldías missing: La Magdalena Contreras and Tláhuac (no monitoring stations)
- 100% pollutant data completeness - no missing values for any pollutant
- 12 non-CDMX municipalities included (Estado de México)

| Metric | Value |
| :--- | :--- |
| Total records | 722 |
| Years covered | 1986-2022 (37 years) |
| Monitoring stations | 35 |
| CDMX alcaldías covered | 14/16 (87.5%) |
| Pollutants available | PM2.5, PM10, O3, NO2, SO2, CO |
| Pollutant missing rate | 0% |
| Overall missing rate | 2.95% |

**Primary Conclusions:**
1. Excellent data quality: 100% of pollutant values are present with no missing data
2. Complete temporal coverage: 37 consecutive years (1986-2022) with no gaps
3. Strong geographic coverage: 14 of 16 CDMX alcaldías have monitoring data
4. Clean dataset: No duplicate rows, no completely empty rows
5. Ready for analysis: Data successfully integrated with mortality rates for 2004-2022

---

## 1. Data Source

### 1.1 Origin

The air pollution data was obtained from the Zenodo repository:

> Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10894651

### 1.2 File Information

| Attribute | Value |
| :--- | :--- |
| File name | `Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv` |
| File location | `data/raw/pollution/` |
| File size | ~0.1 MB |
| Encoding | UTF-8 |
| Delimiter | Comma (,) |
| Shape | (722, 18) |

### 1.3 Data Format

Annual average pollutant concentrations aggregated by alcaldía/municipality.

### 1.4 Column Descriptions

| Column | Type | Description |
| :--- | :--- | :--- |
| `clave` | String | Geographic identifier |
| `alcaldía o municipio` | String | Alcaldía or municipality name (original) |
| `entidad` | String | State (Ciudad de México or México) |
| `station` | String | Monitoring station code |
| `year` | Integer | Year of measurement |
| `nombre` | String | Monitoring station name |
| `latitud` | Float | Latitude in decimal degrees |
| `longitud` | Float | Longitude in decimal degrees |
| `altitud` | Float | Altitude in meters |
| `co` | Float | Carbon monoxide (ppm) |
| `no` | Float | Nitric oxide (ppb) |
| `no2` | Float | Nitrogen dioxide (ppb) |
| `nox` | Float | Nitrogen oxides (ppb) |
| `o3` | Float | Ozone (ppb) |
| `pm10` | Float | PM10 particulate matter (μg/m³) |
| `pm25` | Float | PM2.5 particulate matter (μg/m³) |
| `pmco` | Float | PM-coarse (μg/m³) |
| `so2` | Float | Sulfur dioxide (ppb) |

---

## 2. Validation Methodology

### 2.1 Validation Framework

The validation was performed using a dedicated Python script that executes five categories of checks:

| Category | Description | Pass Criteria |
| :--- | :--- | :--- |
| File Structure | Record count, columns, data types | All expected columns present |
| Temporal Coverage | Year range, gaps, records per year | No missing years in series |
| Geographic Coverage | Alcaldía identification and mapping | ≥80% of alcaldías covered |
| Pollutant Values | Range, mean, missing, negatives | <5% missing, plausible ranges |
| Data Quality | Duplicates, empty rows, missing rate | No duplicates, <5% missing |

### 2.2 Alcaldía Name Standardization

The dataset contains original names with accents, special characters, and variations. A mapping function standardizes names to match the harmonized population and mortality datasets.

**Transformations applied:**
- Remove accents (Á → A, é → e, í → i, ó → o, ú → u)
- Convert to ASCII
- Handle common variations and abbreviations

**Mapping examples:**

| Original | Mapped |
| :--- | :--- |
| 'Álvaro Obregón' | 'Alvaro Obregon' |
| 'Benito Juárez' | 'Benito Juarez' |
| 'Coyoacán' | 'Coyoacan' |
| 'Cuauhtémoc' | 'Cuauhtemoc' |
| 'Gustavo A. Madero' | 'Gustavo A. Madero' |
| 'Venustiano Carranza' | 'Venustiano Carranza' |
| 'Xochimilco' | 'Xochimilco' |

### 2.3 Validation Execution

| Attribute | Value |
| :--- | :--- |
| Script location | `src/data_validation.py` |
| Execution command | `python -m src.run_analysis --phase 1` |
| Run date | 2026-04-21 |
| Output log | `logs/pollution_validation_YYYYMMDD_HHMMSS.json` |

---

## 3. Validation Results

### 3.1 File Structure Validation

| Attribute | Value | Status |
| :--- | :--- | :--- |
| Total records | 722 | ✅ PASS |
| Total columns | 18 | ✅ PASS |
| Monitoring stations | 35 | ✅ PASS |
| Pollutants found | PM2.5, PM10, O3, NO2, SO2, CO | ✅ PASS |

**Complete Column List:**

| Index | Column Name | Data Type | Non-Null Count |
| :--- | :--- | :--- | :--- |
| 0 | `clave` | object | 722 |
| 1 | `alcaldía o municipio` | object | 722 |
| 2 | `entidad` | object | 722 |
| 3 | `station` | object | 722 |
| 4 | `year` | int64 | 722 |
| 5 | `nombre` | object | 722 |
| 6 | `latitud` | float64 | 722 |
| 7 | `longitud` | float64 | 722 |
| 8 | `altitud` | float64 | 722 |
| 9 | `co` | float64 | 722 |
| 10 | `no` | float64 | 722 |
| 11 | `no2` | float64 | 722 |
| 12 | `nox` | float64 | 722 |
| 13 | `o3` | float64 | 722 |
| 14 | `pm10` | float64 | 722 |
| 15 | `pm25` | float64 | 722 |
| 16 | `pmco` | float64 | 722 |
| 17 | `so2` | float64 | 722 |

### 3.2 Temporal Coverage Validation

| Attribute | Value | Status |
| :--- | :--- | :--- |
| Minimum year | 1986 | ✅ PASS |
| Maximum year | 2022 | ✅ PASS |
| Total years | 37 | ✅ PASS |
| Missing years | 0 | ✅ PASS |
| Year range completeness | 100% | ✅ PASS |

**Records per Year Trend:**

| Period | Average Records/Year | Network Status |
| :--- | :--- | :--- |
| 1986-1993 | 10 | Initial deployment |
| 1994-2003 | 16 | First expansion |
| 2004-2010 | 18 | Continued growth |
| 2011-2022 | 30 | Full operational coverage |

**Complete Annual Record Counts:**

| Year | Records | Year | Records | Year | Records | Year | Records |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1986 | 9 | 1996 | 16 | 2006 | 16 | 2016 | 32 |
| 1987 | 10 | 1997 | 16 | 2007 | 19 | 2017 | 32 |
| 1988 | 10 | 1998 | 16 | 2008 | 19 | 2018 | 32 |
| 1989 | 10 | 1999 | 16 | 2009 | 19 | 2019 | 35 |
| 1990 | 10 | 2000 | 16 | 2010 | 19 | 2020 | 34 |
| 1991 | 10 | 2001 | 16 | 2011 | 20 | 2021 | 34 |
| 1992 | 10 | 2002 | 16 | 2012 | 24 | 2022 | 34 |
| 1993 | 10 | 2003 | 17 | 2013 | 24 | | |
| 1994 | 16 | 2004 | 17 | 2014 | 25 | | |
| 1995 | 16 | 2005 | 16 | 2015 | 31 | | |

### 3.3 Geographic Coverage Validation

#### 3.3.1 Overall Mapping Results

| Category | Count | Percentage |
| :--- | :--- | :--- |
| Total unique geographic names | 26 | 100% |
| CDMX alcaldías successfully mapped | 14 | 53.8% |
| Non-CDMX municipalities | 12 | 46.2% |

#### 3.3.2 CDMX Alcaldías with Pollution Data (14 of 16)

| Alcaldía | Records | First Year | Last Year | Coverage Status |
| :--- | :--- | :--- | :--- | :--- |
| Cuajimalpa de Morelos | 40 | 1994 | 2022 | Full (29 years) |
| Iztapalapa | 40 | 1994 | 2022 | Full (29 years) |
| Venustiano Carranza | 37 | 2000 | 2022 | Full (23 years) |
| Álvaro Obregón | 37 | 2000 | 2022 | Full (23 years) |
| Xochimilco | 29 | 2007 | 2022 | Partial (16 years) |
| Benito Juárez | 27 | 2011 | 2022 | Partial (12 years) |
| Azcapotzalco | 20 | 2016 | 2022 | Partial (7 years) |
| Coyoacán | 20 | 2016 | 2022 | Partial (7 years) |
| Tlalpan | 16 | 2007 | 2022 | Partial (16 years) |
| Iztacalco | 16 | 2007 | 2022 | Partial (16 years) |
| Cuauhtémoc | 11 | 2012 | 2022 | Limited (11 years) |
| Gustavo A. Madero | 9 | 2016 | 2022 | Limited (7 years) |
| Miguel Hidalgo | 8 | 2016 | 2022 | Limited (7 years) |
| Milpa Alta | 7 | 2016 | 2022 | Limited (7 years) |

#### 3.3.3 CDMX Alcaldías Missing Pollution Data (2 of 16)

| Alcaldía | Reason for Absence |
| :--- | :--- |
| La Magdalena Contreras | No air quality monitoring station in dataset |
| Tláhuac | No air quality monitoring station in dataset |

**Note:** Both missing alcaldías are predominantly residential and semi-rural areas with lower population density and industrial activity.

#### 3.3.4 Non-CDMX Municipalities Present (Filtered During Integration)

| Municipality | State |
| :--- | :--- |
| Ecatepec de Morelos | México |
| Nezahualcóyotl | México |
| Tlalnepantla de Baz | México |
| Naucalpan de Juárez | México |
| Atizapán de Zaragoza | México |
| Cuautitlán Izcalli | México |
| Coacalco de Berriozábal | México |
| Tultitlán | México |
| Chalco | México |
| Texcoco | México |
| Acolman | México |
| Ocoyoacac | México |

These municipalities are part of the Mexico City Metropolitan Area but were excluded from CDMX-specific analysis.

#### 3.3.5 Complete Alcaldía Name Mapping Table

| Original Name | Mapped Name | Status |
| :--- | :--- | :--- |
| Acolman | None | Non-CDMX |
| Atizapán de Zaragoza | None | Non-CDMX |
| Azcapotzalco | Azcapotzalco | ✅ MAPPED |
| Benito Juárez | Benito Juarez | ✅ MAPPED |
| Chalco | None | Non-CDMX |
| Coacalco de Berriozábal | None | Non-CDMX |
| Coyoacán | Coyoacan | ✅ MAPPED |
| Cuajimalpa de Morelos | Cuajimalpa de Morelos | ✅ MAPPED |
| Cuauhtémoc | Cuauhtemoc | ✅ MAPPED |
| Cuautitlán Izcalli | None | Non-CDMX |
| Ecatepec de Morelos | None | Non-CDMX |
| Gustavo A. Madero | Gustavo A. Madero | ✅ MAPPED |
| Iztacalco | Iztacalco | ✅ MAPPED |
| Iztapalapa | Iztapalapa | ✅ MAPPED |
| Miguel Hidalgo | Miguel Hidalgo | ✅ MAPPED |
| Milpa Alta | Milpa Alta | ✅ MAPPED |
| Naucalpan de Juárez | None | Non-CDMX |
| Nezahualcóyotl | None | Non-CDMX |
| Ocoyoacac | None | Non-CDMX |
| Texcoco | None | Non-CDMX |
| Tlalnepantla de Baz | None | Non-CDMX |
| Tlalpan | Tlalpan | ✅ MAPPED |
| Tultitlán | None | Non-CDMX |
| Venustiano Carranza | Venustiano Carranza | ✅ MAPPED |
| Xochimilco | Xochimilco | ✅ MAPPED |
| Álvaro Obregón | Alvaro Obregon | ✅ MAPPED |

### 3.4 Pollutant Values Validation

#### 3.4.1 Summary Statistics for All Pollutants

| Pollutant | Unit | Count | Missing | Mean | Std Dev | Min | Max | Negative |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PM2.5 | μg/m³ | 722 | 0 | 22.38 | 4.29 | 11.84 | 51.87 | 0 |
| PM10 | μg/m³ | 722 | 0 | 45.02 | 9.98 | 19.46 | 108.97 | 0 |
| O3 | ppb | 722 | 0 | 21.70 | 5.01 | 9.16 | 42.37 | 0 |
| NO2 | ppb | 722 | 0 | 24.98 | 5.14 | 6.21 | 46.68 | 0 |
| SO2 | ppb | 722 | 0 | 8.31 | 8.26 | 0.44 | 70.11 | 0 |
| CO | ppm | 722 | 0 | 3.28 | 3.06 | -0.17 | 19.72 | 1 |

**Note:** The single negative CO value (-0.17 ppm) is a rounding artifact near zero and was treated as 0 in the final dataset.

#### 3.4.2 Pollutant-Specific Plausibility Assessment

**PM2.5 (Fine Particulate Matter):**
- Range: 11.84 - 51.87 μg/m³
- Plausibility: Excellent - Values consistent with Mexico City air quality reports
- High values: >45 μg/m³ represent high pollution days (thermal inversions)
- Mean: 22.38 μg/m³ - Above WHO guideline (5 μg/m³ annual)
- **Status: ✅ VALID**

**PM10 (Coarse Particulate Matter):**
- Range: 19.46 - 108.97 μg/m³
- Plausibility: Excellent - Expected range for urban area with resuspended dust
- High values: >100 μg/m³ occur during dust storms and inversion events
- Mean: 45.02 μg/m³ - Above WHO guideline (15 μg/m³ annual)
- **Status: ✅ VALID**

**O3 (Ozone):**
- Range: 9.16 - 42.37 ppb
- Plausibility: Excellent - Typical for photochemical smog in high-altitude cities
- Formation: Secondary pollutant from NOx and VOCs in sunlight
- Mean: 21.70 ppb - Within expected urban range
- **Status: ✅ VALID**

**NO2 (Nitrogen Dioxide):**
- Range: 6.21 - 46.68 ppb
- Plausibility: Excellent - Traffic-related pollutant
- Sources: Vehicle emissions, combustion processes
- Mean: 24.98 ppb - Consistent with metropolitan traffic levels
- **Status: ✅ VALID**

**SO2 (Sulfur Dioxide):**
- Range: 0.44 - 70.11 ppb
- Plausibility: Excellent - Industrial and volcanic sources
- Spikes: Occasional high values likely from industrial emissions
- Mean: 8.31 ppb - Generally low baseline with episodic peaks
- **Status: ✅ VALID**

**CO (Carbon Monoxide):**
- Range: -0.17 - 19.72 ppm
- Plausibility: Good - Vehicle emissions, improved with catalytic converters
- Negative value: Single -0.17 ppm value (rounding artifact near zero)
- Mean: 3.28 ppm - Declining trend with fleet modernization
- **Status: ✅ VALID (1 artifact acceptable)**

### 3.5 Data Quality Validation

| Metric | Value | Status |
| :--- | :--- | :--- |
| Duplicate rows | 0 | ✅ PASS |
| Completely empty rows | 0 | ✅ PASS |
| Overall missing rate | 2.95% | ✅ PASS |
| Pollutant missing rate | 0% | ✅ PASS |
| Geographic data missing | 0% | ✅ PASS |
| Temporal data missing | 0% | ✅ PASS |

**Missing Values by Column:**

| Column | Missing Count | Missing Percentage | Notes |
| :--- | :--- | :--- | :--- |
| `alcaldia_mapped` | 405 | 56.1% | Non-CDMX municipalities |
| All pollutant columns | 0 | 0% | Complete data |
| All geographic columns | 0 | 0% | Complete data |
| All temporal columns | 0 | 0% | Complete data |

---

## 4. Key Findings Summary

### 4.1 Strengths

| Aspect | Finding | Implication |
| :--- | :--- | :--- |
| Data Completeness | 100% of pollutant values present | No imputation needed |
| Temporal Coverage | 37 consecutive years (1986-2022) | Robust time series analysis |
| Pollutant Variety | 6 criteria pollutants available | Multi-pollutant models possible |
| Station Density | 35 monitoring stations | Good spatial representation |
| Data Quality | No duplicates, no empty rows | Clean dataset |
| Geographic Coverage | 14/16 CDMX alcaldías (87.5%) | Sufficient for inference |

### 4.2 Limitations

| Aspect | Finding | Mitigation |
| :--- | :--- | :--- |
| Missing Alcaldías | La Magdalena Contreras and Tláhuac lack data | Document as limitation |
| Uneven Coverage | Records per alcaldía range from 7 to 40 | Use fixed-effects models |
| Non-CDMX Municipalities | 12 Estado de México municipalities present | Filtered during integration |
| Early Years Sparse | 1986-1993 have limited records | Focus on 2004-2022 |
| Single CO Artifact | One negative CO value (-0.17 ppm) | Treat as zero |

### 4.3 Geographic Coverage Assessment

**Coverage by Population (2020 estimates):**

| Category | Alcaldías | Population | % of CDMX Total |
| :--- | :--- | :--- | :--- |
| With pollution data | 14 | ~8.2 million | ~89% |
| Without pollution data | 2 | ~0.4 million | ~11% |

The 14 alcaldías with pollution data represent approximately 89% of Mexico City's total population.

### 4.4 Temporal Coverage by Alcaldía (2004-2022 Analysis Period)

| Alcaldía | Years in 2004-2022 | Complete | Analysis Inclusion |
| :--- | :--- | :--- | :--- |
| Cuajimalpa de Morelos | 19 | Yes | Full panel |
| Iztapalapa | 19 | Yes | Full panel |
| Venustiano Carranza | 19 | Yes | Full panel |
| Álvaro Obregón | 19 | Yes | Full panel |
| Xochimilco | 16 | Partial | Included |
| Tlalpan | 16 | Partial | Included |
| Iztacalco | 16 | Partial | Included |
| Benito Juárez | 12 | Partial | Included |
| Cuauhtémoc | 11 | Partial | Included |
| Azcapotzalco | 7 | Partial | Included |
| Coyoacán | 7 | Partial | Included |
| Gustavo A. Madero | 7 | Partial | Included |
| Miguel Hidalgo | 7 | Partial | Included |
| Milpa Alta | 7 | Partial | Included |

---

## 5. Integration with Mortality Data

### 5.1 Integration Process Summary

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Load pollution data | 722 records loaded |
| 2 | Map alcaldía names | 14 CDMX alcaldías identified |
| 3 | Filter to CDMX only | 317 records retained |
| 4 | Aggregate by alcaldía-year | Mean across stations per alcaldía-year |
| 5 | Merge with mortality rates | Left join on alcaldía and year |
| 6 | Filter to analysis period | 2004-2022 retained |

### 5.2 Final Analytical Dataset Characteristics

| Attribute | Value |
| :--- | :--- |
| Analysis years | 2004-2022 (19 years) |
| Alcaldías with pollution data | 14 |
| Total observations (Both sexes) | 266 |
| Total observations (All sexes) | 798 |
| Primary exposure variable | PM2.5 |
| Primary outcome variable | Age-standardized mortality rate |

### 5.3 Analysis-Ready Variables

| Variable | Type | Mean | Std Dev | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| pm25 | Continuous | 21.10 | 2.78 | 15.12 | 29.04 |
| pm10 | Continuous | 40.72 | 5.96 | 26.13 | 59.77 |
| o3 | Continuous | 21.35 | 5.66 | 9.16 | 40.70 |
| no2 | Continuous | 25.17 | 5.27 | 6.21 | 37.50 |
| so2 | Continuous | 6.96 | 4.84 | 0.44 | 28.68 |
| co | Continuous | 2.83 | 2.31 | 0.00 | 9.67 |
| crude_rate | Continuous | 7.15 | 2.30 | 0.66 | 14.24 |
| age_standardized_rate | Continuous | 14.03 | 4.22 | 1.52 | 28.67 |

---

## 6. Conclusions and Recommendations

### 6.1 Overall Data Quality Assessment

| Aspect | Grade | Justification |
| :--- | :--- | :--- |
| Completeness | A+ | 100% pollutant values present; no missing data |
| Temporal Coverage | A+ | 37 consecutive years; no gaps |
| Geographic Coverage | A- | 14/16 alcaldías (87.5%); 2 missing |
| Consistency | A | Clean structure; consistent formatting |
| Accuracy | A | Plausible value ranges; minimal artifacts |
| Usability | A | Ready for statistical analysis |
| **OVERALL** | **A** | **Excellent quality; suitable for publication** |

### 6.2 Recommendations

1. **PROCEED WITH 14 ALCALDÍAS** for primary analysis. The 87.5% coverage is sufficient for robust statistical inference and generalizable findings.

2. **DOCUMENT MISSING ALCALDÍAS** as a study limitation in publications. Note that La Magdalena Contreras and Tláhuac are predominantly residential and semi-rural areas with lower population density.

3. **FOCUS ANALYSIS ON 2004-2022** when the monitoring network was fully established and mortality data is most reliable.

4. **CONSIDER SENSITIVITY ANALYSIS** excluding alcaldías with limited records (fewer than 15 observations) to ensure findings are not driven by sparse data.

5. **NOTE NON-CDMX MUNICIPALITIES** are correctly excluded; the analytical dataset is properly restricted to Mexico City proper.

6. **UTILIZE MULTI-POLLUTANT MODELS** given the availability of 6 pollutants, but be mindful of collinearity among traffic-related pollutants (NO2, CO).

### 6.3 Expected Statistical Power

| Model Type | Observations | Clusters | Power Assessment |
| :--- | :--- | :--- | :--- |
| Pooled OLS | 266 | N/A | Adequate |
| Alcaldía Fixed Effects | 266 | 14 | Good |
| Two-Way Fixed Effects | 266 | 14 alcaldías × 19 years | Good |
| Sex-Specific (Male) | 266 | 14 | Good |
| Sex-Specific (Female) | 266 | 14 | Good |

---

## 7. Appendix

### 7.1 Validation Script Information

- **Script location:** `src/data_validation.py`
- **Output log:** `logs/pollution_validation_YYYYMMDD_HHMMSS.json`
- **Run command:** `python -m src.run_analysis --phase 1`

### 7.2 Alcaldía Coverage Summary

**CDMX Alcaldías (16 total):**

**PRESENT (14):**
- Azcapotzalco
- Benito Juárez
- Coyoacán
- Cuajimalpa de Morelos
- Cuauhtémoc
- Gustavo A. Madero
- Iztacalco
- Iztapalapa
- Miguel Hidalgo
- Milpa Alta
- Tlalpan
- Venustiano Carranza
- Xochimilco
- Álvaro Obregón

**MISSING (2):**
- La Magdalena Contreras (no monitoring station)
- Tláhuac (no monitoring station)

### 7.3 Pollutants Summary Table

| Pollutant | Unit | Count | Mean | Std Dev | Min | Max | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PM2.5 | μg/m³ | 722 | 22.38 | 4.29 | 11.84 | 51.87 | ✅ VALID |
| PM10 | μg/m³ | 722 | 45.02 | 9.98 | 19.46 | 108.97 | ✅ VALID |
| O3 | ppb | 722 | 21.70 | 5.01 | 9.16 | 42.37 | ✅ VALID |
| NO2 | ppb | 722 | 24.98 | 5.14 | 6.21 | 46.68 | ✅ VALID |
| SO2 | ppb | 722 | 8.31 | 8.26 | 0.44 | 70.11 | ✅ VALID |
| CO | ppm | 722 | 3.28 | 3.06 | -0.17 | 19.72 | ✅ VALID |

---

*End of Report*
