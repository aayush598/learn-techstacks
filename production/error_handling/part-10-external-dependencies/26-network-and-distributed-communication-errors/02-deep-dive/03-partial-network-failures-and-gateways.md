# Partial Network Failures and Gateways

> Part X · Chapter 26 · Sections 26.12, 26.17, 26.18, 26.19, 26.20 · _Estimated reading time: 14 min_

## In one sentence

**Partitions, partial failures, service discovery issues, and LB/gateway errors** require boundary-aware translation and resilience controls (timeouts, bulkheads) across service boundaries.

## Why this matters in production

Networks fail partially — some packets lost, some connections work. **WebhookIngest** can't reach DB during partition. LB returns `504` while origin might have processed request. Service discovery returns stale endpoints. Without careful handling, these become cascading failures.

## Core concept

| Issue | Behavior | Response |
| ----- | -------- | -------- |
| **Network partition** | Split connectivity | Timeouts, circuit breakers, avoid split-brain writes. |
| **Partial failures** | Some calls succeed/fail | Fail fast per call, don't block all, use bulkheads. |
| **Service discovery failure** | Can't resolve endpoints | Cache last-known-good, retry with backoff, fail fast if critical. |
| **LB/gateway errors** | `502/503/504` | Classify: 503 often retryable, 504 ambiguous, 502 origin issue. |
| **Cross-service boundaries** | Different failure semantics | Translate transport to internal at each boundary. |

## How it works

### Gateway classification
- **`503 Service Unavailable`** — usually temporary (overload/maintenance). Often retryable if idempotent.
- **`504 Gateway Timeout`** — gateway timed out waiting for origin. **Ambiguous** — origin may have processed.
- **`502 Bad Gateway`** — gateway received invalid response from origin. Depends on origin state.
- **Look for headers**: `Retry-After`, `X-Cache` etc.

### Service discovery
- **DNS caching** can cause stale endpoints.
- **Registry failures** need fallback to cached endpoints.
- **Health checks** required.

### Partial failures
- **Use bulkheads** per dependency to isolate failures.
- **Don't let one slow dep block all threads**.
- **Per-request timeouts** mandatory.

## Worked example

```ts
function mapGatewayStatus(s: number, headers: Headers): InternalErr {
  if (s === 429) return mapRateLimit(headers);
  if (s === 503) return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true, retryAfterSec: parseRetryAfter(headers) });
  if (s === 504) return new InternalErr(AcmeErr.UPSTREAM_TIMEOUT, { retryable: false, ambiguous: true, reason: "gateway_timeout" });
  if (s === 502) return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true });
  if (s >= 500) return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true });
  return new InternalErr(AcmeErr.UPSTREAM_UNKNOWN, { retryable: false });
}
```

**Key data:**
- **gRPC via proxy**: Status mapped differently.
- **mTLS** failures separate.

## Real-world use case

**WebhookIngest processing during network partition:** Can't reach payment DB. Must timeout quickly, return 5xx to webhook provider (triggering retry), and not block. Partition handling prevents cascading failure to other services.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Treat all 5xx same** | Simple | Wrong for 504 ambiguity | Never |
| **Cache service discovery** | Resilient to registry failure | Stale endpoints risk | **Recommended** with TTL/health checks |
| **No bulkheads** | Simple | One dep exhausts all resources | Never in production |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify gateway errors by type | Conflate 502/503/504 |
| Treat 504 as ambiguous | Blind retry on 504 |
| Use bulkheads and per-dep timeouts | Share unbounded resources |
| Cache service discovery safely | Use forever-stale |
| Translate at each boundary | Leak transport across services |

## Common mistakes

- **Retrying 504 blindly** — ambiguity risk.
- **No bulkheads** — cascading failure.
- **Stale discovery** — routing to dead endpoints.

## Checklist

- [ ] Gateway status codes mapped with ambiguity flags.
- [ ] Service discovery has fallback cache.
- [ ] Bulkheads per dependency.
- [ ] Cross-boundary translation defined.
- [ ] Partition scenarios considered.

## Related

- [Ambiguous Remote Outcomes](./02-ambiguous-remote-outcomes.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Glossary](../../../GLOSSARY.md)
