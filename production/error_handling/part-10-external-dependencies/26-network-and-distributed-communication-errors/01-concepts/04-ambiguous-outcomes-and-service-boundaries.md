# Ambiguous Outcomes and Service Boundaries

> Part X · Chapter 26 · Sections 26.15, 26.16, 26.17, 26.18, 26.19, 26.20 · _Estimated reading time: 16 min_

## In one sentence

**When a request is sent but no response received, the remote outcome is ambiguous** — handle this with idempotency, uncertainty-aware logic, and clear service boundary semantics across LB/gateway and service discovery.

## Why this matters in production

For **Checkout**, a `POST` to capture payment times out at read phase. Was the payment captured or not? Answering incorrectly risks double charges or leaving money on the table. **WebhookIngest** and cross-service calls in distributed systems must treat "lost response after success" as a distinct failure category.

## Core concept

| Issue | Example | Solution |
| ----- | ------- | -------- |
| **Lost responses after success** | Read timeout after write succeeded remotely | Treat as ambiguous; use idempotency + query/status check. |
| **Ambiguous outcomes** | Timeout, connection reset mid-request | Cannot assume failure; assume uncertainty. |
| **Service discovery failures** | DNS/cache misses, registry down | Fail fast or retry with backoff; avoid thundering herd. |
| **LB/gateway errors** | `502/503/504` | Translate carefully (gateway vs origin). |
| **Partial network failures** | Packet loss, split brain | Timeouts, health checks, redundancy awareness. |
| **Failures across service boundaries** | Cross-service RPC fails | Translate transport to internal, propagate safely. |

## How it works

### Ambiguous outcomes
- **Write succeeded + read timeout** → server may have applied change.
- **Write failed + reset** → may not have applied.
- **Connection closed after partial write** → unknown.
- **Rule:** Never blindly retry non-idempotent operations on ambiguous errors.

### Safe recovery
1. **Idempotency keys** — let server deduplicate.
2. **Status lookup** — call GET/status endpoint to determine actual state.
3. **"Get-or-create" / reconcile** — check before retrying.
4. **Compensation/verification** — for financial ops, verify with provider.
5. **Mark uncertain** — record state as pending/uncertain and resolve later.

### Gateways/LB
- **`502 Bad Gateway`** — gateway got invalid response from origin.
- **`503 Service Unavailable`** — gateway cannot reach origin (overloaded/down).
- **`504 Gateway Timeout`** — gateway timed out waiting for origin.
These often reflect upstream/network; map to `UPSTREAM_UNAVAILABLE` or appropriate internal category.

## Worked example

```ts
async function capturePayment(id: string) {
  const idem = `capture:${id}`;
  try {
    return await adapter.capturePayment(id, idem);
  } catch (e: any) {
    if (e.ambiguous && !e.idempotentSafe) {
      // Query actual state
      const st = await adapter.getPaymentStatus(id);
      if (st.state === "captured") return { alreadyCaptured: true, ...st };
      if (st.state === "requires_capture") {
        // Retry with idempotency key
        return await adapter.capturePayment(id, idem);
      }
      throw e;
    }
    throw e;
  }
}
```

**Key data:**
- **Ambiguity marker**: Internal errors carry `ambiguous: true` for read/write timeouts after send.
- **gRPC codes**: `UNAVAILABLE`, `DEADLINE_EXCEEDED` — map to categories; `DEADLINE_EXCEEDED` after write can be ambiguous.

## Real-world use case

**Acme SaaS Checkout:** Capture API times out with read timeout. Adapter throws `InternalErr` with `ambiguous: true`, `retryable: false` by default. Checkout service queries Stripe for payment intent status — finds it was captured. It records order as paid (idempotent) instead of retrying and potentially causing double capture. This safely resolves ambiguity.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Always assume failure on timeout** | Simple | Can leave paid orders unpaid if remote succeeded | Dangerous for money |
| **Always retry** | Recovers if failed | Can double-charge if succeeded | **Never** for non-idempotent |
| **Status check on ambiguity** | Correct, safe | Requires read endpoint, extra call | **Recommended** for critical ops |
| **Mark uncertain + reconciliation** | Robust for complex cases | Delayed consistency | For high-value or async flows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mark read timeouts as ambiguous | Assume success or failure |
| Use idempotency + status lookup | Blindly retry non-idempotent |
| Translate LB errors correctly | Treat `504` same as app error |
| Plan for lost responses | Ignore ambiguity |
| Propagate boundary semantics cleanly | Leak transport details to domain |

## Common mistakes

- **Treating ambiguous as failed:** Creates inconsistent state (paid but not recorded).
- **Retrying on ambiguity:** Double side effects.
- **No status endpoint:** Can't resolve ambiguity for critical ops.
- **Ignoring GOAWAY/LB semantics:** Misclassifies failures.

## Checklist

- [ ] Ambiguous errors identified (read/write timeouts after send).
- [ ] Idempotency keys used.
- [ ] Status check/reconciliation path exists for critical operations.
- [ ] LB/gateway errors translated appropriately.
- [ ] Partial network failures handled with timeouts/bulkheads.

## Related

- [Ambiguous Remote Outcomes (Deep Dive)](../02-deep-dive/02-ambiguous-remote-outcomes.md)
- [Partial Network Failures and Gateways](../02-deep-dive/03-partial-network-failures-and-gateways.md)
- [Handling Lost Responses Safely](../03-practical-examples/02-handling-lost-responses-and-retries-safely.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Glossary](../../../GLOSSARY.md)
