# Resource Management for GPU Training

## Overview

Efficient GPU resource management is critical for cost-effective recommendation model training at scale. With GPUs being the most expensive compute resource in a training cluster, maximizing utilization while ensuring fair access across teams is a core engineering challenge. This document covers GPU sharing mechanisms, scheduling policies, cost tracking, and preemptible job management.

---

## GPU Sharing Mechanisms

### Multi-Instance GPU (MIG)

NVIDIA MIG partitions a single A100/H100 GPU into up to 7 isolated GPU instances, each with dedicated compute, memory, and cache resources.

| MIG Profile | Compute Units | Memory | SM Count | Use Case |
|-------------|--------------|--------|----------|----------|
| 1g.5gb | 1 | 5 GB | 14 | Light inference, small models |
| 1g.10gb | 1 | 10 GB | 14 | Embedding lookups |
| 2g.10gb | 2 | 10 GB | 28 | Small training jobs |
| 3g.20gb | 3 | 20 GB | 42 | Medium training |
| 4g.20gb | 4 | 20 GB | 56 | Large training jobs |
| 7g.40gb | 7 | 40 GB | 98 | Full A100 (no MIG) |

**MIG Benefits**:
- Hardware-level isolation: one instance cannot affect another's performance
- Guaranteed resource allocation: no oversubscription
- Independent ECC error domains: faults are isolated
- Suitable for multi-tenant environments with strict SLA requirements

**MIG Limitations**:
- Fixed partition profiles; cannot dynamically resize
- Only available on A100 and H100
- Requires driver-level configuration (not dynamic in all versions)
- Cannot combine MIG instances for a single workload

### Time-Slicing (GPU Sharing)

Time-slicing allows multiple processes to share a single GPU by rapidly switching between them at the CUDA context level.

**Implementation via NVIDIA GPU Operator**:
- Configure `timeSlicing` in the device plugin ConfigMap
- Set `resources` to the number of virtual GPUs to expose
- Each virtual GPU gets a time slice (typically 1-10ms)
- No memory isolation: one process can cause OOM for others

**When to Use Time-Slicing**:
- Development and testing workloads where isolation is not critical
- Inference pods that are memory-bound but compute-light
- Hyperparameter search with many small experiments
- Environments where GPU utilization is consistently low

### CUDA MPS (Multi-Process Service)

- Runs multiple CUDA processes concurrently on a single GPU
- Hardware-level thread block scheduling across processes
- Better utilization than time-slicing for compute-bound workloads
- No memory isolation between processes
- Useful when multiple small training jobs share a GPU

### Comparison Matrix

| Mechanism | Isolation | Overhead | Granularity | Best For |
|-----------|-----------|----------|-------------|----------|
| MIG | Full hardware | Minimal | Fixed profiles | Production multi-tenant |
| Time-slicing | None | Context switch | Configurable | Dev/test, light workloads |
| MPS | None (compute) | Minimal | Per-thread-block | Small compute-bound jobs |
| vGPU (NVIDIA) | Full | Moderate | Configurable | VMware/virtual environments |

---

## Training Job Scheduling

### Scheduling Policy Design

1. **Backfill scheduling**: Fill gaps in the GPU schedule with small jobs that fit available resources
2. **Gang scheduling**: Schedule all pods of a distributed job simultaneously or not at all
3. **Fair-share**: Divide GPU resources equally among teams/projects, not by demand
4. **Capacity scheduling**: Reserve guaranteed GPU capacity per team with burst capability

### Kubernetes Scheduler Customization

- Use the **Scheduler Framework** to implement custom scheduling plugins
- `QueueSort`: Priority-based ordering of pending pods
- `Filter`: Eliminate nodes that don't meet GPU requirements
- `Score`: Rank nodes by GPU availability, topology, cost efficiency
- `Reserve`: Reserve GPU resources atomically for gang-scheduled jobs
- `PostBind`: Update GPU utilization tracking after pod placement

### Job Queue Management

| Queue Type | Description | Example |
|------------|-------------|---------|
| Priority Queue | Jobs ordered by priority level | Production > Staging > Experiment |
| FIFO | First-come-first-served within priority | Earliest submission wins |
| Fair Queue | Proportional allocation per team | Team A gets 30%, Team B gets 70% |
| Deadline Queue | Jobs with SLA deadlines get priority | "Complete by Friday" training run |

### Resource Quotas Per Team

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ml-team-quota
  namespace: recommendation-training
spec:
  hard:
    requests.nvidia.com/gpu: "32"
    limits.nvidia.com/gpu: "32"
    requests.cpu: "256"
    requests.memory: "1Ti"
    pods: "50"
```

**Quota Management Strategies**:
- Set soft quotas (warning) at 80% and hard quotas at 100% of allocation
- Allow borrowing from a shared pool when team quota is exhausted
- Implement quota reclamation: reclaim unused quota after configurable idle period
- Track quota usage in real-time dashboards per team/namespace

---

## Cost Tracking Per Experiment

### Cost Attribution Model

| Resource | Pricing Basis | Tracking Method |
|----------|-------------|-----------------|
| GPU hours | Per-GPU-hour rate | Pod runtime × GPU count |
| CPU hours | Per-vCPU-hour rate | Pod runtime × CPU count |
| Memory | Per GB-hour | Peak memory × duration |
| Storage | Per GB-month | PVC usage over time |
| Network | Per GB transferred | Inter-zone/inter-region traffic |
| Spot discount | Credit applied | Spot savings vs on-demand |

### Experiment Cost Calculation

```
experiment_cost = Σ(gpu_type_rate × gpu_count × duration_hours) + 
                  Σ(cpu_rate × cpu_count × duration_hours) +
                  storage_cost + network_cost - spot_discounts
```

### Cost Tracking Implementation

- Label all training pods with `experiment-id`, `team`, `project`, `model-name`
- Use Prometheus metrics to track resource consumption per label combination
- Export cost data to a data warehouse (BigQuery, Snowflake) for analysis
- Generate weekly cost reports per team with drill-down to experiment level
- Set up budget alerts: notify when experiment cost exceeds threshold

### Cost Optimization Strategies

- **Right-sizing**: Profile actual GPU/memory usage; don't over-request
- **Spot utilization**: Route non-critical experiments to spot instances
- **Scheduling optimization**: Pack jobs tightly to minimize idle GPU time
- **Early stopping**: Terminate experiments that show no improvement (saves GPU hours)
- **Hardware selection**: Use T4 for inference testing, A100 for training, H100 only for large-scale runs

---

## Preemptible Training Jobs

### Preemption-Resilient Design

1. **Checkpointing framework**: Implement automatic checkpointing on `SIGTERM` signal
2. **Exponential backoff**: When rescheduled, wait with exponential backoff to avoid thundering herd
3. **State persistence**: Store experiment state (hyperparameters, data pointers, metric history) outside the pod
4. **Graceful degradation**: If GPU is lost mid-training, save partial progress and restart from last checkpoint

### Preemption Priority Management

- Assign lower priority to exploration experiments
- Assign higher priority to production model training with deadlines
- Implement preemption budgets: limit how many times a job can be preempted before escalating to on-demand
- Track preemption rates per team and adjust priority/class accordingly

### Spot Instance Strategy for Training

| Strategy | Description | Risk Level |
|----------|-------------|-----------|
| Checkpoint-every-N-steps | Fixed interval checkpointing | Low |
| Checkpoint-on-demand | Checkpoint before known preemption | Medium |
| Hybrid spot/on-demand | Critical path on on-demand, sweep on spot | Low |
| Multi-cloud spot | Diversify across AWS/GCP/Azure spot pools | Medium |
| Preemptible reservations | Use capacity reservations for critical runs | Low |

---

## Monitoring and Governance

### GPU Utilization Tracking

- Average GPU utilization target: >70% during active training
- Memory utilization target: >60% to justify the GPU allocation
- Idle GPU detection: alert when GPU is allocated but utilization <5% for >15 minutes
- Track GPU utilization trend over weeks to identify patterns

### Resource Governance Policies

- Maximum GPU allocation per team per namespace
- Maximum single-job GPU count (prevent one job from monopolizing cluster)
- Required labels for all training pods (experiment-id, team, project)
- Automatic pod deletion after 7 days without checkpoint updates (abandoned jobs)
- Weekly resource review meetings with team leads

### Reporting and Analytics

- GPU utilization dashboard: real-time and historical
- Cost allocation reports: monthly per team, per project
- Efficiency metrics: cost per model quality improvement
- Capacity planning forecasts: projected GPU demand for next quarter
- SLA adherence tracking: percentage of jobs completing within expected timeframe
