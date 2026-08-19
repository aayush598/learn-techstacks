# Data Pipeline Testing

## 1. Overview

Data pipelines are the backbone of a recommendation system, transforming raw user interactions,
item metadata, and contextual signals into features, training datasets, and real-time signals.
Pipeline failures directly impact recommendation quality. This document defines comprehensive
testing strategies for data pipelines including transformation logic, schema validation, data
quality assertions, Spark/Flink job tests, and feature computation tests.

### 1.1 Pipeline Architecture Under Test

```
Raw Sources → Ingestion → Processing → Storage → Serving
    ↓            ↓           ↓           ↓          ↓
Clickstream   Kafka/Kinesis  Spark/Flink  S3/D1/Hive  Feature Store
User DB       CDC streams    SQL transforms  Redis      Model Registry
Item Catalog  REST APIs      Python ops      Elasticsearch
```

### 1.2 Testing Layers

| Layer | What | Tool Examples | Execution |
|---|---|---|---|
| Transformation logic | SQL/Python correctness | dbt tests, pytest | Per commit |
| Schema validation | Output structure compliance | Great Expectations, Pandera | Per commit |
| Data quality | Completeness, accuracy, timeliness | dbt tests, custom assertions | Nightly |
| Distributed compute | Spark/Flink correctness | PySpark test框架, TestContainers | Per merge |
| Feature computation | Feature value accuracy | Custom harness | Nightly |

---

## 2. Transformation Logic Tests

### 2.1 SQL Transformation Testing

SQL transformations power most batch feature computation. Each transformation must be
tested for correctness against known inputs and expected outputs.

**Testing approach using dbt-style tests:**

```sql
-- Example: User engagement rate calculation
-- Test: CTR calculation matches manual computation

-- Input fixture:
-- user_id | item_id | impressions | clicks
-- u1      | i1      | 100         | 15
-- u2      | i2      | 200         | 0

-- Expected output:
-- user_id | engagement_rate
-- u1      | 0.15
-- u2      | 0.00

-- Test assertion:
-- ABS(output.engagement_rate - expected.engagement_rate) < 0.0001
```

**Test categories for SQL transformations:**

| Category | Description | Example |
|---|---|---|
| Aggregation correctness | SUM, COUNT, AVG calculations | Daily active user counts |
| Join correctness | Multi-table join logic | User profile + interaction join |
| Window function correctness | ROW_NUMBER, LEAD/LAG, running aggregates | Sessionization, ranking |
| Null handling | NULL propagation and coalescence | Missing feature defaults |
| Edge cases | Division by zero, empty groups, single-row windows | Zero-impression items |
| Temporal logic | Date arithmetic, timezone handling | Daily vs weekly aggregations |

### 2.2 Python Transformation Testing

For transformations written in Python (Pandas, Polars, or custom logic):

**Test structure:**

1. **Input fixture creation**: Build minimal DataFrames with known values
2. **Transformation execution**: Apply the transformation function
3. **Output validation**: Compare against expected output with tolerance
4. **Side effect verification**: Ensure no unintended mutations of input data
5. **Performance assertion**: Transformation completes within time budget

**Common transformation test patterns:**

- **Numerical accuracy**: Assert output within epsilon of expected values
- **String transformations**: Exact match for cleaned/normalized strings
- **Categorical encoding**: Verify mapping consistency across runs
- **Temporal transformations**: Timezone-aware date arithmetic correctness
- **Filtering logic**: Correct inclusion/exclusion of records

### 2.3 Cross-Validation Between Implementations

When transformations exist in both SQL and Python (common during migrations):

- Execute both implementations on identical inputs
- Compare outputs record-by-record with numerical tolerance
- Log any discrepancies for investigation
- Track convergence percentage over time
- Maintain parity test suite during migration period

---

## 3. Schema Validation Tests

### 3.1 Schema Definition

Every pipeline output must conform to a registered schema. Schema validation prevents
runtime failures in downstream consumers.

**Schema definition format:**

```yaml
schema:
  name: user_daily_features
  version: 3
  fields:
    - name: user_id
      type: string
      nullable: false
      description: Unique user identifier
    - name: feature_date
      type: date
      nullable: false
      description: Feature computation date
    - name: click_count_7d
      type: integer
      nullable: false
      min_value: 0
      description: Number of clicks in last 7 days
    - name: avg_dwell_time_30d
      type: float
      nullable: true
      min_value: 0.0
      description: Average dwell time in seconds over 30 days
    - name: category_preferences
      type: map<string, float>
      nullable: false
      description: Category affinity scores
  partitions:
    - field: feature_date
      type: date
  primary_key: [user_id, feature_date]
```

### 3.2 Schema Validation Test Types

| Test Type | Description | Failure Impact |
|---|---|---|
| Field existence | All expected fields present | Critical - downstream breakage |
| Type correctness | Field types match specification | Critical - serialization errors |
| Nullable compliance | Null fields marked nullable | High - null pointer exceptions |
| Primary key uniqueness | No duplicate PK combinations | Critical - data duplication |
| Partition completeness | All expected partitions exist | High - missing data for date ranges |
| Enum validation | Categorical values in allowed set | Medium - unexpected categories |
| Range validation | Numerical values within bounds | Medium - feature corruption |

### 3.3 Schema Evolution Testing

Schema changes must be tested for backward compatibility:

- **Additive changes**: New nullable fields are backward-compatible
- **Type changes**: Widening types (int → long) are safe; narrowing is breaking
- **Removal changes**: Removing fields breaks downstream consumers
- **Rename changes**: Treat as remove + add with migration period
- **Partition changes**: Changing partition column breaks historical data access

**Compatibility matrix:**

| Change Type | Backward Compatible | Forward Compatible | Migration Required |
|---|---|---|---|
| Add nullable field | Yes | No | No |
| Add required field | No | No | Yes |
| Remove field | No | Yes | Yes |
| Widen type | Yes | Yes | No |
| Narrow type | No | No | Yes |
| Rename field | No | No | Yes |

---

## 4. Data Quality Assertion Tests

### 4.1 Data Quality Dimensions

| Dimension | Description | Measurement | Threshold |
|---|---|---|---|
| Completeness | No missing required values | % non-null in required fields | > 99.9% |
| Accuracy | Values reflect reality | Cross-source validation | > 99.5% |
| Timeliness | Data available within SLA | Age of newest record | < 4 hours |
| Consistency | No contradictory data | Cross-table reconciliation | 100% |
| Uniqueness | No unintended duplicates | Duplicate detection queries | 0 duplicates |
| Validity | Values within acceptable ranges | Range checks per field | > 99.9% |

### 4.2 Great Expectations Patterns

Common data quality expectations for recommendation systems:

**Completeness expectations:**

```
expect_column_values_to_not_be_null: user_id, item_id, timestamp
expect_table_row_count_to_be_between: min=1000000, max=50000000
expect_column_values_to_be_unique: composite_key (user_id, item_id, timestamp)
```

**Distribution expectations:**

```
expect_column_values_to_be_between: click_count, min=0, max=10000
expect_column_mean_to_be_between: dwell_time_seconds, min=10, max=300
expect_column_proportion_of_unique_values_to_be_between: category, min=0.001, max=0.5
```

**Pattern expectations:**

```
expect_column_values_to_match_regex: user_id, pattern="^usr_[a-f0-9]{16}$"
expect_column_values_to_be_in_set: interaction_type, values=["click","purchase","save","share"]
expect_column_values_to_match_date_format: event_date, format="%Y-%m-%d"
```

### 4.3 Data Quality Gate Workflow

```
Pipeline Output → Quality Check → Gate Decision
                      ↓               ↓
              ┌───────┼───────┐   ┌───┴───┐
              ↓       ↓       ↓   ↓       ↓
         Critical Warning Info Pass  Fail
              ↓       ↓       ↓   ↓       ↓
          Block    Alert   Log  Publish  Block &
          pipeline  team  metrics       alert
```

**Gate criteria:**

- **Critical failures**: Any critical assertion fails → block downstream pipeline
- **Warning failures**: Warning assertion fails → alert but allow with monitoring
- **Info failures**: Info assertion fails → log for analysis, no action required
- **Trend detection**: Metrics trending toward thresholds → proactive alerting

### 4.4 Data Quality Monitoring

Continuous monitoring beyond pipeline-time checks:

- **Hourly distribution snapshots**: Track feature distributions over time
- **Daily completeness reports**: Percentage of expected records produced
- **Weekly anomaly detection**: Statistical tests for unexpected distribution shifts
- **Monthly quality scorecard**: Aggregate quality metrics for stakeholder review

---

## 5. Spark Job Tests

### 5.1 Spark Testing Challenges

- **Distributed execution**: Tests must work with local mode and mini-cluster
- **Non-determinism**: Partition-level ordering may vary across runs
- **Resource management**: Tests should not require full cluster allocation
- **Serialization**: UDFs and custom functions require serialization testing
- **State management**: Shuffle operations create complex state dependencies

### 5.2 Spark Unit Testing Strategy

**Local mode testing with PySpark:**

- Create SparkSession in local mode with limited resources
- Use small datasets (< 100MB) for fast test execution
- Repartition(1) for deterministic ordering in assertions
- Cache test DataFrames to avoid repeated computation
- Stop SparkSession after each test class for resource cleanup

**Test categories for Spark jobs:**

| Category | Description | Data Size | Execution Time |
|---|---|---|---|
| UDF correctness | Custom function behavior | < 1 MB | < 1 second |
| Transformation logic | Map/filter/reduce operations | < 10 MB | < 5 seconds |
| Aggregation correctness | Group-by and join operations | < 100 MB | < 30 seconds |
| Partition behavior | Data distribution across partitions | < 500 MB | < 2 minutes |
| Performance regression | Execution time and shuffle volume | 1-10 GB | < 10 minutes |

### 5.3 Spark Integration Testing

**TestContainers approach:**

- Spin up Spark master and worker containers
- Submit job with test configuration
- Verify output in test storage (HDFS/S3 mock)
- Check job metrics (records processed, shuffle bytes, task count)
- Clean up containers after test completion

**Key assertions:**

- Output record count matches expected
- Output schema matches registered schema
- Aggregated values match reference computation
- Job completes within time budget
- No data skew (no single task takes > 3x average)
- Shuffle spill is within acceptable limits

### 5.4 Spark Job Performance Tests

- **Baseline execution time**: Record and track execution time per job
- **Resource utilization**: Monitor CPU, memory, and shuffle usage
- **Scaling tests**: Verify linear scaling with input size increase
- **Data skew detection**: Ensure no partition processes disproportionate data
- **Caching effectiveness**: Measure cache hit rates and recomputation frequency

---

## 6. Flink Job Tests

### 6.1 Stream Processing Test Challenges

Flink jobs process unbounded streams, requiring different testing approaches than batch:

- **Event-time processing**: Tests must handle watermarks and late events
- **State management**: Tests must validate state correctness across checkpoints
- **Exactly-once semantics**: Tests must verify no duplicates or data loss
- **Window operations**: Tests must validate window boundaries and trigger logic
- **Backpressure**: Tests must verify behavior under varying input rates

### 6.2 Flink Unit Testing Strategy

**MiniClusterWithClientResource approach:**

- Use Flink's MiniCluster for local execution
- Inject test data through DataStream sources
- Collect output through test sinks
- Validate output records against expected results
- Test with multiple parallelism levels

**Key test scenarios:**

| Scenario | Description | Validation |
|---|---|---|
| Event ordering | Events arrive out of order | Output is correctly ordered by event time |
| Late events | Events arrive after watermark | Late events handled per policy |
| State snapshots | Checkpoint and restore | State is correctly restored after failure |
| Window triggers | Tumbling/sliding/session windows | Windows fire at correct boundaries |
| Watermark generation | Watermarks advance correctly | No premature window firing |
| Backpressure | Input rate exceeds processing | System remains stable, no data loss |

### 6.3 Flink State Backend Testing

- **RocksDB state backend**: Test large state with RocksDB backend
- **Heap state backend**: Test fast small-state operations
- **Incremental checkpoints**: Verify incremental checkpoint correctness
- **State TTL**: Verify expired state is correctly cleaned up
- **State migration**: Test schema evolution for stateful operators

### 6.6 Flink Exactly-Once Testing

Verification strategy for exactly-once processing guarantees:

1. **Duplicate detection**: Inject known duplicates, verify output has no duplicates
2. **Data loss detection**: Count input records, verify output count matches
3. **Checkpoint recovery**: Kill and restart job, verify no data loss or duplication
4. **Sink idempotency**: Verify output sinks handle duplicate writes gracefully
5. **End-to-end exactly-once**: Verify source → processing → sink maintains guarantee

---

## 7. Feature Computation Tests

### 7.1 Feature Types and Testing Approaches

| Feature Type | Computation | Test Strategy | Tolerance |
|---|---|---|---|
| Count features | Aggregation over time window | Exact count comparison | 0 |
| Ratio features | Division of two counts | Numerical tolerance | 0.0001 |
| Statistical features | Mean, std, percentiles | Distribution comparison | 0.01 |
| Embedding features | Neural network forward pass | Cosine similarity | 0.01 |
| Temporal features | Time-based calculations | Timestamp comparison | 1 second |
| Text features | NLP processing | Semantic similarity | 0.05 |
| Graph features | Network analysis | Structural comparison | Exact match |

### 7.2 Feature Computation Correctness

**Testing approach:**

1. Create input data with known values
2. Compute features using pipeline implementation
3. Compute reference values using manual calculation
4. Compare outputs with appropriate tolerance
5. Validate edge cases (empty inputs, single records, maximum values)

**Common correctness issues:**

- Off-by-one errors in time window boundaries
- Incorrect handling of null values in aggregations
- Floating-point precision errors in feature normalization
- Timezone-related errors in temporal features
- Off-by-one in rolling window start/end times
- Incorrect handling of duplicate events

### 7.3 Feature Freshness Validation

For both batch and real-time features:

**Batch features:**

- Verify computation completes before downstream consumers need data
- Validate partition timestamps are correct and monotonic
- Check that incremental computation includes all recent events
- Verify late-arriving data is correctly incorporated

**Real-time features:**

- Measure end-to-end latency from event to feature availability
- Validate sliding window boundaries are accurate to within 1 second
- Check that feature values update at expected frequency
- Verify stale features are correctly evicted from feature store

### 7.4 Feature Distribution Tests

Ensure computed features have expected statistical properties:

- **Mean and standard deviation**: Within expected ranges
- **Distribution shape**: Histogram matches expected distribution
- **Outlier rate**: Percentage of extreme values is within bounds
- **Missing rate**: Null percentage within acceptable threshold
- **Cardinality**: Unique value counts match expectations

### 7.5 Feature Importance Tests

Validate that features maintain expected importance rankings:

- **Offline importance scores**: Feature importance from trained model
- **A/B test validation**: Feature impact measured in online experiments
- **Correlation checks**: Features maintain expected correlations with targets
- **Redundancy detection**: No unexpected feature redundancy or collinearity
- **Stability**: Feature importance rankings stable across training runs

### 7.6 Feature Store Integration Tests

Test the complete feature store lifecycle:

```
Write Operation → Feature Store → Read Operation → Validation
      ↓                ↓               ↓              ↓
  Register      Materialize       Serve         Compare
  feature       to store          feature       with expected
  definition    (batch/real-time) value         value
```

**Integration test scenarios:**

| Scenario | Validation |
|---|---|
| Write and read consistency | Feature read after write returns correct value |
| Batch materialization | Scheduled batch jobs populate feature store on time |
| Real-time materialization | Streaming updates propagate within SLA |
| Feature versioning | Multiple versions coexist correctly |
| Feature group operations | Group read/write operations are atomic |
| Feature store failure | Graceful degradation with stale features |
| Feature store recovery | Features correctly restored after failure |

---

## 8. Test Infrastructure

### 8.1 Test Data Management

- **Fixture factories**: Generate test data with controlled distributions
- **Golden datasets**: Curated datasets with known correct outputs
- **Data builders**: Fluent API for constructing test scenarios
- **Snapshot testing**: Compare pipeline outputs against saved snapshots

### 8.2 Test Execution Environment

- **CI pipeline**: Fast tests (unit, schema) run on every commit
- **Nightly pipeline**: Medium tests (data quality, feature correctness)
- **Weekly pipeline**: Heavy tests (full integration, performance)
- **On-demand pipeline**: Ad-hoc tests for debugging and investigation

### 8.3 Test Reporting

- **Per-commit report**: Tests passed, coverage, execution time
- **Trend dashboard**: Test results, data quality metrics, performance trends
- **Failure alerting**: Automated notification for test failures with context
- **Root cause hints**: Common failure patterns with suggested investigation steps
