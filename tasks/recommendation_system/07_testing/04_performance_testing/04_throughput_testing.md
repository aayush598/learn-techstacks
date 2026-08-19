# Throughput Testing

## 1. Overview

Throughput testing measures the maximum rate at which the recommendation system can
serve valid recommendations while maintaining acceptable latency and accuracy. For
production recommendation systems, throughput directly impacts revenue—every request
that cannot be served due to capacity limits is a lost recommendation opportunity.
This document covers QPS measurement, concurrent user simulation, sustained load
testing, ramp-up testing, and throughput vs latency tradeoff analysis.

### 1.1 Throughput Requirements

| System Component | Target QPS | Peak QPS | Burst QPS |
|---|---|---|---|
| Recommendation API | 50,000 | 100,000 | 200,000 |
| Feature store reads | 200,000 | 400,000 | 600,000 |
| Model inference | 10,000 | 20,000 | 40,000 |
| Event ingestion | 500,000 | 1,000,000 | 2,000,000 |
| Cache operations | 500,000 | 1,000,000 | 2,000,000 |

### 1.2 Throughput Measurement Principles

- **Measure valid throughput**: Only count requests that return correct results
- **Separate throughput from latency**: High throughput with high latency is not success
- **Account for error rate**: Throughput includes only successful requests
- **Measure at multiple levels**: Service level, component level, infrastructure level

---

## 2. QPS Measurement

### 2.1 Request Per Second (QPS) Definition

QPS counts the number of complete, valid requests processed per second.

```
Valid QPS = Total Requests Processed / Time Period
Where "valid" = 200 response, correct data, within latency SLA
```

### 2.2 QPS Measurement Methodology

**Step 1: Define measurement window**

| Window Type | Duration | Use Case |
|---|---|---|
| Instantaneous | 1 second | Real-time monitoring |
| Short-term | 5 seconds | Dashboard display |
| Medium-term | 1 minute | Trend analysis |
| Long-term | 1 hour | Capacity planning |

**Step 2: Classify request types**

Recommendation systems serve different request types with different QPS profiles:

| Request Type | % of Traffic | Avg Latency | QPS Contribution |
|---|---|---|---|
| Home page recommendations | 40% | 50ms | 20,000 |
| Related items | 25% | 30ms | 12,500 |
| Search suggestions | 20% | 40ms | 10,000 |
| Category browsing | 10% | 60ms | 5,000 |
| Batch requests | 5% | 200ms | 2,500 |

**Step 3: Measure component QPS**

Track QPS at each system component to identify bottlenecks:

```
Client → [50K QPS] → API Gateway → [50K QPS] → Recommendation Service
                                                    ↓ [50K QPS]
                                              Feature Store → [200K QPS] (4 features per request)
                                                    ↓ [50K QPS]
                                              Model Serving → [50K QPS]
```

### 2.3 QPS Bottleneck Analysis

When QPS plateaus, identify the bottleneck:

| Bottleneck | Symptom | Diagnostic |
|---|---|---|
| CPU bound | CPU at 100%, latency stable | Profile CPU-intensive operations |
| Memory bound | GC frequency increases, OOM risk | Check memory allocation patterns |
| Network bound | Network saturation, packet loss | Check bandwidth utilization |
| I/O bound | Disk I/O wait, database slow | Check disk and DB metrics |
| Connection bound | Connection pool exhaustion | Check pool sizes and wait times |
| Thread bound | Thread pool saturation | Check thread pool configuration |

---

## 3. Concurrent User Simulation

### 3.1 User Behavior Modeling

Realistic user simulation requires modeling actual user behavior patterns:

**User session model:**

```
Session Duration: Exponential(μ=300 seconds)
Requests per Session: Poisson(λ=5)
Think Time between Requests: Exponential(μ=30 seconds)
Request Type Distribution: Weighted by production proportions
Device Distribution: Mobile 65%, Desktop 30%, Tablet 5%
Geographic Distribution: US 40%, EU 30%, APAC 20%, Other 10%
```

### 3.2 Concurrent User Levels

| Level | Concurrent Users | QPS Equivalent | Scenario |
|---|---|---|---|
| Normal | 100,000 | 50,000 | Typical weekday |
| Peak | 250,000 | 100,000 | Evening prime time |
| Event | 500,000 | 200,000 | Special event / viral content |
| Extreme | 1,000,000 | 400,000 | Black Friday / flash sale |

### 3.3 Session-Level Simulation

Simulate realistic user sessions rather than isolated requests:

**Session characteristics:**

- **Sequential requests**: User sees recommendations, clicks, sees updated recommendations
- **Stateful interaction**: Each request depends on previous request's response
- **Varying patterns**: Some users browse extensively, others check once
- **Concurrent sessions**: Many users active simultaneously
- **Session persistence**: Same user returns within and across days

### 3.4 User Behavior Scenarios

| Scenario | Description | Request Pattern |
|---|---|---|
| Casual browser | Opens app, views recs, closes | 1-2 requests per session |
| Active shopper | Multiple searches, views, purchases | 10-20 requests per session |
| Content consumer | Reads articles, views related items | 5-15 requests per session |
| Power user | Intensive feature usage | 20-50 requests per session |
| Returning user | Comes back after absence | 3-5 requests, then leaves |

---

## 4. Sustained Load Testing

### 4.1 Purpose of Sustained Load Testing

Sustained load testing validates that the system maintains performance under prolonged
high traffic, unlike burst testing which validates short-duration peaks.

**Key concerns:**

- Memory leaks that only appear under sustained load
- Connection pool exhaustion over time
- Cache eviction under sustained high throughput
- Database connection drift
- Log volume management
- Monitoring system under load

### 4.2 Sustained Load Test Scenarios

| Scenario | Duration | Load Level | Purpose |
|---|---|---|---|
| Normal sustained | 24 hours | Expected average | Stability validation |
| Peak sustained | 4 hours | Expected peak | Peak performance validation |
| Over-sustained | 2 hours | 1.5x peak | Degradation behavior |
| Variable load | 8 hours | Varying 50%-150% | Auto-scaling validation |
| Weekend simulation | 48 hours | Lower, different pattern | Off-peak behavior |

### 4.3 Sustained Load Metrics

Track these metrics throughout sustained load testing:

| Metric | Measurement | Alert Threshold |
|---|---|---|
| Throughput | Requests per second | > 10% drop from baseline |
| Latency | P99 by endpoint | > 20% increase from baseline |
| Error rate | Percentage of failed requests | > 0.5% |
| Memory usage | Heap and off-heap | > 10% growth per hour |
| GC frequency | Collections per minute | > 50% increase |
| Connection pool usage | Active connections | > 80% of pool |
| Disk usage | Log and temp file growth | > 1GB per hour |
| CPU utilization | Average across instances | > 85% sustained |

### 4.4 Memory Leak Detection

Sustained load testing is the primary method for detecting memory leaks:

- **Heap dump analysis**: Capture heap dumps at regular intervals
- **Memory growth trend**: Plot memory usage over time for linear growth
- **Object count tracking**: Monitor counts of key object types
- **Finalizer queue**: Monitor objects waiting for finalization
- **Off-heap tracking**: Monitor native memory allocations

---

## 5. Ramp-Up Testing

### 5.1 Controlled Ramp-Up

Gradually increase load to observe system behavior at each level:

```
Phase 1: 10% load → stabilize (5 min) → measure
Phase 2: 25% load → stabilize (5 min) → measure
Phase 3: 50% load → stabilize (5 min) → measure
Phase 4: 75% load → stabilize (5 min) → measure
Phase 5: 100% load → stabilize (5 min) → measure
Phase 6: 125% load → stabilize (5 min) → measure
Phase 7: 150% load → stabilize (5 min) → measure
Phase 8: 200% load → stabilize (5 min) → measure
```

### 5.2 Ramp-Up Response Analysis

For each load level, analyze system response:

| Load Level | Expected Behavior | Concerning Behavior |
|---|---|---|
| 10-25% | Linear throughput increase | Any errors or latency spikes |
| 25-50% | Linear throughput increase | Non-linear latency growth |
| 50-75% | Near-linear throughput | Auto-scaling activates |
| 75-100% | Throughput approaching max | Queuing begins |
| 100-125% | Throughput plateaus | Error rate increases |
| 125-150% | Throughput stable or declining | Significant degradation |
| 150-200% | Throughput declining | System unstable |

### 5.3 Auto-Scaling Validation During Ramp-Up

Monitor auto-scaling behavior as load increases:

- **Scale-up trigger**: At what load level does scaling begin?
- **Scale-up latency**: How quickly are new instances available?
- **Scale-up completeness**: Do new instances reach full capacity?
- **Scale-up stability**: Does the system oscillate between scale states?

### 5.4 Ramp-Down Testing

Ramp-down is as important as ramp-up:

- **Scale-down speed**: How quickly are excess instances removed?
- **Resource cleanup**: Are connections, memory, and files properly released?
- **Performance recovery**: Does latency return to normal levels?
- **Cache warming**: How quickly do new instances warm their caches?

---

## 6. Throughput vs Latency Tradeoff Analysis

### 6.1 The Throughput-Latency Curve

Every system has a characteristic curve showing the relationship between throughput and latency:

```
Latency
  ↑
  │                        ╱
  │                      ╱
  │                    ╱  ← Latency cliff
  │                  ╱
  │              ╱╱
  │          ╱╱
  │      ╱╱
  │  ╱╱
  │╱╱ ← Linear region
  └──────────────────────→ Throughput
```

**Curve regions:**

| Region | Throughput | Latency | Status |
|---|---|---|---|
| Linear | 0-60% capacity | Stable, low | Healthy |
| Transitional | 60-80% capacity | Slowly increasing | Caution |
| Knee | 80-90% capacity | Increasing rapidly | Warning |
| Cliff | > 90% capacity | Exponential increase | Critical |

### 6.2 Optimal Operating Point

The optimal operating point balances throughput and latency:

- **Max throughput**: Highest QPS achievable (usually at cliff)
- **Optimal throughput**: Highest QPS within latency SLA (usually at knee)
- **Conservative throughput**: 70% of optimal for headroom

**Decision framework:**

```
IF latency_budget is tight:
    optimize_for = minimum_latency
    target_throughput = 70% of max

IF throughput is more important:
    optimize_for = maximum_throughput_within_sla
    target_throughput = 90% of max

IF both are critical:
    optimize_for = balanced
    target_throughput = 80% of max
```

### 6.3 Tradeoff Optimization Strategies

| Strategy | Throughput Impact | Latency Impact | Complexity |
|---|---|---|---|
| Request batching | ↑↑ | ↑ (batch wait time) | Medium |
| Caching | ↑↑ | ↓↓ | Low |
| Async processing | ↑ | ↑ (async overhead) | High |
| Connection pooling | ↑ | ↓ | Low |
| Model optimization | ↑ | ↓↓ | High |
| Response compression | ↑ | ↓ (compression time) | Low |

### 6.4 Capacity Planning

Use throughput test results for capacity planning:

- **Current capacity**: Maximum sustainable QPS at acceptable latency
- **Growth projection**: Expected QPS increase over next 6-12 months
- **Headroom requirement**: 30-50% headroom above projected peak
- **Infrastructure cost**: Cost per QPS at different capacity levels
- **Scaling plan**: Infrastructure additions needed at each growth milestone

---

## 7. Throughput Testing Framework

### 7.1 Load Generation Tools

| Tool | Language | Features | Best For |
|---|---|---|---|
| Locust | Python | Custom user behavior, distributed | Complex user simulation |
| k6 | JavaScript | Built-in metrics, thresholds | API load testing |
| wrk2 | C | High throughput, constant rate | Raw throughput measurement |
| Gatling | Scala | Detailed reports, scenarios | Full-featured load testing |
| vegeta | Go | Constant rate, attack mode | Throughput benchmarking |

### 7.2 Test Execution Pipeline

```
Baseline Measurement → Ramp-Up Test → Sustained Load Test → Spike Test → Recovery Test
        ↓                  ↓                ↓                  ↓             ↓
   Record metrics     Find limits     Validate stability   Test burst   Verify recovery
   at current         at each level   under prolonged      handling     to baseline
   capacity                           load
```

### 7.3 Throughput Test Reporting

Every throughput test produces:

1. **Maximum sustainable QPS**: Highest QPS within latency SLA
2. **Breaking point**: QPS where error rate exceeds threshold
3. **Latency curve**: Latency at each throughput level
4. **Component bottlenecks**: Which component limits throughput
5. **Auto-scaling effectiveness**: Scaling response time and accuracy
6. **Recovery metrics**: Time to return to baseline after test
7. **Cost analysis**: Infrastructure cost per QPS
8. **Capacity recommendations**: Infrastructure changes for target throughput
