# Testing Data Pipelines for Recommendation Systems

## Overview

Data pipeline testing ensures that transformations produce correct results, schemas remain stable, and regressions are caught before reaching production. Unlike application testing, pipeline testing must validate data correctness, schema evolution, performance, and integration across heterogeneous systems (Kafka, Spark, Flink, feature stores, databases).

This document covers unit tests, integration tests, data contract testing, schema validation, regression testing, and CI/CD integration for recommendation system pipelines.

---

## Unit Tests for Transformations

### Why Unit Test Transformations?

Transformations are the core logic of data pipelines—filtering, joining, aggregating, and enriching data. A bug in a transformation silently produces incorrect features, which degrade model performance without obvious error signals. Unit tests catch these bugs in isolation, before integration with external systems.

### Testing Patterns

**Input-output testing**: Define input data, apply the transformation, and assert the expected output. This is the most straightforward pattern for pure functions and simple transformations.

**Boundary testing**: Test edge cases that are common in real-world data:
- Empty inputs (no events for a user)
- Null values in required fields
- Maximum-size inputs (user with 10,000 events)
- Duplicate records in input
- Events with timestamps at epoch boundaries (midnight, month end)

**Property-based testing**: Define properties that must hold for any input (e.g., output row count <= input row count after filtering). Use tools like Hypothesis (Python) or ScalaCheck (JVM) to generate random inputs and verify properties.

### Transformation Test Categories

| Transformation | Test Focus | Example |
|---|---|---|
| Filtering | Correct rows retained/dropped | Click events with null user_id are dropped |
| Aggregation | Correct grouping and computation | Click count per user matches expected |
| Join | Correct row matching, handling of missing keys | User event join preserves all events |
| Deduplication | Correct dedup logic, tie-breaking | Latest event retained for duplicate timestamps |
| Windowing | Correct window assignment and emission | Event assigned to correct time window |
| Enrichment | Correct lookup, handling of missing lookups | Item metadata joined correctly |

### Testing Stateful Logic

Stateful transformations (windowed aggregations, session computation, stateful filters) are harder to test because they depend on event ordering and state accumulation.

**Strategies:**
- **Event sequence testing**: Provide a sequence of events and verify intermediate and final state values.
- **State snapshot testing**: Freeze state at known points and verify its contents.
- **Timer testing**: For state with time-based cleanup, advance the clock and verify state expiration.

---

## Integration Tests

### What Integration Tests Cover

Integration tests validate the pipeline's interaction with external systems—message brokers, databases, feature stores, and object storage. They catch issues that unit tests miss: serialization/deserialization errors, connection failures, incorrect query syntax, and data format mismatches.

### Test Infrastructure

| Component | Production Equivalent | Test Approach |
|---|---|---|
| Kafka | Kafka cluster | Embedded Kafka (Testcontainers) |
| Spark/Flink | Spark/Flink cluster | Local mode or mini-cluster |
| Feature Store | Redis/DynamoDB | Embedded Redis (Testcontainers) |
| Database | PostgreSQL/MySQL | Embedded PostgreSQL (Testcontainers) |
| Object Storage | S3/GCS | MinIO (S3-compatible) |

**Testcontainers** provide Docker-based test infrastructure that starts real services for integration testing. This eliminates mock-related bugs where tests pass against mocks but fail against real systems.

### End-to-End Pipeline Tests

End-to-end tests execute the full pipeline—from data ingestion to feature output—and verify the complete flow:

1. Publish test events to Kafka.
2. Execute the Flink/Spark pipeline.
3. Verify features are written to the feature store.
4. Verify feature values match expected computations.
5. Clean up test data.

**Test data management:**
- **Synthetic data generation**: Create realistic test data that covers common scenarios and edge cases.
- **Data fixtures**: Maintain a set of known-good input datasets with expected outputs.
- **Test isolation**: Each test run uses unique keys/prefixes to avoid interference between parallel tests.
- **Cleanup**: Always clean up test data after test completion to prevent test pollution.

---

## Data Contract Testing

### What Are Data Contracts?

Data contracts are formal agreements between data producers and consumers that define:
- **Schema**: Column names, types, nullability, and constraints.
- **Semantics**: What each column represents, units, valid ranges.
- **SLAs**: Freshness, completeness, and availability guarantees.
- **Evolution rules**: How the schema can change over time (additive changes only, no removals or type changes).

### Contract Definition

A data contract for a recommendation system event might specify:

| Field | Type | Nullable | Description | Constraints |
|---|---|---|---|---|
| `user_id` | STRING | No | Unique user identifier | Non-empty, UUID format |
| `item_id` | STRING | No | Unique item identifier | Non-empty |
| `event_type` | STRING | No | Type of interaction | One of: click, view, purchase, search |
| `timestamp` | BIGINT | No | Event timestamp (epoch ms) | > 1609459200000 (2021-01-01) |
| `context` | MAP | Yes | Additional context | Keys: device, location |
| `revenue` | DOUBLE | Yes | Transaction revenue | >= 0 if present |

### Contract Enforcement

**Producer-side enforcement**: Validate outbound events against the contract before publishing. Reject or quarantine events that violate the contract.

**Consumer-side enforcement**: Validate inbound events against the contract before processing. Log violations and route to dead letter queue.

**Registry-based enforcement**: Store contracts in a schema registry (Confluent Schema Registry, custom). Both producers and consumers validate against the registry.

### Schema Evolution Testing

Test that the pipeline handles schema changes gracefully:

- **Additive changes**: New optional columns should not break existing consumers.
- **Type changes**: Column type changes should be validated for backward compatibility.
- **Removal testing**: Removing a column should be caught by contract tests.
- **Default values**: Test that missing optional columns use correct defaults.

---

## Schema Validation

### Runtime Schema Validation

Schema validation checks that data conforms to expected structure at runtime. This catches issues not detected by static type checking:

- **Drifted schemas**: Upstream changed column types without notification.
- **Corrupted serialization**: Avro/Protobuf deserialization produced unexpected structures.
- **Partial ingestion**: Network issues caused truncated messages.
- **Schema registry mismatches**: Producer and consumer using different schema versions.

### Schema Validation Tools

| Tool | Approach | Integration |
|---|---|---|
| **Great Expectations** | Expectation-based validation | Python, Spark, Airflow |
| **Deequ** | Constraint-based validation | Spark |
| **PySpark schema assertions** | DataFrame schema comparison | Spark jobs |
| **Avro schema resolution** | Schema compatibility checking | Kafka, Avro |
| **Protobuf validation** | Protobuf descriptor validation | gRPC, Kafka |

### Schema Comparison

When deploying pipeline changes, compare schemas before and after:

- **Column diff**: Identify added, removed, or modified columns.
- **Type diff**: Identify type changes (STRING → INTEGER, etc.).
- **Constraint diff**: Identify changes in nullability, ranges, or formats.
- **Compatibility check**: Determine if the change is backward compatible, forward compatible, or breaking.

---

## Regression Testing

### What is Pipeline Regression?

Pipeline regression occurs when a change to the pipeline (code change, dependency upgrade, configuration change, data format change) causes the output to differ from the expected result. Regression tests detect these unintended changes.

### Regression Test Strategies

**Golden dataset testing**: Maintain a reference dataset with known expected outputs. After any pipeline change, run the pipeline on the reference dataset and compare outputs. Any difference indicates a regression.

**Statistical regression testing**: Instead of exact comparison, verify that statistical properties of the output remain within acceptable bounds:
- Feature distributions (mean, standard deviation, percentiles) within 1% of baseline.
- Correlation between features and labels within 0.01 of baseline.
- Model performance metrics (AUC, NDCG) within 0.5% of baseline.

**Deterministic regression testing**: Ensure the pipeline is deterministic—running it twice on the same input produces identical output. Non-deterministic pipelines (e.g., using current time, random sampling without fixed seed) make regression testing unreliable.

### Regression Test Triggers

| Change Type | Regression Test Required | Scope |
|---|---|---|
| Transformation logic change | Full golden dataset test | All affected features |
| Dependency upgrade | Full test | All features |
| Configuration change | Targeted test | Affected features only |
| Data format change | Schema + golden dataset test | Affected data sources |
| Infrastructure change | Integration test | End-to-end pipeline |
| Performance optimization | Equivalence test | Same output, different implementation |

---

## Pipeline Testing in CI/CD

### CI/CD Pipeline Stages

| Stage | Tests | Duration | Blocking |
|---|---|---|---|
| **Lint** | Code style, import sorting | < 1 minute | Yes |
| **Unit test** | Transformation logic | < 5 minutes | Yes |
| **Schema test** | Schema validation | < 2 minutes | Yes |
| **Integration test** | External system interaction | < 15 minutes | Yes |
| **Contract test** | Data contract validation | < 5 minutes | Yes |
| **Regression test** | Golden dataset comparison | < 30 minutes | Yes |
| **Performance test** | Latency and throughput benchmarks | < 20 minutes | Warning only |
| **Security scan** | Dependency vulnerabilities | < 10 minutes | Yes |

### Test Isolation in CI

- **Docker Compose**: Start dependent services (Kafka, Redis, databases) in Docker Compose for integration tests.
- **Testcontainers**: Dynamically start required services as Docker containers.
- **In-memory backends**: Use in-memory implementations (H2 for databases, embedded Kafka) for faster tests.
- **Parallel execution**: Run independent test suites in parallel to reduce CI time.

### Test Data Management in CI

- **Fixtures**: Version-controlled test datasets in the repository.
- **Generators**: Code-based test data generation for edge cases and large-scale scenarios.
- **Mocks**: Use mocks only for external services not available in CI (e.g., third-party APIs, production databases).
- **Data versioning**: Pin test data versions to ensure reproducibility.

### Quality Gates in CI

| Gate | Condition | Action on Failure |
|---|---|---|
| Code coverage | > 80% for transformation logic | Block merge |
| Schema compatibility | All schema changes backward compatible | Block merge |
| Regression test pass | Golden dataset test passes | Block merge |
| Performance regression | < 10% latency increase | Warning, block if > 20% |
| Security scan | No critical vulnerabilities | Block merge |
| Contract validation | All contracts satisfied | Block merge |

### Monitoring CI Pipeline Health

Track CI pipeline metrics to maintain testing effectiveness:

- **Test pass rate**: Percentage of tests passing over time. Declining rates indicate growing technical debt.
- **Test duration**: Track test suite duration to prevent CI bottlenecks. Split slow test suites.
- **Flaky test rate**: Tests that intermittently pass/fail reduce confidence. Track and fix or quarantine flaky tests.
- **Coverage trends**: Track code coverage over time. Declining coverage indicates untested code additions.
- **Regression detection rate**: How many regressions are caught by tests vs. reaching production. Low detection rates indicate test gaps.
