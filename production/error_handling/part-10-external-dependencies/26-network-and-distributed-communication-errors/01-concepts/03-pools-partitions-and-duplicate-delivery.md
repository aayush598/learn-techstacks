# Pools, Partitions, and Duplicate Delivery

> Part X · Chapter 26 · Sections 26.9, 26.10, 26.12, 26.13, 26.14 · _Estimated reading time: 14 min_

## In one sentence

**Connection pool exhaustion, half-open connections, network partitions, duplicates, and out-of-order messages** are common distributed failure modes that require isolation and deduplication strategies.

## Why this matters in production

**Acme SaaS** uses connection pools to third-party APIs. Under load, pool exhaustion causes queuing/timeouts. A failed connection can become "half-open" and be reused incorrectly. Network partitions between services cause split-brain-like issues. Webhooks can be delivered multiple times or out of order — **WebhookIngest** must handle duplicates.

## Core concept

| Failure | Description | Mitigation |
| ------- | ----------- | ---------- |
| **Pool exhaustion** | No available connections in pool | Timeouts on acquire, queue limits, bulkheads, scale. |
| **Half-open connections** | Connection marked idle but broken | Health checks, validate on checkout, recreate on error. |
| **Network partition** | Network split between components | Timeouts, failover, eventual consistency, idempotency. |
| **Duplicate delivery** | Same message/request delivered twice | Idempotency keys, deduplication store. |
| **Out-of-order delivery** | Messages arrive out of sequence | Sequence numbers, versioning, event ordering strategies. |

## How it works

### Connection pools
- **Max connections** limits concurrent requests.
- **Idle timeout** closes stale connections.
- **Connection validation** checks before reuse.
- **Half-open**: connection failed but not removed from pool — next request gets it and fails again.

### Partitions
- **Asymmetric partitions** possible.
- **Timeout-based failure detection** needed.
- **CAP theorem trade-offs** apply.

### Duplicates/out-of-order
- **At-least-once delivery** common in queues/webhooks.
- **Need deduplication** by event ID/request ID.
- **Ordering not guaranteed** in distributed systems.

## Worked example

```ts
// Pool with validation
class PooledConn {
  async get(): Promise<Conn> {
    const c = this.pool.pop();
    if (c && !(await this.isHealthy(c))) {
      await c.close();
      return this.create();
    }
    if (!c) return this.create();
    return c;
  }
  async isHealthy(c: Conn): Promise<boolean> {
    try { await c.ping(); return true; } catch { return false; }
  }
}

// Dedup for webhooks
async function processWebhook(evt: Event) {
  const key = `webhook:${evt.id}`;
  const seen = await redis.set(key, "1", "EX", 86400, "NX");
  if (seen === null) return { status: "duplicate", ignored: true };
  // process...
}
```

**Key data:**
- **Pool timeouts**: acquire timeout, idle timeout, max lifetime.
- **HTTP/2**: multiplexing changes pooling behavior.
- **Webhook retries**: providers retry on failure → duplicates expected.

## Real-world use case

**WebhookIngest receiving Stripe webhooks:** Stripe retries failed webhooks (at-least-once). Without deduplication by event ID, processing payment succeeded webhook twice could credit account twice. Deduplication store with TTL prevents this.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **No validation** | Fast | Half-open causes cascading failures | Never |
| **Validate on checkout** | Catches broken connections | Extra round-trip cost | **Recommended** |
| **Eager health checks** | Proactive | Complexity, false positives | For critical pools |
| **In-memory dedup only** | Fast | Lost on restart | Insufficient for distributed |
| **Distributed dedup store** | Reliable | Latency, availability dependency | **Recommended** for webhooks/jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate pooled connections | Blindly reuse |
| Expect duplicates in webhooks/queues | Assume exactly-once |
| Use deduplication keys | Process blindly on retry |
| Handle out-of-order with versioning | Assume FIFO everywhere |
| Set pool timeouts and limits | Unbounded pools |

## Common mistakes

- **Half-open connections:** Retry loop on broken pooled connection.
- **No webhook dedup:** Duplicate processing.
- **Assuming ordering:** Events processed out of order corrupt state.

## Checklist

- [ ] Connection pool has validation and timeouts.
- [ ] Deduplication for at-least-once sources.
- [ ] Out-of-order handling strategy defined.
- [ ] Partition behavior tested/reasoned about.

## Related

- [Ambiguous Outcomes and Service Boundaries](./04-ambiguous-outcomes-and-service-boundaries.md)
- [Ambiguous Remote Outcomes](../02-deep-dive/02-ambiguous-remote-outcomes.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Glossary](../../../GLOSSARY.md)
