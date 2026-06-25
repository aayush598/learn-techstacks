# Netflix, Uber, Lyft — OS Topics Interview Guide

## Netflix

### Infrastructure
- **FreeBSD → Linux migration** (2015): moved from FreeBSD to Ubuntu Linux on AWS
- **AWS EC2 + EBS + S3** as primary infrastructure
- **Open Connect CDN:** FreeBSD-based appliances in ISP networks (caching)

### OS + Performance Topics
| Topic | Details |
|-------|---------|
| **EVCache** | Distributed cache (memcached-based, read-heavy) |
| **mTLS** | Encrypted traffic at scale — performance overhead |
| **Hystrix** | Circuit breaker pattern (fault tolerance, thread pool isolation) |
| **Eureka** | Service registry (heartbeat-based health checks) |
| **Zuul** | API gateway (filter chain, async) → Zuul 2 (Netty-based) |

### Performance Engineering
- **I/O performance:** network-bound at CDN edge; disk-bound in storage
- **CPU tuning:** NUMA, huge pages, CPU governor (performance mode)
- **Linux kernel tuning:** `net.core.somaxconn`, `tcp_tw_reuse`, backlog sizing
- **Chaos Engineering:** Chaos Monkey, Chaos Kong (simulate AZ failure)

## Uber

### Distributed Systems
- **Dispatch system:** real-time (needs low latency, high availability)
- **Ringpop:** consistent hashing for distributed systems (Node.js)
  - Uses **SWIM** gossip protocol for membership
- **TChannel:** RPC framework (multiplexed, request/response)

### Storage
- **Schemaless:** MySQL-based document store (schema-less but sharded)
  - Key features: sharding, replication, automatic failover
- **Docstore:** successor to Schemaless (improved consistency)
- **Uber's MySQL fork:** `mysql-5.6` with custom patches

### Real-Time Challenges
- **Geospatial indexing:** H3 (hexagonal hierarchical spatial index)
  - OS relevance: memory-efficient data structures, mmap-based storage
- **Dispatch optimization:** pathfinding, ETA (Dijkstra, contraction hierarchies)
- **Microservices at scale:** 2000+ services → monitoring, tracing (Jaeger)

## Lyft

### Envoy Proxy
- **Service mesh proxy** (C++ implementation)
  - L4/L7 proxy: TCP, HTTP, gRPC, MongoDB, etc.
  - **Thread model:** single process, multiple worker threads
  - **Hot restart:** seamless binary upgrade (shared memory via mmap)
- **Listener** → filter chain → **cluster** (consistent hashing, EDS)

### Lyft's OS Relevance
- **gRPC:** HTTP/2-based RPC (multiplexed, streaming)
  - OS relevance: epoll, connection multiplexing, flow control
- **Distributed tracing:** Jaeger (open-source, Uber + Lyft contrib)
- **Service mesh:** sidecar container per service (Envoy intercepts all traffic)
- **Open source:** `envoy`, `jaeger`, `gRPC`

## Common Themes

| Topic | Netflix | Uber | Lyft |
|-------|---------|------|------|
| **Async I/O** | Zuul 2 (Netty) | TChannel | Envoy (event-driven) |
| **Caching** | EVCache (memcached) | Redis, memcached | Redis |
| **Service Mesh** | Internal | Internal | Envoy |
| **Observability** | Atlas, Spinnaker | Jaeger, M3 | Jaeger, Envoy stats |
| **Scaling** | Chaos Engineering | Ringpop, SWIM | gRPC, Envoy |

## Interview Tips
- *"Netflix: performance engineering is culture — every microsecond counts"*
- *"Uber: real-time dispatch requires low-latency distributed consensus"*
- *"Lyft: Envoy is a high-performance C++ proxy — understand its threading model"*
- *"Service mesh is the future: Envoy + gRPC is becoming industry standard"*
- *"All three are heavy AWS users — know EBS/ENA/EC2 performance tuning"*
