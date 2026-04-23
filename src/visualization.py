"""
Visualization functions for publication-quality figures.

Author: Arlex Marín
Date: April 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

from .utils import format_pvalue, POLLUTANTS
from . import FIGURES_DIR, TABLES_DIR, ensure_directories

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def save_figure(fig, name):
    """Save figure to PNG and SVG."""
    fig.savefig(FIGURES_DIR / f'{name}.png', dpi=300, bbox_inches='tight')
    fig.savefig(FIGURES_DIR / f'{name}.svg', bbox_inches='tight')
    print(f"  ✓ Saved: {name}")


def plot_temporal_trends(df_pm25):
    """Create temporal trends plot."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    yearly_avg = both_sex.groupby('year').agg({
        'pm25': 'mean', 'pm10': 'mean',
        'age_standardized_rate': 'mean', 'crude_rate': 'mean'
    }).reset_index()
    
    yearly_avg.to_csv(TABLES_DIR / 'yearly_averages.csv', index=False)
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Pollution trends
    axes[0].plot(yearly_avg['year'], yearly_avg['pm25'], 'o-', label='PM2.5', color='steelblue', linewidth=2)
    axes[0].plot(yearly_avg['year'], yearly_avg['pm10'], 's-', label='PM10', color='darkorange', linewidth=2)
    axes[0].set_ylabel('Concentration (μg/m³)', fontsize=11)
    axes[0].set_title('Air Pollution Trends in Mexico City (2004-2022, 14 Alcaldías)', 
                      fontsize=12, fontweight='bold')
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.3)
    
    # Mortality trends
    axes[1].plot(yearly_avg['year'], yearly_avg['crude_rate'], 'o-', label='Crude Rate', color='green', linewidth=2)
    axes[1].plot(yearly_avg['year'], yearly_avg['age_standardized_rate'], 's-', 
                 label='Age-Standardized Rate', color='crimson', linewidth=2)
    axes[1].set_xlabel('Year', fontsize=11)
    axes[1].set_ylabel('Mortality Rate (per 100,000)', fontsize=11)
    axes[1].set_title('Lung Cancer Mortality Trends in Mexico City (2004-2022, 14 Alcaldías)', 
                      fontsize=12, fontweight='bold')
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure(fig, 'temporal_trends')
    plt.close()
    
    return yearly_avg


def plot_correlation_scatter(df_pm25):
    """Create PM2.5 vs mortality scatter plot."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    scatter = ax.scatter(both_sex['pm25'], both_sex['age_standardized_rate'], 
                         c=both_sex['year'], cmap='viridis', alpha=0.6, s=50)
    
    z = np.polyfit(both_sex['pm25'], both_sex['age_standardized_rate'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(both_sex['pm25'].min(), both_sex['pm25'].max(), 100)
    ax.plot(x_line, p(x_line), 'r-', linewidth=2, label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    r, p_val = pearsonr(both_sex['pm25'], both_sex['age_standardized_rate'])
    ax.annotate(f'r = {r:.3f}\n{format_pvalue(p_val)}', 
                xy=(0.05, 0.95), xycoords='axes fraction',
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('PM2.5 Concentration (μg/m³)', fontsize=11)
    ax.set_ylabel('Age-Standardized Mortality Rate (per 100,000)', fontsize=11)
    ax.set_title('Association between PM2.5 and Lung Cancer Mortality\nMexico City, 2004-2022 (14 Alcaldías)', 
                 fontsize=12, fontweight='bold')
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('Year', fontsize=10)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure(fig, 'pm25_vs_mortality_scatter')
    plt.close()


def plot_alcaldia_boxplot(df_pm25):
    """Create alcaldía comparison boxplot."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    alcaldia_order = both_sex.groupby('alcaldia')['age_standardized_rate'].mean().sort_values().index
    
    sns.boxplot(data=both_sex, x='alcaldia', y='age_standardized_rate', 
                order=alcaldia_order, palette='Reds', ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel('Age-Standardized Mortality Rate (per 100,000)', fontsize=11)
    ax.set_title('Distribution of Lung Cancer Mortality Rates by Alcaldía\nMexico City, 2004-2022 (14 Alcaldías)', 
                 fontsize=12, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    save_figure(fig, 'alcaldia_boxplot')
    plt.close()


def plot_pm25_by_alcaldia(df_pm25):
    """Create PM2.5 by alcaldía boxplot."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    pm25_order = both_sex.groupby('alcaldia')['pm25'].mean().sort_values().index
    
    sns.boxplot(data=both_sex, x='alcaldia', y='pm25', 
                order=pm25_order, palette='Blues', ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel('PM2.5 Concentration (μg/m³)', fontsize=11)
    ax.set_title('Distribution of PM2.5 Concentrations by Alcaldía\nMexico City, 2004-2022 (14 Alcaldías)', 
                 fontsize=12, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    save_figure(fig, 'pm25_by_alcaldia')
    plt.close()


def plot_regression_coefficients(models):
    """Create regression coefficient comparison plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    model_names = ['Pooled OLS', 'Alcaldía FE', 'Two-Way FE']
    coefs = [
        models['pooled_ols'].params['pm25_10'],
        models['alcaldia_fe'].params['pm25_10'],
        models['twoway_fe'].params['pm25_10']
    ]
    cis = [
        [models['pooled_ols'].conf_int().loc['pm25_10', 0], 
         models['pooled_ols'].conf_int().loc['pm25_10', 1]],
        [models['alcaldia_fe'].conf_int().loc['pm25_10', 0], 
         models['alcaldia_fe'].conf_int().loc['pm25_10', 1]],
        [models['twoway_fe'].conf_int().loc['pm25_10', 0], 
         models['twoway_fe'].conf_int().loc['pm25_10', 1]]
    ]
    errors = [[coef - ci[0], ci[1] - coef] for coef, ci in zip(coefs, cis)]
    errors = np.array(errors).T
    
    ax.errorbar(range(len(model_names)), coefs, yerr=errors, fmt='o', 
                capsize=5, capthick=2, markersize=8, color='steelblue')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.set_xticks(range(len(model_names)))
    ax.set_xticklabels(model_names, rotation=15, ha='right')
    ax.set_ylabel('Coefficient for PM2.5 (per 10 μg/m³)')
    ax.set_title('Effect of PM2.5 on Age-Standardized Lung Cancer Mortality\n(2004-2022, 14 Alcaldías)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure(fig, 'regression_coefficients')
    plt.close()


def plot_sex_specific_effects(sex_models):
    """Create sex-specific effects comparison plot."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sexes = ['Male', 'Female']
    coefs = [sex_models['Male'].params['pm25_10'], sex_models['Female'].params['pm25_10']]
    cis = [
        [sex_models['Male'].conf_int().loc['pm25_10', 0], 
         sex_models['Male'].conf_int().loc['pm25_10', 1]],
        [sex_models['Female'].conf_int().loc['pm25_10', 0], 
         sex_models['Female'].conf_int().loc['pm25_10', 1]]
    ]
    errors = [[coef - ci[0], ci[1] - coef] for coef, ci in zip(coefs, cis)]
    errors = np.array(errors).T
    
    bars = ax.bar(sexes, coefs, color=['steelblue', 'lightcoral'], alpha=0.8)
    ax.errorbar(sexes, coefs, yerr=errors, fmt='none', capsize=5, capthick=2, color='black')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.set_ylabel('Coefficient for PM2.5 (per 10 μg/m³)')
    ax.set_title('Sex-Specific Effects of PM2.5 on Lung Cancer Mortality\n(2004-2022, 14 Alcaldías)', 
                 fontsize=12, fontweight='bold')
    
    for bar, coef in zip(bars, coefs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{coef:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, 'sex_specific_effects')
    plt.close()


def plot_correlation_heatmap(df_pm25):
    """Create correlation heatmap."""
    both_sex = df_pm25[df_pm25['sex'] == 'Both'].copy()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    corr_cols = [p for p in POLLUTANTS if p in both_sex.columns] + ['crude_rate', 'age_standardized_rate']
    corr_matrix = both_sex[corr_cols].corr()
    
    display_names = {
        'pm25': 'PM2.5', 'pm10': 'PM10', 'o3': 'O3', 'no2': 'NO2', 'so2': 'SO2', 'co': 'CO',
        'crude_rate': 'Crude Rate', 'age_standardized_rate': 'ASR'
    }
    corr_matrix_display = corr_matrix.rename(index=display_names, columns=display_names)
    
    sns.heatmap(corr_matrix_display, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, ax=ax,
                cbar_kws={'label': 'Correlation Coefficient'})
    ax.set_title('Correlation Matrix: Air Pollutants and Mortality Rates\n(2004-2022, 14 Alcaldías)', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, 'correlation_heatmap')
    plt.close()


def create_all_visualizations(df_pm25, models=None, sex_models=None):
    """Create all publication-quality visualizations."""
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    ensure_directories()
    
    plot_temporal_trends(df_pm25)
    plot_correlation_scatter(df_pm25)
    plot_alcaldia_boxplot(df_pm25)
    plot_pm25_by_alcaldia(df_pm25)
    plot_correlation_heatmap(df_pm25)
    
    if models:
        plot_regression_coefficients(models)
    
    if sex_models:
        plot_sex_specific_effects(sex_models)
    
    print(f"\n  ✓ All figures saved to: {FIGURES_DIR}")