# Failure-Path Analysis of the Checkout Flow

> Part XX · Chapter 52 · Sections 52.1–52.12 · _Estimated reading time: 28 min_
> **Prerequisite:** [Enumerating Failure Points and Failure Modes (52.1–52.2)](../01-concepts/01-enumerating-failure-points-and-modes.md)

## In one sentence

A complete failure-path analysis of one checkout flow produces **ten numbered failure points,
a total mode → category → recovery matrix, and a list of unhandled cells** — and that last list
is the deliverable.

## Why this matters in production

Checkout is the flow where three things are true at once: it **moves money**, it **writes several
rows that must agree with each other**, and it **calls a third party we do not control**. Any one
of those makes error handling hard; together they make it the difference between a good day and a
chargeback dispute.

The failure modes that hurt here are not the ones people picture. Nobody loses money because the
database was briefly down. People lose money because the charge **succeeded and the response was
lost**, so the customer pays twice; because a subscription row was written and the entitlement was
not, so the customer is billed for something they cannot use; and because the response **failed to
write**, so the client retried and the order was created twice.

## Core concept

### 52.1–52.2 — The failure points

```text
Checkout POST /orders
  FP-01 authenticate           decision       token verify, session load
  FP-02 validateBody           interpretation schema check, field rules
  FP-03 insertAttempt          effect         postgres insert (order_attempts)
  FP-04 chargeStripe           wait           external call, card charged
  FP-05 insertSubscription     effect         postgres insert
  FP-06 insertEntitlement      effect         postgres insert
  FP-07 insertOutboxEvent      effect         postgres insert
  FP-08 publishEvent           boundary       queue publish
  FP-09 sendReceiptEmail       effect         email provider
  FP-10 respond201             boundary       http response write
```

Ten points, in execution order. The dangerous ones are **FP-04** (money moves outside our
transaction) and **FP-05/FP-06** (two rows that must agree with each other).

### 52.3–52.4 — The matrix

Every row is one failure mode, its category, and the policy that answers it:

| Point | Mode | Category | Recovery | Status | Owner |
| ----- | ---- | -------- | -------- | ------ | ----- |
| FP-01 | token invalid | `auth` | fail | `401` | identity |
| FP-02 | body malformed / field invalid | `validation` | fail | `422` | api |
| FP-03 | database down | `database_transient` | retry (3) | `503` | platform |
| FP-03 | unique violation on retry | `conflict` | fail | `409` | platform |
| FP-04 | provider 4xx (card declined) | `external_api_permanent` | fail | `402` | payments |
| FP-04 | provider 5xx / timeout before send | `external_api_transient` | retry (3) | `503` | payments |
| FP-04 | **succeeded, response lost** | `external_api_ambiguous` | resolve later | `202` | payments |
| FP-04 | succeeded, invalid payload | `external_api_ambiguous` | resolve later | `202` | payments |
| FP-05 | **row written, commit failed** | `external_api_ambiguous` (local) | resolve later | `202` | platform |
| FP-06/07 | insert fails | `database_transient` | retry (3) | `503` | platform |
| FP-08 | broker unreachable | `dependency_unavailable` | retry (3) | `503` | platform |
| FP-08 | **published twice** | `ambiguous` | resolve later (consumer dedupes) | `200` | platform |
| FP-09 | email provider fails | `external_api_transient` | degrade (retry in background) | `201` | platform |
| FP-10 | response write fails | `boundary` | fail | `500` | api |

The **totality** check is the point of the table. Both mappings must be total, and the cheapest
way to keep them total is to make them code:

```ts
type Recovery = "fail" | "retry" | "compensate" | "degrade" | "terminate" | "resolve_later";

const POLICY: Record<string, { recovery: Recovery; httpStatus: number }> = {
  auth:                   { recovery: "fail",          httpStatus: 401 },
  validation:             { recovery: "fail",          httpStatus: 422 },
  conflict:               { recovery: "fail",          httpStatus: 409 },
  external_api_permanent: { recovery: "fail",          httpStatus: 402 },
  external_api_transient: { recovery: "retry",         httpStatus: 503 },
  external_api_ambiguous: { recovery: "resolve_later", httpStatus: 202 },
  database_transient:     { recovery: "retry",         httpStatus: 503 },
  dependency_unavailable: { recovery: "retry",         httpStatus: 503 },
  ambiguous:              { recovery: "resolve_later", httpStatus: 200 },
  boundary:               { recovery: "fail",          httpStatus: 500 },
};

export function policyFor(category: string) {
  const p = POLICY[category];
  if (!p) throw new Error(`unmapped category: ${category}`);   // totality check
  return p;
}
```

### 52.5 — The unhandled cells: what the analysis actually found

Mapping the modes against the code found **nine gaps**. These are the deliverable of the whole
exercise:

| # | Gap | Why it was missed | Fix |
| - | --- | ---------------- | --- |
| G-1 | FP-04 "succeeded, response lost" had no branch | The code assumed a timeout means no charge | Resolve by charge id before retrying |
| G-2 | FP-05 "row written, commit failed" was treated as a plain failure | The insert returned an error, so the code retried | Idempotency key on `order_attempts` |
| G-3 | FP-05 and FP-06 were in separate transactions | Each write was "atomic on its own" | One transaction for subscription + entitlement |
| G-4 | FP-08 "published twice" had no consumer-side dedupe | The producer assumed at-most-once | Consumer dedupes on `event_id` |
| G-5 | FP-10 "response write fails" was not a failure point at all | Nobody counts the response as an effect | Client retries with the idempotency key |
| G-6 | FP-09 email failure aborted the whole checkout | The receipt was sent before the response | Move the email to the outbox, degrade |
| G-7 | FP-01 identity provider timeout used the auth deadline | Both shared one 30 s budget | Give the identity call its own 2 s budget |
| G-8 | FP-04 provider 429 was mapped as a permanent failure | The provider's rate limit looked like a decline | Map `429` to transient with `Retry-After` |
| G-9 | No row covered "checkout cancelled mid-flight" | Cancellation was not in the guide-word list | Add the cancellation pass (52.10) |

### 52.6 — Nested operations

FP-04 is a nested operation: the charge happens **inside** the checkout, and its failure is
**translated** into our taxonomy at the boundary. The rule from Chapter 50 applies: never
re-export a provider error verbatim.

```text
Stripe error                     → our category           → our policy
card_declined (402)              → external_api_permanent → fail 402
rate_limited (429) + Retry-After → external_api_transient → retry, honour the delay
api_connection_error             → external_api_transient → retry (3)
invalid_request_error (400)      → external_api_permanent → fail 402 (our code)
```

Two nested-operation rules came out of the analysis:

- **A nested call's timeout MUST be shorter than the caller's remaining budget.** A charge with
  a 30 s timeout inside a 30 s request can never be reported as a failure — the request is dead
  first.
- **A nested call's ambiguous outcome propagates up as ambiguous**, never as transient. Mapping
  it to transient turns one lost charge into a retry storm of charges.

### 52.7 — Multi-step workflows

Checkout is the first step of a longer workflow: charge → provision → ship. When step 2 fails,
step 1 has already happened. The analysis needs a **compensation** row for every effect that
cannot be undone, and a **forward-recovery** row for every effect that can.

| Step | Effect | Undo possible? | On failure of a later step |
| ---- | ------ | -------------- | --------------------------- |
| 1. Charge card | External, irreversible | No | Refund after **15 minutes** (settlement window) |
| 2. Insert subscription | Local row | Yes (delete) | Delete in the same transaction |
| 3. Provision entitlement | External, idempotent | Yes (deactivate) | Deactivate, keep the audit row |
| 4. Publish event | External, at-least-once | No | Dedupe on the consumer side |

The rule that matters: **compensate in an order that cannot make things worse**. A refund must
never be issued before the charge is known to have settled, so the compensation is scheduled, not
immediate — hence the 15-minute delay.

### 52.8 — Dependency boundaries

Every external boundary adds modes that the local code cannot see. The boundaries in this flow:
Stripe (card), Postgres (rows), the queue broker, and the email provider.

```text
BOUNDARY CHECKLIST
  - The timeout is shorter than the caller's remaining budget
  - The response is parsed defensively: 200 with a bad body is a mode, not a success
  - A lost response is an ambiguous mode, never a transient one
  - The boundary has a circuit breaker or budget, and retries carry an idempotency key
```

The boundary checklist is short on purpose: it is the part of the analysis you can re-run on
every new dependency in under five minutes.

### 52.9 — Concurrent interleavings

```text
  client A            client B            what happens
  ───────            ───────            ────────────
  POST /orders        POST /orders
  FP-03 insert        FP-03 insert        two attempts, one order (unique key on the
                                            idempotency key — one wins)
  FP-04 charge        FP-04 charge        two charges for one order → the mode that costs money
  FP-08 publish       FP-08 publish       two events; the consumer dedupes on event_id
```

Two workers processing the same order concurrently is not exotic; it is what happens when a
client retries after a slow response. The analysis must state, per effect, whether the operation
is **serialised** (a lock, a unique constraint, a conditional update) or **safe to repeat**
(idempotent by construction). For FP-04 the answer was neither, and the fix was an idempotency
key sent to Stripe.

### 52.10 — Shutdown and cancellation

A deploy during checkout is a routine event, not an edge case. The analysis adds a pass for
every effect: *what happens if the process dies between this step and the next?*

| Effect | On SIGTERM | On client disconnect |
| ------ | ---------- | -------------------- |
| Order attempt row | Committed or not — safe | Safe |
| Card charge | **Must not be abandoned silently** | Resolve later by charge id |
| Subscription + entitlement | One transaction — safe | Safe |

The rule: **cancellation is a mode, not an exception to the analysis.** If the process can be
killed at any point, the state after the kill must be one of the states the matrix already
describes. Anything else is a new mode.

### 52.11 — Failure during recovery

Recovery can fail, and the matrix must have rows for that too:

| Recovery | Fails how | Then what |
| -------- | --------- | --------- |
| Retry | Every attempt fails | `fail` with the last category, `503` |
| Refund | The refund API is down | Queue the refund, alert, retry later |
| Resolve later | The reconciliation finds no record | Alert for a human; keep the row `unknown` |

The dangerous row is the last one: a reconciliation that concludes "nothing happened" when the
truth is "we cannot see it". That must be an **alert**, not a silent success.

### 52.12 — Ambiguous outcomes

Ambiguity is the state where the system cannot say whether the effect happened. It is not a rare
edge case; it is the **normal** state after any timeout on an irreversible effect.

```text
  client ──► charge ──► Stripe
                │           │
                │           └── effect happened
                └────────────── effect UNKNOWN (timeout, lost response)

  safe: resolve later (read back by idempotency key), or retry with the SAME key
  unsafe: a blind retry with a NEW idempotency key  → two charges
```

An ambiguous row must never be mapped to `transient`. That single mapping decision is the
difference between one charge and two.

## Key data / numbers

- **Failure points in this flow: 10**; the guide-word pass produced **62 raw modes**, pruning
  left **18 rows**, and **9 unhandled cells** were found — the deliverable.
- **Failure points per request flow: 8–15**; per background job **10–20**.
- **Risk = severity × likelihood** (both **1–5**, so **1..25**): **15–25** fix now, **8–14**
  schedule, **1–7** accept and monitor. **RPN = severity × occurrence × detection** (each
  **1–10**, so **1..1000**): ≥ **400** blocks the release, ≥ **200** needs an owner and a date.
- **Retry ceilings:** `maxAttempts` ≤ **5**; `total_deadline_ms` ≤ **30000**; retry budget ≤
  **10%** of the request deadline. The charge call uses **3 attempts** and an **8 s** budget.
- **Timeouts:** request budget **30 s**; identity **2 s**, charge **10 s**, email **3 s** — each
  strictly shorter than the caller's remaining budget.
- **SLO and error budget:** a **99.9%** checkout success SLO allows **43.8 min** of failures per
  month. G-1 (a lost charge response) at **0.4%** of checkouts consumed **17 min** of it in one
  quarter — **40%** of the budget from one gap.
- **HTTP status codes used above:** `401` unauthenticated · `402` payment declined · `409`
  conflict · `413` payload too large · `422` validation · `202` accepted, resolution pending ·
  `429` throttled · `500` unexpected bug · `503` transient.
- **SQLSTATE classes in the matrix:** `08` connection (transient → retry) · `23` constraint,
  e.g. `23505` unique violation (permanent → `409`) · `40` rollback, `40001`
  serialization_failure (transient → retry after rollback) · `42` syntax or access error
  (permanent → `500`).

## Real-world use case — Acme SaaS checkout

Acme's checkout returned `500` for every failure, retried nothing, and had one `catch` block per
step. The analysis above was run on it in a single afternoon by one engineer. Three gaps
accounted for almost all of the damage:

- **G-1 (charge succeeded, response lost).** Customers were charged twice — **37 cases** in one
  quarter, **$4,820** refunded. The fix was a read-back by charge id: on an ambiguous charge,
  look up the charge by the idempotency key before retrying, and if it is not found, retry with
  the *same* key.
- **G-3 (subscription and entitlement in separate transactions).** **0.3%** of checkouts ended with
  a subscription but no entitlement: the customer was billed for a plan they could not use, and
  each case produced a support ticket and a refund. The fix was one transaction.
- **G-8 (provider `429` mapped as permanent).** During a Stripe incident every card was declined
  rather than retried, and the checkout success rate fell from **99.7%** to **71%** in nine
  minutes. After the fix the same incident degraded to a **6%** dip that recovered on its own.

After the changes, checkout success was **99.94%** against a **99.9%** SLO, and the error budget
went from *consumed* to **72% unused**. The analysis cost one afternoon and produced roughly three
weeks of engineering work: the work was already queued, it was just not *prioritised*.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Analyse one flow at a time | Bounded; finishable | Misses cross-flow interactions | Every flow, by risk |
| Analyse the whole service | Complete picture | Nobody finishes it | A service with an owner and a quarter |
| Derive points from the architecture | Finds boundary and workflow modes | Diagrams lie | Checklists, not truth |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Number the points and keep the list in the repo | Describe the happy path and call it analysis |
| Include decision and interpretation points | Enumerate only writes and external calls |
| Treat a lost response as ambiguous | Treat a timeout as "the effect did not happen" |
| Map ambiguous to resolve-later, not retry | Retry a non-idempotent effect blindly |
| Add a row for cancellation and shutdown | Ignore that a deploy can kill the process mid-flow |
| Write a policy for a failing recovery | Assume the recovery itself cannot fail |
| Put the matrix in the repo and check it in CI | Keep the matrix in a document nobody updates |

## Common mistakes

- **The happy-path matrix.** Ten rows that all say "works as expected" — an analysis of what
  should happen, not what can happen.
- **Ambiguity mapped to transient.** The most expensive single decision in the matrix: it turns
  one lost charge into a retry storm of charges.
- **Effects assumed atomic.** Two writes that must agree, in two transactions, is a gap waiting
  for a concurrent request.
- **Analysis without a backlog.** A matrix nobody scores produces a document, not a plan.

## Checklist

- [ ] Every failure point has an id, a kind, a location, and a phase (before/after the effect), and
  every irreversible effect has a "succeeded but not acknowledged" mode.
- [ ] Every mode maps to a category, every category maps to a policy, and no ambiguous mode is
  mapped to `retry`.
- [ ] Every multi-step effect has a compensation row, including the failure of the compensation.
- [ ] Every concurrency question has an answer: serialised, idempotent, or unsafe-and-fixed.
- [ ] Cancellation and shutdown were run as a pass over every effect.
- [ ] The unhandled cells are listed, scored, and assigned an owner.

## Related

- [Enumerating Failure Points and Failure Modes (52.1–52.2)](../01-concepts/01-enumerating-failure-points-and-modes.md)
- [Mapping Modes to Categories and Recovery (52.3–52.4)](../01-concepts/02-mapping-modes-to-categories-and-recovery.md)
- [Unhandled Paths, Nested Operations, Workflows, and Dependency Boundaries (52.5–52.8)](../01-concepts/03-unhandled-nested-and-multi-step-paths.md)
- [FMEA, the Failure-Mode Inventory, and Risk Prioritization](../02-deep-dive/01-fmea-and-risk-prioritization.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
