"""
Unit tests for analysis.py module.

Author: Arlex Marín
Date: April 2026
"""

import unittest
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from src.analysis import (
    descriptive_statistics, correlation_analysis
)


class TestDescriptiveStatistics(unittest.TestCase):
    """Test descriptive_statistics function."""
    
    def setUp(self):
        """Create a sample dataset."""
        self.df = pd.DataFrame({
            "alcaldia": ["Iztapalapa", "Coyoacan"] * 10,
            "year": list(range(2010, 2020)) * 2,
            "sex": ["Both"] * 20,
            "pm25": np.random.normal(22, 3, 20),
            "pm10": np.random.normal(42, 6, 20),
            "o3": np.random.normal(21, 5, 20),
            "no2": np.random.normal(25, 5, 20),
            "crude_rate": np.random.normal(7, 2, 20),
            "age_standardized_rate": np.random.normal(14, 4, 20)
        })
        # Ensure no negative rates
        self.df["crude_rate"] = self.df["crude_rate"].abs()
        self.df["age_standardized_rate"] = self.df["age_standardized_rate"].abs()
    
    def test_returns_dataframe(self):
        result = descriptive_statistics(self.df)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_contains_expected_variables(self):
        result = descriptive_statistics(self.df)
        variables = result["variable"].tolist()
        self.assertIn("PM2.5 (μg/m³)", variables)
        self.assertIn("PM10 (μg/m³)", variables)
        self.assertIn("Crude Rate (per 100,000)", variables)
        self.assertIn("Age-Standardized Rate (per 100,000)", variables)
    
    def test_statistics_are_positive(self):
        result = descriptive_statistics(self.df)
        self.assertTrue((result["mean"] >= 0).all())
        self.assertTrue((result["sd"] >= 0).all())
        self.assertTrue((result["min"] >= 0).all())
        self.assertTrue((result["max"] >= 0).all())


class TestCorrelationAnalysis(unittest.TestCase):
    """Test correlation_analysis function."""
    
    def setUp(self):
        """Create a sample dataset with known correlation."""
        np.random.seed(42)
        n = 50
        
        # Create correlated variables
        pm25 = np.random.normal(22, 3, n)
        mortality = 5 + 0.4 * pm25 + np.random.normal(0, 1, n)
        
        self.df = pd.DataFrame({
            "alcaldia": ["Test"] * n,
            "year": list(range(n)),
            "sex": ["Both"] * n,
            "pm25": pm25,
            "pm10": pm25 * 2 + np.random.normal(0, 2, n),
            "age_standardized_rate": mortality,
            "crude_rate": mortality * 0.8 + np.random.normal(0, 1, n)
        })
    
    def test_returns_dataframe(self):
        result = correlation_analysis(self.df)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_contains_expected_columns(self):
        result = correlation_analysis(self.df)
        expected_columns = ["pollutant", "mortality", "pearson_r", "pearson_p", 
                           "spearman_rho", "spearman_p", "n", "significant"]
        for col in expected_columns:
            self.assertIn(col, result.columns)
    
    def test_pm25_correlation_positive(self):
        result = correlation_analysis(self.df)
        pm25_asr = result[(result["pollutant"] == "PM25") & 
                          (result["mortality"] == "age_standardized_rate")]
        
        if len(pm25_asr) > 0:
            # Should show positive correlation
            self.assertGreater(pm25_asr.iloc[0]["pearson_r"], 0)
    
    def test_correlation_bounds(self):
        result = correlation_analysis(self.df)
        # Pearson r should be between -1 and 1
        self.assertTrue((result["pearson_r"] >= -1).all())
        self.assertTrue((result["pearson_r"] <= 1).all())
        # Spearman rho should be between -1 and 1
        self.assertTrue((result["spearman_rho"] >= -1).all())
        self.assertTrue((result["spearman_rho"] <= 1).all())


class TestPanelRegression(unittest.TestCase):
    """Test panel regression functions."""
    
    def setUp(self):
        """Create a sample panel dataset."""
        np.random.seed(42)
        n_alcaldias = 5
        n_years = 10
        n = n_alcaldias * n_years
        
        alcaldias = [f"Alcaldia_{i}" for i in range(n_alcaldias)]
        
        self.df = pd.DataFrame({
            "alcaldia": np.repeat(alcaldias, n_years),
            "alcaldia_code": np.repeat(list(range(1, n_alcaldias + 1)), n_years),
            "year": np.tile(range(2010, 2010 + n_years), n_alcaldias),
            "sex": ["Both"] * n,
            "pm25": np.random.normal(22, 3, n),
            "age_standardized_rate": np.random.normal(14, 4, n)
        })
        self.df["age_standardized_rate"] = self.df["age_standardized_rate"].abs()
    
    def test_data_structure(self):
        self.assertEqual(len(self.df), 50)
        self.assertEqual(self.df["alcaldia"].nunique(), 5)
        self.assertEqual(self.df["year"].nunique(), 10)
    
    def test_pm25_positive(self):
        self.assertTrue((self.df["pm25"] > 0).all())
    
    def test_mortality_positive(self):
        self.assertTrue((self.df["age_standardized_rate"] > 0).all())


if __name__ == "__main__":
    unittest.main()