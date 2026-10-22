# States, Compensation Safety, and Irreversibility (39.13–39.16)

> Part XV · Chapter 39 · Sections 39.13–39.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Workflow Recovery and Long-Running Operations (39.9–39.12)](./04-workflow-recovery-and-long-running-operations.md)

## In one sentence

Every multi-step operation needs **explicit intermediate states** that say what is true *now*,
**compensation that can never run twice for one logical undo**, and a final distinction between
what is **recoverable** and what is genuinely **terminal**.

## Why this matters in production

The worst production bugs are not crashes; they are systems that *look* finished and are not. A
workflow in memory with no `COMPENSATING` state cannot be resumed, a refund handler without a
dedupe marker issues two refunds, an "email sent" step retried after a crash sends twice, and an
operator who cannot tell `failed` from `blocked` restarts the wrong thing. States, safety, and
terminality are the same concern seen from three angles: **can it continue, can it be undone, and
should it ever run again?**

## Core concept

### 39.13 Explicit intermediate states

Model states as a closed enum — if a value is not in the type, it cannot be reached:

```text
                 ┌──────────▶ failed ──────────────┐
                 │                                ▼
 pending ──▶ running ──▶ (steps done) ──▶ compensating ──▶ compensated
                 │            │                  │
                 │            ▼                  └──▶ blocked   (needs a human)
                 ├──▶ cancelling ──▶ cancelled
                 │
                 └──▶ expired ──▶ (compensate if partial effects)

 terminal: succeeded | compensated | cancelled | failed | expired
 non-terminal: pending | running | compensating | cancelling | blocked | unknown
```

The properties that make a state model trustworthy:

| Property | Rule |
|----------|------|
| **Closed** | an enum; every value is defined, no `"in-progress-ish"` strings |
| **Monotone progress** | forward states never silently jump back to `running` |
| **One terminal transition** | moving to a terminal state happens exactly once (guard it with a conditional `UPDATE`) |
| **Every state has an owner** | who advances it, and by what trigger |
| **Every state has a promise** | what the UI/support may tell the customer |
| **`blocked` is not `failed`** | `failed` implies "done, not applied"; `blocked` implies "inconsistent, human needed" |

```sql
-- One-shot terminal transition: the WHERE clause is the concurrency control.
UPDATE workflows
   SET state = 'succeeded', finished_at = now()
 WHERE id = $1 AND state = 'running';   -- 0 rows = someone else already finished it
```

### 39.14 Preventing duplicate compensation

Compensation runs under retries, redeliveries, operator replays, and crashed runners. Make the
*logical undo* happen exactly once even though the *code* may run many times:

| Mechanism | How | Cost |
|-----------|-----|------|
| **Deterministic idempotency key** | `refund:<order_id>` sent to the provider | none, works across processes |
| **State guard in SQL** | `UPDATE ... WHERE state='running'` → 0 rows means already done | one line, per transition |
| **Compensation ledger row** | `INSERT INTO compensations (step_id, kind) ON CONFLICT DO NOTHING`; skip if conflict | auditable, queryable |
| **Provider read-back** | list refunds for the charge, check metadata | works even after a lost ack |
| **Single-runner lease** | only the lease holder may compensate | prevents concurrent double-undo |

Use **at least two of them** for money. The ledger alone fails if the crash happens *between* the
effect and the ledger write; the provider read-back covers exactly that gap.

```sql
CREATE TABLE compensations (
  step_id      uuid PRIMARY KEY,           -- one logical undo per step
  kind         text    NOT NULL,           -- refund | release | revoke
  state        text    NOT NULL DEFAULT 'pending',
  attempt      int     NOT NULL DEFAULT 0,
  provider_ref text,                       -- refund id, once known
  updated_at   timestamptz NOT NULL DEFAULT now()
);
-- money path: insert first (intent), then act, then mark done
INSERT INTO compensations (step_id, kind) VALUES ($1, 'refund')
ON CONFLICT (step_id) DO NOTHING;
```

### 39.15 Irreversible side effects

Some steps cannot be undone. Treat them as a **design constraint**, not an error-handling detail:

| Effect | Undo available? | Rule |
|--------|-----------------|------|
| DB row insert/update | yes (delete/restore) | keep it local to the workflow's transaction |
| Inventory reservation | yes (release) | reversible, compensate in reverse order |
| Payment capture | yes, but as a **new** action (refund) | costs money, takes days, may be noticed |
| Queue message published | no recall — use **compensating events** | consumers must be idempotent anyway |
| Email/SMS sent | **no** | run last, only after durable success |
| LLM call / token spend (`AgentRun`) | **no** | money spent; cache the result, don't replay |
| Audit/compliance log entry | no | append a *correcting* entry, never delete |
| Webhook delivered to a third party | no | they may already have acted; send a reversal event |

Rules that follow:

1. **Order by reversibility**: fully reversible first, costly-reversible middle, irreversible last.
2. **If an irreversible effect already happened and the workflow must fail, the outcome is not
   "failed"** — it is `failed_with_side_effects`, and it must be visible to a human.
3. **Make irreversible steps conditional on a durable decision** (a committed row), so a crash
   cannot re-decide to send.

### 39.16 Terminal vs recoverable states

A state is **recoverable** if an automated process can, without new information from a human,
move it to a terminal state. A state is **terminal** if no automatic action remains.

```text
recoverable: pending, running, compensating, cancelling, unknown, (expired→compensate)
terminal:    succeeded, compensated, cancelled, failed, expired
needs human: blocked, failed_with_side_effects   ← semi-terminal: automation stopped on purpose
```

- **Recoverable** → belongs to the sweeper/resumer; must have a retry policy and a budget.
- **Terminal** → must be *absorbing*: no code path may move `succeeded` back to `running`.
- **Blocked / needs-human** → the escalation target after retries are exhausted; alert, page, and
  provide the ledger + one-click or runbook actions.

## Worked example

```ts
// A workflow whose states, dedupe, and terminality are enforced in code + SQL.
export async function compensateStep(stepId: string, kind: "refund" | "release" | "revoke") {
  const inserted = await db.one(
    `INSERT INTO compensations (step_id, kind) VALUES ($1, $2)
     ON CONFLICT (step_id) DO NOTHING RETURNING step_id`, [stepId, kind]);
  if (!inserted) {
    const row = await db.oneOrNone(`SELECT state FROM compensations WHERE step_id=$1`, [stepId]);
    if (row?.state === "done") return { skipped: true };     // already compensated
    // row exists in 'pending'/'failed' → this runner (or another) may resume it
  }

  await db.query(`UPDATE compensations SET attempt=attempt+1 WHERE step_id=$1`, [stepId]);
  try {
    const ref = await performCompensation(kind, stepId);      // idempotent provider key
    await db.query(
      `UPDATE compensations SET state='done', provider_ref=$2, updated_at=now()
       WHERE step_id=$1 AND state <> 'done'`, [stepId, ref]);
    return { done: true, ref };
  } catch (err) {
    const attempt = await bumpAndReadAttempt(stepId);
    if (attempt >= MAX) {
      await db.query(`UPDATE compensations SET state='blocked' WHERE step_id=$1`, [stepId]);
      await db.query(
        `UPDATE workflows SET state='blocked' WHERE id = (SELECT workflow_id
           FROM workflow_steps WHERE id=$1) AND state='compensating'`, [stepId]);
      await alert("compensation.blocked", { stepId, kind, err: classify(err) });
      throw new CompensationBlocked(stepId, err);            // never swallow
    }
    throw new RetryCompensation(stepId, err);                // retried by the runner
  }
}
```

```text
Crash after performCompensation, before UPDATE:
  compensations: state='pending', attempt=1, provider_ref=NULL
  provider (Stripe): refund rf_8q2 EXISTS with idempotency_key='refund:ord_3k9'
  on resume → performCompensation re-runs with the SAME key → Stripe replays rf_8q2
  → UPDATE state='done'  ⇒ exactly one refund despite two executions
```

## Key data / numbers

- **`HTTP 409 Conflict`** for an operation already in progress or a state transition that is no
  longer legal; **`410 Gone`** for a terminal state the client should stop retrying (e.g. expired
  workflow); **`422`** for a transition blocked by a business rule.
- Refund idempotency keys are honored by major PSPs for **24 hours**; the *ledger* is what protects
  you beyond that window.
- Keep **compensation retries bounded but long** (e.g. 5–10 attempts over 15–30 minutes) then go
  `blocked`; a compensation that gives up after 3 attempts strands money.
- Sweeper cadence: check for stuck `running`/`compensating` rows every **30–60 s**; lease expiry is
  what lets the sweeper act safely.
- State history matters for support: keep an append-only `workflow_events` row per transition
  (commonly retained **90 days** minimum for billing workflows).

## Real-world use case — Acme SaaS

`Checkout` had a `cleanup` function that refunded and released inventory, called from three places:
the failure path, an operator "cancel" button, and a cron sweeper. All three could run for the same
order within the same minute after a deploy, and one Stripe incident made retries slow enough that
the sweeper joined in: **three refunds for one $4,900 invoice**. The fix was a `compensations` table
with `step_id` as primary key, a state-guarded `UPDATE` for the terminal transition, and the
provider read-back (`Refund.list` by charge) for the crash window. Duplicate refunds went to zero;
support gained an audit trail showing exactly which runner executed which undo and when.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Closed state enum + guarded transitions | impossible to reach undefined states | schema/code churn when states grow | every workflow with money or users |
| Free-form status strings | fast to add | drift, unreachable combinations, silent typos | never |
| Provider idempotency key only | no schema change | 24 h window, lost if key forgotten | as the *second* safety layer |
| Ledger + idempotency key | survives crashes, replay, and multi-process | one table to maintain | money paths, default |
| Compensate everything automatically | no humans needed | wrong for irreversible/blocked cases | only for reversible effects |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model intermediate states explicitly in an enum | Store `status: "in-progress"` as a free string |
| Make the terminal transition a guarded `UPDATE` | Set terminal state unconditionally |
| Dedupe compensation by logical step id | Key compensation by attempt or timestamp |
| Separate `blocked` from `failed` | Report an inconsistent system as "failed, done" |
| Put irreversible effects after durable success | Send email/notify before payment settles |
| Keep a transition history for support | Overwrite status with no history |

## Common mistakes

- **`ON CONFLICT DO NOTHING` without reading back** — you cannot tell "already done" from
  "already pending"; the code then skips work that never happened.
- **Compensating by deleting rows** — destroys the audit trail needed to prove what occurred.
- **Calling the sweep `failed`** — operators stop investigating because it looks finished.
- **`failed` used for both "rolled back cleanly" and "money held"** — the two need opposite
  responses.
- **Allowing `running → running` re-entry from a second runner** — the root of duplicate
  compensation; a lease plus the guarded update prevents it.
- **Treating an irreversible effect as an error to hide** — `failed_with_side_effects` must be
  loud, not caught and logged.

## Checklist

- [ ] Workflow states are a closed enum with an owner and a customer-facing promise per state.
- [ ] Terminal transitions are guarded (`WHERE state=...`) and happen once.
- [ ] Compensation has a ledger keyed by logical step id **and** a provider idempotency key.
- [ ] Reversible → costly → irreversible ordering is enforced in the step list.
- [ ] `blocked` / `failed_with_side_effects` alert a human with the ledger attached.
- [ ] Every recoverable state has a sweeper, a retry policy, and a budget.
- [ ] No path can move a workflow out of a terminal state.

## Related

- [Distributed Transactions, Sagas, and Compensation (39.6–39.8)](./03-distributed-transactions-sagas-and-compensation.md)
- [Saga and Compensation Mechanics — deep dive](../02-deep-dive/01-saga-and-compensation-mechanics.md)
- [Checkout Saga with Compensating Actions](../03-practical-examples/01-checkout-saga-with-compensating-actions.md)
- [Terminal State and Standard Lifecycle](../../../part-04-architecture/11-the-error-lifecycle/01-concepts/05-terminal-state-and-standard-lifecycle.md)
