# Resource Quotas

Resource quotas prevent any single team, namespace, or workload from consuming cluster resources at the expense of others. In a shared Kubernetes cluster running recommendation system components alongside other services, quotas enforce fairness, prevent noisy-neighbor problems, and ensure critical services always have the resources they need. This document covers namespace quotas, limit ranges, priority classes, preemption, monitoring, and right-sizing methodology.

---

## 1. Namespace Quotas

### 1.1 Purpose and Scope

ResourceQuota objects are namespace-scoped. They limit the total resource consumption within a namespace.

### 1.2 Quota Configuration by Namespace Type

| Namespace | CPU Limit | Memory Limit | Pod Count | Purpose |
|---|---|---|---|---|
| `rec-prod` | 64 cores | 128Gi | 100 | Production recommendation services |
| `rec-staging` | 16 cores | 32Gi | 50 | Staging environment |
| `rec-ephemeral` | 8 cores | 16Gi | 30 | PR environments |
| `monitoring` | 16 cores | 32Gi | 40 | Prometheus, Grafana, alerting |
| `shared-infra` | 8 cores | 16Gi | 20 | Ingress, cert-manager, operators |

### 1.3 Quota Types

| Quota Resource | Example Value | What It Limits |
|---|---|---|
| `requests.cpu` | `"32"` | Total CPU requests across all pods |
| `requests.memory` | `"64Gi"` | Total memory requests across all pods |
| `limits.cpu` | `"64"` | Total CPU limits across all pods |
| `limits.memory` | `"128Gi"` | Total memory limits across all pods |
| `pods` | `"100"` | Maximum number of pods |
| `services` | `"20"` | Maximum number of Service objects |
| `configmaps` | `"50"` | Maximum number of ConfigMaps |
| `persistentvolumeclaims` | `"10"` | Maximum number of PVCs |
| `secrets` | `"50"` | Maximum number of Secrets |

### 1.4 Quota Enforcement Modes

| Mode | Behavior | When to Use |
|---|---|---|
| Hard quota | Rejects creation if quota exceeded | Production namespaces |
| Scopes (Terminating) | Only applies to pods with `restartPolicy: Always` | Allow batch jobs to exceed quota |
| Scopes (NotBestEffort) | Only applies to pods with resource requests | Allow burstable workloads |

---

## 2. Limit Ranges

### 2.1 Default Resource Limits

LimitRange sets default and maximum resource allocations for pods in a namespace.

**Configuration:**

| Setting | CPU | Memory | Purpose |
|---|---|---|---|
| Default request | 250m | 512Mi | Applied when pod doesn't specify |
| Default limit | 500m | 1Gi | Applied when pod doesn't specify |
| Minimum | 50m | 128Mi | Prevents zero-resource pods |
| Maximum | 4000m | 16Gi | Prevents runaway resource requests |
| Max limit/request ratio | 4 | 4 | Prevents excessive bursting |

### 2.2 Limit Range per Container Type

| Container Type | Request Range | Limit Range | Rationale |
|---|---|---|---|
| Init containers | 100m–2000m CPU | 256Mi–4Gi memory | Temporary, need resources for startup |
| Application containers | 250m–4000m CPU | 512Mi–16Gi memory | Steady-state serving |
| Sidecar containers | 50m–200m CPU | 64Mi–256Mi memory | Auxiliary, should be lightweight |
| Ephemeral containers | 100m–1000m CPU | 256Mi–2Gi memory | Debugging, temporary |

### 2.3 Limit Range Interaction with Quotas

- LimitRange defaults fill in when pods don't specify resources
- Quota checks happen after LimitRange defaults are applied
- A pod must fit within both LimitRange (per-pod) and Quota (per-namespace) constraints
- If a pod's requests exceed the LimitRange maximum, it's rejected before quota check

---

## 3. Priority Classes

### 3.1 Priority Class Definitions

Priority classes determine the importance of pods for scheduling and preemption decisions.

| Priority Class | Priority Value | Preemption | Use Case |
|---|---|---|---|
| `critical` | 1,000,000 | Can preempt all others | API server, model server (production) |
| `high` | 100,000 | Can preempt normal and low | Feature pipeline, cache warmer |
| `normal` | 10,000 | Can preempt low | Batch training jobs, data ETL |
| `low` | 1,000 | Cannot preempt | Development workloads, experiments |
| `cluster-critical` | 999,999,999 | Can preempt everything | Core cluster services (DNS, ingress) |

### 3.2 Priority Class Assignment Strategy

| Recommendation System Component | Priority Class | Rationale |
|---|---|---|
| API server (prod) | `critical` | Directly serves user traffic |
| Model server (prod) | `critical` | Core ML inference |
| Feature pipeline (prod) | `high` | Feeds features to model server |
| Redis/Feature cache | `critical` | Foundation for feature serving |
| Batch training | `normal` | Important but can be deferred |
| Data ETL jobs | `normal` | Time-flexible |
| Ephemeral environments | `low` | Disposable, can be evicted |
| Monitoring (Prometheus) | `high` | Must survive to detect issues |

---

## 4. Preemption

### 4.1 How Preemption Works

When a high-priority pod cannot be scheduled due to insufficient resources:

1. Scheduler identifies low-priority pods that can be evicted
2. Evicted pods are terminated gracefully (respecting their PDBs)
3. High-priority pod is scheduled on the freed resources
4. Evicted pod enters `Pending` state and waits for resources

### 4.2 Preemption Rules

| Scenario | Behavior |
|---|---|
| Critical pod can't fit anywhere | Evict normal and low priority pods |
| High pod can't fit anywhere | Evict normal and low priority pods |
| Normal pod can't fit anywhere | Wait for resources (no preemption) |
| PDB blocks eviction | Preemption blocked, pod stays pending |
| Multiple candidates for eviction | Evict lowest priority first, then earliest created |

### 4.3 Preemption Risks for Recommendation Systems

| Risk | Impact | Mitigation |
|---|---|---|
| Feature pipeline evicted by batch job | Model server loses fresh features | Set feature pipeline to `high` priority |
| Monitoring evicted during incident | Blind to ongoing issues | Set monitoring to `high` priority |
| Cascading evictions | Multiple pods evicted simultaneously | PDB limits simultaneous evictions |
| Starvation of low-priority work | Development environments always evicted | Dedicated node pools for low-priority |

### 4.4 Node Affinity with Priority

Use dedicated node pools for critical workloads:

| Node Pool | Instance Type | Priority | Taints |
|---|---|---|---|
| `critical` | r6i.2xlarge | Critical only | `critical=true:NoSchedule` |
| `high` | m6i.xlarge | High and above | None |
| `normal` | m6i.large | Normal and above | None |
| `spot` | m6i.large (spot) | Low only | `spot=true:NoSchedule` |

---

## 5. Quota Monitoring

### 5.1 Metrics to Track

| Metric | Source | Alert Threshold |
|---|---|---|
| Quota utilization per namespace | `kube_resourcequota` | > 80% of any hard limit |
| Pod count per namespace | `kube_resourcequota{resource="pods"}` | > 90% of limit |
| CPU request utilization | `kube_resourcequota{resource="requests.cpu"}` | > 85% |
| Memory request utilization | `kube_resourcequota{resource="requests.memory"}` | > 85% |
| Failed pod creation (quota) | `kube_resourcequota{type="hard"}` increasing | Any increase |

### 5.2 Dashboard Design

- Per-namespace quota utilization heatmap
- Time-series of quota consumption trend
- Resource request vs actual usage comparison
- Top consumers within each namespace
- Quota exhaustion prediction (linear regression on consumption trend)

### 5.3 Quota Alert Actions

| Alert Level | Action |
|---|---|
| 70% utilized | Informational — review consumption patterns |
| 80% utilized | Warning — investigate top consumers, consider increase |
| 90% utilized | Critical — immediate action required, potential deployment failures |
| 95% utilized | Emergency — escalate to platform team |

---

## 6. Right-Sizing Methodology

### 6.1 Vertical Pod Autoscaler (VPA)

VPA analyzes actual resource usage and recommends optimal requests/limits.

**VPA modes:**

| Mode | Behavior | Use Case |
|---|---|---|
| Off (recommendation only) | Generates recommendations, doesn't apply | Initial analysis |
| Initial | Sets requests on pod creation only | Production (no restarts) |
| Auto | Sets requests and may evict pods | Staging/development |

### 6.2 Right-Sizing Process

1. **Collect data**: Run VPA in recommendation-only mode for 2 weeks
2. **Analyze recommendations**: Compare VPA recommendations with current settings
3. **Identify waste**: Find pods where actual usage < 50% of requests
4. **Identify risk**: Find pods where actual usage > 80% of limits
5. **Apply adjustments**: Update resource requests based on P95 usage + 20% buffer
6. **Validate**: Monitor for OOMKill events and throttling after changes
7. **Iterate**: Re-evaluate monthly

### 6.3 Right-Sizing Targets

| Metric | Current State | Target State | Savings |
|---|---|---|---|
| CPU request vs usage ratio | 4:1 | 2:1 | ~50% CPU cost reduction |
| Memory request vs usage ratio | 3:1 | 1.5:1 | ~50% memory cost reduction |
| Node utilization | 30% | 65% | Fewer nodes needed |
| Idle resources | 40% of cluster | 15% of cluster | Significant cost savings |

### 6.4 Continuous Right-Sizing

- Run VPA recommendations weekly
- Generate automated PRs for resource adjustments
- Track right-sizing improvements over time
- Set utilization targets per namespace and enforce via quotas
