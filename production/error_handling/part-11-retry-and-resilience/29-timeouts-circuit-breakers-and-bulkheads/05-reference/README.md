# Chapter 29 — Reference

> Part XI · Chapter 29 · All sections

Quick-reference material for timeouts, circuit breakers, bulkheads, and admission control. Pair this
with [Do's and Don'ts](../04-dos-and-donts/README.md).

## Resilience decision guide

```text
Is this a network or bounded-resource call?
├─ No  → do not add a timeout; fix the blocking operation
└─ Yes → set a deadline (and propagate remaining time)
          │
          Is the dependency critical to correctness?
          ├─ Yes → fail-closed fallback; breaker + bulkhead; alert
          └─ No  → fail-open/degrade; breaker + bulkhead; notify

Does the call have side effects?
├─ Yes → require idempotency key (Chapter 28); retry only with key
└─ No  → retry if transient and within budget

Does the dependency recover on its own?
├─ Usually → retries + breaker
└─ Needs time → breaker with cooldown; shed load
```

## Timeout defaults

| Timeout | Typical | Notes |
| ------- | ------- | ----- |
| Connect | 200ms–2s | Tight; don't wait on a blackhole |
| TLS handshake | 1–3s | Included in connect in most clients |
| Per-request | 2–10s | Depends on p99 of the operation |
| Per-operation | 5–60s | Covers retries, not one attempt |
| Job deadline | minutes–hours | Stored on the job |
| Cleanup | 500ms–1s | Independent of the expired deadline |
| Admission minimum | 50–100ms | Below this, reject |

## Deadline propagation

| Transport | Mechanism |
| --------- | --------- |
| gRPC | `context.WithTimeout` / `grpc-timeout` header |
| HTTP | `X-Request-Timeout-Ms` or `X-Request-Deadline` |
| Queue | absolute `deadline_ms` in the message |
| Child call | `min(configured, remaining − safety)` |

```text
remaining = deadline − now
timeout   = min(configured, remaining − safety)
if timeout <= min_useful → reject
```

## Little's Law

```text
concurrency ≈ throughput × latency
```

Example: 50 req/s × 0.4s = 20 concurrent calls. Set the limit at 20, queue ≈ 2× concurrency,
reject beyond.

## Breaker defaults

| Parameter | Conservative | Critical path |
| --------- | ------------ | ------------- |
| Window | 60s sliding | 10–15s sliding |
| Min requests | 50 | 20–30 |
| Failure threshold | 50% | 20–30% |
| Cooldown base | 10s | 5s |
| Cooldown cap | 5min | 2min |
| Close threshold | 5 successes | 3 successes |
| Probe concurrency | 1 | 2–3 |
| Secondary trigger | none | 10 consecutive failures |

## Breaker state variables

```text
shouldOpen = total >= minRequests AND failures/total >= threshold
cooldown(n) = min(cap, base × 2^(n-1)) × jitter(0.8..1.2)
```

## Bulkhead defaults

| Dimension | Limit source |
| --------- | ------------ |
| Per dependency | Provider rate limit × p99 latency |
| Per tenant | 2–10 for heavy operations |
| Queue | 1–2× concurrency in seconds of work |
| Pool headroom | 20–30% |

## HTTP status mapping

| Situation | Status | Headers |
| --------- | ------ | ------- |
| Breaker open | `503` | `Retry-After` |
| Admission reject | `503` | `Retry-After` |
| Rate limited | `429` | `Retry-After` |
| Operation deadline | `504` | correlation id |
| Client disconnected | `499` (internal) | — |
| Provider `4xx` | pass through | — |
| Provider `5xx` exhausted | `502`/`504` | correlation id |

## Combining mechanisms

```text
1. deadline check
2. breaker check
3. bulkhead acquire (bounded queue)
4. call with per-attempt timeout
5. retry if eligible and budget remains (breaker re-checked)
6. fallback / degrade
```

Worst-case calls = attempts of the **single retry owner**, not the product across layers.

## Fail-open vs fail-closed

| Feature | Mode | Rationale |
| ------- | ---- | --------- |
| Payments / checkout | **Fail-closed** | Wrong is worse than unavailable |
| Auth / authorization | **Fail-closed** | Never widen access |
| Account creation | **Fail-closed** | Duplicate identity risk |
| Search suggestions | Fail-open | Empty result acceptable |
| Recommendations | Fail-open | Optional personalization |
| Email notifications | Fail-open (queue) | Delay acceptable |
| LLM summaries | Fail-open (cached) | Template is acceptable |
| Feature flags | Fail-open to last-known | Stale beats broken |
| Analytics | Fail-open (drop) | Non-critical |

Decision rule:

```text
Can the system produce a correct (possibly reduced) result without the dependency?
├─ Yes → fail-open / degrade, label the response
└─ No  → fail-closed with a clear error and Retry-After
```

## Policy template

```yaml
dependency: <name>
  timeout: { connect_ms: 0, request_ms: 0 }
  deadline_ms: 0
  retry: { owner: <service>, max_attempts: 0, base_ms: 0, jitter: full }
  breaker: { threshold: 0, min_requests: 0, window_ms: 0, cooldown_ms: 0 }
  bulkhead: { max_concurrent: 0, max_queue: 0, per_tenant: 0 }
  fallback: { mode: fail_open|fail_closed, action: <...> }
  idempotency: { required: true|false, key: <...>, ttl: <...> }
```

## Review questions

1. What is the worst-case wall-clock time for one request, including retries?
2. What does the caller receive while the breaker is open?
3. What is the maximum concurrent load this dependency can receive?
4. Is every retried operation idempotent or keyed?
5. Which features are fail-open, and are they labeled as degraded?
6. What happens when the queue is full and the deadline has passed?
7. Are breakers checked before every attempt?
8. Are pool limits below the provider's actual capacity?

## Metrics to export

```text
request_duration_seconds{dependency,outcome}
timeout_total{dependency,kind=connect|request|operation}
breaker_state{dependency}                 # 0 closed, 1 half_open, 2 open
breaker_transitions_total{dependency,from,to}
breaker_rejected_total{dependency}
bulkhead_inflight{dependency}
bulkhead_wait_seconds{dependency}
queue_depth{dependency}
admission_rejected_total{reason}
deadline_exceeded_total{service}
```

## Related

- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../30-graceful-degradation-and-fallbacks/README.md)
- [Glossary](../../../GLOSSARY.md)
