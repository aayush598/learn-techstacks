# Unhandled Paths, Nested Operations, Workflows, and Dependency Boundaries (52.5–52.8)

> Part XX · Chapter 52 · Sections 52.5–52.8 · _Estimated reading time: 24 min_
> **Prerequisite:** [Mapping Modes to Categories and Recovery (52.3–52.4)](./02-mapping-modes-to-categories-and-recovery.md)

## In one sentence

Four passes make the failure matrix trustworthy: find the **unhandled cells** (52.5), give nested
operations a single owner (52.6), model multi-step workflows as state machines (52.7), and write an
explicit policy for every **dependency boundary** (52.8).

## Why this matters in production

A matrix built from a single code path has four systematic blind spots. Each is a place where
teams consistently underestimate their exposure:

- **Unhandled cells** — the mode you never wrote a policy for. The gap is silent until the day it
  is used.
- **Nested operations** — an inner call that fails while the outer call is also handling a
  failure. Two retry layers, two compensators, one corrupted state.
- **Multi-step workflows** — the failure between steps 3 and 4, where the process restarts with
  no memory of what it did.
- **Dependency boundaries** — the behaviour when a dependency is *slow* rather than *down*, and
  when it returns *wrong* rather than *failed*.

## Core concept

### 52.5 — Unhandled paths

An **unhandled path** is a failure mode that has no policy, or a policy whose outcome is undefined.
Three shapes:

| Shape | Example | How to detect |
| ----- | ------- | ------------- |
| **Empty cell** | Mode `provider returns 200 with empty body` has no row | Matrix coverage check |
| **Undefined outcome** | Policy says "retry" but nothing says what happens after the attempts are exhausted | Policy completeness review |
| **Orphan point** | A failure point that is not in the matrix at all | Diff of point list vs matrix rows |

Detection techniques, in increasing order of reliability:

1. **Coverage arithmetic** — `mapped modes ÷ enumerated modes`. A single number to track.
2. **Static check** — every `catch` block's error type appears in at least one policy row.
3. **Runtime check** — an error occurred that no policy handled (the `default` branch fired more
   than expected).
4. **Test check** — every registered error code is produced by at least one test, and every policy
   row has an asserted outcome.

```ts
// Runtime detection: count how often the default branch handles something.
// A non-zero count is a defect report, not a metric.
if (cls.code === "UNCLASSIFIED") {
  metrics.increment("error.unclassified", { operation: ctx.operation });
  // and: 51.4 — attach the raw cause so it can be classified later.
}
```

> ⚠️ **Hazard.** A `default` branch that handles everything is what makes a matrix look complete
> while it is empty. Measure how often it fires. If it fires, the matrix has a hole.

### 52.6 — Nested operations

When operation B is called from operation A, a failure in B can be handled by **A, B, or both**.
Every combination is a bug source:

| Pattern | What happens | Rule |
| ------- | ------------ | ---- |
| A retries, B retries | 3 × 3 = 9 attempts | One owner only |
| A compensates, B compensates | Double compensation | Compensation owned by the outermost effect owner |
| B swallows, A sees success | Silent discard | B must propagate unless it fully recovered |
| B translates, A re-translates | Double-wrapped, lossy | Translate once, at the boundary |
| B throws a *different* error type | A's catch misses it | A's catch must cover B's error surface |

The rule of thumb: **exactly one layer owns the failure**. Ownership is decided by the effect, not
by the call stack — the layer that performed the side effect owns the recovery for it.

```text
   API layer          Application layer        Repository layer
   ─────────          ─────────────────        ─────────────────
   owns: response     owns: business outcome   owns: DB effect
   retries: NO        retries: NO              retries: YES (transient only)
   compensates: NO    compensates: NO          compensates: NO
   translates: YES    translates: NO           translates: YES (db → app)
```

### 52.7 — Multi-step workflows

A workflow is a sequence of steps with **commit boundaries** between them. The analysis adds three
questions per step:

1. What is the step's effect (local or external)?
2. Is it reversible, and how (the compensation)?
3. Can a later process detect whether it ran (the observability that makes resume safe)?

```text
   step        effect    commit boundary   reversible?   detectable?
   ──────────  ────────  ────────────────  ───────────   ───────────
   1 reserve    local     yes               yes (release) yes (status column)
   2 charge     EXTERNAL  no                yes (refund)  yes (provider idempotency key)
   3 activate   local     yes               yes (cancel)  yes (status column)
   4 notify     EXTERNAL  no                NO            partially (provider id)
```

Step 4 being irreversible is a **design input**: it runs last, after the workflow is durably
`COMMITTED`. The failure-path analysis must state where each step sits relative to the final
commit, because that determines whether a failure is "retryable" or "compensatable".

### 52.8 — Dependency boundaries

For each dependency, the analysis must answer five questions — and the fourth is the one people
skip:

| Question | Example (Stripe) |
| -------- | ---------------- |
| How can it fail? | 4xx, 5xx, timeout, hang, reset |
| How can it be **slow**? | 30 s response, partial response, connection held open |
| How can it be **wrong**? | `200` with an empty body, `200` with stale data, wrong tenant id |
| What is the *damage* of each? | Duplicate charge, `unknown` outcome, zero-amount subscription |
| What is the policy? | Timeout 8 s, 3 attempts, breaker, fail closed on ambiguity |

The damage column is what turns a dependency list into a risk analysis. "Stripe can be slow" is a
fact; "a slow Stripe turns a 30 s request into a 30 s *and* a duplicate charge, because the retry
starts after the caller gave up" is a finding.

## How it works (mechanics)

### Building the matrix for nested and workflow steps

Extend the matrix with columns that make ownership visible:

| id | point | mode | category | owner | recovery | notes |
| -- | ----- | ---- | -------- | ----- | -------- | ----- |
| FP-04.1 | chargeStripe (inner) | timeout | external_api_transient | payments | retry ×3 | inner must NOT retry if the outer retries |
| FP-05 | insertSubscription (outer) | db down | database_transient | platform | retry ×3 | outer is the retry owner |
| FP-07 | publishEvent | broker down | dependency_unavailable | platform | retry ×3 | outbox keeps it durable |

When two rows would retry the same operation, the matrix flags it:

```ts
// A matrix lint: no operation may have two retry owners.
const retryOwners = new Map<string, string>();
for (const row of matrix) {
  if (row.recovery !== "retry") continue;
  const prev = retryOwners.get(row.operation);
  if (prev && prev !== row.owner) {
    throw new Error(`two retry owners for ${row.operation}: ${prev} and ${row.owner}`);
  }
  retryOwners.set(row.operation, row.owner);
}
```

### Dependency policy record

```yaml
dependency: stripe
criticality: critical          # critical | important | optional
failure_modes:
  - http_4xx:      damage: none              policy: fail (map to business code)
  - http_5xx:      damage: none              policy: retry x3, budgeted
  - timeout_pre:   damage: none              policy: retry x3
  - timeout_post:  damage: POSSIBLE_CHARGE   policy: resolve later, never retry
  - invalid_200:   damage: WRONG_STATE       policy: fail (502), alert
  - slow_30s:      damage: caller timeout + duplicate risk
                    policy: timeout 8s, breaker, deadline propagation
fallback: fail_closed
degraded_mode: disable subscription upgrade UI; keep read-only billing
```

## Worked example — `ExportJob` nested inside a queue worker

`ExportJob` is a workflow whose steps are executed by a worker that itself is wrapped in a retry
and a DLQ handler. That is a nested operation with three owners.

```text
   DLQ handler        Worker loop           ExportJob steps
   ───────────        ───────────           ──────────────
   retry: yes         retry: yes (lease)    retry: per-step
   owner: queue       owner: worker         owner: steps
```

The original code had **three** retry layers. The fix:

- The **worker** owns the retry for the whole job (lease renewal + bounded attempts).
- The **steps** do not retry; they fail fast and let the job-level retry handle it, with the
  idempotency key preserved across attempts.
- The **DLQ handler** does not retry; it records and escalates (a message in the DLQ has already
  exhausted its attempts).

The damage before the fix: a transient S3 error caused 3 × 3 = 9 upload attempts, and because the
upload was not idempotent, the file was written **9 times** into a multipart upload, leaving
corrupt objects for customers.

## Key data / numbers

- **Target matrix coverage: 100%** of money-moving rows, **≥ 90%** overall.
- **Unclassified-error count must be 0** in normal operation; a non-zero weekly count is a
  maintenance trigger.
- **One retry owner per operation** — the matrix lint above enforces it mechanically.
- **Workflow steps per SaaS checkout: 4–7**; commit boundaries per step: 0–2.
- **Dependency policy fields: 6 minimum** (criticality, failure modes, damage, timeout, fallback,
  degraded mode).
- **Slow-dependency damage window**: with an 8 s dependency timeout and a 30 s caller deadline,
  a naive implementation can start **3–4 attempts** after the caller gave up — this is the
  duplicate-effect window.
- **Max matrix rows per operation: 40.** Beyond that, split the operation (e.g. separate
  "charge" from "activate").

## Real-world use case — Acme SaaS `Checkout`

The nested-operation pass found a bug that no amount of local testing would have. The `Checkout`
application service called the `BillingGateway`, which internally called the `StripeClient`, which
had its own retry (from the shared HTTP client library).

```text
   CheckoutService (retry x3 on transient)
     └── BillingGateway
           └── StripeClient (retry x3 from the HTTP library)
                 → 3 × 3 = 9 charge attempts, each with a NEW idempotency key
```

Because the idempotency key was generated *inside* `StripeClient` per attempt, each attempt was a
distinct charge. Acme's duplicate-charge rate was ~3/week, and the incident count had risen after
they upgraded the HTTP client library — a change that "only added retries".

The fix was a single ownership rule, written into the matrix: **the Stripe client library does not
retry charge calls**; the `BillingGateway` retries with a stable idempotency key derived from the
checkout attempt id. The analysis artifact was the matrix row:

```text
FP-04 chargeStripe | timeout_post | external_api_ambiguous | owner: payments | resolve later | never retry
```

That one row was worth more than the incident review that followed it.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Matrix per operation | Complete, reviewable, finite | Needs maintenance as code changes | Critical flows |
| Whole-service matrix | Looks comprehensive | Nobody maintains it; false confidence | Never as the primary artifact |
| Heuristic checklists only | Fast | Misses the specific | First pass on a new codebase |
| Automated coverage checks | Keeps the matrix honest | Only checks what you can express | Alongside a human-written matrix |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Measure coverage as a number and track it | Assume "we covered everything" |
| Give every operation exactly one retry owner | Let the library and the app both retry |
| Ask what damage a slow dependency causes | Only analyse dependencies that are "down" |
| Put irreversible steps last | Send the email before the payment settles |
| Treat the `default` branch firing as a defect | Let `default` handle everything quietly |
| Record damage, not just failure | Catalogue failures without consequences |

## Common mistakes

- **Nested retries with per-layer keys.** Nine attempts, nine keys, nine charges.
- **An analysis that stops at the process boundary.** The queue, the browser, and the CDN all
  have failure points too.
- **Ignoring the slow-dependency damage.** "Slow" is a failure mode with a longer blast radius than
  "down".
- **An irreversible step in the middle.** A receipt email before the payment settles cannot be
  unsent.

## Checklist

- [ ] Every enumerated mode has a policy row; coverage is measured, not assumed.
- [ ] Every operation has exactly one retry owner.
- [ ] Every compensation has exactly one owner.
- [ ] Every dependency has a policy covering fail, slow, and wrong-data cases.
- [ ] Every dependency policy states the damage, not only the action.
- [ ] Every workflow step states its effect, reversibility, and detectability.
- [ ] The `default` branch firing count is monitored and is 0 in normal operation.

## Related

- [FMEA, the Failure-Mode Inventory, and Risk Prioritization (52.13–52.15)](../02-deep-dive/01-fmea-and-risk-prioritization.md)
- [Failure-Path Analysis of the Checkout Flow](../03-practical-examples/01-checkout-failure-path-analysis.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [Chapter 25 — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
