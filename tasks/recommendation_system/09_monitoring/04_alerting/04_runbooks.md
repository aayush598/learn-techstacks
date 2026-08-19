# Runbooks for Recommendation Systems

## 1. Overview

Runbooks are step-by-step guides for diagnosing and resolving common operational issues. In recommendation systems, runbooks ensure consistent incident response, reduce MTTR, and enable junior engineers to handle incidents that would otherwise require senior escalation. A well-maintained runbook is the difference between a 15-minute fix and a 2-hour war room.

### 1.1 Why Runbooks Matter

- **Consistency**: Every engineer follows the same proven steps
- **Speed**: No need to re-investigate known issues from scratch
- **Knowledge preservation**: Institutional knowledge is documented, not tribal
- **Delegation**: Junior engineers can handle incidents with runbook guidance
- **Compliance**: Some regulations require documented operational procedures

### 1.2 Runbook Quality Criteria

| Criterion | Description |
|---|---|
| Actionable | Steps are clear and can be executed immediately |
| Specific | Exact commands, URLs, and thresholds (no vague instructions) |
| Tested | Steps have been verified to work in production-like environment |
| Current | Updated within 30 days of any system change |
| Accessible | Easy to find during an incident (not buried in wiki) |
| Complete | Covers diagnosis, mitigation, and recovery |

---

## 2. Runbook Structure

### 2.1 Standard Runbook Template

```markdown
# Runbook: [Issue Title]

## Metadata
- **Severity**: [P0/P1/P2/P3]
- **Service**: [Affected service]
- **Symptoms**: [How the issue manifests]
- **Impact**: [User/business impact]
- **Last Updated**: [Date]
- **Owner**: [Team/person responsible]

## Detection
### Alert Information
- Alert name: [Alert name]
- Alert query: [Prometheus/monitoring query]
- Threshold: [Threshold that triggered alert]

### Symptoms to Look For
- [Symptom 1]
- [Symptom 2]
- [Symptom 3]

## Diagnosis Steps
1. [Step 1 with exact commands]
2. [Step 2 with exact commands]
3. [Decision point: if X then Y, else Z]

## Remediation Steps
### Option A: Quick Mitigation
1. [Step 1]
2. [Step 2]

### Option B: Root Cause Fix
1. [Step 1]
2. [Step 2]

## Verification
- [How to verify the fix worked]
- [Metrics to monitor]

## Escalation
- If not resolved in [time]: escalate to [team/person]
- Contact: [Contact information]

## Related Incidents
- [INC-YYYY-MMDD-NNN]: [Brief description]

## Changelog
- [Date]: [What changed]
```

---

## 3. Diagnosis Steps

### 3.1 Systematic Diagnosis Framework

```
Step 1: Confirm the issue
  - Is this a real incident or a false alarm?
  - Check dashboards, not just alerts

Step 2: Assess scope
  - How many users are affected?
  - Is it all traffic or specific segments?
  - Is it all regions or specific regions?

Step 3: Identify the failing component
  - Which service is returning errors or slow?
  - Check upstream and downstream dependencies

Step 4: Check recent changes
  - Any recent deployments?
  - Any configuration changes?
  - Any traffic pattern changes?

Step 5: Check resource utilization
  - CPU, memory, GPU, disk, network
  - Any resource exhaustion?

Step 6: Check dependencies
  - Feature store health
  - Model server health
  - Cache hit rates
  - Database connectivity
```

### 3.2 Diagnostic Commands

**Quick health check:**
```bash
# Check service health endpoint
curl -s https://rec-service.internal/health | jq .

# Check recent deployment
kubectl rollout status deployment/rec-ranking -n recommendation

# Check pod status
kubectl get pods -n recommendation -l app=rec-ranking

# Check recent events
kubectl get events -n recommendation --sort-by='.lastTimestamp' | tail -20
```

**Latency investigation:**
```bash
# Check current P99 latency
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,rate(rec_request_duration_seconds_bucket[5m]))" | jq .

# Compare with 1 hour ago
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,rate(rec_request_duration_seconds_bucket[5m]))/histogram_quantile(0.99,rate(rec_request_duration_seconds_bucket[5m] offset 1h))" | jq .
```

**Error investigation:**
```bash
# Check error rate by type
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(rec_errors_total[5m]))by(error_type)" | jq .

# Check recent error logs
kubectl logs -n recommendation -l app=rec-ranking --tail=100 | grep -i error
```

---

## 4. Common Runbook Types

### 4.1 High Latency Runbook

**Symptoms:** P99 latency exceeds SLO threshold for 5+ minutes.

**Diagnosis:**
1. Check which stage is slow: `histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket{stage="*"}[5m]))`
2. Check if slow for all users or specific segments
3. Check if latency spike correlates with deployment
4. Check resource utilization on affected services
5. Check downstream dependency latency (feature store, model server)

**Common causes and fixes:**

| Cause | Diagnosis | Fix |
|---|---|---|
| Model server cold start | High latency after deployment | Wait for warm-up or rollback |
| Feature store latency | Feature computation stage slow | Check feature store, add caching |
| Cache miss storm | Low cache hit rate | Increase cache size, check eviction |
| GC pauses | Periodic latency spikes | Tune JVM GC settings |
| Network congestion | Cross-AZ traffic increase | Check network metrics, optimize routing |
| Traffic spike | Request rate above capacity | Scale horizontally |

**Quick mitigation:**
```bash
# Scale up ranking service
kubectl scale deployment rec-ranking --replicas=12 -n recommendation

# Increase cache TTL temporarily
kubectl set env deployment/rec-ranking CACHE_TTL=600 -n recommendation

# Switch to fallback model (lighter weight)
kubectl set env deployment/rec-ranking MODEL_VERSION=fallback-v1 -n recommendation
```

### 4.2 High Error Rate Runbook

**Symptoms:** Error rate exceeds threshold (typically >1% for warning, >5% for critical).

**Diagnosis:**
1. Check error rate by service: `sum(rate(rec_errors_total[5m]))by(service)`
2. Check error types: `sum(rate(rec_errors_total[5m]))by(error_type)`
3. Check if errors correlate with deployment
4. Check for upstream/downstream failures
5. Check recent logs for error patterns

**Common causes and fixes:**

| Cause | Diagnosis | Fix |
|---|---|---|
| Model server crash | Pods in CrashLoopBackOff | Restart pods, check OOM |
| Feature store down | Feature service errors | Check feature store, enable fallback |
| Index corruption | Candidate retrieval errors | Rebuild index, switch to backup |
| Configuration error | Errors after config change | Rollback config |
| Resource exhaustion | OOMKilled or CPU throttling | Increase resource limits |

**Quick mitigation:**
```bash
# Restart failing pods
kubectl rollout restart deployment/rec-ranking -n recommendation

# Rollback to previous version
kubectl rollout undo deployment/rec-ranking -n recommendation

# Enable circuit breaker
kubectl set env deployment/rec-ranking CIRCUIT_BREAKER_ENABLED=true -n recommendation
```

### 4.3 Resource Exhaustion Runbook

**Symptoms:** CPU >90%, memory >90%, GPU >95%, or disk >85% utilization.

**Diagnosis:**
1. Identify which resource is exhausted
2. Check if exhaustion is gradual (leak) or sudden (spike)
3. Check which service/pod is consuming the most
4. Check if resource limits are appropriate
5. Check for memory leaks or CPU-intensive operations

**Common causes and fixes:**

| Resource | Cause | Fix |
|---|---|---|
| CPU | Traffic spike, inefficient query | Scale horizontally, optimize query |
| Memory | Memory leak, large batch size | Restart, fix leak, reduce batch size |
| GPU | Model too large, batch too large | Optimize model, reduce batch size |
| Disk | Log accumulation, index growth | Clean up, expand disk, archive |
| Network | Large payloads, many connections | Compress, connection pooling |

**Quick mitigation:**
```bash
# Check resource usage
kubectl top pods -n recommendation --sort-by=cpu
kubectl top pods -n recommendation --sort-by=memory

# Scale horizontally
kubectl scale deployment rec-ranking --replicas=16 -n recommendation

# Increase resource limits
kubectl patch deployment rec-ranking -n recommendation -p '{"spec":{"template":{"spec":{"containers":[{"name":"rec-ranking","resources":{"limits":{"memory":"4Gi","cpu":"2000m"}}}]}}}}'
```

### 4.4 Feature Pipeline Failure Runbook

**Symptoms:** Feature freshness exceeds threshold, feature completeness drops.

**Diagnosis:**
1. Check feature freshness: `rec_feature_age_seconds{feature_group="*"}`
2. Check Kafka consumer lag for feature events
3. Check feature computation job status
4. Check feature store connectivity
5. Check for schema changes in upstream events

**Common causes and fixes:**

| Cause | Diagnosis | Fix |
|---|---|---|
| Kafka lag | Consumer lag increasing | Scale consumers, check broker health |
| Job failure | Spark/Flink job failed | Restart job, check data quality |
| Schema change | Deserialization errors | Update schema, deploy compatible version |
| Feature store down | Feature store connection errors | Check feature store, enable cache fallback |
| Data quality issue | Feature validation errors | Fix upstream data, adjust validation rules |

**Quick mitigation:**
```bash
# Check Kafka consumer lag
kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group feature-consumer

# Restart feature computation job
spark-submit --kill feature-computation-job --master yarn

# Use cached features temporarily
kubectl set env deployment/rec-ranking FEATURE_CACHE_MODE=forced -n recommendation
```

### 4.5 Model Serving Failure Runbook

**Symptoms:** Model inference errors, model loading failures, GPU errors.

**Diagnosis:**
1. Check model server health: `rec_model_server_health{model="*"}`
2. Check GPU utilization: `nvidia_gpu_utilization_percent`
3. Check model loading status
4. Check for OOM errors on GPU
5. Check model file integrity

**Common causes and fixes:**

| Cause | Diagnosis | Fix |
|---|---|---|
| Model OOM | GPU memory exceeded | Reduce batch size, use smaller model |
| Model file corrupt | Checksum mismatch | Re-download model, use backup |
| GPU driver error | dmesg shows GPU errors | Restart GPU, update drivers |
| Model version mismatch | Feature dimension mismatch | Rollback model, fix feature pipeline |
| Cold start | Model not loaded in memory | Pre-load model, increase replicas |

**Quick mitigation:**
```bash
# Check GPU status
nvidia-smi

# Restart model server
kubectl rollout restart deployment/model-server -n recommendation

# Switch to CPU fallback
kubectl set env deployment/rec-ranking MODEL_DEVICE=cpu -n recommendation

# Load previous model version
kubectl set env deployment/rec-ranking MODEL_VERSION=previous-version -n recommendation
```

---

## 5. Runbook Automation

### 5.1 Automated Remediation

Some runbook steps can be automated for faster response:

```yaml
auto_remediation_rules:
  - name: "Auto-scale on high CPU"
    trigger: "cpu_utilization > 85% for 5m"
    action: "scale_deployment(service, replicas=current+2)"
    max_scale: 20
    cooldown: 10m

  - name: "Auto-restart on CrashLoopBackOff"
    trigger: "pod_status=CrashLoopBackOff for 5m"
    action: "restart_pods(label_selector)"
    max_restarts: 3
    cooldown: 15m

  - name: "Auto-rollback on error spike"
    trigger: "error_rate > 5% for 3m after_deploy"
    action: "rollback_deployment(service)"
    cooldown: 30m
```

### 5.2 Runbook Automation Tools

| Tool | Purpose | Integration |
|---|---|---|
| Rundeck | Runbook automation platform | SSH, API, script execution |
| Ansible | Configuration management | Playbook execution |
| PagerDuty Automation | Automated response actions | Alert-triggered actions |
| Kubernetes CronJobs | Scheduled maintenance | Automated cleanup, reports |
| Custom scripts | One-off automations | Triggered by alerting system |

### 5.3 Automation Safety

- **Require approval** for destructive actions (rollback, scale-down, data deletion)
- **Implement circuit breakers** for automated actions (max actions per hour)
- **Log all automated actions** for audit trail
- **Test automation** in staging environment before production
- **Set blast radius limits** (e.g., max 50% scale-up per automation)

---

## 6. Maintenance Procedures

### 6.1 Scheduled Maintenance Runbooks

| Procedure | Frequency | Duration | Impact |
|---|---|---|---|
| Model retraining and deployment | Weekly | 30 min | Brief latency spike |
| Index rebuild | Monthly | 2 hours | Reduced capacity during rebuild |
| Feature pipeline restart | Quarterly | 5 min | Feature staleness during restart |
| Configuration review | Monthly | 1 hour | No impact |
| Runbook review and update | Monthly | 2 hours | No impact |

### 6.2 Model Deployment Runbook

```
Pre-deployment:
1. Verify new model passes offline evaluation
2. Deploy to staging and run smoke tests
3. Compare latency benchmarks with current model
4. Review feature compatibility
5. Check model size and memory requirements

Deployment:
1. Deploy to canary (5% of traffic)
2. Monitor for 15 minutes:
   - Error rate
   - Latency P50/P95/P99
   - Prediction distribution
   - Feature completeness
3. If healthy, increase to 25%
4. Monitor for 30 minutes
5. If healthy, increase to 50%
6. Monitor for 1 hour
7. If healthy, complete rollout to 100%

Rollback triggers:
- Error rate > 1% (vs. baseline)
- P99 latency > 150% of baseline
- Prediction distribution shift > 10%
- Any user-facing error reported

Post-deployment:
1. Update model version in monitoring dashboards
2. Verify A/B test configuration
3. Monitor for 24 hours
4. Update runbook with any new observations
```

### 6.3 Feature Pipeline Maintenance

```
Weekly:
1. Review feature freshness metrics
2. Check feature completeness trends
3. Review default value usage rates
4. Verify feature store connectivity

Monthly:
1. Review feature importance rankings
2. Check for unused features (candidates for removal)
3. Review feature computation costs
4. Update feature documentation

Quarterly:
1. Review feature schema compatibility
2. Test feature pipeline disaster recovery
3. Review feature store capacity
4. Plan feature pipeline upgrades
```

---

## 7. Runbook Maintenance

### 7.1 Runbook Review Cadence

| Trigger | Action |
|---|---|
| After every P0/P1 incident | Review and update affected runbooks |
| After every deployment | Check if runbooks need updates |
| Monthly | Full runbook review by team |
| Quarterly | Cross-team runbook audit |
| When on-call engineer changes | New engineer reviews all runbooks |

### 7.2 Runbook Quality Metrics

| Metric | Target | Measurement |
|---|---|---|
| Runbook coverage | >90% of alerts have runbooks | Alerts with runbooks / Total alerts |
| Runbook accuracy | >95% of steps are correct | Verified steps / Total steps |
| Runbook freshness | Updated within 30 days | Runbooks updated on time / Total |
| Runbook usage | Used in >50% of incidents | Incidents using runbooks / Total |
| MTTR with runbook | <50% of MTTR without | Compare resolution times |

### 7.3 Runbook Accessibility

Ensure runbooks are easy to find during incidents:

- **Primary location**: Dedicated runbook repository (GitHub, GitLab)
- **Secondary location**: Wiki or documentation site
- **Alert integration**: Link runbook URL in every alert definition
- **PagerDuty integration**: Include runbook link in PagerDuty service description
- **Slack bot**: `/runbook ranking-high-latency` to fetch runbook on demand

---

## 8. Key Takeaways

1. **Write runbooks for every alert** — if it's worth alerting on, it's worth documenting
2. **Use the standard template** — consistent structure enables faster navigation
3. **Include exact commands** — no vague instructions during an incident
4. **Test runbooks regularly** — verify steps work in staging before production
5. **Automate where safe** — auto-scaling and auto-rollback reduce MTTR
6. **Update runbooks after every incident** — postmortem action items should update runbooks
7. **Make runbooks accessible** — link from alerts, integrate with Slack and PagerDuty
8. **Review runbooks monthly** — stale runbooks are worse than no runbooks
9. **Track runbook usage** — measure MTTR with and without runbooks
10. **Celebrate runbook contributions** — recognize engineers who write and maintain runbooks
