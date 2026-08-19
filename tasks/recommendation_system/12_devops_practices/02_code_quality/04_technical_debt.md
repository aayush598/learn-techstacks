# Technical Debt in ML

## Overview

Technical debt in machine learning systems is insidious because it accumulates silently across code, data, models, and infrastructure. Unlike traditional software debt (which primarily affects code), ML debt spans the entire lifecycle: training data quality issues, unmaintained models, outdated dependencies, and undocumented experiments. Studies show that ML systems have significantly more debt than traditional software, with data and model debt being unique to ML.

## Code Debt

### Definition

Code debt results from quick fixes, incomplete implementations, and shortcuts taken during model development that would need to be addressed for production quality.

### Common Code Debt Patterns

| Pattern | Description | Impact |
|---------|-------------|--------|
| **Notebook-to-production** | Jupyter notebooks adapted for production without proper refactoring | Untestable, fragile code |
| **Copy-paste training code** | Duplicated training logic across experiments | Inconsistent behavior, maintenance burden |
| **Hardcoded values** | Magic numbers, file paths, API endpoints | Configuration brittleness |
| **Missing error handling** | Silent failures in feature computation | Runtime crashes in production |
| **No abstraction** | Everything in one monolithic script | Cannot modify components independently |
| **Dead code** | Unused functions, commented-out experiments | Confusion, increased cognitive load |
| **Missing type hints** | Untyped function signatures | Harder to maintain, more bugs |
| **No logging** | Silent execution without observability | Cannot debug production issues |

### Code Debt Indicators

| Indicator | Measurement | Threshold |
|-----------|-------------|-----------|
| **Test coverage** | % of code covered by tests | < 70% is concerning |
| **Code duplication** | % of duplicated lines | > 5% is concerning |
| **Cyclomatic complexity** | Average function complexity | > 10 is concerning |
| **Dead code ratio** | Unused code / total code | > 10% is concerning |
| **TODO/FIXME count** | Number of outstanding TODOs | Increasing trend is concerning |

## Data Debt

### Definition

Data debt accumulates when data quality, documentation, and governance are sacrificed for speed. Data debt is unique to ML and often the most impactful form of debt because it directly affects model quality.

### Common Data Debt Patterns

| Pattern | Description | Impact |
|---------|-------------|--------|
| **Missing data documentation** | Unknown provenance of training data | Cannot trust model outputs |
| **Inconsistent schemas** | Different versions of feature schemas | Train-serve skew |
| **No data validation** | Missing quality checks in pipelines | Silent data corruption |
| **Label quality issues** | Noisy, inconsistent, or outdated labels | Degraded model performance |
| **Data leakage** | Future information in training features | Inflated offline metrics |
| **Missing versioning** | No tracking of data versions | Cannot reproduce experiments |
| **Stale features** | Features no longer computed or relevant | Wasted compute, confusion |
| **Untracked data sources** | Unknown or undocumented data inputs | Audit and compliance risks |

### Data Quality Dimensions

| Dimension | Description | Measurement |
|-----------|-------------|-------------|
| **Completeness** | % of non-null values | Null rate per feature |
| **Accuracy** | Correctness of values | Validation against ground truth |
| **Consistency** | Consistent values across sources | Cross-source comparison |
| **Timeliness** | Data freshness | Age of most recent update |
| **Uniqueness** | No duplicate records | Duplicate rate |
| **Validity** | Values within expected ranges | Range checks, schema validation |

### Data Debt Tracking

```yaml
# data_quality_registry.yaml
features:
  user_age:
    null_rate: 0.15  # 15% null (was 5% last month - INCREASING)
    source: user_profile_api
    last_updated: 2024-01-15
    quality_score: 0.82  # trending down

  item_price:
    null_rate: 0.02
    source: catalog_api
    last_updated: 2024-01-15
    quality_score: 0.95  # stable

alerts:
  - feature: user_age
    metric: null_rate
    threshold: 0.20
    current: 0.15
    trend: increasing
```

## Model Debt

### Definition

Model debt occurs when models are deployed without proper maintenance, monitoring, or lifecycle management. Models degrade over time as the world changes, and unmaintained models become increasingly harmful.

### Common Model Debt Patterns

| Pattern | Description | Impact |
|---------|-------------|--------|
| **No retraining schedule** | Model trained once and never updated | Performance degradation over time |
| **Missing model monitoring** | No tracking of model quality metrics | Undetected performance issues |
| **Deprecated models in production** | Old models still serving despite being replaced | Confusion, resource waste |
| **No A/B testing** | Model changes deployed without comparison | Unknown impact of changes |
| **Missing model cards** | No documentation of model capabilities | Misuse, compliance issues |
| **Experiment graveyard** | Hundreds of experiments with no conclusions | Wasted compute, lost knowledge |
| **Hyperparameter amnesia** | Lost record of optimal hyperparameters | Cannot reproduce best model |

### Model Lifecycle Management

| Stage | Activity | Debt Risk |
|-------|----------|-----------|
| **Development** | Experimentation, hyperparameter tuning | Low (temporary) |
| **Validation** | Offline evaluation, fairness audit | Medium (skippable steps) |
| **Deployment** | Serving infrastructure setup | Medium (rushed deployment) |
| **Monitoring** | Production quality tracking | High (often neglected) |
| **Retraining** | Scheduled or trigger-based retraining | High (often forgotten) |
| **Decommission** | Removing old models from serving | High (cleanup deferred) |

### Model Monitoring Checklist

| Metric | Frequency | Alert Threshold |
|--------|----------|----------------|
| Prediction distribution | Hourly | Shift > 10% from baseline |
| Feature distribution | Hourly | Drift detected (KS test p < 0.01) |
| Serving latency | Real-time | p99 > 200ms |
| Error rate | Real-time | > 0.1% |
| User engagement metrics | Daily | CTR drop > 5% |
| Revenue metrics | Weekly | Revenue drop > 3% |
| Fairness metrics | Weekly | Demographic parity change > 5% |

## Infrastructure Debt

### Definition

Infrastructure debt accumulates when dependencies, frameworks, and tooling fall out of date, creating security vulnerabilities, compatibility issues, and maintenance burden.

### Common Infrastructure Debt Patterns

| Pattern | Description | Impact |
|---------|-------------|--------|
| **Outdated dependencies** | Using old library versions | Security vulnerabilities, missing features |
| **No dependency pinning** | Unpinned versions in requirements | Non-reproducible builds |
| **Legacy infrastructure** | Old compute platforms (e.g., Python 2, TF 1.x) | Cannot use modern tools |
| **Missing containerization** | No Docker containers for reproducibility | "Works on my machine" |
| **Manual deployment** | Deployments require manual steps | Slow, error-prone releases |
| **No infrastructure-as-code** | Manual server configuration | Cannot replicate environments |
| **Missing CI/CD** | No automated testing or deployment | Slow, risky releases |

### Dependency Management

```toml
# pyproject.toml
[project]
requires-python = ">=3.11"
dependencies = [
    "torch>=2.1.0,<3.0.0",
    "numpy>=1.24.0,<2.0.0",
    "pandas>=2.0.0,<3.0.0",
    "scikit-learn>=1.3.0,<2.0.0",
]

[tool.poetry]
# Or use poetry for strict dependency resolution
```

### Infrastructure Health Metrics

| Metric | Target | Action if Below Target |
|--------|--------|----------------------|
| Dependency freshness | All deps within 6 months | Update dependencies |
| Security vulnerability count | 0 critical, 0 high | Patch immediately |
| Docker image age | < 30 days | Rebuild images |
| CI/CD pipeline success rate | > 95% | Fix flaky tests |
| Deployment frequency | > 1 per week | Automate deployment |
| Mean time to recovery | < 1 hour | Improve monitoring |

## Measurement (Debt Tracking)

### Technical Debt Register

Maintain a running list of all known technical debt:

| ID | Category | Description | Severity | Age (months) | Estimated Effort | Owner |
|----|----------|-------------|----------|-------------|-----------------|-------|
| TD-001 | Code | Notebook training code not refactored | High | 8 | 2 weeks | @alice |
| TD-002 | Data | user_age feature has 15% null rate | Medium | 3 | 1 week | @bob |
| TD-003 | Model | No automated retraining pipeline | High | 12 | 4 weeks | @team |
| TD-004 | Infra | Still using TF 1.x for serving | High | 18 | 6 weeks | @team |
| TD-005 | Code | Missing type hints in feature code | Low | 6 | 1 week | @carol |

### Debt Quantification

```
Total Debt Score = Σ (severity_weight × age_months × effort_weeks)

Severity weights:
  Critical: 10
  High: 5
  Medium: 2
  Low: 1
```

## Prioritization (Interest Rate Analogy)

### The Interest Rate Metaphor

Technical debt accrues "interest"—the longer it remains, the more expensive it becomes to fix:

| Debt Type | Interest Rate | Why |
|-----------|--------------|-----|
| **Code debt** | Medium (10–20% per quarter) | Each new feature makes refactoring harder |
| **Data debt** | High (20–40% per quarter) | Model quality degrades continuously |
| **Model debt** | Very high (30–50% per quarter) | Production impact compounds over time |
| **Infrastructure debt** | Low–Medium (5–15% per quarter) | Stable until it becomes a crisis |

### Prioritization Framework

```
Priority = Impact × Urgency / Effort

Where:
  Impact = Users affected × Revenue impact × Frequency
  Urgency = Interest rate × Age
  Effort = Estimated person-weeks
```

### High-Priority Debt (Fix First)

1. **Data quality issues** affecting production model performance
2. **Security vulnerabilities** in dependencies
3. **Missing monitoring** for production models
4. **No retraining pipeline** (model staleness risk)

## Debt Sprints

### Definition

Dedicated sprint periods (typically 1–2 sprints per quarter) focused exclusively on addressing technical debt.

### Debt Sprint Planning

| Step | Description |
|------|-------------|
| 1. **Audit** | Review debt register, identify new debt |
| 2. **Prioritize** | Rank by interest rate × impact |
| 3. **Estimate** | Assign effort estimates to each item |
| 4. **Allocate** | Reserve 20–30% of sprint capacity for debt |
| 5. **Execute** | Work through prioritized items |
| 6. **Verify** | Test that debt reduction didn't break anything |
| 7. **Update** | Remove resolved items from debt register |

### Debt Sprint Rules

1. **No new features**: Debt sprints focus exclusively on debt reduction
2. **Measure progress**: Track debt score reduction over time
3. **Celebrate wins**: Make debt reduction visible to the team
4. **Prevent new debt**: Update processes to prevent debt recurrence
5. **Track ROI**: Measure the impact of debt reduction on velocity and quality

### Debt Sprint Cadence

| Quarter | Debt Sprints | Focus Area |
|---------|-------------|-----------|
| Q1 | Sprint 3 (2 weeks) | Data quality and validation |
| Q2 | Sprint 6 (2 weeks) | Infrastructure upgrades |
| Q3 | Sprint 9 (2 weeks) | Model lifecycle management |
| Q4 | Sprint 12 (2 weeks) | Code quality and documentation |
