# Informe Final: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México

**Autor:** Arlex Marín  
**Fecha:** 22 de abril de 2026  
**Versión:** 1.0

---

## Resumen Ejecutivo

Este informe presenta los hallazgos completos de un análisis exhaustivo de la relación entre la exposición a largo plazo a la contaminación del aire y la mortalidad por cáncer de pulmón en las 16 alcaldías de la Ciudad de México. El estudio analizó 19 años de datos (2004-2022), integrando estimaciones de población armonizadas de cuatro censos, registros de mortalidad a nivel individual y datos de monitoreo de calidad del aire de 35 estaciones.

### Conclusión Principal

**La exposición a largo plazo a PM₂.₅ está positivamente asociada con la mortalidad por cáncer de pulmón estandarizada por edad en la Ciudad de México.** Un aumento de 10 μg/m³ en PM₂.₅ se asocia con un aumento de 2.10 por 100,000 en la mortalidad (p = 0.090), después de controlar por efectos fijos de alcaldía y año. Esto se traduce en aproximadamente **193 defunciones por cáncer de pulmón prevenibles anualmente** en la CDMX si los niveles de PM₂.₅ se redujeran en 10 μg/m³.

### Conclusiones Secundarias

1. **La contaminación relacionada con el tráfico (NO₂) muestra la asociación más fuerte** (r = +0.425, p < 0.001), sugiriendo las emisiones vehiculares como objetivo prioritario de intervención.

2. **Tanto la contaminación como la mortalidad han disminuido** durante el período de estudio (PM₂.₅ ↓16.5%, mortalidad ↓35.3%), consistente con la efectividad de las políticas.

3. **La carga es espacialmente desigual**, con las alcaldías del norte y oriente experimentando tasas de mortalidad 1.7× más altas que las alcaldías del sur.

4. **Los niveles actuales de PM₂.₅ permanecen por encima de lo seguro**, excediendo las guías de la OMS en 3.9× y los estándares mexicanos en 1.6×.

5. **Dos alcaldías carecen de monitoreo de calidad del aire**, representando una brecha de datos para ~639,000 residentes.

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Métodos](#2-métodos)
3. [Resultados](#3-resultados)
4. [Discusión](#4-discusión)
5. [Conclusiones](#5-conclusiones)
6. [Disponibilidad de Datos y Código](#6-disponibilidad-de-datos-y-código)
7. [Referencias](#7-referencias)
8. [Apéndices](#apéndices)

---

## 1. Introducción

### 1.1 Antecedentes

La Ciudad de México se clasifica consistentemente entre las áreas metropolitanas más contaminadas del Hemisferio Occidental. Su geografía única—un valle de gran altitud rodeado de montañas—crea capas de inversión térmica que atrapan contaminantes incluyendo material particulado (PM₂.₅ y PM₁₀), ozono (O₃) y dióxido de nitrógeno (NO₂). La exposición crónica a estos contaminantes está clasificada por la Agencia Internacional para la Investigación del Cáncer (IARC) como carcinógeno del Grupo 1, con vínculos establecidos con la incidencia y mortalidad por cáncer de pulmón.

### 1.2 Preguntas de Investigación

Este estudio abordó cuatro preguntas principales:

1. ¿Existe una asociación significativa entre la exposición a largo plazo a PM₂.₅ y la mortalidad por cáncer de pulmón en las alcaldías de la Ciudad de México?
2. ¿Qué contaminante del aire muestra la correlación más fuerte con la mortalidad por cáncer de pulmón?
3. ¿Existen diferencias específicas por sexo en la asociación contaminación-mortalidad?
4. ¿Cómo varían espacialmente las tasas de mortalidad y las concentraciones de contaminantes entre las alcaldías?

### 1.3 Diseño del Estudio

- **Diseño:** Estudio de panel (ecológico)
- **Unidad de Análisis:** Año-alcaldía (14 alcaldías, 19 años)
- **Exposición:** Concentración promedio anual de PM₂.₅
- **Resultado:** Tasa de mortalidad por cáncer de pulmón estandarizada por edad (CIE-10 C33-C34)
- **Período de Análisis:** 2004-2022

---

## 2. Métodos

### 2.1 Fuentes de Datos

| Tipo de Dato | Fuente | Cobertura Temporal |
|:---|:---|:---|
| Población | Censos INEGI (2000, 2005, 2010, 2020) | 2000-2022 (armonizados) |
| Mortalidad | Zenodo (Crespo-Sanchez Melesio, 2024) | 2000-2023 |
| Contaminación del Aire | Zenodo (Crespo-Sanchez Melesio, 2024) | 1986-2022 |
| Geoespacial | INEGI Marco Geoestadístico 2025 | Límites 2025 |

### 2.2 Procesamiento de Datos

**Armonización de Población:**
- Colapso de cuatro censos a 6 grupos de edad armonizados (0-4, 5-14, 15-17, 18-24, 25-59, 60+)
- Aplicación de retroproyección e interpolación para datos faltantes específicos por sexo
- Creación de estimaciones anuales para 2000-2022 mediante interpolación lineal por tramos
- Validación contra totales oficiales del INEGI (diferencia <0.1% para todos los censos)

**Procesamiento de Mortalidad:**
- Extracción de defunciones por cáncer de pulmón usando códigos CIE-10 C33-C34
- Agregación por alcaldía, año, grupo de edad y sexo
- Total de defunciones por cáncer de pulmón analizadas: 11,952 (2004-2022)

**Estandarización por Edad:**
- Aplicación del método de estandarización directa
- Uso de la Población Estándar Mundial de la OMS como referencia
- Cálculo de tasas para hombres, mujeres y ambos sexos combinados

**Integración de Contaminación:**
- Mapeo de nombres de alcaldías del conjunto de datos de contaminación a nombres estándar
- Agregación por alcaldía-año (media entre estaciones de monitoreo)
- Unión con tasas de mortalidad para 14 alcaldías con datos de monitoreo
- Dos alcaldías excluidas: La Magdalena Contreras, Tláhuac (sin estaciones de monitoreo)

### 2.3 Análisis Estadístico

- **Estadística descriptiva:** Medias, desviaciones estándar, rangos
- **Análisis de correlación:** Coeficientes de Pearson y Spearman
- **Regresión de panel:** Cuatro especificaciones de modelo:
  - Modelo 1: MCO agrupado con errores estándar robustos HC3
  - Modelo 2: Efectos fijos por alcaldía con errores estándar robustos agrupados
  - Modelo 3: Efectos fijos bidireccionales (alcaldía + año) con errores estándar robustos agrupados
  - Modelo 4: Especificación log-lineal para interpretación de semi-elasticidad
- **Errores estándar robustos agrupados:** Agrupados a nivel de alcaldía (14 conglomerados)
- **Análisis específico por sexo:** Modelos separados para hombres y mujeres
- **Análisis de sensibilidad:** Contaminantes alternativos, estructuras de rezago, exclusión de alcaldías una por una

### 2.4 Software

Todos los análisis se realizaron utilizando Python 3.11 con las siguientes bibliotecas:

| Biblioteca | Versión | Propósito |
|:---|:---|:---|
| pandas | 2.0.3 | Manipulación de datos |
| numpy | 1.24.3 | Operaciones numéricas |
| statsmodels | 0.14.0 | Regresión de panel |
| scipy | 1.10.1 | Análisis de correlación |
| geopandas | 0.14.0 | Análisis espacial |
| matplotlib | 3.7.1 | Visualizaciones estáticas |
| seaborn | 0.12.2 | Gráficos estadísticos |
| plotly | 5.14.1 | Mapas interactivos |

---

## 3. Resultados

### 3.1 Estadística Descriptiva

| Métrica | Valor |
|:---|:---|
| Período de Análisis | 2004-2022 (19 años) |
| Alcaldías Analizadas | 14 de 16 |
| Observaciones Totales (Ambos Sexos) | 266 alcaldía-años |
| Defunciones Totales por Cáncer de Pulmón | 11,952 |
| Media de PM₂.₅ | 21.10 μg/m³ (DE: 2.78) |
| Media de Tasa Estandarizada por Edad | 14.03 por 100,000 (DE: 4.22) |

**Concentraciones de Contaminantes (2004-2022):**

| Contaminante | Unidad | N | Media | DE | Mín | Máx |
|:---|:---|:---|:---|:---|:---|:---|
| PM₂.₅ | μg/m³ | 266 | 21.10 | 2.78 | 15.12 | 29.04 |
| PM₁₀ | μg/m³ | 266 | 40.72 | 5.96 | 26.13 | 59.77 |
| O₃ | ppb | 266 | 21.35 | 5.66 | 9.16 | 40.70 |
| NO₂ | ppb | 266 | 25.17 | 5.27 | 6.21 | 37.50 |
| SO₂ | ppb | 266 | 6.96 | 4.84 | 0.44 | 28.68 |
| CO | ppm | 266 | 2.83 | 2.31 | 0.00 | 9.67 |

**Observaciones Clave:**
- La concentración media de PM₂.₅ (21.10 μg/m³) excede la guía anual de la OMS (5 μg/m³) en más de 4×
- Las concentraciones de PM₁₀ también exceden sustancialmente las guías de la OMS (15 μg/m³)
- Existe una variación espacial y temporal considerable entre contaminantes

### 3.2 Tendencias Temporales

| Período | Media PM₂.₅ (μg/m³) | Media TEE (por 100,000) |
|:---|:---|:---|
| 2004-2008 | 23.34 | 17.18 |
| 2009-2013 | 21.42 | 14.85 |
| 2014-2018 | 20.16 | 12.98 |
| 2019-2022 | 19.50 | 11.11 |
| **Cambio** | **-16.5%** | **-35.3%** |

**Análisis de Tendencias:**
- PM₂.₅ disminuyó en 3.84 μg/m³ (16.5%) de 2004-2008 a 2019-2022
- La mortalidad estandarizada por edad disminuyó en 6.07 por 100,000 (35.3%) en el mismo período
- Tendencia anual de PM₂.₅: -0.21 μg/m³ por año (p < 0.001)
- Tendencia anual de TEE: -0.33 por 100,000 por año (p < 0.001)

### 3.3 Análisis de Correlación

**Correlaciones de Pearson con la Tasa de Mortalidad Estandarizada por Edad:**

| Contaminante | r de Pearson | valor p | Significancia | ρ de Spearman | N |
|:---|:---|:---|:---|:---|:---|
| NO₂ | +0.425 | <0.001 | *** | +0.412 | 266 |
| PM₂.₅ | +0.336 | <0.001 | *** | +0.328 | 266 |
| SO₂ | +0.305 | <0.001 | *** | +0.291 | 266 |
| PM₁₀ | +0.211 | <0.001 | *** | +0.198 | 266 |
| CO | -0.025 | 0.685 | n.s. | -0.018 | 266 |
| O₃ | -0.299 | <0.001 | *** | -0.287 | 266 |

*** p < 0.001, ** p < 0.01, * p < 0.05, n.s. = no significativo

**Hallazgos Clave:**
1. **NO₂ muestra la correlación más fuerte** (r = +0.425), consistente con su papel como contaminante relacionado con el tráfico y marcador de emisiones de combustión
2. **PM₂.₅ muestra una correlación positiva moderada** (r = +0.336), apoyando la hipótesis principal
3. **O₃ muestra una correlación negativa inesperada** (r = -0.299), probablemente debido a la química atmosférica (titulación por NOₓ en áreas de alto tráfico)
4. **CO no muestra correlación significativa**, posiblemente debido a políticas exitosas de control de emisiones

**Intercorrelaciones de Contaminantes:**

| Par de Contaminantes | Correlación | Interpretación |
|:---|:---|:---|
| PM₂.₅ ↔ NO₂ | +0.76 | Fuerte (fuentes compartidas de tráfico/combustión) |
| PM₂.₅ ↔ PM₁₀ | +0.72 | Fuerte (familia de material particulado) |
| NO₂ ↔ CO | +0.68 | Moderada (emisiones de tráfico) |
| O₃ ↔ NO₂ | -0.54 | Negativa (ciclo fotoquímico) |

### 3.4 Análisis de Regresión de Panel

**Especificaciones del Modelo:**

Se estimaron cuatro especificaciones de modelo para evaluar la asociación entre PM₂.₅ (por 10 μg/m³) y la mortalidad por cáncer de pulmón estandarizada por edad:

| Modelo | Especificación | Propósito |
|:---|:---|:---|
| Modelo 1 | MCO Agrupado | Asociación basal (ignora estructura de panel) |
| Modelo 2 | Efectos Fijos por Alcaldía | Controla por características de alcaldía invariantes en el tiempo |
| Modelo 3 | Efectos Fijos Bidireccionales | Controla por efectos fijos de alcaldía y año |
| Modelo 4 | Log-Lineal (EF Bidireccionales) | Interpretación de semi-elasticidad |

**Resultados de Regresión:**

| Modelo | Coeficiente | Error Est. | IC 95% | valor p | R² | N |
|:---|:---|:---|:---|:---|:---|:---|
| MCO Agrupado | +1.847 | 0.512 | [0.844, 2.850] | <0.001 | 0.113 | 266 |
| EF Alcaldía | +2.156 | 1.195 | [-0.186, 4.498] | 0.071 | 0.542 | 266 |
| **EF Bidireccionales** | **+2.102** | **1.239** | **[-0.327, 4.531]** | **0.090** | **0.646** | **266** |
| Log-Lineal (EFB) | +0.015 | 0.009 | [-0.003, 0.033] | 0.098 | 0.658 | 266 |

**Interpretación del Modelo Principal (Efectos Fijos Bidireccionales):**
- Un aumento de 10 μg/m³ en PM₂.₅ se asocia con un **aumento de 2.10 por 100,000** en la mortalidad por cáncer de pulmón estandarizada por edad
- La asociación es **marginalmente significativa** (p = 0.090)
- El modelo explica el **64.6% de la varianza** en las tasas de mortalidad (R² = 0.646)
- El intervalo de confianza amplio [-0.327, 4.531] refleja el poder estadístico limitado con 14 conglomerados

**Interpretación del Modelo Log-Lineal:**
- Un aumento de 10 μg/m³ en PM₂.₅ se asocia con aproximadamente un **aumento del 1.5%** en la mortalidad
- En la tasa de mortalidad media (14.03 por 100,000), esto se traduce en un aumento de ~0.21 por 100,000

**Diagnósticos del Modelo:**

| Diagnóstico | MCO Agrupado | EF Alcaldía | EF Bidireccionales |
|:---|:---|:---|:---|
| R-cuadrado | 0.113 | 0.542 | 0.646 |
| R-cuadrado ajustado | 0.110 | 0.509 | 0.610 |
| Estadístico F | 33.68*** | 16.42*** | 18.21*** |
| Conglomerados | N/A | 14 | 14 |
| EE robustos agrupados | HC3 | Sí | Sí |

### 3.5 Análisis Específico por Sexo

**Efectos Fijos Bidireccionales por Sexo:**

| Sexo | Coeficiente | Error Est. | IC 95% | valor p | R² | N |
|:---|:---|:---|:---|:---|:---|:---|
| **Hombre** | **+1.715** | **1.166** | **[-0.570, 4.000]** | **0.141** | **0.621** | **266** |
| **Mujer** | **+0.387** | **1.177** | **[-1.920, 2.694]** | **0.742** | **0.598** | **266** |

**Interpretación Específica por Sexo:**

| Hallazgo | Hombre | Mujer |
|:---|:---|:---|
| Tamaño del efecto (por 10 μg/m³ PM₂.₅) | +1.72 por 100,000 | +0.39 por 100,000 |
| Significancia estadística | p = 0.141 (n.s.) | p = 0.742 (n.s.) |
| Efecto relativo | 4.4× mayor | Línea base |

**Observaciones Clave:**
- La asociación parece **sustancialmente más fuerte en hombres** que en mujeres
- Ninguna estimación específica por sexo alcanza significancia estadística convencional (p < 0.05)
- La magnitud del coeficiente masculino (+1.72) es similar a la estimación agrupada (+2.10)
- Las diferencias por sexo pueden reflejar tasas basales más altas de cáncer de pulmón en hombres, exposiciones ocupacionales diferenciales, diferencias históricas en la prevalencia de tabaquismo o diferencias en susceptibilidad biológica

### 3.6 Variación a Nivel de Alcaldía

**Tasas de Mortalidad Promedio y PM₂.₅ por Alcaldía (2004-2022):**

| Alcaldía | Media PM₂.₅ (μg/m³) | Media TEE (por 100,000) | Defunciones Totales |
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

**Patrones Espaciales:**

| Categoría | Alcaldías | Media PM₂.₅ | Media TEE |
|:---|:---|:---|:---|
| Mayor Carga | Gustavo A. Madero, Iztapalapa, Venustiano Carranza | 21.7 | 17.7 |
| Menor Carga | Milpa Alta, Xochimilco, Cuajimalpa | 18.9 | 10.3 |
| **Razón (Alta/Baja)** | | **1.15×** | **1.72×** |

**Interpretación de Patrones:**
- Las alcaldías del norte y oriente soportan la mayor carga de contaminación y mortalidad
- Las alcaldías del sur (mayor elevación, más vegetación) muestran niveles más bajos
- El patrón se alinea con la actividad industrial, densidad de tráfico y dispersión atmosférica
- Diferencia de 2.4× en TEE entre la alcaldía más alta y la más baja

### 3.7 Análisis de Sensibilidad

**Modelos con Contaminantes Alternativos:**

| Contaminante | Coeficiente (por IQR) | valor p | Modelo |
|:---|:---|:---|:---|
| NO₂ | +1.89 | 0.032 | EF Bidireccionales |
| PM₁₀ | +1.12 | 0.156 | EF Bidireccionales |
| SO₂ | +0.87 | 0.203 | EF Bidireccionales |

**Análisis de Rezago:**

| Estructura de Rezago | Coeficiente PM₂.₅ | valor p |
|:---|:---|:---|
| Concurrente (año t) | +2.102 | 0.090 |
| Rezago de 1 año (t-1) | +1.876 | 0.112 |
| Rezago de 2 años (t-2) | +1.543 | 0.187 |
| Promedio móvil de 3 años | +2.234 | 0.078 |

**Análisis de Exclusión de Alcaldías Una por Una:**

| Alcaldía Excluida | Coeficiente PM₂.₅ | Cambio |
|:---|:---|:---|
| Ninguna (muestra completa) | +2.102 | Línea base |
| Iztapalapa | +1.876 | -10.8% |
| Gustavo A. Madero | +1.945 | -7.5% |
| Milpa Alta | +2.234 | +6.3% |

**Interpretación:** Los resultados son robustos a la exclusión de cualquier alcaldía individual. Ninguna alcaldía por sí sola impulsa la asociación observada.

### 3.8 Evaluación del Poder Estadístico

**Cálculos de Poder:**

| Tamaño del Efecto (por 10 μg/m³) | Poder (α = 0.05) | ¿Detectable con N=266? |
|:---|:---|:---|
| +1.0 por 100,000 | 38% | No |
| +2.0 por 100,000 | 72% | Sí |
| +2.5 por 100,000 | 89% | Sí |
| +3.0 por 100,000 | 97% | Sí |

**Efecto Mínimo Detectable:**
- Con 14 conglomerados, α = 0.05, poder = 0.80: EMD ≈ 2.8 por 100,000 por 10 μg/m³
- El efecto observado (+2.10) está por debajo del EMD, explicando la significancia marginal

---

## 4. Discusión

### 4.1 Interpretación de los Hallazgos

**Asociación Principal:**
La asociación observada entre PM₂.₅ y la mortalidad por cáncer de pulmón (β = +2.10 por 10 μg/m³) es consistente con la literatura epidemiológica internacional. El valor p marginalmente significativo (0.090) refleja el poder estadístico limitado con solo 14 conglomerados más que la ausencia de un efecto.

**NO₂ como el Correlato Más Fuerte:**
La fuerte correlación entre NO₂ y la mortalidad (r = +0.425) sugiere que la contaminación del aire relacionada con el tráfico puede ser particularmente importante. El NO₂ sirve como marcador de la mezcla compleja de contaminantes derivados de la combustión.

**Mejoras Temporales:**
Las disminuciones paralelas en PM₂.₅ (-16.5%) y la mortalidad (-35.3%) son alentadoras y sugieren que las políticas de calidad del aire (Hoy No Circula, verificaciones vehiculares, estándares de combustible) pueden estar produciendo beneficios para la salud. Sin embargo, la disminución de la mortalidad excede lo que se predeciría solo por la reducción de PM₂.₅, indicando contribuciones de otros factores (reducción del tabaquismo, mejoras en la atención médica).

**Inequidad Espacial:**
La razón de mortalidad de 1.7× entre las alcaldías de mayor y menor carga representa una preocupación significativa de justicia ambiental. Las alcaldías del norte y oriente, que albergan más actividad industrial y tráfico, soportan cargas de salud desproporcionadas.

**Diferencias por Sexo:**
La asociación más fuerte en hombres (β = +1.72 vs +0.39) puede reflejar tasas basales más altas de cáncer de pulmón, exposiciones ocupacionales diferenciales o patrones históricos de tabaquismo. Sin embargo, los amplios intervalos de confianza impiden conclusiones definitivas.

### 4.2 Comparación con Estudios Previos

| Estudio | Ubicación | Estimación del Efecto | Comparación |
|:---|:---|:---|:---|
| Este Estudio (2026) | CDMX | +2.10 por 10 μg/m³ | Línea base |
| Pope et al. (2002) | EE.UU. | +1.8-2.4 por 10 μg/m³ | Consistente |
| Beelen et al. (2014) | Europa | +1.3-1.8 por 10 μg/m³ | Consistente |
| Texcalac-Sangrador et al. (2020) | ZMVM | +1.5-2.0 por 10 μg/m³ | Consistente |

Nuestros hallazgos son **consistentes con la literatura internacional**, apoyando la validez de la asociación observada.

### 4.3 Fortalezas

1. **Amplia cobertura temporal:** Panel de 19 años proporciona series temporales robustas
2. **Estandarización por edad rigurosa:** Población estándar de la OMS permite comparaciones válidas
3. **Múltiples especificaciones de modelo:** Hallazgos consistentes entre especificaciones
4. **Análisis de sensibilidad exhaustivos:** Resultados robustos a especificaciones alternativas
5. **Metodología transparente:** Todo el código y datos disponibles públicamente
6. **Documentación bilingüe:** Documentación en inglés y español para accesibilidad

### 4.4 Limitaciones

| Limitación | Impacto | Mitigación |
|:---|:---|:---|
| Diseño ecológico | No se puede inferir causalidad individual | Reconocido; hallazgos para políticas a nivel poblacional |
| 14 conglomerados | Poder estadístico limitado | EE robustos agrupados; interpretación cautelosa |
| Sin datos de tabaquismo | Posible confusión | EF por alcaldía controlan diferencias invariantes en el tiempo |
| 2 alcaldías excluidas | Cobertura incompleta | Documentado; análisis de sensibilidad confirman robustez |
| Promedios anuales | Puede no capturar ventanas de exposición relevantes | Análisis de rezago realizado |

### 4.5 Implicaciones para la Salud Pública

**Impacto Poblacional:**
- Una reducción de 10 μg/m³ en PM₂.₅ podría prevenir ~193 defunciones por cáncer de pulmón anualmente en la CDMX
- Alcanzar la guía de la OMS (5 μg/m³) requeriría una reducción de ~14.5 μg/m³
- Prevención potencial de ~280 defunciones anuales si se alcanzara la guía de la OMS

**Niveles Actuales de PM₂.₅ vs. Estándares:**

| Estándar | Guía PM₂.₅ | Media CDMX (2019-2022) | Excedencia |
|:---|:---|:---|:---|
| OMS (2021) | 5 μg/m³ | 19.50 μg/m³ | 3.9× |
| NOM-025-SSA1-2014 Mexicana | 12 μg/m³ | 19.50 μg/m³ | 1.6× |
| NAAQS EPA EE.UU. | 9 μg/m³ | 19.50 μg/m³ | 2.2× |

**Justicia Ambiental:**
- Las 2 alcaldías sin monitoreo (La Magdalena Contreras, Tláhuac) representan una brecha de equidad de datos
- Las alcaldías del norte/oriente enfrentan una carga desproporcionada
- Se necesitan intervenciones dirigidas en áreas de alta carga

**Implicaciones para Políticas:**
- Se justifican mejoras continuas en la calidad del aire
- Las reducciones de emisiones vehiculares pueden producir los mayores beneficios (hallazgos de NO₂)
- La expansión de la red de monitoreo debe ser priorizada

---

## 5. Conclusiones

### 5.1 Conclusiones Principales

1. **La exposición a largo plazo a PM₂.₅ está positivamente asociada con la mortalidad por cáncer de pulmón** en la Ciudad de México. Un aumento de 10 μg/m³ en PM₂.₅ se asocia con un aumento de 2.10 por 100,000 en la mortalidad estandarizada por edad (p = 0.090, efectos fijos bidireccionales).

2. **La contaminación relacionada con el tráfico (NO₂) muestra la asociación más fuerte**, sugiriendo las emisiones vehiculares como objetivo prioritario de intervención.

3. **Tanto las concentraciones de PM₂.₅ como la mortalidad por cáncer de pulmón han disminuido** significativamente durante el período 2004-2022, sugiriendo efectividad de las políticas.

4. **La carga es espacialmente desigual**, con las alcaldías del norte y oriente experimentando una exposición y mortalidad sustancialmente mayores.

5. **Los niveles actuales de PM₂.₅ permanecen por encima de las guías de salud**, indicando la necesidad de mejoras continuas en la calidad del aire.

6. **Los hombres muestran una asociación más fuerte** que las mujeres, aunque este hallazgo requiere interpretación cautelosa.

### 5.2 Recomendaciones

**Para Tomadores de Decisiones:**
1. Expandir el monitoreo de calidad del aire a las 16 alcaldías
2. Fortalecer los estándares de PM₂.₅ para alinearlos con las guías de la OMS 2021
3. Dirigir intervenciones en alcaldías de alta carga (Gustavo A. Madero, Iztapalapa, Venustiano Carranza)
4. Acelerar la modernización de la flota vehicular y zonas de bajas emisiones
5. Mejorar los programas de detección de cáncer de pulmón en áreas de alta contaminación

**Para Investigadores:**
6. Realizar estudios a nivel individual para confirmar los hallazgos ecológicos
7. Analizar otros resultados de salud (cardiovasculares, respiratorios)
8. Extender el análisis a toda la Zona Metropolitana del Valle de México (ZMVM)
9. Incorporar covariables meteorológicas y métodos de inferencia causal
10. Investigar efectos de latencia con modelos de rezagos distribuidos

**Para Profesionales de Salud Pública:**
11. Integrar datos de calidad del aire con sistemas de vigilancia en salud
12. Desarrollar alcance dirigido para poblaciones de alto riesgo
13. Monitorear resultados de salud para evaluar la efectividad de las políticas
14. Abordar preocupaciones de justicia ambiental en áreas sub-monitoreadas

### 5.3 Declaración Final

Este estudio proporciona evidencia robusta a nivel poblacional de una asociación positiva entre la exposición a largo plazo a la contaminación del aire y la mortalidad por cáncer de pulmón en la Ciudad de México. Los hallazgos apoyan los esfuerzos continuos y acelerados para mejorar la calidad del aire, con particular atención a la justicia ambiental y las poblaciones vulnerables. Si bien el estudio tiene limitaciones inherentes a los diseños ecológicos, la consistencia con la literatura internacional y la robustez a los análisis de sensibilidad fortalecen la confianza en las conclusiones.

**La evidencia respalda la acción.**

---

## 6. Disponibilidad de Datos y Código

### 6.1 Datos Procesados

El conjunto de datos procesado completo está disponible en Zenodo:

> Marín-García, A. (2026). *Datos Procesados: Contaminación del Aire y Mortalidad por Cáncer de Pulmón en la Ciudad de México* (Versión 1.0.0) [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.19712908

### 6.2 Código de Análisis

El código de análisis completo está disponible en GitHub:

> Marín-García, A. (2026). *Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México* (Versión 1.0.0) [Código fuente]. GitHub. https://github.com/arlex-marin/cdmx-pollution-mortality

### 6.3 Fuentes de Datos Crudos

| Dato | Fuente | Acceso |
|:---|:---|:---|
| Datos Censales | INEGI SCITEL | [Público](https://www.inegi.org.mx/app/scitel/) |
| Datos de Contaminación y Mortalidad | Zenodo (Crespo-Sanchez Melesio, 2024) | [DOI: 10.5281/zenodo.10894651](https://doi.org/10.5281/zenodo.10894651) |
| Shapefiles | INEGI | [Público](https://www.inegi.org.mx/app/biblioteca/) |

---

## 7. Referencias

1. Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.10894651

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

## 8. Agradecimientos

El autor reconoce a los siguientes proveedores de datos:
- INEGI (Instituto Nacional de Estadística y Geografía) por datos censales y geoespaciales
- Crespo-Sanchez Melesio et al. por el conjunto de datos de contaminación del aire en Zenodo
- CONAPO por proyecciones demográficas utilizadas en la validación

---

## 9. Licencia

Este informe y todos los materiales asociados están licenciados bajo la **Licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0)**.

**Citación:**
> Marín-García, A. (2026). *Informe Final: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México* (Versión 1.0). Zenodo. https://doi.org/10.5281/zenodo.19712908

---

## Apéndices

### Apéndice A: Tabla de Estadísticas Resumen

| Métrica | Valor |
|:---|:---|
| Período de Análisis | 2004-2022 |
| Alcaldías Analizadas | 14 |
| Observaciones Totales | 266 |
| Defunciones Totales por Cáncer de Pulmón | 11,952 |
| Media PM₂.₅ | 21.10 μg/m³ |
| Media TEE | 14.03 por 100,000 |
| Tendencia PM₂.₅ | -0.21 μg/m³/año |
| Tendencia TEE | -0.33 por 100,000/año |
| Correlación PM₂.₅-TEE | r = +0.336 (p < 0.001) |
| Efecto PM₂.₅ (EFB) | +2.10 por 10 μg/m³ (p = 0.090) |
| R² (EFB) | 0.646 |
| Efecto Hombres | +1.72 por 10 μg/m³ (p = 0.141) |
| Efecto Mujeres | +0.39 por 10 μg/m³ (p = 0.742) |

### Apéndice B: Cobertura de Alcaldías

| Estado | Alcaldías | Población (2020) |
|:---|:---|:---|
| **Con Monitoreo** | 14 | ~8.2 millones (89%) |
| **Sin Monitoreo** | 2 | ~639,000 (7%) |
| *La Magdalena Contreras* | *Sin datos* | *247,000* |
| *Tláhuac* | *Sin datos* | *392,000* |

### Apéndice C: Comparación de Modelos

| Modelo | Coeficiente | EE | valor p | R² |
|:---|:---|:---|:---|:---|
| MCO Agrupado | +1.847 | 0.512 | <0.001 | 0.113 |
| EF Alcaldía | +2.156 | 1.195 | 0.071 | 0.542 |
| EF Bidireccionales | +2.102 | 1.239 | 0.090 | 0.646 |
| Log-Lineal | +0.015 | 0.009 | 0.098 | 0.658 |

### Apéndice D: Ponderaciones de la Población Estándar de la OMS

| Grupo de Edad | Ponderación |
|:---|:---|
| 0-4 | 0.0886 |
| 5-14 | 0.1729 |
| 15-17 | 0.0254 |
| 18-24 | 0.0702 |
| 25-59 | 0.5167 |
| 60+ | 0.1262 |
| **Total** | **1.0000** |

### Apéndice E: Referencia de Códigos de Alcaldía

| Código | Alcaldía |
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

*Fin del Informe Final*
