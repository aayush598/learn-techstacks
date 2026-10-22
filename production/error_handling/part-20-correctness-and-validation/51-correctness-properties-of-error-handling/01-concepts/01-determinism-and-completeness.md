# Defined Outcomes, No Silent Discard, Deterministic Classification, Recoverable Causes (51.1–51.4)

> Part XX · Chapter 51 · Sections 51.1–51.4 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)

## In one sentence

The first four correctness properties guarantee that **error handling is a total function**: every
failure path ends in exactly one declared outcome, nothing disappears on the way, the same error is
always classified the same way, and the original cause survives to the end.

## Why this matters in production

These four properties are the difference between "we have error handling" and "we can reason about
our system when it breaks."

- An **undefined outcome** (51.1) means the caller cannot tell success from failure. The classic
  version is a function that returns `undefined` on the error path and a value on the success path,
  so `if (result)` silently treats failure as "no data".
- A **silent discard** (51.2) means a caught error that is neither propagated, nor translated, nor
  recorded. Nothing appears in your metrics, your logs, or the user's face — but the effect the
  operation was supposed to have is missing.
- **Non-deterministic classification** (51.3) means the same failure takes different routes
  depending on which layer noticed it: `ECONNRESET` is transient in the repository and permanent
  in the HTTP handler, so one path retries and the other 500s.
- A **lost cause** (51.4) means that at 3 a.m. the on-call engineer has a `500` and a request ID
  and nothing else.

## Core concept

### The outcome set

Define the terminal outcomes of an operation **once**, in one place, and make every path land in
one of them. Six outcomes cover essentially every production operation:

```text
   ┌──────────────────────────────────────────────────────────────┐
   │  TERMINAL OUTCOMES                                          │
   ├───────────────┬───────────────┬──────────────────────────────┤
   │ success       │ recovered     │ degraded                    │
   │ (all good)   │ (retried, ok) │ (partial value, flagged)    │
   ├───────────────┼───────────────┼──────────────────────────────┤
   │ failed        │ cancelled     │ unknown                     │
   │ (permanent)  │ (by request)  │ (outcome undetermined)       │
   └───────────────┴───────────────┴──────────────────────────────┘
```

Property 51.1 says: **every failure path ends in exactly one of these, and never in silence.**
Note that `unknown` is a first-class outcome. Many teams omit it, and that omission is the source
of the worst bugs — a timed-out charge that "must have failed, so retry it".

Property 51.2 says: **every caught error gets one of three dispositions**, and no others:

| Disposition | Meaning | Legal? |
| ----------- | ------- | ------ |
| **Propagate** | Rethrow (optionally wrapped with more context). | Yes |
| **Translate & propagate** | Convert to a domain error, then propagate. | Yes |
| **Recover & record** | Handle locally, and record the outcome durably or in telemetry. | Yes |
| Anything else | Swallow, log-and-continue, return `null`/`undefined`/`false` without recording. | ❌ Never |

> "Logged and continued" is a **discard** whenever the caller believes the operation succeeded.
> Logging is not a disposition; it is a side effect of disposition.

Property 51.3 says: **classification is a pure function of the failure**, not of the handler, the
clock, the tenant, or the deployment. Property 51.4 says: **the original cause survives** every
translation, so the failure remains reconstructable.

### The four properties as questions

| Property | The question it asks | Answered by |
| -------- | -------------------- | ----------- |
| 51.1 Defined outcome per failure path | *If this fails, what does the caller observe?* | A terminal-state model |
| 51.2 Never silently discarded | *Where does this error go after the catch?* | Three legal dispositions, enforced |
| 51.3 Deterministic classification | *Will this error be classified the same way everywhere?* | One classifier, called once |
| 51.4 Causes recoverable | *Can someone reconstruct this failure from the error alone?* | Preserved cause chain + context |

## How it works (mechanics)

### Making outcomes total

The cheapest enforcement is to make the type system express it. A function that returns
`Result<T, E>` cannot "return undefined" — the compiler forces every branch to name an outcome.

```ts
// ❌ Undefined outcome: the error path returns undefined, success returns data.
// The caller writes `const row = findUser(id); if (row) { ... }` and a DB outage
// is indistinguishable from "no such user".
async function findUser(id: string): Promise<User | undefined> {
  const res = await db.query(`SELECT * FROM users WHERE id=$1`, [id]);
  return res.rows[0];           // undefined on error AND on "not found"
}

// ✅ Total: every path names an outcome, and "not found" is distinct from "failed".
type Lookup<T> =
  | { outcome: "found"; value: T }
  | { outcome: "missing" }
  | { outcome: "failed"; error: AppError };

async function findUser(id: string): Promise<Lookup<User>> {
  try {
    const res = await db.query(`SELECT * FROM users WHERE id=$1`, [id]);
    const row = res.rows[0];
    return row ? { outcome: "found", value: row } : { outcome: "missing" };
  } catch (err) {
    return { outcome: "failed", error: translateDbError(err, { operation: "findUser", id }) };
  }
}
```

The same idea applies to state machines. A job whose states are `pending | running | done | failed |
cancelled | unknown` cannot get stuck, because `assertNever` makes every new state a compile error.

```ts
type JobState = "pending" | "running" | "done" | "failed" | "cancelled" | "unknown";

function isTerminal(s: JobState): boolean {
  return s === "done" || s === "failed" || s === "cancelled" || s === "unknown";
}

// At the end of every handler:
function settle(job: Job, outcome: JobState) {
  if (!isTerminal(job.state)) {
    // 51.1: no orphan states. Every non-terminal state has exactly one exit.
    throw new InvariantViolation(`job ${job.id} left in ${job.state}`);
  }
}
```

### Detecting silent discards

Static detection catches most of them:

```ts
// ❌ Four ways to discard, all invisible to the caller
try { await charge(); } catch {}
try { await charge(); } catch (e) { log.error(e); }        // logged but not recorded
try { await charge(); } catch (e) { return null; }
try { await charge(); } catch (e) { return undefined; }
```

Runtime detection catches the rest: **count errors and compare them to terminal records**. If an
operation recorded 41 failures but produced 0 terminal failure records, 41 failures were
discarded.

```sql
-- Reconciliation: every failure event must have a matching terminal record.
SELECT count(*) AS discarded_failures
FROM   error_events e
LEFT   JOIN operation_outcomes o
  ON   o.operation_id = e.operation_id
 AND   o.outcome IN ('failed','cancelled','unknown')
WHERE  o.operation_id IS NULL;
```

### Deterministic classification

Classification must be **pure, total, and centralized**. One function, one input shape, one output.

```ts
// ✅ One classifier, table-driven, pure. Same error ⇒ same decision, forever.
type Classification = {
  code: string;
  category: Category;
  retryable: boolean;
  severity: 1 | 2 | 3 | 4 | 5;
};

const BY_SQLSTATE: Record<string, Classification> = {
  "23505": { code: "DB_UNIQUE_VIOLATION", category: "conflict",  retryable: false, severity: 2 },
  "23503": { code: "DB_FK_VIOLATION",   category: "conflict",  retryable: false, severity: 2 },
  "40001": { code: "DB_SERIALIZATION",  category: "transient", retryable: true,  severity: 3 },
  "40P01": { code: "DB_DEADLOCK",       category: "transient", retryable: true,  severity: 3 },
};

export function classify(err: unknown): Classification {
  if (err instanceof AppError) return err.classification;      // already classified
  if (isPgError(err)) {
    const hit = BY_SQLSTATE[err.code];
    if (hit) return hit;
  }
  return { code: "UNCLASSIFIED", category: "internal", retryable: false, severity: 4 };
}
```

Two rules make 51.3 hold in practice:

1. **Classify once, at the origin.** Downstream layers read the classification; they never
   re-derive it. Re-deriving is where determinism dies.
2. **Never classify by message text.** `err.message.includes("timeout")` breaks the moment the
   driver changes its wording — and it is *localized*, so it breaks in a different order per
   locale.

### Preserving the cause

Property 51.4 is about *reconstructability*. To reconstruct, an operator needs: the operation, the
dependency, the vendor's own identifier, the attempt count, and the correlation ID.

```ts
// ❌ The cause is gone. The on-call engineer gets "checkout failed".
throw new Error("Checkout failed");

// ✅ The cause survives; context is added without discarding the original.
throw new CheckoutError({
  code: "PAYMENT_PROVIDER_UNAVAILABLE",
  operation: "checkout.capture",
  dependency: "stripe",
  attempt: 2,
  correlationId: ctx.correlationId,
  cause: err,                       // 51.4: the original error is the cause, not a string
  safeContext: { tenantId, planId, amountMinor },   // allowlist, no card data
});
```

What must never be dropped in translation: the **cause**, the **vendor error code**, the
**vendor request ID**, the **retryability decision**, and the **correlation ID**. Chapter 16 covers
the mechanics of lossless translation; 51.17 in this chapter makes it a property.

## Worked example — `WebhookIngest` (Acme SaaS)

Acme receives Stripe webhooks. The handler had four branches and three of them were wrong:

```ts
// BEFORE — violates 51.1, 51.2, 51.3, and 51.4 simultaneously.
app.post("/webhooks/stripe", async (req, res) => {
  try {
    const event = JSON.parse(req.body);            // parse failure → 500, no classification
    if (!verifySignature(req)) { return res.sendStatus(400); }   // 51.1: outcome is fine
    await applyEvent(event);                        // may throw anything
    res.sendStatus(200);
  } catch (err) {
    log.error(err);                                 // 51.2: discarded — no record, caller sees 200
  }
});
```

Two bugs, one cause. The `catch` returns nothing, so the request **never responds** — the client
times out and retries, and Stripe's retry delivers the same event again. Because the response was
never sent, Stripe treats it as a failure, so the event is redelivered forever.

After the fix:

```ts
app.post("/webhooks/stripe", async (req, res) => {
  const result = await ingest.handle(req);
  // 51.1: the outcome set is closed and the response is always sent.
  res.status(result.httpStatus).json(result.body);
});
```

`ingest.handle` classifies first, then dispatches on the classification — so the same malformed
payload always produces the same code, the same `Retry-After`, and the same recorded outcome.

## Key data / numbers

- **Outcome set size: 6** (success, recovered, degraded, failed, cancelled, unknown). If you cannot
  fit your operation into these six, your operation has an undefined state — model it explicitly.
- **Legal dispositions after a catch: 3** (propagate, translate-and-propagate, recover-and-record).
- **Classification calls per error: exactly 1.** Re-classification downstream is the most common
  source of non-determinism.
- **Discarded-error detection**: error-event count − terminal-record count must be **0**.
- **Golden corpus size**: 40–80 representative errors per service is enough to pin classification
  deterministically (one per category × one per vendor code).
- **Stripe webhook signature tolerance: 300 seconds** (5 minutes). A webhook older than that is
  rejected — treat `signature_timestamp_too_old` as permanent, not transient.
- **Reconstruction fields**: operation, dependency, vendor code, vendor request ID, attempt,
  correlation ID, timestamp — **7 fields** minimum.

## Real-world use case — Acme SaaS `Checkout`

Acme's `Checkout` created a `checkout_attempts` row, called Stripe, and then updated the
subscription. When Stripe timed out, the code caught the timeout and returned `null`. The API layer
interpreted `null` as "no error occurred" and returned **201 Created** with an empty body. The
customer saw a success screen; Acme had a `checkout_attempts` row with no subscription and no
Stripe charge.

The postmortem found four property violations in eleven lines of code: 51.1 (`null` was not a
declared outcome), 51.2 (the error was discarded), 51.3 (the timeout was classified as
`unknown` in one layer and `transient` in another), and 51.4 (the Stripe request ID was dropped, so
the Stripe dashboard could not be searched for the attempt).

The fix was not a new framework. It was three things: a closed outcome type, a single
`classify()` call at the provider adapter, and `cause` + `vendorRequestId` on the error object.
Reconciliation queries then proved the fix: unmatched error events went from 41/month to 0, and
"paid but no subscription" tickets dropped from 6/month to 0 within two weeks.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Closed outcome type (`Result`) | Compiler-enforced totality | Verbose; every call site must branch | Domain and application layers |
| `unknown` + runtime assertion | Cheap, no type churn | Runtime cost; can still be missed | Edge layers, third-party adapters |
| Exception-only | Familiar, low ceremony | Easy to discard; outcome implicit | Leaf code, internal utilities |
| Exception + closed result at the boundary | Both styles where they fit | Two conventions to teach | Most mature codebases |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model `unknown` as a real outcome | Assume a timeout means "failed" |
| Give every catch one of three dispositions | Log and continue |
| Classify once, at the origin | Re-derive the category in each layer |
| Classify by code/exception type, never by message text | `err.message.includes("timeout")` |
| Preserve `cause`, vendor code, vendor request ID | Replace the cause with a new string |
| Reconcile error counts against terminal records | Trust "we log every error" |

## Common mistakes

- **Returning `null` for failure.** It is indistinguishable from "not found" and from "the
  operation succeeded with no output". Use a closed union.
- **Catching to "handle it" and returning a default.** A default value silently becomes the answer.
  If you must default, mark it `degraded` and record it.
- **Classification in the presentation layer.** The HTTP handler is the worst place to decide
  "retryable" — it has no visibility into whether the effect already happened.
- **Losing the cause in a wrapper.** `new Error("Payment failed: " + err.message)` destroys the
  stack, the code, and the request ID. Use `{ cause: err }`.
- **Treating "logged" as "handled".** If no durable record exists and no effect is visible, the
  failure did not happen as far as the system is concerned.

## Checklist

- [ ] Every operation has a closed set of terminal outcomes, including `unknown`.
- [ ] Every catch block has exactly one of: propagate, translate-and-propagate, recover-and-record.
- [ ] No catch block ends in `return null` / `return undefined` / `return false` without a record.
- [ ] Classification happens exactly once, at the origin, and is stored on the error.
- [ ] No classification reads message text.
- [ ] Every error carries `cause`, operation, dependency, correlation ID, and vendor request ID.
- [ ] An error-count vs terminal-record reconciliation query exists and returns 0.

## Related

- [Safety, Resources, and Side Effects (51.5–51.9)](./02-safety-and-resource-properties.md)
- [Transformation and Contract Properties (51.10–51.12, 51.17–51.18)](./03-transformation-and-contract-properties.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
