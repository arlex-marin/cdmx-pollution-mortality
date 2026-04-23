# Data Dictionary: CDMX Air Pollution and Lung Cancer Mortality Analysis Dataset

**Project 1: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City**

**Author:** Arlex Marín  
**Date:** April 21, 2026  
**Version:** 1.0

---

## File: `cdmx_analysis_dataset_2004_2022.csv`

### Overview
This dataset contains annual observations for 16 alcaldías of Mexico City from 2004 to 2022. Each row represents a unique combination of alcaldía, year, and sex category (Female, Male, Both). The dataset includes population estimates, lung cancer mortality counts, crude and age-standardized mortality rates, and annual average air pollutant concentrations.

### Dataset Dimensions
| Attribute | Value |
| :--- | :--- |
| Total records | 912 |
| Alcaldías | 16 |
| Years | 2004-2022 (19 years) |
| Sex categories | 3 (Female, Male, Both) |
| Variables | 13 |

### Variables

| Variable | Type | Description | Units | Valid Range | Missing Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `alcaldia` | String | Name of the alcaldía (municipality) | - | 16 alcaldías of CDMX | 0 |
| `year` | Integer | Year of observation | - | 2004-2022 | 0 |
| `sex` | String | Sex category | - | Female, Male, Both | 0 |
| `population` | Integer | Estimated population | Persons | >0 | 0 |
| `deaths` | Integer | Lung cancer deaths (ICD-10 C33-C34) | Count | ≥0 | 0 |
| `crude_rate` | Float | Crude mortality rate | per 100,000 | ≥0 | 0 |
| `age_standardized_rate` | Float | Age-standardized mortality rate (WHO standard) | per 100,000 | ≥0 | 0 |
| `pm25` | Float | Annual average PM₂.₅ concentration | μg/m³ | 11.8-51.9 | 76 (8.3%) |
| `pm10` | Float | Annual average PM₁₀ concentration | μg/m³ | 19.5-109.0 | 76 (8.3%) |
| `o3` | Float | Annual average ozone concentration | ppb | 9.2-42.4 | 76 (8.3%) |
| `no2` | Float | Annual average nitrogen dioxide concentration | ppb | 6.2-46.7 | 76 (8.3%) |
| `so2` | Float | Annual average sulfur dioxide concentration | ppb | 0.4-70.1 | 76 (8.3%) |
| `co` | Float | Annual average carbon monoxide concentration | ppm | 0.0-19.7 | 76 (8.3%) |

### Notes on Missing Values
- Pollution data (pm25, pm10, o3, no2, so2, co) is missing for **La Magdalena Contreras** and **Tláhuac** because these alcaldías do not have air quality monitoring stations in the source dataset.
- This results in 76 missing pollution records out of 912 total analysis records (8.3%).
- All 14 other alcaldías have complete pollution data for all years 2004-2022.
- The single negative CO value reported in validation (-0.17 ppm) was treated as 0 in the final dataset.

### Alcaldías Included
| Alcaldía | Pollution Data Available | INEGI Code |
| :--- | :--- | :--- |
| Azcapotzalco | Yes | 002 |
| Coyoacán | Yes | 003 |
| Cuajimalpa de Morelos | Yes | 004 |
| Gustavo A. Madero | Yes | 005 |
| Iztacalco | Yes | 006 |
| Iztapalapa | Yes | 007 |
| La Magdalena Contreras | **No** | 008 |
| Milpa Alta | Yes | 009 |
| Álvaro Obregón | Yes | 010 |
| Tláhuac | **No** | 011 |
| Tlalpan | Yes | 012 |
| Xochimilco | Yes | 013 |
| Benito Juárez | Yes | 014 |
| Cuauhtémoc | Yes | 015 |
| Miguel Hidalgo | Yes | 016 |
| Venustiano Carranza | Yes | 017 |

**Note:** Alcaldía names in the dataset use ASCII characters (e.g., "Alvaro Obregon" instead of "Álvaro Obregón") for compatibility.

### Summary Statistics (Both Sexes, 2004-2022)

| Variable | N | Mean | SD | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| pm25 | 266 | 21.10 | 2.78 | 15.12 | 29.04 |
| pm10 | 266 | 40.72 | 5.96 | 26.13 | 59.77 |
| o3 | 266 | 21.35 | 5.66 | 9.16 | 40.70 |
| no2 | 266 | 25.17 | 5.27 | 6.21 | 37.50 |
| so2 | 266 | 6.96 | 4.84 | 0.44 | 28.68 |
| co | 266 | 2.83 | 2.31 | 0.00 | 9.67 |
| crude_rate | 304 | 7.15 | 2.30 | 0.66 | 14.24 |
| age_standardized_rate | 304 | 14.03 | 4.22 | 1.52 | 28.67 |
| population | 304 | 542,420 | 393,353 | 18,835 | 1,835,486 |
| deaths | 304 | 39.3 | 27.1 | 1 | 128 |

### Source Datasets
| Variable Group | Source | Temporal Coverage |
| :--- | :--- | :--- |
| Population | INEGI Censuses 2000, 2005, 2010, 2020 (harmonized) | 2000-2022 |
| Mortality | Zenodo Air Pollution Dataset (Crespo-Sanchez, Melesio, 2024) | 2000-2023 |
| Pollution | Zenodo Air Pollution Dataset (Crespo-Sanchez, Melesio, 2024) | 1986-2022 |

### Age Standardization
Age-standardized rates were calculated using the direct method with the WHO World Standard Population as reference. The harmonized age groups used were: 0-4, 5-14, 15-17, 18-24, 25-59, and 60+ years.

### WHO Standard Weights Applied
| Age Group | Weight |
| :--- | :--- |
| 0-4 | 0.0886 |
| 5-14 | 0.1729 |
| 15-17 | 0.0254 |
| 18-24 | 0.0702 |
| 25-59 | 0.5167 |
| 60+ | 0.1262 |

### ICD-10 Codes Used
| Code | Description |
| :--- | :--- |
| C33 | Malignant neoplasm of trachea |
| C34 | Malignant neoplasm of bronchus and lung |

---

*End of Data Dictionary*
