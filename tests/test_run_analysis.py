"""
Unit tests for run_analysis.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


class TestRunAnalysisImports(unittest.TestCase):
    """Test that all modules can be imported."""

    def test_import_utils(self):
        try:
            from src import utils
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import utils: {e}")

    def test_import_data_validation(self):
        try:
            from src import data_validation
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import data_validation: {e}")

    def test_import_harmonization(self):
        try:
            from src import harmonization
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import harmonization: {e}")

    def test_import_mortality_processing(self):
        try:
            from src import mortality_processing
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import mortality_processing: {e}")

    def test_import_integration(self):
        try:
            from src import integration
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import integration: {e}")

    def test_import_analysis(self):
        try:
            from src import analysis
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import analysis: {e}")

    def test_import_visualization(self):
        try:
            from src import visualization
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import visualization: {e}")

    def test_import_geospatial(self):
        try:
            from src import geospatial
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import geospatial: {e}")

    def test_import_run_analysis(self):
        try:
            from src import run_analysis
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import run_analysis: {e}")


class TestConstants(unittest.TestCase):
    """Test that constants are properly defined."""

    def test_alcaldia_count(self):
        from src.utils import ALCALDIA_CODES
        self.assertEqual(len(ALCALDIA_CODES), 16)

    def test_age_groups(self):
        from src.utils import HARMONIZED_AGE_GROUPS
        self.assertEqual(len(HARMONIZED_AGE_GROUPS), 6)

    def test_pollutants(self):
        from src.utils import POLLUTANTS
        self.assertEqual(len(POLLUTANTS), 6)
        self.assertIn("pm25", POLLUTANTS)


class TestDirectoryStructure(unittest.TestCase):
    """Test that required directories exist or can be created."""

    def test_ensure_directories(self):
        from src import ensure_directories
        result = ensure_directories()
        self.assertTrue(result)

    def test_paths_defined(self):
        from src import (
            DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR,
            OUTPUTS_DIR, LOGS_DIR, DOCS_DIR,
            CENSUS_RAW_DIR, MORTALITY_RAW_DIR, POLLUTION_RAW_DIR,
            POPULATION_PROCESSED_DIR, MORTALITY_PROCESSED_DIR, INTEGRATED_PROCESSED_DIR,
            FIGURES_DIR, TABLES_DIR, MODELS_DIR
        )

        # All paths should be Path objects
        self.assertIsInstance(DATA_DIR, Path)
        self.assertIsInstance(FIGURES_DIR, Path)
        self.assertIsInstance(CENSUS_RAW_DIR, Path)


if __name__ == "__main__":
    unittest.main()
