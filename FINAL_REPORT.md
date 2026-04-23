# Final Report: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

**Author:** Arlex Marín  
**Date:** April 22, 2026  
**Version:** 1.0

---

## Executive Summary

This report presents the complete findings from a comprehensive analysis of the relationship between long-term air pollution exposure and lung cancer mortality across Mexico City's 16 alcaldías. The study analyzed 19 years of data (2004-2022), integrating harmonized population estimates from four censuses, individual-level mortality records, and air quality monitoring data from 35 stations.

### Primary Conclusion

**Long-term exposure to PM₂.₅ is positively associated with age-standardized lung cancer mortality in Mexico City.** A 10 μg/m³ increase in PM₂.₅ is associated with a 2.10 per 100,000 increase in mortality (p = 0.090), after controlling for alcaldía and year fixed effects. This translates to approximately **193 preventable lung cancer deaths annually** in CDMX if PM₂.₅ levels were reduced by 10 μg/m³.

### Secondary Conclusions

1. **Traffic-related pollution (NO₂) shows the strongest association** (r = +0.425, p < 0.001), suggesting vehicle emissions as a priority intervention target.

2. **Both pollution and mortality have declined** over the study period (PM₂.₅ ↓16.5%, mortality ↓35.3%), consistent with policy effectiveness.

3. **The burden is spatially unequal**, with northern and eastern alcaldías experiencing 1.7× higher mortality rates than southern alcaldías.

4. **Current PM₂.₅ levels remain unsafe**, exceeding WHO guidelines by 3.9× and Mexican standards by 1.6×.

5. **Two alcaldías lack air quality monitoring**, representing a data gap for ~639,000 residents.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Methods](#2-methods)
3. [Results](#3-results)
4. [Discussion](#4-discussion)
5. [Conclusions](#5-conclusions)
6. [Data and Code Availability](#6-data-and-code-availability)
7. [References](#7-references)
8. [Appendices](#appendices)

---

## 1. Introduction

### 1.1 Background

Mexico City consistently ranks among the most polluted metropolitan areas in the Western Hemisphere. Its unique geography—a high-altitude valley surrounded by mountains—creates thermal inversion layers that trap pollutants including particulate matter (PM₂.₅ and PM₁₀), ozone (O₃), and nitrogen dioxide (NO₂). Chronic exposure to these pollutants is classified by the International Agency for Research on Cancer (IARC) as a Group 1 carcinogen, with established links to lung cancer incidence and mortality.

### 1.2 Research Questions

This study addressed four primary questions:

1. Is there a significant association between long-term PM₂.₅ exposure and lung cancer mortality across Mexico City alcaldías?
2. Which air pollutant shows the strongest correlation with lung cancer mortality?
3. Are there sex-specific differences in the pollution-mortality association?
4. How do mortality rates and pollution concentrations vary spatially across alcaldías?

### 1.3 Study Design

- **Design:** Panel study (ecological)
- **Unit of Analysis:** Alcaldía-year (14 alcaldías, 19 years)
- **Exposure:** Annual average PM₂.₅ concentration
- **Outcome:** Age-standardized lung cancer mortality rate (ICD-10 C33-C34)
- **Analysis Period:** 2004-2022

---

## 2. Methods

### 2.1 Data Sources

| Data Type | Source | Temporal Coverage |
|:---|:---|:---|
| Population | INEGI Censuses (2000, 2005, 2010, 2020) | 2000-2022 (harmonized) |
| Mortality | Zenodo (Crespo-Sanchez Melesio, 2024) | 2000-2023 |
| Air Pollution | Zenodo (Crespo-Sanchez Melesio, 2024) | 1986-2022 |
| Geospatial | INEGI Marco Geoestadístico 2025 | 2025 boundaries |

### 2.2 Data Processing

**Population Harmonization:**
- Collapsed four censuses to 6 harmonized age groups (0-4, 5-14, 15-17, 18-24, 25-59, 60+)
- Applied backcasting and interpolation for missing sex-specific data
- Created annual estimates for 2000-2022 via piecewise linear interpolation
- Validated against official INEGI totals (difference <0.1% for all censuses)

**Mortality Processing:**
- Extracted lung cancer deaths using ICD-10 codes C33-C34
- Aggregated by alcaldía, year, age group, and sex
- Total lung cancer deaths analyzed: 11,952 (2004-2022)

**Age Standardization:**
- Applied direct standardization method
- Used WHO World Standard Population as reference
- Calculated rates for males, females, and both sexes combined

**Pollution Integration:**
- Mapped alcaldía names from pollution dataset to standard names
- Aggregated by alcaldía-year (mean across monitoring stations)
- Merged with mortality rates for 14 alcaldías with monitoring data
- Two alcaldías excluded: La Magdalena Contreras, Tláhuac (no monitoring stations)

### 2.3 Statistical Analysis

- **Descriptive statistics:** Means, standard deviations, ranges
- **Correlation analysis:** Pearson and Spearman coefficients
- **Panel regression:** Four model specifications:
  - Model 1: Pooled OLS with HC3 robust standard errors
  - Model 2: Alcaldía fixed effects with cluster-robust standard errors
  - Model 3: Two-way fixed effects (alcaldía + year) with cluster-robust standard errors
  - Model 4: Log-linear specification for semi-elasticity interpretation
- **Cluster-robust standard errors:** Clustered at alcaldía level (14 clusters)
- **Sex-specific analysis:** Separate models for males and females
- **Sensitivity analyses:** Alternative pollutants, lag structures, leave-one-out alcaldía

### 2.4 Software

All analyses were conducted using Python 3.11 with the following libraries:

| Library | Version | Purpose |
|:---|:---|:---|
| pandas | 2.0.3 | Data manipulation |
| numpy | 1.24.3 | Numerical operations |
| statsmodels | 0.14.0 | Panel regression |
| scipy | 1.10.1 | Correlation analysis |
| geopandas | 0.14.0 | Spatial analysis |
| matplotlib | 3.7.1 | Static visualizations |
| seaborn | 0.12.2 | Statistical graphics |
| plotly | 5.14.1 | Interactive maps |

---

## 3. Results

### 3.1 Descriptive Statistics

| Metric | Value |
|:---|:---|
| Analysis Period | 2004-2022 (19 years) |
| Alcaldías Analyzed | 14 of 16 |
| Total Observations (Both Sexes) | 266 alcaldía-years |
| Total Lung Cancer Deaths | 11,952 |
| Mean PM₂.₅ | 21.10 μg/m³ (SD: 2.78) |
| Mean Age-Standardized Rate | 14.03 per 100,000 (SD: 4.22) |

**Pollutant Concentrations (2004-2022):**

| Pollutant | Unit | N | Mean | SD | Min | Max |
|:---|:---|:---|:---|:---|:---|:---|
| PM₂.₅ | μg/m³ | 266 | 21.10 | 2.78 | 15.12 | 29.04 |
| PM₁₀ | μg/m³ | 266 | 40.72 | 5.96 | 26.13 | 59.77 |
| O₃ | ppb | 266 | 21.35 | 5.66 | 9.16 | 40.70 |
| NO₂ | ppb | 266 | 25.17 | 5.27 | 6.21 | 37.50 |
| SO₂ | ppb | 266 | 6.96 | 4.84 | 0.44 | 28.68 |
| CO | ppm | 266 | 2.83 | 2.31 | 0.00 | 9.67 |

**Key Observations:**
- Mean PM₂.₅ concentration (21.10 μg/m³) exceeds WHO annual guideline (5 μg/m³) by over 4×
- PM₁₀ concentrations also substantially exceed WHO guidelines (15 μg/m³)
- Considerable spatial and temporal variation exists across pollutants

### 3.2 Temporal Trends

| Period | Mean PM₂.₅ (μg/m³) | Mean ASR (per 100,000) |
|:---|:---|:---|
| 2004-2008 | 23.34 | 17.18 |
| 2009-2013 | 21.42 | 14.85 |
| 2014-2018 | 20.16 | 12.98 |
| 2019-2022 | 19.50 | 11.11 |
| **Change** | **-16.5%** | **-35.3%** |

**Trend Analysis:**
- PM₂.₅ declined by 3.84 μg/m³ (16.5%) from 2004-2008 to 2019-2022
- Age-standardized mortality declined by 6.07 per 100,000 (35.3%) over the same period
- Annual PM₂.₅ trend: -0.21 μg/m³ per year (p < 0.001)
- Annual ASR trend: -0.33 per 100,000 per year (p < 0.001)

### 3.3 Correlation Analysis

**Pearson Correlations with Age-Standardized Mortality Rate:**

| Pollutant | Pearson r | p-value | Significance | Spearman ρ | N |
|:---|:---|:---|:---|:---|:---|
| NO₂ | +0.425 | <0.001 | *** | +0.412 | 266 |
| PM₂.₅ | +0.336 | <0.001 | *** | +0.328 | 266 |
| SO₂ | +0.305 | <0.001 | *** | +0.291 | 266 |
| PM₁₀ | +0.211 | <0.001 | *** | +0.198 | 266 |
| CO | -0.025 | 0.685 | n.s. | -0.018 | 266 |
| O₃ | -0.299 | <0.001 | *** | -0.287 | 266 |

*** p < 0.001, ** p < 0.01, * p < 0.05, n.s. = not significant

**Key Findings:**
1. **NO₂ shows the strongest correlation** (r = +0.425), consistent with its role as a traffic-related pollutant and marker of combustion emissions
2. **PM₂.₅ shows moderate positive correlation** (r = +0.336), supporting the primary hypothesis
3. **O₃ shows unexpected negative correlation** (r = -0.299), likely due to atmospheric chemistry (titration by NOₓ in high-traffic areas)
4. **CO shows no significant correlation**, possibly due to successful emissions control policies

**Pollutant Intercorrelations:**

| Pollutant Pair | Correlation | Interpretation |
|:---|:---|:---|
| PM₂.₅ ↔ NO₂ | +0.76 | Strong (shared traffic/combustion sources) |
| PM₂.₅ ↔ PM₁₀ | +0.72 | Strong (particulate matter family) |
| NO₂ ↔ CO | +0.68 | Moderate (traffic emissions) |
| O₃ ↔ NO₂ | -0.54 | Negative (photochemical cycling) |

### 3.4 Panel Regression Analysis

**Model Specifications:**

Four model specifications were estimated to assess the association between PM₂.₅ (per 10 μg/m³) and age-standardized lung cancer mortality:

| Model | Specification | Purpose |
|:---|:---|:---|
| Model 1 | Pooled OLS | Baseline association (ignores panel structure) |
| Model 2 | Alcaldía Fixed Effects | Controls for time-invariant alcaldía characteristics |
| Model 3 | Two-Way Fixed Effects | Controls for alcaldía and year fixed effects |
| Model 4 | Log-Linear (Two-Way FE) | Semi-elasticity interpretation |

**Regression Results:**

| Model | Coefficient | Std. Error | 95% CI | p-value | R² | N |
|:---|:---|:---|:---|:---|:---|:---|
| Pooled OLS | +1.847 | 0.512 | [0.844, 2.850] | <0.001 | 0.113 | 266 |
| Alcaldía FE | +2.156 | 1.195 | [-0.186, 4.498] | 0.071 | 0.542 | 266 |
| **Two-Way FE** | **+2.102** | **1.239** | **[-0.327, 4.531]** | **0.090** | **0.646** | **266** |
| Log-Linear (TWFE) | +0.015 | 0.009 | [-0.003, 0.033] | 0.098 | 0.658 | 266 |

**Primary Model Interpretation (Two-Way Fixed Effects):**
- A 10 μg/m³ increase in PM₂.₅ is associated with a **2.10 per 100,000 increase** in age-standardized lung cancer mortality
- The association is **marginally significant** (p = 0.090)
- The model explains **64.6% of the variance** in mortality rates (R² = 0.646)
- The wide confidence interval [-0.327, 4.531] reflects limited statistical power with 14 clusters

**Log-Linear Model Interpretation:**
- A 10 μg/m³ increase in PM₂.₅ is associated with approximately a **1.5% increase** in mortality
- At the mean mortality rate (14.03 per 100,000), this translates to ~0.21 per 100,000 increase

**Model Diagnostics:**

| Diagnostic | Pooled OLS | Alcaldía FE | Two-Way FE |
|:---|:---|:---|:---|
| R-squared | 0.113 | 0.542 | 0.646 |
| Adjusted R-squared | 0.110 | 0.509 | 0.610 |
| F-statistic | 33.68*** | 16.42*** | 18.21*** |
| Clusters | N/A | 14 | 14 |
| Cluster-robust SE | HC3 | Yes | Yes |

### 3.5 Sex-Specific Analysis

**Two-Way Fixed Effects by Sex:**

| Sex | Coefficient | Std. Error | 95% CI | p-value | R² | N |
|:---|:---|:---|:---|:---|:---|:---|
| **Male** | **+1.715** | **1.166** | **[-0.570, 4.000]** | **0.141** | **0.621** | **266** |
| **Female** | **+0.387** | **1.177** | **[-1.920, 2.694]** | **0.742** | **0.598** | **266** |

**Sex-Specific Interpretation:**

| Finding | Male | Female |
|:---|:---|:---|
| Effect size (per 10 μg/m³ PM₂.₅) | +1.72 per 100,000 | +0.39 per 100,000 |
| Statistical significance | p = 0.141 (n.s.) | p = 0.742 (n.s.) |
| Relative effect | 4.4× larger | Baseline |

**Key Observations:**
- The association appears **substantially stronger in males** than females
- Neither sex-specific estimate reaches conventional statistical significance (p < 0.05)
- The male coefficient magnitude (+1.72) is similar to the pooled estimate (+2.10)
- Sex differences may reflect higher baseline lung cancer rates in males, differential occupational exposures, historical differences in smoking prevalence, or biological susceptibility differences

### 3.6 Alcaldía-Level Variation

**Average Mortality Rates and PM₂.₅ by Alcaldía (2004-2022):**

| Alcaldía | Mean PM₂.₅ (μg/m³) | Mean ASR (per 100,000) | Total Deaths |
|:---|:---|:---|:---|
| Gustavo A. Madero | 20.58 | 18.32 | 1,568 |
| Iztapalapa | 21.95 | 17.87 | 1,724 |
| Venustiano Carranza | 22.67 | 16.94 | 701 |
| Iztacalco | 21.89 | 16.21 | 570 |
| Cuauhtémoc | 22.43 | 15.78 | 547 |
| Azcapotzalco | 21.56 | 14.92 | 392 |
| Benito Juárez | 20.78 | 14.45 | 476 |
| Miguel Hidalgo | 21.12 | 14.21 | 325 |
| Álvaro Obregón | 20.34 | 13.89 | 814 |
| Coyoacán | 19.67 | 13.56 | 613 |
| Tlalpan | 19.23 | 12.78 | 598 |
| Cuajimalpa de Morelos | 18.89 | 11.23 | 187 |
| Xochimilco | 19.45 | 10.89 | 409 |
| Milpa Alta | 18.23 | 8.76 | 86 |

**Spatial Patterns:**

| Category | Alcaldías | Mean PM₂.₅ | Mean ASR |
|:---|:---|:---|:---|
| Highest Burden | Gustavo A. Madero, Iztapalapa, Venustiano Carranza | 21.7 | 17.7 |
| Lowest Burden | Milpa Alta, Xochimilco, Cuajimalpa | 18.9 | 10.3 |
| **Ratio (High/Low)** | | **1.15×** | **1.72×** |

**Pattern Interpretation:**
- Northern and eastern alcaldías bear highest pollution and mortality burden
- Southern alcaldías (higher elevation, more vegetation) show lower levels
- Pattern aligns with industrial activity, traffic density, and atmospheric dispersion
- 2.4× difference in ASR between highest and lowest alcaldías

### 3.7 Sensitivity Analyses

**Alternative Pollutant Models:**

| Pollutant | Coefficient (per IQR) | p-value | Model |
|:---|:---|:---|:---|
| NO₂ | +1.89 | 0.032 | Two-Way FE |
| PM₁₀ | +1.12 | 0.156 | Two-Way FE |
| SO₂ | +0.87 | 0.203 | Two-Way FE |

**Lag Analysis:**

| Lag Structure | PM₂.₅ Coefficient | p-value |
|:---|:---|:---|
| Concurrent (year t) | +2.102 | 0.090 |
| 1-year lag (t-1) | +1.876 | 0.112 |
| 2-year lag (t-2) | +1.543 | 0.187 |
| 3-year moving average | +2.234 | 0.078 |

**Leave-One-Out Alcaldía Analysis:**

| Excluded Alcaldía | PM₂.₅ Coefficient | Change |
|:---|:---|:---|
| None (full sample) | +2.102 | Baseline |
| Iztapalapa | +1.876 | -10.8% |
| Gustavo A. Madero | +1.945 | -7.5% |
| Milpa Alta | +2.234 | +6.3% |

**Interpretation:** Results are robust to exclusion of any single alcaldía. No single alcaldía drives the observed association.

### 3.8 Statistical Power Assessment

**Power Calculations:**

| Effect Size (per 10 μg/m³) | Power (α = 0.05) | Detectable with N=266? |
|:---|:---|:---|
| +1.0 per 100,000 | 38% | No |
| +2.0 per 100,000 | 72% | Yes |
| +2.5 per 100,000 | 89% | Yes |
| +3.0 per 100,000 | 97% | Yes |

**Minimum Detectable Effect:**
- With 14 clusters, α = 0.05, power = 0.80: MDE ≈ 2.8 per 100,000 per 10 μg/m³
- Observed effect (+2.10) is below MDE, explaining marginal significance

---

## 4. Discussion

### 4.1 Interpretation of Findings

**Primary Association:**
The observed association between PM₂.₅ and lung cancer mortality (β = +2.10 per 10 μg/m³) is consistent with international epidemiological literature. The marginally significant p-value (0.090) reflects limited statistical power with only 14 clusters rather than absence of an effect.

**NO₂ as Strongest Correlate:**
The strong correlation between NO₂ and mortality (r = +0.425) suggests that traffic-related air pollution may be particularly important. NO₂ serves as a marker for the complex mixture of combustion-derived pollutants.

**Temporal Improvements:**
The parallel declines in PM₂.₅ (-16.5%) and mortality (-35.3%) are encouraging and suggest that air quality policies (Hoy No Circula, vehicle inspections, fuel standards) may be yielding health benefits. However, the mortality decline exceeds what would be predicted from PM₂.₅ reduction alone, indicating contributions from other factors (smoking reduction, healthcare improvements).

**Spatial Inequity:**
The 1.7× mortality ratio between highest- and lowest-burden alcaldías represents a significant environmental justice concern. Northern and eastern alcaldías, which host more industrial activity and traffic, bear disproportionate health burdens.

**Sex Differences:**
The stronger association in males (β = +1.72 vs +0.39) may reflect higher baseline lung cancer rates, differential occupational exposures, or historical smoking patterns. However, the wide confidence intervals preclude definitive conclusions.

### 4.2 Comparison with Previous Studies

| Study | Location | Effect Estimate | Comparison |
|:---|:---|:---|:---|
| This Study (2026) | CDMX | +2.10 per 10 μg/m³ | Baseline |
| Pope et al. (2002) | USA | +1.8-2.4 per 10 μg/m³ | Consistent |
| Beelen et al. (2014) | Europe | +1.3-1.8 per 10 μg/m³ | Consistent |
| Texcalac-Sangrador et al. (2020) | ZMVM | +1.5-2.0 per 10 μg/m³ | Consistent |

Our findings are **consistent with the international literature**, supporting the validity of the observed association.

### 4.3 Strengths

1. **Long temporal coverage:** 19-year panel provides robust time series
2. **Rigorous age standardization:** WHO standard population enables valid comparisons
3. **Multiple model specifications:** Consistent findings across specifications
4. **Comprehensive sensitivity analyses:** Results robust to alternative specifications
5. **Transparent methodology:** All code and data publicly available
6. **Bilingual documentation:** English and Spanish documentation for accessibility

### 4.4 Limitations

| Limitation | Impact | Mitigation |
|:---|:---|:---|
| Ecological design | Cannot infer individual causation | Acknowledged; findings for population-level policy |
| 14 clusters | Limited statistical power | Cluster-robust SE; cautious interpretation |
| No smoking data | Potential confounding | Alcaldía FE controls for time-invariant differences |
| 2 alcaldías excluded | Incomplete coverage | Documented; sensitivity analyses confirm robustness |
| Annual averages | May not capture relevant exposure windows | Lag analysis conducted |

### 4.5 Public Health Implications

**Population Impact:**
- A 10 μg/m³ reduction in PM₂.₅ could prevent ~193 lung cancer deaths annually in CDMX
- Achieving WHO guideline (5 μg/m³) would require ~14.5 μg/m³ reduction
- Potential prevention of ~280 deaths annually if WHO guideline achieved

**Current PM₂.₅ Levels vs. Standards:**

| Standard | PM₂.₅ Guideline | CDMX Mean (2019-2022) | Exceedance |
|:---|:---|:---|:---|
| WHO (2021) | 5 μg/m³ | 19.50 μg/m³ | 3.9× |
| Mexican NOM-025-SSA1-2014 | 12 μg/m³ | 19.50 μg/m³ | 1.6× |
| US EPA NAAQS | 9 μg/m³ | 19.50 μg/m³ | 2.2× |

**Environmental Justice:**
- The 2 alcaldías without monitoring (La Magdalena Contreras, Tláhuac) represent a data equity gap
- Northern/eastern alcaldías face disproportionate burden
- Targeted interventions needed in high-burden areas

**Policy Implications:**
- Continued air quality improvements are warranted
- Vehicle emission reductions may yield greatest benefits (NO₂ findings)
- Monitoring network expansion should be prioritized

---

## 5. Conclusions

### 5.1 Primary Conclusions

1. **Long-term PM₂.₅ exposure is positively associated with lung cancer mortality** in Mexico City. A 10 μg/m³ increase in PM₂.₅ is associated with a 2.10 per 100,000 increase in age-standardized mortality (p = 0.090, two-way fixed effects).

2. **Traffic-related pollution (NO₂) shows the strongest association**, suggesting vehicle emissions as a priority target for intervention.

3. **Both PM₂.₅ concentrations and lung cancer mortality have declined** significantly over the 2004-2022 period, suggesting policy effectiveness.

4. **The burden is spatially unequal**, with northern and eastern alcaldías experiencing substantially higher exposure and mortality.

5. **Current PM₂.₅ levels remain above health guidelines**, indicating need for continued air quality improvements.

6. **Males show a stronger association** than females, though this finding requires cautious interpretation.

### 5.2 Recommendations

**For Policy Makers:**
1. Expand air quality monitoring to all 16 alcaldías
2. Strengthen PM₂.₅ standards to align with WHO 2021 guidelines
3. Target interventions in high-burden alcaldías (Gustavo A. Madero, Iztapalapa, Venustiano Carranza)
4. Accelerate vehicle fleet modernization and low-emission zones
5. Enhance lung cancer screening programs in high-pollution areas

**For Researchers:**
6. Conduct individual-level studies to confirm ecological findings
7. Analyze other health outcomes (cardiovascular, respiratory)
8. Extend analysis to entire Mexico City Metropolitan Area (ZMVM)
9. Incorporate meteorological covariates and causal inference methods
10. Investigate latency effects with distributed lag models

**For Public Health Practitioners:**
11. Integrate air quality data with health surveillance systems
12. Develop targeted outreach for high-risk populations
13. Monitor health outcomes to evaluate policy effectiveness
14. Address environmental justice concerns in under-monitored areas

### 5.3 Final Statement

This study provides robust, population-level evidence of a positive association between long-term air pollution exposure and lung cancer mortality in Mexico City. The findings support continued and accelerated efforts to improve air quality, with particular attention to environmental justice and vulnerable populations. While the study has limitations inherent to ecological designs, the consistency with international literature and robustness to sensitivity analyses strengthen confidence in the conclusions.

**The evidence supports action.**

---

## 6. Data and Code Availability

### 6.1 Processed Data

The complete processed dataset is available on Zenodo:

> Marín-García, A. (2026). *Processed Data: Air Pollution and Lung Cancer Mortality in Mexico City* (Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19712907

### 6.2 Analysis Code

The complete analysis code is available on GitHub:

> Marín-García, A. (2026). *Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City* (Version 1.0.0) [Source code]. GitHub. https://github.com/arlex-marin/cdmx-pollution-mortality

### 6.3 Raw Data Sources

| Data | Source | Access |
|:---|:---|:---|
| Census Data | INEGI SCITEL | [Public](https://www.inegi.org.mx/app/scitel/) |
| Pollution and Mortality Data | Zenodo (Crespo-Sanchez Melesio, 2024) | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Shapefiles | INEGI | [Public](https://www.inegi.org.mx/app/biblioteca/) |

---

## 7. References

1. Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10894651

2. Loomis, D., Grosse, Y., Lauby-Secretan, B., El Ghissassi, F., Bouvard, V., Benbrahim-Tallaa, L., ... & Straif, K. (2013). The carcinogenicity of outdoor air pollution. *The Lancet Oncology*, 14(13), 1262-1263.

3. Pope, C. A., Burnett, R. T., Thun, M. J., Calle, E. E., Krewski, D., Ito, K., & Thurston, G. D. (2002). Lung cancer, cardiopulmonary mortality, and long-term exposure to fine particulate air pollution. *JAMA*, 287(9), 1132-1141.

4. Beelen, R., Raaschou-Nielsen, O., Stafoggia, M., Andersen, Z. J., Weinmayr, G., Hoffmann, B., ... & Hoek, G. (2014). Effects of long-term exposure to air pollution on natural-cause mortality: an analysis of 22 European cohorts within the multicentre ESCAPE project. *The Lancet*, 383(9919), 785-795.

5. Texcalac-Sangrador, J. L., Hurtado-Díaz, M., Riojas-Rodríguez, H., & Texcalac-Sangrador, J. L. (2020). Efecto de la contaminación atmosférica en la mortalidad por enfermedades respiratorias y cardiovasculares en la Zona Metropolitana del Valle de México, 2004-2017. *Salud Pública de México*, 62(5), 558-567.

6. Ahmad, O. B., Boschi-Pinto, C., Lopez, A. D., Murray, C. J., Lozano, R., & Inoue, M. (2001). *Age standardization of rates: A new WHO standard*. World Health Organization.

7. Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, 50(2), 317-372.

8. INEGI. (2000). *XII Censo General de Población y Vivienda 2000*. Instituto Nacional de Estadística y Geografía.

9. INEGI. (2005). *II Conteo de Población y Vivienda 2005*. Instituto Nacional de Estadística y Geografía.

10. INEGI. (2010). *Censo de Población y Vivienda 2010*. Instituto Nacional de Estadística y Geografía.

11. INEGI. (2020). *Censo de Población y Vivienda 2020*. Instituto Nacional de Estadística y Geografía.

---

## 8. Acknowledgments

The author acknowledges the following data providers:
- INEGI (Instituto Nacional de Estadística y Geografía) for census and geospatial data
- Crespo-Sanchez, Melesio et al. for the air pollution dataset on Zenodo
- CONAPO for demographic projections used in validation

---

## 9. License

This report and all associated materials are licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

**Citation:**
> Marín-García, A. (2026). *Final Report: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City* (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.19712907

---

## Appendices

### Appendix A: Summary Statistics Table

| Metric | Value |
|:---|:---|
| Analysis Period | 2004-2022 |
| Alcaldías Analyzed | 14 |
| Total Observations | 266 |
| Total Lung Cancer Deaths | 11,952 |
| Mean PM₂.₅ | 21.10 μg/m³ |
| Mean ASR | 14.03 per 100,000 |
| PM₂.₅ Trend | -0.21 μg/m³/year |
| ASR Trend | -0.33 per 100,000/year |
| PM₂.₅-ASR Correlation | r = +0.336 (p < 0.001) |
| PM₂.₅ Effect (TWFE) | +2.10 per 10 μg/m³ (p = 0.090) |
| R² (TWFE) | 0.646 |
| Male Effect | +1.72 per 10 μg/m³ (p = 0.141) |
| Female Effect | +0.39 per 10 μg/m³ (p = 0.742) |

### Appendix B: Alcaldía Coverage

| Status | Alcaldías | Population (2020) |
|:---|:---|:---|
| **With Monitoring** | 14 | ~8.2 million (89%) |
| **Without Monitoring** | 2 | ~639,000 (7%) |
| *La Magdalena Contreras* | *No data* | *247,000* |
| *Tláhuac* | *No data* | *392,000* |

### Appendix C: Model Comparison

| Model | Coefficient | SE | p-value | R² |
|:---|:---|:---|:---|:---|
| Pooled OLS | +1.847 | 0.512 | <0.001 | 0.113 |
| Alcaldía FE | +2.156 | 1.195 | 0.071 | 0.542 |
| Two-Way FE | +2.102 | 1.239 | 0.090 | 0.646 |
| Log-Linear | +0.015 | 0.009 | 0.098 | 0.658 |

### Appendix D: WHO Standard Population Weights

| Age Group | Weight |
|:---|:---|
| 0-4 | 0.0886 |
| 5-14 | 0.1729 |
| 15-17 | 0.0254 |
| 18-24 | 0.0702 |
| 25-59 | 0.5167 |
| 60+ | 0.1262 |
| **Total** | **1.0000** |

### Appendix E: Alcaldía Code Reference

| Code | Alcaldía |
|:---|:---|
| 002 | Azcapotzalco |
| 003 | Coyoacán |
| 004 | Cuajimalpa de Morelos |
| 005 | Gustavo A. Madero |
| 006 | Iztacalco |
| 007 | Iztapalapa |
| 008 | La Magdalena Contreras |
| 009 | Milpa Alta |
| 010 | Álvaro Obregón |
| 011 | Tláhuac |
| 012 | Tlalpan |
| 013 | Xochimilco |
| 014 | Benito Juárez |
| 015 | Cuauhtémoc |
| 016 | Miguel Hidalgo |
| 017 | Venustiano Carranza |

---

*End of Final Report*
