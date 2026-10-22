# Saga and Compensation Mechanics

> Part XV · Chapter 39 · Sections 39.6–39.8, 39.14 (mechanics) · _Estimated reading time: 26 min_
> **Prerequisite:** [Distributed Transactions, Sagas, and Compensation (39.6–39.8)](../01-concepts/03-distributed-transactions-sagas-and-compensation.md)

## In one sentence

A saga's correctness comes from four mechanical properties — **durable step records, reverse-order
compensation, idempotent undo, and an escalation terminal state** — and breaking any one of them
turns the saga into a distributed inconsistency generator.

## Why this matters in production

Design docs describe sagas as boxes and arrows; production breaks them in the seams: the
compensation that fires twice, the one that never fires because the orchestrator crashed before
recording the decision, the event published for a step that rolled back. This file is the
mechanics — the exact write ordering and state transitions that make a saga behave like the
diagram.

## The two coordinators

```text
ORCHESTRATION                              CHOREOGRAPHY
┌──────────────┐                           order.created ──▶ inventory-svc
│ orchestrator │── invokes step 1          inventory.reserved ──▶ billing-svc
│ (durable FSM)│── invokes step 2          charge.captured ──▶ subscription-svc
│── decides    │── runs compensation       subscription.active ──▶ notifier
│   to undo    │                           each consumer: act on event, emit next
└──────────────┘                           undo: each consumer listens for *.failed
   state lives HERE                          state lives NOWHERE (the bug)
```

| Concern | Orchestration | Choreography |
|---------|---------------|--------------|
| Source of truth | `sagas` + `saga_steps` rows | the union of every consumer's tables |
| "Where is this order?" | one query | grep three services |
| Compensation trigger | orchestrator, one place | every consumer must react to a failure event |
| Coupling | orchestrator knows steps | producers/consumers know each other's events |
| Failure if a message is lost | orchestrator retries its own step | workflow silently stalls |
| Recommended for | money, >3 steps, user-visible state | loose, optional, low-stakes flows |

**Recommendation: orchestration with a durable state record** for anything involving money or
entitlement. Choreography is not wrong — it is just missing a place to look when it breaks.

## The write ordering (this is the whole game)

Every step follows the same five writes. Deviating from the order is how sagas lose work:

```text
1. INSERT/UPDATE saga_steps (state='running', attempt+1)     durable intent
2. perform the step (local txn OR external call with key)
3. UPDATE saga_steps (state='done', result_ref)              durable outcome
4. append saga_events (outbox, same txn as 3)                progression event
5. advance the FSM: next step or finish                      decision

on failure of 2:
  UPDATE saga_steps (state='failed', error_code)
  set saga.state = 'compensating'                            durable decision to undo
  → compensation loop runs from the highest 'done' step
```

Why each write exists:

| Write | If you skip it |
|-------|----------------|
| 1 intent before action | a crash leaves no evidence the step was attempted; a sweeper may double-run it |
| 3 outcome after action | a crash after the effect looks like "never ran" → duplicate effect |
| 4 outbox with 3 | the next consumer never hears; the saga stalls with `done` steps and no progress |
| 5 durable decision | a crash after failure but before deciding leaves `failed` with no compensation — the worst state of all |

> ⚠️ **Hazard.** The decision to compensate must be **persisted before compensation starts**.
> If the orchestrator dies between "T3 failed" and "start undoing," a fresh process must be able to
> see `state='compensating'` and continue. A decision that lives only in a local `catch` block is
> lost, and the saga is stranded mid-flight.

## Compensation ordering

Compensations run in **reverse dependency order**, not reverse execution order by accident — they
are related but not identical. Dependency order is the rule:

```text
Forward (dependency order):   reserve ─▶ charge ─▶ activate ─▶ notify
Reverse (compensate):                        notify* ─▶ deactivate ─▶ refund ─▶ release
                                                     (* irreversible — see below)
```

Rules:

1. **Reverse of dependency**, so no compensation invalidates an assumption a later compensation
   still needs. Refund before releasing inventory: if the refund fails and you must re-activate,
   inventory is still held.
2. **Skip forward steps that never completed** (`pending`, `failed`) — compensate only `done`.
3. **Skip already-`compensated` steps** (idempotent by state guard).
4. **Irreversible steps are never compensated** — they are either not-yet-run (because they are
   last) or they require `failed_with_side_effects` escalation.
5. **Compensation runs even when nobody is watching**: a sweeper picks up `state='compensating'`
   rows and continues — compensation cannot depend on the original process being alive.

## Retrying a failed compensation

```text
compensation attempt loop
  attempt 1..N:  run Ck (idempotent key) ── ok ─▶ mark step compensated ─▶ continue Ck-1
                      │
                      └── fail ─▶ backoff (1s, 2s, 4s, … + jitter)
                                      │
                    attempt < N ──────┘
                    attempt = N ──────▶ saga.state='blocked'
                                        alert with: saga id, step, last error, ledger link
                                        NO further automatic action
```

- **Bound attempts but not too tightly.** Compensations are the only path to consistency; give
  them 5–10 attempts across 15–30 minutes before escalating.
- **Differentiate errors while retrying**: `40001`/`40P01`/timeout/5xx are retryable; `409`
  (already refunded / state conflict) means *re-read* and possibly mark done; a permanent provider
  rejection (`402`, invalid refund window) means escalate immediately — retrying cannot help.
- **Never let compensation retry forever silently.** An infinite loop with no alert is an
  unowned inconsistency.

## Failure matrix

| Failure point | Mechanical response |
|---------------|---------------------|
| Step 2 (action) fails cleanly | mark `failed`, persist `compensating`, undo `done` steps |
| Step 2 outcome **ambiguous** (timeout) | resolve by read-back first; only then run or continue |
| Crash **before** write 1 | nothing happened — safe, sweeper sees no intent |
| Crash **between** 1 and 2 | step `running` with no effect or an unknown effect → resolve by key on resume |
| Crash **between** 2 and 3 | effect exists, ledger says `running` → idempotent re-run or read-back |
| Crash **between** 3 and 4 | state advanced, event missing → outbox relay publishes on restart |
| Crash **after** 5 (decision) | `compensating` persisted → sweeper completes the undo |
| Compensation fails N times | `blocked` + alert; human runbook |
| Orchestrator itself lost | new instance claims the lease and resumes from durable state |

## Worked example — the orchestrator core

```ts
export class SagaRunner {
  async advance(sagaId: string) {
    const saga = await this.store.load(sagaId);            // durable FSM
    if (saga.leaseExpired() === false) return;             // another runner owns it

    if (saga.state === "compensating") return this.compensate(saga);
    if (saga.state !== "running") return;                  // terminal or blocked: stop

    for (const step of saga.pendingSteps()) {
      await this.store.markRunning(sagaId, step.name);                     // write 1
      try {
        const ref = await step.execute(saga.input);                        // step 2
        await this.store.markDone(sagaId, step.name, ref);                 // write 3
        await this.store.appendOutbox(sagaId, `${step.name}.done`, ref);   // write 4
      } catch (err) {
        const e = classify(err);
        if (e.ambiguous) {
          const resolved = await resolveByKey(step, saga.input);           // never guess
          if (!resolved.known) { await this.store.markUnknown(sagaId, step.name); return; }
          if (resolved.done) { await this.store.markDone(sagaId, step.name, resolved.ref); continue; }
        }
        await this.store.markFailed(sagaId, step.name, e.code);            // write 3'
        if (e.retryable && step.attempt < MAX_STEP_ATTEMPTS) {
          await this.store.markPending(sagaId, step.name);                 // retry forward
          return;
        }
        await this.store.enterCompensating(sagaId, e.code);                // write 5 — durable
        return this.compensate(saga);                                      // then act
      }
    }
    await this.store.finish(sagaId, "succeeded");          // guarded terminal transition
  }
}
```

```sql
-- The guarded terminal transition: concurrency control in one statement.
UPDATE sagas SET state='succeeded', finished_at=now()
 WHERE id=$1 AND state='running';
-- The compensation claim: only one runner may execute a given undo.
INSERT INTO compensations (step_id, kind) VALUES ($1,$2)
ON CONFLICT (step_id) DO UPDATE SET attempt=compensations.attempt+1
 WHERE compensations.state IN ('pending','failed') RETURNING attempt;
```

## Key data / numbers

- Typical orchestration overhead: **1 extra write per step** (ledger + outbox in the same
  transaction) plus **1 state row per saga** — negligible next to the business writes.
- Deadlock/serialization inside the ledger writes: retry on **`40001` / `40P01`** with the wrapper
  from [Ch. 23 practical examples](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
  — the ledger is itself a hot table under concurrency.
- Outbox relay poll interval is commonly **250 ms–2 s**; CDC-based relays approach sub-second.
- Compensation escalation defaults: **5–10 attempts, 15–30 min**, then `blocked` + page.
- Queue redelivery/visibility timeout (commonly **30–300 s**) must exceed the longest single step
  or two runners overlap; fencing (40.11) is the belt to that suspenders.

## Real-world use case — Acme SaaS

Acme's first saga used choreography and recorded "decision to refund" only in a log line. During a
`billing-svc` deploy, the process died after `charge.captured` failed and before `refund.requested`
was emitted: three customers were charged with no subscription and **no pending undo anywhere**.
Support found them by accident two weeks later. Moving to an orchestrated saga with
`state='compensating'` persisted *before* the first refund call, plus a 60-second sweeper, made the
same class of crash self-healing: inject the failure in staging today and the saga reaches
`compensated` within ~90 seconds with zero human involvement; a compensation that exhausts retries
lands in `blocked` with a Slack alert carrying the ledger link.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Orchestrator in the same DB as step 1 | atomic state + outbox, simplest | orchestrator tied to one store | one primary DB owns the workflow |
| Separate workflow engine | durability, timers, visual state | operational cost, another system | dozens of sagas, long timers |
| Choreography | zero central component | scattered state, silent stalls | optional/low-stakes flows |
| Compensate forward order | simpler code | breaks dependency assumptions | never once steps have dependencies |
| No compensation for failed steps | less code | permanent divergence | never once money/entitlements are involved |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Persist the compensate decision before compensating | Decide to undo inside a local `catch` only |
| Compensate in reverse dependency order | Compensate in whatever order the array has |
| Claim each undo with a ledger row | Fire compensations from three call sites |
| Let a sweeper finish `compensating` | Rely on the original request/process being alive |
| Escalate to `blocked` after bounded retries | Retry a permanently-rejected refund forever |
| Emit progression events from an outbox | Publish after commit with no durability |

## Common mistakes

- **State and events written in separate transactions** — the saga advances but nobody hears, or
  the event claims progress that rolled back.
- **Retrying the whole saga instead of the failed step** — duplicates every completed effect.
- **Compensating `failed` steps** — undoing something that never happened.
- **A compensator that calls a non-idempotent API with a fresh key per attempt** — the classic
  double refund.
- **Optimistic "the orchestrator will never die"** — if resume is not implemented and tested, the
  saga is not implemented.
- **Alerting only on `failed`, not on `blocked`/stale `compensating`** — the states that actually
  need a human never page anyone.

## Checklist

- [ ] Orchestration vs choreography chosen deliberately and documented.
- [ ] The five-write ordering is enforced for every step.
- [ ] The compensate decision is durable before the first undo call.
- [ ] Compensation order is reverse dependency, computed from the step graph.
- [ ] Every undo is idempotent (ledger key + provider key).
- [ ] A sweeper resumes `compensating` and `running` with an expired lease.
- [ ] Bounded retries end in `blocked` + alert, never in silence.
- [ ] Events come from an outbox written with the state change.
- [ ] Injected-crash tests prove resume works for each failure point.

## Related

- [Checkout Saga with Compensating Actions](../03-practical-examples/01-checkout-saga-with-compensating-actions.md)
- [States, Compensation Safety, and Irreversibility (39.13–39.16)](../01-concepts/05-states-compensation-safety-and-irreversibility.md)
- [Outbox and Compensation in Code](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/03-practical-examples/02-outbox-and-compensation-in-code.md)
- [Chapter 39 Reference — rollback vs compensation guide](../05-reference/README.md)
