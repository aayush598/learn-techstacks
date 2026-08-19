# Rollback Procedures

Rollbacks are the safety net of deployment. For recommendation systems, rollback is uniquely complex because you may need to revert application code, model artifacts, feature configurations, and database schemas — potentially in different combinations. A recommendation system stuck on a degraded model while engineers scramble to understand what to roll back is a failed rollback process. This document defines automated triggers, rollback procedures for each system layer, communication protocols, and post-rollback verification.

---

## 1. Automated Rollback Triggers

### 1.1 Error Rate Monitoring

| Metric | Detection Window | Threshold | Action |
|---|---|---|---|
| HTTP 5xx rate | 1-minute sliding window | > 1% of total requests | Auto-rollback (immediate) |
| HTTP 5xx rate | 5-minute sliding window | > 0.5% of total requests | Auto-rollback (immediate) |
| Prediction error rate | 2-minute window | > 5% invalid responses | Auto-rollback (immediate) |
| Timeout rate | 1-minute window | > 2% requests exceeding SLA | Auto-rollback (with 30s grace) |

**Implementation:** Prometheus alert rules trigger PagerDuty incidents and simultaneously execute rollback via webhook to the deployment controller (ArgoCD, Argo Rollouts).

### 1.2 Latency Spike Detection

| Metric | Detection Method | Threshold | Action |
|---|---|---|---|
| P95 latency | Rolling 5-minute comparison | > 2× baseline | Auto-rollback |
| P99 latency | Rolling 5-minute comparison | > 3× baseline | Auto-rollback |
| Latency regression | Mann-Whitney U test | p-value < 0.01, effect size > 20% | Auto-rollback |
| Feature store latency | Rolling 2-minute window | > 50ms P95 (baseline: 10ms) | Feature cache fallback + alert |

### 1.3 Model-Specific Triggers

| Trigger | Measurement | Threshold | Action |
|---|---|---|---|
| Recommendation diversity collapse | Average intra-list diversity | < 50% of baseline | Model rollback |
| Cold-start failure rate | Predictions for new users | > 30% error | Model rollback |
| Catalog coverage drop | Unique items recommended | < 40% of catalog | Model rollback |
| Score distribution shift | KL divergence vs baseline | > 0.1 | Alert + investigation |
| Feature importance anomaly | Top feature coefficient | > 3σ from expected | Alert + investigation |

### 1.4 Alert Escalation

| Severity | Response Time | Notification Channel | Escalation |
|---|---|---|---|
| P0 (service down) | Immediate | PagerDuty (call) | Engineering lead in 5 minutes |
| P1 (significant degradation) | 5 minutes | PagerDuty (page) | Engineering lead in 15 minutes |
| P2 (minor degradation) | 15 minutes | Slack + email | Team review in 1 hour |
| P3 (observation) | 1 hour | Slack channel | Next standup |

---

## 2. Service Rollback

### 2.1 Application Code Rollback

Rolling back the application container to the previous known-good image tag.

**Kubernetes implementation:**

```
Deployment strategy: RollingUpdate
Rollback: kubectl rollout undo deployment/<service>
```

**Key considerations:**

- Previous image tag must be available in the registry (retention policy ensures this)
- Rolling update gradually replaces pods — no downtime during rollback
- `rollout history` shows all revisions and their triggering commits
- Set `revisionHistoryLimit` to 10 (minimum) for sufficient rollback history

### 2.2 Graceful Rollback Sequence

1. Detect trigger (automated or manual)
2. Identify current and target (previous) image versions
3. Execute rollback command
4. Monitor rollout status until all pods are updated
5. Verify health checks pass on rolled-back version
6. Run smoke tests against the rolled-back deployment
7. Monitor error rate and latency for 10 minutes post-rollback
8. Communicate rollback completion

### 2.3 Rollback with Zero Downtime

- Ensure the previous version's database schema is compatible
- If feature flags control new behavior, disable flags before rolling back code
- Verify that cached responses from the new version won't cause issues after rollback
- Consider connection draining — existing requests to old pods should complete

---

## 3. Model Rollback

### 3.1 Model Version Management

Maintain a registry of model versions with metadata:

| Field | Example | Purpose |
|---|---|---|
| Version | `v2.3.1` | Human-readable identifier |
| Artifact path | `s3://models/prod/collab-filter/v2.3.1/model.pkl` | Artifact location |
| Training date | `2024-01-15` | Freshness tracking |
| Training data range | `2023-12-01 to 2024-01-15` | Data lineage |
| Evaluation metrics | AUC=0.82, NDCG=0.45 | Quality baseline |
| Deployed timestamp | `2024-01-20T10:00:00Z` | Deployment tracking |
| Status | `active`, `retired`, `rollback_target` | Lifecycle state |

### 3.2 Hot-Swap Model Rollback

Model rollback without service restart:

1. Model server detects rollback command (via API or config change)
2. Load previous model artifact from artifact store
3. Validate artifact integrity (checksum, format compatibility)
4. Warm up model on sample requests
5. Switch traffic from new model to old model (atomic swap)
6. Unload new model from memory
7. Verify prediction quality on test requests

**Target time: < 60 seconds for full model swap.**

### 3.3 Rollback Decision Matrix

| Scenario | Rollback Type | Target |
|---|---|---|
| Model accuracy degraded | Full model rollback | Previous model version |
| Feature pipeline bug fixed | Feature config rollback | Previous feature config |
| Model serving infra issue | Service rollback | Previous container image |
| Model + code change together | Coordinated rollback | Both previous versions |
| Database schema change | Schema-aware rollback | Expand phase (backward-compatible) |

### 3.4 Model Rollback for Ensemble Systems

For ensemble recommendation systems:

- Roll back individual model components independently
- Adjust ensemble weights to exclude the problematic model
- Re-weight remaining models to compensate
- Monitor ensemble performance after component rollback

---

## 4. Database Migration Rollback

### 4.1 Backward-Compatible Migration Pattern

All database migrations must be deployable with zero downtime:

**Phase 1 — Expand:**
- Add new columns/tables
- Add new indexes (non-blocking)
- Deploy code that writes to both old and new schema
- Backfill existing data

**Phase 2 — Migrate:**
- Deploy code that reads from new schema
- Verify all reads use new schema (via logging/metrics)
- Deprecate old schema columns

**Phase 3 — Contract:**
- Remove old columns/tables in a subsequent deployment
- Remove deprecated indexes

### 4.2 Rollback by Phase

| Migration Phase | Rollback Action | Risk |
|---|---|---|
| Expand (Phase 1) | Remove new columns (safe if no code uses them) | Low |
| Migrate (Phase 2) | Revert to reading old columns | Medium (data may be stale in old columns) |
| Contract (Phase 3) | **Cannot rollback** — old columns are gone | High (requires restore from backup) |

### 4.3 Feature Store Migration

Feature store migrations need special handling:

- New features: Add without breaking existing consumers
- Feature schema changes: Version features (`user_age_v2`) and support both during transition
- Feature removal: Deprecate with warning, monitor usage, remove after zero consumers

---

## 5. Rollback Communication

### 5.1 Internal Communication

| Audience | Channel | Content | Timing |
|---|---|---|---|
| On-call engineers | PagerDuty incident | Rollback initiated, impact assessment | Immediate |
| Engineering team | Slack #deployments | Rollback details, root cause status | Within 5 minutes |
| Engineering leadership | Slack DM + email | Impact summary, ETA for resolution | Within 15 minutes |
| Data science team | Slack #ml-ops | Model rollback details, metric impact | Within 15 minutes |

### 5.2 External Communication

| Audience | Channel | Content | Timing |
|---|---|---|---|
| Affected customers | Status page | "We're investigating degraded recommendations" | Within 15 minutes |
| All customers | Status page | "Issue resolved, recommendations back to normal" | After resolution |
| Partners (API consumers) | Email | Technical details, affected endpoints | Within 1 hour |
| Executive team | Email | Business impact, user impact numbers | Within 2 hours |

### 5.3 Rollback Status Page Template

```
[Investigating] We are aware of degraded recommendation quality
and are investigating. Some users may see less personalized
recommendations during this time.

[Identified] The issue has been identified as a regression in the
recommendation model deployed at [timestamp]. We are rolling back
to the previous model version.

[Monitoring] The rollback is complete. We are monitoring system
health and recommendation quality metrics.

[Resolved] The issue has been resolved. All recommendation services
are operating normally.
```

---

## 6. Post-Rollback Verification

### 6.1 Immediate Verification (0–15 minutes)

| Check | Method | Expected Result |
|---|---|---|
| Health checks | Kubernetes probes | All pods healthy |
| Error rate | Prometheus query | Returns to baseline |
| Latency | Prometheus query | Returns to baseline |
| Model serving | Direct prediction requests | Valid, expected responses |
| Feature freshness | Feature store monitoring | Features updating normally |
| User-facing validation | Manual spot checks | Recommendations look reasonable |

### 6.2 Short-Term Verification (15–60 minutes)

- Monitor recommendation quality metrics (CTR, engagement)
- Verify user-facing metrics stabilize
- Confirm no cascading effects on downstream services
- Check that rollback didn't introduce new errors
- Validate logs show no unexpected warnings

### 6.3 Root Cause Analysis (within 24 hours)

1. **Timeline reconstruction**: What happened, when, in what order
2. **Contributing factors**: What allowed the issue to reach production
3. **Detection gap**: How long was the issue live before rollback
4. **Prevention measures**: What tests/monitoring should have caught this
5. **Action items**: Specific, assigned, time-bound improvements

### 6.4 Rollback Metrics Tracking

| Metric | Target | Measurement |
|---|---|---|
| Mean time to detect (MTTD) | < 5 minutes | Time from issue start to alert firing |
| Mean time to rollback (MTTR) | < 10 minutes | Time from alert to rollback complete |
| Rollback success rate | > 99% | Percentage of rollbacks that resolve the issue |
| Root cause analysis completion | 100% within 48 hours | Post-incident review completion rate |
