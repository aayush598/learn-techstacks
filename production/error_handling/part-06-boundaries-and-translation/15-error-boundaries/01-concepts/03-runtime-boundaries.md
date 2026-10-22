# Runtime Boundaries: Request, Transaction, Job, Process, Service, Third-Party, UI

> Part VI · Chapter 15 · Sections 15.6–15.12 · _Estimated reading time: 24 min_
> **Prerequisite:** [Code-Level Boundaries](./02-code-level-boundaries.md)

## In one sentence

Above the code-level boundaries sits the set of **runtime boundaries** — request, transaction,
job, process, service, third-party, and UI — each defined by a unit of work that must reach a
**defined terminal state** no matter what fails inside it.

## Why this matters in production

These are the boundaries that decide whether a failure becomes an outage, a stuck record, or a
lost job. The request boundary decides the HTTP response; the transaction boundary decides
atomicity; the job boundary decides retry; the process boundary decides whether the whole
instance survives; the service boundary decides cross-service contracts; the third-party boundary
decides degradation; the UI boundary decides whether the user sees a broken page. Miss one and the
failure propagates into a domain that cannot handle it.

---

## 15.6 — Request-level boundary

The unit is **one request** (one HTTP call, one gRPC call, one GraphQL operation). Its job: catch
everything, translate to the transport contract, and **never leak internals**. This is the
canonical outermost boundary for interactive traffic.

```ts
// Express-style request boundary (middleware order matters).
app.use((err, req, res, _next) => {
  const requestId = req.id;

  if (err instanceof DomainError) {
    // expected business outcome — stable code + client-actionable status
    return res.status(err.httpStatus ?? 422).json({
      type: "https://errors.acme.example/domain",
      title: err.code,
      status: err.httpStatus ?? 422,
      detail: err.safeMessage,
      instance: requestId,
    });
  }

  // unknown/unexpected — generic, no internals; log the full cause server-side
  log.error({ err, requestId }, "unhandled request error");
  return res.status(500).json({
    type: "about:blank",
    title: "INTERNAL_ERROR",
    status: 500,
    detail: "An unexpected error occurred.",
    instance: requestId,
  });
});
```

Key properties: single owner (the transport layer), one response shape (RFC 9457 — see Ch. 20),
correlation ID attached, and **no stack traces or SQL in the body**.

## 15.7 — Transaction-level boundary

The unit is **one database transaction** (or unit of work). Its job: guarantee atomicity — either
everything commits or nothing does — and translate commit/rollback failures.

```python
# Transaction boundary: one unit of work; commit failure is itself an error to handle.
def place_order(db, order):
    with db.transaction():          # BEGIN
        db.insert(order)            # may raise IntegrityError
        db.decrement_stock(order)   # may raise; rolls back the insert
    # commit happens on successful exit; a commit failure raises here
```

Rules for a transaction boundary:

- **Rollback is part of the boundary**, not an afterthought.
- **Commit failure is ambiguous** — the write may or may not have landed (connection lost after
  `COMMIT`). Treat as an uncertain outcome and check via idempotency (Ch. 23).
- **Never swallow** an error inside the transaction and still commit — you will persist partial state.
- Serialization failures (`SQLSTATE 40001`) and deadlocks (`40P01`) are **transient** and often
  retried by the transaction owner, not the repository.

## 15.8 — Job-level boundary

The unit is **one background job / message**. Its job: run the task to a terminal state
(success, retry, or dead-letter) and **survive partial completion**.

```go
// Job boundary: classify the outcome; never crash the worker loop.
func runExportJob(ctx context.Context, job ExportJob) error {
    if err := doExport(ctx, job); err != nil {
        var transient interface{ Temporary() bool }
        switch {
        case errors.As(err, &transient) && transient.Temporary():
            return err // signal retry to the queue
        default:
            return fmt.Errorf("permanent failure: %w", err) // route to DLQ
        }
    }
    return nil
}
```

The job boundary decides: **retry**, **dead-letter**, or **terminal success**. It records enough
context for a later replay (Ch. 32). It must not assume the job ran exactly once.

## 15.9 — Process-level boundary

The unit is **the process / instance**. Its job: handle uncaught exceptions and unhandled promise
rejections so the runtime exits or recovers **safely**, and so no resource is left corrupt.

```ts
// Process boundary: last resort. Log, attempt a clean shutdown, then exit.
process.on("uncaughtException", (err) => {
  log.fatal({ err }, "uncaught exception; shutting down");
  server.close(() => process.exit(1));
  setTimeout(() => process.exit(1), 10_000).unref(); // hard deadline
});

process.on("unhandledRejection", (reason) => {
  log.error({ reason }, "unhandled rejection");
  // In Node ≥15 this terminates by default; a boundary may choose to keep running
  // only if the rejection is known to be harmless — usually it is not.
});
```

> ⚠️ **Hazard.** Continuing after an uncaught exception leaves the process in an unknown state.
> Fail-fast with a clean shutdown is almost always safer than "keep going."

## 15.10 — Service-level boundary

The unit is **one service** in a distributed system. Its job: define and honor the **error contract**
across the network — turn internal errors into a stable, documented protocol (HTTP status + body,
gRPC status code) and never leak another service's internals.

| Direction | Boundary concern |
| --------- | ---------------- |
| **Inbound** | A caller's request that is malformed/unauthenticated is rejected consistently |
| **Outbound** | A dependency's failure is translated to **your** contract, not replayed verbatim |
| **Cross-service** | Contracts align: an `ALREADY_EXISTS` here maps consistently from upstream |

gRPC mapping example: unique violation → `ALREADY_EXISTS` (6), not found → `NOT_FOUND` (5),
rate limit → `RESOURCE_EXHAUSTED` (8), transient → `UNAVAILABLE` (14).

## 15.11 — Third-party integration boundary

The unit is **one external dependency** (Stripe, S3, an LLM provider). Its job: contain the
vendor's format, authentication failures, and outages; translate to internal errors; decide
degradation.

```ts
// Integration boundary: adapt the vendor error into the internal model + retry class.
function translateStripe(err: StripeError): AppError {
  switch (err.type) {
    case "card_error":
      return new DomainError("PAYMENT_CARD_DECLINED", { details: { code: err.code } });
    case "rate_limit_error":
      return new TransientError("PAYMENT_PROVIDER_RATE_LIMITED", { retryAfterMs: 2_000 });
    case "api_connection_error":
      return new TransientError("PAYMENT_PROVIDER_UNAVAILABLE");
    case "authentication_error":
      return new ConfigError("PAYMENT_PROVIDER_AUTH_FAILED"); // operational, not retryable
    default:
      return new InfrastructureError("PAYMENT_PROVIDER_ERROR", { cause: err });
  }
}
```

This boundary is where **vendor coupling dies**. Downstream code should never see `card_error` or a
Stripe request ID.

## 15.12 — UI boundary

The unit is **a component / page / app subtree**. Its job: keep a render or data error from
blanking the whole screen, and offer recovery (retry button, cached data, placeholder).

```tsx
// React error boundary: contains render errors to this subtree.
class WidgetBoundary extends React.Component {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    reportClientError(error, info.componentStack); // ship to error reporting
  }
  render() {
    return this.state.failed
      ? <WidgetFallback onRetry={() => this.setState({ failed: false })} />
      : this.props.children;
  }
}
```

Note: React error boundaries catch **render/lifecycle** errors, not event handlers, async code, or
data fetching — those need their own boundaries (Ch. 37). A failed API call inside a component
must set an error state, not throw during render.

## How the runtime boundaries stack

```text
UI subtree  ──►  HTTP client  ──►  [network]  ──►  Request boundary (service A)
                                                    ├─ Transaction boundary
                                                    │   └─ Repository boundary (DB→domain)
                                                    └─ Integration boundary (Stripe/S3/LLM)
Job worker loop  ──►  Job boundary  ──►  Process boundary (runtime)
```

Each line must have: **one owner, a defined fallback, a translation, and a terminal state.**

## Key data / numbers

- HTTP status decision belongs to the request boundary: `400`/`422` validation, `401`/`403` auth,
  `404` missing, `409` conflict, `429` rate limit, `503`/`504` upstream.
- gRPC codes for service boundaries: `ALREADY_EXISTS`=6, `NOT_FOUND`=5, `UNAVAILABLE`=14,
  `DEADLINE_EXCEEDED`=4, `RESOURCE_EXHAUSTED`=8.
- Stripe error types: `card_error`, `rate_limit_error`, `api_connection_error`,
  `authentication_error`, `invalid_request_error`, `idempotency_error`.
- S3 error codes: `SlowDown` (`503`), `RequestTimeout`, `AccessDenied`, `NoSuchKey`.

## Real-world use case — WebhookIngest

`WebhookIngest` sits at a **third-party + request boundary**. The request boundary verifies the
Stripe signature: a missing/invalid signature is a **permanent, local** failure → return `400`, log
at `warn`, never retry. A signature-verification service *timeout* is **transient, remote** → the
webhook is retried by Stripe. Inside, a duplicate event is contained by an idempotency check (not
an error at all). Three different outcomes, three different boundaries, one endpoint.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each runtime unit a defined terminal state | Leave "impossible" states undefined |
| Translate vendor errors to internal ones at integration boundaries | Let `card_error` reach the domain |
| Treat commit failure as ambiguous | Assume a lost `COMMIT` response means failure |
| Fail-fast at the process boundary | Continue after an uncaught exception |

## Common mistakes

- **Replaying an upstream status verbatim.** Returning a dependency's `404` for *your* resource.
- **Job boundary that crashes the worker loop.** One poison message stalls the queue (Ch. 32).
- **Transaction committed despite an inner swallow.** Partial state persists; accounting breaks.
- **UI error boundary expected to catch async errors.** It does not; data paths need their own.

## Checklist

- [ ] Every request has one outer boundary producing the contract response.
- [ ] Every transaction rolls back on failure and treats commit failure as ambiguous.
- [ ] Every job reaches success / retry / DLQ — never "stuck."
- [ ] Every service translates inbound/outbound errors to its own contract.
- [ ] Every vendor has an integration boundary that removes coupling.
- [ ] Every UI subtree has a boundary and a recovery affordance.

## Related

- [Code-Level Boundaries](./02-code-level-boundaries.md)
- [Ownership, Granularity, and Fallback Behavior](./04-ownership-granularity-and-fallback.md)
- [Nested Boundaries](../02-deep-dive/01-nested-boundaries.md)
