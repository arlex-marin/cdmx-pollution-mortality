# Contributing to CDMX Pollution-Mortality Analysis

Thank you for your interest in contributing! This project investigates the spatial and temporal relationship between air pollution and lung cancer mortality in Mexico City.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project is committed to fostering an inclusive and respectful community. Please:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

## How to Contribute

### Types of Contributions

We welcome:

- **Bug reports** — Open an issue with a minimal reproduction
- **Feature requests** — Open an issue describing the use case
- **Code improvements** — Submit a pull request
- **Documentation improvements** — Fix typos, add examples, translate
- **Data extensions** — Add new data sources, extend temporal/spatial coverage
- **Methodological improvements** — Suggest better statistical methods

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python tests/run_all_tests.py`
5. Submit a pull request

## Development Setup

```bash
# 1. Clone your fork
git clone https://github.com/<your-username>/cdmx-pollution-mortality.git
cd cdmx-pollution-mortality

# 2. Create conda environment
conda env create -f environment.yml
conda activate mx-public-health-analysis

# 3. Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# 4. Download raw data (see docs/en/02_data_acquisition_procedure.md)
```

## Project Structure

```
cdmx-pollution-mortality/
├── src/                    # Python source code (9 modules)
│   ├── __init__.py         # Package init, paths, exports
│   ├── utils.py            # Shared utilities and constants
│   ├── data_validation.py  # Phase 1: Input data validation
│   ├── harmonization.py    # Phase 2: Population harmonization
│   ├── mortality_processing.py  # Phase 3: Mortality processing
│   ├── integration.py      # Phase 4: Integration & standardization
│   ├── analysis.py         # Phase 5: Statistical analysis
│   ├── visualization.py    # Phase 5: Publication-quality figures
│   ├── geospatial.py       # Phase 6: Choropleth maps
│   └── run_analysis.py     # Pipeline orchestrator
├── tests/                  # Unit tests (99 test cases)
├── docs/                   # Bilingual documentation (EN/ES)
├── data/                   # Raw, processed, external data
└── outputs/                # Figures, tables, models
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Line length: 110 characters max
- Use type hints for public function signatures
- Use Google-style or NumPy-style docstrings (be consistent)
- Prefer `pathlib.Path` over `os.path`
- Prefer `logging` over `print()` for progress messages

### Commit Messages

```
<type>: <short description>

- Bullet points for details
- Reference issues with #issue_number
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`

### Imports

Use isort with `--profile=black` to sort imports:

```python
# Standard library
import logging
from pathlib import Path

# Third-party
import pandas as pd
import numpy as np

# Local
from .utils import safe_int, format_number
```

## Testing

- All code must pass existing tests before merging
- Add tests for new functionality
- Run all tests: `python tests/run_all_tests.py`
- Run a specific test: `python -m unittest tests/test_analysis.py`

### Test Requirements

- Tests must not depend on external data files (use synthetic data)
- Geospatial tests should skip gracefully when geopandas is not installed
- Use descriptive test method names (`test_<feature>_<scenario>`)

## Documentation

- Keep bilingual documentation updated (English + Spanish)
- Update `docs/en/` and `docs/es/` with any methodology changes
- Update `CHANGELOG.md` with notable changes
- Update `CITATION.cff` if authorship or citation info changes

## Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if your change affects the API or methodology
3. Add a changelog entry
4. Submit the PR with a clear description of what and why
5. A maintainer will review within 1-2 weeks

### PR Checklist

- [ ] Tests pass: `python tests/run_all_tests.py`
- [ ] Code follows project style (run `black` and `isort`)
- [ ] No new warnings or errors
- [ ] Updated `CHANGELOG.md`
- [ ] Updated documentation if applicable

---

Thank you for contributing to open science! 🌍
