# Integration Testing for Recommendation System Microservices

## Overview

Integration testing validates that multiple services, data stores, and pipelines work together
correctly in a production-like environment. For recommendation systems, this encompasses service
contracts, feature stores, model serving, event pipelines (Kafka), API gateways, and caching
layers. Integration tests catch the failures that unit tests cannot — boundary mismatches,
protocol disagreements, serialization errors, and timing issues between distributed components.

## Integration Testing vs. Unit Testing

| Aspect           | Unit Tests                              | Integration Tests                           |
|------------------|----------------------------------------|---------------------------------------------|
| Scope            | Single function/class                  | Multiple services or components             |
| Speed            | Milliseconds                           | Seconds to minutes                          |
| Dependencies     | Mocked                                 | Real (or test-container) instances          |
| Failure mode     | Logic errors                           | Contract mismatches, timeout, serialization |
| Data             | Synthetic fixtures                     | Realistic production-like data              |
| Environment      | In-process                             | Docker containers or staging cluster        |

## Contract Testing Between Services

### Why Contract Testing Matters

In a microservices architecture, each service evolves independently. A recommendation service
may depend on a user profile service, a catalog service, a feature store, and a model serving
endpoint. Without contract testing, a schema change in any upstream service can break downstream
consumers silently.

### Consumer-Driven Contracts

The consumer (e.g., recommendation API) defines the contract it expects, and the provider
(e.g., user service) validates that it fulfills that contract:

```
Consumer Contract (Recommendation API expects from User Service):
- GET /users/{user_id} returns:
  - user_id: string (UUID)
  - preferences: array of {category: string, weight: float}
  - segment: string (one of: "new", "active", "dormant", "premium")
  - created_at: ISO 8601 timestamp
  - status: string (one of: "active", "suspended", "deleted")
```

### Contract Testing Tools and Patterns

- **Pact**: Record consumer expectations, verify against provider stubs
- **Spring Cloud Contract**: Groovy-based contract definitions for JVM services
- **Custom validators**: Schema-based validators using JSON Schema or Avro schemas

### Contract Evolution Strategy

1. All schema changes must be backward compatible (additive only)
2. Deprecated fields require a deprecation period (minimum 2 release cycles)
3. Breaking changes require versioned endpoints (v1, v2)
4. Contract tests run in CI for both consumer and provider on every PR

## API Integration Tests

### Test Categories

**Happy Path Tests**
- Valid request produces expected response structure
- Pagination works correctly (cursor-based or offset)
- Filtering and sorting parameters are honored
- Authentication tokens are validated and passed through

**Error Handling Tests**
- 400 Bad Request for malformed input
- 401 Unauthorized for missing or expired tokens
- 403 Forbidden for insufficient permissions
- 404 Not Found for unknown user or item
- 429 Too Many Requests when rate limited
- 500 Internal Server Error returns structured error response

**Schema Validation Tests**
- Response JSON matches OpenAPI/AsyncAPI schema definition
- All required fields are present and non-null
- Field types match specification (string, integer, array)
- Enum values are within allowed set

### API Test Data Strategy

Use realistic but anonymized data in integration test environments:
- Generate user profiles using production-like distributions
- Use actual item catalog snapshots (sanitized of PII)
- Replay a subset of production interaction events

## Feature Store Integration

### Offline-to-Online Feature Consistency

A critical integration test verifies that features computed offline (batch pipeline) match
features served online (feature store):

```
Test: Feature Consistency
1. Compute user aggregate features from batch data
2. Look up same features from online feature store
3. Assert feature values match within tolerance
4. Tolerance accounts for time window differences
```

### Feature Store Test Scenarios

| Scenario                   | What to Verify                                    |
|---------------------------|---------------------------------------------------|
| Feature write pipeline     | Kafka events update feature store within SLA       |
| Feature read path          | Feature retrieval latency < 10ms at P99           |
| Feature freshness          | Features are not older than maximum allowed TTL   |
| Feature completeness       | Required features are never null for valid users   |
| Feature versioning         | New feature schema is backward compatible          |
| Feature store failover     | Graceful degradation when primary store is down    |

### Feature Pipeline Integration Tests

1. **End-to-end feature computation**: Raw events in, computed features out
2. **Feature transformation correctness**: Aggregation windows, decay functions, normalization
3. **Feature store synchronization**: Batch features appear in online store
4. **Feature serving latency**: Online feature retrieval meets latency budget

## Model Serving Integration

### Model Loading and Warmup

```
Test: Model Server Startup
1. Start model serving container with production config
2. Verify health endpoint returns ready after warmup
3. Send prediction request with known input
4. Verify prediction output matches offline evaluation
5. Verify prediction latency within SLA (P95 < 50ms)
```

### Model Serving Test Matrix

| Test                        | Input                         | Expected                           |
|-----------------------------|-------------------------------|-------------------------------------|
| Single prediction           | One user, one context         | Ranked list of items                |
| Batch prediction            | Multiple users                | One ranked list per user            |
| Cold-start prediction       | Unknown user ID               | Fallback to popularity-based list   |
| Model version routing       | Request with version header   | Response from specified model       |
| A/B test traffic split      | 10K simulated requests        | Distribution matches configured %   |
| Model hot-reload            | New model artifact deployed   | New predictions within 60s          |
| GPU inference (if applicable)| Request on GPU-enabled node   | Prediction with GPU latency profile |

## Kafka Event Integration

### Event Pipeline Tests

Recommendation systems are event-driven. User actions (views, clicks, purchases) flow through
Kafka topics and must be processed reliably.

**Test: Event Production**
- User action API call produces event to correct Kafka topic
- Event schema matches Avro/Protobuf schema registry definition
- Event contains required headers (correlation ID, timestamp, schema version)

**Test: Event Consumption**
- Consumer reads events from topic and processes within expected latency
- Consumer handles malformed events without crashing (dead letter queue)
- Consumer group rebalancing does not lose events

**Test: Event Ordering**
- Events for the same user are processed in order
- Partitioning strategy ensures same-user events go to same partition
- Out-of-order events are handled gracefully

### Kafka Integration Test Patterns

| Pattern                 | Description                                        |
|------------------------|---------------------------------------------------|
| Embedded Kafka         | In-process Kafka broker for fast tests            |
| Testcontainers         | Docker-based Kafka for realistic testing          |
| Schema validation      | Verify events against registered schemas          |
| Consumer lag monitoring| Ensure processing keeps up with production rates  |
| Dead letter queue      | Verify failed events are routed to DLQ            |

## Test Environment Management

### Environment Tiers

```
Development (local)
├── Docker Compose with all dependencies
├── Seeded with minimal test data
├── Fast feedback (< 2 min full suite)
│
Integration (CI ephemeral)
├── Docker containers per test run
├── Realistic data volumes (10-100 GB)
├── Parallel test execution
│
Staging (persistent)
├── Production-mirror infrastructure
├── Anonymized production data snapshot
├── Full integration suite + contract tests
│
Pre-production
├── Exact production configuration
├── Load tests + chaos tests
├── Final validation before release
```

### Container Orchestration for Tests

Use Docker Compose or Testcontainers to spin up isolated dependencies:

- PostgreSQL with test schema and fixtures
- Redis with pre-loaded feature cache
- Kafka with test topics and consumer groups
- Model serving endpoint with test model artifact
- MinIO/S3 with test training data

### Data Management for Test Environments

1. **Snapshot-based**: Copy production data snapshots (anonymized) to test environments
2. **Generator-based**: Programmatically generate test data with realistic distributions
3. **Replay-based**: Record production traffic and replay in test environment
4. **Hybrid**: Synthetic base data augmented with real production samples

### Environment Cleanup

Each test run should leave the environment in a clean state:
- Database migrations are reverted or run in isolated schemas
- Kafka topics are recreated or messages are consumed and discarded
- Feature store entries are removed or namespaced by test run ID
- Model serving caches are flushed between test suites

## Common Integration Failure Patterns

| Failure Pattern              | Symptom                                   | Prevention                              |
|------------------------------|------------------------------------------|------------------------------------------|
| Schema mismatch              | Deserialization error or wrong field      | Contract tests + schema registry        |
| Timeout cascading            | One slow service blocks entire chain      | Circuit breakers + timeout budgets      |
| Race condition               | Intermittent test failures               | Idempotent operations + retry logic     |
| Data staleness               | Tests pass with cached, stale data        | TTL enforcement + freshness checks      |
| Port conflict                | Tests fail when run in parallel          | Dynamic port allocation                 |
| Shared mutable state         | Tests affect each other                  | Test isolation via namespaces/schemas    |

## Integration Test Automation

### CI Pipeline Configuration

```
PR Pipeline:
  ├── Contract tests (consumer side)           ~ 2 min
  ├── API schema validation tests              ~ 1 min
  └── Feature store consistency tests          ~ 3 min

Merge to Main:
  ├── Full integration suite                   ~ 15 min
  ├── Kafka event pipeline tests               ~ 5 min
  ├── Model serving integration tests          ~ 10 min
  └── Contract tests (provider verification)   ~ 3 min

Nightly:
  ├── Staging environment full suite           ~ 45 min
  ├── Data pipeline end-to-end tests           ~ 30 min
  └── Cross-service performance benchmarks     ~ 20 min
```

### Test Reporting and Debugging

- Aggregate test results across all services in a central dashboard
- Include service logs and traces for failed tests
- Capture network captures (tcpdump) for protocol-level debugging
- Diff feature values between offline computation and online store for mismatches
