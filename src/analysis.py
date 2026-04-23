"""
Statistical analysis functions for panel regression and correlations.

Author: Arlex Marín
Date: April 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr

from .utils import (
    format_number, format_pvalue, save_json,
    POLLUTANTS, ALCALDIAS_WITH_POLLUTION, ALCALDIAS_WITHOUT_POLLUTION,
    ALCALDIA_NAME_TO_CODE, get_integrated_dataset_path
)
from . import TABLES_DIR, MODELS_DIR, ensure_directories


def prepare_analysis_sample():
    """
    Load analysis data and prepare samples for statistical analysis.

    Returns:
    --------
    df : pd.DataFrame
        Complete analytical dataset
    df_pm25 : pd.DataFrame
        Dataset filtered to records with PM2.5 data
    """
    filepath = get_integrated_dataset_path()
    if not filepath.exists():
        raise FileNotFoundError(f"Analysis data not found: {filepath}")

    df = pd.read_csv(filepath)

    # Filter to records with PM2.5 data
    df_pm25 = df.dropna(subset=['pm25']).copy()

    # Add alcaldía code for fixed effects
    df['alcaldia_code'] = df['alcaldia'].map(ALCALDIA_NAME_TO_CODE).astype(int)
    df_pm25['alcaldia_code'] = df_pm25['alcaldia'].map(ALCALDIA_NAME_TO_CODE).astype(int)

    print(f"  Analysis sample: {len(df_pm25)} records with PM2.5 data")
    print(f"  Alcaldías: {df_pm25['alcaldia'].nunique()}")
    print(f"  Years: {df_pm25['year'].min()} - {df_pm25['year'].max()}")

    return df, df_pm25


def descriptive_statistics(df_pm25):
    """Generate descriptive statistics."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()

    stats = {
        'variable': [],
        'n': [],
        'mean': [],
        'sd': [],
        'min': [],
        'max': []
    }

    variables = POLLUTANTS + ['crude_rate', 'age_standardized_rate']
    names = {
        'pm25': 'PM2.5 (μg/m³)', 'pm10': 'PM10 (μg/m³)', 'o3': 'O3 (ppb)',
        'no2': 'NO2 (ppb)', 'so2': 'SO2 (ppb)', 'co': 'CO (ppm)',
        'crude_rate': 'Crude Rate (per 100,000)',
        'age_standardized_rate': 'Age-Standardized Rate (per 100,000)'
    }

    for var in variables:
        if var in both_sex.columns:
            valid = both_sex[var].dropna()
            if len(valid) > 0:
                stats['variable'].append(names.get(var, var))
                stats['n'].append(len(valid))
                stats['mean'].append(round(valid.mean(), 2))
                stats['sd'].append(round(valid.std(), 2))
                stats['min'].append(round(valid.min(), 2))
                stats['max'].append(round(valid.max(), 2))

    df_stats = pd.DataFrame(stats)
    df_stats.to_csv(TABLES_DIR / 'descriptive_statistics.csv', index=False)
    print(f"  ✓ Descriptive statistics saved")

    return df_stats


def correlation_analysis(df_pm25):
    """Perform correlation analysis."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()

    results = []
    mortality_vars = ['crude_rate', 'age_standardized_rate']

    for pol in POLLUTANTS:
        if pol not in both_sex.columns:
            continue
        for mort in mortality_vars:
            valid = both_sex[[pol, mort]].dropna()
            if len(valid) > 0:
                r, p = pearsonr(valid[pol], valid[mort])
                rho, p_s = spearmanr(valid[pol], valid[mort])
                results.append({
                    'pollutant': pol.upper(),
                    'mortality': mort,
                    'pearson_r': round(r, 3),
                    'pearson_p': p,
                    'spearman_rho': round(rho, 3),
                    'spearman_p': p_s,
                    'n': len(valid),
                    'significant': p < 0.05
                })

    df_corr = pd.DataFrame(results)
    df_corr.to_csv(TABLES_DIR / 'correlation_results.csv', index=False)

    print(f"\n  Pearson Correlations with Age-Standardized Rate:")
    for _, row in df_corr[df_corr['mortality'] == 'age_standardized_rate'].iterrows():
        sig = "***" if row['pearson_p'] < 0.001 else ("**" if row['pearson_p'] < 0.01 else ("*" if row['pearson_p'] < 0.05 else ""))
        print(f"    {row['pollutant']:6}: r = {row['pearson_r']:+.3f} {sig}")

    return df_corr


def panel_regression(df_pm25):
    """Perform panel regression with cluster-robust standard errors."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    both_sex = both_sex.dropna(subset=['pm25', 'age_standardized_rate'])
    both_sex['pm25_10'] = both_sex['pm25'] / 10
    both_sex['log_asr'] = np.log(both_sex['age_standardized_rate'])

    print(f"\n  Analysis sample: {len(both_sex)} observations")

    models = {}
    results_table = []

    # Model 1: Pooled OLS
    X1 = sm.add_constant(both_sex['pm25_10'])
    y1 = both_sex['age_standardized_rate']
    model1 = sm.OLS(y1, X1).fit(cov_type='HC3')
    models['pooled_ols'] = model1
    results_table.append({
        'model': 'Pooled OLS',
        'coef': round(model1.params['pm25_10'], 3),
        'se': round(model1.bse['pm25_10'], 3),
        'p_value': model1.pvalues['pm25_10'],
        'r_squared': round(model1.rsquared, 3),
        'n': len(both_sex)
    })

    # Model 2: Alcaldía Fixed Effects
    X2 = pd.get_dummies(both_sex['alcaldia'], drop_first=True).astype(float)
    X2['pm25_10'] = both_sex['pm25_10'].values
    X2 = sm.add_constant(X2)
    y2 = both_sex['age_standardized_rate'].values
    model2 = sm.OLS(y2, X2).fit(cov_type='cluster', cov_kwds={'groups': both_sex['alcaldia_code']})
    models['alcaldia_fe'] = model2
    results_table.append({
        'model': 'Alcaldía FE',
        'coef': round(model2.params['pm25_10'], 3),
        'se': round(model2.bse['pm25_10'], 3),
        'p_value': model2.pvalues['pm25_10'],
        'r_squared': round(model2.rsquared, 3),
        'n': len(both_sex)
    })

    # Model 3: Two-Way Fixed Effects
    X3 = pd.get_dummies(both_sex['alcaldia'], drop_first=True).astype(float)
    year_dummies = pd.get_dummies(both_sex['year'], drop_first=True).astype(float)
    X3 = pd.concat([X3, year_dummies], axis=1)
    X3['pm25_10'] = both_sex['pm25_10'].values
    X3 = sm.add_constant(X3)
    model3 = sm.OLS(y2, X3).fit(cov_type='cluster', cov_kwds={'groups': both_sex['alcaldia_code']})
    models['twoway_fe'] = model3
    results_table.append({
        'model': 'Two-Way FE',
        'coef': round(model3.params['pm25_10'], 3),
        'se': round(model3.bse['pm25_10'], 3),
        'p_value': model3.pvalues['pm25_10'],
        'r_squared': round(model3.rsquared, 3),
        'n': len(both_sex)
    })

    # Model 4: Log-Linear
    y4 = both_sex['log_asr'].values
    model4 = sm.OLS(y4, X3).fit(cov_type='cluster', cov_kwds={'groups': both_sex['alcaldia_code']})
    effect_pct = (np.exp(model4.params['pm25_10']) - 1) * 100
    models['log_linear'] = model4
    results_table.append({
        'model': 'Log-Linear (Two-Way FE)',
        'coef': round(model4.params['pm25_10'], 4),
        'se': round(model4.bse['pm25_10'], 4),
        'p_value': model4.pvalues['pm25_10'],
        'effect_pct': round(effect_pct, 2),
        'r_squared': round(model4.rsquared, 3),
        'n': len(both_sex)
    })

    df_results = pd.DataFrame(results_table)
    df_results.to_csv(TABLES_DIR / 'regression_results_summary.csv', index=False)

    print(f"\n  Regression Results (Two-Way FE):")
    print(f"    PM2.5 (per 10 μg/m³): {model3.params['pm25_10']:.3f} (SE: {model3.bse['pm25_10']:.3f})")
    print(f"    {format_pvalue(model3.pvalues['pm25_10'])}")
    print(f"    R-squared: {model3.rsquared:.3f}")

    # Save full model summaries
    with open(MODELS_DIR / 'regression_results.txt', 'w') as f:
        f.write("PANEL REGRESSION ANALYSIS RESULTS\n")
        f.write("=" * 60 + "\n")
        f.write(f"Alcaldías included: {len(ALCALDIAS_WITH_POLLUTION)}\n")
        f.write(f"Alcaldías excluded: {', '.join(ALCALDIAS_WITHOUT_POLLUTION)}\n")
        f.write(f"Observations: {len(both_sex)}\n")
        f.write("=" * 60 + "\n\n")
        for name, model in models.items():
            f.write(f"\n{'='*60}\n{name}\n{'='*60}\n")
            f.write(model.summary().as_text())
            f.write("\n\n")

    print(f"  ✓ Regression results saved")

    return models, df_results


def sex_specific_analysis(df_pm25):
    """Perform sex-specific regression analysis."""
    results = {}
    results_table = []

    for sex in ['Male', 'Female']:
        df_sex = df_pm25[df_pm25['sex'] == sex].copy()
        df_sex = df_sex.dropna(subset=['pm25', 'age_standardized_rate'])
        df_sex['pm25_10'] = df_sex['pm25'] / 10

        X = pd.get_dummies(df_sex['alcaldia'], drop_first=True).astype(float)
        year_dummies = pd.get_dummies(df_sex['year'], drop_first=True).astype(float)
        X = pd.concat([X, year_dummies], axis=1)
        X['pm25_10'] = df_sex['pm25_10'].values
        X = sm.add_constant(X)
        y = df_sex['age_standardized_rate'].values

        model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df_sex['alcaldia_code']})
        results[sex] = model

        results_table.append({
            'sex': sex,
            'coef': round(model.params['pm25_10'], 3),
            'se': round(model.bse['pm25_10'], 3),
            'p_value': model.pvalues['pm25_10'],
            'r_squared': round(model.rsquared, 3),
            'n': len(df_sex)
        })

    df_sex_results = pd.DataFrame(results_table)
    df_sex_results.to_csv(TABLES_DIR / 'sex_specific_regression.csv', index=False)

    print(f"\n  Sex-Specific Results (Two-Way FE):")
    for _, row in df_sex_results.iterrows():
        print(f"    {row['sex']}: β = {row['coef']:.3f} (SE: {row['se']:.3f}), {format_pvalue(row['p_value'])}")

    # Save sex-specific summaries
    with open(MODELS_DIR / 'sex_specific_results.txt', 'w') as f:
        f.write("SEX-SPECIFIC REGRESSION ANALYSIS\n")
        f.write("=" * 60 + "\n\n")
        for sex, model in results.items():
            f.write(f"\n{'='*60}\n{sex}\n{'='*60}\n")
            f.write(model.summary().as_text())
            f.write("\n\n")

    print(f"  ✓ Sex-specific results saved")

    return results, df_sex_results


def run_analysis():
    """Main analysis pipeline."""
    print("\n" + "=" * 70)
    print("STATISTICAL ANALYSIS")
    print("=" * 70)

    ensure_directories()

    print(f"\n  Alcaldías included: {len(ALCALDIAS_WITH_POLLUTION)}")
    print(f"  Alcaldías excluded: {', '.join(ALCALDIAS_WITHOUT_POLLUTION)}")

    # Load data
    df, df_pm25 = prepare_analysis_sample()

    # Descriptive statistics
    df_stats = descriptive_statistics(df_pm25)

    # Correlation analysis
    df_corr = correlation_analysis(df_pm25)

    # Panel regression
    models, df_results = panel_regression(df_pm25)

    # Sex-specific analysis
    sex_models, df_sex_results = sex_specific_analysis(df_pm25)

    # Metadata
    metadata = {
        'date_created': datetime.now().isoformat(),
        'observations': len(df_pm25[df_pm25['sex'] == 'Both']),
        'alcaldias_included': ALCALDIAS_WITH_POLLUTION,
        'alcaldias_excluded': ALCALDIAS_WITHOUT_POLLUTION,
        'models': {
            'twoway_fe': {
                'coef': float(models['twoway_fe'].params['pm25_10']),
                'se': float(models['twoway_fe'].bse['pm25_10']),
                'p_value': float(models['twoway_fe'].pvalues['pm25_10'])
            }
        }
    }

    metadata_path = TABLES_DIR.parent / 'analysis_metadata.json'
    save_json(metadata, metadata_path)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return df_pm25, models
