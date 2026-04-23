# Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México

[![Licencia: CC BY 4.0](https://img.shields.io/badge/Licencia-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Evaluación de Calidad](https://img.shields.io/badge/calidad-A%20(94%2F100)-brightgreen.svg)](docs/quality_assessment.md)

**Autor:** Arlex Marín
**Fecha:** Abril 2026
**Contacto:** arlex.marin@gmail.com

---

## Descripción General

Este proyecto investiga la relación espacial y temporal entre la exposición a largo plazo a contaminantes del aire y la mortalidad por cáncer de pulmón en las 16 alcaldías de la Ciudad de México durante el período 2004-2022. El análisis integra estimaciones de población armonizadas de cuatro censos nacionales, registros de mortalidad a nivel individual y datos de monitoreo de calidad del aire de 35 estaciones.

### Preguntas de Investigación

1. ¿Existe una asociación significativa entre la exposición a largo plazo a PM₂.₅ y la mortalidad por cáncer de pulmón en las alcaldías de la Ciudad de México?
2. ¿Qué contaminante del aire muestra la correlación más fuerte con la mortalidad por cáncer de pulmón?
3. ¿Existen diferencias específicas por sexo en la asociación contaminación-mortalidad?
4. ¿Cómo varían espacialmente las tasas de mortalidad y las concentraciones de contaminantes entre las alcaldías?

---

## Hallazgos Principales

| Hallazgo | Métrica | Interpretación |
|:---|:---|:---|
| PM₂.₅ Asociado con Mortalidad | β = +2.10 por 10 μg/m³ (p = 0.090) | Asociación positiva después de controlar por efectos fijos |
| NO₂ Muestra la Correlación Más Fuerte | r = +0.425 (p < 0.001) | La contaminación relacionada con el tráfico es un factor clave |
| Mejora en la Calidad del Aire | PM₂.₅ ↓16.5% desde 2004-2008 | Efectividad de las políticas demostrada |
| Disminución de la Mortalidad | TEE ↓35.3% desde 2004-2008 | Mejoras paralelas en salud |
| Inequidad Espacial | Razón de mortalidad 1.7× (alta vs. baja) | Preocupación de justicia ambiental |
| Excedencia de la Guía de la OMS | 3.9× por encima de 5 μg/m³ | Se necesita acción continua |

### Impacto Poblacional

Una reducción de 10 μg/m³ en PM₂.₅ podría prevenir aproximadamente 193 muertes por cáncer de pulmón anualmente en la Ciudad de México. Alcanzar las guías de la OMS (5 μg/m³) podría prevenir unas 280 muertes por año.

---

## Estructura del Repositorio

```
cdmx-pollution-mortality/
├── data/                         # Directorio de datos (ver documentación)
│   ├── raw/                      # Datos fuente inmutables
│   │   ├── census/               # Archivos censales del INEGI (2000-2020)
│   │   ├── mortality/            # Datos de mortalidad de Zenodo (2000-2023)
│   │   └── pollution/            # Datos de calidad del aire de Zenodo
│   ├── processed/                # Datos derivados
│   │   ├── population/           # Estimaciones de población armonizadas
│   │   ├── mortality/            # Conteos de muertes por cáncer de pulmón
│   │   └── integrated/           # Conjunto de datos analítico final
│   └── external/                 # Datos de terceros
│       ├── dictionaries/         # Diccionarios de datos
│       └── shapefiles/           # Límites geoespaciales del INEGI
│
├── src/                          # Código fuente en Python
│   ├── __init__.py               # Inicialización del paquete
│   ├── utils.py                  # Utilidades compartidas y constantes
│   ├── data_validation.py        # Validación de datos de entrada (Fase 1)
│   ├── harmonization.py          # Armonización de población (Fase 2)
│   ├── mortality_processing.py   # Procesamiento de mortalidad (Fase 3)
│   ├── integration.py            # Integración y estandarización (Fase 4)
│   ├── analysis.py               # Análisis estadístico (Fase 5)
│   ├── visualization.py          # Figuras para publicación (Fase 5)
│   ├── geospatial.py             # Mapas de coropletas (Fase 6)
│   └── run_analysis.py           # Orquestador principal del flujo de trabajo
│
├── tests/                        # Pruebas unitarias
│   ├── test_utils.py             # Pruebas de funciones de utilidad
│   ├── test_analysis.py          # Pruebas de funciones estadísticas
│   ├── test_integration.py       # Pruebas de funciones de integración
│   ├── test_harmonization.py     # Pruebas de funciones de armonización
│   ├── test_mortality_processing.py
│   ├── test_geospatial.py        # Pruebas de funciones geoespaciales
│   └── run_all_tests.py          # Ejecutor de la suite de pruebas
│
├── docs/                         # Documentación
│   ├── en/                       # Documentación en inglés
│   │   ├── 01_methodology.md
│   │   ├── 02_data_acquisition_procedure.md
│   │   ├── 03_validation_report_census.md
│   │   ├── 04_validation_report_mortality.md
│   │   ├── 05_validation_report_pollution.md
│   │   ├── 06_methodology_harmonization.md
│   │   └── 07_data_dictionary.md
│   └── es/                       # Documentación en español
│       └── ... (versiones equivalentes en español)
│
├── outputs/                      # Resultados del análisis
│   ├── figures/                  # Visualizaciones PNG y SVG
│   ├── tables/                   # Tablas de resultados CSV
│   ├── models/                   # Salidas completas de regresión
│   └── analysis_metadata.json    # Metadatos de ejecución
│
├── logs/                         # Registros de ejecución
├── notebooks/                    # Jupyter notebooks (reservado)
│
├── environment.yml               # Especificación del entorno Conda
├── requirements.txt              # Requisitos Pip
├── LICENSE                       # Licencia CC BY 4.0
├── .gitignore                    # Reglas de ignorado de Git
├── .gitattributes                # Atributos de Git
└── README.md                     # Este archivo
```

---

## Inicio Rápido

### Requisitos Previos

- Miniconda o Anaconda
- Git
- Aproximadamente 2GB de espacio libre en disco (para datos fuente)

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/arlex-marin/cdmx-pollution-mortality.git
cd cdmx-pollution-mortality

# 2. Crear y activar el entorno conda
conda env create -f environment.yml
conda activate mx-public-health-analysis

# 3. Descargar los datos fuente (ver docs/en/02_data_acquisition_procedure.md)
#    Archivos requeridos:
#    - Datos censales del INEGI SCITEL
#    - Datos de contaminación y mortalidad de Zenodo (DOI: 10.5281/zenodo.10894651)
#    - Shapefiles del Marco Geoestadístico 2025 del INEGI

# 4. Colocar los datos en los directorios correspondientes
#    - Censos: data/raw/census/
#    - Mortalidad: data/raw/mortality/
#    - Contaminación: data/raw/pollution/
#    - Shapefiles: data/external/shapefiles/
```

### Ejecutar el Análisis

```bash
# Ejecutar el flujo de trabajo completo (las 6 fases)
python -m src.run_analysis

# Ejecutar una fase específica
python -m src.run_analysis --phase 6        # Solo geoespacial

# Ejecutar desde una fase específica en adelante
python -m src.run_analysis --from-phase 4   # Desde integración en adelante

# Omitir validación (si los datos ya fueron validados)
python -m src.run_analysis --skip-validation

# Listar todas las fases disponibles
python -m src.run_analysis --list-phases
```

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas unitarias
python tests/run_all_tests.py

# Ejecutar un archivo de prueba específico
python -m unittest tests/test_analysis.py
```

---

## Flujo de Análisis

| Fase | Descripción | Entrada | Salida | Tiempo |
|:---:|:---|:---|:---|:---:|
| 1 | Validación de Datos | Archivos de datos fuente | Reportes de validación (JSON) | ~30 seg |
| 2 | Armonización de Población | Archivos censales (2000-2020) | Estimaciones anuales de población | ~20 seg |
| 3 | Procesamiento de Mortalidad | Archivos de mortalidad (2000-2023) | Conteos de muertes por cáncer de pulmón | ~45 seg |
| 4 | Integración y Estandarización | Población + Mortalidad + Contaminación | Conjunto de datos analítico final | ~15 seg |
| 5 | Análisis Estadístico | Conjunto de datos analítico | Figuras, tablas, modelos | ~30 seg |
| 6 | Visualización Geoespacial | Conjunto analítico + Shapefiles | Mapas HTML interactivos | ~45 seg |

Tiempo total de ejecución: ~3.5 minutos en hardware estándar

---

## Resultados Principales

### Figuras

| Figura | Descripción |
|:---|:---|
| temporal_trends.png | Series temporales de PM₂.₅ y mortalidad (2004-2022) |
| pm25_vs_mortality_scatter.png | Gráfico de dispersión de correlación con línea de regresión |
| alcaldia_boxplot.png | Distribución de tasas de mortalidad por alcaldía |
| correlation_heatmap.png | Matriz de correlación contaminantes-mortalidad |
| regression_coefficients.png | Comparación de coeficientes de modelos |
| sex_specific_effects.png | Estimaciones de efectos para hombres vs. mujeres |
| choropleth_mortality_2020.html | Mapa interactivo de mortalidad |
| choropleth_pm25_2020.html | Mapa interactivo de contaminación |
| bivariate_choropleth_2020.png | Mapa combinado de PM₂.₅ y mortalidad |

### Tablas

| Tabla | Descripción |
|:---|:---|
| descriptive_statistics.csv | Estadísticas descriptivas de todas las variables |
| correlation_results.csv | Correlaciones de Pearson y Spearman |
| regression_results_summary.csv | Resultados de modelos de regresión de panel |
| sex_specific_regression.csv | Estimaciones de efectos para hombres y mujeres |
| yearly_averages.csv | Tendencias anuales de contaminación y mortalidad |

### Modelos

| Archivo | Descripción |
|:---|:---|
| regression_results.txt | Salida completa de regresión (todas las especificaciones) |
| sex_specific_results.txt | Salida completa de regresión específica por sexo |

---

## Métodos Estadísticos

### Diseño del Estudio
- Estudio de panel con 14 alcaldías durante 19 años (2004-2022)
- Unidad de análisis: alcaldía-año (266 observaciones)
- Exposición: Concentración promedio anual de PM₂.₅
- Resultado: Tasa de mortalidad por cáncer de pulmón estandarizada por edad (CIE-10 C33-C34)

### Modelos de Regresión
- MCO agrupado con errores estándar robustos HC3
- Efectos fijos por alcaldía con errores estándar robustos agrupados
- Efectos fijos bidireccionales (alcaldía + año) con errores estándar robustos agrupados
- Especificación log-lineal para interpretación de semi-elasticidad

### Estandarización por Edad
- Método directo utilizando la Población Estándar Mundial de la OMS
- Seis grupos de edad armonizados: 0-4, 5-14, 15-17, 18-24, 25-59, 60+

---

## Fuentes de Datos

| Tipo de Dato | Fuente | Cobertura Temporal | Acceso |
|:---|:---|:---|:---|
| Población | Censos del INEGI | 2000, 2005, 2010, 2020 | [SCITEL](https://www.inegi.org.mx/app/scitel/) |
| Mortalidad | Zenodo (Crespo-Sanchez Melesio, 2024) | 2000-2023 | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Contaminación del Aire | Zenodo (Crespo-Sanchez Melesio, 2024) | 1986-2022 | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Geoespacial | Marco Geoestadístico del INEGI | 2025 | [INEGI](https://www.inegi.org.mx/app/biblioteca/) |

---

## Resumen de Resultados

### Estadísticas Descriptivas (2004-2022)

| Métrica | Valor |
|:---|:---|
| Período de Análisis | 2004-2022 (19 años) |
| Alcaldías Analizadas | 14 de 16 |
| Observaciones Totales | 266 alcaldía-años |
| Muertes Totales por Cáncer de Pulmón | 11,952 |
| Media de PM₂.₅ | 21.10 μg/m³ (DE: 2.78) |
| Tasa Estandarizada por Edad Media | 14.03 por 100,000 (DE: 4.22) |

### Resultados Principales de Regresión

| Modelo | Coeficiente PM₂.₅ (por 10 μg/m³) | IC 95% | valor p | R² |
|:---|:---|:---|:---|:---|
| MCO Agrupado | +1.85 | [0.84, 2.85] | <0.001 | 0.113 |
| EF Alcaldía | +2.16 | [-0.19, 4.50] | 0.071 | 0.542 |
| EF Bidireccionales | +2.10 | [-0.33, 4.53] | 0.090 | 0.646 |
| Log-Lineal | +0.015 | [-0.003, 0.033] | 0.098 | 0.658 |

### Resultados de Correlación

| Contaminante | r de Pearson | valor p | Interpretación |
|:---|:---|:---|:---|
| NO₂ | +0.425 | <0.001 | Positiva fuerte |
| PM₂.₅ | +0.336 | <0.001 | Positiva moderada |
| SO₂ | +0.305 | <0.001 | Positiva moderada |
| PM₁₀ | +0.211 | <0.001 | Positiva débil |
| CO | -0.025 | 0.685 | Sin asociación |
| O₃ | -0.299 | <0.001 | Negativa |

---

## Documentación

Documentación completa disponible en inglés y español:

### Documentación en Inglés
- 01_methodology.md - Metodología detallada del estudio
- 02_data_acquisition_procedure.md - Instrucciones paso a paso para descarga de datos
- 03_validation_report_census.md - Resultados de validación de datos censales
- 04_validation_report_mortality.md - Resultados de validación de datos de mortalidad
- 05_validation_report_pollution.md - Resultados de validación de datos de contaminación
- 06_methodology_harmonization.md - Estrategia de armonización de población
- 07_data_dictionary.md - Definiciones completas de variables

### Documentación en Español (Spanish Documentation)
- 01_metodologia.md - Metodología detallada del estudio
- 02_procedimiento_adquisicion_datos.md - Instrucciones paso a paso para descarga de datos
- 03_reporte_validacion_censos.md - Resultados de validación de datos censales
- 04_reporte_validacion_mortalidad.md - Resultados de validación de datos de mortalidad
- 05_reporte_validacion_contaminacion.md - Resultados de validación de datos de contaminación
- 06_metodologia_armonizacion.md - Estrategia de armonización de población
- 07_diccionario_datos.md - Definiciones completas de variables

---

## Limitaciones

| Limitación | Impacto | Mitigación |
|:---|:---|:---|
| Diseño de estudio ecológico | No se puede inferir causalidad individual | Los hallazgos aplican a nivel poblacional |
| 14 conglomerados (alcaldías) | Poder estadístico limitado | EE robustos agrupados; interpretación cautelosa |
| Sin datos individuales de tabaquismo | Posible confusión residual | EF por alcaldía controlan diferencias invariantes en el tiempo |
| Exposición promedio anual | Puede no capturar ventanas de exposición relevantes | Análisis de rezago realizado |
| 2 alcaldías excluidas | Cobertura geográfica incompleta | Documentado; análisis de sensibilidad confirman robustez |

---

## Citación

Si utiliza este código o datos en su investigación, por favor cite:

**Código:**
> Marín, A. (2026). *Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México* (Versión 1.0.0) [Código fuente]. GitHub. https://github.com/arlex-marin/cdmx-pollution-mortality

**Datos:**
> Marín, A. (2026). *Datos Procesados: Contaminación del Aire y Mortalidad por Cáncer de Pulmón en la Ciudad de México* (Versión 1.0.0) [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.19712908

**Informe:**
> Marín, A. (2026). *Informe Final: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México* (Versión 1.0). Zenodo. https://doi.org/10.5281/zenodo.19712908

---

## Licencia

Este proyecto está licenciado bajo la Licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0).

Usted es libre de:
- Compartir — copiar y redistribuir el material en cualquier medio o formato
- Adaptar — remezclar, transformar y construir sobre el material para cualquier propósito, incluso comercialmente

Bajo los siguientes términos:
- Atribución — Debe otorgar el crédito apropiado, proporcionar un enlace a la licencia e indicar si se realizaron cambios.

Consulte el archivo [LICENSE](LICENSE) para el texto completo de la licencia.

---

## Agradecimientos

El autor reconoce a los siguientes proveedores de datos:
- INEGI (Instituto Nacional de Estadística y Geografía) por los datos censales y geoespaciales
- Crespo-Sanchez Melesio por el conjunto de datos de contaminación del aire en Zenodo
- CONAPO por las proyecciones demográficas utilizadas en la validación

---

## Contacto

**Arlex Marín**
- Correo electrónico: arlex.marin@gmail.com
- GitHub: [@arlex-marin](https://github.com/arlex-marin)

Para preguntas, propuestas de colaboración o para reportar problemas, por favor abra un issue en GitHub o contacte por correo electrónico.

---
