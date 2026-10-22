# Retry Safety and Nondeterminism

> Part XVI · Chapter 44 · Sections 44.13, 44.14 · _Estimated reading time: 28 min_
> **Prerequisite:** [Agent Loop Failures and Recovery](../01-concepts/04-agent-loop-failures-and-recovery.md)

## In one sentence

Retrying an agent is safe only when the **plan is frozen and every effect is
idempotent** — because the same request is free to produce a **different plan** on the
retry, which is how one transient error becomes two emails.

## Why this matters in production

Retrying a model call feels safe because a model call has no side effect. That is true of
the *call* and false of the *run*: the call is one step in a loop whose steps call your
tools, and your tools write to the world.

The failure is subtle because the retry usually "works". The provider returned a 503, you
retried, and the run completed — successfully, and with a duplicate notification. The
provider error is gone from the log, so the incident looks like a "harmless transient
error", and the duplicate is discovered days later by a customer. Every piece of evidence
points away from the cause.

## The three retry planes

| Plane | What is retried | Safe when | Unsafe when |
| ----- | --------------- | --------- | ------------ |
| **Provider call** | The same messages + tools | No tool ran since the last attempt, or the call is read-only | The model can choose a different tool this time |
| **Tool call** | The same tool + arguments | The tool is idempotent or has an idempotency key | The tool writes and has no key |
| **Whole run** | Everything from step 1 | Every effect is idempotent and the plan is frozen | Any write happened along the way |

The mistake is treating them as one thing. "We retry on 503" is ambiguous until you say
**which** plane.

## Why "just retry the same request" is unsafe

```text
attempt 1:  model → "search_docs(q='refund')"  → tool → 200 OK → provider 503 (timeout)
attempt 2:  model → "search_docs(q='refund policy 2024')"  → tool → 200 OK
            → model → "send_email(to='ops@…')"  → tool → email sent
            → provider 503 (timeout)

result: one email sent... but the retried plan also reached a write.
```

Attempt 2 was not a retry of attempt 1 — it was a **new plan**. The provider error only
looks like the trigger; the real trigger was the model being allowed to replan after a
failure that occurred *after* an effect.

> ⚠️ **Hazard.** The dangerous retry is not the one that repeats the same tool call. It is
> the one that re-enters the **planning** step after a side effect. Guard the boundary
> between "plan" and "execute": once a write has happened, the plan for the rest of the run
> must be **resumed, not regenerated**.

### The freeze boundary

```text
        plan ──────────────── execute ──────────────── observe
     (model decides)      (tools run)               (results come back)
         ▲
         └── only re-enter here if NO write has happened yet
```

```ts
export function mayReplan(run: AgentRun): boolean {
  // If any completed step had a side effect, the plan is now load-bearing.
  return !run.executedSteps.some((s) => s.sideEffects === "write");
}
```

**Key data:** the freeze boundary is the moment the **first mutating tool** succeeds.
Before it, re-planning is safe and often better. After it, re-planning can duplicate the
effect. This one rule prevents most duplicate-side-effect incidents.

## Nondeterminism: where the variation comes from

| Source | Frequency | Observable? | Controllable? |
| ------ | --------- | ----------- | ------------- |
| Sampling (`temperature > 0`) | Every request | Wording differs | Partially — lower the temperature |
| Model version drift (same name, new weights) | Weekly-ish | Behaviour changes | ❌ — pin the version |
| Provider infrastructure | Rare | Occasional flakiness | ❌ |
| Tool schema/description change | On deploy | Different tool chosen | ✅ — version and log |
| Retrieved context changes | Always | Different facts | ✅ — log the ids |
| Tool result ordering / non-determinism | Rare | Different ordering | ✅ — sort deterministically |
| Floating-point / backend nondeterminism | Rare | Tiny differences | ❌ |

### `temperature: 0` is not determinism

Greedy sampling removes the biggest source of variation, not all of it. Two requests with
`temperature: 0` can still differ because the provider changed the model, the tool
descriptions changed, the retrieved chunks differ, or the infrastructure is not
bit-identical. Building an invariant on identical outputs is building on sand.

```ts
// What you CAN rely on, even at temperature 0:
export type ReliableInvariants = {
  schemaConformance: boolean;      // with schema mode
  toolArgumentShape: boolean;      // with strict schemas
  finishReasonIn: Set<FinishReason>;
};
// What you CANNOT:
//   "the same prompt produces the same tool sequence"
//   "the same prompt produces the same wording"
//   "a model that agreed yesterday agrees today"
```

**Key data:** `temperature: 0` plus a **pinned model version** plus a **frozen tool
schema** plus a **fixed context** gets you close to reproducible — but the guarantee that
actually matters is at the *effect* layer, not the text layer: the same input produces the
same **database state**, because the state is written by your code, not by the model.

### Pinning model versions

Provider model names are often aliases that float. If `acme-large-1` silently changes,
your regression suite keeps passing (it tests the alias) while behaviour drifts.

```ts
export type ModelRef = {
  alias: string;        // "acme-large"
  version: string;      // "2026-03-14" — pinned
  region?: string;
};

export const MODELS = {
  primary:   { alias: "acme-large", version: "2026-03-14", region: "us-east-1" },
  fallback:  { alias: "acme-medium", version: "2026-02-02", region: "us-east-1" },
  cheap:     { alias: "acme-small", version: "2026-02-02", region: "us-east-1" },
} as const;
```

**Key data:** pin **both** the alias and the version, and log both. A version rollback
should be a one-line change plus a deploy, not an archaeology exercise.

## The retry budget is per-run, not per-call

This is the most common structural bug: every layer has its own retry policy, and they
multiply.

```text
provider adapter:  3 attempts
  └─ agent loop:   3 attempts
       └─ tool runner: 3 attempts
            └─ total worst case: 27 executions of one side effect
```

```ts
export type RetryBudget = {
  maxProviderAttempts: number;   // 3
  maxToolAttempts: number;       // 2
  maxRunAttempts: number;        // 1  — a run is NOT re-planned
  deadlineMs: number;            // 120_000
};

export class BudgetExhausted extends Error {}
```

**Key data:** one retry budget per run, threaded through every layer. A run is retried at
most once, and only if **no write has been applied**. Nested retries without a shared
budget multiply into exponential request volume — which is exactly what a provider
overload does not need.

## Debugging a nondeterministic failure

You cannot debug "it worked yesterday". You can debug a **replay**.

```ts
export type RunRecord = {
  runId: string;
  fingerprint: {
    model: string;            // alias + version
    temperature: number;
    toolSchemaHash: string;
    retrievedIds: string[];
    promptHash: string;
  };
  steps: Array<{
    index: number;
    toolName: string;
    argsHash: string;
    resultHash: string;
    sideEffects: "none" | "read" | "write";
    idempotencyKey?: string;
  }>;
};

export function replayable(record: RunRecord): boolean {
  return record.fingerprint.toolSchemaHash.length > 0
      && record.steps.every((s) => s.argsHash.length > 0);
}
```

The five fingerprint fields are the minimum for reconstruction:

| Field | Without it |
| ----- | ---------- |
| Model alias **+ version** | You cannot tell a provider change from your bug |
| Temperature | A different sample is a different plan |
| Tool schema hash | You cannot tell a tool contract change from nondeterminism |
| Retrieved document ids | You cannot tell a stale index from a model failure |
| Prompt hash | You cannot tell a prompt change from noise |

**Key data:** store **hashes** of arguments and results (not the full payloads) so the
record is small, and keep the full payloads for a sampled subset of runs. A run record
without a fingerprint is a transcript, and transcripts do not reproduce bugs.

## Real-world use case — the research agent that emailed twice

Acme's `AgentRun` research agent searches the knowledge base, reads documents, and posts
a summary to a shared channel. A provider `503` after the summary was posted produced two
identical posts — and no error anywhere, because the retry eventually succeeded.

The trace explained it. The first attempt ran `search_docs`, then `read_doc`, then
`post_summary`, and only then hit the `503`. The retry re-entered the **planning** step:
the model re-read the transcript, produced a slightly different plan, and reached
`post_summary` again. Same key derivation, same business object, second post.

Three changes stopped it:

1. **The freeze boundary.** Once `post_summary` succeeded, the run could no longer
   re-plan; the retry resumed from the recorded effect and returned the stored result.
2. **The effect ledger.** `post_summary` derives its key from
   `sha256("acme:post_summary:" + channelId + ":" + sourceDocIds)`, so a re-plan that
   changed the wording but not the channel and documents still hits the same key.
3. **One shared retry budget.** The provider adapter's 3 attempts and the loop's 3
   attempts were multiplied into 9 provider calls per failure. The budget is now per run,
   so the worst case is 3.

The team also added the run fingerprint after a separate incident — a user reported the
agent summarizing the wrong document, and the logs could not distinguish a stale index
from a model change. With the embedding model version, the retrieved document ids, and
the tool schema hash in the record, the cause turned out to be a provider-side model
update that changed retrieval behaviour.

## Key data

| Fact | Value |
| ---- | ----- |
| Retry planes | provider call · tool call · whole run — name them separately |
| Safe provider retry | Only when no tool ran since the last attempt |
| Safe tool retry | Only with an idempotency key |
| Safe run retry | Only if every effect is idempotent |
| Freeze boundary | The first successful mutating tool |
| Retry budget | One per run: 3 provider attempts, 2 tool attempts, 1 run attempt |
| Nested retries | 3 × 3 × 3 = 27 executions — the reason a shared budget exists |
| `temperature: 0` | Reduces sampling variation; it is **not** determinism |
| Model pinning | Pin alias **and** version (`acme-large-2026-03`) |
| Reproducibility log | model version, temperature, tool schema hash, retrieved ids, prompt hash |
| Repetition signature | Tool name + canonicalized arguments, 3 in a row |
| Assorted limits | 12 model turns · 20 tool calls · 120 s deadline · 120k tokens per run |

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Retry the whole run | Simple | Duplicates every effect | Only if all effects are idempotent |
| Retry the provider call only | Cheap | The model may replan | ✅ Read-only calls |
| Freeze the plan after the first write | No duplicate effects | Less adaptive | ✅ Any run with writes |
| Idempotency key on every write | Survives any retry | Extra storage and code | ✅ Always |
| `temperature: 0` | Reduces variation | Not determinism | ✅ Always, as a floor |
| Pin model versions | Reproducible | Versions age out | ✅ Always |
| Retry budget shared per run | Bounds amplification | Requires plumbing | ✅ Always |
| Record-and-replay | Debuggable | Storage and privacy cost | ✅ For paid/failed runs |
| Assert on text equality | Simple | Fails constantly | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Distinguish provider-call, tool-call, and run retries | Say "we retry on 503" |
| Freeze the plan once a mutating tool has succeeded | Re-plan after a write |
| Give every write an idempotency key | Rely on "the model probably won't" |
| Share one retry budget across the whole run | Let each layer retry independently |
| Pin the model alias **and** version | Track only the alias |
| Log the five fingerprint fields | Log only the prompt |
| Assert on effects, not on text | Assert on identical model output |
| Treat `temperature: 0` as a reduction, not a guarantee | Claim determinism |
| Replay the transcript to reproduce | Try to reproduce from the prompt alone |

## Common mistakes

- **Re-entering the planning step after an effect.** The classic duplicate-email cause.
- **Nested retries without a shared budget.** 3 × 3 × 3 = 27 executions.
- **Asserting on model wording.** The test fails randomly and gets deleted.
- **Logging the model alias only.** A provider update looks like a mystery.
- **Treating a timeout as "nothing happened".** The effect may have been applied.
- **Retrying with a fresh context.** A fresh context re-plans from scratch.
- **Storing full transcripts for every run.** Cost and privacy, with no fingerprint to
  make them useful.

## Checklist

- [ ] The three retry planes are named separately in your code and your runbooks.
- [ ] The plan is frozen once a mutating tool succeeds.
- [ ] Every mutating tool has an idempotency key derived from the business operation.
- [ ] One retry budget per run, threaded through every layer.
- [ ] Model alias and version are both pinned and both logged.
- [ ] The five fingerprint fields are recorded per run.
- [ ] Tests assert on effects and on the tool-call sequence, not on prose.
- [ ] Timeouts are treated as ambiguous outcomes, and their effects are reconciled.
- [ ] Failed and paid runs keep a replayable record.

## Related

- [Agent Loop Failures and Recovery](../01-concepts/04-agent-loop-failures-and-recovery.md)
- [Duplicate Side Effects During Agent Retries](./02-duplicate-side-effects-during-agent-retries.md)
- [Chapter 28 — Idempotency and Duplicate Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 44 Reference](../05-reference/README.md)
