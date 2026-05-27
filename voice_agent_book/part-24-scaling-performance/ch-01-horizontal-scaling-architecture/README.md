# Chapter 01: Horizontal Scaling Architecture

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Stateless Design Principles](sec-01-stateless-design-principles.md) | Stateless application architecture, externalizing state, session management, idempotency |
| 02 | [Auto-Scaling Groups](sec-02-auto-scaling-groups.md) | Scaling policies, metric-based scaling, scheduled scaling, warm pools, cooldown periods |
| 03 | [Distributed State Management](sec-03-distributed-state-management.md) | Redis for distributed state, state synchronization, conflict resolution, eventual consistency |
| 04 | [Read Replicas Strategy](sec-04-read-replicas-strategy.md) | Read replica architecture, replication lag handling, read/write splitting, failover |
| 05 | [Sharding Strategy](sec-05-sharding-strategy.md) | Horizontal sharding, shard key selection, rebalancing, cross-shard queries |
| 06 | [Service Mesh for Scaling](sec-06-service-mesh-scaling.md) | Service discovery, load balancing, traffic splitting, circuit breaking |
| 07 | [Global Load Balancing](sec-07-global-load-balancing.md) | DNS-based routing, anycast, geographic load balancing, latency-based routing |
| 08 | [Scaling Stateful Services](sec-08-scaling-stateful-services.md) | WebSocket scaling, media server scaling, database scaling, cache cluster scaling |
