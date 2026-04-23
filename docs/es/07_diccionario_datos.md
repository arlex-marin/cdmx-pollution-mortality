# Diccionario de Datos: Conjunto de Datos de Análisis de Contaminación del Aire y Mortalidad por Cáncer de Pulmón en la CDMX

**Proyecto 1: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México**

**Autor:** Arlex Marín  
**Fecha:** 21 de abril de 2026  
**Versión:** 1.0

---

## Archivo: `cdmx_analysis_dataset_2004_2022.csv`

### Descripción General
Este conjunto de datos contiene observaciones anuales para las 16 alcaldías de la Ciudad de México desde 2004 hasta 2022. Cada fila representa una combinación única de alcaldía, año y categoría de sexo (Mujer, Hombre, Ambos). El conjunto de datos incluye estimaciones de población, conteos de mortalidad por cáncer de pulmón, tasas de mortalidad crudas y estandarizadas por edad, y concentraciones promedio anuales de contaminantes del aire.

### Dimensiones del Conjunto de Datos
| Atributo | Valor |
| :--- | :--- |
| Registros totales | 912 |
| Alcaldías | 16 |
| Años | 2004-2022 (19 años) |
| Categorías de sexo | 3 (Mujer, Hombre, Ambos) |
| Variables | 13 |

### Variables

| Variable | Tipo | Descripción | Unidades | Rango Válido | Valores Faltantes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `alcaldia` | Cadena | Nombre de la alcaldía (municipio) | - | 16 alcaldías de la CDMX | 0 |
| `year` | Entero | Año de observación | - | 2004-2022 | 0 |
| `sex` | Cadena | Categoría de sexo | - | Mujer, Hombre, Ambos | 0 |
| `population` | Entero | Población estimada | Personas | >0 | 0 |
| `deaths` | Entero | Defunciones por cáncer de pulmón (CIE-10 C33-C34) | Conteo | ≥0 | 0 |
| `crude_rate` | Flotante | Tasa de mortalidad cruda | por 100,000 | ≥0 | 0 |
| `age_standardized_rate` | Flotante | Tasa de mortalidad estandarizada por edad (estándar OMS) | por 100,000 | ≥0 | 0 |
| `pm25` | Flotante | Concentración promedio anual de PM₂.₅ | μg/m³ | 11.8-51.9 | 76 (8.3%) |
| `pm10` | Flotante | Concentración promedio anual de PM₁₀ | μg/m³ | 19.5-109.0 | 76 (8.3%) |
| `o3` | Flotante | Concentración promedio anual de ozono | ppb | 9.2-42.4 | 76 (8.3%) |
| `no2` | Flotante | Concentración promedio anual de dióxido de nitrógeno | ppb | 6.2-46.7 | 76 (8.3%) |
| `so2` | Flotante | Concentración promedio anual de dióxido de azufre | ppb | 0.4-70.1 | 76 (8.3%) |
| `co` | Flotante | Concentración promedio anual de monóxido de carbono | ppm | 0.0-19.7 | 76 (8.3%) |

### Notas sobre Valores Faltantes
- Los datos de contaminación (pm25, pm10, o3, no2, so2, co) están ausentes para **La Magdalena Contreras** y **Tláhuac** porque estas alcaldías no cuentan con estaciones de monitoreo de calidad del aire en el conjunto de datos fuente.
- Esto resulta en 76 registros de contaminación faltantes de un total de 912 registros de análisis (8.3%).
- Las otras 14 alcaldías tienen datos de contaminación completos para todos los años 2004-2022.
- El valor único negativo de CO reportado en la validación (-0.17 ppm) se trató como 0 en el conjunto de datos final.

### Alcaldías Incluidas
| Alcaldía | Datos de Contaminación Disponibles | Código INEGI |
| :--- | :--- | :--- |
| Azcapotzalco | Sí | 002 |
| Coyoacán | Sí | 003 |
| Cuajimalpa de Morelos | Sí | 004 |
| Gustavo A. Madero | Sí | 005 |
| Iztacalco | Sí | 006 |
| Iztapalapa | Sí | 007 |
| La Magdalena Contreras | **No** | 008 |
| Milpa Alta | Sí | 009 |
| Álvaro Obregón | Sí | 010 |
| Tláhuac | **No** | 011 |
| Tlalpan | Sí | 012 |
| Xochimilco | Sí | 013 |
| Benito Juárez | Sí | 014 |
| Cuauhtémoc | Sí | 015 |
| Miguel Hidalgo | Sí | 016 |
| Venustiano Carranza | Sí | 017 |

**Nota:** Los nombres de las alcaldías en el conjunto de datos utilizan caracteres ASCII (por ejemplo, "Alvaro Obregon" en lugar de "Álvaro Obregón") por compatibilidad.

### Estadísticas Descriptivas (Ambos Sexos, 2004-2022)

| Variable | N | Media | DE | Mín | Máx |
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

### Conjuntos de Datos Fuente
| Grupo de Variables | Fuente | Cobertura Temporal |
| :--- | :--- | :--- |
| Población | Censos INEGI 2000, 2005, 2010, 2020 (armonizados) | 2000-2022 |
| Contaminación y Mortalidad | Conjunto de Datos de Contaminación del Aire en Zenodo (Crespo-Sanchez, Melesio, 2024) | 1986-2022 |

### Estandarización por Edad
Las tasas estandarizadas por edad se calcularon utilizando el método directo con la Población Estándar Mundial de la OMS como referencia. Los grupos de edad armonizados utilizados fueron: 0-4, 5-14, 15-17, 18-24, 25-59 y 60+ años.

### Ponderaciones del Estándar de la OMS Aplicadas
| Grupo de Edad | Ponderación |
| :--- | :--- |
| 0-4 | 0.0886 |
| 5-14 | 0.1729 |
| 15-17 | 0.0254 |
| 18-24 | 0.0702 |
| 25-59 | 0.5167 |
| 60+ | 0.1262 |

### Códigos CIE-10 Utilizados
| Código | Descripción |
| :--- | :--- |
| C33 | Tumor maligno de la tráquea |
| C34 | Tumor maligno de los bronquios y del pulmón |

---

*Fin del Diccionario de Datos*
