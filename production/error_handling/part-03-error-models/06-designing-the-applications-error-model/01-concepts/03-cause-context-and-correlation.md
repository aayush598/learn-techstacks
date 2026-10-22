# Cause, Context, and Correlation

> Part III · Chapter 6 · Sections 6.8–6.12 · _Estimated reading time: 20 min_
> **Prerequisite:** [Core Identity Fields](./02-core-identity-fields.md)

## In one sentence

The **cause** preserves why the error happened, the **context** records the safe circumstances,
the **stack trace** preserves where it happened, and the **correlation ID** ties everything to one
request or workflow — together they turn a terse code into a debuggable event.

## Why this matters in production

An error with a code and message but no cause, tenant, or correlation is a dead end: you know
*something* failed but not what triggered it, for whom, or in which request. At 2am during an
incident, the difference between "`PAYMENT_FAILED`" and "`PAYMENT_PROVIDER_TIMEOUT` caused by
`fetch ETIMEDOUT` for tenant `t_acme` request `req_8f3`" is the difference between a 45-minute
investigation and a 2-minute fix.

## Original cause (6.8)

Every translation and wrap must **preserve the original cause**. Losing it is the single most
common reason production errors are undebuggable.

JavaScript has a native mechanism (ES2022): `new Error(msg, { cause })`. Many languages do not, so
carry an explicit `cause` field.

```ts
try {
  await stripe.charges.create(params);
} catch (native) {
  // WRONG: throw new PaymentError("PAYMENT_FAILED", "Charge failed");
  throw new PaymentError("PAYMENT_PROVIDER_TIMEOUT", "Stripe request timed out", { cause: native });
}
```

Rules:

- **Wrap, don't replace.** The new error adds meaning; it does not erase the old one.
- **Never `catch (e) { throw new Thing() }`** — pass `e` as cause.
- **Bound the chain.** Cap depth (commonly 10–20) to avoid runaway chains and memory growth.

## Context and safe metadata (6.9)

`metadata` carries the **safe, structured facts** a handler or log consumer needs: tenant, resource
IDs, attempt number, provider name, feature flag state. It is the machine-readable companion to the
message.

```ts
metadata: {
  tenantId: "t_acme",
  orderId: "ord_123",
  provider: "stripe",
  attempt: 2,
}
```

Rules for metadata:

- **Allowlist, not denylist.** Only add known-safe keys.
- **Scalars and small arrays only.** No large blobs, no nested user objects.
- **No secrets, tokens, PII, or full request bodies** (Chapter 36 — redaction).
- **Stable key names** so logs and dashboards can index them.

> ⚠️ **Hazard.** `metadata` is the most common accidental-disclosure channel. A single
> `metadata: { ...req.body }` can ship passwords and tokens into every log and error response.

## Stack trace preservation (6.10)

The stack trace is *where* in the code the error occurred. Preserve it through wrapping:

- **Native JS:** the original error keeps its `stack`; when you wrap, keep `cause` so the stack is
  reachable.
- **Some runtimes reset the stack on rethrow.** Capture `err.stack` at creation into a field if the
  runtime does not preserve it through wrapping.
- **Never send stacks to clients.** Stacks reveal paths, versions, and internals (Chapter 34).
  Send them to logs/traces only.

```ts
class AppError extends Error {
  readonly stackTrace: string;
  constructor(msg: string, opts?: ErrorOptions) {
    super(msg, opts);
    this.stackTrace = this.stack ?? "";
  }
}
```

## Creation time and operation context (6.11)

- **`timestamp`** — ISO-8601 UTC at creation. Used to correlate with logs, measure latency to
  failure, and order events.
- **Operation context** — what was being done: `operation: "createExport"`, `step: "uploadToS3"`,
  `jobId: "job_88"`. Context tells a reader *which phase* failed, which is often more useful than
  the code alone in multi-step workflows.

```ts
{
  operation: "checkout.capture",
  step: "provider-call",
  timestamp: "2026-03-01T10:22:01.482Z",
}
```

Do **not** record wall-clock durations as a substitute for tracing; just record the timestamp and
let the trace system compute deltas.

## Request and correlation IDs (6.12)

A **correlation ID** is stable across *all* errors in one logical operation, including across
services and asynchronous boundaries. A **request ID** is per inbound request.

| ID | Scope | Source | Use |
| -- | ----- | ------ | --- |
| `requestId` | One inbound HTTP request | Generated at the edge (or from a gateway/trace header) | Log lookup for one request |
| `correlationId` | One end-to-end logical operation | Propagated through calls/jobs/events | Cross-service and async tracing |
| `traceId` / `spanId` | Distributed trace | OpenTelemetry or similar | Full trace view |

```ts
// Propagate the correlation ID into the job payload, not just the request.
interface ExportJobPayload { correlationId: string; tenantId: string; queryId: string; }
```

The correlation ID must **survive queue hops**. A job that starts an hour after the request still
carries the same `correlationId`, so an operator can see the whole story.

## Worked example

```ts
async function capture(order: Order, ctx: RequestContext): Promise<void> {
  try {
    await stripe.charges.create({ amount: order.total, currency: order.currency });
  } catch (native: unknown) {
    throw new PaymentError("PAYMENT_PROVIDER_TIMEOUT", "Stripe capture timed out", {
      cause: native,
      metadata: { tenantId: ctx.tenantId, orderId: order.id, provider: "stripe" },
      correlationId: ctx.correlationId,
      operation: "checkout.capture",
    });
  }
}
```

If this fails, a log line contains: the code, the human message, the original network error, the
tenant, the order, the provider, and the correlation ID — everything a responder needs, and no
secrets.

## Key data / numbers

- **`Error.cause`** is standard in Node.js ≥ 16.9 and ES2022; use it where available.
- **Cap cause-chain depth at 10–20** links; beyond that, log the chain and stop.
- **Timestamp format:** ISO-8601 with milliseconds and `Z` (`2026-03-01T10:22:01.482Z`).
- **Correlation IDs** are conventionally 128-bit random hex or a ULID for sortability.
- **W3C Trace Context** (`traceparent`) is the standard header for propagating trace IDs across
  services.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` processes Stripe events. A failure logged only `"webhook failed"`, so
operators could not tell whether the signature was invalid, the event was a duplicate, or the
handler threw. After adopting the model, every failure carries `correlationId` (reused from the
Stripe event ID), `metadata.eventId`, `metadata.eventType`, the `cause` (a Stripe verification
error or a DB error), and the operation step. Mean time to diagnosis for webhook incidents fell
from ~40 minutes to under 10 because one grep on the correlation ID reassembled the whole story.

## Trade-offs

| Field | Always on? | Cost | Benefit |
| ----- | ---------- | ---- | ------- |
| `cause` | Yes | Small memory | Root-cause debugging |
| `metadata` | Yes (safe keys) | Small | Routing + triage |
| `stackTrace` | Yes internally | CPU/memory in hot paths | Locating the fault |
| `correlationId` | Yes | Negligible | Cross-service tracing |
| Full request body | **No** | Large + leak risk | Almost never justified |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve the original `cause` on every wrap | `throw new Error("failed")` and lose the cause |
| Allowlist safe metadata keys | Spread `req.body` or `process.env` into metadata |
| Propagate correlation IDs through queues | Generate a new ID at each hop |
| Send stacks to logs only | Serialize `stack` into HTTP responses |

## Common mistakes

- **Dropping the cause** in a catch-and-rethrow.
- **Unbounded cause chains** from retry loops appending a new cause each attempt.
- **Per-hop correlation IDs** that break the end-to-end story.
- **Context without keys** — free-text blobs that cannot be indexed or queried.
- **PII in metadata** because it was convenient at the call site.

## Checklist

- [ ] Does every wrap pass the original error as `cause`?
- [ ] Is `metadata` built from an allowlist of safe keys?
- [ ] Is cause-chain depth bounded?
- [ ] Does `correlationId` propagate across every async boundary?
- [ ] Are stack traces excluded from client responses?

## Related

- [Validation Details and Chaining](./04-validation-details-and-chaining.md)
- [Preventing Sensitive Data](./05-immutability-serialization-and-safety.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
