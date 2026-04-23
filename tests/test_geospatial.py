"""
Unit tests for geospatial.py module.

Author: Arlex Marín
Date: April 2026
Updated: April 21, 2026 - Geopandas now required
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path

# Geopandas is now a required dependency
import geopandas as gpd
from shapely.geometry import Polygon

from src.geospatial import (
    get_municipal_shapefile_path, get_entity_shapefile_path,
    prepare_alcaldia_shapefile, create_choropleth_map,
    create_pollution_choropleth, create_bivariate_choropleth
)


class TestShapefilePaths(unittest.TestCase):
    """Test shapefile path functions."""

    def test_get_municipal_shapefile_path(self):
        """Test municipal shapefile path returns a Path object."""
        path = get_municipal_shapefile_path()
        self.assertIsInstance(path, Path)
        path_str = str(path).lower()
        self.assertTrue('09mun' in path_str or 'municipal' in path_str or 'shapefile' in path_str)

    def test_get_entity_shapefile_path(self):
        """Test entity shapefile path returns a Path object."""
        path = get_entity_shapefile_path()
        self.assertIsInstance(path, Path)
        path_str = str(path).lower()
        self.assertTrue('09ent' in path_str or 'entity' in path_str or 'shapefile' in path_str)


class TestLoadShapefile(unittest.TestCase):
    """Test shapefile loading functions."""

    def test_load_cdmx_shapefile_municipal(self):
        """Test loading municipal shapefile."""
        from src.geospatial import load_cdmx_shapefile

        # Skip if shapefile doesn't exist
        shapefile_path = get_municipal_shapefile_path()
        if not shapefile_path.exists():
            self.skipTest(f"Shapefile not found: {shapefile_path}")

        gdf = load_cdmx_shapefile('municipal')
        self.assertIsInstance(gdf, gpd.GeoDataFrame)
        self.assertGreater(len(gdf), 0)
        self.assertIn('geometry', gdf.columns)

    def test_load_cdmx_shapefile_entity(self):
        """Test loading entity shapefile."""
        from src.geospatial import load_cdmx_shapefile

        # Skip if shapefile doesn't exist
        shapefile_path = get_entity_shapefile_path()
        if not shapefile_path.exists():
            self.skipTest(f"Shapefile not found: {shapefile_path}")

        gdf = load_cdmx_shapefile('entity')
        self.assertIsInstance(gdf, gpd.GeoDataFrame)
        self.assertGreater(len(gdf), 0)
        self.assertIn('geometry', gdf.columns)


class TestPrepareAlcaldiaShapefile(unittest.TestCase):
    """Test prepare_alcaldia_shapefile function."""

    def test_function_exists(self):
        """Test that the function is defined."""
        self.assertTrue(callable(prepare_alcaldia_shapefile))

    def test_prepare_with_sample_data(self):
        """Test with a sample GeoDataFrame."""
        # Create a simple GeoDataFrame
        gdf = gpd.GeoDataFrame({
            "CVE_MUN": ["002", "003", "007", "010", "015"],
            "NOM_MUN": ["Azcapotzalco", "Coyoacán", "Iztapalapa", "Álvaro Obregón", "Cuauhtémoc"],
            "geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])] * 5
        })

        result = prepare_alcaldia_shapefile(gdf)

        self.assertIsInstance(result, gpd.GeoDataFrame)
        self.assertIn("alcaldia", result.columns)
        self.assertIn("alcaldia_code", result.columns)
        self.assertEqual(len(result), 5)

    def test_prepare_filters_non_cdmx(self):
        """Test that non-CDMX municipalities are filtered out."""
        # Create GeoDataFrame with mixed municipalities
        gdf = gpd.GeoDataFrame({
            "CVE_MUN": ["002", "003", "999", "007"],
            "NOM_MUN": ["Azcapotzalco", "Coyoacán", "Other", "Iztapalapa"],
            "geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])] * 4
        })

        result = prepare_alcaldia_shapefile(gdf)

        # Should only keep valid CDMX alcaldías
        self.assertEqual(len(result), 3)
        self.assertIn("Azcapotzalco", result["alcaldia"].values)
        self.assertIn("Coyoacan", result["alcaldia"].values)
        self.assertIn("Iztapalapa", result["alcaldia"].values)
        self.assertNotIn("Other", result["alcaldia"].values)


class TestChoroplethCreation(unittest.TestCase):
    """Test choropleth creation functions."""

    def setUp(self):
        """Create a sample analysis dataset."""
        self.df = pd.DataFrame({
            "alcaldia": ["Iztapalapa", "Coyoacan", "Cuauhtemoc", "Benito Juarez",
                        "Azcapotzalco", "Gustavo A. Madero", "Miguel Hidalgo", "Tlalpan"],
            "year": [2020] * 8,
            "sex": ["Both"] * 8,
            "age_standardized_rate": [10.5, 8.3, 12.1, 9.7, 16.4, 10.6, 18.3, 10.2],
            "crude_rate": [6.2, 5.1, 7.8, 5.9, 10.2, 6.4, 11.5, 5.9],
            "pm25": [20.1, 16.5, 21.1, 16.9, 18.5, 19.4, 20.6, 19.9]
        })

    def test_data_structure(self):
        """Test sample data has correct structure."""
        self.assertEqual(len(self.df), 8)
        self.assertIn("age_standardized_rate", self.df.columns)
        self.assertIn("pm25", self.df.columns)
        self.assertIn("crude_rate", self.df.columns)

    def test_rates_positive(self):
        """Test all rates are positive."""
        self.assertTrue((self.df["age_standardized_rate"] > 0).all())
        self.assertTrue((self.df["crude_rate"] > 0).all())
        self.assertTrue((self.df["pm25"] > 0).all())

    def test_create_choropleth_map_function_exists(self):
        """Test that choropleth map function exists."""
        self.assertTrue(callable(create_choropleth_map))

    def test_create_pollution_choropleth_function_exists(self):
        """Test that pollution choropleth function exists."""
        self.assertTrue(callable(create_pollution_choropleth))

    def test_create_bivariate_choropleth_function_exists(self):
        """Test that bivariate choropleth function exists."""
        self.assertTrue(callable(create_bivariate_choropleth))


class TestGeospatialImports(unittest.TestCase):
    """Test that all geospatial functions are properly exposed."""

    def test_geospatial_module_imports(self):
        """Test importing from geospatial module."""
        from src.geospatial import (
            load_cdmx_shapefile,
            prepare_alcaldia_shapefile,
            create_choropleth_map,
            create_pollution_choropleth,
            create_bivariate_choropleth,
            create_all_geospatial_visualizations
        )

        self.assertTrue(callable(load_cdmx_shapefile))
        self.assertTrue(callable(prepare_alcaldia_shapefile))
        self.assertTrue(callable(create_choropleth_map))
        self.assertTrue(callable(create_pollution_choropleth))
        self.assertTrue(callable(create_bivariate_choropleth))
        self.assertTrue(callable(create_all_geospatial_visualizations))


if __name__ == "__main__":
    unittest.main()
