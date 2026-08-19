# Service Mesh

A service mesh provides infrastructure-level networking, security, and observability for microservices without requiring application code changes. For recommendation systems with multiple interconnected services — API servers, model servers, feature stores, event processors — a service mesh eliminates cross-cutting concerns scattered across service code. However, service meshes add operational complexity and latency overhead. This document covers Istio architecture, traffic management, security, observability, adoption criteria, and alternatives.

---

## 1. Istio Architecture

### 1.1 Core Components

| Component | Role | Resource Overhead | Failure Impact |
|---|---|---|---|
| Envoy sidecar | Per-pod proxy handling all network traffic | 50–100m CPU, 100–128Mi memory | Pod becomes unreachable |
| istiod (Pilot) | Control plane — configuration distribution, service discovery | 500m CPU, 2Gi memory | No new config propagation |
| istiod (Citadel) | Certificate authority for mTLS | Included in istiod | No new mTLS certs |
| istiod (Galley) | Configuration validation and distribution | Included in istiod | Config validation stops |

### 1.2 Data Plane Architecture

Every pod with the sidecar injection label gets an Envoy proxy injected alongside the application container:

- **Inbound traffic**: Envoy intercepts all inbound connections before they reach the application
- **Outbound traffic**: Envoy intercepts all outbound connections from the application
- **Inter-pod traffic**: Goes through both source and destination Envoy proxies (double hop)
- **Traffic path**: Client → Client Envoy → Server Envoy → Server application

### 1.3 Control Plane Communication

- istiod watches Kubernetes API for service endpoint changes
- Pushes configuration updates to all Envoy proxies via xDS API
- Maintains certificate rotation for mTLS (24-hour cert lifetime by default)
- Configures traffic routing rules, timeout policies, retry policies

---

## 2. Traffic Management

### 2.1 Canary Routing

Istio enables fine-grained traffic splitting without application code changes:

**VirtualService configuration:**

| Destination | Weight | Purpose |
|---|---|---|
| `recommendation-api-stable` | 95% | Current production version |
| `recommendation-api-canary` | 5% | New version under evaluation |

Gradually shift weight: 5% → 25% → 50% → 100% based on automated analysis results.

### 2.2 Traffic Mirroring (Shadow Testing)

Mirror production traffic to a canary without affecting real responses:

- 100% of production traffic is served by the stable version
- 100% of the same traffic is also sent to the canary (shadow)
- Canary processes the request but its response is **discarded**
- Compare canary metrics against stable to evaluate quality
- Zero user impact during evaluation

**Use case:** Test a new model that may significantly change recommendation quality. Shadow testing reveals issues before any users are affected.

### 2.3 Traffic Policies

| Policy | Configuration | Purpose |
|---|---|---|
| Connection pool | `maxConnections: 100`, `maxPendingRequests: 50` | Prevent overload |
| Circuit breaking | `consecutiveErrors: 5`, `interval: 30s` | Stop sending to failing instances |
| Retries | `attempts: 3`, `perTryTimeout: 2s` | Handle transient failures |
| Timeout | `timeout: 10s` | Prevent hanging requests |
| Load balancing | `LEAST_REQUEST` | Distribute load evenly |

### 2.4 Fault Injection (Testing)

Inject faults to test resilience:

- **Delay injection**: Add 500ms delay to 10% of requests to feature store
- **Abort injection**: Return HTTP 503 to 5% of requests to model server
- **Purpose**: Verify that recommendation API degrades gracefully when downstream services fail

---

## 3. Security

### 3.1 Mutual TLS (mTLS)

Istio automatically encrypts all inter-service traffic:

| Aspect | Configuration |
|---|---|
| Mode | `STRICT` in production (rejects non-mTLS connections) |
| Certificate rotation | Every 24 hours (automatic) |
| Certificate authority | Istio Citadel (or external CA integration) |
| Scope | Mesh-wide (all namespaces) |
| Overhead | ~1ms per hop (encryption/decryption) |

### 3.2 Authorization Policies

Control which services can communicate:

| Policy | From | To | Action |
|---|---|---|---|
| API server → model server | `recommendation-api` | `model-server` | ALLOW |
| API server → feature store | `recommendation-api` | `feature-store` | ALLOW |
| External → API server | `*` | `recommendation-api` (port 8080) | ALLOW |
| External → model server | `*` | `model-server` | DENY |
| Default | `*` | `*` | DENY (zero-trust) |

### 3.3 JWT Authentication

- Validate JWT tokens at the Envoy proxy layer
- Extract claims (user ID, roles) and forward as headers to application
- Offload token validation from application code
- Support JWKS endpoint rotation without application restart

### 3.4 Network Policies

Istio authorization policies complement Kubernetes NetworkPolicies:

- NetworkPolicies: L3/L4 enforcement (IP, port)
- Istio policies: L7 enforcement (HTTP methods, paths, headers)
- Use both for defense in depth

---

## 4. Observability

### 4.1 Automatic Metrics

Istio's Envoy proxy generates metrics without application changes:

| Metric Category | Examples | Granularity |
|---|---|---|
| Request metrics | `istio_requests_total`, `istio_request_duration_milliseconds` | Per-route, per-status code |
| Connection metrics | `istio_tcp_connections_opened_total` | Per-source/destination |
| Resource metrics | `envoy_server_memory_allocated` | Per-proxy |
| Pilot metrics | `pilot_xds_pushes`, `pilot_xds_push_time` | Control plane health |

### 4.2 Distributed Tracing

Istio automatically generates trace spans for every request:

- Propagates `traceparent` (W3C) or `x-b3-*` (Zipkin) headers
- Creates spans for each Envoy hop (inbound, outbound)
- Adds application-specific spans via OpenTelemetry SDK
- Sampling rate: 1% in production (configurable per-route)

**Trace structure for a recommendation request:**

```
[API Gateway] → [API Server] → [Feature Store]
                                → [Model Server]
                                → [Result Ranking]
```

### 4.3 Service Topology Visualization

- Kiali dashboard: Real-time service graph with traffic flow
- Jaeger/Tempo: Distributed trace exploration
- Grafana: Pre-built Istio dashboards for mesh health
- Prometheus: Custom queries on Istio metrics

---

## 5. When to Adopt a Service Mesh

### 5.1 Complexity vs Benefit Analysis

| Factor | Mesh Benefit | Mesh Cost | Verdict |
|---|---|---|---|
| Number of services | > 10 services | +10% resource overhead | Benefit if > 10 |
| Inter-service communication | Complex routing needed | Double network hop | Benefit if routing is complex |
| mTLS requirement | Automatic encryption | Certificate management overhead | Benefit (major) |
| Observability gaps | Automatic metrics/tracing | Dashboard maintenance | Benefit if lacking observability |
| Team expertise | Standardizes networking | Learning curve (months) | Cost if team is small |
| Latency sensitivity | < 5ms overhead per hop | Critical for < 50ms P99 | Cost if ultra-low-latency |

### 5.2 Adoption Decision Framework

| Recommendation System Scale | Recommendation |
|---|---|
| < 5 services | **No mesh** — overhead exceeds benefit |
| 5–15 services | **Evaluate** — try on non-critical services first |
| 15–50 services | **Adopt** — clear benefit for networking, security, observability |
| > 50 services | **Essential** — impossible to manage networking manually |

### 5.3 Phased Adoption Strategy

1. Install control plane in dedicated namespace
2. Enable sidecar injection for one non-critical namespace
3. Validate observability improvements (metrics, tracing)
4. Enable mTLS in `PERMISSIVE` mode (accept both mTLS and plain text)
5. Switch to `STRICT` mTLS mode
6. Expand to production namespaces
7. Implement authorization policies (zero-trust)
8. Optimize resource allocation for sidecar proxies

---

## 6. Linkerd Comparison

| Dimension | Istio | Linkerd |
|---|---|---|
| Proxy | Envoy (C++) | linkerd2-proxy (Rust) |
| Resource overhead | ~100m CPU, 128Mi memory | ~20m CPU, 20Mi memory |
| Latency overhead | ~1–3ms per hop | ~0.5–1ms per hop |
| Feature richness | Extensive (traffic management, fault injection, Wasm plugins) | Focused (mTLS, metrics, retries) |
| Operational complexity | High (many CRDs, complex config) | Low (simple, opinionated) |
| Learning curve | Steep (months to master) | Moderate (days to weeks) |
| Control plane | istiod (single binary) | Multiple small components |
| Community | Large (CNCF graduated) | Smaller (CNCF graduated) |

### 6.1 Recommendation

- **Choose Istio** if you need advanced traffic management, Wasm extensibility, or multi-cluster mesh
- **Choose Linkerd** if you want simplicity, lower overhead, and faster time-to-value
- **Choose no mesh** if you have fewer than 10 services and don't need mTLS or advanced traffic management
