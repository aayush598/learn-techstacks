# Service Level Indicators (SLIs)

## Overview

Service Level Indicators (SLIs) establishes the monitoring, observability, and alerting framework for the 03 Sla Monitoring Reporting chapter. This section covers metrics collection, dashboard design, alert configuration, and operational runbooks.

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Application                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Metrics  │  │  Logs    │  │  Traces  │          │
│  │ (prom-  │  │ (pino)   │  │ (OpenTel)│          │
│  │ client) │  │          │  │          │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │             │                 │
└───────┼─────────────┼─────────────┼─────────────────┘
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌────────┐ ┌──────────────┐
│  Prometheus  │ │  Loki  │ │    Tempo     │
│  (Metrics)   │ │ (Logs) │ │  (Traces)    │
└──────┬───────┘ └───┬────┘ └──────┬───────┘
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
            ┌────────────────┐
            │    Grafana     │
            │  (Dashboards)  │
            └───────┬────────┘
                    │
                    ▼
            ┌────────────────┐
            │  AlertManager  │──► PagerDuty / Slack / Email
            └────────────────┘
```

## Key Metrics

```typescript
// Prometheus metrics definition
const metrics = {
  requestTotal: new Counter({
    name: 'service_requests_total',
    help: 'Total number of requests',
    labelNames: ['method', 'path', 'status'],
  }),

  requestDuration: new Histogram({
    name: 'service_request_duration_seconds',
    help: 'Request duration in seconds',
    labelNames: ['method', 'path'],
    buckets: [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5],
  }),

  activeConnections: new Gauge({
    name: 'service_active_connections',
    help: 'Number of active connections',
  }),

  errorsTotal: new Counter({
    name: 'service_errors_total',
    help: 'Total number of errors',
    labelNames: ['type', 'code'],
  }),

  cacheHitRatio: new Gauge({
    name: 'service_cache_hit_ratio',
    help: 'Cache hit ratio (0-1)',
  }),
};
```

## Alert Rules

```yaml
# Prometheus alert rules
groups:
  - name: service_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          rate(service_errors_total[5m]) / rate(service_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1% for 5 minutes"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(service_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p95 latency above 500ms for 5 minutes"

      - alert: ServiceDown
        expr: |
          up{job="voice-agent-service"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
```

## Dashboard Structure

The Grafana dashboard is organized into these sections:

1. **Overview**: Request rate, error rate, average latency
2. **Performance**: Latency percentiles (p50, p95, p99)
3. **Resources**: CPU, memory, active connections
4. **Dependencies**: Database, cache, external service health
5. **Business**: Key business metrics and SLIs

## Open Source Tools

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Dashboard visualization
- **Loki**: Log aggregation and querying
- **Tempo**: Distributed tracing
- **OpenTelemetry**: Instrumentation framework
- **prom-client**: Node.js Prometheus client
- **Pino**: Structured logging

## Production Runbook

### Incident Response Flow

1. **Alert fires** → On-call engineer acknowledges within 5 minutes
2. **Assessment** → Determine severity (SEV1-SEV4)
3. **Mitigation** → Apply known fix or rollback
4. **Resolution** → Confirm service restored
5. **Postmortem** → Document root cause and prevention

### Common Alerts

| Alert | Possible Cause | Immediate Action |
|-------|---------------|------------------|
| High error rate | Code bug, dependency failure | Check recent deploys, rollback if needed |
| High latency | Resource exhaustion, slow queries | Scale horizontally, identify slow queries |
| Service down | Crash, OOM, config error | Check logs, restart, rollback config |
| Low cache hit rate | Cache eviction, cold start | Warm cache, adjust TTL |

## Summary

The monitoring framework for Service Level Indicators (SLIs) provides comprehensive observability into the platform's operations. With proper metrics, alerting, and dashboards, the team can maintain high availability and quickly respond to incidents.
