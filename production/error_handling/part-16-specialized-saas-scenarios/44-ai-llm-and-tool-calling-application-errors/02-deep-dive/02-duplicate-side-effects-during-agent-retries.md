# Duplicate Side Effects During Agent Retries

> Part XVI · Chapter 44 · Sections 44.12, 44.19 · _Estimated reading time: 26 min_
> **Prerequisite:** [Retry Safety and Nondeterminism](./01-retry-safety-and-nondeterminism.md)

## In one sentence

A duplicate side effect happens when **the same business operation is applied twice** — and
the only reliable defense is a **write-ahead effect ledger** keyed by an operation-derived
idempotency key.

## Why this matters in production

Duplicates are the class of AI bug that produces a customer-facing consequence: two
invoices, two emails, two refunds, two rows, two webhook deliveries. Unlike a wrong
answer, a duplicate is a **mutation of the customer's world**, and it is often discovered
by the customer rather than by you.

They are also the hardest to detect. The second execution looks exactly like the first.
Nothing throws. No log line says "duplicate". The only evidence is a count that should be
one and is two — which you will usually find in a reconciliation report weeks later.

## The anatomy of a duplicate

```text
  t0  model → call tool "create_refund(order=O, amount=50)"  args = {order:"O", amount:50}
  t1  key = hash(run_id=R, tool="create_refund", canonical_args)
  t2  ledger: INSERT (key) → claimed
  t3  effect: stripe.refunds.create(...) → refund id r_123      ← THE EFFECT
  t4  ledger: UPDATE (key) SET result = {...}                   ← never reached
  t5  provider call times out — the loop sees a 504              ← AMBIGUOUS
  t6  retry: model → call tool "create_refund(order=O, amount=50)"  args = {order:"O", amount:500}
  t7  key = hash(run_id=R, tool="create_refund", canonical_args)   ← DIFFERENT (amount changed)
  t8  ledger: INSERT (key) → claimed (no conflict!)
  t9  effect: stripe.refunds.create(...) → refund id r_124      ← DUPLICATE
```

Two failure modes hide in that trace:

1. **The key changed** (t6→t7). The model produced a slightly different argument, so the
   key differs and the ledger does not catch the duplicate. This is the hard case.
2. **The result was not recorded** (t3→t4). The effect happened but the ledger has no
   result, so a retry of the *same* key must re-execute or return an unknown.

## The effect ledger

```sql
CREATE TABLE tool_effect (
  idempotency_key TEXT PRIMARY KEY,
  run_id         TEXT NOT NULL,
  tool_name      TEXT NOT NULL,
  args_hash      TEXT NOT NULL,
  status         TEXT NOT NULL,          -- claimed | applied | failed
  result         JSONB,                   -- the result to return on replay
  created_at     TIMESTAMPTZ NOT NULL,
  applied_at     TIMESTAMPTZ,
  expires_at     TIMESTAMPTZ NOT NULL
);
CREATE INDEX tool_effect_run ON tool_effect (run_id, created_at);
```

The ledger has exactly three jobs:

1. **Claim** the operation before performing it (write-ahead).
2. **Record** the result so a replay returns it instead of re-executing.
3. **Expire** so the table does not grow forever.

### Claim, act, record

```ts
export async function applyEffect<T>(
  key: string, runId: string, toolName: string, args: unknown, fn: () => Promise<T>,
): Promise<{ replayed: boolean; value: T }> {
  const argsHash = sha256(canonicalJson(args));

  // 1. CLAIM — atomic, and the only place a duplicate can be stopped.
  const claimed = await db.query(
    `INSERT INTO tool_effect (idempotency_key, run_id, tool_name, args_hash, status, expires_at)
     VALUES ($1, $2, $3, $4, 'claimed', now() + interval '7 days')
     ON CONFLICT (idempotency_key) DO NOTHING
     RETURNING idempotency_key`,
    [key, runId, toolName, argsHash]);

  if (claimed.rowCount === 0) {
    // Someone already claimed this key. Replay their result, or report "in progress".
    const existing = await db.get(`SELECT status, result FROM tool_effect
                                   WHERE idempotency_key = $1`, [key]);
    if (existing.status === "applied") {
      return { replayed: true, value: existing.result as T };
    }
    if (existing.status === "claimed") {
      // A previous attempt claimed it and then died. The effect may or may not exist.
      throw new AppError("TOOL_EFFECT_IN_FLIGHT", { key });
    }
    // status = failed → the previous attempt failed before applying; safe to re-claim.
    await db.query(`UPDATE tool_effect SET status = 'claimed' WHERE idempotency_key = $1`, [key]);
  }

  // 2. ACT — the side effect, exactly once per key.
  try {
    const value = await fn();
    // 3. RECORD — so a replay returns this instead of repeating the effect.
    await db.query(
      `UPDATE tool_effect SET status = 'applied', result = $2, applied_at = now()
       WHERE idempotency_key = $1`, [key, JSON.stringify(value)]);
    return { replayed: false, value };
  } catch (err) {
    await db.query(`UPDATE tool_effect SET status = 'failed' WHERE idempotency_key = $1`, [key]);
    throw err;
  }
}
```

**Key data:** the claim is a **single atomic `INSERT ... ON CONFLICT DO NOTHING`**, not a
read-then-write. Two workers racing on the same key must produce exactly one winner; a
`SELECT` followed by an `INSERT` produces two.

## Deriving the key

The key must identify the **business operation**, not the request.

```ts
/** Canonical JSON: sorted keys, stable number formatting, no whitespace. */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  const entries = Object.entries(value as Record<string, unknown>)
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
  return `{${entries.map(([k, v]) => `${JSON.stringify(k)}:${canonicalJson(v)}`).join(",")}}`;
}

export function effectKey(runId: string, toolName: string, args: unknown): string {
  return sha256(`${runId}|${toolName}|${canonicalJson(args)}`);
}
```

**Key data:** canonicalization must sort object keys — `{a:1,b:2}` and `{b:2,a:1}` must
hash identically — and must not include whitespace. Array order is significant and must
**not** be sorted: `["a","b"]` and `["b","a"]` are different arguments.

### The argument-drift problem

The trace above showed a retry with `amount: 500` against an original `amount: 50`. A key
derived from the arguments cannot catch that. Options, in increasing order of strength:

| Strategy | Catches | Cost |
| -------- | ------- | ---- |
| Key from arguments | Exact repeats | Free |
| Key from a **stable subset** of arguments (the operation id) | Same operation, different detail | Requires the tool to expose an operation id |
| Key from the **plan**, frozen at planning time | Any re-plan | Requires a frozen plan |
| Key from a **server-issued operation id** | Everything | The API must allocate the id |

The strongest design: **the operation id comes from your side**. When the model asks to
refund order O, your tool maps that to a refund operation with an id you allocate
(`refund:{orderId}:{attemptWithinOrder}`), and *that* is the key. The model's argument
drift then cannot change the key.

> ⚠️ **Hazard.** Do not derive the key from the **model's run id** alone. If the user
> retries the whole conversation as a new run, the run id changes and the key changes, so
> the second run duplicates the first. Business-operation keys must be stable across runs
> that mean the same business thing.

**Key data:** the key should be stable across **re-runs of the same business request**.
A practical shape is `{tenantId}:{operationType}:{businessObjectId}` — for a refund,
`acme:refund:order_123`. Include the amount only when multiple partial operations against
one object are legitimate.

## Concurrency: two workers, one key

Sometimes the duplicate comes from parallelism, not from a retry: two agent workers
process the same task, or a queue redelivers while the first copy is still running.

```ts
// A claimed-but-unfinished key blocks the second worker instead of duplicating the effect.
const inFlight = await db.get(
  `SELECT created_at FROM tool_effect WHERE idempotency_key = $1 AND status = 'claimed'`, [key]);
if (inFlight && Date.now() - new Date(inFlight.created_at).getTime() < STALE_CLAIM_MS) {
  throw new AppError("TOOL_EFFECT_IN_FLIGHT", { key });
}
```

**Key data:** a claim is *stale* after **5 minutes** (tune to your tool's p99 duration).
After that, a second worker may reclaim it — which is safe **only** if the effect is
itself idempotent at the downstream provider (a refund keyed by `orderId`, a message with
a `client_token`). Otherwise a stale claim means an unknown outcome, and you reconcile
before retrying.

## Compensation when idempotency is impossible

Some effects cannot be keyed — you cannot refund a payment with the same key twice if the
provider does not support it, and you cannot un-send an email. For those, compensate:

```ts
export type SagaStep =
  | { kind: "effect"; name: string; undo?: () => Promise<void> }
  | { kind: "compensate"; name: string; forward: () => Promise<void> };

export async function runSaga(steps: SagaStep[]): Promise<void> {
  const done: SagaStep[] = [];
  try {
    for (const step of steps) { await step.forward(); done.push(step); }
  } catch (err) {
    for (const step of done.reverse()) {
      if (step.kind === "effect" && step.undo) {
        await step.undo().catch(() => undefined);   // best effort; log failures
      }
    }
    throw err;
  }
}
```

**Key data:** compensation is a **best-effort, ordered, reverse** rollback — it is not
atomic and it can fail. Use it only when the downstream provider cannot dedupe; when it
can, prefer the idempotency key, because a key cannot fail halfway.

## Finding duplicates after the fact

Even with all of the above, some duplicates get through — especially via argument drift.
You need a detector:

```sql
-- Refunds created for the same order on the same day.
SELECT order_id, count(*), array_agg(provider_refund_id ORDER BY created_at)
FROM refund_effect
WHERE created_at > now() - interval '1 day'
GROUP BY order_id
HAVING count(*) > 1;
```

The metric that proves the ledger works:

```text
tool_effect_replay_suppressed_total{tool="create_refund"}  147
tool_effect_duplicate_suspected_total{tool="create_refund"}  2
```

**Key data:** alert when `duplicate_suspected` is non-zero, and keep the replay counter
per tool — a sudden jump in suppressed replays usually means a retry storm, and a sudden
jump in suspected duplicates usually means a key derivation bug.

## Partial completion and the ledger

The ledger is what makes a **partial run** resumable. Because every applied effect is
recorded with its result, a resumed run can:

1. Read the run's recorded effects.
2. Replay their results into the transcript **instead of re-executing them**.
3. Continue from the first step with no recorded effect.

```ts
export async function resumeRun(runId: string): Promise<AgentRunResult> {
  const effects = await db.query(
    `SELECT tool_name, args_hash, result FROM tool_effect
     WHERE run_id = $1 AND status = 'applied' ORDER BY applied_at`, [runId]);
  const replay = new Map(effects.map((e) => [e.args_hash, e.result]));
  // Rebuild the transcript with the recorded results, then continue the loop.
  return continueRun(runId, { replay });
}
```

**Key data:** a resumed run **must not** re-plan from step 1 (see the freeze boundary in
the retry deep dive). It replays the recorded effects and continues. Without the ledger,
a resumed run has no memory of what it already did.

## Worked example — the refund agent

Acme's `AgentRun` agent can issue refunds. The first implementation called the payments
service directly, and a provider 503 after the refund succeeded produced a second refund
of the same amount. The customer was refunded twice; the second refund was caught by a
downstream reconciliation eight days later.

The rebuild put a ledger in front of the payment call:

- The key is `sha256("acme:refund:" + orderId)` — derived from the **business object**,
  not from the model's arguments, so a re-plan with `amount: 50` vs `amount: 500` cannot
  create a second key.
- The claim is an atomic `INSERT ... ON CONFLICT DO NOTHING`.
- The result (the provider's refund id) is recorded, so a replay returns it.
- The payments service receives its own idempotency key, so even a stale-claim reclaim
  cannot double-refund.
- A daily query groups refunds by order and raises a ticket for any count above one.

After the rebuild, two provider outages in the following month produced four suppressed
replays and zero duplicate refunds. The `tool_effect_replay_suppressed_total` counter
also became the team's early warning for retry storms.

## Key data

| Fact | Value |
| ---- | ----- |
| Ledger claim | Atomic `INSERT ... ON CONFLICT DO NOTHING` |
| Ledger states | `claimed` → `applied` \| `failed` |
| Key derivation | Business operation, not the request: `{tenant}:{opType}:{objectId}` |
| Canonicalization | Sorted object keys, no whitespace; array order preserved |
| Ledger TTL | 7 days (longer than any retry window) |
| Stale claim threshold | ~5 minutes (tune to the tool's p99 duration) |
| Downstream provider | Must also accept an idempotency key |
| Compensation | Ordered reverse rollback, best effort, not atomic |
| Detectors | Group by business object; alert on count > 1 |
| Metrics | `replay_suppressed`, `duplicate_suspected` per tool |

## Real-world use case

A multi-tenant SaaS lets an AI agent issue refunds and send apology emails. In the first
month the agent refunded a customer twice after a provider timeout — the money was
returned, then returned again, and the customer received two apology emails.

The team built the effect ledger and moved the key derivation out of the model's hands.
The agent's `refund` tool takes an `order_id`; the tool maps that to a refund operation
whose key is `sha256("acme:refund:{orderId}")`. The model's argument drift no longer
matters, because the key never depends on the amount or the phrasing.

The second fix was making the payments provider itself idempotent: the refund request
carries the same key, so even if a stale claim is reclaimed after five minutes, the
provider returns the original refund instead of creating a second one. The team's daily
reconciliation query now finds zero duplicates, and the replay counter is wired to a
dashboard — a spike in suppressed replays is now their first signal that a provider is
degrading.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Retry freely | Simple | Duplicates effects | Only for read-only tools |
| Ledger with argument-derived key | Catches exact repeats | Misses argument drift | Read-mostly tools |
| Ledger with operation-derived key | Survives argument drift | Needs an operation id | ✅ Write tools |
| Provider-side idempotency key | Strongest | Needs provider support | ✅ Where available |
| Compensation | Works without provider support | Best effort, can fail | Last resort |
| Lock the run (no concurrency) | Simple | Throughput loss | Single-worker agents |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Claim the operation **before** applying it | Apply, then check |
| Use an atomic `INSERT ... ON CONFLICT` | `SELECT` then `INSERT` |
| Derive the key from the business operation | Derive it from the model's arguments |
| Record the result so a replay returns it | Record only "done" |
| Canonicalize args (sorted keys) | Hash the raw JSON string |
| Pass an idempotency key to the downstream provider too | Rely on your ledger alone |
| Reconcile by business object | Reconcile by request id |
| Alert on suspected duplicates | Discover them from customers |
| Freeze the plan when resuming a run | Re-plan from step 1 |

## Common mistakes

- **Hashing the raw arguments string.** `{a:1,b:2}` and `{b:2,a:1}` produce different keys.
- **Keying on the run id.** A user retry starts a new run and duplicates everything.
- **Checking after the effect.** Too late to prevent anything.
- **Recording "done" without the result.** A replay cannot return what it needs.
- **Relying on the ledger alone.** A stale-claim reclaim still duplicates without a
  downstream idempotency key.
- **Compensating instead of keying.** Compensation can fail halfway.
- **No detector.** You need to know how many duplicates got through.

## Checklist

- [ ] Every write effect is claimed in a ledger before it is applied.
- [ ] The claim is a single atomic insert with conflict handling.
- [ ] The result is recorded so a replay returns it.
- [ ] Keys are derived from the business operation and are stable across runs.
- [ ] Arguments are canonicalized before hashing.
- [ ] The downstream provider receives an idempotency key as well.
- [ ] Ledger entries expire, and the TTL exceeds the retry window.
- [ ] Stale claims have a documented threshold and a defined outcome.
- [ ] A reconciliation query detects duplicates by business object.
- [ ] Replay and duplicate-suspected metrics exist per tool.

## Related

- [Retry Safety and Nondeterminism](./01-retry-safety-and-nondeterminism.md)
- [Tool-Calling Failures](../01-concepts/03-tool-calling-failures.md)
- [Chapter 28 — Idempotency and Duplicate Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
