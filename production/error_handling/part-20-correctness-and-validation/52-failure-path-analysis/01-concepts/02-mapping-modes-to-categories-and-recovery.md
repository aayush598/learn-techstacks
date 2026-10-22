# Mapping Modes to Categories and Recovery Policies (52.3–52.4)

> Part XX · Chapter 52 · Sections 52.3–52.4 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 4 — Designing a Comprehensive Error Taxonomy](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)

## In one sentence

The analysis becomes actionable at exactly two mapping steps: **mode → category** (what kind of
failure this is) and **category → recovery** (what the system should do about it) — and both
mappings must be total.

## Why this matters in production

A failure-mode matrix without mappings is a list of fears. A matrix with mappings is a policy
specification you can implement, test, and audit.

The failure mode of most teams is not that they lack error handling. It is that their handling is
**ad hoc per call site**, so the same category of failure is retried in one place, swallowed in
another, and turned into a 500 in a third. The mappings are what stop that.

## Core concept

### Mapping 1 — mode → category

Every mode gets a category from your taxonomy, plus the axes that determine policy:

| Axis | Values | Why it decides policy |
| ---- | ------ | ---------------------- |
| **Category** | validation, business, conflict, external_api, database, transient, ambiguous, internal, security, resource, cancellation | The routing key |
| **Transient?** | yes / no | Retry eligibility (51.3, 51.6) |
| **Effect happened?** | yes / no / unknown | Whether a retry is safe (51.9, 51.16) |
| **Compensation needed?** | yes / no | Saga step (Chapter 39) |
| **User-visible?** | yes / no | Whether a 4xx or 5xx, whether to alert |
| **Owner** | team | Who is paged |

Two rules make this mapping reliable:

1. **A mode that maps to two categories is usually a timing artefact.** The same mode can be
   `transient` before a commit and `ambiguous` after it. Split the row by phase rather than
   choosing one arbitrarily.
2. **A mode you cannot classify is a finding, not a shrug.** "Unknown" is a valid *category* for
   the error-handling default branch, but it must be a deliberate, reviewed row — not a place where
   the analysis stopped.

```text
   FP-04 chargeStripe — the SAME failure mode, two phases:

   before the request is sent   → transient        → retry
   after the request was sent   → ambiguous        → read-back, never blind retry
```

### Mapping 2 — category → recovery policy

The recovery policy answers: what does the system do, who owns it, and what does the user see?

| Recovery | Meaning | Typical categories |
| -------- | ------- | ------------------ |
| **retry** | Try again, bounded | transient network, deadlock, serialization failure, 503 |
| **compensate** | Undo what happened | partial multi-step failure, over-charge |
| **degrade** | Continue with reduced function | optional dependency down, unknown outcome |
| **fail** | Stop and report the failure | validation, business rule, permission |
| **terminate** | Stop the whole process/worker | corrupted state, invariant violation |
| **resolve later** | Reconcile asynchronously | ambiguous outcome, duplicate delivery |

Every row needs **six fields**, or it is not a policy:

```yaml
- category: external_api_transient
  recovery: retry
  max_attempts: 3
  total_deadline_ms: 8000
  backoff: exponential_full_jitter
  idempotent_required: true
  user_sees: 503 PAYMENT_PROVIDER_UNAVAILABLE
  alerts: true
  owner: payments
```

### Totality

Both mappings must be **total**: every mode maps to a category, and every category maps to a
policy. The way to prove it is to make the tables executable.

```ts
// The mapping is code, so a missing row is a crash at startup, not a silent gap.
const RECOVERY_BY_CATEGORY: Record<Category, RecoveryPolicy> = {
  validation:            { recovery: "fail",       httpStatus: 422 },
  business:              { recovery: "fail",       httpStatus: 409 },
  conflict:              { recovery: "fail",       httpStatus: 409 },
  external_api_transient:{ recovery: "retry",      httpStatus: 503, maxAttempts: 3 },
  external_api_ambiguous:{ recovery: "resolve later", httpStatus: 202 },
  database_transient:    { recovery: "retry",      httpStatus: 503, maxAttempts: 3 },
  data_integrity:        { recovery: "terminate",  httpStatus: 500 },
  resource_exhausted:    { recovery: "degrade",    httpStatus: 503 },
  cancellation:          { recovery: "fail",       httpStatus: 499 },
  internal:              { recovery: "fail",       httpStatus: 500 },
};

export function policyFor(category: Category): RecoveryPolicy {
  const p = RECOVERY_BY_CATEGORY[category];
  if (!p) throw new Error(`no recovery policy for category: ${category}`);   // totality check
  return p;
}
```

## How it works (mechanics)

### The full matrix

```text
 id    point        mode                category                 recovery       owner
 ────  ──────────  ──────────────────  ───────────────────────  ─────────────  ──────────
 FP-01 auth         token invalid       auth                     fail (401)     identity
 FP-01 auth         idp unreachable     dependency_unavailable  retry (1)      identity
 FP-02 validate     field invalid       validation               fail (422)     api
 FP-03 insert       db down             database_transient      retry (3)      platform
 FP-03 insert       unique violation    conflict                 fail (409)     platform
 FP-04 charge       provider 4xx        external_api_permanent   fail (402)     payments
 FP-04 charge       provider 5xx        external_api_transient   retry (3)      payments
 FP-04 charge       timeout, pre-send   external_api_transient   retry (3)      payments
 FP-04 charge       timeout, post-send  external_api_ambiguous   resolve later  payments
 FP-04 charge       invalid 200 body    external_api_invalid     fail (502)     payments
 FP-05 subscribe    db down             database_transient      retry (3)      platform
 FP-05 subscribe    invariant broken    data_integrity           terminate      platform
 FP-08 publish      broker down         dependency_unavailable  retry (3)      platform
 FP-08 publish      unknown type        event_unknown            degrade (202)  platform
 FP-09 email        provider 5xx        external_api_transient   retry (2)      platform
 FP-10 respond      serialisation fails internal                 fail (500)     api
```

Twelve rows, each with a policy. **The empty rows are the deliverable** — see 52.5.

### The policy must respect preconditions

A recovery policy is only correct if its preconditions hold in the situation where it fires.

| Recovery | Precondition | If it fails |
| -------- | ------------ | ----------- |
| retry | idempotent · transient · deadline available | stop, record the reason (51.16) |
| compensate | the effect definitely happened | stop — do not compensate a non-effect |
| degrade | a defined fallback exists and is *different* | fail |
| resolve later | a read-back or reconciliation path exists | escalate to manual review |
| terminate | the state is unrecoverable | escalate to manual review |

### Alerting is a policy decision, not a side effect

Two questions decide whether a category pages someone:

1. Is the failure **recoverable without a human**? If yes, it is a metric, not a page.
2. Is the failure **silent or wrong** (money moved, data lost)? If yes, it pages regardless of
   frequency.

```text
   external_api_transient  → retryable, self-healing  → dashboard, no page
   external_api_ambiguous  → may need a human later    → page if unresolved > 1 h
   data_integrity          → wrong state              → page immediately
   validation              → user-caused              → no page, ever
```

## Worked example — mapping `Checkout`'s modes

| Mode | Category | Recovery | Note |
| ---- | -------- | -------- | ---- |
| Auth token invalid | `auth` | fail 401 | Terminal, user re-authenticates |
| Stripe card declined | `business` | fail 402 | Terminal, no retry, no page |
| Stripe 500 | `external_api_transient` | retry ×3 | Bounded by the 8 s deadline |
| Stripe timeout **before** send | `external_api_transient` | retry ×3 | Safe: no effect occurred |
| Stripe timeout **after** send | `external_api_ambiguous` | resolve later | **Never blind-retry**: read back by idempotency key |
| Stripe returns 200 with empty body | `external_api_invalid` | fail 502 | Do not create a $0 subscription |
| Postgres down | `database_transient` | retry ×3 | Same transaction, so no partial state |
| Unique violation on `checkout_attempts` | `conflict` | fail 409 / replay | Duplicate request: replay the original outcome |
| Queue broker down | `dependency_unavailable` | retry ×3 | Event stays in the outbox |
| Client disconnected | `cancellation` | record `cancelled` | 499; never report success |
| Unknown | `internal` | fail 500 + alert | Never a 200 |

The row that took longest to get right was **"Stripe timeout after send"**. Naively it is the same
as "Stripe timeout before send", and treating them the same caused the duplicate-charge bug
(51.9). The distinguishing question is always: *did the effect happen?* If you cannot answer it,
the category is `ambiguous` and the recovery is `resolve later`.

## Key data / numbers

- **Policy fields per row: 6 minimum** (recovery, bound, precondition, user-visible result, alert,
  owner). Fewer means the policy is implicit.
- **Matrix rows for a typical flow: 15–30** after pruning (from 100+ raw cells).
- **Coverage target: 100%** of money-moving rows, **≥ 90%** overall for a mature service.
- **Retry bounds**: attempts **3**, total deadline **8 s**, backoff **exponential with full jitter**,
  base **250 ms**.
- **Resolve-later SLA**: ambiguous outcomes must be resolved within **1 hour**; unresolved ones
  escalate.
- **Alert threshold**: page on `data_integrity` and `external_api_ambiguous` immediately;
  `external_api_transient` only if the error rate exceeds **5%** for **5 minutes**.

## Real-world use case — Acme SaaS `WebhookIngest`

Acme's webhook handler had three catch blocks and no policy table. The mapping exercise produced
this table, and it immediately revealed two holes:

```yaml
- category: webhook_signature_invalid   recovery: fail (401)     alert: true   # security event
- category: webhook_payload_invalid     recovery: fail (400)     alert: false  # sender bug
- category: webhook_unknown_type        recovery: degrade (202)  alert: false  # ack + record
- category: webhook_duplicate           recovery: degrade (202)  alert: false  # success, record
- category: external_api_transient      recovery: retry (3)      alert: true
- category: external_api_ambiguous      recovery: resolve later alert: true   # ← was missing
```

The missing row was `external_api_ambiguous`: when Acme called Stripe to fetch the full event
after a signature mismatch, that call could time out, and the handler had **no policy at all** for
it — the error escaped to the global handler and returned `500`, so Stripe redelivered the event
for three days.

The policy table also fixed a subtle bug: `webhook_unknown_type` previously fell into the same
catch as `webhook_signature_invalid` and returned `400`. Stripe treats `4xx` as permanent, so the
event was dropped forever. Splitting the categories made the unknown type a `202` with a record —
Acme could process it later from its own inbox.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One global policy table | Total, reviewable, one place | Coarse for wide systems | Most systems |
| Per-dependency policy tables | Finer control of external effects | More tables to keep in sync | Systems with many critical dependencies |
| Policy decided at each call site | Flexible | Inconsistent; unfalsifiable | Never |
| Policy as code (table + types) | Exhaustiveness checkable | Slightly more ceremony | Mature systems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Split a mode by phase when the category changes | Pick one category for "timeout" and move on |
| Give every policy a bound, a precondition, an owner, and a user-visible result | Write "retry" with no limit |
| Make the category→policy table total and executable | Leave categories without a row "for now" |
| Treat "I cannot classify this" as a finding | Label it "unknown" and move on |
| Decide alerting in the policy, not in the logger | Page on every 5xx |

## Common mistakes

- **One row per vendor error.** "Stripe error 402" is an instance, not a category. Categories are
  about behaviour: retry, fail, compensate.
- **Retrying the ambiguous category.** Retrying an unknown-outcome payment is how duplicate charges
  happen.
- **A policy without a user-visible result.** If nobody can say what the customer sees, the
  behaviour is whatever the framework does.
- **Policy tables that drift from the code.** The same enforcement trick as Chapter 51: make the
  table the single source, and assert totality at startup.

## Checklist

- [ ] Every mode in the matrix has a category.
- [ ] Every category has exactly one policy row, and the table is total.
- [ ] Each policy states its bound (attempts, deadline) or states that it has none.
- [ ] Each policy states the precondition under which it may run.
- [ ] Each policy states the user-visible result.
- [ ] Each policy states the owner and whether it alerts.
- [ ] Ambiguous outcomes have a `resolve later` policy with an SLA.

## Related

- [Enumerating Failure Points and Failure Modes (52.1–52.2)](./01-enumerating-failure-points-and-modes.md)
- [Unhandled, Nested, and Multi-Step Paths (52.5–52.8)](./03-unhandled-nested-and-multi-step-paths.md)
- [Chapter 4 — Designing a Comprehensive Error Taxonomy](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
