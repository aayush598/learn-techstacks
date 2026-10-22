# The Same Matrix, Different Answers: `ExportJob` and `AgentRun`

> Part XXII · Chapter 56 · Sections 56.1–56.18 (applied) · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 56 README](../README.md), [Checkout Decision Walkthrough](./01-checkout-decision-walkthrough.md)

## In one sentence

The **rubric generalizes, the answers do not**: the same 18 pairs produce a *retry-and-DLQ*
design for `ExportJob` and a *degrade-and-retry* design for `AgentRun`, because the tiers,
the callers, and the boundaries are different.

## Why this matters in production

Teams that learn one design and apply it everywhere produce two failure modes:

- A background job treated like a request — retried in-process forever, holding a worker,
  and never reaching the DLQ.
- An AI feature treated like a critical dependency — every summary failure becomes an error
  page, and a provider rate limit becomes an outage.

Showing the same matrix applied to two very different flows demonstrates that the matrix
produces *different answers* when the inputs differ. That is the whole point of a rubric: it
constrains the reasoning, not the result.

## The matrix

| Subsection | `Checkout` (T3, synchronous, money) | `ExportJob` (T2, deferred, long-running) | `AgentRun` (T1–T3, synchronous-ish, nondeterministic) |
| ----------- | --------------------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| 56.1 exceptions vs results | Result (8 enumerable failures) | Result + job state machine | Result (typed union per step) |
| 56.2 centralized vs local | Registry shared, fallback local | Registry shared, DLQ policy shared | Registry shared, degrade local |
| 56.3 global vs domain | `CheckoutError` | `ExportError` | `AgentRunError` |
| 56.4 fail-fast vs degrade | Fail fast (charge), degrade (email) | Fail fast (job), never degrade the file | Degrade (summary), fail fast (tool write) |
| 56.5 retry vs immediate | Retry only with idempotency key | Retry in the worker with backoff | Retry `429`/`503`; never retry schema errors |
| 56.6 retry vs compensation | Compensate on completed charge | Compensate the S3 object if the record write fails | Compensate a partial tool write |
| 56.7 throwing vs returning | Domain returns, adapter throws | Worker throws, runner catches | Adapter throws, loop returns |
| 56.8 wrapping vs preserving | Preserve `req_9f2…` | Preserve the S3 request ID | Preserve the provider `request_id` |
| 56.9 generic vs specific | Specific codes per decline reason | Specific codes per stage | Specific codes per failure mode |
| 56.10 inheritance vs composition | Composition (code union) | Composition | Composition |
| 56.11 universal vs bounded | Bounded tree | Bounded tree | Bounded tree |
| 56.12 shared vs feature | Feature-owned codes | Feature-owned codes | Feature-owned codes |
| 56.13 strict vs permissive | Strict on the request body | Strict on the job payload | Strict on tool args, permissive on model output |
| 56.14 aggregation vs first-error | Aggregate field errors; fail fast between steps | Aggregate per-row failures; fail fast between stages | Aggregate tool errors per step |
| 56.15 sync vs deferred | Checkout sync; email deferred | Fully deferred | Sync for the run, deferred for the summary cache |
| 56.16 local recovery vs termination | Recover locally | Recover locally; terminate the worker on corruption | Recover locally; terminate on a corrupted transcript |
| 56.17 abstraction vs indirection | Registry shared, no framework | Named retry policy shared | Provider adapter shared, model-agnostic |
| 56.18 policies by business risk | T3 money | T2 workflow | T1 summary, T3 tool write |

The three columns differ in **every** row that matters, and the differences are all
traceable to three inputs: tier, caller, and boundary.

## `ExportJob` — deferred, long-running, bounded by a queue

### The controlling facts

| Fact | Consequence |
| ---- | ----------- |
| The caller is a **job runner**, not a user | Recovery can be deferred (56.15) |
| The job runs for **minutes** | Per-request timeouts do not apply; per-stage budgets do |
| The output is a **file**, not a value | The file is the effect; the completion record is the truth |
| The job is **retryable** because the object key is deterministic | Retrying is safe (56.5) |
| A partial file is **useless** | The S3 object must be written atomically |

### The shape

```ts
export type ExportJobState =
  | "pending"
  | "snapshotting"
  | "generating"
  | "uploading"
  | "recording"
  | "completed"
  | "failed"
  | "dead_lettered";

export type ExportError =
  | { code: "EXPORT_SUBSCRIPTION_INACTIVE"; stage: "snapshotting"; retryable: false }
  | { code: "EXPORT_QUERY_TOO_LARGE"; stage: "snapshotting"; retryable: false }
  | { code: "EXPORT_DB_TRANSIENT"; stage: "snapshotting"; retryable: true }
  | { code: "EXPORT_MEMORY_EXHAUSTED"; stage: "generating"; retryable: false }
  | { code: "EXPORT_S3_UNAVAILABLE"; stage: "uploading"; retryable: true }
  | { code: "EXPORT_S3_WRITE_FAILED"; stage: "uploading"; retryable: true }
  | { code: "EXPORT_RECORD_WRITE_FAILED"; stage: "recording"; retryable: true };
```

Note `EXPORT_S3_WRITE_FAILED` is retryable and `EXPORT_RECORD_WRITE_FAILED` is also
retryable — but the two differ in their **compensation** behavior (see below), which is
exactly the kind of subtlety the matrix exists to surface.

### Compensation for the awkward stage

The hard case is the last stage: the file is in S3, but the "job completed" record was not
written. The customer-facing truth (the record) and the physical artifact (the file) have
disagreed.

Two valid designs, with different tiers:

| Design | Behaviour | Consequence |
| ------ | --------- | ----------- |
| **Compensate** | Delete the S3 object, fail the job, let the job retry cleanly | Wastes the upload; the next attempt re-uploads the same bytes under the same key |
| **Reconcile** | Keep the object, retry only the record write | Faster; needs a deterministic key so the retry is idempotent |

Acme chose **reconcile** for the record write (the object key is
`exports/{tenantId}/{jobId}.csv`, and the record write is an upsert on `jobId`), because the
record write is T3 (it is the customer-visible truth) while the object is T2 (a stale extra
file is a nuisance). Deleting the object would have been a T3 action (destroying the
artifact) driven by a T2 problem — an inversion the tier matrix prevents.

```ts
// ✅ The record write is idempotent and retryable on its own.
const written = await storage.putObject(key, bytes, { contentType: "text/csv" });
if (!written.ok) throw new ExportError({ code: "EXPORT_S3_WRITE_FAILED", stage: "uploading", retryable: true });

const recorded = await jobs.markCompleted(job.id, { key, bytes: written.value.size });
if (!recorded.ok) {
  // Do NOT delete the object: the key is deterministic, so the next attempt
  // overwrites it and the record write is an idempotent upsert.
  throw new ExportError({ code: "EXPORT_RECORD_WRITE_FAILED", stage: "recording", retryable: true });
}
```

### Retry and DLQ policy

| Stage | Attempts | Backoff | Notes |
| ----- | -------- | ------- | ----- |
| Snapshot | 3 | exponential + jitter | Re-read with a smaller window on the 3rd attempt |
| Generate | 2 | fixed 30 s | Re-running costs CPU; fail fast to the DLQ after 2 |
| Upload | 5 | exponential + jitter | S3 `503 Slow Down` → honor `Retry-After` |
| Record | 3 | exponential + jitter | Upsert is idempotent |

After 5 failed attempts on the upload stage, the job goes to the **DLQ** with the preserved
S3 request ID, and the tenant sees "your export failed — contact support with reference
`{jobId}`".

## `AgentRun` — nondeterministic, tiered, and partial

### The controlling facts

| Fact | Consequence |
| ---- | ----------- |
| The LLM provider is **nondeterministic** | The same input can fail differently; error identity comes from codes, not stacks |
| The provider rate-limits aggressively | `429` must be handled with `Retry-After` and a budget |
| Tool calls can **write data** | A tool write is T3; a summary is T1 |
| A run can fail **midway** | Partial completion needs explicit states |
| The model may emit **invalid output** | Schema failures are permanent — retrying gives the same invalid output |

### The shape

```ts
export type AgentRunError =
  | { code: "AGENT_PROVIDER_RATE_LIMITED"; retryAfterSeconds: number; retryable: true }
  | { code: "AGENT_PROVIDER_UNAVAILABLE"; retryable: true }
  | { code: "AGENT_TOKEN_LIMIT_EXCEEDED"; used: number; limit: number; retryable: false }
  | { code: "AGENT_OUTPUT_SCHEMA_INVALID"; toolName: string; retryable: false }
  | { code: "AGENT_TOOL_ARGS_INVALID"; toolName: string; retryable: false }
  | { code: "AGENT_TOOL_TIMEOUT"; toolName: string; retryable: true }
  | { code: "AGENT_TOOL_FAILED"; toolName: string; retryable: false }
  | { code: "AGENT_BUDGET_EXCEEDED"; spentUsd: number; limitUsd: number; retryable: false };
```

### Step-level tiering inside one run

```text
  AGENT_PROVIDER_RATE_LIMITED  → T1 (cosmetic-ish)  → degrade or retry within budget
  AGENT_OUTPUT_SCHEMA_INVALID  → T1                 → fail this step, keep prior steps
  AGENT_TOOL_ARGS_INVALID      → T1                 → fail this step (never retry)
  AGENT_TOKEN_LIMIT_EXCEEDED   → T1                 → fail with a clear message
  AGENT_TOOL_FAILED (a write)  → T3                 → compensate the partial write, page
```

That last row is where a run-level tier would have been wrong. The run as a whole is T1 (a
summary is a nicety), but a *tool that writes to the database* is T3 inside that run. This is
why 56.18 says to tier the **operation**, not the feature.

### Retry with a budget, not a count

An `AgentRun` may make up to 12 provider calls. If each call retries 3× with no global
budget, one run can issue 36 provider requests — which is how a run loop turns a provider
rate-limit into a self-inflicted denial.

```ts
const budget = new ProviderBudget({ maxRequests: 20, maxRetries: 5, deadlineMs: 30_000 });

// Retry only while the budget allows it.
if (!budget.canRetry()) {
  throw new AgentRunError({ code: "AGENT_BUDGET_EXCEEDED", spentUsd: budget.spent(),
                            limitUsd: budget.limitUsd(), retryable: false });
}
```

A `429` from the provider also carries `Retry-After`, which Acme honors (capped at 60 s)
rather than using its own backoff — the provider knows its own capacity.

## What the three flows teach

| Lesson | Where it shows up |
| ------ | ----------------- |
| The **caller** decides the shape | `Checkout` returns a result; the worker throws into a runner; the transport catches once |
| The **tier** decides the policy | `Checkout` charge = T3 (no degrade); `AgentRun` summary = T1 (degrade) |
| The **effect** decides retry vs compensation | `Checkout` charge happened → refund; `ExportJob` object written → keep it |
| The **boundary** decides where the fallback lives | Route vs job runner vs feature boundary |
| The **shape** of the union differs by failure set | 8 variants for checkout, 7 for export, 8 for the agent — but different codes |

## Key data / numbers

| Item | `Checkout` | `ExportJob` | `AgentRun` |
| ---- | ---------- | ----------- | ---------- |
| Max retry attempts | 3 | 2–5 (per stage) | Within a 20-request / 5-retry budget |
| Retry deadline | 30 s | Per stage, not per job | 30 s per provider call |
| Max provider requests per run | n/a | n/a | 20 (12 calls + 8 retries) |
| DLQ | n/a | After 5 upload attempts | n/a (run fails, user retries) |
| `Retry-After` honored | Up to 60 s | Up to 60 s | Up to 60 s, provider-supplied |
| Idempotency key required | Yes (all T3 writes) | Yes (record write, S3 key) | Yes (tool writes) |
| Degradation allowed | Email only (T1) | No | Summary only (T1) |
| Compensation window | 24 h | Until the next attempt | Until the run's transaction ends |
| Preserved vendor IDs | Stripe `request_id` | S3 request ID | Provider `request_id` |
| Terminal states | 3 (`done`, `failed`, `unknown`) | 8 (job state machine) | 4 (`completed`, `degraded`, `failed`, `cancelled`) |

## Real-world use case — `AgentRun` during a provider incident

During a provider rate-limit incident, Acme's `AgentRun` began hammering the provider because
each provider call retried 3× with a local backoff, ignoring the provider's `Retry-After`.
The result: 8× the normal provider traffic, and the provider's recovery was delayed by
Acme's own retries.

The fix applied the matrix rather than a new mechanism:

1. **Tier it** (56.18): `AGENT_PROVIDER_RATE_LIMITED` is T1 → the run *degrades* (no summary)
   rather than retrying hard.
2. **Budget it** (56.5): retries are drawn from a per-run budget of 20 requests / 5 retries.
3. **Honor the server** (56.5): `Retry-After` from the provider wins over the local backoff.
4. **Preserve** (56.8): the provider's `request_id` is stored, so support can match Acme's
   traffic to the provider's rate-limit events.

Measured outcome: Acme's provider traffic during the incident dropped from 8× baseline to
1.4×, the provider recovered 3 hours sooner, and Acme's own summary success rate (measured
as "not degraded") went from 11% to 68% because the run stopped wasting its budget on
requests the provider had already refused.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Re-run the matrix for each flow and record the answers | Copy one flow's design to another |
| Tier each **operation**, including tool calls inside a run | Tier the whole feature |
| Bound retries with a **budget** for long or multi-call flows | Give each call its own retry count |
| Honor the server's `Retry-After` over your own backoff | Ignore `Retry-After` and use a local schedule |
| Choose compensation by asking "did the effect happen?" | Compensate because the flow "failed" |

## Checklist

- [ ] Each flow has its own decision record, with the differing answers highlighted.
- [ ] Tiers are assigned per operation, including sub-operations (tool calls, stages).
- [ ] Long or multi-call flows use a retry **budget**, not a per-call count.
- [ ] `Retry-After` from the provider is honored, capped locally.
- [ ] Partial completion has explicit terminal states.
- [ ] The DLQ is used for jobs and only for jobs.

## Related

- [Checkout Decision Walkthrough](./01-checkout-decision-walkthrough.md)
- [Structure and Ownership](../01-concepts/02-structure-and-ownership.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Application Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
