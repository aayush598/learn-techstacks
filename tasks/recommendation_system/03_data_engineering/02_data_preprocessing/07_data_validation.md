# Data Validation — Recommendation System Data Preprocessing

## 1. Why Data Validation is Critical

### 1.1 The Cost of Bad Data

- **Garbage In, Garbage Out**: A recommendation model trained on invalid data will produce invalid recommendations. No amount of algorithmic sophistication can compensate for fundamentally flawed data.
- **Silent Failures**: Invalid data does not always cause crashes — it often causes subtle degradation that goes undetected for weeks or months, gradually eroding recommendation quality.
- **Cascading Errors**: Invalid data in the feature pipeline propagates through model training, inference, and evaluation, contaminating every downstream component.
- **Revenue Impact**: In production recommendation systems, data quality issues can cause measurable revenue loss through incorrect recommendations, broken personalization, or user experience degradation.

### 1.2 Validation Dimensions

| Dimension | Description | Example |
|-----------|-------------|---------|
| **Completeness** | Are required fields present? | Missing user_id in interaction event |
| **Validity** | Do values conform to expected formats? | Invalid email format, negative purchase amount |
| **Consistency** | Are related fields logically consistent? | Event timestamp before user account creation |
| **Freshness** | Is the data recent enough for its use case? | 30-day-old "real-time" feature |
| **Accuracy** | Does the data reflect reality? | Item price of $0.00 for a $50 product |
| **Uniqueness** | Are there duplicate records? | Same interaction event logged twice |

---

## 2. Schema Validation

### 2.1 Schema Definition

Define explicit schemas for every data source, specifying expected field names, types, constraints, and relationships.

- **Interaction Event Schema**:
  ```yaml
  event_id: string (UUID, required, unique)
  user_id: string (required, format: "usr_[0-9]+")
  item_id: string (required, format: "itm_[0-9]+")
  event_type: enum (required, values: [view, click, purchase, rate, add_to_cart, remove_from_cart])
  timestamp: datetime (required, ISO 8601, must be ≤ current_time)
  session_id: string (required)
  device_type: enum (values: [mobile, desktop, tablet, tv, other])
  country_code: string (required, ISO 3166-1 alpha-2)
  rating_value: float (optional, range: [0.0, 5.0], required if event_type = "rate")
  ```

### 2.2 Schema Validation Tools

| Tool | Type | Strengths | Use Case |
|------|------|-----------|----------|
| **Great Expectations** | Python library | Rich expectation library, data docs, integration with data platforms | Comprehensive validation pipelines |
| **Pandera** | Python library | DataFrame-level validation, integrates with pandas/polars | In-memory data validation |
| **Pydantic** | Python library | Fast, type-safe validation | API request/response validation |
| **Protobuf / Avro** | Schema format | Binary serialization, schema evolution | Event schema enforcement |
| **JSON Schema** | Schema format | Declarative, widely supported | API payload validation |
| **dbt Tests** | SQL-based | SQL-native, integrates with data warehouse | Warehouse table validation |

### 2.3 Schema Evolution Management

- **Backward Compatibility**: New schema versions must accept data written by old schema versions. Adding optional fields is backward-compatible; removing or renaming fields is not.
- **Forward Compatibility**: Old consumers must be able to read data written by new schema versions. Ignoring unknown fields is the minimum requirement.
- **Schema Registry**: Use a schema registry (e.g., Confluent Schema Registry for Kafka) to manage schema versions, enforce compatibility rules, and prevent breaking changes.
- **Version Tagging**: Every data record must include a schema version tag to enable version-aware validation and processing.

---

## 3. Statistical Validation

### 3.1 Distribution Validation

Compare the statistical properties of incoming data against expected distributions.

- **Numerical Features**:
  - **Range Check**: Values must fall within expected bounds (e.g., ratings in [0, 5], prices > 0).
  - **Distribution Check**: Compare the distribution of incoming data against a reference distribution using Kolmogorov-Smirnov test, Wasserstein distance, or Population Stability Index (PSI).
  - **Percentile Monitoring**: Track P1, P5, P25, P50, P75, P95, P99 of key metrics and alert if they deviate significantly from historical values.

- **Categorical Features**:
  - **Value Set Check**: Ensure all values are within the allowed set (e.g., event_type ∈ {view, click, purchase, ...}).
  - **Cardinality Check**: Monitor the number of unique values. A sudden increase may indicate data corruption or a new data source.
  - **Frequency Distribution**: Compare the frequency distribution of categorical values against historical baselines using chi-squared test or KL divergence.

### 3.2 Statistical Tests for Data Validation

| Test | Use Case | Null Hypothesis | When to Reject |
|------|----------|-----------------|----------------|
| **Kolmogorov-Smirnov** | Distribution comparison | Two samples from same distribution | p-value < 0.01 |
| **Chi-Squared** | Categorical frequency comparison | Observed frequencies match expected | p-value < 0.01 |
| **Z-Proportion** | Rate comparison (CTR, conversion) | Two rates are equal | |z| > 3.0 |
| **Anderson-Darling** | Normality testing | Data is normally distributed | p-value < 0.05 |
| **Benford's Law** | Digit distribution fraud detection | First digits follow Benford's law | χ² statistic > threshold |

### 3.3 Data Drift Detection

- **Concept Drift**: The relationship between features and target changes over time (e.g., user preferences shift seasonally).
- **Data Drift (Covariate Shift)**: The distribution of features changes over time (e.g., a new user segment with different behavior joins the platform).
- **Label Drift**: The distribution of the target variable changes (e.g., overall purchase rate increases due to a marketing campaign).

**Detection Methods**:
- **PSI (Population Stability Index)**: PSI < 0.1: no significant drift; PSI 0.1–0.25: moderate drift; PSI > 0.25: significant drift requiring investigation.
- **ADWIN (Adaptive Windowing)**: Automatically detects drift by monitoring the mean of a streaming variable over an adaptive window size.
- **Page-Hinkley Test**: Detects changes in the mean of a Gaussian signal. Used for streaming drift detection.

---

## 4. Business Logic Validation

### 4.1 Referential Integrity

- **Foreign Key Checks**: Every user_id in interaction events must reference an existing user in the user table. Every item_id must reference an existing item in the item catalog.
- **Temporal Consistency**: Event timestamps must be after user account creation time and after item creation time.
- **Logical Consistency**: A "purchase" event must have an associated item. A "rate" event must have a rating value. A "remove_from_cart" event should be preceded by an "add_to_cart" event for the same user-item pair.

### 4.2 Business Rule Validation

| Rule Category | Example Rules | Action on Violation |
|--------------|---------------|-------------------|
| **User Rules** | user.age ≥ 13 (COPPA compliance); user.email matches regex | Reject event, log violation |
| **Item Rules** | item.price > 0; item.category ∈ valid_categories | Flag item for review |
| **Event Rules** | event.timestamp ≤ now(); event.timestamp ≥ item.created_at | Reject event |
| **Interaction Rules** | Same user cannot purchase the same item twice (unless explicitly allowed) | Deduplicate or flag |
| **Aggregation Rules** | Daily purchase count per user < 100 (anti-fraud) | Flag for manual review |

### 4.3 Cross-Source Consistency

- **User Profile vs Events**: If a user's demographic profile indicates they are from the US, but their events show activity from 10 different countries in a single day, this is a consistency violation (possible shared account or bot).
- **Item Metadata vs Catalog**: If an item's price in the interaction event log differs from the price in the item catalog by more than 5%, flag for reconciliation.
- **Feature Store vs Raw Data**: If a computed feature in the feature store differs from the expected value computed from raw data, flag for investigation.

---

## 5. Great Expectations for Recommendation Systems

### 5.1 Core Expectations

| Expectation | Description | Implementation |
|-------------|-------------|---------------|
| `expect_column_values_to_not_be_null` | Required fields must be present | `user_id`, `item_id`, `event_type`, `timestamp` |
| `expect_column_values_to_be_in_set` | Categorical fields must have valid values | `event_type` in valid set |
| `expect_column_values_to_be_between` | Numerical fields must be in valid range | `rating_value` in [0, 5] |
| `expect_column_values_to_match_regex` | String fields must match format | `user_id` matches pattern |
| `expect_table_row_count_to_be_between` | Table volume within expected range | Daily events between 10M and 500M |
| `expect_column_unique_value_count_to_be_between` | Cardinality within expected range | Unique items between 1M and 100M |
| `expect_compound_columns_to_be_unique` | Composite uniqueness constraint | (user_id, item_id, timestamp) unique |

### 5.2 Custom Expectations for Recommendation Data

- **Interaction Rate Validation**: The click-through rate for any item should be between 0.01 and 0.95. Values outside this range suggest data quality issues.
- **Session Continuity**: Events within a session should have monotonically increasing timestamps.
- **Feature Freshness**: Real-time features should be updated within 60 seconds of the latest event.
- **Embedding Validity**: Embedding vectors should have no NaN values, should be approximately unit-normalized (if using cosine similarity), and should have reasonable magnitude (within 3 standard deviations of the training distribution).

---

## 6. Automated Validation Pipelines

### 6.1 Pipeline Architecture

```
Data Ingestion → Schema Validation → Statistical Validation → Business Logic Validation → Quality Score → Pass/Fail
    │                    │                     │                       │                        │              │
    │              Check schema         Check distributions,     Check referential        Compute        Alert on
    │              compatibility        drift, outliers          integrity, rules         quality score  failure
    │
    ├── Passed → Continue to preprocessing pipeline
    ├── Failed (critical) → Reject data, alert on-call, route to dead letter queue
    └── Failed (warning) → Accept data with quality flag, log warning, continue
```

### 6.2 Validation SLAs

| Validation Type | Timeout | Failure Action | Retry Policy |
|----------------|---------|----------------|-------------|
| Schema Validation | < 1 second per batch | Reject batch | No retry |
| Statistical Validation | < 30 seconds per batch | Flag for review | No retry |
| Business Logic Validation | < 60 seconds per batch | Reject invalid records, accept valid | No retry |
| Great Expectations Suite | < 5 minutes per batch | Critical: reject; Warning: accept with flag | No retry |
| Full Data Profiling | < 30 minutes (daily) | Generate quality report, alert if score < threshold | Retry once |

### 6.3 Data Quality Scoring

Compute a composite data quality score for each data batch:

```
Quality Score = w1 × Completeness + w2 × Validity + w3 × Consistency + w4 × Freshness
```

Where:
- **Completeness** = 1 - (count of missing required values / total required values)
- **Validity** = 1 - (count of invalid values / total values)
- **Consistency** = 1 - (count of consistency violations / total records)
- **Freshness** = 1 - (average data age in seconds / maximum acceptable age in seconds)

**Thresholds**:
- Score ≥ 0.95: Pass — proceed normally
- Score 0.80–0.95: Warning — accept with quality flag, investigate
- Score < 0.80: Critical — reject batch, alert on-call, investigate root cause

### 6.4 Monitoring and Alerting

- **Data Quality Dashboard**: Real-time dashboard showing completeness, validity, consistency, and freshness metrics for each data source.
- **Anomaly Alerts**: Alert when any quality metric drops below its historical average by more than 2 standard deviations.
- **Trend Alerts**: Alert when quality metrics show a sustained downward trend over 7 days.
- **SLO Integration**: Data quality SLOs should be integrated into the overall system SLO framework, with error budgets that trigger investigation when consumed.
