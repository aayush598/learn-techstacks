# Failover Mechanisms

Failover is the process of detecting a component failure and automatically redirecting traffic or operations to a healthy backup. For recommendation systems, failover must cover not just application servers but also databases, caches, model serving endpoints, and feature stores. A recommendation system with a single point of failure is not production-ready. This document covers automatic detection, DNS failover, database failover, cache failover, model serving failover, and split-brain prevention.

---

## 1. Automatic Detection

### 1.1 Health Check Mechanisms

| Check Type | Interval | Timeout | Scope | Failure Threshold |
|---|---|---|---|---|
| Kubernetes liveness probe | 10s | 5s | Pod-level | 3 consecutive failures |
| Kubernetes readiness probe | 5s | 3s | Pod-level | 3 consecutive failures |
| TCP health check | 10s | 5s | Port-level | 3 consecutive failures |
| HTTP health check | 15s | 10s | Application-level | 2 consecutive failures |
| gRPC health check | 10s | 5s | Service-level | 3 consecutive failures |
| Custom deep health check | 30s | 15s | Dependencies (DB, cache, model) | 2 consecutive failures |

### 1.2 Deep Health Check Design

A deep health check verifies all critical dependencies:

| Dependency | Check Method | Fail Action |
|---|---|---|
| PostgreSQL connection | `SELECT 1` with 2s timeout | Mark unhealthy |
| Redis connection | `PING` with 1s timeout | Mark unhealthy |
| Model loaded | Check model version in memory | Mark unhealthy |
| Feature store reachable | Feature retrieval test with 2s timeout | Degrade (use cached) |
| Disk space | Check available disk > 10% | Warn (don't mark unhealthy yet) |

### 1.3 Heartbeat Monitoring

| Pattern | Implementation | Detection Time |
|---|---|---|
| Active heartbeat | Service sends heartbeat every 10s | 30s (3 missed heartbeats) |
| Passive heartbeat | Load balancer tracks last request | 60s (configurable) |
| Consul/TTL health | Service registers with TTL health check | TTL duration (10–30s) |
| Kubernetes watch | Controller watches pod status | Near-instant |

---

## 2. DNS Failover

### 2.1 AWS Route53 Failover

| Record Type | Primary | Secondary | Failover Criteria |
|---|---|---|---|
| A/AAAA | us-east-1 endpoint | us-west-2 endpoint | Health check failure |
| CNAME | Primary ALB | Secondary ALB | Health check failure |
| Alias | Primary Regional | Secondary Regional | Automatic |

**Configuration:**

- Health check: HTTP endpoint, 10s interval, 3 failure threshold
- Failover routing: Primary (us-east-1) → Secondary (us-west-2)
- TTL: 60 seconds (balances failover speed vs DNS load)
- Health checkers: 18 global health check locations (majority must agree)

### 2.2 Cloudflare Load Balancer Failover

| Feature | Configuration |
|---|---|
| Pool assignment | Primary pool (active), secondary pool (failover) |
| Health monitoring | HTTP health check, 60s interval |
| Failover order | Primary → Secondary → Tertiary |
| Steering | Latency-based (within healthy pools) |
| Session affinity | Cookie-based (sticky sessions) |

### 2.3 DNS Failover Timing

| Component | Duration | Cumulative |
|---|---|---|
| Failure detection (health check) | 30–60 seconds | 30–60s |
| DNS propagation | 0–60 seconds (based on TTL) | 30–120s |
| Client DNS cache expiry | 0–60 seconds | 30–180s |
| **Total failover time** | | **30–180 seconds** |

### 2.4 DNS Failover Limitations

- DNS-based failover cannot detect partial failures (service up but degraded)
- TTL caching means some clients continue hitting failed endpoint
- Cannot do sub-second failover (unlike load balancer-level)
- Use as a last resort (region-level failure), not for individual service failover

---

## 3. Database Failover

### 3.1 PostgreSQL Primary Promotion

| Scenario | Detection | Action | Downtime |
|---|---|---|---|
| Primary crash | Replication lag = 0 (no heartbeat) | Promote replica to primary | 10–30 seconds |
| Primary network partition | Quorum-based detection | Promote replica | 10–30 seconds |
| Primary disk failure | I/O error detection | Promote replica + provision new primary | 30–120 seconds |

### 3.2 PostgreSQL HA Topology

| Tool | Approach | Failover Time | Data Loss Risk |
|---|---|---|---|
| PostgreSQL streaming replication + Patroni | Leader election via DCS | 10–30 seconds | 0–10 transactions (async) |
| AWS RDS Multi-AZ | Automatic failover | 60–120 seconds | 0 transactions (sync) |
| AWS RDS Read Replicas | Manual promotion | 60–120 seconds | 0–30 seconds (replication lag) |
| PgBouncer + HAProxy | Connection pooling + health check | 5–10 seconds | 0 transactions |

### 3.3 Failover Data Consistency

| Replication Mode | Data Loss | Failover Speed | Use Case |
|---|---|---|---|
| Synchronous | 0 (zero data loss) | Slower (waits for replica) | Financial, critical data |
| Asynchronous | Up to replication lag | Faster | Most application data |
| Semi-synchronous | 0 (if replica acks) | Moderate | Recommended default |

### 3.4 Post-Failover Steps

1. Verify new primary accepts writes
2. Update connection strings (if using DNS-based discovery)
3. Verify application connectivity to new primary
4. Provision a new replica to restore redundancy
5. Monitor replication lag on new replica
6. Investigate root cause of original primary failure

---

## 4. Cache Failover

### 4.1 Redis Sentinel

| Component | Role | Quantity |
|---|---|---|
| Sentinel | Monitors Redis instances, manages failover | 3+ (odd number for quorum) |
| Primary | Handles writes and reads | 1 |
| Replica | Handles reads, ready for promotion | 1+ |
| Application | Connects via Sentinel, discovers current primary | N/A |

### 4.2 Sentinel Failover Process

1. Sentinel detects primary unreachable (30 seconds)
2. Sentinel confirms with quorum (2 of 3 sentinels agree)
3. Sentinel elects best replica (offset, priority, age)
4. Sentinel promotes replica to primary
5. Sentinel reconfigures other replicas to replicate from new primary
6. Sentinel notifies clients of new primary address
7. Old primary becomes replica when it recovers

**Failover time: 10–30 seconds.**

### 4.3 Redis Cluster Failover

| Feature | Sentinel | Cluster |
|---|---|---|
| Data partitioning | No (single primary) | Yes (16384 slots) |
| Failover scope | Single primary → replica | Per-shard failover |
| Scaling | Vertical | Horizontal (add shards) |
| Complexity | Low | High |
| Best for | Small datasets (< 32GB) | Large datasets (> 32GB) |

### 4.4 Cache Miss During Failover

When the cache is unavailable during failover:

| Strategy | Behavior | Impact |
|---|---|---|
| Degrade to database | Read from PostgreSQL directly | Higher latency (10ms → 50ms) |
| Serve stale cache | Use application-level stale cache | Slightly stale data |
| Return default recommendations | Serve popular/trending items | Less personalized |
| Fail request | Return 503 | User-facing error (worst option) |

---

## 5. Model Serving Failover

### 5.1 Model Server Failure Scenarios

| Scenario | Detection | Failover Action |
|---|---|---|
| Model server pod crash | Kubernetes liveness probe | Pod restart + load balancer removes pod |
| Model inference error rate spike | Prometheus alert (> 5%) | Route to backup model version |
| Model server OOM | Container OOMKilled event | Restart with previous model version |
| Model server overload | Request queue full | Circuit breaker → fallback model |

### 5.2 Model Version Fallback Chain

| Priority | Model Version | Use Case |
|---|---|---|
| 1 (primary) | Latest production model | Normal operation |
| 2 (secondary) | Previous production model | Current model failure |
| 3 (tertiary) | Popular items model | Both primary and secondary fail |
| 4 (emergency) | Static editorial picks | Complete ML system failure |

### 5.3 Hot-Swap Model Failover

When the primary model fails:

1. Load balancer detects error rate increase (30 seconds)
2. Traffic shifted to backup model server pool (immediate)
3. Backup pool serves using previous model version
4. Alert fires for on-call investigation
5. Primary pool is investigated and fixed
6. Traffic gradually shifted back after verification

### 5.4 Model Health Check Design

| Check | Method | Failure Impact |
|---|---|---|
| Model loaded | Verify model artifact in memory | Mark unhealthy |
| Inference working | Run sample prediction | Mark unhealthy |
| Latency acceptable | P95 < 100ms (last 60s) | Mark unhealthy |
| Feature store connected | Test feature retrieval | Degrade (use cached features) |
| Memory within bounds | RSS < 90% of limit | Warn |

---

## 6. Split-Brain Prevention

### 6.1 What is Split-Brain

Split-brain occurs when a network partition causes two nodes to believe they are the primary, leading to conflicting writes and data inconsistency.

### 6.2 Prevention Mechanisms

| Mechanism | Implementation | Trade-off |
|---|---|---|
| Quorum-based election | Majority of nodes must agree (3/5, 2/3) | Requires odd number of nodes |
| Fencing/STONITH | Shoot The Other Node In The Head | Requires ILO/IPMI access |
| Lease-based locking | Time-limited locks in distributed store (etcd, ZooKeeper) | Clock skew sensitivity |
| Pacemaker + Corosync | Cluster communication and membership | Complex setup |

### 6.3 Quorum Calculation

| Cluster Size | Quorum Needed | Fault Tolerance |
|---|---|---|
| 1 node | 1 | 0 (no fault tolerance) |
| 3 nodes | 2 | 1 node failure |
| 5 nodes | 3 | 2 node failures |
| 7 nodes | 4 | 3 node failures |

### 6.4 Split-Brain in Practice

**Scenario: Network partition in Redis Sentinel cluster**

| State | Before Partition | During Partition | After Healing |
|---|---|---|---|
| Primary (AZ-1) | Primary (serves writes) | Believes it's primary (isolated) | Becomes replica (loses data since partition) |
| Replica (AZ-2) | Replica (serves reads) | Promoted to primary (quorum) | Stays primary |
| Sentinels | 3 healthy | 2 in AZ-2 elect new primary | Old primary rejoins as replica |

**Data loss:** Only writes to old primary during the partition window are lost.

### 6.5 Recommendation System Split-Brain Mitigation

| Component | Mitigation | Implementation |
|---|---|---|
| PostgreSQL | Patroni + etcd quorum | Only writable with etcd lease |
| Redis | Sentinel with quorum | 3 sentinels, 2 required for election |
| Model serving | Stateless (no split-brain risk) | Each pod is independent |
| Feature pipeline | Leader election via Kubernetes lease | Only one leader writes to feature store |
| Event ingestion | Kafka partition assignment | Each partition owned by one consumer |
