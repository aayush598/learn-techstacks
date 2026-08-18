# Chaos Engineering for Recommendation Systems

## Overview

Chaos engineering is the discipline of experimenting on a system to build confidence in its
capability to withstand turbulent conditions in production. For recommendation systems, this
means deliberately introducing failures — latency spikes, service outages, resource exhaustion,
network partitions — to verify that the system degrades gracefully and recovers automatically.
The goal is not to break things, but to discover weaknesses before they cause customer-facing
incidents.

## Principles of Chaos Engineering

### The Chaos Engineering Formula

1. **Steady state hypothesis**: Define what "normal" looks like (latency, throughput, error rate)
2. **Introduce real-world events**: Simulate failures that occur in production
3. **Observe the difference**: Compare system behavior during experiment vs. steady state
4. **Automate and run continuously**: Chaos experiments run in CI/CD, not just ad hoc

### Blast Radius Containment

Every chaos experiment must have defined boundaries:

- **Scope**: Which services and users are affected
- **Duration**: Maximum experiment duration before automatic rollback
- **Thresholds**: Automated abort if key metrics degrade beyond acceptable limits
- **Rollback plan**: How to immediately restore normal operation
- **Notification**: Alert on-call engineers before experiment begins

## Fault Injection Types for Recommendation Systems

### 1. Latency Injection

**Purpose**: Verify timeout handling and graceful degradation

| Target                     | Injection Method                            | Expected Behavior                              |
|---------------------------|----------------------------------------------|------------------------------------------------|
| Feature store (Redis)     | Add 200ms delay to 50% of reads             | Fall back to cached features or default values |
| User service API          | Add 500ms delay to all requests             | Use cached user profile, return stale recs     |
| Model serving endpoint    | Add 100ms delay to inference calls          | Switch to lighter model or popularity fallback |
| Catalog service           | Add 300ms delay to item metadata requests   | Return recommendations without metadata        |
| Kafka consumer            | Inject processing delay                      | Consumer lag increases but events not lost     |

**Key Metrics to Monitor**:
- Request latency distribution shifts
- Timeout rate and retry amplification
- Circuit breaker state transitions
- Fallback path activation rate

### 2. Error Injection

**Purpose**: Verify error handling and fallback mechanisms

| Target                     | Injection Method                            | Expected Behavior                              |
|---------------------------|----------------------------------------------|------------------------------------------------|
| Feature store             | Return HTTP 500 for 20% of requests         | Feature computation falls back to defaults     |
| User service              | Return HTTP 503 for 30s                      | Serve popular items instead of personalized    |
| Model serving             | Return model prediction errors               | Graceful degradation to rule-based system      |
| Catalog service           | Return partial item data                     | Serve recommendations with missing metadata    |
| Database                  | Connection refused for 60s                   | Read replicas handle traffic, write queue buffers |

### 3. Resource Exhaustion

**Purpose**: Verify behavior under constrained resources

| Resource                  | Exhaustion Method                            | Expected Behavior                              |
|---------------------------|----------------------------------------------|------------------------------------------------|
| CPU                      | Stress one pod to 100% CPU                   | Horizontal scaling, other pods unaffected       |
| Memory                   | Allocate memory until near OOM               | Graceful connection draining, no data loss     |
| Disk I/O                 | Saturate disk with write operations          | Log rotation, metric buffering, no crash       |
| Network bandwidth        | Throttle network to 1Mbps                    | Reduced batch sizes, increased timeouts        |
| File descriptors         | Exhaust FD limit                             | Connection pooling handles gracefully          |
| Feature store memory     | Fill Redis to 95% capacity                   | Eviction policy activates, popular items stay  |

### 4. Network Partition

**Purpose**: Verify split-brain handling and data consistency

| Scenario                                | Expected Behavior                             |
|----------------------------------------|------------------------------------------------|
| Partition between API and feature store | Serve cached features, queue writes            |
| Partition between model server and API  | Switch to local model or fallback system       |
| Partition between Kafka brokers        | Leader election, message delivery guarantee     |
| DNS resolution failure                 | Circuit breaker activates, cached DNS used     |
| TLS certificate expiration             | Automatic renewal, graceful degradation        |

## Chaos Monkey and Litmus Principles

### Chaos Monkey (Netflix Pattern)

- Randomly terminates instances in production during business hours
- Forces engineers to design resilient services from day one
- Assumes failures will happen and validates recovery automatically
- Runs continuously, not as one-time experiments

### Litmus (Kubernetes-Native Chaos)

Litmus provides Kubernetes-native chaos engineering:

**Chaos Engineering Workflow in Kubernetes**:
1. **Install Litmus**: Deploy chaos control plane in cluster
2. **Define experiments**: ChaosEngine CRDs specify fault injection
3. **Inject faults**: Pod delete, CPU stress, network latency, DNS chaos
4. **Observe**: Monitor application metrics during experiment
5. **Analyze**: Compare metrics against steady-state hypothesis
6. **Automate**: Run experiments in CI/CD pipeline

### Common Litmus Experiments for Recommendation Systems

- `pod-delete`: Kill random recommendation service pods
- `cpu-hog`: Stress CPU on model serving pods
- `memory-hog`: Exhaust memory on feature store pods
- `pod-network-latency`: Add latency between microservices
- `pod-network-loss`: Simulate packet loss on inter-service communication
- `disk-fill`: Fill disk on logging/cache nodes
- `node-drain`: Evict all pods from a Kubernetes node

## Game Day Exercises

### What Are Game Days?

Scheduled, coordinated chaos experiments involving multiple teams. Unlike automated chaos tests,
game days involve human decision-making and cross-team coordination.

### Game Day Planning Template

```
Experiment: Feature Store Failure
Date: [Scheduled Date]
Duration: 2 hours
Participants: Recommendation team, Platform team, SRE on-call
Severity: High (simulating production incident)

Objectives:
  - Verify recommendation service falls back correctly
  - Measure time to detect and auto-recover
  - Practice incident communication procedures

Pre-conditions:
  - Staging environment with full traffic mirror
  - All teams notified and available
  - Rollback procedure documented and tested

Success Criteria:
  - Fallback activated within 30 seconds
  - No customer-facing errors
  - Full recovery within 5 minutes
  - Incident runbook is accurate and complete

Post-experiment:
  - Team retrospective within 24 hours
  - Action items tracked in issue tracker
  - Runbook updated with findings
```

### Game Day Scenarios for Recommendation Systems

| Scenario                           | Duration  | Teams Involved                |
|------------------------------------|-----------|-------------------------------|
| Complete model serving outage      | 1 hour    | ML, Platform, SRE            |
| Feature store data corruption      | 2 hours   | ML, Data Engineering, SRE    |
| Kafka topic partition loss         | 30 min    | Platform, SRE                |
| Full region failure                | 3 hours   | All engineering teams        |
| DNS failure for external services  | 1 hour    | Platform, SRE                |
| Database primary failover          | 45 min    | Data Engineering, SRE        |
| Memory leak causing OOM kills      | 2 hours   | Recommendation team, SRE     |

## Chaos Testing in Kubernetes

### Pod-Level Experiments

```
Experiment: Random Pod Termination
Target: recommendation-service namespace
Parameters:
  - Force: true (immediate termination, not graceful)
  - Interval: every 5 minutes
  - Max pod kills: 2 per interval
  - Label selector: app=recommendation-api

Verification:
  - No dropped requests (all retries succeed)
  - P99 latency stays below 500ms
  - New pods are scheduled within 30 seconds
  - Feature cache is warm before handling production traffic
```

### Node-Level Experiments

```
Experiment: Node Drain
Target: recommendation-compute node pool
Parameters:
  - Drain one node every 30 minutes
  - Node unschedulable for 5 minutes
  - Pods rescheduled to remaining nodes

Verification:
  - Cluster autoscaler adds replacement node within 3 minutes
  - No OOM kills on remaining nodes
  - Model serving latency does not exceed 2x baseline
  - Inter-pod affinity rules are respected during rescheduling
```

### Namespace-Level Experiments

```
Experiment: Network Policy Isolation
Target: model-serving namespace
Parameters:
  - Block all ingress from recommendation-api namespace
  - Duration: 10 minutes

Verification:
  - Circuit breakers activate within 5 seconds
  - Fallback model is used for all requests
  - No health check failures (should use local health endpoint)
  - Recovery is automatic when network policy is removed
```

## Blast Radius Containment Strategies

### Progressive Exposure

Run chaos experiments with increasing blast radius:

1. **Single pod**: Kill one pod, verify self-healing
2. **Multiple pods**: Kill 30% of pods, verify horizontal scaling
3. **Single node**: Drain one node, verify rescheduling
4. **Service-wide**: Inject latency across all instances of one service
5. **Cross-service**: Simulate network partition between two services
6. **Full region**: Simulate complete region failure (game day only)

### Automatic Abort Conditions

Every chaos experiment must have circuit breakers:

- Error rate exceeds 5% for more than 30 seconds
- P99 latency exceeds 2x baseline for more than 1 minute
- Any dependent service becomes unavailable
- Data loss is detected (missing events, corrupted features)
- Manual abort signal from on-call engineer

### Canary Experiments

Before running chaos in staging, run in a production canary:

1. Deploy chaos experiment targeting 1% of production traffic
2. Monitor for 15 minutes
3. If metrics are within bounds, expand to 10%
4. If metrics degrade, abort and investigate
5. Never run untested chaos experiments in full production

## Chaos Testing Metrics

### Experiment Success Criteria

| Metric                    | Pass Threshold                           |
|--------------------------|------------------------------------------|
| Availability during chaos | >= 99.9% (for latency injection)        |
| Error rate during chaos   | <= 1% (for error injection)             |
| Recovery time             | <= 5 minutes to full steady state        |
| Data loss                 | Zero events lost                         |
| Alerting accuracy         | Correct alerts fire, no false positives  |

### Chaos Maturity Model

| Level | Description                                          |
|-------|------------------------------------------------------|
| 1     | Ad hoc game days, manual fault injection             |
| 2     | Automated single-fault experiments in staging        |
| 3     | Continuous chaos in CI/CD, multiple fault types      |
| 4     | Production chaos with progressive exposure           |
| 5     | Full regional failure testing, automated abort       |
