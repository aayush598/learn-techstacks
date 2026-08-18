# Auto-Scaling for Recommendation Systems

## 1. Auto-Scaling Policies

### 1.1 Metric-Based Scaling

**CPU-Based Scaling**:
- Target: 70% CPU utilization
- Scale up when sustained above target for 60 seconds
- Scale down when sustained below target for 300 seconds
- Minimum 3 replicas for high availability

**Memory-Based Scaling**:
- Target: 80% memory utilization
- Critical at 90% (immediate scale up)
- Scale down when below 60% for 10 minutes
- Consider memory-intensive workloads (feature computation, model loading)

**GPU-Based Scaling**:
- Target: 80% GPU utilization
- Scale up when utilization above 80% for 60 seconds
- Scale down when below 30% for 10 minutes
- Consider GPU memory utilization as secondary metric

**QPS-Based Scaling**:
- Target: 1000 QPS per replica (varies by service)
- Scale up when QPS exceeds capacity by 20%
- Scale down when QPS drops below 50% of capacity
- Best for: Stateless services with predictable per-request cost

### 1.2 Custom Metrics Scaling

**Inference Queue Depth**:
- Scale up when queue depth exceeds threshold
- Scale down when queue is empty for sustained period
- Best for: Model serving with request queuing

**Latency-Based Scaling**:
- Scale up when P99 latency exceeds target
- Scale down when P95 latency is well below target
- Best for: Latency-sensitive recommendation serving

**Feature Freshness**:
- Scale up feature computation when freshness degrades
- Scale down when freshness is within SLA
- Best for: Streaming feature computation

---

## 2. Kubernetes Auto-Scaling

### 2.1 Horizontal Pod Autoscaler (HPA)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ranking-service
  minReplicas: 3
  maxReplicas: 50
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
          name: inference_queue_depth
        target:
          type: AverageValue
          averageValue: "10"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 120
```

### 2.2 Cluster Autoscaler
- Automatically adds/removes nodes based on pod scheduling needs
- Scales node pools when pods are pending due to insufficient resources
- Consolidates pods to fewer nodes during low traffic
- Integrates with cloud provider auto-scaling groups

### 2.3 Vertical Pod Autoscaler (VPA)
- Adjusts CPU/memory requests based on actual usage
- Recommends right-sizing for pods
- Useful for: Initial capacity planning, identifying resource needs
- Caution: VPA changes require pod restart

---

## 3. Predictive Auto-Scaling

### 3.1 Time-Based Predictions
- Scale up before known traffic spikes (e.g., evening peak hours)
- Scale down during predictable low-traffic periods
- Use historical traffic patterns for prediction
- Schedule scaling actions in advance

### 3.2 ML-Based Predictions
- Train model on historical traffic patterns
- Predict future QPS, latency, resource needs
- Proactively scale before demand increases
- Consider: time of day, day of week, seasonality, special events

### 3.3 Hybrid Approach
- Combine reactive (current metrics) and predictive (forecasted demand)
- Use predictive as leading indicator for proactive scaling
- Use reactive as safety net for unexpected changes
- Tune based on observed accuracy of predictions

---

## 4. Cost-Aware Auto-Scaling

### 4.1 Spot/Preemptible Instances
- Use spot instances for training and batch processing (60-90% savings)
- Maintain minimum on-demand capacity for critical services
- Handle spot interruptions gracefully (checkpoint, migrate)
- Mixed instance types for availability

### 4.2 Scale-Down Policies
- Gradual scale-down to avoid oscillation
- Cooldown periods after scale-down
- Protect minimum replica count for availability
- Consider time-of-day patterns for aggressive scale-down

### 4.3 Resource Quotas
- Set maximum resource limits per service
- Prevent runaway scaling from consuming entire cluster
- Namespace-level resource quotas
- Team-level budget limits

---

## 5. Scaling ML Workloads

### 5.1 Training Job Scaling
- **GPU Auto-Scaling**: Scale GPU nodes for training jobs
- **Job Scheduling**: Use Kubernetes Job with resource requests
- **Preemption**: Lower-priority training jobs preemptible by serving
- **Checkpointing**: Save training state for resumption after preemption

### 5.2 Feature Pipeline Scaling
- **Spark Dynamic Allocation**: Add/remove executors based on workload
- **Flink Reactive Scaling**: Scale task managers based on backpressure
- **Batch Pipeline Scaling**: Scale based on data volume
- **Streaming Pipeline Scaling**: Scale based on consumer lag

### 5.3 Inference Scaling
- **GPU Pod Auto-Scaling**: Scale based on inference demand
- **Model-Specific Scaling**: Different scaling for different models
- **Batch vs Real-Time**: Separate scaling for batch and real-time inference
- **Multi-Model GPU**: Share GPU across models for efficiency
