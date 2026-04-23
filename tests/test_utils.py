"""
Unit tests for utils.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json

from src.utils import (
    safe_int, normalize_string, format_number, format_percent, format_pvalue,
    clamp_proportion, save_json, load_json,
    ALCALDIA_CODES, ALCALDIA_NAME_TO_CODE, CDMX_ENTIDAD, CDMX_ENTIDAD_INT,
    HARMONIZED_AGE_GROUPS, WHO_WEIGHTS, LUNG_CANCER_CODES, POLLUTANTS,
    ALCALDIAS_WITH_POLLUTION, ALCALDIAS_WITHOUT_POLLUTION
)


class TestSafeInt(unittest.TestCase):
    """Test safe_int function."""
    
    def test_integer_input(self):
        self.assertEqual(safe_int(42), 42)
        self.assertEqual(safe_int(0), 0)
        self.assertEqual(safe_int(-5), -5)
    
    def test_float_input(self):
        self.assertEqual(safe_int(3.14), 3)
        self.assertEqual(safe_int(9.99), 9)
    
    def test_string_input(self):
        self.assertEqual(safe_int("42"), 42)
        self.assertEqual(safe_int("  123  "), 123)
        self.assertEqual(safe_int("0"), 0)
    
    def test_special_characters(self):
        self.assertEqual(safe_int("*"), 0)
        self.assertEqual(safe_int(""), 0)
        self.assertEqual(safe_int("N/D"), 0)
        self.assertEqual(safe_int("NA"), 0)
    
    def test_nan_input(self):
        self.assertEqual(safe_int(np.nan), 0)
        self.assertEqual(safe_int(None), 0)
        self.assertEqual(safe_int(pd.NA), 0)


class TestNormalizeString(unittest.TestCase):
    """Test normalize_string function."""
    
    def test_accent_removal(self):
        self.assertEqual(normalize_string("Álvaro Obregón"), "alvaro obregon")
        self.assertEqual(normalize_string("Benito Juárez"), "benito juarez")
        self.assertEqual(normalize_string("Coyoacán"), "coyoacan")
        self.assertEqual(normalize_string("Cuauhtémoc"), "cuauhtemoc")
    
    def test_case_conversion(self):
        self.assertEqual(normalize_string("MEXICO CITY"), "mexico city")
        self.assertEqual(normalize_string("Iztapalapa"), "iztapalapa")
    
    def test_whitespace_handling(self):
        self.assertEqual(normalize_string("  Tlalpan  "), "tlalpan")
        self.assertEqual(normalize_string("\tXochimilco\n"), "xochimilco")
    
    def test_nan_input(self):
        self.assertEqual(normalize_string(np.nan), "")
        self.assertEqual(normalize_string(None), "")


class TestFormatFunctions(unittest.TestCase):
    """Test formatting functions."""
    
    def test_format_number(self):
        self.assertEqual(format_number(1000), "1,000")
        self.assertEqual(format_number(1234567), "1,234,567")
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(-5000), "-5,000")
    
    def test_format_percent(self):
        self.assertEqual(format_percent(25, 100), "25.00%")
        self.assertEqual(format_percent(1, 3), "33.33%")
        self.assertEqual(format_percent(0, 10), "0.00%")
        self.assertEqual(format_percent(5, 0), "0.00%")
    
    def test_format_pvalue(self):
        self.assertEqual(format_pvalue(0.0001), "p < 0.001 ***")
        self.assertEqual(format_pvalue(0.005), "p = 0.005 **")
        self.assertEqual(format_pvalue(0.03), "p = 0.030 *")
        self.assertEqual(format_pvalue(0.15), "p = 0.150")
        self.assertEqual(format_pvalue(0.001), "p = 0.001 **")


class TestClampProportion(unittest.TestCase):
    """Test clamp_proportion function."""
    
    def test_within_range(self):
        self.assertEqual(clamp_proportion(0.5), 0.5)
        self.assertEqual(clamp_proportion(0.0), 0.0)
        self.assertEqual(clamp_proportion(1.0), 1.0)
    
    def test_below_range(self):
        self.assertEqual(clamp_proportion(-0.5), 0.0)
        self.assertEqual(clamp_proportion(-10), 0.0)
    
    def test_above_range(self):
        self.assertEqual(clamp_proportion(1.5), 1.0)
        self.assertEqual(clamp_proportion(100), 1.0)
    
    def test_nan_input(self):
        self.assertAlmostEqual(clamp_proportion(np.nan), 0.52)  # DEFAULT_PROP_FEMALE


class TestJsonFunctions(unittest.TestCase):
    """Test JSON save/load functions."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.json"
    
    def test_save_and_load_json(self):
        data = {"name": "Test", "values": [1, 2, 3], "nested": {"key": "value"}}
        save_json(data, self.test_file)
        
        self.assertTrue(self.test_file.exists())
        
        loaded = load_json(self.test_file)
        self.assertEqual(loaded, data)
    
    def test_save_json_with_numpy_types(self):
        data = {"int": np.int64(42), "float": np.float64(3.14)}
        save_json(data, self.test_file)
        
        loaded = load_json(self.test_file)
        self.assertEqual(loaded["int"], 42)
        self.assertAlmostEqual(loaded["float"], 3.14)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_alcaldia_codes(self):
        self.assertEqual(len(ALCALDIA_CODES), 16)
        self.assertEqual(ALCALDIA_CODES["007"], "Iztapalapa")
        self.assertEqual(ALCALDIA_CODES["010"], "Alvaro Obregon")
    
    def test_alcaldia_name_to_code(self):
        self.assertEqual(ALCALDIA_NAME_TO_CODE["Iztapalapa"], "007")
        self.assertEqual(ALCALDIA_NAME_TO_CODE["Coyoacan"], "003")
    
    def test_cdmx_entity_codes(self):
        self.assertEqual(CDMX_ENTIDAD, "09")
        self.assertEqual(CDMX_ENTIDAD_INT, 9)
    
    def test_harmonized_age_groups(self):
        self.assertEqual(len(HARMONIZED_AGE_GROUPS), 6)
        self.assertIn("0-4", HARMONIZED_AGE_GROUPS)
        self.assertIn("60+", HARMONIZED_AGE_GROUPS)
    
    def test_who_weights(self):
        self.assertEqual(len(WHO_WEIGHTS), 6)
        self.assertAlmostEqual(sum(WHO_WEIGHTS.values()), 1.0, places=4)
        self.assertAlmostEqual(WHO_WEIGHTS["0-4"], 0.0886)
    
    def test_lung_cancer_codes(self):
        self.assertEqual(LUNG_CANCER_CODES, ["C33", "C34"])
    
    def test_pollutants(self):
        self.assertEqual(len(POLLUTANTS), 6)
        self.assertIn("pm25", POLLUTANTS)
        self.assertIn("o3", POLLUTANTS)
    
    def test_alcaldias_with_pollution(self):
        self.assertEqual(len(ALCALDIAS_WITH_POLLUTION), 14)
        self.assertIn("Iztapalapa", ALCALDIAS_WITH_POLLUTION)
        self.assertIn("Cuauhtemoc", ALCALDIAS_WITH_POLLUTION)
    
    def test_alcaldias_without_pollution(self):
        self.assertEqual(len(ALCALDIAS_WITHOUT_POLLUTION), 2)
        self.assertIn("La Magdalena Contreras", ALCALDIAS_WITHOUT_POLLUTION)
        self.assertIn("Tlahuac", ALCALDIAS_WITHOUT_POLLUTION)


if __name__ == "__main__":
    unittest.main()