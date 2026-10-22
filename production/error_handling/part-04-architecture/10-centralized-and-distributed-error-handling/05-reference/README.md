# Chapter 10 — Reference

> Part IV · Chapter 10 · Cheat sheets, decision tables, and the contract checklist.

## Cheat sheet — the two halves

```text
CENTRALIZED (one place)          LOCAL (many, context-rich)
· serialize to envelope          · retry / no-retry verdict
· correlation ID                 · compensation / saga steps
· redaction policy               · conflict vs bug
· unclassified safety net        · optional-feature fallback
· log/metric shape               · entitlement-aware degradation
```

**Rule:** central = mechanical and total; local = business and partial.

## Decision table — where does this concern live?

| Concern | Home | Sections |
| ------- | ---- | -------- |
| Envelope serialization | central utility | 10.8 |
| Status map (code → HTTP) | central, registry-driven | 10.3, 10.8 |
| Redaction / sensitive fields | central policy | 10.8 |
| Request/correlation ID | central middleware | 10.5 |
| Parsing/auth/rate-limit rejection | middleware (preconditions) | 10.5 |
| Shape normalization (SDK → AppError) | interceptor / adapter | 10.6 |
| Retry decision | application / worker | 10.2, 10.9 |
| Compensation | application (saga owner) | 10.11 |
| Optional-feature fallback | the feature's boundary | 10.9 |
| Unknown-error safety net | global handler | 10.3 |
| Uncaught exception / crash | process boundary (Ch. 9) | 10.3 |

## Mechanism chooser

| You need… | Use | Don't use |
| --------- | --- | --------- |
| Reject malformed/auth/oversized requests | middleware | decorator |
| Uniform body for everything escaping handlers | error filter / error middleware | per-route try/catch |
| Normalize SDK/thrown shapes near a handler | interceptor | global filter |
| Attach policy to specific methods (`@Retryable`) | decorator | middleware |
| Reuse logic across HTTP, worker, CLI | pure utility (10.8) | framework-specific hook |
| Terminal crash handling | process handler | any of the above |

## Cheat sheet — global handler: allowed vs forbidden

| Allowed (mechanical) | Forbidden (business) |
| -------------------- | -------------------- |
| `headersSent` guard | `if (message.includes(...))` |
| `normalize(err)` | retry / backoff loops |
| `STATUS[code] ?? 500` | refund / compensation |
| log code + correlation + cause | tenant/plan branching |
| `toProblem()` render | fallback values presented as success |
| redact per policy | severity-based per-customer responses |

## Decision table — central vs local recovery (10.9)

| Question | If yes | If no |
| -------- | ------ | ----- |
| Does the fallback need transaction/attempt state? | local | consider central (usually: no recovery, just render) |
| Must every route behave identically? | central mechanism | local boundary |
| Is the dependency optional? | local degradation + flag | propagate to the center for rendering |
| Is the error unclassified? | central safety net (`500` + ID) | — |

## Contract checklist across services (10.14–10.17)

- [ ] One published artifact: codes, statuses, `retryable`, envelope schema.
- [ ] Envelope = RFC 9457 members + `code` + `request-id`.
- [ ] Namespace codes by owning domain (`BILLING_*`, `CHECKOUT_*`).
- [ ] Consumers: unknown code → classify by status class; log producer; never crash/never fake `200`.
- [ ] Correlation ID immutable across hops (HTTP header + message attribute).
- [ ] Compatibility: additive = non-breaking; status/retryability changes = major bump.
- [ ] Skew design target: N / N-1 / N-2 coexist; CI replays error-body corpus per consumer.
- [ ] Deprecations keep old codes answerable for ≥ one release window.

## Ordering cheat sheet (10.5–10.7)

```text
inbound:  requestId → rate limit → auth → parse → interceptor(normalize) → handler
outbound: interceptor(after) → error filter (first body-writer, headersSent-checked)
express:  error middleware registered LAST, 4-arg signature
nestjs:   middleware → guards → interceptors → pipes → handler → filters
decorators: outer decorator sees every attempt (logging outside retry)
```

## Key numbers

- Global filter budget: **≤ ~30 lines**; error kernel budget: **≤ ~300 lines**, 0 feature imports.
- Unknown-error fallback: **`500`** + correlation ID, no stack (and per Ch. 34: no internals).
- Express: 4-arg error middleware; `ERR_HTTP_HEADERS_SENT` on double write.
- RFC 9457 members: `type`, `title`, `status`, `detail`, `instance`.
- Version-skew assumption: **N/N-1/N-2**.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Centralized handling | One implementation of mechanical policy used by all entry points |
| Local handling | Decisions made where business context exists |
| Safety net | The last-resort handler for unclassified errors |
| Hidden business decision | Product policy encoded in infrastructure code |
| Error kernel | Small framework-free package: types, registry, serializer |
| Contract artifact | Versioned published codes/statuses/envelope shared by services |
| Tolerant consumer | Treats unknown codes as their status class |
| Fallthrough | An error passing an outer layer that chose not to write |

## Signposts

- Framework specifics → [Ch. 48 Framework Integration](../../../part-18-languages-and-frameworks/48-framework-and-runtime-integration/README.md)
- Middleware edge cases → [Ch. 21 API Boundary](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- Contracts and versioning → [Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- Module organization → [Ch. 45](../../../part-17-organization/45-organizing-error-handling-modules/README.md)

## Related

- [Chapter 10 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part IV Index](../../README.md)
