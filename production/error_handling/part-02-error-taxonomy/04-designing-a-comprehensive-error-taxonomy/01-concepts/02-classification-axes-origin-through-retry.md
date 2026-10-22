# Classification Axes: Origin through Retry Eligibility

> Part II · Chapter 4 · Sections 4.3–4.9 · _Estimated reading time: 28 min_
> **Prerequisite:** [Why Every Codebase Needs a Taxonomy](./01-why-a-taxonomy.md)

## In one sentence

The first seven classification axes — **origin, severity, recoverability, permanence, affected
component, user impact, and retry eligibility** — answer *who caused it, how bad it is, and what
we may do about it*.

## Why this matters in production

These axes drive the two most consequential decisions in error handling: **do we retry?** and **do
we alert a human?** Get them wrong and you either retry permanent failures (amplifying outages) or
fail to retry transient ones (needless user-visible errors), or you page on-call for a declined
card while sleeping through a data-corruption event.

## Core concept — the seven axes

| Axis | Question | Typical values | Drives |
| ---- | -------- | -------------- | ------ |
| **Origin** | Where did it originate? | client, app, datastore, dependency, runtime | Ownership, fix location |
| **Severity** | How bad is it? | info, warning, error, critical, fatal | Alerting, log level |
| **Recoverability** | Can we continue safely? | recoverable, unrecoverable | Recover vs terminate |
| **Permanence** | Will retry help? | transient, permanent | Retry policy |
| **Affected component** | What broke? | API, worker, DB, cache, queue, provider | Blast radius, routing |
| **User impact** | Who is affected and how? | none, degraded, blocked, data loss | Priority, messaging, SLA |
| **Retry eligibility** | May this be retried? | yes, no, conditional | Retry engine |

## 4.3 By origin

Origin names **where the defect lives**, which determines who fixes it:

```text
client      → bad input, bad credentials        (caller fixes)
application → our bug or our business rule      (we fix)
datastore   → DB/cache/storage failure          (infra or query fix)
dependency  → third-party / network failure     (wait, adapt, degrade)
runtime     → process, memory, config, startup  (ops/platform fix)
```

Origin is *not* the same as HTTP status. A `401` may originate from the client (bad token) or
from the application (misconfigured signing key). Classify origin by the **actual cause**, not the
response code.

```ts
// Origin = dependency (not "our bug"): the provider's gateway timed out.
// Origin = runtime (not "dependency"): our outbound proxy env var is unset.
```

## 4.4 By severity

Severity is a property of the **event**, not the category. The same category can be `warning` in
one context and `critical` in another.

| Severity | Meaning | Example |
| -------- | ------- | ------- |
| `info` | Expected, no action | `404` on an optional resource |
| `warning` | Expected but noteworthy | `429` from a throttled provider |
| `error` | Unexpected, impact possible | `500` from an unhandled exception |
| `critical` | User/data impact now | failed commit, corrupted export |
| `fatal` | Process cannot continue | out-of-memory, bootstrap failure |

> ⚠️ **Hazard.** Severity inflation destroys its value. If every `4xx` logs at `error`, real
> errors drown. Business failures should be `info`/`warning`, technical failures `error`+.

## 4.5 By recoverability

**Recoverable** means you can continue or retry **without violating an invariant**. **Unrecoverable**
means continuing risks corruption; you must abort, roll back, or terminate.

```text
Cache read fails        → recoverable (fall through to DB)
DB write fails mid-tx    → recoverable (rollback, retry once)
Integrity check fails    → unrecoverable (do NOT "fix and continue")
```

Recoverability is about **safety**, not optimism. It is the axis that decides fail-fast vs
degrade (Chapter 30).

## 4.6 By permanence

**Transient** failures succeed on retry (deadlock, `503`, connection reset). **Permanent** failures
never do (validation, `404`, `401`, schema mismatch). This is the *only* legitimate basis for a
retry decision (Chapter 27).

| Signal | Permanence |
| ------ | ---------- |
| `429`, `503`, `504`, `ECONNRESET`, `40001`, `40P01` | transient |
| `400`, `401`, `403`, `404`, `409` (version), `422`, `23505` | permanent |
| Provider 5xx | *usually* transient — but verify against provider docs |

## 4.7 By affected component

Naming the component bounds the **blast radius** and routes the alert to the right team:

```text
API edge | auth service | billing worker | Postgres primary | Redis | S3 | queue | Stripe adapter
```

Component + failure domain (Chapter 1) tell you whether to isolate, shed load, or fail over.

## 4.8 By user impact

Impact answers "how does the user experience this?"

| Impact | Meaning | Example |
| ------ | ------- | ------- |
| **none** | Internal only | background cache refresh missed |
| **degraded** | Feature reduced | summaries unavailable, page works |
| **blocked** | User cannot proceed | checkout fails, 500 on submit |
| **data loss** | User's work lost or wrong | export missing rows, charge doubled |

Impact drives priority and the *urgency* of a page — not the same as severity (an internal
corruption can be high severity with zero current user impact).

## 4.9 By retry eligibility

Retry eligibility is the **derived** decision that combines permanence, idempotency, and
resources:

```text
retry if:  permanent = false  AND  operation is idempotent (or has a key)  AND budget remains
```

Conditional example: a write to Stripe is retryable **only with an idempotency key**. Without the
key, retry eligibility is `no` even though the failure is transient — because a duplicate charge is
worse than a failed request (Chapter 28).

## Worked example — same endpoint, three axes

Acme's `POST /exports` can fail three ways. Classification drives opposite behavior:

| Failure | Origin | Severity | Permanence | Impact | Retry |
| ------- | ------ | -------- | ---------- | ------ | ----- |
| date range inverted | client | info | permanent | blocked(4xx) | no |
| queue publish `503` | dependency | error | transient | blocked | yes (bounded) |
| tenant over export quota | application | warning | permanent | blocked | no |

## Key data / numbers

- PostgreSQL `40001` `serialization_failure` and `40P01` `deadlock_detected` are **transient**;
  `23505` `unique_violation` and `23503` `foreign_key_violation` are **permanent**.
- HTTP `429` and `503` normally carry `Retry-After`; treat its presence as a retry-eligible hint.
- gRPC `UNAVAILABLE (14)` and `DEADLINE_EXCEEDED (4)` are transient; `INVALID_ARGUMENT (3)` and
  `NOT_FOUND (5)` are permanent.

## Real-world use case — WebhookIngest

A Stripe webhook signature fails to verify. Origin = **client** (bad/missing header or a
misconfigured secret). Permanence = **permanent**. Severity = `warning` unless the rate spikes
(then it is a config incident). Impact = **none for the user** (the event is simply rejected).
Policy: return `400`, never retry, never process. Contrast with a DSS verification service
timeout: origin = **dependency**, permanence = **transient**, retry = **yes with backoff**.

## Trade-offs

| If you classify by… | You risk… | Prefer… |
| ------------------- | --------- | ------- |
| HTTP status | Wrong origin (a vendor's fake `400`) | Actual cause |
| Message text | Brittle matching | Category + code |
| Endpoint | Conflating independent failures | Category per call |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify origin by real cause | Infer origin from status code |
| Set severity per event context | Log every `4xx` at `error` |
| Gate retries on permanence + idempotency | Retry anything that "failed once" |
| Name the component for routing | Alert a generic channel |

## Common mistakes

- **Treating `401` as always client-caused** — it can be our key rotation bug.
- **Retrying non-idempotent writes** because the failure looked transient.
- **Skipping the user-impact axis** — leading to over- or under-prioritized incidents.
- **Deriving retry eligibility twice, differently** in two layers.

## Checklist

- [ ] Can you fill all seven axes for your top 10 failures?
- [ ] Is severity contextual, not hard-coded per category?
- [ ] Does retry eligibility check idempotency?
- [ ] Does the component axis route alerts to owners?

## Related

- [Classification Axes: HTTP → Compensation](./03-classification-axes-http-through-compensation.md)
- [Classification Axes: origin, severity, permanence](../05-reference/README.md)
- [Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
