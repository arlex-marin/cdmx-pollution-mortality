"""
End-to-end integration tests for the CDMX pollution-mortality pipeline.

Uses synthetic data fixtures to test the full pipeline flow without
requiring real data files. Tests cover:

1. Alcaldía name mapping (all known variations)
2. Population-mortality merge
3. Crude rate calculation
4. Age-standardized rates (WHO direct method)
5. Pollution merge and analytical dataset creation
6. Statistical pipeline (descriptive → correlation → regression)
7. Sex-specific analysis
8. Full pipeline end-to-end (miniature dataset)

Author: Arlex Marín
Date: April 2026
Updated: April 23, 2026 - Initial creation
"""

import unittest
import tempfile
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# SYNTHETIC DATA FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

SYNTHETIC_POPULATION = pd.DataFrame(
    {
        "alcaldia": ["Iztapalapa", "Coyoacan", "Cuauhtemoc"] * 12,
        "alcaldia_code": ["007", "003", "015"] * 12,
        "year": sorted([2020, 2021] * 18),
        "age_group": (["0-4", "5-14", "15-17", "18-24", "25-59", "60+"] * 6),
        "sex": (["Female"] * 18 + ["Male"] * 18),
        "population": [
            50000,
            80000,
            30000,
            60000,
            200000,
            40000,
            180000,
            250000,
            120000,
            200000,
            600000,
            150000,
        ]
        * 3,
    }
)

# Fixture WITH deaths column (for rate calculation tests)
SYNTHETIC_POP_WITH_DEATHS = SYNTHETIC_POPULATION.copy()
SYNTHETIC_POP_WITH_DEATHS["deaths"] = 0  # Zero deaths by default

SYNTHETIC_MORTALITY = pd.DataFrame(
    {
        "alcaldia": ["Iztapalapa", "Coyoacan", "Cuauhtemoc", "Iztapalapa"] * 3,
        "alcaldia_code": ["007", "003", "015", "007"] * 3,
        "year": [2020] * 6 + [2021] * 6,
        "age_group": (["0-4", "25-59", "60+", "25-59"] * 3),
        "sex": (["Female", "Male", "Male", "Female"] * 3),
        "deaths": [2, 15, 20, 8] * 3,
    }
)

SYNTHETIC_POLLUTION = pd.DataFrame(
    {
        "alcaldía": [
            "Iztapalapa",
            "Coyoacán",
            "Cuauhtémoc",
            "Iztapalapa",
            "Coyoacán",
            "Cuauhtémoc",
        ],
        "year": [2020, 2020, 2020, 2021, 2021, 2021],
        "pm25": [22.0, 16.0, 21.0, 20.0, 15.0, 19.0],
        "pm10": [42.0, 30.0, 38.0, 40.0, 28.0, 36.0],
        "o3": [20.0, 18.0, 22.0, 19.0, 17.0, 21.0],
        "no2": [28.0, 20.0, 26.0, 25.0, 18.0, 24.0],
        "so2": [8.0, 4.0, 6.0, 7.0, 3.0, 5.0],
        "co": [3.0, 1.5, 2.0, 2.8, 1.3, 1.8],
    }
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


class TestAlcaldiaNameMapping(unittest.TestCase):
    """Test alcaldía name mapping with all known variations."""

    @classmethod
    def setUpClass(cls):
        from src.integration import map_alcaldia_name as _mapper

        cls._mapper = staticmethod(_mapper)

    def setUp(self):
        from src.integration import map_alcaldia_name

        self.mapper = map_alcaldia_name

    def test_exact_matches(self):
        for name in ["Azcapotzalco", "Iztapalapa", "Coyoacan", "Cuauhtemoc"]:
            self.assertEqual(self.mapper(name), name)

    def test_accent_variations(self):
        self.assertEqual(self.mapper("Álvaro Obregón"), "Alvaro Obregon")
        self.assertEqual(self.mapper("Benito Juárez"), "Benito Juarez")
        self.assertEqual(self.mapper("Coyoacán"), "Coyoacan")
        self.assertEqual(self.mapper("Cuauhtémoc"), "Cuauhtemoc")
        self.assertEqual(self.mapper("Tláhuac"), "Tlahuac")

    def test_case_insensitive(self):
        self.assertEqual(self.mapper("iztapalapa"), "Iztapalapa")
        self.assertEqual(self.mapper("XOCHIMILCO"), "Xochimilco")

    def test_abbreviations(self):
        self.assertEqual(self.mapper("Cuajimalpa"), "Cuajimalpa de Morelos")
        self.assertEqual(self.mapper("Gustavo A. Madero"), "Gustavo A. Madero")
        self.assertEqual(self.mapper("Gustavo Madero"), "Gustavo A. Madero")
        self.assertEqual(self.mapper("Magdalena Contreras"), "La Magdalena Contreras")

    def test_non_cdmx_returns_none(self):
        self.assertIsNone(self.mapper("Ecatepec"))
        self.assertIsNone(self.mapper("Naucalpan"))

    def test_nan_returns_none(self):
        self.assertIsNone(self.mapper(np.nan))
        self.assertIsNone(self.mapper(None))


class TestPopulationMortalityMerge(unittest.TestCase):
    """Test merge_population_mortality with synthetic data."""

    def setUp(self):
        from src.integration import merge_population_mortality

        self.merger = merge_population_mortality

    def test_merge_completes(self):
        result = self.merger(SYNTHETIC_POPULATION.copy(), SYNTHETIC_MORTALITY.copy())
        self.assertIsInstance(result, pd.DataFrame)

    def test_merge_adds_alcaldia_code(self):
        result = self.merger(SYNTHETIC_POPULATION.copy(), SYNTHETIC_MORTALITY.copy())
        self.assertIn("alcaldia_code", result.columns)

    def test_merge_fills_missing_deaths_with_zero(self):
        result = self.merger(SYNTHETIC_POPULATION.copy(), SYNTHETIC_MORTALITY.copy())
        self.assertFalse(result["deaths"].isna().any())
        self.assertEqual(result["deaths"].dtype, np.int64)

    def test_merge_preserves_population(self):
        pop = SYNTHETIC_POPULATION.copy()
        result = self.merger(pop, SYNTHETIC_MORTALITY.copy())
        # Each original population row should exist in the result
        # (population preserved after left join)
        self.assertGreaterEqual(len(result), len(pop))
        self.assertTrue(result["population"].notna().all())

    def test_merge_fails_on_missing_column(self):
        bad_pop = SYNTHETIC_POPULATION.drop(columns=["age_group"])
        with self.assertRaises(ValueError):
            self.merger(bad_pop, SYNTHETIC_MORTALITY.copy())


class TestCrudeRates(unittest.TestCase):
    """Test calculate_crude_rates with synthetic data."""

    def setUp(self):
        from src.integration import calculate_crude_rates

        self.calculator = calculate_crude_rates

    def test_crude_rate_per_100k(self):
        df = pd.DataFrame(
            {
                "population": [100000, 50000, 10000],
                "deaths": [100, 50, 10],
            }
        )
        result = self.calculator(df)
        self.assertAlmostEqual(result.loc[0, "crude_rate"], 100.0)
        self.assertAlmostEqual(result.loc[1, "crude_rate"], 100.0)
        self.assertAlmostEqual(result.loc[2, "crude_rate"], 100.0)

    def test_zero_population_returns_zero_rate(self):
        df = pd.DataFrame({"population": [0, 100], "deaths": [5, 1]})
        result = self.calculator(df)
        self.assertEqual(result.loc[0, "crude_rate"], 0.0)

    def test_output_has_crude_rate_column(self):
        result = self.calculator(SYNTHETIC_POP_WITH_DEATHS.copy())
        self.assertIn("crude_rate", result.columns)


class TestAgeStandardizedRates(unittest.TestCase):
    """Test age-standardized rates with synthetic data."""

    def setUp(self):
        from src.integration import calculate_age_standardized_rates

        self.calculator = calculate_age_standardized_rates

    def test_asr_creates_both_sex_rows(self):
        result = self.calculator(SYNTHETIC_POP_WITH_DEATHS.copy())
        both_rows = result[result["sex"] == "Both"]
        self.assertGreater(len(both_rows), 0)

    def test_asr_creates_sex_specific_rows(self):
        result = self.calculator(SYNTHETIC_POP_WITH_DEATHS.copy())
        self.assertIn("Male", result["sex"].values)
        self.assertIn("Female", result["sex"].values)

    def test_asr_is_positive(self):
        df = SYNTHETIC_POP_WITH_DEATHS.copy()
        df["deaths"] = [1] * len(df)
        result = self.calculator(df)
        both = result[result["sex"] == "Both"]
        if len(both) > 0:
            self.assertTrue((both["age_standardized_rate"] >= 0).all())

    def test_asr_has_expected_columns(self):
        result = self.calculator(SYNTHETIC_POP_WITH_DEATHS.copy())
        for col in [
            "alcaldia",
            "year",
            "sex",
            "population",
            "deaths",
            "crude_rate",
            "age_standardized_rate",
        ]:
            self.assertIn(col, result.columns)


class TestPollutionMerge(unittest.TestCase):
    """Test pollution data merge with synthetic data."""

    def setUp(self):
        from src.integration import map_alcaldia_name, merge_with_pollution

        self.mapper = map_alcaldia_name
        self.merger = merge_with_pollution

    def _make_mortality_data(self):
        return pd.DataFrame(
            {
                "alcaldia": ["Iztapalapa", "Coyoacan", "Cuauhtemoc"] * 2,
                "year": [2020, 2020, 2020, 2021, 2021, 2021],
                "sex": ["Both"] * 6,
                "population": [500000, 400000, 300000] * 2,
                "deaths": [50, 30, 40, 45, 28, 38],
                "crude_rate": [10.0, 7.5, 13.3, 9.0, 7.0, 12.7],
                "age_standardized_rate": [12.0, 8.0, 14.0, 11.0, 7.5, 13.5],
            }
        )

    def test_merge_maps_alcaldia_names(self):
        mort = self._make_mortality_data()
        poll = SYNTHETIC_POLLUTION.copy()
        poll["alcaldia"] = poll["alcaldía"].apply(self.mapper)

        result = self.merger(mort, poll)
        records_with_pm25 = result["pm25"].notna().sum()
        self.assertGreater(records_with_pm25, 0)

    def test_merge_excludes_outside_analysis_years(self):
        mort = self._make_mortality_data()
        mort.loc[0, "year"] = 1990  # Before analysis window
        poll = SYNTHETIC_POLLUTION.copy()
        poll["alcaldia"] = poll["alcaldía"].apply(self.mapper)

        result = self.merger(mort, poll)
        # 1990 row should be excluded
        self.assertNotIn(1990, result["year"].values)

    def test_merge_reports_excluded_alcaldias(self):
        mort = self._make_mortality_data()
        poll = SYNTHETIC_POLLUTION.copy()
        poll["alcaldia"] = poll["alcaldía"].apply(self.mapper)

        result = self.merger(mort, poll)
        self.assertIn("pm25", result.columns)


class TestAnalysisPipeline(unittest.TestCase):
    """Test the statistical analysis pipeline end-to-end."""

    def _make_analysis_df(self):
        """Create a synthetic analysis dataset with known structure."""
        np.random.seed(42)
        n = 30  # 3 alcaldías × 10 years
        df = pd.DataFrame(
            {
                "alcaldia": ["Iztapalapa", "Coyoacan", "Cuauhtemoc"] * 10,
                "alcaldia_code": [7, 3, 15] * 10,
                "year": sorted(list(range(2010, 2020)) * 3),
                "sex": ["Both"] * n,
                "pm25": np.random.normal(22, 3, n),
                "pm10": np.random.normal(42, 6, n),
                "o3": np.random.normal(21, 5, n),
                "no2": np.random.normal(25, 5, n),
                "so2": np.random.normal(7, 4, n),
                "co": np.random.normal(2.8, 2, n),
                "crude_rate": np.abs(np.random.normal(7, 2, n)),
                "age_standardized_rate": np.abs(np.random.normal(14, 4, n)),
            }
        )
        return df

    def test_descriptive_statistics(self):
        from src.analysis import descriptive_statistics

        df = self._make_analysis_df()
        result = descriptive_statistics(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)

    def test_correlation_analysis(self):
        from src.analysis import correlation_analysis

        df = self._make_analysis_df()
        result = correlation_analysis(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("pearson_r", result.columns)
        self.assertIn("spearman_rho", result.columns)

    def test_panel_regression(self):
        from src.analysis import panel_regression

        df = self._make_analysis_df()
        models, results = panel_regression(df)

        self.assertIn("pooled_ols", models)
        self.assertIn("alcaldia_fe", models)
        self.assertIn("twoway_fe", models)

        # All models should produce coefficients
        for name in ["pooled_ols", "alcaldia_fe", "twoway_fe"]:
            self.assertIn("pm25_10", models[name].params.index)

    def test_sex_specific_analysis(self):
        from src.analysis import sex_specific_analysis

        # Create sex-specific data
        n = 30
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "alcaldia": (["Iztapalapa", "Coyoacan", "Cuauhtemoc"] * 10),
                "alcaldia_code": ([7, 3, 15] * 10),
                "year": sorted(list(range(2010, 2020)) * 3),
                "sex": (["Male"] * 15 + ["Female"] * 15),
                "pm25": np.random.normal(22, 3, n),
                "age_standardized_rate": np.abs(np.random.normal(14, 4, n)),
            }
        )
        sex_models, sex_results = sex_specific_analysis(df)
        self.assertIn("Male", sex_models)
        self.assertIn("Female", sex_models)


class TestEndToEndPipeline(unittest.TestCase):
    """Minimal end-to-end pipeline test with synthetic data."""

    def test_full_pipeline_with_synthetic_data(self):
        """Run the complete analysis pipeline on synthetic data."""
        from src.integration import (
            merge_population_mortality,
            calculate_crude_rates,
            calculate_age_standardized_rates,
        )
        from src.analysis import descriptive_statistics, correlation_analysis

        # 1. Merge population and mortality
        merged = merge_population_mortality(
            SYNTHETIC_POPULATION.copy(), SYNTHETIC_MORTALITY.copy()
        )
        self.assertIsInstance(merged, pd.DataFrame)

        # 2. Calculate crude rates
        with_rates = calculate_crude_rates(merged)
        self.assertIn("crude_rate", with_rates.columns)

        # 3. Age-standardize
        asr = calculate_age_standardized_rates(with_rates)
        self.assertIn("age_standardized_rate", asr.columns)

        # 4. Build synthetic analysis dataset (minimum 5 alcaldías × 5 years
        #    for cluster-robust SE to work)
        np.random.seed(42)
        both_sex = asr[asr["sex"] == "Both"].copy()
        # Expand to more alcaldías/years for statistical validity
        alcaldias = [
            "Iztapalapa",
            "Coyoacan",
            "Cuauhtemoc",
            "Benito Juarez",
            "Tlalpan",
        ]
        years = list(range(2015, 2020))
        expanded = []
        for alc in alcaldias:
            for yr in years:
                row = {"alcaldia": alc, "year": yr, "sex": "Both"}
                row["age_standardized_rate"] = np.abs(np.random.normal(14, 4))
                row["crude_rate"] = np.abs(np.random.normal(7, 2))
                expanded.append(row)
        both_sex = pd.DataFrame(expanded)
        both_sex["pm25"] = np.random.normal(21, 3, len(both_sex))
        both_sex["pm10"] = np.random.normal(42, 6, len(both_sex))
        both_sex["no2"] = np.random.normal(25, 5, len(both_sex))
        from src.utils import ALCALDIA_NAME_TO_CODE

        both_sex["alcaldia_code"] = (
            both_sex["alcaldia"].map(ALCALDIA_NAME_TO_CODE).astype(int)
        )

        # 5. Run statistical analysis
        stats = descriptive_statistics(both_sex)
        self.assertIsInstance(stats, pd.DataFrame)

        corr = correlation_analysis(both_sex)
        self.assertIsInstance(corr, pd.DataFrame)

        # Panel regression needs sufficient clusters for cluster-robust SE
        # With 5 alcaldías × 5 years = 25 obs, this is marginal but should work
        from src.analysis import panel_regression

        models, results = panel_regression(both_sex)
        self.assertIn("twoway_fe", models)

        twoway_coef = float(models["twoway_fe"].params["pm25_10"])
        self.assertIsInstance(twoway_coef, float)

    def test_mortality_processing_functions(self):
        """Test mortality processing helper functions."""
        from src.mortality_processing import map_edad_to_age_group, map_sexo_to_sex

        self.assertEqual(map_edad_to_age_group(4001), "0-4")
        self.assertEqual(map_edad_to_age_group(4015), "15-17")
        self.assertEqual(map_edad_to_age_group(4060), "60+")
        self.assertEqual(map_sexo_to_sex(1), "Male")
        self.assertEqual(map_sexo_to_sex(2), "Female")
        self.assertIsNone(map_sexo_to_sex(9))

    def test_harmonization_constants(self):
        """Test harmonization constants are valid."""
        from src.harmonization import (
            DEFAULT_PROP_FEMALE,
            DEFAULT_PROP_MALE,
            PROP_15_17_OF_15_24,
        )

        self.assertAlmostEqual(DEFAULT_PROP_FEMALE + DEFAULT_PROP_MALE, 1.0)
        self.assertGreater(PROP_15_17_OF_15_24, 0)
        self.assertLess(PROP_15_17_OF_15_24, 1)

    def test_utils_constants(self):
        """Test that utility constants are consistent."""
        from src.utils import (
            ALCALDIA_CODES,
            ALCALDIA_NAME_TO_CODE,
            WHO_WEIGHTS,
            HARMONIZED_AGE_GROUPS,
            POLLUTANTS,
            LUNG_CANCER_CODES,
        )

        self.assertEqual(len(ALCALDIA_CODES), 16)
        self.assertEqual(len(ALCALDIA_NAME_TO_CODE), 16)
        self.assertAlmostEqual(sum(WHO_WEIGHTS.values()), 1.0, places=4)
        self.assertEqual(len(HARMONIZED_AGE_GROUPS), 6)
        self.assertEqual(len(POLLUTANTS), 6)
        self.assertEqual(LUNG_CANCER_CODES, ["C33", "C34"])


if __name__ == "__main__":
    unittest.main()
