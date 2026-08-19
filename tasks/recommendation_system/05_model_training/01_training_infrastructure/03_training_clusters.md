# Kubernetes GPU Training Clusters

## Overview

Training production recommendation systems requires orchestrated GPU clusters that efficiently share hardware across multiple training jobs, prioritize critical workloads, and manage costs. Kubernetes has emerged as the standard orchestration layer for GPU training, with NVIDIA's GPU Operator and device plugin providing GPU awareness. This document covers cluster design, scheduling strategies, and cost management.

---

## Cluster Architecture

### Node Pool Design

| Node Pool | GPU Type | Count | Purpose | Preemptible |
|-----------|----------|-------|---------|-------------|
| training-premium | H100 SXM8 | 8-16 | Large model training, NAS | No |
| training-standard | A100 80GB | 16-64 | Standard training runs | Mixed |
| training-spot | A100 40GB | 32-128 | Hyperparameter sweeps, experiments | Yes |
| serving-gpu | T4/A10 | 8-32 | Model serving (separate cluster preferred) | No |
| data-prep | CPU-only | 16-32 | Feature engineering, data preprocessing | Yes |

### Kubernetes Components for GPU Support

- **NVIDIA GPU Operator**: Deploys device plugin, driver, container toolkit, DCGM exporter as a unified Helm chart
- **Device Plugin**: Exposes GPUs as schedulable resources (`nvidia.com/gpu: 4`)
- **GPU Feature Discovery**: Auto-labels nodes with GPU properties (type, memory, count, MIG status)
- **DCGM Exporter**: GPU metrics collection for Prometheus (utilization, memory, temperature, ECC errors)
- **NVIDIA Network Operator**: InfiniBand/RoCE networking for multi-node training

### Node Configuration Requirements

- Install NVIDIA driver >= 525.x with CUDA 12.x support
- Enable NVIDIA Container Toolkit for GPU passthrough
- Configure `nvidia-device-plugin` DaemonSet with time-sharing or MIG mode
- Set kernel parameters: `isolcpus`, `nohz_full` for CPU pinning in latency-sensitive workloads
- Disable CPU frequency scaling (set performance mode) for consistent training times

---

## GPU Scheduling Strategies

### Resource Requests and Limits

```yaml
resources:
  requests:
    nvidia.com/gpu: 4      # Request 4 GPUs
    cpu: "32"
    memory: "128Gi"
  limits:
    nvidia.com/gpu: 4      # Limits match requests (Guaranteed QoS)
```

- GPU resources are **not shareable** at the device plugin level (whole GPUs only)
- Use MIG or time-sharing plugins for GPU sharing (see Resource Management)
- Always set both requests and limits equal for GPU jobs (Guaranteed QoS class)
- CPU and memory should be sized to match GPU count (typically 8 CPU cores and 32GB RAM per GPU)

### GPU Affinity and Topology Awareness

- **Node affinity**: Schedule multi-GPU jobs on nodes with NVLink/NVSwitch connectivity
- **Topology spread constraints**: Distribute single-GPU jobs across nodes to avoid fragmentation
- **GPU to CPU socket affinity**: Pin GPU workloads to the nearest CPU NUMA node to minimize PCIe traversal latency
- Use `nvidia.com/gpu.product` node labels to target specific GPU models
- Pod anti-affinity rules prevent two large training jobs from sharing a node (avoiding memory pressure)

### Multi-Node Training Scheduling

- Gang scheduling: all pods for a distributed job must be scheduled simultaneously
- Use Kubernetes `scheduling.k8s.io/pod-group` annotation or Volcano scheduler for gang scheduling
- Ensure all nodes in a job are in the same availability zone for low-latency InfiniBand
- Pre-provision PVCs for checkpoint storage before training pods start
- Configure `NCCL_DEBUG=INFO` and NCCL environment variables for optimal inter-node communication

---

## Priority Classes and Preemption

### Priority Class Hierarchy

| Priority | Name | Value | Preempts |
|----------|------|-------|----------|
| Critical | serving-production | 1000000 | Everything except system |
| High | training-production | 100000 | Spot, experiments |
| Medium | training-staging | 50000 | Spot only |
| Low | training-experiment | 10000 | Nothing |
| Lowest | best-effort | 1000 | Nothing |

### Preemption Behavior

- Kubernetes preempts lower-priority pods when higher-priority pods are pending
- Preempted pods receive a 30-second grace period for checkpointing
- Training jobs must implement checkpoint-on-preemption handlers
- Use `PriorityClassName` in pod spec to assign priority
- Set `preemptionPolicy: PreemptLowerPriority` (default) or `Never` for critical workloads

### Avoiding Starvation

- Reserve 20% of cluster capacity for high-priority training jobs
- Use ResourceQuota per namespace to limit total GPU consumption by team
- Implement fair-share scheduling with Kubernetes Scheduler Framework plugins
- Monitor eviction rates and adjust priorities based on actual usage patterns

---

## Spot Instance Integration

### Benefits and Risks

- **Cost reduction**: 60-70% savings on GPU compute
- **Availability**: Can be revoked with 30-120 seconds notice
- **Best for**: Hyperparameter sweeps, data augmentation runs, non-critical experiments
- **Avoid for**: Final model training, time-sensitive deadlines

### Spot-Resilient Training Design

1. **Frequent checkpointing**: Every 10-15 minutes to cloud storage (S3/GCS)
2. **Graceful shutdown handlers**: Listen for `SIGTERM` and write checkpoint before termination
3. **Dynamic rescheduling**: Use training operators (e.g., Kubeflow Training Operator) to automatically reschedule preempted jobs
4. **Mixed spot/on-demand**: Run primary training on on-demand, hyperparameter sweep on spot
5. **Instance diversity**: Mix spot instance types to reduce correlated preemption risk

### Spot Instance Monitoring

- Track preemption frequency per instance type and availability zone
- Maintain a preemption history dashboard to identify stable instance pools
- Set up alerts when spot interruption notices arrive (via cloud provider metadata)
- Calculate effective cost including checkpointing overhead and preemption-induced restarts

---

## Checkpoint Storage Architecture

### Persistent Volume Configuration

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-checkpoints
spec:
  accessModes: [ReadWriteMany]
  storageClassName: nfs-csi
  resources:
    requests:
      storage: 500Gi
```

### Storage Backend Selection

| Backend | Throughput | Cost | Durability | Best For |
|---------|-----------|------|-----------|----------|
| NFS/CephFS | 1-3 GB/s | Medium | Medium | Frequent checkpointing |
| S3/GCS | 0.1-1 GB/s | Low | Very High | Long-term checkpoint storage |
| Local NVMe | 3-7 GB/s | High (per-node) | Low | Intermediate checkpoints |
| EFS | 1 GB/s | High | High | AWS-native shared storage |
| JuiceFS | 2-5 GB/s | Low | High | Cloud-native distributed FS |

### Checkpoint Management Strategy

- Write checkpoints to local NVMe first (fastest), then async replicate to S3/GCS
- Implement checkpoint rotation: keep last N checkpoints, delete older ones
- Store model metadata (hyperparams, metrics, data version) alongside checkpoint
- Use compression for checkpoint files (PyTorch `torch.save` with `zipfile` or manual tensor compression)
- Implement checkpoint validation: load and verify integrity before resuming training

### Data Pipeline Storage

- Training data should be on high-throughput storage (S3 with acceleration, GCS with parallel reads)
- Use prefetching and caching at the DataLoader level
- Consider Alluxio or similar caching layer for hot training data
- Separate data storage from checkpoint storage to avoid I/O contention

---

## Monitoring and Observability

### GPU Metrics (via DCGM Exporter)

- `DCGM_FI_DEV_GPU_UTIL`: GPU compute utilization (%)
- `DCGM_FI_DEV_FB_USED`: Framebuffer memory used (MiB)
- `DCGM_FI_DEV_SM_ACTIVE`: Streaming multiprocessor activity (%)
- `DCGM_FI_DEV_PCIE_TX/RX`: PCIe throughput (KB/s)
- `DCGM_FI_DEV_NVLINK_TX/RX`: NVLink throughput (KB/s)
- `DCGM_FI_DEV_ECC_SBE`: Single-bit ECC errors (hardware health indicator)

### Cluster-Level Monitoring

- GPU utilization heatmap across all nodes (Grafana dashboard)
- Node resource fragmentation: track partially allocated GPU nodes
- Pending pod queue: jobs waiting for GPU resources
- Preemption events: count and impact analysis
- Cost allocation: GPU-hours consumed per team, project, experiment

### Alerting Rules

- GPU temperature >85°C sustained: potential hardware issue
- GPU utilization <20% for >30 minutes: possible training stall
- ECC error rate spike: hardware degradation
- Checkpoint failure: training may not be recoverable
- Node GPU not ready: driver or hardware failure

---

## Scaling Considerations

### Cluster Autoscaler for GPUs

- Use node auto-provisioning (NAP) to automatically add GPU nodes when pods are pending
- Set scale-down delay to avoid frequent node churn (10-15 minutes idle before removal)
- Pre-provision a minimum number of GPU nodes to avoid cold-start delays
- Use separate node pools for different GPU types to prevent mixed-GPU nodes

### Multi-Cluster Training

- For very large models (>8 GPUs), distribute training across multiple clusters
- Use high-bandwidth inter-cluster links (dedicated interconnect, VPN with QoS)
- Consider federated training setups for geographically distributed data
- Coordinate checkpoints across clusters using distributed consensus

### Capacity Planning

- Forecast GPU demand based on planned experiments and model sizes
- Maintain 15-20% excess capacity for burst demand and maintenance
- Track GPU utilization trends to right-size the cluster
- Use reserved instances for baseline capacity, spot/on-demand for peaks
