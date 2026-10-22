# Limits of the Global Handler

> Part IV · Chapter 10 · Sections 10.10, 10.11 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Machinery of Centralized Handling](./02-the-machinery-of-centralized-handling.md)

## In one sentence

A global handler sees **an error object and nothing else** — no transaction state, no attempt
count, no partial progress — so any *business* decision it makes is a guess, and hidden guesses
are how systems double-charge customers.

## Why this matters in production

"The global handler will take care of it" is the most expensive sentence in error handling.
Because the handler sits at the edge, it is structurally blind to everything that makes a
decision correct:

- It cannot know the payment already succeeded when the **email** step failed (partial
  progress), so it marks the whole checkout failed.
- It cannot know the operation is idempotent, so its "helpful" retry duplicates a charge.
- It cannot know `409` here means "user should pick another slug" versus "two admins raced, and
  the second should just succeed."
- It cannot know the tenant is on a plan that tolerates degraded features, so it fails the whole
  request instead of degrading.

Every one of these has shipped somewhere. The pattern's alias is the **hidden business decision
(10.11)**: logic that looks like infrastructure but encodes product policy — unreviewed by
product people, untested by domain tests, invisible in the architecture doc.

## Core concept — what the handler can and cannot know

| The handler CAN | The handler CANNOT |
| --------------- | ------------------ |
| Map a stable code → status/title (mechanical) | Decide whether this code is retryable *here* |
| Attach correlation ID, redact, log | Know how many attempts already happened |
| Render RFC 9457 for unknown errors | Know what side effects completed |
| Terminate unclassified errors safely | Know whether compensation is required or possible |
| Enforce "no stack traces leak" | Know tenant entitlements or business severity |

The dividing line: **mechanical policy is total and context-free; business policy is partial and
context-rich.** A global handler can only honestly implement the former.

## How hidden business decisions sneak in

Six recognizable forms — each with the fix:

```ts
// 1. Status invention from message text
if (err.message.includes("slug")) res.status(409);           // ❌ text matching is not classification
// fix: map registered codes only

// 2. Retry in the handler
if (isRetryable(e)) return retry(() => originalWork());       // ❌ handler has no idempotency knowledge
// fix: retry in the application/worker that owns the operation

// 3. Failure-to-success conversion
if (e.code === "SUMMARY_UNAVAILABLE") return res.json({ summary: null, ok: true }); // ❌ optional-feature policy in the center
// fix: the feature's own boundary degrades locally

// 4. Compensation in the handler
if (e.code === "CHARGE_SUCCEEDED_EMAIL_FAILED") await refunds.reverse(); // ❌ saga steps at the edge
// fix: the checkout saga (application layer) owns compensation

// 5. Severity/tier branching
if (tenant.plan === "enterprise") res.status(200).json({ degraded: true }); // ❌ entitlement logic in infra
// fix: entitlement checks in the application; the handler renders the result

// 6. Swallowing to "protect" the client
catch { res.status(200).json({ data: [] }); }                 // ❌ failure disguised as empty success
// fix: propagate; the safety net answers 500 with a correlation ID
```

Forms 3–6 are the most dangerous because they **change failure into success** — the book's
cardinal sin (Chapters 2 and 13).

## The audit: finding hidden decisions today

```bash
# In your global handler/filter/middleware files, look for these tells:
grep -nE "retry|refund|compensat|tenant\.plan|feature|fallback|ok:\s*true" src/http/errors.ts
```

Every hit is a candidate to move down a layer. For each, ask: *does this branch need information
the handler does not have?* If yes, move it. If it is a pure code→status map, it may stay.

## Key data / numbers

- RFC 9457's own fields are the proof of the split: `status`, `title`, `type`, `detail`,
  `instance` are **mechanical**; nothing in the RFC asks the handler to decide outcomes.
- Safe global fallback for unknown errors: **`500`**, a correlation/request ID, and a generic
  title — no stack, no SQL, no vendor object (recommendation, and a Chapter 34 requirement).
- The handler's honest vocabulary is exactly your **registry's** codes (Chapter 8): if a code
  needs business context to map, the mapping is not the handler's job.
- Latency tell: if the global handler file imports `stripe`, `pg`, or a domain service, it has
  crossed the line (import-boundary lint makes this a CI failure).

## Real-world use case — Acme SaaS `WebhookIngest`

Acme's global handler contained this gem:

```ts
// hidden policy: "treat webhook processing errors as acknowledged"
if (err.scope === "webhook") { res.status(200).json({ received: true }); }
```

Intent was nice: don't make Stripe retry storms. Effect: a Postgres outage during
`invoice.paid` processing returned `200`, Stripe marked the event delivered, and **Acme's
billing state silently diverged from Stripe for 6 hours** — 214 customers got wrong invoice
statuses. The fix moved the decision where the context lived: the webhook *application service*
decided per error class — signature failure → `400` (terminal for Stripe), transient storage
error → `500` (Stripe retries), business conflict → `200` + recorded skip. The handler went back
to mechanical rendering only, and missed invoices became impossible to hide.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Mechanical-only global handler (recommended) | Honest, testable, boring | Requires local decision points to exist | Default |
| Feature-aware global handler | Fewer lines at call sites | Blind guesses; incident generator | Never |
| No global handler at all | No center to misuse | Every route hand-rolls serialization | Never beyond toys |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map registered codes → status in the center | Match on `err.message` text |
| Decide retry/compensate at the owning layer | Retry in the global handler |
| Let optional features degrade at their boundary | Centralize "friendly defaults" that hide failure |
| Answer unknown errors with `500` + request ID | Convert unknown errors into `200` |

## Common mistakes

- **Business logic hidden in status maps** — `DUPLICATE_KEY: 409` is mechanical; special-casing
  one tenant's duplicate as `200` is business policy.
- **The helper that grew** — `toProblem()` accumulates an `if` per incident; give new branches
  a home in the registry (Chapter 8) instead.
- **Testing only the happy path of the handler** — add a test that every registry code renders,
  and that no handler path returns `2xx` for a thrown error.

## Checklist

- [ ] The global handler imports no domain service, vendor SDK, or database client.
- [ ] No `retry`/`refund`/`compensate`/`fallback` strings appear in central files (grep audit).
- [ ] Optional-feature degradation happens at the feature's boundary.
- [ ] Unknown errors always become `500` + correlation ID, never `200`.

## Related

- [Centralized and Local Handling](./01-centralized-vs-local-handling.md)
- [Avoiding Tight Coupling and the Giant Error Module](../02-deep-dive/01-avoiding-coupling-and-the-giant-module.md)
- [A Global Handler and Local Recovery, Together](../03-practical-examples/01-global-handler-and-local-recovery.md)
- [Chapter 13 — Catch Blocks and Recovery Logic](../../../part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)
