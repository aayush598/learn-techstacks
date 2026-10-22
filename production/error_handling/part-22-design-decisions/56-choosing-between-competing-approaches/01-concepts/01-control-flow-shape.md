# Control-Flow Shape: Throw vs Return, Exceptions vs Results, Aggregate vs First-Error

> Part XXII · Chapter 56 · Sections 56.1, 56.7, 56.14 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 7 — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)

## In one sentence

The **shape of failure** — thrown, returned, or collected — should be decided by whether the
caller can *enumerate the possible failures*, not by which style the author prefers.

## Why this matters in production

Control-flow shape is the most consequential and least examined decision in error handling,
because it determines whether a failure can be **forgotten**.

- An **exception** is invisible to the type system. A function that throws is type-identical to
  one that does not, so a caller who forgets to handle it compiles, deploys, and 500s.
- A **result** is visible. `const r = await charge();` forces a branch on `r.ok`, so a forgotten
  failure becomes a compile error rather than a production incident.
- But a **result everywhere** has its own failure mode: nested `Result<Result<T, E1>, E2>` chains
  make the happy path unreadable, and developers start writing `unwrap()` helpers that
  reintroduce exceptions with worse ergonomics.

The third decision — **aggregate all failures or fail on the first** — determines whether a
user sees "3 of 5 fields are invalid" or a generic "validation failed", and whether a bulk
import of 10,000 rows aborts at row 3,417.

## Core concept

### The three shapes

```text
  THROW (unwind)                    RETURN (bind)                    COLLECT (fold)
  ┌──────────────┐                  ┌──────────────┐                ┌──────────────┐
  │ f() throws   │                  │ f() returns  │                │ f() returns  │
  │   ↓ unwind   │                  │   Result     │                │   Result[]   │
  │ caller's     │                  │   caller must│                │   caller sees│
  │ try/catch    │                  │   branch     │                │   all of them│
  └──────────────┘                  └──────────────┘                └──────────────┘
  caller may forget                 caller cannot forget            caller pays for volume
  ← good for rare/unexpected        ← good for known failure       ← good for bulk input
    programmer errors                  sets and domain rules          and multi-step ops
```

### Decision table

| Question | If **yes** | If **no** |
| -------- | ----------- | --------- |
| Can the caller enumerate the failure set? | **Return a result** | **Throw** |
| Is the failure an expected business outcome (not found, declined)? | **Return a result** | — |
| Is the failure a programmer error (null deref, type violation)? | — | **Throw** (or better: don't allow it) |
| Do you need to branch on the failure *type*? | **Result** with a discriminated union | Throw with typed classes is acceptable |
| Is the error a "last resort" you cannot classify? | — | **Throw** |
| Are there many operations to run over a collection? | **Collect** | — |

### 56.1 — Exceptions vs results

The distinction that actually matters is **not** "exceptions are idiomatic in this language". It
is: **is the failure part of the operation's contract?**

- `getUser(id)` — "no such user" is a legitimate answer. It belongs in the return type.
- `chargeCard(...)` — "the card was declined" is also a legitimate answer.
- `serializeConfig(raw)` — "this file is malformed" is a legitimate answer.
- `connectToDatabase()` — "the database is unreachable" is an *environmental* fact, not a
  value the caller can meaningfully receive. Throwing (or returning a transport-level error)
  is fine.

A rule that holds up in practice:

> **Return the failures that are part of the domain's vocabulary; throw the ones that are
> violations of the system's assumptions.**

### 56.7 — Throwing vs returning

This is the same question at a different altitude: *where does the failure get represented?*

| Layer | Recommended shape | Reason |
| ----- | ----------------- | ------ |
| Domain / application service | Result or typed error | The caller must branch on the failure |
| Adapter (DB, HTTP client) | Translate to a domain error, then **throw or return per the layer contract** | Adapters should not decide the caller's style |
| Transport (HTTP handler) | Catch once, serialize | The transport owns the external contract |
| Job worker | Catch once, classify into a job outcome | The worker owns retries and DLQ |
| Utility / leaf function | Throw | Nobody upstream has a use for a `Result` here |

The mistake to avoid is a **mixed style without a rule**. A codebase where `serviceA` returns
`Result` and `serviceB` throws, with no boundary between them, makes every call site a
guess. Pick per *layer*, and write the rule down.

### 56.14 — Aggregation vs first-error

Two different questions hide under "aggregation vs first-error":

**Q1: Does the caller need to know *all* failures?**

- **Validation of a single request** → aggregate. A user fixing a form needs every bad field,
  not the first one. Return a list of field-level errors; respond `422 Unprocessable Entity`
  with `errors: [...]`.
- **A multi-step workflow** → aggregate *per step*, but **fail fast between steps**. If step 1
  (reserve inventory) fails, do not attempt step 2 (charge card). The failures are ordered and
  dependent, so continuing adds load without adding information.

**Q2: Is the operation over a collection?**

- **Bulk import of 10,000 rows** → aggregate. Return a report: `processed: 9,982, failed: 18,
  failures: [...]`. Aborting at row 3,417 wastes the customer's work and produces a support
  ticket.
- **A pipeline of independent fetches** → aggregate but **bounded**. Collect at most N
  failures (say 25) and note that the count was truncated; unbounded aggregation is a memory
  leak with a business vocabulary.

> ⚠️ **Hazard.** Aggregation hides the *ordering* of failures. If one failure invalidates
> another (a duplicate email plus a password mismatch), reporting both is confusing. Rule:
> aggregate **independent** failures; report the first **dependent** one.

## How it works (mechanics)

### A hybrid that actually works

The hybrid — result in the domain, exception at the edge — is not a compromise; it is the
design most mature codebases converge on:

```ts
// ✅ Domain layer: the failure set is enumerable, so it is in the type.
export type CheckoutOutcome =
  | { ok: true; subscriptionId: string }
  | { ok: false; error: CheckoutError };

export type CheckoutError =
  | { code: "PAYMENT_CARD_DECLINED"; retryable: false }
  | { code: "PLAN_NOT_PURCHASABLE"; retryable: false }
  | { code: "PAYMENT_PROVIDER_UNAVAILABLE"; retryable: true; retryAfterSeconds: number };

export async function startCheckout(
  input: CheckoutInput,
): Promise<CheckoutOutcome> {
  const plan = await plans.find(input.planId);            // -> Result<Plan, NotFound>
  if (!plan.ok) return { ok: false, error: { code: "PLAN_NOT_PURCHASABLE", retryable: false } };

  const charge = await payments.charge(input);            // -> Result<Charge, PaymentError>
  if (!charge.ok) return { ok: false, error: charge.error };

  await subscriptions.activate(charge.value.id);
  return { ok: true, subscriptionId: charge.value.id };
}
```

The transport then converts the outcome into an HTTP response in exactly one place:

```ts
// ✅ Transport layer: one place that knows about status codes.
app.post("/checkout", async (req, res) => {
  const outcome = await startCheckout(parseCheckout(req.body));
  if (outcome.ok) return res.status(201).json({ subscriptionId: outcome.subscriptionId });

  const meta = registry.get(outcome.error.code);        // status, public title, retryable
  res.status(meta.httpStatus).json(problemFrom(outcome.error, req.id));
});
```

Notice what did **not** happen: no `try/catch` in the domain, no `null` returns, no
`success: false` inside a `200`. The caller's obligation is visible in the type.

### Aggregation, bounded

```ts
// ✅ Bounded aggregation for a bulk import.
const MAX_REPORTED_FAILURES = 25;

export type ImportReport = {
  processed: number;
  failed: number;
  failures: RowFailure[];      // at most MAX_REPORTED_FAILURES
  failuresTruncated: boolean;  // true when failed > failures.length
};

export async function importRows(rows: RowInput[]): Promise<ImportReport> {
  const failures: RowFailure[] = [];
  let processed = 0;
  let failed = 0;

  for (const [index, row] of rows.entries()) {
    const parsed = validateRow(row);
    if (!parsed.ok) {
      failed++;
      if (failures.length < MAX_REPORTED_FAILURES) {
        failures.push({ row: index + 1, issues: parsed.error.issues });
      }
      continue;               // independent failure → keep going
    }
    await persistRow(parsed.value);
    processed++;
  }

  return { processed, failed, failures, failuresTruncated: failed > failures.length };
}
```

> **Bound the collection, not the work.** The cap belongs on the *report*, not on the attempt:
> you still process all 10,000 rows, you just stop collecting detail after 25.

### First-error for dependent steps

```ts
// ✅ Ordered, dependent steps → fail fast between steps.
export async function runOnboarding(steps: Step[]): Promise<OnboardingResult> {
  const completed: string[] = [];

  for (const step of steps) {
    const outcome = await step.run();
    if (!outcome.ok) {
      return {
        ok: false,
        failedStep: step.name,
        error: outcome.error,
        completed,          // tells the operator where to resume
      };
    }
    completed.push(step.name);
  }

  return { ok: true, completed };
}
```

## Worked example — `Checkout` (Acme SaaS)

Acme's `Checkout` originally threw `StripeError` from the payment adapter and let it reach the
controller. The controller had a `catch` that mapped `err.type` to a status code. Three
problems followed:

1. A `StripeError` with an unrecognized `type` fell through to `500` — a card decline
   (customer's problem) surfaced as "internal error" and triggered an on-call page.
2. The controller's `switch` on `err.type` was **vendor-coupled**: when Stripe renamed
   `card_error` to `card_declined`, the mapping silently fell through and every decline
   became a 500.
3. Because the domain used exceptions, the *caller* of `startCheckout` — the subscription
   activation service — could not tell a decline from a provider outage, so it retried
   declines.

The fix used the rubric above:

- The payment adapter **translates** the vendor error into a domain error with a stable code
  and a `retryable` flag (see 56.8), and returns it as a `Result` (56.1, 56.7).
- The domain returns a `CheckoutOutcome` union; the **caller branches** on it.
- The transport maps `PAYMENT_CARD_DECLINED` → `402 Payment Required` via the registry, and
  `PAYMENT_PROVIDER_UNAVAILABLE` → `503 Service Unavailable` with a `Retry-After` header.

Result: declines stopped appearing in the 5xx dashboards, the subscription service stopped
retrying non-retryable failures, and adding a new decline reason no longer required editing a
controller.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Union variants in a domain result | 3–7 | Above 7, split by outcome class; the union stops being readable |
| Max reported validation failures in one response | 20–50 | Above 50, the user cannot act; summarize the rest by field |
| Max failures collected in a bulk operation report | 25 (recommended), 100 (hard cap) | Always return `failuresTruncated` |
| Max aggregation in a parallel operation | 10 | Beyond 10, switch to a per-item status list |
| HTTP status for aggregated field validation | `422 Unprocessable Entity` | `400` for malformed syntax, `422` for well-formed but invalid |
| Retryable flag | Derived from the registry, never from a message | One source of truth (Chapter 8) |
| Minimum `Retry-After` on a retryable outcome | 1 second | Sub-second retries are a storm (Chapter 57) |
| Error `detail` length in an HTTP body | ≤ 200 characters | Detail is for humans, not logs |

## Real-world use case — `WebhookIngest` (Acme SaaS)

`WebhookIngest` receives Stripe events. Two failure shapes had to coexist:

- **Malformed payload** — a validation failure with 3 field-level issues. The sender cannot
  fix it by retrying, and Acme needs the details to debug it.
- **Duplicate delivery** — a *successful* outcome, not an error. Stripe retries on
  non-2xx, so returning `200` for an already-processed event is the correct idempotent answer.

The team first modeled duplicates as an error, which produced `409 Conflict` responses, which
made Stripe retry harder, which produced more duplicates — a self-inflicted storm (Chapter 57).

The fix separated the three outcomes explicitly:

```ts
export type IngestOutcome =
  | { ok: true; disposition: "applied" | "duplicate"; eventId: string }
  | { ok: false; error: IngestError };

export type IngestError =
  | { code: "WEBHOOK_SIGNATURE_INVALID"; retryable: false }
  | { code: "WEBHOOK_PAYLOAD_INVALID"; retryable: false; issues: FieldIssue[] }
  | { code: "WEBHOOK_DEPENDENCY_UNAVAILABLE"; retryable: true; retryAfterSeconds: number };
```

`WebhookIngest` returns `200` for `duplicate`, `400` for signature/payload failures, and
`503` with `Retry-After: 5` for a dependency outage — which tells Stripe exactly when to come
back. One more detail mattered: **the signature failure and the payload failure were
aggregated into one response** when both applied, because they are independent — a request can
have a bad signature *and* a malformed body, and reporting both at once saves a round trip.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Exceptions only | Low ceremony; familiar; fast to write | Forgotten handling compiles; type system blind | Leaf utilities, programmer errors |
| Results only | Compiler-enforced; explicit | Verbose; nested unions hurt readability | Domain/application layers with enumerable failures |
| Hybrid by layer | Each layer uses its natural shape | Needs a written rule, else looks inconsistent | Most production codebases |
| Aggregated failures | User fixes everything in one pass | More bytes; hides ordering | Validation, bulk operations |
| First-error only | Simple; stops wasted work | User fixes one field per round trip | Ordered, dependent steps |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put domain failures in the **return type** | Throw `BusinessException` for "not found" |
| Pick one shape **per layer** and write the rule down | Mix styles with no boundary |
| Aggregate **independent** failures; fail fast between **dependent** steps | Aggregate everything, including ordered steps |
| Cap the collected failures and report truncation | Collect unbounded failures into memory |
| Treat a duplicate webhook as a **success** | Return `409` and trigger a retry storm |
| Use `422` for well-formed but invalid input | Use `400` for everything invalid |

## Common mistakes

- **Throwing from the domain to "keep the code short".** The cost lands on every caller, all
  of whom now must remember to catch. The short code is the long bug.
- **`unwrap()` / `unwrapOrDefault()` everywhere.** This is exceptions wearing a costume: the
  failure still escapes as an exception, and the type no longer says so.
- **Aggregating dependent failures.** Reporting "invalid email" and "subscription not active"
  together is noise; the second is a consequence of the first.
- **Reporting the first validation error and returning `400`.** Users fix fields one at a
  time; a per-field list is strictly better for conversion and support load.
- **Using `null`/`undefined` as the failure channel.** `undefined` conflates "not found",
  "failed", and "no value" — three different operational stories.

## Checklist

- [ ] Every domain operation returns a closed outcome type, including an `unknown` variant.
- [ ] Every adapter translates vendor errors into domain codes before returning.
- [ ] The control-flow rule (which layer throws, which returns) is written in your repo docs.
- [ ] Validation responses carry a **field-level list**, with `422` for semantic failures.
- [ ] Bulk and parallel operations **cap** collected failures and report truncation.
- [ ] Ordered multi-step workflows stop at the first failed step and record what completed.
- [ ] No `null` / `undefined` is used as a failure signal.

## Related

- [Structure and Ownership (56.2, 56.3, 56.9–56.12)](./02-structure-and-ownership.md)
- [Recovery Policy Trade-offs (56.4, 56.5, 56.6, 56.15, 56.16)](./03-recovery-policy-tradeoffs.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
