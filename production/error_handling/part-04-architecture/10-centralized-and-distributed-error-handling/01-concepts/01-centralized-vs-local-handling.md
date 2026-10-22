# Centralized and Local Handling: The Two Halves

> Part IV · Chapter 10 · Sections 10.1, 10.2, 10.9 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 9 — Layered Architecture](../../09-layered-error-handling-architecture/README.md)

## In one sentence

**Centralized** handling owns one policy applied everywhere (serialize, correlate, safety-net);
**local** handling owns decisions that need context the center cannot see — and production code
needs both without overlap.

## Why this matters in production

Pick either extreme and the system fails visibly:

- **All central:** the global handler must decide whether a `Conflict` retries, whether a
  provider timeout is retryable, whether a partial export compensates. It has none of that
  context, so it guesses — uniformly and wrongly.
- **All local:** twenty modules, twenty envelopes, two status vocabularies, and an incident at
  3 a.m. where nobody can say what "db err" in one service's logs has to do with the `500`s the
  other service emits.

The mature shape is a **policy engine in the center and decisions at the edges**, meeting at one
error model (Part III).

## Core concept — the two halves

```text
                    ┌─────────── CENTRALIZED (one place) ───────────┐
                    │  · serialize to the standard envelope          │
 request ──▶ local │  · attach correlation/request ID                │▶ response
   errors   decide │  · redact sensitive fields                       │
            (many) │  · log/metric shape (what info errors carry)     │
                    │  · safety net for unclassified errors           │
                    └──────────────────────────────────────────────────┘
 local decision points (many, context-rich):
   application service · worker · integration adapter · route-level recovery
```

| Concern | Centralized (10.1) | Local (10.2) |
| ------- | ------------------ | ------------ |
| Envelope serialization | ✅ single serializer | never re-serialize |
| Correlation ID propagation | ✅ | pass through |
| Redaction policy | ✅ | never invent |
| Retry / no-retry verdict | ❌ | ✅ application/worker |
| Compensation / saga steps | ❌ | ✅ application |
| Domain conflict vs bug | ❌ | ✅ domain + application |
| Fallback for an optional feature | ❌ | ✅ the feature's own boundary |
| Unknown-error safety net | ✅ `500` + correlation ID | raise, don't swallow |

**Global vs local recovery (10.9)** is the same axis applied to recovery:

| Recovery type | Where it belongs | Example |
| ------------- | ---------------- | ------- |
| Local recovery | the layer with the state | retry one idempotent DB write; serve cached feature flag |
| Centralized recovery | nowhere (a myth) | "the handler will figure it out" — it cannot |
| Centralized *termination* | process/global handler | unclassified error → `500`; `uncaughtException` → exit |

## How it works — the meeting point

Both halves speak the same error model. The local half *decides* and produces an outcome; the
central half *renders* it:

```ts
// LOCAL: decision with full context (application layer)
if (err.code === "UPSTREAM_RATE_LIMITED" && attempt === 1) {
  await stripe.retry({ delayMs: err.retryAfterSec * 1000 });
} else if (err.code === "PAYMENT_CARD_DECLINED") {
  await payments.markFailed(checkoutId, err.declineCode);   // decide: no retry
}
throw err;  // outcome decided; rendering belongs to the center

// CENTRAL: one renderer, applied to everything that escapes
export function toProblem(err: AppError, reqId: string): ProblemDetails {
  return {
    type: `https://acme.example/errors/${err.code}`,   // stable identifier, not a doc URL we fake
    title: TITLES[err.code] ?? "Internal error",
    status: STATUS[err.code] ?? 500,
    "request-id": reqId,
    ...(SAFE_DETAIL[err.code] ? { detail: SAFE_DETAIL[err.code] } : {}),
  };
}
```

Note what the center does **not** contain: no retry loops, no business `if`s — only maps from
code → status/title/detail, which is mechanical policy (RFC 9457 shape, Chapter 20).

## Mechanisms on each half

| Mechanism | Belongs to | Job |
| --------- | ---------- | --- |
| Global exception filter / error middleware (10.3–10.5) | central | catch anything escaping; render envelope |
| Interceptors (10.6) | central | wrap handler execution; transform outcomes |
| Decorators (10.7) | either | local: `@Retryable`; central: `@SerializeProblem` |
| Shared utilities (10.8) | central | `toProblem()`, `normalize()`, redaction — pure functions |
| try/catch in application service | local | decide retry/compensate/abort |

The deep-dive files cover composition and ordering; this file's rule is: **a mechanism is
central when its behavior must be identical for every route, and local when it needs arguments
only the call site knows.**

## Key data / numbers

- RFC 9457 "Problem Details" fields: `type`, `title`, `status`, `detail`, `instance` — the
  central serializer's canonical vocabulary (Chapter 20).
- Express error middleware is identified by **four** parameters `(err, req, res, next)`; NestJS
  filters implement `catch(exception, host)`; FastAPI uses
  `app.add_exception_handler(EXCEPTION_CLASS, handler)`.
- A central safety net must answer unknown errors with a stable fallback: `500`, correlation ID,
  **no stack** — recommendation: never more than one nested safety net per process.
- Centralization ROI appears when > ~5 routes exist; below that, a single utility function +
  one middleware is enough (recommendation).

## Real-world use case — Acme SaaS + `AgentRun`

Acme's LLM `AgentRun` endpoint initially relied on the global handler for everything: provider
`429`s became `500`s, and a token-limit error that could have fallen back to a smaller model
killed whole agent sessions. The two-halves fix:

1. **Local:** `AgentRun` recovered where it had context — token-limit → retry with truncated
   prompt; provider `429` → wait `Retry-After` once; tool timeout → substitute the tool's
   documented fallback value.
2. **Central:** everything still unhandled reached one filter that rendered the standard
   envelope with the correlation ID — including a new `AGENT_PROVIDER_DEGRADED` code the
   frontend already knew how to show.

Session success rate rose without the global handler learning a single business rule.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Central mechanics + local decisions (recommended) | Consistent contracts, correct decisions | Requires a shared error model | Default |
| Fully centralized | One file to read | Guesses on business context; god handler | Never beyond demos |
| Fully local | Fast to write per feature | Envelope drift, inconsistent statuses | Never beyond prototypes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep serialization and redaction in one module | Re-format errors in each route |
| Decide business outcomes where the state is | Ask the global handler to decide |
| Give the center a boring, total safety net | Give the center feature-specific logic |
| Pass decided errors *through* the center untouched | Have local code write response bodies directly |

## Common mistakes

- **Local code writing status codes directly** (`res.status(409)`) — the center's mapping now
  has a competitor; route-local writes are the first step to drift.
- **"Just one more if" in the filter** — every business `if` in the center is a future bug;
  move it down and give it a code.
- **Central retry** — a global handler that retries has no idea about idempotency; it will
  double-charge eventually.

## Checklist

- [ ] Every error response is produced by exactly one serializer.
- [ ] Business `if`-statements in central handlers: zero.
- [ ] Optional features recover locally with their own fallback.
- [ ] Unknown errors always surface as `500` + correlation ID, never swallowed.

## Related

- [The Machinery of Centralized Handling](./02-the-machinery-of-centralized-handling.md)
- [Limits of the Global Handler](./03-limits-of-a-global-handler.md)
- [A Global Handler and Local Recovery, Together](../03-practical-examples/01-global-handler-and-local-recovery.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
