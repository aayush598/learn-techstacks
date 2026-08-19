# SLO/SLI Design for Recommendation Systems

## 1. SLI (Service Level Indicator) Definitions

### 1.1 Availability SLIs
- **Successful Request Ratio**: Percentage of requests returning 2xx responses
- **Healthy Endpoint Ratio**: Percentage of endpoints passing health checks
- **Model Availability**: Percentage of time model is serving predictions
- **Feature Store Availability**: Percentage of feature requests successful

### 1.2 Latency SLIs
- **Request Latency**: Time from request receipt to response delivery
- **Model Inference Latency**: Time for model to produce predictions
- **Feature Retrieval Latency**: Time to fetch features from store
- **End-to-End Latency**: Total recommendation generation time

### 1.3 Quality SLIs
- **Recommendation Relevance**: Percentage of recommendations meeting quality threshold
- **Prediction Accuracy**: Alignment between predicted and actual outcomes
- **Feature Freshness**: Percentage of features within freshness SLA
- **Content Availability**: Percentage of recommended items actually available

---

## 2. SLO (Service Level Objective) Targets

### 2.1 Availability SLOs
| Service | SLO Target | Error Budget (30 days) |
|---|---|---|
| API Gateway | 99.95% | 21.6 minutes |
| Candidate Generation | 99.9% | 43.2 minutes |
| Ranking Service | 99.9% | 43.2 minutes |
| Feature Store | 99.95% | 21.6 minutes |
| Model Serving | 99.9% | 43.2 minutes |

### 2.2 Latency SLOs
| Service | P50 Target | P95 Target | P99 Target |
|---|---|---|---|
| API Gateway | <10ms | <50ms | <100ms |
| Candidate Generation | <20ms | <50ms | <100ms |
| Ranking Service | <30ms | <80ms | <150ms |
| Feature Store | <3ms | <10ms | <20ms |
| End-to-End | <100ms | <200ms | <300ms |

### 2.3 Quality SLOs
- **CTR**: Maintain > baseline CTR for active experiments
- **Coverage**: Recommend >80% of catalog monthly
- **Diversity**: Average intra-list diversity >0.7
- **Freshness**: >95% of recommendations from last 7 days

---

## 3. Error Budget

### 3.1 Error Budget Calculation
```
Error Budget = (1 - SLO Target) × Time Period

Example:
  SLO: 99.9% availability
  Time Period: 30 days = 43,200 minutes
  Error Budget: 0.1% × 43,200 = 43.2 minutes of downtime
```

### 3.2 Error Budget Policies
- **Budget Remaining >50%**: Normal development velocity; deploy freely
- **Budget Remaining 25-50%**: Caution; additional testing required
- **Budget Remaining 10-25%**: Freeze non-critical changes; focus on reliability
- **Budget Remaining <10%**: Code freeze; only critical fixes; postmortem required
- **Budget Exhausted**: Full feature freeze; mandatory reliability sprint

### 3.3 Burn Rate
```
Burn Rate = Actual Error Rate / SLO Error Rate

Example:
  SLO: 99.9% (0.1% error rate allowed)
  Actual: 0.5% error rate
  Burn Rate: 5x (will exhaust budget in 1/5 of time period)
```

### 3.4 Multi-Burn-Rate Alerting
- **Fast Burn**: 14.4x burn rate for 1 hour → Page immediately
- **Slow Burn**: 3x burn rate for 6 hours → Ticket for investigation
- **Critical**: 1x sustained burn rate → Monitor closely

---

## 4. SLO-Based Alerting

### 4.1 Alert Rules
```yaml
# Fast burn alert (immediate page)
- alert: HighErrorBudgetBurn
  expr: |
    sum(rate(recommendation_errors_total[1h]))
    / sum(rate(recommendation_requests_total[1h]))
    > 14.4 * 0.001
  for: 1h
  labels:
    severity: critical

# Slow burn alert (create ticket)
- alert: SlowErrorBudgetBurn
  expr: |
    sum(rate(recommendation_errors_total[6h]))
    / sum(rate(recommendation_requests_total[6h]))
    > 3 * 0.001
  for: 6h
  labels:
    severity: warning
```

### 4.2 Alert Routing
- **Critical**: Page on-call immediately
- **Warning**: Create ticket for next business day
- **Info**: Log for weekly review

---

## 5. SLO Reporting

### 5.1 SLO Dashboard
- Current SLO compliance status (green/yellow/red)
- Error budget remaining (minutes/percentage)
- Burn rate trend over last 7/30 days
- SLI values over time with SLO targets as thresholds
- Per-service SLO breakdown

### 5.2 SLO Review Process
- **Weekly**: ML team reviews SLO status and error budget
- **Monthly**: Leadership reviews SLO trends and reliability posture
- **Quarterly**: SLO target review and adjustment
- **Post-Incident**: SLO impact assessment and budget review

---

## 6. Implementation with Open Source

### 6.1 Prometheus + Grafana
- SLI metrics collected via Prometheus exporters
- SLO calculations in Prometheus recording rules
- Error budget dashboards in Grafana
- Alerting via Alertmanager

### 6.2 pyrra (SLO Management)
- Kubernetes-native SLO management
- Declarative SLO definitions
- Automatic error budget calculation
- Integration with Prometheus
