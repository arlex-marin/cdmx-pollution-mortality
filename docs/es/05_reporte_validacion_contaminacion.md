# INFORME DE VALIDACIÓN DE DATOS DE CONTAMINACIÓN DEL AIRE EN ZENODO

## Proyecto 1: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México

**Autor:** Arlex Marín  
**Fecha:** 21 de abril de 2026  
**Versión:** 1.1 (Rutas de scripts y referencias de ejecución actualizadas)

---

## Resumen Ejecutivo

Este documento presenta los resultados de validación para el conjunto de datos de contaminación del aire en Zenodo (Crespo-Sanchez, Melesio) utilizado en el análisis de mortalidad por cáncer de pulmón en la Ciudad de México. El conjunto de datos contiene concentraciones promedio anuales de múltiples contaminantes del aire en estaciones de monitoreo de la Zona Metropolitana de la Ciudad de México desde 1986 hasta 2022.

**Hallazgos Clave:**
- 722 registros totales que abarcan 37 años (1986-2022)
- 6 contaminantes disponibles: PM2.5, PM10, O3, NO2, SO2, CO
- 35 estaciones de monitoreo en toda el área metropolitana
- 14 de 16 alcaldías de la CDMX tienen datos de contaminación
- 2 alcaldías faltantes: La Magdalena Contreras y Tláhuac (sin estaciones de monitoreo)
- 100% de completitud de datos de contaminantes - sin valores faltantes para ningún contaminante
- 12 municipios no pertenecientes a la CDMX incluidos (Estado de México)

| Métrica | Valor |
| :--- | :--- |
| Registros totales | 722 |
| Años cubiertos | 1986-2022 (37 años) |
| Estaciones de monitoreo | 35 |
| Alcaldías de CDMX cubiertas | 14/16 (87.5%) |
| Contaminantes disponibles | PM2.5, PM10, O3, NO2, SO2, CO |
| Tasa de datos faltantes de contaminantes | 0% |
| Tasa general de datos faltantes | 2.95% |

**Conclusiones Principales:**
1. Excelente calidad de datos: 100% de los valores de contaminantes están presentes sin datos faltantes
2. Cobertura temporal completa: 37 años consecutivos (1986-2022) sin interrupciones
3. Fuerte cobertura geográfica: 14 de 16 alcaldías de la CDMX tienen datos de monitoreo
4. Conjunto de datos limpio: Sin filas duplicadas, sin filas completamente vacías
5. Listo para análisis: Datos integrados exitosamente con tasas de mortalidad para 2004-2022

---

## 1. Fuente de Datos

### 1.1 Origen

Los datos de contaminación del aire se obtuvieron del repositorio Zenodo:

> Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.10894651

### 1.2 Información del Archivo

| Atributo | Valor |
| :--- | :--- |
| Nombre del archivo | `Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv` |
| Ubicación del archivo | `data/raw/pollution/` |
| Tamaño del archivo | ~0.1 MB |
| Codificación | UTF-8 |
| Delimitador | Coma (,) |
| Forma | (722, 18) |

### 1.3 Formato de Datos

Concentraciones promedio anuales de contaminantes agregadas por alcaldía/municipio.

### 1.4 Descripciones de Columnas

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `clave` | Cadena | Identificador geográfico |
| `alcaldía o municipio` | Cadena | Nombre de alcaldía o municipio (original) |
| `entidad` | Cadena | Estado (Ciudad de México o México) |
| `station` | Cadena | Código de estación de monitoreo |
| `year` | Entero | Año de medición |
| `nombre` | Cadena | Nombre de la estación de monitoreo |
| `latitud` | Flotante | Latitud en grados decimales |
| `longitud` | Flotante | Longitud en grados decimales |
| `altitud` | Flotante | Altitud en metros |
| `co` | Flotante | Monóxido de carbono (ppm) |
| `no` | Flotante | Óxido nítrico (ppb) |
| `no2` | Flotante | Dióxido de nitrógeno (ppb) |
| `nox` | Flotante | Óxidos de nitrógeno (ppb) |
| `o3` | Flotante | Ozono (ppb) |
| `pm10` | Flotante | Partículas PM10 (μg/m³) |
| `pm25` | Flotante | Partículas PM2.5 (μg/m³) |
| `pmco` | Flotante | PM-grueso (μg/m³) |
| `so2` | Flotante | Dióxido de azufre (ppb) |

---

## 2. Metodología de Validación

### 2.1 Marco de Validación

La validación se realizó utilizando un script Python dedicado que ejecuta cinco categorías de verificaciones:

| Categoría | Descripción | Criterio de Aprobación |
| :--- | :--- | :--- |
| Estructura del Archivo | Conteo de registros, columnas, tipos de datos | Todas las columnas esperadas presentes |
| Cobertura Temporal | Rango de años, interrupciones, registros por año | Sin años faltantes en la serie |
| Cobertura Geográfica | Identificación y mapeo de alcaldías | ≥80% de alcaldías cubiertas |
| Valores de Contaminantes | Rango, media, faltantes, negativos | <5% faltantes, rangos plausibles |
| Calidad de Datos | Duplicados, filas vacías, tasa de faltantes | Sin duplicados, <5% faltantes |

### 2.2 Estandarización de Nombres de Alcaldías

El conjunto de datos contiene nombres originales con acentos, caracteres especiales y variaciones. Una función de mapeo estandariza los nombres para que coincidan con los conjuntos de datos armonizados de población y mortalidad.

**Transformaciones aplicadas:**
- Eliminar acentos (Á → A, é → e, í → i, ó → o, ú → u)
- Convertir a ASCII
- Manejar variaciones comunes y abreviaturas

**Ejemplos de mapeo:**

| Original | Mapeado |
| :--- | :--- |
| 'Álvaro Obregón' | 'Alvaro Obregon' |
| 'Benito Juárez' | 'Benito Juarez' |
| 'Coyoacán' | 'Coyoacan' |
| 'Cuauhtémoc' | 'Cuauhtemoc' |
| 'Gustavo A. Madero' | 'Gustavo A. Madero' |
| 'Venustiano Carranza' | 'Venustiano Carranza' |
| 'Xochimilco' | 'Xochimilco' |

### 2.3 Ejecución de la Validación

| Atributo | Valor |
| :--- | :--- |
| Ubicación del script | `src/data_validation.py` |
| Comando de ejecución | `python -m src.run_analysis --phase 1` |
| Fecha de ejecución | 2026-04-21 |
| Registro de salida | `logs/pollution_validation_AAAAMMDD_HHMMSS.json` |

---

## 3. Resultados de la Validación

### 3.1 Validación de Estructura del Archivo

| Atributo | Valor | Estado |
| :--- | :--- | :--- |
| Registros totales | 722 | ✅ APROBADO |
| Columnas totales | 18 | ✅ APROBADO |
| Estaciones de monitoreo | 35 | ✅ APROBADO |
| Contaminantes encontrados | PM2.5, PM10, O3, NO2, SO2, CO | ✅ APROBADO |

**Lista Completa de Columnas:**

| Índice | Nombre de Columna | Tipo de Dato | Conteo No Nulo |
| :--- | :--- | :--- | :--- |
| 0 | `clave` | objeto | 722 |
| 1 | `alcaldía o municipio` | objeto | 722 |
| 2 | `entidad` | objeto | 722 |
| 3 | `station` | objeto | 722 |
| 4 | `year` | int64 | 722 |
| 5 | `nombre` | objeto | 722 |
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

### 3.2 Validación de Cobertura Temporal

| Atributo | Valor | Estado |
| :--- | :--- | :--- |
| Año mínimo | 1986 | ✅ APROBADO |
| Año máximo | 2022 | ✅ APROBADO |
| Años totales | 37 | ✅ APROBADO |
| Años faltantes | 0 | ✅ APROBADO |
| Completitud del rango de años | 100% | ✅ APROBADO |

**Tendencia de Registros por Año:**

| Período | Promedio de Registros/Año | Estado de la Red |
| :--- | :--- | :--- |
| 1986-1993 | 10 | Despliegue inicial |
| 1994-2003 | 16 | Primera expansión |
| 2004-2010 | 18 | Crecimiento continuo |
| 2011-2022 | 30 | Cobertura operativa completa |

**Conteos Completos de Registros Anuales:**

| Año | Registros | Año | Registros | Año | Registros | Año | Registros |
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

### 3.3 Validación de Cobertura Geográfica

#### 3.3.1 Resultados Generales del Mapeo

| Categoría | Conteo | Porcentaje |
| :--- | :--- | :--- |
| Nombres geográficos únicos totales | 26 | 100% |
| Alcaldías de CDMX mapeadas exitosamente | 14 | 53.8% |
| Municipios no pertenecientes a CDMX | 12 | 46.2% |

#### 3.3.2 Alcaldías de CDMX con Datos de Contaminación (14 de 16)

| Alcaldía | Registros | Primer Año | Último Año | Estado de Cobertura |
| :--- | :--- | :--- | :--- | :--- |
| Cuajimalpa de Morelos | 40 | 1994 | 2022 | Completa (29 años) |
| Iztapalapa | 40 | 1994 | 2022 | Completa (29 años) |
| Venustiano Carranza | 37 | 2000 | 2022 | Completa (23 años) |
| Álvaro Obregón | 37 | 2000 | 2022 | Completa (23 años) |
| Xochimilco | 29 | 2007 | 2022 | Parcial (16 años) |
| Benito Juárez | 27 | 2011 | 2022 | Parcial (12 años) |
| Azcapotzalco | 20 | 2016 | 2022 | Parcial (7 años) |
| Coyoacán | 20 | 2016 | 2022 | Parcial (7 años) |
| Tlalpan | 16 | 2007 | 2022 | Parcial (16 años) |
| Iztacalco | 16 | 2007 | 2022 | Parcial (16 años) |
| Cuauhtémoc | 11 | 2012 | 2022 | Limitada (11 años) |
| Gustavo A. Madero | 9 | 2016 | 2022 | Limitada (7 años) |
| Miguel Hidalgo | 8 | 2016 | 2022 | Limitada (7 años) |
| Milpa Alta | 7 | 2016 | 2022 | Limitada (7 años) |

#### 3.3.3 Alcaldías de CDMX Sin Datos de Contaminación (2 de 16)

| Alcaldía | Razón de Ausencia |
| :--- | :--- |
| La Magdalena Contreras | Sin estación de monitoreo de calidad del aire en el conjunto de datos |
| Tláhuac | Sin estación de monitoreo de calidad del aire en el conjunto de datos |

**Nota:** Ambas alcaldías faltantes son predominantemente residenciales y semi-rurales con menor densidad poblacional y actividad industrial.

#### 3.3.4 Municipios No Pertenecientes a CDMX Presentes (Filtrados Durante la Integración)

| Municipio | Estado |
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

Estos municipios son parte de la Zona Metropolitana de la Ciudad de México pero fueron excluidos del análisis específico de la CDMX.

#### 3.3.5 Tabla Completa de Mapeo de Nombres de Alcaldías

| Nombre Original | Nombre Mapeado | Estado |
| :--- | :--- | :--- |
| Acolman | Ninguno | No CDMX |
| Atizapán de Zaragoza | Ninguno | No CDMX |
| Azcapotzalco | Azcapotzalco | ✅ MAPEADO |
| Benito Juárez | Benito Juarez | ✅ MAPEADO |
| Chalco | Ninguno | No CDMX |
| Coacalco de Berriozábal | Ninguno | No CDMX |
| Coyoacán | Coyoacan | ✅ MAPEADO |
| Cuajimalpa de Morelos | Cuajimalpa de Morelos | ✅ MAPEADO |
| Cuauhtémoc | Cuauhtemoc | ✅ MAPEADO |
| Cuautitlán Izcalli | Ninguno | No CDMX |
| Ecatepec de Morelos | Ninguno | No CDMX |
| Gustavo A. Madero | Gustavo A. Madero | ✅ MAPEADO |
| Iztacalco | Iztacalco | ✅ MAPEADO |
| Iztapalapa | Iztapalapa | ✅ MAPEADO |
| Miguel Hidalgo | Miguel Hidalgo | ✅ MAPEADO |
| Milpa Alta | Milpa Alta | ✅ MAPEADO |
| Naucalpan de Juárez | Ninguno | No CDMX |
| Nezahualcóyotl | Ninguno | No CDMX |
| Ocoyoacac | Ninguno | No CDMX |
| Texcoco | Ninguno | No CDMX |
| Tlalnepantla de Baz | Ninguno | No CDMX |
| Tlalpan | Tlalpan | ✅ MAPEADO |
| Tultitlán | Ninguno | No CDMX |
| Venustiano Carranza | Venustiano Carranza | ✅ MAPEADO |
| Xochimilco | Xochimilco | ✅ MAPEADO |
| Álvaro Obregón | Alvaro Obregon | ✅ MAPEADO |

### 3.4 Validación de Valores de Contaminantes

#### 3.4.1 Estadísticas Descriptivas para Todos los Contaminantes

| Contaminante | Unidad | Conteo | Faltantes | Media | Desv Est | Mín | Máx | Negativos |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PM2.5 | μg/m³ | 722 | 0 | 22.38 | 4.29 | 11.84 | 51.87 | 0 |
| PM10 | μg/m³ | 722 | 0 | 45.02 | 9.98 | 19.46 | 108.97 | 0 |
| O3 | ppb | 722 | 0 | 21.70 | 5.01 | 9.16 | 42.37 | 0 |
| NO2 | ppb | 722 | 0 | 24.98 | 5.14 | 6.21 | 46.68 | 0 |
| SO2 | ppb | 722 | 0 | 8.31 | 8.26 | 0.44 | 70.11 | 0 |
| CO | ppm | 722 | 0 | 3.28 | 3.06 | -0.17 | 19.72 | 1 |

**Nota:** El valor negativo único de CO (-0.17 ppm) es un artefacto de redondeo cercano a cero y se trató como 0 en el conjunto de datos final.

#### 3.4.2 Evaluación de Plausibilidad Específica por Contaminante

**PM2.5 (Partículas Finas):**
- Rango: 11.84 - 51.87 μg/m³
- Plausibilidad: Excelente - Valores consistentes con los informes de calidad del aire de la Ciudad de México
- Valores altos: >45 μg/m³ representan días de alta contaminación (inversiones térmicas)
- Media: 22.38 μg/m³ - Por encima de la guía de la OMS (5 μg/m³ anual)
- **Estado: ✅ VÁLIDO**

**PM10 (Partículas Gruesas):**
- Rango: 19.46 - 108.97 μg/m³
- Plausibilidad: Excelente - Rango esperado para área urbana con polvo resuspendido
- Valores altos: >100 μg/m³ ocurren durante tormentas de polvo y eventos de inversión
- Media: 45.02 μg/m³ - Por encima de la guía de la OMS (15 μg/m³ anual)
- **Estado: ✅ VÁLIDO**

**O3 (Ozono):**
- Rango: 9.16 - 42.37 ppb
- Plausibilidad: Excelente - Típico para smog fotoquímico en ciudades de gran altitud
- Formación: Contaminante secundario a partir de NOx y COV con luz solar
- Media: 21.70 ppb - Dentro del rango urbano esperado
- **Estado: ✅ VÁLIDO**

**NO2 (Dióxido de Nitrógeno):**
- Rango: 6.21 - 46.68 ppb
- Plausibilidad: Excelente - Contaminante relacionado con el tráfico
- Fuentes: Emisiones vehiculares, procesos de combustión
- Media: 24.98 ppb - Consistente con niveles de tráfico metropolitano
- **Estado: ✅ VÁLIDO**

**SO2 (Dióxido de Azufre):**
- Rango: 0.44 - 70.11 ppb
- Plausibilidad: Excelente - Fuentes industriales y volcánicas
- Picos: Valores altos ocasionales probablemente de emisiones industriales
- Media: 8.31 ppb - Generalmente línea base baja con picos episódicos
- **Estado: ✅ VÁLIDO**

**CO (Monóxido de Carbono):**
- Rango: -0.17 - 19.72 ppm
- Plausibilidad: Buena - Emisiones vehiculares, mejorado con convertidores catalíticos
- Valor negativo: Un solo valor de -0.17 ppm (artefacto de redondeo cercano a cero)
- Media: 3.28 ppm - Tendencia decreciente con modernización vehicular
- **Estado: ✅ VÁLIDO (1 artefacto aceptable)**

### 3.5 Validación de Calidad de Datos

| Métrica | Valor | Estado |
| :--- | :--- | :--- |
| Filas duplicadas | 0 | ✅ APROBADO |
| Filas completamente vacías | 0 | ✅ APROBADO |
| Tasa general de faltantes | 2.95% | ✅ APROBADO |
| Tasa de faltantes de contaminantes | 0% | ✅ APROBADO |
| Datos geográficos faltantes | 0% | ✅ APROBADO |
| Datos temporales faltantes | 0% | ✅ APROBADO |

**Valores Faltantes por Columna:**

| Columna | Conteo Faltante | Porcentaje Faltante | Notas |
| :--- | :--- | :--- | :--- |
| `alcaldia_mapped` | 405 | 56.1% | Municipios no CDMX |
| Todas las columnas de contaminantes | 0 | 0% | Datos completos |
| Todas las columnas geográficas | 0 | 0% | Datos completos |
| Todas las columnas temporales | 0 | 0% | Datos completos |

---

## 4. Resumen de Hallazgos Clave

### 4.1 Fortalezas

| Aspecto | Hallazgo | Implicación |
| :--- | :--- | :--- |
| Completitud de Datos | 100% de valores de contaminantes presentes | No se requiere imputación |
| Cobertura Temporal | 37 años consecutivos (1986-2022) | Análisis robusto de series temporales |
| Variedad de Contaminantes | 6 contaminantes criterio disponibles | Modelos multi-contaminantes posibles |
| Densidad de Estaciones | 35 estaciones de monitoreo | Buena representación espacial |
| Calidad de Datos | Sin duplicados, sin filas vacías | Conjunto de datos limpio |
| Cobertura Geográfica | 14/16 alcaldías de CDMX (87.5%) | Suficiente para inferencia |

### 4.2 Limitaciones

| Aspecto | Hallazgo | Mitigación |
| :--- | :--- | :--- |
| Alcaldías Faltantes | La Magdalena Contreras y Tláhuac carecen de datos | Documentar como limitación |
| Cobertura Desigual | Registros por alcaldía varían de 7 a 40 | Usar modelos de efectos fijos |
| Municipios No CDMX | 12 municipios del Estado de México presentes | Filtrados durante la integración |
| Primeros Años Escasos | 1986-1993 tienen registros limitados | Enfocar en 2004-2022 |
| Artefacto Único de CO | Un valor negativo de CO (-0.17 ppm) | Tratar como cero |

### 4.3 Evaluación de Cobertura Geográfica

**Cobertura por Población (estimaciones 2020):**

| Categoría | Alcaldías | Población | % del Total CDMX |
| :--- | :--- | :--- | :--- |
| Con datos de contaminación | 14 | ~8.2 millones | ~89% |
| Sin datos de contaminación | 2 | ~0.4 millones | ~11% |

Las 14 alcaldías con datos de contaminación representan aproximadamente el 89% de la población total de la Ciudad de México.

### 4.4 Cobertura Temporal por Alcaldía (Período de Análisis 2004-2022)

| Alcaldía | Años en 2004-2022 | Completo | Inclusión en Análisis |
| :--- | :--- | :--- | :--- |
| Cuajimalpa de Morelos | 19 | Sí | Panel completo |
| Iztapalapa | 19 | Sí | Panel completo |
| Venustiano Carranza | 19 | Sí | Panel completo |
| Álvaro Obregón | 19 | Sí | Panel completo |
| Xochimilco | 16 | Parcial | Incluido |
| Tlalpan | 16 | Parcial | Incluido |
| Iztacalco | 16 | Parcial | Incluido |
| Benito Juárez | 12 | Parcial | Incluido |
| Cuauhtémoc | 11 | Parcial | Incluido |
| Azcapotzalco | 7 | Parcial | Incluido |
| Coyoacán | 7 | Parcial | Incluido |
| Gustavo A. Madero | 7 | Parcial | Incluido |
| Miguel Hidalgo | 7 | Parcial | Incluido |
| Milpa Alta | 7 | Parcial | Incluido |

---

## 5. Integración con Datos de Mortalidad

### 5.1 Resumen del Proceso de Integración

| Paso | Acción | Resultado |
| :--- | :--- | :--- |
| 1 | Cargar datos de contaminación | 722 registros cargados |
| 2 | Mapear nombres de alcaldías | 14 alcaldías de CDMX identificadas |
| 3 | Filtrar solo CDMX | 317 registros retenidos |
| 4 | Agregar por alcaldía-año | Media entre estaciones por alcaldía-año |
| 5 | Unir con tasas de mortalidad | Unión izquierda por alcaldía y año |
| 6 | Filtrar al período de análisis | 2004-2022 retenido |

### 5.2 Características del Conjunto de Datos Analítico Final

| Atributo | Valor |
| :--- | :--- |
| Años de análisis | 2004-2022 (19 años) |
| Alcaldías con datos de contaminación | 14 |
| Observaciones totales (Ambos sexos) | 266 |
| Observaciones totales (Todos los sexos) | 798 |
| Variable de exposición primaria | PM2.5 |
| Variable de resultado primaria | Tasa de mortalidad estandarizada por edad |

### 5.3 Variables Listas para Análisis

| Variable | Tipo | Media | Desv Est | Mín | Máx |
| :--- | :--- | :--- | :--- | :--- | :--- |
| pm25 | Continua | 21.10 | 2.78 | 15.12 | 29.04 |
| pm10 | Continua | 40.72 | 5.96 | 26.13 | 59.77 |
| o3 | Continua | 21.35 | 5.66 | 9.16 | 40.70 |
| no2 | Continua | 25.17 | 5.27 | 6.21 | 37.50 |
| so2 | Continua | 6.96 | 4.84 | 0.44 | 28.68 |
| co | Continua | 2.83 | 2.31 | 0.00 | 9.67 |
| crude_rate | Continua | 7.15 | 2.30 | 0.66 | 14.24 |
| age_standardized_rate | Continua | 14.03 | 4.22 | 1.52 | 28.67 |

---

## 6. Conclusiones y Recomendaciones

### 6.1 Evaluación General de Calidad de Datos

| Aspecto | Calificación | Justificación |
| :--- | :--- | :--- |
| Completitud | A+ | 100% de valores de contaminantes presentes; sin datos faltantes |
| Cobertura Temporal | A+ | 37 años consecutivos; sin interrupciones |
| Cobertura Geográfica | A- | 14/16 alcaldías (87.5%); 2 faltantes |
| Consistencia | A | Estructura limpia; formato consistente |
| Exactitud | A | Rangos de valores plausibles; artefactos mínimos |
| Usabilidad | A | Listo para análisis estadístico |
| **GENERAL** | **A** | **Excelente calidad; adecuado para publicación** |

### 6.2 Recomendaciones

1. **PROCEDER CON 14 ALCALDÍAS** para el análisis primario. La cobertura del 87.5% es suficiente para inferencia estadística robusta y hallazgos generalizables.

2. **DOCUMENTAR ALCALDÍAS FALTANTES** como limitación del estudio en publicaciones. Señalar que La Magdalena Contreras y Tláhuac son áreas predominantemente residenciales y semi-rurales con menor densidad poblacional.

3. **ENFOCAR EL ANÁLISIS EN 2004-2022** cuando la red de monitoreo estaba completamente establecida y los datos de mortalidad son más confiables.

4. **CONSIDERAR ANÁLISIS DE SENSIBILIDAD** excluyendo alcaldías con registros limitados (menos de 15 observaciones) para asegurar que los hallazgos no estén impulsados por datos escasos.

5. **SEÑALAR QUE LOS MUNICIPIOS NO PERTENECIENTES A CDMX** están correctamente excluidos; el conjunto de datos analítico está apropiadamente restringido a la Ciudad de México propiamente dicha.

6. **UTILIZAR MODELOS MULTI-CONTAMINANTES** dada la disponibilidad de 6 contaminantes, pero tener en cuenta la colinealidad entre contaminantes relacionados con el tráfico (NO2, CO).

### 6.3 Poder Estadístico Esperado

| Tipo de Modelo | Observaciones | Conglomerados | Evaluación de Poder |
| :--- | :--- | :--- | :--- |
| MCO Agrupado | 266 | N/A | Adecuado |
| Efectos Fijos por Alcaldía | 266 | 14 | Bueno |
| Efectos Fijos Bidireccionales | 266 | 14 alcaldías × 19 años | Bueno |
| Específico por Sexo (Hombre) | 266 | 14 | Bueno |
| Específico por Sexo (Mujer) | 266 | 14 | Bueno |

---

## 7. Apéndice

### 7.1 Información del Script de Validación

- **Ubicación del script:** `src/data_validation.py`
- **Registro de salida:** `logs/pollution_validation_AAAAMMDD_HHMMSS.json`
- **Comando de ejecución:** `python -m src.run_analysis --phase 1`

### 7.2 Resumen de Cobertura de Alcaldías

**Alcaldías de CDMX (16 total):**

**PRESENTES (14):**
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

**FALTANTES (2):**
- La Magdalena Contreras (sin estación de monitoreo)
- Tláhuac (sin estación de monitoreo)

### 7.3 Tabla Resumen de Contaminantes

| Contaminante | Unidad | Conteo | Media | Desv Est | Mín | Máx | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PM2.5 | μg/m³ | 722 | 22.38 | 4.29 | 11.84 | 51.87 | ✅ VÁLIDO |
| PM10 | μg/m³ | 722 | 45.02 | 9.98 | 19.46 | 108.97 | ✅ VÁLIDO |
| O3 | ppb | 722 | 21.70 | 5.01 | 9.16 | 42.37 | ✅ VÁLIDO |
| NO2 | ppb | 722 | 24.98 | 5.14 | 6.21 | 46.68 | ✅ VÁLIDO |
| SO2 | ppb | 722 | 8.31 | 8.26 | 0.44 | 70.11 | ✅ VÁLIDO |
| CO | ppm | 722 | 3.28 | 3.06 | -0.17 | 19.72 | ✅ VÁLIDO |

---

*Fin del Informe*
