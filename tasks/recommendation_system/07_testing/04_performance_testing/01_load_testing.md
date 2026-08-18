# Load Testing for Recommendation APIs

## Overview

Load testing validates that the recommendation system meets performance requirements under
expected, peak, and degraded traffic conditions. This covers latency distribution testing,
throughput measurement, capacity planning, performance regression detection, and test scenario
design for recommendation-specific patterns (personalized endpoints, cold-start, real-time
feature retrieval).

## Why Recommendation APIs Are Hard to Load Test

Recommendation APIs have unique characteristics that distinguish them from typical CRUD services:

- **Computationally heterogeneous**: A request for a known user (cached features) takes 5ms;
  a cold-start user requires feature computation, model inference, and filtering (200ms+)
- **Stateful dependencies**: Each request touches feature stores, model servers, caches,
  and potentially external catalog services
- **Personalization variance**: Different users produce different computational paths
- **Large response payloads**: Recommendation lists with item metadata can be 50-500KB
- **Feedback loops**: User clicks on recommendations generate events that update features,
  which affects subsequent requests

## Load Testing Tools

### Locust (Python)

Locust provides programmatic load test definitions with realistic user behavior modeling:

- Custom user classes model different user segments (power users, new users, anonymous)
- Event hooks enable recording and analyzing response patterns
- Distributed mode supports thousands of concurrent users across multiple machines
- Web UI provides real-time latency and throughput visualization

### k6 (JavaScript)

k6 offers a scripting approach with strong performance characteristics:

- VU (Virtual User) scripts run in Go-based runtime for efficiency
- Threshold-based assertions automate pass/fail decisions
- Built-in metrics for TCP, TLS, HTTP, and WebSocket connections
- Output to InfluxDB/Prometheus for dashboarding

### Tool Comparison

| Feature             | Locust                           | k6                                 |
|---------------------|----------------------------------|------------------------------------|
| Language            | Python                           | JavaScript                         |
| Performance         | ~1K VUs per node                 | ~30K VUs per node                  |
| Realism             | High (programmatic behaviors)    | Medium (scripted scenarios)        |
| Extensibility       | Plugin ecosystem                 | Extensions + custom output         |
| Cloud execution     | Locust Cloud                     | Grafana Cloud k6                   |
| Best for            | Complex user flows               | High-volume protocol testing       |

## Load Test Design Principles

### Realistic User Behavior Modeling

Load tests must simulate real user patterns, not uniform request distribution:

**User Segment Distribution**:
- 40% anonymous users (cold-start path, no personalization)
- 35% casual users (limited history, content-based recommendations)
- 20% active users (rich history, collaborative filtering path)
- 5% power users (extensive history, complex feature computation)

**Request Pattern Distribution**:
- 60% homepage recommendation requests (cached, fast path)
- 20% category/explore recommendations (semi-personalized)
- 10% search-based recommendations (query-dependent)
- 10% email/notification recommendation requests (batch, async)

**Temporal Patterns**:
- Ramp-up period simulating morning traffic increase
- Peak traffic simulation (evening browsing hours)
- Sustained load over extended duration
- Ramp-down with graceful connection draining

### Request Payload Realism

Each load test request should include realistic parameters:

```
GET /api/v1/recommendations?user_id={segment_user}
  &context={"device": "mobile", "session_id": "test_session"}
  &count=10
  &strategy="personalized"
  &exclude_items={recently_viewed}
```

## Test Scenario Design

### Scenario 1: Steady-State Baseline

**Purpose**: Establish performance baseline under normal traffic conditions

| Parameter            | Value                              |
|----------------------|------------------------------------|
| Duration             | 30 minutes                         |
| Concurrent users     | 500 (ramp from 0 over 5 minutes)   |
| Request rate         | 200 requests/second                |
| Think time           | 2-5 seconds between requests       |
| Success threshold    | P95 < 100ms, P99 < 250ms          |
| Error rate threshold | < 0.1%                            |

### Scenario 2: Peak Traffic

**Purpose**: Validate behavior under expected peak load

| Parameter            | Value                              |
|----------------------|------------------------------------|
| Duration             | 15 minutes                         |
| Concurrent users     | 2000                               |
| Request rate         | 1000 requests/second               |
| Think time           | 1-3 seconds between requests       |
| Success threshold    | P95 < 200ms, P99 < 500ms          |
| Error rate threshold | < 0.5%                            |

### Scenario 3: Spike Test

**Purpose**: System behavior under sudden traffic surge

| Phase               | Duration   | Users   | Request Rate |
|---------------------|-----------|---------|--------------|
| Baseline            | 5 min     | 200     | 100 req/s    |
| Spike               | 1 min     | 5000    | 3000 req/s   |
| Sustain             | 5 min     | 5000    | 3000 req/s   |
| Recovery            | 5 min     | 200     | 100 req/s    |

Key assertions:
- Auto-scaling activates within 2 minutes of spike
- Error rate during spike < 2%
- Full recovery to baseline latency within 3 minutes of spike end
- No cascading failures to dependent services

### Scenario 4: Sustained Load (Soak Test)

**Purpose**: Detect memory leaks, connection pool exhaustion, cache degradation

| Parameter            | Value                              |
|----------------------|------------------------------------|
| Duration             | 4 hours                            |
| Concurrent users     | 1000                               |
| Request rate         | 500 requests/second                |
| Success threshold    | Latency does not degrade > 10% over duration |
| Memory threshold     | No monotonic memory increase        |

### Scenario 5: Cold-Start Stress

**Purpose**: Test performance when cache is cold (e.g., after deployment)

| Phase               | Description                                  |
|---------------------|----------------------------------------------|
| Flush all caches    | Clear Redis, CDN, in-memory caches           |
| Load test           | 500 users, 200 req/s for 10 minutes         |
| Assertion           | P99 < 1000ms even during cold-start          |
| Recovery            | Verify cache warming reduces latency over time |

## Latency Distribution Testing

### Percentile Targets

Recommendation APIs require latency measured at multiple percentiles:

| Percentile | Target   | Rationale                                        |
|------------|----------|--------------------------------------------------|
| P50        | < 30ms   | Median user experience                           |
| P75        | < 60ms   | Most users should not notice delay               |
| P90        | < 100ms  | Acceptable for majority of traffic               |
| P95        | < 150ms  | Tail latency budget for active users             |
| P99        | < 300ms  | Worst-case acceptable experience                 |
| P99.9      | < 1000ms | outliers should not timeout                      |

### Latency Breakdown Analysis

Load test results should decompose latency into components:

```
Total Request Latency = API Gateway + Auth + Feature Retrieval
                      + Model Inference + Post-processing + Serialization
                      + Network Transfer

Typical breakdown:
  API Gateway + Auth:        5ms   (10%)
  Feature Retrieval:        10ms   (20%)
  Model Inference:          25ms   (50%)
  Post-processing + Filter:  5ms   (10%)
  Serialization + Network:   5ms   (10%)
  Total:                    50ms
```

## Throughput Testing

### Maximum Throughput Determination

Gradually increase request rate until error rate exceeds threshold:

1. Start at 100 req/s
2. Increase by 100 req/s every 2 minutes
3. Monitor latency percentiles and error rate
4. Stop when P99 exceeds 500ms or error rate exceeds 1%
5. Record maximum sustainable throughput

### Throughput Benchmarks

| Component              | Expected Throughput              |
|------------------------|----------------------------------|
| Recommendation API     | 5,000 req/s per replica          |
| Feature store (Redis)  | 50,000 reads/sec per node        |
| Model serving (GPU)    | 1,000 inferences/sec per GPU     |
| Model serving (CPU)    | 200 inferences/sec per core      |
| Kafka event ingestion  | 100,000 events/sec per topic     |

## Capacity Planning Through Load Testing

### Scaling Thresholds

Use load test results to define auto-scaling triggers:

| Metric                 | Scale-Up Threshold | Scale-Down Threshold |
|------------------------|-------------------|----------------------|
| CPU utilization        | > 70% for 3 min   | < 30% for 10 min     |
| Request queue depth    | > 100 requests    | < 10 requests        |
| P95 latency            | > 200ms for 2 min | < 50ms for 10 min    |
| Memory utilization     | > 80%             | < 40%                |
| Model inference queue  | > 50 pending      | < 5 pending          |

### Capacity Model

```
Required Replicas = ceil(Peak Request Rate / Per-Replica Throughput)
                   * (1 + Headroom Factor)

Where Headroom Factor = 0.3 (30% buffer for unexpected spikes)

Example:
  Peak Rate: 5,000 req/s
  Per-Replica Throughput: 5,000 req/s
  Headroom: 30%
  Required Replicas: ceil(5000 / 5000) * 1.3 = 2 replicas
```

## Performance Regression Testing

### Baseline Comparison

Every load test run should compare against a stored baseline:

1. Run load test with standard configuration
2. Compare latency percentiles against baseline
3. Flag regression if P95 increases by > 10% or error rate increases by > 0.1%
4. Block deployment if regression detected

### CI Integration for Performance Tests

```
Nightly Performance Gate:
  ├── Run Scenario 1 (baseline): ~ 35 min
  ├── Compare against stored baseline
  ├── Update baseline if improved
  ├── Alert team if regressed
  └── Store results in time-series database

Pre-Release Performance Gate:
  ├── Run Scenarios 1-4: ~ 3 hours
  ├── All scenarios must pass thresholds
  ├── Generate performance report
  └── Require manual approval to proceed
```

## Load Test Anti-Patterns

1. **Testing against production**: Load tests should run against staging, not production
2. **Uniform request distribution**: Real users exhibit skewed, bursty behavior
3. **Ignoring think time**: Removing think time inflates concurrency unrealistically
4. **Testing cached paths only**: Cold-start and cache-miss paths are where failures occur
5. **Single-duration tests**: Short tests miss memory leaks and connection degradation
6. **Ignoring dependent services**: Load test the full dependency chain, not just the API
