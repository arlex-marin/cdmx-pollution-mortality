# Data Acquisition and Curation Procedure

**Project 1: Geospatial Analysis of Air Pollution and Cancer Mortality in Mexico City**
**Author:** Arlex Marín
**Date:** April 21, 2026
**Version:** 1.0 (English Translation)

---

## Population and Housing Census Data

1. Population and housing census data were downloaded on April 16, 2026, along with data dictionaries for each census from the official INEGI website through the SCITEL tool: https://www.inegi.org.mx/app/scitel/Default?ev=9

2. Data for each census were downloaded by selecting all indicators for "geographic identification" and "Age and sex structure" for the year 2020, and all indicators for "geographic identification" and "population" for the years 2010, 2005, and 2000.

3. The four downloaded files are:
   - `ITER2020 - 09 Ciudad de México.csv` for the census corresponding to the year 2020
   - `RESLOC2010 - 09 Ciudad de México.txt` for the census corresponding to the year 2010
   - `RESLOC2005 - 09 Ciudad de México.txt` for the census corresponding to the year 2005
   - `RESLOC2000 - 09 Ciudad de México.txt` for the census corresponding to the year 2000

4. File names were changed:
   - from `ITER2020 - 09 Ciudad de México.csv` to `ITER2020_09_CDMX.csv`
   - from `RESLOC2010 - 09 Ciudad de México.txt` to `RESLOC2010_09_CDMX.csv`
   - from `RESLOC2005 - 09 Ciudad de México.txt` to `RESLOC2005_09_CDMX.csv`
   - from `RESLOC2000 - 09 Ciudad de México.txt` to `RESLOC2000_09_CDMX.csv`

   to standardize names and file handling without sacrificing functionality.

5. These data were moved to the folder `data/raw/census/`.

6. Data dictionaries for each census were downloaded, these are:
   - `fd_2020.pdf` for the census corresponding to the year 2020
   - `fd_2010.pdf` for the census corresponding to the year 2010
   - `fd_2005.pdf` for the census corresponding to the year 2005
   - `fd_2000.pdf` for the census corresponding to the year 2000

7. These dictionaries were moved to the folder `data/external/dictionaries/`.

---

## Air Pollution and Mortality Data by Alcaldía

1. Data files were downloaded on April 16, 2026, from the official website of the database "Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico data" on Zenodo: https://zenodo.org/records/17691800

2. The files `Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv` and `deaths_registry.rar` were downloaded.

3. The file csv file was moved to the folder `data/raw/pollution/` to standardize data organization and file handling without sacrificing functionality.

4. The compressed rar file was extracted to the folder `data/raw/mortality/` to standardize data organization and file handling without sacrificing functionality.

---

## Geospatial Data for Mexico City

1. Geospatial data were downloaded on April 21, 2026, from the official INEGI Marco Geoestadístico website corresponding to the year 2025, through the official INEGI tool: https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551163061

2. The file `09_ciudaddemexico.zip` (794551163061_s.zip) was downloaded.

3. Its contents were extracted into the folder `data/external/shapefiles/` maintaining the original directory structure.

4. The resulting structure is:

```
data/external/shapefiles/
└── 09_ciudaddemexico/
    ├── catalogos/
    ├── conjunto_de_datos/
    │   ├── 09mun.shp
    │   ├── 09mun.shx
    │   ├── 09mun.dbf
    │   └── ...
    └── metadatos/
```

5. The main file used for mapping is `09mun.shp`, which contains the polygons of the 16 alcaldías of Mexico City.

---

## Directory Structure Summary

```
data/
├── external/
│   ├── dictionaries/
│   │   ├── fd_2000.pdf
│   │   ├── fd_2005.pdf
│   │   ├── fd_2010.pdf
│   │   └── fd_2020.pdf
│   └── shapefiles/
│       ├── 09_ciudaddemexico/
│       │   ├── catalogos/
│       │   │   ├── áreas_geoestadísticas_estatales.csv
│       │   │   ├── ...
│       │   │   └── localidades_urbanas_y_rurales_amanzanadas.pdf
│       │   ├── conjunto_de_datos/
│       │   │   ├── 09a.cpg
│       │   │   ├── ...
│       │   │   ├── 09mun.cpg
│       │   │   ├── 09mun.dbf
│       │   │   ├── 09mun.prj
│       │   │   ├── 09mun.shp
│       │   │   ├── 09mun.shx
│       │   │   ├── ...
│       │   │   └── 09sip.shx
│       │   └── metadatos/
│       │       ├── metadato_mg_2025.txt
│       │       ├── mg_2025_09.txt
│       │       └── mg_2025_09.xml
│       └── 09_ciudaddemexico.zip
├── processed/
│   ├── integrated/
│   ├── mortality/
│   └── population/
└── raw/
    ├── census/
    │   ├── ITER2020_09_CDMX.csv
    │   ├── RESLOC2000_09_CDMX.csv
    │   ├── RESLOC2005_09_CDMX.csv
    │   └── RESLOC2010_09_CDMX.csv
    ├── mortality/
    │   ├── 2000.csv
    │   ├── ...
    │   └── 2023.csv
    └── pollution/
        └── Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv
```

---

## Data Source References

| Data Type | Source | URL |
| :--- | :--- | :--- |
| Census Data | INEGI SCITEL | https://www.inegi.org.mx/app/scitel/Default?ev=9 |
| Pollution and Mortality Data  | Zenodo (Crespo-Sanchez, Melesio, 2024) | https://zenodo.org/records/17691800 |
| Geospatial Data | INEGI Marco Geoestadístico 2025 | https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551163061 |

---

## Data Citation

When using these data sources, please cite:

- **Census Data:** INEGI. (2000, 2005, 2010, 2020). *Censos y Conteos de Población y Vivienda*. Instituto Nacional de Estadística y Geografía, México.

- **Pollution and Mortality Data:** Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10894651

- **Geospatial Data:** INEGI. (2025). *Marco Geoestadístico 2025*. Instituto Nacional de Estadística y Geografía, México.

---

## Notes on Data Usage

### Census Data Considerations
- The 2000 census has limited age detail at the municipal level; sex-specific age distributions required estimation
- The 2005 Conteo provides good coverage but requires splitting of the 15-24 age group
- The 2010 census has detailed breakdowns but requires estimation for sex-specific 25-59 population
- The 2020 census is the gold standard with full quinquennial age-sex detail; note that `POBTOT` is empty at the municipal level

### Mortality Data Considerations
- ICD-10 codes C33 (trachea) and C34 (bronchus and lung) identify lung cancer cases

### Pollution Data Considerations
- Two alcaldías (La Magdalena Contreras and Tláhuac) lack monitoring stations
- The dataset includes 12 non-CDMX municipalities from Estado de México (filtered during integration)
- A single negative CO value (-0.17 ppm) is a rounding artifact and was treated as 0

### Geospatial Data Considerations
- The original CRS is EPSG:6372 (transformed to EPSG:4326 for mapping)
- The `09mun.shp` file contains boundaries for all 16 alcaldías

---

*End of Data Acquisition Procedure document*
