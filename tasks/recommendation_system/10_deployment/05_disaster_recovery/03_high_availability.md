# High Availability

High availability (HA) ensures a recommendation system remains operational despite component failures. For a system serving millions of users generating billions of recommendations daily, even minutes of downtime translate to significant revenue loss and user trust erosion. HA is not a feature you add — it's an architectural decision made at every layer. This document covers multi-AZ deployment, multi-region active-active, redundancy patterns, replication strategies, consensus protocols, and availability calculation.

---

## 1. Multi-AZ Deployment

### 1.1 Why Multi-AZ

Cloud providers run multiple isolated availability zones (AZs) per region. Each AZ has independent power, networking, and cooling. Deploying across AZs protects against:

- Single AZ power failure
- Single AZ network partition
- Single AZ hardware failure
- Single AZ natural disaster (rare but possible)

### 1.2 Multi-AZ Architecture for Recommendation Systems

| Component | AZ Distribution | Strategy |
|---|---|---|
| API servers | 3 AZs (2+ per AZ) | Spread across AZs, PDB ensures availability |
| Model servers | 3 AZs (1+ per AZ) | Spread across AZs, autoscaling |
| PostgreSQL | Primary in AZ-1, replica in AZ-2, standby in AZ-3 | Synchronous replication to AZ-2, async to AZ-3 |
| Redis | Primary in AZ-1, replica in AZ-2 | Synchronous replication |
| Kafka | Brokers spread across 3 AZs | Replication factor 3, min.insync.replicas=2 |
| Load balancer | Regional (cross-AZ) | Automatic AZ failover |
| S3/Cloud Storage | Regional (AZ-independent) | Automatic replication |

### 1.3 AZ Failure Impact

| Failure | Multi-AZ Impact | Single-AZ Impact |
|---|---|---|
| 1 AZ down | ~33% capacity reduction, service continues | Complete outage |
| 2 AZs down | ~66% capacity reduction, degraded service | Complete outage |
| Cross-AZ latency spike | Increased latency, may trigger circuit breakers | N/A |

### 1.4 Kubernetes Multi-AZ Configuration

| Setting | Configuration | Purpose |
|---|---|---|
| Topology spread | `maxSkew: 1` across `topology.kubernetes.io/zone` | Even pod distribution |
| PodDisruptionBudget | `minAvailable: 83%` | Survive 1 AZ loss |
| Node affinity | Spread node pools across AZs | No AZ concentration |
| PVC topology | `WaitForFirstConsumer` | Volumes in same AZ as pod |

---

## 2. Multi-Region Active-Active

### 2.1 Active-Active vs Active-Passive

| Dimension | Active-Active | Active-Passive |
|---|---|---|
| Traffic | Serves traffic from all regions | Serves traffic from one region only |
| Failover time | Near-zero (traffic routing change) | Minutes (DNS + cold standby) |
| Cost | 2x (full capacity in each region) | 1.5x (warm standby) |
| Complexity | High (data replication, consistency) | Medium (backup + restore) |
| Data consistency | Eventual consistency challenge | Simpler (single writer) |
| Best for | Global user base, < 100ms latency requirement | Regional user base, RPO > 0 acceptable |

### 2.2 Active-Active Architecture

| Layer | Implementation | Consistency Model |
|---|---|---|
| Traffic routing | Global load balancer (Cloudflare, Route53) | N/A |
| API servers | Full stack in each region | Stateless (no consistency issue) |
| Model serving | Independent model copies per region | Eventually consistent (model artifacts sync) |
| Feature store | Cross-region replication | Eventual consistency (seconds) |
| User profiles | Multi-region database (CockroachDB, Spanner) | Strong consistency |
| Event streaming | Kafka MirrorMaker 2 | Eventual consistency (sub-second) |
| Object storage | Cross-region replication (S3 CRR) | Eventual consistency (minutes) |

### 2.3 Data Consistency Challenges

| Data Type | Consistency Need | Challenge |
|---|---|---|
| User preferences | Strong (write-once, read-many) | Cross-region replication lag |
| Interaction events | Eventual (append-only) | Ordering across regions |
| Feature values | Eventual (time-series) | Stale features in some regions |
| Model artifacts | Eventual (large files) | Transfer time for large models |
| Experiment allocation | Strong (consistent bucketing) | User may be in different buckets per region |

### 2.4 Conflict Resolution for Active-Active

| Strategy | Use Case | Trade-off |
|---|---|---|
| Region affinity | User always routed to same region | Doesn't handle region failure gracefully |
| Last-writer-wins | Simple event data | May lose recent writes during conflict |
| CRDTs | Counter-based metrics, sets | Limited data type support |
| Application-level merge | Complex business logic | Implementation complexity |

---

## 3. Redundancy Patterns

### 3.1 Pattern Comparison

| Pattern | Description | Availability | Cost | Use Case |
|---|---|---|---|---|
| **N+1** | N active + 1 standby | Withstands 1 failure | 1/N overhead | Most services |
| **N+N** | 2 full copies | Withstands 1 complete failure | 100% overhead | Critical databases |
| **N+M** | N active + M standbys | Withstands M failures | M/N overhead | Large-scale systems |
| **Active-Active** | All instances serve traffic | Withstands any single failure | 100% overhead (2N) | Global services |

### 3.2 Recommendation System Redundancy

| Component | Pattern | Instances | Justification |
|---|---|---|---|
| API servers | N+M (4+2) | 6 total | High throughput, stateless |
| Model servers | N+1 (4+1) | 5 total | Memory-intensive, stateless |
| PostgreSQL | N+N (1+1) | Primary + replica | Stateful, critical |
| Redis | N+1 (1+1) | Primary + replica | Stateful, moderate criticality |
| Feature pipeline | N+1 (1+1) | 2 total | Stateless workers |
| Kafka | N+M (3+0) | 3 brokers | Replication provides redundancy |

### 3.3 Redundancy vs Efficiency Trade-off

| Redundancy Level | Cost Multiplier | Availability |
|---|---|---|
| No redundancy (N) | 1.0x | 1 - (failure_rate)^N |
| N+1 | 1 + 1/N | Much higher |
| N+2 | 1 + 2/N | Even higher |
| 2N (Active-Active) | 2.0x | Highest practical |

---

## 4. Replication Strategies

### 4.1 Synchronous Replication

| Aspect | Configuration |
|---|---|
| How it works | Write completes only after replica confirms receipt |
| Consistency | Strong (no data loss on failover) |
| Latency impact | +1–5ms (cross-AZ), +10–50ms (cross-region) |
| Availability impact | If replica is down, write fails |
| Best for | Financial data, user account changes |

### 4.2 Asynchronous Replication

| Aspect | Configuration |
|---|---|
| How it works | Write completes immediately, replica catches up later |
| Consistency | Eventual (data loss possible on failover) |
| Latency impact | None (write returns immediately) |
| Availability impact | Write succeeds even if replica is down |
| Best for | Interaction events, feature snapshots, logs |

### 4.3 Semi-Synchronous Replication

| Aspect | Configuration |
|---|---|
| How it works | Write completes after at least one replica confirms |
| Consistency | Strong if at least one replica is available |
| Latency impact | +1–5ms (same AZ) |
| Availability impact | Degrades to async if no replica available |
| Best for | PostgreSQL primary/replica (recommended default) |

### 4.4 Replication Topology

| Topology | Description | Pros | Cons |
|---|---|---|---|
| Chain | A → B → C | Simple | Slowest (C is 2 hops behind) |
| Tree | A → B, A → C | Fast for 2 replicas | Imbalanced if more replicas |
| Star | A → B, A → C, A → D | Fastest (all replicas close to primary) | Primary is bottleneck |
| Ring | A → B → C → A | Balanced | Complex failure modes |

---

## 5. Quorum-Based Consensus

### 5.1 What is Quorum

Quorum is the minimum number of nodes that must agree for a distributed operation to proceed.

### 5.2 Quorum in Practice

| System | Quorum Mechanism | Configuration |
|---|---|---|
| etcd | Raft consensus | 3 or 5 nodes, majority required |
| Kafka | ISR (In-Sync Replicas) | `min.insync.replicas=2`, `acks=all` |
| PostgreSQL (Patroni) | DCS (etcd/Consul/ZooKeeper) | 3 DCS nodes, 2 for leader election |
| Redis Sentinel | Sentinel quorum | 3 sentinels, 2 for failover |

### 5.3 Quorum Rules

For a cluster of N nodes:

| Property | Formula | Example (N=5) |
|---|---|---|
| Quorum size | floor(N/2) + 1 | 3 |
| Fault tolerance | floor((N-1)/2) | 2 |
| Maximum writes without quorum | 0 | 0 |
| Network partitions handled | 1 partition with majority | Yes |

### 5.4 CAP Theorem Implications

| Property | Recommendation System Choice | Rationale |
|---|---|---|
| **C**onsistency vs **A**vailability | Availability over consistency (mostly) | Users prefer slightly stale recommendations over errors |
| **P**artition tolerance | Required (network partitions happen) | Must handle network splits |
| AP system | Prefer availability + eventual consistency | Most recommendation data is tolerant of staleness |
| CP system | Use for critical data (user profiles, billing) | Strong consistency needed |

---

## 6. Availability Calculation

### 6.1 Mathematical Framework

For independent components in series (all must work):

```
System Availability = A₁ × A₂ × A₃ × ... × Aₙ
```

For redundant components in parallel (at least one must work):

```
System Availability = 1 - (1 - A₁) × (1 - A₂) × ... × (1 - Aₙ)
```

### 6.2 Availability Examples

| Component | Individual Availability | Redundancy | Effective Availability |
|---|---|---|---|
| API server (1 instance) | 0.999 (99.9%) | N/A | 0.999 |
| API server (2 instances) | 0.999 | N+1 | 0.999999 (99.9999%) |
| PostgreSQL (single) | 0.999 | N/A | 0.999 |
| PostgreSQL (primary + replica) | 0.999 | N+1 | 0.999999 |
| Redis (single) | 0.999 | N/A | 0.999 |
| Redis (primary + replica) | 0.999 | N+1 | 0.999999 |

### 6.3 End-to-End System Availability

A recommendation system with serial dependencies:

| Chain | Availability | Redundancy | Effective |
|---|---|---|---|
| Load balancer | 0.9999 | Built-in HA | 0.9999 |
| API servers | 0.999 | 3 replicas | 0.999999 |
| Feature store | 0.999 | Primary + replica | 0.999999 |
| Model server | 0.999 | 2 replicas | 0.999999 |
| Database | 0.999 | Primary + replica | 0.999999 |
| **End-to-end** | | | **0.999 × 0.999999⁴ ≈ 0.999** |

**Key insight:** The weakest link in a serial chain determines overall availability. Even with redundant components at every layer, a single non-redundant dependency (e.g., a shared config store) can limit system availability.

### 6.4 SLA Targets

| Availability Level | Downtime per Year | Downtime per Month | Typical SLA |
|---|---|---|---|
| 99.9% (three 9s) | 8.76 hours | 43.8 minutes | Standard |
| 99.95% | 4.38 hours | 21.9 minutes | Good |
| 99.99% (four 9s) | 52.6 minutes | 4.38 minutes | Excellent |
| 99.999% (five 9s) | 5.26 minutes | 26.3 seconds | World-class |

### 6.5 Availability Improvement Priorities

| Priority | Improvement | Impact | Cost |
|---|---|---|---|
| 1 | Remove single points of failure | Highest | Medium |
| 2 | Add redundancy at weakest link | High | Medium |
| 3 | Implement automated failover | High | Medium |
| 4 | Multi-AZ deployment | Medium | Medium |
| 5 | Multi-region deployment | Medium | High |
