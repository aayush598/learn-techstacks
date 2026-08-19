# Availability Requirements — Recommendation System

## 1. SLA / SLO / SLI Framework

### 1.1 Definitions

- **SLI (Service Level Indicator)**: A quantitative measure of a specific aspect of service behavior — e.g., the proportion of requests that complete within 200ms.
- **SLO (Service Level Objective)**: A target value for an SLI over a specified time window — e.g., "99.5% of requests complete within 200ms over a rolling 30-day window."
- **SLA (Service Level Agreement)**: A contractual commitment that specifies consequences (financial penalties, service credits) if SLOs are not met. SLAs are always more conservative than SLOs.

### 1.2 SLI Definitions for Recommendation System

| SLI Name | Formula | Measurement Window | Alert Threshold |
|----------|---------|-------------------|-----------------|
| Availability SLI | Successful requests / Total requests (excluding client errors) | 5-min rolling | < 99.9% |
| Latency SLI | Requests within latency budget / Total requests | 5-min rolling | < 99.0% |
| Correctness SLI | Recommendations matching expected schema / Total recommendations | 1-hour rolling | < 99.9% |
| Freshness SLI | Recommendations generated within TTL / Total recommendations | 1-hour rolling | < 95.0% |
| Error Budget | 1 - Availability SLI target | 30-day rolling | Consumed > 50% |

### 1.3 SLO Targets by Component

| Component | Availability SLO | Latency SLO (P95) | Error Budget (30-day) |
|-----------|-----------------|-------------------|----------------------|
| Core Recommendation API | 99.99% | ≤ 200 ms | 4.32 minutes |
| Feature Store | 99.99% | ≤ 10 ms | 4.32 minutes |
| Candidate Retrieval | 99.95% | ≤ 50 ms | 21.6 minutes |
| Model Serving | 99.95% | ≤ 15 ms | 21.6 minutes |
| Event Ingestion | 99.9% | N/A (async) | 43.2 minutes |
| Model Training | 99.5% | N/A (batch) | 3.6 hours |
| Email Recommendations | 99.5% | N/A (batch) | 3.6 hours |
| Admin Dashboard | 99.0% | ≤ 1000 ms | 7.2 hours |

---

## 2. Availability Tiers

### 2.1 Tier 1 — Mission Critical (99.99%)

- **Components**: Core recommendation API, feature store, user authentication.
- **Downtime Budget**: 52.6 minutes per year, 4.32 minutes per month.
- **Architecture Requirements**:
  - Active-active deployment across ≥ 2 availability zones.
  - Automatic failover with ≤ 30 second detection + ≤ 60 second switchover.
  - No single point of failure at any layer.
  - Data replication with synchronous or near-synchronous consistency.
- **Testing**: Monthly chaos engineering tests; quarterly full AZ failure simulation.

### 2.2 Tier 2 — Business Critical (99.9%)

- **Components**: Candidate retrieval, model serving, real-time feature computation.
- **Downtime Budget**: 8.76 hours per year, 43.2 minutes per month.
- **Architecture Requirements**:
  - Active-active or active-passive deployment across ≥ 2 availability zones.
  - Automatic failover with ≤ 5 minute recovery time.
  - Graceful degradation to cached or simplified responses during outages.
- **Testing**: Quarterly failover tests; monthly health check validation.

### 2.3 Tier 3 — Important (99.5%)

- **Components**: Email recommendations, batch processing, analytics dashboards.
- **Downtime Budget**: 1.83 days per year, 3.6 hours per month.
- **Architecture Requirements**:
  - Single-region deployment with standby in another region.
  - Manual failover with documented runbook.
  - Retry and backfill capabilities for missed batch jobs.
- **Testing**: Semi-annual failover tests.

### 2.4 Tier 4 — Best Effort (99.0%)

- **Components**: Admin tools, model training pipelines, development environments.
- **Downtime Budget**: 3.65 days per year, 7.2 hours per month.
- **Architecture Requirements**:
  - Single-region deployment with backup.
  - Best-effort availability with SLA defined for internal teams only.

---

## 3. Mean Time Between Failures (MTBF) and Mean Time To Repair (MTTR)

### 3.1 MTBF Targets

| Component | MTBF Target | Implication |
|-----------|------------|-------------|
| Core API | ≥ 720 hours (30 days) | Failures should be rare; infrastructure resilience is paramount |
| Feature Store | ≥ 720 hours | Redundant storage with automatic failover |
| Model Serving | ≥ 360 hours (15 days) | Model servers are more failure-prone; fast recovery is key |
| Event Pipeline | ≥ 168 hours (7 days) | Stream processing failures are expected; resilience through retries and DLQs |

### 3.2 MTTR Targets

| Severity | Detection Time | Escalation Time | Resolution Target | Total MTTR |
|----------|---------------|-----------------|-------------------|------------|
| SEV-1 (Core API down) | ≤ 1 minute | ≤ 5 minutes | ≤ 30 minutes | ≤ 36 minutes |
| SEV-2 (Degraded performance) | ≤ 2 minutes | ≤ 10 minutes | ≤ 1 hour | ≤ 72 minutes |
| SEV-3 (Non-critical component) | ≤ 5 minutes | ≤ 30 minutes | ≤ 4 hours | ≤ 4 hours 35 min |
| SEV-4 (Batch job failure) | ≤ 15 minutes | ≤ 1 hour | ≤ 8 hours | ~8 hours |

### 3.3 Reliability Engineering Practices

- **Post-Incident Reviews**: Every SEV-1 and SEV-2 incident must have a post-incident review (blameless) within 48 hours, with action items tracked to completion.
- **Error Budget Policies**: When 50% of the monthly error budget is consumed, deploy freezes are triggered for non-critical changes. When 100% is consumed, all deployments are frozen except security and reliability fixes.
- **Reliability Reviews**: Quarterly reliability reviews must assess SLO compliance, incident trends, and error budget consumption, with findings presented to engineering leadership.

---

## 4. Graceful Degradation

### 4.1 Degradation Hierarchy

When components fail, the system must degrade gracefully through a defined hierarchy rather than failing completely:

| Level | Condition | Behavior | User Impact |
|-------|-----------|----------|-------------|
| **L0 — Full Service** | All components healthy | Full personalized recommendations with all features | None |
| **L1 — Cached Mode** | Model serving degraded | Serve cached or pre-computed recommendations | Recommendations may be slightly stale (up to 1 hour) |
| **L2 — Popularity Mode** | Feature store unavailable | Serve popularity-based recommendations per category | Personalization lost; recommendations still relevant |
| **L3 — Static Fallback** | Candidate retrieval unavailable | Serve editorially curated or static recommendation lists | Limited catalog coverage; no personalization |
| **L4 — Minimal Response** | Core API severely degraded | Return a basic response with "Recommendations unavailable" message | No recommendations; other site functionality preserved |

### 4.2 Degradation Implementation

- **Health Check Propagation**: Each service must expose a health endpoint that reflects the status of its critical dependencies. The recommendation API must check upstream health and select the appropriate degradation level.
- **Feature Flag Control**: Degradation levels must be controllable via feature flags, allowing operations to manually force a degradation level during incidents.
- **User Communication**: At degradation levels L2 and below, the UI must gracefully handle missing or generic recommendations without displaying errors or empty states.
- **Automatic Recovery**: When upstream dependencies recover, the system must automatically transition back to the full service level without manual intervention, with a configurable cool-down period (e.g., 2 minutes).

---

## 5. Fallback Mechanisms

### 5.1 Fallback Chain

```
Primary Model (Full Personalization)
    ↓ (model serving failure)
Cached Model Predictions (pre-computed for active users)
    ↓ (cache miss or staleness > TTL)
Popularity-Based Recommendations (real-time popularity computation)
    ↓ (popularity service unavailable)
Pre-Computed Trending Lists (updated hourly, served from cache)
    ↓ (all dynamic sources unavailable)
Editorial Picks (static content, served from CDN)
    ↓ (CDN unavailable)
Empty State with "Try Again Later" message
```

### 5.2 Fallback Data Freshness

| Fallback Source | Data Freshness | Coverage | Personalization Level |
|----------------|---------------|----------|---------------------|
| Cached Model Predictions | Last computation (up to 1 hour) | Active users only | High |
| Popularity-Based | Real-time or near-real-time | Full catalog | None (category-level only) |
| Pre-Computed Trending | Updated hourly | Top 1K items | None |
| Editorial Picks | Updated daily | Top 100 items | None |

### 5.3 Fallback Testing

- **Chaos Testing**: Monthly chaos experiments must verify that each fallback level activates correctly when the corresponding dependency is artificially failed.
- **Fallback Latency**: Each fallback must respond faster than the primary path — the system should never add latency by attempting a slow fallback after a primary timeout.
- **User Experience Validation**: A/B tests must validate that fallback experiences maintain acceptable user engagement compared to full personalization.

---

## 6. Circuit Breaker Pattern

### 6.1 Circuit Breaker Configuration

| Dependency | Failure Threshold | Open Duration | Half-Open Probe Interval | Success Threshold to Close |
|-----------|-------------------|---------------|-------------------------|---------------------------|
| Model Serving | 5 failures in 10 seconds | 30 seconds | 10 seconds | 3 consecutive successes |
| Feature Store | 3 failures in 10 seconds | 60 seconds | 15 seconds | 5 consecutive successes |
| Candidate Retrieval | 5 failures in 10 seconds | 30 seconds | 10 seconds | 3 consecutive successes |
| External APIs | 3 failures in 30 seconds | 120 seconds | 30 seconds | 5 consecutive successes |

### 6.2 Circuit Breaker States

- **Closed (Normal)**: Requests flow through to the dependency. Failures are counted; when the threshold is reached, the circuit opens.
- **Open (Failing)**: All requests are immediately rejected with the fallback response. No requests reach the dependency, allowing it to recover.
- **Half-Open (Probing)**: A limited number of requests are allowed through to probe if the dependency has recovered. If they succeed, the circuit closes; if they fail, it re-opens.

### 6.3 Observability

- **Circuit Breaker Metrics**: State transitions, failure counts, and fallback invocations must be emitted as metrics with dependency labels.
- **Alerting**: Circuit breaker state changes must trigger alerts (SEV-2 for open state lasting > 5 minutes; SEV-1 for cascading circuit breakers across multiple dependencies).

---

## 7. Health Checks

### 7.1 Health Check Types

| Check Type | Frequency | Timeout | Purpose |
|-----------|-----------|---------|---------|
| Liveness Probe | Every 10 seconds | 3 seconds | Detect deadlocked or unresponsive processes |
| Readiness Probe | Every 5 seconds | 2 seconds | Determine if the instance can accept traffic |
| Startup Probe | Every 5 seconds | 30 seconds | Allow slow-starting instances to initialize |

### 7.2 Health Check Implementation

- **Liveness Check**: Verifies that the process is alive and not deadlocked — typically a simple `/healthz` endpoint that returns 200 OK. Must not check external dependencies (to avoid false positives).
- **Readiness Check**: Verifies that the instance is ready to serve traffic — checks connectivity to critical dependencies (feature store, model serving, cache). Returns 503 if any critical dependency is unreachable.
- **Deep Health Check**: A `/healthz/deep` endpoint that runs a full diagnostic — verifying model loading, feature computation, and end-to-end pipeline integrity. Used during deployment validation and periodic audits (every 5 minutes).

### 7.3 Health Check Cascading Prevention

- **Timeout Budget**: Health checks must complete within their timeout budget; slow dependency checks must be short-circuited to prevent health check timeouts from triggering unnecessary restarts.
- **Cached Health**: Health check results must be cached for 5 seconds to avoid overwhelming downstream dependencies with health check requests during partial outages.
- **Independent Health Endpoints**: Each service must have its own health endpoint; a service must report unhealthy only if it cannot fulfill its own responsibilities, not if a downstream dependency is unhealthy (that is handled by the circuit breaker).
