# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-04-23

### Changed
- R1: Removed unused dependencies (shap, xgboost, scikit-learn, calplot, windrose) from `environment.yml` and `requirements.txt`
- R2: Unified path definitions — `utils.py` now imports from `__init__.py` as single source of truth
- R3: Removed duplicate `get_shapefile_path` function from `utils.py` (dead code, geospatial module has its own)
- R7: Replaced `print()` calls with structured `logging` throughout all 9 source modules
- R8: Extracted duplicated encoding detection logic into canonical `read_csv_with_encoding()` in `utils.py`
- R9: Replaced blanket `warnings.filterwarnings('ignore')` with targeted context managers in `analysis.py`
- R10: Added type hints to all public pipeline functions (return types + parameter types)

### Added
- R5: `docs/quality_assessment.md` — code quality report (score 93/100)
- R11: `.github/workflows/ci.yml` — GitHub Actions CI pipeline (test + lint)
- R12: `.pre-commit-config.yaml` — pre-commit hooks (black, flake8, isort)
- R13: `CHANGELOG.md` — this file
- R14: `CONTRIBUTING.md` — contributor guide
- `docs/CRITICAL_EVALUATION_REPORT.md` — full engineering evaluation

### Fixed
- R4: `test_geospatial.py` now skips gracefully when geopandas is unavailable (14 skipped tests instead of 2 failures)
- `test_run_analysis.py` skips geospatial import test when geopandas not installed

### Removed
- R6: Orphan files: `tree.txt`, `src/src_init_py.txt`, `tests/tests_init_py.txt`

## [1.0.0] - 2026-04-22

### Added
- Initial release: complete 6-phase pipeline for air pollution and lung cancer mortality analysis in Mexico City
- Data validation (Phase 1): census, mortality, pollution datasets
- Population harmonization (Phase 2): 4 censuses → annual estimates 2000-2022
- Mortality processing (Phase 3): ICD-10 C33-C34 extraction from 24-year records
- Integration & age standardization (Phase 4): WHO direct method, pollution merge
- Statistical analysis (Phase 5): panel regression, correlations, sex-specific
- Visualization (Phase 6): PNG/SVG figures + interactive HTML choropleth maps
- Bilingual documentation (EN/ES): 14 documents covering methodology, validation, harmonization, data dictionary
- 87 unit tests across 7 test modules
- CC BY 4.0 license, CITATION.cff with Zenodo DOI
