# Kubernetes Architecture for Recommendation Systems

## Overview

Kubernetes provides the orchestration backbone for running recommendation systems at scale. A well-designed Kubernetes architecture must accommodate heterogeneous workloads: CPU-intensive feature computation, GPU-accelerated model inference, memory-intensive caching layers, and data-intensive batch processing. This document covers the architectural decisions, resource management strategies, and operational patterns required for production recommendation systems.

## Cluster Design

### Node Pool Architecture

A recommendation system typically requires multiple specialized node pools to optimize cost and performance for different workload types.

**System Node Pool**

- Purpose: Run cluster-critical components (API server, etcd, CoreDNS, kube-proxy, ingress controllers, monitoring agents).
- Instance type: `m5.large` or equivalent (2 vCPU, 8 GiB RAM) with standard SSD.
- Minimum 3 nodes across 3 availability zones for high availability.
- Taint: `CriticalAddonsOnly=true:NoSchedule` to prevent non-system workloads from scheduling.
- Do not run recommendation workloads on system nodes regardless of available resources.

**Application Node Pool**

- Purpose: Run recommendation API servers, feature serving containers, and stateless microservices.
- Instance type: `m5.2xlarge` or equivalent (8 vCPU, 32 GiB RAM).
- Scale: 3-50 nodes based on traffic patterns.
- Use Spot/Preemptible instances for cost savings with proper disruption budgets.
- Configure Pod Disruption Budgets (PDBs) to ensure minimum availability during node maintenance.

**GPU Node Pool**

- Purpose: Run model inference services requiring GPU acceleration.
- Instance type: `g4dn.xlarge` (T4) for inference, `p3.2xlarge` (V100) or `g5.xlarge` (A10G) for heavier models.
- Scale: 2-20 nodes based on inference throughput requirements.
- Enable GPU sharing with NVIDIA MPS or time-slicing for small models.
- Use `nvidia.com/gpu` resource requests and limits on all GPU pods.

**Data Node Pool**

- Purpose: Run stateful workloads such as Redis, PostgreSQL replicas, Elasticsearch, and batch processing jobs.
- Instance type: `r5.2xlarge` (memory-optimized) or `i3.2xlarge` (storage-optimized).
- Scale: Fixed capacity (3-6 nodes) with manual scaling for data-intensive operations.
- Use local NVMe SSDs for caching workloads and EBS gp3 for persistent storage.
- Taint workloads to prevent scheduling of non-data pods.

### Namespace Strategy

```
├── system/              # Cluster infrastructure components
├── monitoring/          # Prometheus, Grafana, alerting stack
├── recommendation-api/  # Model serving API containers
├── feature-service/     # Feature computation and serving
├── training/            # Model training jobs and workflows
├── data-pipeline/       # ETL and data processing jobs
├── cache/               # Redis clusters and caching layers
├── database/            # PostgreSQL, DynamoDB proxy
├── ingress/             # NGINX or Envoy ingress controllers
├── staging/             # Staging environment mirror
└── argocd/              # GitOps deployment controller
```

**Namespace Naming Conventions**

- Use lowercase alphanumeric characters and hyphens only.
- Follow `{team}-{function}` or `{function}` naming patterns.
- Tag namespaces with labels for policy enforcement and cost allocation.
- Implement ResourceQuotas at the namespace level to prevent resource starvation.

### Resource Quotas and Limits

**Namespace-Level ResourceQuotas**

- Set hard limits on total CPU, memory, GPU, and persistent volume claims per namespace.
- Enforce pod count limits to prevent namespace sprawl.
- Limit the number of Services, ConfigMaps, and Secrets per namespace.
- Use LimitRange to set default and maximum resource requests per pod.

**Pod-Level Resource Management**

- Always set both `requests` and `limits` for CPU and memory.
- Set CPU requests based on observed P95 utilization; set limits to 2x requests.
- Set memory requests at P99 utilization; set limits at 1.5x requests.
- For GPU pods, request exactly the number of GPUs needed (GPU resources cannot be fractional).
- Use `resources.requests` for scheduling decisions and `resources.limits` for runtime enforcement.

**Resource Right-Sizing Process**

1. Deploy without limits initially using VPA in recommendation mode.
2. Collect resource utilization metrics for 2-4 weeks of production traffic.
3. Set requests at P95 utilization to ensure reliable scheduling.
4. Set limits at 2x requests for CPU and 1.5x for memory.
5. Review and adjust quarterly or after significant traffic changes.

## Pod Scheduling

### GPU Affinity and Topology

**GPU Scheduling Configuration**

- Use `nodeSelector` or `nodeAffinity` to target GPU node pools.
- Implement `podAntiAffinity` to spread GPU pods across nodes for fault tolerance.
- Set `topologySpreadConstraints` with `maxSkew: 1` across `kubernetes.io/hostname`.
- For multi-GPU models, use `requiredDuringSchedulingIgnoredDuringExecution` to ensure co-location.

**GPU Sharing Strategies**

- NVIDIA Time-Slicing: Split a single GPU across multiple small inference pods.
- NVIDIA MPS: Run multiple CUDA processes on a single GPU with hardware isolation.
- GPU Operator: Automate GPU driver installation and node labeling.
- MIG (Multi-Instance GPU): Partition A10/H100 GPUs into isolated instances.

### Topology Spread Constraints

- Spread recommendation API pods across availability zones with `topologyKey: topology.kubernetes.io/zone`.
- Ensure at least 2 replicas per zone for zone-level fault tolerance.
- Use `podAntiAffinity` with `preferredDuringSchedulingIgnoredDuringExecution` for soft spreading across nodes.
- For stateful components (Redis, PostgreSQL), use `requiredDuringScheduling` with zone constraints.

### Priority Classes

| Priority | Value | Use Case |
|----------|-------|----------|
| System Critical | 1000000000 | API server, etcd, CoreDNS |
| High | 1000000 | Recommendation API, Feature Service |
| Medium | 100000 | Cache Layer, Data Pipeline |
| Low | 10000 | Training Jobs, Batch Processing |
| Preemptible | 1000 | Spot instance workloads |

### Node Affinity Rules

- Use `requiredDuringSchedulingIgnoredDuringExecution` for strict requirements (GPU, memory-optimized).
- Use `preferredDuringSchedulingIgnoredDuringExecution` for soft preferences (AZ distribution).
- Combine with `tolerations` for tainted nodes (GPU, system-critical).
- Validate affinity rules with `kubectl describe node` to verify correct scheduling.

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

**Scaling Configuration**

- Scale recommendation API pods based on CPU utilization (target: 60-70%).
- Scale based on custom metrics (requests/second, queue depth) when available.
- Set `minReplicas: 3` to ensure zone-level redundancy.
- Set `maxReplicas` based on maximum expected traffic (typically 3-5x baseline).
- Configure `behavior.scaleDown.stabilizationWindowSeconds: 300` to prevent thrashing.
- Configure `behavior.scaleUp.stabilizationWindowSeconds: 30` for rapid response to traffic spikes.

**Scaling Metrics for Recommendation Systems**

| Metric | Target | Scaling Direction |
|--------|--------|-------------------|
| CPU Utilization | 65% | Scale up at 70%, scale down at 50% |
| Request Rate | 1000 RPS/pod | Scale up when exceeded |
| P99 Latency | 200ms | Scale up when exceeded |
| Queue Depth | 100 items | Scale up when exceeded |
| GPU Utilization | 80% | Scale up when exceeded |

**HPA Behavior Tuning**

- Set `scaleUp.policies` with `percent: 100` and `periodSeconds: 60` for aggressive scale-up.
- Set `scaleDown.policies` with `percent: 10` and `periodSeconds: 300` for conservative scale-down.
- Use `selectPolicy: Max` for scale-up and `selectPolicy: Min` for scale-down.
- Set `stabilizationWindowSeconds` to smooth out transient traffic spikes.

### Vertical Pod Autoscaler (VPA)

- Deploy VPA in `recommendation` mode for all workloads to gather sizing data.
- After 2-4 weeks, switch to `Auto` mode for non-critical workloads.
- Never use VPA for GPU workloads (GPU requests are discrete, not continuous).
- Set VPA update policies to `Off` during peak traffic hours to prevent disruption.
- Use VPA recommendations to tune HPA custom metrics thresholds.

### Cluster Autoscaler

- Enable cluster autoscaler on all non-system node pools.
- Set `--scale-down-utilization-threshold: 0.5` to consolidate underutilized nodes.
- Set `--scale-down-delay-after-add: 10m` to prevent rapid node churn.
- Set `--max-node-provision-time: 15m` for cloud provider node provisioning.
- Use priority expander to prefer Spot instances for cost optimization.
- Implement overprovisioning with pause pods to maintain capacity headroom during scale-up.

**Autoscaler Cost Optimization**

- Use Spot/Preemptible instances for application and training node pools.
- Maintain a mix of on-demand and Spot for cost/resilience balance.
- Implement cluster overprovisioning with low-priority pause pods for fast scale-up.
- Use bin-packing scoring to reduce the number of underutilized nodes.

## Network Policies

### Default Deny All

- Implement default deny-all ingress and egress policies in each namespace.
- Explicitly allow only required traffic flows between services.
- Log denied connections for debugging and security audit.

### Service Mesh Communication Patterns

| Source | Destination | Protocol | Port | Purpose |
|--------|------------|----------|------|---------|
| Ingress Controller | recommendation-api | gRPC | 8080 | External traffic |
| recommendation-api | feature-service | gRPC | 8080 | Feature retrieval |
| recommendation-api | cache (Redis) | TCP | 6379 | Cache operations |
| feature-service | database (PG) | TCP | 5432 | Feature storage |
| training | S3/MinIO | HTTPS | 443 | Model artifact I/O |
| monitoring | all pods | HTTP | 9090 | Metrics scraping |

### Ingress Configuration

- Use NGINX Ingress Controller or Envoy Gateway for external traffic routing.
- Implement TLS termination at the ingress layer with automatic certificate rotation.
- Configure rate limiting at the ingress level (1000 RPS per client by default).
- Enable request compression (gzip/brotli) for recommendation responses.
- Set appropriate timeouts: connect=5s, send=30s, read=30s for recommendation APIs.

## RBAC (Role-Based Access Control)

### Service Account Strategy

- Create dedicated service accounts for each microservice (no default service account usage).
- Never mount service account tokens into pods unless required for API access.
- Use Workload Identity (GKE) or IRSA (EKS) for cloud API access instead of static credentials.

### Role Definitions

| Role | Namespace | Permissions |
|------|-----------|-------------|
| recommendation-api-role | recommendation-api | Read ConfigMaps, Secrets; write logs |
| feature-service-role | feature-service | Read/Write ConfigMaps; read Secrets |
| training-role | training | Read/Write PVCs; create Jobs |
| monitoring-role | monitoring | Read all namespaces (metrics) |
| admin | all | Full cluster administration |

### Pod Security Standards

- Apply `restricted` Pod Security Standards to all application namespaces.
- Forbid privileged containers, host networking, and host PID namespace.
- Require non-root user execution with `runAsNonRoot: true`.
- Set `readOnlyRootFilesystem: true` and use emptyDir for writable paths.
- Drop all capabilities except `NET_BIND_SERVICE` where required.
- Enforce seccomp profile `RuntimeDefault` or `RuntimeDefault` on all pods.

## Observability

### Pod-Level Monitoring

- Instrument all recommendation pods with Prometheus metrics endpoints.
- Use ServiceMonitor CRDs for automatic metrics scraping configuration.
- Implement distributed tracing with OpenTelemetry (Jaeger or Tempo backend).
- Collect structured JSON logs with correlation IDs for request tracing.

### Health Check Configuration

- Implement liveness probes with `/healthz` endpoints (HTTP or gRPC).
- Implement readiness probes with `/readyz` endpoints that verify dependencies.
- Set appropriate probe periods: liveness every 10s, readiness every 5s.
- Use `initialDelaySeconds` to account for model loading time (30-120s for large models).
- Configure startup probes for slow-starting containers with `failureThreshold: 30`.

## Disaster Recovery

### Multi-Cluster Strategy

- Deploy primary cluster in the main region with full capacity.
- Maintain a warm standby cluster in a secondary region with scaled-down capacity.
- Use DNS-based traffic routing (Route53, CloudDNS) for automatic failover.
- Replicate critical data (PostgreSQL, Redis) cross-region asynchronously.

### Backup and Recovery

- Schedule etcd snapshots every 6 hours with 30-day retention.
- Use Velero for Kubernetes resource backups with daily schedule.
- Back up PVCs using volume snapshots (CSI snapshot drivers).
- Test restoration procedures quarterly with documented runbooks.
