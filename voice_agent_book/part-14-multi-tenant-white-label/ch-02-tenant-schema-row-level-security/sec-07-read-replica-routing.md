# Section 07: Read-Replica Tenant Routing

## Overview

In a multi-tenant SaaS platform, read replicas serve a dual purpose: scaling read throughput and providing high availability. Proper tenant-aware read replica routing ensures that each tenant's queries are directed to replicas that have consistent data for that tenant, while avoiding stale reads that could present outdated information. The routing strategy must account for replication lag, tenant isolation, query consistency requirements, and geographic distribution.

PostgreSQL streaming replication creates a lag between the primary and replicas, typically 10-100ms in normal operation. For most read operations in a voice agent platform (listing call history, viewing analytics), this lag is acceptable. However, some operations require strong consistency (reading a call record immediately after creation, checking account balance before placing a call). These operations must be routed to the primary or wait for replica consistency.

Tenant-aware read replica routing adds intelligence to the standard read/write splitting pattern. Instead of randomly distributing reads across replicas, the router considers the tenant's consistency requirements, the replica's replication lag for that tenant's data, and the tenant's geographic region. Enterprise tenants with strict SLA requirements may get dedicated replicas with lower lag targets.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface ReadReplica {
  id: string;
  host: string;
  port: number;
  region: string;
  lag: number; // Current lag in milliseconds
  maxLag: number; // Configured maximum acceptable lag
  weight: number; // For load balancing
}

enum ConsistencyLevel {
  STRONG = 'strong',       // Must read from primary
  SESSION = 'session',     // Must read own writes
  EVENTUAL = 'eventual',   // Any replica is fine
  TIMESTAMP = 'timestamp', // Replica must be caught up to timestamp
}

class TenantAwareReplicaRouter {
  private replicas: ReadReplica[];
  private lagMonitor: LagMonitor;
  private tenantLagCache: RedisCache;

  async getReadConnection(
    tenantId: string,
    consistency: ConsistencyLevel
  ): Promise<PoolClient> {
    switch (consistency) {
      case ConsistencyLevel.STRONG:
        return this.getPrimaryConnection(tenantId);
      
      case ConsistencyLevel.SESSION:
        // Check if this session has pending writes
        if (this.hasPendingWrites(tenantId)) {
          return this.getPrimaryConnection(tenantId);
        }
        return this.getBestReplica(tenantId);
      
      case ConsistencyLevel.EVENTUAL:
        return this.getBestReplica(tenantId);
      
      case ConsistencyLevel.TIMESTAMP:
        const requiredTimestamp = this.getWriteTimestamp(tenantId);
        return this.getReplicaCaughtUpTo(tenantId, requiredTimestamp);
    }
  }

  private async getBestReplica(tenantId: string): Promise<PoolClient> {
    const region = this.getTenantRegion(tenantId);
    
    // Filter replicas by region and lag
    const eligible = this.replicas.filter(r => 
      r.region === region && 
      r.lag <= r.maxLag &&
      this.isTenantReplicaCaughtUp(tenantId, r.id)
    );

    if (eligible.length === 0) {
      // Fall back to cross-region replica or primary
      const crossRegion = this.replicas
        .filter(r => r.lag <= r.maxLag)
        .sort((a, b) => a.lag - b.lag);
      
      if (crossRegion.length > 0) {
        return this.getPoolConnection(crossRegion[0]);
      }
      
      // Ultimate fallback: read from primary
      return this.getPrimaryConnection(tenantId);
    }

    // Weighted random selection among eligible replicas
    const selected = this.weightedRandom(eligible);
    return this.getPoolConnection(selected);
  }

  private async getReplicaCaughtUpTo(
    tenantId: string, 
    timestamp: Date
  ): Promise<PoolClient> {
    const replicas = this.replicas
      .filter(r => r.region === this.getTenantRegion(tenantId))
      .sort((a, b) => a.lag - b.lag);

    for (const replica of replicas) {
      const lastApplied = await this.getReplicaLastApplied(replica.id);
      if (lastApplied >= timestamp) {
        return this.getPoolConnection(replica);
      }
    }

    // No replica caught up, use primary
    return this.getPrimaryConnection(tenantId);
  }

  private weightedRandom(replicas: ReadReplica[]): ReadReplica {
    const totalWeight = replicas.reduce((sum, r) => sum + r.weight, 0);
    let random = Math.random() * totalWeight;
    
    for (const replica of replicas) {
      random -= replica.weight;
      if (random <= 0) return replica;
    }
    
    return replicas[replicas.length - 1];
  }

  isStrongConsistencyRequired(query: string): boolean {
    const strongConsistencyPatterns = [
      /INSERT\s+INTO/i,
      /UPDATE.*current_balance/i,
      /SELECT.*account.*FOR UPDATE/i,
      /SELECT.*FROM\s+calls\s+WHERE\s+id\s*=/i,  // Single call lookup after creation
    ];
    return strongConsistencyPatterns.some(p => p.test(query));
  }
}

// Lag monitor
class LagMonitor {
  async checkLag(replicaId: string): Promise<number> {
    const client = await this.getReplicaConnection(replicaId);
    const result = await client.query(`
      SELECT EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())) 
      AS lag_seconds
    `);
    return result.rows[0].lag_seconds * 1000; // Convert to ms
  }

  async checkTenantLag(tenantId: string, replicaId: string): Promise<number> {
    // Check if the latest write for this tenant has propagated
    const latestWrite = await this.getLatestWriteTimestamp(tenantId);
    const replicaTimestamp = await this.getReplicaTimestamp(replicaId, tenantId);
    return latestWrite.getTime() - replicaTimestamp.getTime();
  }

  startPeriodicCheck(intervalMs = 1000): void {
    setInterval(async () => {
      for (const replica of this.replicas) {
        const lag = await this.checkLag(replica.id);
        replica.lag = lag;
      }
    }, intervalMs);
  }
}

// Usage in application
async function getCalls(tenantId: string, filters: CallFilters) {
  const router = getReplicaRouter();
  
  // Determine consistency level based on query type
  const consistency = router.isStrongConsistencyRequired(filters.query)
    ? ConsistencyLevel.STRONG
    : ConsistencyLevel.EVENTUAL;

  const client = await router.getReadConnection(tenantId, consistency);
  
  try {
    return client.query(
      'SELECT * FROM calls WHERE tenant_id = $1 AND ...',
      [tenantId, ...]
    );
  } finally {
    client.release();
  }
}
```

## Integration Points

- **Tenant Context (Ch 02 Sec 03):** Tenant ID from context drives replica selection
- **Provisioning (Ch 03):** Dedicated replicas provisioned for enterprise tenants
- **Multi-Region (Ch 15 Sec 10):** Replica routing integrates with data residency
- **Analytics (Part 11):** Heavy analytics queries routed to dedicated analytics replicas
- **Monitoring:** Replica lag metrics per tenant feed into SLA dashboards

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Lag Budget:** Define maximum acceptable staleness for eventual consistency reads (typically 1 second for standard queries, 100ms for recent data views).
- **Replica Failure Handling:** When a replica fails or exceeds lag threshold, the router should automatically redirect traffic to other replicas or the primary. Monitor replica health with automatic failover.
- **Stale Read Detection:** Track and alert on stale reads detected by users. A user seeing "call not found" immediately after creating it indicates a routing issue.
- **Connection Pooling per Replica:** Maintain separate connection pools for each replica. This prevents connection exhaustion on one replica from affecting others.
- **Regional Replicas:** For multi-region deployments, use local replicas in each region. Cross-region replication lag (100-500ms) requires region-aware routing.
- **Enterprise SLAs:** Enterprise tenants on the dedicated tier may require synchronous replication, guaranteeing zero data loss. Route all their reads to their dedicated replica.
- **Load Balancing Weights:** Adjust replica weights based on instance size and current load. A larger instance should receive more read traffic.
- **Testing Consistency:** Integration tests should verify that strong consistency reads return immediately visible data, while eventual consistency reads may return slightly stale data.
