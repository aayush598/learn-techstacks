# Distributed Transactions, Sagas, and Compensation (39.6–39.8)

> Part XV · Chapter 39 · Sections 39.6–39.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Partial Failure and Multi-Step Operations (39.1–39.3)](./01-partial-failure-and-multi-step-operations.md)

## In one sentence

A **distributed transaction** tries to make several databases commit together and can only do so
by *blocking*; a **saga** gives up on that, runs **local transactions in order**, and repairs the
middle with **compensating actions that can themselves fail**.

## Why this matters in production

Someone always proposes "just use a distributed transaction / 2PC" the first time money and
inventory disagree. It works in the demo and then holds locks across a network: one slow node and
every participant is stuck waiting for a coordinator that may itself have crashed. The alternative
— a saga — avoids the blocking but trades it for a new class of failure: **compensation failure**,
where the system has decided to undo and cannot. Both paths are legitimate; choosing blind is how
teams end up with 3 a.m. lock timeouts *or* with a refund that never happened.

## Core concept

### 39.6 Distributed transaction failures

Two-phase commit (2PC) has a coordinator and participants:

```text
                 coordinator
                    │
   PREPARE ────────▶├────────▶ participant A: can you commit?  → "yes, locked"
   PREPARE ────────▶├────────▶ participant B: can you commit?  → "yes, locked"
                    │
   ... coordinator crashes here ...
                    │
   participants hold locks, waiting for a decision that may never come
```

| Failure | What happens | Consequence |
| ------- | ------------ | ----------- |
| Participant fails before `PREPARE` | never votes yes | abort, no blocking |
| Participant fails **after** `PREPARE` | voted yes, cannot finish | coordinator must decide; if it is alive, presumed abort/commit resolves it |
| **Coordinator crashes after PREPARE** | nobody knows the decision | **blocking**: prepared participants hold locks until the coordinator returns |
| Network partition during commit | participant cannot hear the decision | same blocking; may resolve only when the partition heals |
| Mixed store, no shared 2PC | (Postgres + S3 + Stripe) | **not possible at all** — there is no coordinator everyone obeys |

Two hard limits worth memorizing:

1. **2PC is only as available as the coordinator.** It converts a partial failure into a *wait*.
2. **2PC does not exist across a payment provider or object store.** Stripe and S3 do not vote in
   your transaction. Your real system is a saga whether you named it or not.

### 39.7 Saga and compensation

A saga is a sequence of **local transactions T1…Tn**, each with a **compensating transaction
Cn…C1**. If Tk fails, the system runs Ck-1…C1 in reverse order. The saga is "atomic" only in the
sense that it always ends in a *consistent* state — possibly after a visible, user-affecting
intermediate one.

```text
Forward:   T1 reserve ─▶ T2 charge ─▶ T3 activate ─▶ T4 notify
                 ✓            ✓           ✗
Backward:                                   C2 refund ─▶ C1 release
                                            (reverse dependency order)
```

Two coordination styles:

| | **Orchestration** | **Choreography** |
|-|-------------------|------------------|
| Control | one orchestrator owns the state machine | each service reacts to events |
| Visibility | one place to read the state | state is scattered across consumers |
| Failure handling | orchestrator decides compensation | every consumer must know when to undo |
| New step | edit the orchestrator | add a consumer; coupling grows |
| Typical failure mode | orchestrator is a single point of failure (needs durability) | a missed event strands the workflow; ordering bugs |

**Recommendation:** orchestration in a durable workflow record (or a workflow engine) for anything
with money or more than three steps; choreography only for loose, event-shaped, low-stakes flows.

### 39.8 Compensation failure

Compensation is *new work*, so it fails like any other work — and it fails at the worst time,
because the forward path has already abandoned.

```text
T2 charge ✓  →  T3 fails  →  C2 refund  →  refund times out (Stripe 5xx / network)
                              ▲
                              └── money still held, workflow says "failed"
```

What makes compensation failure different:

- **It is not optional.** A failed forward step is a decision; a failed compensation is an
  *inconsistency* that persists until fixed.
- **It must be retried indefinitely (with bounds),** because there is no alternative path to
  consistency. This is where a **dead-letter / needs-attention state** for compensations matters.
- **It must be idempotent.** Refund with a deterministic key: `refund(order_id)` — never
  `refund(now())`.
- **It must be observable to humans** when it exhausts retries: this is money held by the system
  with no owner.

The three-line rule: **forward failure → decide; compensation failure → escalate; both failed →
declare `COMPENSATION_BLOCKED`, alert, and never pretend the workflow ended.**

## Worked example

```ts
// Orchestration: the orchestrator's own state is durable, one row per step.
type SagaState = "running" | "compensating" | "compensated" | "failed" | "blocked";

async function compensate(saga: Saga) {
  await setState(saga.id, "compensating");
  const done = await loadSteps(saga.id);                 // completed T's, in order
  for (const step of done.reverse()) {                   // reverse dependency order
    for (let attempt = 1; attempt <= MAX_COMP_ATTEMPTS; attempt++) {
      try {
        await step.compensate(saga.input);               // idempotent by design
        await markCompensated(saga.id, step.name);
        break;
      } catch (err) {
        await recordCompensationError(saga.id, step.name, err, attempt);
        if (attempt === MAX_COMP_ATTEMPTS) {
          await setState(saga.id, "blocked");            // never "failed" and done
          await alert("saga.compensation_blocked", { saga: saga.id, step: step.name });
          return { state: "blocked", step: step.name };
        }
        await sleep(backoff(attempt));                   // 1s, 2s, 4s… + jitter
      }
    }
  }
  await setState(saga.id, "compensated");
  return { state: "compensated" };
}
```

```python
# The compensation itself must be idempotent: refund once per order, not per attempt.
def refund(order_id: str, amount: int) -> None:
    existing = stripe.Refund.list(charge=charge_for(order_id), limit=10)
    if any(r.metadata.get("order_id") == order_id for r in existing.data):
        return                                   # already refunded — success, not an error
    stripe.Refund.create(charge=charge_for(order_id),
                         amount=amount,
                         idempotency_key=f"refund:{order_id}")   # one key per logical refund
```

## Key data / numbers

- **SQLSTATE `40001` (`serialization_failure`) and `40P01` (`deadlock_detected`)** are the retry
  signals inside a *local* step; **`55P03` lock_not_available** is what long-held 2PC/prepared
  locks and `lock_timeout = 0` (wait forever) produce under load.
- Postgres `deadlock_timeout` defaults to **1 s** (detect, then abort one victim with `40P01`);
  MySQL `innodb_lock_wait_timeout` defaults to **50 s** — a prepared/locked participant can hold
  a row for 50 s before anyone notices.
- Stripe refunds: pass an **`Idempotency-Key`** (`refund:<order_id>`); duplicate refund attempts
  with the same key replay the same response instead of double-refunding.
- A saga compensating chain is **O(n)** sequential calls; budget its worst case (e.g. 6 steps ×
  2 s timeout × 5 retries) before you promise an API response time.
- **The transactional outbox** (write the event in the same local transaction, relay it after) is
  how saga progression events survive a crash between "state changed" and "published."

## Real-world use case — Acme SaaS

`Checkout` used choreography: `order.created` → `inventory.reserved` → `charge.captured` →
`subscription.active`. One consumer was redeployed and missed `inventory.reserved`; the charge
succeeded anyway and the subscription never activated. Compensation (`release` + `refund`) was
triggered by a *different* consumer and raced with a retry of `charge.captured`, producing two
refunds for one order. The fix: an **orchestrated saga** with a durable `sagas`/`saga_steps` table,
compensation keyed by `order_id`, and `COMPENSATION_BLOCKED` alerting. Refund duplicates went to
zero; the ambiguous workflow that used to sit in "unknown forever" now reaches a terminal state
within **5 minutes**, visible in the admin UI.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| 2PC across two databases you control | true atomicity, no compensations | blocking, coordinator availability, lock holding | rare; only two owned stores, low latency, strong ops |
| Saga + orchestration | non-blocking, visible, resumable | visible intermediate states; compensation code | default for money + external effects |
| Saga + choreography | loose coupling, simple services | scattered state, missed events, hard to undo | low-stakes, event-shaped flows |
| Best-effort + reconciliation job | simple at write time | inconsistent window; needs a source of truth | high volume, tolerance for lag (analytics, counters) |
| Do nothing | — | divergence accumulates | never once money is involved |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "can Stripe vote in my transaction?" before proposing 2PC | Apply 2PC across a payment provider or object store |
| Make every compensation idempotent by business key | Generate a refund/idempotency key per attempt |
| Retry compensations with a bounded loop + escalation | `catch` a failed compensation and continue |
| Persist saga state in the same DB as the step it describes | Keep saga state only in the orchestrator's memory |
| Publish progression events through an outbox | Publish after commit with a bare `fire-and-forget` |
| Give compensation failures a human-visible terminal state | Let a blocked compensation look like `failed` (done) |

## Common mistakes

- **Compensating an ambiguous step** — refunding a charge you cannot confirm happened, or skipping
  one that did. Resolve first (read-back), compensate second.
- **Compensation in forward order** — releasing inventory before refunding can oversell if the
  refund then fails and the order must be reinstated.
- **"It's a saga" as an excuse for no atomicity** — each *step* must still be atomic locally; sagas
  compose transactions, they do not replace them.
- **Infinite compensation retries with no escalation** — a permanently declined refund loops
  forever and hides the real problem.
- **Choreography with no single state reader** — nobody can answer "is this order paid?" without
  grepping three services.

## Checklist

- [ ] Cross-boundary operations are named: 2PC (rare) or saga (usual).
- [ ] Each step is a local transaction with its own idempotency key.
- [ ] Compensation exists for every step that has an external or money effect.
- [ ] Compensation is idempotent and runs in reverse dependency order.
- [ ] Compensation failures have bounded retries **and** an escalation state.
- [ ] Saga state is durable and readable by one owner.
- [ ] Events leave through an outbox, not a post-commit publish.
- [ ] Ambiguous steps are resolved before compensation is chosen.

## Related

- [Saga and Compensation Mechanics — deep dive](../02-deep-dive/01-saga-and-compensation-mechanics.md)
- [Checkout Saga with Compensating Actions](../03-practical-examples/01-checkout-saga-with-compensating-actions.md)
- [After-Commit Failures, Outbox, and Cross-Store (23.15–23.20)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/01-concepts/05-after-commit-failures-outbox-and-cross-store.md)
- [Idempotency in Payments, Jobs, and Webhooks](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md)
