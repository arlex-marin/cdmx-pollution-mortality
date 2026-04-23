# Informe de Validación de Datos de Mortalidad

## Proyecto 1: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México

**Autor:** Arlex Marín  
**Fecha:** 21 de abril de 2026  
**Versión:** 1.1 (Fuente de datos y rutas de scripts actualizadas)

---

## Resumen Ejecutivo

Este documento presenta los resultados de validación para el conjunto de datos de mortalidad utilizado en el análisis de mortalidad por cáncer de pulmón en la Ciudad de México. El conjunto de datos contiene registros de mortalidad a nivel individual para México desde 2000 hasta 2023, con codificación exhaustiva de causa de muerte utilizando CIE-10.

**Hallazgos Clave:**

- 14,876 defunciones por cáncer de pulmón (C33-C34) identificadas en la CDMX durante 24 años (2000-2023)
- Promedio de 620 defunciones por año
- 77.1% de las defunciones ocurren en el grupo de edad de 60+
- 56.3% de las defunciones son hombres, 43.7% mujeres
- Las 16 alcaldías tienen defunciones por cáncer de pulmón en todos los años
- Las convenciones de nombres de columna cambian entre mayúsculas y minúsculas a lo largo de los años

| Métrica | Valor |
| :--- | :--- |
| Total de defunciones por cáncer de pulmón (2000-2023) | 14,876 |
| Total de defunciones por cáncer de pulmón (2000-2022, período de análisis) | 14,266 |
| Promedio anual de defunciones | 620 |
| Grupo de edad con mayor mortalidad | 60+ (77.1%) |
| Distribución por sexo | Hombres 56.3% / Mujeres 43.7% |
| Cobertura de alcaldías | 16/16 todos los años |
| Años validados | 24 (2000-2023) |

---

## 1. Fuente de Datos

Los datos de mortalidad se obtuvieron del archivo "deaths_registry.rar" del repositorio de Zenodo:

> Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10894651

**Ubicación del Archivo:** `data/raw/mortality/`

**Archivos:** 24 archivos CSV anuales (`2000.csv` hasta `2023.csv`)

**Formato:** Registros de mortalidad a nivel individual con 59 columnas que incluyen:

- Identificadores geográficos (entidad, municipio de residencia)
- Causa de defunción (códigos CIE-10)
- Variables demográficas (edad, sexo)
- Covariables adicionales (educación, ocupación, etc.)

---

## 2. Metodología de Validación

### 2.1 Extracción de Datos

Para cada año, se realizaron los siguientes pasos:

1. Filtrar a residentes de la CDMX: Código de entidad 9
2. Filtrar a alcaldías de la CDMX: Códigos de municipio 2-17
3. Identificar defunciones por cáncer de pulmón: Códigos CIE-10 que comienzan con C33 o C34
4. Mapear edad a grupos armonizados: Usando la codificación EDAD de la DGIS
5. Mapear sexo: 1 = Hombre, 2 = Mujer

### 2.2 Mapeo de Grupos de Edad

Los códigos de edad de la DGIS se mapearon a grupos de edad armonizados:

| Rango de Código DGIS | Significado | Grupo Armonizado |
| :--- | :--- | :--- |
| < 4000 | Menor de 1 año | 0-4 |
| 4001-4004 | 1-4 años | 0-4 |
| 4005-4014 | 5-14 años | 5-14 |
| 4015-4017 | 15-17 años | 15-17 |
| 4018-4024 | 18-24 años | 18-24 |
| 4025-4059 | 25-59 años | 25-59 |
| 4060-4120 | 60+ años | 60+ |
| 4998 | No especificado | Excluido |

### 2.3 Verificaciones de Validación

| Verificación | Descripción | Resultado |
| :--- | :--- | :--- |
| Integridad de archivos | Todos los años esperados presentes | 24/24 archivos |
| Identificación CDMX | Código de entidad 9 válido | Todos los años |
| Cobertura de alcaldías | Las 16 alcaldías representadas | 16/16 todos los años |
| Códigos CIE-10 | C33-C34 presentes | Todos los años |
| Mapeo de edad | Grupos de edad válidos | 99.9% mapeado |
| Mapeo de sexo | Hombre/Mujer válido | 100% mapeado |

---

## 3. Resultados de la Validación

### 3.1 Defunciones Anuales por Cáncer de Pulmón

| Año | Defunciones Totales (Nacional) | Defunciones CDMX | Defunciones Cáncer de Pulmón | % de CDMX |
| :--- | :--- | :--- | :--- | :--- |
| 2000 | 437,667 | 45,889 | 561 | 1.22% |
| 2001 | 443,127 | 46,546 | 581 | 1.25% |
| 2002 | 459,687 | 46,885 | 572 | 1.22% |
| 2003 | 472,140 | 48,488 | 600 | 1.24% |
| 2004 | 473,417 | 48,884 | 605 | 1.24% |
| 2005 | 495,240 | 49,802 | 629 | 1.26% |
| 2006 | 494,471 | 49,835 | 641 | 1.29% |
| 2007 | 514,420 | 51,379 | 588 | 1.14% |
| 2008 | 539,530 | 52,357 | 602 | 1.15% |
| 2009 | 564,673 | 53,725 | 623 | 1.16% |
| 2010 | 592,018 | 55,082 | 647 | 1.17% |
| 2011 | 590,693 | 54,561 | 657 | 1.20% |
| 2012 | 602,354 | 55,946 | 601 | 1.07% |
| 2013 | 623,599 | 57,105 | 648 | 1.13% |
| 2014 | 633,641 | 58,832 | 644 | 1.09% |
| 2015 | 655,688 | 59,394 | 619 | 1.04% |
| 2016 | 685,766 | 62,202 | 628 | 1.01% |
| 2017 | 703,047 | 61,522 | 692 | 1.12% |
| 2018 | 722,611 | 63,055 | 673 | 1.07% |
| 2019 | 747,784 | 63,294 | 627 | 0.99% |
| 2020 | 1,086,743 | 107,205 | 637 | 0.59% |
| 2021 | 1,122,249 | 100,334 | 599 | 0.60% |
| 2022 | 847,716 | 69,341 | 592 | 0.85% |
| 2023 | 799,869 | 65,282 | 610 | 0.93% |
| **Total** | **14,958,390** | **1,467,225** | **14,876** | **1.01%** |

### 3.2 Tendencias Temporales

**Observaciones:**

- Las defunciones por cáncer de pulmón permanecen relativamente estables (580-690 por año)
- Sin tendencia significativa al alza o a la baja durante el período de 24 años
- La pandemia de COVID-19 (2020-2021) no afectó significativamente los conteos de mortalidad por cáncer de pulmón
- Una ligera disminución en 2021-2022 puede reflejar interrupciones en la atención médica relacionadas con la pandemia

### 3.3 Análisis de Impacto de COVID-19

| Período | Promedio Defunciones Totales | Promedio Cáncer de Pulmón | % Cáncer de Pulmón |
| :--- | :--- | :--- | :--- |
| Pre-COVID (2017-2019) | 724,481 | 664 | 1.06% |
| Pico COVID (2020-2021) | 1,104,496 | 618 | 0.60% |
| Post-COVID (2022-2023) | 823,793 | 601 | 0.89% |

**Hallazgo Clave:** La mortalidad total aumentó un 52% durante COVID-19, pero las defunciones por cáncer de pulmón permanecieron estables, lo que provocó que el porcentaje disminuyera de ~1.1% a ~0.6%.

### 3.4 Distribución por Edad

| Grupo de Edad | Defunciones Totales (2000-2023) | Porcentaje |
| :--- | :--- | :--- |
| 0-4 | 4 | 0.03% |
| 5-14 | 5 | 0.03% |
| 15-17 | 9 | 0.06% |
| 18-24 | 46 | 0.31% |
| 25-59 | 3,334 | 22.41% |
| 60+ | 11,478 | 77.16% |
| **Total** | **14,876** | **100%** |

**Hallazgo Clave:** El cáncer de pulmón es predominantemente una enfermedad de adultos mayores, con más del 77% de las defunciones ocurriendo en el grupo de edad de 60+.

### 3.5 Distribución por Sexo

| Sexo | Defunciones Totales (2000-2023) | Porcentaje |
| :--- | :--- | :--- |
| Hombres | 8,374 | 56.29% |
| Mujeres | 6,502 | 43.71% |
| **Total** | **14,876** | **100%** |

**Razón Hombre-Mujer:** 1.29:1

Esto refleja patrones epidemiológicos conocidos donde la incidencia y mortalidad por cáncer de pulmón son mayores en hombres, en gran parte debido a diferencias históricas en la prevalencia del tabaquismo.

### 3.6 Cobertura de Alcaldías

Las 16 alcaldías tuvieron defunciones por cáncer de pulmón en todos los años desde 2000 hasta 2023. Ninguna alcaldía tuvo cero defunciones en ningún año, lo que confirma una cobertura geográfica completa.

---

## 4. Hallazgos de Calidad de los Datos

### 4.1 Inconsistencias en Nombres de Columnas

Los archivos de mortalidad exhiben convenciones inconsistentes de nombres de columna a lo largo de los años:

| Rango de Años | Formato de Columna | Ejemplo |
| :--- | :--- | :--- |
| 2000-2012 | MAYÚSCULAS | ENT_RESID, MUN_RESID, CAUSA_DEF |
| 2013-2016 | minúsculas | ent_resid, mun_resid, causa_def |
| 2017-2018 | MAYÚSCULAS | ENT_RESID, MUN_RESID, CAUSA_DEF |
| 2019-2023 | minúsculas | ent_resid, mun_resid, causa_def |

**Mitigación:** El script de procesamiento utiliza detección de columnas insensible a mayúsculas/minúsculas para manejar esta variación automáticamente.

### 4.2 Validación de Codificación de Edad

| Tipo de Código de Edad | Conteo | % del Total | Estado |
| :--- | :--- | :--- | :--- |
| Años válidos (4001-4120) | 14,850 | 99.83% | Mapeado |
| Menor de 1 año (<4000) | 22 | 0.15% | Mapeado a 0-4 |
| No especificado (4998) | 4 | 0.03% | Excluido |
| **Total** | **14,876** | **100%** | |

Solo 4 registros (0.03%) tenían edad no especificada y fueron excluidos del análisis.

### 4.3 Validación de Codificación de Sexo

| Código de Sexo | Conteo | Porcentaje | Estado |
| :--- | :--- | :--- | :--- |
| 1 (Hombre) | 8,374 | 56.29% | Mapeado |
| 2 (Mujer) | 6,502 | 43.71% | Mapeado |
| Otro (9) | 0 | 0% | Ninguno encontrado |

Todos los registros tenían códigos de sexo válidos (1 o 2).

### 4.4 Validación de Códigos CIE-10

| CIE-10 | Descripción | Conteo | Porcentaje |
| :--- | :--- | :--- | :--- |
| C34 | Tumor maligno de los bronquios y del pulmón | ~14,500 | ~97.5% |
| C33 | Tumor maligno de la tráquea | ~376 | ~2.5% |

La distribución entre C34 y C33 es consistente con las expectativas clínicas.

---

## 5. Resumen del Conjunto de Datos Procesado

Los datos de mortalidad validados se agregaron en un conjunto de datos armonizado para el análisis:

**Archivo de Salida:** `data/processed/mortality/cdmx_lung_cancer_deaths_2000_2022.csv`

| Atributo | Valor |
| :--- | :--- |
| Registros totales | 4,416 |
| Años | 2000-2022 (23 años) |
| Alcaldías | 16 |
| Grupos de edad | 6 |
| Sexos | 2 |
| Defunciones totales por cáncer de pulmón | 14,266 |

**Nota:** El análisis utiliza 2000-2022 (14,266 defunciones). Las 610 defunciones adicionales de 2023 están disponibles en los datos crudos pero se excluyen del conjunto de datos analítico final porque los datos de contaminación del aire terminan en 2022.

**Esquema:**

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `alcaldia` | cadena | Nombre de la alcaldía |
| `alcaldia_code` | cadena | Código de municipio INEGI (3 dígitos) |
| `year` | entero | Año de defunción |
| `age_group` | cadena | Grupo de edad armonizado |
| `sex` | cadena | Mujer / Hombre |
| `deaths` | entero | Número de defunciones por cáncer de pulmón |

---

## 6. Conclusiones y Recomendaciones

### 6.1 Evaluación de Calidad de los Datos

| Aspecto | Calificación | Notas |
| :--- | :--- | :--- |
| Integridad | Excelente | Los 24 años presentes, todas las alcaldías cubiertas |
| Consistencia | Buena | Los nombres de columna varían pero el contenido es consistente |
| Exactitud | Excelente | Codificación de edad/sexo válida para >99.9% de los registros |
| Usabilidad | Excelente | Listo para integración con datos de población |

### 6.2 Hallazgos Clave

1. **Tendencia de mortalidad estable:** Las defunciones por cáncer de pulmón en la CDMX se han mantenido estables en ~620 por año desde 2000-2023
2. **Concentración por edad:** El 77% de las defunciones ocurren en el grupo de edad de 60+, destacando la importancia de la estandarización por edad
3. **Disparidad por sexo:** Los hombres representan el 56% de las defunciones, consistente con patrones epidemiológicos conocidos
4. **Cobertura geográfica completa:** Las 16 alcaldías tienen defunciones por cáncer de pulmón en todos los años
5. **Impacto de COVID-19:** La mortalidad total aumentó pero las defunciones por cáncer de pulmón permanecieron estables

### 6.3 Recomendaciones para el Análisis

1. **La estandarización por edad es esencial:** Dada la concentración de defunciones en grupos de mayor edad, se deben utilizar tasas estandarizadas por edad para todas las comparaciones
2. **Análisis específico por sexo:** Analizar la mortalidad masculina y femenina por separado debido a diferentes perfiles de riesgo
3. **Enfoque temporal:** Usar 2004-2022 para el análisis de contaminación-mortalidad (coincide con la disponibilidad de datos de contaminación del aire)
4. **Análisis a nivel de alcaldía:** Suficientes defunciones por alcaldía para un análisis estadístico robusto

---

## 7. Apéndice

### 7.1 Códigos CIE-10 Utilizados

| Código | Descripción |
| :--- | :--- |
| C33 | Tumor maligno de la tráquea |
| C34 | Tumor maligno de los bronquios y del pulmón |

### 7.2 Códigos de Alcaldía

| Código | Alcaldía |
| :--- | :--- |
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

### 7.3 Información del Script de Validación

La validación se realizó utilizando la tubería integrada de validación y procesamiento.

**Ubicaciones de Scripts:**

- Validación: `src/data_validation.py`
- Procesamiento: `src/mortality_processing.py`

**Comando de Ejecución:**
```bash
# Validación completa (Fase 1)
python -m src.run_analysis --phase 1

# Solo procesamiento de mortalidad (Fase 3)
python -m src.run_analysis --phase 3
```

**Archivos de Registro:**

- `logs/mortality_validation_AAAAMMDD_HHMMSS.json`
- `logs/analysis_AAAAMMDD_HHMMSS.log`

---

*Fin del Informe*
