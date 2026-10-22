# Chapter 5 — Do's and Don'ts

> Part II · Chapter 5 · All sections

A condensed rule set distilled from the 35 categories. Use it as a review checklist per family.

## Input, auth, and business (5.1–5.9)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `422` for rule violations, `400` for parsing | Return `500` for bad input |
| Normalize auth failures to one code | Reveal whether a user exists |
| Use `404` when existence is sensitive | Leak other tenants' resources via `403` |
| Replay idempotent duplicates with `200` | Re-execute a completed payment |
| Model state transitions in the domain | Encode lifecycle rules in the transport |

## Limits, concurrency, and data (5.10–5.15, 5.28)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Honor `Retry-After` on `429` | Hammer `429` in a tight loop |
| Disambiguate quota vs rate limit by **code** | Treat both as retryable |
| Retry `40001`/`40P01` with fresh reads | Retry `23505` (duplicate) |
| Bypass cache on error | `500` because Redis is down |
| Abort and page on data-integrity failure | "Continue and fix later" |
| Abort multipart uploads on failure | Leave orphaned parts |

## External, network, and config (5.16–5.21, 5.32)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put a timeout on every outbound call | Let calls hang |
| Use idempotency keys for writes | Retry after a timeout blindly |
| Translate vendor codes to stable codes | Leak provider raw errors |
| Validate config at startup; fail fast | Discover bad config per-request |
| Classify dependency criticality | Treat every dependency as required |

## Runtime, resources, and lifecycle (5.22, 5.25–5.27, 5.31)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bound retries under resource pressure | Retry-storm a saturated resource |
| Fail fast on programming defects | Catch an NPE and return `400` |
| Log cancellation at `info` | Log cancel as `error` |
| Drain, checkpoint, and clean up on shutdown | Drop in-flight work on `SIGTERM` |
| Use one outermost catch-all | Catch-all inside the domain |

## Async, partial, and specialized (5.23, 5.24, 5.29, 5.30, 5.33–5.35)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Declare retryable vs terminal per job | Retry permanent failures forever |
| Dedupe webhooks by event id | Assume single delivery |
| Return `4xx` for permanent webhook errors | Return `5xx` and create a poison loop |
| Record partial results per item | Mark partial work as complete |
| Make compensation idempotent | Refund twice |
| Treat token limits as permanent | Retry `context_length_exceeded` |

## Anti-patterns in the wild

1. **The `409` Monolith** — every conflict, duplicate, and state error returned as generic
   `CONFLICT`, breaking idempotent replay.
2. **The Retry-Everything** — including `23505`, `422`, and `401`.
3. **The Ambiguous Retry** — retrying an unkeyed write after a timeout.
4. **The Silent Partial** — marking a half-done job "success."
5. **The Poison Webhook** — `500` on a permanent payload error.
6. **The Cache Outage** — failing requests when an optional cache is down.
7. **The Cancelled Error** — turning a user cancel into a `500` alert.

## Chapter checklist

- [ ] Every category has a stable code, HTTP status, and retry verdict.
- [ ] Shared statuses (`409`, `429`) are disambiguated by code.
- [ ] Writes are idempotent before any retry.
- [ ] Partial completion is represented explicitly.
- [ ] Cancellation is a signal, not a failure.
- [ ] Specialized categories (AI, webhook, file) are handled explicitly.

## Related

- [Chapter 5 Reference Cheat-Sheet](../05-reference/README.md)
- [Chapter 4 — Do's and Don'ts](../../04-designing-a-comprehensive-error-taxonomy/04-dos-and-donts/README.md)
- [Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
