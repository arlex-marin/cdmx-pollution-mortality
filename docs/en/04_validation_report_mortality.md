Mortality Data Validation Report
Project 1: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City

Author: Arlex Marín
Date: April 21, 2026
Version: 1.1 (Updated data source and script paths)

Executive Summary

This document presents the validation results for the mortality dataset used in the analysis of lung cancer mortality in Mexico City. The dataset contains individual-level mortality records for Mexico from 2000 to 2023, with comprehensive cause-of-death coding using ICD-10.

Key Findings:

    14,876 lung cancer deaths (C33-C34) identified in CDMX over 24 years (2000-2023)

    Average of 620 deaths per year

    77.1% of deaths occur in the 60+ age group

    56.3% of deaths are male, 43.7% female

    All 16 alcaldías have lung cancer deaths in every year

    Column naming conventions change between uppercase and lowercase across years

Metric	Value
Total lung cancer deaths (2000-2023)	14,876
Total lung cancer deaths (2000-2022, analysis period)	14,266
Average annual deaths	620
Age group with highest mortality	60+ (77.1%)
Sex distribution	Male 56.3% / Female 43.7%
Alcaldía coverage	16/16 all years
Years validated	24 (2000-2023)

1. Data Source

The mortality data was obtained from the Zenodo repository:

> Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10894651

File Location: data/raw/mortality/

Files: 24 annual CSV files (2000.csv through 2023.csv)

Format: Individual-level mortality records with 59 columns including:

    Geographic identifiers (entity, municipality of residence)

    Cause of death (ICD-10 codes)

    Demographic variables (age, sex)

    Additional covariates (education, occupation, etc.)

2. Validation Methodology

2.1 Data Extraction

For each year, the following steps were performed:

    Filter to CDMX residents: Entity code 9

    Filter to CDMX alcaldías: Municipality codes 2-17

    Identify lung cancer deaths: ICD-10 codes starting with C33 or C34

    Map age to harmonized groups: Using DGIS EDAD coding

    Map sex: 1 = Male, 2 = Female

2.2 Age Group Mapping

DGIS age codes were mapped to harmonized age groups:
DGIS Code Range	Meaning	Harmonized Group
< 4000	Under 1 year	0-4
4001-4004	1-4 years	0-4
4005-4014	5-14 years	5-14
4015-4017	15-17 years	15-17
4018-4024	18-24 years	18-24
4025-4059	25-59 years	25-59
4060-4120	60+ years	60+
4998	Unspecified	Excluded

2.3 Validation Checks

Check	Description	Result
File completeness	All expected years present	24/24 files
CDMX identification	Entity code 9 valid	All years
Alcaldía coverage	All 16 alcaldías represented	16/16 all years
ICD-10 codes	C33-C34 present	All years
Age mapping	Valid age groups	99.9% mapped
Sex mapping	Male/Female valid	100% mapped

3. Validation Results

3.1 Annual Lung Cancer Deaths

Year	Total Deaths (National)	CDMX Deaths	Lung Cancer Deaths	% of CDMX
2000	437,667	45,889	561	1.22%
2001	443,127	46,546	581	1.25%
2002	459,687	46,885	572	1.22%
2003	472,140	48,488	600	1.24%
2004	473,417	48,884	605	1.24%
2005	495,240	49,802	629	1.26%
2006	494,471	49,835	641	1.29%
2007	514,420	51,379	588	1.14%
2008	539,530	52,357	602	1.15%
2009	564,673	53,725	623	1.16%
2010	592,018	55,082	647	1.17%
2011	590,693	54,561	657	1.20%
2012	602,354	55,946	601	1.07%
2013	623,599	57,105	648	1.13%
2014	633,641	58,832	644	1.09%
2015	655,688	59,394	619	1.04%
2016	685,766	62,202	628	1.01%
2017	703,047	61,522	692	1.12%
2018	722,611	63,055	673	1.07%
2019	747,784	63,294	627	0.99%
2020	1,086,743	107,205	637	0.59%
2021	1,122,249	100,334	599	0.60%
2022	847,716	69,341	592	0.85%
2023	799,869	65,282	610	0.93%
Total	14,958,390	1,467,225	14,876	1.01%

3.2 Temporal Trends

Observations:

    Lung cancer deaths remain relatively stable (580-690 per year)

    No significant upward or downward trend over the 24-year period

    COVID-19 pandemic (2020-2021) did not significantly affect lung cancer mortality counts

    Slight dip in 2021-2022 may reflect pandemic-related healthcare disruptions

3.3 COVID-19 Impact Analysis

Period	Avg Total Deaths	Avg Lung Cancer	% Lung Cancer
Pre-COVID (2017-2019)	724,481	664	1.06%
COVID Peak (2020-2021)	1,104,496	618	0.60%
Post-COVID (2022-2023)	823,793	601	0.89%

Key Insight: Total mortality spiked 52% during COVID-19, but lung cancer deaths remained stable, causing the percentage to drop from ~1.1% to ~0.6%.

3.4 Age Distribution

Age Group	Total Deaths (2000-2023)	Percentage
0-4	4	0.03%
5-14	5	0.03%
15-17	9	0.06%
18-24	46	0.31%
25-59	3,334	22.41%
60+	11,478	77.16%
Total	14,876	100%

Key Insight: Lung cancer is overwhelmingly a disease of older adults, with over 77% of deaths occurring in the 60+ age group.

3.5 Sex Distribution

Sex	Total Deaths (2000-2023)	Percentage
Male	8,374	56.29%
Female	6,502	43.71%
Total	14,876	100%

Male-to-Female Ratio: 1.29:1

This reflects known epidemiological patterns where lung cancer incidence and mortality are higher in males, largely due to historical differences in smoking prevalence.

3.6 Alcaldía Coverage

All 16 alcaldías had lung cancer deaths in every year from 2000-2023. No alcaldía had zero deaths in any year, confirming complete geographic coverage.

4. Data Quality Findings

4.1 Column Naming Inconsistencies

The mortality files exhibit inconsistent column naming conventions across years:
Year Range	Column Case	Example
2000-2012	UPPERCASE	ENT_RESID, MUN_RESID, CAUSA_DEF
2013-2016	lowercase	ent_resid, mun_resid, causa_def
2017-2018	UPPERCASE	ENT_RESID, MUN_RESID, CAUSA_DEF
2019-2023	lowercase	ent_resid, mun_resid, causa_def

Mitigation: The processing script uses case-insensitive column detection to handle this variation automatically.

4.2 Age Coding Validation

Age Code Type	Count	% of Total	Status
Valid years (4001-4120)	14,850	99.83%	Mapped
Under 1 year (<4000)	22	0.15%	Mapped to 0-4
Unspecified (4998)	4	0.03%	Excluded
Total	14,876	100%	

Only 4 records (0.03%) had unspecified age and were excluded from analysis.

4.3 Sex Coding Validation

Sex Code	Count	Percentage	Status
1 (Male)	8,374	56.29%	Mapped
2 (Female)	6,502	43.71%	Mapped
Other (9)	0	0%	None found

All records had valid sex codes (1 or 2).

4.4 ICD-10 Code Validation

ICD-10	Description	Count	Percentage
C34	Malignant neoplasm of bronchus and lung	~14,500	~97.5%
C33	Malignant neoplasm of trachea	~376	~2.5%

The distribution between C34 and C33 is consistent with clinical expectations.

5. Processed Dataset Summary

The validated mortality data was aggregated into a harmonized dataset for analysis:

Output File: data/processed/mortality/cdmx_lung_cancer_deaths_2000_2022.csv
Attribute	Value
Total records	4,416
Years	2000-2022 (23 years)
Alcaldías	16
Age groups	6
Sexes	2
Total lung cancer deaths	14,266

Note: Analysis uses 2000-2022 (14,266 deaths). The additional 610 deaths from 2023 are available in the raw data but excluded from the final analytical dataset because the air pollution data ends in 2022.

Schema:
Column	Type	Description
alcaldia	string	Alcaldía name
alcaldia_code	string	INEGI municipality code (3 digits)
year	integer	Year of death
age_group	string	Harmonized age group
sex	string	Female / Male
deaths	integer	Number of lung cancer deaths

6. Conclusions and Recommendations

6.1 Data Quality Assessment

Aspect	Rating	Notes
Completeness	Excellent	All 24 years present, all alcaldías covered
Consistency	Good	Column naming varies but content consistent
Accuracy	Excellent	Age/sex coding valid for >99.9% of records
Usability	Excellent	Ready for integration with population data

6.2 Key Findings

    Stable mortality trend: Lung cancer deaths in CDMX have remained stable at ~620 per year from 2000-2023

    Age concentration: 77% of deaths occur in the 60+ age group, highlighting the importance of age standardization

    Sex disparity: Males account for 56% of deaths, consistent with known epidemiological patterns

    Complete geographic coverage: All 16 alcaldías have lung cancer deaths in every year

    COVID-19 impact: Total mortality spiked but lung cancer deaths remained stable

6.3 Recommendations for Analysis

    Age standardization is essential: Given the concentration of deaths in older age groups, age-standardized rates should be used for all comparisons

    Sex-specific analysis: Analyze male and female mortality separately due to different risk profiles

    Temporal focus: Use 2004-2022 for pollution-mortality analysis (matches air pollution data availability)

    Alcaldía-level analysis: Sufficient deaths per alcaldía for robust statistical analysis

7. Appendix

7.1 ICD-10 Codes Used

Code	Description
C33	Malignant neoplasm of trachea
C34	Malignant neoplasm of bronchus and lung

7.2 Alcaldía Codes

Code	Alcaldía
002	Azcapotzalco
003	Coyoacán
004	Cuajimalpa de Morelos
005	Gustavo A. Madero
006	Iztacalco
007	Iztapalapa
008	La Magdalena Contreras
009	Milpa Alta
010	Álvaro Obregón
011	Tláhuac
012	Tlalpan
013	Xochimilco
014	Benito Juárez
015	Cuauhtémoc
016	Miguel Hidalgo
017	Venustiano Carranza
7.3 Validation Script Information

The validation was performed using the integrated validation and processing pipeline.

Script Locations:

    Validation: src/data_validation.py

    Processing: src/mortality_processing.py

Execution Command:
bash

# Full validation (Phase 1)
python -m src.run_analysis --phase 1

# Mortality processing only (Phase 3)
python -m src.run_analysis --phase 3

Log Files:

    logs/mortality_validation_YYYYMMDD_HHMMSS.json

    logs/analysis_YYYYMMDD_HHMMSS.log

End of Report
