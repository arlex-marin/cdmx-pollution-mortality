# Methodology: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

**Project 1: High-Impact Public Data Analysis Projects for México**

**Author:** Arlex Marín  
**Date:** April 21, 2026  
**Version:** 2.0

---

## 1. Study Design

This study employs a **panel study design** analyzing 14 alcaldías of Mexico City over a 19-year period (2004-2022). The primary exposure is annual average PM₂.₅ concentration, and the primary outcome is age-standardized lung cancer mortality rate (ICD-10 codes C33-C34).

### 1.1 Research Questions
1. Is there a significant association between long-term PM₂.₅ exposure and lung cancer mortality across Mexico City alcaldías?
2. Which air pollutant shows the strongest correlation with lung cancer mortality?
3. Are there sex-specific differences in the pollution-mortality association?
4. How do mortality rates and pollution concentrations vary spatially across alcaldías?

### 1.2 Unit of Analysis
The unit of analysis is the **alcaldía-year**, with separate observations for males, females, and both sexes combined.

---

## 2. Data Sources

### 2.1 Population Data
Population estimates were derived from four Mexican censuses (2000, 2005, 2010, 2020) obtained from INEGI via the SCITEL tool. Annual population estimates for 2000-2022 were created using piecewise linear interpolation between census years. Age groups were harmonized to six categories (0-4, 5-14, 15-17, 18-24, 25-59, 60+) to ensure comparability across all census years.

**Source:** INEGI - Instituto Nacional de Estadística y Geografía
**Files:** RESLOC2000, RESLOC2005, RESLOC2010, ITER2020 (CDMX only)

### 2.2 Mortality Data
Individual-level mortality records for 2000-2023 were obtained from the Zenodo air pollution mortality dataset (Crespo-Sanchez, Melesio, 2024). Lung cancer deaths were identified using ICD-10 codes C33 (malignant neoplasm of trachea) and C34 (malignant neoplasm of bronchus and lung). Deaths were aggregated by alcaldía, year, harmonized age group, and sex.

**Source:** Zenodo - Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico
**Files:** deaths_registry.rar

### 2.3 Air Pollution Data
Annual average concentrations of PM₂.₅, PM₁₀, O₃, NO₂, SO₂, and CO for 1986-2022 were obtained from the Zenodo air pollution dataset (Crespo-Sanchez, Melesio, 2024). Data were aggregated by alcaldía and year, taking the mean across all monitoring stations within each alcaldía. 
Individual-level mortality records for 2000-2023 were obtained from the Zenodo air pollution dataset (Crespo-Sanchez, Melesio, 2024). Lung cancer deaths were identified using ICD-10 codes C33 (malignant neoplasm of trachea) and C34 (malignant neoplasm of bronchus and lung). Deaths were aggregated by alcaldía, year, harmonized age group, and sex.

**Source:** Zenodo - Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico
**Files:** Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv

### 2.4 Geospatial Data
Alcaldía boundary shapefiles were obtained from INEGI's Marco Geoestadístico 2025.

**Source:** INEGI - Marco Geoestadístico 2025
**File:** 09_ciudaddemexico/conjunto_de_datos/09mun.shp

---

## 3. Age Standardization

### 3.1 Method
Age-standardized mortality rates were calculated using the **direct standardization method** with the WHO World Standard Population as reference. The formula used was:

ASR = Σ (w_i × r_i) × 100,000


where:
- w_i = WHO standard population weight for age group i
- r_i = age-specific mortality rate for age group i

### 3.2 Harmonized Age Groups
| Age Group | Age Range | WHO Weight |
| :--- | :--- | :--- |
| 0-4 | 0 to 4 years | 0.0886 |
| 5-14 | 5 to 14 years | 0.1729 |
| 15-17 | 15 to 17 years | 0.0254 |
| 18-24 | 18 to 24 years | 0.0702 |
| 25-59 | 25 to 59 years | 0.5167 |
| 60+ | 60 years and older | 0.1262 |

---

## 4. Statistical Analysis

### 4.1 Descriptive Statistics
Descriptive statistics (mean, standard deviation, minimum, maximum) were calculated for all pollutants and mortality rates across the 14 alcaldías with monitoring data.

### 4.2 Correlation Analysis
Pearson and Spearman correlation coefficients were calculated between each pollutant and both crude and age-standardized mortality rates. Statistical significance was assessed at α = 0.05.

### 4.3 Panel Regression Models
We estimated four model specifications to assess the association between PM₂.₅ and lung cancer mortality:

#### Model 1: Pooled OLS

Mortality_rate_it = α + β × PM2.5_it + ε_it

Basic ordinary least squares regression ignoring panel structure.

#### Model 2: Alcaldía Fixed Effects

Mortality_rate_it = α_i + β × PM2.5_it + ε_it

Controls for time-invariant, unobserved alcaldía characteristics (e.g., baseline health status, socioeconomic factors).

#### Model 3: Two-Way Fixed Effects

Mortality_rate_it = α_i + γ_t + β × PM2.5_it + ε_it

Controls for both alcaldía fixed effects and year fixed effects (e.g., secular trends, policy changes).

#### Model 4: Log-Linear Model

ln(Mortality_rate_it) = α_i + γ_t + β × PM2.5_it + ε_it

Natural log transformation of the outcome variable; coefficient represents approximate percentage change.

### 4.4 Standard Errors
All models used **cluster-robust standard errors** clustered at the alcaldía level to account for within-alcaldía serial correlation.

### 4.5 Sex-Specific Analysis
Separate two-way fixed effects models were estimated for male and female mortality to assess sex-specific associations between PM₂.₅ and lung cancer mortality.

### 4.6 Software
All analyses were conducted using Python 3.11 with the following libraries:
- pandas 2.0.3 (data manipulation)
- statsmodels 0.14.0 (panel regression)
- scipy 1.10.1 (correlation analysis)
- geopandas 0.14.0 (spatial analysis)
- matplotlib 3.7.1 / seaborn 0.12.2 (visualization)
- plotly 5.14.1 (interactive maps)

---

## 5. Geospatial Analysis

### 5.1 Choropleth Maps
Choropleth maps were created using INEGI's 2025 Marco Geoestadístico shapefiles to visualize:
- Age-standardized lung cancer mortality rates by alcaldía (2010 and 2020)
- PM₂.₅ concentrations by alcaldía (2020)

### 5.2 Bivariate Choropleth Map
A 3×3 bivariate choropleth map was created for 2020, cross-classifying alcaldías by:
- PM₂.₅ concentration tertiles (Low, Medium, High)
- Age-standardized mortality rate tertiles (Low, Medium, High)

This visualization allows simultaneous assessment of exposure and outcome spatial patterns.

### 5.3 Interactive Maps
Interactive HTML maps were generated using Plotly for exploratory analysis and dissemination.

---

## 6. Sensitivity Analyses

### 6.1 Multi-Pollutant Models
Additional models including multiple pollutants (PM₂.₅, NO₂, O₃) were estimated to assess the independent effect of PM₂.₅ controlling for co-pollutants.

### 6.2 Lag Analysis
One-year and two-year lagged pollution variables were tested to account for potential latency between exposure and mortality.

---

## 7. Limitations

| Limitation | Mitigation |
| :--- | :--- |
| Ecological study design (alcaldía-level exposure) | Inherent to available data; findings apply to population level |
| Two alcaldías lack pollution monitoring | Documented as limitation; sensitivity analyses excluding them |
| Uneven temporal coverage across alcaldías | Two-way fixed effects models account for unbalanced panels |
| Potential confounding by smoking prevalence | Alcaldía fixed effects control for time-invariant differences |
| Latency between exposure and outcome | Lag analysis conducted as sensitivity check |

---

## 8. Reproducibility

### 8.1 Code Availability
All analysis code is available in the `src/` directory of the project repository. The complete pipeline can be executed using:

```bash
conda env create -f environment.yml
conda activate mx-public-health-analysis
python -m src.run_analysis
```

### 8.2 Data Availability

Census data: Publicly available from INEGI

Pollution and Mortality data: Available from Zenodo (DOI: 10.5281/zenodo.10894651)

Shapefiles: Publicly available from INEGI

### 9. References

Ahmad, O. B., Boschi-Pinto, C., Lopez, A. D., Murray, C. J., Lozano, R., & Inoue, M. (2001). Age standardization of rates: A new WHO standard. World Health Organization.

INEGI. (2000). XII Censo General de Población y Vivienda 2000.

INEGI. (2005). II Conteo de Población y Vivienda 2005.

INEGI. (2010). Censo de Población y Vivienda 2010.

INEGI. (2020). Censo de Población y Vivienda 2020.

Crespo-Sanchez, Melesio. (2024). Air Pollution and Cancer Mortality Dataset - Mexico City. Zenodo. https://doi.org/10.5281/zenodo.10894651

---

*End of Methodology Document*
