# Service Discovery for Recommendation Systems

## 1. Service Discovery Fundamentals

### 1.1 Why Service Discovery
In a microservices architecture, services are dynamically scaled and their network locations change frequently. Service discovery enables:
- **Dynamic Registration**: Services register themselves when they start
- **Dynamic Lookup**: Clients discover service locations at runtime
- **Health Awareness**: Unhealthy instances are removed from discovery
- **Load Distribution**: Multiple instances registered for load balancing

### 1.2 Discovery Patterns

**Client-Side Discovery**:
- Client queries service registry directly
- Client selects instance using load balancing algorithm
- Examples: Eureka + Ribbon, Consul + custom resolver
- Pros: No additional network hop; client controls selection
- Cons: Client complexity; client must implement discovery logic

**Server-Side Discovery**:
- Client makes request to load balancer/load balancer queries registry
- Load balancer selects instance and forwards request
- Examples: Kubernetes Services, AWS ELB, NGINX
- Pros: Simple client; centralized load balancing logic
- Cons: Additional network hop; load balancer is potential bottleneck

**DNS-Based Discovery**:
- Service instances registered as DNS records
- Client resolves DNS to get service addresses
- Examples: Kubernetes CoreDNS, Consul DNS
- Pros: Universal support; no client changes needed
- Cons: DNS caching can cause stale data; limited health check info

---

## 2. Kubernetes-Native Service Discovery

### 2.1 Kubernetes Services
- **ClusterIP**: Internal service access within cluster
- **NodePort**: Expose service on node ports
- **LoadBalancer**: External load balancer integration
- **Headless**: Direct pod IP resolution for StatefulSets

### 2.2 Service Types for Recommendation Services

| Service | Type | Reasoning |
|---|---|---|
| API Gateway | LoadBalancer | External access required |
| Candidate Generation | ClusterIP | Internal service only |
| Ranking Service | ClusterIP | Internal service only |
| Feature Store (Redis) | Headless | Direct pod access for cluster mode |
| Model Serving | ClusterIP | Internal service only |
| Monitoring | NodePort/LoadBalancer | Dashboard access needed |

### 2.3 Service Mesh Discovery
- **Istio**: Pilot manages service discovery; Envoy sidecar handles routing
- **Linkerd**: Destination service provides discovery; proxy handles routing
- **Benefits**: Automatic mTLS, traffic management, observability integrated with discovery

---

## 3. External Service Discovery

### 3.1 Consul
- **Key-Value Store**: Store service metadata and configuration
- **Health Checks**: HTTP, TCP, script-based health checks
- **Service Mesh**: Consul Connect for mTLS between services
- **DNS Interface**: DNS-based discovery for non-Consul-aware clients
- **Multi-Datacenter**: Built-in WAN federation for multi-DC

### 3.2 etcd
- **Strong Consistency**: Raft consensus for consistent service registry
- **Watch API**: Watch for service registration changes
- **Kubernetes Backend**: etcd is Kubernetes' backing store
- **Simplicity**: Fewer features than Consul but simpler to operate

### 3.3 ZooKeeper
- **Proven at Scale**: Used by Kafka, HBase, and other distributed systems
- **Ephemeral Nodes**: Services register as ephemeral nodes; auto-removed on disconnect
- **Sequential Nodes**: For leader election among service instances
- **Complex Operation**: Historically complex to operate; less common for new deployments

---

## 4. Health Check Design

### 4.1 Health Check Types
- **Liveness Check**: Is the process alive? Restart if no.
- **Readiness Check**: Is the service ready to accept traffic? Remove from load balancer if no.
- **Startup Check**: Has the service finished initialization? Critical for model loading.

### 4.2 Health Check Configuration for ML Services
```yaml
readiness_probe:
  httpGet:
    path: /health/ready
    port: 8080
  initial_delay_seconds: 30    # Allow time for model loading
  period_seconds: 10
  timeout_seconds: 5
  failure_threshold: 3

liveness_probe:
  httpGet:
    path: /health/live
    port: 8080
  initial_delay_seconds: 60    # Longer delay for ML services
  period_seconds: 15
  timeout_seconds: 5
  failure_threshold: 3

startup_probe:
  httpGet:
    path: /health/started
    port: 8080
  initial_delay_seconds: 10
  period_seconds: 5
  failure_threshold: 30       # Allow up to 150s for model loading
```

### 4.3 Health Check Endpoints
- `/health/live` — Returns 200 if process is running
- `/health/ready` — Returns 200 if service can handle requests (model loaded, dependencies available)
- `/health/started` — Returns 200 if initialization complete
- `/health/deep` — Comprehensive check: model loaded, feature store reachable, cache available
- `/health/model` — Check model version and freshness

### 4.4 Health Check Response
```json
{
  "status": "healthy",
  "version": "1.2.3",
  "model_version": "v4.2.1",
  "model_age_hours": 6.5,
  "dependencies": {
    "feature_store": "healthy",
    "model_serving": "healthy",
    "cache": "healthy"
  },
  "uptime_seconds": 86400,
  "requests_served": 1234567
}
```

---

## 5. Load Balancing Algorithms

### 5.1 Algorithms for Recommendation Services

**Round Robin**:
- Distribute requests evenly across instances
- Good for: Stateless services with uniform request cost
- Use case: API Gateway, User Profile Service

**Least Connections**:
- Route to instance with fewest active connections
- Good for: Services with variable request processing time
- Use case: Model Serving (inference time varies by model and input)

**Consistent Hashing**:
- Hash request key to determine instance
- Good for: Cache-friendly routing; user affinity
- Use case: Feature Store (cache locality), Model Serving (user-specific caching)

**Weighted Round Robin**:
- Route based on instance capacity (e.g., GPU vs CPU instances)
- Good for: Heterogeneous instance pools
- Use case: Mixed GPU/CPU model serving clusters

**Random**:
- Randomly select instance
- Good for: Simple load balancing with large instance counts
- Use case: Internal service mesh default

### 5.2 Recommendation-Specific Load Balancing
- **User Affinity**: Route same user to same instance for cache locality (consistent hashing by user_id)
- **GPU Affinity**: Route large model inference to GPU instances; small models to CPU instances
- **Context Affinity**: Route batch requests to dedicated batch-serving instances
- **Priority Routing**: Route premium users to higher-capacity instances
