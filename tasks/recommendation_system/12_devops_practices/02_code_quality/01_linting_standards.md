# Code Quality for ML Projects

## Overview

Code quality in ML projects is often neglected due to the experimental nature of the work. However, production ML systems demand the same rigor as any production software. Poor code quality leads to subtle bugs, reproducibility issues, and technical debt that compounds over time. This document covers linting, type checking, formatting, and code quality practices specific to ML projects.

## Linting Tools

### Ruff

Ruff is a fast Python linter written in Rust that replaces flake8, isort, pyupgrade, and more.

**Recommended Configuration**:

- Enable rule sets: E (pycodestyle errors), F (pyflakes), W (pycodestyle warnings), I (isort), UP (pyupgrade), B (flake8-bugbear), SIM (flake8-simplify), TCH (flake8-type-checking), RUF (Ruff-specific).
- Set line length to 88 characters (Black compatible).
- Ignore S101 in tests (assert is expected), F401 in `__init__.py` (unused imports are re-exports).
- Target Python 3.11+ for modern syntax support.

### Flake8 (Legacy)

If Ruff adoption is not yet complete, configure flake8 as the baseline:

- Install plugins: `flake8-bugbear`, `flake8-comprehensions`, `flake8-import-order`.
- Max line length: 88 characters (compatible with Black).
- Ignore: E203 (whitespace before colon), W503 (line break before binary operator).
- Per-file ignores for test files and `__init__.py`.

### Pylint

Pylint provides deeper analysis than flake8, including:

- Code complexity metrics.
- Convention violations.
- Refactoring suggestions.
- Error detection beyond syntax.

Use pylint as a secondary linter after ruff/flake8 for catching deeper issues.

## Type Checking

### Mypy

Mypy provides static type checking for Python.

**Recommended Configuration**:

- Set `strict = true` as the baseline.
- Enable `disallow_untyped_defs`, `disallow_incomplete_defs`, `no_implicit_optional`.
- Enable `warn_return_any`, `warn_unused_configs`, `warn_redundant_casts`, `warn_unused_ignores`.
- Override for tests: relax `disallow_untyped_defs` to false.
- Override for third-party: `ignore_missing_imports = true` for numpy, pandas, sklearn, torch.

**Type Checking Strategy**:

- Enable strict mode for all new code.
- Gradually enable strict mode for existing code (one module at a time).
- Use `# type: ignore[error-code]` sparingly and only with justification.
- Review type ignore comments in code review.
- Run mypy as part of CI and block merges on type errors.

### Pyright

Pyright provides complementary type checking to mypy:

- Faster execution time than mypy.
- Better support for newer Python features.
- More aggressive about detecting type errors.
- Use as a secondary checker to catch what mypy misses.

## Code Formatting

### Black

Black is the standard Python code formatter.

**Configuration**:

- Line length: 88 characters.
- Target version: Python 3.11.
- Skip string normalization: false (use double quotes consistently).

**Usage**:

- Format all code before commit (via pre-commit hook).
- Black is opinionated: it enforces a single style with no configuration.
- Never override Black decisions in code reviews.
- Format the entire codebase periodically to maintain consistency.

### Isort

Isort sorts and organizes imports.

**Configuration**:

- Profile: "black" (ensures compatibility with Black formatting).
- Multi-line output style: 3 (vertical hanging indent).
- Include trailing comma: true.
- Line length: 88.

**Import Ordering Convention**:

1. Standard library imports (os, sys, json).
2. Third-party imports (numpy, pandas, torch).
3. Local imports (from myproject.module import func).
4. Separate each group with a blank line.

### Prettier (for non-Python files)

- Format YAML, JSON, Markdown, and TOML files.
- Use consistent formatting for configuration files.
- Integrate with pre-commit hooks.

## ML-Specific Linting

### Feature Store Schema Validation

- Validate feature schemas at ingestion time using schema validation libraries.
- Define feature schemas as versioned contracts (JSON Schema, protobuf).
- Check for schema drift between training and serving environments.
- Validate feature value types, ranges, and distributions.

### Model Configuration Validation

- Validate model configuration files against a schema before training.
- Check that all required hyperparameters are present.
- Validate value ranges for numeric hyperparameters.
- Ensure configuration consistency across training and serving.

**Validation Checks**:

| Check | Description | Tool |
|-------|-------------|------|
| Schema validation | Config matches expected structure | pydantic, jsonschema |
| Range validation | Numeric values within bounds | Custom validators |
| Type validation | Values are correct types | pydantic |
| Dependency validation | Dependent parameters are consistent | Custom validators |
| Environment validation | Config matches target environment | Custom validators |

### Data Pipeline Validation

- Validate data schemas at each pipeline stage.
- Check for data quality issues (missing values, outliers, distribution shifts).
- Verify that feature distributions match training data distributions.
- Log data quality metrics and alert on anomalies.

## Pre-Commit Hooks

### Pre-Commit Configuration

- Use the `pre-commit` framework for managing Git hooks.
- Run all hooks on every commit (local enforcement).
- Mirror pre-commit hooks in CI (never trust local-only hooks).

**Recommended Hooks**:

| Hook | Purpose | When to Run |
|------|---------|-------------|
| `ruff` | Python linting | Every commit |
| `ruff-format` | Code formatting | Every commit |
| `mypy` | Type checking | Every commit |
| `check-yaml` | YAML validation | Every commit |
| `check-json` | JSON validation | Every commit |
| `trailing-whitespace` | Whitespace cleanup | Every commit |
| `end-of-file-fixer` | File ending consistency | Every commit |
| `dvc` | DVC status check | Every commit (if using DVC) |
| `validate-config` | Model config schema check | Every commit |

### Pre-Commit Hook Strategy

- Keep hooks fast (<30 seconds total) to avoid developer friction.
- Use `pre-commit run --all-files` in CI for full validation.
- Cache hook environments to speed up subsequent runs.
- Update hook versions monthly using `pre-commit autoupdate`.
- Document any manual hook bypasses in the PR description.

## Code Review Checklists

### General Code Review

- Code is readable and follows project conventions.
- Function and variable names are descriptive.
- No code duplication; abstractions are appropriate.
- Error handling is comprehensive.
- Logging is informative and appropriately leveled.
- No hardcoded values; configuration is externalized.
- Tests cover happy path, edge cases, and error conditions.

### ML-Specific Code Review

- Random seeds are fixed for reproducibility.
- Data splitting methodology is documented and correct.
- Evaluation metrics are correctly computed (no data leakage).
- Baseline comparison is provided.
- Feature engineering logic is documented.
- Model configuration is externalized and version-controlled.
- Training and serving code use the same preprocessing logic.
- No data leakage between training and evaluation sets.
- Resource requirements are documented.
- Model size and inference latency are within acceptable bounds.

### Infrastructure Code Review

- Resource requirements are specified (CPU, memory, GPU).
- Scaling behavior is documented.
- Monitoring and alerting are configured.
- Security implications are considered.
- Cost impact is estimated.
- Backup and rollback procedures are documented.

## Technical Debt Management

### Tracking Technical Debt

- Maintain a technical debt register (GitHub Issues with `tech-debt` label).
- Categorize debt: code quality, ML debt, infrastructure debt, documentation debt.
- Estimate effort and impact for each debt item.
- Review debt register quarterly and prioritize paydown.

### ML-Specific Technical Debt

| Debt Type | Example | Impact | Priority |
|-----------|---------|--------|----------|
| Feature engineering duplication | Same feature computed in 3 places | Bugs, inconsistency | High |
| Untested model logic | No unit tests for ranking function | Regression risk | High |
| Stale configurations | Hardcoded hyperparameters | Reproducibility | Medium |
| Missing documentation | Undocumented feature pipeline | Onboarding friction | Medium |
| Outdated dependencies | Old PyTorch version | Security, performance | Low-Medium |
| Legacy code paths | Unused feature extractors | Maintenance burden | Low |

### Debt Paydown Strategy

- Allocate 20% of each sprint to technical debt reduction.
- Prioritize high-impact, high-urgency debt items first.
- Include debt paydown in sprint planning alongside feature work.
- Track debt reduction metrics (debt items closed per sprint, code coverage trend).
- Prevent new debt by enforcing code quality standards in PR reviews.
