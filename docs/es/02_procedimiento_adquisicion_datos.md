# Procedimiento de Adquisición y Curación de Datos

**Proyecto 1: Análisis Geoespacial de Contaminación del Aire y Mortalidad por Cáncer en la Ciudad de México**
**Autor:** Arlex Marín
**Fecha:** 21 de abril de 2026
**Versión:** 1.0 (Traducción al Español)

---

## Datos de Censos de Población y Vivienda

1. Los datos de los censos de población y vivienda se descargaron el 16 de abril de 2026, junto con los diccionarios de datos de cada censo, desde el sitio web oficial del INEGI a través de la herramienta SCITEL: https://www.inegi.org.mx/app/scitel/Default?ev=9

2. Los datos de cada censo se descargaron seleccionando todos los indicadores de "identificación geográfica" y "Estructura por edad y sexo" para el año 2020, y todos los indicadores de "identificación geográfica" y "población" para los años 2010, 2005 y 2000.

3. Los cuatro archivos descargados son:
   - `ITER2020 - 09 Ciudad de México.csv` para el censo correspondiente al año 2020
   - `RESLOC2010 - 09 Ciudad de México.txt` para el censo correspondiente al año 2010
   - `RESLOC2005 - 09 Ciudad de México.txt` para el censo correspondiente al año 2005
   - `RESLOC2000 - 09 Ciudad de México.txt` para el censo correspondiente al año 2000

4. Se modificaron los nombres de los archivos:
   - de `ITER2020 - 09 Ciudad de México.csv` a `ITER2020_09_CDMX.csv`
   - de `RESLOC2010 - 09 Ciudad de México.txt` a `RESLOC2010_09_CDMX.csv`
   - de `RESLOC2005 - 09 Ciudad de México.txt` a `RESLOC2005_09_CDMX.csv`
   - de `RESLOC2000 - 09 Ciudad de México.txt` a `RESLOC2000_09_CDMX.csv`

   para estandarizar los nombres y el manejo de archivos sin sacrificar funcionalidad.

5. Estos datos se movieron a la carpeta `data/raw/census/`.

6. Se descargaron los diccionarios de datos de cada censo, los cuales son:
   - `fd_2020.pdf` para el censo correspondiente al año 2020
   - `fd_2010.pdf` para el censo correspondiente al año 2010
   - `fd_2005.pdf` para el censo correspondiente al año 2005
   - `fd_2000.pdf` para el censo correspondiente al año 2000

7. Estos diccionarios se movieron a la carpeta `data/external/dictionaries/`.

---

## Datos de Contaminación del Aire por Alcaldía y Mortalidad

1. Los archivos de datos se descargaron el 16 de abril de 2026 desde el sitio web oficial de la base de datos "Jub's Case Study: Cancer Mortality and Air Pollutants in Mexico data" en Zenodo: https://zenodo.org/records/17691800

2. Se descargaron los archivos `Alcaldias_contaminantes_Anual_geo_limpio_86-22.csv` y `deaths_registry.rar`.

3. El archivo csv se movió a la carpeta `data/raw/pollution/` para estandarizar la organización de datos y el manejo de archivos sin sacrificar funcionalidad.

4. El archivo comprimido rar fue extraído en la carpeta `data/raw/mortality/` para estandarizar la organización de datos y el manejo de archivos sin sacrificar funcionalidad.

---

## Datos Geoespaciales de la Ciudad de México

1. Los datos geoespaciales se descargaron el 21 de abril de 2026 desde el sitio web oficial del Marco Geoestadístico del INEGI correspondiente al año 2025, a través de la herramienta oficial del INEGI: https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551163061

2. Se descargó el archivo `09_ciudaddemexico.zip` (794551163061_s.zip).

3. Su contenido se extrajo en la carpeta `data/external/shapefiles/` manteniendo la estructura original de directorios.

4. La estructura resultante es:

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

5. El archivo principal utilizado para el mapeo es `09mun.shp`, el cual contiene los polígonos de las 16 alcaldías de la Ciudad de México.

---

## Resumen de la Estructura de Directorios

```
data/
├── external/
│   ├── dictionaries/
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2000_2001.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2002_2003.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2004_2011.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2012_2013.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2014.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2015.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2016.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2017.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2018.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2019.csv
│   │   ├── DESCRIPTOR_CAMPOS_DEFUN_2020.csv
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

## Referencias de las Fuentes de Datos

| Tipo de Dato | Fuente | URL |
| :--- | :--- | :--- |
| Datos Censales | INEGI SCITEL | https://www.inegi.org.mx/app/scitel/Default?ev=9 |
| Datos de Contaminación y Mortalidad | Zenodo (Crespo-Sanchez, Melesio, 2024) | https://zenodo.org/records/17691800 |
| Datos Geoespaciales | INEGI Marco Geoestadístico 2025 | https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551163061 |

---

## Citación de los Datos

Al utilizar estas fuentes de datos, favor de citar:

- **Datos Censales:** INEGI. (2000, 2005, 2010, 2020). *Censos y Conteos de Población y Vivienda*. Instituto Nacional de Estadística y Geografía, México.

- **Datos de Contaminación y Mortalidad:** Crespo-Sanchez, Melesio. (2024). *Air Pollution and Cancer Mortality Dataset - Mexico City* [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.10894651

- **Datos Geoespaciales:** INEGI. (2025). *Marco Geoestadístico 2025*. Instituto Nacional de Estadística y Geografía, México.

---

## Notas sobre el Uso de los Datos

### Consideraciones sobre los Datos Censales
- El censo del año 2000 tiene un detalle limitado de edad a nivel municipal; las distribuciones de edad por sexo requirieron estimación
- El Conteo de 2005 proporciona una buena cobertura pero requiere la división del grupo de edad de 15-24 años
- El censo de 2010 tiene desgloses detallados pero requiere estimación para la población de 25-59 años por sexo
- El censo de 2020 es el estándar de referencia con desglose completo de edad y sexo en grupos quinquenales; nótese que `POBTOT` está vacío a nivel municipal

### Consideraciones sobre los Datos de Mortalidad
- Los códigos CIE-10 C33 (tráquea) y C34 (bronquios y pulmón) identifican los casos de cáncer de pulmón

### Consideraciones sobre los Datos de Contaminación
- Dos alcaldías (La Magdalena Contreras y Tláhuac) carecen de estaciones de monitoreo
- El conjunto de datos incluye 12 municipios del Estado de México que no pertenecen a la CDMX (filtrados durante la integración)
- Un valor único negativo de CO (-0.17 ppm) es un artefacto de redondeo y se trató como 0

### Consideraciones sobre los Datos Geoespaciales
- El SRC original es EPSG:6372 (transformado a EPSG:4326 para el mapeo)
- El archivo `09mun.shp` contiene los límites de las 16 alcaldías

---

*Fin del documento de Procedimiento de Adquisición de Datos*
