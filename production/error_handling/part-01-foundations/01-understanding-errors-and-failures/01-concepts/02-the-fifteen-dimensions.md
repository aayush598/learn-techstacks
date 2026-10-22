# The Classification Dimensions of Failure

> Part I · Chapter 1 · Sections 1.4–1.15 · _Estimated reading time: 25 min_

## In one sentence

Every failure can be classified along twelve mostly-independent axes, and **the combination of
those axes — not the error message — determines what you should do about it.**

The twelve axes are the *output* of classification and the *input* to policy (retry, validate,
degrade, alert, disclose). Master them and most "what should this code do?" debates resolve
themselves.

## The twelve dimensions at a glance

| # | Dimension | Question it answers | Drives |
| - | --------- | ------------------- | ------ |
| 1 | Expected / Unexpected | Did we anticipate this? | Error model vs generic handler |
| 2 | Recoverable / Unrecoverable | Can we continue safely? | Recovery vs termination |
| 3 | Transient / Permanent | Will retry help? | Retry policy |
| 4 | Deterministic / Nondeterministic | Same input → same result? | Reproducibility, testing |
| 5 | Synchronous / Asynchronous | When does it surface? | Propagation, unhandled rejections |
| 6 | Local / Remote | Did our process fail or someone else's? | Timeouts, circuit breakers |
| 7 | Operational / Programming | Config/infra vs bug? | Who fixes it, how |
| 8 | Business / Technical | A rule vs a malfunction? | User messaging, status codes |
| 9 | User-caused / System-caused | Who triggered it? | Blame, UX, quotas |
| 10 | Partial / Complete | Did some work succeed? | Compensation, idempotency |
| 11 | Fail-fast / Fail-safe | On failure, stop or protect? | Control-flow choice |
| 12 | Propagate / Contain | Let it travel or trap it? | Boundary design |

The axes are **mostly independent**: a failure is a *point* in 12-dimensional space, not a member
of one bucket. A timeout is asynchronous + remote + transient + often nondeterministic + partial.

---

## 1. Expected vs unexpected

**Expected** errors are part of the contract: invalid input, not-found, insufficient funds. You
model them explicitly, name them, and map them to stable outcomes.

**Unexpected** errors are surprises: a null dereference, a disk full, a provider returning HTML
instead of JSON. You catch them with a safe fallback and treat them as defects.

```ts
// Expected: modeled, typed, no stack trace needed.
if (!user) throw new NotFoundError("USER_NOT_FOUND");

// Unexpected: let it bubble to the boundary; record it as a defect.
const data = JSON.parse(providerBody); // may throw SyntaxError
```

| | Expected | Unexpected |
| --- | --- | --- |
| Modeled as | Typed error / `Result` | Generic catch + fallback |
| Log level | `warn`/`info` | `error` (defect) |
| User message | Specific, actionable | Generic "something went wrong" |

> ⚠️ **Hazard.** Never route an unexpected error through a user-facing message derived from its
> text — it may leak internals or confuse the user.

## 2. Recoverable vs unrecoverable

**Recoverable** means the operation can continue or be retried *without violating invariants*.
**Unrecoverable** means continuing risks corruption; you must abort, roll back, or terminate.

Recoverability is about **safety**, not optimism. A failed cache read is recoverable (go to DB).
A failed integrity check after a partial write is not.

## 3. Transient vs permanent

**Transient** failures succeed if you try again after a delay: deadlock, connection reset, 503,
rate limit. **Permanent** failures never succeed: 400, 404, 401, schema mismatch.

This distinction is the *only* legitimate basis for a retry decision (Chapter 27).

```text
Transient  → retry with backoff + jitter, bounded attempts
Permanent  → do not retry; translate and return
```

## 4. Deterministic vs nondeterministic

A **deterministic** failure recurs for the same input and is reproducible (a badge number off by
one). A **nondeterministic** failure depends on timing, load, or external state (a race, a flaky
network).

Deterministic failures are debuggable and should be fixed; nondeterministic failures need
isolation, timeouts, and idempotency because you cannot always reproduce them.

## 5. Synchronous vs asynchronous

**Synchronous** errors surface on the current call stack; you can `try/catch` them locally.
**Asynchronous** errors surface later — in a promise rejection, a callback, a timer, a message
handler — and may become *detached* if unobserved.

```ts
// Detached async failure: nothing awaits this, so it becomes unhandled.
queue.publish(job); // if publish returns a rejected promise, who sees it?
```

Asynchronous failures are where "node crashed at 3am" stories come from (Chapters 31, 41).

## 6. Local vs remote

A **local** failure is in-process: a bug, a missing file, exhausted memory. A **remote** failure
crosses the network to another process you do not control: a third-party API, a replica, another
microservice.

Remote failures add the hardest problem in distributed systems — **ambiguous outcomes** (the
request may or may not have taken effect). They demand timeouts, idempotency, and circuit
breakers (Chapters 25–29, 39).

## 7. Operational vs programming

**Operational** errors come from the environment and configuration: a wrong env var, a disk full,
a DNS blip, a quota exceeded. **Programming** errors are defects in the code: bugs, wrong
assumptions, unhandled states.

| | Operational | Programming |
| --- | --- | --- |
| Fixed by | Ops/config change | Code change + test |
| Should page a human? | Sometimes (sustained) | Yes (a bug on the path) |
| Retry? | Often | Never (it will recur) |

## 8. Business vs technical

A **business** error is a legitimate outcome of the domain: card declined, seat already taken,
quota exceeded, trial expired. A **technical** error is a malfunction: DB down, malformed response.

Business errors are **not bugs** and should *not* alert on-call engineers. They are normal,
expected, and often high-volume (Chapter 57 covers validating high-volume business errors).

## 9. User-caused vs system-caused

**User-caused**: bad input, invalid password, forbidden action. **System-caused**: our bug, our
outage.

The origin affects **how you communicate** and **who pays**. User-caused errors are actionable and
specific; system-caused errors are apologetic and generic, and may entitle the user to a credit.

## 10. Partial vs complete

**Complete** failure: nothing happened, no state changed. **Partial** failure: some steps/items
succeeded, others did not — the hardest category because it requires compensation or resume logic.

```text
Charge succeeded → Provision failed → Email sent means... what state are we in?
```

Partial failures are the subject of Chapter 39; ignoring them is how systems get "orphaned
subscriptions" and "double charges."

## 11. Fail-fast vs fail-safe

**Fail-fast**: abort at the first sign of trouble, loudly. Good for developer errors and
corruption prevention.
**Fail-safe**: keep running in a safe mode, protecting users and data. Good for optional features.

These are **design choices**, not universal goods. A payment write should fail-fast; a
recommendations widget should fail-safe (show nothing rather than crash the page).

## 12. Propagate vs contain

**Propagation** lets an error travel up to a handler that can act. **Containment** traps it
locally and substitutes a safe outcome.

Both are correct in different places: propagate to the boundary that owns the decision; contain
where the alternative would be worse than the failure. The skill is choosing the boundary
(Chapter 15).

---

## Putting it together — classify, then decide

```text
Failure: Stripe API returns 429 on charge attempt.
Expected?    Yes (documented)
Business?    No — technical
Transient?   Yes
Remote?      Yes
Partial?     No (charge not attempted)
Decision:    retry with backoff, respect Retry-After, bounded; if exhausted, return a
             retryable error to the caller; do NOT create a second charge (idempotency).
```

```text
Failure: card_declined on charge attempt.
Expected?    Yes
Business?    Yes
Transient?   No
Decision:    no retry; return CARD_DECLINED; do not alert; surface actionable UI message.
```

Same endpoint, opposite policies — because the *classification* differs.

## Real-world use case — WebhookIngest

An inbound Stripe webhook fails because the signature header is missing. Classification:
expected, permanent, synchronous, local (within our verify code), technical, system-caused
(misconfiguration), complete, contain-and-reject. Policy: return `400`, log at `warn`, never
retry, never process. Contrast with a signature *verification service* timing out: remote,
transient → retry with backoff.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify before choosing a policy | Retry because "it failed once" |
| Keep axes independent | Assume 4xx ⇒ business error always (401 may be config) |
| Record the classification on the error | Re-derive it differently in every handler |

## Common mistakes

- **Conflating business and technical** — alerting on declined cards.
- **Retrying permanent errors** — infinite loops on 400s.
- **Ignoring partial failure** — treating a multi-step op as atomic when it is not.
- **Assuming a 4xx cannot be a bug** — a 500 returned with status 400 is common from vendors.

## Checklist

- [ ] For your top 10 failure modes, can you fill in all twelve axes?
- [ ] Does your retry policy consult the transient/permanent axis only?
- [ ] Are business errors excluded from on-call alerts?
- [ ] Are partial-failure outcomes represented explicitly?

## Related

- [Error, Fault, Failure, and Exception](./01-error-fault-failure-exception.md)
- [Failure Domains and Fault Boundaries](../02-deep-dive/01-failure-domains-and-fault-boundaries.md)
- [Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
