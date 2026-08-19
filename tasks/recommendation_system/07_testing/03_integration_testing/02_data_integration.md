# Data Integration Testing

## 1. Overview

Data integration testing validates that the entire data flow—from raw event ingestion
through processing, storage, and serving—works correctly as a unified system. Unlike unit
tests that verify individual components, data integration tests verify that components
correctly communicate, transform data end-to-end, and maintain consistency across system
boundaries. For recommendation systems, data integration failures are among the most
damaging because they can silently corrupt features, skip events, or introduce delays that
degrade recommendation quality without obvious error signals.

### 1.1 Integration Test Scope

```
User Event → Ingestion → Stream Processing → Batch Processing → Feature Store → Serving
     ↓           ↓              ↓                  ↓                ↓            ↓
  Clickstream   Kafka      Flink streaming    Spark batch      Redis/Hive    API Gateway
  User DB       CDC        Real-time features  Daily features   Online/offline
  Item catalog  REST       Session updates     User profiles    Pre-computed
```

### 1.2 Integration Test Categories

| Category | Scope | Data Volume | Execution Time | Frequency |
|---|---|---|---|---|
| Pipeline E2E | Full data flow | 1-10 GB | 1-4 hours | Nightly |
| Stream processing | Kafka → Flink → Store | 100 MB - 1 GB | 15-30 minutes | Nightly |
| Batch processing | Spark job → Storage | 10-100 GB | 1-2 hours | Nightly |
| Feature materialization | Computation → Feature Store | 1-10 GB | 30-60 minutes | Nightly |
| Data quality gates | Quality checks across pipeline | Same as source | Included above | Per pipeline |

---

## 2. End-to-End Pipeline Tests

### 2.1 Full Pipeline Validation

End-to-end pipeline tests verify that a recommendation request triggers the complete
data flow and produces correct results.

**Test flow:**

```
Step 1: Generate test user events (clicks, purchases, views)
Step 2: Verify events ingested into Kafka (check topic partition counts)
Step 3: Verify streaming processor consumed events (check processing lag)
Step 4: Verify features computed and stored in feature store
Step 5: Verify batch pipeline incorporates events in next run
Step 6: Verify model serving uses updated features
Step 7: Verify recommendation output reflects test events
Step 8: Verify no data loss or duplication across pipeline
```

### 2.2 Pipeline Completeness Tests

Ensure no events are lost or duplicated:

| Test | Method | Acceptance Criteria |
|---|---|---|
| Event counting | Count events at source vs sink | 100% delivery (±0.1%) |
| Deduplication | Track event IDs across pipeline | 0 duplicates |
| Ordering | Verify ordering guarantees within partitions | Per-partition ordering preserved |
| At-least-once | Simulate consumer restart mid-processing | No data loss, acceptable duplicates |
| Exactly-once | Verify idempotent processing | No duplicates, no data loss |

### 2.3 Pipeline Correctness Tests

Verify data transformations maintain correctness:

- **Aggregation accuracy**: Sum, count, average match expected values across pipeline
- **Join correctness**: Cross-source joins produce expected records
- **Filter correctness**: Filtered events are excluded, included events are correct
- **Enrichment correctness**: Joined data from external sources is accurate
- **Temporal correctness**: Events assigned to correct time windows

### 2.4 Pipeline Latency Tests

Measure end-to-end latency for each pipeline stage:

| Stage | SLA | Measurement |
|---|---|---|
| Event ingestion to Kafka | < 100ms | Producer send time |
| Kafka to Flink processing | < 500ms | Consumer lag |
| Feature computation to store | < 2 seconds | Write latency |
| Feature store to serving | < 10ms | Read latency |
| Total event to serving | < 5 seconds | End-to-end measurement |

### 2.5 Pipeline Failure Recovery Tests

| Scenario | Test Method | Expected Behavior |
|---|---|---|
| Kafka broker failure | Kill broker mid-pipeline | Pipeline recovers, no data loss |
| Flink job crash | Kill job manager | Checkpoint restore, processing resumes |
| Feature store outage | Block feature store writes | Events buffered, replayed on recovery |
| Network partition | Block inter-service traffic | Graceful degradation, eventual consistency |
| Schema change | Modify upstream schema | Pipeline handles with compatibility |

---

## 3. Data Flow Validation

### 3.1 Source-to-Sink Data Lineage

Track and validate data flow from every source to every sink:

```
Source: Clickstream Kafka Topic (user_events)
├── Sink 1: Flink → Real-time features (user_realtime_features)
├── Sink 2: Spark → Daily aggregates (user_daily_features)
├── Sink 3: Spark → Training dataset (training_interactions)
└── Sink 4: Elasticsearch → Search index (user_event_index)

Source: User Profile Database (users)
├── Sink 1: CDC → Feature Store (user_profile_features)
├── Sink 2: Spark → User embeddings (user_embeddings)
└── Sink 3: API → Serving cache (user_profile_cache)

Source: Item Catalog (items)
├── Sink 1: CDC → Feature Store (item_features)
├── Sink 2: Spark → Item embeddings (item_embeddings)
└── Sink 3: API → Search index (item_search_index)
```

### 3.2 Data Transformation Validation

For each source-to-sink path, validate:

- **Record count preservation**: Input records = Output records (accounting for joins)
- **Field mapping correctness**: Source fields map to correct destination fields
- **Type conversion accuracy**: Data types convert without loss
- **Null handling consistency**: Nulls handled per specification
- **Default value application**: Missing values filled with correct defaults

### 3.3 Cross-Source Consistency

Verify that data from different sources is consistent:

- **User ID consistency**: Same user ID format across all systems
- **Timestamp consistency**: All timestamps in consistent timezone (UTC)
- **Category consistency**: Item categories consistent between catalog and features
- **Interaction consistency**: Event counts match between streaming and batch views

### 3.4 Data Flow Monitoring

Implement continuous data flow monitoring:

- **Throughput metrics**: Events processed per second at each stage
- **Latency metrics**: Time spent at each pipeline stage
- **Error metrics**: Failed records, retry counts, dead letter queue size
- **Freshness metrics**: Age of newest record at each sink

---

## 4. Kafka Event Processing Tests

### 4.1 Producer Tests

| Test Scenario | Method | Expected Behavior |
|---|---|---|
| Normal publishing | Send 10,000 events | All events published, acknowledged |
| Schema validation | Send event violating schema | Producer rejects event |
| Partition key consistency | Events with same key | All go to same partition |
| Serialization | Events with complex nested structures | Correctly serialized/deserialized |
| Backpressure | Producer exceeds broker capacity | Producer slows down, no data loss |

### 4.2 Consumer Tests

| Test Scenario | Method | Expected Behavior |
|---|---|---|
| Normal consumption | Consume from empty topic | All events consumed in order |
| Consumer group rebalance | Kill consumer mid-processing | Partition reassigned, no data loss |
| Offset management | Process events, commit offsets | Restart resumes from committed offset |
| Dead letter queue | Send malformed event | Event routed to DLQ, processing continues |
| Backpressure handling | Consumer slower than producer | Consumer catches up during low-traffic periods |

### 4.3 Topic Configuration Tests

| Configuration | Test Method | Expected Behavior |
|---|---|---|
| Replication factor | Kill broker | Data available on remaining replicas |
| Partition count | Check parallel consumption | Consumers scale with partitions |
| Retention policy | Send old events | Old events deleted per retention policy |
| Compaction | Send key updates | Only latest value per key retained |

### 4.4 Stream Processing Tests

**Flink job integration tests:**

- **Event-time windowing**: Events within window produce correct aggregation
- **Watermark handling**: Late events handled per policy (drop, update, late buffer)
- **State management**: Checkpoint/restore preserves processing state
- **Side output**: Late/malformed events routed to side outputs correctly
- **Output consistency**: Multiple runs on same input produce identical output

---

## 5. Feature Store Materialization Tests

### 5.1 Batch Materialization Tests

Test scheduled batch jobs that populate the feature store:

| Test | Input | Expected Behavior |
|---|---|---|
| Full materialization | Complete daily data | All entities updated with new features |
| Incremental materialization | Delta since last run | Only changed entities updated |
| Backfill materialization | Historical data | Features recomputed for date range |
| Partition materialization | Specific date partition | Features for that date correct |
| Materialization SLA | Pipeline execution | Completes within time budget |

### 5.2 Online Feature Materialization

Test real-time feature updates:

| Test | Method | Expected Behavior |
|---|---|---|
| Streaming update | Inject real-time event | Feature updated within 5 seconds |
| Concurrent updates | Multiple events for same entity | Latest event wins |
| Feature group update | Event triggering multiple features | All features in group update atomically |
| Update propagation | Write feature, read immediately | New value returned |

### 5.3 Feature Store Consistency Tests

- **Read-after-write consistency**: Written features immediately readable
- **Cross-replica consistency**: All replicas eventually consistent
- **Batch-online consistency**: Batch and online views agree on feature values
- **Version consistency**: Feature versions correctly managed

### 5.4 Feature Store Performance Tests

| Metric | Target | Measurement |
|---|---|---|
| Write latency (single entity) | < 5ms | p99 latency |
| Write latency (batch) | < 10s for 10K entities | Batch write throughput |
| Read latency (single entity) | < 2ms | p99 latency |
| Read latency (batch) | < 10ms for 100 entities | Batch read throughput |
| Storage capacity | Linear with entity count | Monitoring |
| Memory usage | < 80% of allocated | Monitoring |

---

## 6. Data Quality Gate Tests

### 6.1 Quality Gate Architecture

```
Pipeline Stage → Quality Gate → Decision
                    ↓                ↓
             ┌──────┼──────┐   ┌────┴────┐
             ↓      ↓      ↓   ↓         ↓
         Schema  Completeness  Pass    Fail
         Check   Check         ↓         ↓
             ↓      ↓        Continue   Block + Alert
             ↓      ↓                    ↓
         Validation  Distribution      Rollback
         Results     Check             or Fix
```

### 6.2 Gate Criteria

Each data quality gate has specific pass/fail criteria:

| Gate | Criteria | Failure Action |
|---|---|---|
| Schema gate | Output matches registered schema | Block downstream, alert data team |
| Completeness gate | > 99.9% required fields non-null | Block downstream, alert data team |
| Freshness gate | Data age < SLA threshold | Alert, allow with stale data flag |
| Volume gate | Record count within 20% of expected | Warning, investigate |
| Distribution gate | PSI < 0.25 for all features | Alert, investigate |
| Uniqueness gate | 0 duplicate primary keys | Block downstream, dedup and retry |

### 6.3 Gate Testing Methodology

Test that quality gates correctly:

- **Block bad data**: Introduce known defects, verify gates catch them
- **Allow good data**: Pass clean data through gates, verify no false positives
- **Report accurately**: Gate metrics match actual data quality
- **Recover from failures**: Gate service restart doesn't lose state
- **Scale with volume**: Gates process data within SLA even at peak volume

### 6.4 Quality Gate Metrics

Track gate effectiveness:

- **False positive rate**: Good data incorrectly rejected (target: < 1%)
- **False negative rate**: Bad data incorrectly accepted (target: < 0.1%)
- **Gate processing time**: Time to evaluate data quality (target: < 10% of pipeline time)
- **Gate availability**: Uptime of quality gate infrastructure (target: 99.99%)
- **Defect escape rate**: Quality issues reaching production (target: < 0.5%)

---

## 7. Test Infrastructure

### 7.1 Integration Test Environment

- **Docker Compose**: Local development with all dependencies
- **Kubernetes (minikube/kind)**: Production-like environment for thorough testing
- **TestContainers**: Dynamic container management for CI pipelines
- **Cloud staging environments**: Full infrastructure mirror for pre-production

### 7.2 Test Data Management

- **Golden datasets**: Curated test data with known correct outputs
- **Data generators**: Synthetic data for specific test scenarios
- **Production snapshots**: Anonymized production data for realistic testing
- **Data versioning**: Versioned test datasets for reproducible results

### 7.3 Test Execution and Reporting

- **CI pipeline integration**: Integration tests run on merge to main
- **Parallel execution**: Independent test suites run in parallel
- **Flaky test management**: Quarantine and track intermittent failures
- **Result reporting**: Automated reports with trend analysis and failure categorization
