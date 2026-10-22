# Enumerating Failure Points and Failure Modes (52.1–52.2)

> Part XX · Chapter 52 · Sections 52.1–52.2 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 5 — Error Categories in Detail](../../../part-02-error-taxonomy/05-error-categories-in-detail/README.md)

## In one sentence

A **failure point** is a place where control can leave the happy path, and a **failure mode** is
the specific way it can leave — enumerating both is the first half of failure-path analysis.

## Why this matters in production

Teams find bugs by thinking about what could go wrong, which is exactly backwards: you find them by
thinking about **where the code could go wrong**, and that list is finite and checkable.

The difference is measurable. A flow with **12 failure points** has, conservatively, **20–40
distinct failure modes**. A team that reviews "the error handling" in the abstract will find 3–4
of them. A team that walks the failure-point list finds 15–25. The remaining ones are the ones that
page you at 3 a.m.

## Core concept

### What counts as a failure point

A failure point is **any place where the program can stop, diverge, or produce something other
than the expected result**. Five kinds:

| Kind | Example | Why it matters |
| ---- | ------- | -------------- |
| **Effect** | A DB write, a Stripe charge, an email send | A failure here leaves a *partial* state |
| **Decision** | An authorization check, a state-transition guard | A failure here means the wrong action was allowed |
| **Boundary** | An HTTP response, a queue ack, a webhook reply | A failure here is *visible* to the outside world |
| **Wait** | An `await`, a lock acquisition, a queue poll | A failure here is a timeout or a hang |
| **Interpretation** | JSON parse, schema validation, config load | A failure here means garbage in, garbage out |

> A common mistake is to enumerate only *effects*. Decision and interpretation points are where
> **security** and **data quality** failures live, and they are cheap to enumerate.

### The failure-mode guide words

For each failure point, run a fixed list of "guide words" — borrowed from hazard analysis — to
generate modes mechanically instead of by inspiration.

| Guide word | Question | Typical mode |
| ---------- | -------- | ------------ |
| **None** | What if it does not happen at all? | The event never arrives; the job is never scheduled |
| **Late** | What if it arrives late? | Timeout after the effect; stale state read |
| **Early** | What if it arrives early? | Event processed before its predecessor; clock skew |
| **More** | What if there are more than expected? | Duplicate delivery; fan-out amplification |
| **Less** | What if there are fewer? | Partial batch; missing pages |
| **Wrong** | What if the content is wrong? | Provider returns `200` with garbage; wrong tenant id |
| **Partial** | What if only part completes? | Half-written file; 3 of 5 steps committed |
| **Lost** | What if it never arrives? | Dropped queue message; lost ack |
| **Duplicated** | What if it arrives twice? | Two workers, same job |
| **Reversed** | What if order is inverted? | Out-of-order events; refund before charge |
| **Corrupted** | What if the stored form is damaged? | Truncated JSON; half-written row |
| **Hung** | What if it never returns? | Deadlock; infinite await; deadlock on a lock |

Twelve guide words × N failure points is the raw enumeration. You will prune it in step 3 (mapping
to categories) — the guide words are there to make sure you *do not miss one*, not to produce
duplicate rows.

## How it works (mechanics)

### Step 1 — Walk the operation and number the points

```ts
// Checkout: the numbered failure points, in execution order.
export const CHECKOUT_FAILURE_POINTS = [
  { id: "FP-01", kind: "decision",  where: "authenticate",          note: "token verify" },
  { id: "FP-02", kind: "decision",  where: "validateBody",         note: "schema + fields" },
  { id: "FP-03", kind: "effect",    where: "insertAttempt",        note: "postgres insert" },
  { id: "FP-04", kind: "wait",      where: "chargeStripe",         note: "external call" },
  { id: "FP-05", kind: "effect",    where: "insertSubscription",   note: "postgres insert" },
  { id: "FP-06", kind: "effect",    where: "insertEntitlement",    note: "postgres insert" },
  { id: "FP-07", kind: "effect",    where: "insertOutboxEvent",    note: "postgres insert" },
  { id: "FP-08", kind: "boundary",  where: "publishEvent",         note: "queue publish" },
  { id: "FP-09", kind: "effect",    where: "sendReceiptEmail",     note: "email provider" },
  { id: "FP-10", kind: "boundary",  where: "respond201",           note: "http response" },
] as const;
```

A good failure-point list has **8–15 entries for a typical request flow**. More than 20 means you
listed implementation details; fewer than 8 means you probably skipped the decision and
interpretation points.

### Step 2 — Generate modes per point

```text
FP-04 (wait: chargeStripe)
  ├─ throws (provider error 4xx/5xx)
  ├─ times out (deadline exceeded)
  ├─ hangs (no response, connection open)
  ├─ succeeds but the response is lost        ← the dangerous one
  ├─ succeeds with a wrong/invalid payload    ← the dangerous one
  └─ is called twice (retry of the whole flow)
```

Two modes deserve special attention because they are the ones that cause silent damage:

- **Success with a lost response.** The provider did the work; you did not hear about it. This is
  the seed of every duplicate-effect bug.
- **Success with invalid data.** The provider returned `200` with an empty or malformed body. The
  system believes it succeeded and writes garbage.

### Step 3 — Prune by equivalence

Modes that map to the same category **and** the same recovery collapse into one row. Keep the mode
that is cheapest to detect, but keep the *note* about the others.

| Modes | Category | Recovery |
| ----- | -------- | -------- |
| 4xx from provider · timeout · 5xx · hang | `external_api_transient` | Retry with backoff (bounded) |
| Success-but-lost · success-but-invalid | `external_api_ambiguous` | Read-back / resolve, **never blind retry** |

> Pruning by category-and-recovery is what keeps the matrix finite. Pruning by *what you think will
> never happen* is how you end up with a matrix full of holes.

### A checklist that works

| Check | Failure points you would otherwise miss |
| ----- | -------------------------------------- |
| Every `await` on a remote resource | Hang, timeout, lost response |
| Every `try/catch` | The modes your catch handles — and the ones it does not |
| Every state transition | Illegal transitions, and the "guard check" itself |
| Every `parse` / `JSON.parse` | Malformed, truncated, empty, wrong-shape |
| Every queue publish / ack | Publish failure, ack lost, duplicate delivery |
| Every read of config/env | Missing key, wrong type, stale value |
| Every external side effect | Success-with-lost-response, success-with-wrong-data |
| The boundaries themselves | Response write failure, serialisation failure |

## Worked example — `ExportJob` (Acme SaaS)

```text
ExportJob (queue worker)
  FP-01 read job payload          interpretation  → malformed JSON, missing fields
  FP-02 claim job (lease)         effect/wait     → lease held by another worker, DB slow
  FP-03 query rows                wait            → timeout, pool exhausted, replica lag
  FP-04 render CSV                effect          → OOM on huge row, encoding error
  FP-05 upload to S3              wait/effect     → timeout, partial upload, lost response
  FP-06 mark job done             effect          → DB down
  FP-07 publish notification      boundary        → broker down
  FP-08 delete temp file          effect          → permission error
```

Each point has its own mode list. Two that the original code never considered:

- **FP-05 partial upload**: a multipart upload interrupted at 60%. The object exists but is
  incomplete, and the customer gets a truncated CSV from a "successful" export.
- **FP-08 delete temp file fails**: harmless-looking, but the temp bucket fills, and the cleanup job
  that assumes "delete succeeded" stops cleaning.

## Key data / numbers

- **Failure points per request flow: 8–15**; per background job: **10–20**.
- **Guide words: 12** — the standard set for generating modes.
- **Raw enumeration size**: 12 modes × 12 points ≈ **144 cells** before pruning; typically **20–40
  distinct rows** survive.
- **Pruning rule**: collapse when category *and* recovery match. Expect **50–70% reduction**.
- **Enumeration time**: **30 minutes** per flow for the first pass, 10 minutes for a flow you have
  analysed before (the point list is reusable; only the policies change).
- **Points people miss most often**: the response boundary (10%), the "success but lost" mode (10%),
  and the parse/interpretation points (8%).

## Real-world use case — Acme SaaS `AgentRun`

`AgentRun` is an LLM tool-calling agent, so its failure points are unusual: the model is a
dependency whose output is **probabilistic**, and the tools are **side effects**.

```text
AgentRun
  FP-01 load prompt + tool catalog     interpretation → tool schema drift after a deploy
  FP-02 call the LLM provider          wait          → 429, timeout, invalid tool JSON
  FP-03 parse the tool call            interpretation → malformed arguments, unknown tool
  FP-04 authorize the tool call        decision      → policy service down (fail open or closed?)
  FP-05 execute the tool               effect        → tool succeeded, response lost
  FP-06 append the tool result         effect        → DB write failed after the tool ran
  FP-07 loop back to the provider      decision      → token limit reached mid-loop
  FP-08 emit the final answer          boundary      → stream broken mid-sentence
```

The mode list surfaced a gap the team had never considered: **FP-05 success-but-lost**. The tool
sent an email, the HTTP response to Acme timed out, and the agent's retry sent the email again.
The fix was to make every side-effecting tool require an `idempotencyKey` derived from
`(runId, toolCallIndex)` — 51.9 in action — and to treat a lost response as `unknown` rather than
as a failure.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Manual walk of the code | Fast, sees intent | Depends on the author's care | Small flows, first analysis |
| Guide-word enumeration | Systematic, finds the forgotten | Verbose; many irrelevant modes | Every flow that matters |
| Static analysis / coverage tools | Finds untested lines | Finds lines, not failure paths | Supporting evidence, not the method |
| Architecture-derived points | From your own diagrams | Diagrams lie | Use the diagram as a checklist, not as truth |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Number the failure points and keep the list in the repo | Redo the enumeration from scratch each quarter |
| Include decision and interpretation points | Enumerate only writes and calls |
| Always ask "what if it succeeded but we did not hear?" | Only consider "it failed" |
| Prune by category *and* recovery | Prune by "that will never happen" |
| Reuse the point list when policies change | Treat the matrix as a one-time document |

## Common mistakes

- **Enumerating libraries, not your code.** "Stripe could fail" is not a failure point; "the
  `chargeStripe` await" is.
- **Missing the response boundary.** The failure to *write* the response is a real failure point
  and a frequent cause of hanging requests.
- **Ignoring time.** A failure point has a time dimension: before, during, or after the effect.
  "After" is where the ambiguous outcomes live (52.12).
- **Stopping at the happy path.** If your list has fewer than 8 points, you have described the
  happy path, not the operation.

## Checklist

- [ ] Every failure point has an id, a kind, and a location.
- [ ] Decision and interpretation points are included.
- [ ] Each point has at least the modes: throw, timeout, hang.
- [ ] Irreversible points additionally have: lost response, wrong data, duplicate.
- [ ] The point list is stored in the repository, next to the code it describes.
- [ ] Raw modes are pruned only when category *and* recovery match.

## Related

- [Mapping Modes to Categories and Recovery (52.3–52.4)](./02-mapping-modes-to-categories-and-recovery.md)
- [Failure-Path Analysis of the Checkout Flow](../03-practical-examples/01-checkout-failure-path-analysis.md)
- Chapter 58 — Less Obvious Error-Handling Scenarios (planned)
- [Glossary](../../../GLOSSARY.md)
