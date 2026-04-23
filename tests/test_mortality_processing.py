"""
Unit tests for mortality_processing.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import pandas as pd
import numpy as np

from src.mortality_processing import (
    map_edad_to_age_group, map_sexo_to_sex
)


class TestMapEdadToAgeGroup(unittest.TestCase):
    """Test map_edad_to_age_group function."""
    
    def test_under_one_year(self):
        # Minutes, hours, days, months should all map to 0-4
        self.assertEqual(map_edad_to_age_group(1001), "0-4")  # 1 minute
        self.assertEqual(map_edad_to_age_group(1097), "0-4")  # hours
        self.assertEqual(map_edad_to_age_group(2001), "0-4")  # 1 day
        self.assertEqual(map_edad_to_age_group(3001), "0-4")  # 1 month
        self.assertEqual(map_edad_to_age_group(3999), "0-4")  # < 4000
    
    def test_years_0_to_4(self):
        self.assertEqual(map_edad_to_age_group(4001), "0-4")   # 1 year
        self.assertEqual(map_edad_to_age_group(4004), "0-4")   # 4 years
    
    def test_years_5_to_14(self):
        self.assertEqual(map_edad_to_age_group(4005), "5-14")  # 5 years
        self.assertEqual(map_edad_to_age_group(4010), "5-14")  # 10 years
        self.assertEqual(map_edad_to_age_group(4014), "5-14")  # 14 years
    
    def test_years_15_to_17(self):
        self.assertEqual(map_edad_to_age_group(4015), "15-17")  # 15 years
        self.assertEqual(map_edad_to_age_group(4017), "15-17")  # 17 years
    
    def test_years_18_to_24(self):
        self.assertEqual(map_edad_to_age_group(4018), "18-24")  # 18 years
        self.assertEqual(map_edad_to_age_group(4020), "18-24")  # 20 years
        self.assertEqual(map_edad_to_age_group(4024), "18-24")  # 24 years
    
    def test_years_25_to_59(self):
        self.assertEqual(map_edad_to_age_group(4025), "25-59")  # 25 years
        self.assertEqual(map_edad_to_age_group(4040), "25-59")  # 40 years
        self.assertEqual(map_edad_to_age_group(4059), "25-59")  # 59 years
    
    def test_years_60_plus(self):
        self.assertEqual(map_edad_to_age_group(4060), "60+")    # 60 years
        self.assertEqual(map_edad_to_age_group(4080), "60+")    # 80 years
        self.assertEqual(map_edad_to_age_group(4120), "60+")    # 120 years
    
    def test_invalid_input(self):
        self.assertIsNone(map_edad_to_age_group(np.nan))
        self.assertIsNone(map_edad_to_age_group(None))
        self.assertIsNone(map_edad_to_age_group("invalid"))
        self.assertIsNone(map_edad_to_age_group(4998))  # Unspecified age


class TestMapSexoToSex(unittest.TestCase):
    """Test map_sexo_to_sex function."""
    
    def test_male(self):
        self.assertEqual(map_sexo_to_sex(1), "Male")
        self.assertEqual(map_sexo_to_sex("1"), "Male")
        self.assertEqual(map_sexo_to_sex(1.0), "Male")
    
    def test_female(self):
        self.assertEqual(map_sexo_to_sex(2), "Female")
        self.assertEqual(map_sexo_to_sex("2"), "Female")
        self.assertEqual(map_sexo_to_sex(2.0), "Female")
    
    def test_invalid_input(self):
        self.assertIsNone(map_sexo_to_sex(np.nan))
        self.assertIsNone(map_sexo_to_sex(None))
        self.assertIsNone(map_sexo_to_sex(9))
        self.assertIsNone(map_sexo_to_sex("invalid"))
        self.assertIsNone(map_sexo_to_sex(0))
        self.assertIsNone(map_sexo_to_sex(3))


if __name__ == "__main__":
    unittest.main()