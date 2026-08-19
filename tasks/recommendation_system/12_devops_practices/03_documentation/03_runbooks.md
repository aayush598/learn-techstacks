# Runbooks

## Overview

Runbooks are step-by-step operational guides that help on-call engineers diagnose and resolve incidents quickly. For recommendation systems, runbooks must address ML-specific failure modes: model degradation, data pipeline failures, feature store outages, and serving infrastructure issues. Well-written runbooks reduce mean time to resolution (MTTR), prevent knowledge silos, and ensure consistent incident response.

## Runbook Structure

### Standard Template

Every runbook should follow this structure:

```markdown
# Runbook: [Incident Type]

## Overview
Brief description of what this runbook covers, when it applies, and expected impact.

## Symptoms
Observable symptoms that indicate this issue is occurring.

## Severity
SEV1/SEV2/SEV3/SEV4 classification.

## Diagnosis
Step-by-step diagnostic procedure to identify root cause.

## Remediation
Step-by-step fix procedures.

## Verification
Steps to verify the fix worked.

## Prevention
How to prevent this issue from recurring.

## Escalation
When and how to escalate.

## Appendix
Reference links, related runbooks, historical incidents.
```

### Component Mapping

| System Component | Common Failures | Runbook Category |
|-----------------|----------------|-----------------|
| **Model serving** | High latency, errors, OOM | Serving infrastructure |
| **Feature store** | Feature staleness, schema errors | Data pipeline |
| **Training pipeline** | Training failures, quality degradation | Model pipeline |
| **Data ingestion** | Pipeline delays, data quality issues | Data infrastructure |
| **API gateway** | Rate limiting, authentication failures | Infrastructure |
| **Monitoring** | Alert fatigue, missing alerts | Observability |

## Runbook Types

### Incident Runbooks

Used during active incidents to diagnose and resolve problems quickly.

| Incident Type | Severity | Typical MTTR | Impact |
|--------------|----------|-------------|--------|
| Model serving down | SEV1 | 15–30 min | No recommendations served |
| High latency (>500ms p99) | SEV2 | 30–60 min | Degraded user experience |
| Model quality degradation | SEV2 | 1–4 hours | Reduced click-through, revenue |
| Data pipeline delay | SEV3 | 2–8 hours | Stale features, model drift |
| Training failure | SEV3 | 4–24 hours | Delayed model updates |
| Non-critical alert | SEV4 | Next business day | Minor issue |

### Operational Runbooks

Used for routine operational tasks.

| Task | Frequency | Description |
|------|----------|-------------|
| **Model retraining** | Weekly/Monthly | Trigger and validate model retraining |
| **Data pipeline monitoring** | Daily | Check pipeline health and data quality |
| **Capacity planning** | Monthly | Review resource utilization and scale |
| **Dependency updates** | Quarterly | Update libraries and infrastructure |
| **Model promotion** | As needed | Promote model from staging to production |
| **A/B test setup** | As needed | Configure new A/B test experiments |

### Maintenance Runbooks

Used for scheduled maintenance tasks.

| Task | Frequency | Description |
|------|----------|-------------|
| **Certificate rotation** | Quarterly | Rotate TLS certificates |
| **Secret rotation** | Quarterly | Rotate API keys, database passwords |
| **Infrastructure upgrades** | Semi-annual | Upgrade Kubernetes, Python, etc. |
| **Data migration** | As needed | Migrate data schemas or storage |
| **Disaster recovery test** | Semi-annual | Test backup and restore procedures |

## Runbook Examples

### Incident Runbook: Model Serving High Latency

```markdown
# Runbook: Model Serving High Latency

## Overview
This runbook addresses situations where model serving latency exceeds
normal thresholds (p99 > 200ms, p50 > 50ms).

## Symptoms
- Serving latency p99 > 200ms (alert: recs-serving-latency-p99)
- User complaints about slow recommendations
- Increased timeout rate in API gateway logs
- Elevated error rate in serving pods

## Severity: SEV2
Degraded user experience but service still functional.

## Diagnosis

### Step 1: Check current latency
```bash
# Grafana dashboard: Model Serving - Latency
# URL: https://grafana.company.com/d/recs-serving-latency
```

### Step 2: Check for resource constraints
```bash
kubectl top pods -n recs-serving
# Check CPU, memory usage
# If CPU > 80% or memory > 80%, resource constraint likely
```

### Step 3: Check for traffic spike
```bash
# Check request rate in Prometheus
# URL: https://prometheus.company.com/graph?query=rate(recs_requests_total[5m])
# Compare current rate to baseline
```

### Step 4: Check model file integrity
```bash
# Verify model file hash matches registry
md5sum /models/production/model.pkl
# Compare with: cat /models/production/model.pkl.dvc
```

### Step 5: Check feature store connectivity
```bash
# Test feature store connection
curl -s https://feature-store.company.com/health
# Check feature retrieval latency
curl -w "@curl-format.txt" -o /dev/null -s \
  https://feature-store.company.com/features/user/12345
```

## Remediation

### If resource constrained:
```bash
# Scale up serving pods
kubectl scale deployment recs-serving --replicas=10 -n recs-serving
```

### If traffic spike:
```bash
# Enable rate limiting
kubectl apply -f rate-limit-config.yaml -n recs-serving
```

### If model file corrupted:
```bash
# Reload model from registry
dvc pull models/production/model.pkl
# Restart serving pods
kubectl rollout restart deployment recs-serving -n recs-serving
```

### If feature store degraded:
```bash
# Switch to cached features
kubectl set env deployment/recs-serving FEATURE_CACHE_ENABLED=true -n recs-serving
```

## Verification
1. Check latency returns to normal (p99 < 200ms)
2. Check error rate returns to baseline
3. Check user-facing metrics (CTR, conversion) stabilize
4. Monitor for 30 minutes after fix

## Prevention
- Set up auto-scaling based on latency
- Implement feature caching for degradation scenarios
- Add model file integrity checks on startup
- Regular load testing to validate capacity
```

## Runbook Automation

### Automated Remediation Scripts

```bash
#!/bin/bash
# auto-fix-high-latency.sh

ALERT_NAME=$1
POD_COUNT=$(kubectl get pods -n recs-serving --no-headers | wc -l)
CPU_USAGE=$(kubectl top pods -n recs-serving --no-headers | awk '{print $2}' | sort -r | head -1)

if [ "$ALERT_NAME" == "high-latency" ]; then
    if [ $CPU_USAGE -gt 80 ]; then
        echo "CPU constraint detected. Scaling up..."
        CURRENT=$(kubectl get deployment recs-serving -n recs-serving -o jsonpath='{.spec.replicas}')
        NEW=$((CURRENT + 3))
        kubectl scale deployment recs-serving --replicas=$NEW -n recs-serving
        echo "Scaled from $CURRENT to $NEW pods"
    fi
fi
```

### Automation Levels

| Level | Description | Example |
|-------|-------------|---------|
| **L0: Manual** | Human performs all steps | Complex investigation |
| **L1: Assisted** | Script guides human through steps | Diagnosis scripts |
| **L2: Automated** | Script performs fix, human approves | Auto-scaling |
| **L3: Auto-remediation** | Script performs fix automatically | Restart on crash |
| **L4: Self-healing** | System detects and fixes without human | Auto-scaling, circuit breakers |

## Runbook Testing

### Testing Methodology

| Test Type | Description | Frequency |
|-----------|-------------|----------|
| **Tabletop exercise** | Walk through runbook verbally with team | Monthly |
| **Chaos engineering** | Inject actual failures and follow runbook | Quarterly |
| **Drill** | Simulate incident during business hours | Monthly |
| **Surprise test** | Inject failure without warning | Semi-annually |
| **New hire test** | Have new team member follow runbook | On onboarding |

### Runbook Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **MTTR with runbook** | < 30 min for SEV1 | Time from alert to resolution |
| **MTTR without runbook** | Compare to with runbook | Baseline measurement |
| **Accuracy** | > 95% of steps correct | Chaos testing results |
| **Completeness** | No missing steps | Post-incident review |
| **Freshness** | Updated within 30 days of system change | Last update date |

## Runbook Maintenance

### When to Update Runbooks

| Trigger | Action |
|---------|--------|
| New deployment | Update serving runbooks |
| Schema change | Update data pipeline runbooks |
| New dependency | Update infrastructure runbooks |
| Post-incident | Update based on lessons learned |
| Quarterly review | Full runbook audit |
| Team change | Update escalation contacts |

### Runbook Review Process

```
1. Author creates/updates runbook
2. Peer review by another on-call engineer
3. Tabletop exercise to validate steps
4. Chaos test to verify automation
5. Merge to main branch
6. Notify on-call team of changes
```

## Runbook Tools

### Tool Comparison

| Tool | Features | Best For |
|------|----------|---------|
| **PagerDuty** | Incident management, escalation, runbooks | Enterprise on-call |
| **OpsGenie** | Alert management, runbooks, postmortems | Mid-size teams |
| **Rootly** | Incident management, status pages, runbooks | Modern teams |
| **GitHub Wiki** | Simple runbook storage | Small teams |
| **Notion** | Collaborative documentation | Documentation-heavy teams |
| **Confluence** | Enterprise documentation | Large organizations |

### Integration Architecture

```
Alert (Prometheus/Grafana)
    ↓
Alert Manager (PagerDuty/OpsGenie)
    ↓
On-Call Engineer notified (Phone/Slack)
    ↓
Runbook linked in alert
    ↓
Engineer follows runbook steps
    ↓
Incident resolved
    ↓
Postmortem created
    ↓
Runbook updated with lessons learned
```
