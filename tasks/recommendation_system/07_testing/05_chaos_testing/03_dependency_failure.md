# Dependency Failure Testing

## 1. Overview

Recommendation systems depend on numerous external services, databases, caches, and
message queues. Each dependency is a potential point of failure. Dependency failure testing
systematically simulates failures in each dependency to validate that the recommendation
system degrades gracefully rather than failing catastrophically. This document covers
failure simulation for feature stores, model serving, Kafka, databases, caches, and
cascading failure prevention.

### 1.1 Dependency Map

```
Recommendation Service
├── Feature Store (Redis/Hive) ← Critical dependency
├── Model Serving (GPU cluster) ← Critical dependency
├── User Profile DB (PostgreSQL) ← Critical dependency
├── Item Catalog (Elasticsearch) ← Important dependency
├── Kafka (Event streaming) ← Important dependency
├── Cache Layer (Redis/Memcached) ← Performance dependency
├── Experiment Service ← Operational dependency
├── Monitoring Service ← Observability dependency
└── Auth Service ← Security dependency
```

### 1.2 Failure Impact Classification

| Dependency | Failure Impact | Degradation Strategy | RTO |
|---|---|---|---|
| Feature store | High | Use cached features + defaults | < 10s |
| Model serving | Critical | Serve popularity-based recs | < 30s |
| User profile DB | High | Use cached profiles | < 10s |
| Kafka | Medium | Buffer events locally | < 5min |
| Cache layer | Low | Compute in real-time | < 5s |
| Item catalog | Medium | Use cached catalog | < 30s |
| Auth service | Critical | Reject unauthenticated requests | N/A |

---

## 2. Feature Store Failure Simulation

### 2.1 Failure Scenarios

| Scenario | Method | Expected Behavior |
|---|---|---|
| Complete outage | Block all connections | Serve cached/default features |
| Slow responses (>1s) | Inject latency | Timeout → fallback within 100ms |
| Partial failure | Block 50% of requests | Use available replicas |
| Memory pressure | Increase Redis memory usage | Evict least-recently-used, serve available |
| Network timeout | Drop packets to feature store | Timeout fallback within 100ms |
| Data corruption | Return random data | Detect corruption, use defaults |

### 2.2 Feature Store Fallback Strategy

```
Feature Store Request
    ↓
┌───┴───┐
│ Try   │ → Feature Store (primary)
│ First │
└───┬───┘
    ↓ (failure detected)
┌───┴───┐
│ Try   │ → Feature Store (replica)
│ Second│
└───┬───┘
    ↓ (failure detected)
┌───┴───┐
│ Try   │ → Local cache (Redis local)
│ Cache │
└───┬───┘
    ↓ (cache miss)
┌───┴───┐
│ Use   │ → Default feature values (based on user segment)
│ Default│
└───────┘
```

### 2.3 Feature Quality During Failure

| Feature Category | Fallback Quality | Impact on Recommendations |
|---|---|---|
| User behavioral features | Stale (cache TTL) | Moderate degradation |
| User profile features | Default values | Significant degradation |
| Item features | Stale (less frequently updated) | Minor degradation |
| Context features | Computed locally | No degradation |
| Real-time features | Not available | Significant degradation |

### 2.4 Recovery Validation

After feature store recovers:

- Feature serving resumes within 10 seconds
- Feature freshness catches up within 2 minutes
- No stale features served after recovery
- Monitoring confirms feature store health

---

## 3. Model Serving Failure Simulation

### 3.1 Failure Scenarios

| Scenario | Method | Expected Behavior |
|---|---|---|
| Complete model serving outage | Kill model serving instances | Serve popularity-based recs |
| Single model failure | Corrupt one model version | Route to healthy model version |
| GPU failure | Simulate GPU error | Fall back to CPU inference |
| Model loading failure | Corrupt model artifact | Keep previous model loaded |
| Inference timeout | Inject 5s latency per inference | Timeout → cached recommendations |
| OOM during inference | Feed oversized input | Reject request, serve fallback |

### 3.2 Model Serving Fallback Cascade

```
Primary Model Serving
    ↓ (failure)
┌───┴──────────────────┐
│ Fallback Level 1     │ → Cached recommendations (last valid)
│ (cached results)     │   Valid for: 5 minutes
└───┬──────────────────┘
    ↓ (expired or unavailable)
┌───┴──────────────────┐
│ Fallback Level 2     │ → Pre-computed popular recommendations
│ (popularity-based)   │   Updated: daily
└───┬──────────────────┘
    ↓ (unavailable)
┌───┴──────────────────┐
│ Fallback Level 3     │ → Static curated recommendations
│ (static fallback)    │   Updated: weekly
└──────────────────────┘
```

### 3.3 Model Version Failure

When a new model version causes errors:

- **Detection**: Error rate spike on new version traffic
- **Automatic rollback**: Route traffic back to previous version
- **Manual investigation**: Analyze failure cause
- **Re-deployment**: Fix issue and re-deploy

---

## 4. Kafka Lag Simulation

### 4.1 Consumer Lag Scenarios

| Scenario | Lag Level | Impact | Mitigation |
|---|---|---|---|
| Normal | < 1000 messages | No impact | Normal processing |
| Moderate lag | 1K - 100K messages | Feature freshness degraded | Prioritize critical topics |
| High lag | 100K - 1M messages | Significant staleness | Scale consumers, alert team |
| Extreme lag | > 1M messages | Feature values very stale | Switch to batch features |

### 4.2 Kafka Broker Failure

| Scenario | Expected Behavior |
|---|---|
| Single broker down | Replicas serve from remaining brokers |
| Multiple brokers down | Topic availability degraded, reduce write throughput |
| Leader election | Brief pause, then resume with new leader |
| Full cluster down | Local event buffering, batch replay on recovery |

### 4.3 Event Processing During Lag

When Kafka lag increases:

- **Feature freshness monitoring**: Alert when lag exceeds SLA
- **Consumer scaling**: Auto-scale consumers to reduce lag
- **Priority processing**: Process critical events first
- **Batch fallback**: Serve batch-computed features instead of real-time
- **Lag recovery**: Measure time for lag to return to normal after fix

### 4.4 Kafka Recovery Testing

After Kafka recovery:

- Consumer lag returns to zero within SLA
- No duplicate event processing
- No lost events
- Feature freshness recovers within expected time
- Event ordering preserved within partitions

---

## 5. Database Failure Simulation

### 5.1 Primary Database Failure

| Scenario | Method | Expected Behavior |
|---|---|---|
| Primary down | Kill primary instance | Promote replica to primary |
| Primary slow | Inject 2s query latency | Read from replicas, queue writes |
| Connection pool exhaustion | Maximize connections | Queue requests, reject excess |
| Disk failure | Simulate disk errors | Failover to replica with data |
| Replication lag | Delay replication | Read from primary for recent data |

### 5.2 Read Replica Failure

| Scenario | Expected Behavior |
|---|---|
| Single replica down | Route reads to remaining replicas |
| All replicas down | Read from primary (with load impact) |
| Replica with stale data | Detect staleness, read from primary |

### 5.3 Database Recovery Validation

After database recovery:

- All queued writes successfully committed
- Read consistency restored
- Replication lag returns to zero
- Connection pool health restored
- No data corruption detected

---

## 6. Cache Failure Simulation

### 6.1 Cache Failure Scenarios

| Scenario | Method | Expected Behavior |
|---|---|---|
| Cache complete outage | Stop cache service | Compute in real-time |
| Cache eviction storm | Maximize eviction rate | Serve stale + compute miss |
| Cache poisoning | Inject incorrect data | Detect corruption, invalidate |
| Cache network partition | Block cache network | Timeout → direct computation |
| Cache memory full | Fill cache to capacity | Eviction, graceful degradation |

### 6.2 Cache Failure Impact

| Metric | With Cache | Without Cache | Recovery |
|---|---|---|---|
| Latency | 5ms p99 | 50ms p99 | Returns to 5ms |
| Throughput | 100K QPS | 20K QPS | Returns to 100K |
| Error rate | 0.01% | 0.01% | No change |
| Database load | 10K QPS | 100K QPS | Returns to 10K |

### 6.3 Cache Warming After Recovery

After cache failure recovery:

1. **Gradual warming**: Don't thunder-herd the cache on recovery
2. **Priority warming**: Warm most-requested items first
3. **Background warming**: Warm cache while serving from database
4. **Verification**: Confirm cache hit rate returns to normal within 30 minutes

---

## 7. Cascading Failure Prevention

### 7.1 Cascading Failure Patterns

```
Pattern 1: Retry Storm
Service A fails → Service B retries → Service B overloaded → Service C retries → All fail

Pattern 2: Timeout Cascade
Service A slow → Service B waits → Service B slow → Service C waits → All slow

Pattern 3: Resource Exhaustion
Service A fails → Retries consume connections → Service B can't get connections → All fail

Pattern 4: Memory Cascade
Service A fails → Fallback allocates memory → Service B memory pressure → OOM → All fail
```

### 7.2 Prevention Mechanisms

| Mechanism | Description | Implementation |
|---|---|---|
| Circuit breakers | Stop calling failing services | Hystrix, Resilience4j, custom |
| Rate limiters | Limit retry rate | Token bucket, sliding window |
| Timeouts | Set aggressive timeouts | Per-dependency timeout configuration |
| Bulkheads | Isolate failure domains | Separate thread pools per dependency |
| Backoff | Exponential backoff on retries | Jittered exponential backoff |
| Dead letter queues | Queue failed operations | Kafka DLQ, SQS dead letter |

### 7.3 Circuit Breaker Testing

| State | Test Method | Expected Behavior |
|---|---|---|
| Closed (normal) | Normal traffic | All requests pass through |
| Open (tripping) | Dependency failure detected | All requests use fallback |
| Half-open (recovery) | Dependency recovering | Limited requests test recovery |
| Repeated trips | Intermittent failures | Circuit stabilizes in open state |

### 7.4 Chaos Experiments for Cascading Failures

| Experiment | Target | Expected Result |
|---|---|---|
| Dependency failure cascade | Kill feature store | Circuit breaker trips, fallback active |
| Retry storm prevention | Inject 500ms latency | Backoff prevents overload |
| Timeout cascade prevention | Kill model serving | Timeout + fallback, no cascade |
| Resource isolation | Fill one connection pool | Other pools unaffected |

---

## 8. Dependency Failure Test Framework

### 8.1 Fault Injection Tools

| Tool | Type | Use Case |
|---|---|---|
| Chaos Monkey | Process kill | Random instance termination |
| Toxiproxy | Network fault | Latency injection, connection drops |
| Litmus Chaos | Kubernetes | Pod deletion, network partitions |
| Gremlin | Platform | Comprehensive fault injection |
| custom scripts | Targeted | Dependency-specific failures |

### 8.2 Test Execution Protocol

1. **Pre-test baseline**: Record system metrics under normal conditions
2. **Inject fault**: Apply specific failure to target dependency
3. **Observe degradation**: Monitor system behavior during failure
4. **Validate fallback**: Ensure fallback strategy activates correctly
5. **Remove fault**: Restore dependency to normal operation
6. **Validate recovery**: Confirm system returns to normal operation
7. **Post-test analysis**: Compare pre/post metrics, document findings

### 8.3 Dependency Failure Test Results Template

| Metric | Baseline | During Failure | After Recovery |
|---|---|---|---|
| Request success rate | 99.99% | 99.5% (fallback) | 99.99% |
| P99 latency | 80ms | 150ms (degraded) | 80ms |
| Feature freshness | 2s | 300s (stale) | 5s |
| Recommendation quality | 85% relevant | 60% relevant | 85% relevant |
| Recovery time | N/A | N/A | 45 seconds |
