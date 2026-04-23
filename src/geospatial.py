"""
Geospatial visualization functions using CDMX shapefiles.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Robust shapefile path discovery with recursive search,
                         fixed bivariate choropleth NaN color handling
"""

import pandas as pd
import numpy as np
import warnings
from pathlib import Path
import matplotlib.pyplot as plt

# Geopandas is required - fail early with clear message
try:
    import geopandas as gpd
except ImportError as e:
    raise ImportError(
        "Geopandas is required for geospatial visualizations. "
        "Install with: conda install -c conda-forge geopandas\n"
        f"Original error: {e}"
    )

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    warnings.warn("Plotly not available. Interactive maps will be disabled.")

from .utils import ALCALDIA_CODES, ALCALDIA_NAME_TO_CODE
from . import SHAPEFILE_DIR, FIGURES_DIR, ensure_directories


def get_municipal_shapefile_path():
    """
    Get the path to the municipal shapefile using recursive search.

    Returns:
    --------
    Path
        Path to 09mun.shp

    Raises:
    -------
    FileNotFoundError
        If shapefile cannot be found
    """
    # Recursive search for the municipal shapefile
    matches = list(SHAPEFILE_DIR.rglob('09mun.shp'))

    if matches:
        # Prefer paths that include 'conjunto_de_datos' as they're likely the correct one
        preferred = [m for m in matches if 'conjunto_de_datos' in str(m)]
        if preferred:
            path = preferred[0]
        else:
            path = matches[0]
        print(f"  Found shapefile: {path}")
        return path

    # Provide helpful error message with extraction instructions
    raise FileNotFoundError(
        f"Municipal shapefile '09mun.shp' not found in {SHAPEFILE_DIR}.\n"
        "Please ensure you have:\n"
        "1. Downloaded the INEGI Marco Geoestadístico shapefile for CDMX\n"
        "2. Extracted the ZIP file maintaining the directory structure\n"
        "3. Placed the extracted contents in the 'data/external/shapefiles/' directory\n"
        "Expected structure: .../shapefiles/[extracted_folder]/conjunto_de_datos/09mun.shp"
    )


def get_entity_shapefile_path():
    """
    Get the path to the entity shapefile using recursive search.

    Returns:
    --------
    Path
        Path to 09ent.shp

    Raises:
    -------
    FileNotFoundError
        If shapefile cannot be found
    """
    matches = list(SHAPEFILE_DIR.rglob('09ent.shp'))

    if matches:
        preferred = [m for m in matches if 'conjunto_de_datos' in str(m)]
        path = preferred[0] if preferred else matches[0]
        print(f"  Found entity shapefile: {path}")
        return path

    raise FileNotFoundError(
        f"Entity shapefile '09ent.shp' not found in {SHAPEFILE_DIR}.\n"
        "Please ensure the INEGI shapefile is properly extracted."
    )


def load_cdmx_shapefile(level='municipal'):
    """
    Load CDMX shapefile.

    Parameters:
    -----------
    level : str
        'municipal' for alcaldía boundaries, 'entity' for state boundary

    Returns:
    --------
    geopandas.GeoDataFrame
    """
    if level == 'municipal':
        shapefile_path = get_municipal_shapefile_path()
    elif level == 'entity':
        shapefile_path = get_entity_shapefile_path()
    else:
        raise ValueError(f"Invalid level '{level}'. Use 'municipal' or 'entity'.")

    gdf = gpd.read_file(shapefile_path)
    print(f"  Loaded shapefile: {shapefile_path.name}")
    print(f"  Features: {len(gdf)}")
    print(f"  CRS: {gdf.crs}")

    # Ensure CRS is WGS84 for Plotly compatibility
    if gdf.crs is not None and str(gdf.crs).upper() != 'EPSG:4326':
        print(f"  Converting CRS from {gdf.crs} to EPSG:4326")
        gdf = gdf.to_crs('EPSG:4326')

    return gdf


def prepare_alcaldia_shapefile(gdf):
    """
    Prepare municipal shapefile for merging with analysis data.

    Parameters:
    -----------
    gdf : geopandas.GeoDataFrame
        Raw municipal shapefile

    Returns:
    --------
    geopandas.GeoDataFrame
        Shapefile with standardized alcaldía names and codes
    """
    gdf = gdf.copy()

    # Identify municipality code column (CVE_MUN or CVEGEO)
    code_col = None
    for col in ['CVE_MUN', 'CVEGEO', 'MUNICIPIO', 'CVE_GEO']:
        if col in gdf.columns:
            code_col = col
            break

    if code_col:
        # Extract the last 3 digits for municipal code
        gdf['alcaldia_code'] = gdf[code_col].astype(str).str[-3:].str.zfill(3)
    else:
        warnings.warn("Could not find municipality code column in shapefile")
        gdf['alcaldia_code'] = None

    # Identify municipality name column
    name_col = None
    for col in ['NOM_MUN', 'MUNICIPIO', 'NOMBRE', 'NOMGEO']:
        if col in gdf.columns:
            name_col = col
            break

    if name_col:
        gdf['alcaldia_original'] = gdf[name_col]
        gdf['alcaldia'] = gdf['alcaldia_code'].map(ALCALDIA_CODES)
    else:
        warnings.warn("Could not find municipality name column in shapefile")
        gdf['alcaldia'] = None

    # Keep only CDMX alcaldías
    gdf = gdf[gdf['alcaldia_code'].isin(ALCALDIA_CODES.keys())].copy()

    print(f"  Prepared {len(gdf)} alcaldía boundaries")

    return gdf


def create_choropleth_map(df_analysis, year=2020, save_html=True):
    """
    Create an interactive choropleth map of mortality rates.

    Parameters:
    -----------
    df_analysis : pd.DataFrame
        Analysis dataset with mortality rates
    year : int
        Year to display (default 2020)
    save_html : bool
        Save as interactive HTML file

    Returns:
    --------
    plotly.graph_objects.Figure or matplotlib.figure.Figure
    """
    print(f"\n  Creating choropleth map for {year}...")

    ensure_directories()

    # Load and prepare shapefile
    gdf = load_cdmx_shapefile('municipal')
    gdf = prepare_alcaldia_shapefile(gdf)

    # Get mortality data for the specified year (Both sexes)
    df_year = df_analysis[
        (df_analysis['year'] == year) &
        (df_analysis['sex'] == 'Both')
    ].copy()

    # Merge shapefile with mortality data
    gdf_merged = gdf.merge(
        df_year[['alcaldia', 'age_standardized_rate', 'crude_rate', 'pm25']],
        on='alcaldia',
        how='left'
    )

    # Identify missing alcaldías
    missing = gdf_merged[gdf_merged['age_standardized_rate'].isna()]['alcaldia'].tolist()
    if missing:
        print(f"  ⚠️ Missing data for: {missing}")

    # Create static matplotlib choropleth
    fig_static, ax = plt.subplots(1, 1, figsize=(12, 10))

    gdf_merged.plot(
        column='age_standardized_rate',
        ax=ax,
        legend=True,
        legend_kwds={'label': 'Age-Standardized Mortality Rate (per 100,000)',
                     'orientation': 'horizontal',
                     'shrink': 0.6},
        cmap='Reds',
        edgecolor='black',
        linewidth=0.5,
        missing_kwds={'color': 'lightgrey', 'label': 'No data'}
    )

    # Add alcaldía labels
    for idx, row in gdf_merged.iterrows():
        if pd.notna(row['age_standardized_rate']):
            centroid = row.geometry.centroid
            ax.annotate(
                row['alcaldia'][:10] if row['alcaldia'] else '',
                xy=(centroid.x, centroid.y),
                ha='center',
                va='center',
                fontsize=7,
                color='black',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7)
            )

    ax.set_title(f'Age-Standardized Lung Cancer Mortality Rates by Alcaldía\nMexico City, {year}',
                 fontsize=14, fontweight='bold')
    ax.set_axis_off()

    plt.tight_layout()
    fig_static.savefig(FIGURES_DIR / f'choropleth_mortality_{year}.png', dpi=300, bbox_inches='tight')
    fig_static.savefig(FIGURES_DIR / f'choropleth_mortality_{year}.svg', bbox_inches='tight')
    print(f"  ✓ Saved static map: choropleth_mortality_{year}.png")

    # Create interactive Plotly map
    fig_interactive = None
    if save_html and PLOTLY_AVAILABLE:
        # Convert to GeoJSON
        geojson = gdf_merged.__geo_interface__

        fig_interactive = px.choropleth_mapbox(
            gdf_merged,
            geojson=geojson,
            locations=gdf_merged.index,
            color='age_standardized_rate',
            color_continuous_scale='Reds',
            range_color=(0, 30),
            mapbox_style='carto-positron',
            zoom=9,
            center={'lat': 19.4326, 'lon': -99.1332},
            opacity=0.7,
            labels={'age_standardized_rate': 'Mortality Rate per 100,000'},
            title=f'Age-Standardized Lung Cancer Mortality Rates by Alcaldía, Mexico City ({year})',
            hover_data={
                'alcaldia': True,
                'age_standardized_rate': ':.2f',
                'crude_rate': ':.2f',
                'pm25': ':.2f'
            }
        )

        fig_interactive.write_html(FIGURES_DIR / f'choropleth_mortality_{year}.html')
        print(f"  ✓ Saved interactive map: choropleth_mortality_{year}.html")
    elif save_html and not PLOTLY_AVAILABLE:
        warnings.warn("Plotly not available - skipping interactive map")

    plt.close(fig_static)

    if save_html and PLOTLY_AVAILABLE:
        return fig_interactive
    return fig_static


def create_pollution_choropleth(df_analysis, year=2020, pollutant='pm25', save_html=True):
    """
    Create an interactive choropleth map of air pollution.

    Parameters:
    -----------
    df_analysis : pd.DataFrame
        Analysis dataset with pollution data
    year : int
        Year to display (default 2020)
    pollutant : str
        Pollutant to display ('pm25', 'pm10', 'o3', 'no2', 'so2', 'co')
    save_html : bool
        Save as interactive HTML file

    Returns:
    --------
    plotly.graph_objects.Figure or matplotlib.figure.Figure
    """
    print(f"\n  Creating pollution choropleth map for {year} ({pollutant.upper()})...")

    ensure_directories()

    # Load and prepare shapefile
    gdf = load_cdmx_shapefile('municipal')
    gdf = prepare_alcaldia_shapefile(gdf)

    # Get pollution data for the specified year (Both sexes)
    df_year = df_analysis[
        (df_analysis['year'] == year) &
        (df_analysis['sex'] == 'Both')
    ].copy()

    # Merge shapefile with pollution data
    gdf_merged = gdf.merge(
        df_year[['alcaldia', pollutant]],
        on='alcaldia',
        how='left'
    )

    # Identify missing alcaldías
    missing = gdf_merged[gdf_merged[pollutant].isna()]['alcaldia'].tolist()
    if missing:
        print(f"  ⚠️ Missing data for: {missing}")

    # Pollutant display names and units
    pollutant_info = {
        'pm25': {'name': 'PM₂.₅', 'unit': 'μg/m³', 'cmap': 'Blues', 'range': (10, 30)},
        'pm10': {'name': 'PM₁₀', 'unit': 'μg/m³', 'cmap': 'Greens', 'range': (20, 60)},
        'o3': {'name': 'Ozone', 'unit': 'ppb', 'cmap': 'Purples', 'range': (10, 40)},
        'no2': {'name': 'NO₂', 'unit': 'ppb', 'cmap': 'Oranges', 'range': (10, 40)},
        'so2': {'name': 'SO₂', 'unit': 'ppb', 'cmap': 'Reds', 'range': (0, 20)},
        'co': {'name': 'CO', 'unit': 'ppm', 'cmap': 'Greys', 'range': (0, 10)}
    }

    info = pollutant_info.get(pollutant, {'name': pollutant.upper(), 'unit': '', 'cmap': 'Blues', 'range': None})

    # Create static matplotlib choropleth
    fig_static, ax = plt.subplots(1, 1, figsize=(12, 10))

    gdf_merged.plot(
        column=pollutant,
        ax=ax,
        legend=True,
        legend_kwds={'label': f"{info['name']} ({info['unit']})",
                     'orientation': 'horizontal',
                     'shrink': 0.6},
        cmap=info['cmap'],
        edgecolor='black',
        linewidth=0.5,
        missing_kwds={'color': 'lightgrey', 'label': 'No data'}
    )

    # Add alcaldía labels
    for idx, row in gdf_merged.iterrows():
        if pd.notna(row[pollutant]):
            centroid = row.geometry.centroid
            ax.annotate(
                row['alcaldia'][:10] if row['alcaldia'] else '',
                xy=(centroid.x, centroid.y),
                ha='center',
                va='center',
                fontsize=7,
                color='black',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7)
            )

    ax.set_title(f"{info['name']} Concentrations by Alcaldía\nMexico City, {year}",
                 fontsize=14, fontweight='bold')
    ax.set_axis_off()

    plt.tight_layout()
    fig_static.savefig(FIGURES_DIR / f'choropleth_{pollutant}_{year}.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved static map: choropleth_{pollutant}_{year}.png")

    # Create interactive Plotly map
    fig_interactive = None
    if save_html and PLOTLY_AVAILABLE:
        geojson = gdf_merged.__geo_interface__

        fig_interactive = px.choropleth_mapbox(
            gdf_merged,
            geojson=geojson,
            locations=gdf_merged.index,
            color=pollutant,
            color_continuous_scale=info['cmap'],
            range_color=info['range'],
            mapbox_style='carto-positron',
            zoom=9,
            center={'lat': 19.4326, 'lon': -99.1332},
            opacity=0.7,
            labels={pollutant: f"{info['name']} ({info['unit']})"},
            title=f"{info['name']} Concentrations by Alcaldía, Mexico City ({year})",
            hover_data={
                'alcaldia': True,
                pollutant: ':.2f'
            }
        )

        fig_interactive.write_html(FIGURES_DIR / f'choropleth_{pollutant}_{year}.html')
        print(f"  ✓ Saved interactive map: choropleth_{pollutant}_{year}.html")

    plt.close(fig_static)

    if save_html and PLOTLY_AVAILABLE:
        return fig_interactive
    return fig_static


def create_bivariate_choropleth(df_analysis, year=2020, save_html=True):
    """
    Create a bivariate choropleth map showing PM2.5 and mortality together.

    Parameters:
    -----------
    df_analysis : pd.DataFrame
        Analysis dataset
    year : int
        Year to display
    save_html : bool
        Save as interactive HTML file

    Returns:
    --------
    matplotlib.figure.Figure
    """
    print(f"\n  Creating bivariate choropleth map for {year}...")

    ensure_directories()

    # Load and prepare shapefile
    gdf = load_cdmx_shapefile('municipal')
    gdf = prepare_alcaldia_shapefile(gdf)

    # Get data for the specified year
    df_year = df_analysis[
        (df_analysis['year'] == year) &
        (df_analysis['sex'] == 'Both')
    ].copy()

    # Merge shapefile with data
    gdf_merged = gdf.merge(
        df_year[['alcaldia', 'age_standardized_rate', 'pm25']],
        on='alcaldia',
        how='left'
    )

    # Create quantile categories for both variables
    gdf_merged['pm25_quartile'] = pd.qcut(
        gdf_merged['pm25'].dropna(),
        q=3,
        labels=['Low', 'Medium', 'High']
    ).reindex(gdf_merged.index)

    gdf_merged['mortality_quartile'] = pd.qcut(
        gdf_merged['age_standardized_rate'].dropna(),
        q=3,
        labels=['Low', 'Medium', 'High']
    ).reindex(gdf_merged.index)

    # Create combined category
    gdf_merged['bivariate'] = (
        gdf_merged['pm25_quartile'].astype(str) + ' PM / ' +
        gdf_merged['mortality_quartile'].astype(str) + ' Mort'
    )

    # Color mapping for 3x3 bivariate
    colors = {
        'Low PM / Low Mort': '#e8e8e8',
        'Low PM / Medium Mort': '#e4d4e8',
        'Low PM / High Mort': '#c8a8d4',
        'Medium PM / Low Mort': '#c1e8c1',
        'Medium PM / Medium Mort': '#b8d4b8',
        'Medium PM / High Mort': '#a8c4a8',
        'High PM / Low Mort': '#a8d4d4',
        'High PM / Medium Mort': '#8cc4c4',
        'High PM / High Mort': '#6bb4b4'
    }

    gdf_merged['color'] = gdf_merged['bivariate'].map(colors)
    # Fill NaN colors with lightgrey for missing data (alcaldías without pollution)
    gdf_merged['color'] = gdf_merged['color'].fillna('lightgrey')

    # Create static map
    fig_static, ax = plt.subplots(1, 1, figsize=(12, 10))

    gdf_merged.plot(
        color=gdf_merged['color'],
        ax=ax,
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title(f'Bivariate Map: PM₂.₅ and Lung Cancer Mortality\nMexico City, {year}',
                 fontsize=14, fontweight='bold')
    ax.set_axis_off()

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors['Low PM / Low Mort'], label='Low PM / Low Mortality'),
        Patch(facecolor=colors['Low PM / Medium Mort'], label='Low PM / Medium Mortality'),
        Patch(facecolor=colors['Low PM / High Mort'], label='Low PM / High Mortality'),
        Patch(facecolor=colors['Medium PM / Low Mort'], label='Medium PM / Low Mortality'),
        Patch(facecolor=colors['Medium PM / Medium Mort'], label='Medium PM / Medium Mortality'),
        Patch(facecolor=colors['Medium PM / High Mort'], label='Medium PM / High Mortality'),
        Patch(facecolor=colors['High PM / Low Mort'], label='High PM / Low Mortality'),
        Patch(facecolor=colors['High PM / Medium Mort'], label='High PM / Medium Mortality'),
        Patch(facecolor=colors['High PM / High Mort'], label='High PM / High Mortality'),
        Patch(facecolor='lightgrey', label='No data'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(1, 0), fontsize=8)

    plt.tight_layout()
    fig_static.savefig(FIGURES_DIR / f'bivariate_choropleth_{year}.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved bivariate map: bivariate_choropleth_{year}.png")
    plt.close(fig_static)

    return fig_static


def create_all_geospatial_visualizations(df_analysis):
    """
    Create all geospatial visualizations.

    Parameters:
    -----------
    df_analysis : pd.DataFrame
        Analysis dataset

    Returns:
    --------
    dict
        Dictionary of created figures
    """
    print("\n" + "=" * 70)
    print("CREATING GEOSPATIAL VISUALIZATIONS")
    print("=" * 70)

    ensure_directories()

    figures = {}

    # Mortality choropleth for 2020
    figures['mortality_2020'] = create_choropleth_map(df_analysis, year=2020, save_html=True)

    # Mortality choropleth for 2010 (comparison)
    figures['mortality_2010'] = create_choropleth_map(df_analysis, year=2010, save_html=True)

    # PM2.5 choropleth for 2020
    figures['pm25_2020'] = create_pollution_choropleth(df_analysis, year=2020, pollutant='pm25', save_html=True)

    # Bivariate choropleth
    figures['bivariate_2020'] = create_bivariate_choropleth(df_analysis, year=2020, save_html=True)

    print(f"\n  ✓ All geospatial figures saved to: {FIGURES_DIR}")

    return figures


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys
    from .integration import load_analysis_data

    print("=" * 70)
    print("GEOSPATIAL VISUALIZATION TEST")
    print("=" * 70)

    # Load analysis data
    try:
        df, _ = load_analysis_data()
    except Exception as e:
        print(f"  ✗ Error loading analysis data: {e}")
        print("  Run the full pipeline first: python -m src.run_analysis")
        sys.exit(1)

    # Test shapefile loading
    print("\n1. Testing shapefile loading...")
    try:
        gdf = load_cdmx_shapefile('municipal')
        gdf = prepare_alcaldia_shapefile(gdf)
        print(f"  ✓ Successfully loaded {len(gdf)} alcaldías")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        sys.exit(1)

    # Test choropleth creation
    print("\n2. Testing choropleth creation...")
    try:
        fig = create_choropleth_map(df, year=2020, save_html=True)
        print("  ✓ Successfully created choropleth map")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
