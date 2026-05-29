# Section 04: Service Mesh (Istio/Linkerd)

## Service Mesh Architecture

The service mesh provides a **dedicated infrastructure layer** for handling service-to-service communication, security, observability, and traffic management. It offloads these concerns from application code to a sidecar proxy.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      SERVICE MESH ARCHITECTURE                        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CONTROL PLANE (Istiod)                       │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Pilot    │  │ Citadel  │  │ Galley   │  │ Sidecar  │        │    │
│  │  │ (Service │  │ (mTLS   │  │ (Config  │  │ Injector │        │    │
│  │  │  Discov.)│  │  Certs)  │  │  Mgmt)   │  │          │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    DATA PLANE (Envoy Sidecars)                   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Pod: call-service-7d9f8c6b4f-xk9lq                     │   │    │
│  │  │  ┌──────────────┐     ┌──────────────┐                  │   │    │
│  │  │  │  application  │────▶│  Envoy Proxy │───────────────── │   │    │
│  │  │  │  (Node.js)   │     │  (sidecar)  │                  │   │    │
│  │  │  └──────────────┘     └──────────────┘                  │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Pod: voice-service-8b2e9d7c5f-yh3mn                     │   │    │
│  │  │  ┌──────────────┐     ┌──────────────┐                  │   │    │
│  │  │  │  application  │────▶│  Envoy Proxy │◀──────────────── │   │    │
│  │  │  │  (Python)    │     │  (sidecar)  │  Mutual TLS       │   │    │
│  │  │  └──────────────┘     └──────────────┘                  │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    SERVICE MESH CAPABILITIES                    │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Traffic     │  │  Security    │  │  Observability│         │    │
│  │  │  Management  │  │              │  │               │         │    │
│  │  │              │  │              │  │               │         │    │
│  │  │ • Load       │  │ • mTLS       │  │ • Metrics     │         │    │
│  │  │   Balancing  │  │ • Auth       │  │   (Prometheus)│         │    │
│  │  │ • Canary     │  │ • RBAC       │  │ • Logging     │         │    │
│  │  │ • Circuit    │  │ • SPIFFE     │  │   (Loki)      │         │    │
│  │  │   Breaking   │  │   Identity   │  │ • Tracing     │         │    │
│  │  │ • Retry/     │  │ • Secret     │  │   (Tempo)     │         │    │
│  │  │   Timeout    │  │   Rotation   │  │ • Access Logs │         │    │
│  │  │ • Mirroring  │  │              │  │               │         │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Istio Configuration

```yaml
# istio-config.yaml — Service mesh configuration

# Enable sidecar injection for the voice platform namespace
apiVersion: v1
kind: Namespace
metadata:
  name: voice-platform
  labels:
    istio-injection: enabled
---
# VirtualService — Traffic routing with canary deployments
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: call-service
  namespace: voice-platform
spec:
  hosts:
    - call-service
  http:
    - match:
        - headers:
            x-canary:
              exact: "v2"
      route:
        - destination:
            host: call-service
            subset: v2
          weight: 100
    - route:
        - destination:
            host: call-service
            subset: v1
          weight: 90
        - destination:
            host: call-service
            subset: v2
          weight: 10
    # Retry configuration
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: "connect-failure,refused-stream,unavailable,cancelled"
    # Timeout
    timeout: 10s
---
# DestinationRule — Circuit breaking and load balancing
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: call-service
  namespace: voice-platform
spec:
  host: call-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
---
# PeerAuthentication — mTLS enforcement
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: voice-platform
spec:
  mtls:
    mode: STRICT  # STRICT | PERMISSIVE | DISABLE
---
# AuthorizationPolicy — Service-level access control
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: call-service-authz
  namespace: voice-platform
spec:
  selector:
    matchLabels:
      app: call-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/voice-platform/sa/call-service"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/*"]
    - from:
        - source:
            namespaces: ["voice-platform"]
      to:
        - operation:
            methods: ["GET"]
            paths: ["/healthz", "/metrics"]
```

## mTLS and SPIFFE Identity

```typescript
// Service-to-service identity using SPIFFE (via Istio)
// Every pod has a unique identity: spiffe://cluster.local/ns/voice-platform/sa/call-service

// Accessing service identity from application
export function getServiceIdentity(): string {
  // Injected by Istio sidecar
  return process.env.SPIFFE_IDENTITY
    ?? `spiffe://cluster.local/ns/${process.env.NAMESPACE}/sa/${process.env.SERVICE_ACCOUNT}`
}

// Making mTLS requests (automatic with sidecar)
// The Envoy sidecar automatically handles mTLS handshake
// Application code just makes plain HTTP requests

export async function makeInternalRequest(
  service: string,
  path: string,
  options?: RequestInit
): Promise<Response> {
  // No TLS configuration needed — Envoy sidecar handles it
  const url = `http://${service}.voice-platform.svc.cluster.local${path}`

  const response = await fetch(url, {
    ...options,
    headers: {
      ...options?.headers,
      'X-Request-Id': crypto.randomUUID(),
      'X-Service-Name': process.env.SERVICE_NAME ?? 'unknown'
    },
    signal: AbortSignal.timeout(5000)
  })

  return response
}
```

## Circuit Breaking Pattern

```typescript
// Application-level circuit breaker (backup to Istio's outlier detection)
// Useful for non-HTTP protocols (Kafka, gRPC)

export class CircuitBreaker {
  private state: 'closed' | 'open' | 'half-open' = 'closed'
  private failureCount = 0
  private successCount = 0
  private lastFailureTime = 0
  private readonly threshold: number
  private readonly recoveryTimeout: number
  private readonly halfOpenMaxSuccess: number

  constructor(options: {
    threshold?: number      // Failures before opening circuit
    recoveryTimeout?: number // ms before trying half-open
    halfOpenMaxSuccess?: number // Successes to close circuit
  } = {}) {
    this.threshold = options.threshold ?? 5
    this.recoveryTimeout = options.recoveryTimeout ?? 30000
    this.halfOpenMaxSuccess = options.halfOpenMaxSuccess ?? 3
  }

  async call<T>(fn: () => Promise<T>, fallback: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailureTime > this.recoveryTimeout) {
        this.state = 'half-open'
        logger.info('Circuit half-open, allowing trial request')
      } else {
        logger.warn('Circuit open, using fallback')
        return fallback()
      }
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      if (this.state === 'half-open') {
        this.state = 'open'
        this.lastFailureTime = Date.now()
      }
      return fallback()
    }
  }

  private onSuccess() {
    if (this.state === 'half-open') {
      this.successCount++
      if (this.successCount >= this.halfOpenMaxSuccess) {
        this.state = 'closed'
        this.failureCount = 0
        this.successCount = 0
        logger.info('Circuit closed after recovery')
      }
    }
    this.failureCount = 0
  }

  private onFailure() {
    this.failureCount++
    this.lastFailureTime = Date.now()

    if (this.failureCount >= this.threshold) {
      this.state = 'open'
      logger.error('Circuit opened due to failures', { failures: this.failureCount })
    }
  }
}
```

## Observability with Service Mesh

```yaml
# Telemetry configuration
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  accessLogging:
    - providers:
        - name: envoy
  metrics:
    - providers:
        - name: prometheus
  tracing:
    - providers:
        - name: zipkin  # Compatible with Tempo
      randomSamplingPercentage: 10.0  # Sample 10% of requests
      customTags:
        service.name:
          literal:
            value: "voice-platform"
```

## Linkerd as Alternative

```yaml
# Linkerd configuration (lighter alternative to Istio)
# Linkerd is simpler, faster, but has fewer features

# Install
# linkerd install | kubectl apply -f -

# mTLS
# linkerd check --pre
# linkerd inject deployment/call-service

# Service profile for retries and timeouts
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: call-service.voice-platform.svc.cluster.local
  namespace: voice-platform
spec:
  routes:
    - condition:
        method: POST
        pathRegex: /api/v1/calls
      isRetryable: true
      retries:
        budget:
          minRetriesPerSecond: 10
          retryRatio: 0.2
      timeout: 10s
```

## Istio vs Linkerd Comparison

| Feature | Istio | Linkerd |
|---------|-------|---------|
| Proxy | Envoy (powerful) | Linkerd-proxy (lightweight) |
| CPU Overhead | ~15-20% | ~5-10% |
| Memory per Proxy | ~50MB | ~10MB |
| Feature Set | Traffic mirroring, fault injection, WASM | Circuit breaking, retry, timeout |
| Complexity | High | Low |
| mTLS | ✓ | ✓ |
| Multi-Cluster | ✓ | Via extension |
| API Gateway | Ingress Gateway | Independent (NGINX) |
| Community | Large, CNCF graduated | CNCF graduated |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Service Mesh | Istio (primary) | Feature-rich, full control plane |
| mTLS Mode | STRICT (reject plaintext) | Defense in depth, compliance |
| Circuit Breaking | Istio outlier detection + app-level breaker | Double protection |
| Canary Deployments | Istio VirtualService weight routing | Gradual rollout with observability |
| Proxy Resources | CPU: 500m, Memory: 128Mi | Balanced for voice platform workload |

## Integration Points

- **Part 23 (DevOps/CI-CD)** — Service mesh deployed with Istio operator
- **Part 15 (Security)** — mTLS enforced by service mesh
- **Part 24 (Scaling)** — Service mesh metrics drive auto-scaling
- **Part 01 (Observability)** — Mesh generates rich telemetry

## Production Considerations

- **Resource Overhead**: Each sidecar adds ~50MB RAM; for 100 pods = 5GB additional
- **Startup Delay**: Sidecar injection adds 2-5s to pod startup
- **Debugging**: Use `istioctl proxy-status` and `istioctl dashboard` for troubleshooting
- **Upgrade Strategy**: Canary upgrade the control plane before data plane
- **Egress Controls**: Restrict egress traffic with ServiceEntry and Sidecar resources
- **Cost**: Istio is free (open-source), but the additional resource consumption has a cost
