# External, Network, and Config Categories (5.16–5.21, 5.32)

> Part II · Chapter 5 · Sections 5.16–5.21, 5.32 · _Estimated reading time: 30 min_
> **Prerequisite:** [Limits, Concurrency, and Data Categories](./02-limits-concurrency-and-data.md)

## In one sentence

This family covers everything that fails *outside your process* — **external APIs, networks,
timeouts, serialization, configuration, dependency initialization, and third-party dependencies**
— where the hard problem is **ambiguous outcomes**.

## Why this matters in production

Most production outages are integration failures. They are usually **transient** — so people
retry — but retrying a non-idempotent call across an ambiguous outcome causes duplicate side
effects. This family requires timeouts on every call, idempotency before retry, and a clear line
between "the remote is down" and "we configured it wrong."

## 5.16 External API

**External API** errors are non-2xx responses (or malformed bodies) from a provider you call:
Stripe, an email provider, an LLM provider.

| Provider response | Meaning | Retry |
| ----------------- | ------- | ----- |
| `5xx` | provider fault | yes (usually) |
| `429` | throttle | yes with `Retry-After` |
| `401`/`403` | our credentials/scope | **no** — fix config |
| `400`/`422` | our request is bad | no |
| malformed body | contract violation | no (log, degrade) |

**Translate vendor codes to stable internal codes** (Chapter 25). Never leak a vendor's raw error
or couple your logic to its wording.

## 5.17 Network / connectivity

Network failures are below the HTTP layer:

| Error | Cause | Retry |
| ----- | ----- | ----- |
| `ENOTFOUND` / DNS | name resolution failed | yes (typically) |
| `ECONNREFUSED` | nothing listening | maybe — could be a config bug |
| `ECONNRESET` | peer reset | yes |
| `ETIMEDOUT` | connect/read timeout | yes (idempotent only) |
| TLS/cert error | cert expired/mismatch | **no** — fix cert |

Distinguish a **connect** failure (request likely never applied) from a **reset after send**
(outcome **ambiguous** — the write may have happened). Ambiguity is the reason idempotency is
mandatory, not optional (Chapter 26).

## 5.18 Timeout

A **timeout** means *you stopped waiting* — the remote may still be processing.

| Kind | Budget owner |
| ---- | ------------ |
| connect timeout | usually short (seconds) |
| request/read timeout | per-operation |
| overall deadline | must exceed downstream sum |

| Aspect | Value |
| ------ | ----- |
| HTTP to caller | `504` |
| gRPC | `DEADLINE_EXCEEDED (4)` |
| Retry | yes, **only if idempotent** |

> ⚠️ **A timeout is not "it failed."** It is "the outcome is unknown." Never blindly retry a write
> after a timeout without an idempotency key (Chapters 28, 58).

## 5.19 Serialization / deserialization

**Serialization** failures are parse/shape errors crossing a format boundary: invalid JSON,
schema mismatch, unexpected field types, message-schema version drift.

| Trigger | Direction | HTTP |
| ------- | --------- | ---- |
| malformed JSON request | inbound | `400` (`5.2`) |
| unsupported content type | inbound | `415` |
| provider returns HTML | outbound | treat as `external_api` |
| event schema mismatch | async | route to DLQ |

Deserialization errors are **permanent** for the same payload. For event streams, a schema
mismatch is often a **version incompatibility** (Chapter 33) and belongs in a quarantine/DLQ, not
an infinite retry.

## 5.20 Configuration

**Configuration** failures are runtime environment problems: missing env var, invalid value,
unreachable endpoint configured wrong, missing secret.

| Aspect | Value |
| ------ | ----- |
| Detected | ideally at **startup** (fail fast) |
| HTTP | `500` (never expose which variable) |
| Retry | no |
| Alert | page (ops) |

Validate configuration once at boot and **refuse to start** on invalid config (fail-fast,
Chapter 48). A config error discovered per-request is a config error you should have caught once.

## 5.21 Dependency initialization

**Dependency initialization** failures happen when a required client (DB pool, SDK, queue
consumer) cannot be constructed or connected at startup.

| Trigger | Policy |
| ------- | ------ |
| DB unreachable at boot | retry with backoff up to a budget; then fail startup |
| bad credentials at boot | fail fast, alert |
| pool cannot be created | fail fast (no partial service) |

Two patterns: **fail-closed at boot** (required deps) vs **lazy optional init** (best-effort
deps) that degrades rather than blocks startup (Chapter 41).

## 5.32 Third-party dependency

This is the umbrella over 5.16–5.18 for a *named* dependency, and the place to classify
**criticality**:

| Dependency | Criticality | On failure |
| ---------- | ----------- | ---------- |
| payments (Stripe) | required for billing | no silent success; idempotent retry |
| LLM provider | optional per feature | degrade to cached/placeholder |
| analytics / email | best-effort | enqueue; drop after budget |
| search | optional | fall back to basic query |

Classify by dependency so resilience policy (bulkheads, breakers, fallbacks) can be applied per
dependency, not globally (Chapters 29–30).

## Worked example — Checkout calls Stripe

```text
POST https://api.stripe.com/v1/payment_intents
   ├─ 200 OK                     → success
   ├─ 429 + Retry-After          → 5.10 rate_limit → retry idempotently
   ├─ 500                        → 5.16 external_api → retry idempotently
   ├─ 401                        → 5.20 configuration → page, do NOT retry
   ├─ connection reset after send→ 5.17 network (AMBIGUOUS) → re-query by idempotency key
   └─ read timeout               → 5.18 timeout (AMBIGUOUS) → same as above
```

The two ambiguous cases are the reason `Checkout` uses a Stripe idempotency key on **every**
attempt.

## Key data / numbers

- Common defaults: connect timeout **2–5s**, request timeout **10–30s**, whole-request deadline
  strictly greater than the sum of downstream budgets (Chapter 29).
- DNS failure `ENOTFOUND` is almost always transient; TLS cert errors are permanent.
- gRPC `UNAVAILABLE (14)` and `DEADLINE_EXCEEDED (4)` are retryable; `PERMISSION_DENIED (7)` and
  `UNAUTHENTICATED (16)` are not.
- Validate config at startup; treat "missing config at runtime" as a defect.

## Real-world use case — Acme SaaS (LLM summaries)

Acme's summary feature called an LLM provider. On a provider `500`, the code retried **and** the
dashboard 500-ed. After classification: provider errors are `external_api` (`502` to the caller,
degraded to "summary unavailable"); a `401` from the provider is `configuration` (page ops, never
retry); a read timeout is `timeout` (ambiguous → degrade, do not re-bill). The page stayed up
through two provider incidents.

## Trade-offs

| Category | Retry | Ambiguous? | Needs idempotency |
| -------- | ----- | ---------- | ----------------- |
| external_api 5xx/429 | yes | maybe | yes for writes |
| network connect fail | yes | no | no |
| network reset/timeout | yes | **yes** | **yes** |
| serialization | no | no | n/a |
| configuration | no | no | n/a |
| dependency init | until budget | n/a | n/a |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put timeouts on every call | Let calls hang forever |
| Use idempotency keys for writes | Blindly retry after a timeout |
| Translate vendor codes | Leak provider raw errors |
| Validate config at startup | Discover bad config per-request |
| Classify dependency criticality | Treat every dep as required |

## Common mistakes

- **Retrying after a timeout without idempotency** → duplicate side effects.
- **Treating `401` from a provider as transient** and looping forever.
- **No connect vs read distinction**, missing ambiguity.
- **Starting with missing config** instead of failing fast.

## Checklist

- [ ] Does every outbound call have a timeout?
- [ ] Are writes idempotent before retry?
- [ ] Are vendor codes translated to stable internal codes?
- [ ] Is config validated at startup?
- [ ] Is each dependency's criticality classified?

## Related

- [Limits, Concurrency, and Data Categories](./02-limits-concurrency-and-data.md)
- [Runtime, Resource, and Lifecycle Categories](./04-runtime-lifecycle-and-resources.md)
- [Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
