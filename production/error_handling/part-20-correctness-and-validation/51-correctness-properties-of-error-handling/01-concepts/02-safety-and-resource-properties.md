# Safety, Resources, and Side Effects (51.5–51.9)

> Part XX · Chapter 51 · Sections 51.5–51.9 · _Estimated reading time: 24 min_
> **Prerequisite:** [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md), [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)

## In one sentence

Five properties make failure **safe to survive**: nothing sensitive escapes, retries stop, resources
are released, invariants still hold, and no effect happens twice.

## Why this matters in production

These five properties describe what happens *after* the error handling itself is correct. A system
can classify errors perfectly and still be unsafe:

- **Leaking** a stack trace or a card number to a customer is a security incident (51.5).
- A **retry loop with no ceiling** turns a 30-second Stripe outage into a 4-hour stampede that
  takes down your database too (51.6).
- A **connection never returned to the pool** turns one failed request into a pool exhaustion 200
  requests later (51.7).
- **Broken invariants** after a partial failure are silent — no error is raised, so nothing appears
  in your dashboards (51.8).
- **A duplicated charge** is reported to the customer as a billing error and refunded manually,
  every single time (51.9).

## Core concept

### 51.5 — No sensitive exposure

The error leaves your process along **three channels**, and each needs its own projection:

```text
   internal error object
          │
          ├──▶ END USER        → public DTO: code + safe message + correlation ID
          ├──▶ THIRD PARTY     → public DTO + HTTP status, no internal codes
          └──▶ LOGS/METRICS    → redacted context allowlist, cause preserved, stack kept
```

The rule: **the public representation is a projection, never the internal object**. Serializing the
error object itself is the leak.

| Channel | Allow | Deny |
| ------- | ----- | ---- |
| End user | Stable error code, human message, correlation ID, field details for validation | Stack traces, SQL, hostnames, vendor payloads, internal IDs, PII, prices of other tenants |
| Third party | Stable error code, HTTP status, documentation URL (not a fabricated link), correlation ID | Internal codes, retry hints that contradict policy, quota internals |
| Logs/metrics | Everything needed to debug, **after redaction** | Secrets, tokens, PAN, raw request bodies, PII beyond the allowlist |

The test that catches almost everything: put a **canary secret** in the error path and assert it
never appears in any output.

### 51.6 — Retries terminate

Every retry mechanism needs **three independent bounds**. Any one alone is insufficient:

| Bound | Prevents | Typical value |
| ----- | -------- | ------------- |
| **Max attempts** | Infinite loop on an instantly-failing call | 3–5 |
| **Elapsed deadline** | Slow failures that never exhaust attempts | ≤ caller deadline, e.g. 10 s of a 30 s budget |
| **Retry budget** | Retry storms when everything fails at once | ≤ 10% of request volume |

Nested retries are the multiplier people forget: 3 × 3 × 3 = **27 attempts** for one logical
operation. **Only one layer owns retries for a given operation** — normally the layer that knows
whether the effect is idempotent.

```ts
// ❌ Unbounded in three ways: no attempt cap, no deadline, no budget.
async function withRetry<T>(fn: () => Promise<T>): Promise<T> {
  for (;;) {
    try { return await fn(); }
    catch (err) { await sleep(100); }      // 100 ms forever, even for a 400
  }
}

// ✅ Bounded on all three axes, and only retries what is retryable.
async function withRetry<T>(fn: () => Promise<T>, policy: RetryPolicy, signal: AbortSignal): Promise<T> {
  let attempt = 0;
  const deadline = Date.now() + policy.totalTimeoutMs;
  while (true) {
    attempt++;
    try {
      return await fn();
    } catch (err) {
      const class_ = classify(err);
      if (!class_.retryable) throw err;                 // permanent → no retry
      if (attempt >= policy.maxAttempts) throw err;      // bound 1: attempts
      if (Date.now() >= deadline) throw err;             // bound 2: deadline
      if (!policy.budget.tryConsume()) throw err;        // bound 3: budget
      await sleep(backoff(attempt, policy));             // exponential + full jitter
    }
  }
}
```

### 51.7 — Cleanup occurs

Cleanup must be **guaranteed on every exit path**: success, failure, timeout, cancellation, panic,
and process termination. The guarantee comes from ownership, not from discipline.

The rule that makes this work: **the code that acquires a resource is the code that releases it**,
ideally in the same lexical scope.

```ts
// ❌ Acquire in one function, release in another: every early return leaks.
async function handle(req: Request) {
  const conn = await pool.connect();
  const row = await conn.query("SELECT ...");
  if (!row) { return null; }        // leak: conn never released
  await conn.query("UPDATE ...");
  conn.release();
}

// ✅ Scope guard: release happens on every path, including cancellation.
async function handle(req: Request) {
  return await using conn = await pool.connect();
  const row = await conn.query("SELECT ...");
  if (!row) return null;            // released automatically
  await conn.query("UPDATE ...");
}   // released here too
```

Three subtleties that cause real leaks:

- **Cleanup that runs but does not complete.** A release that blocks forever holds the resource.
  Give cleanup its own short timeout (e.g. 2 s) and abandon it after that.
- **Cleanup that is not idempotent.** Double-release corrupts pools. Make release idempotent.
- **Cleanup skipped by abrupt termination.** `process.exit()` and OOM kill skip `finally`. Durable
  cleanup belongs in the database (lease expiry), not only in memory.

### 51.8 — Consistency preserved

Consistency has two scopes:

| Scope | Example | Enforced by |
| ----- | ------- | ----------- |
| **Local** | `subscription.status = 'active'` implies a `subscription_entitlements` row exists | Constraints, triggers, invariant assertions |
| **Cross-store** | A charge in Stripe implies an entitlement in Acme **or** a pending compensation | State machine, ledger, reconciliation job |

The property is about **every observable state**, including the ones between steps. A system that is
inconsistent only for 400 ms is still inconsistent — the reconciliation job will eventually notice,
but a customer may act on the inconsistent state.

### 51.9 — No duplicate side effects

With at-least-once delivery (queues, webhooks, client retries), the same operation will arrive more
than once. The property is: **N deliveries produce at most one observable effect.**

Side effects that must be protected: charges, refunds, emails, outbound webhooks, row inserts,
file writes, and — easy to forget — **LLM tool calls** in `AgentRun` that send email or create
tickets.

```sql
-- The protection is a unique constraint, not application logic. Application-level
-- "check then insert" races under concurrency (property 51.13).
ALTER TABLE webhook_events
  ADD CONSTRAINT webhook_events_event_id_uniq UNIQUE (provider, event_id);
```

Mechanisms, in order of strength:

1. **Unique constraint** on a natural key — the ground truth. Racing inserts fail with `23505`,
   which is a *success*, not an error.
2. **Idempotency key** forwarded to the provider (`Idempotency-Key` on Stripe charges).
3. **Dedupe window** keyed by a deterministic operation id (e.g. `sha256(tenant + event_id)`).
4. **Transactional outbox** for "send this event exactly once" claims.

## Worked example — `ExportJob` (Acme SaaS)

`ExportJob` renders a CSV to S3 and emails the customer a link. Four properties bit at once:

```ts
// BEFORE
async function runExport(job: ExportJob) {
  const conn = await pool.connect();                    // 51.7 risk: released manually
  try {
    const rows = await conn.query(`SELECT ... LIMIT $1`, [job.limit]);
    const key = `exports/${job.tenantId}/${job.id}.csv`;
    await s3.put(key, await renderCsv(rows));           // 51.9 risk: retried → duplicate
    await mailer.send(job.email, { link });             // 51.9 risk: retried → duplicate email
    await conn.query(`UPDATE export_jobs SET status='done' WHERE id=$1`, [job.id]);
  } catch (err) {
    log.error(err);                                     // 51.2 risk: no terminal record
    await conn.release();                               // only reached on the success path
  }
}
```

Fixes, one per property:

```ts
async function runExport(job: ExportJob) {
  const outcome = await using conn = await pool.connect();      // 51.7: scope guard
  try {
    const rows = await conn.query(...);
    const key = `exports/${job.tenantId}/${job.id}.csv`;
    await s3.put(key, await renderCsv(rows));                   // 51.9: deterministic key = idempotent
    await mailer.send(job.email, { link }, { idempotencyKey: `export-mail:${job.id}` });
    await conn.query(`UPDATE export_jobs SET status='done' WHERE id=$1`, [job.id]);
  } catch (err) {
    const cls = classify(err);
    await conn.query(                                     // 51.2: record a terminal outcome
      `UPDATE export_jobs SET status=$2, error_code=$3, failed_at=now() WHERE id=$1`,
      [job.id, cls.retryable ? "retrying" : "failed", cls.code]);
    throw err;                                            // 51.2: propagate — the worker decides
  }
}
```

The result: a retried `ExportJob` overwrites the same S3 key and sends exactly one email; a failed
export always lands in a terminal state that the dashboard can show.

## Key data / numbers

- **Public error fields: 4–6** (`code`, `message`, `correlationId`, optional `fieldErrors`,
  optional `supportRef`). Everything else is internal.
- **Retry attempts: 3–5**, exponential base **200 ms–1 s**, cap **30 s**, **full jitter** so retries
  from many instances do not align.
- **Retry budget: ≤ 10%** of request volume (the classic value used by large-scale systems); below
  5% you barely damp a storm, above 20% you are the storm.
- **Cleanup timeout: ~2 s** — long enough to close a socket, short enough not to hold a worker.
- **Idempotency retention**: Stripe `Idempotency-Key` replays for **24 hours**; keep your own
  dedupe record at least as long.
- **Lease TTL > max job runtime + heartbeat interval.** A 60 s heartbeat with a 30 s lease means a
  dead worker's lease expires in 30 s; the inverse (lease < heartbeat) causes duplicate execution.
- **Consistency window**: the shorter the better; treat anything under **1 second** as observable by
  a customer, and design the reconciliation job for the rest.

## Real-world use case — Acme SaaS `Checkout`

Acme's Checkout called Stripe, then wrote the subscription row. Stripe's client library timed out
after **30 seconds** on a slow-but-successful response. The retry policy retried **3 times**, and
Stripe's idempotency key was **not** forwarded, so two of those attempts produced two charges.

Meanwhile the connection to Postgres had been acquired outside the retry scope and was only released
on the success path — after three failed attempts the pool was down to **2 free connections** for
the entire pod, and the pod began returning 500s to every endpoint, not just Checkout.

Three properties, three fixes: forward the `Idempotency-Key` on every attempt (51.9), scope the
connection with `await using` (51.7), and cap the retry deadline at 8 seconds inside a 30-second
request budget (51.6). Duplicate charges went from 3/month to 0; pool-exhaustion incidents went to
zero in the same week.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Retry with attempts + deadline + budget | Predictable, storm-safe | Three knobs to tune | Every remote call |
| Single attempt, fail fast | Cheapest, clearest | User sees transient failures | Cheap, idempotent, non-critical calls |
| Circuit breaker + fallback | Absorbs outages | Needs a fallback worth having | Critical dependency with a real degraded mode |
| Client-side retry only | Server stays simple | Depends on client behaviour | Public APIs with documented retry guidance |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Project a public DTO for outbound errors | Serialize the internal error object |
| Test that a canary secret never appears in output | Trust the redaction helper |
| Bound attempts, deadline, and budget | Retry `while (true)` |
| Retry only classified-transient errors | Retry everything, including 4xx |
| Acquire and release in the same scope | Acquire in one function, release in another |
| Enforce uniqueness in the database | "Check then insert" in application code |
| Make cleanup idempotent and time-bounded | Assume cleanup always completes |

## Common mistakes

- **A retry ceiling with no deadline.** A call that fails after 30 s, three times, exceeds the
  caller's timeout — the caller has already given up while you keep working.
- **Nested retries in two libraries.** The HTTP client retries, the SDK retries, and your handler
  retries. 27 attempts, and nobody can explain why the database saw 27 writes.
- **Redaction that removes the discriminator.** Stripping the vendor error code to "protect" the
  user also removes the only thing that made the error actionable (51.4).
- **Unique constraint treated as a bug.** The second insert returning `23505` is the *system working
  correctly* — the duplicate was prevented.
- **Cleanup after the deadline.** When the request deadline expires, cleanup still runs — but it
  gets a short timeout, not the full request budget.

## Checklist

- [ ] Every outbound error is a projection through an allowlist, not the internal object.
- [ ] A canary-secret test proves no secret reaches any output channel.
- [ ] Every retry loop has an attempt cap, a deadline, and a budget.
- [ ] Exactly one layer owns retries per operation.
- [ ] Every acquired resource is released on success, failure, timeout, and cancellation.
- [ ] Cleanup is idempotent and has its own timeout.
- [ ] Post-failure invariants are asserted, not assumed.
- [ ] Every side effect has a uniqueness mechanism (constraint, idempotency key, or dedupe window).

## Related

- [Determinism and Completeness (51.1–51.4)](./01-determinism-and-completeness.md)
- [Concurrency, Cancellation, and Partial Failures (51.13–51.16)](./04-concurrency-cancellation-and-partial-properties.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
