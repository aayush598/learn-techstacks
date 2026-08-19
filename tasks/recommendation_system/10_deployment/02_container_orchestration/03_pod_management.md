# Pod Management

Pods are the smallest deployable units in Kubernetes, and for a recommendation system, pod configuration directly impacts latency, reliability, and resource efficiency. A misconfigured pod — missing resource limits, poor shutdown handling, improper scheduling — becomes a production incident waiting to happen. This document covers pod lifecycle, init containers for model loading, sidecar patterns, disruption budgets, graceful shutdown, resource management, and topology constraints.

---

## 1. Pod Lifecycle

### 1.1 Lifecycle Phases

| Phase | Description | Typical Duration | Common Issues |
|---|---|---|---|
| `Pending` | Pod accepted but not yet scheduled | < 30s (normal) | Insufficient resources, node affinity mismatch |
| `Running` | Pod scheduled, at least one container running | Service lifetime | Container crash loops, OOMKilled |
| `Succeeded` | All containers terminated successfully | N/A (batch jobs) | Normal for init and batch workloads |
| `Failed` | At least one container terminated with error | N/A | Application error, image pull failure |
| `Unknown` | Pod status cannot be determined | N/A | Node communication failure |

### 1.2 Container Lifecycle Hooks

| Hook | When | Purpose for Recommendation Systems |
|---|---|---|
| `postStart` | After container creation | Pre-warm model cache, establish connections |
| `preStop` | Before container termination | Drain in-flight requests, deregister from load balancer |

### 1.3 Readiness vs Liveness vs Startup Probes

| Probe | Purpose | Failure Action | Recommendation Service Config |
|---|---|---|---|
| Startup | Detect slow-starting containers | Restart container | `httpGet /startup`, period=10s, failureThreshold=30 |
| Readiness | Traffic routing gate | Remove from Service endpoints | `httpGet /ready`, period=5s, failureThreshold=3 |
| Liveness | Detect deadlocked containers | Restart container | `httpGet /health`, period=10s, failureThreshold=3 |

**Critical:** For ML model servers that load large models on startup, configure `startupProbe` with high `failureThreshold` (30+). Without this, `livenessProbe` kills the container before the model finishes loading.

---

## 2. Init Containers

Init containers run before the main application container starts. For recommendation systems, they serve critical roles.

### 2.1 Model Loading Init Container

| Aspect | Configuration | Rationale |
|---|---|---|
| Image | `python:3.12-slim` | Lightweight, no serving framework needed |
| Command | Download model from S3/GCS | Isolate download logic from serving logic |
| Volume mount | Shared emptyDir for model artifacts | Model file available to main container |
| Resource limit | 2Gi memory, 1 CPU | Model download is I/O bound |
| Restart policy | OnFailure | Retry download on transient errors |

### 2.2 Feature Store Warmup Init Container

- Pre-populate local cache with frequently accessed features
- Validate connectivity to external feature stores
- Run data migration scripts if schema version changed
- Download configuration files from centralized config store

### 2.3 Init Container Ordering

When multiple init containers are needed, they execute sequentially:

1. **Config download**: Fetch latest configuration from config service
2. **Model download**: Download model artifacts from object storage
3. **Schema validation**: Verify model artifact format matches serving framework version
4. **Cache warmup**: Pre-populate feature cache for cold-start performance

### 2.4 Init Container Failure Handling

| Failure Type | Response | User Impact |
|---|---|---|
| Network timeout (model download) | Init container restarts (backoff) | Pod stays in `Pending` |
| Model checksum mismatch | Init container fails, pod restarts | Delayed startup |
| Feature store unreachable | Init container retries (exponential backoff) | Delayed startup |
| All retries exhausted | Pod goes to `Failed` state | Alert fires, no traffic served |

---

## 3. Sidecar Containers

### 3.1 Logging Sidecar

| Aspect | Configuration |
|---|---|
| Purpose | Ship structured logs to centralized logging (ELK, Datadog) |
| Image | Fluentd, Fluent Bit, Vector |
| Volume mount | Shared log directory (emptyDir) |
| Resources | 100m CPU, 128Mi memory |
| Config | Tail application logs, add Kubernetes metadata, forward to aggregator |

### 3.2 Envoy Proxy Sidecar (Service Mesh)

- Handles mTLS encryption between services
- Provides load balancing, circuit breaking, retries
- Emits detailed request metrics without application changes
- Manages service discovery automatically
- Resource cost: ~100m CPU, 128Mi memory per pod

### 3.3 Metrics Exporter Sidecar

For model servers that don't natively expose Prometheus metrics:

- Scrape model server internal metrics endpoint
- Transform into Prometheus-compatible format
- Add Kubernetes metadata labels
- Expose on standard metrics port (9090)

### 3.4 Log Collection Sidecar Costs

| Sidecar Type | CPU Overhead | Memory Overhead | Network Overhead |
|---|---|---|---|
| Logging (Fluent Bit) | 50–100m | 50–100Mi | Minimal |
| Service mesh (Envoy) | 50–100m | 100–128Mi | Latency +2–5ms |
| Metrics exporter | 25–50m | 30–64Mi | Minimal |
| **Total overhead** | **125–250m** | **180–292Mi** | **Varies** |

**Important:** Budget for sidecar overhead when setting resource requests. A "2 CPU, 4Gi" service with 3 sidecars actually needs ~2.25 CPU and ~4.3Gi.

---

## 4. Pod Disruption Budgets

### 4.1 Purpose

PDBs protect against voluntary disruptions (node drains, cluster upgrades, autoscaler scale-downs).

### 4.2 Configuration for Recommendation Systems

| Component | PDB Strategy | minAvailable | maxUnavailable |
|---|---|---|---|
| API server (6 replicas) | Availability-focused | 5 (83%) | 1 |
| Model server (4 replicas) | Availability-focused | 3 (75%) | 1 |
| Feature pipeline (2 replicas) | Tolerance | 1 (50%) | 1 |
| Batch worker (1 replica) | None (single instance) | N/A | N/A |

### 4.3 PDB Best Practices

- Set PDBs before scaling up — retroactive PDB application doesn't protect existing pods
- Use `minAvailable` for critical services (absolute guarantee)
- Use `maxUnavailable` for services with variable replica counts
- Test PDB effectiveness by draining a node during normal operations
- Monitor PDB violations in cluster upgrade dashboards

---

## 5. Graceful Shutdown

### 5.1 SIGTERM Handling

When Kubernetes terminates a pod, it sends SIGTERM to the main process.

**Shutdown sequence:**

1. Pod marked as `Terminating`
2. Removed from Service endpoints (no new traffic)
3. SIGTERM sent to main process
4. Grace period countdown starts (default: 30s)
5. Process should drain in-flight requests and shut down cleanly
6. If process doesn't exit before grace period, SIGKILL is sent

### 5.2 Graceful Shutdown Checklist for ML Services

| Step | Action | Timeout |
|---|---|---|
| 1 | Stop accepting new requests | Immediate |
| 2 | Complete in-flight predictions | 10s |
| 3 | Flush prediction logs to aggregator | 5s |
| 4 | Close model inference session | 5s |
| 5 | Close database connections | 5s |
| 6 | Deregister from service discovery | 2s |
| 7 | Exit process | Remaining time |

### 5.3 preStop Hook

Use `preStop` hook to add a delay before SIGTERM:

- Gives load balancer time to stop routing new traffic
- Typically 5–10 seconds
- Ensures in-flight requests complete
- Critical for avoiding 5xx errors during rolling updates

### 5.4 Termination Grace Period

Set `terminationGracePeriodSeconds` appropriately:

| Component | Recommended Value | Rationale |
|---|---|---|
| API server | 60s | Short-lived requests |
| Model server | 120s | Long-running inferences, model unload |
| Feature pipeline | 300s | May be processing batches |
| Batch workers | 600s | Complete current batch before exit |

---

## 6. Resource Requests and Limits

### 6.1 Resource Configuration

| Resource | Request | Limit | OOMKill Risk |
|---|---|---|---|
| CPU (API server) | 1000m | 2000m | N/A (CPU is compressible) |
| Memory (API server) | 2Gi | 4Gi | Yes if exceeded |
| CPU (Model server) | 2000m | 4000m | N/A |
| Memory (Model server) | 8Gi | 16Gi | Yes — must accommodate model + working set |
| CPU (Feature pipeline) | 500m | 1000m | N/A |
| Memory (Feature pipeline) | 1Gi | 2Gi | Yes |

### 6.2 Request vs Limit Guidelines

- **Requests** should reflect actual usage (P95) to enable efficient scheduling
- **Limits** should be 2× requests for memory (headroom for spikes), 2× for CPU
- CPU limits cause throttling — prefer Burstable QoS with generous CPU limits
- Memory limits cause OOMKill — set limit = request for Guaranteed QoS on critical services
- Use VPA (Vertical Pod Autoscaler) recommendations to right-size over time

### 6.3 Quality of Service Classes

| QoS Class | Configuration | Guaranteed? | Eviction Priority |
|---|---|---|---|
| Guaranteed | request = limit for CPU and memory | Last to be evicted | Lowest |
| Burstable | request < limit | Middle | Medium |
| BestEffort | No requests or limits | First to be evicted | Highest |

**Recommendation:** Run API server and model server as `Guaranteed` QoS. Run batch workers as `Burstable` or `BestEffort`.

---

## 7. Topology Spread Constraints

### 7.1 Purpose

Topology spread constraints ensure pods are distributed across failure domains (nodes, zones, regions).

### 7.2 Configuration for Multi-AZ Deployment

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app.kubernetes.io/component: api-server
```

### 7.3 Spread Strategies

| Strategy | maxSkew | topologyKey | whenUnsatisfiable | Use Case |
|---|---|---|---|---|
| Strict zone spread | 1 | zone | DoNotSchedule | API server, model server |
| Prefer zone spread | 1 | zone | ScheduleAnyway | Feature pipeline |
| Node spread | 1 | hostname | ScheduleAnyway | All services (anti-affinity) |
| Region spread | 1 | region | DoNotSchedule | Multi-region deployment |

### 7.4 Anti-Affinity vs Topology Spread

| Feature | Pod Anti-Affinity | Topology Spread |
|---|---|---|
| Distribution guarantee | Binary (same or different topology) | Skew-based (quantitative) |
| Flexibility | Rigid | Tunable via maxSkew |
| Scheduling efficiency | Can cause Pending pods | Graceful degradation |
| Recommended for | Critical pods (1 per node) | General distribution |
