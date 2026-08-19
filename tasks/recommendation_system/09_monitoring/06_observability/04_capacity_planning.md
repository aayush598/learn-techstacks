# Capacity Planning for Recommendation Systems

## 1. Overview

Capacity planning ensures that recommendation system infrastructure can handle current and projected demand while maintaining SLO compliance and cost efficiency. For recommendation systems, capacity planning is uniquely complex due to GPU requirements for model serving, variable traffic patterns, and the need to balance performance with cost.

### 1.1 Why Capacity Planning Matters

- **SLO compliance**: Under-provisioned infrastructure causes latency and availability issues
- **Cost optimization**: Over-provisioned infrastructure wastes money
- **Growth readiness**: Recommendation systems must scale with user growth
- **Seasonal preparedness**: Traffic spikes (holidays, events) require提前 preparation
- **Model evolution**: Larger models require more GPU resources

### 1.2 Capacity Planning Goals

| Goal | Metric | Target |
|---|---|---|
| SLO compliance | Uptime and latency | Meet all SLO targets |
| Cost efficiency | Cost per recommendation | Decreasing or stable trend |
| Growth readiness | Headroom for growth | 30-50% headroom above current peak |
| Scaling speed | Time to scale | <5 minutes for horizontal, <1 hour for vertical |
| Forecast accuracy | Predicted vs. actual usage | Within 20% |

---

## 2. Resource Utilization Forecasting

### 2.1 Key Metrics to Forecast

| Resource | Current Usage | Growth Rate | Forecast Method |
|---|---|---|---|
| CPU | 65% average | 5% monthly | Linear regression on 90-day trend |
| Memory | 72% average | 3% monthly | Linear regression on 90-day trend |
| GPU | 78% average | 8% monthly | Linear + model size growth |
| Network | 40% bandwidth | 10% monthly | Linear regression on 90-day trend |
| Storage | 60% capacity | 15% monthly | Linear regression on 90-day trend |

### 2.2 Forecasting Methods

**Linear regression:**
```
Projected usage = current_usage + (growth_rate × months_ahead)

Where growth_rate is calculated from:
  - 90-day trend (short-term forecast)
  - 180-day trend (medium-term forecast)
  - 365-day trend (long-term forecast, accounts for seasonality)
```

**Seasonal adjustment:**
```
Adjusted forecast = trend_forecast × seasonal_index

Where seasonal_index = (average_usage_this_month / average_usage_this_month_last_year)
```

**Traffic spike projection:**
```
Peak capacity = average_capacity × peak_multiplier

Where peak_multiplier varies by event:
  - Normal day: 1.0x
  - Weekend: 1.2x
  - Holiday: 2-3x
  - Viral event: 5-10x
```

### 2.3 Forecasting Dashboard

| Panel | Metric | Visualization |
|---|---|---|
| CPU utilization trend | 90-day trend with forecast | Time series with projection band |
| Memory utilization trend | 90-day trend with forecast | Time series with projection band |
| GPU utilization trend | 90-day trend with forecast | Time series with projection band |
| Request rate trend | 90-day trend with forecast | Time series with projection band |
| Storage growth trend | 90-day trend with forecast | Time series with projection band |
| Capacity exhaustion date | When resource hits 80% | Single stat with countdown |

---

## 3. Growth Projection

### 3.1 User Growth Projection

```
Current MAU: 100M
Growth rate: 5% monthly
Projected MAU (6 months): 100M × (1.05)^6 = 134M
Projected MAU (12 months): 100M × (1.05)^12 = 180M
```

### 3.2 Traffic Growth Projection

```
Current daily requests: 500M
Growth rate: 5% monthly (from user growth) + 3% monthly (from feature adoption)
Combined growth rate: 8% monthly
Projected daily requests (6 months): 500M × (1.08)^6 = 793M
Projected daily requests (12 months): 500M × (1.08)^12 = 1.26B
```

### 3.3 Model Complexity Growth

```
Current model: 100M parameters, 20ms inference
Projected model (6 months): 150M parameters, 30ms inference (50% larger)
Projected model (12 months): 250M parameters, 50ms inference (150% larger)

GPU requirement growth:
  Current: T4 GPUs (16GB memory)
  6 months: A10G GPUs (24GB memory) for larger models
  12 months: A100 GPUs (40GB memory) for largest models
```

### 3.4 Resource Requirement Projection

| Resource | Current | 6-Month | 12-Month | Action Needed |
|---|---|---|---|---|
| CPU instances | 50 | 80 | 130 | Order in 3 months |
| GPU instances | 20 | 35 | 60 | Order in 2 months |
| Memory (TB) | 200 | 320 | 520 | Upgrade in 4 months |
| Storage (TB) | 500 | 800 | 1,300 | Expand in 3 months |
| Network (Gbps) | 10 | 16 | 26 | Upgrade in 5 months |

---

## 4. Cost Modeling

### 4.1 Cost Per Recommendation

```
Cost per recommendation = total_infrastructure_cost / total_recommendations_served

Example:
  Monthly infrastructure cost: $500,000
  Monthly recommendations: 15 billion
  Cost per recommendation: $0.000033
```

### 4.2 Cost Breakdown by Component

| Component | Monthly Cost | % of Total | Cost/1K Recs |
|---|---|---|---|
| GPU instances (model serving) | $200,000 | 40% | $0.013 |
| CPU instances (services) | $120,000 | 24% | $0.008 |
| Storage (model artifacts, features) | $50,000 | 10% | $0.003 |
| Networking (cross-region, CDN) | $40,000 | 8% | $0.003 |
| Feature store (managed service) | $30,000 | 6% | $0.002 |
| Monitoring (logs, metrics, traces) | $25,000 | 5% | $0.002 |
| Caching (Redis/Memcached) | $20,000 | 4% | $0.001 |
| Other (DNS, LB, etc.) | $15,000 | 3% | $0.001 |
| **Total** | **$500,000** | **100%** | **$0.033** |

### 4.3 Cost Optimization Opportunities

| Optimization | Savings | Implementation Effort |
|---|---|---|
| Spot instances for non-critical workloads | 30-60% on compute | Low |
| Reserved instances for steady-state workloads | 20-40% on compute | Low |
| GPU right-sizing (match model to GPU) | 10-30% on GPU cost | Medium |
| Model optimization (quantization, pruning) | 20-50% on GPU cost | High |
| Auto-scaling tuning | 10-20% on compute | Medium |
| Storage tiering | 30-60% on storage cost | Low |
| Feature caching optimization | 10-20% on feature store cost | Medium |

### 4.4 Cost Trend Dashboard

| Panel | Metric | Visualization |
|---|---|---|
| Total cost trend | Monthly infrastructure cost | Time series |
| Cost per recommendation | Cost / recommendations served | Time series |
| Cost by component | Breakdown by service | Stacked area chart |
| Cost efficiency trend | Cost per recommendation over time | Time series |
| Forecasted cost | Projected cost based on growth | Time series with projection |
| Optimization savings | Savings from optimization actions | Bar chart |

---

## 5. Scaling Triggers

### 5.1 Horizontal Scaling Triggers

| Trigger | Condition | Action |
|---|---|---|
| CPU utilization | > 70% for 5 min | Add 2 instances |
| Memory utilization | > 80% for 5 min | Add 2 instances |
| GPU utilization | > 85% for 5 min | Add 1 GPU instance |
| Queue depth | > 100 for 5 min | Add 2 instances |
| Request rate | > 80% of capacity | Add instances to match |
| Latency P99 | > SLO threshold for 5 min | Add instances |
| Error rate | > 1% for 5 min | Add instances |

### 5.2 Vertical Scaling Triggers

| Trigger | Condition | Action |
|---|---|---|
| Memory pressure | > 90% sustained | Upgrade instance type |
| CPU bottleneck | > 85% sustained | Upgrade instance type |
| GPU memory | > 90% sustained | Upgrade GPU type |
| Model too large for current GPU | OOM error | Upgrade GPU type |

### 5.3 Auto-Scaling Configuration

```yaml
auto_scaling:
  ranking_service:
    min_replicas: 10
    max_replicas: 50
    target_cpu_utilization: 70
    target_memory_utilization: 80
    scale_up_cooldown: 60s
    scale_down_cooldown: 300s
    metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      - type: Pods
        pods:
          metric:
            name: rec_queue_depth
          target:
            type: AverageValue
            averageValue: 50
```

### 5.4 Scaling Safety

- **Minimum capacity**: Always maintain minimum instances for baseline traffic
- **Maximum cap**: Set maximum replicas to prevent cost runaway
- **Cooldown periods**: Prevent rapid scaling oscillation
- **Gradual scale-down**: Reduce capacity slowly to avoid connection draining issues
- **Pre-scaling**: Scale up before known traffic spikes (deployments, events)

---

## 6. GPU Capacity Planning

### 6.1 GPU Requirements

| Model Type | Parameters | GPU Memory | GPU Type | Inference Throughput |
|---|---|---|---|---|
| Candidate retrieval (ANN) | N/A | 2GB | T4 | 10K QPS |
| Lightweight ranking (GBDT) | N/A | 1GB | T4 | 5K QPS |
| Deep ranking (DNN) | 50M | 4GB | T4 | 1K QPS |
| Deep ranking (Transformer) | 200M | 16GB | A10G | 500 QPS |
| Large ranking (LLM-based) | 1B+ | 40GB | A100 | 100 QPS |

### 6.2 GPU Utilization Optimization

| Technique | Improvement | Complexity |
|---|---|---|
| Dynamic batching | 2-3x throughput | Low |
| TensorRT optimization | 2-3x throughput | Medium |
| Model quantization (FP16) | 2x throughput | Low |
| Model quantization (INT8) | 3-4x throughput | High |
| Model pruning | 1.5-2x throughput | High |
| Multi-model GPU sharing (MPS) | 30-50% utilization improvement | Medium |

### 6.3 GPU Cost Optimization

| Strategy | Savings | Risk |
|---|---|---|
| Spot instances | 60-70% | Interruption risk |
| Reserved instances | 30-40% | Commitment |
| Right-sizing (match GPU to model) | 20-30% | Requires profiling |
| Auto-scaling GPU instances | 20-40% | Cold start latency |
| GPU time-sharing | 30-50% | Complexity |

### 6.4 GPU Monitoring Dashboard

| Panel | Metric | Visualization |
|---|---|---|
| GPU utilization | nvidia_gpu_utilization_percent | Gauge per GPU |
| GPU memory | nvidia_gpu_memory_used_percent | Gauge per GPU |
| GPU temperature | nvidia_gpu_temperature | Gauge per GPU |
| GPU power | nvidia_gpu_power_usage | Time series |
| GPU error count | nvidia_gpu_errors_total | Counter |
| GPU instance count | Active GPU instances | Single stat |

---

## 7. Right-Sizing

### 7.1 Right-Sizing Methodology

```
Step 1: Profile current resource usage (30 days)
Step 2: Identify over-provisioned resources (>50% headroom consistently)
Step 3: Identify under-provisioned resources (>80% utilization consistently)
Step 4: Match resource type to workload requirements
Step 5: Test with reduced resources (canary)
Step 6: Monitor after right-sizing
Step 7: Repeat quarterly
```

### 7.2 Right-Sizing Recommendations

| Service | Current | Recommended | Savings | Risk |
|---|---|---|---|---|
| Feature service | c5.4xlarge (16 vCPU) | c5.2xlarge (8 vCPU) | 50% | Low (CPU avg 35%) |
| Ranking service | p3.2xlarge (V100) | g5.xlarge (A10G) | 60% | Medium (GPU avg 45%) |
| Candidate service | c5.2xlarge (8 vCPU) | c5.xlarge (4 vCPU) | 50% | Low (CPU avg 40%) |
| Caching layer | r5.4xlarge (128GB) | r5.2xlarge (64GB) | 50% | Medium (memory avg 55%) |

### 7.3 Right-Sizing Dashboard

| Panel | Metric | Visualization |
|---|---|---|
| Resource utilization vs. allocated | Utilization / allocation ratio | Time series |
| Right-sizing recommendations | Automated recommendations | Table |
| Cost savings potential | Monthly savings from right-sizing | Bar chart |
| Right-sizing history | Past right-sizing actions and results | Timeline |

---

## 8. Capacity Review Process

### 8.1 Review Cadence

| Review | Frequency | Participants | Focus |
|---|---|---|---|
| Weekly capacity check | Weekly | SRE team | Current utilization, alerts |
| Monthly capacity review | Monthly | SRE + ML team | Trends, forecasts, optimizations |
| Quarterly capacity planning | Quarterly | SRE + ML + Finance | Budget, growth, infrastructure orders |
| Annual capacity strategy | Annually | Leadership | Multi-year planning, technology roadmap |

### 8.2 Capacity Review Template

```
Capacity Review - [Month Year]

1. Current State
   - Resource utilization (CPU, memory, GPU, storage)
   - Cost per recommendation
   - SLO compliance

2. Trends and Forecasts
   - 90-day utilization trends
   - 6-month growth projection
   - Capacity exhaustion dates

3. Optimization Opportunities
   - Right-sizing recommendations
   - Cost optimization actions
   - Performance improvements

4. Growth Preparedness
   - Headroom for growth
   - Scaling speed assessment
   - Infrastructure order timeline

5. Action Items
   - Immediate (this month)
   - Short-term (next quarter)
   - Long-term (next year)
```

### 8.3 Capacity Alert Thresholds

| Threshold | Action |
|---|---|
| Resource utilization > 70% | Monitor, plan for expansion |
| Resource utilization > 80% | Expand capacity within 2 weeks |
| Resource utilization > 90% | Emergency expansion within 24 hours |
| Cost per recommendation increasing > 10% monthly | Investigate and optimize |
| Forecast shows capacity exhaustion < 30 days | Order infrastructure immediately |

---

## 9. Key Takeaways

1. **Forecast resource needs** based on user growth, traffic patterns, and model evolution
2. **Set scaling triggers** for automatic horizontal and vertical scaling
3. **Monitor cost per recommendation** — it should decrease or stay stable over time
4. **Right-size resources quarterly** — match infrastructure to actual workload
5. **Plan GPU capacity carefully** — GPU is the most expensive and constrained resource
6. **Implement auto-scaling** with safety guards (min/max, cooldown, gradual scale-down)
7. **Pre-scale for known events** — holidays, launches, viral content
8. **Use cost optimization** — spot instances, reserved instances, model optimization
9. **Review capacity monthly** — catch issues before they become outages
10. **Maintain 30-50% headroom** — provides buffer for traffic spikes and growth
