# State Transitions, Lifecycle, and Workflow Preconditions

> Part VII · Chapter 18 · Sections 18.4, 18.6, 18.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [Invariants, Business Rules, and Multiple Violations](./02-invariants-and-business-rules.md)

## In one sentence

An **invalid state transition** is a caller attempting an arrow your state machine does not have,
a **lifecycle** is the full set of legal arrows over time, and a **workflow precondition** is a
gate that must be satisfied *before* an arrow is even considered — each deserving its own coded
domain error, not a generic `409`.

## Why this matters in production

Subscriptions, jobs, exports, invoices, and agent runs are all state machines, and the most
common production bugs are transition bugs: double-cancel, activate-after-cancel, export start
during pause, refund after capture-failure. When these arrive as generic errors, clients retry
blindly (making it worse), support cannot tell "already done" from "never started", and each new
state is added in three different `switch` statements that drift. Explicit machines + explicit
errors turn "cannot cancel" from a crash into a **documented answer**.

## The pattern

```text
                    ┌──────────► canceled ◄──────────┐
                    │  cancel                        │ cancel
 trial ──activate──►│ active ──past_due──► suspended │
                    │   │                    │       │
                    │   └──cancel──► canceled┘       │
                    └────────────────────────────────┘
   legal arrows only; every other (state, action) pair has a code.
```

```ts
const TRANSITIONS: Record<State, Partial<Record<Action, State>>> = {
  trial:     { activate: "active",  cancel: "canceled" },
  active:    { past_due: "past_due", cancel: "canceled" },
  past_due:  { activate: "active",  cancel: "canceled", suspend: "suspended" },
  suspended: { activate: "active",  cancel: "canceled" },
  canceled:  {},                                              // terminal
};

export function transition(sub: Subscription, action: Action): Result<Subscription, DomainError> {
  const next = TRANSITIONS[sub.state]?.[action];
  if (!next) {
    return err(new InvalidTransition(action, sub.state, {
      allowed: Object.keys(TRANSITIONS[sub.state] ?? {}),
    }));
  }
  return ok(withState(sub, next));
}
```

Why the table beats scattered `if`s: **one place to audit**, one place to add a state (review
shows every legal arrow), and `allowed` in the error details is free documentation for clients.

## 18.4 — Invalid state transition

The error must answer three questions the caller needs:

```json
{
  "code": "INVALID_TRANSITION",
  "category": "LIFECYCLE",
  "details": { "action": "cancel", "state": "canceled", "allowed": [] },
  "httpStatus": 409
}
```

| Member | Why it exists |
| ------ | ------------- |
| `action` | Which arrow was attempted |
| `state` | Current state (fresh — see staleness below) |
| `allowed` | What the caller *can* do now — turns a rejection into guidance |
| `409` | Conflict with current state; client must refresh, not retry identically |

**Staleness discipline:** evaluate transitions against **re-read state** (or a version-checked
read). A transition rejected against a cached 30-second-old subscription may have become legal —
or the reverse — and the difference is a support incident ([optimistic
concurrency](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)).

**Idempotent actions:** if "cancel" on an already-canceled subscription is a *no-op by design*,
return `ok` (idempotent success), not an error. Reserve `INVALID_TRANSITION` for genuinely
illegal arrows. Document which actions are idempotent — this is the #1 source of "double-click"
bugs.

## 18.6 — Lifecycle

The lifecycle is the *whole machine*, and each state needs an explicit contract:

| Concern | Decide per state | Example (`ExportJob`) |
| ------- | ---------------- | --------------------- |
| Entry rules | Precondition to enter | `start` requires valid spec (Ch. 17) |
| Exit rules | Actions allowed | `running → pause/cancel/complete` |
| Terminal states | Nothing exits | `completed`, `canceled`, `failed` |
| Time-driven edges | Scheduler owns them | `past_due` grace → `suspended` |
| Observability | State exposed to clients | `GET /jobs/:id` returns `state` + `stateReason` |

Lifecycle rules that prevent the classic bugs:

1. **Terminal is terminal.** No resurrection from `canceled`/`completed` without a *new* entity
   (or a named, coded `RESURRECTION_NOT_SUPPORTED` — better: forbid it).
2. **Every edge has an owner**: a command (`pause`), a scheduler tick (`grace_expired`), or a
   webhook (`payment_failed`) — never "whatever happened to run".
3. **Illegal edges are tested** — enumerate the matrix `(state × action)` in tests; the table
   above makes that a loop, not a wishlist.

```text
 state × action matrix test (one row per state, one column per action):
            activate  pause  resume  cancel  fail
 trial        ✓         ✗      ✗       ✓      ✗
 active       ✗         ✓      ✗       ✓      ✓
 canceled     ✗         ✗      ✗       (idem) ✗
   ✗ must produce INVALID_TRANSITION with correct `allowed`.
```

## 18.10 — Workflow preconditions

A precondition is a gate evaluated *before* the transition even makes sense — "cannot start
export while another export is running", "cannot downgrade below current seat usage", "cannot
publish while verification is pending".

| Precondition | Code (example) | HTTP | Caller remedy |
| ------------ | -------------- | ---- | ------------- |
| Another operation in flight | `OPERATION_IN_PROGRESS` | `409` | Wait / status endpoint |
| Usage exceeds target plan | `DOWNGRADE_NOT_POSSIBLE` | `409` + details | Free seats first |
| Verification/email pending | `VERIFICATION_REQUIRED` | `409` (or `403`) | Complete verification |
| Dependency not ready (parent job) | `DEPENDENCY_PENDING` | `409` | Poll dependency |
| Grace period policy | `GRACE_PERIOD_ACTIVE` | `409` | Wait; shows `endsAt` |

Precondition vs transition, in one line: **transition checks the machine; preconditions check the
world around the machine.** Both map to `409` commonly, but their `code`s differ so clients can
act (wait vs refresh vs upgrade).

```json
{
  "code": "OPERATION_IN_PROGRESS",
  "category": "PRECONDITION",
  "details": { "blocking": { "kind": "export_job", "id": "job_71a2", "state": "running" },
               "retryAfterMs": 30000 },
  "httpStatus": 409
}
```

`retryAfterMs` (or `Retry-After` on the response) is what keeps clients from hammering a
deliberately-blocked action — see Ch. 27 for the retry contract.

## Key data / numbers

- Default status for transition/precondition denial: **`409 Conflict`**; include `state`,
  `action`, `allowed` in `details`.
- Idempotent re-invocation of a completed action: **success**, not `409` — document per action.
- Staleness: re-read state or compare a **version** before rejecting/accepting transitions.
- Terminal states: `canceled`, `completed`, `failed` — no exits; new work = new entity.
- Time-driven edges (grace expiry) are transitions too: same table, scheduler as caller.

## Real-world use case — ExportJob

`ExportJob` allowed `start` from any state. Two exports ran concurrently for one tenant, doubling
S3 costs, and a "cancel" during `finalizing` deleted a nearly-complete object — the worker
thought `cancel` meant abort, the client thought it meant "lose nothing". The fix: a transition
table where `start` is legal only from `queued`/`failed` (retry), `cancel` from
`queued/running/paused` only, and `finalizing` accepts nothing but `complete`. `cancel` during
`finalizing` now returns `409 INVALID_TRANSITION` with `allowed: []` and `stateReason:
"finalizing_near_complete"` so the client can tell the user "almost done — cancelling now would
discard it". Concurrent-start attempts get `409 OPERATION_IN_PROGRESS` with the blocking job id.
Cost anomaly alerts for the tenant stopped.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Declarative transition table | Auditable, testable, free `allowed` | Slightly more upfront design | ✅ Any real state machine |
| Scattered `if (state == …)` | Easy first draft | Drift, untestable matrix | Prototypes only |
| State-machine library (XState, etc.) | Visualization, history | Dependency, learning curve | Complex long-lived workflows |
| `409` + details for all gates | One client branch | Overloads 409 meaning | ✅ Default; keep codes distinct |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode the machine as a table; test the full matrix | Scatter transitions across services |
| Return `allowed` and `state` with every rejection | Emit bare "invalid operation" |
| Make re-invoking a completed action idempotent-success | Punish double-clicks with `409` |
| Re-read/version-check before transitions | Decide against stale caches |
| Give each gate its own code (`OPERATION_IN_PROGRESS`, …) | One `PRECONDITION_FAILED` for all |

## Common mistakes

- **`cancel` treated as idempotent when it discards data** — decide per action, not per verb
  habit.
- **Scheduler edges without codes** — grace expiry silently transitions; nobody can explain a
  suspension.
- **Leaking internal state names** (`ST_FIN_03`) — expose stable, documented state identifiers.
- **Forgetting `allowed`** — forces clients to hardcode your machine, which then breaks when you
  add a state.

## Checklist

- [ ] Transition table is the single source; matrix test covers every (state × action).
- [ ] Every rejection carries `state`, `action`, `allowed`, a specific code.
- [ ] Idempotency of each action is decided and documented.
- [ ] Preconditions have distinct codes and retry hints where waiting is the remedy.
- [ ] State transitions are version-checked; terminal states have no exits.

## Related

- [Access, Duplicates, Quota, and Entitlements](./04-access-duplicates-quota-entitlements.md)
- [Outcome Modeling and Contracts](./05-outcome-modeling-and-contracts.md)
- [Entitlement, Lifecycle, and Webhook Examples](../03-practical-examples/02-entitlement-lifecycle-and-webhooks.md)
- [Chapter 40 — Consistency and Concurrency Failures](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
