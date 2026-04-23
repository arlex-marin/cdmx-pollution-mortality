"""
Unit tests for integration.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import pandas as pd
import numpy as np

from src.integration import (
    map_alcaldia_name, calculate_crude_rates, calculate_age_standardized_rates
)
from src.utils import WHO_WEIGHTS, HARMONIZED_AGE_GROUPS


class TestMapAlcaldiaName(unittest.TestCase):
    """Test map_alcaldia_name function."""
    
    def test_exact_match(self):
        self.assertEqual(map_alcaldia_name("Azcapotzalco"), "Azcapotzalco")
        self.assertEqual(map_alcaldia_name("Iztapalapa"), "Iztapalapa")
    
    def test_accent_variations(self):
        self.assertEqual(map_alcaldia_name("Álvaro Obregón"), "Alvaro Obregon")
        self.assertEqual(map_alcaldia_name("Benito Juárez"), "Benito Juarez")
        self.assertEqual(map_alcaldia_name("Coyoacán"), "Coyoacan")
        self.assertEqual(map_alcaldia_name("Cuauhtémoc"), "Cuauhtemoc")
    
    def test_case_insensitive(self):
        self.assertEqual(map_alcaldia_name("iztapalapa"), "Iztapalapa")
        self.assertEqual(map_alcaldia_name("XOCHIMILCO"), "Xochimilco")
    
    def test_with_spaces(self):
        self.assertEqual(map_alcaldia_name("  Tlalpan  "), "Tlalpan")
        self.assertEqual(map_alcaldia_name("Gustavo A. Madero"), "Gustavo A. Madero")
    
    def test_non_cdmx_municipality(self):
        self.assertIsNone(map_alcaldia_name("Ecatepec"))
        self.assertIsNone(map_alcaldia_name("Nezahualcóyotl"))
        self.assertIsNone(map_alcaldia_name("Naucalpan"))
    
    def test_nan_input(self):
        self.assertIsNone(map_alcaldia_name(np.nan))
        self.assertIsNone(map_alcaldia_name(None))


class TestCalculateCrudeRates(unittest.TestCase):
    """Test calculate_crude_rates function."""
    
    def setUp(self):
        self.df = pd.DataFrame({
            "alcaldia": ["Iztapalapa", "Iztapalapa", "Coyoacan"],
            "year": [2020, 2020, 2020],
            "age_group": ["0-4", "60+", "0-4"],
            "sex": ["Both", "Both", "Both"],
            "population": [100000, 50000, 50000],
            "deaths": [50, 100, 25]
        })
    
    def test_crude_rate_calculation(self):
        result = calculate_crude_rates(self.df)
        
        # First row: 50 deaths / 100,000 population * 100,000 = 50
        self.assertAlmostEqual(result.loc[0, "crude_rate"], 50.0)
        
        # Second row: 100 deaths / 50,000 population * 100,000 = 200
        self.assertAlmostEqual(result.loc[1, "crude_rate"], 200.0)
        
        # Third row: 25 deaths / 50,000 population * 100,000 = 50
        self.assertAlmostEqual(result.loc[2, "crude_rate"], 50.0)
    
    def test_zero_population(self):
        df_zero = self.df.copy()
        df_zero.loc[0, "population"] = 0
        
        result = calculate_crude_rates(df_zero)
        self.assertEqual(result.loc[0, "crude_rate"], 0.0)


class TestCalculateAgeStandardizedRates(unittest.TestCase):
    """Test calculate_age_standardized_rates function."""
    
    def setUp(self):
        """Create a sample dataset for age standardization."""
        self.df = pd.DataFrame({
            "alcaldia": ["Iztapalapa", "Iztapalapa", "Iztapalapa"],
            "year": [2020, 2020, 2020],
            "age_group": ["0-4", "25-59", "60+"],
            "sex": ["Male", "Male", "Male"],
            "population": [100000, 200000, 50000],
            "deaths": [10, 200, 150]
        })
    
    def test_asr_calculation(self):
        result = calculate_age_standardized_rates(self.df)
        
        # Should have entries for "Both" sexes combined and each sex separately
        self.assertGreater(len(result), 0)
        
        # Check that Both sexes combined exists
        both_rows = result[result["sex"] == "Both"]
        self.assertEqual(len(both_rows), 1)
        self.assertEqual(both_rows.iloc[0]["alcaldia"], "Iztapalapa")
        self.assertEqual(both_rows.iloc[0]["year"], 2020)
    
    def test_asr_positive(self):
        result = calculate_age_standardized_rates(self.df)
        both_row = result[result["sex"] == "Both"].iloc[0]
        
        # ASR should be positive
        self.assertGreater(both_row["age_standardized_rate"], 0)
    
    def test_sex_specific_rates(self):
        result = calculate_age_standardized_rates(self.df)
        
        male_rows = result[result["sex"] == "Male"]
        self.assertEqual(len(male_rows), 1)
        self.assertEqual(male_rows.iloc[0]["alcaldia"], "Iztapalapa")


class TestAgeStandardizationFormula(unittest.TestCase):
    """Test the age standardization formula directly."""
    
    def test_direct_standardization(self):
        # Example from WHO documentation
        age_specific_rates = {
            "0-4": 0.001,
            "5-14": 0.002,
            "15-17": 0.005,
            "18-24": 0.010,
            "25-59": 0.050,
            "60+": 0.100
        }
        
        # Calculate ASR
        asr = sum(age_specific_rates[age] * WHO_WEIGHTS[age] for age in HARMONIZED_AGE_GROUPS)
        asr_per_100k = asr * 100000
        
        # Expected value
        expected = (
            0.001 * 0.0886 +
            0.002 * 0.1729 +
            0.005 * 0.0254 +
            0.010 * 0.0702 +
            0.050 * 0.5167 +
            0.100 * 0.1262
        ) * 100000
        
        self.assertAlmostEqual(asr_per_100k, expected)


if __name__ == "__main__":
    unittest.main()