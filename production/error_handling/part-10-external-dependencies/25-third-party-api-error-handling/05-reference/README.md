# Chapter 25 — Reference

> Part X · Chapter 25 · All subsections 25.1–25.20 · _Estimated reading time: 12 min_

## External API Failure Handling Guide

### Classification matrix
| Class | Examples | Retryable | Notes |
| ----- | -------- | ---------- | -----|
| **Auth/Config** | `401` invalid, `403` forbidden | Usually no | Alert on config issues. |
| **Token expiry** | `401` token_expired | Once if refresh possible | Token refresh middleware. |
| **Rate limit** | `429` + `Retry-After` | Yes with backoff + budget | Respect headers. |
| **Quota/Billing** | `402`, quota exceeded | No until account changes | Route to ops/billing. |
| **Client error (bad request)** | `400`, `422` validation | No | Fix request. |
| **Conflict** | `409` | Case-dependent | May need idempotency/retry logic. |
| **Decline/Business** | Card declined | No | User-actionable. |
| **Timeout** | Connect/read timeout | If idempotent | Ambiguous — see Chapter 26. |
| **Connectivity** | `ECONNREFUSED/RESET` | If idempotent | Transport failure. |
| **Server/Gateway** | `500`, `502`, `503`, `504` | Often if idempotent | Check if origin error. |
| **Malformed/Unexpected** | HTML, bad JSON, schema change | No until fixed | Defensive parsing. |

### Translation checklist
- [ ] Classify (http/payload/network) at adapter.
- [ ] Normalize provider fields.
- [ ] Map to stable internal code.
- [ ] Set `retryable`, `retryAfterSec` if applicable.
- [ ] Preserve `cause` (redacted).
- [ ] Set user-safe message separately.
- [ ] Avoid leaking vendor types/codes to clients.

### Adapter checklist
- [ ] Interface defined; vendor SDK isolated.
- [ ] Per-vendor mapper with tables.
- [ ] Idempotency keys passed for mutations.
- [ ] Critical vs optional defined.
- [ ] Timeouts configured per operation.
- [ ] Circuit breaker/retry budget if needed.
- [ ] Feature flag for vendor disable.
- [ ] Contract tests exist.

### Outage playbook (quick)
1. **Detect** — timeouts/errors spike, circuit opens.
2. **Contain** — fail closed for critical, degrade optional.
3. **Communicate** — safe errors to users, alerts to oncall.
4. **Recover** — half-open probes, drain queues, verify consistency.
5. **Post-mortem** — review idempotency and failure paths.

## Related

- [Chapter 25 README](../README.md)
- [Dos and Don'ts](../04-dos-and-donts/README.md)
- [Stripe Error Mapping Adapter](../03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Chapter 26 Reference](../../26-network-and-distributed-communication-errors/05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
