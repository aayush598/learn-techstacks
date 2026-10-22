# Shared Retry and Recovery Policies

> Part XXI · Chapter 54 · Sections 54.6, 54.7 · _Estimated reading time: 18 min_
> **Prerequisite:** [Mapping Interfaces and Adapters](./02-mapping-interfaces-and-adapters.md)

## In one sentence

Shared retry and recovery policies encode the decisions that **must** be the same everywhere
— and everything else stays with the service, because a policy that varies is a policy
nobody can rely on.

## Why this matters in production

Retry and recovery are where divergence is most expensive, because a divergent retry policy
does not produce a wrong answer — it produces **load**, and the load is amplified exactly
when the system is already struggling.

Three failures follow from unsynchronised policies:

- **Retry storms.** Service A retries 5 times with no jitter, service B retries 3 times with
  jitter. During an outage, the combined amplification is 8×, and the jitter from B is
  destroyed by A.
- **Unequal blast radius.** One service treats a timeout as terminal, another retries it for
  10 minutes. The client sees a `504` from one and a `200` from the other, for the same
  underlying condition.
- **Undocumented policies.** The runbook says "we retry three times". One service does
  three, one does five, one does zero. The runbook is wrong in a way nobody can detect.

The fix is not "one policy for everything". It is a **clear split** between what must be
shared and what is genuinely situational.

## Core concept

### 54.6 — Shared retry policies

A retry policy answers four questions: **how many attempts, how long between them, how long
in total, and what counts as retryable**. The first three are shared. The fourth is derived
from the category, which is also shared.

```ts
export const RETRY_POLICIES: Partial<Record<ErrorCategory, RetryPolicy>> = {
  external_api_transient: {
    maxAttempts: 3, baseDelayMs: 250, maxDelayMs: 4_000,
    jitter: true, totalDeadlineMs: 10_000, honourRetryAfter: true,
  },
  database_transient: {
    maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1_000,
    jitter: true, totalDeadlineMs: 5_000, honourRetryAfter: false,
  },
  dependency_unavailable: {
    maxAttempts: 2, baseDelayMs: 500, maxDelayMs: 2_000,
    jitter: true, totalDeadlineMs: 6_000, honourRetryAfter: true,
  },
  rate_limit: {
    maxAttempts: 2, baseDelayMs: 1_000, maxDelayMs: 5_000,
    jitter: true, totalDeadlineMs: 15_000, honourRetryAfter: true,
  },
};
```

The design rules:

| Rule | Value | Reason |
| ---- | ----- | ------ |
| **Attempts are bounded** | ≤ **5**, ≤ **3** for interactive requests | Prevents amplification |
| **Delays grow** | exponential from `baseDelayMs`, capped at `maxDelayMs` | Gives the dependency room to recover |
| **Jitter is on** | full jitter, on every policy | Breaks synchronised retries |
| **A total deadline exists** | ≤ the caller's remaining budget | Bounds the latency cost |
| **`Retry-After` is honoured** | but only if it fits the remaining budget | Obeys the server without hanging |
| **A non-idempotent operation never retries** | the policy is skipped, not shortened | Prevents duplicate effects |

The last rule is the one that is usually missing, and it is the dangerous one. The shared
policy says "3 attempts"; the *operation* says "I am not idempotent". The shared retry
helper must therefore take the operation's idempotency as an input:

```ts
export function decideRetry(ctx: RetryContext, policy: RetryPolicy): "retry" | "stop" {
  if (!policy.retryOn.includes(ctx.category)) return "stop";
  if (!ctx.idempotent) return "stop";                 // ← the operation decides
  if (ctx.remainingMs <= policy.baseDelayMs) return "stop";
  if (policy.honourRetryAfter && ctx.serverHintMs !== undefined) {
    if (ctx.serverHintMs > ctx.remainingMs) return "stop";
  }
  return "retry";
}
```

### What stays in the service

| Policy aspect | Shared? | Why |
| ------------- | ------- | --- |
| Attempts, delay, deadline, jitter | **Yes** | Must not vary, or the load varies |
| Which categories are retryable | **Yes** | It is the category's meaning |
| Whether *this operation* is idempotent | **No** | It is a property of the operation |
| The **context** of the retry (attempt number, elapsed) | **No** | It is per call |
| A service-specific override for a **critical** dependency | **No** | Situational |

The last row is the escape hatch, and it needs a rule. Acme's rule: **an override is allowed
only if it is stricter than the shared policy** (fewer attempts, shorter deadline), unless
an ADR says otherwise. A service that wants *more* retries than the shared policy must
argue for it explicitly, because loosening a retry policy is a global decision.

### 54.7 — Common recovery policies

**Recovery** is the decision of what the system does *about* the failure, as opposed to
retry, which is the decision of *how many times to try again*. The shared recovery table is
keyed by category:

```ts
export const RECOVERY_POLICIES: Record<ErrorCategory, RecoveryPolicy> = {
  validation:             { action: "fail" },
  business:               { action: "fail" },
  conflict:               { action: "fail" },
  auth:                   { action: "fail" },
  not_found:              { action: "fail" },
  external_api_permanent: { action: "fail" },
  external_api_transient: { action: "retry" },
  external_api_ambiguous: { action: "resolve_later" },
  database_transient:     { action: "retry" },
  data_integrity:         { action: "terminate" },
  dependency_unavailable: { action: "degrade" },
  resource_exhausted:     { action: "degrade" },
  rate_limit:             { action: "fail" },
  cancellation:           { action: "fail" },
  internal:               { action: "fail" },
};
```

The six actions, and what each one obliges you to do:

| Action | Meaning | Obligation |
| ------ | ------- | ----------- |
| `fail` | Stop and report the failure | The failure must reach a boundary and produce a contract response |
| `retry` | Try again under the retry policy | The operation must be idempotent, or explicitly not |
| `degrade` | Continue with reduced functionality | The degraded state must be *visible* to the caller, not silent |
| `compensate` | Undo a completed effect | The compensation must be idempotent and must not run before settlement |
| `terminate` | Stop the process | The state must be safe; the process must be restarted by the supervisor |
| `resolve_later` | The outcome is unknown; reconcile later | A read-back must be scheduled, and "not found" must alert, not succeed |

Two of these are easy to get wrong:

- **`degrade` must be visible.** A degraded result that looks like a normal result is a
  correctness bug (Chapter 30). The shared helper returns a `degraded` flag for exactly this
  reason.
- **`resolve_later` must not become "succeed".** The reconciliation finding no record is an
  **alert**, not a success. This is the failure that loses money.

### The split, in one table

| Question | Owner | Shared? |
| -------- | ----- | ------- |
| Is this category retryable? | core (category table) | yes |
| How many attempts, what delay, what deadline? | core (retry policy table) | yes |
| Is *this operation* safe to repeat? | the operation | no |
| What happens when retries are exhausted? | core (recovery table) | yes |
| What is the fallback value for a degraded feature? | the feature | no |
| When is a compensation scheduled? | the workflow | no |
| What does the caller see? | core (category table) | yes |

The pattern: **the shared package owns the decisions about *failures as a category*; the
service owns the decisions about *its own workflow*.**

## How it works (mechanics)

The retry helper in the package, with the service supplying only the operation:

```ts
export async function withRetry<T>(
  operation: () => Promise<T>,
  ctx: { category: ErrorCategory; idempotent: boolean; remainingMs: number; serverHintMs?: number },
): Promise<T> {
  const policy = RETRY_POLICIES[ctx.category] ?? NO_RETRY;
  let attempt = 0;
  let lastError: unknown;

  while (attempt < policy.maxAttempts) {
    attempt += 1;
    try {
      return await operation();
    } catch (err) {
      lastError = err;
      if (decideRetry(ctx, policy) === "stop") break;
      await sleep(backoffDelay(policy, attempt));
    }
  }
  throw lastError;   // the final failure preserves the original error
}
```

The **final failure preserves the original error**. A retry helper that throws a generic
"retries exhausted" error destroys the information the operator needs. If the last attempt
failed with a provider error, that is what the operator should see, with the attempt count
attached as context.

## Worked example

Acme's `ExportJob` writer against S3. The service-specific part and the shared part, side
by side:

```ts
// The service owns: which operation, whether it is idempotent, what the deadline is.
export async function writeExportPart(job: ExportJob, rows: Row[]): Promise<WriteResult> {
  return withRetry(
    () => s3.putObject({ key: job.partKey, body: encode(rows) }),
    {
      category: "external_api_transient",
      idempotent: true,                 // same key + same body ⇒ same object
      remainingMs: job.deadlineMs - Date.now(),
    },
  );
}
```

What the shared package contributed that the service would not have:

- **The attempt ceiling (3)** and the **exponential backoff with full jitter** (250 ms →
  4 s cap).
- **The 10-second total deadline**, checked against the job's remaining budget, so a slow
  S3 does not consume the whole job window.
- **The exhaustion behaviour**: the last error is rethrown, with `attempts: 3` in its
  context, so the DLQ record says how hard it tried.
- **`Retry-After` handling**: when S3 returns `503` with a `Retry-After: 2`, the helper
  waits 2 s — but only if 2 s fits inside the remaining budget.

What stayed in the service: the key format (which makes the write idempotent), the job's
deadline, and the decision that a failed part write is a `job_transient` category rather
than a fatal one.

The measurable result: during a **23-minute S3 degradation** in one quarter, the export
workers made **3.1 attempts** per failing write instead of an unbounded number, and the
provider's rate limiter did not trip. The exports that failed went to the DLQ with
`attempts: 3` recorded, and the replay after recovery succeeded.

## Key data / numbers

- **Shared policy fields: 6** (attempts, base delay, max delay, jitter, deadline, honour
  `Retry-After`).
- **Attempt ceilings:** ≤ **5** in general; **3** for interactive requests; **2** for
  `dependency_unavailable` and `rate_limit`.
- **Base delays:** 100 ms (database) to 1,000 ms (rate limit). **Max delay:** 1–5 s for
  interactive; up to 300 s for background jobs.
- **Total deadline:** ≤ the caller's remaining budget, always; ≤ **10 s** for external APIs
  in the shared policy.
- **Jitter:** full jitter, on every shared policy.
- **Retry budget:** ≤ **10%** of a service's request volume may be retries.
- **Recovery actions: 6** (`fail`, `retry`, `degrade`, `compensate`, `terminate`,
  `resolve_later`).
- **Category → recovery table: 15 rows, total.** Every category has exactly one recovery.
- **Service override rule:** an override must be **stricter** than the shared policy unless
  an ADR says otherwise.
- **Measured:** the S3 degradation produced **3.1 attempts** per failing write (was unbounded
  in the previous incident, which lasted **61 minutes** and produced **412,000** failed
  requests).
- **Exhaustion behaviour:** the original error is rethrown with `attempts` in context —
  **never** replaced with a generic "retries exhausted" error.

## Real-world use case — Acme SaaS, the retry that ate the provider

During a Stripe incident, Acme's Checkout service made **~9 requests per customer attempt**
instead of 3. The cause was not Stripe's behaviour; it was Acme's:

- The checkout service retried a declined-card error **3 times**, because the category
  mapping for one provider error was `external_api_transient` instead of
  `external_api_permanent`. **Every card decline was retried 3 times.**
- The Stripe client library also had its own built-in retry (2 attempts), because nobody had
  told it not to.
- The API gateway retried `5xx` responses once more.

**Multiplicative amplification: 3 × 2 × 2 = 12 requests per card decline.** During the
incident, Stripe's rate limiter tripped and the checkout success rate fell to **58%** for
**11 minutes**, even though Stripe itself was healthy — the outage was self-inflicted.

The fix used the shared package in three parts:

1. The category mapping moved into the shared adapter, so a card decline is
   `external_api_permanent` **everywhere**, and the shared policy does not retry it.
2. The client library's built-in retry was **disabled** in the adapter, with the shared
   policy as the only retry layer — one owner, no multiplication.
3. The gateway's `5xx` retry was reduced to a single attempt for a specific, documented
   reason, and the shared policy's `503` response tells the client when a retry is
   appropriate.

The rule that came out of it, and that went into the package:

> **Exactly one retry layer per dependency, per request.** The layer is the adapter. The
> shared policy is the only source of the decision, and any client-library retry is
> disabled.

After the change, the same kind of incident produced a **6%** dip for **90 seconds** instead
of a **42%** dip for **11 minutes**.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fully shared policies | One behaviour everywhere | Cannot fit a special dependency | The default; override only with an ADR |
| Fully local policies | Fits each service | Diverges; storm risk | Never |
| Shared defaults + strict local overrides | Fits, and stays safe | Needs a rule for "stricter only" | The recommended middle |
| A configurable policy engine | Maximum flexibility | Configuration surface; framework smell | Only with a dedicated owner and a real need |
| Retry owned by the transport (gateway) | Invisible to the app | Amplifies and hides; multiplies | No |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Have exactly one retry layer per dependency | Stack the app retry, the SDK retry, and the gateway retry |
| Bound attempts *and* elapsed time | Bound only attempts, or only elapsed time |
| Honour `Retry-After` within the budget | Honour `Retry-After` blindly and blow the deadline |
| Re-throw the original error after exhaustion | Replace it with a generic "retries exhausted" error |
| Let a service override only to be stricter | Let a service loosen a shared policy without an ADR |
| Mark degraded results as degraded | Degrade silently |
| Alert when a `resolve_later` reconciliation finds nothing | Treat "not found" as success |

## Common mistakes

- **The retry sandwich.** An app-level retry wrapping an SDK retry wrapping a gateway
  retry. This is the single most common cause of self-inflicted outages.
- **The permanent error classified as transient.** One mapping mistake multiplies every
  request for that error.
- **The unbounded deadline.** A retry policy with no total deadline can outlive the request
  that started it.
- **The generic exhaustion error.** It destroys the cause, so the operator cannot tell a
  card decline from a provider outage.
- **The "we will decide at the call site" deferral.** The call site is where the policies
  diverge.

## Checklist

- [ ] Every category has exactly one retry policy and one recovery action.
- [ ] Every policy has an attempt ceiling and a total deadline.
- [ ] Jitter is on in every shared policy.
- [ ] Non-idempotent operations are excluded from retrying.
- [ ] There is exactly one retry layer per dependency.
- [ ] The original error survives retry exhaustion.
- [ ] Overrides are stricter than the shared policy, or covered by an ADR.

## Related

- [Mapping Interfaces and Adapters](./02-mapping-interfaces-and-adapters.md)
- [Reusable API and Job Handling](./04-reusable-api-and-job-handling.md)
- [Chapter 27 — Retry Policies](../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
