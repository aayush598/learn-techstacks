# Static Analysis

## Overview

Static analysis tools automatically examine code without executing it, catching errors, enforcing style, detecting security vulnerabilities, and validating type safety. For recommendation system projects, static analysis is essential because ML code is complex, data-dependent, and prone to subtle bugs that traditional testing may miss. A well-configured static analysis pipeline catches issues before code review, reducing reviewer burden and improving code quality.

## Ruff (Python Linter)

### Overview

Ruff is a fast Python linter written in Rust. It replaces flake8, isort, pyupgrade, and many other linters with a single, fast tool.

### Configuration

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
    "RUF",  # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default argument (common in FastAPI)
]

[tool.ruff.per-file-ignores]
"tests/*" = ["B011"]  # allow assert False in tests
"__init__.py" = ["F401"]  # allow unused imports

[tool.ruff.isort]
known-first-party = ["recsys"]
```

### Key Rules for ML Code

| Rule | Description | Example |
|------|-------------|---------|
| **F841** | Local variable assigned but never used | Dead feature computation |
| **E711** | Comparison to None (use `is` instead of `==`) | Null checking in feature code |
| **B006** | Mutable default argument | Shared state in model functions |
| **I001** | Import not sorted | Unorganized imports |
| **UP007** | Use modern type syntax | `Optional[X]` → `X | None` |

## Mypy (Type Checking)

### Overview

Mypy performs static type checking on Python code, catching type errors before runtime.

### Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "scripts.*"
disallow_untyped_defs = false
```

### Type Checking for ML Code

| Check | Importance | Example |
|-------|-----------|---------|
| **Function signatures** | Ensure models have typed inputs/outputs | `def predict(features: pd.DataFrame) -> np.ndarray` |
| **Dataclass fields** | Typed configuration objects | `@dataclass class ModelConfig: learning_rate: float` |
| **Return types** | Prevent silent type mismatches | Feature functions must declare return types |
| **Optional handling** | Force explicit None handling | Cold-start features may be None |
| **Union types** | Handle multiple possible types | Model outputs may be different formats |

### Common Type Annotations for ML

```python
import numpy as np
import pandas as pd
from typing import Protocol

class Recommender(Protocol):
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None: ...
    def predict(self, X: pd.DataFrame) -> np.ndarray: ...
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray: ...

def compute_features(
    user_id: int,
    item_ids: list[int],
    context: dict[str, float],
) -> pd.DataFrame: ...

def evaluate_model(
    model: Recommender,
    test_data: pd.DataFrame,
    metrics: list[str],
) -> dict[str, float]: ...
```

## Bandit (Security Linting)

### Overview

Bandit finds common security issues in Python code. For ML systems, it's particularly important for detecting hardcoded secrets, insecure deserialization, and injection vulnerabilities.

### Configuration

```toml
# pyproject.toml
[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]  # skip assert warnings in non-test code
```

### Key Security Checks for ML Code

| Check ID | Description | ML Relevance |
|----------|-------------|-------------|
| **B105** | Hardcoded password strings | API keys for data sources |
| **B106** | Hardcoded password function argument | Model serving auth tokens |
| **B108** | Insecure temporary file usage | Training data temp files |
| **B301** | pickle.loads usage (insecure deserialization) | Model loading (use safetensors) |
| **B311** | Random number generation (not for security) | Training random seeds |
| **B501** | SSL certificate verification disabled | API connections to data sources |
| **B602** | Subprocess with shell=True | Training script execution |
| **B608** | SQL injection (hardcoded SQL) | Feature store queries |

### Safe Model Loading

```python
# BAD: Bandit will flag this
import pickle
model = pickle.load(open("model.pkl", "rb"))

# GOOD: Use safetensors or joblib with controlled deserialization
from safetensors.torch import load_file
model = load_file("model.safetensors")

# GOOD: Use joblib with hash check
import joblib
model = joblib.load("model.pkl")  # Requires trusted source
```

## Pylint

### Overview

Pylint is a comprehensive Python linter that checks for errors, enforces coding standards, and detects code smells.

### Configuration

```ini
# .pylintrc
[MASTER]
jobs=0
load-plugins=

[MESSAGES CONTROL]
disable=
    C0114,  # missing-module-docstring
    C0115,  # missing-class-docstring
    C0116,  # missing-function-docstring
    R0903,  # too-few-public-methods
    R0913,  # too-many-arguments

[FORMAT]
max-line-length=88

[DESIGN]
max-args=8
max-locals=15
max-returns=6
max-branches=12
```

### Pylint vs Ruff

| Aspect | Pylint | Ruff |
|--------|--------|------|
| Speed | Slow (pure Python) | Fast (Rust-based) |
| Rules | Comprehensive (1000+) | Growing (700+) |
| Configuration | Complex | Simple |
| Modern Python | Good | Excellent |
| IDE integration | Good | Excellent |
| Recommendation | Use alongside Ruff for deep analysis | Use as primary linter |

## Pre-commit Hooks

### Overview

Pre-commit hooks run automatically before each git commit, catching issues before they enter the codebase.

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # General code quality
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  # Linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, pandas-stubs]

  # Security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ["bandit[toml]"]

  # Data validation
  - repo: local
    hooks:
      - id: validate-data-schema
        name: Validate data schemas
        entry: python -m pandera --numpy
        language: system
        files: 'src/data/.*\.py$'
        pass_filenames: false
```

### Pre-commit Hook Performance

| Hook | Typical Runtime | Optimization |
|------|----------------|-------------|
| trailing-whitespace | < 1s | Always fast |
| black | 1–5s | Only check changed files |
| ruff | < 1s | Very fast (Rust) |
| mypy | 5–30s | Cache type stubs |
| bandit | 1–3s | Only check changed files |
| validate-data-schema | 2–10s | Run only when schema files change |

## IDE Integration

### VS Code Configuration

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    },
    "mypy-type-checker.args": ["--strict"],
    "mypy-type-checker.path": [".venv/bin/mypy"],
    "ruff.args": ["--config", "pyproject.toml"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".mypy_cache": true
    }
}
```

### Recommended IDE Extensions

| Extension | Purpose |
|-----------|---------|
| Python (ms-python) | Core Python support |
| Ruff (charliermarsh.ruff) | Linting and formatting |
| Mypy Type Checker | Type checking |
| Pylance | Language intelligence |
| GitLens | Git integration |
| Data Version Control | DVC integration |

## CI/CD Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/lint.yml
name: Lint and Type Check

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install ruff mypy bandit black pandas-stubs
      - name: Ruff
        run: ruff check src/ tests/
      - name: Black check
        run: black --check src/ tests/
      - name: Mypy
        run: mypy src/
      - name: Bandit
        run: bandit -r src/ -c pyproject.toml
```

### CI Pipeline Stages

```
1. Lint (Ruff) - < 30s
2. Format check (Black) - < 30s
3. Type check (Mypy) - 1–3 min
4. Security scan (Bandit) - < 30s
5. Unit tests (pytest) - 2–10 min
6. Integration tests - 5–15 min
7. Data validation (if data PR) - 2–5 min
8. Model validation (if model PR) - 5–20 min
```

## Custom Linting Rules for ML

### Feature Schema Validation

```python
# Custom rule: validate feature schemas
import pandera as pa

feature_schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, checks=[pa.Check.ge(0)]),
    "item_id": pa.Column(int, checks=[pa.Check.ge(0)]),
    "user_age": pa.Column(float, nullable=True),
    "item_price": pa.Column(float, checks=[pa.Check.gt(0)]),
    "timestamp": pa.Column("datetime64[ns]"),
})

# In CI: validate training data against schema
feature_schema.validate(training_data)
```

### Model Card Validation

```python
# Custom rule: ensure model cards are complete
required_fields = [
    "model_name", "version", "training_data_version",
    "metrics", "fairness_audit", "limitations", "intended_use"
]

def validate_model_card(card_path: str) -> bool:
    card = load_model_card(card_path)
    missing = [f for f in required_fields if f not in card]
    if missing:
        raise ValueError(f"Model card missing: {missing}")
    return True
```
