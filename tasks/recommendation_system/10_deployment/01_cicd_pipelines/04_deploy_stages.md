# Deploy Stages

Deploy stages translate verified code into production traffic. For recommendation systems, deployment is uniquely complex because you're deploying not just application code but also model artifacts, feature configurations, and experiment parameters. A failed deployment doesn't just break the service — it silently degrades recommendation quality for millions of users. This document covers staging deployments, canary and blue-green strategies, deployment verification, automated rollback, ML-specific feature flags, and deployment window management.

---

## 1. Staging Deployment

### 1.1 Full Environment Parity

Staging must mirror production as closely as possible to catch environment-specific issues.

| Dimension | Staging Configuration | Rationale |
|---|---|---|
| Cluster topology | Same number of AZs as production | Catch AZ-awareness bugs |
| Instance types | Same family, possibly smaller sizes | Catch architecture-specific issues |
| Data volume | 10–20% of production | Realistic enough for performance testing |
| Feature store | Production snapshot (T-1 day) | Real feature distributions |
| Model version | Candidate model + production baseline | A/B comparison in staging |
| Traffic patterns | Replay production traffic (1 hour sample) | Validate under realistic load |
| Dependencies | Point to staging instances, not production | Isolate staging failures |

### 1.2 Staging Deployment Gates

| Gate | Criteria | Blocking? |
|---|---|---|
| Container image | Passed build stage, scanned, signed | Yes |
| Helm chart | Values validated, template rendered successfully | Yes |
| Smoke tests | All critical endpoints return correct responses | Yes |
| Performance tests | P95 latency within 15% of baseline | Yes |
| Model quality | Offline metrics meet minimum thresholds | Yes |
| Data pipeline | Feature freshness < 5 minutes | Yes |
| Monitoring | Dashboards show healthy trends for 30 minutes | No (advisory) |

### 1.3 Staging Data Management

- Refresh staging data weekly from production snapshots
- Anonymize all PII before loading into staging
- Preserve data distributions and edge cases (cold-start users, popular items)
- Maintain referential integrity across staging data sources

---

## 2. Canary Deployment

Canary deployment gradually shifts traffic to the new version while monitoring for issues.

### 2.1 Traffic Shifting Strategy

| Phase | Traffic % | Duration | Monitoring Focus | Auto-Advance? |
|---|---|---|---|---|
| Phase 1 | 5% | 15 minutes | Error rate, crash rate | No (manual approval) |
| Phase 2 | 25% | 30 minutes | Latency P95, model metrics | No (manual approval) |
| Phase 3 | 50% | 1 hour | Full monitoring suite | Yes (if all green) |
| Phase 4 | 100% | Permanent | Standard monitoring | N/A |

### 2.2 Canary Analysis

Automated canary analysis compares new version against baseline:

**Statistical approach:**

- Use **sequential hypothesis testing** (not fixed-horizon tests) for faster decisions
- Compare error rates using a two-proportion z-test
- Compare latency distributions using Mann-Whitney U test
- Compare model quality metrics using bootstrapped confidence intervals
- Require 95% confidence before advancing traffic

**Key metrics for canary evaluation:**

| Metric | Comparison | Threshold |
|---|---|---|
| Error rate | New vs baseline | < 0.1% increase |
| P50 latency | New vs baseline | < 5% increase |
| P99 latency | New vs baseline | < 10% increase |
| Recommendation CTR | New vs baseline | > -2% (no significant degradation) |
| Model confidence | New vs baseline | Distribution shift < 5% (KS test) |

### 2.3 Traffic Routing Implementation

**Istio-based routing:**

- Define `VirtualService` with traffic weight split
- Define `DestinationRule` with canary subset
- Update weights via ArgoCD or automated pipeline step
- Automatic rollback triggers on metric violation

**Nginx-based routing:**

- Use `split_clients` module for percentage-based routing
- Cookie-based sticky sessions ensure user consistency during canary
- Fallback to baseline on upstream timeout

### 2.4 Canary for Model Updates

Model canary deployments require additional validation:

- **Prediction distribution check**: Ensure new model's score distribution doesn't diverge dramatically from baseline
- **Feature importance stability**: Monitor that feature importance rankings remain reasonable
- **User cohort analysis**: Compare new vs baseline across user segments (new users, power users, churned users)
- **Catalog coverage**: Verify new model doesn't collapse recommendations to a small subset of items

---

## 3. Blue-Green Deployment

### 3.1 Architecture

Blue-green maintains two identical production environments:

| Environment | State | Traffic | Purpose |
|---|---|---|---|
| Blue | Current production | 100% | Serving live traffic |
| Green | New version | 0% | Deployed and verified, ready for switch |
| (After switch) | | | |
| Blue | Previous version | 0% | Standby for rollback |
| Green | New version | 100% | Now serving live traffic |

### 3.2 Switch Process

1. Deploy new version to Green environment
2. Run health checks and smoke tests against Green
3. Run canary analysis with 5% traffic split (optional)
4. Switch DNS/load balancer to point to Green
5. Keep Blue running for 30 minutes (rollback window)
6. Drain Blue connections
7. Decommission Blue (or prepare for next deployment)

### 3.3 Database Considerations

Blue-green deployments complicate database management:

- Database schema changes must be **backward-compatible** (both old and new app versions must work)
- Use expand-and-contract migration pattern:
  - **Expand**: Add new columns/tables without removing old ones
  - **Migrate**: Deploy new app version that uses new schema
  - **Contract**: Remove old columns/tables in subsequent deployment
- Feature flags control which code path accesses which schema version

---

## 4. Deployment Verification

### 4.1 Smoke Tests

Automated smoke tests run immediately after deployment:

| Test | Endpoint | Expected | Timeout |
|---|---|---|---|
| Health check | `GET /health` | 200 OK | 5s |
| Readiness check | `GET /ready` | 200 OK | 10s |
| Model loading | `GET /model/status` | model_loaded=true | 30s |
| Sample prediction | `POST /predict` | 200, valid response schema | 5s |
| Feature store connection | `GET /features/health` | 200 OK | 5s |
| Cache connectivity | `GET /cache/health` | 200 OK | 5s |

### 4.2 Automated Rollback Triggers

Define precise triggers that automatically roll back without human intervention:

| Trigger | Measurement | Threshold | Action |
|---|---|---|---|
| Error rate spike | 5xx responses / total requests | > 1% for 2 minutes | Immediate rollback |
| Latency spike | P95 latency | > 2x baseline for 3 minutes | Immediate rollback |
| Crash loop | Container restart count | > 3 restarts in 5 minutes | Immediate rollback |
| Model failure | Prediction error rate | > 5% for 2 minutes | Rollback model only |
| Feature store down | Feature retrieval failure rate | > 10% for 1 minute | Rollback to cached features |
| Health check failure | Failed health checks | > 3 consecutive | Immediate rollback |

### 4.3 Rollback Execution

**Service rollback**: Update deployment to previous image tag. Kubernetes rolling update handles graceful transition.

**Model rollback**: Reload previous model checkpoint from artifact store. Does not require service restart (hot swap).

**Configuration rollback**: Revert feature flag changes, config map updates, or environment variable changes.

**Database rollback**: Only if migration was backward-compatible (expand phase). Contract phase rollback requires careful coordination.

---

## 5. Feature Flags for ML

### 5.1 ML-Specific Feature Flag Patterns

Feature flags in ML systems control more than UI elements — they control model selection, feature computation paths, and ranking algorithms.

**Flag categories:**

| Category | Example Flag | Purpose |
|---|---|---|
| Model selection | `model_v2_enabled` | Toggle between model versions |
| Feature pipeline | `use_real_time_features` | Enable/disable real-time feature computation |
| Ranking strategy | `diversity_weighting_v2` | Switch between ranking algorithms |
| Experiment allocation | `exp_2024_q1_collaborative_filtering` | A/B test experiment groups |
| Fallback behavior | `degrade_to_popular` | Enable graceful degradation mode |
| Rate limiting | `feature_store_rate_limit` | Throttle feature store queries during incidents |

### 5.2 LaunchDarkly Patterns

| Pattern | Implementation | Use Case |
|---|---|---|
| Percentage rollout | Gradual percentage increase over time | New model deployment |
| User targeting | Specific user IDs or segments | Beta testing with internal users |
| Targeting rules | Based on user attributes (country, device, plan) | Regional or segment-specific features |
| Prerequisites | Flag B only active if Flag A is active | Model B requires feature pipeline v2 |
| Scheduled changes | Automatic flag changes at specific times | Deployment window management |
| Experimentation | Built-in statistical analysis for flag variations | A/B testing ranking algorithms |

### 5.3 Flag Lifecycle Management

- **Creation**: Requires justification document and owner
- **Activation**: Automated via CI/CD pipeline on deploy
- **Monitoring**: Flag state changes logged and alerted
- **Retirement**: Flags older than 90 days require cleanup plan
- **Audit trail**: All flag changes attributed to specific deployments or engineers

---

## 6. Deployment Windows

### 6.1 Why Deployment Windows Matter

Recommendation systems serve global audiences. Deployments during peak hours risk user-facing degradation.

### 6.2 Window Definition

| Window | Hours (UTC) | Traffic Level | Deployment Allowed? |
|---|---|---|---|
| Peak (APAC + Americas overlap) | 13:00–17:00 | Highest | No (critical path only) |
| Americas business | 17:00–01:00 | High | Canary only (5% max) |
| EMEA business | 07:00–13:00 | Medium | Full deployment |
| Off-peak | 01:00–07:00 | Lowest | Full deployment + migrations |
| Freeze | Varies | Any | No (holidays, major events) |

### 6.3 Automated Window Enforcement

- Pipeline checks current time against deployment window schedule
- Block production deployments outside allowed windows
- Emergency deployments require override approval (2 approvers minimum)
- Deployment freeze calendar maintained in shared tool (PagerDuty, OpsGenie)

### 6.4 Deployment Velocity Tracking

| Metric | Target | Measurement |
|---|---|---|
| Deployment frequency | ≥ 3 per week | Count of production deployments |
| Lead time for changes | < 2 hours | Commit to production |
| Change failure rate | < 5% | Deployments causing rollback or incident |
| Mean time to recovery | < 30 minutes | Time from incident detection to resolution |
