"""
Unit tests for harmonization.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path

from src.harmonization import (
    clamp_proportion, prepare_alcaldia_dataframe,
    DEFAULT_PROP_FEMALE, DEFAULT_PROP_MALE, PROP_15_17_OF_15_24
)
from src.utils import ALCALDIA_CODES, CDMX_ENTIDAD


class TestClampProportion(unittest.TestCase):
    """Test clamp_proportion function."""

    def test_within_range(self):
        self.assertEqual(clamp_proportion(0.5), 0.5)
        self.assertEqual(clamp_proportion(0.0), 0.0)
        self.assertEqual(clamp_proportion(1.0), 1.0)

    def test_below_range(self):
        self.assertEqual(clamp_proportion(-0.5), 0.0)

    def test_above_range(self):
        self.assertEqual(clamp_proportion(1.5), 1.0)

    def test_nan_input(self):
        self.assertEqual(clamp_proportion(np.nan), DEFAULT_PROP_FEMALE)


class TestPrepareAlcaldiaDataframe(unittest.TestCase):
    """Test prepare_alcaldia_dataframe function."""

    def setUp(self):
        """Create a sample dataframe mimicking census structure."""
        self.df = pd.DataFrame({
            "ENTIDAD": ["09", "09", "09", "09", "09"],
            "MUN": ["002", "003", "007", "010", "015"],
            "LOC": ["0000", "0000", "0000", "0001", "0000"],
            "P_TOTAL": ["100000", "200000", "300000", "50000", "150000"]
        })

    def test_filter_cdmx_alcaldias(self):
        result = prepare_alcaldia_dataframe(self.df)

        # Should return CDMX alcaldías
        self.assertGreaterEqual(len(result), 4)
        self.assertIn("Azcapotzalco", result["alcaldia"].values)
        self.assertIn("Coyoacan", result["alcaldia"].values)
        self.assertIn("Iztapalapa", result["alcaldia"].values)
        self.assertIn("Cuauhtemoc", result["alcaldia"].values)

    def test_alcaldia_mapping(self):
        result = prepare_alcaldia_dataframe(self.df)

        azcapotzalco_row = result[result["MUN"] == "002"].iloc[0]
        self.assertEqual(azcapotzalco_row["alcaldia"], "Azcapotzalco")

        iztapalapa_row = result[result["MUN"] == "007"].iloc[0]
        self.assertEqual(iztapalapa_row["alcaldia"], "Iztapalapa")

    def test_column_standardization(self):
        result = prepare_alcaldia_dataframe(self.df)

        # Check that key columns exist
        self.assertIn("alcaldia", result.columns)
        self.assertIn("MUN", result.columns)

    def test_entity_filter(self):
        # Add a row from another entity
        df_with_other = pd.concat([
            self.df,
            pd.DataFrame({"ENTIDAD": ["15"], "MUN": ["001"], "LOC": ["0000"], "P_TOTAL": ["50000"]})
        ])

        result = prepare_alcaldia_dataframe(df_with_other)

        # Should have at least the CDMX ones
        self.assertGreaterEqual(len(result), 4)


class TestConstants(unittest.TestCase):
    """Test harmonization constants."""

    def test_default_proportions(self):
        self.assertEqual(DEFAULT_PROP_FEMALE, 0.52)
        self.assertEqual(DEFAULT_PROP_MALE, 0.48)

    def test_prop_15_17_of_15_24(self):
        self.assertEqual(PROP_15_17_OF_15_24, 0.288)


class TestAgeGroupMapping(unittest.TestCase):
    """Test age group mapping functions."""

    def test_harmonized_age_groups_order(self):
        from src.utils import HARMONIZED_AGE_GROUPS
        expected = ['0-4', '5-14', '15-17', '18-24', '25-59', '60+']
        self.assertEqual(HARMONIZED_AGE_GROUPS, expected)

    def test_who_weights_sum(self):
        from src.utils import WHO_WEIGHTS
        total = sum(WHO_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
