# Metodología: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México

**Proyecto 1: Proyectos de Análisis de Datos Públicos de Alto Impacto para México**

**Autor:** Arlex Marín  
**Fecha:** 21 de abril de 2026  
**Versión:** 2.0

---

## 1. Diseño del Estudio

Este estudio emplea un **diseño de estudio de panel** que analiza 14 alcaldías de la Ciudad de México durante un período de 19 años (2004-2022). La exposición primaria es la concentración promedio anual de PM₂.₅, y el resultado primario es la tasa de mortalidad por cáncer de pulmón estandarizada por edad (códigos CIE-10 C33-C34).

### 1.1 Preguntas de Investigación
1. ¿Existe una asociación significativa entre la exposición a largo plazo a PM₂.₅ y la mortalidad por cáncer de pulmón en las alcaldías de la Ciudad de México?
2. ¿Qué contaminante del aire muestra la correlación más fuerte con la mortalidad por cáncer de pulmón?
3. ¿Existen diferencias específicas por sexo en la asociación contaminación-mortalidad?
4. ¿Cómo varían espacialmente las tasas de mortalidad y las concentraciones de contaminantes entre las alcaldías?

### 1.2 Unidad de Análisis
La unidad de análisis es el **año-alcaldía**, con observaciones separadas para hombres, mujeres y ambos sexos combinados.

---

## 2. Fuentes de Datos

### 2.1 Datos de Población
Las estimaciones de población se derivaron de cuatro censos mexicanos (2000, 2005, 2010, 2020) obtenidos del INEGI a través de la herramienta SCITEL. Las estimaciones anuales de población para 2000-2022 se crearon utilizando interpolación lineal por tramos entre los años censales. Los grupos de edad se armonizaron en seis categorías (0-4, 5-14, 15-17, 18-24, 25-59, 60+) para garantizar la comparabilidad en todos los años censales.

**Fuente:** INEGI - Instituto Nacional de Estadística y Geografía  
**Archivos:** RESLOC2000, RESLOC2005, RESLOC2010, ITER2020 (solo CDMX)

### 2.2 Datos de Mortalidad
Los registros de mortalidad a nivel individual para 2000-2023 se obtuvieron del conjunto de datos de defunciones del repositorio en Zenodo (Crespo-Sanchez, Melesio, 2024). Las defunciones por cáncer de pulmón se identificaron utilizando los códigos CIE-10 C33 (tumor maligno de la tráquea) y C34 (tumor maligno de los bronquios y del pulmón). Las defunciones se agregaron por alcaldía, año, grupo de edad armonizado y sexo.

**Fuente:** Zenodo - Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico  
**Archivos:** deaths_registry.rar

### 2.3 Datos de Contaminación del Aire
Las concentraciones promedio anuales de PM₂.₅, PM₁₀, O₃, NO₂, SO₂ y CO para 1986-2022 se obtuvieron del conjunto de datos de contaminación del aire del repositorio en Zenodo (Crespo-Sanchez, Melesio, 2024). Los datos se agregaron por alcaldía y año, calculando el promedio de todas las estaciones de monitoreo dentro de cada alcaldía.

**Fuente:** Zenodo - Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico  
**Archivo:** Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv

### 2.4 Datos Geoespaciales
Los archivos shapefile de los límites de las alcaldías se obtuvieron del Marco Geoestadístico 2025 del INEGI.

**Fuente:** INEGI - Marco Geoestadístico 2025  
**Archivo:** 09_ciudaddemexico/conjunto_de_datos/09mun.shp

---

## 3. Estandarización por Edad

### 3.1 Método
Las tasas de mortalidad estandarizadas por edad se calcularon utilizando el **método de estandarización directa** con la Población Estándar Mundial de la OMS como referencia. La fórmula utilizada fue:

TEE = Σ (w_i × r_i) × 100,000

donde:
- w_i = ponderación de la población estándar de la OMS para el grupo de edad i
- r_i = tasa de mortalidad específica por edad para el grupo de edad i

### 3.2 Grupos de Edad Armonizados
| Grupo de Edad | Rango de Edad | Ponderación OMS |
| :--- | :--- | :--- |
| 0-4 | 0 a 4 años | 0.0886 |
| 5-14 | 5 a 14 años | 0.1729 |
| 15-17 | 15 a 17 años | 0.0254 |
| 18-24 | 18 a 24 años | 0.0702 |
| 25-59 | 25 a 59 años | 0.5167 |
| 60+ | 60 años y más | 0.1262 |

---

## 4. Análisis Estadístico

### 4.1 Estadística Descriptiva
Se calcularon estadísticas descriptivas (media, desviación estándar, mínimo, máximo) para todos los contaminantes y las tasas de mortalidad en las 14 alcaldías con datos de monitoreo.

### 4.2 Análisis de Correlación
Se calcularon los coeficientes de correlación de Pearson y Spearman entre cada contaminante y las tasas de mortalidad tanto crudas como estandarizadas por edad. La significancia estadística se evaluó con α = 0.05.

### 4.3 Modelos de Regresión de Panel
Se estimaron cuatro especificaciones de modelo para evaluar la asociación entre PM₂.₅ y la mortalidad por cáncer de pulmón:

#### Modelo 1: MCO Agrupado

Tasa_mortalidad_it = α + β × PM2.5_it + ε_it

Regresión básica por mínimos cuadrados ordinarios que ignora la estructura de panel.

#### Modelo 2: Efectos Fijos por Alcaldía

Tasa_mortalidad_it = α_i + β × PM2.5_it + ε_it

Controla por características no observadas de las alcaldías que son invariantes en el tiempo (por ejemplo, estado de salud basal, factores socioeconómicos).

#### Modelo 3: Efectos Fijos Bidireccionales

Tasa_mortalidad_it = α_i + γ_t + β × PM2.5_it + ε_it

Controla tanto por efectos fijos de alcaldía como por efectos fijos de año (por ejemplo, tendencias seculares, cambios en políticas).

#### Modelo 4: Modelo Log-Lineal

ln(Tasa_mortalidad_it) = α_i + γ_t + β × PM2.5_it + ε_it

Transformación logarítmica natural de la variable de resultado; el coeficiente representa el cambio porcentual aproximado.

### 4.4 Errores Estándar
Todos los modelos utilizaron **errores estándar robustos agrupados** a nivel de alcaldía para considerar la correlación serial dentro de cada alcaldía.

### 4.5 Análisis Específico por Sexo
Se estimaron modelos separados de efectos fijos bidireccionales para la mortalidad masculina y femenina con el fin de evaluar las asociaciones específicas por sexo entre PM₂.₅ y la mortalidad por cáncer de pulmón.

### 4.6 Software
Todos los análisis se realizaron utilizando Python 3.11 con las siguientes bibliotecas:
- pandas 2.0.3 (manipulación de datos)
- statsmodels 0.14.0 (regresión de panel)
- scipy 1.10.1 (análisis de correlación)
- geopandas 0.14.0 (análisis espacial)
- matplotlib 3.7.1 / seaborn 0.12.2 (visualización)
- plotly 5.14.1 (mapas interactivos)

---

## 5. Análisis Geoespacial

### 5.1 Mapas de Coropletas
Se crearon mapas de coropletas utilizando los archivos shapefile del Marco Geoestadístico 2025 del INEGI para visualizar:
- Tasas de mortalidad por cáncer de pulmón estandarizadas por edad por alcaldía (2010 y 2020)
- Concentraciones de PM₂.₅ por alcaldía (2020)

### 5.2 Mapa de Coropletas Bivariado
Se creó un mapa de coropletas bivariado de 3×3 para 2020, clasificando de manera cruzada las alcaldías por:
- Terciles de concentración de PM₂.₅ (Bajo, Medio, Alto)
- Terciles de tasa de mortalidad estandarizada por edad (Bajo, Medio, Alto)

Esta visualización permite la evaluación simultánea de los patrones espaciales de exposición y resultado.

### 5.3 Mapas Interactivos
Se generaron mapas interactivos en HTML utilizando Plotly para el análisis exploratorio y la difusión de resultados.

---

## 6. Análisis de Sensibilidad

### 6.1 Modelos con Múltiples Contaminantes
Se estimaron modelos adicionales que incluyen múltiples contaminantes (PM₂.₅, NO₂, O₃) para evaluar el efecto independiente de PM₂.₅ controlando por co-contaminantes.

### 6.2 Análisis de Rezago
Se probaron variables de contaminación con rezago de uno y dos años para considerar la latencia potencial entre la exposición y la mortalidad.

---

## 7. Limitaciones

| Limitación | Mitigación |
| :--- | :--- |
| Diseño de estudio ecológico (exposición a nivel de alcaldía) | Inherente a los datos disponibles; los hallazgos aplican a nivel poblacional |
| Dos alcaldías carecen de monitoreo de contaminación | Documentado como limitación; análisis de sensibilidad excluyéndolas |
| Cobertura temporal desigual entre alcaldías | Los modelos de efectos fijos bidireccionales contemplan paneles no balanceados |
| Posible confusión por prevalencia de tabaquismo | Los efectos fijos por alcaldía controlan diferencias invariantes en el tiempo |
| Latencia entre exposición y resultado | Análisis de rezago realizado como verificación de sensibilidad |

---

## 8. Reproducibilidad

### 8.1 Disponibilidad del Código
Todo el código de análisis está disponible en el directorio `src/` del repositorio del proyecto. La tubería completa se puede ejecutar usando:

```bash
conda env create -f environment.yml
conda activate mx-public-health-analysis
python -m src.run_analysis
```

### 8.2 Disponibilidad de los Datos

Datos censales: Disponibles públicamente en INEGI

Datos de contaminación y mortalidad: Disponibles en Zenodo (DOI: 10.5281/zenodo.10894651)

Archivos shapefile: Disponibles públicamente en INEGI

---

## 9. Referencias

Ahmad, O. B., Boschi-Pinto, C., Lopez, A. D., Murray, C. J., Lozano, R., & Inoue, M. (2001). Age standardization of rates: A new WHO standard. World Health Organization.

INEGI. (2000). XII Censo General de Población y Vivienda 2000.

INEGI. (2005). II Conteo de Población y Vivienda 2005.

INEGI. (2010). Censo de Población y Vivienda 2010.

INEGI. (2020). Censo de Población y Vivienda 2020.

Crespo-Sanchez, Melesio. (2024). Air Pollution and Cancer Mortality Dataset - Mexico City. Zenodo. https://doi.org/10.5281/zenodo.10894651

---

*Fin del Documento de Metodología*
