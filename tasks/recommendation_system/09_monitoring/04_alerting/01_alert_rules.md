# Alerting Strategy for Recommendation Systems

## Overview

Effective alerting ensures the right people are notified about the right problems at the right
time. Poor alerting — too many alerts, unclear severity, missing context — leads to alert fatigue,
delayed response, and missed incidents. This covers Prometheus alerting rules, Alertmanager
configuration, severity levels, escalation policies, runbook automation, composite alerts,
and SLO-based alerting for recommendation systems.

## Alerting Architecture

```
Prometheus Server
├── Recording Rules (pre-computed metrics)
├── Alerting Rules (threshold and anomaly detection)
│   ├── Infrastructure alerts
│   ├── Application alerts
│   ├── ML model alerts
│   └── SLO burn rate alerts
│
└── Alertmanager (HA pair)
    ├── Deduplication
    ├── Grouping
    ├── Routing
    ├── Inhibition
    ├── Silence
    └── Notification
        ├── PagerDuty (pages)
        ├── Slack (team channels)
        ├── Email (non-urgent)
        └── Webhook (automation)
```

## Prometheus Alerting Rules

### Infrastructure Alert Rules

```yaml
groups:
  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: >
          100 * (1 - avg by(instance)
          (rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 80
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value | humanize }}% for 5+ minutes"
          runbook_url: "https://runbooks.example.com/high-cpu"

      - alert: HighMemoryUsage
        expr: >
          100 * (1 - node_memory_MemAvailable_bytes
          / node_memory_MemTotal_bytes) > 85
        for: 5m
        labels:
          severity: warning
          team: platform

      - alert: DiskSpaceLow
        expr: >
          100 * node_filesystem_avail_bytes{fstype!="tmpfs"}
          / node_filesystem_size_bytes < 15
        for: 10m
        labels:
          severity: critical
          team: platform

      - alert: PodOOMKilled
        expr: increase(kube_pod_container_status_restarts_total[15m]) > 0
        and on(pod) kube_pod_container_status_last_terminated_reason == "OOMKilled"
        labels:
          severity: critical
          team: platform
```

### Application Alert Rules

```yaml
groups:
  - name: recommendation-api
    rules:
      - alert: HighErrorRate
        expr: >
          sum(rate(http_requests_total{service="rec-api",status=~"5.."}[5m]))
          / sum(rate(http_requests_total{service="rec-api"}[5m])) > 0.01
        for: 3m
        labels:
          severity: critical
          team: recommendation
        annotations:
          summary: "Recommendation API error rate above 1%"
          description: "Current error rate: {{ $value | humanizePercentage }}"
          runbook_url: "https://runbooks.example.com/rec-api-errors"

      - alert: HighLatencyP95
        expr: >
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="rec-api"}[5m]))
            by (le)
          ) > 0.2
        for: 5m
        labels:
          severity: warning
          team: recommendation

      - alert: ModelInferenceSlow
        expr: >
          histogram_quantile(0.99,
            sum(rate(model_inference_duration_seconds_bucket[5m])) by (le)
          ) > 0.1
        for: 5m
        labels:
          severity: warning
          team: ml

      - alert: NoRecommendationsGenerated
        expr: >
          sum(rate(recommendations_generated_total[5m])) == 0
        for: 5m
        labels:
          severity: critical
          team: recommendation

      - alert: FeatureStoreHighLatency
        expr: >
          histogram_quantile(0.95,
            sum(rate(feature_store_read_duration_seconds_bucket[5m])) by (le)
          ) > 0.05
        for: 5m
        labels:
          severity: warning
          team: ml
```

### ML Model Alert Rules

```yaml
groups:
  - name: ml-models
    rules:
      - alert: ModelAccuracyDegraded
        expr: >
          model_accuracy_score < 0.35
        for: 1h
        labels:
          severity: critical
          team: ml
        annotations:
          summary: "Model accuracy below threshold"
          description: "Current accuracy: {{ $value }}"

      - alert: PredictionDistributionShift
        expr: >
          abs(population_stability_index - 1.0) > 0.2
        for: 30m
        labels:
          severity: warning
          team: ml

      - alert: FeatureDriftDetected
        expr: >
          max by(feature_name)
          (feature_kolmogorov_smirnov_statistic > 0.1)
        for: 1h
        labels:
          severity: warning
          team: ml

      - alert: ColdStartRateHigh
        expr: >
          cold_start_requests_total / total_requests_total > 0.3
        for: 30m
        labels:
          severity: warning
          team: recommendation
```

## Severity Levels

### Classification Matrix

| Severity    | Response Time  | Notification Channel | Escalation            | Examples                        |
|------------|---------------|---------------------|-----------------------|----------------------------------|
| Critical   | < 5 minutes    | PagerDuty (page)    | Immediately to IC     | Service down, data loss, SLO    |
| High       | < 30 minutes   | Slack + PagerDuty   | After 30 min if no ACK| Error rate > 5%, latency > 1s   |
| Warning    | < 4 hours      | Slack               | After 4 hours         | Degraded performance, approaching limits |
| Info       | Next business day | Email / Dashboard | None                  | Capacity planning, optimization  |

### Severity Assignment Rules

- **Critical**: Customer-facing impact, data integrity risk, security breach
- **High**: Partial customer impact, degraded but functional, approaching limits
- **Warning**: No customer impact yet, early warning, requires investigation
- **Info**: Observations, recommendations, non-urgent maintenance

## Escalation Policies

### Tiered Escalation

```
Tier 1: On-call engineer (automated notification)
  ├── ACK required within 5 minutes (Critical) / 15 minutes (High)
  ├── If no ACK: escalate to Tier 2
  └── Auto-acknowledge possible for known false positives

Tier 2: Team lead + secondary on-call
  ├── ACK required within 10 minutes
  ├── If no ACK: escalate to Tier 3
  └── Page additional team members if needed

Tier 3: Engineering manager + platform SRE
  ├── Management awareness
  ├── Cross-team coordination
  └── Customer communication if needed

Tier 4: VP Engineering + CTO
  ├── Major incident declaration
  ├── Customer communication
  └── Post-incident review coordination
```

### Escalation Rules for Recommendation Systems

| Scenario                         | Tier 1         | Tier 2          | Tier 3           |
|----------------------------------|----------------|-----------------|-------------------|
| Full service outage              | On-call ML     | ML lead + SRE   | Engineering mgr   |
| Elevated error rate              | On-call ML     | ML lead         | Team lead         |
| Slow recommendations             | On-call ML     | ML lead         | -                 |
| Model accuracy degradation       | On-call ML     | ML lead         | Product manager   |
| Feature pipeline failure         | On-call Data   | Data lead       | ML lead           |
| Infrastructure issue             | On-call SRE    | SRE lead        | Platform mgr      |

## Runbook Automation

### Runbook Structure

Every alert must have a linked runbook with:

```
Runbook: HighErrorRate (Recommendation API)
├── Alert Description
│   What: Error rate > 1% for 3+ minutes
│   Impact: Users receiving error responses instead of recommendations
│   Severity: Critical
│
├── Initial Triage (first 5 minutes)
│   1. Check Grafana dashboard: Service Health → Recommendation API
│   2. Check if recent deployment occurred (last 2 hours)
│   3. Check dependent service health (Feature Store, Model Server)
│   4. Check Slack #incidents channel for related reports
│
├── Common Causes and Remediation
│   1. Bad deployment → Rollback to previous version
│   2. Feature store down → Activate fallback feature mode
│   3. Model server overloaded → Scale model server replicas
│   4. Database connection pool exhausted → Restart with increased pool
│
├── Deep Investigation (after stabilization)
│   1. Examine error logs in Grafana Loki
│   2. Trace failing requests in Jaeger/Tempo
│   3. Check for data pipeline issues
│   4. Review recent model retraining results
│
├── Communication
│   Update Slack #incidents every 15 minutes
│   Notify product team if user impact confirmed
│
└── Post-Incident
    ├── Timeline documentation
    ├── Root cause analysis
    ├── Action items for prevention
    └── Update runbook with new findings
```

### Auto-Remediation Actions

| Alert                        | Auto-Remediation                                    |
|------------------------------|----------------------------------------------------|
| Pod OOMKilled                | Increase memory limit by 25%, restart pod           |
| Feature store timeout         | Switch to cached features, alert feature team       |
| High error rate (post-deploy)| Automatic rollback to previous version              |
| Disk space low               | Trigger log rotation, archive old data              |
| Model server overloaded      | Auto-scale model server replicas                    |
| Connection pool exhausted    | Restart service with increased pool configuration   |

## Alert Fatigue Prevention

### Anti-Patterns

1. **Alerting on symptoms AND causes**: If you alert on both high latency AND its cause (e.g., high CPU), you get double the alerts. Alert on the symptom only.
2. **Static thresholds that are too tight**: Alert fires constantly, team ignores it
3. **Alerting on transient conditions**: Conditions that resolve in < 1 minute
4. **Missing context in alert**: Engineer cannot triage without investigating logs
5. **Same issue, multiple alerts**: Feature store slow triggers 3 different alerts

### Best Practices

- **One alert per customer-impact scenario**: Group related conditions
- **Threshold with sustained duration**: `for: 5m` minimum to avoid transient spikes
- **Context-rich annotations**: Include current value, threshold, dashboard link, runbook link
- **Regular alert review**: Monthly review of alert frequency, false positive rate, and MTTA
- **Alert deprecation**: Remove alerts that haven't fired in 90 days (or adjust thresholds)

### Alert Quality Metrics

| Metric                         | Target                    | Measurement                    |
|-------------------------------|---------------------------|--------------------------------|
| Mean Time to Acknowledge (MTTA)| < 5 min (critical)       | Time from alert to first ACK   |
| Mean Time to Resolve (MTTR)    | < 30 min (critical)      | Time from alert to resolution  |
| False positive rate            | < 10%                     | Alerts that are not real issues|
| Alert volume per team per day  | < 10                      | Total alerts / team members    |
| Runbook coverage               | 100%                      | Alerts with linked runbooks    |

## Composite Alerts

### What Are Composite Alerts?

Composite alerts combine multiple simple alerts into a single higher-level alert, reducing
noise while improving signal quality.

### Examples for Recommendation Systems

```yaml
groups:
  - name: composite
    rules:
      - alert: RecommendationSystemDegraded
        expr: >
          (HighErrorRate{service="rec-api"} == 1
          and
          HighLatencyP95{service="rec-api"} == 1)
          or
          (NoRecommendationsGenerated == 1)
          or
          (ModelServerDown == 1
          and
          HighErrorRate{service="rec-api"} == 1)
        for: 3m
        labels:
          severity: critical
          team: recommendation
        annotations:
          summary: "Recommendation system is degraded"
          description: >
            Multiple conditions indicate the recommendation system
            is not functioning correctly. Investigate immediately.

      - alert: FeaturePipelineHealthy
        expr: >
          FeaturePipelineErrors == 0
          and
          FeatureFreshnessSeconds < 3600
          and
          FeatureStoreAvailability > 0.999
        labels:
          severity: info
          team: ml
        annotations:
          summary: "Feature pipeline is healthy"
```

## SLO-Based Alerting

### Error Budget Burn Rate Alerts

Instead of threshold-based alerts, use SLO-based alerting that focuses on whether the error
budget is being consumed too quickly:

```
SLO: 99.9% availability (10-minute window)
Error budget burn rate thresholds:

- 14.4x burn rate (2% budget consumed in 1 hour)
  → Page immediately

- 6x burn rate (5% budget consumed in 6 hours)
  → Page within 30 minutes

- 3x burn rate (10% budget consumed in 1 day)
  → Create ticket, investigate next business day

- 1x burn rate (budget consumed at expected rate)
  → No action, monitoring only
```

### Benefits of SLO-Based Alerting

1. **Business-aligned**: Alerts reflect actual user impact, not arbitrary thresholds
2. **Reduced noise**: Only alerts when error budget is at risk
3. **Actionable**: Clear decision framework (can we still deploy?)
4. **Scalable**: Works across teams and services with consistent methodology

## Alert Routing Configuration

### Alertmanager Route Tree

```yaml
route:
  receiver: default-slack
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    - match:
        severity: critical
      receiver: pagerduty-critical
      group_wait: 10s
      repeat_interval: 5m

    - match:
        severity: high
      receiver: slack-high-priority
      group_wait: 30s
      repeat_interval: 30m

    - match:
        severity: warning
      receiver: slack-default
      group_interval: 15m
      repeat_interval: 4h

    - match:
        team: ml
      receiver: slack-ml-team

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['service']
```

### Silence Management

- Auto-silence during planned maintenance windows
- Silence templates for common scenarios (deployments, data pipeline runs)
- Maximum silence duration: 24 hours (forces review)
- All silences logged and auditable
