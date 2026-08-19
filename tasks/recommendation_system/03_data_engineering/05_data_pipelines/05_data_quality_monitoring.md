# Data Quality Frameworks for Recommendation Systems

## Overview

Data quality directly determines recommendation quality. Corrupted features, missing values, schema drift, or stale data can silently degrade model performance, leading to poor user experiences and lost revenue. A robust data quality framework provides automated detection, alerting, and remediation of data issues before they impact downstream systems.

This document covers quality dimensions, frameworks (Great Expectations, Deequ, Soda), automated checks, quality dashboards, and quality alerting for production recommendation pipelines.

---

## Quality Dimensions

### Completeness

Completeness measures the proportion of non-null values in a dataset. Missing data directly impacts feature availability for model serving.

**Metrics:**
- **Column-level completeness**: Percentage of non-null values per column. A user feature table with 99.5% completeness on `last_purchase_date` means 0.5% of users have no purchase history.
- **Row-level completeness**: Percentage of rows with all expected columns populated. A row with any null in a required column is incomplete.
- **Table-level completeness**: Percentage of expected rows present. If the daily user event table should have 10M rows and has 8M, it is 80% complete.

**Thresholds for recommendation systems:**

| Feature Category | Minimum Completeness | Action on Breach |
|---|---|---|
| User identifiers | 100% | Halt pipeline |
| Core interaction features | 99% | Alert, investigate |
| Demographic features | 95% | Alert, impute |
| Derived/aggregated features | 90% | Alert, fall back to batch |
| Optional enrichment features | 80% | Log, continue |

### Accuracy

Accuracy measures whether data values are correct and within expected ranges. In recommendation systems, inaccurate data leads to incorrect feature values and model predictions.

**Types of accuracy violations:**
- **Range violations**: Click-through rate > 1.0, negative view counts, timestamps in the future.
- **Referential integrity**: Item IDs in interaction events that don't exist in the item catalog.
- **Format violations**: Email addresses without `@`, phone numbers with wrong length.
- **Statistical anomalies**: Feature values that deviate significantly from historical distributions (detected via Z-score, IQR, or KS tests).

### Consistency

Consistency ensures that the same data is represented the same way across different systems and tables.

**Consistency checks:**
- **Cross-table consistency**: User count in the event table matches user count in the user profile table (within tolerance).
- **Cross-system consistency**: Feature values in the online feature store match the offline training data for the same user at the same timestamp.
- **Temporal consistency**: Cumulative metrics are monotonically increasing (e.g., lifetime purchase count never decreases).
- **Encoding consistency**: Gender encoded as `M/F` in one table and `male/female` in another.

### Freshness

Freshness measures how recent the data is. In recommendation systems, stale features lead to outdated personalization.

**Freshness metrics:**
- **Data age**: Time between data generation and availability in the target system.
- **Update frequency**: How often the data is refreshed.
- **Staleness threshold**: Maximum acceptable age before the data is considered stale.

| Data Type | Expected Freshness | Maximum Staleness |
|---|---|---|
| Real-time click features | < 1 minute | 5 minutes |
| Session features | < 5 minutes | 30 minutes |
| Daily aggregations | < 1 hour after midnight | 4 hours |
| User profile updates | < 15 minutes | 1 hour |
| Item catalog | < 1 hour | 6 hours |

### Uniqueness

Uniqueness ensures that each record is represented exactly once in the dataset.

**Uniqueness violations:**
- **Duplicate events**: The same click event appears twice (common with at-least-once delivery).
- **Duplicate keys**: Multiple rows with the same primary key in a dimension table.
- **Double-counting**: Events processed by both a real-time and batch pipeline without deduplication.

---

## Quality Frameworks

### Great Expectations

Great Expectations (GX) is a Python-based data quality framework that uses declarative expectations to validate data. It integrates with Airflow, Spark, pandas, and databases.

**Core concepts:**
- **Expectations**: Declarative statements about data properties (e.g., `expect_column_values_to_not_be_null`).
- **Expectation Suites**: Collections of expectations grouped by purpose (e.g., "user_features_daily" suite).
- **Validators**: Execute expectations against a batch of data and return pass/fail results.
- **Data Docs**: Auto-generated documentation of expectations and validation results.
- **Checkpoints**: Named validation configurations that can be triggered as part of a pipeline.

**Integration with recommendation pipelines:**

| GX Feature | Recsys Use Case |
|---|---|
| Batch validation | Validate daily feature tables before training |
| Profiling | Understand feature distributions for threshold setting |
| Data Docs | Documentation of feature contracts |
| Checkpoints in Airflow | Quality gates between pipeline stages |
| Custom expectations | Domain-specific checks (e.g., item ID exists in catalog) |

### AWS Deequ

Deequ is a Spark-based data quality library developed by Amazon. It is optimized for large-scale datasets and provides metrics computation, constraint verification, and anomaly detection.

**Core concepts:**
- **Metrics**: Aggregate computations over data (e.g., completeness, uniqueness, distribution).
- **Constraints**: Condition that must be satisfied (e.g., completeness of column > 0.95).
- **Verification Suite**: Orchestrates constraint verification and produces a verification result.
- **Anomaly Detection**: Statistical methods to detect metric anomalies (e.g., suddenly decreasing row count).
- **Data Quality Actions**: Automated responses to quality issues (e.g., alert, quarantine data, halt pipeline).

**Deequ for large-scale recommendation data:**

| Capability | Description |
|---|---|
| Spark integration | Processes terabyte-scale feature tables natively |
| Incremental analysis | Reuses previous results for efficiency |
| Anomaly detection | Time-series anomaly detection on metric history |
| Metrics repository | Stores metric history in a database for trending |
| Constraint suggestions | Automatically suggests constraints based on data profiling |

### Soda

Soda is a data quality platform with a SQL-like query language (SodaCL) for defining checks. It is simpler than Great Expectations and Deequ, focusing on ease of use and quick adoption.

**SodaCL check types:**
- **Row count**: Verify minimum, maximum, or exact row count.
- **Schema checks**: Verify column names, types, and order.
- **Missing/invalid**: Check for null values, regex mismatches, or value not in set.
- **Duplicate checks**: Detect duplicate primary keys.
- **Freshness checks**: Verify data is newer than a threshold.
- **Custom SQL**: Write arbitrary SQL queries as checks.

**SodaCL example for recommendation features:**
```yaml
checks for user_features_daily:
  - row_count > 9000000
  - missing_count(user_id) = 0
  - invalid_percent(email) < 1.0:
      valid regex: ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$
  - duplicate_count(user_id) = 0
  - freshness(event_date) < 24h
  - schema:
      fail:
        when required column missing:
          - user_id
          - last_click_timestamp
          - purchase_count_30d
```

### Framework Comparison

| Feature | Great Expectations | Deequ | Soda |
|---|---|---|---|
| Language | Python | Scala/Python | YAML/SQL |
| Scale | pandas, Spark, SQL | Spark only | SQL-based |
| Learning curve | Medium | High | Low |
| Documentation | Data Docs | Metrics repository | SodaCL docs |
| Anomaly detection | Basic | Advanced | Basic |
| Airflow integration | Operator available | Custom operator | CLI-based |
| Best for | Complex validation logic | Large-scale Spark data | Quick SQL-based checks |

---

## Automated Quality Checks

### Check Scheduling

Quality checks should run at multiple points in the pipeline:

| Check Point | Timing | Purpose |
|---|---|---|
| **Source ingestion** | After data arrives | Validate raw data before processing |
| **Post-transformation** | After each ETL step | Catch transformation errors |
| **Pre-training** | Before model training | Ensure training data quality |
| **Post-training** | After model training | Validate model output quality |
| **Pre-deployment** | Before model serving | Final quality gate |
| **Continuous monitoring** | Real-time or hourly | Detect quality degradation |

### Check Execution Models

- **Blocking checks**: Fail the pipeline immediately on quality breach. Use for critical checks (missing primary keys, schema violations).
- **Non-blocking checks**: Log warnings but continue processing. Use for soft quality issues (slightly elevated null rates).
- **Quarantine checks**: Route failing records to a quarantine table for investigation. Use for data that is partially valid.
- **Anomaly checks**: Compare current metrics against historical baselines. Use for detecting subtle quality degradation.

### Check Result Storage

Store quality check results for trending, debugging, and audit:

- **Structured results**: Store pass/fail status, metric values, and check parameters in a database.
- **Time-series metrics**: Store metric values over time for trend analysis and anomaly detection.
- **Alert correlation**: Link quality check failures to downstream impact (model performance degradation, user experience issues).

---

## Quality Dashboards

### Dashboard Components

A comprehensive data quality dashboard should include:

**Overview panel:**
- Overall quality score (weighted average of all checks)
- Number of passing/failing/warning checks
- Trend over time (improving, stable, degrading)
- Top 5 quality issues by severity

**Dimension-specific panels:**
- **Completeness**: Null rates per column over time, with thresholds
- **Accuracy**: Range violation counts, statistical anomaly alerts
- **Consistency**: Cross-system consistency metrics, encoding mismatches
- **Freshness**: Data age per table, update frequency compliance
- **Uniqueness**: Duplicate record counts, primary key violation rates

**Pipeline-specific panels:**
- Quality gate pass/fail rates per pipeline
- Quality check duration and performance
- Historical quality trends correlated with model performance

### Dashboard Tools

| Tool | Use Case | Integration |
|---|---|---|
| **Grafana** | Real-time quality metrics | Prometheus, InfluxDB, SQL |
| **Great Expectations Data Docs** | Expectation documentation | GX validation results |
| **Deequ Metrics Repository** | Spark-based quality metrics | JDBC database |
| **Custom dashboards** | Domain-specific views | Airflow, MLflow |
| **Soda Dashboard** | Soda check results | Soda Cloud |

---

## Quality Alerting

### Alert Severity Levels

| Level | Criteria | Response Time | Channel |
|---|---|---|---|
| **Critical** | Data pipeline halted, feature store unavailable | Immediate | PagerDuty, phone |
| **High** | Core feature quality breach, training data affected | < 30 minutes | Slack #alerts, PagerDuty |
| **Medium** | Non-critical quality degradation, anomaly detected | < 4 hours | Slack #data-quality |
| **Low** | Minor quality issue, informational | Next business day | Email |

### Alert Design

**Actionable alerts:**
- Include the specific check that failed, the metric value, and the threshold.
- Link to the quality dashboard for visual context.
- Include a runbook link with remediation steps.
- Distinguish between transient issues (retry may fix) and systemic issues (requires investigation).

**Alert fatigue prevention:**
- Use severity levels to control notification frequency.
- Implement alert grouping and deduplication.
- Require manual acknowledgment for critical alerts.
- Review and tune alert thresholds quarterly based on false positive rates.

### Automated Remediation

| Issue | Automated Response |
|---|---|
| Stale data | Trigger upstream pipeline re-run |
| Schema change | Halt downstream, notify schema owner |
| Null rate spike | Fall back to default feature values |
| Duplicate records | Dedup and reprocess |
| Distribution shift | Retrain model with recent data |
| Pipeline failure | Retry with exponential backoff |

---

## Quality Culture

### Quality Ownership

Data quality is everyone's responsibility, but specific roles should be defined:

- **Data producers**: Responsible for quality at the source. Own source-level quality checks and schemas.
- **Data engineers**: Responsible for pipeline quality. Own transformation logic, quality gates, and monitoring.
- **ML engineers**: Responsible for feature and model quality. Own feature validation, model evaluation, and serving quality.
- **Data stewards**: Responsible for data governance. Own quality standards, policies, and cross-team coordination.

### Quality SLAs

Define explicit quality SLAs for each data product:

| Data Product | SLA | Measurement |
|---|---|---|
| User click features | Completeness > 99.5%, Freshness < 5 min | Hourly check |
| Item catalog | Completeness > 99.9%, Freshness < 1 hour | Hourly check |
| Training dataset | All quality checks pass | Per training run |
| Feature store | All features available, freshness within SLA | Continuous monitoring |

### Quality Reviews

- **Weekly quality reviews**: Review quality trends, discuss recurring issues, and prioritize improvements.
- **Post-incident quality reviews**: After any quality-related incident, conduct a root cause analysis and implement preventive checks.
- **Quarterly quality audits**: Comprehensive review of all quality checks, thresholds, and alerting configurations.
